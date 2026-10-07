"""Radar tren mingguan: Google Trends utk niche Katalog B Store. 0 token Muse."""
import json, os, datetime, time
from pytrends.request import TrendReq

GROUPS = {
    "kids_printables": ["coloring book printable", "coloring pages for kids", "busy book printable"],
    "planners": ["printable planner", "budget planner printable", "daily planner pdf"],
    "islamic_kids": ["hijaiyah", "arabic alphabet for kids", "islamic coloring book"],
}
GEOS = ["US", "ID"]
out = {"date": datetime.date.today().isoformat(), "groups": {}}
py = TrendReq(hl="en-US", tz=420, timeout=(10, 25))
for gname, kws in GROUPS.items():
    out["groups"][gname] = {}
    for geo in GEOS:
        try:
            py.build_payload(kws, timeframe="today 12-m", geo=geo)
            df = py.interest_over_time()
            time.sleep(2)
            stats = {}
            for k in kws:
                if k in df.columns:
                    s = df[k]
                    first, last = float(s.head(8).mean()), float(s.tail(8).mean())
                    stats[k] = {"avg": round(float(s.mean()), 1),
                                "arah": "naik" if last > first * 1.25 else ("turun" if last < first * 0.75 else "datar")}
            out["groups"][gname][geo] = stats
        except Exception as e:
            out["groups"][gname][geo] = {"error": str(e)[:120]}
os.makedirs("data", exist_ok=True)
p = f"data/trends_{out['date']}.json"
json.dump(out, open(p, "w"), indent=1)
print("OK ->", p)
