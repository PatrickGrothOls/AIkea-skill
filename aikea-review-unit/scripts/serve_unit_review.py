"""Scope: Start the terminal-launched browser review for one cabinet GLB."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from unit_review_server import UnitReviewServer


class ServeUnitReviewCommand:
    """Validate review files, announce the URL, and run the local server."""

    def run(self, model_path: Path, port: int, open_browser: bool) -> int:
        viewer_root = Path(__file__).resolve().parents[1] / "assets" / "viewer"
        if not model_path.is_file():
            return self._invalid(f"GLB does not exist: {model_path}")
        if not (viewer_root / "index.html").is_file():
            return self._invalid("the bundled viewer asset is missing")
        server = UnitReviewServer(viewer_root, model_path, port)
        print(json.dumps({"status": "serving", "url": server.url}), flush=True)
        if open_browser:
            server.open_browser()
        try:
            server.serve()
        except KeyboardInterrupt:
            pass
        finally:
            server.close()
        return 0

    def _invalid(self, problem: str) -> int:
        print(json.dumps({"status": "invalid", "problems": [problem]}))
        return 2


# A small function is the direct adapter from Python's CLI entry point to the command object.
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Open one AIkea cabinet GLB in the bundled local viewer."
    )
    parser.add_argument("glb", type=Path)
    parser.add_argument("--port", type=int, default=0)
    parser.add_argument("--no-open", action="store_true")
    arguments = parser.parse_args()
    return ServeUnitReviewCommand().run(
        arguments.glb.resolve(), arguments.port, not arguments.no_open
    )


if __name__ == "__main__":
    raise SystemExit(main())
