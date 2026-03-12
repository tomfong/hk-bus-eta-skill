import json
import os
import time
import math
import concurrent.futures
from urllib.request import urlopen, Request
from datetime import datetime, timezone, timedelta

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
    path = CACHE_FILE_KMB
    if os.path.exists(path):
        with open(path, 'r') as f:
            cache = json.load(f)
        now_ts = time.time()
        now_struct = time.localtime(now_ts)
        if now_ts - cache['ts'] < CACHE_EXPIRY:
            if not (now_struct.tm_hour >= 5 and time.localtime(cache['ts']).tm_mday != now_struct.tm_mday):
                return {s['stop']: s for s in cache['data']}
    
    res = fetch_api("https://data.etabus.gov.hk/v1/transport/kmb/stop")
    if res and 'data' in res:
        with open(path, 'w') as f:
            json.dump({"ts": time.time(), "data": res['data']}, f)
        return {s['stop']: s for s in res['data']}
    return {}

def fetch_stop_info(op, stop_id):
    url = f"https://data.etabus.gov.hk/v1/transport/kmb/stop/{stop_id}" if op == "kmb" else f"https://rt.data.gov.hk/v2/transport/citybus/stop/{stop_id}"
    res = fetch_api(url)
    return res['data'] if res and 'data' in res else None

def fetch_route_info(op, route, bound=None):
    if op == 'kmb':
        b = bound if bound else 'outbound'
        url = f"https://data.etabus.gov.hk/v1/transport/kmb/route/{route}/{b}/1"
    else:
        url = f"https://rt.data.gov.hk/v2/transport/citybus/route/CTB/{route}"
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
    is_joint = any(route.startswith(p) for p in ["1", "3", "6", "9", "N"])
    kmb_stops_dict = get_cached_kmb_stops()
    
    ops_bounds = [('kmb', 'outbound'), ('kmb', 'inbound'), ('ctb', 'outbound'), ('ctb', 'inbound')]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        rs_results = list(executor.map(lambda x: fetch_route_stops(x[0], route, x[1]), ops_bounds))
    
    tasks = []
    for i, (op, bound) in enumerate(ops_bounds):
        rs = rs_results[i]
        if not rs: continue
        candidates = []
        if op == 'kmb':
            for r in rs:
                s_info = kmb_stops_dict.get(r['stop'])
                if s_info:
                    s_info_copy = s_info.copy()
                    s_info_copy['_seq'] = int(r.get('seq', 0))
                    s_info_copy['_bound'] = bound
                    if u_lat and u_lon: s_info_copy['_dist'] = get_dist(u_lat, u_lon, s_info_copy['lat'], s_info_copy['long'])
                    candidates.append(s_info_copy)
        else:
            stop_ids = [r['stop'] for r in rs]
            with concurrent.futures.ThreadPoolExecutor() as exec2:
                ctb_infos = list(exec2.map(lambda sid: fetch_stop_info('ctb', sid), stop_ids))
            for idx, sinfo in enumerate(ctb_infos):
                if sinfo:
                    sinfo_copy = sinfo.copy()
                    sinfo_copy['_seq'] = int(rs[idx].get('seq', 0))
                    sinfo_copy['_bound'] = bound
                    if u_lat and u_lon: sinfo_copy['_dist'] = get_dist(u_lat, u_lon, sinfo_copy['lat'], sinfo_copy['long'])
                    candidates.append(sinfo_copy)

        if not candidates: continue
        matched = []
        p = pattern.lower()
        if p == "總站" or p == "terminus":
            matched = [candidates[0], candidates[-1]]
        else:
            for s in candidates:
                name_field = s.get('name_en', '').lower() if lang == "en" else s.get('name_tc', '').lower()
                if p in name_field: matched.append(s)
        if not matched:
            matched = sorted(candidates, key=lambda x: x.get('_dist', 9999))[:1]
        for s in matched:
            tasks.append((op, s['stop'], route, s))

    if not tasks:
        print("No route or stop found." if lang == "en" else f"⚠️ 搵唔到路線 {route} 或站名 {pattern}。")
        return

    # Cache route metadata for origin names
    route_origins = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        unique_op_bounds = list(set((t[0], t[3]['_bound']) for t in tasks))
        meta_results = list(executor.map(lambda x: fetch_route_info(x[0], route, x[1]), unique_op_bounds))
        for idx, (op, b) in enumerate(unique_op_bounds):
            m = meta_results[idx]
            if not m: continue
            # Unified origin logic for KMB and CTB
            route_origins[(op, b)] = m.get('dest_tc') if b == 'inbound' else m.get('orig_tc')

    merged_results = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        eta_results = list(executor.map(lambda x: fetch_eta(x[0], x[1], x[2]), tasks))
        for i, (op, stop_id, r, s_info) in enumerate(tasks):
            eta_data = [e for e in eta_results[i] if e.get('eta')]
            lat, lon = float(s_info['lat']), float(s_info['long'])
            group_key = None
            for key in merged_results.keys():
                klat, klon = map(float, key.split(','))
                if get_dist(lat, lon, klat, klon) < 0.1:
                    group_key = key
                    break
            if not group_key:
                group_key = f"{lat},{lon}"
                name = s_info['name_en'] if lang == "en" else s_info['name_tc']
                merged_results[group_key] = {"name": name, "lat": lat, "lon": lon, "seq": s_info.get('_seq'), "bound": s_info.get('_bound'), "etas": {}, "ops": set()}
            merged_results[group_key]['ops'].add(op)
            for e in eta_data:
                d = e.get('dest_en') if lang == "en" else e.get('dest_tc', '未知')
                f_eta = format_eta(e['eta'])
                if f_eta:
                    if d not in merged_results[group_key]['etas']: merged_results[group_key]['etas'][d] = []
                    merged_results[group_key]['etas'][d].append({"raw": f_eta, "op": op, "bound": e.get('dir')})

    for g in merged_results.values():
        is_actual_joint = "kmb" in g['ops'] and "ctb" in g['ops']
        op_primary = list(g['ops'])[0]
        prefix = "KMB" if op_primary == 'kmb' else "CTB"
        if lang != "en": prefix = "九巴" if op_primary == "kmb" else "城巴"
        if is_actual_joint: prefix = "KMB/CTB Joint" if lang == "en" else "九巴/城巴聯營"

        print(f"🚌 **{prefix} {route}** @ {g['name']} [📍地圖](https://www.google.com/maps?q={g['lat']},{g['lon']})")
        for d, etas in g['etas'].items():
            sorted_etas = sorted(etas, key=lambda x: x['raw']['ts'])[:3]
            time_strs = []
            for se in sorted_etas:
                s = f"{se['raw']['str']} ({se['raw']['min']} min)"
                if is_actual_joint:
                    op_label = "KMB Cycle" if se['op'] == "kmb" else "CTB Cycle"
                    if lang != "en":
                        op_label = "九巴時段" if se['op'] == "kmb" else "城巴時段"
                    s += f" [{op_label}]"
                time_strs.append(s)
            
            # Fetch Origin
            origin_name = "起點"
            # Try to match the bound of this specific destination set
            target_bound = sorted_etas[0]['bound'] # Use direction from first ETA
            if target_bound == 'O': b_key = 'outbound'
            elif target_bound == 'I': b_key = 'inbound'
            else: b_key = g['bound']
            
            origin_name = route_origins.get((op_primary, b_key), "起點")
            
            sep = "To" if lang == "en" else "往"
            print(f"• {origin_name} {sep} {d}: " + ", ".join(time_strs))
        if not g['etas']:
            print("- No ETA / Out of Service" if lang == "en" else "- 暫時無班次資料 / 日間線已停駛")
        print()

if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    if len(args) >= 2:
        main(args[0], args[1], args[2] if len(args) > 2 and args[2] != "None" else None, args[3] if len(args) > 3 and args[3] != "None" else None, args[4] if len(args) > 4 else "tc")
