#!/usr/bin/env python3
"""Extracción de texto PDF reproducible con modos explícitos.

El modo ``union`` (default) combina por página pypdf y
``pdftotext -layout``. Conserva primero las líneas de pypdf y agrega las
líneas nuevas de poppler, deduplicadas por whitespace normalizado. El helper
no usa ni requiere ``pdfinfo``.
"""

from __future__ import annotations

import shutil
import subprocess
import warnings as warnings_module
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


MODES = ("union", "pypdf", "pdftotext")


class PdfExtractError(RuntimeError):
    """Fallo material de extracción; nunca representa un PDF vacío válido."""


class PdfExtractWarning(UserWarning):
    """Degradación visible de ``union`` a un solo extractor."""


@dataclass(frozen=True)
class PdfExtraction:
    """Texto por página y trazabilidad de la extracción."""

    pages: tuple[str, ...]
    page_numbers: tuple[int, ...]
    extractors: tuple[str, ...]
    warnings: tuple[str, ...]

    @property
    def text(self) -> str:
        return "\f".join(self.pages)


def _selected_pages(total: int, pages: Iterable[int] | None) -> tuple[int, ...]:
    if pages is None:
        return tuple(range(1, total + 1))
    selected = tuple(dict.fromkeys(int(page) for page in pages))
    if any(page < 1 or page > total for page in selected):
        raise PdfExtractError(f"PAGINA_FUERA_DE_RANGO:total={total};paginas={selected}")
    return selected


def _pypdf_pages(path: Path, pages: Iterable[int] | None) -> tuple[tuple[int, ...], tuple[str, ...]]:
    try:
        from pypdf import PdfReader
    except ImportError as exc:  # pragma: no cover - se prueba forzando el import
        raise PdfExtractError(
            "PYPDF_NO_INSTALADO: instale "
            "tools/curador_registro/requirements-curador-registro.txt"
        ) from exc
    try:
        reader = PdfReader(str(path))
        selected = _selected_pages(len(reader.pages), pages)
        texts = tuple(reader.pages[page - 1].extract_text() or "" for page in selected)
    except PdfExtractError:
        raise
    except Exception as exc:
        raise PdfExtractError(f"PYPDF_FALLO:{type(exc).__name__}:{exc}") from exc
    return selected, texts


def _pdftotext_pages(
    path: Path,
    pages: Iterable[int] | None,
) -> tuple[tuple[int, ...], tuple[str, ...]]:
    executable = shutil.which("pdftotext")
    if executable is None:
        raise PdfExtractError("PDFTOTEXT_NO_INSTALADO: se requiere poppler-utils")

    requested = tuple(dict.fromkeys(int(page) for page in pages)) if pages is not None else ()
    command = [executable, "-layout"]
    if requested:
        if any(page < 1 for page in requested):
            raise PdfExtractError(f"PAGINA_FUERA_DE_RANGO:paginas={requested}")
        command.extend(["-f", str(min(requested)), "-l", str(max(requested))])
    command.extend([str(path), "-"])
    try:
        result = subprocess.run(command, capture_output=True, timeout=120, check=False)
    except (OSError, subprocess.SubprocessError) as exc:
        raise PdfExtractError(f"PDFTOTEXT_FALLO:{type(exc).__name__}:{exc}") from exc
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()[:300]
        raise PdfExtractError(f"PDFTOTEXT_FALLO:rc={result.returncode}:{detail}")

    decoded = result.stdout.decode("utf-8", errors="replace")
    extracted = decoded.split("\f")
    if extracted and extracted[-1] in {"", "\n", "\r\n"}:
        extracted.pop()
    if requested:
        first = min(requested)
        by_page = {first + offset: value for offset, value in enumerate(extracted)}
        return requested, tuple(by_page.get(page, "") for page in requested)
    return tuple(range(1, len(extracted) + 1)), tuple(extracted)


def _normal_line(line: str) -> str:
    return " ".join(line.split())


def union_page(pypdf_text: str, pdftotext_text: str) -> str:
    """Une una página, preservando orden y el texto de la primera aparición."""

    output: list[str] = []
    seen: set[str] = set()
    for source in (pypdf_text, pdftotext_text):
        for raw in source.splitlines():
            line = raw.strip()
            key = _normal_line(line)
            if not key or key in seen:
                continue
            seen.add(key)
            output.append(line)
    return "\n".join(output)


def _warn(message: str, collected: list[str]) -> None:
    collected.append(message)
    warnings_module.warn(message, PdfExtractWarning, stacklevel=3)


def extract_pdf(
    path: Path | str,
    *,
    mode: str = "union",
    pages: Iterable[int] | None = None,
) -> PdfExtraction:
    """Extrae texto con ``union`` (default), ``pypdf`` o ``pdftotext``.

    En ``union``, una falla de ejecución de uno de los extractores se registra
    como advertencia y se conserva el resultado del otro. La ausencia de
    pypdf es un error de instalación; la ausencia de pdftotext solo degrada el
    modo ``union``. Si ambos extractores fallan, no se devuelve texto vacío.
    """

    path = Path(path)
    if mode not in MODES:
        raise PdfExtractError(f"MODO_PDF_INVALIDO:{mode};esperados={','.join(MODES)}")
    selected = tuple(dict.fromkeys(int(page) for page in pages)) if pages is not None else None
    if selected == ():
        extractors = ("pypdf", "pdftotext-layout") if mode == "union" else (mode,)
        return PdfExtraction((), (), extractors, ())

    if mode == "pypdf":
        numbers, extracted = _pypdf_pages(path, selected)
        return PdfExtraction(extracted, numbers, ("pypdf",), ())
    if mode == "pdftotext":
        numbers, extracted = _pdftotext_pages(path, selected)
        return PdfExtraction(extracted, numbers, ("pdftotext-layout",), ())

    collected: list[str] = []
    try:
        numbers, pypdf_text = _pypdf_pages(path, selected)
    except PdfExtractError as pypdf_error:
        if str(pypdf_error).startswith("PYPDF_NO_INSTALADO"):
            raise
        try:
            poppler_numbers, poppler_text = _pdftotext_pages(path, selected)
        except PdfExtractError as poppler_error:
            raise PdfExtractError(
                f"PDF_AMBOS_EXTRACTORES_FALLARON:{pypdf_error};{poppler_error}"
            ) from poppler_error
        if not any(text.strip() for text in poppler_text):
            raise PdfExtractError(
                "PDF_AMBOS_EXTRACTORES_FALLARON:"
                f"{pypdf_error};PDFTOTEXT_SIN_TEXTO"
            )
        _warn(f"PDF_UNION_FALLBACK_PDFTOTEXT:{pypdf_error}", collected)
        return PdfExtraction(poppler_text, poppler_numbers, ("pdftotext-layout",), tuple(collected))

    try:
        poppler_numbers, poppler_text = _pdftotext_pages(path, numbers)
    except PdfExtractError as poppler_error:
        if not any(text.strip() for text in pypdf_text):
            raise PdfExtractError(
                "PDF_AMBOS_EXTRACTORES_FALLARON:"
                f"PDF_SIN_TEXTO;{poppler_error}"
            ) from poppler_error
        _warn(f"PDF_UNION_FALLBACK_PYPDF:{poppler_error}", collected)
        return PdfExtraction(pypdf_text, numbers, ("pypdf",), tuple(collected))

    if poppler_numbers != numbers:
        raise PdfExtractError(
            f"PDF_PAGINAS_NO_ALINEADAS:pypdf={numbers};pdftotext={poppler_numbers}"
        )
    merged = tuple(union_page(left, right) for left, right in zip(pypdf_text, poppler_text))
    if not any(text.strip() for text in merged):
        raise PdfExtractError("PDF_AMBOS_EXTRACTORES_FALLARON:PDF_SIN_TEXTO")
    return PdfExtraction(merged, numbers, ("pypdf", "pdftotext-layout"), tuple(collected))
