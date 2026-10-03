"""Scope: Require the real background engine, Cycles and glTF IO before a bake."""

import bpy


class BlenderEngineProbe:
    def run(self):
        if bpy.app.version[:3] != (5, 2, 1) or not bpy.app.background:
            raise RuntimeError("AIkea requires the Blender 5.2.1 background engine")
        if not bpy.app.build_options.cycles:
            raise RuntimeError("This Blender engine has no Cycles renderer")
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.preferences.addon_enable(module="io_scene_gltf2")
        bpy.ops.import_scene.gltf.get_rna_type()
        bpy.ops.export_scene.gltf.get_rna_type()
        print("ENGINE_READY Blender 5.2.1, background, Cycles, glTF import/export", flush=True)


if __name__ == "__main__":
    BlenderEngineProbe().run()
