# Meridian 59 API

This is a FastAPI-based API for managing the **Meridian 59** server.
It ocntains two executables
- a discord bot
- a fastapi server


## What
- Created FastAPI routes for server management in `api.py`
- Configured FastAPI server to connect to the BlakSton server maintenance port
- Example API endpoints:
  - GET /api/v1/admin/who
  - POST /api/v1/admin/send-users

## Why
- Enable modern web-based management interface for blakserv
- Provide secure, RESTful API access to server functions
- Allow external tools/services to interact with the server

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

## Implementation Details
### FastAPI Router (`api.py`):

- REST endpoint definitions
- JSON response formatting
- Maintenance port command handling

### Maintenance Client (`maintenance.py`):

- TCP socket connection to BlakSton server maintenance port
- Command sending and response handling

## Configuration
Add the following to the `blakserv.cfg` in the server running directory:
```
[Socket]             
MaintenancePort      9998
MaintenanceMask      0.0.0.0
```

config.py - defines discord webhook url if used for discord bot

#### **Configuration**
Before running the application, you need to set the `DISCORD_WEBHOOK_URL` environment variable. This variable is used to send messages to Discord.

1. **On Windows**:
   Open a Command Prompt or PowerShell and run:
   ```cmd
   set DISCORD_WEBHOOK_URL=https://your-discord-webhook-url 
   ```

2.  **On macOS/Linux**:
 Open a terminal and run:

`export DISCORD_WEBHOOK_URL=https://your-discord-webhook-url`


## Features

## Running it
- uvicorn main:app --reload --log-level debug
    - optional windows batch file that does the same: `debug.bat`
- discord_bot.py
    - optional Discord bot
    - populate config.py with your `DISCORD_BOT_TOKEN` and `API_BASE_URL`
    - `python discord_bot.py`


## Testing
- Access the API documentation at `http://127.0.0.1:8000/docs`
- Test the endpoints using curl or a web browser:
   ```bash
   curl -X GET "http://127.0.0.1:8000/api/v1/admin/who"
   curl -X GET "http://127.0.0.1:8000/api/v1/admin/status"
   curl -X GET "http://127.0.0.1:8000/api/v1/admin/memory"
   curl -X POST "http://127.0.0.1:8000/api/v1/admin/send-users?message=Hello"
   ```

``` mermaid
graph TD
    subgraph Users
        P[Players] --> W[Web Interface]
        A[Admins] --> W
        I[IoT/Automations] --> API[FastAPI Endpoints]
    end
    
    subgraph Server Integration
        W --> API
        API --> M[Maintenance Port]
        M --> B[Blakserv]
        B --> G[Game World]
    end
```
## Installation

### 1 Install dependencies
`pip install -r requirements.txt`
(Or use Poetry, see below)

### 2 Run the server:
`uvicorn main:app --reload`

### 3 Open API documentation:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc UI: http://127.0.0.1:8000/redoc


## Configuration

### cli.py
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

export ENV=development
m59api --reload

Test Without --reload Before Deployment:

Always test your app in a production-like environment (without --reload) to ensure it behaves as expected.

## License
Meridian 59 is open-source. See `LICENSE` for details.