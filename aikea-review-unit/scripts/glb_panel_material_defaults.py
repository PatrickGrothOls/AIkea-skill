"""Scope: Give CAD panel colours an explicit nonmetal default without changing hardware."""

from copy import deepcopy


class GlbPanelMaterialDefaults:
    """CAD colours are placeholders; selected presentation materials remain authoritative."""

    def apply(self, document):
        panels = [node for node in document['nodes'] if 'mesh' in node
                  and node.get('extras', {}).get('aikea', {}).get('kind') == 'panel']
        other_meshes = {node['mesh'] for node in document['nodes'] if 'mesh' in node
                        and node.get('extras', {}).get('aikea', {}).get('kind') != 'panel'}
        materials = document.get('materials', [])
        converted = {}
        for node in panels:
            mesh = document['meshes'][node['mesh']]
            if not any('material' in part and 'metallicFactor' not in
                       materials[part['material']].get('pbrMetallicRoughness', {})
                       for part in mesh['primitives']):
                continue
            if node['mesh'] in other_meshes:
                mesh = deepcopy(mesh)
                node['mesh'] = len(document['meshes'])
                document['meshes'].append(mesh)
            for primitive in mesh['primitives']:
                if 'material' not in primitive:
                    continue
                index = primitive['material']
                material = materials[index]
                if 'metallicFactor' in material.get('pbrMetallicRoughness', {}):
                    continue
                if index not in converted:
                    material = deepcopy(material)
                    material.setdefault('pbrMetallicRoughness', {})['metallicFactor'] = 0.0
                    converted[index] = len(materials)
                    materials.append(material)
                primitive['material'] = converted[index]
