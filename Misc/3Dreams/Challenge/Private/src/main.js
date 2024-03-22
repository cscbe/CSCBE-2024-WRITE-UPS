import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { PointerLockControls } from 'three/addons/controls/PointerLockControls.js';

let renderer, raycaster, scale;
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
let moveForward = false;
let moveBackward = false;
var pathValue = 0;
const curvePath = new THREE.CurvePath();
const controls = new PointerLockControls(camera, document.body);
scene.add(controls.getObject());


function init() {

    const loader = new GLTFLoader();
    loader.load('cameraPath.glb', function (gltf) {
        const curveData = gltf.scene.children[0].geometry.attributes.position.array;
        scale = gltf.scene.children[0].scale
        const points = [];
        for (let i = 0; i < curveData.length; i += 3) {
            const point = new THREE.Vector3(curveData[i] * scale.x, curveData[i + 1] * scale.y, curveData[i + 2] * scale.z);
            points.push(point);
        }
        const curve = new THREE.CatmullRomCurve3(points);
        curvePath.add(curve);
    }, undefined, function (error) {
        console.error(error);
    });

    loader.load('Texts.glb', function (gltf) {
        scene.add(gltf.scene);
    }, undefined, function (error) {
        console.error(error);
    });

    const onKeyDown = function (event) {
        switch (event.code) {
            case 'ArrowUp':
            case 'KeyZ':
            case 'KeyW':
                moveForward = true;
                break;

            case 'ArrowDown':
            case 'KeyS':
                moveBackward = true;
                break;
        }
    };

    const onKeyUp = function (event) {
        switch (event.code) {
            case 'ArrowUp':
            case 'KeyZ':
            case 'KeyW':
                moveForward = false;
                break;

            case 'ArrowDown':
            case 'KeyS':
                moveBackward = false;
                break;
        }
    };

    document.addEventListener('keydown', onKeyDown);
    document.addEventListener('keyup', onKeyUp);

    raycaster = new THREE.Raycaster(new THREE.Vector3(), new THREE.Vector3(0, - 1, 0), 0, 10);
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    const spotLight = new THREE.SpotLight(0xffffff, 1000, 0, Math.PI / 12);
    camera.add(spotLight);
    camera.add(spotLight.target);
    spotLight.target.position.z = -8 ;

    const groundGeo = new THREE.PlaneGeometry(10000, 10000);
    const groundMat = new THREE.MeshLambertMaterial({ color: 0x021a00});

    const ground = new THREE.Mesh(groundGeo, groundMat);
    ground.position.y = - 33;
    ground.rotation.x = - Math.PI / 2;
    ground.receiveShadow = true;
    scene.add(ground);

    const sphere = new THREE.SphereGeometry( 2, 32, 16 );
    const bigSphere = new THREE.SphereGeometry( 6, 32, 16 );

    const light1 = new THREE.PointLight( 0xff0040, 10000 );
	light1.add( new THREE.Mesh( sphere, new THREE.MeshBasicMaterial( { color: 0xff0040 } ) ) );
    light1.position.set( 100, 30, -95 );
    scene.add( light1 );

    const light2 = new THREE.PointLight( 0xc28910, 8000 );
	light2.add( new THREE.Mesh( bigSphere, new THREE.MeshBasicMaterial( { color: 0xc28910 } ) ) );
    light2.position.set( 50, 50, -150 );
    scene.add( light2 );

    const light3 = new THREE.PointLight( 0x05540e, 10000 );
	light3.add( new THREE.Mesh( sphere, new THREE.MeshBasicMaterial( { color: 0x05540e } ) ) );
    light3.position.set( -90, 35, -90);
    scene.add( light3 );

    const light4 = new THREE.PointLight( 0x031e8c, 10000 );
	light4.add( new THREE.Mesh( sphere, new THREE.MeshBasicMaterial( { color: 0x031e8c } ) ) );
    light4.position.set( 60, 30, -300 );
    scene.add( light4 );

    window.addEventListener('resize', onWindowResize);
    const instructions = document.getElementById( 'instructions' );
	instructions.addEventListener('click', function () {
        controls.lock();
    }
        , false);
}

    controls.addEventListener( 'lock', function () {
        instructions.style.display = 'none';
        blocker.style.display = 'none';
    } );
    
    controls.addEventListener( 'unlock', function () {
        blocker.style.display = 'block';
        instructions.style.display = '';
    } );

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

function animate() {
    requestAnimationFrame(animate);
    if (controls.isLocked === true) {
        raycaster.ray.origin.copy(controls.getObject().position);
        const direction = Number(moveForward) - Number(moveBackward);
        if (moveForward || moveBackward) pathValue = (pathValue + direction * 0.00015) % 1;
        if (pathValue > 0.704) { pathValue = 0 }
        if (pathValue < 0) { pathValue = 0.704 -pathValue}
        const positionOnCurve = curvePath.getPointAt(pathValue);
        controls.getObject().position.copy(positionOnCurve)
    }
    renderer.render(scene, camera);
}

init();
animate();