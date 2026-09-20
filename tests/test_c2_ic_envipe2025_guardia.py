#!/usr/bin/env python3
"""Guardias del COMMIT-1 de `CALC-C2-COMPUESTO-IC-ENVIPE2025-0001` ·
`ACTO GEN2-GUARDIAN-ENVIPE-EJES-IC-1` (20/sep/2026).

Pinan el contrato congelado para que el COMMIT-2 no pueda desviarse en
silencio. **Cero microdato**: ninguna prueba abre ENVIPE 2025; todo es
lectura de FUENTE (AST) o de constantes del pre-registro. Nada describe a
México.

  G1  AST del medidor: ninguna agrupación por más de una variable (ningún
      `groupby`/`value_counts` con lista o tupla; ningún `groupby` a secas),
      ningún `crosstab`/`pivot`/`pivot_table`, ningún `merge`/`join`.
  G2  AST: `cruce` no se llama, ni por atributo ni por nombre.
  G3  AST: `marginal(...)` se llama con exactamente UN argumento posicional
      de grupo, y ese argumento es un nombre iterado sobre `ejes`, nunca una
      lista ni dos posicionales; `replicas_compartidas` una sola vez.
  G4  Payload: el único `inputs[...]` con origen manifiesto que la fuente
      nombra es `envipe2025_csv`; ninguna cadena menciona enif, encig,
      envipe2023 ni envipe2024; `carga_ola` se llama con `reservada=True`.
  G5  spec.md del CALC == prereg-caja + sidecar == spec_md_sha256 del yaml.
  G6  Los marginales sellados congelados en `parametros.marginales_sellados`
      coinciden, valor por valor, con las líneas citadas del yaml del árbitro
      (sexo y edad incluidos): la transcripción no puede estar torcida.
  G7  El guardián extendido: `PARES_VETADOS[2025]` contiene
      {edad, dominio_urbano_rural}; `EJES` termina en (sexo, edad).
  G8  38 celdas / 4 pares en el TSV derivado, y ninguna del par vetado.
"""
from __future__ import annotations

import ast
import hashlib
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CALC = os.path.join(ROOT, "data", "corrida0", "CALC-C2-COMPUESTO-IC-ENVIPE2025-0001")
MEDIDOR = os.path.join(CALC, "medidor.py")
SPEC_YAML = os.path.join(CALC, "spec.yaml")
SPEC_MD_CALC = os.path.join(CALC, "spec.md")
SPEC_MD = os.path.join(ROOT, "forense", "prereg-caja", "C2-COMPUESTO-IC-ENVIPE2025-spec-v1_0.md")
SIDECAR = SPEC_MD.replace(".md", ".sha256")
GUARDIAN = os.path.join(ROOT, "tools", "celda_d", "marginales_reproduccion.py")
ARBITRO = os.path.join(ROOT, "milpa", "tramite-ola5-propuesta-v0.yaml")
EMISIONES = os.path.join(ROOT, "data", "corrida0", "c2-compuesto-emisiones-v1_0.tsv")

with open(MEDIDOR, encoding="utf-8") as fh:
    FUENTE = fh.read()
ARBOL = ast.parse(FUENTE)


def _nombre(call):
    f = call.func
    if isinstance(f, ast.Attribute):
        return f.attr
    if isinstance(f, ast.Name):
        return f.id
    return None


CALLS = [n for n in ast.walk(ARBOL) if isinstance(n, ast.Call)]


class G1_UnaVariable(unittest.TestCase):
    def test_sin_agrupacion_multivariable_ni_tablas_cruzadas(self):
        prohibidos = {"groupby", "crosstab", "pivot", "pivot_table", "merge",
                      "join", "value_counts", "cruce"}
        vistos = sorted({_nombre(c) for c in CALLS} & prohibidos)
        self.assertEqual(vistos, [], f"llamadas prohibidas en el medidor: {vistos}")

    def test_sin_atributo_cruce(self):
        attrs = {n.attr for n in ast.walk(ARBOL) if isinstance(n, ast.Attribute)}
        self.assertNotIn("cruce", attrs)


class G3_MarginalPorUnaVariable(unittest.TestCase):
    def test_marginal_un_solo_grupo_posicional_iterado_sobre_ejes(self):
        llamadas = [c for c in CALLS if _nombre(c) == "marginal"]
        self.assertEqual(len(llamadas), 1, "una sola llamada a marginal(), en el bucle")
        c = llamadas[0]
        self.assertEqual(len(c.args), 2, "marginal(ola, eje): dos posicionales")
        self.assertIsInstance(c.args[1], ast.Name)
        self.assertEqual(c.args[1].id, "eje")
        self.assertNotIsInstance(c.args[1], (ast.List, ast.Tuple))
        # el nombre `eje` viene de `for eje in ejes`, y `ejes` del contrato
        fors = [n for n in ast.walk(ARBOL) if isinstance(n, ast.For)
                and isinstance(n.target, ast.Name) and n.target.id == "eje"]
        self.assertTrue(fors)
        self.assertTrue(all(isinstance(f.iter, ast.Name) and f.iter.id == "ejes" for f in fors))

    def test_un_solo_remuestreo(self):
        self.assertEqual(sum(1 for c in CALLS if _nombre(c) == "replicas_compartidas"), 1)

    def test_lector_tsv_propio_sin_modulo_csv(self):
        imports = {a.name for n in ast.walk(ARBOL) if isinstance(n, ast.Import) for a in n.names}
        self.assertNotIn("csv", imports)
        self.assertNotIn("pandas", imports)


class G4_SoloEnvipe2025(unittest.TestCase):
    def test_unico_payload_y_reservada(self):
        subs = re.findall(r'inputs\["([^"]+)"\]', FUENTE)
        self.assertEqual(set(subs), {"envipe2025_csv", "IN-C2-SELLADO",
                                     "IN-C2-EMISIONES", "IN-ARBITRO-MARGINALES"})
        for malo in ("enif", "encig", "envipe2023", "envipe2024", "ENIF", "ENCIG"):
            self.assertNotIn(malo, FUENTE)
        carga = [c for c in CALLS if _nombre(c) == "carga_ola"]
        self.assertEqual(len(carga), 1)
        kw = {k.arg: k.value for k in carga[0].keywords}
        self.assertIn("reservada", kw)
        self.assertIsInstance(kw["reservada"], ast.Constant)
        self.assertIs(kw["reservada"].value, True)


class G5_SpecCongelada(unittest.TestCase):
    def _sha(self, ruta):
        with open(ruta, "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()

    def test_spec_md_sidecar_y_yaml_coinciden(self):
        s = self._sha(SPEC_MD)
        self.assertEqual(s, self._sha(SPEC_MD_CALC))
        with open(SIDECAR, encoding="utf-8") as fh:
            self.assertEqual(fh.read().split()[0], s)
        with open(SPEC_YAML, encoding="utf-8") as fh:
            self.assertIn(f"spec_md_sha256: {s}", fh.read())

    def test_frase_de_primer_resultado(self):
        with open(SPEC_MD, encoding="utf-8") as fh:
            self.assertIn("El primer resultado que produzca este procedimiento es el que se", fh.read())


class G6_SelladosTranscritos(unittest.TestCase):
    def test_marginales_sellados_coinciden_con_el_yaml_del_arbitro(self):
        import yaml
        with open(SPEC_YAML, encoding="utf-8") as fh:
            sell = yaml.safe_load(fh)["parametros"]["marginales_sellados"]
        with open(ARBITRO, encoding="utf-8") as fh:
            lineas = fh.read().splitlines()
        n = 0
        for eje, celdas in sell.items():
            for celda, v in celdas.items():
                m = re.match(r"milpa/tramite-ola5-propuesta-v0\.yaml:(\d+)$", v["linea"])
                if not m:
                    continue                       # el nacional cita tramite.yaml
                ln = lineas[int(m.group(1)) - 1]
                self.assertIn(f'celda: "{celda}"', ln, (eje, celda))
                self.assertIn(f"p: {v['p']:.6f}", ln, (eje, celda))
                self.assertIn(f"n: {v['n']}", ln, (eje, celda))
                self.assertIn(f"ic95: [{v['ic95'][0]:.6f}, {v['ic95'][1]:.6f}]", ln, (eje, celda))
                n += 1
        self.assertEqual(n, 13, "4 escolaridad + 3 dominio + 2 sexo + 4 edad")


class G7_GuardianExtendido(unittest.TestCase):
    def test_veto_por_nombre_y_ejes_nuevos(self):
        with open(GUARDIAN, encoding="utf-8") as fh:
            src = fh.read()
        self.assertIn('PARES_VETADOS = {2025: frozenset({frozenset({"edad", "dominio_urbano_rural"})})}', src)
        self.assertIn("NC-0328", src)
        self.assertRegex(src, r'EJES = \("escolaridad_proxy", "dominio_urbano_rural", "nacional",\s*"sexo", "edad"\)')
        self.assertIn('"SEXO", "EDAD")', src)          # en COLUMNAS_TMOD


class G8_Dictamen(unittest.TestCase):
    def test_38_celdas_4_pares_sin_par_vetado(self):
        filas, cab = [], None
        with open(EMISIONES, encoding="utf-8") as fh:
            for l in fh:
                if not l.strip() or l.startswith("#"):
                    continue
                campos = l.rstrip("\n").split("\t")
                if cab is None:
                    cab = campos
                    continue
                filas.append(dict(zip(cab, campos)))
        env = [f for f in filas if f["ola"] == "ENVIPE 2025"]
        self.assertEqual(len(env), 38)
        pares = {}
        for f in env:
            pares[f["par"]] = pares.get(f["par"], 0) + 1
        self.assertEqual(pares, {"dominio_urbano_ruralxsexo": 6, "edadxescolaridad_proxy": 16,
                                 "edadxsexo": 8, "escolaridad_proxyxsexo": 8})
        self.assertNotIn("edadxdominio_urbano_rural", pares)
        self.assertNotIn("dominio_urbano_ruralxedad", pares)


if __name__ == "__main__":
    unittest.main(verbosity=2)
