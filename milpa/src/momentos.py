"""El catálogo `M`, los roles, y el muro `AJUSTE`/`HOLDOUT`.

Fuente única: `milpa/catalogo-momentos-v0_1.tsv`, sellado en el COMMIT C1 de
este mismo acto — ANTES que este módulo, en historia de git. Ese orden es el
umbral (1) de `ADR-68` (Ronda 1 §7): `commit_declaracion` anterior en git a
todo resultado.

EL MURO, CON DIENTES: `momentos_holdout()` devuelve METADATOS SIN VALORES.
Pedir el valor de un momento `HOLDOUT` durante E0 lanza `HoldoutTocado`. No es
una convención de estilo: es la única barrera entre "pre-registro" y "cuento".
"""

import csv
import os
from dataclasses import dataclass

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RUTA_CATALOGO = os.path.join(RAIZ, "milpa", "catalogo-momentos-v0_1.tsv")

#: S2 de RONDA-M: el campo es `rol_calibracion`, NO `rol` — `rol:` ya está
#: sellado por `ADR-68(a)` con otro enum (BASELINE|CHALLENGER|COMPLEMENTO) y en
#: uso en las tres celdas-D del disco. Dos vocabularios bajo una misma llave es
#: una colisión, no un sinónimo.
ROLES = ("AJUSTE", "HOLDOUT", "DIAGNÓSTICO")


class HoldoutTocado(RuntimeError):
    """Se intentó leer el valor de un momento `HOLDOUT`.

    Violación de pre-registro (`canon/gobernanza-v1_15.md:461`,
    "los momentos a reproducir SE DECLARAN ANTES DE AJUSTAR").
    """


class CatalogoNoSellado(RuntimeError):
    """Se pidió operar sobre un catálogo sin `commit_sha` de sello."""


@dataclass(frozen=True)
class Momento:
    id_momento: str
    objeto_modelo: str
    necesidad_id: str
    rol_calibracion: str
    universo_candidatos: str
    universo_instrumento: str
    nivel: str
    computo_pretendido: str
    estatus_disponibilidad: str
    fuente_regla: str
    reserva: str


@dataclass(frozen=True)
class Catalogo:
    momentos: tuple
    commit_sha: str

    def __len__(self):
        return len(self.momentos)


def cargar_catalogo(ruta=None, commit_sha="C1"):
    ruta = ruta or RUTA_CATALOGO
    with open(ruta, encoding="utf-8", newline="") as fh:
        filas = list(csv.DictReader(fh, delimiter="\t"))
    momentos = []
    for f in filas:
        if f["rol_calibracion"] not in ROLES:
            raise ValueError(
                f"{f['id_momento']}: `rol_calibracion` desconocido "
                f"{f['rol_calibracion']!r}; los admitidos son {ROLES}"
            )
        momentos.append(
            Momento(
                id_momento=f["id_momento"],
                objeto_modelo=f["objeto_modelo"],
                necesidad_id=f["necesidad_id"],
                rol_calibracion=f["rol_calibracion"],
                universo_candidatos=f["universo_candidatos"],
                universo_instrumento=f["universo_instrumento"],
                nivel=f["nivel"],
                computo_pretendido=f["computo_pretendido"],
                estatus_disponibilidad=f["estatus_disponibilidad"],
                fuente_regla=f["fuente_regla"],
                reserva=f["reserva"],
            )
        )
    return sellar_catalogo(momentos, commit_sha)


def sellar_catalogo(entradas, commit_sha):
    """Congela ids y `rol_calibracion`. Append-only por construcción."""
    if not commit_sha:
        raise CatalogoNoSellado("un catálogo sin `commit_sha` no está sellado")
    return Catalogo(momentos=tuple(entradas), commit_sha=commit_sha)


def momentos_ajuste(catalogo):
    return tuple(m for m in catalogo.momentos if m.rol_calibracion == "AJUSTE")


def momentos_holdout(catalogo):
    """Metadatos SIN valores. Ver `valor_de()`."""
    return tuple(m for m in catalogo.momentos if m.rol_calibracion == "HOLDOUT")


def firma_de_roles(catalogo):
    """La huella del reparto sellado: `(id, rol)` ordenado.

    Es lo que `tests/test_motor_holdout.py` compara entre commits. Si cambia,
    el pre-registro cambió.
    """
    return tuple(
        sorted((m.id_momento, m.rol_calibracion) for m in catalogo.momentos)
    )


def valor_de(momento):
    """El valor observado de un momento. En E0, sólo para `AJUSTE`.

    `HOLDOUT` lanza. No devuelve `None`, no advierte y sigue: lanza. Un muro
    que se puede cruzar avisando no es un muro.
    """
    if momento.rol_calibracion == "HOLDOUT":
        raise HoldoutTocado(
            f"`{momento.id_momento}` ({momento.objeto_modelo}) es HOLDOUT: "
            f"leer su valor en E0 es violación de pre-registro."
        )
    raise NotImplementedError(
        f"`{momento.id_momento}`: `estatus_disponibilidad` es "
        f"{momento.estatus_disponibilidad!r} y su `universo_candidatos` está "
        f"POR DECLARAR. E0 no mira el disco (§3.3 de la propuesta)."
    )
