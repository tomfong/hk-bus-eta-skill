"""
Hong Kong Bus ETA Query Script
Version: 0.1.1

Changelog:
- 2026-03-12 18:33 (by Agent): When exact match found, only output matched stops (suppress fuzzy matches)
- 2026-03-12 18:33 (by Agent): Added ★ symbol to highlight exact matched stops
- 2026-03-12 18:27 (by Agent): Exact match priority for stop name
- 2026-03-12 18:18 (by Agent): Origin/Terminus labels added
"""

import json
import os
import time
import math
import concurrent.futures
from urllib.request import urlopen, Request
from datetime import datetime, timezone, timedelta

# Configuration
BASE_DIR = "/home/admin/.openclaw/workspace/skills/hk-bus-eta/scripts"
CACHE_FILE_KMB = os.path.join(BASE_DIR, "kmb_stops.json")
CACHE_EXPIRY = 12 * 3600

def get_dist(lat1, lon1, lat2, lon2):
    try:
        R = 6371
        dlat = math.radians(float(lat2) - float(lat1))
        dlon = math.radians(float(lon2) - float(lon1))
        a = math.sin(dlat/2)**2 + math.cos(math.radians(float(lat1))) * math.cos(math.radians(float(lat2))) * math.sin(dlon/2)**2
        return R * 2 * math.asin(math.sqrt(a))
    except: return 9999

def fetch_api(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode())
    except: return None

def get_cached_kmb_stops():
    if os.path.exists(CACHE_FILE_KMB):
        with open(CACHE_FILE_KMB, 'r') as f:
            cache = json.load(f)
        now_ts = time.time()
        if now_ts - cache['ts'] < CACHE_EXPIRY:
            last_dt = datetime.fromtimestamp(cache['ts'], timezone(timedelta(hours=8)))
            now_dt = datetime.fromtimestamp(now_ts, timezone(timedelta(hours=8)))
            if not (now_dt.hour >= 5 and last_dt.day != now_dt.day):
                return {s['stop']: s for s in cache['data']}
    res = fetch_api("https://data.etabus.gov.hk/v1/transport/kmb/stop")
    if res and 'data' in res:
        with open(CACHE_FILE_KMB, 'w') as f:
            json.dump({"ts": time.time(), "data": res['data']}, f)
        return {s['stop']: s for s in res['data']}
    return {}

def fetch_stop_info(op, stop_id):
    url = f"https://data.etabus.gov.hk/v1/transport/kmb/stop/{stop_id}" if op == "kmb" else f"https://rt.data.gov.hk/v2/transport/citybus/stop/{stop_id}"
    res = fetch_api(url)
    return res['data'] if res and 'data' in res else None

def fetch_route_info(op, route):
    op_upper = op.upper()
    url = f"https://data.etabus.gov.hk/v1/transport/kmb/route/{route}/outbound/1" if op == 'kmb' else f"https://rt.data.gov.hk/v2/transport/citybus/route/{op_upper}/{route}"
    res = fetch_api(url)
    return res['data'] if res and 'data' in res else {}

def fetch_route_stops(op, route, bound):
    op_upper = op.upper()
    url = f"https://data.etabus.gov.hk/v1/transport/kmb/route-stop/{route}/{bound}/1" if op == "kmb" else f"https://rt.data.gov.hk/v2/transport/citybus/route-stop/{op_upper}/{route}/{bound}"
    res = fetch_api(url)
    return res['data'] if res and 'data' in res else []

def fetch_eta(op, stop_id, route):
    op_upper = op.upper()
    url = f"https://data.etabus.gov.hk/v1/transport/kmb/eta/{stop_id}/{route}/1" if op == "kmb" else f"https://rt.data.gov.hk/v2/transport/citybus/eta/{op_upper}/{stop_id}/{route}"
    res = fetch_api(url)
    return res['data'] if res and 'data' in res else []

def format_eta(eta_str):
    if not eta_str: return None
    try:
        t = datetime.fromisoformat(eta_str.replace("Z", "+00:00"))
        now = datetime.now(timezone(timedelta(hours=8)))
        diff = int((t - now).total_seconds() / 60)
        return {"str": t.strftime('%H:%M'), "min": diff if diff >= 0 else 0, "ts": t.timestamp()}
    except: return None

def main(route, pattern, u_lat=None, u_lon=None, lang="tc"):
    kmb_stops_dict = get_cached_kmb_stops()
    ops_bounds = [('kmb', 'outbound'), ('kmb', 'inbound'), ('ctb', 'outbound'), ('ctb', 'inbound')]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        rs_results = list(executor.map(lambda x: fetch_route_stops(x[0], route, x[1]), ops_bounds))
    
    max_seqs = {}
    for i, (op, bound) in enumerate(ops_bounds):
        if rs_results[i]: max_seqs[(op, bound)] = max(int(r['seq']) for r in rs_results[i])

    tasks = []
    has_exact_match = False# 2026-03-12 18:33 (by Agent): Track if exact match found
    
    for i, (op, bound) in enumerate(ops_bounds):
        rs = rs_results[i]
        if not rs: continue
        candidates = []
        if op == 'kmb':
            for r in rs:
                s_info = kmb_stops_dict.get(r['stop'])
                if s_info:
                    s = s_info.copy()
                    s['_seq'] = int(r.get('seq', 1))
                    s['_bound'] = bound
                    if u_lat and u_lon: s['_dist'] = get_dist(u_lat, u_lon, s['lat'], s['long'])
                    candidates.append(s)
        else:
            stop_ids = [r['stop'] for r in rs]
            with concurrent.futures.ThreadPoolExecutor() as exec2:
                ctb_infos = list(exec2.map(lambda sid: fetch_stop_info('ctb', sid), stop_ids))
            for idx, sinfo in enumerate(ctb_infos):
                if sinfo:
                    s = sinfo.copy()
                    s['_seq'] = int(rs[idx].get('seq', 1))
                    s['_bound'] = bound
                    if u_lat and u_lon: s['_dist'] = get_dist(u_lat, u_lon, s['lat'], s['long'])
                    candidates.append(s)

        if not candidates: continue
        p = pattern.lower()
        matched = []
        if p == "總站" or p == "terminus": 
            matched = [candidates[0], candidates[-1]]
        else:
            # 2026-03-12 18:33 (by Agent): Check exact match first
            exact = [s for s in candidates if p == s.get('name_en', '').lower() or p == s.get('name_tc', '').lower()]
            if exact:
                matched = exact
                has_exact_match = True
            else:
                for s in candidates:
                    name = s.get('name_en' if lang=="en" else 'name_tc', '').lower()
                    if p in name: matched.append(s)
        
        if not matched: matched = sorted(candidates, key=lambda x: x.get('_dist', 9999))[:1]
        
        # 2026-03-12 18:33 (by Agent): Only add tasks if exact match or no exact match found yet
        if not has_exact_match or (has_exact_match and matched and any(p == s.get('name_en', '').lower() or p == s.get('name_tc', '').lower() for s in matched)):
            for s in matched:
                s['_is_exact'] = has_exact_match and any(p == s.get('name_en', '').lower() or p == s.get('name_tc', '').lower() for s in matched)
                tasks.append((op, s['stop'], route, s, bound))

    if not tasks:
        print("No route or stop found." if lang == "en" else "⚠️ 搵唔到路線或車站數據。")
        return

    route_info_kmb = fetch_route_info('kmb', route)
    route_info_ctb = fetch_route_info('ctb', route)
    merged_results = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        eta_results = list(executor.map(lambda x: fetch_eta(x[0], x[1], x[2]), tasks))
        for i, (op, stop_id, r, s_info, bound) in enumerate(tasks):
            eta_data = [e for e in eta_results[i] if e.get('eta')]
            lat, lon = float(s_info['lat']), float(s_info['long'])
            group_key = None
            for key in merged_results.keys():
                klat, klon = map(float, key.split(','))
                if get_dist(lat, lon, klat, klon) < 0.08:
                    group_key = key
                    break
            if not group_key:
                group_key = f"{lat},{lon}"
                name = s_info['name_en' if lang=="en" else 'name_tc']
                merged_results[group_key] = {"name": name, "lat": lat, "lon": lon, "etas": {}, "ops": set(), "is_exact": s_info.get('_is_exact', False)}
            merged_results[group_key]['ops'].add(op)
            for e in eta_data:
                d = e.get('dest_en' if lang=="en" else 'dest_tc', '未知')
                f_eta = format_eta(e['eta'])
                if f_eta and not any(x['raw']['ts'] == f_eta['ts'] for x in merged_results[group_key]['etas'].get(d, [])):
                    if d not in merged_results[group_key]['etas']: merged_results[group_key]['etas'][d] = []
                    is_start = s_info['_seq'] == 1
                    is_end = s_info['_seq'] == max_seqs.get((op, bound), 0)
                    merged_results[group_key]['etas'][d].append({"raw": f_eta, "op": op, "dir": e.get('dir'), "is_start": is_start, "is_end": is_end})

    for g in merged_results.values():
        is_actual_joint = "kmb" in g['ops'] and "ctb" in g['ops']
        op_for_meta = "kmb" if "kmb" in g['ops'] else "ctb"
        r_meta = route_info_kmb if op_for_meta == "kmb" else route_info_ctb
        prefix = "KMB" if "kmb" in g['ops'] else "CTB"
        if lang != "en": prefix = "九巴 (KMB)" if "kmb" in g['ops'] else "城巴 (CTB)"
        if is_actual_joint: prefix = "KMB/CTB Joint-op" if lang == "en" else "九巴 (KMB)/城巴 (CTB) 聯營"
        # 2026-03-12 18:33 (by Agent): Add ★ for exact match
        exact_marker = " ★" if g.get('is_exact') else ""
        print(f"🚌 **{prefix} {route}** @ {g['name']}{exact_marker} [📍地圖](https://www.google.com/maps?q={g['lat']},{g['lon']})")
        for d, etas in g['etas'].items():
            sorted_etas = sorted(etas, key=lambda x: x['raw']['ts'])[:3]
            time_strs = []
            for se in sorted_etas:
                s = f"{se['raw']['str']} ({se['raw']['min']} min)"
                if is_actual_joint:
                    ol = "KMB" if se['op'] == "kmb" else "CTB"
                    if lang != "en": ol = "九巴 (KMB)" if se['op'] == "kmb" else "城巴 (CTB)"
                    s += f" [{ol}]"
                if se['is_start']: s += " [起點站]" if lang != "en" else " [Origin]"
                if se['is_end']: s += " [終點站]" if lang != "en" else " [Terminus]"
                time_strs.append(s)
            bound = sorted_etas[0]['dir']
            if lang != "en": origin = r_meta.get('dest_tc') if bound == 'I' else r_meta.get('orig_tc')
            else: origin = r_meta.get('dest_en') if bound == 'I' else r_meta.get('orig_en')
            print(f"• {origin} {'To' if lang=='en' else '往'} {d}: " + ", ".join(time_strs))
        if not g['etas']: print("- No Data / Out of service" if lang == "en" else "- 暫時無資料 / 日間線已停駛")
        print()

if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    if len(args) >= 2:
        main(args[0], args[1], args[2] if len(args)>2 and args[2]!="None" else None, args[3] if len(args)>3 and args[3]!="None" else None, args[4] if len(args)>4 else "tc")