"""ACTO GEN2-CAJA-REACTIVOS-FD-1 -- regresión del crosswalk de tablas (NC-0245)
y de la extensión del extractor a los 26 grupos con FD en el repo (NC-0235).

Lo que protegen, uno por uno, y por qué un cambio bienintencionado los rompe:

* La **cobertura se cuenta por variable, no por clave**. Las claves son
  variantes de la misma variable (plegada, sin sufijo de ola); contarlas infla
  el denominador. Defecto real, medido en esta sesión: ENASEM 2018 salía con
  cobertura 0.50 y caía al residual por `IDENTIDAD-INSUFICIENTE` cuando su
  cobertura verdadera es 0.99.
* Un **miembro que vive dentro del propio FD** no es una tabla de payload: sus
  "variables" son los rótulos de columna del descriptor (`Nombre de la BD`,
  `Tipo de dato`). Publicarlo como emparejamiento infla el crosswalk con 150
  filas que no cruzan nada.
* La **declaración dentro del FD gana al título de la hoja**. Son dos fuerzas
  de evidencia distintas y el método viaja en cada fila; fundirlas en un solo
  rótulo borra la diferencia entre "el descriptor lo dice" y "los nombres se
  parecen".
* El **crosswalk manda sobre la identidad de tabla escrita a mano** en
  `actualiza_reactivos_contexto.py`, y excluye a la hoja parecida. Sin esa
  regla, ENDUTIH 2025 publica 0 filas (medido: 0 con `--crosswalk` apagado,
  499 con él).
* Una tabla con el **eje transpuesto** (periodos por columna) no se empareja
  con calzador: se declara y se sale del denominador.
"""
import unittest

from tools import busca_reactivos as busca
from tools import crosswalk_tablas_fd as cw
from tools import actualiza_reactivos_contexto as ctx


class NormalizaTablaTest(unittest.TestCase):
    def test_quita_extension_conocida(self):
        self.assertEqual(cw.normaliza_tabla("ti25hog.dbf"), "ti25hog")
        self.assertEqual(cw.normaliza_tabla("TI_MANZANA_EU_00.csv"), "timanzanaeu")

    def test_quita_el_sello_de_publicacion_de_cnbv(self):
        self.assertEqual(cw.normaliza_tabla("52Sep2022_BD_Acceso_Edo.csv"),
                         cw.normaliza_tabla("BD Acceso Edo"))

    def test_no_quita_lo_que_no_es_extension_conocida(self):
        # Un punto en el nombre no es una extensión: quitarlo perdería la tabla.
        self.assertEqual(cw.normaliza_tabla("tic_2023.usuarios"), "tic2023usuarios")


class ClavesDeVariableTest(unittest.TestCase):
    def test_sufijo_de_ola_se_deriva_del_instrumento(self):
        self.assertEqual(cw.olas_de("enasem2018"), ("2018", "18"))
        self.assertEqual(cw.olas_de("ADQ15_CNBV_BDIF_inclusion_financiera"), ())

    def test_la_variable_con_sufijo_de_ola_alcanza_a_la_del_fd(self):
        claves = cw.claves_variable("A13A_18", cw.olas_de("enasem2018"))
        self.assertIn("a13a", claves)
        self.assertIn("a13a18", claves)

    def test_no_recorta_cuando_el_sufijo_es_todo_el_nombre(self):
        self.assertEqual(cw.claves_variable("_18", cw.olas_de("enasem2018")), ("18",))

    def test_pliega_mayusculas_del_sav_al_dbf(self):
        # MOCIBA escribe `upm` en el .sav y `UPM` en el .dbf y en el FD.
        self.assertEqual(cw.claves_variable("upm", ())[0], cw.claves_variable("UPM", ())[0])


class EjeTranspuestoTest(unittest.TestCase):
    def test_una_fecha_por_columna_es_periodo(self):
        self.assertTrue(cw.es_periodo("2000-09-01 00:00:00"))
        self.assertTrue(cw.es_periodo("2022/12"))

    def test_un_mnemonico_no_es_periodo(self):
        self.assertFalse(cw.es_periodo("P4_1_1"))
        self.assertFalse(cw.es_periodo("FAC_MOCIBA"))


class DeclaracionesDelFdTest(unittest.TestCase):
    def test_lee_la_celda_tabla_del_censo(self):
        filas = [("CENSO DE POBLACIÓN Y VIVIENDA 2020",), (None,), ("TABLA: TR_ALO_CAAS",)]
        nombres = [n for n, _e in cw.declaraciones_de_hoja(filas)]
        self.assertIn("TR_ALO_CAAS", nombres)

    def test_lee_la_columna_nombre_de_la_bd_de_cnbv(self):
        filas = [("Nombre de la BD", "Nombre de la columna"),
                 ("BD Acceso Edo", "Clave_Estado"),
                 ("BD Acceso Edo", "Region")]
        nombres = [n for n, _e in cw.declaraciones_de_hoja(filas)]
        self.assertEqual(nombres, ["BD Acceso Edo"])

    def test_lee_el_rotulo_de_seccion(self):
        filas = [("1. Título", "Base de Ahorro"), ("4. Sección", "Ahorro financiero")]
        nombres = [n for n, _e in cw.declaraciones_de_hoja(filas)]
        self.assertIn("Ahorro financiero", nombres)

    def test_una_hoja_sin_declaracion_no_inventa_ninguna(self):
        self.assertEqual(cw.declaraciones_de_hoja([("NÚMERO", "DESCRIPCIÓN")]), [])

    def test_la_evidencia_es_literal_no_parafraseada(self):
        (_nombre, evidencia), = cw.declaraciones_de_hoja([("TABLA: TI_USU_CAAS",)])
        self.assertIn("TI_USU_CAAS", evidencia)


class CrosswalkPublicadoTest(unittest.TestCase):
    """Propiedades de la tabla publicada, no del código que la escribe."""

    @classmethod
    def setUpClass(cls):
        cls.filas = cw.lee_tsv(cw.SALIDA)
        cls.residual = cw.lee_tsv(cw.SALIDA_RESIDUAL)

    def test_el_metodo_distingue_declaracion_de_parecido_de_nombre(self):
        metodos = {f["metodo"] for f in self.filas}
        self.assertTrue(metodos <= {"FD-DECLARA-TABLA", "FD-NOMBRE-DE-HOJA",
                                    "IDENTIDAD-DE-VARIABLES"}, metodos)
        self.assertIn("FD-DECLARA-TABLA", metodos)

    def test_toda_fila_cita_el_sha_del_descriptor_que_la_sostiene(self):
        sin_cita = [f for f in self.filas if not f["sha256_12_fd"].strip()]
        self.assertEqual(sin_cita, [])

    def test_endutih2025_empareja_el_dbf_con_la_hoja_del_fd(self):
        # El caso que NC-0245 nombró: `ti25hog.dbf` ↔ `tic_2025_hogares` es
        # mapeo semántico, no normalizable por ortografía.
        fila, = [f for f in self.filas
                 if f["instrumento"] == "endutih2025" and f["archivo_miembro"] == "ti25hog.dbf"]
        self.assertEqual(fila["hoja_fd"], "tic_2025_hogares")
        self.assertEqual(fila["metodo"], "IDENTIDAD-DE-VARIABLES")

    def test_una_hoja_describe_una_sola_tabla(self):
        # Dos formatos de la MISMA tabla (`.DBF` y `.sav` de MOCIBA) sí comparten
        # hoja -- son el mismo objeto escrito dos veces. Dos tablas DISTINTAS
        # apuntando a la misma hoja serían una identidad inventada.
        tablas_por_hoja = {}
        for f in self.filas:
            llave = (f["instrumento"], f["hoja_fd"])
            tablas_por_hoja.setdefault(llave, set()).add(
                cw.normaliza_tabla(f["archivo_miembro"]))
        repartidas = {k: v for k, v in tablas_por_hoja.items() if len(v) > 1}
        self.assertEqual(repartidas, {})

    def test_el_residual_no_se_maquilla(self):
        motivos = {f["motivo"] for f in self.residual}
        self.assertIn("EJE-TRANSPUESTO", motivos)
        self.assertIn("MIEMBRO-ES-EL-PROPIO-FD", motivos)
        for fila in self.residual:
            self.assertTrue(fila["detalle"].strip(), fila)

    def test_el_denominador_no_se_recorta(self):
        # Cubiertas + residuales = las 7 620 filas ciegas que NC-0245 dejó.
        cubiertas = sum(int(f["filas_ciegas_cubiertas"]) for f in self.filas)
        residuales = sum(int(f["filas_ciegas"]) for f in self.residual)
        entrada = len(cw.lee_tsv(cw.RESIDUAL_ENTRADA))
        self.assertEqual(cubiertas + residuales, entrada)


class ExtensionDelExtractorTest(unittest.TestCase):
    def setUp(self):
        ctx.carga_crosswalk(ctx.CROSSWALK_PATH)

    def tearDown(self):
        ctx.carga_crosswalk(ctx.CROSSWALK_PATH)

    def test_el_crosswalk_manda_sobre_la_identidad_escrita_a_mano(self):
        self.assertTrue(ctx.compatible_table("ti25hog.dbf", "tic_2025_hogares", "endutih2025"))

    def test_y_excluye_a_la_hoja_parecida(self):
        # Sin esta exclusión, `choose_candidate` ve dos candidatas y no publica
        # ninguna: es el `CORRESPONDENCIA_AMBIGUA` de 499 filas que se midió.
        self.assertFalse(ctx.compatible_table("ti25hog.dbf", "tic_2025_usuarios", "endutih2025"))

    def test_donde_el_crosswalk_calla_el_comportamiento_historico_queda_intacto(self):
        ctx.carga_crosswalk(ctx.Path("/no/existe.tsv"))
        self.assertTrue(ctx.compatible_table("tperviv", "TPer_Vic"))

    def test_las_tablas_de_fuentes_se_suman_no_se_sustituyen(self):
        juntas = ctx.read_tsv_many([ctx.SOURCES_PATH, ctx.SOURCES_FD26_PATH])
        self.assertEqual(len(juntas),
                         len(ctx.read_tsv(ctx.SOURCES_PATH))
                         + len(ctx.read_tsv(ctx.SOURCES_FD26_PATH)))

    def test_las_26_fuentes_nuevas_no_pisan_la_tabla_historica(self):
        historicos = {r["instrumento"] for r in ctx.read_tsv(ctx.SOURCES_PATH)}
        nuevos = {r["instrumento"] for r in ctx.read_tsv(ctx.SOURCES_FD26_PATH)}
        self.assertEqual(historicos & nuevos, set())
        self.assertEqual(len(nuevos), 26)


class ConsumoDelBuscadorTest(unittest.TestCase):
    def test_la_capa_nueva_tiene_clave_explicita(self):
        self.assertIn("contexto_fd26", busca.TABLAS)

    def test_y_no_entra_en_vigente(self):
        # `vigente` es lo que lee quien NO pidió esta capa: reapuntarla cambiaría
        # en silencio el universo de toda búsqueda anterior.
        self.assertNotIn("contexto_fd26", busca.FUENTES)

    def test_el_crosswalk_no_entra_al_buscador(self):
        # Otro grano: su fila es una TABLA, no un reactivo. Recorrerlo con
        # `--tablas todas` daría filas sin texto que se leen como ausencia.
        self.assertNotIn("crosswalk_fd", busca.TABLAS)


if __name__ == "__main__":
    unittest.main()
