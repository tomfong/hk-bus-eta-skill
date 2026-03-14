# Hong Kong Bus ETA Skill for AI Agents

Author: [Tom FONG](https://github.com/tomfong) (with Mr. Usagi - Tom's OpenClaw Agent) 

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 🚌 Real-time Hong Kong bus arrival predictions for KMB, LWB and Citybus. 

## What is this?

A skill package for OpenClaw (and compatible AI agents) that provides real-time bus arrival predictions in Hong Kong. Supports:

- **九巴 (KMB)** - The Kowloon Motor Bus Co. (1933)
- **龍運 (LWB)** - Long Win Bus
- **城巴 (CTB)** - Citybus

## Installation

Please refer to the [installation guide](./hk-bus-eta/README.md#installation).

**Important**: After installation, you must initialize the database by running:
```bash
cd {skill_dir}/scripts
python3 sync_bus_stops.py
```

This step takes about 1-2 minutes and is required before the first query.

## Documentation

Full skill documentation is available in the [`hk-bus-eta/`](hk-bus-eta/) folder.

- [Skill README](hk-bus-eta/README.md) - Usage guide
- [SKILL.md](hk-bus-eta/SKILL.md) - Technical specification

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

<br>

<img src="./hk-bus-eta/docs/images/example01.PNG" width="400" alt="Bus ETA Example">

👉🏼 [View detailed GUIDES and EXAMPLES](./hk-bus-eta/README.md#features) 👈🏼

## Performance Improvements (v1.0.1)

**Key Optimizations:**

1. **Parallel API Fetching**: Uses `ThreadPoolExecutor` to fetch KMB and CTB ETA data simultaneously
2. **Cache-First Strategy**: Pre-loads KMB stops cache and full CTB cache (2250+ stops)
3. **Multi-Route Batch Queries**: Supports parallel execution for multiple route queries
4. **Reduced Latency**: Significantly faster response times for multi-route queries

**Example Performance Gain:**
- **Before**: Sequential queries for A29 and E22A took ~1 minute
- **After**: Parallel queries complete in ~2-3 seconds

**Usage for Multi-Route Queries:**
When users ask for multiple routes (e.g., "A29同E22A"), agents should use:
```
cd {skill_dir}/scripts && (python3 eta.py A29 機場 & python3 eta.py E22A 機場 & wait)
```

This parallel execution dramatically reduces wait time for multi-route queries (2-3 seconds).

## Changelog

### v1.0.1 (2026-03-14)
- **Parallel API Fetching**: Simultaneous KMB and CTB ETA data fetching
- **Cache-First Strategy**: Pre-loaded KMB stops and full CTB cache
- **Multi-Route Batch Support**: Parallel execution for multiple route queries with proper syntax
- **Performance Improvements**: Reduced latency from ~1 minute to ~2-3 seconds for multi-route queries

### v1.0.0 (2026-03-13)
- Initial release with smart location association and coordinate clustering
- Support for KMB, Citybus, LWB, and joint routes
- Local SQLite cache for fast queries
- Auto-sync recommendation (weekly)

## License

MIT License - See [LICENSE](LICENSE) for details.

---

_SIMPLE DEV, SIMPLER WORLD_
