"""E2 tabular: el encabezado de una tabla es metadato, no una fila de datos.

El §8 del encargo de BARRIDO-2 exige que la caracterización neutral conserve
nombre de variable, etiqueta, categorías y value labels. La primera pasada
material los perdió en todo lo tabular —202 316 objetos `COLUMNA` con nombre
posicional y `categorias` en 0.00 % del universo— porque el encabezado real sólo
se conservaba cuando el archivo se autodeclaraba diccionario por su nombre, y
ese detector no disparó ni una vez en 672 representaciones.

Estas pruebas fijan el contrato de la corrección. Son sintéticas a propósito: el
corpus vive fuera de git y una prueba que dependa de él no corre en otra caja.
"""

from __future__ import annotations

import io
import unittest
import zipfile
from pathlib import Path

import openpyxl

from tools.curador_registro.barrido2_material import (
    _csv_objects,
    _looks_like_header,
    _xlsx_objects,
)


def csv_objects(texto: str, *, locator: str = "tabla=raiz", suffix: str = ".csv") -> list[dict]:
    return _csv_objects(io.BytesIO(texto.encode("utf-8")), locator, suffix)


def tabla(objects: list[dict]) -> dict:
    return next(o for o in objects if o["type"] == "TABLA")


def columnas(objects: list[dict]) -> list[str]:
    return [o["name"] for o in objects if o["type"] == "COLUMNA"]


class EncabezadoDelimitadoTests(unittest.TestCase):
    def test_encabezado_limpio_se_conserva_y_no_se_cuenta_como_dato(self) -> None:
        objetos = csv_objects("LLAVEVIV,PAREN,SEXO,EDAD\n1,1,2,34\n2,3,1,17\n")
        self.assertEqual(["LLAVEVIV", "PAREN", "SEXO", "EDAD"], columnas(objetos))
        definicion = tabla(objetos)["definition"]
        self.assertIn("encabezado=SI-DERIVADO", definicion)
        # Dos observaciones, no tres: la fila de nombres no es un dato.
        self.assertIn("filas=2", definicion)

    def test_nombres_de_variable_inegi_no_activan_la_heuristica_de_nombre_propio(self) -> None:
        """`VIV_SEL`, `N_REN`, `FAC_HOG` tienen la FORMA de un nombre propio en
        mayúsculas y no son datos personales. Basta una columna así para vetar
        el encabezado entero de casi cualquier archivo del INEGI."""
        fila = "LLAVEVIV,VIV_SEL,N_REN,FAC_HOG,EST_DIS,UPM_DIS"
        self.assertTrue(_looks_like_header(fila.split(",")))
        objetos = csv_objects(f"{fila}\n1,2,3,4,5,6\n")
        self.assertEqual(fila.split(","), columnas(objetos))
        self.assertNotIn("[REDACTADO-PRIVACIDAD]", columnas(objetos))

    def test_un_identificador_real_en_la_primera_fila_veta_el_encabezado(self) -> None:
        """La contrapartida: si la primera fila trae algo que sí identifica a
        una persona, no es un encabezado y no se persiste."""
        objetos = csv_objects("7,juan.perez@example.com,34\n8,ana.lopez@example.com,29\n")
        self.assertTrue(all(nombre.startswith("COLUMNA-") for nombre in columnas(objetos)))
        objetos = csv_objects("VAPM920101HDFRRL03,GOMA850713MDFNRN08,edad\n1,2,3\n")
        self.assertIn("encabezado=NO-DETERMINADO", tabla(objetos)["definition"])

    def test_primera_fila_de_datos_numericos_no_es_encabezado(self) -> None:
        objetos = csv_objects("1,2,3,4\n5,6,7,8\n")
        self.assertEqual(["COLUMNA-1", "COLUMNA-2", "COLUMNA-3", "COLUMNA-4"], columnas(objetos))
        definicion = tabla(objetos)["definition"]
        self.assertIn("encabezado=NO-DETERMINADO", definicion)
        self.assertIn("filas=2", definicion)

    def test_titulo_libre_en_la_primera_fila_no_es_encabezado(self) -> None:
        """Caso real: `0_indice_tablas_enif2024.csv` abre con el nombre de la
        encuesta y una celda vacía."""
        objetos = csv_objects("Encuesta Nacional de Inclusión Finanzas 2024,\nTHOGAR,hogar\n")
        self.assertIn("encabezado=NO-DETERMINADO", tabla(objetos)["definition"])

    def test_nombres_repetidos_no_son_encabezado(self) -> None:
        self.assertFalse(_looks_like_header(["sexo", "edad", "sexo"]))

    def test_diccionario_se_detecta_por_estructura_y_no_por_nombre_de_archivo(self) -> None:
        """El detector viejo exigía que el NOMBRE del archivo dijera
        `diccionario|codebook|catalogo`. Con eso no disparó nunca. La evidencia
        que manda es que la fila traiga a la vez una columna de variable y una
        de etiqueta."""
        objetos = csv_objects(
            "variable,etiqueta\nP6_38,Quien debe hacerse cargo de los adultos mayores\n",
            locator="zip!/miembro=1:tabla_sin_nombre_revelador.csv#/contenido-tabla",
        )
        self.assertIn("encabezado=SI-DICCIONARIO", tabla(objetos)["definition"])
        self.assertIn("diccionario_declarado=NO", tabla(objetos)["definition"])
        variables = [o for o in objetos if o["type"] == "VARIABLE-DICCIONARIO"]
        self.assertEqual(1, len(variables))
        self.assertEqual("P6_38", variables[0]["name"])
        self.assertIn("adultos mayores", variables[0]["label"])


class EncabezadoXlsxTests(unittest.TestCase):
    def _libro(self, filas: list[list], titulo: str = "TVIVIENDA") -> Path:
        libro = openpyxl.Workbook()
        hoja = libro.active
        hoja.title = titulo
        for fila in filas:
            hoja.append(fila)
        destino = Path(self.enclosing) / "libro.xlsx"
        libro.save(destino)
        return destino

    def setUp(self) -> None:
        import tempfile
        self._tmp = tempfile.TemporaryDirectory()
        self.enclosing = self._tmp.name

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_encabezado_en_fila_1_se_conserva(self) -> None:
        ruta = self._libro([["LLAVEVIV", "P1_1", "P1_2"], [1, 2, 3]])
        objetos = _xlsx_objects(ruta)
        self.assertEqual(["LLAVEVIV", "P1_1", "P1_2"], columnas(objetos))

    def test_bloque_de_titulo_de_inegi_no_deja_columnas_fantasma(self) -> None:
        """Caso real medido: en `enasic_2022_fd.xlsx` la fila 1 está VACÍA y el
        encabezado real vive en la 15. El parser sólo miraba la fila 1, así que
        las 42 columnas de ENASIC son artefactos de una fila vacía. Una fila
        vacía no produce columnas."""
        ruta = self._libro([
            [None, None, None, None, None, None, None],
            [None, "Encuesta Nacional sobre Salud y Cuidados", None, None, None, None, None],
            [None, "ESTRUCTURA DEL ARCHIVO", None, None, None, None, None],
            [None, None, None, None, None, None, None],
            [None, "Pregunta", "Nemónico", "Tipo", "Tamaño", "Códigos Válidos", "Concepto"],
            [None, "1.1 ¿De qué material es la mayor parte del piso?", "P1_1", "Alfanumérico", "1", "1", "Tierra"],
        ])
        objetos = _xlsx_objects(ruta)
        self.assertEqual([], [c for c in columnas(objetos) if c.startswith("COLUMNA-")])

    def test_diccionario_fd_de_inegi_entrega_reactivo_y_categorias(self) -> None:
        """Lo que ese mismo archivo contiene y el índice E2 no conservó: el
        texto del reactivo, el nombre de variable y las categorías."""
        ruta = self._libro([
            [None, None, None, None, None, None, None],
            [None, "ESTRUCTURA DEL ARCHIVO", None, None, None, None, None],
            [None, "Pregunta", "Nemónico", "Tipo", "Tamaño", "Códigos Válidos", "Concepto"],
            [None, "1.1 ¿De qué material es la mayor parte del piso?", "P1_1", "Alfanumérico", "1", "1", "Tierra"],
            [None, "1.2 ¿Cuántos cuartos tiene esta vivienda?", "P1_2", "Numérico", "2", "01 - 20", "Número de cuartos"],
        ])
        objetos = _xlsx_objects(ruta)
        variables = [o for o in objetos if o["type"].startswith("VARIABLE-DICCIONARIO")]
        self.assertEqual({"P1_1", "P1_2"}, {o["name"] for o in variables})
        primera = next(o for o in variables if o["name"] == "P1_1")
        self.assertIn("material", primera["label"].lower())
        self.assertIn("Tierra", primera.get("categories", []))


if __name__ == "__main__":
    unittest.main()
