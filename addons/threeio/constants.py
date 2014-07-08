BLENDING = type('Blending', (), {
    'NONE': 'NoBlending',
    'NORMAL': 'NormalBlending',
    'ADDITIVE': 'AdditiveBlending',
    'SUBTRACTIVE': 'SubtractiveBlending',
    'MULTIPLY': 'MultiplyBlending',
    'CUSTOM': 'CustomBlending'
})


EXTENSION = '.json'


MATERIALS = 'materials'
SCENE = 'scene'
VERTICES = 'vertices'
FACES = 'faces'
NORMALS = 'normals'
BONES = 'bones'
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
EMBED= 'embed'

CRITICAL = 'critical'
ERROR = 'error'
WARNING = 'warning'
INFO = 'info'
DEBUG = 'debug'


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
    EMBED: True
}
