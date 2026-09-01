#!/usr/bin/env python3
"""Sorteo de ``MARCO-M-v1_1``, ``ACTO MAESTRA33-B2 · MARCO-M-SORTEA-v1_1`` (ACTO B″).

Reutiliza el mecanismo YA sellado en ``sorteo_v2.py`` (``sortear``,
``semilla_desde_sha_merge``, ADR-178/FP-150) y en ``sorteo_marco_m.py``
(``regla_de_tamano``, ``sortear_marco_m``) -- ninguno de los dos se edita
(precedente del reglamento ADR-178, ya invocado por ``ACTO B′``).

``sorteo_marco_m.cargar_marco_m`` apunta por defecto a
``marco-M-congelado-v1_0.tsv``/``CONGELADO-M-v1_0.sha256`` y, aunque acepta
rutas por parámetro, construye sus filas de **todas** las filas del TSV
leído -- no conoce la columna ``elegible_v1_1``. Contra
``marco-M-congelado-v1_1.tsv`` (27 filas totales, ``N_elegibles=22``) ese
cargador leería 27 filas y las compararía contra ``N_elegibles=22``
declarado en ``CONGELADO-M-v1_1.sha256`` -> ``AssertionError`` en su
propio ``assert len(filas) == n_elegibles_declarado``. El propio sidecar
lo advierte (nota ``nota_lectura``): "Quien lea este marco para sortear
debe filtrar ``elegible_v1_1=='SI'`` ANTES del assert de conteo... el
cambio es de B''". Este módulo aporta exactamente ese filtro, como
"cargador propio" (precedente ADR-178 explícito en el encargo B″) -- no
edita ``cargar_marco_m`` ni su default v1_0.

Hallazgo, no decisión de este acto: la columna legacy ``elegible`` cuenta
23 filas ``SI`` (una más que ``elegible_v1_1``, que cuenta 22 -- el propio
``FP-208``/``AGENTE-DESPACHO-1`` ya adjudicó esta junta al encolar). Este
módulo usa ``elegible_v1_1`` porque es la que el encargo B″ declara
("N_elegibles esperado 22") y la que ``CONGELADO-M-v1_1.sha256`` declara
-- no ``elegible``.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
CONGELADO_M_V1_1 = DIR / "marco-M-congelado-v1_1.tsv"
SHA256_M_V1_1 = DIR / "CONGELADO-M-v1_1.sha256"

_SPEC = importlib.util.spec_from_file_location("sorteo_marco_m", DIR / "sorteo_marco_m.py")
_MARCO_M = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _MARCO_M
_SPEC.loader.exec_module(_MARCO_M)

Fila = _MARCO_M.Fila
ResultadoSorteo = _MARCO_M.ResultadoSorteo
semilla_desde_sha_merge = _MARCO_M.semilla_desde_sha_merge
regla_de_tamano = _MARCO_M.regla_de_tamano
sortear_marco_m = _MARCO_M.sortear_marco_m
_SORTEO_V2 = _MARCO_M._SORTEO_V2


def _leer_n_elegibles_declarado(ruta: Path = SHA256_M_V1_1) -> tuple[str, int]:
    """Mismo formato que el sidecar v1_0: ``<sha256>  <archivo>`` y
    ``N_elegibles=<n>`` en líneas separadas."""
    lineas = ruta.read_text(encoding="utf-8").splitlines()
    sha_declarado = lineas[0].split(None, 1)[0].strip()
    n_linea = next(l for l in lineas if l.startswith("N_elegibles="))
    n_elegibles = int(n_linea.split("=", 1)[1].strip())
    return sha_declarado, n_elegibles


def cargar_marco_m_v1_1(
    ruta: Path = CONGELADO_M_V1_1, ruta_sha: Path = SHA256_M_V1_1
) -> list[Fila]:
    """Verifica el sha256 de ``marco-M-congelado-v1_1.tsv`` contra
    ``CONGELADO-M-v1_1.sha256`` (PARO por ``AssertionError`` si no
    coincide), filtra ``elegible_v1_1 == 'SI'`` -- ANTES de contar, a
    diferencia de ``sorteo_marco_m.cargar_marco_m`` -- y verifica que el
    conteo filtrado coincida con ``N_elegibles`` declarado ahí."""
    sha_declarado, n_elegibles_declarado = _leer_n_elegibles_declarado(ruta_sha)

    contenido = ruta.read_bytes()
    sha_real = hashlib.sha256(contenido).hexdigest()
    assert sha_real == sha_declarado, (
        f"sha256 de {ruta.name} no coincide con {ruta_sha.name}: "
        f"real={sha_real} declarado={sha_declarado}"
    )

    with ruta.open(encoding="utf-8", newline="") as fh:
        lector = csv.DictReader(fh, delimiter="\t")
        filas = [
            Fila(
                id=renglon["id"],
                estrato=renglon["estrato"].strip(),
                publicada=(
                    _SORTEO_V2._publicada_de(renglon["publicada"])
                    if renglon["publicada"].strip()
                    else "NO"
                ),
            )
            for renglon in lector
            if renglon["elegible_v1_1"].strip() == "SI"
        ]
    filas.sort(key=lambda f: f.id)

    assert len(filas) == n_elegibles_declarado, (
        f"filas elegible_v1_1=='SI' leídas de {ruta.name} = {len(filas)}, "
        f"N_elegibles declarado en {ruta_sha.name} = {n_elegibles_declarado}"
    )
    return filas


if __name__ == "__main__":
    raise SystemExit(
        "sorteo_marco_m_v1_1.py no se ejecuta como CLI aquí -- ver"
        " forense/prereg-duelo-v2/sorteo-marco-M-resultados-v1_1.md para la"
        " invocación exacta pre-registrada y su corrida única."
    )
