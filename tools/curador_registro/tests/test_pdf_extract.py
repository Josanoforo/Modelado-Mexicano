from __future__ import annotations

import subprocess
import tempfile
import unittest
import warnings
from pathlib import Path
from unittest import mock

from tools.curador_registro import barrido2_material, inspect_assets, pdf_extract, semantic_run
from tools.curador_registro.pdf_extract import (
    PdfExtractError,
    PdfExtraction,
    PdfExtractWarning,
    extract_pdf,
    union_page,
)


class PdfExtractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "synthetic.pdf"
        self.path.write_bytes(b"%PDF-1.4\nsynthetic-test\n")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_union_is_default_and_combines_exclusive_lines(self) -> None:
        with (
            mock.patch.object(pdf_extract, "_pypdf_pages", return_value=((1,), ("Pypdf only\nShared line",))) as pypdf_call,
            mock.patch.object(pdf_extract, "_pdftotext_pages", return_value=((1,), ("Shared line\nPoppler only",))) as poppler_call,
        ):
            result = extract_pdf(self.path)
        self.assertEqual(("pypdf", "pdftotext-layout"), result.extractors)
        self.assertEqual("Pypdf only\nShared line\nPoppler only", result.pages[0])
        pypdf_call.assert_called_once()
        poppler_call.assert_called_once()

    def test_pdftotext_uses_layout(self) -> None:
        completed = subprocess.CompletedProcess([], 0, stdout=b"uno\f", stderr=b"")
        with (
            mock.patch.object(pdf_extract.shutil, "which", return_value="/usr/bin/pdftotext"),
            mock.patch.object(pdf_extract.subprocess, "run", return_value=completed) as run,
        ):
            result = extract_pdf(self.path, mode="pdftotext")
        command = run.call_args.args[0]
        self.assertEqual("/usr/bin/pdftotext", command[0])
        self.assertIn("-layout", command)
        self.assertEqual(("uno",), result.pages)

    def test_union_deduplicates_by_normalized_whitespace_stably(self) -> None:
        merged = union_page("Primera\nA   B\nTercera", " A B \nCuarta\nPrimera")
        self.assertEqual("Primera\nA   B\nTercera\nCuarta", merged)

    def test_missing_pdftotext_falls_back_visibly_to_pypdf(self) -> None:
        with (
            mock.patch.object(pdf_extract, "_pypdf_pages", return_value=((1,), ("texto",))),
            mock.patch.object(pdf_extract, "_pdftotext_pages", side_effect=PdfExtractError("PDFTOTEXT_NO_INSTALADO")),
            warnings.catch_warnings(record=True) as caught,
        ):
            warnings.simplefilter("always")
            result = extract_pdf(self.path)
        self.assertEqual(("pypdf",), result.extractors)
        self.assertIn("PDF_UNION_FALLBACK_PYPDF", result.warnings[0])
        self.assertTrue(any(issubclass(item.category, PdfExtractWarning) for item in caught))

    def test_explicit_modes_do_not_call_other_extractor(self) -> None:
        with (
            mock.patch.object(pdf_extract, "_pypdf_pages", return_value=((1,), ("py",))) as pypdf_call,
            mock.patch.object(pdf_extract, "_pdftotext_pages", return_value=((1,), ("pop",))) as poppler_call,
        ):
            self.assertEqual(("py",), extract_pdf(self.path, mode="pypdf").pages)
            poppler_call.assert_not_called()
            pypdf_call.reset_mock()
            self.assertEqual(("pop",), extract_pdf(self.path, mode="pdftotext").pages)
            pypdf_call.assert_not_called()

    def test_explicit_pdftotext_without_binary_is_error(self) -> None:
        with mock.patch.object(pdf_extract.shutil, "which", return_value=None):
            with self.assertRaisesRegex(PdfExtractError, "PDFTOTEXT_NO_INSTALADO"):
                extract_pdf(self.path, mode="pdftotext")

    def test_missing_pypdf_is_clear_installation_error(self) -> None:
        with mock.patch.object(pdf_extract, "_pypdf_pages", side_effect=PdfExtractError("PYPDF_NO_INSTALADO: instale requirements")):
            with self.assertRaisesRegex(PdfExtractError, "PYPDF_NO_INSTALADO"):
                extract_pdf(self.path)

    def test_both_extractors_failure_is_error_not_empty_result(self) -> None:
        with (
            mock.patch.object(pdf_extract, "_pypdf_pages", side_effect=PdfExtractError("PYPDF_FALLO:x")),
            mock.patch.object(pdf_extract, "_pdftotext_pages", side_effect=PdfExtractError("PDFTOTEXT_FALLO:y")),
        ):
            with self.assertRaisesRegex(PdfExtractError, "PDF_AMBOS_EXTRACTORES_FALLARON"):
                extract_pdf(self.path)

    def test_both_successful_extractors_without_text_are_error(self) -> None:
        with (
            mock.patch.object(pdf_extract, "_pypdf_pages", return_value=((1,), ("  \n",))),
            mock.patch.object(pdf_extract, "_pdftotext_pages", return_value=((1,), ("\t",))),
        ):
            with self.assertRaisesRegex(
                PdfExtractError, "PDF_AMBOS_EXTRACTORES_FALLARON:PDF_SIN_TEXTO"
            ):
                extract_pdf(self.path)

    def test_pdftotext_failure_and_empty_pypdf_are_error(self) -> None:
        with (
            mock.patch.object(pdf_extract, "_pypdf_pages", return_value=((1,), ("\n",))),
            mock.patch.object(
                pdf_extract, "_pdftotext_pages",
                side_effect=PdfExtractError("PDFTOTEXT_FALLO:rc=1"),
            ),
        ):
            with self.assertRaisesRegex(
                PdfExtractError, "PDF_AMBOS_EXTRACTORES_FALLARON:PDF_SIN_TEXTO"
            ):
                extract_pdf(self.path)

    def test_barrido2_productive_callsite_uses_union_default(self) -> None:
        extraction = PdfExtraction(("PREGUNTA?",), (1,), ("pypdf", "pdftotext-layout"), ())
        info = subprocess.CompletedProcess([], 0, stdout="Pages: 1\nEncrypted: no\n", stderr="")
        with (
            mock.patch.object(barrido2_material.subprocess, "run", return_value=info),
            mock.patch.object(barrido2_material, "extract_pdf", return_value=extraction) as shared,
        ):
            objects = barrido2_material._pdf_objects(self.path)
        self.assertTrue(any(row["type"] == "REACTIVO-PDF" for row in objects))
        self.assertEqual("union", shared.call_args.kwargs["mode"])

    def test_barrido2_union_does_not_depend_on_pdfinfo(self) -> None:
        extraction = PdfExtraction(("texto",), (1,), ("pypdf", "pdftotext-layout"), ())
        with (
            mock.patch.object(barrido2_material.subprocess, "run", side_effect=FileNotFoundError("pdfinfo")),
            mock.patch.object(barrido2_material, "extract_pdf", return_value=extraction),
        ):
            objects = barrido2_material._pdf_objects(self.path)
        page = next(row for row in objects if row["type"] == "PAGINA-PDF")
        self.assertIn("PDFINFO_NO_DISPONIBLE", page["definition"])

    def test_inspect_assets_productive_callsite_uses_union_default(self) -> None:
        extraction = PdfExtraction(("I. ENCABEZADO",), (1,), ("pypdf", "pdftotext-layout"), ())
        info = subprocess.CompletedProcess([], 0, stdout="Pages: 1\nEncrypted: no\n", stderr="")
        with (
            mock.patch.object(inspect_assets.subprocess, "run", return_value=info),
            mock.patch.object(inspect_assets, "extract_pdf", return_value=extraction) as shared,
        ):
            structure, objects, _ = inspect_assets.inspect_pdf(self.path)
        self.assertEqual(["pypdf", "pdftotext-layout"], structure["extractores_texto"])
        self.assertTrue(objects)
        self.assertEqual("union", shared.call_args.kwargs["mode"])

    def test_inspect_assets_union_does_not_depend_on_pdfinfo(self) -> None:
        extraction = PdfExtraction(("I. ENCABEZADO",), (1,), ("pypdf", "pdftotext-layout"), ())
        with (
            mock.patch.object(inspect_assets.subprocess, "run", side_effect=FileNotFoundError("pdfinfo")),
            mock.patch.object(inspect_assets, "extract_pdf", return_value=extraction),
        ):
            structure, _, boundary = inspect_assets.inspect_pdf(self.path)
        self.assertIn("PDFINFO_NO_DISPONIBLE", structure["advertencias_extraccion"][0])
        self.assertIn("PDFINFO_NO_DISPONIBLE", boundary)

    def test_semantic_productive_callsite_uses_union_default(self) -> None:
        extraction = PdfExtraction(("texto semantico",), (1,), ("pypdf", "pdftotext-layout"), ())
        with mock.patch.object(semantic_run, "extract_pdf", return_value=extraction) as shared:
            opened = semantic_run.open_local_object(self.path, "PDF")
        self.assertEqual("ABIERTO_PDF_TEXTO", opened["resultado"])
        self.assertEqual("pypdf;pdftotext-layout", opened["extractores_pdf"])
        self.assertEqual("union", shared.call_args.kwargs["mode"])


if __name__ == "__main__":
    unittest.main()
