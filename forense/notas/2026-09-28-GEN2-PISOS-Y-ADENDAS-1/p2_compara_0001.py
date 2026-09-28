"""P2 · compara los RESULT de CALC-PISO-PERSISTENCIA-ERROR-0002 contra los sellados de 0001
(RETROSPECTIVA-MECÁNICA; tolerancia abs 1e-10 de la spec v1.0). Escribe p2-comparacion-0001-0002.tsv."""
import json, sys
from pathlib import Path
R = Path(__file__).resolve().parents[3] / "data/corrida0"
a = json.loads((R / "CALC-PISO-PERSISTENCIA-ERROR-0001/resultados.json").read_text())["resultados"]
b = json.loads((R / "CALC-PISO-PERSISTENCIA-ERROR-0002/resultados.json").read_text())["resultados"]
filas, peor, fallan = [], 0.0, 0
for k in sorted(set(a) | set(b)):
    va, vb = a.get(k, "AUSENTE"), b.get(k, "AUSENTE")
    if isinstance(va, (int, float)) and isinstance(vb, (int, float)) and not isinstance(va, bool):
        d = abs(float(va) - float(vb)); peor = max(peor, d); ok = d <= 1e-10
    else:
        d = ""; ok = va == vb
    fallan += not ok
    filas.append(f"{k}\t{va}\t{vb}\t{d}\t{'COINCIDE' if ok else 'DIFIERE'}")
out = Path(__file__).with_name("p2-comparacion-0001-0002.tsv")
out.write_text("result_id\tsellado_0001\tsellado_0002\tabs_delta\testado\n" + "\n".join(filas) + "\n", encoding="utf-8")
print(f"ids_0001={len(a)} ids_0002={len(b)} union={len(filas)} difieren={fallan} max_abs_delta={peor!r}")
print("DICTAMEN:", "REPRODUCE" if fallan == 0 and set(a) == set(b) else "NO-REPRODUCE")
