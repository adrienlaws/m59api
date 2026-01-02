# Changelog

All notable changes to m59api are documented here.

---

## [0.2.2] - 2026-01-01

### Added

- **Multi-server webhook routing** - Run multiple game servers on the same
  machine, each routing to different Discord channels
- JSON configuration file (`m59api.json`) for server-specific webhooks
- Prefix-based pipe routing (e.g., `101_m59apiwebhook1-10`)
- Automatic config file discovery (CLI, env var, cwd, home, /etc)
- `--config` CLI argument for explicit config file path
- Runtime webhook URL updates via API endpoint

### Changed

- Complete rewrite of `config.py` with `ServerConfig` class
- Dynamic pipe creation based on configured servers
- Message routing per configured server prefix

### Backwards Compatibility

- Single-server setups continue to work with `DISCORD_WEBHOOK_URL` environment variable
- No breaking changes for existing deployments

### Config File Search Order

1. `--config /path/to/config.json` (CLI argument)
2. `M59API_CONFIG` environment variable
3. `./m59api.json` (current directory)
4. `~/.m59api.json` (home directory)
5. `/etc/m59api.json` (Linux/macOS only)
6. Fallback: `DISCORD_WEBHOOK_URL` env var

---

## [0.1.x] - 2025

### Added

- Initial release
- Single-server Discord webhook routing
- Named pipe communication with blakserv
- FastAPI-based HTTP interface
- Swagger UI documentation at `/docs`
