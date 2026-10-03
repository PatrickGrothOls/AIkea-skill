"""Scope: Bound and verify PNG structure without decoding or rendering images."""

import struct
import zlib


class PreviewValidation:
    def validate(self, content):
        if not 45 <= len(content) <= 4_000_000 or content[:8] != b"\x89PNG\r\n\x1a\n":
            raise ValueError("Invalid or oversized PNG preview.")
        offset, kinds = 8, []
        while offset + 12 <= len(content):
            size = struct.unpack(">I", content[offset:offset + 4])[0]
            kind = content[offset + 4:offset + 8]
            end = offset + 12 + size
            if end > len(content):
                raise ValueError("Truncated PNG preview.")
            chunk = content[offset + 4:end - 4]
            crc = struct.unpack(">I", content[end - 4:end])[0]
            if zlib.crc32(chunk) != crc or kind not in {b"IHDR", b"PLTE", b"IDAT", b"IEND", b"tRNS", b"sRGB", b"gAMA", b"pHYs"}:
                raise ValueError("Unsupported PNG chunk or invalid checksum.")
            kinds.append(kind)
            if kind == b"IHDR":
                if size != 13 or len(kinds) != 1:
                    raise ValueError("Invalid PNG header.")
                width, height = struct.unpack(">II", content[offset + 8:offset + 16])
                if not 0 < width <= 4096 or not 0 < height <= 4096 or width * height > 8_000_000:
                    raise ValueError("Preview dimensions exceed limits.")
            if kind == b"IEND" and (size != 0 or end != len(content)):
                raise ValueError("Invalid PNG ending.")
            offset = end
        if offset != len(content) or not kinds or kinds[0] != b"IHDR" or kinds[-1] != b"IEND" or b"IDAT" not in kinds:
            raise ValueError("Incomplete PNG preview.")
