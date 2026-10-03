"""Scope: Compare AIkea semantic release tags including numeric prerelease identifiers."""

from dataclasses import dataclass
import re


@dataclass(frozen=True, order=True)
class SkillReleaseVersion:
    major: int
    minor: int
    patch: int
    prerelease_order: tuple

    @classmethod
    def parse(cls, tag):
        match = re.fullmatch(r"v?(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
                             r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
                             r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?", tag)
        if not match:
            raise ValueError("release tag is not a semantic version")
        pre = match[4]
        identifiers = pre.split(".") if pre else []
        if any(item.isdigit() and len(item) > 1 and item.startswith("0") for item in identifiers):
            raise ValueError("numeric prerelease identifiers cannot have leading zeros")
        order = (0, tuple((0, int(item)) if item.isdigit() else (1, item) for item in identifiers)) if pre else (1,)
        return cls(*(int(match[index]) for index in (1, 2, 3)), order)
