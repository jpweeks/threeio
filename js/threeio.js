ThreeIO = {};

/*
 * This function requires that your web app sources require.js and has
 * setup the baseUrl correctly (if loading from a partial path)
 */
ThreeIO.loadMSGPack = function( url, onLoad ) {

    require(['msgpack-js'], function( msgpack ) {
          
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url );
        xhr.responseType = 'arraybuffer';

        xhr.onload = function( e ) {

            var decoded = msgpack.decode( this.response );
            onLoad( decoded );

        };

        xhr.send();

    } );

};

ThreeIO.loadJSON = function ( url, onLoad ) {

    var xhr = new XMLHttpRequest();
    xhr.open( 'GET', url );
    
    xhr.onload = function() {

        if ( xhr.status == 200 ) {
            
            onLoad( JSON.parse( xhr.responseText ) );

        } else {

            Error( xhr.statusText );

        }

    };

    xhr.onerror = function ( ) {

        Error( 'Network Error' ) ;

    };

    xhr.send( null );

};

ThreeIO.loadTexture = function ( url, callback ) {

    var compressed = /\.dds$/i;
    var mapping = THREE.UVMapping;
    var texture;
    
    if ( url instanceof Array ) {
    
        var index = ( compressed.test( url[ 0 ] ) ) ? 0 : 1;
        var dispatch = [
            THREE.ImageUtils.loadCompressedTextureCube,
            THREE.ImageUtils.loadTextureCube
        ];
        texture = dispatch[ index  ]( url );

    } else {

        var index = ( compressed.test( url ) ) ? 0 : 1;
        var dispatch = [
            THREE.ImageUtils.loadCompressedTexture,
            THREE.ImageUtils.loadTexture
        ];
        texture = dispatch[ index ]( url, mapping );

    }


    callback( texture );
};

ThreeIO.Loader = function ( ) {

    this.urlHandlers = {};

    var scope = this;

    this.urlHandlers[ 'geometry' ] =  function ( data, onLoad ) {
        
        ThreeIO.loadJSON( data.url, function ( response ) {

            onLoad( response, data.uuid );

        } );
    };

    this.urlHandlers[ 'image' ] = function ( data, callback ) {

        ThreeIO.loadTexture( data.url, function ( texture ) {
        
            callback( texture );
        
        } );

    };

}

ThreeIO.Loader.prototype.parse = function ( data, onLoad ) {

    var textures = {};

    var scope = this;
    var parseNodes = function ( textures ) {

        var materials = scope.parseMaterials( 
            data.materials, textures );
        
        var geometries = {};
		scope.parseGeometries( data.geometries, function ( geometry ) {

            geometries[ geometry.uuid ] = geometry;
            var processed = Object.keys( geometries ).length;

            if ( processed == data.geometries.length ) {
            
                var object = scope.parseObject( data.object, 
                    geometries, materials );

                onLoad( object );

            }

        } );

    };

    if ( data.textures !== undefined && data.textures.length > 0 ) {

        this.parseTextures( data , function ( texture ) {
            
            textures[ texture.uuid] = texture;
            var processed = Object.keys( textures ).length;

            if ( processed == data.textures.length ) {

                parseNodes( textures );

            }

        } );

    } else {

        parseNodes();

    }

}

ThreeIO.Loader.prototype.parseObject = function () {

    var matrix = new THREE.Matrix4();

    var objAttributes = [];

    return function ( data, geometries, materials ) {

        var object;

        switch ( data.type ) {

            case 'Scene':

                object = new THREE.Scene();

                break;

            case 'AreaLight':

                object = new THREE.AreaLight( data.color, data.intensity );

                objAttributes = [ 'height', 'width', 'linearAttenuation', 
                    'constantAttenuation', 'quadraticAttenuation' ];

                break;

            case 'PerspectiveCamera':

                object = new THREE.PerspectiveCamera( data.fov, 
                    data.aspect, data.near, data.far );

                break;

            case 'OrthographicCamera':

                object = new THREE.OrthographicCamera( data.left, 
                    data.right, data.top, data.bottom, data.near, 
                    data.far );

                break;

            case 'AmbientLight':

                object = new THREE.AmbientLight( data.color );

                break;

            case 'DirectionalLight':

                object = new THREE.DirectionalLight( data.color, 
                    data.intensity );

                objAttributes = [ 'onlyShadow', 'shadowCameraNear', 
                    'shadowCameraFar', 'shadowCameraLeft', 
                    'shadowCameraRight', 'shadowCameraTop', 
                    'shadowCameraBottom', 'shadowCameraVisible', 
                    'shadowBias', 'shadowDarkness', 'shadowMapWidth', 
                    'shadowMapHeight', 'shadowCascade', 
                    'shadowCascadeCount', 'shadowMap', 'shadowMapSize',
                    'shadowCamera'];

                break;

            case 'PointLight':

                object = new THREE.PointLight( data.color, 
                    data.intensity, data.distance );

                break;

            case 'SpotLight':

                object = new THREE.SpotLight( data.color, data.intensity, 
                    data.distance, data.angle, data.exponent );

                objAttributes = [ 'onlyShadow', 'shadowCameraNear', 
                    'shadowCameraFar', 'shadowCameraFov', 
                    'shadowCameraVisible', 'shadowBias', 'shadowDarkness', 
                    'shadowMapWidth', 'shadowMapHeight', 'shadowBias',
                    'shadowMapSize', 'shadowCamera', 'shadowMap' ];

                break;

            case 'HemisphereLight':

                object = new THREE.HemisphereLight( data.color, 
                    data.groundColor, data.intensity );

                break;

            case 'Mesh':

                var geometry = geometries[ data.geometry ];
                var material = materials[ data.material ];

                if ( geometry === undefined ) {

                    console.error( 'ThreeIO: Undefined geometry ' + data.geometry );

                }

                if ( material === undefined ) {

                    console.error( 'ThreeIO: Undefined material ' + data.material );

                }

                object = new THREE.Mesh( geometry, material );

                break;

            case 'Sprite':

                var material = materials[ data.material ];

                if ( material === undefined ) {

                    console.error( 'ThreeIO: Undefined material ' + data.material );

                }

                object = new THREE.Sprite( material );

                break;

            default:

                object = new THREE.Object3D();

        }

        object.uuid = data.uuid;

        var commonAttributes = [ 'name', 'visible', 'userData', 
            'receiveShadow', 'castShadow' ];
        
        var attributes = commonAttributes.concat( objAttributes );

        for ( i = 0; i < attributes.length; i ++ ) {

            var attribute = attributes[ i ];
            if ( data[ attribute ] !== undefined ) {

                object[ attribute ] = data[ attribute ];

            }

        }

        if ( data.matrix !== undefined ) {

            matrix.fromArray( data.matrix );
            matrix.decompose( object.position, object.quaternion, object.scale );

        } else {

            if ( data.position !== undefined ) object.position.fromArray( data.position );
            if ( data.rotation !== undefined ) object.rotation.fromArray( data.rotation );
            if ( data.scale !== undefined ) object.scale.fromArray( data.scale );

        }

        if ( data.children !== undefined ) {

            for ( var child in data.children ) {

                object.add( this.parseObject( data.children[ child ], geometries, materials ) );

            }

        }

        return object;

    }

}()


ThreeIO.Loader.prototype.parseGeometries = function ( geometries, onLoad ) {

    var jsonLoader = new THREE.JSONLoader();
    var bufferLoader = new THREE.BufferGeometryLoader();

    var parseJSON = function ( data, callback ) {

        var geometry = jsonLoader.parse( data.data ).geometry;

        if ( data.uuid !== undefined ) geometry.uuid = data.uuid;
        if ( data.data.name !== undefined ) geometry.name = data.data.name;

        callback( geometry );

    };

    var parseBuffer = function ( data, callback ) {

        var geometry = bufferLoader.parse( data );

        if ( data.uuid !== undefined ) geometry.uuid = data.uuid;
        if ( data.name !== undefined ) geometry.name = data.name;

        callback( geometry );

    };

    for ( i = 0; i < geometries.length; i ++ ) {

        var data = geometries[ i ];

        if ( data.type == 'Geometry' ) {

            if ( data.url === undefined ) {

                parseJSON( data, function ( geometry ) { 
                
                    onLoad( geometry );

                } );

            } else {

                this.urlHandlers.geometry( data, function ( geom, uuid ) {

                    var args = { data : geom, uuid: uuid };
                    parseJSON( args, function ( geometry ) {

                        onLoad( geometry );

                    } );

                } );

            }

        } else if ( data.type == 'BufferGeometry' ) {
        
            if ( data.url === undefined ) {

                parseBuffer( data, function ( geometry ) { 
                
                    onLoad( geometry );

                } );

            } else {

                this.urlHandlers.geometry( data, function ( geom, uuid ) {

                    if ( geom.uuid === undefined ) geom.uuid = uuid;
                    parseBuffer( geom, function ( geometry ) {

                        onLoad( geometry );

                    } );

                } );

            }

        } else {

            console.error('unrecognized geometry type');

        }

    }

}

ThreeIO.Loader.prototype.parseMaterials = function ( materials, textures ) {

    var loaded = {};
    var maps = [ 'map', 'lightMap', 'specularMap', 
        'bumpMap', 'normalMap' ];

    var attributes = [ 'bumpScale', 'normalScale' ];

    var loader = new THREE.MaterialLoader();

    for ( i = 0; i < materials.length; i ++ ) {

        var data = materials[ i ];
        var material = loader.parse( data );

        material.uuid = data.uuid;

        if ( data.name !== undefined ) material.name = data.name;

        loaded[ data.uuid ] = material;

        if ( textures === undefined ) continue;

        for ( j = 0; j < maps.length; j ++ ) {

            if ( data[ maps[ j ] ] === undefined ) continue;

            var uuid = data[ maps [ j ] ];
            material[ maps[ j ] ] = textures[ uuid ];

            for ( k = 0; k < attributes.length; k ++ ) {

                var attribute = attributes[ k ];

                if ( data[ attribute ] === undefined ) continue;

                material[ attribute ] = data[ attribute ];

            }

        }

    }

    return loaded;

}


ThreeIO.Loader.prototype.parseTextures = function ( json, callback ) {

    var urlHandler = this.urlHandlers.image;
    var values = [ 'anisotropy', 'name', 'flipY'];
    var vector2 = [ 'repeat', 'offset' ];
    var keys = [ 'mapping', 'magFilter', 'minFilter' ];

    var updateAttributes = function( texture, data ) {

        texture[ 'uuid' ] = data.uuid;

        for ( k = 0; k < values.length; k ++ ) {

            var value = values[ k ];
            if ( data[ value ] !== undefined ) {

                texture[ value ] = data[ value ];

            }

        }

        for ( k = 0; k < keys.length; k ++ ) {

            var key = keys[ k ];
            if ( data[ key ] !== undefined ) {

                var value = THREE[ key ];
                texture[ value ] = data[ value ];

            }

        }

        for ( k = 0; k < vector2.length; k ++ ) {

            var key = vector2[ k ];
            if ( data[ key ] !== undefined ) {
            
                var val = data[ key ];
                texture[ key ].set(val[ 0 ], val[ 1 ]);

            }

        }

        if ( data.wrap !== undefined ) {

            texture.wrapS = THREE[ data.wrap[ 0 ] ];
            texture.wrapT = THREE[ data.wrap[ 1 ] ];

        }

        callback( texture );
    }

    for ( i = 0; i < json.textures.length; i ++ ) {

        var data = json.textures[ i ];

        for ( j = 0; j < json.images.length; j ++ ) {
        
            var image = json.images[ j ];

            if ( image.uuid != data.image ) continue;

            urlHandler( image, function ( texture ) {
                
                updateAttributes( texture, data );
            
            } );

            break;

        }

    }
    
}
