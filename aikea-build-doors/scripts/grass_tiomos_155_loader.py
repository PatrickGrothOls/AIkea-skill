"""Scope: Import unchanged public GRASS hinge/plate CAD and verify native geometry."""
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
import cadquery as cq


@dataclass(frozen=True)
class GrassTiomos155Sources:
    hinge: object
    plate: object


class GrassTiomos155Loader:
    records=(
        ('tiomos-155-plus/f028122660/source/F028122660_TIOMOS 155 PLUS_C03_DRILL 45_9-5_SCREW.step',
         '823644b3ec2683fb40307bf66154c6e2c5c80d43cb28b4bc4e1b6a8f66bd8c2a',
         (-13,53.953542539,-49.5,42.71394913,-31,31)),
        ('tiomos-1d-cross-plate/f058139748/source/F058139748_TIOMOS 1D CROSS PLATE_H03_DRILL 37_SCREW.step',
         '8a043f77f0c595d8dc621d670218218732555c15f1879b905f55c6d4c0180c84',
         (-3,10.5,-25.55,39.95,-24,24)))

    def load(self, grass_root: Path):
        items=[]
        for name, checksum, expected in self.records:
            path=grass_root/name
            if sha256(path.read_bytes()).hexdigest()!=checksum:
                raise ValueError('GRASS source bytes differ: '+name)
            solid=cq.importers.importStep(str(path)).val()
            box=solid.BoundingBox()
            bounds=(box.xmin,box.xmax,box.ymin,box.ymax,box.zmin,box.zmax)
            if (not solid.isValid() or len(solid.Solids())!=1 or
                    any(abs(a-b)>1e-5 for a,b in zip(bounds,expected))):
                raise ValueError('GRASS source geometry differs: '+name)
            items.append(solid)
        return GrassTiomos155Sources(*items)
