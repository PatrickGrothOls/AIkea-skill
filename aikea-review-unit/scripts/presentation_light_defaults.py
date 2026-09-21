"""Scope: Apply approved representative LED output to a geometry-identical bake input."""

import json
from pathlib import Path
import struct
from glb_artifact_snapshot import GlbArtifactSnapshot


class PresentationLightDefaults:
    REPRESENTATIVE_STRENGTH = 40
    EXTENSION = "KHR_materials_emissive_strength"

    def prepare(self, source, directory):
        snapshot = GlbArtifactSnapshot.load(Path(source))
        length = struct.unpack_from("<I", snapshot.content, 12)[0]
        document = json.loads(snapshot.content[20:20 + length])
        changed = []
        for index, material in enumerate(document.get("materials", [])):
            provenance = material.get("extras", {}).get("aikea", {})
            # Only explicitly representative emitters use this fallback. Product
            # calibration, deliberate overrides and ordinary surfaces are untouched.
            eligible = (
                provenance.get("appearance_status") == "representative_output",
                provenance.get("photometric_calibration") is False,
                not provenance.get("preserve_emission", False),
                any(material.get("emissiveFactor", [])),
            )
            if not all(eligible):
                continue
            extensions = material.setdefault("extensions", {})
            current = extensions.get(self.EXTENSION, {}).get("emissiveStrength", 1)
            if current == self.REPRESENTATIVE_STRENGTH:
                continue
            extensions[self.EXTENSION] = {"emissiveStrength": self.REPRESENTATIVE_STRENGTH}
            changed.append({"material": index, "previous_strength": current,
                            "representative_strength": self.REPRESENTATIVE_STRENGTH})
        if not changed:
            return snapshot.path
        used = document.setdefault("extensionsUsed", [])
        if self.EXTENSION not in used:
            used.append(self.EXTENSION)
        encoded = json.dumps(document, separators=(",", ":")).encode()
        encoded += b" " * (-len(encoded) % 4)
        # Keep every non-JSON chunk byte-for-byte, including mesh and image data.
        tail = snapshot.content[20 + length:]
        chunks = struct.pack("<II", len(encoded), 0x4E4F534A) + encoded + tail
        target = Path(directory) / "inspection-materials.glb"
        target.write_bytes(struct.pack("<4sII", b"glTF", 2, 12 + len(chunks)) + chunks)
        report = {"original_source": str(snapshot.path), "original_sha256": snapshot.sha256,
                  "inspection_model": str(target.resolve()), "changed_materials": changed,
                  "non_json_chunks_unchanged": True, "photometric_calibration": False}
        (Path(directory) / "lighting-defaults.json").write_text(json.dumps(report, indent=2))
        return target.resolve()
