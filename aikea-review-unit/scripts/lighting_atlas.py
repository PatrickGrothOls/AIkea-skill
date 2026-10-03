"""Scope: Give the furniture panels unique bake UVs and one bounded lighting atlas."""

import math
import bpy


class LightingAtlas:
    def __init__(self, panels, size=4096):
        self.panels = panels
        self.image = bpy.data.images.new('Assembled diffuse lighting', width=size, height=size)
        self.image.colorspace_settings.name = 'sRGB'
        self.image.generated_color = (0,0,0,1)

    def prepare(self):
        bpy.ops.object.select_all(action='DESELECT')
        materials = set()
        for obj in self.panels:
            original = obj.data.uv_layers.active
            old_name = original.name
            original.name = 'SourceMaterialUV'
            for material in obj.data.materials:
                for node in material.node_tree.nodes:
                    if node.type in {'UVMAP', 'NORMAL_MAP'} and node.uv_map == old_name:
                        node.uv_map = 'SourceMaterialUV'
            obj.data.uv_layers.new(name='BakedLightingUV')
            obj.data.uv_layers.active_index = len(obj.data.uv_layers)-1
            original.active_render = True
            obj.select_set(True)
            materials.update(slot.material for slot in obj.material_slots)
        for material in materials:
            nodes = material.node_tree.nodes
            source = nodes.new('ShaderNodeUVMap')
            source.uv_map = 'SourceMaterialUV'
            for node in list(nodes):
                if node.type == 'TEX_IMAGE' and not node.inputs['Vector'].is_linked:
                    material.node_tree.links.new(source.outputs['UV'], node.inputs['Vector'])
                if node.type == 'NORMAL_MAP':
                    node.uv_map = 'SourceMaterialUV'
            target = nodes.new('ShaderNodeTexImage')
            target.name = 'Assembled lighting bake target'
            target.image = self.image
            nodes.active = target
        bpy.context.view_layer.objects.active = self.panels[0]
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.002)
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.pack_islands(rotate=True, margin=0.002)
        bpy.ops.object.mode_set(mode='OBJECT')

    def apply(self):
        material = bpy.data.materials.new('Assembled baked panel lighting')
        material.use_nodes = True
        material['aikea'] = {'material_id':'ASSEMBLED_DIFFUSE_LIGHTING',
            'appearance_status':'baked_from_source_materials',
            'presentation_state':'assembled_only'}
        nodes = material.node_tree.nodes
        nodes.clear()
        output = nodes.new('ShaderNodeOutputMaterial')
        emission = nodes.new('ShaderNodeEmission')
        texture = nodes.new('ShaderNodeTexImage')
        texture.image = self.image
        uv = nodes.new('ShaderNodeUVMap')
        uv.uv_map = 'BakedLightingUV'
        for first, second in [(uv.outputs['UV'],texture.inputs['Vector']),
                (texture.outputs['Color'],emission.inputs['Color']),
                (emission.outputs[0],output.inputs['Surface'])]:
            material.node_tree.links.new(first, second)
        for obj in self.panels:
            obj.data.materials.clear()
            obj.data.materials.append(material)
            obj.data.uv_layers['BakedLightingUV'].active_render = True
