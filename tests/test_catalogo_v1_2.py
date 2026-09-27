"""Catálogo del mexicano v1.2 (ACTO GEN2-CIERRE-SEMANAL-1).

Defecto que atrapa: cifras de catálogo escritas a mano o copiadas sin RESULT
(v1.0 citaba conteos de prosa; el informe v1.3 corrigió «5 dominios» a mano),
estimadores sin firma de adopción citada y pisos de origen legacy colados
como adopción (censo de GEN2-ENCIG-PISOS-GEN2-1).
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
DIR = ROOT / "forense/analisis/catalogo/v1_2"
TSV = ROOT / "canon/catalogo-del-mexicano-v1_2.tsv"
MD = ROOT / "canon/catalogo-del-mexicano-v1_2.md"
GEN = ROOT / "forense/analisis/catalogo/genera_catalogo_v1_2.py"
CENSO = ROOT / "forense/notas/2026-09-24-GEN2-ENCIG-PISOS-GEN2-1-censo.tsv"
csv.field_size_limit(sys.maxsize)


def lee(path):
    with path.open(newline="") as s:
        return list(csv.DictReader((l for l in s if not l.startswith("#")), delimiter="\t"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class CatalogoV12(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = lee(TSV)

    def test_regenera_identico(self):
        productos = [TSV, MD, DIR / "calcs-v1_2.tsv", DIR / "cobertura-31-v1_2.tsv",
                     DIR / "conteos-v1_2.json", DIR / "excluidos-v1_2.tsv", DIR / "pendientes-de-firma-v1_2.tsv"]
        antes = [sha(p) for p in productos]
        subprocess.run([sys.executable, str(GEN), "--sin-registro"], cwd=ROOT, check=True,
                       stdout=subprocess.DEVNULL)
        self.assertEqual(antes, [sha(p) for p in productos])

    def test_cada_cifra_es_su_result_sellado(self):
        calcs = {r["calc"]: r for r in lee(DIR / "calcs-v1_2.tsv")}
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
            if f.startswith("FP-"):
                self.assertTrue(fps.get(f, "").startswith("FIRMADA"), (row["llave"], f))
            elif f.startswith("decisiones.tsv:"):
                self.assertIn(f.split(":", 1)[1], objetos, row["llave"])
            else:
                self.assertTrue((ROOT / f.split("#")[0]).exists(), (row["llave"], f))
            self.assertIn(row["estado_adopcion"], ("ADOPTADO", "ADOPTADO-CON-RESERVA-DE-ANCHO"))
            self.assertIn(row["origen_piso"], ("NUEVO", "HEREDADO-DE-GEN2"))
            self.assertIn(row["temporalidad"], ("PROSPECTIVA", "RETROSPECTIVA"))
            self.assertNotIn(row["result_id"], legacy)
            if row["dominio"] == "DINERO":
                self.assertTrue(row["oferta_exclusion"] and row["oferta_exclusion"] != "NO-APLICA")

    def test_cero_cifras_tecleadas_en_la_plantilla(self):
        texto = (DIR / "plantilla-v1_2.md").read_text()
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

    def test_firmas19_entran_y_sin_dominio_vacio(self):
        firmadas = {r["firma_fp"] for r in self.rows}
        for sufijo in ("2d37-01", "2d37-02", "ac7b-01", "ac7b-02", "ac7b-03", "ac7b-04",
                       "2a0e-01", "2a0e-02", "2a0e-03"):
            self.assertTrue(any(f.endswith(sufijo) for f in firmadas), sufijo)
        self.assertFalse([r["llave"] for r in self.rows if r["dominio"] == "SIN-DOMINIO"])
        # J3: las filas vetadas de -0001 no entran.
        self.assertFalse([r for r in self.rows if r["calc"] == "CALC-ENIGH-CONSUMO-PISOS-0001"])

    def test_tabla_de_piso_v1_1_derivada_y_solo_adoptada(self):
        r = subprocess.run([sys.executable, "tools/genera_tabla_piso_v1_1.py", "--verifica"], cwd=ROOT,
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout)
        piso = lee(ROOT / "canon/tabla-de-piso-v1_1.tsv")
        self.assertEqual(len(piso), len(self.rows))
        self.assertEqual({f["estado_adopcion"] for f in piso}, {"ADOPTADO", "ADOPTADO-CON-RESERVA-DE-ANCHO"})
        self.assertIn("tabla-de-piso-v1_1", (ROOT / "docs/reto.md").read_text())

    def test_puntero_y_v1_0_intacto(self):
        self.assertIn("catalogo-del-mexicano-v1_2", (ROOT / "docs/catalogo.md").read_text())
        for p in ("canon/catalogo-del-mexicano-v1_0.md", "canon/catalogo-del-mexicano-v1_0.tsv",
                  "canon/catalogo-del-mexicano-v1_1.md", "canon/catalogo-del-mexicano-v1_1.tsv",
                  "canon/tabla-de-piso-v1_0.tsv"):
            r = subprocess.run(["git", "diff", "--quiet", "origin/main", "--", p], cwd=ROOT)
            self.assertIn(r.returncode, (0, 128), p)
            self.assertNotEqual(r.returncode, 1, f"{p} modificado respecto a origin/main")


if __name__ == "__main__":
    unittest.main()
