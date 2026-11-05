import sys, io, re

with open(r'c:\Users\adity\Desktop\Personal Projects\ERRA BUS\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

for c in ['116', '308', '16R', '1']:
    m = re.search(rf'"{c}":\s*\{{(?:[^{{}}]*|\{{[^{{}}]*\}})*\}}', html)
    if m:
        stops = re.findall(r'"stops":\s*\[(.*?)\]', m.group(0), re.DOTALL)
        clean = [s.strip().strip('"') for s in stops[0].split(',') if s.strip()]
        print(f"Route {c} ({len(clean)} stops): {clean}")
