"""Dos defectos de la misma familia: tratar metadato de máquina como dato de
persona.

`safe_text_compuesto` (ARREGLO 1) corrige el lado de las cadenas `k=v;k=v`: el
detector de PII redactaba por FORMA (longitud de dígitos, forma de nombre) sin
distinguir un identificador de máquina de un dato de informante. La exención
ahora va por CAMPO, declarada en un producto durable
(`data/curacion-universo/campos-maquina-barrido2.tsv`) y no en código, y nunca
alcanza a `label`, que es texto humano. Medido en el corpus real: se perdían
132 396 de 135 262 value labels de SAV (97.9 %) porque `codigo_hex` es hex de
16 dígitos y disparaba el patrón de identificador de 11 a 18 dígitos, y el
71.6 % de los metadatos de miembro ZIP —incluida la garantía `zip_slip`— por
la misma razón.

`_pdf_objects` (ARREGLO 2) corrige el lado del PDF: `Encrypted: yes` dejaba el
archivo entero en `PermissionError` sin intentar nada. La mayoría de los PDF
oficiales mexicanos traen la bandera puesta y la contraseña de usuario vacía,
así que ahora se sondea con `pdftotext -f 1 -l 1` antes de descartar; sólo si
el sondeo de verdad falla se declara `PDF_CIFRADO`, y con la salida cruda del
intento. Medido: 77 de 78 PDF que antes daban cero objetos abren ahora.

Estas pruebas son sintéticas a propósito: el corpus vive fuera de git y una
prueba que dependa de él no corre en otra caja. Para el PDF sin cifrar se usa
un generador mínimo propio (sin librerías externas) porque `pdfinfo` y
`pdftotext` sí están instalados en esta caja y demuestran el comportamiento
real; para los dos casos cifrados no hay en esta caja ninguna herramienta que
produzca un PDF cifrado de verdad (no hay `qpdf` ni `pdftk`, y no están
instalados `pypdf`/`PyPDF2`/`reportlab`), así que esos dos casos se fijan con
`mock.patch` sobre `subprocess.run`, siguiendo el precedente de
`test_barrido2_material.py`.
"""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools.curador_registro.barrido2_material import (
    CAMPOS_MAQUINA,
    MaterialDriftError,
    _campos_maquina,
    _pdf_objects,
    safe_text_compuesto,
)


def _pdf_sin_cifrar(path: Path, pages: int = 1) -> None:
    """PDF pequeño y válido, sin depender de librerías externas.

    Copia local del generador de `test_barrido2_material.py`: este archivo no
    debe importar ni modificar ese módulo, así que la construcción se repite
    aquí en vez de compartirse.
    """
    font_object = 3 + pages * 2
    objects: list[bytes] = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        (
            "<< /Type /Pages /Kids ["
            + " ".join(f"{3 + index * 2} 0 R" for index in range(pages))
            + f"] /Count {pages} >>"
        ).encode(),
    ]
    for index in range(pages):
        page_object = 3 + index * 2
        stream_object = page_object + 1
        objects.append(
            (
                f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
                f"/Resources << /Font << /F1 {font_object} 0 R >> >> "
                f"/Contents {stream_object} 0 R >>"
            ).encode()
        )
        content = f"BT /F1 12 Tf 72 720 Td (PAGINA {index + 1}) Tj ET".encode()
        objects.append(
            b"<< /Length " + str(len(content)).encode() + b" >>\nstream\n" + content + b"\nendstream"
        )
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    payload = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for number, body in enumerate(objects, 1):
        offsets.append(len(payload))
        payload.extend(f"{number} 0 obj\n".encode() + body + b"\nendobj\n")
    xref = len(payload)
    payload.extend(f"xref\n0 {len(objects) + 1}\n".encode())
    payload.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        payload.extend(f"{offset:010d} 00000 n \n".encode())
    payload.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    )
    path.write_bytes(payload)


class SafeTextCompuestoTests(unittest.TestCase):
    """Redacción por campo declarado, no por forma del valor."""

    def test_codigo_hex_sobrevive_intacto_pese_a_dieciseis_digitos(self) -> None:
        """El patrón de identificador de 11 a 18 dígitos disparaba con los 16
        dígitos del hex y se perdían 132 396 de 135 262 value labels de SAV
        (97.9 %). `codigo_hex` está exento por campo, no por longitud."""
        original = "codigo_hex=0000000000000000;label=Sí"
        texto, redactado = safe_text_compuesto(original)
        self.assertEqual(original, texto)
        self.assertFalse(redactado)

    def test_metadatos_zip_sobreviven_incluyendo_la_garantia_zip_slip(self) -> None:
        """Antes se perdía el 71.6 % de los metadatos de miembro ZIP,
        incluida la declaración `zip_slip` por miembro, que es una garantía
        de seguridad y no un adorno."""
        original = "bytes=1404772;comprimidos=1398210;crc=3266880665;zip_slip=NO;cifrado=NO"
        texto, redactado = safe_text_compuesto(original)
        self.assertEqual(original, texto)
        self.assertFalse(redactado)
        self.assertIn("zip_slip=NO", texto)

    def test_control_negativo_label_con_nombre_real_se_redacta_pese_a_codigo_hex_exento(self) -> None:
        """El caso más importante: la privacidad manda sobre la cobertura.
        `codigo_hex` exime por campo, pero `label` es texto humano y nunca
        puede estar en la lista de exención — aquí sí puede aparecer una
        persona, y debe seguir redactándose segmento por segmento."""
        texto, redactado = safe_text_compuesto(
            "codigo_hex=0000000000000000;label=Juan Pérez García"
        )
        self.assertEqual(
            "codigo_hex=0000000000000000;label=[REDACTADO-PRIVACIDAD]", texto
        )
        self.assertTrue(redactado)

    def test_correo_en_campo_no_exento_se_sigue_redactando(self) -> None:
        """Un identificador duro real en un campo que NO está en la lista de
        máquina no se salva por estar junto a uno que sí lo está."""
        texto, redactado = safe_text_compuesto(
            "contacto=juan.perez@example.com;bytes=1404772"
        )
        self.assertEqual("contacto=[REDACTADO-PRIVACIDAD];bytes=1404772", texto)
        self.assertTrue(redactado)

    def test_curp_sintetica_en_campo_no_exento_se_sigue_redactando(self) -> None:
        """Misma garantía con un identificador de forma distinta (CURP en vez
        de correo), para no fijar el contrato a un solo patrón."""
        texto, redactado = safe_text_compuesto(
            "titular=VAPM920101HDFRRL03;crc=3266880665"
        )
        self.assertEqual("titular=[REDACTADO-PRIVACIDAD];crc=3266880665", texto)
        self.assertTrue(redactado)

    def test_cadena_sin_forma_compuesta_cae_a_safe_text_simple(self) -> None:
        """Sin `=` no hay campo que exentar; se comporta como `safe_text`."""
        texto, redactado = safe_text_compuesto("Juan Pérez García")
        self.assertEqual("[REDACTADO-PRIVACIDAD]", texto)
        self.assertTrue(redactado)


class CamposMaquinaContratoTests(unittest.TestCase):
    """El contrato de exención vive en un TSV durable, no en código."""

    def test_los_nueve_campos_medidos_estan_declarados_y_label_nunca_lo_esta(self) -> None:
        """Fija la lista medida en el corpus real: éstos son los campos que
        hoy pierden cobertura si el detector no los exime por campo, y
        `label` —texto humano— nunca puede estar entre ellos."""
        esperados = {
            "codigo_hex", "crc", "bytes", "comprimidos", "formato_impresion",
            "formato_escritura", "filas", "columnas", "lineas_texto",
        }
        self.assertTrue(esperados.issubset(CAMPOS_MAQUINA))
        self.assertNotIn("label", CAMPOS_MAQUINA)

    def test_campos_maquina_lanza_material_drift_error_si_el_tsv_no_existe(self) -> None:
        """Fail-closed: sin el producto durable, no hay exención posible."""
        con_ruta_ausente = Path(tempfile.mkdtemp()) / "no-existe" / "campos-maquina-barrido2.tsv"
        with mock.patch(
            "tools.curador_registro.barrido2_material.CAMPOS_MAQUINA_TSV",
            con_ruta_ausente,
        ):
            with self.assertRaises(MaterialDriftError) as contexto:
                _campos_maquina()
        self.assertIn("CONTRATO_CAMPOS_MAQUINA_AUSENTE", str(contexto.exception))

    def test_campos_maquina_rechaza_un_contrato_que_exima_label(self) -> None:
        """`label` es exactamente el campo donde aparecieron 44 nombres
        reales de personas en el corpus (candidatos electorales de los .dta
        de Veracruz). Un contrato que lo eximiera relajaría la privacidad en
        silencio; debe reventar al leerse, no al usarse."""
        with tempfile.TemporaryDirectory() as directorio:
            tsv_malo = Path(directorio) / "campos-maquina-barrido2.tsv"
            tsv_malo.write_text(
                "campo\tdescripcion\ncrc\tbueno\nlabel\tmalo\n", encoding="utf-8"
            )
            with mock.patch(
                "tools.curador_registro.barrido2_material.CAMPOS_MAQUINA_TSV",
                tsv_malo,
            ):
                with self.assertRaises(MaterialDriftError) as contexto:
                    _campos_maquina()
        self.assertIn("CONTRATO_CAMPOS_MAQUINA_EXIME_TEXTO_HUMANO", str(contexto.exception))


class PdfCifradoTests(unittest.TestCase):
    """`Encrypted: yes` deja de ser descarte automático y pasa a ser intento.

    `pdfinfo` y `pdftotext` (poppler-utils) sí están instalados en esta caja,
    pero no hay ninguna herramienta para PRODUCIR un PDF cifrado de verdad
    (`qpdf`, `pdftk` ausentes; `pypdf`, `PyPDF2` y `reportlab` no instalados).
    Los dos casos con `Encrypted: yes` se fijan mockeando `subprocess.run`
    para simular el `pdfinfo`/`pdftotext` reales; el caso sin cifrar corre
    contra los binarios reales sobre un PDF sintético.
    """

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.pdf_path = Path(self.tmp.name) / "cuestionario_cifrado.pdf"
        # El contenido es irrelevante en los dos primeros casos: subprocess.run
        # está mockeado y nunca lee el archivo de verdad. Sólo debe existir
        # porque _pdf_objects pasa la ruta como argumento de comando.
        self.pdf_path.write_bytes(b"%PDF-1.4\n%contenido-irrelevante-bajo-mock\n")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    @staticmethod
    def _subprocess_run_simulado(
        *,
        pdfinfo_stdout: str,
        pdftotext_stdout: bytes,
        pdftotext_returncode: int = 0,
        pdftotext_stderr: bytes = b"",
    ):
        def _run(cmd, **kwargs):
            if cmd[0] == "pdfinfo":
                return subprocess.CompletedProcess(cmd, 0, stdout=pdfinfo_stdout, stderr="")
            if cmd[0] == "pdftotext":
                return subprocess.CompletedProcess(
                    cmd, pdftotext_returncode, stdout=pdftotext_stdout, stderr=pdftotext_stderr
                )
            raise AssertionError(f"comando no esperado en el sondeo de PDF: {cmd}")

        return _run

    def test_encrypted_yes_con_sondeo_que_extrae_no_lanza_y_marca_si_extraible(self) -> None:
        """Caso (a): la mayoría de los PDF oficiales mexicanos traen la
        bandera puesta y contraseña de usuario vacía. `_pdf_objects` ya no
        debe lanzar, y cada página queda marcada `cifrado=SI-EXTRAIBLE`."""
        corrida = self._subprocess_run_simulado(
            pdfinfo_stdout="Pages: 1\nEncrypted: yes (print:yes copy:no)\n",
            pdftotext_stdout=b"Texto extraido de la pagina uno.\n",
        )
        with mock.patch(
            "tools.curador_registro.barrido2_material.subprocess.run", side_effect=corrida
        ):
            objetos = _pdf_objects(self.pdf_path)
        paginas = [o for o in objetos if o["type"] == "PAGINA-PDF"]
        self.assertEqual(1, len(paginas))
        self.assertIn("cifrado=SI-EXTRAIBLE", paginas[0]["definition"])

    def test_encrypted_yes_con_sondeo_vacio_lanza_permission_error_con_diagnostico(self) -> None:
        """Caso (b): el único de los 78 PDF medidos que sigue sin abrir
        (`enut2002_fd.pdf`) es exactamente este — el sondeo falla de verdad.
        El mensaje debe traer `PDF_CIFRADO`, `rc=` y `bytes_texto=`, no un
        `PermissionError("PDF_CIFRADO")` desnudo."""
        corrida = self._subprocess_run_simulado(
            pdfinfo_stdout="Pages: 3\nEncrypted: yes (print:no copy:no)\n",
            pdftotext_stdout=b"",
            pdftotext_returncode=1,
            pdftotext_stderr=b"Command Line Error: Incorrect password\n",
        )
        with mock.patch(
            "tools.curador_registro.barrido2_material.subprocess.run", side_effect=corrida
        ):
            with self.assertRaises(PermissionError) as contexto:
                _pdf_objects(self.pdf_path)
        mensaje = str(contexto.exception)
        self.assertIn("PDF_CIFRADO", mensaje)
        self.assertIn("rc=", mensaje)
        self.assertIn("bytes_texto=", mensaje)

    def test_encrypted_yes_con_sondeo_vacio_por_texto_en_blanco_tambien_lanza(self) -> None:
        """Variante del caso (b): `pdftotext` puede salir con rc=0 y no
        obstante no extraer nada (texto en blanco). El sondeo exige texto no
        vacío, no sólo un código de salida limpio."""
        corrida = self._subprocess_run_simulado(
            pdfinfo_stdout="Pages: 1\nEncrypted: yes (print:no copy:no)\n",
            pdftotext_stdout=b"   \n\x0c",
            pdftotext_returncode=0,
        )
        with mock.patch(
            "tools.curador_registro.barrido2_material.subprocess.run", side_effect=corrida
        ):
            with self.assertRaises(PermissionError) as contexto:
                _pdf_objects(self.pdf_path)
        mensaje = str(contexto.exception)
        self.assertIn("PDF_CIFRADO", mensaje)
        self.assertIn("bytes_texto=", mensaje)

    def test_pdf_sin_cifrar_declara_cifrado_no(self) -> None:
        """Caso (c), control: contra los binarios reales de poppler, un PDF
        genuinamente sin cifrar declara `cifrado=NO` en cada página."""
        ruta = Path(self.tmp.name) / "cuestionario_abierto.pdf"
        _pdf_sin_cifrar(ruta, pages=1)
        objetos = _pdf_objects(ruta)
        paginas = [o for o in objetos if o["type"] == "PAGINA-PDF"]
        self.assertEqual(1, len(paginas))
        self.assertIn("cifrado=NO", paginas[0]["definition"])


if __name__ == "__main__":
    unittest.main()
