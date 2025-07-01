# Meridian 59 API or `m59api`
This is a FastAPI-based API for managing a **Meridian 59** server.

---

## Configuration

Before running the application, you need to set the `DISCORD_WEBHOOK_URL` environment variable. This variable is used to send messages to Discord.

**On Windows (Command Prompt or PowerShell):**
```cmd
set DISCORD_WEBHOOK_URL=https://your-discord-webhook-url
```

**On macOS/Linux (bash/zsh):**
```bash
export DISCORD_WEBHOOK_URL=https://your-discord-webhook-url
```

**With Docker:**
```sh
docker run --rm -it \
  -e DISCORD_WEBHOOK_URL=https://your-discord-webhook-url \
  -p 5959:5959 -p 8000:8000 -p 9998:9998 \
  m59-linux-test
```

> **Tip:** Never commit secrets (like webhooks or API keys) to your repository. Always use environment variables or a `.env` file (with [python-dotenv](https://pypi.org/project/python-dotenv/)) for local development.

---

## Running m59api

### 1. Running as a PyPI-installed Package
If you installed m59api via pip, you can run it using:
```sh
m59api --host 127.0.0.1 --port 8000 --reload
```
This launches the server using the CLI entry point defined in the package.

### 2. Running from Source (Development Mode)
If you cloned this repository and installed the dependencies manually, you can start the FastAPI server using:
```sh
uvicorn m59api.main:app --reload --log-level debug
```
This is useful for development and testing.

### 3. Running with Docker
```sh
docker run --rm -it \
  -e DISCORD_WEBHOOK_URL=https://your-discord-webhook-url \
  -p 5959:5959 -p 8000:8000 -p 9998:9998 \
  m59-linux-test
```

---

## Features

- FastAPI routes for server management in `api.py`
- Connects to the BlakSton server maintenance port
- Example API endpoints:
  - GET /api/v1/admin/who
  - POST /api/v1/admin/send-users

---

## Why

- Enable modern web-based management interface for blakserv
- Provide secure, RESTful API access to server functions
- Allow external tools/services to interact with the server

---

## Technical Flow

```ascii
FastAPI Client -> FastAPI Routes -> Maintenance Port -> Blakserv
   (HTTP)          (api.py)       (TCP Socket)         (C Core)

[Web Client] --HTTP--> [FastAPI Router] 
                          |
                          v
                    [Maintenance Port] 
                          |
                          v
                        Blakserv
```

---

## Implementation Details

### FastAPI Router (`api.py`):

- REST endpoint definitions
- JSON response formatting
- Maintenance port command handling

### Maintenance Client (`maintenance.py`):

- TCP socket connection to BlakSton server maintenance port
- Command sending and response handling

---

## Server Configuration

Add the following to the `blakserv.cfg` in the server running directory:
```
[Socket]             
MaintenancePort      9998
MaintenanceMask      0.0.0.0
```

---

## API Documentation

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc UI: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Testing Endpoints

```bash
curl -X GET "http://127.0.0.1:8000/api/v1/admin/who"
curl -X GET "http://127.0.0.1:8000/api/v1/admin/status"
curl -X GET "http://127.0.0.1:8000/api/v1/admin/memory"
curl -X POST "http://127.0.0.1:8000/api/v1/admin/send-users?message=Hello"
```

---

## Security & Best Practices

- **Never commit secrets** (webhooks, API keys, passwords) to your repository.
- Use environment variables or a `.env` file (with `python-dotenv`) for local development.
- Use `--reload` only for development, not in production.
- Always test your app in a production-like environment before deployment.

---

## Installation

### 1. Install dependencies
```sh
pip install -r requirements.txt
```
(Or use Poetry, see below)

### 2. Run the server:
```sh
uvicorn m59api.main:app --reload
```

### 3. Open API documentation:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc UI: http://127.0.0.1:8000/redoc

---

## CLI Arguments (`cli.py`)

Command-Line Arguments:
```
--host: Allows the user to specify the host (e.g., 0.0.0.0 for external access).
--port: Allows the user to specify the port (e.g., 8080).
--reload: Enables auto-reload for development.
--log-level: Sets the logging level (e.g., debug, info, warning).
```
Default Values:

If no arguments are provided, the app will run on 127.0.0.1:8000 with info log level and no auto-reload.

Customizable:

Users can override the defaults by providing arguments when running the m59api command.

Use --reload only in development:

It’s a great tool for speeding up development but should not be used in production.

Use Environment-Specific Configurations:

Use environment variables or configuration files to differentiate between development and production environments.
For example:

```sh
export ENV=development
m59api --reload
```

Test Without --reload Before Deployment:

Always test your app in a production-like environment (without --reload) to ensure it behaves as expected.

---

## License
Meridian 59 is open-source. See `LICENSE` for details.