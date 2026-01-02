import uvicorn
import argparse

from m59api import config


def main():
    parser = argparse.ArgumentParser(description="Run the Meridian 59 API server.")
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host to bind to (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind to (default: 8000)",
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for development",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="info",
        help="Set log level (default: info)",
    )
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to m59api.json config file for multi-server webhook routing",
    )

    args = parser.parse_args()

    # Load configuration before starting server
    # This sets up the webhook URL mappings for each server prefix
    config.load_config(args.config)

    print(f"\nAdmin API docs: http://{args.host}:{args.port}/docs")

    uvicorn.run(
        "m59api.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level=args.log_level,
    )
