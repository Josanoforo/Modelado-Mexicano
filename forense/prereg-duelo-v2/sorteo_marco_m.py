#!/usr/bin/env python3
"""Sorteo de ``MARCO-M-v1``, ACTO ``MAESTRA32-E14 · MARCO-M-SORTEA`` (ACTO B′).

Reutiliza el mecanismo YA sellado en ``sorteo_v2.py`` (``sortear``,
``semilla_desde_sha_merge``, ADR-178/FP-150) — no lo edita. ``sorteo_v2.py``
sigue apuntando a ``marco-congelado-piloto-v1_0.tsv`` con su propio
``assert n=50``; ese cargador no se toca, no se reutiliza para el marco-M.

Este módulo aporta solo lo que falta: un cargador para
``marco-M-congelado-v1_0.tsv`` que verifica su sha256 contra
``CONGELADO-M-v1_0.sha256`` (PARO si no coincide) y su ``N_elegibles``
declarado, más el caso de la regla de tamaño de
``forense/notas/2026-08-31-marco-M-spec.md`` §e: cuando
``N_elegibles < 15`` el "sorteo" es la identidad (entran todas las filas
elegibles, sin PRNG) y se sella igual.
"""
from __future__ import annotations

import hashlib
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = Path(__file__).resolve().parent
CONGELADO_M = DIR / "marco-M-congelado-v1_0.tsv"
SHA256_M = DIR / "CONGELADO-M-v1_0.sha256"

_SPEC = importlib.util.spec_from_file_location("sorteo_v2", DIR / "sorteo_v2.py")
_SORTEO_V2 = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _SORTEO_V2
_SPEC.loader.exec_module(_SORTEO_V2)

Fila = _SORTEO_V2.Fila
ResultadoSorteo = _SORTEO_V2.ResultadoSorteo
sortear = _SORTEO_V2.sortear
semilla_desde_sha_merge = _SORTEO_V2.semilla_desde_sha_merge


def _leer_n_elegibles_declarado(ruta: Path = SHA256_M) -> tuple[str, int]:
    """``CONGELADO-M-v1_0.sha256`` trae dos líneas: ``<sha256>  <archivo>`` y
    ``N_elegibles=<n>``. Devuelve ``(sha_declarado, n_elegibles)``."""
    lineas = ruta.read_text(encoding="utf-8").splitlines()
    sha_declarado = lineas[0].split(None, 1)[0].strip()
    n_linea = next(l for l in lineas if l.startswith("N_elegibles="))
    n_elegibles = int(n_linea.split("=", 1)[1].strip())
    return sha_declarado, n_elegibles


def cargar_marco_m(ruta: Path = CONGELADO_M, ruta_sha: Path = SHA256_M) -> list[Fila]:
    """Verifica el sha256 del congelado contra ``CONGELADO-M-v1_0.sha256``
    (PARO por ``AssertionError`` si no coincide) y que el número de filas
    coincida con ``N_elegibles`` declarado ahí — no con un valor tecleado en
    este módulo."""
    sha_declarado, n_elegibles_declarado = _leer_n_elegibles_declarado(ruta_sha)

    contenido = ruta.read_bytes()
    sha_real = hashlib.sha256(contenido).hexdigest()
    assert sha_real == sha_declarado, (
        f"sha256 de {ruta.name} no coincide con {ruta_sha.name}: "
        f"real={sha_real} declarado={sha_declarado}"
    )

    import csv

    with ruta.open(encoding="utf-8", newline="") as fh:
        lector = csv.DictReader(fh, delimiter="\t")
        filas = [
            Fila(
                id=renglon["id"],
                estrato=renglon["estrato"].strip(),
                publicada=(_SORTEO_V2._publicada_de(renglon["publicada"]) if renglon["publicada"].strip() else "NO"),
            )
            for renglon in lector
        ]
    filas.sort(key=lambda f: f.id)

    assert len(filas) == n_elegibles_declarado, (
        f"filas leídas de {ruta.name} = {len(filas)}, "
        f"N_elegibles declarado en {ruta_sha.name} = {n_elegibles_declarado}"
    )
    return filas


def regla_de_tamano(n_elegibles: int) -> tuple[int, int]:
    """§e de ``2026-08-31-marco-M-spec.md``, fijada ANTES de ver ``N``:
    ``N>=30 -> n_sorteo=15``; ``15<=N<30 -> n_sorteo=ceil(N/2)``;
    ``N<15 -> sin sorteo (todas las elegibles)``, aquí representado como
    ``n_sorteo = N`` para que ``cuota_max = floor(0.20*n_sorteo)`` siga
    siendo una cifra bien definida aunque no haya PRNG."""
    if n_elegibles >= 30:
        n_sorteo = 15
    elif n_elegibles >= 15:
        import math

        n_sorteo = math.ceil(n_elegibles / 2)
    else:
        n_sorteo = n_elegibles
    cuota_max = n_sorteo * 20 // 100
    return n_sorteo, cuota_max


def sortear_marco_m(marco: list[Fila], n_sorteo: int, cuota_max: int, semilla: int) -> ResultadoSorteo:
    """Si ``len(marco) < 15`` el "sorteo" es la identidad (§e): todas las
    filas elegibles entran, sin invocar el PRNG — no hay universo del que
    muestrear sin reposición debajo de ese piso. Con 15 o más filas se
    delega literalmente en ``sorteo_v2.sortear`` (mismo mecanismo, sin
    reimplementarlo)."""
    if len(marco) < 15:
        return ResultadoSorteo(resultado=sorted(marco, key=lambda f: f.id))
    return sortear(marco, n_sorteo, cuota_max, semilla)


if __name__ == "__main__":
    raise SystemExit(
        "sorteo_marco_m.py no se ejecuta como CLI aquí -- ver"
        " forense/prereg-duelo-v2/sorteo-marco-M-resultados-v1_0.md para la"
        " invocación exacta pre-registrada y su corrida única."
    )
