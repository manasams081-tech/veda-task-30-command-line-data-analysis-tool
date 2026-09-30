#!/usr/bin/env python3
"""
Unique lightweight web application for VEDA Task 30.

No web framework is required. It uses Python's built-in http.server and
the same reusable Pandas analysis module as the CLI.
"""

from __future__ import annotations
import json
import mimetypes
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from analysis import (
    DataAnalysisError,
    filter_data,
    group_data,
    load_csv,
    preview,
    statistics,
    summary,
)

ROOT = Path(__file__).resolve().parent
WEB_DIR = ROOT / "web"
HOST = "127.0.0.1"
PORT = 8000


def clean_value(value):
    if hasattr(value, "item"):
        try:
            return value.item()
        except Exception:
            pass
    return value


def records(df):
    return [
        {str(k): clean_value(v) for k, v in row.items()}
        for row in df.where(df.notna(), None).to_dict("records")
    ]


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, payload, status=200):
        body = json.dumps(payload, indent=2, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path):
        if not path.exists() or not path.is_file():
            self.send_error(404, "File not found")
            return
        content = path.read_bytes()
        content_type = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/":
            return self._send_file(WEB_DIR / "index.html")

        if parsed.path.startswith("/static/"):
            safe_name = Path(parsed.path.removeprefix("/static/")).name
            return self._send_file(WEB_DIR / safe_name)

        if parsed.path == "/api/analyze":
            query = parse_qs(parsed.query)
            file_path = query.get("file", ["sample_data/sales.csv"])[0]
            action = query.get("action", ["summary"])[0]
            column = query.get("column", [""])[0]
            value = query.get("value", [""])[0]
            metric = query.get("metric", [""])[0]
            limit = min(max(int(query.get("limit", ["20"])[0]), 1), 100)

            try:
                df = load_csv(str(ROOT / file_path) if not os.path.isabs(file_path) else file_path)

                if action == "summary":
                    payload = {"ok": True, "action": action, "result": summary(df)}
                elif action == "preview":
                    payload = {"ok": True, "action": action, "result": preview(df, limit)}
                elif action == "filter":
                    payload = {"ok": True, "action": action,
                               "result": records(filter_data(df, column, value).head(limit))}
                elif action == "group":
                    payload = {"ok": True, "action": action,
                               "result": records(group_data(df, column, metric or None).head(limit))}
                elif action == "stats":
                    payload = {"ok": True, "action": action,
                               "result": statistics(df, column)}
                else:
                    raise DataAnalysisError("Unknown analysis action.")
                return self._send_json(payload)

            except (DataAnalysisError, ValueError) as exc:
                return self._send_json({"ok": False, "error": str(exc)}, 400)

        self.send_error(404, "Route not found")

    def log_message(self, format, *args):
        # Keep the terminal clean and beginner-friendly.
        print("[web]", format % args)


def main():
    print("VEDA Task 30 web application")
    print(f"Open: http://{HOST}:{PORT}")
    print("Press Ctrl+C to stop.")
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
