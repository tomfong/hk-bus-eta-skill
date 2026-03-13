# Hong Kong Bus ETA Skill for AI Agents

Author: [Tom FONG](https://github.com/tomfong) (with Mr. Usagi - Tom's OpenClaw Agent)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 🚌 Real-time Hong Kong bus ETA for KMB, LWB, and Citybus (CTB).

## What is this?

A skill package for OpenClaw (and compatible AI agents) that provides real-time bus arrival predictions in Hong Kong. Supports:

- **九巴 (KMB)** - Kowloon Motor Bus
- **城巴 (CTB)** - Citybus
- **龍運 (LWB)** - Long Win Bus

## Installation

### For OpenClaw Users

Install directly from ClawHub:

```bash
clawhub install hk-bus-eta
```

Or install from this repository:

```bash
clawhub install https://github.com/tomfong/hk-bus-eta-skill
```

### For Developers

Clone the repository:

```bash
git clone https://github.com/tomfong/hk-bus-eta-skill.git
cd hk-bus-eta-skill
```

## Documentation

Full skill documentation is available in the [`hk-bus-eta/`](hk-bus-eta/) folder.

- [Skill README](hk-bus-eta/README.md) - Usage guide
- [SKILL.md](hk-bus-eta/SKILL.md) - Technical specification

## Features

- 🔍 Smart location matching (search by area name)
- 📍 Coordinate clustering (merge stops within 50m)
- 🔀 Joint-operation route support
- 🚏 Terminus marking for drop-off only stops
- ⚡ Local cache for fast queries
- 🔄 Auto-sync bus stop database (weekly)

## Requirements

- Python 3.x
- `curl` (for API calls)
- `sqlite3` (for local cache)

## License

MIT License - See [LICENSE](LICENSE) for details.

---

Made in Hong Kong