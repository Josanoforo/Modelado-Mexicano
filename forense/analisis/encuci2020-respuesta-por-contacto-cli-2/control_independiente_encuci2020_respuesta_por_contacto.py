#!/usr/bin/env python3
"""Control externo: unión condicionada a contacto con salud pública."""
import importlib.util
import json
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MEDIDOR = ROOT / "data/corrida0/CALC-ENCUCI2020-RESPUESTA-POR-CONTACTO-0001-v1_1/medidor.py"
spec = importlib.util.spec_from_file_location("rpc", MEDIDOR)
rpc = importlib.util.module_from_spec(spec)
sys.modules["rpc"] = rpc
spec.loader.exec_module(rpc)

payload = ROOT / "data/raw/BD_ENCUCI2020_dbf.zip"
with zipfile.ZipFile(payload) as z:
    member = next(x for x in z.namelist() if x.rsplit("/", 1)[-1] == rpc.MEMBER)
    rows = rpc._read_dbf(z.read(member), ["AP5_16_4", "AP5_17", "AP5_18",
                                           "FAC_SEL", "EST_DIS", "UPM_DIS"])

# El marco se construye primero: toda FAC_SEL válida conserva su UPM, incluso
# cuando su contribución al dominio es cero.
psu = defaultdict(lambda: [0.0, 0.0])
for row in rows:
    w = rpc._weight(row["FAC_SEL"])
    if w is None:
        continue
    key = (row["EST_DIS"].strip(), row["UPM_DIS"].strip())
    # Inicializa la UPM antes de decidir dominio: fuera de él aporta cero.
    _ = psu[key]
    contact, request, delivery = (rpc._code(row[x]) for x in ("AP5_16_4", "AP5_17", "AP5_18"))
    domain = contact == 1 and request in (1, 2) and delivery in (1, 2)
    if domain:
        psu[key][0] += w * (request == 1 or delivery == 1)
        psu[key][1] += w

y = sum(v[0] for v in psu.values()); x = sum(v[1] for v in psu.values()); p = y / x
by_stratum = defaultdict(list)
for (h, _), (yy, xx) in psu.items(): by_stratum[h].append(yy - p * xx)
var = 0.0
for values in by_stratum.values():
    m = len(values)
    if m > 1:
        mean = sum(values) / m
        centered = sum((z - mean) ** 2 for z in values)
        var += (m / (m - 1)) * centered
var /= x * x

published = json.loads((ROOT / "data/corrida0/CALC-ENCUCI2020-RESPUESTA-POR-CONTACTO-0001-v1_1/resultados.json").read_text())
profile = json.loads(published["resultados"]["RESULT-ENCUCI2020-RPCV11-PERFIL-POR-CONTACTO"])
reported = next(x["p_solicitud_o_entrega"]["p"] for x in profile if x["variable"] == "AP5_16_4")
tolerance = 1e-12
print(json.dumps({"estimando": "P(solicitud o entrega | contacto salud publica, AP5_17/18 validas)",
                  "p_control": p, "p_publicado": reported, "delta": p - reported,
                  "tolerancia_abs": tolerance, "coincide": abs(p - reported) <= tolerance,
                  "varianza_WR_UPM": var, "se_WR": var ** .5,
                  "estratos": len(by_stratum), "upm_marco": len(psu)}, sort_keys=True))
