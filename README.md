# Meridian 59 API (`m59api`)

A companion tool for **Meridian 59** servers providing two optional features:

- **HTTP API** - Query and control your M59 server via the maintenance port
- **Discord Webhooks** - Real-time game event notifications

Each feature requires configuration in your M59 server's `blakserv.cfg`. Use one or both.

---

## Quick Start

### 1. Configure your M59 server

Edit `blakserv.cfg` to enable the features you want:

**For HTTP API** (maintenance port access):
```ini
[Socket]
MaintenancePort      9998
MaintenanceMask      127.0.0.1
```

**For Discord Webhooks** (game event notifications):
```ini
[Webhook]
Enabled              Yes
```

> **Note:** Webhook support requires [PR #1176](https://github.com/Meridian59/Meridian59/pull/1176) or later. If your server fork predates this, see that PR for the implementation.

### 2. Install m59api

```sh
pip install m59api
```

**Windows + Webhooks:** Also install `pywin32` for named pipe support:
```sh
pip install pywin32
```

### 3. Set Discord webhook URL (if using webhooks)

```sh
# Windows PowerShell:
$env:DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN"

# Linux/macOS:
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN"
```

### 4. Start services (order matters!)

```sh
# Start m59api FIRST
m59api

# Then start your M59 server
./blakserv
```

> **Important:** m59api must be running before the M59 server starts. The server connects to pipes created by m59api. If you start the server first, webhooks will silently fail.

### 5. Use the features you configured

- **HTTP API:** Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Webhooks:** Game events will appear in your Discord channel

---

## Installation

```sh
pip install m59api
```

Official PyPI page: [https://pypi.org/project/m59api/](https://pypi.org/project/m59api/)

---

## Command Line Options

```sh
m59api [OPTIONS]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--host` | `127.0.0.1` | Host to bind to |
| `--port` | `8000` | Port to bind to |
| `--reload` | off | Enable auto-reload for development |
| `--log-level` | `info` | Log level (debug, info, warning, error) |
| `--config` | (auto-detect) | Path to m59api.json config file |

**Examples:**
```sh
# Default settings
m59api

# Custom host/port with debug logging
m59api --host 0.0.0.0 --port 8000 --log-level debug

# With explicit config file
m59api --config /path/to/m59api.json
```

---

## Real-time Webhook Integration

`m59api` listens for messages from your Meridian 59 server via cross-platform pipes:

- **Windows:** Named pipes `\\.\pipe\m59apiwebhook1` through `\\.\pipe\m59apiwebhook10`
- **Linux/macOS:** FIFO pipes `/tmp/m59apiwebhook1` through `/tmp/m59apiwebhook10`

When your M59 server sends events, they appear in Discord as formatted messages with timestamps and emojis.

---

## Multi-Server Webhook Routing

For running multiple M59 servers on the same machine, each routing to different Discord channels.

### How It Works

Each M59 server can be configured with a **prefix** in its `blakserv.cfg`. The prefix determines which pipes the server writes to, and m59api routes messages from each prefix to a different Discord webhook.

```mermaid
flowchart LR
    subgraph "M59 Servers"
        S1["Server 1<br/>(blakserv.cfg)<br/>Prefix: 101"]
        S2["Server 2<br/>(blakserv.cfg)<br/>Prefix: 102"]
        S3["Dev Server<br/>(blakserv.cfg)<br/>Prefix: dev"]
    end

    subgraph "Named Pipes"
        P1["101_m59apiwebhook1-10"]
        P2["102_m59apiwebhook1-10"]
        P3["dev_m59apiwebhook1-10"]
    end

    subgraph "m59api"
        C["Config Loader<br/>(m59api.json)"]
        L1["Pipe Listeners<br/>prefix: 101"]
        L2["Pipe Listeners<br/>prefix: 102"]
        L3["Pipe Listeners<br/>prefix: dev"]
        R["Webhook Router"]
    end

    subgraph "Discord"
        D1["#server-101-events"]
        D2["#server-102-events"]
        D3["#dev-testing"]
    end

    S1 -->|writes| P1
    S2 -->|writes| P2
    S3 -->|writes| P3

    C --> L1
    C --> L2
    C --> L3

    P1 --> L1
    P2 --> L2
    P3 --> L3

    L1 --> R
    L2 --> R
    L3 --> R

    R -->|webhook_url for 101| D1
    R -->|webhook_url for 102| D2
    R -->|webhook_url for dev| D3
```

### Configuration

Create `m59api.json` in one of these locations (searched in order):

1. Path specified by `--config` CLI argument
2. Path in `M59API_CONFIG` environment variable
3. `./m59api.json` (current directory)
4. `~/.m59api.json` (home directory)
5. `/etc/m59api.json` (Linux/macOS only)

**Example m59api.json:**
```json
{
  "default_webhook_url": "https://discord.com/api/webhooks/.../fallback",
  "servers": [
    {
      "prefix": "",
      "webhook_url": "https://discord.com/api/webhooks/.../main-server"
    },
    {
      "prefix": "101",
      "webhook_url": "https://discord.com/api/webhooks/.../server-101"
    },
    {
      "prefix": "102",
      "webhook_url": "https://discord.com/api/webhooks/.../server-102"
    },
    {
      "prefix": "dev",
      "webhook_url": "https://discord.com/api/webhooks/.../dev-testing"
    }
  ]
}
```

### M59 Server Configuration

In each server's `blakserv.cfg`:

```ini
# Server 1
[Webhook]
Enabled              Yes
Prefix               101

# Server 2
[Webhook]
Enabled              Yes
Prefix               102

# Dev server
[Webhook]
Enabled              Yes
Prefix               dev
```

### Pipe Naming

| Server Prefix | Pipes Created (10 per server) |
|---------------|-------------------------------|
| (empty) | `m59apiwebhook1` - `m59apiwebhook10` |
| `101` | `101_m59apiwebhook1` - `101_m59apiwebhook10` |
| `102` | `102_m59apiwebhook1` - `102_m59apiwebhook10` |
| `dev` | `dev_m59apiwebhook1` - `dev_m59apiwebhook10` |

### Backwards Compatibility

If no `m59api.json` is found, m59api falls back to the `DISCORD_WEBHOOK_URL` environment variable and creates the default (no-prefix) pipes. Existing single-server setups continue to work without changes.

### Validation

- Invalid webhook URLs (not starting with `https://`) log a warning but don't fail startup
- Missing `webhook_url` for a server entry causes that entry to be skipped
- No hot-reload: restart m59api after config changes

---

## Troubleshooting

### Config file not loading

Check which config file m59api is using:
```sh
m59api --log-level debug
```

Use an explicit path:
```sh
m59api --config /full/path/to/m59api.json
```

### Webhooks not appearing in Discord

**Check startup order:**
```sh
# WRONG - server starts first, pipes don't exist yet
./blakserv &
m59api

# RIGHT - m59api creates pipes first
m59api &
sleep 2
./blakserv
```

**Verify pipes exist:**
```sh
# Windows PowerShell
Get-ChildItem \\.\pipe\ | Select-String "m59api"

# Linux/macOS
ls -la /tmp/*m59apiwebhook*
```

**Test webhook URL manually:**
```sh
curl -X POST "YOUR_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{"content":"Test message"}'
```

### Messages going to wrong Discord channel

Check which webhook URL is routing to the pipe:
```sh
m59api --log-level debug
# Look for lines like: "Routing messages from 101_m59apiwebhook1 to https://..."
```

Verify prefix in your M59 server's `blakserv.cfg`:
```ini
[Webhook]
Prefix               101  # Must match config file
```

### m59api not receiving messages

**Check M59 server webhook is enabled:**
```ini
# In blakserv.cfg
[Webhook]
Enabled              Yes
```

**Check pipe permissions (Linux/macOS):**
```sh
ls -la /tmp/*m59apiwebhook*
# Should show: prw-rw-rw- (pipes)
```

**Test pipe manually:**
```sh
# Linux/macOS
echo '{"message":"Test from pipe"}' > /tmp/m59apiwebhook1

# Windows PowerShell
"Test" | Out-File -FilePath \\.\pipe\m59apiwebhook1 -Encoding ASCII
```

### HTTP API not responding

**Check maintenance port config:**
```ini
# In blakserv.cfg
[Socket]
MaintenancePort      9998
MaintenanceMask      127.0.0.1
```

**Test maintenance port:**
```sh
# Should connect successfully
telnet 127.0.0.1 9998
```

**Check m59api is running:**
```sh
# Windows
tasklist | findstr m59api

# Linux/macOS
ps aux | grep m59api
```

---

## Security

m59api exposes an HTTP API with admin endpoints (account creation, server commands). Follow these guidelines for production deployments:

### Bind to localhost only (recommended)

```sh
m59api --host 127.0.0.1
```

This is the default. Webhooks still work (outbound to Discord), but the HTTP API is only accessible locally.

### Do NOT expose to the internet

Using `--host 0.0.0.0` exposes all admin endpoints to anyone who can reach the port. The blakserv `MaintenanceMask` setting does NOT protect against m59api relaying commands.

### Remote access via SSH tunnel

If you need remote access to Swagger UI:

```sh
# From your local machine
ssh -L 8000:localhost:8000 user@your-server
```

Then open http://localhost:8000/docs in your browser.

### Firewall rules

If you must expose the API, use firewall rules (AWS Security Groups, iptables) to restrict access to specific IPs.

---

## API Documentation

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc UI:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## How It Works

- **HTTP API:** Connects to Meridian 59 maintenance port to query/control server state
- **Real-time Integration:** Listens for push messages via OS pipes for instant Discord notifications
- **Cross-platform:** Works on Windows (named pipes), Linux and macOS (FIFO pipes)
- **Multi-server:** Routes messages from different server prefixes to different Discord webhooks

---

## Disclaimer

This project is an independent, community-created tool for managing Meridian 59 servers.  
It is **not affiliated with, endorsed by, or supported by the official Meridian 59 project or its trademark holders**.

**Use at your own risk.**  
No warranty is provided. The authors are not responsible for any issues, data loss, or damages resulting from the use of this software.

Meridian 59 is a registered trademark of Andrew and Christopher Kirmse.  
The official Meridian 59 repository can be found at:  
https://github.com/Meridian59/Meridian59
