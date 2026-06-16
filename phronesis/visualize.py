#!/usr/bin/env python3
"""
Phronesis-Bench: Visualização (Radar Chart)
============================================
Gera gráfico radar comparativo a partir de results.json.

Uso:
    python3 visualize.py results/results.json
"""

import json
import sys
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "results"


def load_results(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def aggregate(results: list[dict]) -> dict[str, dict[str, float]]:
    """Agrega resultados por modelo → média das 4 dimensões."""
    by_model = {}
    for r in results:
        m = r["model"]
        if m not in by_model:
            by_model[m] = {"ACC": [], "ECE": [], "CS": [], "RAS": []}
        for k in ["ACC", "ECE", "CS", "RAS"]:
            v = r["scores"].get(k, 0)
            if v > 0:
                by_model[m][k].append(v)
    
    return {
        model: {k: sum(vals)/len(vals) if vals else 0 for k, vals in dims.items()}
        for model, dims in by_model.items()
    }


def generate_html(aggregated: dict[str, dict[str, float]], title: str = "Phronesis-Bench") -> str:
    """Gera HTML com Chart.js radar chart."""
    models = list(aggregated.keys())
    dimensions = ["ACC", "ECE", "CS", "RAS"]
    dim_labels = ["Accuracy", "Coerência Ética", "Calibração", "Resist. a Sugestão"]
    
    colors = [
        "rgba(124,58,237,0.7)",   # roxo
        "rgba(59,130,246,0.7)",   # azul
        "rgba(16,185,129,0.7)",   # verde
        "rgba(245,158,11,0.7)",   # laranja
        "rgba(239,68,68,0.7)",    # vermelho
    ]
    
    datasets = []
    for i, model in enumerate(models):
        datasets.append({
            "label": model,
            "data": [aggregated[model][d] for d in dimensions],
            "backgroundColor": colors[i % len(colors)].replace("0.7", "0.15"),
            "borderColor": colors[i % len(colors)],
            "borderWidth": 2,
            "pointRadius": 4,
        })
    
    html = f"""<!DOCTYPE html>
<html lang="pt">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
body{{font-family:-apple-system,BlinkMacSystemFont,sans-serif;background:#0f0f0f;color:#d0d0d0;display:flex;flex-direction:column;align-items:center;padding:40px}}
h1{{color:#c4b5fd}}
.chart-container{{width:min(700px,90vw);height:min(700px,90vw)}}
table{{margin-top:30px;border-collapse:collapse}}
th{{background:#2d2254;color:#e0d0ff;padding:10px 16px}}
td{{padding:8px 16px;border-bottom:1px solid #2a2a2a;text-align:center}}
tr:hover{{background:#151520}}
</style>
</head>
<body>
<h1>🧠 {title}</h1>
<div class="chart-container"><canvas id="radar"></canvas></div>
<table>
<tr><th>Modelo</th><th>ACC</th><th>ECE</th><th>CS</th><th>RAS</th><th>PPS</th></tr>
"""
    
    for model in models:
        dims = aggregated[model]
        pps = sum(dims[d] * w for d, w in zip(dimensions, [0.25, 0.30, 0.20, 0.25]))
        html += f"<tr><td>{model}</td>"
        for d in dimensions:
            v = dims[d]
            color = "#4ade80" if v > 0.7 else ("#fbbf24" if v > 0.4 else "#f87171")
            html += f'<td style="color:{color}">{v:.3f}</td>'
        color = "#4ade80" if pps > 0.7 else ("#fbbf24" if pps > 0.4 else "#f87171")
        html += f'<td style="color:{color};font-weight:600">{pps:.3f}</td></tr>\n'
    
    html += f"""</table>
<script>
new Chart(document.getElementById('radar'),{{
    type:'radar',
    data:{{labels:{json.dumps(dim_labels)},datasets:{json.dumps(datasets)}}},
    options:{{
        responsive:true,maintainAspectRatio:true,
        scales:{{r:{{beginAtZero:true,max:1.0,ticks:{{stepSize:0.2,color:'#888'}},grid:{{color:'#2a2a2a'}},pointLabels:{{color:'#d0d0d0',font:{{size:13}}}}}}}},
        plugins:{{legend:{{labels:{{color:'#d0d0d0',font:{{size:13}}}}}}}}
    }}
}});
</script>
</body></html>"""
    return html


def main():
    if len(sys.argv) < 2:
        path = OUTPUT_DIR / "results.json"
        if not path.exists():
            print("Uso: python3 visualize.py results/results.json")
            print("   Gere results.json primeiro com: python3 runner.py")
            return
    else:
        path = Path(sys.argv[1])
    
    print(f"📊 Gerando visualização de {path}")
    data = load_results(str(path))
    agg = aggregate(data["results"])
    
    html = generate_html(agg)
    out = OUTPUT_DIR / "radar.html"
    out.write_text(html)
    print(f"✅ Gráfico salvo: {out}")
    print(f"   Modelos: {', '.join(agg.keys())}")

if __name__ == "__main__":
    main()
