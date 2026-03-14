# Hong Kong Bus ETA Skill for AI Agents | 香港巴士到站預報

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)
[![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-Compatible-green.svg)](https://github.com/openclaw/openclaw)
[![Hong Kong Bus](https://img.shields.io/badge/Hong%20Kong-Bus-red.svg)](https://data.gov.hk)
[![Last Updated](https://img.shields.io/badge/Last%20Updated-2026--03--14-brightgreen.svg)](https://github.com/tomfong/hk-bus-eta-skill)

> 🚌 **Real-time Hong Kong bus arrival predictions** for KMB, LWB, and Citybus | **香港九巴、龍運、城巴實時到站時間查詢**

Author: [Tom FONG](https://github.com/tomfong) (with Mr. Usagi - Tom's OpenClaw Agent) 

## Overview

A skill package for **OpenClaw** (and compatible AI agents) that provides **real-time bus arrival predictions** in **Hong Kong**. This tool enables AI assistants to query bus ETA (Estimated Time of Arrival) data with **fuzzy location matching**, **bilingual support** (Chinese/English), and **parallel processing** for fast responses.

**Key Features:**
- **Real-time Hong Kong bus ETA** - Get accurate arrival times for buses across Hong Kong
- **Multi-operator support** - KMB, Citybus, LWB, and joint routes
- **AI Agent Integration** - Designed specifically for AI assistants and chatbots
- **Smart location matching** - Fuzzy search by area names and landmarks
- **Bilingual interface** - Supports both Traditional Chinese and English queries

**Supported Operators:**
- **九巴 (KMB)** - The Kowloon Motor Bus Co. (1933) | 九龍巴士
- **龍運 (LWB)** - Long Win Bus | 龍運巴士
- **城巴 (CTB)** - Citybus | 城巴

## Quick Start

**For AI Agents/Developers:**
```bash
# Install from ClawHub
clawhub install hk-bus-eta

# Or install from GitHub source
clawhub install https://github.com/tomfong/hk-bus-eta-skill --path hk-bus-eta --as hk-bus-eta
```

**For End Users:** Ask your AI assistant questions like:
- "下一班 1A 幾時到中間道？"
- "When does the next bus on route A21 arrive at the airport?"
- "城巴 11 喺中環有邊幾個站？巴士最快幾時到？"

## Installation

### Installation Methods

#### From ClawHub (Recommended)
```bash
clawhub install hk-bus-eta
```

#### From GitHub Source
```bash
clawhub install https://github.com/tomfong/hk-bus-eta-skill --path hk-bus-eta --as hk-bus-eta
```

### ⚡ **First-Time Setup (Recommended) **

⏱️ **First-time initialization takes ~1-2 minutes** to download and build the bus stops database (~20MB).
Subsequent queries are instant.

**You MUST run the following command once before first use:**

```bash
python3 <DIRECTORY_OF_SKILLS>/hk-bus-eta/scripts/sync_bus_stops.py
```

**Example**

```bash
python3 ~/.openclaw/workspace/skills/hk-bus-eta/scripts/sync_bus_stops.py
```

**What this does:**
- Downloads bus stop data from DATA.GOV.HK (約 20MB)
- Builds local SQLite database for fast queries
- Takes **1-2 minutes** for initial setup
- Required before first query

**Why is this needed?**
- Provides **offline bus stop lookup** capability
- Enables **fuzzy location matching** without API calls
- **Speeds up subsequent queries** significantly
- Supports **smart area name search** (e.g., "尚德", "寶琳站")

> ⚠️ **HIGHLY RECOMMENDED**: Complete this step before your first query for optimal performance.
> 
> If skipped, the first query will automatically download and initialize the database, but you'll need to wait 15-20 seconds.
> 
> `{skill_dir}` = skill installation directory, e.g. `~/.openclaw/workspace/skills/hk-bus-eta`

## Documentation

### This README contains complete documentation including:
- ✅ Installation instructions
- ✅ Usage examples
- ✅ Feature overview
- ✅ Technical details
- ✅ Changelog

### Additional Technical References:
- **[Technical Reference](hk-bus-eta/README.md)** - Technical architecture and script usage
- **[SKILL.md](hk-bus-eta/SKILL.md)** - AI agent specification and implementation details
- **[Scripts Directory](hk-bus-eta/scripts/)** - Python scripts source code

## Search Optimization

This skill is optimized for **natural language queries** with **fuzzy matching** capabilities:

**Search by:**
- **Route Numbers**: "1A", "A21", "690", "296D"
- **Area Names**: "尖沙咀", "Tsim Sha Tsui", "Central", "中環"
- **Landmarks**: "機場", "Airport", "紅隧", "Cross Harbour Tunnel"
- **Bus Stops**: "中間道", "Middle Road", "尚德總站", "Sheung Tak Bus Terminus"

**Smart Features:**
- **Fuzzy Matching**: Handles variations like "尖沙咀碼頭" vs "尖沙咀碼頭總站"
- **Stop Clustering**: Groups stops within 50m radius
- **Bilingual Support**: Query in Chinese or English, get results in same language
- **Multi-route Batch**: Query multiple routes simultaneously

## Features 

| Feature                  | Description                                  |
| ------------------------ | -------------------------------------------- |
| 🚌 **Multi-Operator**    | KMB, Citybus, LWB, and joint routes          |
| 🔍 **Smart Location**    | Search by area name (e.g., "尚德", "寶琳站") |
| 📍 **Stop Clustering**   | Merges stops within 50m radius               |
| 🔄 **Destination Merge** | Handles joint-route destination variations   |
| 🚏 **Terminus Marking**  | Shows `[終點站]` for drop-off only stops     |
| ⚡ **Local Cache**       | SQLite database for fast queries             |
| 📅 **Auto Sync** (Beta)  | Weekly database update recommended          |
| ⚡ **Parallel Processing**| Simultaneous API fetching for faster queries |
| 🔄 **Multi-Route Batch**  | Batch query support for multiple routes      |

## Usage Examples

### Natural Language Queries | 自然語言查詢
**Just ask in Cantonese, English, or mixed:**

**Chinese Examples:**
- "下一班 1A 幾時到中間道？"
- "城巴 11 喺中環有邊幾個站？巴士最快幾時到？"
- "我宜家人喺尖沙咀，想返將軍澳，請問296D、98D下班車幾時到?"

**English Examples:**
- "When does the next bus on route A21 arrive at the airport?"
- "What's the ETA for bus 690 at Central?"
- "Next bus for route 1A at Tsim Sha Tsui?"

### Direct Command Usage
The skill supports direct commands for query:

```bash
exec python3 <DIRECTORY_OF_SKILLS>/hk-bus-eta/scripts/eta.py {ROUTE} {STOP_NAME} [USER_LAT] [USER_LON] [LANG]
```

**Examples:**

```bash
# Route 690 at Central (English output)
exec python3 ~/.openclaw/workspace/skills/hk-bus-eta/scripts/eta.py 690 Central en

# Route 1A at Tsim Sha Tsui area (Chinese output)
exec python3 ~/.openclaw/workspace/skills/hk-bus-eta/scripts/eta.py 1A 尖沙咀 tc

# Route A21 at Airport (English output)
exec python3 ~/.openclaw/workspace/skills/hk-bus-eta/scripts/eta.py A21 Airport en
```

### Sample Output
```
🚌 路線 1A - 尖沙咀碼頭

📍 尖沙咀碼頭總站 [終點站]
   Google Maps: https://maps.google.com/...
   └─ 中秀茂坪
       14:32 (3 min) [KMB]
       14:45 (16 min) [KMB]
       15:02 (33 min) [KMB]
```

<img src="./docs/images/example01.PNG" width="400" alt="Bus ETA Example">

## Changelog

### v1.0.2 (2026-03-14) - Performance Optimizations
**Performance Optimizations:**

- **Parallel API Fetching**: Uses `ThreadPoolExecutor` to fetch KMB and CTB ETA data simultaneously
- **Cache-First Strategy**: Pre-loads KMB stops cache and full CTB cache (2250+ stops)
- **Multi-Route Batch Support**: Parallel execution for multiple route queries
- **Reduced Latency**: Significantly faster response times for multi-route queries
- **Improved Error Handling**: Better timeout management and error recovery
- **Language Handling**: English query/output mode supported

### v1.0.0 (2026-03-13) - Initial Release
- Initial release with smart location association and coordinate clustering
- Support for KMB, Citybus, LWB, and joint routes
- Local SQLite cache for fast queries
- Auto-sync recommendation (weekly)

## Technical Details

### Data Sync | 數據同步
Run weekly to keep bus stop data fresh:

```bash
python3 <DIRECTORY_OF_SKILLS>/hk-bus-eta/scripts/sync_bus_stops.py
```

**Example**

```bash
python3 ~/.openclaw/workspace/skills/hk-bus-eta/scripts/sync_bus_stops.py
```

**Recommended CRON schedule:** Every Sunday at 03:30

### Requirements
| Requirement | Notes                |
| ----------- | -------------------- |
| Python 3.x  | Main script runtime  |
| `curl`      | API calls            |
| `sqlite3`   | Local cache database |

### Data Source | 數據來源
Bus ETA data from APIs of [DATA.GOV.HK](https://data.gov.hk) (開放數據平台)

**Architecture:**
- **Local SQLite Cache**: Stores bus stop data for fast lookups
- **Parallel API Calls**: Simultaneous fetching from KMB and Citybus APIs
- **Fuzzy Matching**: Smart location association with 50m clustering
- **Bilingual Support**: Chinese (Traditional) and English interfaces

## SEO Keywords

**Primary Keywords:**
- Hong Kong bus ETA
- Real-time bus arrival Hong Kong
- KMB bus arrival time
- Citybus ETA
- Hong Kong bus tracking
- Next bus Hong Kong

**Chinese Keywords:**
- 香港巴士到站時間
- 九巴到站時間
- 城巴實時到站
- 龍運巴士ETA
- 下一班巴士幾時到
- 巴士到站查詢

**Technical Keywords:**
- OpenClaw skill
- AI agent bus ETA
- Python bus API
- Hong Kong transport API
- DATA.GOV.HK integration
- SQLite bus database

## GitHub Topics

```
hong-kong-bus
bus-eta
real-time-transport
hong-kong-transport
kmb
citybus
lwb
openclaw
ai-agent
python
transport-api
data-gov-hk
public-transport
hong-kong
bus-tracking
arrival-time
next-bus
```

## License

MIT License - See [LICENSE](LICENSE) for details.

---

_SIMPLE DEV, SIMPLER WORLD_
