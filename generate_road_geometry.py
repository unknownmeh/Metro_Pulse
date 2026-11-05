"""Generate route-specific road paths from the ordered stop sequences in index.html."""

import json
import pathlib
import re
import time
import threading
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed


ROOT = pathlib.Path(__file__).resolve().parent
HTML_PATH = ROOT / "index.html"
OUTPUT_PATH = ROOT / "route_road_geometry.js"
OSRM_BASE = "https://router.project-osrm.org/route/v1/driving/"
REQUEST_INTERVAL_SECONDS = 0.4
_request_lock = threading.Lock()
_next_request_at = 0.0


def extract_object(source: str, assignment: str, next_assignment: str) -> dict:
    start = source.index(assignment)
    start = source.index("{", start)
    end = source.index(next_assignment, start)
    raw = source[start:end].strip()
    if raw.endswith(";"):
        raw = raw[:-1].rstrip()
    raw = re.sub(r"/\*.*?\*/", "", raw, flags=re.DOTALL)
    return json.loads(raw)


def leg_points(leg: dict) -> list[list[float]]:
    coordinates = []
    for step in leg.get("steps", []):
        coordinates.extend(step.get("geometry", {}).get("coordinates", []))
    if not coordinates:
        coordinates = leg.get("geometry", {}).get("coordinates", [])

    points = []
    for longitude, latitude in coordinates:
        point = [round(latitude, 6), round(longitude, 6)]
        if not points or point != points[-1]:
            points.append(point)
    if len(points) == 1:
        points.append(points[0].copy())
    return points


def fetch_route_geometry(route_code: str, route: dict, stops: dict) -> list[list[list[float]]]:
    stop_ids = route.get("stops", [])
    coordinates = []
    for stop_id in stop_ids:
        stop = stops.get(stop_id)
        if not stop:
            raise ValueError(f"Route {route_code}: stop {stop_id!r} has no coordinates")
        coordinates.append(f"{stop['lng']:.6f},{stop['lat']:.6f}")

    coordinate_path = urllib.parse.quote(";".join(coordinates), safe=",;")
    query = urllib.parse.urlencode({
        "steps": "true",
        "overview": "false",
        "geometries": "geojson",
    })
    url = f"{OSRM_BASE}{coordinate_path}?{query}"
    payload = None
    for attempt in range(3):
        global _next_request_at
        with _request_lock:
            wait = _next_request_at - time.monotonic()
            if wait > 0:
                time.sleep(wait)
            _next_request_at = time.monotonic() + REQUEST_INTERVAL_SECONDS
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "MetroPulse route geometry builder/1.0", "Accept": "application/json"},
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                payload = json.load(response)
            break
        except Exception:
            if attempt == 2:
                raise
            time.sleep(1.5 * (attempt + 1))

    if payload.get("code") != "Ok" or not payload.get("routes"):
        raise ValueError(f"Route {route_code}: OSRM returned {payload.get('code', 'no route')}")

    legs = payload["routes"][0].get("legs", [])
    if len(legs) != len(stop_ids) - 1:
        raise ValueError(f"Route {route_code}: expected {len(stop_ids) - 1} legs, received {len(legs)}")

    geometry = [leg_points(leg) for leg in legs]
    for index, points in enumerate(geometry):
        if len(points) < 2:
            raise ValueError(f"Route {route_code}: road geometry missing for stop segment {index + 1}")
    return geometry


def load_existing_geometry() -> dict:
    if not OUTPUT_PATH.exists():
        return {}
    try:
        source = OUTPUT_PATH.read_text(encoding="utf-8")
        raw = source.split("=", 1)[1].strip().rstrip(";").strip()
        if raw.startswith("window."):
            return {}
        value = json.loads(raw)
        return value if isinstance(value, dict) else {}
    except (OSError, IndexError, json.JSONDecodeError):
        return {}


def save_geometry(geometry_by_route: dict) -> None:
    output = "window.ROUTE_ROAD_GEOMETRY = " + json.dumps(
        geometry_by_route, ensure_ascii=False, separators=(",", ":")
    ) + ";\n"
    temporary_path = OUTPUT_PATH.with_suffix(".js.tmp")
    temporary_path.write_text(output, encoding="utf-8")
    temporary_path.replace(OUTPUT_PATH)


def resolve_missing_stops(routes: dict, stops: dict) -> dict:
    missing_ids = sorted({
        stop_id
        for route in routes.values()
        for stop_id in route.get("stops", [])
        if stop_id not in stops
    })
    known_stops = {
        "penamuluru": {
            "name": "Penamaluru X Roads",
            "lat": 16.4712,
            "lng": 80.7201,
        },
        "kasaraneni_vari_palem": {
            "name": "Kasaraneni Vari Palem",
            "lat": 16.41661,
            "lng": 80.71525,
        },
    }
    unresolved = [stop_id for stop_id in missing_ids if stop_id not in known_stops]
    if unresolved:
        raise ValueError(f"No coordinates configured for stops: {', '.join(unresolved)}")
    resolved = {
        stop_id: {
            "id": stop_id,
            **known_stops[stop_id],
            "teName": "",
        }
        for stop_id in missing_ids
    }
    for stop_id, stop in resolved.items():
        print(f"Added missing stop coordinate: {stop['name']} ({stop['lat']}, {stop['lng']})")
    return resolved


def add_stops_to_html(html: str, new_stops: dict) -> str:
    if not new_stops:
        return html
    stop_start = html.index("var STOPS_DATABASE = window.STOPS_DATABASE = ")
    stop_end = html.index("\n};\n\nvar ROUTES_DATABASE", stop_start)
    additions = ",\n".join(
        "  " + json.dumps(stop, ensure_ascii=False, indent=2).replace("\n", "\n  ")
        for stop in new_stops.values()
    )
    return html[:stop_end] + ",\n" + additions + html[stop_end:]


def main() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    stop_text = extract_object(html, "var STOPS_DATABASE = window.STOPS_DATABASE = ", "var ROUTES_DATABASE")
    routes = extract_object(html, "var ROUTES_DATABASE = window.ROUTES_DATABASE = ", "var PNBS_TIMETABLE")
    new_stops = resolve_missing_stops(routes, stop_text)
    stops = {**stop_text, **new_stops}

    if new_stops:
        html = add_stops_to_html(html, new_stops)
        HTML_PATH.write_text(html, encoding="utf-8")

    geometry_by_route = load_existing_geometry()
    route_items = [(code, route) for code, route in routes.items() if len(route.get("stops", [])) >= 2]
    pending = []
    for route_code, route in route_items:
        saved = geometry_by_route.get(route_code)
        expected = len(route.get("stops", [])) - 1
        if not isinstance(saved, list) or len(saved) != expected or any(not isinstance(points, list) or len(points) < 2 for points in saved):
            pending.append((route_code, route))

    print(f"Using {len(route_items) - len(pending)} saved routes; routing {len(pending)} routes from ordered stop lists.", flush=True)
    failures = []
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {
            executor.submit(fetch_route_geometry, route_code, route, stops): route_code
            for route_code, route in pending
        }
        for completed, future in enumerate(as_completed(futures), start=1):
            route_code = futures[future]
            try:
                geometry_by_route[route_code] = future.result()
                save_geometry(geometry_by_route)
                print(f"Routed {route_code} ({completed}/{len(pending)}); {len(geometry_by_route)}/{len(route_items)} routes saved.", flush=True)
            except Exception as error:
                failures.append(route_code)
                print(f"Could not route {route_code}: {error}", flush=True)

    save_geometry(geometry_by_route)
    print(f"Saved road paths for {len(geometry_by_route)}/{len(route_items)} routes to {OUTPUT_PATH.name}.", flush=True)
    if failures:
        print("Routes needing retry: " + ", ".join(failures), flush=True)


if __name__ == "__main__":
    main()
