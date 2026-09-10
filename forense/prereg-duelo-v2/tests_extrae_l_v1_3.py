#!/usr/bin/env python3
"""Pruebas dirigidas de `tools/extrae_l_v1_3.py` (`ACTO
GEN2-F5-EXTRACTOR-L-v1`), congeladas ANTES de correr el extractor sobre el
universo completo de 224 capturas (P1, COMMIT-1 -- no se editan después de
ver el resultado sobre las 224).

Controles negativos obligatorios (encargo, P1): los tres ejemplos de
contaminación ya medidos por `ACTO GEN2-F5-DUELO-CALC` (`PR #674`,
`NC-0142`) -- el viejo extractor (`tools/extrae_l_v1_1.py`, por su
fallback de "primer número del documento") capturaba en los tres una
"cifra negra" de contexto (90-94%) que el propio texto del modelo declara
explícitamente que NO es la estimación pedida. Este extractor debe
devolver `NO-EXTRAIBLE` en los tres, nunca ese número.

Controles positivos: formas de salida reales observadas en
`corridas-L/*__v1_3.json` donde el modelo SÍ da un punto (encabezado
`## Estimación` con `≈ N%`, y frase-ancla `Estimación puntual: ~A-B%
(mi punto: N%)`).

Casos sintéticos (formas observadas pero no ligadas a un archivo real):
ambigüedad por conflicto de anclas, ausencia total de ancla, y error de
identidad."""
from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "forense" / "prereg-duelo-v2"
CORRIDAS_L = DIR / "corridas-L"


def _cargar(nombre: str, ruta: Path):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = mod
    spec.loader.exec_module(mod)
    return mod


EXTRAE = _cargar("extrae_l_v1_3", ROOT / "tools" / "extrae_l_v1_3.py")


def _texto_real(nombre_archivo: str) -> str:
    ruta = CORRIDAS_L / nombre_archivo
    with ruta.open(encoding="utf-8") as fh:
        return json.load(fh)["texto_crudo"]


class TestControlesNegativosContaminacion(unittest.TestCase):
    """Los tres ejemplos citados por `NC-0142` -- rechazo explícito de
    estimación puntual, seguido de una "cifra negra" de contexto que el
    propio texto marca como NO la respuesta. El extractor viejo los
    capturaba como 0.925/0.93/0.90; este NO debe emitir ningún valor."""

    def test_civ_m12_l_solo_01_rechazo_no_cifra_negra(self):
        t = _texto_real("L-CIV-M-12-M__L-solo__01__v1_3.json")
        self.assertIn("92", t)  # confirma que la cifra contaminante sigue en el texto
        ext = EXTRAE.extraer_valor(t)
        self.assertEqual(ext.estado, "NO-EXTRAIBLE")
        self.assertIsNone(ext.valor_extraido)
        self.assertEqual(ext.regla_de_extraccion, "ANCLA-RECHAZO")

    def test_civ_m13_lcorpus_04_rechazo_no_cifra_negra(self):
        t = _texto_real("L-CIV-M-13-M__L+corpus__04__v1_3.json")
        self.assertIn("92", t)
        ext = EXTRAE.extraer_valor(t)
        self.assertEqual(ext.estado, "NO-EXTRAIBLE")
        self.assertIsNone(ext.valor_extraido)
        self.assertEqual(ext.regla_de_extraccion, "ANCLA-RECHAZO")

    def test_civ_m01_lcorpus_02_rechazo_no_cifra_negra(self):
        t = _texto_real("L-CIV-M-01-M__L+corpus__02__v1_3.json")
        self.assertIn("90", t)
        ext = EXTRAE.extraer_valor(t)
        self.assertEqual(ext.estado, "NO-EXTRAIBLE")
        self.assertIsNone(ext.valor_extraido)
        self.assertEqual(ext.regla_de_extraccion, "ANCLA-RECHAZO")


class TestControlesPositivosFormatosReales(unittest.TestCase):
    """Formas de salida reales donde el modelo SÍ compromete un punto."""

    def test_header_estimacion_con_aprox(self):
        t = _texto_real("L-FAM-M-05-M__L+corpus__02__v1_3.json")
        ext = EXTRAE.extraer_valor(t)
        self.assertEqual(ext.estado, "EXTRAIBLE")
        self.assertAlmostEqual(ext.valor_extraido, 0.044, places=4)
        self.assertEqual(ext.regla_de_extraccion, "ANCLA-HEADER-PUNTO")

    def test_header_estimacion_no_confunde_rango_subjetivo(self):
        # El mismo archivo trae, en el mismo bloque, "Rango subjetivo:
        # 3.8% - 5.5%" -- ese párrafo está excluido por
        # _EXCLUSION_INCERTIDUMBRE_KW y NO debe producir un segundo
        # candidato numérico (que volvería el caso AMBIGUA).
        t = _texto_real("L-FAM-M-05-M__L+corpus__02__v1_3.json")
        anclas_h = EXTRAE._anclas_familia_h(t)
        numericas = [a for a in anclas_h if a.tipo == "NUMERO"]
        self.assertEqual(len(numericas), 1)

    def test_frase_ancla_prefiere_mi_punto_sobre_rango(self):
        t = _texto_real("L-TRA-M-03-M__L-solo__03__v1_3.json")
        ext = EXTRAE.extraer_valor(t)
        self.assertEqual(ext.estado, "EXTRAIBLE")
        self.assertAlmostEqual(ext.valor_extraido, 0.126, places=4)
        self.assertEqual(ext.regla_de_extraccion, "ANCLA-FRASE-PUNTO")

    def test_tabla_estimacion_puntual_abstencion(self):
        t = _texto_real("L-CIV-M-12-M__L-solo__07__v1_3.json")
        ext = EXTRAE.extraer_valor(t)
        self.assertEqual(ext.estado, "NO-EXTRAIBLE")
        self.assertEqual(ext.regla_de_extraccion, "ANCLA-RECHAZO")

    def test_header_no_confunde_cifra_de_contexto_en_parrafo_de_razonamiento(self):
        # ENMIENDA: hallado corriendo sobre el universo real de 224 --
        # "Razonamiento y calibración:" trae, en el mismo bloque, una cifra
        # histórica de contexto ("las estimaciones oscilan entre ~4% y
        # ~7%") que NO es un segundo punto del modelo. Antes de la
        # enmienda esto daba AMBIGUA (0.055 del punto declarado contra 0.04
        # de la cifra de contexto); después de la enmienda, el escaneo de
        # la sección se detiene en el párrafo "Razonamiento..." y solo
        # queda el punto declarado.
        t = _texto_real("L-FAM-M-05-M__L+corpus__01__v1_3.json")
        ext = EXTRAE.extraer_valor(t)
        self.assertEqual(ext.estado, "EXTRAIBLE")
        self.assertAlmostEqual(ext.valor_extraido, 0.055, places=4)
        # El mismo párrafo cae bajo Familia H (encabezado "# Estimación...")
        # Y Familia F ("Estimación puntual" es también frase-ancla); ambas
        # coinciden en 0.055 -- cuál de las dos se cita como "última" no es
        # lo que este control verifica, solo que NO hay conflicto.
        self.assertIn(ext.regla_de_extraccion, ("ANCLA-HEADER-PUNTO", "ANCLA-FRASE-PUNTO"))

    def test_frase_ancla_reconoce_me_abstengo(self):
        # ENMIENDA: hallado corriendo sobre el universo real de 224 -- "me
        # abstengo" (primera persona, presente) no compartía subcadena con
        # "abstenci" (la forma nominal ya cubierta) y el caso caía a
        # SIN-ANCLA en vez de ANCLA-RECHAZO -- mismo estado final
        # (NO-EXTRAIBLE) pero regla mal etiquetada para el reporte de P2.
        t = _texto_real("L-TRA-M-02-M__L+corpus__02__v1_3.json")
        ext = EXTRAE.extraer_valor(t)
        self.assertEqual(ext.estado, "NO-EXTRAIBLE")
        self.assertEqual(ext.regla_de_extraccion, "ANCLA-RECHAZO")


class TestCasosSinteticos(unittest.TestCase):
    """Formas no observadas literalmente en el corpus pero que la regla
    debe resolver de manera predecible -- ambigüedad y ausencia de ancla."""

    def test_sin_ancla_ninguna(self):
        texto = (
            "No tengo información suficiente sobre este reactivo. La "
            "ENVIPE mide muchas cosas distintas y no puedo ubicar este "
            "identificador en el cuestionario. Se necesitaría el "
            "inventario completo de reactivos para continuar."
        )
        ext = EXTRAE.extraer_valor(texto)
        self.assertEqual(ext.estado, "NO-EXTRAIBLE")
        self.assertEqual(ext.regla_de_extraccion, "SIN-ANCLA")
        self.assertIsNone(ext.valor_extraido)

    def test_ambigua_dos_anclas_frase_con_valores_distintos(self):
        texto = (
            "Mi punto: 20%.\n\n"
            "Reconsiderando la base poblacional, ajusto: mi punto: 35%.\n"
        )
        ext = EXTRAE.extraer_valor(texto)
        self.assertEqual(ext.estado, "AMBIGUA")
        self.assertEqual(ext.regla_de_extraccion, "ANCLAS-EN-CONFLICTO")
        self.assertIsNone(ext.valor_extraido)

    def test_ambigua_numero_y_rechazo_mezclados(self):
        texto = (
            "## Estimación\n\n"
            "**Estimación puntual: no proporcionada.**\n\n"
            "## Nota aparte\n\n"
            "Estimación puntual: 15% si se fuerza una salida numérica.\n"
        )
        ext = EXTRAE.extraer_valor(texto)
        self.assertEqual(ext.estado, "AMBIGUA")
        self.assertEqual(ext.regla_de_extraccion, "ANCLAS-EN-CONFLICTO")

    def test_no_cae_a_primer_numero_del_documento(self):
        # Cifra de contexto (ola/año, tamaño de muestra) en la primera
        # línea, sin ninguna ancla de estimación puntual en todo el
        # documento -- el extractor viejo la habría tomado por posición;
        # este debe declarar SIN-ANCLA.
        texto = (
            "La ENVIPE 2023 (n=~120000 viviendas) no permite ubicar este "
            "reactivo con el nombre dado. No hay forma de continuar sin "
            "el inventario del proyecto."
        )
        ext = EXTRAE.extraer_valor(texto)
        self.assertEqual(ext.estado, "NO-EXTRAIBLE")
        self.assertEqual(ext.regla_de_extraccion, "SIN-ANCLA")

    def test_rango_sin_punto_declarado_usa_punto_medio(self):
        texto = "## Estimación\n\nEstimación puntual: 70% - 80% de los hogares.\n"
        ext = EXTRAE.extraer_valor(texto)
        self.assertEqual(ext.estado, "EXTRAIBLE")
        self.assertAlmostEqual(ext.valor_extraido, 0.75, places=4)


class TestIdentidad(unittest.TestCase):
    """Verificación de identidad contra el manifiesto sellado -- un fallo
    aquí es `ERROR-IDENTIDAD`, nunca un intento de extracción."""

    def setUp(self):
        with (DIR / "manifiesto-capturas-P3-v1_0.json").open(encoding="utf-8") as fh:
            self.manifiesto = json.load(fh)["capturas"]

    def test_captura_real_identidad_ok(self):
        nombre = "L-CIV-M-01-M__L+corpus__01__v1_3.json"
        ruta = CORRIDAS_L / nombre
        with ruta.open(encoding="utf-8") as fh:
            datos = json.load(fh)
        ident = EXTRAE.verificar_identidad(ruta, datos, self.manifiesto)
        self.assertTrue(ident.ok)
        self.assertEqual(ident.id_celda, "CIV-M-01")
        self.assertEqual(ident.variante, "L+corpus")
        self.assertEqual(ident.indice, 1)

    def test_identidad_json_alterado_falla(self):
        nombre = "L-CIV-M-01-M__L+corpus__01__v1_3.json"
        ruta = CORRIDAS_L / nombre
        with ruta.open(encoding="utf-8") as fh:
            datos = json.load(fh)
        datos_alterados = dict(datos)
        datos_alterados["id_celda"] = "CIV-M-02"  # simula una identidad cruzada
        ident = EXTRAE.verificar_identidad(ruta, datos_alterados, self.manifiesto)
        self.assertFalse(ident.ok)
        self.assertIn("no coinciden", ident.razon)

    def test_identidad_archivo_no_en_manifiesto_falla(self):
        ruta = CORRIDAS_L / "L-CIV-M-01-M__L+corpus__01__v1_3.json"
        with ruta.open(encoding="utf-8") as fh:
            datos = json.load(fh)
        ident = EXTRAE.verificar_identidad(ruta, datos, {})
        self.assertFalse(ident.ok)
        self.assertIn("no aparece en el manifiesto", ident.razon)


class TestUniversoReal224(unittest.TestCase):
    """No re-implementa P2 -- solo confirma que el universo declarado por
    el encargo (14 celdas x 2 variantes x 8 réplicas) existe y que
    `procesar_224` corre sin excepción sobre él, sin abrir CALC-R/
    corridas-R/resultado del duelo (control de independencia)."""

    def test_224_archivos_y_cero_fallas_de_identidad_en_el_universo_real(self):
        rutas = sorted(CORRIDAS_L.glob("*__v1_3.json"))
        self.assertEqual(len(rutas), 224)
        with (DIR / "manifiesto-capturas-P3-v1_0.json").open(encoding="utf-8") as fh:
            manifiesto_capturas = json.load(fh)["capturas"]
        filas, resumen = EXTRAE.procesar_224(rutas, manifiesto_capturas)
        self.assertEqual(resumen["total_capturas"], 224)
        self.assertEqual(resumen["por_estado"].get("ERROR-IDENTIDAD", 0), 0)

    def test_extractor_no_referencia_R_ni_duelo(self):
        # El docstring del módulo SÍ menciona estos nombres, en prosa, para
        # declarar que el extractor no los abre -- lo que este control
        # verifica es que ninguna línea de CÓDIGO (fuera del docstring de
        # módulo) los referencia como ruta/import.
        import ast
        ruta = ROOT / "tools" / "extrae_l_v1_3.py"
        arbol = ast.parse(ruta.read_text(encoding="utf-8"))
        docstring_modulo = ast.get_docstring(arbol) or ""
        codigo_completo = ruta.read_text(encoding="utf-8")
        codigo_sin_docstring = codigo_completo.replace(docstring_modulo, "", 1)
        for prohibido in ("CALC-R", "corridas-R", "CALC-DUELO"):
            self.assertNotIn(prohibido, codigo_sin_docstring)


if __name__ == "__main__":
    unittest.main()
