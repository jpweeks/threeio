import shutil
from . import _json, logger, exceptions, constants


def copy_registered_textures(dest, registration):
    logger.debug('io.copy_registered_textures(%s, %s)', dest, registration)
    for value in registration.values():
        copy(value['file_path'], dest)


def copy(src, dst):
    logger.debug('io.copy(%s, %s)' % (src, dst))
    shutil.copy(src, dst)


def dump(filepath, data, options=None):
    options = options or {}
    logger.debug('io.dump(%s, data, options=%s)', filepath, options)

    compress = options.get(constants.COMPRESSION)
    if compress:
        message = 'Compression not yet implemented'
        logger.error(message)
        raise exceptions.UnimplementedFeatureError(message)
    else:
        round_off = options.get(constants.ROUND_OFF)
        if round_off:
            _json.ROUND = options[constants.ROUND_VALUE]
        else:
            _json.ROUND = None

        logger.info('Dumping to JSON')
        func = lambda x,y: _json.json.dump(x, y, indent=4)
        mode = 'w'

    logger.info('Writing to %s', filepath)
    with open(filepath, mode=mode) as stream:
        func(data, stream)

    print('LOG: %s', logger.LOG_FILE) 


def load(filepath, options):
    logger.debug('io.load(%s, %s)', filepath, options)
    if options.get(constant.MSGPack):
        message = 'MSGPack loading not yet supported'
        logger.error(message)
        raise exceptions.UnimplementedFeatureError(message)
        module = msgpack
        mode = 'rb'
    else:
        logger.info('Loading JSON')
        module = _json.json
        mode = 'r'

    with open(filepath, mode=mode) as stream:
        data = module.load(stream)

    return data