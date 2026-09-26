"""ACTO GEN2-SEGURIDAD-ENSU-SERIE-1 · prueba sintética del medidor ENSU (D-22).

No toca el corpus: fabrica payloads anuales con la forma que la spec declara
(DBF con descriptor de 32 bytes por campo en 2013-2020, CSV con BOM y `\\r` en
2021+, zips anidados como los publica INEGI) y corre el `medir()` real con el
contrato de cada CALC. Comprueba:

  1. el conjunto de ids devuelto es EXACTAMENTE el de `esquema_resultados`
     (`corrida0._valida_outputs` vacío), en los dos puntos de entrada;
  2. las tres eras de llaves (ENT/CON/V_SEL · UPM/VIV_SEL/R_SEL · SEXO en CB);
  3. reglas de par R1-R4 (spec §5) y que la guardia rechaza el año 2026;
  4. `medidor.py` de cada CALC es byte a byte `tools/dominios/ensu/ensu_medidor.py`.
"""
from __future__ import annotations

import hashlib
import importlib.util
import io
import random
import struct
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

_s = importlib.util.spec_from_file_location("ensu_medidor", RAIZ / "tools/dominios/ensu/ensu_medidor.py")
M = importlib.util.module_from_spec(_s)
_s.loader.exec_module(M)

from tools import corrida0  # noqa: E402

RECETA = RAIZ / "tools/dominios/salud/pisos_diseno.py"
DICT = RAIZ / "tools/series/dictamen.py"
CALCS = ("CALC-ENSU-PISOS-0001", "CALC-ENSU-SERIE-0001")


def dbf(cols, filas):
    """DBF III mínimo: campos C de ancho 12."""
    ancho = 12
    hl = 32 + 32 * len(cols) + 1
    rl = 1 + ancho * len(cols)
    b = bytearray(struct.pack("<BBBBIHH20x", 3, 126, 1, 1, len(filas), hl, rl))
    for c in cols:
        b += c.encode("latin-1").ljust(11, b"\0") + b"C" + b"\0" * 4 + bytes([ancho]) + b"\0" * 15
    b += b"\x0d"
    for f in filas:
        b += b" " + b"".join(str(v).encode("latin-1").ljust(ancho)[:ancho] for v in f)
    b += b"\x1a"
    return bytes(b)


def csv(cols, filas):
    t = ",".join(cols) + "\r" + "\r".join(",".join(str(v) for v in f) for f in filas) + "\r"
    return "﻿".encode() + t.encode("utf-8")


def zipb(miembros):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        for n, b in miembros.items():
            z.writestr(n, b)
    return buf.getvalue()


MES = {1: "03", 2: "06", 3: "09", 4: "12"}


def _reac(ola):
    era1 = ola <= M.ERA1_FIN
    return sorted({(c[2] if era1 else c[1]) for c in M.CONDUCTAS if (c[2] if era1 else c[1])}
                  | {v for v, _ in M.FILTRO.values()})


def tablas_ola(ola, rng, n=240):
    """(cb_bytes, cs_bytes|None, ext) de un trimestre sintético."""
    era1, era3 = ola <= M.ERA1_FIN, ola >= M.ERA3_INI
    reac = _reac(ola)
    cds = ["01", "02", "03"] if ola < "2021" else ["01", "02", "03", "55"]
    cb, cs = [], []
    for i in range(n):
        cd = cds[i % len(cds)]
        est = str(1 + rng.randrange(3))
        upm = f"{1 + rng.randrange(6):05d}"
        w = str(rng.randrange(50, 900))
        resp = {v: rng.choice(["1", "2", "3", "4", "9", "", "2", "1"]) for v in reac}
        sexo, edad = rng.choice(["1", "2"]), str(rng.choice([19, 33, 50, 71, 98]))
        if era1:
            fila = {"CD": cd, "EDIS": est, "UPM_DIS": upm, "FACTOR": w, "ENT": "01", "CON": f"{i:05d}",
                    "V_SEL": "1", "N_HOG": "1", "H_MUD": "0", "N_REN": "01"}
            cs.append([f"{1:02d}", f"{i:05d}", "1", "1", "0", "1", sexo, edad])
        else:
            fila = {"CD": cd, "EST_DIS": f"{int(cd) * 10 + int(est):04d}", "UPM_DIS": upm, "FAC_SEL": w,
                    "UPM": f"{int(cd):02d}{i:05d}", "VIV_SEL": "1", "H_MUD": "0", "R_SEL": "2"}
            if era3:
                fila.update({"SEXO": sexo, "EDAD": edad})
            else:
                cs.append([f"{int(cd):02d}{i:05d}", "1", "0", "02", sexo, edad])
        fila.update(resp)
        cb.append(fila)
    cols = list(cb[0])
    filas = [[f[c] for c in cols] for f in cb]
    if era1:
        cs_cols = ["ENT", "CON", "V_SEL", "N_HOG", "H_MUD", "N_REN", "SEX", "EDA"]
    else:
        cs_cols = ["UPM", "VIV_SEL", "H_MUD", "N_REN", "SEX", "EDA"]
    if ola >= "2021":
        return csv(cols, filas), (csv(cs_cols, cs) if cs else None), "csv"
    return dbf(cols, filas), (dbf(cs_cols, cs) if cs else None), "dbf"


def payload(anio, olas, rng):
    """Zip anual con la forma INEGI: DBF en carpeta (<=2016), zip anidado (2017+)."""
    externos = {}
    for ola in olas:
        mm, aa = MES[int(ola[-1])], ola[2:4]
        cb, cs, ext = tablas_ola(ola, rng)
        sfx = "_sec1_2_3" if ola == "2020T3" else ""
        inner = {f"ENSU_CB{sfx}_{mm}{aa}.{ext}": cb}
        if ola == "2020T3":
            inner[f"ENSU_CB_sec4_{mm}{aa}.{ext}"] = cb
        if cs is not None:
            inner[f"ENSU_CS_{mm}{aa}.{ext}"] = cs
        if anio <= 2016:
            for k, v in inner.items():
                externos[f"ensu_bd_{ola}/{k}"] = v
        else:
            externos[f"ensu_bd_{ola}_{ext}.zip"] = zipb(inner)
    return zipb(externos)


def contrato(punto, olas, tmp, rng):
    disp = {c: [o for o in olas if not (
        (c in ("C02-INSEG-CALLE", "C03-INSEG-CAJERO", "C04-INSEG-TRANSPORTE", "C05-EXPECT-EMPEORA",
               "C13-POLICIA-MUN-CONFIANZA", "C14-POLICIA-MUN-EFECTIVA") and o <= M.ERA1_FIN)
        or (c == "C15-CORRUPCION-POLICIA" and (o < "2019T2" or (o[-1] not in "24" and o != "2020T3"))))] for c in M.NOMBRES}
    payloads, inputs = {}, {}
    anios = sorted({int(o[:4]) for o in olas})
    for a in M.ANIOS:
        pid = f"ensu{a}_sint"
        payloads[str(a)] = pid
        ruta = Path(tmp) / f"ensu_bd_{a}.zip"
        if a in anios:
            ruta.write_bytes(payload(a, [o for o in olas if o.startswith(str(a))], rng))
        else:
            ruta.write_bytes(zipb({"vacio.txt": b""}))
        inputs[pid] = {"ruta_absoluta": str(ruta)}
    for k, p in (("receta_pisos", RECETA), ("dictamen_series", DICT)):
        b = p.read_bytes()
        inputs[k] = {"bytes": b, "sha256": hashlib.sha256(b).hexdigest()}
    c = {"parametros": {"punto_de_entrada": punto, "bootstrap_replicas": 20, "olas": olas,
                        "payloads": payloads, "disponibilidad": disp},
         "seed": {"valor": 20260925}}
    return inputs, c, disp


OLAS = ["2015T3", "2015T4", "2016T1", "2019T4", "2020T1", "2020T3", "2021T2", "2025T4"]


class TestMedidorEnsu(unittest.TestCase):
    def _corre(self, punto, olas):
        with tempfile.TemporaryDirectory() as tmp:
            inputs, c, disp = contrato(punto, olas, tmp, random.Random(7))
            out = M.medir(inputs, c)
        esquema = M.esquema_resultados(punto, olas, disp)
        return out, esquema

    def test_serie_ids_exactos(self):
        out, esq = self._corre("serie", OLAS)
        self.assertEqual(corrida0._valida_outputs({"resultados": esq}, out), [])
        self.assertIn("RESULT-ENSU-DICTAMEN-TAU2-TRIMESTRAL-TOTAL", out)
        d = out["RESULT-ENSU-DICTAMEN-C01-INSEG-CIUDAD-TOTAL-TODOS-DICTAMEN"]
        self.assertIn(d, M_VOCAB)

    def test_pisos_ids_exactos(self):
        out, esq = self._corre("pisos", ["2024T1", "2025T3", "2025T4"])
        self.assertEqual(corrida0._valida_outputs({"resultados": esq}, out), [])
        self.assertGreater(out["RESULT-ENSU-PISOS-C01-INSEG-CIUDAD-2025T4-CIUDAD-55-N"], 0)
        self.assertEqual(out["RESULT-ENSU-PISOS-C01-INSEG-CIUDAD-2025T4-CIUDAD-96-N"], 0)
        self.assertIsNone(out["RESULT-ENSU-PISOS-C01-INSEG-CIUDAD-2025T4-CIUDAD-96-P"])

    def test_eras_de_llaves(self):
        out, _ = self._corre("serie", OLAS)
        for ola in ("2015T4", "2019T4", "2020T3"):
            self.assertEqual(out[f"RESULT-ENSU-SERIE-G-{ola}-JOIN-SIN-CS"], 0, ola)
            self.assertGreater(out[f"RESULT-ENSU-SERIE-C01-INSEG-CIUDAD-{ola}-SEXO-MUJER-N"], 0, ola)
        # edad 98 (no especificada) queda fuera del eje, no en 60-MAS
        n_eje = sum(out[f"RESULT-ENSU-SERIE-C01-INSEG-CIUDAD-2025T4-EDAD-{e}-N"] for e, _, _ in M.EDADES)
        self.assertLess(n_eje, out["RESULT-ENSU-SERIE-C01-INSEG-CIUDAD-2025T4-TOTAL-TODOS-N"])
        # 2013-2015 sin eje CIUDAD
        self.assertNotIn("RESULT-ENSU-SERIE-C01-INSEG-CIUDAD-2015T4-CIUDAD-01-P", out)

    def test_reglas_de_par(self):
        d = {o: {"CIUDADES-SHA256": "x"} for o in OLAS}
        d["2021T2"] = {"CIUDADES-SHA256": "y"}
        pe = M.par_estado
        self.assertEqual(pe("C01-INSEG-CIUDAD", "TOTAL", "2015T4", "2016T1", d), "CAMBIO-DOCUMENTADO")
        self.assertEqual(pe("C13-POLICIA-MUN-CONFIANZA", "TOTAL", "2020T1", "2020T3", d), "CAMBIO-DOCUMENTADO")
        self.assertEqual(pe("C01-INSEG-CIUDAD", "TOTAL", "2020T1", "2020T3", d), "COMPARABLE")
        self.assertEqual(pe("C01-INSEG-CIUDAD", "SEXO", "2020T3", "2021T2", d), "CAMBIO-DOCUMENTADO")
        self.assertEqual(pe("C01-INSEG-CIUDAD", "CIUDAD", "2020T3", "2021T2", d), "COMPARABLE")

    def test_guardia_2026(self):
        with tempfile.TemporaryDirectory() as tmp:
            inputs, c, _ = contrato("pisos", ["2025T4"], tmp, random.Random(1))
            inputs[c["parametros"]["payloads"]["2025"]]["ruta_absoluta"] = "/x/INEGI/ENSU/2026/ensu_bd_2026_csv.zip"
            with self.assertRaises(M.ParoDeGuardia):
                M.medir(inputs, c)

    def test_medidor_byte_a_byte(self):
        fuente = (RAIZ / "tools/dominios/ensu/ensu_medidor.py").read_bytes()
        for calc in CALCS:
            p = RAIZ / "data/corrida0" / calc / "medidor.py"
            if p.exists():
                self.assertEqual(p.read_bytes(), fuente, calc)


_d = importlib.util.spec_from_file_location("dictamen_series", DICT)
_D = importlib.util.module_from_spec(_d)
_d.loader.exec_module(_D)
M_VOCAB = _D.VOCAB

if __name__ == "__main__":
    unittest.main()
