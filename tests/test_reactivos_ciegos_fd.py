"""ACTO GEN2-REACTIVOS-RESIDUALES-2 -- regresión de P1 (censo) y P2 (cableado FD).

Lo que estas pruebas protegen es el hueco que el acto cerró: el 81 de NC-0136
dejaba de ser derivable si alguien cambiaba el grano del censo, y la capa FD
volvía a ser invisible si alguien retiraba las claves `fd`/`fd_ext`. También
protegen lo contrario: que esas claves NO entren en `vigente` ni en `--fuente`,
porque hacerlo cambiaría en silencio las cifras publicadas del buscador.
"""
import unittest

from tools import busca_reactivos as busca
from tools import censa_reactivos_ciegos as censa


class CensoCiegosTest(unittest.TestCase):
    def setUp(self):
        self.c = censa.censa()

    def test_universo_y_ciegos_son_los_publicados(self):
        # Cifras declaradas en la cabecera de data/inventario-reactivos-v1_2.tsv
        # (ACTO GEN2-DERIVADORES-FIX, NC-0123): 241591 filas, 116 instrumentos,
        # 102 ciegos. Si el índice cambia, esta prueba lo dice en vez de que el
        # censo publique un número nuevo en silencio.
        self.assertEqual(self.c["universo_filas"], 241591)
        self.assertEqual(self.c["universo_instrumentos"], 116)
        self.assertEqual(self.c["ciegos"], 102)

    def test_los_81_grupos_de_nc0136_se_derivan(self):
        self.assertEqual(len(self.c["filas"]), 81)
        self.assertEqual(self.c["ciegos_en_lote"], 21)
        self.assertEqual(sum(r["filas_ciegas"] for r in self.c["filas"]), 129648)

    def test_ningun_grupo_del_lote_se_cuela(self):
        for r in self.c["filas"]:
            self.assertFalse(r["instrumento"].lower().startswith(censa.LOTE), r["instrumento"])

    def test_ruta_de_recuperacion_es_consecuencia_del_conteo(self):
        for r in self.c["filas"]:
            if r["fd_filas_capa_limpia"] > 0:
                esperada = "CABLEAR-CAPA-FD-YA-EN-REPO"
            elif r["fd_filas_con_texto"] > 0:
                esperada = "CANDIDATA-FD-EXT-POR-VERIFICAR"
            else:
                esperada = "REQUIERE-FD-EN-CORPUS"
            self.assertEqual(r["ruta_recuperacion"], esperada, r["instrumento"])

    def test_la_capa_pdf_no_se_promete_como_resuelta(self):
        """`elcos2012` tiene 29 filas en fd_ext y CERO enunciados utilizables: sus
        29 textos son el encabezado «(1)» de la tabla. Si el censo lo rotulara
        CABLEAR-CAPA-FD-YA-EN-REPO estaría prometiendo texto que no existe."""
        fila = {r["instrumento"]: r for r in self.c["filas"]}["elcos2012"]
        self.assertEqual(fila["fd_filas_capa_limpia"], 0)
        self.assertGreater(fila["fd_filas_con_texto"], 0)
        self.assertEqual(fila["ruta_recuperacion"], "CANDIDATA-FD-EXT-POR-VERIFICAR")

    def test_el_panel_f6_leido_es_el_vigente_por_version(self):
        """Apuntar a una versión fija haría que el censo declarara
        NINGUNA-DECLARADA-HOY sobre familias que un panel nuevo ya reclama."""
        panel = censa.panel_f6_vigente()
        self.assertIsNotNone(panel)
        candidatos = sorted(censa._PANEL_DIR.glob("F5-panel-candidatos-v*.tsv"))
        self.assertEqual(panel, candidatos[-1])
        self.assertEqual(self.c["panel_f6_leido"], panel.name)

    def test_demanda_no_se_inventa_por_subcadena(self):
        # `enif2024` es del lote (no está en el censo) y `encig2011` NO lo
        # reclama el mapa-19 aunque `encig2023` sí: la derivación es por
        # igualdad, no por prefijo compartido.
        fila = {r["instrumento"]: r for r in self.c["filas"]}
        self.assertEqual(fila["encig2011"]["demanda_hoy"], "NINGUNA-DECLARADA-HOY")
        self.assertIn("CORR-0001", fila["encig2023"]["demanda_hoy"])


class CapaFDCableadaTest(unittest.TestCase):
    def test_claves_fd_existen_y_apuntan_a_la_capa_fd(self):
        for clave, nombre in (("fd", "inventario-fd-v1_1.tsv"),
                              ("fd_ext", "inventario-fd-ext-v1_0.tsv")):
            self.assertIn(clave, busca.TABLAS)
            self.assertEqual(busca.TABLAS[clave].name, nombre)
            self.assertTrue(busca.TABLAS[clave].exists())

    def test_fd_no_entra_en_vigente_ni_en_fuente(self):
        # El convenio de `contexto_v1_0`/`descargas_mx`: claves explícitas.
        self.assertNotIn("fd", busca.FUENTES)
        self.assertNotIn("fd_ext", busca.FUENTES)
        self.assertNotEqual(busca.CONTEXTO, busca.TABLAS["fd"])

    def test_la_bateria_de_denuncia_de_mociba_es_visible_por_la_capa_fd(self):
        # La compuerta que ACTO GEN2-F5-CIERRE-Y-PANEL-1 dejó escrita para
        # R01 · MOCIBA. Antes de este acto, esta búsqueda daba cero por
        # construcción: la capa que la contiene no se consultaba.
        filas = busca.lee_filas(busca.TABLAS["fd"])
        hits = [f for f in filas
                if f["instrumento"] in ("mociba2021", "mociba2023")
                and "Denunciar ante el Ministerio" in (f.get("texto_reactivo") or "")]
        self.assertEqual(len(hits), 2)
        self.assertEqual({f["variable_id"] for f in hits}, {"P12_5", "P12_05"})


if __name__ == "__main__":
    unittest.main()
