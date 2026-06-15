// Constrói o grafo 3D a partir dos fragmentos.
// Layout esférico determinístico (Fibonacci) no v1; força real é refino (B2-3).
import * as THREE from "three";

const COR = {
  arquivo: 0x8fd3ff,
  sensorial: 0xff6b6b,
  memoria: 0x4f9dff,
  identidade_operacional: 0x5ff0d0,
  default: 0x9fb3c8,
};

function kindDe(f) {
  if (f.kind) return f.kind;
  if (f.tipo === "sensorial") return "sensorial";
  if (f.tipo === "identidade_operacional") return "identidade_operacional";
  return "memoria";
}

function ehSensivel(f) {
  return Boolean(f.sensivel ?? f.metadata?.sensivel);
}

export function construirGrafo(fragmentos) {
  const grupo = new THREE.Group();
  const nodes = [];
  const total = Math.max(fragmentos.length, 1);

  fragmentos.forEach((f, i) => {
    const kind = kindDe(f);
    const cor = COR[kind] ?? COR.default;
    const raioNo = kind === "arquivo" ? 0.12 : 0.07;

    const mesh = new THREE.Mesh(
      new THREE.SphereGeometry(raioNo, 18, 18),
      new THREE.MeshStandardMaterial({ color: cor, emissive: cor, emissiveIntensity: 0.45 }),
    );

    // distribuição esférica de Fibonacci (espalha uniforme sem física)
    const phi = Math.acos(1 - (2 * (i + 0.5)) / total);
    const theta = Math.PI * (1 + Math.sqrt(5)) * i;
    const r = 1.7;
    mesh.position.set(
      r * Math.cos(theta) * Math.sin(phi),
      r * Math.sin(theta) * Math.sin(phi) + 1.5,
      r * Math.cos(phi) - 2.6,
    );

    // brain "gus" -> anel orbital branco (gus-30.1)
    if (f.user_id === "gus") {
      const ring = new THREE.Mesh(
        new THREE.RingGeometry(raioNo + 0.03, raioNo + 0.05, 28),
        new THREE.MeshBasicMaterial({ color: 0xffffff, side: THREE.DoubleSide }),
      );
      ring.rotation.x = Math.PI / 2;
      mesh.add(ring);
    }

    mesh.userData.fragmento = f;
    mesh.userData.sensivel = ehSensivel(f);
    grupo.add(mesh);
    nodes.push(mesh);
  });

  return { grupo, nodes };
}
