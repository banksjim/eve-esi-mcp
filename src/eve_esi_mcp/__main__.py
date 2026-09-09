from __future__ import annotations

import argparse

from .server import build_server


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="eve-esi-mcp",
        description=(
            "EVE ESI MCP server. Defaults to stdio (launched as a child "
            "process by an editor). Use --http to run standalone so several "
            "clients can share one instance and one SSO session."
        ),
    )
    parser.add_argument(
        "--http",
        action="store_true",
        help="Serve over HTTP instead of stdio",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="HTTP bind address (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="HTTP port (default: 8000)",
    )
    args = parser.parse_args()

    server = build_server()
    if args.http:
        server.run(transport="http", host=args.host, port=args.port)
    else:
        server.run(transport="stdio")


if __name__ == "__main__":
    main()
