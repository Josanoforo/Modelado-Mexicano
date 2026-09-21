"""`Θ(x)` — los parámetros como distribuciones condicionales.

`ADR-28.d` sigue vigente y se relee sobre la malla nueva: dos agentes CON EL
MISMO VECTOR DE ATRIBUTOS DEBEN PODER DIFERIR. La dispersión no es un extra: es
parte de la especificación de θ_k.

En E0 este módulo NO estima nada. Lee lo ya adjudicado en
`milpa/procedencia.yaml` y respeta el contrato de clase que impone
`procedencia.py`: una `MEDIDO·NACIONAL` no se segmenta, una `MEDIDO·PARCIAL(x)`
sólo por sus `x`, y una `ASIGNADO` devuelve punto sin banda con su deuda a la
vista.

ESTADO VIGENTE (ACTO MOTOR-THETA-CONGELADA-1, 21/sep/2026): `valor()` lanza
para las 43 entradas, y por eso `matriz.g` no es camino de emisión vigente.
No es un defecto a parchar: bajo `ADR-531` la matriz compone, no estima, y
compite como candidato de una celda solo cuando esa celda la adjudica por
contrato celda-D (`ADR-68`). Mientras ninguna lo haga, lanzar es lo correcto.
"""

from dataclasses import dataclass

from .clases import Clase, SegmentacionProhibida
from .procedencia import segmentar


class ThetaNoDisponible(LookupError):
    """No hay θ adjudicada para ese nombre. No se sustituye por un default."""


@dataclass
class Theta:
    entradas: dict     # nombre -> Entrada

    @classmethod
    def desde(cls, procedencia):
        # La restricción de nivel hogar viaja con la condicional
        # (`modelo` §1.1.B, inciso 2): no se pierde al indexar por nombre.
        return cls(entradas={e.llave: e for e in procedencia.consumibles()})

    def valor(self, nombre, celda=None):
        """Devuelve el valor de θ_k en la celda.

        En E0 no hay condicional cargable por celda para la mayoría de los
        nombres. Antes que devolver un default, LANZA: un default silencioso es
        una cifra nueva al canon disfrazada de valor por omisión.
        """
        e = self.entradas.get(nombre)
        if e is None:
            raise ThetaNoDisponible(
                f"no hay θ adjudicada para `{nombre}` en "
                f"`milpa/procedencia.yaml`. No se sustituye por un default."
            )
        if celda is not None:
            for eje, _ in celda.coordenadas:
                segmentar(e, eje)
        raise ThetaNoDisponible(
            f"`{nombre}` está registrada como {e.clase.value} pero no hay "
            f"distribución cargable: `matriz.g` no es camino de emisión "
            f"vigente. Bajo ADR-531 la matriz compone, no estima, y solo "
            f"compite en una celda que la adjudique por contrato celda-D "
            f"(ADR-68). No se sustituye por un default."
        )

    def segmentable(self, nombre, eje):
        """¿Puede `nombre` segmentarse por `eje`? Contesta sin computar."""
        e = self.entradas.get(nombre)
        if e is None:
            raise ThetaNoDisponible(nombre)
        try:
            segmentar(e, eje)
        except (SegmentacionProhibida, ValueError):
            return False
        return True

    def nacionales(self):
        return [
            e for e in self.entradas.values()
            if e.clase is Clase.MEDIDO_NACIONAL
        ]
