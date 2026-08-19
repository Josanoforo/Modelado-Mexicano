"""π(x) — CERRADO CON LLAVE hasta que M2 selle cortes y exista fuente.

Este módulo es el ejemplo del principio del paquete: **existe, tiene contrato,
y falla ruidosamente**. No está ausente, porque un módulo ausente se reinventa;
está cerrado, porque lo que falta es un dato que nadie ha producido.

MEDIDO, no supuesto (§4.2 del plan de MOTOR-3/E0):
  · `tasa_informalidad` aparece 0 veces en `milpa/procedencia.yaml`.
  · el carácter `π` tampoco aparece nunca ahí.
  · el bloque de `milpa/milpa-spec-v0_2.md:65-90` que se cita como ejemplo NO
    es YAML cargable: es documentación en fence de Markdown, con `...`
    literales como placeholders.

Lo que SÍ está anclado y es firme: el tick trimestral, alineado con ENOE
(`milpa/milpa-spec-v0_2.md:269`).

RESTRICCIÓN HEREDADA que el módulo hace cumplir, citada:
"el IPU reproduce marginales; no fabrica conjuntas que nadie midió"
(`canon/modelo-decision-v4_0.md`). Consecuencia ejecutable: `validar_momento()`
rechaza todo momento que exija una conjunta de atributos que ENIGH no observe.
"""

from dataclasses import dataclass

from .celdas import Cortes
from .clases import EJES_HOGAR

TICK = "1 trimestre (alineado con ENOE, `milpa/milpa-spec-v0_2.md:269`)"


class FuentePiPendiente(RuntimeError):
    """No hay fuente cargable para π(x). No se fabrica una."""


class CortesNoSellados(RuntimeError):
    """Los cortes no traen la firma de M2."""


class ConjuntaNoObservada(ValueError):
    """El momento exige una conjunta que el instrumento no observa."""


@dataclass(frozen=True)
class Pi:
    """π(x). `frozen=True` a propósito.

    π SE CONGELA ANTES DE CALIBRAR y no es grado de libertad (§2 de la
    propuesta). Un π mutable es un grado de libertad que nadie contó.
    """

    pesos: tuple
    fuente: str
    tick: str = TICK


def construir_pi(cortes, fuente=None):
    """Lanza siempre, hoy. Cada rama dice qué falta y quién lo produce."""
    if not isinstance(cortes, Cortes) or not cortes.firma_m2:
        raise CortesNoSellados(
            "π no se construye con cortes sin la firma de M2 (`ADR-100(2)`)."
        )
    if cortes.pendientes:
        raise CortesNoSellados(
            f"cortes PENDIENTE: {cortes.pendientes}. `FP-53` tiene abierta esa "
            f"deuda; definirlos exige dato mexicano propio y es acto propio."
        )
    if not fuente:
        raise FuentePiPendiente(
            "π(x) no tiene hoy fuente cargable: `tasa_informalidad` aparece 0 "
            "veces en `milpa/procedencia.yaml` y el bloque de "
            "`milpa/milpa-spec-v0_2.md` es documentación, no YAML. Qué acto la "
            "produce y con qué nombre es pregunta abierta a mesa."
        )
    raise FuentePiPendiente(
        f"fuente {fuente!r} declarada pero no hay lector sellado para ella en "
        f"E0. Construir π es calibración (E1+)."
    )


def validar_momento(momento, ejes_exigidos):
    """Rechaza el momento que exija una conjunta que el instrumento no observa.

    Los tres ejes de hogar no admiten contraste intra-hogar: un momento que lo
    exija es infalsable con ENIGH, y decirlo antes de correr es más barato que
    descubrirlo después.
    """
    malos = [e for e in ejes_exigidos if e in EJES_HOGAR]
    if malos:
        raise ConjuntaNoObservada(
            f"`{momento.id_momento}` exige contraste intra-hogar en {malos}: "
            f"el IPU reproduce marginales, no fabrica conjuntas que nadie "
            f"midió."
        )
    return True
