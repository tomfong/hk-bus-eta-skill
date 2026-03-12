# HK Bus ETA Skill for OpenClaw (BETA)

Author: Tom Fong

GitHub: https://github.com/tomfong

> **BETA**: This skill is under active development and may change. Use with caution in production environments.

This skill provides real-time Hong Kong bus ETA queries for KMB, LWB, and Citybus (CTB).

## Features

- Query ETA for 九巴/KMB, 龍運/LWB, and 城巴/Citybus/CTB
- Joint-operation route merging
- Location-aware stop matching
- Stop cache for performance

## Prerequisites

- Python 3.x
- `curl` (for API calls)

## Installation (Clawhub)

```bash
claw skill install tomfong/hk-bus-eta
```

## Usage

Ask your OpenClaw agent:
- "When will bus 1A arrive at Star Ferry?"
- "KMB route 68X to Yuen Long"
- "Nearest bus stop for route 11"

## License

MIT License - See [LICENSE](LICENSE) for details.