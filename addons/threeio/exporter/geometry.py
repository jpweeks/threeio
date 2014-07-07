import os
from . import base_classes, constants, io, logger, api


FORMAT_VERSION = 3


class Geometry(base_classes.BaseNode):
    _defaults = {
        constants.TYPE: constants.GEOMETRY.title()
    }

    def __init__(self, node, parent=None):
        logger.debug('Geometry().__init__(%s)', node)
        base_classes.BaseNode.__init__(self, node, parent=parent,
            type=constants.GEOMETRY.title())

    @property
    def face_count(self):
        try:
            faces = self[constants.FACES]
        except KeyError:
            logger.debug('No parsed faces found')
            return 0

        length = len(faces)
        offset = 0
        bitset = lambda x,y: x & ( 1 << y )
        face_count = 0

        while offset < length:
            bit = faces[offset]
            offset += 1
            face_count += 1
            is_quad = bitset(bit, constants.MASK[constants.QUAD])
            has_material = bitset(bit, constants.MASK[constants.MATERIALS])
            has_uv = bitset(bit, constants.MASK[constants.UVS])
            has_normal = bitset(bit, constants.MASK[constants.NORMALS])
            has_color = bitset(bit, constants.MASK[constants.COLORS])

            vector = 4 if is_quad else 3
            offset += vector

            if has_material:
                offset += 1
            if has_uv:
                offset += vector
            if has_normal:
                offset += vector
            if has_color:
                offset += vector

        return face_count

    @property
    def metadata(self):
        metadata = {
            constants.GENERATOR: constants.THREE_IO,
            constants.VERSION: FORMAT_VERSION
        }

        skip = (constants.TYPE, constants.FACES, constants.UUID,
            constants.ANIMATION, constants.SKIN_INDICES,
            constants.SKIN_WEIGHTS, constants.NAME)
        vectors = (constants.VERTICES, constants.NORMALS)

        for key in self.keys():
            if key in vectors:
                try:
                    metadata[key] = int(len(self[key])/3)
                except KeyError:
                    pass
                continue

            if key in skip: continue

            metadata[key] = len(self[key])

        faces = self.face_count
        if faces > 0:
            metadata[constants.FACES] = faces

        return metadata

    def copy(self, scene=True):
        logger.debug('Geometry().copy(scene=%s)', scene)
        dispatch = {
            True: self._scene_format,
            False: self._geometry_format
        }
        data = dispatch[scene]()

        try:
            data[constants.MATERIALS] = self[constants.MATERIALS].copy()
        except KeyError:
            logger.debug('No materials to copy')
            pass

        return data

    def copy_textures(self):
        logger.debug('Geometry().copy_textures()')
        if self.options.get(constants.COPY_TEXTURES):
            texture_registration = self.register_textures()
            if texture_registration:
                logger.info('%s has registered textures', self.node)
                io.copy_registered_textures(
                    os.path.dirname(self.scene.filepath),
                    texture_registration)

    def parse(self):
        logger.debug('Geometry().parse()')

        if self.options.get(constants.VERTICES):
            logger.info('Parsing %s', constants.VERTICES)
            self[constants.VERTICES] = api.mesh.vertices(
                self.node, self.options)

        if self.options.get(constants.FACES):
            logger.info('Parsing %s', constants.FACES)
            self[constants.FACES] = api.mesh.faces(
                self.node, self.options)

        if self.options.get(constants.NORMALS):
            logger.info('Parsing %s', constants.NORMALS)
            self[constants.NORMALS] = api.mesh.normals(
                self.node, self.options)

        if self.options.get(constants.COLORS):
            logger.info('Parsing %s', constants.COLORS)
            self[constants.COLORS] = api.mesh.vertex_colors(self.node)
        
        if self.options.get(constants.FACE_MATERIALS):
            logger.info('Parsing %s', constants.FACE_MATERIALS)
            self[constants.MATERIALS] = api.mesh.materials(
                self.node, self.options)

        if self.options.get(constants.UVS):
            logger.info('Parsing %s', constants.UVS)
            self[constants.UVS] = api.mesh.uvs(self.node, self.options)

        if self.options.get(constants.ANIMATION):
            logger.info('Parsing %s', constants.ANIMATION)
            self[constants.ANIMATION] = api.mesh.animation(
                self.node, self.options)

        if self.options.get(constants.BONES):
            logger.info('Parsing %s', constants.BONES)
            self[constants.BONES] = api.mesh.bones(self.node) 

        if self.options.get(constants.SKINNING):
            logger.info('Parsing %s', constants.SKINNING)
            self[constants.SKIN_INDICES] = api.mesh.skin_indices(self.node)
            self[constants.SKIN_WEIGHTS] = api.mesh.skin_weights(self.node)

        if self.options.get(constants.MORPH_TARGETS):
            logger.info('Parsing %s', constants.MORPH_TARGETS)
            self[constants.MORPH_TARGETS] = api.mesh.morph_targets(
                self.node, self.options)

    def register_textures(self):
        logger.debug('Geometry().register_textures()')
        return api.mesh.texture_registration(self.node) 

    def write(self):
        logger.debug('Geometry().write(compress=%s)', compress)
        io.dump(self.parent.filepath, self.copy(scene=False), 
            options=options) 

        if self.options.get(constants.MAPS):
            logger.info('Copying textures for %s', self.node)
            self.copy_textures()

    def _component_data(self):
        logger.debug('Geometry()._component_data()')
        components = (constants.VERTICES, constants.FACES, 
            constants.UVS, constants.COLORS, constants.NORMALS,
            constants.ANIMATION, constants.BONES, constants.MORPH_TARGETS,
            constants.SKIN_WEIGHTS, constants.SKIN_INDICES,
            constants.NAME)
        data = {}

        for component in components:
            try:
                data[component] = self[component]
            except KeyError:
                logger.debug('Component %s not found', component)
                pass

        return data

    def _geometry_format(self):
        data = self._component_data()
        data[constants.METADATA] = {
            constants.TYPE: self[constants.TYPE]
        }

        data[constants.METADATA].update(self.metadata)

        return data

    def _scene_format(self):
        data = {
            constants.UUID: self[constants.UUID],
            constants.TYPE: self[constants.TYPE].title(),
            constants.DATA: self._component_data()
        }

        data[constants.DATA].update({
            constants.METADATA: self.metadata
        })

        return data 
