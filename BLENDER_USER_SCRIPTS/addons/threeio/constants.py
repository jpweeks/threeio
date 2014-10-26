BLENDING = type('Blending', (), {
    'NONE': 'NoBlending',
    'NORMAL': 'NormalBlending',
    'ADDITIVE': 'AdditiveBlending',
    'SUBTRACTIVE': 'SubtractiveBlending',
    'MULTIPLY': 'MultiplyBlending',
    'CUSTOM': 'CustomBlending'
})

NEAREST_FILTERS = type('NearestFilters', (), {
    'NEAREST': 'NearestFilter',
    'MIP_MAP_NEAREST': 'NearestMipMapNearestFilter',
    'MIP_MAP_LINEAR': 'NearestMipMapLinearFilter'
})

LINEAR_FILTERS = type('LinearFilters', (), {
    'LINEAR': 'LinearFilter',
    'MIP_MAP_NEAREST': 'LinearMipMapNearestFilter',
    'MIP_MAP_LINEAR': 'LinearMipMapLinearFilter'
})

MAPPING = type('Mapping', (), {
    'UV': 'UVMapping',
    'CUBE_REFLECTION': 'CubeReflectionMapping',
    'CUBE_REFRACTION': 'CubeRefractionMapping',
    'SPHERICAL_REFLECTION': 'SphericalReflectionMapping',
    'SPHERICAL_REFRACTION': 'SphericalRefractionMapping'
})

JSON = 'json'
EXTENSION = '.%s' % JSON


MATERIALS = 'materials'
SCENE = 'scene'
VERTICES = 'vertices'
FACES = 'faces'
NORMALS = 'normals'
BONES = 'bones'
BONE_MAP = 'boneMap'
UVS = 'uvs'
COLORS = 'colors'
MIX_COLORS = 'mixColors'
SCALE = 'scale'
COMPRESSION = 'compression'
MAPS = 'maps'
FRAME_STEP = 'frameStep'
ANIMATION = 'animation'
MORPH_TARGETS = 'morphTargets'
SKIN_INDICES = 'skinIndices'
SKIN_WEIGHTS = 'skinWeights'
LOGGING = 'logging'
CAMERAS = 'cameras'
LIGHTS = 'lights'
FACE_MATERIALS = 'faceMaterials'
SKINNING = 'skinning'
COPY_TEXTURES = 'copyTextures'
ROUND_OFF = 'roundOff'
ROUND_VALUE = 'roundValue'
ROUND = 6
EMBED_GEOMETRY = 'embedGeometry'
EMBED_ANIMATION = 'embedAnimation'

GLOBAL = 'global'
BUFFER_GEOMETRY = 'BufferGeometry'
GEOMETRY = 'geometry'
GEOMETRY_TYPE = 'geometryType'

CRITICAL = 'critical'
ERROR = 'error'
WARNING = 'warning'
INFO = 'info'
DEBUG = 'debug'

NONE = 'None'
MSGPACK = 'msgpack'

PACK = 'pack'

EXPORT_OPTIONS = {
    FACES: True,
    VERTICES: True,
    NORMALS: False,
    UVS: False,
    COLORS: False,
    MATERIALS: False,
    FACE_MATERIALS: False,
    SCALE: 1,
    FRAME_STEP: 1,
    SCENE: True,
    MIX_COLORS: False,
    COMPRESSION: None,
    MAPS: False,
    ANIMATION: False,
    BONES: False,
    SKINNING: False,
    MORPH_TARGETS: False,
    CAMERAS: False,
    LIGHTS: False,
    COPY_TEXTURES: True,
    LOGGING: DEBUG,
    ROUND_OFF: False,
    ROUND_VALUE: ROUND,
    EMBED_GEOMETRY: True,
    EMBED_ANIMATION: True,
    GEOMETRY_TYPE: GEOMETRY
}
