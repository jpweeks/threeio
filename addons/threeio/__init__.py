import os
import json

import bpy
from bpy_extras.io_utils import ExportHelper
from bpy.props import (
    EnumProperty,
    BoolProperty,
    FloatProperty,
    IntProperty
)

from . import constants

SETTINGS_FILE_EXPORT = 'threeio_settings_export.js'


bl_info = {
    'name': 'ThreeIO',
    'author': 'Ed Caspersen',
    'version': (0, 2, 1),
    'blender': (2, 7, 1),
    'location': 'File > Import-Export',
    'description': 'Export ThreeJs scenes',
    'warning': '',
    'wiki_url': 'https://github.com/repsac/threeio/wiki',
    'tracker_url':  'https://github.com/repsac/threeio/issues',
    'category': 'Import-Export'
}

def _blending_types(index):
    types = (constants.BLENDING.NONE, constants.BLENDING.NORMAL, 
        constants.BLENDING.ADDITIVE, constants.BLENDING.SUBTRACTIVE, 
        constants.BLENDING.MULTIPLY, constants.BLENDING.CUSTOM)
    return (types[index], types[index], types[index])

bpy.types.Material.THREE_blending_type = EnumProperty(
    name='Blending type', 
    description='Blending type', 
    items=[_blending_types(x) for x in range(5)], 
    default=constants.BLENDING.NORMAL)

bpy.types.Material.THREE_depth_write = BoolProperty(default=True)
bpy.types.Material.THREE_depth_test = BoolProperty(default=True)


class MATERIAL_PT_hello(bpy.types.Panel):

    bl_label = 'THREE'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'material'
    
    def draw(self, context):
        layout = self.layout
        mat = context.material

        row = layout.row()
        row.label(text='Selected material: %s' % mat.name )

        row = layout.row()
        row.prop(mat, 'THREE_blending_type', text='Blending type' )

        row = layout.row()
        row.prop(mat, 'THREE_depth_write', text='Enable depth writing' )

        row = layout.row()
        row.prop(mat, 'THREE_depth_test', text='Enable depth testing' )


def get_settings_fullpath():
    return os.path.join(bpy.app.tempdir, SETTINGS_FILE_EXPORT)


def save_settings_export(properties):

    settings = {
        constants.VERTICES: properties.option_vertices,
        constants.FACES: properties.option_faces,
        constants.NORMALS: properties.option_normals,
        constants.SKINNING: properties.option_skinning,
        constants.BONES: properties.option_bones,

        constants.MATERIALS: properties.option_materials,
        constants.UVS: properties.option_uv_coords,
        constants.FACE_MATERIALS: properties.option_face_materials,
        constants.MAPS: properties.option_maps,
        constants.COLORS: properties.option_colors,
        constants.MIX_COLORS: properties.option_mix_colors,

        constants.SCALE: properties.option_scale,
        constants.ROUND_OFF: properties.option_round_off,
        constants.ROUND_VALUE: properties.option_round_value,
        constants.LOGGING: properties.option_logging,
        constants.COPY_TEXTURES: properties.option_copy_textures,

        constants.SCENE: properties.option_export_scene,
        constants.EMBED: properties.option_embed_meshes,
        constants.LIGHTS: properties.option_lights,
        constants.CAMERAS: properties.option_cameras,

        constants.MORPH_TARGETS: properties.option_animation_morph,
        constants.ANIMATION: properties.option_animation_skeletal,
        constants.FRAME_STEP: properties.option_frame_step
    }

    fname = get_settings_fullpath()
    with open(fname, 'w') as stream:
        json.dump(settings, stream)

    return settings


def restore_settings_export(properties):

    settings = {}

    fname = get_settings_fullpath()
    if os.path.exists(fname) and os.access(fname, os.R_OK):
        f = open(fname, 'r')
        settings = json.load(f)

    ## Geometry {
    properties.option_vertices = settings.get(
        constants.VERTICES, constants.EXPORT_OPTIONS[constants.VERTICES])
    properties.option_faces = settings.get(
        constants.FACES, constants.EXPORT_OPTIONS[constants.FACES])
    properties.option_normals = settings.get(
        constants.NORMALS, constants.EXPORT_OPTIONS[constants.NORMALS])

    properties.option_skinning = settings.get(
        constants.SKINNING, constants.EXPORT_OPTIONS[constants.SKINNING])
    properties.option_bones = settings.get(
        constants.BONES, constants.EXPORT_OPTIONS[constants.BONES])
    ## }

    ## Materials {
    properties.option_materials = settings.get(
        constants.MATERIALS, constants.EXPORT_OPTIONS[constants.MATERIALS])
    properties.option_uv_coords = settings.get(
        constants.UVS, constants.EXPORT_OPTIONS[constants.UVS])
    properties.option_face_materials = settings.get(
        constants.FACE_MATERIALS, constants.EXPORT_OPTIONS[constants.FACE_MATERIALS])
    properties.option_maps = settings.get(
        constants.MAPS, constants.EXPORT_OPTIONS[constants.MAPS])
    properties.option_colors = settings.get(
        constants.COLORS, constants.EXPORT_OPTIONS[constants.COLORS])
    properties.option_mix_colors = settings.get(
        constants.MIX_COLORS, constants.EXPORT_OPTIONS[constants.MIX_COLORS])
    ## }

    ## Settings {
    properties.option_scale = settings.get(
        constants.SCALE, constants.EXPORT_OPTIONS[constants.SCALE])
    properties.option_round_off = settings.get(
        constants.ROUND_OFF, constants.EXPORT_OPTIONS[constants.ROUND_OFF])
    properties.option_round_value = settings.get(
        constants.ROUND_VALUE, constants.EXPORT_OPTIONS[constants.ROUND_VALUE])
    properties.option_logging = settings.get(
        constants.LOGGING, constants.EXPORT_OPTIONS[constants.LOGGING])
    properties.option_copy_textures = settings.get(
        constants.COPY_TEXTURES, constants.EXPORT_OPTIONS[constants.COPY_TEXTURES])
    ## }

    ## Scene {
    properties.option_export_scene = settings.get(
        constants.SCENE, constants.EXPORT_OPTIONS[constants.SCENE])
    properties.option_embed_meshes = settings.get(
        constants.EMBED, constants.EXPORT_OPTIONS[constants.EMBED])
    properties.option_lights = settings.get(
        constants.LIGHTS, constants.EXPORT_OPTIONS[constants.LIGHTS])
    properties.option_cameras = settings.get(
        constants.CAMERAS, constants.EXPORT_OPTIONS[constants.CAMERAS])
    ## }

    ## Animation {
    properties.option_animation_morph = settings.get(
        constants.MORPH_TARGETS, constants.EXPORT_OPTIONS[constants.MORPH_TARGETS])
    properties.option_animation_skeletal = settings.get(
        constants.ANIMATION, constants.EXPORT_OPTIONS[constants.ANIMATION])
    #properties.option_frame_index_as_time = settings.get(
    #    'option_frame_index_as_time', False)

    properties.option_frame_step = settings.get(
        constants.FRAME_STEP, constants.EXPORT_OPTIONS[constants.FRAME_STEP])
    ## }


class ExportThreeIO(bpy.types.Operator, ExportHelper):

    bl_idname='export.threeio'
    bl_label = 'Export ThreeIO'

    filename_ext = constants.EXTENSION

    option_vertices = BoolProperty(
        name='Vertices', 
        description='Export vertices', 
        default=constants.EXPORT_OPTIONS[constants.VERTICES])

    option_faces = BoolProperty(
        name='Faces', 
        description='Export faces', 
        default=constants.EXPORT_OPTIONS[constants.FACES])

    option_normals = BoolProperty(
        name='Normals', 
        description='Export normals', 
        default=constants.EXPORT_OPTIONS[constants.NORMALS])

    option_colors = BoolProperty(
        name='Colors', 
        description='Export vertex colors', 
        default=constants.EXPORT_OPTIONS[constants.COLORS])

    option_mix_colors = BoolProperty(
        name='Mix Colors',
        description='Mix material and vertex colors',
        default=constants.EXPORT_OPTIONS[constants.MIX_COLORS])

    option_uv_coords = BoolProperty(
        name='UVs', 
        description='Export texture coordinates', 
        default=constants.EXPORT_OPTIONS[constants.UVS])

    option_materials = BoolProperty(
        name='Materials', 
        description='Export materials', 
        default=constants.EXPORT_OPTIONS[constants.MATERIALS])

    option_face_materials = BoolProperty(
        name='Face Materials',
        description='Face mapping materials',
        default=constants.EXPORT_OPTIONS[constants.FACE_MATERIALS])

    option_maps = BoolProperty(
        name='Textures',
        description='Include texture maps',
        default=constants.EXPORT_OPTIONS[constants.MAPS])

    option_skinning = BoolProperty(
        name='Skinning', 
        description='Export skin data', 
        default=constants.EXPORT_OPTIONS[constants.SKINNING])

    option_bones = BoolProperty(
        name='Bones', 
        description='Export bones', 
        default=constants.EXPORT_OPTIONS[constants.BONES])

    option_scale = FloatProperty(
        name='Scale', 
        description='Scale vertices', 
        min=0.01, 
        max=1000.0, 
        soft_min=0.01, 
        soft_max=1000.0, 
        default=constants.EXPORT_OPTIONS[constants.SCALE])

    option_round_off = BoolProperty(
        name='Round Off',
        description='Round of floating point values',
        default=constants.EXPORT_OPTIONS[constants.ROUND_OFF])

    option_round_value = IntProperty(
        name='Precision',
        min=0,
        max=16,
        description='Floating point precision',
        default=constants.EXPORT_OPTIONS[constants.ROUND_VALUE])

    logging_types = [
        (constants.DEBUG, constants.DEBUG, constants.DEBUG),
        (constants.INFO, constants.INFO, constants.INFO),
        (constants.WARNING, constants.WARNING, constants.WARNING),
        (constants.ERROR, constants.ERROR, constants.ERROR),
        (constants.CRITICAL, constants.CRITICAL, constants.CRITICAL)]

    option_logging = EnumProperty(
        name='Logging', 
        description = 'Logging verbosity level', 
        items=logging_types, 
        default=constants.DEBUG)


    option_export_scene = BoolProperty(
        name='Scene', 
        description='Export scene', 
        default=constants.EXPORT_OPTIONS[constants.SCENE])

    option_embed_meshes = BoolProperty(
        name='Embed meshes', 
        description='Embed meshes', 
        default=constants.EXPORT_OPTIONS[constants.EMBED])

    option_copy_textures = BoolProperty(
        name='Copy textures', 
        description='Copy textures', 
        default=constants.EXPORT_OPTIONS[constants.COPY_TEXTURES])

    option_lights = BoolProperty(
        name='Lights', 
        description='Export default scene lights', 
        default=False)

    option_cameras = BoolProperty(
        name='Cameras', 
        description='Export default scene cameras', 
        default=False)

    option_animation_morph = BoolProperty(
        name='Morph animation', 
        description='Export animation (morphs)', 
        default=constants.EXPORT_OPTIONS[constants.MORPH_TARGETS])

    option_animation_skeletal = BoolProperty(
        name='Skeletal animation', 
        description='Export animation (skeletal)', 
        default=constants.EXPORT_OPTIONS[constants.ANIMATION])

    option_frame_step = IntProperty(
        name='Frame step', 
        description='Animation frame step', 
        min=1, 
        max=1000, 
        soft_min=1, 
        soft_max=1000, 
        default=1)

    def invoke(self, context, event):
        restore_settings_export(self.properties)
        return ExportHelper.invoke(self, context, event)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        if not self.properties.filepath:
            raise Exception('filename not set')

        settings = save_settings_export(self.properties)

        from threeio import exporter
        if settings[constants.SCALE]:
            exporter.export_scene(self.filepath, settings)
        else:
            exporter.export_geometry(self.filepath, settings)

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout

        ## Geometry {
        row = layout.row()
        row.label(text='Geometry:')

        row = layout.row()
        row.prop(self.properties, 'option_vertices')
        row.enabled = self.properties.option_vertices
        row.prop(self.properties, 'option_faces')
        row.enabled = self.properties.option_faces

        row = layout.row()
        row.prop(self.properties, 'option_normals')
        row.enabled = self.properties.option_normals

        row = layout.row()
        row.prop(self.properties, 'option_bones')
        row.prop(self.properties, 'option_skinning')
        ## }

        layout.separator()

        ## Materials {
        row = layout.row()
        row.label(text='Materials:')

        row = layout.row()
        row.prop(self.properties, 'option_materials')
        row.prop(self.properties, 'option_uv_coords')

        row = layout.row()
        row.prop(self.properties, 'option_face_materials')
        row.prop(self.properties, 'option_maps')

        row = layout.row()
        row.prop(self.properties, 'option_colors')
        row.prop(self.properties, 'option_mix_colors')
        ## }
    
        layout.separator()

        ## Settings {
        row = layout.row()
        row.label(text='Settings:')

        row = layout.row()
        row.prop(self.properties, 'option_scale')
        
        row = layout.row()
        row.prop(self.properties, 'option_round_off')
        row.prop(self.properties, 'option_round_value')

        row = layout.row()
        row.prop(self.properties, 'option_logging')

        row = layout.row()
        row.prop(self.properties, 'option_copy_textures')
        ## }

        layout.separator()

        ## Scene {
        row = layout.row()
        row.label(text='Scene:')

        row = layout.row()
        row.prop(self.properties, 'option_export_scene')
        row.prop(self.properties, 'option_embed_meshes')

        row = layout.row()
        row.prop(self.properties, 'option_lights')
        row.prop(self.properties, 'option_cameras')
        ## }

        ## Animation {
        layout.separator()

        row = layout.row()
        row.label(text='Animation:')

        row = layout.row()
        row.prop(self.properties, 'option_animation_morph')
        row = layout.row()
        row.prop(self.properties, 'option_animation_skeletal')
        row = layout.row()
        row.prop(self.properties, 'option_frame_step')
        ## }

def menu_func_export(self, context):
    default_path = bpy.data.filepath.replace('.blend', constants.EXTENSION)
    text = 'ThreeIO (%s)' % constants.EXTENSION
    operator = self.layout.operator(ExportThreeIO.bl_idname, text=text)
    operator.filepath = default_path


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)


if __name__ == '__main__':
    register() 
