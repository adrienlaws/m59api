# Meridian 59 API (`m59api`)

This is a FastAPI-based API for managing a **Meridian 59** server with real-time Discord webhook integration.

---

## Quick Start

1. **Install from PyPI:**
   ```sh
   pip install m59api
   ```

2. **Set Discord webhook URL (optional but recommended):**
   ```sh
   # Windows Command Prompt:
   set DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN
   
   # Windows PowerShell:
   $env:DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN"
   
   # Linux/macOS:
   export DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN
   ```

3. **Start the API:**
   ```sh
   m59api
   ```

4. **Access the API documentation:**
   - Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser

**That's it!** Your API is now running and ready to receive messages from your Meridian 59 server.

---

## Installation

You can install `m59api` directly from PyPI:

```sh
pip install m59api
```

Official PyPI page: [https://pypi.org/project/m59api/](https://pypi.org/project/m59api/)

---

## Configuration

### Discord Webhook Setup

To enable Discord notifications, you'll need a Discord webhook URL:

1. Go to your Discord server
2. Server Settings ? Integrations ? Webhooks
3. Create New Webhook
4. Copy the Webhook URL
5. Set it as an environment variable (see Quick Start above)

Alternatively, you can set the webhook URL at runtime via the API:
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/admin/set-webhook-endpoint?webhook_url=YOUR_WEBHOOK_URL"
```

---

## Running Options

**Default (recommended for most users):**
```sh
m59api
```

**With custom options:**
```sh
m59api --host 0.0.0.0 --port 8000 --reload --log-level debug
```

**With Uvicorn directly:**
```sh
uvicorn m59api.main:app --reload
```

**With Docker:**
```sh
docker run --rm -it -e DISCORD_WEBHOOK_URL=https://your-discord-webhook-url -p 5959:5959 -p 8000:8000 -p 9998:9998 m59-linux-test
```

### Configuration Options

- `--host`: Host to bind to (default: `127.0.0.1`)
- `--port`: Port to bind to (default: `8000`)
- `--reload`: Enable auto-reload for development (default: off)
- `--log-level`: Set log level (default: `info`)

---

## Real-time Message Integration

`m59api` automatically listens for real-time messages from your Meridian 59 server via cross-platform pipes:

- **Windows:** Named pipes `\\.\pipe\m59apiwebhook1` through `\\.\pipe\m59apiwebhook10`
- **Linux/macOS:** FIFO pipe `/tmp/m59apiwebhook1`

When your M59 server sends JSON messages like:
```json
{"timestamp":1764182137,"message":"[DEATH] Player killed by another player"}
```

They automatically appear in Discord as formatted messages:
```
?? January 26, 2025 at 3:28 PM [DEATH] Player killed by another player
```

> **Windows users:** Install `pywin32` for named pipe support:
> ```sh
> pip install pywin32
> ```

---

## API Documentation

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc UI:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## How it Works

- **HTTP API:** Connect to Meridian 59 maintenance port to query/control server state
- **Real-time Integration:** Listen for push messages via OS pipes for instant Discord notifications
- **Cross-platform:** Works on Windows (named pipes), Linux and macOS (FIFO pipes)

---

## Disclaimer

This project is an independent, community-created tool for managing Meridian 59 servers.  
It is **not affiliated with, endorsed by, or supported by the official Meridian 59 project or its trademark holders**.

**Use at your own risk.**  
No warranty is provided. The authors are not responsible for any issues, data loss, or damages resulting from the use of this software.

Meridian 59 is a registered trademark of Andrew and Christopher Kirmse.  
The official Meridian 59 repository can be found at:  
https://github.com/Meridian59/Meridian59

---

**Quick start with all defaults:**
```
m59api
```
This will run the API on `127.0.0.1:8000` with log level `info`.

**Specify options (optional):**
```
m59api --host 0.0.0.0 --port 8000 --reload --log-level debug
```

**Or with Uvicorn directly:**
```
uvicorn m59api.main:app --reload
```

**With Docker:**
```
docker run --rm -it -e DISCORD_WEBHOOK_URL=https://your-discord-webhook-url -p 5959:5959 -p 8000:8000 -p 9998:9998 m59-linux-test
```

---

## Configuration Options

- `--host`: Host to bind to (default: `127.0.0.1`)
- `--port`: Port to bind to (default: `8000`)
- `--reload`: Enable auto-reload for development (default: off)
- `--log-level`: Set log level (default: `info`)

You can combine these options as needed, or just run `m59api` for the defaults.

---

## API Documentation

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc UI: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Listening for Pushes from Meridian 59

In addition to querying the Meridian 59 server via the maintenance port, `m59api` can also listen for push messages sent from the server or other processes via named pipes (Windows) or FIFOs (Linux/macOS).

- **On Linux/macOS:** Listens on `/tmp/m59apiwebhook1` (FIFO)
- **On Windows:** Listens on `\\.\pipe\m59apiwebhook1-10` (named pipes)

Any message written to this pipe will be received and printed by the API service. This allows the game server or other tools to push notifications or events to the API in real time.

> **Note:** On Windows, you must install `pywin32` for named pipe support:
> ```sh
> pip install pywin32
> ```

---

## How it Works

- **Querying:** Most API endpoints connect to the Meridian 59 maintenance port and issue commands to retrieve or modify server state.
- **Pushes:** The API also listens for messages sent to the OS pipe, allowing for real-time event pushes from the server or other processes.

---

## Disclaimer

This project is an independent, community-created tool for managing Meridian 59 servers.  
It is **not affiliated with, endorsed by, or supported by the official Meridian 59 project or its trademark holders**.

**Use at your own risk.**  
No warranty is provided. The authors are not responsible for any issues, data loss, or damages resulting from the use of this software.

Meridian 59 is a registered trademark of Andrew and Christopher Kirmse.  
The official Meridian 59 repository can be found at:  
https://github.com/Meridian59/Meridian59

---
