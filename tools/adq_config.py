#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools/adq_config.py -- lector de `data/adq-config.yaml` (P6, ACTO
ADQ-CRON-V2 · DISPARO-PERSISTENTE-Y-RUNNER-IDEMPOTENTE, 7/sep/2026).

Antes de este acto, `tools/adquiere_cron.sh` traía cableadas a mano las
URLs, las claves física/lógica y los ids de referencia de manifiesto de la
PDN. Un archivo de configuración pequeño y versionado permite auditarlas
sin leer el shell y reutilizarlas desde `tools/adq_doctor.py` -- este
módulo es el único lector, para que shell y Python nunca diverjan sobre
qué significa cada clave.

No decide nada: si una clave falta, error explícito -- nunca un default
inventado que enmascare un `data/adq-config.yaml` mal editado.

Uso:
    python3 tools/adq_config.py <ruta.punteada>
        Imprime el valor (str/num tal cual; dict/list como JSON) en stdout.
        Exit 1 y mensaje en stderr si la ruta no existe.

    from adq_config import cargar, obten
        cargar()             -> dict completo
        obten("pdn.sistemas.s1.url", cfg=None)  -> valor resuelto
"""
import json
import os
import sys

import yaml

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_CONFIG = os.path.join(RAIZ, "data", "adq-config.yaml")


def cargar(ruta=RUTA_CONFIG):
    with open(ruta, encoding="utf-8") as f:
        return yaml.safe_load(f)


def obten(ruta_punteada, cfg=None, config_path=None):
    """Resuelve `a.b.c` sobre el dict de configuración. Lanza KeyError con
    el tramo exacto que faltó -- nunca devuelve None por una clave ausente.

    `config_path=None` (default real, no ligado en tiempo de definición)
    resuelve `RUTA_CONFIG` en tiempo de LLAMADA -- así un llamador que
    parcha `adq_config.RUTA_CONFIG` (pruebas) sí lo ve; un default de
    parámetro (`config_path=RUTA_CONFIG`) se congela en el import y nunca
    vería el parche."""
    if cfg is None:
        cfg = cargar(config_path if config_path is not None else RUTA_CONFIG)
    valor = cfg
    recorrido = []
    for parte in ruta_punteada.split("."):
        recorrido.append(parte)
        if not isinstance(valor, dict) or parte not in valor:
            raise KeyError(f"{'.'.join(recorrido)} (dentro de {ruta_punteada!r})")
        valor = valor[parte]
    return valor


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print("uso: adq_config.py <ruta.punteada>", file=sys.stderr)
        return 2
    try:
        valor = obten(argv[0])
    except KeyError as e:
        print(f"ERROR: no existe la clave {e} en {RUTA_CONFIG}", file=sys.stderr)
        return 1
    except FileNotFoundError:
        print(f"ERROR: no existe {RUTA_CONFIG}", file=sys.stderr)
        return 1
    if isinstance(valor, (dict, list)):
        print(json.dumps(valor, ensure_ascii=False))
    else:
        print(valor)
    return 0


if __name__ == "__main__":
    sys.exit(main())
