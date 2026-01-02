# Multi-Server Webhook Deployment Guide

> **Note for other open source server operators:** This guide uses Meridian 59
> servers 101 and 102 as a concrete example, but the same approach works for
> any number of game servers. Simply adjust the prefixes and webhook URLs to
> match your setup. The m59api tool routes messages from any prefix to its
> configured Discord channel.

Q1 2026 Production Deployment Guide

---

## Overview

This guide covers setting up Discord webhooks for multiple game servers running
on a single Linux instance. One m59api instance routes webhooks from all
servers to their respective Discord channels.

**Example setup:**
- Server 101 -> #server-101-chat Discord channel
- Server 102 -> #server-102-chat Discord channel

---

## Prerequisites

- Python 3.7+ installed
- Game server instances ready to restart
- Discord webhook URLs for each server's channel
- Webhook support enabled in game server (PR #1176 for Meridian 59)

---

## Step 1: Install m59api

```bash
pip install m59api
```

Verify installation:
```bash
m59api --help
```

---

## Step 2: Create the config file

Create `/etc/m59api.json` with your server prefixes:

```json
{
  "servers": [
    {
      "prefix": "101",
      "webhook_url": "https://discord.com/api/webhooks/YOUR_101_WEBHOOK_ID/YOUR_101_TOKEN"
    },
    {
      "prefix": "102",
      "webhook_url": "https://discord.com/api/webhooks/YOUR_102_WEBHOOK_ID/YOUR_102_TOKEN"
    }
  ]
}
```

Replace the webhook URLs with your actual Discord webhook URLs.

> **Tip:** Add more server blocks for additional servers. Each prefix must be unique.

---

## Step 3: Update blakserv.cfg for each server

Add or update the Webhook section in each server's config:

**Server 101:**
```ini
[Webhook]
Enabled              Yes
Prefix               101
```

**Server 102:**
```ini
[Webhook]
Enabled              Yes
Prefix               102
```

---

## Step 4: Start m59api

Start m59api BEFORE starting the game servers.

IMPORTANT: Bind to localhost only for security (see Security section below):

```bash
m59api --host 127.0.0.1 --config /etc/m59api.json &
```

Or run in a screen/tmux session:
```bash
screen -S m59api
m59api --host 127.0.0.1 --config /etc/m59api.json
```
Then detach with Ctrl+A, D

---

## Step 5: Restart game servers

Restart all game servers. They will connect to the pipes created by m59api.

---

## Verification

1. Check that pipes were created:
```bash
ls -la /tmp/*webhook*
```

You should see pipes for each server:
- /tmp/101_m59apiwebhook1 through /tmp/101_m59apiwebhook10
- /tmp/102_m59apiwebhook1 through /tmp/102_m59apiwebhook10

2. Test manually:
```bash
echo '{"content":"Test from 101"}' > /tmp/101_m59apiwebhook1
echo '{"content":"Test from 102"}' > /tmp/102_m59apiwebhook1
```

3. Check your Discord channels - test messages should appear in their respective channels.

---

## Startup Order

This order is critical:

1. Start m59api first (creates the pipes)
2. Start game servers

If game servers start before m59api, webhooks will not work until both are restarted in the correct order.

---

## Troubleshooting

If webhooks are not appearing in Discord:

1. Check m59api is running:
```bash
ps aux | grep m59api
```

2. Check pipes exist:
```bash
ls -la /tmp/*webhook*
```

3. Check config file is valid JSON:
```bash
cat /etc/m59api.json | python3 -m json.tool
```

4. Check server config has the correct prefix:
```bash
grep -A 2 "Webhook" /path/to/blakserv.cfg
```

5. Test webhook URL directly:
```bash
curl -X POST "YOUR_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{"content":"Direct test"}'
```

---

## Optional: Run m59api as a systemd service

Create `/etc/systemd/system/m59api.service`:

```ini
[Unit]
Description=Meridian 59 Webhook Router
Before=blakserv-101.service blakserv-102.service

[Service]
ExecStart=/usr/local/bin/m59api --host 127.0.0.1 --config /etc/m59api.json
Restart=always
User=m59

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable m59api
sudo systemctl start m59api
```

---

## Changing Webhook URLs at Runtime

You can update webhook URLs without restarting the game servers:

1. Via the API (no restart needed):
```bash
curl -X POST "http://localhost:8000/api/v1/admin/webhook/update" \
  -H "Content-Type: application/json" \
  -d '{"prefix": "101", "webhook_url": "https://discord.com/api/webhooks/NEW_URL"}'
```

2. Or edit the config file and restart m59api only (game servers keep running).

---

## Security

IMPORTANT: m59api exposes an HTTP API with admin endpoints that can create
accounts and send server commands.

For production servers:

1. **Always bind to localhost only:**
```bash
m59api --host 127.0.0.1 --config /etc/m59api.json
```

2. **Do NOT use `--host 0.0.0.0`** unless you have firewall rules restricting access.

3. The blakserv MaintenanceMask setting does NOT protect against m59api relaying commands from the internet.

4. If you need remote access to the Swagger UI, use an SSH tunnel:
```bash
ssh -L 8000:localhost:8000 user@your-server
```
Then access http://localhost:8000/docs from your local machine.

---

## Summary

- One m59api instance handles all servers
- Each server has a unique prefix in its config
- Each prefix routes to a different Discord channel
- Start m59api before starting game servers
- Webhook URLs can be changed at runtime via the API
- Always bind m59api to localhost (127.0.0.1) in production
