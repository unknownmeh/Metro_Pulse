"""
generate_timetable_fleet.py
Reads Excel file 'ERRA BUS ROUTE INFORMATION.xlsx', extracts all departure times from PNBS for City and Suburban Metro routes,
maps them to ROUTES_DATABASE in index.html, and generates:
1. window.PNBS_TIMETABLE dictionary containing real departure schedules
2. Python calculation functions to test and estimate real-time bus locations along road waypoints
3. JS schedule simulation engine that computes real-time active buses from real departure timestamps
"""
import openpyxl, re, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

wb = openpyxl.load_workbook(r'c:\Users\adity\Desktop\Personal Projects\ERRA BUS\ERRA BUS ROUTE INFORMATION.xlsx', data_only=True)

timetable = {}

for sheet in wb.sheetnames:
    ws = wb[sheet]
    default_cat = 'City' if 'CITY' in sheet else 'Suburban'
    for r in range(2, ws.max_row + 1):
        code = str(ws.cell(row=r, column=1).value or '').strip()
        od = str(ws.cell(row=r, column=2).value or '').strip()
        dep_cell = str(ws.cell(row=r, column=4).value or '').strip()
        if not code or code == 'None': continue
        if dep_cell and dep_cell != 'None':
            # Extract times like 06:00, 13:10, 03:35 etc.
            raw_times = re.findall(r'\b\d{1,2}:\d{2}\b', dep_cell)
            if raw_times:
                # normalize to HH:MM format
                norm_times = []
                for t in raw_times:
                    parts = t.split(':')
                    hh = int(parts[0])
                    mm = int(parts[1])
                    norm_times.append(f"{hh:02d}:{mm:02d}")
                # remove duplicates while preserving order
                seen = set()
                dedup = [x for x in norm_times if not (x in seen or seen.add(x))]
                timetable[code] = {
                    'category': default_cat,
                    'od': od,
                    'departures': dedup
                }

print(f"Extracted timetables for {len(timetable)} routes:")
total_trips = sum(len(v['departures']) for v in timetable.values())
print(f"Total scheduled departures: {total_trips}")
for code, d in sorted(timetable.items()):
    print(f"  Route {code:6s} ({d['category']}): {len(d['departures']):2d} trips -> {', '.join(d['departures'][:6])}{'...' if len(d['departures'])>6 else ''}")

# Save JSON representation
with open(r'c:\Users\adity\Desktop\Personal Projects\ERRA BUS\timetable_data.json', 'w', encoding='utf-8') as f:
    json.dump(timetable, f, indent=2, ensure_ascii=False)
print("Saved timetable_data.json")
