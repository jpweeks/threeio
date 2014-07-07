ThreeIO = {}

ThreeIO.jsonParser = function ( url ) {

    return new Promise( function ( resolve, reject ) {
	    var xhr = new XMLHttpRequest();
        xhr.open( 'GET', url );
        
        xhr.onload = function() {

            if ( xhr.status == 200 ) {
                
                resolve( xhr.responseText );

            } else {

                reject( Error( xhr.statusText ) );

            }

        };

        xhr.onerror = function ( ) {

            reject( Error( 'Network Error' ) );

        };
    
        xhr.send( null );

    } );

}

ThreeIO.loadTexture = function ( url, callback ) {

    var compressed = /\.dds$/i;
    var mapping = THREE.UVMapping;
    var texture;
    
    if ( url instanceof Array ) {

        var dispatch = {
            true: THREE.ImageUtils.loadCompressedTextureCube,
            false: THRE.ImageUtils.loadTextureCube
        }
        texture = dispatch[ compressed.test( url[ 0 ] ) ]( url );

    } else {

        var dispatch = {
            true: THREE.ImageUtils.loadCompressedTexture,
            false: THREE.ImageUtils.loadTexture
        }
        texture = dispatch[ compressed.test( url ) ]( url, mapping );

    }

    callback( texture );

}

ThreeIO.Loader = function ( ) {

    this._urlHandlers = {};

    var scope = this;

    this._urlHandlers[ 'geometry' ] =  function ( url, onLoad ) {
        
        ThreeIO.jsonParser( url ).then ( function ( response ) {

            scope.parse( JSON.parse ( response ), onLoad );

        }, function ( error ) {
        
            console.error( 'failed to load ' + url );

        } );
    };

    this._urlHandlers[ 'image' ] = function ( url, callback ) {

        ThreeIO.loadTexture( url, function ( texture ) {
        
            callback( texture );
        
        } );

    };

}

ThreeIO.Loader.prototype.parse = function ( data, onLoad ) {

    var textures = {};
    var nodes = {
        objects: [],
        materials: [],
        geometries: []
    };

    var scope = this;
    var parseNodes = function ( textures ) {

        var materials = scope.parseMaterials( 
            data.materials, textures );
        
		var geometries = scope.parseGeometries( data.geometries );

        var object = scope.parseObject( data.object, geometries, materials );

        onLoad( object );

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


ThreeIO.Loader.prototype.parseGeometries = function ( geometries ) {

    var loaded = {};

    var loader = new THREE.JSONLoader();
    for ( i = 0; i < geometries.length; i ++ ) {

        var data = geometries[ i ];
        var geometry = loader.parse( data.data ).geometry;

        geometry.uuid = data.uuid;

        if ( data.name !== undefined ) geometry.name = data.name;

        loaded[ data.uuid ] = geometry;

    }

    return loaded;

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

    var urlHandler = this._urlHandlers.image;
    var values = [ 'anisotropy', 'repeat', 'offset', 'name', 'flipY'];
    var keys = [ 'mapping', 'magFilter', 'minFilter' ];

    var updateAttributes = function( texture, data ) {

        texture[ 'uuid' ] = data.uuid;

        for ( k = 0; k < values.length; k ++ ) {
            break;
            var value = values[ k ];
            if ( data[ value ] !== undefined ) {

                texture[ value ] = data[ value ];

            }

        }

        for ( k = 0; k < keys.length; k ++ ) {
            break;
            var key = keys[ k ];
            if ( data[ key ] !== undefined ) {

                var value = THREE[ key ];
                texture[ value ] = data[ value ];

            }

        }

        if ( data.wrap !== undefined ) {

            texture.wrapS = THREE[ data.wrap[ 0 ] ];
            texture.wrapT = THREE[ data.wrap[ 1 ] ];

        }

        if ( data.repeat !== undefined ) {
        
            texture.repeat.set(data.repeat[ 0 ], data.repeat[ 1 ]);

        }

        callback( texture );
    }

    for ( i = 0; i < json.textures.length; i ++ ) {

        var data = json.textures[ i ];

        for ( j = 0; j < json.images.length; j ++ ) {
        
            var image = json.images[ j ];

            if ( image.uuid != data.image ) continue;

            urlHandler( image.url, function ( texture ) {
                
                updateAttributes( texture, data );
            
            } );

            break;

        }

    }
    
}
