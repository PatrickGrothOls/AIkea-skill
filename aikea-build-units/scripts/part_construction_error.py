"""Scope: Report generated parts that cannot use the supported construction path."""


class PartConstructionError(ValueError):
    """Report a generated part that has no supported construction method."""


__all__ = ["PartConstructionError"]
