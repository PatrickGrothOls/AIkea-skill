"""Scope: Verify approved default compartment lighting in Blender without an expensive bake."""

from pathlib import Path
import sys
from types import SimpleNamespace
import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "aikea-review-unit/scripts"))
from blender_furniture_studio import BlenderFurnitureStudio


class StudioAcceptance:
    def run(self):
        for multiplier in (1, 2):
            bpy.ops.wm.read_factory_settings(use_empty=True)
            source = SimpleNamespace(minimum=Vector((0, 0, 0)),
                                     maximum=Vector((2.4, .6, 2.4)) * multiplier)
            source.center = (source.minimum + source.maximum) / 2
            studio = BlenderFurnitureStudio(source)
            scene = studio.build()
            lights = [obj for obj in scene.objects if obj.type == "LIGHT"]
            assert len(lights) == 3
            for name in ("Large window", "Gentle fill"):
                light = bpy.data.objects[name]
                assert light.location.y < source.minimum.y
                direction = light.rotation_euler.to_quaternion() @ Vector((0, 0, -1))
                toward = (source.center - light.location).normalized()
                assert direction.dot(toward) > .999
            fill = bpy.data.objects["Gentle fill"]
            assert abs(fill.data.energy / studio.scale ** 2 - 300) < .001
            assert abs(fill.data.size / studio.scale - 3.2) < .001
            background = scene.world.node_tree.nodes["Background"]
            assert abs(background.inputs[1].default_value - .3) < .0001
            assert scene.view_settings.look == "AgX - Medium Low Contrast"
            assert scene.cycles.diffuse_bounces == 4
        print("STUDIO_DEFAULTS_PASS: frontal fill, aim, scale and contrast verified")


if __name__ == "__main__":
    StudioAcceptance().run()
