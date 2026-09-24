"""Guardas de mutación del primer escritor de consumo GEN2."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import escribe_relevo_consumo as writer  # noqa: E402


class WriterTest(unittest.TestCase):
    def setUp(self):
        self.source = (
            '  - {conducta: denuncia_por_otra_razon, p: 0.705687, '
            'clase: "DERIVADO", rol_uso: complemento_dependiente, '
            'uso_motor: "PROPUESTA-NO-ADOPTADA-NC-0085: complemento"}\n'
        )

    def test_exact_single_structural_change_and_idempotence(self):
        changed = writer.transform(self.source, "0.705687")
        self.assertIn("corrida0_resultado_id: " + writer.RESULT, changed)
        self.assertIn("corrida0_generacion: GEN2", changed)
        self.assertIn("p: 0.705687", changed)
        self.assertIn("GEN2-RELEVADO-POR-PIN", changed)
        self.assertEqual(changed, writer.transform(changed, "0.705687"))

    def test_rejects_prior_value_or_partial_citation(self):
        with self.assertRaises(ValueError):
            writer.transform(self.source.replace("0.705687", "0.705688"), "0.705687")
        with self.assertRaises(ValueError):
            writer.transform(self.source.replace("clase:", "corrida0_generacion: GEN2, clase:"), "0.705687")

    def test_rejects_nonunique_consumer(self):
        with self.assertRaises(ValueError):
            writer.transform(self.source + self.source, "0.705687")


class CrearDesdePropuestaTest(unittest.TestCase):
    """Guardas del modo V2 (ACTO GEN2-ADOPCION-BLOQUE-Y-PINES-4): datos
    sintéticos, no el `tramite.yaml`/`tramite-ola5-propuesta-v0.yaml`
    reales -- una vez este acto aplique el escritor, las tres reglas ya
    viven en el consumidor y un test contra los archivos reales dejaría
    de poder ejercitar la ruta de creación."""

    def setUp(self):
        self.propuesta_lineas = (
            "  - id: dominio.otra.regla_previa\n"
            "    situacion: PENDIENTE-DE-MESA\n"
            "    entonces:\n"
            "      - {conducta: previa, p: 0.1}\n"
            "    falsable_si: PENDIENTE-DE-MESA\n"
            "    fuente: [\"X\"]\n"
            "\n"
            "  # ══════════════════════════════════════════════════════\n"
            "  # banner que documenta la regla SIGUIENTE, no ésta\n"
            "  # ══════════════════════════════════════════════════════\n"
            "  - id: dominio.prueba.regla_sintetica\n"
            "    situacion: PENDIENTE-DE-MESA\n"
            "    si:\n"
            "      disparadores: PENDIENTE-DE-MESA\n"
            "    entonces:\n"
            "      - {conducta: sintetica_alta, p: 0.4242, clase: \"MEDIDO\","
            " corrida0_resultado_id: RESULT-SINTETICO-ALTA, corrida0_generacion: GEN2,"
            " rol_uso: proxy_descriptivo, uso_motor: \"PROXY-DESCRIPTIVO de prueba\"}\n"
            "      - {conducta: sintetica_no_estimable, p: null, clase: \"NO-ESTIMABLE\","
            " corrida0_resultado_id: RESULT-SINTETICO-NULO, corrida0_generacion: GEN2,"
            " rol_uso: proxy_descriptivo, uso_motor: \"sin estimación\"}\n"
            "    porque: {generador: PENDIENTE-DE-MESA, mecanismo: PENDIENTE-DE-MESA}\n"
            "    tier: PENDIENTE-DE-MESA\n"
            "    falsable_si: PENDIENTE-DE-MESA\n"
            "    fuente: [\"FUENTE-SINTETICA\"]\n"
            "    universo: \"universo sintético de prueba\"\n"
            "\n"
            "  - id: dominio.otra.regla_siguiente\n"
            "    situacion: PENDIENTE-DE-MESA\n"
        ).splitlines(keepends=True)
        self.resultados = {
            "RESULT-SINTETICO-ALTA": {"resultado_id": "RESULT-SINTETICO-ALTA",
                                      "valor": "0.4242"},
        }
        self.redaccion = {
            "dominio.prueba.regla_sintetica": {
                "situacion": "segmento_sintetico_de_prueba",
                "disparadores_estado": "explicación   con\nsaltos de línea de prueba",
                "tier": "MEDIA",
                "falsable_si": "si el dato sintético cambia, esto se falsa",
                "porque": {"generador": ["G3"], "mecanismo": "mecanismo sintético de prueba"},
            },
        }

    def test_extrae_bloque_recorta_banner_de_la_siguiente_regla(self):
        bloque = writer._extraer_bloque_regla(
            self.propuesta_lineas, "dominio.prueba.regla_sintetica")
        self.assertEqual(bloque[0], "  - id: dominio.prueba.regla_sintetica\n")
        self.assertTrue(bloque[-1].startswith('    universo:'))
        self.assertFalse(any(l.startswith("  #") for l in bloque))
        self.assertFalse(any("regla_siguiente" in l for l in bloque))

    def test_extrae_bloque_exige_aparicion_unica(self):
        with self.assertRaises(ValueError):
            writer._extraer_bloque_regla(
                self.propuesta_lineas + self.propuesta_lineas[9:20],
                "dominio.prueba.regla_sintetica")

    def test_divide_bloque_separa_entonces_de_la_cola(self):
        bloque = writer._extraer_bloque_regla(
            self.propuesta_lineas, "dominio.prueba.regla_sintetica")
        entonces, cola = writer._dividir_bloque(bloque, "dominio.prueba.regla_sintetica")
        self.assertTrue(entonces.startswith("    entonces:\n"))
        self.assertIn("RESULT-SINTETICO-ALTA", entonces)
        self.assertNotIn("porque:", entonces)
        self.assertTrue(cola.startswith('    fuente: ["FUENTE-SINTETICA"]\n'))
        self.assertIn("universo sintético de prueba", cola)
        self.assertNotIn("falsable_si", cola)

    def test_verifica_entonces_pasa_con_p_identico_y_null_se_salta(self):
        regla = {"entonces": [
            {"conducta": "sintetica_alta", "p": 0.4242,
             "corrida0_resultado_id": "RESULT-SINTETICO-ALTA",
             "corrida0_generacion": "GEN2", "rol_uso": "proxy_descriptivo"},
            {"conducta": "sintetica_no_estimable", "p": None,
             "corrida0_resultado_id": "RESULT-SINTETICO-NULO",
             "corrida0_generacion": "GEN2", "rol_uso": "proxy_descriptivo"},
        ]}
        writer._verifica_entonces("dominio.prueba.regla_sintetica", regla, self.resultados)

    def test_verifica_entonces_detecta_p_discordante_con_el_result(self):
        regla = {"entonces": [
            {"conducta": "sintetica_alta", "p": 0.9999,
             "corrida0_resultado_id": "RESULT-SINTETICO-ALTA",
             "corrida0_generacion": "GEN2", "rol_uso": "proxy_descriptivo"},
        ]}
        with self.assertRaises(ValueError):
            writer._verifica_entonces("dominio.prueba.regla_sintetica", regla, self.resultados)

    def test_verifica_entonces_exige_generacion_gen2_y_rol_proxy(self):
        base = {"conducta": "sintetica_alta", "p": 0.4242,
                "corrida0_resultado_id": "RESULT-SINTETICO-ALTA"}
        with self.assertRaises(ValueError):
            writer._verifica_entonces(
                "x", {"entonces": [dict(base, corrida0_generacion="GEN1",
                                       rol_uso="proxy_descriptivo")]},
                self.resultados)
        with self.assertRaises(ValueError):
            writer._verifica_entonces(
                "x", {"entonces": [dict(base, corrida0_generacion="GEN2",
                                       rol_uso="medicion_directa")]},
                self.resultados)

    def test_renderiza_regla_incluye_los_cuatro_campos_rotulados_y_el_verbatim(self):
        bloque = writer._extraer_bloque_regla(
            self.propuesta_lineas, "dominio.prueba.regla_sintetica")
        entonces, cola = writer._dividir_bloque(bloque, "dominio.prueba.regla_sintetica")
        writer._CITAS_ORIGEN_PROPUESTA["dominio.prueba.regla_sintetica"] = "líneas de prueba"
        try:
            texto = writer._renderiza_regla_nueva(
                "dominio.prueba.regla_sintetica", entonces, cola, self.redaccion)
        finally:
            del writer._CITAS_ORIGEN_PROPUESTA["dominio.prueba.regla_sintetica"]
        self.assertIn("situacion: segmento_sintetico_de_prueba  # PROPUESTO-POR-EJECUTOR", texto)
        self.assertIn('tier: MEDIA  # PROPUESTO-POR-EJECUTOR', texto)
        self.assertIn('falsable_si: "si el dato sintético cambia, esto se falsa"', texto)
        self.assertIn('mecanismo: "mecanismo sintético de prueba"', texto)
        self.assertIn("generador: [G3]", texto)
        self.assertIn(entonces, texto)
        self.assertIn(cola, texto)
        # `disparadores_estado` con saltos de línea se colapsa a una sola línea
        self.assertIn('"explicación con saltos de línea de prueba"', texto)
        # el bloque completo debe seguir siendo YAML válido
        import yaml  # noqa: PLC0415
        doc = yaml.safe_load("reglas:\n" + texto)
        regla_cargada = doc["reglas"][0]
        self.assertEqual(regla_cargada["id"], "dominio.prueba.regla_sintetica")
        self.assertEqual(regla_cargada["si"]["disparadores"], {})

    def test_renderiza_regla_rechaza_comillas_rectas_en_campo_redactado(self):
        redaccion = {"dominio.prueba.regla_sintetica": {
            "situacion": "x", "disparadores_estado": 'con "comillas" rectas',
            "tier": "MEDIA", "falsable_si": "y",
            "porque": {"generador": ["G3"], "mecanismo": "z"},
        }}
        writer._CITAS_ORIGEN_PROPUESTA["dominio.prueba.regla_sintetica"] = "líneas de prueba"
        try:
            with self.assertRaises(ValueError):
                writer._renderiza_regla_nueva(
                    "dominio.prueba.regla_sintetica", "    entonces: []\n", "", redaccion)
        finally:
            del writer._CITAS_ORIGEN_PROPUESTA["dominio.prueba.regla_sintetica"]


if __name__ == "__main__":
    unittest.main()
