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
| 📅 **Auto Sync** (Beta)  | Weekly database update recommended           |

<br>

<img src="./hk-bus-eta/docs/images/example01.PNG" width="400" alt="Bus ETA Example">

👉🏼 [View detailed GUIDES and EXAMPLES](./hk-bus-eta/README.md#features) 👈🏼

## License

MIT License - See [LICENSE](LICENSE) for details.

---

_SIMPLE DEV, SIMPLER WORLD_
