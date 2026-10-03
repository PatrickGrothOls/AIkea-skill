"""Scope: Render the exact shared hinge purchase declarations as editable project source."""
from riex_nc70_hardware_specs import RiexNc70HardwareSpecs


class DoorHardwareSpecRenderer:
    def render(self, assembly, plan, profile):
        hardware = RiexNc70HardwareSpecs().build(assembly, plan, profile)
        return ('"""Scope: Declare exact purchased hinge instances."""\n\n'
                'from assemblies.specification import AxisBasis, AxisDirection, LocalToParentPlacement, Point3D\n'
                'from purchased_hardware_spec import PurchasedHardwareSpec, HardwarePurchaseSpec\n\n'
                'DOOR_HARDWARE = (\n'+''.join(f"    {item!r},\n" for item in hardware)+')\n')
