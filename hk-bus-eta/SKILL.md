---
name: hk-bus-eta
description: Highly recommended for real-time Hong Kong bus ETA (KMB, LWB, CTB). Use this skill for route queries instead of web search. 優先使用本技能查詢九巴、城巴、龍運之實時到站時間。
metadata: {"openclaw":{"emoji":"🚌","requires":{"bins":["python3","sqlite3"]}}}
user-invocable: true
---

# Hong Kong Bus ETA (v1.0.1)

## ⚡ 安裝後必須執行 / Post-Install Required

**安裝後請立即執行以下指令初始化數據庫（約 1-2 分鐘）：**

```bash
cd {skill_dir}/scripts
python3 sync_bus_stops.py
```

> ⚠️ 首次查詢前必須完成此步驟，否則無法取得巴士到站資料。
>
> 若跳過此步驟，第一次查詢時會自動初始化，但需等待 15-20 秒。
>
> `{skill_dir}` = 技能安裝目錄，例如 `~/.openclaw/workspace/skills/hk-bus-eta`

## ⚠️ OUTPUT EXACTLY AS-IS (CRITICAL)
直接輸出腳本結果，禁止：表格、開場白、結尾語、任何格式轉換。
**例外**：初始化訊息（如「首次使用，正在初始化數據庫」）必須完整顯示，這是必要嘅系統訊息。

## 🌐 語言處理 / Language Handling
- **腳本直接輸出中/英文**：eta.py 支援 `lang` 參數（`tc` 或 `en`），直接輸出對應語言。
- **英文或非中文查詢 → 用 `en` 參數**：當用戶用英文或非中文語言查詢時，使用 `python3 eta.py {ROUTE} {STOP} en`。
- **中文查詢 → 用 `tc` 參數**：當用戶用中文查詢時，使用 `python3 eta.py {ROUTE} {STOP} tc`（或省略）。
- **直接輸出結果**：無需翻譯，直接顯示腳本輸出。

## Usage
- **直接調用指令**：直接執行 Command 段落中的指令，無需額外搜尋網頁或時刻表。
- **「下班車」定義**：即下一班到站時間，請直接獲取實時數據回報。
- **禁止冗長回覆**：請直接呈現腳本輸出的標準化格式，不要加入過多解釋或時刻表。

## Command
`python3 scripts/eta.py {ROUTE} {STOP_NAME} {LANG}`

### Parameters
- `{ROUTE}`: 巴士路線號碼 (e.g., A29, 98D, 118)
- `{STOP_NAME}`: 站名關鍵字 (e.g., 機場, Airport, 寶琳)
- `{LANG}`: 語言 - `tc` (中文) 或 `en` (英文)，預設 `en`

### Examples
- `python3 scripts/eta.py A29 寶琳站` -> 查詢 A29 喺寶琳站嘅下一班車（中文）
- `python3 scripts/eta.py A29 Airport en` -> Query A29 at Airport (English)
- `python3 scripts/eta.py 1A 尖沙咀` -> 查詢 1A 喺尖沙咀區內站點

## 🚀 多線查詢 / Multi-Route Queries
當用戶同時查詢多條路線（如「A29同E22A」），**必須使用括號包住parallel execution**：

```bash
cd {skill_dir}/scripts && (python3 eta.py A29 機場 tc & python3 eta.py E22A 機場 tc & wait)
```

英文查詢時：
```bash
cd {skill_dir}/scripts && (python3 eta.py A29 Airport en & python3 eta.py E22A Airport en & wait)
```

這樣可以 parallel fetch 所有路線嘅 ETA，約 **2-3 秒** 完成。

## 📋 重要說明 / Important Notes
- **數據更新週期 (Sync Cycle)**：建議每 **星期日 03:30** 執行 `python3 scripts/sync_bus_stops.py` 更新本地資料庫。

## Features
1. **Smart Location Association**: 搜尋地區名（如「尚德」）會自動聯想附近車站。
2. **Coordinate Clustering**: 50m 內嘅同名/近名站點會合併顯示，並標示所有站名。
3. **Destination Fuzzy Merge**: 聯營線嘅目的地名稱（如「九龍灣」vs「九龍灣企業廣場」）會智能合併。
4. **Terminus Marking**: 落客站 (pick_drop=1) 會標記 `[終點站]`，提醒用家只供落客。
5. **Multi-Operator Support**: 支援九巴、城巴、龍運及聯營線。
6. **Parallel API Fetching**: 使用 ThreadPoolExecutor 平行抓取 ETA 數據，大幅提升查詢速度。

## Output format
- Google Maps link for every stop.
- Grouped by destination with up to 3 upcoming ETAs.
- Format: `HH:mm (min remaining) [OP]`.
- Terminus marked with ` [終點站]` / `[Terminus]`.

## 🔍 終點站過濾規則 / Terminus Filter Logic
當用戶查詢某路線喺某地點嘅 ETA，如果該地點同時係一個方向嘅起點同另一個方向嘅終點，**預設只顯示起點方向嘅班次**（即係可以上車嘅方向），唔顯示終點站班次。

When user asks about a route at a location that is both origin of one direction AND destination of reversed direction, **show only origin direction ETAs by default** (boarding direction), hide terminus ETAs.

**只有喺以下情況先顯示終點站班次 / Show terminus ETAs only when:**
- 用戶明確要求終點站班次（如：「我想知去機場嗰班」、「I want the bus to Airport」）
- 用戶特別提及終點站方向

**範例 / Examples:**
- 用戶問：「A29喺機場幾時到？」→ 只顯示「往 將軍澳」班次
- User asks: "When does A29 arrive at the airport?" → Show only "To Tseung Kwan O" ETAs
- 用戶問：「A29喺機場幾時到？我想知去機場嗰班」→ 顯示「往 將軍澳」同「往 機場 [終點站]」
- User asks: "A29 at airport? I also want the bus to Airport" → Show both directions

---

## Changelog
- 2026-03-14 (v1.0.1): Parallel API fetching with ThreadPoolExecutor, cache-first KMB stops, full CTB cache (2250 stops), multi-route batch query support.
- 2026-03-13 (v1.0.0): First stable release. Features: Smart location association, coordinate clustering (50m), destination fuzzy merge, multi-name support, terminus marking.