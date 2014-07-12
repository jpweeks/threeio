'''
All constant data used in the package should be defined here.
'''

from collections import OrderedDict as BASE_DICT

# I really wish I didn't have to do this...
from ..constants import  (
    MATERIALS,
    SCENE,
    VERTICES,
    FACES,
    NORMALS,
    BONES,
    UVS,
    COLORS,
    MIX_COLORS,
    SCALE,
    COMPRESSION,
    MAPS,
    FRAME_STEP,
    ANIMATION,
    MORPH_TARGETS,
    SKIN_INDICES,
    SKIN_WEIGHTS,
    LOGGING,
    CAMERAS,
    LIGHTS,
    FACE_MATERIALS,
    SKINNING,
    COPY_TEXTURES,
    ROUND_OFF,
    ROUND_VALUE,
    ROUND,
    EMBED,
    CRITICAL,
    ERROR,
    WARNING,
    INFO,
    DEBUG,
    EXPORT_OPTIONS as OPTIONS
)


FORMAT_VERSION = 4.3
VERSION = 'version'
THREE_IO = 'ThreeIO'
GENERATOR = 'generator'
SOURCE_FILE = 'sourceFile'
VALID_DATA_TYPES = (str, int, float, bool, list, tuple, dict)

ROUND = 6
ROUND_VALUE = 'roundValue'
ROUND_OFF = 'roundOff'

JSON = 'json'
MSGPACK = 'msgpack'
GZIP = 'gzip'

EXTENSIONS = {
    JSON: '.json',
    MSGPACK: '.pack',
    GZIP: '.gz'
}

METADATA = 'metadata'
GEOMETRIES = 'geometries'
IMAGES = 'images'
TEXTURE = 'texture'
TEXTURES = 'textures'

USER_DATA = 'userData'
DATA = 'data'
TYPE = 'type'

MATERIAL = 'material'
GEOMETRY = 'geometry'
OBJECT = 'object'
PERSPECTIVE_CAMERA = 'PerspectiveCamera'
ORTHOGRAPHIC_CAMERA = 'OrthographicCamera'
AMBIENT_LIGHT = 'AmbientLight'
DIRECTIONAL_LIGHT = 'DirectionalLight'
AREA_LIGHT = 'AreaLight'
POINT_LIGHT = 'PointLight'
SPOT_LIGHT = 'SpotLight'
HEMISPHERE_LIGHT = 'HemisphereLight'
MESH = 'Mesh'
SPRITE = 'Sprite'

DEFAULT_METADATA = {
    VERSION: FORMAT_VERSION,
    TYPE: OBJECT.title(),
    GENERATOR: THREE_IO
}

UUID = 'uuid'

MATRIX = 'matrix'
POSITION = 'position'
QUATERNION = 'quaternion'
ROTATION ='rotation'
SCALE = 'scale'

VISIBLE = 'visible'
CAST_SHADOW = 'castShadow'
RECEIVE_SHADOW = 'receiveShadow'
QUAD = 'quad'

USER_DATA = 'userData'

MASK = {
    QUAD: 0,
    MATERIALS: 1,
    UVS: 3,
    NORMALS: 5,
    COLORS: 7
}


CHILDREN = 'children'

URL = 'url'
WRAP = 'wrap'
REPEAT = 'repeat'
WRAPPING = type('Wrapping', (), {
    'REPEAT': 'RepeatWrapping',
    'CLAMP': 'ClampToEdgeWrapping',
    'MIRROR': 'MirroredRepeatWrapping'
})
ANISOTROPY = 'anisotropy'
MAG_FILTER = 'magFilter'
MIN_FILTER = 'minFilter'
MAPPING = 'mapping'

IMAGE = 'image'

NAME = 'name'
PARENT = 'parent'

#@TODO move to api.constants?
POS = 'pos'
ROTQ = 'rotq'

AMBIENT = 'ambient'
COLOR = 'color'
EMISSIVE = 'emissive'
SPECULAR = 'specular'
SPECULAR_COEF = 'specularCoef'
SHININESS = 'shininess'
SIDE = 'side'
OPACITY = 'opacity'
TRANSPARENT = 'transparent'
WIREFRAME = 'wireframe'
BLENDING = 'blending'
VERTEX_COLORS = 'vertexColors'
DEPTH_WRITE = 'depthWrite'
DEPTH_TEST = 'depthTest'

MAP = 'map'
SPECULAR_MAP = 'specularMap'
LIGHT_MAP = 'lightMap'
BUMP_MAP = 'bumpMap'
BUMP_SCALE = 'bumpScale'
NORMAL_MAP = 'normalMap'
NORMAL_SCALE = 'normalScale'

#@TODO ENV_MAP, REFLECTIVITY, REFRACTION_RATIO, COMBINE

MAP_DIFFUSE = 'mapDiffuse'
MAP_DIFFUSE_REPEAT = 'mapDiffuseRepeat'
MAP_DIFFUSE_WRAP = 'mapDiffuseWrap'
MAP_DIFFUSE_ANISOTROPY = 'mapDiffuseAnisotropy'

MAP_SPECULAR = 'mapSpecular'
MAP_SPECULAR_REPEAT = 'mapSpecularRepeat'
MAP_SPECULAR_WRAP = 'mapSpecularWrap'
MAP_SPECULAR_ANISOTROPY = 'mapSpecularAnisotropy'

MAP_LIGHT = 'mapLight'
MAP_LIGHT_REPEAT = 'mapLightRepeat'
MAP_LIGHT_WRAP = 'mapLightWrap'
MAP_LIGHT_ANISOTROPY = 'mapLightAnisotropy'

MAP_NORMAL = 'mapNormal'
MAP_NORMAL_FACTOR = 'mapNormalFactor'
MAP_NORMAL_REPEAT = 'mapNormalRepeat'
MAP_NORMAL_WRAP = 'mapNormalWrap'
MAP_NORMAL_ANISOTROPY = 'mapNormalAnisotropy'

MAP_BUMP = 'mapBump'
MAP_BUMP_REPEAT = 'mapBumpRepeat'
MAP_BUMP_WRAP = 'mapBumpWrap'
MAP_BUMP_ANISOTROPY = 'mapBumpAnisotropy'
MAP_BUMP_SCALE = 'mapBumpScale'

NORMAL_BLENDING = 0

VERTEX_COLORS_ON = 2
VERTEX_COLORS_OFF = 0

THREE_BASIC = 'MeshBasicMaterial'
THREE_LAMBERT = 'MeshLambertMaterial'
THREE_PHONG = 'MeshPhongMaterial'

INTENSITY = 'intensity'
DISTANCE = 'distance'
ASPECT = 'aspect'
ANGLE = 'angle'

FOV = 'fov'
ASPECT = 'aspect'
NEAR = 'near'
FAR = 'far'

LEFT = 'left'
RIGHT = 'right'
TOP = 'top'
BOTTOM = 'bottom'

SHADING = 'shading'
COLOR_DIFFUSE = 'colorDiffuse'
COLOR_AMBIENT = 'colorAmbient'
COLOR_EMISSIVE = 'colorEmissive'
COLOR_SPECULAR = 'colorSpecular'
DBG_NAME = 'DbgName'
DBG_COLOR = 'DbgColor'
DBG_INDEX = 'DbgIndex'
EMIT = 'emit'

PHONG = 'phong'
LAMBERT = 'lambert'
BASIC = 'basic'

NORMAL_BLENDING = 'NormalBlending'

DBG_COLORS = (0xeeeeee, 0xee0000, 0x00ee00, 0x0000ee, 0xeeee00, 0x00eeee, 0xee00ee)

DOUBLE_SIDED = 'doubleSided'

