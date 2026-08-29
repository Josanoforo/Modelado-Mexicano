"""`B` y `g(x) = B·θ(x)` — con las advertencias que se pierden al reformular.

`B` se lee de `asignados_coeficiente.detalle`, con clave compuesta
**`(generador, coeficiente)`** — obligatorio, porque seis nombres de
coeficiente se repiten entre generadores (`confianza_institucional` en G1 y G4,
`aversion_riesgo` en G2 y G3, `horizonte_temporal` en G3 y G4,
`familismo_apoyo` en G3 y G5, `radio_confianza` en G1 y G5, `sens_estatus` en
G2 y G4). Es la misma clave compuesta que ya usa
`rutas_estimabilidad_coeficiente.detalle`.

DOS ADVERTENCIAS QUE ESTE MÓDULO CONSERVA POR DISEÑO, porque son justamente
las que se pierden al cambiar de formalismo:

1. EL ERROR DE CATEGORÍA. Sumar los 22 grados de libertad del ajuste y las
   condicionales medidas "sería un error de categoría" (`canon/modelo-decision-v4_0.md`).
   La matriz lo hace MÁS fácil, no menos: pone β y θ en el mismo objeto
   algebraico donde nada en la notación recuerda que unos se ajustan y otras se
   miden. Por eso `Coeficiente` y `Condicional` son tipos DISTINTOS aquí y no
   existe ninguna operación que los sume.

2. M5 y M7 de RONDA-M, cableados. Las salidas del ajuste son
   **14 puntuales + 1 sin magnitud**, nunca "15"; y los parámetros de forma de
   `h_r` quedan FUERA de los 22 por declaración, con un assert que falla si
   alguno se marca ajustable sin recontar el denominador.
"""

from dataclasses import dataclass

from .clases import SinMagnitud

#: M7 de RONDA-M, verbatim del fix: "los parámetros de forma de `h_r` quedan
#: FIJOS por declaración y fuera de los 22; si alguno se ajusta, se cuenta y el
#: 22 deja de ser el denominador".
GRADOS_DE_LIBERTAD_DEL_AJUSTE = 22


@dataclass(frozen=True)
class Coeficiente:
    """Una celda de `B`. Se AJUSTA. Nunca se suma con una `Condicional`."""

    generador: str
    nombre: str
    valor: float


@dataclass(frozen=True)
class CoeficienteSinMagnitud:
    """Una celda de `B` cuyo valor es texto, no número.

    Caso real y único: `G5 × familismo_obligacion`. No es un 0 y no es un
    faltante: es un signo sostenido sin magnitud sostenida. Cargarla como
    `0.0` la volvería inocua en el cómputo, que es exactamente el error.
    """

    generador: str
    nombre: str
    literal: str


@dataclass(frozen=True)
class Condicional:
    """Un θ_k(x). Se MIDE. Nunca se suma con un `Coeficiente`."""

    nombre: str
    clase: str


@dataclass
class Matriz:
    celdas: dict          # (gen, coef) -> Coeficiente | CoeficienteSinMagnitud

    @property
    def generadores(self):
        return tuple(sorted({g for g, _ in self.celdas}))

    @property
    def no_cero(self):
        return len(self.celdas)

    @property
    def puntuales(self):
        return [c for c in self.celdas.values() if isinstance(c, Coeficiente)]

    @property
    def sin_magnitud(self):
        return [
            c for c in self.celdas.values()
            if isinstance(c, CoeficienteSinMagnitud)
        ]


def cargar_B(procedencia):
    """`B` desde `asignados_coeficiente.detalle`, clave compuesta.

    `G5 × familismo_obligacion` carga como `CoeficienteSinMagnitud`, no como
    `float` y no como ausencia.

    ADR-220 (`ACTO MAESTRA32-E1 · SELLA-ENLACE`, firma de mesa `M-ENLACE=A`):
    tras construir las 15 celdas de siempre (fallback intacto, arriba), se
    sobre-escribe SOLO la celda de un par que traiga `valor_ejecutable` en
    `coeficientes_generador_sellados` -- la sección nueva de
    `milpa/procedencia.yaml` donde vive el enlace identidad sellado (rótulo
    `ASOCIACION-MEDIDA`, `M-176`; nunca coeficiente identificado, A-bis 3).
    Los 10 pares sin medición y los 2 multi-ítem (`SELLADO-ESCALA·SIN-
    AGREGACION`, `M-AGREGA=(a)`, sin `valor_ejecutable` por diseño) NO se
    tocan aquí -- siguen exactamente el `ASIGNADO` de siempre. El conteo de
    celdas no cambia (15 antes, 15 después): solo el *valor* de las que
    traen override.
    """
    detalle = procedencia.crudo["asignados_coeficiente"]["detalle"]
    celdas = {}
    for fila in detalle:
        gen = fila["gen"]
        for nombre, valor in fila["coefs"].items():
            clave = (gen, nombre)
            if isinstance(valor, (int, float)):
                celdas[clave] = Coeficiente(gen, nombre, float(valor))
            else:
                celdas[clave] = CoeficienteSinMagnitud(gen, nombre, str(valor))

    sellados = procedencia.crudo.get("coeficientes_generador_sellados") or ()
    for entrada in sellados:
        if "valor_ejecutable" not in entrada:
            continue  # multi-ítem SELLADO-ESCALA·SIN-AGREGACION: no se consume aquí
        gen, nombre = entrada["gen"], entrada["coef"]
        clave = (gen, nombre)
        if clave not in celdas:
            # Defensivo, no debería ocurrir: un par sellado que no exista en
            # `asignados_coeficiente.detalle` es una discrepancia de datos,
            # no algo que este cargador deba silenciar fabricando una celda
            # nueva -- se deja el fallback intacto y se ignora el override.
            continue
        celdas[clave] = Coeficiente(gen, nombre, float(entrada["valor_ejecutable"]))

    return Matriz(celdas=celdas)


def g(matriz, theta, celda):
    """`g(x) = B·θ(x)`, por generador.

    Lanza `SinMagnitud` si una celda participante no tiene número. NO la trata
    como cero: un parámetro sin magnitud no es un parámetro nulo, y hacerlo
    pasar por cero es la manera silenciosa de que el modelo produzca un número
    que nadie sostiene.
    """
    # La comprobación de contrato va ANTES de tocar θ, no entremezclada con
    # el cómputo: si depende del orden de iteración, es una comprobación que
    # a veces no ocurre.
    for celda_B in matriz.celdas.values():
        if isinstance(celda_B, CoeficienteSinMagnitud):
            raise SinMagnitud(
                f"`{celda_B.generador} × {celda_B.nombre}`: "
                f"{celda_B.literal}. No se computa como cero — decidir su "
                f"forma es acto propio."
            )
    salida = {}
    for (gen, nombre), celda_B in matriz.celdas.items():
        valor_theta = theta.valor(nombre, celda)
        salida[gen] = salida.get(gen, 0.0) + celda_B.valor * valor_theta
    return salida


def verificar_denominador(parametros_hr_ajustables):
    """M7 de RONDA-M, ejecutable.

    Si algún parámetro de forma de `h_r` se marca ajustable, el 22 deja de ser
    el denominador y este assert lo dice antes de que ninguna cifra salga.
    """
    if parametros_hr_ajustables:
        raise AssertionError(
            f"{len(parametros_hr_ajustables)} parámetro(s) de forma de `h_r` "
            f"marcados ajustables: {sorted(parametros_hr_ajustables)}. El "
            f"denominador deja de ser {GRADOS_DE_LIBERTAD_DEL_AJUSTE} y hay "
            f"que recontarlo — M7 de RONDA-M."
        )
    return GRADOS_DE_LIBERTAD_DEL_AJUSTE
