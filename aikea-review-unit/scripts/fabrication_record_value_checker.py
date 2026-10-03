"""Scope: Compare fabrication record values with closed-tree physical values."""

from __future__ import annotations

from math import isclose, isfinite


class FabricationRecordValueChecker:
    """Validate quantities, identities, dimensions, and declared joint machining."""

    _TOLERANCE_MM = 1e-6

    def part_bom_problems(self, evidence, rows) -> tuple[str, ...]:
        return tuple(
            item.path
            for item in evidence.parts
            if item.path in rows
            and not (
                self._text(getattr(item.part.spec, "material_id", None))
                and rows[item.path].get("material") == item.part.spec.material_id
                and self._same(
                    rows[item.path].get("thickness_mm"),
                    item.part.spec.local_size_mm[2],
                )
                and self._quantity_one(rows[item.path].get("quantity"))
            )
        )

    def hardware_bom_problems(self, evidence, rows) -> tuple[str, ...]:
        return tuple(
            item.path
            for item in evidence.hardware
            if item.path in rows
            and not (
                rows[item.path].get("manufacturer")
                == item.hardware.spec.manufacturer
                and rows[item.path].get("product_code")
                == item.hardware.spec.product_code
                and self._quantity_one(rows[item.path].get("quantity"))
            )
        )

    def cut_list_problems(self, evidence, rows, bom_rows) -> tuple[str, ...]:
        return tuple(
            item.path
            for item in evidence.parts
            if item.path in rows
            and not self._valid_cut_row(item, rows[item.path], bom_rows.get(item.path))
        )

    def machining_problems(self, evidence, rows) -> tuple[str, ...]:
        return tuple(
            item.path
            for item in evidence.parts
            if item.path in rows
            and not self._valid_operations(rows[item.path].get("operations"), item.joint_ids)
        )

    def _valid_cut_row(self, item, row, bom_row) -> bool:
        width_mm, height_mm, thickness_mm = item.part.spec.local_size_mm
        material_id = getattr(item.part.spec, "material_id", None)
        return bool(
            bom_row
            and self._text(material_id)
            and row.get("material") == material_id
            and bom_row.get("material") == material_id
            and self._same(row.get("thickness_mm"), thickness_mm)
            and self._quantity_one(row.get("quantity"))
            and self._same(row.get("blank_width_mm"), width_mm)
            and self._same(row.get("blank_height_mm"), height_mm)
        )

    def _valid_operations(self, operations, joint_ids) -> bool:
        if not isinstance(operations, list):
            return False
        valid = all(
            isinstance(item, dict)
            and (
                self._text(item.get("operation_id"))
                or self._text(item.get("joint_id"))
            )
            for item in operations
        )
        declared_joint_ids = tuple(
            item.get("joint_id")
            for item in operations
            if isinstance(item, dict) and item.get("joint_id")
        )
        operation_ids = tuple(
            item.get("joint_id") or item.get("operation_id")
            for item in operations
            if isinstance(item, dict)
        )
        return bool(
            valid
            and len(operation_ids) == len(set(operation_ids))
            and len(declared_joint_ids) == len(set(declared_joint_ids))
            and set(declared_joint_ids) == set(joint_ids)
        )

    def _same(self, actual, expected) -> bool:
        return bool(
            self._positive_number(actual)
            and isclose(
                float(actual),
                float(expected),
                rel_tol=0.0,
                abs_tol=self._TOLERANCE_MM,
            )
        )

    def _quantity_one(self, value) -> bool:
        return self._positive_number(value) and float(value) == 1.0

    def _positive_number(self, value) -> bool:
        return bool(
            not isinstance(value, bool)
            and isinstance(value, (int, float, str))
            and self._finite_positive_float(value)
        )

    def _finite_positive_float(self, value) -> bool:
        try:
            number = float(value)
        except (TypeError, ValueError):
            return False
        return isfinite(number) and number > 0.0

    def _text(self, value) -> bool:
        return isinstance(value, str) and bool(value.strip())


__all__ = ["FabricationRecordValueChecker"]
