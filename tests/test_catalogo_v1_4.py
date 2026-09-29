"""Catálogo del mexicano v1.4 y tabla de piso v1.3 (ACTO GEN2-CIERRE-Y-PRODUCTO-3).

v1.4 añade al defecto que atrapa v1.3: una fila del bloque de la semana que entra sin
estar SELLADA/cuenta_gen2=SI en el registro del commit (o con una propuesta NO-ENTRA),
un nodo de tabla de momento (CALC-ALT, tabla por REF) cuyo punto no es el sellado, un
contraste de momento colado en la tabla de piso, el rótulo del lote 3 sobre llaves
distintas de las del dictamen, y una suspensión R21 borrada en vez de rotulada.

Texto heredado de v1.3:

Defecto que atrapa: cifras de catálogo escritas a mano o copiadas sin RESULT
(v1.0 citaba conteos de prosa; el informe v1.3 corrigió «5 dominios» a mano),
estimadores sin firma de adopción citada y pisos de origen legacy colados
como adopción (censo de GEN2-ENCIG-PISOS-GEN2-1). v1.3 añade: el rótulo de
validación ciega aplicado a llaves distintas de las de la tabla del recibo (beee-02),
una fila suspendida borrada en vez de rotulada, y un veto firmado (Intercensal 2015)
sin fila en decisiones.tsv, que es donde `status` lo lee (NC-…-96f9-03).
"""

import csv
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
CORRIDA = ROOT / "data/corrida0"
DIR = ROOT / "forense/analisis/catalogo/v1_4"
TSV = ROOT / "canon/catalogo-del-mexicano-v1_4.tsv"
MD = ROOT / "canon/catalogo-del-mexicano-v1_4.md"
GEN = ROOT / "forense/analisis/catalogo/genera_catalogo_v1_4.py"
CENSO = ROOT / "forense/notas/2026-09-24-GEN2-ENCIG-PISOS-GEN2-1-censo.tsv"
RECIBO = ROOT / ("forense/notas/2026-09-27-GEN2-RECIBO-ASTRA6-1/"
                 "2026-09-27-gen2-recibo-astra6-1--tabla-result-estado-efecto.tsv")
csv.field_size_limit(sys.maxsize)


def lee(path):
    with path.open(newline="") as s:
        return list(csv.DictReader((l for l in s if not l.startswith("#")), delimiter="\t"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class CatalogoV14(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = lee(TSV)
        cls.bloque = lee(DIR / "bloque-adopcion-cifras-v1_4.tsv")
        reg = {r["spec_id"]: r for r in lee(DIR / "registro-semana-v1_4.tsv")}
        cls.bloque_entra = {b["calc"] for b in cls.bloque if b["propuesta"] != "NO-ENTRA"
                            and reg[b["calc"]]["estado"].startswith("SELLADA") and reg[b["calc"]]["cuenta_gen2"] == "SI"}

    def test_regenera_identico(self):
        productos = [TSV, MD, DIR / "calcs-v1_4.tsv", DIR / "cobertura-31-v1_4.tsv",
                     DIR / "conteos-v1_4.json", DIR / "excluidos-v1_4.tsv", DIR / "pendientes-de-firma-v1_4.tsv",
                     DIR / "bloque-adopcion-cifras-v1_4.tsv"]
        antes = [sha(p) for p in productos]
        subprocess.run([sys.executable, str(GEN), "--sin-registro"], cwd=ROOT, check=True,
                       stdout=subprocess.DEVNULL)
        self.assertEqual(antes, [sha(p) for p in productos])

    def test_cada_cifra_es_su_result_sellado(self):
        calcs = {r["calc"]: r for r in lee(DIR / "calcs-v1_4.tsv")}
        datos = {}
        for c, r in calcs.items():
            sello = CORRIDA / c / "sello.json"
            self.assertEqual(sha(sello), r["sha256_sello"], c)
            self.assertEqual((CORRIDA / c / "sello.sha256").read_text().split()[0], r["sha256_sello"], c)
            self.assertEqual(json.loads(sello.read_text())["resultados.json"], r["sha256_resultados"], c)
            self.assertEqual(sha(CORRIDA / c / "resultados.json"), r["sha256_resultados"], c)
            datos[c] = json.loads((CORRIDA / c / "resultados.json").read_text())["resultados"]
        tablas = {}
        for row in self.rows:
            d = datos[row["calc"]]
            rid = row["result_id"]
            self.assertIn(rid, d, row["llave"])
            if row["celda"] and "#" in row["llave"] and not row["celda"].isdigit():
                v = d[rid]
                ruta, _, h = v[4:].partition("#sha256:")
                self.assertEqual(sha(ROOT / ruta), h, row["llave"])
                nodo = json.loads((ROOT / ruta).read_text())
                for k in row["celda"].split("/"):
                    nodo = nodo[k]
                p = next(nodo[k] for k in ("diferencia", "d_hat", "p") if k in nodo)
                self.assertEqual(float(row["punto"]), float(p), row["llave"])
                continue
            if row["celda"]:
                if (row["calc"], rid) not in tablas:
                    v = d[rid]
                    v = json.loads(v) if isinstance(v, str) else v
                    tablas[(row["calc"], rid)] = v["celdas"] if isinstance(v, dict) else v
                cel = tablas[(row["calc"], rid)][int(row["celda"])] if row["celda"].isdigit() else None
                if cel is not None:
                    p = cel.get("punto", cel.get("p"))
                    self.assertEqual(float(row["punto"]), float(p), row["llave"])
                    continue
            self.assertEqual(float(row["punto"]), float(d[rid]), row["llave"])

    def test_firma_citada_y_sin_legacy(self):
        fps = {r["id"]: r["estado"] for r in lee(ROOT / "forense/firmas-pendientes.tsv")}
        objetos = {r["objeto"] for r in lee(CORRIDA / "decisiones.tsv")}
        legacy = {r["resultado_puntual"] for r in lee(CENSO) if r["clase_censo"] == "HEREDADO-DE-LEGACY"}
        for row in self.rows:
            f = row["firma_fp"]
            if f == "MERGE-DE-MESA:GEN2-CIERRE-Y-PRODUCTO-3":
                self.assertIn(row["calc"], self.bloque_entra, row["llave"])
            elif f.startswith("FP-"):
                self.assertTrue(fps.get(f, "").startswith("FIRMADA"), (row["llave"], f))
            elif f.startswith("decisiones.tsv:"):
                self.assertIn(f.split(":", 1)[1], objetos, row["llave"])
            else:
                self.assertTrue((ROOT / f.split("#")[0]).exists(), (row["llave"], f))
            self.assertIn(row["estado_adopcion"], ("ADOPTADO", "ADOPTADO-CON-RESERVA-DE-ANCHO", "SUSPENDIDA-POR-FIRMA"))
            self.assertIn(row["origen_piso"], ("NUEVO", "HEREDADO-DE-GEN2"))
            self.assertIn(row["temporalidad"], ("PROSPECTIVA", "RETROSPECTIVA"))
            self.assertNotIn(row["result_id"], legacy)
            if row["dominio"] == "DINERO":
                self.assertTrue(row["oferta_exclusion"] and row["oferta_exclusion"] != "NO-APLICA")

    def test_cero_cifras_tecleadas_en_la_plantilla(self):
        texto = (DIR / "plantilla-v1_4.md").read_text()
        limpio = re.sub(r"\{\{[crt]:[^}]+\}\}", "", texto)
        limpio = re.sub(r"`[^`]*`", "", limpio)                     # identificadores
        limpio = re.sub(r"\([^)]*\.(md|tsv)\)", "", limpio)         # rutas de enlaces
        limpio = re.sub(r"\b(19|20)\d\d(T[1-4])?\b", "", limpio)    # años y trimestres
        limpio = re.sub(r"§\d+(\.\d+)?|\bv\d[._]\d\b|\bE\.\d\b", "", limpio)
        limpio = re.sub(r"^\d+\. ", "", limpio, flags=re.M)         # numeración de lista
        limpio = re.sub(r"\bt−1\b|\bregla \d+\b", "", limpio)             # notación y referencias
        limpio = re.sub(r"\b[A-Z][A-Z0-9]*(-[A-Z0-9]+)+\b", "", limpio)  # rótulos y ids
        limpio = re.sub(r"\b[A-Z]+\d[A-Z0-9]*\b", "", limpio)             # GEN2, U1
        sueltos = re.findall(r".{0,30}\d.{0,30}", limpio)
        self.assertEqual(sueltos, [], "dígitos fuera de placeholder, id o año")

    def test_firmas19_y_20_entran_y_sin_dominio_vacio(self):
        firmadas = {r["firma_fp"] for r in self.rows}
        for sufijo in ("2d37-01", "2d37-02", "ac7b-01", "ac7b-02", "ac7b-03", "ac7b-04",
                       "2a0e-01", "2a0e-02", "2a0e-03", "5916-01", "3a49-01", "3a49-02", "3a49-03",
                       "3a49-04", "0d4a-01"):
            self.assertTrue(any(f.endswith(sufijo) for f in firmadas), sufijo)
        self.assertFalse([r["llave"] for r in self.rows if r["dominio"] == "SIN-DOMINIO"])
        # J3: las filas vetadas de -0001 no entran.
        self.assertFalse([r for r in self.rows if r["calc"] == "CALC-ENIGH-CONSUMO-PISOS-0001"])

    def test_tabla_de_piso_v1_3_derivada_mismas_filas_y_rotulos(self):
        r = subprocess.run([sys.executable, "tools/genera_tabla_piso_v1_3.py", "--verifica"], cwd=ROOT,
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout)
        piso = lee(ROOT / "canon/tabla-de-piso-v1_3.tsv")
        filas = [r for r in self.rows if r["alcance"] != "CONTRASTE-DE-MOMENTO"]
        self.assertEqual(len(piso), len(filas))
        self.assertFalse([f for f in piso if f["calc"].startswith("CALC-ALT-")])
        self.assertEqual({f["estado_adopcion"] for f in piso},
                         {"ADOPTADO", "ADOPTADO-CON-RESERVA-DE-ANCHO", "SUSPENDIDA-POR-FIRMA"})
        cat = {r["llave"]: (r["estado_adopcion"], r["validacion_ciega"], r["sucesor"], r["validacion_ciega_lote3"])
               for r in filas}
        self.assertEqual({f["llave"]: (f["estado_adopcion"], f["validacion_ciega"], f["sucesor"], f["validacion_ciega_lote3"])
                          for f in piso}, cat)
        self.assertIn("tabla-de-piso-v1_3", (ROOT / "docs/reto.md").read_text())

    def test_beee02_rotulos_por_llave_del_recibo(self):
        recibo = lee(RECIBO)
        cat = {r["llave"]: r for r in self.rows}
        por = {}
        for t in recibo:
            por.setdefault(t["recomendacion"], set()).add(t["llave"])
        r21 = {t["llave_historica"] for t in lee(ROOT / "forense/validacion-independiente/catalogo-1-sucesores/r21-envipe-15-llaves.tsv")}
        susp = {k for k, r in cat.items() if r["estado_adopcion"] == "SUSPENDIDA-POR-FIRMA"} - r21
        acot = {k for k, r in cat.items() if r["validacion_ciega"].startswith("ACOTADA")}
        self.assertEqual(susp, por["PROPONER-SUSPENDER"])
        self.assertEqual(acot, por["ACOTAR"])
        self.assertTrue(all(cat[k]["sucesor"] for k in susp))
        con_rotulo = {k for k, r in cat.items() if r["validacion_ciega"]}
        self.assertEqual(con_rotulo, {t["llave"] for t in recibo})
        # suspender no es borrar: toda llave de v1.3 sigue en v1.4
        v13 = {r["llave"] for r in lee(ROOT / "canon/catalogo-del-mexicano-v1_3.tsv")}
        self.assertFalse(v13 - set(cat))

    def test_lote3_y_r21_por_llave(self):
        cat = {r["llave"]: r for r in self.rows}
        d = lee(ROOT / "forense/validacion-independiente/catalogo-1-lote3/dictamen-lote3-v1_1.tsv")
        r21 = {t["llave_historica"] for t in lee(ROOT / "forense/validacion-independiente/catalogo-1-sucesores/r21-envipe-15-llaves.tsv")}
        con = {k for k, r in cat.items() if r["validacion_ciega_lote3"]}
        self.assertEqual(con, {t["llave"] for t in d} | r21)
        for k in r21:
            self.assertEqual(cat[k]["estado_adopcion"], "SUSPENDIDA-POR-FIRMA", k)
            self.assertTrue(cat[k]["sucesor"], k)
        acot = {t["llave"] for t in d if t["dictamen"] == "ACOTAR"}
        self.assertEqual(acot, {k for k, r in cat.items() if r["validacion_ciega_lote3"].startswith("ACOTADA")})

    def test_mapa11_dominios_medidos_derivado(self):
        c = json.loads((DIR / "conteos-v1_4.json").read_text())
        mapa = {r["dominio"] for r in lee(ROOT / "canon/mapa-dominios-v1_1.tsv")}
        self.assertEqual(c["mapa11_dominios_medidos"], len(mapa & {r["dominio"] for r in self.rows}))
        r = subprocess.run([sys.executable, "forense/analisis/informe-v1_6/cifra_v1_6.py", "mapa11_dominios_medidos"],
                           cwd=ROOT, capture_output=True, text=True, check=True)
        self.assertEqual(int(r.stdout.strip()), c["mapa11_dominios_medidos"])
        holdout = {r["holdout_gastado"] for r in self.rows if r["alcance"] == "CONTRASTE-DE-MOMENTO"}
        self.assertFalse("" in holdout, "contraste de momento sin holdout_gastado declarado")

    def test_veto_intercensal_2015_donde_status_lo_lee(self):
        vetos = {r["objeto"] for r in lee(CORRIDA / "decisiones.tsv")
                 if r["decision"].startswith("adopcion=VETADA-POR-DECISION")}
        data = json.loads((CORRIDA / "CALC-EIC-HOGARES-2015-0001/resultados.json").read_text())["resultados"]
        self.assertFalse(set(data) - vetos)
        self.assertFalse([r for r in self.rows if r["calc"] == "CALC-EIC-HOGARES-2015-0001"])

    def test_puntero_y_v1_0_intacto(self):
        self.assertIn("catalogo-del-mexicano-v1_4", (ROOT / "docs/catalogo.md").read_text())
        for p in ("canon/catalogo-del-mexicano-v1_3.md", "canon/catalogo-del-mexicano-v1_3.tsv",
                  "canon/tabla-de-piso-v1_2.tsv", "canon/catalogo-del-mexicano-v1_0.md", "canon/catalogo-del-mexicano-v1_0.tsv",
                  "canon/catalogo-del-mexicano-v1_1.md", "canon/catalogo-del-mexicano-v1_1.tsv",
                  "canon/catalogo-del-mexicano-v1_2.md", "canon/catalogo-del-mexicano-v1_2.tsv",
                  "canon/tabla-de-piso-v1_0.tsv", "canon/tabla-de-piso-v1_1.tsv"):
            r = subprocess.run(["git", "diff", "--quiet", "origin/main", "--", p], cwd=ROOT)
            self.assertIn(r.returncode, (0, 128), p)
            self.assertNotEqual(r.returncode, 1, f"{p} modificado respecto a origin/main")


if __name__ == "__main__":
    unittest.main()
