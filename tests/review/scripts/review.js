var scene, renderer, camera, container, animation;

var clock = new THREE.Clock();
function render() {
        
    renderer.render( scene, camera );
      
}

function animate() {

    requestAnimationFrame( animate );

    if ( animation != null ) {

        var delta = clock.getDelta();
        THREE.AnimationHandler.update( delta );

    }

    render();

}

function setupScene( result, data ) {

    if ( result === undefined ) {

        scene = new THREE.Scene();

    } else {

        scene = result;

    }

    var setupLights = true;
    if ( data !== undefined ) {

        var lights = ['AmbientLight', 'DirectionalLight', 'AreaLight',
            'PointLight', 'SpotLight', 'HemisphereLight']
    
        for ( i = 0; i < data.object.children.length; i ++ ) {

            var index = lights.indexOf( data.object.children[ i ].type );

            if ( index > -1 ) {

                setupLights = false;
                break;

            }

        }

    }

    scene.add( new THREE.GridHelper( 10, 2.5 ) );
    if ( setupLights ) threePointLight();

}

function loadData( data, url ) {

    if ( data.metadata.type == 'Geometry' ) {
        
        var loader = new THREE.JSONLoader();
        var texturePath = loader.extractUrlBase( url );
        data = loader.parse( data, texturePath );
        if ( data.materials === undefined ) {
        
            console.log('using default material');
            data.materials = [new THREE.MeshLambertMaterial( { color: 0xb8b8b8 } )];
        
        }

        var material = new THREE.MeshFaceMaterial( data.materials ); 
        var mesh;

        if ( data.geometry.animation !== undefined ) {

            console.log( 'loading animation' );
            data.materials[ 0 ].skinning = true;
            mesh = new THREE.SkinnedMesh( data.geometry, material, false);
            THREE.AnimationHandler.add( data.geometry.animation );

            var name = data.geometry.animation.name;
            animation = new THREE.Animation( mesh, name );


        } else {

            mesh = new THREE.Mesh( data.geometry, material );
 
            //@TODO currently the morph targets are not animating
            //      the JSON tested fine in the 3js horse example
            //      scene which makes me thing there is something
            //      else wrong, possibly in this js library
            if ( data.geometry.morphTargets.length > 0 ) {
        
                console.log( 'loading morph targets' );
                data.materials[ 0 ].morphTargets = true;
                animation = new THREE.MorphAnimation( mesh );

            }       
        }

        setupScene();
        scene.add( mesh );
            
        if ( animation != null ) {

            console.log( 'playing animation' );
            animation.play();

        }


    } else if ( data.metadata.type == 'Object' ) { 

        var onLoad = function ( parsed ) {

            console.log( parsed );
            setupScene( parsed, data );

            parsed.children.forEach( function ( child ) {
        
                if ( child instanceof THREE.Camera ) {
                
                    camera = child;
                    var aspect = container.offsetWidth / container.offsetHeight;
                    camera.aspect = aspect;
                    orbit = new THREE.OrbitControls( camera, container );
                    orbit.addEventListener( 'change', render );
                    camera.updateProjectionMatrix();

                }

            } );

        };

        var loader = new ThreeIO.Loader();
        loader.parse( data, onLoad );
    
    } else {
    
        throw 'wtf did you pass me?';
    
    }

    animate();

}

function onWindowResize() {

    camera.aspect = container.offsetWidth / container.offsetHeight;
    camera.updateProjectionMatrix();

    renderer.setSize( container.offsetWidth, container.offsetHeight );

    render();

}

function threePointLight() {
    
    var directionalLight = new THREE.DirectionalLight( 0xb8b8b8 );
    directionalLight.position.set(1, 1, 1).normalize();
    directionalLight.intensity = 1.0;
    scene.add( directionalLight );
    
    directionalLight = new THREE.DirectionalLight( 0xb8b8b8 );
    directionalLight.position.set(-1, 0.6, 0.5).normalize();
    directionalLight.intensity = 0.5;
    scene.add(directionalLight);

    directionalLight = new THREE.DirectionalLight();
    directionalLight.position.set(-0.3, 0.6, -0.8).normalize( 0xb8b8b8 );
    directionalLight.intensity = 0.45;
    scene.add(directionalLight);

}

function init( url ) {

    container = document.createElement( 'div' );
    container.id = 'viewport';
    document.body.appendChild( container );

    renderer = new THREE.WebGLRenderer( { antialias: true, alpha: true  } );
    renderer.setSize( container.offsetWidth, container.offsetHeight );
    renderer.setClearColor( 0x000000, 0 );
    container.appendChild( renderer.domElement );
    renderer.gammaInput = true;
    renderer.gammaOutput = true;
    
    var aspect = container.offsetWidth / container.offsetHeight;
    camera = new THREE.PerspectiveCamera( 50, aspect, 0.01, 50 );
    orbit = new THREE.OrbitControls( camera, container );
    orbit.addEventListener( 'change', render );
    camera.position.z = 5;
    camera.position.x = 5;
    camera.position.y = 5;
    var target = new THREE.Vector3( 0, 1, 0 );
    camera.lookAt( target );
    orbit.target = target;
    camera.updateProjectionMatrix();

    window.addEventListener( 'resize', onWindowResize, false );

	var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function ( x ) {
    
        if ( xhr.readyState === xhr.DONE ) {

            if ( xhr.status === 200 || xhr.status === 0  ) {

                loadData( JSON.parse( xhr.responseText ), url );

            } else {

                console.error( 'could not load json ' + xhr.status );

            }

        } 
    
    };
    xhr.open( 'GET', url, true );
    xhr.withCredentials = false;
    xhr.send( null );

}
