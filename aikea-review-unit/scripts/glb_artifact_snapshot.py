"""Scope: Load and validate immutable bytes for one GLB v2 artifact."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
import struct

from unit_mockup import UnitMockupInputError


@dataclass(frozen=True, slots=True)
class GlbArtifactSnapshot:
    """Bind a resolved path, validated GLB bytes, and their SHA-256 digest."""

    path: Path
    content: bytes
    sha256: str

    @classmethod
    def load(cls, path: Path) -> "GlbArtifactSnapshot":
        resolved = path.resolve()
        try:
            content = resolved.read_bytes()
        except OSError as error:
            raise UnitMockupInputError([f"GLB cannot be read: {resolved}"]) from error
        header = content[:12]
        if len(header) != 12:
            raise UnitMockupInputError([f"GLB has an invalid header: {resolved}"])
        magic, version, declared_length = struct.unpack("<4sII", header)
        if magic != b"glTF" or version != 2 or declared_length != len(content):
            raise UnitMockupInputError([f"GLB has an invalid header: {resolved}"])
        cls._validate_chunks(resolved, content)
        return cls(resolved, content, sha256(content).hexdigest())

    @staticmethod
    def _validate_chunks(path: Path, content: bytes) -> None:
        chunks = []
        offset = 12
        while offset < len(content):
            if offset + 8 > len(content):
                raise UnitMockupInputError([f"GLB has an invalid chunk: {path}"])
            length, chunk_type = struct.unpack("<II", content[offset : offset + 8])
            offset += 8
            end = offset + length
            if length % 4 or end > len(content):
                raise UnitMockupInputError([f"GLB has an invalid chunk: {path}"])
            chunks.append((chunk_type, content[offset:end]))
            offset = end
        if not chunks or chunks[0][0] != 0x4E4F534A:
            raise UnitMockupInputError([f"GLB is missing its JSON scene: {path}"])
        try:
            document = json.loads(chunks[0][1].rstrip(b" \x00").decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise UnitMockupInputError([f"GLB has invalid JSON: {path}"]) from error
        scenes = document.get("scenes") if isinstance(document, dict) else None
        scene = document.get("scene") if isinstance(document, dict) else None
        asset = document.get("asset") if isinstance(document, dict) else None
        if (
            not isinstance(asset, dict)
            or asset.get("version") != "2.0"
            or not isinstance(scenes, list)
            or not scenes
            or not isinstance(scene, int)
            or scene not in range(len(scenes))
        ):
            raise UnitMockupInputError([f"GLB has no valid default scene: {path}"])
        if not GlbArtifactSnapshot._default_scene_has_reachable_mesh(
            document,
            scenes[scene],
        ):
            raise UnitMockupInputError(
                [f"GLB has no renderable default scene: {path}"]
            )

    @staticmethod
    def _default_scene_has_reachable_mesh(document: dict, scene: object) -> bool:
        nodes = document.get("nodes")
        meshes = document.get("meshes")
        roots = scene.get("nodes") if isinstance(scene, dict) else None
        if (
            not isinstance(nodes, list)
            or not isinstance(meshes, list)
            or not isinstance(roots, list)
            or not roots
        ):
            return False
        pending = list(roots)
        visited: set[int] = set()
        has_mesh = False
        while pending:
            node_index = pending.pop()
            if (
                type(node_index) is not int
                or node_index not in range(len(nodes))
            ):
                return False
            if node_index in visited:
                continue
            visited.add(node_index)
            node = nodes[node_index]
            if not isinstance(node, dict):
                return False
            mesh_index = node.get("mesh")
            if mesh_index is not None:
                if (
                    type(mesh_index) is not int
                    or mesh_index not in range(len(meshes))
                    or not GlbArtifactSnapshot._has_mesh_primitives(
                        meshes[mesh_index]
                    )
                ):
                    return False
                has_mesh = True
            children = node.get("children", [])
            if not isinstance(children, list):
                return False
            pending.extend(children)
        return has_mesh

    @staticmethod
    def _has_mesh_primitives(mesh: object) -> bool:
        primitives = mesh.get("primitives") if isinstance(mesh, dict) else None
        return (
            isinstance(primitives, list)
            and bool(primitives)
            and all(
                isinstance(primitive, dict)
                and isinstance(primitive.get("attributes"), dict)
                and type(primitive["attributes"].get("POSITION")) is int
                for primitive in primitives
            )
        )


__all__ = ["GlbArtifactSnapshot"]
