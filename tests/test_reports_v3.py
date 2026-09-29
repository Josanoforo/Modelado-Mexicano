"""Reports v3 (ACTO GEN2-CIERRE-Y-PRODUCTO-3, P4) — test de procedencia.

Defecto que atrapa: un report que cita una cifra que no es la del RESULT sellado que nombra
(el catálogo v1.0 citaba conteos de prosa; C3-1 dejó 31 homónimos v2 con cifras sin RESULT),
un v3 abierto para un carril sin cifra nueva («no relanzar reports»), un cuerpo v2 editado al
heredarlo, y una afirmación con cifra sin procedencia (a)/(b)/(c) ni las preguntas [v2.16].
"""
import csv
import hashlib
import pathlib
import re
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
V3 = ROOT / "corpus/reports-v3"
csv.field_size_limit(sys.maxsize)
LINEA_CIFRA = re.compile(r"^- `(RESULT-[^`]+)` · (-?\d+\.\d{3})")


def lee(p):
    with p.open(newline="", encoding="utf-8") as s:
        return list(csv.DictReader((l for l in s if not l.startswith("#")), delimiter="\t"))


class ReportsV3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cat = {r["llave"]: r for r in lee(ROOT / "canon/catalogo-del-mexicano-v1_4.tsv")}
        cls.carriles = lee(ROOT / "forense/analisis/reports-v3/carriles-v3-v1_0.tsv")
        cls.v3 = sorted(p for p in V3.glob("*.md") if p.name != "INDICE.md")

    def test_regenera_identico(self):
        r = subprocess.run([sys.executable, "forense/analisis/reports-v3/genera_reports_v3.py", "--verifica"],
                           cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_solo_carriles_con_cifra_nueva(self):
        si = {c["report"] for c in self.carriles if c["sale_v3"] == "SI"}
        self.assertEqual({p.name for p in self.v3}, si)
        self.assertTrue(si)

    def test_procedencia_y_cifra_por_result(self):
        for p in self.v3:
            capa, _, cuerpo = p.read_text(encoding="utf-8").partition("# Cuerpo heredado de v2")
            n = 0
            for linea in capa.splitlines():
                m = LINEA_CIFRA.match(linea)
                if not m:
                    continue
                n += 1
                rid, punto = m.groups()
                self.assertIn(rid, self.cat, (p.name, rid))
                self.assertEqual(f"{float(self.cat[rid]['punto']):.3f}", punto, (p.name, rid))
                self.assertRegex(linea, r"procedencia \((a|b|c)\)", (p.name, rid))
                self.assertIn(self.cat[rid]["unidad"], linea, (p.name, rid))
            self.assertGreater(n, 0, p.name)
            self.assertIn("[v2.16] ¿Qué cifra es PROSPECTIVA y cuál RETROSPECTIVA", capa, p.name)
            self.assertIn("[v2.16] ¿Qué unidad tiene cada cifra", capa, p.name)
            self.assertIn("Firewall genético", capa, p.name)

    def test_cuerpo_v2_heredado_sin_editar(self):
        for p in self.v3:
            texto = p.read_text(encoding="utf-8")
            m = re.search(r"# Cuerpo heredado de v2 \(sin editar · sha256 `([0-9a-f]{64})`\)\n\n", texto)
            self.assertIsNotNone(m, p.name)
            v2 = ROOT / "corpus/reports-v2" / p.name
            self.assertEqual(hashlib.sha256(v2.read_bytes()).hexdigest(), m.group(1), p.name)
            self.assertEqual(texto[m.end():], v2.read_text(encoding="utf-8"), p.name)
            r = subprocess.run(["git", "diff", "--quiet", "origin/main", "--", str(v2.relative_to(ROOT))], cwd=ROOT)
            self.assertNotEqual(r.returncode, 1, f"{v2.name} v2 modificado respecto a origin/main")


if __name__ == "__main__":
    unittest.main()
