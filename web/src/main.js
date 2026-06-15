// Bloco 2 — corpo lê. Liga: Hub (leitura) -> grafo 3D -> cena -> seleção.
import * as THREE from "three";

import { carregarFragmentos } from "./hub.js";
import { construirGrafo } from "./graph.js";
import { criarCena } from "./scene.js";
import { mostrarPainel, esconderPainel } from "./focus.js";

const { scene, camera, renderer } = criarCena();

const fragmentos = await carregarFragmentos();
const { grupo, nodes } = construirGrafo(fragmentos);
scene.add(grupo);

// Seleção por clique (desktop). Gaze/controle/mão é Bloco 3.
const raycaster = new THREE.Raycaster();
const ponteiro = new THREE.Vector2();

addEventListener("pointerdown", (e) => {
  ponteiro.x = (e.clientX / innerWidth) * 2 - 1;
  ponteiro.y = -(e.clientY / innerHeight) * 2 + 1;
  raycaster.setFromCamera(ponteiro, camera);
  const hit = raycaster.intersectObjects(nodes, false)[0];
  if (hit) {
    mostrarPainel(hit.object.userData.fragmento, hit.object.userData.sensivel);
  } else {
    esconderPainel();
  }
});

renderer.setAnimationLoop(() => {
  grupo.rotation.y += 0.0015; // leve giro pra dar volume
  renderer.render(scene, camera);
});
