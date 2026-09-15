"""Scope: Stage the unchanged furniture with a neutral floor, camera, and soft studio light."""

import bpy
from mathutils import Vector


class BlenderFurnitureStudio:
    def __init__(self, source):
        self.source = source
        self.center = source.center
        self.scale = max(source.maximum-source.minimum)/1.45

    def build(self):
        scene = bpy.context.scene
        scene.unit_settings.system = 'METRIC'
        world = bpy.data.worlds.new('Soft ambient studio')
        world.use_nodes = True
        world.node_tree.nodes['Background'].inputs[0].default_value = (0.78,0.84,1,1)
        world.node_tree.nodes['Background'].inputs[1].default_value = 0.18
        scene.world = world
        self.area('Large window', (-2.8,-3.0,3.5), 500, 3.0, (1,0.90,0.78))
        self.area('Gentle fill', (3.0,-0.2,2.0), 100, 2.4, (0.83,0.91,1))
        self.area('Top softbox', (0.3,1.5,3.8), 200, 2.0, (1,0.96,0.89))
        bpy.ops.mesh.primitive_plane_add(size=200*self.scale, location=(self.center.x,self.center.y,self.source.minimum.z-0.001*self.scale))
        floor = bpy.context.object
        floor.name = 'STUDIO_floor_not_a_furniture_part'
        material = bpy.data.materials.new('Warm neutral studio floor')
        material.use_nodes = True
        bsdf = material.node_tree.nodes['Principled BSDF']
        bsdf.inputs['Base Color'].default_value = (0.43,0.40,0.35,1)
        bsdf.inputs['Roughness'].default_value = 0.9
        floor.data.materials.append(material)
        bpy.ops.object.camera_add(location=self.center+Vector((2.25,-3.8,1.25))*self.scale)
        camera = bpy.context.object
        camera.name = 'Furniture three-quarter view'
        camera.rotation_euler = (self.center-camera.location).to_track_quat('-Z','Y').to_euler()
        camera.data.lens = 60
        camera.data.clip_end = 500
        camera.data.dof.use_dof = False
        scene.camera = camera
        scene.render.engine = 'CYCLES'
        scene.cycles.device = 'CPU'
        scene.cycles.samples = 48
        scene.cycles.use_denoising = True
        scene.cycles.max_bounces = 6
        scene.cycles.diffuse_bounces = 4
        scene.cycles.glossy_bounces = 4
        scene.render.threads_mode = 'FIXED'
        scene.render.threads = 3
        scene.render.resolution_x = 1100
        scene.render.resolution_y = 800
        scene.render.resolution_percentage = 100
        scene.render.image_settings.file_format = 'PNG'
        scene.view_settings.view_transform = 'AgX'
        scene.view_settings.look = 'AgX - Medium High Contrast'
        scene.view_settings.exposure = 0.1
        scene.render.film_transparent = False
        return scene

    def area(self, name, offset, power, size, color):
        light = bpy.data.lights.new(name, 'AREA')
        light.energy = power*self.scale**2
        light.shape = 'DISK'
        light.size = size*self.scale
        light.color = color
        obj = bpy.data.objects.new(name, light)
        bpy.context.collection.objects.link(obj)
        obj.location = self.center+Vector(offset)*self.scale
        obj.rotation_euler = (self.center-obj.location).to_track_quat('-Z','Y').to_euler()

    def prepare_viewport(self):
        camera = bpy.context.scene.camera
        bpy.ops.object.select_all(action='DESELECT')
        for screen in bpy.data.screens:
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    space = area.spaces.active
                    space.overlay.show_overlays = False
                    space.shading.type = 'RENDERED'
                    space.shading.use_scene_world = True
                    space.shading.use_scene_lights = True
                    space.region_3d.view_perspective = 'PERSP'
                    space.region_3d.view_location = self.center
                    space.region_3d.view_rotation = camera.rotation_euler.to_quaternion()
                    space.region_3d.view_distance = (camera.location-self.center).length
                    space.clip_end = 500
