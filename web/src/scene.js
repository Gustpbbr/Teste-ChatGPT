// Cena Three.js + WebXR. Desktop tem fallback (sem headset); o botão VR
// aparece quando o navegador suporta WebXR (ex.: browser do Quest).
import * as THREE from "three";
import { VRButton } from "three/addons/webxr/VRButton.js";

export function criarCena() {
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x05070d);

  const camera = new THREE.PerspectiveCamera(70, innerWidth / innerHeight, 0.1, 100);
  camera.position.set(0, 1.5, 0);

  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(innerWidth, innerHeight);
  renderer.setPixelRatio(devicePixelRatio);
  renderer.xr.enabled = true;
  document.body.appendChild(renderer.domElement);
  document.body.appendChild(VRButton.createButton(renderer));

  scene.add(new THREE.HemisphereLight(0x88aaff, 0x080820, 1.3));

  addEventListener("resize", () => {
    camera.aspect = innerWidth / innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(innerWidth, innerHeight);
  });

  return { scene, camera, renderer };
}
