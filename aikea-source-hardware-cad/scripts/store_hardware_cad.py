"""Scope: Run the project-local hardware CAD storage command."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from hardware_cad_store import HardwareCadSource, HardwareCadStore


class StoreHardwareCadCommand:
    """Translate one explicit source selection into the standard local library."""

    def __init__(self) -> None:
        self.store = HardwareCadStore()

    def run(self, arguments: argparse.Namespace) -> int:
        result = self.store.store(
            arguments.aikea_file,
            arguments.download,
            HardwareCadSource(
                manufacturer=arguments.manufacturer,
                product_family=arguments.product_family,
                catalog_item=arguments.catalog_item,
                product_url=arguments.product_url,
                cad_page_url=arguments.cad_page_url,
                terms_url=arguments.terms_url,
            ),
        )
        print(
            json.dumps(
                {
                    "status": "stored",
                    "hardware_directory": str(result.hardware_directory),
                    "source_record": str(result.source_record),
                    "cad_files": [str(path) for path in result.cad_files],
                },
                indent=2,
            )
        )
        return 0


# A function is the smallest adapter between Python's CLI boundary and the command object.
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Store an exact purchased-hardware CAD download for AIkea."
    )
    parser.add_argument("aikea_file", type=Path)
    parser.add_argument("--manufacturer", required=True)
    parser.add_argument("--product-family", required=True)
    parser.add_argument("--catalog-item", required=True)
    parser.add_argument("--product-url", required=True)
    parser.add_argument("--cad-page-url", required=True)
    parser.add_argument("--terms-url", required=True)
    parser.add_argument("--download", required=True, type=Path)
    return StoreHardwareCadCommand().run(parser.parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
