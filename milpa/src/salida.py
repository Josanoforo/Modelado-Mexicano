"""Determinismo, serialización canónica y hash.

Misma semilla ⇒ mismo hash. Sin `datetime.now()`, sin RNG no sembrado, orden de
claves FIJO en la serialización. El hash es sobre la serialización canónica,
no sobre `repr()` — `repr()` de un dict depende del orden de inserción y eso
haría del determinismo una coincidencia.
"""

import hashlib
import json


def serializar(obj):
    """Serialización canónica: claves ordenadas, sin espacios variables, UTF-8."""
    return json.dumps(
        obj, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    )


def hash_salida(resultado):
    """`sha256` sobre la serialización canónica del resultado."""
    payload = resultado if isinstance(resultado, (dict, list)) else resultado.como_dict()
    return hashlib.sha256(serializar(payload).encode("utf-8")).hexdigest()
