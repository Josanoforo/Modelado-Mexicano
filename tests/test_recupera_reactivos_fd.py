"""ACTO GEN2-RESIDUAL-81-1 -- regresión de la recuperación por identidad exacta.

Lo que protegen: que la recuperación NO se afloje a emparejar por nombre de
variable (10 765 filas emparejarían así), que el puente de tabla siga siendo
el declarado, que el residual no se maquille, y que `fd_recuperado` no entre
en `vigente` -- todas son propiedades que un cambio bienintencionado puede
romper en silencio.
"""
import unittest

from tools import busca_reactivos as busca
from tools import recupera_reactivos_fd as rec


class PuenteDeTablaTest(unittest.TestCase):
    def test_pliega_miembro_quita_extension_conocida(self):
        self.assertEqual(rec.pliega_miembro("thogar.csv"), "thogar")
        self.assertEqual(rec.pliega_miembro("mod_2017_ciberacoso.dbf"), "mod_2017_ciberacoso")
        self.assertEqual(rec.pliega_miembro("TMOCIBA"), "tmociba")

    def test_quita_la_ruta_interna_del_paquete(self):
        # El índice guarda a veces el camino dentro del zip; el descriptor nunca.
        self.assertEqual(rec.pliega_miembro("enut_2019/THOGAR.csv"), "thogar")

    def test_no_quita_lo_que_no_es_extension_conocida(self):
        # Un punto en el nombre no es una extensión: quitarlo perdería la tabla.
        self.assertEqual(rec.pliega_miembro("tic_2023.usuarios"), "tic_2023.usuarios")

    def test_texto_tipo_se_deriva_del_rasgo_observable(self):
        self.assertEqual(rec.texto_tipo("Condición de actividad"), "ETIQUETA_VARIABLE")
        self.assertEqual(rec.texto_tipo("6.33.1 ¿cuántas horas?"), "PREGUNTA_DICCIONARIO")


class RecuperacionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = rec.recupera()

    def test_los_18_grupos_del_censo_son_el_universo(self):
        self.assertEqual(self.c["grupos"], 18)
        total = len(self.c["publicadas"]) + len(self.c["residual"])
        self.assertEqual(total, 16815)

    def test_la_identidad_publicada_es_exacta_y_nunca_por_variable_sola(self):
        vias = self.c["motivos"]
        self.assertEqual(vias.get("EXACTO", 0) + vias.get("EXACTO_PREFIJO_31", 0),
                         len(self.c["publicadas"]))
        # No existe ninguna vía de publicación que no sea una de las dos exactas.
        for f in self.c["publicadas"]:
            self.assertRegex(f["referencia_fuente"], r"via=(EXACTO|EXACTO_PREFIJO_31)$")

    def test_el_residual_no_se_maquilla(self):
        self.assertEqual(len(self.c["residual"]),
                         sum(self.c["motivos"].get(k, 0)
                             for k in ("TABLA_SIN_FD", "VARIABLE_SIN_FD", "TABLA_AMBIGUA")))
        for f in self.c["residual"]:
            self.assertIn(f["motivo"], ("TABLA_SIN_FD", "VARIABLE_SIN_FD", "TABLA_AMBIGUA"))
            self.assertTrue(f["detalle"])

    def test_cada_fila_publicada_conserva_su_origen_y_su_fuente(self):
        for f in self.c["publicadas"][:200]:
            self.assertTrue(f["id_origen"])
            self.assertTrue(f["fuente_texto"])
            self.assertTrue(f["texto_reactivo"].strip())
            self.assertIn(f["texto_tipo"], ("ETIQUETA_VARIABLE", "PREGUNTA_DICCIONARIO"))

    def test_ningun_instrumento_del_lote_prioritario_entra(self):
        # El overlay del lote (43 020/55 895) no se toca ni se amplía por aquí.
        for f in self.c["publicadas"]:
            self.assertFalse(f["instrumento"].lower().startswith(
                ("envipe", "enif", "encuci", "ensafi", "ennvih")), f["instrumento"])


class ClaveDelBuscadorTest(unittest.TestCase):
    def test_fd_recuperado_existe_y_es_explicita(self):
        self.assertIn("fd_recuperado", busca.TABLAS)
        self.assertTrue(busca.TABLAS["fd_recuperado"].exists())
        self.assertNotIn("fd_recuperado", busca.FUENTES)

    def test_devuelve_lo_que_el_universo_ciego_no_podia(self):
        filas = busca.lee_filas(busca.TABLAS["fd_recuperado"])
        hits = [f for f in filas if "TRAB_NO_REM" in (f["variable_id"] or "")]
        self.assertTrue(hits)
        self.assertTrue(all(f["instrumento"] == "enut2024" for f in hits))


if __name__ == "__main__":
    unittest.main()
