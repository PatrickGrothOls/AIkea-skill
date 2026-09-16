"""Scope: Reject the retired NC70 review route after the project moved to GRASS."""


class RetiredReviewRoute:
    def run(self):
        raise SystemExit(
            "This NC70 complete/open review route is retired. "
            "Use build_grass_closed_diagnostic.py for the labelled closed proposal "
            "and export_current_parts.py for matching part evidence. "
            "A GRASS complete/open review requires verified motion evidence."
        )


if __name__ == "__main__":
    RetiredReviewRoute().run()
