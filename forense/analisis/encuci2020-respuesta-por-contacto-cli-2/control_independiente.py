#!/usr/bin/env python3
"""Control externo al estimador: punto y varianza WR de AP5_16_4."""
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
    rows = rpc._read_dbf(z.read(member), ["AP5_16_4", "FAC_SEL", "EST_DIS", "UPM_DIS"])

psu = defaultdict(lambda: [0.0, 0.0])
for row in rows:
    w = rpc._weight(row["FAC_SEL"])
    code = rpc._code(row["AP5_16_4"])
    if w is None or code not in (1, 2):
        continue
    key = (row["EST_DIS"].strip(), row["UPM_DIS"].strip())
    psu[key][0] += w * (code == 1)
    psu[key][1] += w

y = sum(v[0] for v in psu.values()); x = sum(v[1] for v in psu.values()); p = y / x
by_stratum = defaultdict(list)
for (h, _), (yy, xx) in psu.items(): by_stratum[h].append(yy - p * xx)
var = sum(sum(z * z for z in values) / (len(values) - 1)
          for values in by_stratum.values() if len(values) > 1) / (x * x)
print(json.dumps({"variable": "AP5_16_4", "p": p, "varianza_WR_UPM": var,
                  "se_WR": var ** .5, "estratos": len(by_stratum), "upm": len(psu)}, sort_keys=True))
