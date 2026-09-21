#!/usr/bin/env python3
"""Conducto de `tools/enut_nucleo.py` y de los tres CALC del acto
GEN2-ENUT-PISOS-Y-SERIE-1 (21/sep/2026) — D-22 ampliada, ANTES de abrir dato:

  · sintético por ola (2024 CSV, 2019 CSV, 2014 DBF anidado, 2009 DBF): el
    punto de entrada `medir_ola` corre de punta a punta y su salida pasa por
    `corrida0._valida_outputs` contra el `spec.yaml` real de cada CALC, en
    todos los caminos: celda con soporte, celda rara (n=0 → nulos declarados),
    ítem «Sí» sin tiempo, hogar sin ponderador, persona sin categoría;
  · respuesta conocida: la media ponderada nacional y la razón de hogar se
    recalculan a mano sobre el sintético y deben coincidir (tolerancia 1e-9);
  · validación CONCP y oro: en el sintético tvar_crea = suma de ítems, así
    que `VALIDACION-CONCP-MAX-ABS` = 0 y `ORO-A-R-DELTA` = 0 contra la razón
    recalculada en el test;
  · `ITEMS` coteja con `data/enut-comparabilidad-texto-v1_0.tsv` (P1): los
    sufijos de cada variante son los de la tabla, no otros;
  · la guardia de una sola variable: `celdas_de_eje` rechaza lista, dos
    argumentos y eje fuera de lista; `auditoria_ast()` PASA sobre el módulo
    real y FALLA sobre once mutaciones (control positivo por regla, R1-R6).

Necesita numpy/pandas/dbfread (CI no los instala: FP-398 (a)); corre en CAJA.
Cero microdato real: todo lo que abre lo escribe él mismo en un tmpdir.
"""
from __future__ import annotations

import importlib.util
import io
import json
import os
import struct
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "tools"))
import enut_nucleo as N  # noqa: E402

CALCS = {"2024": "CALC-ENUT2024-NUCLEO-EJES-0001", "2019": "CALC-ENUT2019-NUCLEO-EJES-0001",
         "serie": "CALC-ENUT-SERIE-2009-2014-NUCLEO-0001"}
REPS = 120


def _corrida0():
    spec = importlib.util.spec_from_file_location("corrida0", RAIZ / "tools" / "corrida0.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["corrida0"] = mod
    spec.loader.exec_module(mod)
    return mod


def _spec_yaml(calc: str) -> dict:
    import yaml
    return yaml.safe_load((RAIZ / "data" / "corrida0" / calc / "spec.yaml").read_text(encoding="utf-8"))


# ── escritores sintéticos ───────────────────────────────────────────────────
def _csv(rows: list[dict], cols: list[str]) -> bytes:
    out = [",".join(cols)]
    for r in rows:
        out.append(",".join(str(r.get(c, "")) for c in cols))
    return ("\n".join(out) + "\n").encode("utf-8")


def _dbf(rows: list[dict], cols: list[str], ancho: int = 12) -> bytes:
    """dBase III mínimo: todos los campos 'C' de `ancho`, sin memo."""
    n = len(rows)
    hdr_len = 32 + 32 * len(cols) + 1
    rec_len = 1 + ancho * len(cols)
    head = struct.pack("<BBBBIHH20x", 0x03, 24, 1, 1, n, hdr_len, rec_len)
    fields = b""
    for c in cols:
        fields += struct.pack("<11sc4xBB14x", c.encode("ascii").ljust(11, b"\0"), b"C", ancho, 0)
    body = b""
    for r in rows:
        body += b" " + b"".join(str(r.get(c, "")).encode("latin-1").ljust(ancho)[:ancho] for c in cols)
    return head + fields + b"\r" + body + b"\x1a"


def _persona(i: int, sexo: str, edad: int, niv: str, tloc: str, est: str, upm: str, fac: str, hog: str) -> dict:
    return {"SEXO": sexo, "EDAD": str(edad), "NIV": niv, "TLOC": tloc, "EST_DIS": est, "UPM_DIS": upm,
            "FAC_PER": fac, "_hog": hog, "_i": i}


def _poblacion() -> list[dict]:
    """20 personas en 3 estratos × 2-3 UPM; ninguna en `secundaria` (celda
    rara → nulos); una sin FAC_PER; una con NIV inválido; una edad < 12."""
    P = []
    base = [("1", 15, "2", "1"), ("2", 25, "6", "1"), ("2", 35, "8", "4"), ("1", 45, "0", "2"),
            ("2", 65, "9", "3"), ("1", 70, "4", "4"), ("2", 42, "2", "1"), ("1", 33, "7", "1"),
            ("2", 19, "6", "4"), ("1", 58, "8", "1")]
    hogs = ["H1", "H1", "H2", "H2", "H3", "H3", "H4", "H5", "H5", "H6"]
    k = 0
    for est, upms in (("01", ["001", "002"]), ("02", ["003", "004", "005"]), ("03", ["006", "007"])):
        for upm in upms:
            for j in range(3):
                if k >= 20:
                    break
                s, e, n, t = base[k % 10]
                P.append(_persona(k, s, e, n, t, est, upm, str(10 + k), hogs[k % 10] + est))
                k += 1
    P[3]["FAC_PER"] = ""          # sin ponderador
    P[7]["NIV"] = "99"            # escolaridad inválida
    P[11]["EDAD"] = "9"           # fuera de edad
    return P


def _tiempos(i: int, suf_idx: int) -> tuple[str, str, str, str, str]:
    """(Sí, h_LV, m_LV, h_SD, m_SD) determinista; algunos ítems «Sí» sin tiempo."""
    if (i + suf_idx) % 3 == 0:
        return "2", "", "", "", ""
    if (i * 7 + suf_idx) % 11 == 0:
        return "1", "", "", "", ""          # Sí sin tiempo declarado
    return "1", str((i + suf_idx) % 5), str((i * 3) % 60), str(suf_idx % 3), str((i * 13) % 60)


def _horas(t) -> float:
    def f(x):
        return float(x) if x != "" else 0.0
    return f(t[1]) + f(t[2]) / 60 + f(t[3]) + f(t[4]) / 60


class Sintetico:
    """Construye el zip de una ola y la respuesta conocida."""

    def __init__(self, ola: str, tmp: str):
        self.ola, self.tmp = ola, tmp
        self.P = _poblacion()
        self.zip = os.path.join(tmp, f"enut{ola}.zip")
        self.horas = {}          # variante → {i: horas}
        getattr(self, f"_build_{ola}")()

    def _items_ola(self, i: int, p: dict, variantes: tuple[str, ...]) -> dict:
        """Escribe TODOS los ítems de la ola (para 2024, los de TODOS) y
        acumula las horas por variante."""
        fila = {}
        todos = N.ITEMS[self.ola].get("TODOS") or N.ITEMS[self.ola].get("NUCLEO") or N.ITEMS[self.ola]["MIN"]
        k = 0
        acum = {v: 0.0 for v in variantes}
        for bloque, sufs in todos.items():
            if self.ola == "2009" and bloque == "5.10":
                continue
            for s in sufs:
                si, ts = N._cols_item(self.ola, bloque, s)
                t = _tiempos(i, k)
                k += 1
                fila[si] = t[0]
                for c, v in zip(ts, t[1:]):
                    fila[c] = v
                h = _horas(t)
                for v in variantes:
                    if s in N.ITEMS[self.ola][v].get(bloque, []):
                        acum[v] += h
        for v in variantes:
            self.horas.setdefault(v, {})[i] = acum[v]
        return fila

    def _build_2024(self):
        cols_mod = ["LLAVEMOD", "LLAVEHOG", "SEXO", "EDAD_V", "NIV", "TLOC", "EST_DIS", "UPM_DIS", "FAC_PER"]
        cols_mod += N.columnas_de("2024", "TODOS")
        mod, tv, ts = [], [], []
        hog_w = {}
        for p in self.P:
            i = p["_i"]
            fila = {"LLAVEMOD": f"M{i:03d}", "LLAVEHOG": p["_hog"], "SEXO": p["SEXO"], "EDAD_V": p["EDAD"],
                    "NIV": p["NIV"].zfill(2), "TLOC": p["TLOC"], "EST_DIS": p["EST_DIS"], "UPM_DIS": p["UPM_DIS"],
                    "FAC_PER": p["FAC_PER"]}
            fila.update(self._items_ola(i, p, ("NUCLEO", "MIN")))
            mod.append(fila)
            # tvar_crea = suma exacta por bloque de TODOS los ítems
            fila_tv = {"LLAVEMOD": f"M{i:03d}", "LLAVEHOG": p["_hog"], "SEXO": p["SEXO"], "EDAD": p["EDAD"],
                       "FAC_PER": p["FAC_PER"], "EST_DIS": p["EST_DIS"], "UPM_DIS": p["UPM_DIS"], "CUID_INT_15A59": "0"}
            k = 0
            for bloque, sufs in N.ITEMS["2024"]["TODOS"].items():
                tot = 0.0
                for s in sufs:
                    tot += _horas(_tiempos(i, k))
                    k += 1
                fila_tv[N.CONCP_COLS[bloque]] = repr(tot)
            tv.append(fila_tv)
            hog_w.setdefault(p["_hog"], 100 + len(hog_w) * 7)
        # la variante CONCP se lee de tvar_crea: igual a TODOS por construcción
        self.horas["CONCP"] = {p["_i"]: sum(float(r[c]) for c in N.CONCP_COLS.values())
                               for p, r in zip(self.P, tv)}
        for h, w in hog_w.items():
            ts.append({"LLAVEHOG": h, "FAC_HOG": "" if h.startswith("H6") else str(w)})
            ts.append({"LLAVEHOG": h, "FAC_HOG": "" if h.startswith("H6") else str(w)})
        self.hog_w = {h: (None if h.startswith("H6") else w) for h, w in hog_w.items()}
        cols_tv = list(tv[0].keys())
        with zipfile.ZipFile(self.zip, "w") as z:
            z.writestr("tmodulo.csv", _csv(mod, cols_mod))
            z.writestr("tvar_crea.csv", _csv(tv, cols_tv))
            z.writestr("tsdem.csv", _csv(ts, ["LLAVEHOG", "FAC_HOG"]))
            z.writestr("thogar.csv", b"LLAVEHOG\n")

    def _build_2019(self):
        cols = ["UPM", "VIV_SEL", "HOGAR", "N_REN", "SEXO", "EDAD_V", "NIV", "TLOC", "EST_DIS", "UPM_DIS", "FAC_PER"]
        cols += N.columnas_de("2019", "NUCLEO")
        mod, hg, hog_w = [], [], {}
        for p in self.P:
            i = p["_i"]
            upm, viv, hog = p["_hog"][:2], "01", p["_hog"][2:]
            fila = {"UPM": upm, "VIV_SEL": viv, "HOGAR": hog, "N_REN": f"{i:02d}", "SEXO": p["SEXO"],
                    "EDAD_V": p["EDAD"], "NIV": p["NIV"], "TLOC": p["TLOC"], "EST_DIS": p["EST_DIS"],
                    "UPM_DIS": p["UPM_DIS"], "FAC_PER": p["FAC_PER"]}
            fila.update(self._items_ola(i, p, ("NUCLEO", "MIN")))
            mod.append(fila)
            hog_w.setdefault(p["_hog"], 100 + len(hog_w) * 7)
        for h, w in hog_w.items():
            hg.append({"UPM": h[:2], "VIV_SEL": "01", "HOGAR": h[2:], "FAC_HOG": "" if h.startswith("H6") else str(w)})
        self.hog_w = {h: (None if h.startswith("H6") else w) for h, w in hog_w.items()}
        with zipfile.ZipFile(self.zip, "w") as z:
            z.writestr("enut_2019/TMODULO.csv", _csv(mod, cols))
            z.writestr("enut_2019/THOGAR.csv", _csv(hg, ["UPM", "VIV_SEL", "HOGAR", "FAC_HOG"]))

    def _build_2014(self):
        it = N.ITEMS["2014"]["NUCLEO"]
        c2 = [c for b in ("6.11", "6.12", "6.13") for s in it[b] for c in [N._cols_item("2014", b, s)[0]] + N._cols_item("2014", b, s)[1]]
        c3 = [c for s in it["6.15"] for c in [N._cols_item("2014", "6.15", s)[0]] + N._cols_item("2014", "6.15", s)[1]]
        llave = ["CONTROL", "VIV_SEL", "HOGAR", "N_REN"]
        m2, m3, m1, sd, hg, hog_w = [], [], [], [], [], {}
        for p in self.P:
            i = p["_i"]
            k = {"CONTROL": p["_hog"][:2], "VIV_SEL": "01", "HOGAR": p["_hog"][2:], "N_REN": f"{i:02d}"}
            items = self._items_ola(i, p, ("NUCLEO", "MIN"))
            m2.append({**k, "TLOC": p["TLOC"], "UPM_DIS": p["UPM_DIS"], "EDIS": p["EST_DIS"], "FAC_PER": p["FAC_PER"],
                       **{c: items[c] for c in c2}})
            m3.append({**k, **{c: items[c] for c in c3}})
            m1.append({**k, "NIV": p["NIV"]})
            sd.append({**k, "SEXO": p["SEXO"], "EDAD": p["EDAD"]})
            hog_w.setdefault(p["_hog"], 100 + len(hog_w) * 7)
        for h, w in hog_w.items():
            hg.append({"CONTROL": h[:2], "VIV_SEL": "01", "HOGAR": h[2:], "FAC_VIV": "" if h.startswith("H6") else str(w)})
        self.hog_w = {h: (None if h.startswith("H6") else w) for h, w in hog_w.items()}
        inner = io.BytesIO()
        with zipfile.ZipFile(inner, "w") as z:
            z.writestr("TMODULO2.dbf", _dbf(m2, llave + ["TLOC", "UPM_DIS", "EDIS", "FAC_PER"] + c2))
            z.writestr("TMODULO3.dbf", _dbf(m3, llave + c3))
            z.writestr("TMODULO1.dbf", _dbf(m1, llave + ["NIV"]))
            z.writestr("TSDem.dbf", _dbf(sd, llave + ["SEXO", "EDAD"]))
            z.writestr("THOGAR.dbf", _dbf(hg, ["CONTROL", "VIV_SEL", "HOGAR", "FAC_VIV"]))
        with zipfile.ZipFile(self.zip, "w") as z:
            z.writestr("Enut2014.zip", inner.getvalue())
            z.writestr("Enut2014_PoblacionIndigena.zip", b"")

    def _build_2009(self):
        it = N.ITEMS["2009"]["MIN"]
        cm = [c for b in ("5.11", "5.12", "5.13") for s in it[b] for c in [N._cols_item("2009", b, s)[0]] + N._cols_item("2009", b, s)[1]]
        cc = [c for s in it["5.10"] for c in [N._cols_item("2009", "5.10", s)[0]] + N._cols_item("2009", "5.10", s)[1]]
        llave = ["CONTROL", "VIV_SEL", "HOGAR", "N_REN"]
        m2, tc, sd, hg, hog_w = [], [], [], [], {}
        for p in self.P:
            i = p["_i"]
            k = {"CONTROL": p["_hog"][:2], "VIV_SEL": "01", "HOGAR": p["_hog"][2:], "N_REN": f"{i:02d}"}
            items = self._items_ola(i, p, ("MIN",))
            m2.append({**k, "LOC": "2" if p["TLOC"] == "4" else "1", "EST_DIS": p["EST_DIS"], "UPM_DIS": p["UPM_DIS"],
                       "FAC_PER": p["FAC_PER"], **{c: items[c] for c in cm}})
            sd.append({**k, "SEXO": p["SEXO"], "EDAD": p["EDAD"], "NIV": p["NIV"] if p["NIV"] != "99" else "b"})
            # 5.10: dos dependientes (N_REF) para las personas pares, cero para impares
            if i % 2 == 0:
                for ref in ("01", "02"):
                    fila = {**k, "N_REF": ref}
                    kk = 100 + int(ref)
                    for s in it["5.10"]:
                        si, ts = N._cols_item("2009", "5.10", s)
                        t = _tiempos(i, kk)
                        kk += 1
                        fila[si] = t[0]
                        for c, v in zip(ts, t[1:]):
                            fila[c] = v
                        self.horas["MIN"][i] += _horas(t)
                    tc.append(fila)
            hog_w.setdefault(p["_hog"], 100 + len(hog_w) * 7)
        for h, w in hog_w.items():
            hg.append({"CONTROL": h[:2], "VIV_SEL": "01", "HOGAR": h[2:], "FAC_VIV": "" if h.startswith("H6") else str(w)})
        self.hog_w = {h: (None if h.startswith("H6") else w) for h, w in hog_w.items()}
        with zipfile.ZipFile(self.zip, "w") as z:
            z.writestr("TModulo2.dbf", _dbf(m2, llave + ["LOC", "EST_DIS", "UPM_DIS", "FAC_PER"] + cm))
            z.writestr("TCuidados.dbf", _dbf(tc, llave + ["N_REF"] + cc))
            z.writestr("TSDem.dbf", _dbf(sd, llave + ["SEXO", "EDAD", "NIV"]))
            z.writestr("THogar.dbf", _dbf(hg, ["CONTROL", "VIV_SEL", "HOGAR", "FAC_VIV"]))

    # respuesta conocida
    def media_nacional(self, v: str) -> float:
        num = den = 0.0
        for p in self.P:
            if p["FAC_PER"] == "":
                continue
            w = float(p["FAC_PER"])
            num += w * self.horas[v][p["_i"]]
            den += w
        return num / den

    def razon(self, v: str) -> float:
        hog: dict[str, list[float]] = {}
        for p in self.P:
            h = hog.setdefault(p["_hog"], [0.0, 0.0])
            y = self.horas[v][p["_i"]]
            h[1] += y
            if p["SEXO"] == "2" and int(p["EDAD"]) >= 40:
                h[0] += y
        num = den = 0.0
        for k, (a, b) in hog.items():
            w = self.hog_w[k]
            if w is None:
                continue
            num += w * a
            den += w * b
        return num / den


class TestConducto(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(dir=os.environ.get("TMPDIR"))
        cls.c0 = _corrida0()
        cls.S = {ola: Sintetico(ola, cls.tmp) for ola in ("2024", "2019", "2014", "2009")}
        cls.out = {}
        for ola, s in cls.S.items():
            oro = {"A_R": s.razon("CONCP")} if ola == "2024" else None
            cls.out[ola] = N.medir_ola(ola, s.zip, reps=REPS, seed=42, oro=oro)
            cls.out[ola][f"RESULT-ENUT{ola}-AUDITORIA-AST"] = "PASA"

    def _valida(self, calc: str, valores: dict):
        spec = _spec_yaml(calc)
        problemas = self.c0._valida_outputs(spec, valores)
        self.assertEqual(problemas, [], problemas[:10])

    def test_2024_conducto_y_valida_outputs(self):
        self._valida(CALCS["2024"], self.out["2024"])

    def test_2019_conducto_y_valida_outputs(self):
        self._valida(CALCS["2019"], self.out["2019"])

    def test_serie_conducto_y_valida_outputs(self):
        v = dict(self.out["2014"])
        v.update(self.out["2009"])
        self._valida(CALCS["serie"], v)

    def test_catalogo_es_el_spec(self):
        for ola, calc in (("2024", CALCS["2024"]), ("2019", CALCS["2019"])):
            ids = {r["id"] for r in N.catalogo_resultados(ola)}
            self.assertEqual(ids, {r["id"] for r in _spec_yaml(calc)["resultados"]}, ola)
        ids = {r["id"] for r in N.catalogo_resultados("2014")} | {r["id"] for r in N.catalogo_resultados("2009")}
        self.assertEqual(ids, {r["id"] for r in _spec_yaml(CALCS["serie"])["resultados"]})

    def test_respuesta_conocida_media_y_razon(self):
        for ola, s in self.S.items():
            for v in N.VARIANTES[ola]:
                P = f"RESULT-ENUT{ola}-{v}"
                self.assertAlmostEqual(self.out[ola][f"{P}-NACIONAL-NAC-P"], s.media_nacional(v), places=9, msg=(ola, v))
                self.assertAlmostEqual(self.out[ola][f"RESULT-ENUT{ola}-RAZON-{v}-NACIONAL-P"], s.razon(v), places=9, msg=(ola, v))
                self.assertEqual(self.out[ola][f"{P}-NACIONAL-NAC-N"], 19)   # 20 menos la persona sin FAC_PER

    def test_validacion_concp_y_oro_en_cero(self):
        o = self.out["2024"]
        self.assertLess(o["RESULT-ENUT2024-VALIDACION-CONCP-MAX-ABS"], 1e-9)
        for b in N.CONCP_COLS:
            self.assertEqual(o[f"RESULT-ENUT2024-VALIDACION-CONCP-{N._slug(b)}-N-DISCORDANTES"], 0)
        self.assertAlmostEqual(o["RESULT-ENUT2024-ORO-A-R-DELTA"], 0.0, places=12)
        self.assertEqual(o["RESULT-ENUT2024-JOIN-SIN-TVAR-CREA"], 0)

    def test_caminos_raros(self):
        for ola in self.S:
            o = self.out[ola]
            v = N.VARIANTES[ola][0]
            base = f"RESULT-ENUT{ola}-{v}-ESCOLARIDAD-SECUNDARIA"
            self.assertIsNone(o[base + "-P"])
            self.assertIsNone(o[base + "-IC-LO"])
            self.assertEqual(o[base + "-N"], 0)
            self.assertEqual(o[base + "-B-VALIDAS"], 0)
            self.assertGreater(o[f"RESULT-ENUT{ola}-{v}-SI-SIN-TIEMPO"], 0)
            self.assertEqual(o[f"RESULT-ENUT{ola}-N-SIN-PONDERADOR"], 1)
            self.assertEqual(o[f"RESULT-ENUT{ola}-FUERA-EDAD"], 1)
            self.assertEqual(o[f"RESULT-ENUT{ola}-FUERA-ESCOLARIDAD"], 1)
            sin_w = sum(1 for w in self.S[ola].hog_w.values() if w is None)
            self.assertEqual(o[f"RESULT-ENUT{ola}-RAZON-{v}-HOGARES-SIN-PONDERADOR"], sin_w)
            self.assertGreater(sin_w, 0)
            self.assertEqual(o[f"RESULT-ENUT{ola}-{v}-NACIONAL-NAC-B-VALIDAS"], REPS)

    def test_items_cotejan_con_p1(self):
        tabla = (RAIZ / "data" / "enut-comparabilidad-texto-v1_0.tsv").read_text(encoding="utf-8").split("\n")
        cab = tabla[0].split("\t")
        filas = [dict(zip(cab, l.split("\t"))) for l in tabla[1:] if l]
        import re

        def sufijos(reactivo: str, bloque: str) -> list[str]:
            m = re.search(re.escape(bloque) + r" \{([^}]*)\}", reactivo)
            self.assertIsNotNone(m, (bloque, reactivo))
            return [x.strip() for x in m.group(1).split(",")]
        for r in filas:
            if r["conducta"] == "C2" and r["ola"] == "2024":
                for b in ("6.11", "6.12", "6.13", "6.15"):
                    self.assertEqual(sufijos(r["reactivo"], b), N.ITEMS["2024"]["NUCLEO"][b], b)
            if r["conducta"] == "C3" and r["ola"] in ("2024", "2019"):
                for b in ("6.11", "6.12", "6.13", "6.15"):
                    self.assertEqual(sufijos(r["reactivo"], b), N.ITEMS[r["ola"]]["MIN"][b], (r["ola"], b))


class TestGuardia(unittest.TestCase):
    def test_celdas_de_eje_rechaza(self):
        import pandas as pd
        f = pd.DataFrame({"_eje_sexo": ["hombre", "mujer"]})
        with self.assertRaises(TypeError):
            N.celdas_de_eje(f, ["sexo", "edad"])
        with self.assertRaises(TypeError):
            N.celdas_de_eje(f, "sexo", "edad")
        with self.assertRaises(ValueError):
            N.celdas_de_eje(f, "sexo_edad")
        self.assertFalse(hasattr(N, "cruce"))
        self.assertEqual(list(N.celdas_de_eje(f, "sexo")), ["hombre", "mujer"])

    def test_auditoria_pasa_sobre_el_modulo_real(self):
        self.assertEqual(N.auditoria_ast(), [])

    def test_auditoria_falla_por_mutacion(self):
        fuente = (RAIZ / "tools" / "enut_nucleo.py").read_text(encoding="utf-8")
        mutaciones = {
            "R1": ("import numpy as np\n", "import numpy as np\nimport pickle\n"),
            "R2 crosstab": ("def celdas_de_eje(", "def _x(df):\n    return pd.crosstab(df.a, df.b)\n\n\ndef celdas_de_eje("),
            "R2 pivot": ("def celdas_de_eje(", "def _x(df):\n    return df.pivot_table()\n\n\ndef celdas_de_eje("),
            "R3 groupby fuera": ("def celdas_de_eje(", "def _x(df):\n    return df.groupby(\"_llave\").sum()\n\n\ndef celdas_de_eje("),
            "R3 dos llaves": ('df.groupby("_llave", sort=True)', 'df.groupby(["_llave", "_eje_sexo"], sort=True)'),
            "R4 &": ("def celdas_de_eje(", "def _x(df):\n    return df.a.eq(1) & df.b.eq(2)\n\n\ndef celdas_de_eje("),
            "R4 and": ("def celdas_de_eje(", "def _x(a, b):\n    return (a == 1) and (b == 2)\n\n\ndef celdas_de_eje("),
            "R4 mul": ("def celdas_de_eje(", "def _x(df):\n    return df.a.eq(1).mul(df.b.isin([2]))\n\n\ndef celdas_de_eje("),
            "R4 *": ("def celdas_de_eje(", "def _x(x, y):\n    return (x > 1) * (y > 2)\n\n\ndef celdas_de_eje("),
            "R5 open": ("def celdas_de_eje(", "def _x(p):\n    return open(p).read()\n\n\ndef celdas_de_eje("),
            "R6 instrumento": ("def celdas_de_eje(", "def _x():\n    return \"envipe2025.zip\"\n\n\ndef celdas_de_eje("),
        }
        for regla, (viejo, nuevo) in mutaciones.items():
            self.assertIn(viejo, fuente, regla)
            viol = N.auditoria_ast_fuente(fuente.replace(viejo, nuevo, 1))
            self.assertTrue(viol, regla)
            self.assertTrue(any(v.startswith(regla.split()[0]) for v in viol), (regla, viol))


if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]] + sys.argv[1:], verbosity=2)
