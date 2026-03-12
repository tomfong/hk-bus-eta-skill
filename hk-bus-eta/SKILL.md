---
name: hk-bus-eta
version: 0.1.0
author: Tom Fong (with my Agent "Mr. Usagi")
description: Query Hong Kong bus ETA for 九巴/KMB, 龍運/LWB, and 城巴/Citybus/CTB, with joint-operation merging, location-aware stop matching, and stop cache.
metadata: {"openclaw":{"emoji":"🚌","requires":{"bins":["python3","curl"]}}}
---

# Hong Kong Bus ETA

Query real-time Hong Kong bus ETAs, or match the most likely boarding stop using the user's location.

## Use when
- The user asks when a bus route will arrive at a stop
- The user names a route and stop, or refers to 九巴 / 龍運 / KMB / 城巴 / Citybus / CTB
- The user wants the nearest or best-matching stop based on their current location

## Command
`exec python3 /home/admin/.openclaw/skills/hk-bus-eta/scripts/eta.py {ROUTE} {STOP_NAME} [USER_LAT] [USER_LON] [LANG]`

## Changelog
- 2026-03-12 18:27 (by Agent): Exact name match priority for stop searches
- 2026-03-12 18:18 (by Agent): Origin/Terminus labels added

## Provider rules
- For genuine joint-operation cross-harbour or overnight routes (for example 1XX, 3XX, 6XX, 9XX, NXX), query both 九巴/KMB/龍運 and 城巴/Citybus/CTB, then merge results and show the soonest arrivals first.
- If the same route number exists under different operators but is not a joint-operation route, ask the user whether they want 九巴/KMB/龍運 or 城巴/Citybus/CTB.
- Always refer to the operator as `城巴 (CTB)` and `九巴 (KMB)` in output.
- Joint-operation labels must follow the format: `九巴 (KMB)/城巴 (CTB) 聯營`.

## Output rules
- Include a Google Maps link for the matched stop.
- For terminus/start points, mark with `[起點站]` or `[終點站]` (English: `[Origin]` or `[Terminus]`).
- Directional display: Always use `Origin 往 Destination` (English: `Origin To Destination`).
- ETA format: `HH:mm (min remaining)`.
- If a route is a joint-operation, append operator tags like `[九巴 (KMB)]` to each ETA entry.
- Group results by destination and show up to 3 upcoming buses per group.

## Matching logic
1. **Exact match priority**: If a stop name exactly matches the search pattern, use those stops first.
2. **Fuzzy match fallback**: If no exact match, use substring matching on stop names.
3. **Distance fallback**: If no match found, use the nearest stop based on user coordinates (if provided).
4. **Directional validation**: Only query stops that exist in the route's direction.

## Error handling
- If no stop is found, return the closest fuzzy-match suggestions or indicate it might be a terminus drop-off point.
- API failures must not crash the skill.