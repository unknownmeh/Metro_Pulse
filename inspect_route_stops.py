import sys, io, re

with open(r'c:\Users\adity\Desktop\Personal Projects\ERRA BUS\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_s = html.find('var STOPS_DATABASE = window.STOPS_DATABASE = {')
end_s = html.find('};\nvar ROUTES_DATABASE', start_s)
stops_block = html[start_s:end_s]

stops = {}
for m in re.finditer(r'"([^"]+)":\s*\{\s*"id":\s*"[^"]*",\s*"name":\s*"([^"]*)",\s*"teName":\s*"([^"]*)",\s*"lat":\s*([\d.-]+),\s*"lng":\s*([\d.-]+)', stops_block):
    k = m.group(1)
    stops[k] = (float(m.group(4)), float(m.group(5)), m.group(2))

for c in ['116', '1', '16R']:
    print(f"\n=== Route {c} Waypoints ===")
    m = re.search(rf'"{c}":\s*\{{(?:[^{{}}]*|\{{[^{{}}]*\}})*\}}', html)
    if m:
        st_match = re.findall(r'"stops":\s*\[(.*?)\]', m.group(0), re.DOTALL)
        clean = [s.strip().strip('"') for s in st_match[0].split(',') if s.strip()]
        for s in clean:
            coord = stops.get(s, (0, 0, 'UNKNOWN'))
            print(f"  {s:20s}: lat={coord[0]:.4f}, lng={coord[1]:.4f} ({coord[2]})")
