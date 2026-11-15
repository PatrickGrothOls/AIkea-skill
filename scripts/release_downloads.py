"""Scope: Read public release ZIP download counts without tracking skill users."""

import argparse
from datetime import datetime, timezone
import json
from urllib.error import URLError
from urllib.request import Request, urlopen


class ReleaseDownloads:
    def __init__(self, repository):
        self.repository = repository

    def read(self):
        releases = []
        page = 1
        while True:
            url = f"https://api.github.com/repos/{self.repository}/releases?per_page=100&page={page}"
            request = Request(url, headers={"Accept": "application/vnd.github+json",
                                           "User-Agent": "furniture-skill-download-counts"})
            with urlopen(request, timeout=10) as response:
                batch = json.load(response)
            for release in batch:
                assets = [{"name": asset["name"], "downloads": asset["download_count"]}
                          for asset in release["assets"] if asset["name"].endswith(".zip")]
                releases.append({"version": release["tag_name"], "assets": assets,
                                 "downloads": sum(asset["downloads"] for asset in assets)})
            if len(batch) < 100:
                break
            page += 1
        return {"repository": self.repository,
                "checked_at": datetime.now(timezone.utc).isoformat(),
                "metric": "release ZIP downloads, not unique users or installations",
                "total_downloads": sum(release["downloads"] for release in releases),
                "releases": releases}


class DownloadCountsCommand:
    def run(self):
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("--repository", default="PatrickGrothOls/AIkea-skill")
        args = parser.parse_args()
        try:
            result = ReleaseDownloads(args.repository).read()
        except (URLError, OSError, ValueError, KeyError, TypeError) as error:
            # Public API/network and response parsing failures terminate this read-only CLI.
            parser.exit(1, f"Download counts unavailable: {error}\n")
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    DownloadCountsCommand().run()
