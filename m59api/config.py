"""
Configuration management for m59api.

Supports multi-server webhook routing via JSON config file.
Config file search order:
  1. --config CLI argument
  2. M59API_CONFIG environment variable
  3. ./m59api.json
  4. ~/.m59api.json
  5. /etc/m59api.json (Linux/macOS only)

Falls back to DISCORD_WEBHOOK_URL env var for backwards compatibility.
"""

import json
import os
import platform
from pathlib import Path
from typing import Optional

# Legacy env var for backwards compatibility
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

# Global config state
_config: Optional[dict] = None
_config_path: Optional[str] = None


class ServerConfig:
    """Configuration for a single M59 server's webhook routing."""
    
    def __init__(self, prefix: str, webhook_url: str):
        self.prefix = prefix
        self.webhook_url = webhook_url
    
    def get_pipe_paths(self) -> list[str]:
        """Returns list of 10 pipe paths for this server prefix."""
        if platform.system() == "Windows":
            if self.prefix:
                return [fr'\\.\pipe\{self.prefix}_m59apiwebhook{i}' for i in range(1, 11)]
            else:
                return [fr'\\.\pipe\m59apiwebhook{i}' for i in range(1, 11)]
        else:
            if self.prefix:
                return [f'/tmp/{self.prefix}_m59apiwebhook{i}' for i in range(1, 11)]
            else:
                return [f'/tmp/m59apiwebhook{i}' for i in range(1, 11)]


def find_config_file(cli_path: Optional[str] = None) -> Optional[str]:
    """
    Find config file using search order:
      1. CLI argument (--config)
      2. M59API_CONFIG env var
      3. ./m59api.json
      4. ~/.m59api.json
      5. /etc/m59api.json (Linux/macOS only)
    
    Returns path if found and readable, None otherwise.
    """
    candidates = []
    
    # 1. CLI argument
    if cli_path:
        candidates.append(cli_path)
    
    # 2. Environment variable
    env_path = os.environ.get("M59API_CONFIG")
    if env_path:
        candidates.append(env_path)
    
    # 3. Current directory
    candidates.append("./m59api.json")
    
    # 4. User home directory
    home = Path.home()
    candidates.append(str(home / ".m59api.json"))
    
    # 5. System config (Linux/macOS only)
    if platform.system() != "Windows":
        candidates.append("/etc/m59api.json")
    
    for path in candidates:
        expanded = os.path.expanduser(os.path.expandvars(path))
        if os.path.isfile(expanded):
            return expanded
    
    return None


def load_config(cli_path: Optional[str] = None) -> dict:
    """
    Load configuration from JSON file or fall back to env var.
    
    Returns dict with:
      - 'servers': list of ServerConfig objects
      - 'default_webhook_url': fallback URL (optional)
      - 'source': where config came from ('file', 'env', or 'none')
    """
    global _config, _config_path
    
    config_file = find_config_file(cli_path)
    
    if config_file:
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            _config_path = config_file
            servers = []
            
            # Parse server entries
            for server in data.get("servers", []):
                prefix = server.get("prefix", "")
                webhook_url = server.get("webhook_url", "")
                
                if not webhook_url:
                    print(f"Warning: Server prefix '{prefix}' has no webhook_url, skipping")
                    continue
                
                # Validate webhook URL format
                if not webhook_url.startswith("https://"):
                    print(f"Warning: Server prefix '{prefix}' has invalid webhook URL (must start with https://)")
                    continue
                
                servers.append(ServerConfig(prefix, webhook_url))
            
            default_url = data.get("default_webhook_url", "")
            if default_url and not default_url.startswith("https://"):
                print(f"Warning: default_webhook_url has invalid format (must start with https://)")
                default_url = ""
            
            _config = {
                "servers": servers,
                "default_webhook_url": default_url,
                "source": "file",
                "config_path": config_file
            }
            
            print(f"Loaded config from: {config_file}")
            print(f"  Configured servers: {len(servers)}")
            for s in servers:
                print(f"    - prefix='{s.prefix}' -> {s.webhook_url[:50]}...")
            
            return _config
            
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in config file {config_file}: {e}")
        except Exception as e:
            print(f"Error loading config file {config_file}: {e}")
    
    # Fall back to environment variable (backwards compatible)
    env_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if env_url:
        _config = {
            "servers": [ServerConfig("", env_url)],
            "default_webhook_url": env_url,
            "source": "env"
        }
        print("Using DISCORD_WEBHOOK_URL from environment (no config file found)")
        return _config
    
    # No configuration found
    _config = {
        "servers": [],
        "default_webhook_url": "",
        "source": "none"
    }
    print("Warning: No webhook configuration found. Webhooks will not be sent.")
    return _config


def get_config() -> dict:
    """Get current configuration, loading if not already loaded."""
    global _config
    if _config is None:
        return load_config()
    return _config


def get_servers() -> list[ServerConfig]:
    """Get list of configured servers."""
    return get_config().get("servers", [])


def get_webhook_url_for_pipe(pipe_path: str) -> Optional[str]:
    """
    Get the webhook URL for a specific pipe path.
    
    Matches pipe path to server prefix and returns corresponding webhook URL.
    Falls back to default_webhook_url if no match.
    """
    config = get_config()
    
    # Extract prefix from pipe path
    # Windows: \\.\pipe\{prefix}_m59apiwebhook{n} or \\.\pipe\m59apiwebhook{n}
    # Linux: /tmp/{prefix}_m59apiwebhook{n} or /tmp/m59apiwebhook{n}
    
    pipe_name = os.path.basename(pipe_path)
    
    # Check if pipe has a prefix (contains underscore before m59apiwebhook)
    if "_m59apiwebhook" in pipe_name:
        prefix = pipe_name.split("_m59apiwebhook")[0]
    else:
        prefix = ""
    
    # Find matching server config
    for server in config.get("servers", []):
        if server.prefix == prefix:
            return server.webhook_url
    
    # Fall back to default
    return config.get("default_webhook_url", "")


def update_webhook_url(prefix: str, webhook_url: str) -> bool:
    """
    Update webhook URL for a specific server prefix at runtime.
    Creates new ServerConfig if prefix doesn't exist.
    
    Returns True if successful, False otherwise.
    """
    global _config
    
    if _config is None:
        load_config()
    
    # Validate webhook URL
    if not webhook_url.startswith("https://"):
        return False
    
    # Find existing server config
    for server in _config.get("servers", []):
        if server.prefix == prefix:
            server.webhook_url = webhook_url
            print(f"Updated webhook URL for prefix '{prefix}'")
            return True
    
    # Create new server config if not found
    new_server = ServerConfig(prefix, webhook_url)
    _config.setdefault("servers", []).append(new_server)
    print(f"Added new server config for prefix '{prefix}'")
    return True


def get_all_webhook_configs() -> list[dict]:
    """
    Get all configured webhook URLs with their prefixes.
    Returns list of dicts with 'prefix' and 'webhook_url' keys.
    """
    config = get_config()
    return [
        {"prefix": server.prefix, "webhook_url": server.webhook_url}
        for server in config.get("servers", [])
    ]
