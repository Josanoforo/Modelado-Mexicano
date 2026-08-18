"""El eje DURABLE del predicado de exención: escritor y validador, una sola regla.

Por qué existe este archivo, medido y no supuesto. El gate material de BARRIDO-2
estuvo VERDE dos veces —`ledger-v2` y `ledger-v5`, 672 de 672 terminales— con un
escritor y un validador igual de romos: los dos redactaban el metadato de máquina.
El commit `abb978a` (17/ago/2026 22:33) hizo al escritor deliberadamente más fino
—conservar `codigo_hex` y `crc` ES el entregable del bloque 2— aplicando
`safe_text_compuesto` a `definition`, `categories` y `value_labels`, y no tocó una
sola línea del bloque PII del validador. Desde entonces el gate no volvió a cerrar:
`ledger-v6` 273 de 672, `ledger-v7` 296 de 672, con 13 953 `E2_PII_NO_REDACTADA`
sobre 376 expedientes y **cero PII real**. `7ef2c0f` unificó el eje ESTRUCTURAL
(`nombre`/`hoja`/`tabla`) con `exento_estructural()`, que es otro eje, y por eso no
lo destrabó.

Es la tercera instancia de la misma familia de defecto. Estas pruebas fijan las dos
propiedades que impiden la cuarta: que el validador no tenga regla propia, y que la
exención del escritor distinga conservar-verbatim de eximir-por-forma.
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from tools.curador_registro.barrido2_material import (  # noqa: E402
    CAMPOS_ESQUEMA,
    _durable_row,
    CAMPOS_MAQUINA,
    MaterialDriftError,
    PII_PATTERNS,
    _campos_esquema,
    _campos_maquina,
    activa_pii_compuesto,
    safe_text_compuesto,
)

REDACTADO = "[REDACTADO-PRIVACIDAD]"


class UnSoloPredicado(unittest.TestCase):
    """El validador no puede tener una regla propia: usa la del escritor."""

    def test_el_validador_acepta_todo_lo_que_el_escritor_escribe(self) -> None:
        """Ésta es LA propiedad. Si alguna vez falla, los dos lados volvieron a
        divergir y el gate rechazará expedientes recién hechos, que es
        exactamente lo que costó tres reejecuciones."""
        entradas = [
            "crc=2719796586;zip_slip=NO;cifrado=NO",
            "codigo_hex=0000000000c05840;label=Sí",
            "codigo_hex=3120202020202020;label=Localidades con 100 000 y más habitantes",
            "label=RAÚL GONZÁLEZ GARCÍA",
            "telefono_contacto=8711234567",
            "variables=EST_DIS;categorias=4",
            "bytes=14440942;comprimidos=1760580;crc=1414568376;zip_slip=SI",
            "lineas_texto=68;texto_extraible=SI;cifrado=NO",
            "8711234567",
            "prosa libre sin ningun igual",
            "",
        ]
        for entrada in entradas:
            with self.subTest(entrada=entrada):
                escrito, _ = safe_text_compuesto(entrada)
                self.assertFalse(
                    activa_pii_compuesto(escrito),
                    f"el validador rechaza lo que el escritor acaba de escribir: {escrito!r}",
                )

    def test_activa_pii_compuesto_es_literalmente_la_bandera_del_escritor(self) -> None:
        """No una copia equivalente: la misma función. Una copia se
        desincroniza; una llamada no puede."""
        for entrada in ["crc=123;label=x", "label=RAÚL GONZÁLEZ GARCÍA", "8711234567"]:
            with self.subTest(entrada=entrada):
                self.assertEqual(activa_pii_compuesto(entrada), safe_text_compuesto(entrada)[1])


class ControlesDelEncargo(unittest.TestCase):
    """Los seis controles obligatorios del encargo, verbatim."""

    def test_P1_metadato_de_miembro_zip_sobrevive_entero(self) -> None:
        entrada = "crc=2719796586;zip_slip=NO"
        self.assertEqual(safe_text_compuesto(entrada), (entrada, False))

    def test_P2_value_label_de_sav_sobrevive_entero(self) -> None:
        entrada = "codigo_hex=0000000000c05840;label=Sí"
        self.assertEqual(safe_text_compuesto(entrada), (entrada, False))

    def test_N1_un_nombre_en_label_se_redacta_aunque_lleve_prefijo_de_clave(self) -> None:
        """El precedente Veracruz. Tres de los once patrones están anclados
        (`^…$`) y el prefijo `label=` les rompía el ancla, así que sobre el
        segmento entero NUNCA disparaban. Barrido el índice v7 completo
        (1 833 802 registros), el hueco existía y nunca llegó a ejercerse —
        cero `label=` con forma de nombre lo cruzaron. Se cierra igual."""
        salida, red = safe_text_compuesto("label=RAÚL GONZÁLEZ GARCÍA")
        self.assertTrue(red)
        self.assertEqual(salida, f"label={REDACTADO}")

    def test_N2_se_redacta_el_valor_y_se_conserva_la_llave(self) -> None:
        salida, red = safe_text_compuesto("codigo_hex=abc;label=555 812 4930")
        self.assertTrue(red)
        self.assertEqual(salida, f"codigo_hex=abc;label={REDACTADO}")

    def test_N3_un_telefono_suelto_sin_llave_se_redacta(self) -> None:
        self.assertEqual(safe_text_compuesto("8711234567"), (REDACTADO, True))

    def test_N4_la_lista_es_cerrada_una_llave_no_declarada_no_exime(self) -> None:
        salida, red = safe_text_compuesto("telefono_contacto=8711234567")
        self.assertTrue(red)
        self.assertEqual(salida, f"telefono_contacto={REDACTADO}")


class MaquinaNoEsEsquema(unittest.TestCase):
    """Las dos clases del contrato no son intercambiables, y la diferencia es
    toda la seguridad del mecanismo."""

    def test_campo_de_esquema_se_exime_por_forma_no_verbatim(self) -> None:
        """`variables` lleva un nombre de variable SPSS. Con forma de código
        sobrevive; con forma de nombre de persona NO — porque en los `.dta`
        electorales de Veracruz cada candidato es una columna, así que un
        nombre de variable **puede** ser el nombre de alguien."""
        self.assertIn("variables", CAMPOS_ESQUEMA)
        self.assertNotIn("variables", CAMPOS_MAQUINA)
        entero = "variables=EST_DIS;categorias=4"
        self.assertEqual(safe_text_compuesto(entero), (entero, False))
        salida, red = safe_text_compuesto("variables=RAÚL GONZÁLEZ GARCÍA")
        self.assertTrue(red)
        self.assertEqual(salida, f"variables={REDACTADO}")

    def test_campo_de_maquina_si_se_conserva_verbatim(self) -> None:
        """La contraparte: `crc` es un número calculado por `zipfile`, no puede
        contener a una persona, y se conserva tal cual."""
        self.assertIn("crc", CAMPOS_MAQUINA)
        entrada = "crc=3266880665"
        self.assertEqual(safe_text_compuesto(entrada), (entrada, False))

    def test_la_llave_se_evalua_y_por_eso_no_es_una_via_abierta(self) -> None:
        """88 de las 122 llaves medidas en el índice real son prosa humana
        partida por un `=` que venía dentro del propio texto. Una llave sin
        revisar sería una vía para publicar lo que se quiso redactar."""
        salida, red = safe_text_compuesto("RAÚL GONZÁLEZ GARCÍA=1")
        self.assertTrue(red)
        self.assertEqual(salida, REDACTADO)

    def test_zip_slip_sobrevive_como_llave_pese_a_parecer_dos_palabras(self) -> None:
        """`zip_slip` activa el patrón de nombre en minúsculas (`zip`+`_`+`slip`).
        Sin la exención por forma sobre la llave se perdería la declaración de
        seguridad de cada miembro ZIP — la misma que hoy permite ver los 5
        miembros con `zip_slip=SI` que tiene el corpus."""
        self.assertTrue(any(p.search("zip_slip") for p in PII_PATTERNS))
        entrada = "zip_slip=SI"
        self.assertEqual(safe_text_compuesto(entrada), (entrada, False))


class NoRompeLoQueNoDebeTocar(unittest.TestCase):
    """Tres defectos que la revisión adversarial encontró en la primera versión
    de este arreglo, reproducidos y cerrados. Los tres se descubrieron con la
    reejecución ya en vuelo y costaron pararla a los 23 minutos; se paga una vez."""

    def test_un_segmento_no_redactado_sale_verbatim(self) -> None:
        """Reconstruir desde la clave recortada mutilaba el texto del documento
        fuente: `ENT = 15` salía `ENT=15`. Y como sólo se parte por el PRIMER
        `=`, la mutilación era además inconsistente dentro de la misma cadena."""
        for entrada in ["ENT = 15", "(5.6 = 3 Y 5.8 = 7)", "Sexo (Hombre = 1)",
                        "tipo=NUMERICO;formato_impresion=0x50802"]:
            with self.subTest(entrada=entrada):
                self.assertEqual(safe_text_compuesto(entrada), (entrada, False))

    def test_una_cadena_con_igual_no_se_convierte_en_una_sin_igual(self) -> None:
        """`=calle;=5` salía `calle;5`, que al revalidarse cae por la rama plana
        de `safe_text_compuesto` y activa el patrón de domicilio — o sea, el gate
        rechazaba un expediente recién escrito. Es la misma clase de defecto que
        este acto cierra, reintroducida por comodidad de formato."""
        entrada = "=calle;=5"
        escrito, red = safe_text_compuesto(entrada)
        self.assertEqual(escrito, entrada)
        self.assertFalse(red)
        self.assertFalse(activa_pii_compuesto(escrito))

    def test_la_llave_de_maquina_no_exime_un_valor_que_no_es_de_maquina(self) -> None:
        """La exención la controlaba el DATO, no la máquina: bastaba con que un
        valor externo llegara conteniendo `;crc=<nombre>` para fabricar un
        segmento con llave declarada que el escritor conservaba entero y el
        validador ya no revisaba. Se cierra por FORMA del valor, que cierra la
        clase entera y no un emisor."""
        escrito, red = safe_text_compuesto("tipo=NUMERICO;crc=Ana Maria Lopez")
        self.assertTrue(red)
        self.assertEqual(escrito, f"tipo=NUMERICO;crc={REDACTADO}")
        self.assertFalse(activa_pii_compuesto(escrito))
        # y la contraparte sigue viva: un crc de verdad no se toca
        self.assertEqual(safe_text_compuesto("crc=2719796586"), ("crc=2719796586", False))


class TipoDeObjetoNoEsProsa(unittest.TestCase):
    """`objeto_tipo` es el vocabulario que el propio módulo emite, no texto
    extraído. Pasarlo por el detector de nombres es el mismo error de categoría
    que este acto corrige en los campos compuestos, y su efecto estaba medido:
    `PII_PATTERNS[8]` muerde todo tipo con guion, así que 1 650 224 de 1 833 802
    filas durables (89.99 %) salían con el tipo redactado. El daño no era sólo de
    lectura — `write_barrido2_material.py` agrupa por esa clave, o sea que clases
    distintas se fusionaban en una sola fila publicada."""

    BASE = {
        "record_id": "r", "representacion_id": "REP-x", "record_sha256": "a",
        "batch_id": "b", "batch_sha256": "c", "payload_id": "p", "sha256": "s",
        "objeto_logico_id": "o", "localizador": "pagina=1", "nombre": "NO-APLICA",
        "etiqueta": "NO-APLICA", "texto_reactivo": "NO-APLICA",
        "definicion": "lineas_texto=1", "frontera_inspeccion": "todas las paginas",
        "estado": "E2-COMPLETO", "privacidad": "DEPURADO", "fecha": "2026-08-18",
    }

    def _tipo(self, valor: str) -> str:
        fila = dict(self.BASE)
        fila["objeto_tipo"] = valor
        return _durable_row(fila)["objeto_tipo"]

    def test_el_vocabulario_real_sobrevive_entero(self) -> None:
        """Los 52 valores distintos medidos en el índice v7. Incluye los nombres
        de etiqueta HTML en mayúsculas que el parser emite tal cual del
        documento (`TH`, `OPTION`, `H1`), que no son vocabulario cerrado y por eso
        la exención va por FORMA y no por lista."""
        for tipo in ["MIEMBRO-ZIP", "SECCION-PDF", "VALUE-LABEL-COLLECTION-SAV",
                     "VARIABLE-DICCIONARIO-XLSX", "EXCEPCION-MIEMBRO-ZIP",
                     "FORMATO-NO-SOPORTADO", "COLUMNA", "TABLA", "TH", "H1",
                     "OPTION", "LEGEND", "CONTROL-CHECKBOX", "PARRAFO-DOCX"]:
            with self.subTest(tipo=tipo):
                self.assertEqual(self._tipo(tipo), tipo)

    def test_un_tipo_con_forma_de_nombre_se_sigue_redactando(self) -> None:
        """La exención es por forma, no por confiar en el nombre del campo."""
        for impostor in ["RAÚL GONZÁLEZ GARCÍA", "JUAN PEREZ", "Ana Maria"]:
            with self.subTest(impostor=impostor):
                self.assertEqual(self._tipo(impostor), REDACTADO)

    def test_no_ensancha_el_eje_estructural(self) -> None:
        """El predicado del tipo vive aparte a propósito: ampliar
        `exento_estructural()` para arreglar un cuarto campo habría relajado
        `nombre`/`hoja`/`tabla` de paso, que es justo el error que este acto
        cierra. `MIEMBRO-ZIP` no es código para el eje estructural."""
        from tools.curador_registro.barrido2_material import exento_estructural
        self.assertFalse(exento_estructural("MIEMBRO-ZIP"))


class ContratoDurable(unittest.TestCase):
    """El contrato vive en un TSV, falla cerrado, y nunca exime texto humano."""

    def test_ninguna_de_las_dos_clases_puede_eximir_label(self) -> None:
        self.assertNotIn("label", CAMPOS_MAQUINA)
        self.assertNotIn("label", CAMPOS_ESQUEMA)

    def test_un_contrato_que_declare_label_como_esquema_revienta_al_leerse(self) -> None:
        with tempfile.TemporaryDirectory() as directorio:
            malo = Path(directorio) / "campos.tsv"
            malo.write_text(
                "campo\tclase\ncrc\tMAQUINA\nlabel\tESQUEMA\n", encoding="utf-8"
            )
            with mock.patch(
                "tools.curador_registro.barrido2_material.CAMPOS_MAQUINA_TSV", malo
            ):
                with self.assertRaises(MaterialDriftError) as ctx:
                    _campos_esquema()
        self.assertIn("CONTRATO_CAMPOS_MAQUINA_EXIME_TEXTO_HUMANO", str(ctx.exception))

    def test_un_contrato_sin_la_columna_clase_se_lee_como_maquina(self) -> None:
        """Retrocompatible a propósito: así nació el archivo, y un contrato
        viejo debe leerse sin reventar y sin cambiar de significado."""
        with tempfile.TemporaryDirectory() as directorio:
            viejo = Path(directorio) / "campos.tsv"
            viejo.write_text("campo\tdescripcion\ncrc\tbueno\n", encoding="utf-8")
            with mock.patch(
                "tools.curador_registro.barrido2_material.CAMPOS_MAQUINA_TSV", viejo
            ):
                self.assertEqual(_campos_maquina(), frozenset({"crc"}))
                self.assertEqual(_campos_esquema(), frozenset())


if __name__ == "__main__":
    unittest.main()
