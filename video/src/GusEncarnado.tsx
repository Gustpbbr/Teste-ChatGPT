import React from "react";
import {
  AbsoluteFill,
  interpolate,
  Sequence,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

const C = {
  bg: "#05070d",
  cyan: "#4fd0e0",
  blue: "#4f9dff",
  red: "#ff6b6b",
  green: "#5ff0d0",
  gold: "#ffd479",
  txt: "#eaf4ff",
  muted: "#7fa6cf",
};

const fonte =
  'system-ui, -apple-system, "Segoe UI", Roboto, sans-serif';

const Fundo: React.FC = () => (
  <AbsoluteFill
    style={{
      background: `radial-gradient(1200px 800px at 50% 35%, #0e2138, ${C.bg} 60%)`,
    }}
  />
);

// Fade in/out por cena, baseado no frame local da Sequence
const Cena: React.FC<{ dur: number; children: React.ReactNode }> = ({
  dur,
  children,
}) => {
  const f = useCurrentFrame();
  const op = interpolate(f, [0, 18, dur - 18, dur], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const y = interpolate(f, [0, 18], [26, 0], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        opacity: op,
        transform: `translateY(${y}px)`,
        padding: 60,
      }}
    >
      {children}
    </AbsoluteFill>
  );
};

const Orbe: React.FC<{ escala?: number }> = ({ escala = 1 }) => {
  const f = useCurrentFrame();
  const pulse = 1 + 0.05 * Math.sin(f / 12);
  return (
    <div
      style={{
        position: "relative",
        width: 260 * escala,
        height: 260 * escala,
        transform: `scale(${pulse})`,
      }}
    >
      <div
        style={{
          position: "absolute",
          inset: 0,
          borderRadius: "50%",
          border: `2px solid ${C.cyan}`,
          opacity: 0.4,
          transform: `rotate(${f * 1.2}deg)`,
        }}
      />
      <div
        style={{
          position: "absolute",
          inset: 46 * escala,
          borderRadius: "50%",
          background: `radial-gradient(circle at 40% 35%, #bfefff, #3aa6d8 45%, #06314a)`,
          boxShadow: `0 0 70px rgba(79,208,224,.6)`,
        }}
      />
    </div>
  );
};

const Card: React.FC<{
  atraso: number;
  children: React.ReactNode;
  cor?: string;
}> = ({ atraso, children, cor = "#1d3a5f" }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: f - atraso, fps, config: { damping: 14 } });
  return (
    <div
      style={{
        background: "#0d1828",
        border: `1px solid ${cor}`,
        borderRadius: 16,
        padding: "22px 26px",
        opacity: s,
        transform: `translateY(${(1 - s) * 24}px)`,
        margin: 8,
      }}
    >
      {children}
    </div>
  );
};

export const GusEncarnado: React.FC = () => {
  return (
    <AbsoluteFill style={{ background: C.bg, fontFamily: fonte, color: C.txt }}>
      <Fundo />

      {/* 0 — título */}
      <Sequence durationInFrames={120}>
        <Cena dur={120}>
          <Orbe />
          <h1 style={{ fontSize: 96, margin: "26px 0 0", letterSpacing: -1 }}>
            Gus Encarnado
          </h1>
          <div style={{ fontSize: 30, color: C.muted, marginTop: 10 }}>
            <span style={{ color: C.cyan }}>corpo</span> ·{" "}
            <span style={{ color: C.cyan }}>sentidos</span> ·{" "}
            <span style={{ color: C.cyan }}>memória</span>
          </div>
        </Cena>
      </Sequence>

      {/* 1 — três camadas */}
      <Sequence from={120} durationInFrames={135}>
        <Cena dur={135}>
          <div style={{ fontSize: 26, color: C.muted, marginBottom: 24 }}>
            um organismo de três camadas
          </div>
          <div style={{ display: "flex", gap: 12 }}>
            <Card atraso={6}>
              <div style={{ fontSize: 46 }}>🖐️</div>
              <h3>Corpo</h3>
              <p style={{ color: C.muted, fontSize: 16 }}>manipular no espaço (VR)</p>
            </Card>
            <Card atraso={16}>
              <div style={{ fontSize: 46 }}>🕸️</div>
              <h3>Alma</h3>
              <p style={{ color: C.muted, fontSize: 16 }}>memória que lembra</p>
            </Card>
            <Card atraso={26}>
              <div style={{ fontSize: 46 }}>👁️</div>
              <h3>Sentidos</h3>
              <p style={{ color: C.muted, fontSize: 16 }}>sensores que percebem</p>
            </Card>
          </div>
        </Cena>
      </Sequence>

      {/* 2 — tese */}
      <Sequence from={255} durationInFrames={120}>
        <Cena dur={120}>
          <div style={{ fontSize: 44, fontWeight: 600, maxWidth: 1100, lineHeight: 1.3 }}>
            Sensor sozinho não é “sentir”.
            <br />
            <span style={{ color: C.cyan }}>
              A memória transforma sensação em percepção.
            </span>
          </div>
        </Cena>
      </Sequence>

      {/* 3 — fluxo */}
      <Sequence from={375} durationInFrames={150}>
        <Cena dur={150}>
          <div style={{ fontSize: 26, color: C.muted, marginBottom: 22 }}>
            como funciona
          </div>
          <div style={{ display: "flex", alignItems: "center", flexWrap: "wrap", justifyContent: "center" }}>
            {[
              "👁️ Sensores",
              "→",
              "🔌 Gateway",
              "→",
              "🕸️ Hub",
              "↔",
              "🧠 Cérebro",
              "↔",
              "🖐️ Corpo",
            ].map((t, i) =>
              t.length <= 2 ? (
                <span key={i} style={{ color: C.cyan, fontSize: 30, margin: 6 }}>
                  {t}
                </span>
              ) : (
                <Card key={i} atraso={i * 6}>
                  <span style={{ fontSize: 20 }}>{t}</span>
                </Card>
              )
            )}
          </div>
          <div style={{ color: C.muted, fontSize: 17, marginTop: 18 }}>
            o Gateway é 90% filtro · dado sensível: rota local
          </div>
        </Cena>
      </Sequence>

      {/* 4 — blocos */}
      <Sequence from={525} durationInFrames={150}>
        <Cena dur={150}>
          <div style={{ fontSize: 26, color: C.muted, marginBottom: 22 }}>o roadmap</div>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(3,1fr)", gap: 12, maxWidth: 980 }}>
            {[
              ["0 · Interocepção", "✅ pronto", C.green],
              ["1 · 1º sentido", "✅ pronto", C.green],
              ["2 · Corpo lê", "🟡 scaffold", C.gold],
              ["3 · Corpo escreve", "🟡 parcial", C.gold],
              ["4 · Tempo real", "⏳ a fazer", C.muted],
              ["5 · Proatividade", "🟡 núcleo", C.gold],
            ].map(([titulo, status, cor], i) => (
              <Card key={i} atraso={i * 5} cor="#1d3a5f">
                <b style={{ fontSize: 18 }}>{titulo}</b>
                <div style={{ fontSize: 14, color: cor as string }}>{status}</div>
              </Card>
            ))}
          </div>
        </Cena>
      </Sequence>

      {/* 5 — fecho */}
      <Sequence from={675} durationInFrames={135}>
        <Cena dur={135}>
          <Orbe escala={0.7} />
          <div style={{ fontSize: 46, fontWeight: 600, maxWidth: 1100, marginTop: 20 }}>
            um organismo que <span style={{ color: C.cyan }}>sente</span>,{" "}
            <span style={{ color: C.cyan }}>habita</span> e{" "}
            <span style={{ color: C.cyan }}>lembra</span>
          </div>
          <div style={{ color: C.muted, fontSize: 18, marginTop: 14 }}>
            não é mágica — é arquitetura
          </div>
        </Cena>
      </Sequence>
    </AbsoluteFill>
  );
};
