"""Scope: Preserve closed-tree panel and purchase ownership on exact alternate Riex poses."""

from dataclasses import replace


class RiexReviewIdentity:
    def apply(self, parts, assembly, plan):
        hardware = {item.spec.hardware_id: item.spec for item in assembly.purchased_hardware}
        names = {f'{item.hinge_id}{suffix}__source_cad': f'{item.hinge_id}_{kind}'
                 for item in plan.placements
                 for suffix, kind in (('', 'hinge'), ('_plate', 'plate'))}
        result = []
        for part in parts:
            if part.name == plan.door_part_id:
                result.append(replace(part, inspection_path=(plan.door_part_id,), review_kind='panel'))
            elif part.name in names:
                spec = hardware[names[part.name]]
                mounting = getattr(spec, 'mounting_part_id', None)
                path = (mounting, spec.hardware_id) if mounting else (spec.hardware_id,)
                asset = ('riex-nc70-f000001-open' if spec.product_code == 'F000001'
                         else spec.hardware_asset_id)
                result.append(replace(part, inspection_path=path, review_kind='hardware',
                                      source_hardware_asset_id=asset,
                                      source_geometry_selector=spec.geometry_selector))
        return tuple(result)
