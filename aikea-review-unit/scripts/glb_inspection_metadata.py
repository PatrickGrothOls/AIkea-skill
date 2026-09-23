"""Scope: Attach inspection identities to GLB nodes without changing geometry or placement."""

import json
from pathlib import Path
import struct

from glb_artifact_snapshot import GlbArtifactSnapshot
from glb_panel_material_defaults import GlbPanelMaterialDefaults
from unit_mockup import MockupPart, UnitMockupInputError


class GlbInspectionMetadata:
    """Preserve binary buffers and original node names while describing display ownership."""

    def write(self, output: Path, parts: tuple[MockupPart, ...]) -> None:
        identities = {
            part.name: {"inspection_path": list(part.inspection_path), "kind": part.review_kind}
            for part in parts if part.inspection_path
        }
        if not identities:
            return
        snapshot = GlbArtifactSnapshot.load(output)
        json_length = struct.unpack_from("<I", snapshot.content, 12)[0]
        json_end = 20 + json_length
        document = json.loads(snapshot.content[20:json_end])
        found = set()
        for node in document["nodes"]:
            name = node.get("name")
            if name in identities and "mesh" in node:
                node.setdefault("extras", {})["aikea"] = identities[name]
                found.add(name)
        if found != identities.keys():
            raise UnitMockupInputError([
                "exported inspection parts are missing: " + ", ".join(sorted(identities.keys() - found))
            ])
        GlbPanelMaterialDefaults().apply(document)
        encoded = json.dumps(document, separators=(",", ":")).encode("utf-8")
        encoded += b" " * (-len(encoded) % 4)
        chunk = struct.pack("<II", len(encoded), 0x4E4F534A) + encoded
        payload = chunk + snapshot.content[json_end:]
        output.write_bytes(struct.pack("<4sII", b"glTF", 2, 12 + len(payload)) + payload)
