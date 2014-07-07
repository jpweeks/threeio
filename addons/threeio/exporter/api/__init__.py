import os
import bpy
from bpy.app.handlers import persistent
from . import object, mesh, material, camera, light
from .. import logger


def init():
    logger.debug('Initializing API')
    object._MESH_MAP.clear()


def selected_objects(valid_types):
    logger.debug('api.selected_objects(%s)', valid_types)
    for node in bpy.context.selected_objects:
        if node.type in valid_types:
            yield node.name


@persistent
def scene_name():
    return os.path.basename(bpy.data.filepath)

