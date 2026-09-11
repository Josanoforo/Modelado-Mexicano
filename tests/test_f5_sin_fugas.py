from __future__ import annotations

import builtins
import copy
import hashlib
import importlib.util
import json
import pathlib
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "calcula_f5_sin_fugas_bajo_prueba",
    ROOT / "tools" / "calcula_f5_sin_fugas.py",
)
CALC = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(CALC)

SPEC_GENERADOR = importlib.util.spec_from_file_location(
    "genera_f5_sin_fugas_bajo_prueba",
    ROOT / "tools" / "genera_f5_sin_fugas_spec.py",
)
GENERADOR = importlib.util.module_from_spec(SPEC_GENERADOR)
assert SPEC_GENERADOR.loader
SPEC_GENERADOR.loader.exec_module(GENERADOR)


def entrada(iid: str, rol: str, contenido, **meta) -> dict:
    if not isinstance(contenido, bytes):
        if isinstance(contenido, str):
            contenido = contenido.encode("utf-8")
        else:
            contenido = (json.dumps(contenido, ensure_ascii=False, sort_keys=True)
                         + "\n").encode("utf-8")
    return {
        "id": iid,
        "rol": rol,
        "origen": "repo",
        "ruta": meta.pop("ruta", f"fixture/{iid}"),
        "estado": "COINCIDE",
        "bytes": contenido,
        "sha256": hashlib.sha256(contenido).hexdigest(),
        **meta,
    }


def reemplaza_json(ent: dict, mutar, conserva_sha: bool = False) -> None:
    datos = json.loads(ent["bytes"])
    mutar(datos)
    ent["bytes"] = (json.dumps(datos, ensure_ascii=False, sort_keys=True)
                    + "\n").encode("utf-8")
    if not conserva_sha:
        ent["sha256"] = hashlib.sha256(ent["bytes"]).hexdigest()


def linaje_fixture(**kwargs) -> dict:
    marca = kwargs["celda_m"].get("linaje_prueba", "APTO")
    if marca == "DEPENDIENTE-R":
        return {
            "estado": "NO-APTO", "origen_numerico": "HEREDADO",
            "dependencia_objetivo": "SI", "camino": ["M", "R"],
            "razon": "padre o derivado del árbitro",
        }
    if marca == "INDETERMINADO":
        return {
            "estado": "INDETERMINADO", "origen_numerico": "INDETERMINADO",
            "dependencia_objetivo": "INDETERMINADA", "camino": [],
            "razon": "sin cadena acreditada",
        }
    return {
        "estado": "APTO", "origen_numerico": "NUEVO",
        "dependencia_objetivo": "NO", "camino": ["M", "fuente-independiente"],
        "razon": "fixture independiente",
    }


def fixture() -> tuple[dict, dict]:
    variantes = {"L-solo": "L_SOLO", "L+corpus": "L_CORPUS"}
    posiciones = []
    inputs = {
        "IN-CONTRATO": entrada("IN-CONTRATO", "contrato_estudio", "contrato"),
        "IN-CALCULADOR": entrada("IN-CALCULADOR", "calculador", "codigo"),
        "IN-LINAJE": entrada("IN-LINAJE", "linaje", "codigo-linaje"),
    }
    valores_l = {
        ("A", "L-solo"): [10, 30],
        ("A", "L+corpus"): [20, 40],
        ("B", "L-solo"): [40, 60],
        ("B", "L+corpus"): [30, 50],
    }
    for cid in ("A", "B"):
        for variante in variantes:
            for replica in (1, 2):
                token = f"{cid}:{variante}:{replica}"
                identidad = hashlib.sha256(token.encode()).hexdigest()
                ruta = f"capturas/{token}.json"
                posiciones.append({
                    "id_celda": cid, "variante": variante,
                    "replica": replica, "ruta": ruta,
                    "identidad": identidad,
                })
                captura = {
                    "id_celda": cid, "variante": variante,
                    "replica": replica, "identidad": identidad,
                    "estado_captura": "OK",
                    "texto_crudo": (
                        f"respuesta\nESTIMACION_PUNTUAL="
                        f"{valores_l[(cid, variante)][replica - 1]}%"
                    ),
                }
                iid = f"IN-L-{cid}-{variante}-{replica}"
                inputs[iid] = entrada(
                    iid, "captura_l", captura, ruta=ruta,
                    id_celda=cid, variante=variante, replica=replica,
                )

    plan = {
        "version": "fixture-v1", "n_posiciones": 8, "k": 2,
        "variantes": list(variantes), "posiciones": posiciones,
    }
    inputs["IN-PLAN"] = entrada("IN-PLAN", "plan", plan)
    universo = (
        "id_celda\tfuente_R\n"
        "A\tr/A/\n"
        "B\tr/B/\n"
    )
    inputs["IN-UNIVERSO"] = entrada("IN-UNIVERSO", "universo_r", universo)
    tarjetas = (
        "id_celda\tproposito\testimando_alineado\tcumple_corte\t"
        "R_punto_apto\tR_incertidumbre\tcomparabilidad\t"
        "fuente_criterio\tcausa\n"
        "A\tPRUEBA\tSI\tSI\tSI\tACREDITADA\tACREDITADA\tfixture\tapta\n"
        "B\tPRUEBA\tSI\tSI\tSI\tACREDITADA\tACREDITADA\tfixture\tapta\n"
    )
    inputs["IN-TARJETAS"] = entrada("IN-TARJETAS", "tarjetas_mr", tarjetas)
    snapshot = {
        "celdas": [
            {"id_celda": "A", "punto_M": .25, "identidad_confirmada": True,
             "estado_M": "EMITE", "estado_firewall": "LIMPIO-DE-OBJETIVO",
             "archivo_fuente": "m/A.json", "linaje_prueba": "APTO"},
            {"id_celda": "B", "punto_M": .35, "identidad_confirmada": True,
             "estado_M": "EMITE", "estado_firewall": "LIMPIO-DE-OBJETIVO",
             "archivo_fuente": "m/B.json", "linaje_prueba": "APTO"},
        ]
    }
    inputs["IN-SNAPSHOT"] = entrada("IN-SNAPSHOT", "snapshot_m", snapshot)
    for cid, punto in (("A", .2), ("B", .4)):
        iid = f"IN-R-{cid}"
        calc_id = f"CALC-R-{cid}"
        rid = f"RESULT-R-{cid}-PUNTO"
        inputs[iid] = entrada(
            iid, "resultado_r",
            {"spec_id": calc_id, "resultados": {rid: punto}},
            ruta=f"r/{cid}/resultados.json", id_celda=cid,
            calc_id_esperado=calc_id, result_id_punto=rid,
        )

    contrato = {
        "parametros": {
            "plan_version": "fixture-v1",
            "n_posiciones": 8,
            "k_replicas": 2,
            "variantes": variantes,
            "seleccion": "MEDIANA-DE-REPLICAS-VALIDAS",
            "bootstrap_replicas": 100,
            "nivel_ic": .95,
            "delta_banda_pp": .5,
            "tolerancia_numerica_pp": 1e-9,
            "contendientes": ["L_SOLO", "L_CORPUS", "M"],
            "comparaciones": [
                ["L_CORPUS", "L_SOLO"], ["M", "L_SOLO"],
                ["M", "L_CORPUS"],
            ],
            "u3_congelado": ["A", "B"],
            "proposito": "PRUEBA",
            "estado_firewall_apto": "LIMPIO-DE-OBJETIVO",
            "estado_m_apto": "EMITE",
            "comparabilidad_apta": "ACREDITADA",
            "cumple_corte_apto": "SI",
            "r_punto_apto": "SI",
            "regex_punto_l": r"^ESTIMACION_PUNTUAL=(\d+(?:[.,]\d+)?)%$",
            "estados_r_aptos": ["CALCULADO"],
        },
        "seed": {"aplica": True, "valor": 42, "rng": "random.Random"},
    }
    return inputs, contrato


class TestElegibilidad(unittest.TestCase):
    def test_baseline_reducido_puntua_mismo_u3(self):
        inputs, contrato = fixture()
        resultado, filas = CALC.calcular(inputs, contrato, linaje_fixture)
        self.assertEqual(resultado["u3_puntuable"], ["A", "B"])
        self.assertEqual(resultado["cobertura"]["U3_puntuable"], 2)
        self.assertEqual(len(filas), 8)
        self.assertFalse(resultado["comparacion_congelada_comprometida"])
        self.assertEqual(resultado["veredicto_global"], "SIN-GANADOR-UNICO")

    def test_incertidumbre_r_no_acreditada_no_borra_punto_descriptivo(self):
        inputs, contrato = fixture()
        tarjetas = inputs["IN-TARJETAS"]
        tarjetas["bytes"] = tarjetas["bytes"].replace(
            b"SI\tACREDITADA\tACREDITADA",
            b"SI\tSENSIBILIDAD-NO-DISENO\tACREDITADA",
        )
        tarjetas["sha256"] = hashlib.sha256(tarjetas["bytes"]).hexdigest()
        resultado, _ = CALC.calcular(inputs, contrato, linaje_fixture)
        self.assertEqual(resultado["u3_puntuable"], ["A", "B"])
        self.assertEqual(
            resultado["celdas"]["A"]["R_incertidumbre"],
            "SENSIBILIDAD-NO-DISENO",
        )

    def test_dominancia_sin_cobertura_no_corona_ganador(self):
        inputs, contrato = fixture()
        contrato["parametros"]["u3_congelado"] = ["A"]
        for entrada_l in inputs.values():
            if (entrada_l.get("rol") == "captura_l"
                    and entrada_l.get("id_celda") == "B"
                    and entrada_l.get("variante") == "L-solo"):
                reemplaza_json(
                    entrada_l,
                    lambda d: d.update(texto_crudo="respuesta\nABSTENCION"),
                )
        for entrada_l in inputs.values():
            if (entrada_l.get("rol") == "captura_l"
                    and entrada_l.get("id_celda") == "A"):
                valor = 20 if entrada_l.get("variante") == "L-solo" else 50
                reemplaza_json(
                    entrada_l,
                    lambda d, v=valor: d.update(
                        texto_crudo=f"respuesta\nESTIMACION_PUNTUAL={v}%"),
                )
        reemplaza_json(
            inputs["IN-SNAPSHOT"],
            lambda d: d["celdas"][0].update(punto_M=.6),
        )
        resultado, _ = CALC.calcular(inputs, contrato, linaje_fixture)
        self.assertEqual(resultado["u3_puntuable"], ["A"])
        self.assertEqual(resultado["cobertura_contendiente_para_adjudicacion"], {
            "L_SOLO": 1, "L_CORPUS": 2, "M": 2,
        })
        self.assertEqual(resultado["veredicto_global"], "SIN-GANADOR-UNICO")

    def test_contaminada_no_puntua_y_controla_veredicto(self):
        inputs, contrato = fixture()
        reemplaza_json(
            inputs["IN-SNAPSHOT"],
            lambda d: d["celdas"][0].update(
                estado_firewall="CONTAMINADO-POR-OBJETIVO"),
        )
        resultado, _ = CALC.calcular(inputs, contrato, linaje_fixture)
        self.assertNotIn("A", resultado["u3_puntuable"])
        self.assertFalse(resultado["celdas"]["A"]["elegible"])
        self.assertIn("FIREWALL-CONTAMINADO-POR-OBJETIVO",
                      resultado["celdas"]["A"]["razones_exclusion"])
        self.assertEqual(resultado["veredicto_global"],
                         "NO-ADJUDICABLE-POR-CONTROL")

    def test_identidad_m_falsa_o_desconocida_no_puntua(self):
        for valor in (False, None, "SI"):
            with self.subTest(valor=valor):
                inputs, contrato = fixture()
                reemplaza_json(
                    inputs["IN-SNAPSHOT"],
                    lambda d, v=valor: d["celdas"][0].update(
                        identidad_confirmada=v),
                )
                resultado, _ = CALC.calcular(inputs, contrato, linaje_fixture)
                self.assertNotIn("A", resultado["u3_puntuable"])
                self.assertIn("IDENTIDAD-M-NO-CONFIRMADA",
                              resultado["celdas"]["A"]["razones_exclusion"])

    def test_estado_desconocido_no_equivale_a_limpio(self):
        inputs, contrato = fixture()
        reemplaza_json(
            inputs["IN-SNAPSHOT"],
            lambda d: d["celdas"][0].pop("estado_firewall"),
        )
        resultado, _ = CALC.calcular(inputs, contrato, linaje_fixture)
        self.assertNotIn("A", resultado["u3_puntuable"])
        self.assertIn("FIREWALL-DESCONOCIDO",
                      resultado["celdas"]["A"]["razones_exclusion"])

    def test_punto_m_cadena_no_es_numero(self):
        inputs, contrato = fixture()
        reemplaza_json(
            inputs["IN-SNAPSHOT"],
            lambda d: d["celdas"][0].update(punto_M="0.25"),
        )
        resultado, _ = CALC.calcular(inputs, contrato, linaje_fixture)
        self.assertIsNone(resultado["celdas"]["A"]["M"])
        self.assertNotIn("A", resultado["u3_puntuable"])

    def test_faltante_l_no_se_convierte_en_cero(self):
        inputs, contrato = fixture()
        for replica in (1, 2):
            reemplaza_json(
                inputs[f"IN-L-A-L+corpus-{replica}"],
                lambda d: d.update(texto_crudo="explicación\nABSTENCION"),
            )
        resultado, _ = CALC.calcular(inputs, contrato, linaje_fixture)
        self.assertIsNone(resultado["celdas"]["A"]["brazos"]
                          ["L_CORPUS"]["punto_mediana"])
        self.assertEqual(resultado["celdas"]["A"]["brazos"]
                         ["L_CORPUS"]["abstenciones"], 2)
        self.assertNotIn("A", resultado["u3_puntuable"])


class TestIdentidadYClausura(unittest.TestCase):
    def test_mismo_prompt_respuesta_modificada_rompe_hash(self):
        inputs, contrato = fixture()
        reemplaza_json(
            inputs["IN-L-A-L-solo-1"],
            lambda d: d.update(texto_crudo="ESTIMACION_PUNTUAL=99%"),
            conserva_sha=True,
        )
        with self.assertRaisesRegex(CALC.ContratoInvalido,
                                    "input_sha_discorda"):
            CALC.calcular(inputs, contrato, linaje_fixture)

    def test_cambio_r_o_snapshot_rompe_identidad(self):
        for iid in ("IN-R-A", "IN-SNAPSHOT"):
            with self.subTest(iid=iid):
                inputs, contrato = fixture()
                inputs[iid]["bytes"] += b" "
                with self.assertRaisesRegex(CALC.ContratoInvalido,
                                            "input_sha_discorda"):
                    CALC.calcular(inputs, contrato, linaje_fixture)

    def test_duplicado_e_id_extrano_se_rechazan(self):
        inputs, contrato = fixture()
        reemplaza_json(
            inputs["IN-PLAN"],
            lambda d: d["posiciones"].__setitem__(1,
                                                   copy.deepcopy(d["posiciones"][0])),
        )
        with self.assertRaisesRegex(CALC.ContratoInvalido,
                                    "plan_posicion_duplicada"):
            CALC.calcular(inputs, contrato, linaje_fixture)

        inputs, contrato = fixture()
        reemplaza_json(
            inputs["IN-SNAPSHOT"],
            lambda d: d["celdas"][1].update(id_celda="EXTRAÑA"),
        )
        with self.assertRaisesRegex(CALC.ContratoInvalido,
                                    "no_corresponden"):
            CALC.calcular(inputs, contrato, linaje_fixture)

    def test_copia_rename_y_derivado_r_conservan_reserva(self):
        for ruta in ("m/copia.json", "m/renombrada.json"):
            with self.subTest(ruta=ruta):
                inputs, contrato = fixture()
                reemplaza_json(
                    inputs["IN-SNAPSHOT"],
                    lambda d, r=ruta: d["celdas"][0].update(
                        archivo_fuente=r, linaje_prueba="DEPENDIENTE-R"),
                )
                resultado, _ = CALC.calcular(inputs, contrato, linaje_fixture)
                self.assertNotIn("A", resultado["u3_puntuable"])
                self.assertIn("DEPENDENCIA-OBJETIVO-SI",
                              resultado["celdas"]["A"]["razones_exclusion"])

    def test_procedencia_indeterminada_no_es_limpia(self):
        inputs, contrato = fixture()
        reemplaza_json(
            inputs["IN-SNAPSHOT"],
            lambda d: d["celdas"][0].update(linaje_prueba="INDETERMINADO"),
        )
        resultado, _ = CALC.calcular(inputs, contrato, linaje_fixture)
        self.assertIn("LINAJE-INDETERMINADO",
                      resultado["celdas"]["A"]["razones_exclusion"])
        self.assertNotIn("A", resultado["u3_puntuable"])

    def test_no_lee_json_extra_ni_rutas_despues_del_snapshot(self):
        inputs, contrato = fixture()
        with tempfile.TemporaryDirectory() as td:
            pathlib.Path(td, "R-extra.json").write_text(
                '{"valor": 999}', encoding="utf-8")
            original = builtins.open

            def prohibido(*args, **kwargs):
                raise AssertionError(f"lectura fuera del snapshot: {args[0]}")

            builtins.open = prohibido
            try:
                resultado, _ = CALC.calcular(inputs, contrato, linaje_fixture)
            finally:
                builtins.open = original
        self.assertEqual(resultado["u3_n"], 2)


class TestContrato(unittest.TestCase):
    def test_parametros_consumidos_salen_del_contrato(self):
        inputs, contrato = fixture()
        contrato["parametros"]["bootstrap_replicas"] = 17
        contrato["parametros"]["delta_banda_pp"] = 2.75
        contrato["parametros"]["tolerancia_numerica_pp"] = 1e-7
        contrato["seed"]["valor"] = 987
        resultado, _ = CALC.calcular(inputs, contrato, linaje_fixture)
        self.assertEqual(resultado["parametros_consumidos"], {
            "n_posiciones": 8,
            "k_replicas": 2,
            "seleccion": "MEDIANA-DE-REPLICAS-VALIDAS",
            "bootstrap_replicas": 17,
            "seed": 987,
            "rng": "random.Random",
            "nivel_ic": .95,
            "delta_banda_pp": 2.75,
            "tolerancia_numerica_pp": 1e-7,
        })

    def test_seleccion_no_autorizada_no_tiene_fallback(self):
        inputs, contrato = fixture()
        contrato["parametros"]["seleccion"] = "PROMEDIO"
        with self.assertRaisesRegex(CALC.ContratoInvalido,
                                    "seleccion_no_soportada"):
            CALC.calcular(inputs, contrato, linaje_fixture)

    def test_bootstrap_fraccional_y_pares_incompletos_se_rechazan(self):
        inputs, contrato = fixture()
        contrato["parametros"]["bootstrap_replicas"] = 17.5
        with self.assertRaisesRegex(CALC.ContratoInvalido,
                                    "bootstrap_replicas_no_entero"):
            CALC.calcular(inputs, contrato, linaje_fixture)

        inputs, contrato = fixture()
        contrato["parametros"]["comparaciones"].pop()
        with self.assertRaisesRegex(CALC.ContratoInvalido,
                                    "comparaciones_no_cubren_triada"):
            CALC.calcular(inputs, contrato, linaje_fixture)


class TestBaselineHistorico(unittest.TestCase):
    def test_mismos_criterios_reproducen_triada_0002(self):
        spec = GENERADOR.construir(pathlib.Path("tools/corrida0.py"))
        inputs = {}
        for declarada in spec["inputs"]:
            completa = dict(declarada)
            crudo = (ROOT / declarada["ruta"]).read_bytes()
            completa.update(estado="COINCIDE", bytes=crudo)
            inputs[completa["id"]] = completa

        ids = sorted(json.loads(inputs["IN-F5SF-SNAPSHOT-M"]["bytes"])[
            "celdas"][i]["id_celda"] for i in range(14))
        tarjetas = (
            "id_celda\tproposito\testimando_alineado\tcumple_corte\t"
            "R_punto_apto\tR_incertidumbre\tcomparabilidad\t"
            "fuente_criterio\tcausa\n" + "".join(
                f"{cid}\tREANALISIS-DIAGNOSTICO-TRANSFERENCIA\tSI\tSI\t"
                "SI\tSEPARADA-DEL-PUNTO\tACREDITADA\t"
                "baseline-historico\tcriterios históricos sin endurecer\n"
                for cid in ids
            )
        ).encode("utf-8")
        entrada_tarjetas = inputs["IN-F5SF-TARJETAS-MR"]
        entrada_tarjetas["bytes"] = tarjetas
        entrada_tarjetas["sha256"] = hashlib.sha256(tarjetas).hexdigest()
        contrato = {
            clave: copy.deepcopy(spec[clave])
            for clave in (
                "variables", "universo", "filtros", "ponderador",
                "transformacion", "estimando", "parametros", "seed",
            )
        }

        resultado, filas = CALC.calcular(inputs, contrato, linaje_fixture)
        self.assertEqual(len(filas), 224)
        self.assertEqual(resultado["u3_n"], 12)
        self.assertEqual(resultado["u3_puntuable"], [
            "CIV-M-01", "CIV-M-02", "CIV-M-04", "CIV-M-10",
            "CIV-M-12", "CIV-M-13", "FAM-M-01", "FAM-M-05",
            "FAM-M-06", "FAM-M-07", "TRA-M-02", "TRA-M-03",
        ])
        self.assertEqual(
            resultado["cobertura_contendiente_para_adjudicacion"],
            {"L_SOLO": 14, "L_CORPUS": 12, "M": 14},
        )
        esperado = {
            "L_SOLO": 3.9573621816025666,
            "L_CORPUS": 3.889025747112979,
            "M": 4.9866732397828875,
        }
        for nombre, valor in esperado.items():
            self.assertAlmostEqual(
                resultado["mae_pp_diagnostico"][nombre], valor, places=12)
        self.assertEqual(resultado["veredicto_global"],
                         "SIN-GANADOR-UNICO")

    def test_borde_de_banda_usa_delta_y_tolerancia_recibidos(self):
        self.assertEqual(CALC.adjudicar_ic(-.5, .5, .5, 1e-9, "A", "B"),
                         "EMPATE-PRACTICO")
        self.assertEqual(CALC.adjudicar_ic(-.8, -.6, .5, 1e-9, "A", "B"),
                         "A-GANA")


if __name__ == "__main__":
    unittest.main()
