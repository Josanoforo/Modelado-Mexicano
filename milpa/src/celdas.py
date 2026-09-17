"""`D`, el vector de atributos, y la malla de celdas.

LA MALLA ES MIXTA, y el módulo lo hace cumplir en vez de recordarlo: un agente
hereda TRES coordenadas de su hogar (urbanización, ingreso, acceso digital) y
porta TRES propias (formalidad, edad, migración) —
`canon/modelo-decision-v4_0.md` §1.1.A, veredicto de P1.

Consecuencia ejecutable: ninguna condicional puede definirse por contraste
intra-hogar en los tres ejes de hogar. `Cortes` lo valida AL CONSTRUIRSE, no al
usarse — un contrato que sólo se comprueba en el punto de uso ya se violó
varias veces antes de fallar.
"""

from dataclasses import dataclass

from .clases import EJES, EJES_HOGAR


class ContrasteIntraHogarProhibido(ValueError):
    """Se pidió contraste intra-hogar en un eje de hogar.

    No es una celda vacía por muestra pequeña: es vacía POR DISEÑO DEL
    INSTRUMENTO. Ninguna muestra mayor la llena.
    """


class CortesNoSellados(RuntimeError):
    """Se pidió construir con cortes que no traen la firma de M2."""


@dataclass(frozen=True)
class Cortes:
    """Los cortes por eje. `None` = corte PENDIENTE, declarado, no inventado.

    Los cortes sellados en el COMMIT C1 son los que el propio instrumento ya
    trae en catálogo. Edad y migración quedan `None`: definir ese corte exige
    dato mexicano propio y es acto por sí mismo (`FP-53`).
    """

    por_eje: dict
    firma_m2: str
    intra_hogar: tuple = ()

    def __post_init__(self):
        if not self.firma_m2:
            raise CortesNoSellados(
                "los cortes no traen la firma de M2 (`ADR-100(2)`)"
            )
        for eje in self.por_eje:
            if eje not in EJES:
                raise ValueError(
                    f"`{eje}` no es uno de los seis ejes de §1.1.A: {EJES}"
                )
        malos = [e for e in self.intra_hogar if e in EJES_HOGAR]
        if malos:
            raise ContrasteIntraHogarProhibido(
                f"{malos} son ejes de HOGAR: todas las personas del mismo "
                f"hogar comparten su valor. Esa varianza no existe en ENIGH — "
                f"por diseño del instrumento, no por hueco de muestra."
            )

    @property
    def sellados(self):
        return tuple(e for e, v in sorted(self.por_eje.items()) if v)

    @property
    def pendientes(self):
        return tuple(e for e, v in sorted(self.por_eje.items()) if not v)


#: Los cortes iniciales sellados por el COMMIT C1 de este acto, bajo M2.
#: Se declaran aquí como DATO, no se re-derivan: el catálogo es su sitio de
#: sello y este módulo lo consume.
CORTES_C1 = Cortes(
    por_eje={
        "formalidad": ("segsoc=1", "segsoc=2"),
        # PENDIENTE — FP-53   [línea original del sello del 17/ago/2026; NO se borra]
        # ENMIENDA FECHADA 17/sep/2026 · ACTO GEN2-CORTE-EDAD-1 · ADR-534:
        #   resuelto por ADR-534; FP-53 era otro objeto. FP-53 quedó FIRMADA el
        #   18/ago/2026 (ADR-111(b), ejecutada por ADR-116, PR #281) y fija el
        #   umbral binario «joven» = 15-29 para los 9 sitios de
        #   canon/modelo-decision-v4_0.md. Este corte es un objeto DISTINTO: la
        #   partición en cuatro tramos de las celdas del modelo. El comentario
        #   `PENDIENTE — FP-53` sobrevivió un mes a su propio bloqueador porque
        #   ningún acto posterior tocó este archivo sellado.
        # Firma que autoriza el sello: D4 de mesa, 16/sep/2026, archivada verbatim
        #   en forense/encargos/2026-09-16-GEN2-CORTE-EDAD-1.md; edición del dato
        #   sellado autorizada bajo ADR-100(2) con ADR-534 como fuente.
        # Variable de referencia (ENVIPE 2025, nivel persona, la base que esto corta):
        #   TSDem.EDAD, años cumplidos — envipe2025_csv.zip sha256_12 8a7a99fd90ce.
        #   Verificación por definición sobre los tres FD (ENVIPE 2025 / ENCIG 2025 /
        #   ENIF 2024), con su reserva de no-respuesta pendiente de caja:
        #   forense/notas/2026-09-17-GEN2-CORTE-EDAD-1-p1-por-definicion.md
        # ⚠ `60+` es el RÓTULO; la operación del árbitro
        #   (tools/ejes_maestra35_l1.py::tramos_edad) topa en 96: todo valor ≥ 97
        #   cae a «(fuera)», igual que un blanco. No leer `60+` como «60 y más».
        "edad": ("18-29", "30-44", "45-59", "60+"),
        "urbanizacion": ("1", "2", "3", "4"),          # tam_loc
        "ingreso": ("1", "2", "3", "4"),               # est_socio
        "acceso_digital": ("1", "2"),                  # tenencia binaria
        "migracion": None,                  # PENDIENTE — 34 categorías
    },
    firma_m2=(
        "ADR-100(2) · ACTO LANE-A-E0-E5 C1 · catalogo-momentos v0.1 §3"
        " || ADR-534 · ACTO GEN2-CORTE-EDAD-1 · firma D4 de mesa 16/sep/2026"
        " (eje `edad`, cuatro tramos; los demás ejes sin tocar)"
    ),
)


@dataclass(frozen=True)
class Celda:
    """Una celda de la malla `D`. Sólo los ejes con corte sellado."""

    coordenadas: tuple    # ((eje, valor), ...) ordenado

    def como_dict(self):
        return dict(self.coordenadas)

    def __str__(self):
        return "·".join(f"{e}={v}" for e, v in self.coordenadas)


def celda(cortes=None, **coords):
    cortes = cortes or CORTES_C1
    for eje in coords:
        if eje not in cortes.por_eje:
            raise ValueError(f"`{eje}` no está en los cortes")
        if cortes.por_eje[eje] is None:
            raise CortesNoSellados(
                # ENMIENDA FECHADA 17/sep/2026 · ACTO GEN2-CORTE-EDAD-1 · ADR-534.
                # El texto anterior citaba `FP-53` como bloqueador de CUALQUIER eje
                # pendiente. Nunca fue cierto para `migracion` (su pendiente es «34
                # categorías») y dejó de serlo para `edad`, sellado por este acto.
                # Un bloqueador se cita por su nombre sólo donde de verdad bloquea.
                f"el corte de `{eje}` está PENDIENTE: no se inventa aquí. "
                f"Definirlo exige dato mexicano propio y es acto propio."
            )
    return Celda(coordenadas=tuple(sorted(coords.items())))
