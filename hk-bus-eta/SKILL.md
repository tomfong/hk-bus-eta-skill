---
name: hk-bus-eta
description: Query Hong Kong bus ETA for 九巴/KMB, 龍運/LWB, and 城巴/Citybus/CTB, using TD Super Dictionary for high-precision matching.
metadata: {"openclaw":{"emoji":"🚌","requires":{"bins":["python3","sqlite3"]}}}
user-invocable: true
---

# Hong Kong Bus ETA (v0.2.3 BETA)

Query real-time Hong Kong bus ETAs with high-precision TD Government Database matching and coordinate bridging.

## 📋 重要說明 / Important Notes

- **首次使用 (First-time Setup)**：安裝本技能後，必須執行 `python3 sync_bus_stops.py` 以建立本地資料庫 `bus_stops.db` 並預建快取。本資料庫不會隨安裝包提供。
- **數據更新週期 (Sync Cycle)**：本地資料庫每 **14 日** 需更新一次。週期由 **2026-03-10** 開始計算。下次建議更新日期為 **2026-03-24 05:30 AM**。
- **First-time Setup**: Run `python3 sync_bus_stops.py` immediately after installation. This is mandatory as `bus_stops.db` is not bundled.

## Command
`exec python3 /home/admin/.openclaw/skills/hk-bus-eta/scripts/eta.py {ROUTE} {STOP_NAME} [USER_LAT] [USER_LON] [LANG]`

## Matching logic (v0.2.3 BETA)
1. **TD Database Local Lookup**: Uses `bus_stops.db` (from TD `JSON_BUS.json`) to resolve official stop names and coordinates.
2. **Coordinate Bridging**: Bridges TD data to KMB/CTB APIs by matching physical coordinates (radius < 80m). This bypasses mismatched `stopId` systems.
3. **Smart Cache**: Uses `ctb_stops.json` and `kmb_stops.json` to store resolved API coordinates, ensuring sub-second response times for recurring queries.
4. **Terminus Filtering**: Automatically filters out "Drop-off only" stops (Official spec `stopPickDrop=1`).
5. **Output Cleanup**: Sanitizes stop names by removing HTML tags (e.g., `<br>`).
6. **15s Golden Rule**: Queries exceeding 15 seconds are terminated to prevent excessive waiting, with the message "對不起，我暫時無法查詢相關路線".

## Data Dictionary (Official TD Spec)
Reference for internal logic:
- **stopPickDrop**: 1=Drop-only, 2=Pick-only, 3=Both. (1 is filtered out).
- **routeSeq**: 1=Outbound/Circular, 2=Inbound.
- **companyCode**: KMB, CTB, LWB, etc.

## Provider rules
- **Joint-ops**: Merges KMB and CTB results for joint-operation routes, labeled as `九巴 (KMB)/城巴 (CTB) 聯營`.
- **Naming**: Always refer to operators as `九巴 (KMB)` and `城巴 (CTB)`.

## Output format
- Google Maps link for every stop.
- Grouped by destination with up to 3 upcoming ETAs.
- Format: `HH:mm (min remaining) [OP]`.

---

## Changelog
- 2026-03-13 (v0.2.3 BETA): Pre-built CTB cache, dynamic caching, coordinate bridging, and 15s Golden Rule timeout. By "Mr. Usagi - Tom's Agent".
- 2026-03-13 (v0.2.2 BETA): Performance optimization via reduced Stop-Info API calls.
- 2026-03-13 (v0.2.1 BETA): Fixed HTML tags, duplicated ETA, and terminus filtering based on TD spec.
