---
name: hk-bus-eta
version: 0.1.0
author: Tom Fong
description: Query Hong Kong bus ETA for 九巴/KMB, 龍運/LWB, and 城巴/Citybus/CTB, with joint-operation merging, location-aware stop matching, and stop cache.
metadata:
  openclaw:
    emoji: 🚌
    category: transport
    tags:
      - hongkong
      - bus
      - eta
      - kmb
      - ctb
    requires:
      bins:
        - python3
        - curl
user-invocable: true
---

# Hong Kong Bus ETA

Query real-time Hong Kong bus ETAs, or match the most likely boarding stop using the user's location.

## Use when
- The user asks when a bus route will arrive at a stop
- The user names a route and stop, or refers to 九巴 / 龍運 / KMB / 城巴 / Citybus / CTB
- The user wants the nearest or best-matching stop based on their current location

## Command
`exec python3 /home/admin/.openclaw/skills/hk-bus-eta/scripts/eta.py {ROUTE} {STOP_NAME} [USER_LAT] [USER_LON]`

## Provider rules
- For genuine joint-operation cross-harbour or overnight routes (for example 1XX, 3XX, 6XX, 9XX, NXX), query both 九巴/KMB/龍運 and 城巴/Citybus/CTB, then merge results and show the soonest arrivals first.
- If the same route number exists under different operators but is not a joint-operation route, ask the user whether they want 九巴/KMB/龍運 or 城巴/Citybus/CTB.
- If the user does not specify and refuses to choose, query both and list them separately.
- Always refer to the operator as `城巴 (CTB)` in output. Do not use obsolete names.

## Output rules
- Include a Google Maps link for the matched stop, using `%2C` between latitude and longitude
- Hide terminus drop-off entries by default
- Mark origin departures with `[From Terminus]`
- If the destination includes `循環線`, rewrite the display from `To Destination` to `Origin → Destination`
- Do not add operator timing tags for non-joint-operation routes
- Add operator timing tags only when showing merged joint-operation results
- ETA format: `HH:mm [min remaining]`
- Do not manually merge or alter the output structure returned by the helper script. Present the script's textual grouping exactly as generated to avoid mixing ETAs from different physical stops.
- Group results by destination and show up to 3 upcoming buses per group

## Error handling
- If no stop is found, return the closest fuzzy-match suggestions
- If an official API does not respond, report that honestly
- API failures must not crash the skill
