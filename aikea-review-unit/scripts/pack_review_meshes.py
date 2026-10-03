"""Scope: Create a static review GLB with fewer draws and verified unchanged geometry."""
import argparse
import json
from review_mesh_packer import ReviewMeshPacker


class PackReviewMeshesCommand:
    def run(self):
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument('source')
        parser.add_argument('output')
        args = parser.parse_args()
        print(json.dumps(ReviewMeshPacker().pack(args.source, args.output), indent=2))


if __name__ == '__main__':
    PackReviewMeshesCommand().run()
