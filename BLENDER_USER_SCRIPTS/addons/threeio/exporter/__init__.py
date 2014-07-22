import os
import sys
import traceback
from . import (
    scene, 
    geometry, 
    api, 
    exceptions, 
    logger, 
    constants, 
    base_classes
)


def _error_handler(func):
    
    def inner(filepath, options, *args, **kwargs):
        level = options.get(constants.LOGGING, constants.DEBUG)
        logger.init(level=level)
        api.init()
        
        try:
            func(filepath, options, *args, **kwargs)
        except:
            info = sys.exc_info()
            trace = traceback.format_exception(
                info[0], info[1], info[2].tb_next)
            trace = ''.join(trace)
            logger.error(trace)
            
            print('Error recorded to %s' % logger.LOG_FILE)

            raise
        else:
            print('Log: %s' % logger.LOG_FILE)

    return inner


@_error_handler
def export_scene(filepath, options):
    scene_ = scene.Scene(filepath, options=options)
    scene_.parse()
    scene_.write()


@_error_handler
def export_geometry(filepath, options, node=None):
    if node is None:
        for node in api.selected_objects(['MESH']):
            break
        else:
            raise exceptions.SelectionError('Nothing selected')
    
    mesh = api.object.mesh(node, options)
    parent = base_classes.BaseScene(filepath, options)
    geo = geometry.Geometry(mesh, parent)
    geo.parse()
    geo.write()
    
    if not options.get(constants.EMBED_ANIMATION, True):
        geo.write_animation(os.path.dirname(filepath))
