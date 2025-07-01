# Meridian 59 API (`m59api`)

This is a FastAPI-based API for managing a **Meridian 59** server.

---

## Installation

You can install `m59api` directly from PyPI:

```sh
pip install m59api
```

Official PyPI page: [https://pypi.org/project/m59api/](https://pypi.org/project/m59api/)

---

## Configuration

Before running the application, set the `DISCORD_WEBHOOK_URL` environment variable if you want to use Discord webhook features.

**On Windows (Command Prompt or PowerShell):**
```cmd
set DISCORD_WEBHOOK_URL=https://your-discord-webhook-url
```

**On macOS/Linux (bash/zsh):**
```bash
export DISCORD_WEBHOOK_URL=https://your-discord-webhook-url
```

---

## Running

**From the command line (after pip install):**
```sh
m59api --host 127.0.0.1 --port 8000 --reload
```

**Or with Uvicorn directly:**
```sh
uvicorn m59api.main:app --reload
```

**With Docker:**
```sh
docker run --rm -it \
  -e DISCORD_WEBHOOK_URL=https://your-discord-webhook-url \
  -p 5959:5959 -p 8000:8000 -p 9998:9998 \
  m59-linux-test
```

---

## API Documentation

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc UI: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

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
