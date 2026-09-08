#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/payload_resolver.py -- resolver único de payload.

ACTO GEN2-E3-1 · READINESS-DEL-RUNNER, P1. Antes de este módulo,
`tools/corrida0.py` verificaba un payload de `origen: manifiesto` lanzando
`tests/manifiesto.py --verifica` en un SUBPROCESO y parseando su salida de
texto -- ni `ruta_absoluta` ni `sha256_actual` ni `tamano` viajaban de vuelta:
el medidor se quedaba sin saber dónde está su propio insumo (`ADR-379`-clase
de defecto, A.8 de este acto). Este módulo expone `resolver_payload(id)`
como función pura, importable directamente -- MISMO PATRÓN que
`tests/corpus.py` ya usa para reutilizar las primitivas de
`tests/manifiesto.py` (import directo con `sys.path.insert`, nunca
subproceso; ver la cabecera de `tests/corpus.py`).

Extraído de `tests/manifiesto.py::cmd_verifica`, no reimplementado: la
resolución por entrada (raíz declarada -> raíz física -> archivo -> hash) es
la misma que ese comando ya hacía; `cmd_verifica` ahora LLAMA a
`resolver_payload` para cada entrada en vez de resolver a mano -- su CLI y su
salida de texto no cambian (P1 lo exige).

Cinco estados, cerrados -- ninguno implícito fuera de estos cinco:
    COINCIDE             sha256 (y tamaño, si el manifiesto lo declara)
                          coinciden con el archivo real.
    NO_COINCIDE           el archivo existe pero su contenido no coincide.
    AUSENTE               el id no está en el manifiesto (o no trae
                           `sha256`), la entrada no declara `archivo`, o el
                           archivo no está en su raíz -- las tres son la
                           misma consecuencia operativa (nada que hashear) y
                           ninguna es un error del manifiesto: el payload
                           nunca se commitea.
    RAIZ_NO_CONFIGURADA   la entrada declara una raíz que ESTE entorno no
                           define en `data/raices.local.yaml` (puede ser
                           válida en otra máquina).
    FUERA_DE_PERIMETRO    la raíz declarada existe pero no es
                           `raiz_escaneable()` (ACTO AUTOMATIZA-1-E1) -- no
                           se resuelve, no se abre, no se hashea.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import manifiesto as M  # noqa: E402

ESTADOS = ("COINCIDE", "NO_COINCIDE", "AUSENTE", "RAIZ_NO_CONFIGURADA",
           "FUERA_DE_PERIMETRO")


def resolver_payload(payload_id, *, entradas=None, root=None, raw_dir=None):
    """{id, raiz_logica, ruta_absoluta, sha256_esperado, sha256_actual,
    tamano, estado}. Puro -- ningún efecto secundario, solo lectura.

    `entradas`/`root`/`raw_dir` son optativos: si el llamador ya los tiene
    (p.ej. `cmd_verifica`, que verifica muchos ids en la misma invocación),
    se los pasa y esta función no vuelve a leer `data/manifiesto.yaml` por
    cada id; si no, los resuelve por su cuenta (un id suelto, como hace
    `tools/corrida0.py` por cada input de una spec).
    """
    if root is None:
        root = M.repo_root()
    if raw_dir is None:
        _mp, raw_dir = M.rutas(root)
    if entradas is None:
        manifiesto_path, _rd = M.rutas(root)
        _cab, entradas = M.leer_manifiesto(manifiesto_path)

    base = {"id": payload_id, "raiz_logica": None, "ruta_absoluta": None,
            "sha256_esperado": None, "sha256_actual": None, "tamano": None}

    entrada = M.buscar(entradas, payload_id)
    if entrada is None or "sha256" not in entrada:
        return {**base, "estado": "AUSENTE"}

    nombre_raiz = entrada.get("raiz", M.RAIZ_INTEGRADA)
    base["raiz_logica"] = nombre_raiz
    base["sha256_esperado"] = entrada.get("sha256")

    if not M.raiz_escaneable(nombre_raiz):
        # ACTO AUTOMATIZA-1-E1: raíz histórica fuera del perímetro físico --
        # no se resuelve, no se abre, no se stat/hashea.
        return {**base, "estado": "FUERA_DE_PERIMETRO"}

    archivo = entrada.get("archivo")
    if not archivo:
        return {**base, "estado": "AUSENTE"}

    base_dir = M.resolver_raiz(nombre_raiz, root, raw_dir)
    if base_dir is None:
        return {**base, "estado": "RAIZ_NO_CONFIGURADA"}

    ruta = os.path.join(base_dir, archivo)
    base["ruta_absoluta"] = ruta
    if not os.path.exists(ruta):
        return {**base, "estado": "AUSENTE"}

    sha_real = M.sha256_de(ruta)
    tam_real = os.path.getsize(ruta)
    base["sha256_actual"] = sha_real
    base["tamano"] = tam_real
    tam_declarado = entrada.get("tamano_bytes")
    coincide = sha_real == base["sha256_esperado"] and tam_real == tam_declarado
    return {**base, "estado": "COINCIDE" if coincide else "NO_COINCIDE"}
