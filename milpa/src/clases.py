"""La taxonomía de procedencia y sus reglas de uso.

EL HALLAZGO QUE FIJA EL DISEÑO (medido, no supuesto): las clases de
procedencia viven en COMENTARIOS `#` de `milpa/procedencia.yaml`, no en datos
— `yaml.safe_load` las descarta. Y el campo `clase:` usa en la práctica más
vocabularios que los siete del encabezado: además de ellos aparecen
`PENDIENTE`, `MEDIDO·β̂(...)` y `GATE·ID-X`.

REGLA DE DISEÑO, NO NEGOCIABLE: `clase` se resuelve por PREFIX-MATCH, jamás
por igualdad. Un enum cerrado rechazaría entradas reales del archivo: los
valores no son etiquetas limpias — `MEDIDO·PARCIAL(formalidad,edad,...)` lleva
sus ejes dentro del propio valor y `GATE·ID-X -- ...` lleva un párrafo entero.

TRAMPAS DE CODIFICACIÓN que este módulo encapsula (medidas, no supuestas):
  `·` U+00B7 · `→` U+2192 · `∅` U+2205 · `—` U+2014
  `β̂` son DOS code points (U+03B2 + U+0302).
Llaves con no-ASCII (`educación`, `norma_de_género`) y con guiones
(`seguridad-FFAA`): acceso siempre por `dict[...]`, nunca por atributo.
Apertura siempre con `encoding='utf-8'`.
"""

from enum import Enum


class ClaseDesconocida(ValueError):
    """Ningún prefijo conocido casa con el valor crudo de `clase:`.

    Se lanza en vez de adivinar. Una clase nueva en el archivo tiene que
    llegar aquí por edición declarada, no por caer en un `else`.
    """


class SegmentacionProhibida(ValueError):
    """Se intentó segmentar por eje una entrada `MEDIDO·NACIONAL` (x = ∅).

    `milpa/procedencia.yaml` lo declara: admitir una θ a esta clase NO abre su
    condicional por eje. Quien la necesite corre la medición condicionada
    aparte (puerta D3-B).
    """


class EjeNoDeclarado(ValueError):
    """Se intentó segmentar `MEDIDO·PARCIAL(x)` por un eje fuera de su `x`."""


class GateDetiene(RuntimeError):
    """Se intentó usar una entrada `GATE·ID` como estimando.

    El gate detiene, no estima (`GATE·ID-X`, verbatim del archivo:
    "compuerta de identificación inalcanzable por construcción ... NO es una
    estimación: el gate detiene el acto antes de cruzar exposición contra
    desenlace").
    """


class SinMagnitud(ValueError):
    """Una celda participante no tiene número.

    Caso real y único hoy: `G5 × familismo_obligacion`, cuyo valor literal en
    `milpa/procedencia.yaml` es la cadena
    "signo negativo o no monotónico — SIN MAGNITUD".
    """


class Clase(Enum):
    """Las clases de procedencia, como PREFIJOS.

    El orden de declaración no importa; la resolución usa el prefijo más
    largo que case, para que `MEDIDO·PARCIAL` gane sobre `MEDIDO`.
    """

    MEDIDO = "MEDIDO"
    DERIVADO = "DERIVADO"
    ORDINAL_CARDINAL = "ORDINAL→CARDINAL"
    ASIGNADO = "ASIGNADO"
    AJUSTADO = "AJUSTADO"
    MEDIDO_PARCIAL = "MEDIDO·PARCIAL"      # prefijo; los ejes van en el valor
    MEDIDO_NACIONAL = "MEDIDO·NACIONAL"    # x = ∅ declarado, no omitido
    PENDIENTE = "PENDIENTE"
    MEDIDO_BETA = "MEDIDO·β̂"    # dos code points: β + U+0302
    GATE_ID = "GATE·ID"


def clasificar(valor):
    """Resuelve por prefijo el valor crudo de `clase:`.

    Devuelve `(Clase, resto)`, donde `resto` es lo que sigue al prefijo — que
    NO se descarta: ahí viven los ejes de `MEDIDO·PARCIAL(x)` y el párrafo de
    `GATE·ID-X`.

    Lanza `ClaseDesconocida` si ningún prefijo casa. Nunca adivina.
    """
    if not isinstance(valor, str):
        raise ClaseDesconocida(f"`clase:` no es texto: {valor!r}")
    v = valor.strip()
    casan = [c for c in Clase if v.startswith(c.value)]
    if not casan:
        raise ClaseDesconocida(f"ningún prefijo conocido casa con {valor!r}")
    # prefijo más largo: `MEDIDO·PARCIAL` gana sobre `MEDIDO`.
    c = max(casan, key=lambda k: len(k.value))
    return c, v[len(c.value):]


def ejes_declarados(valor):
    """Extrae los ejes de `MEDIDO·PARCIAL(a,b,c)`.

    Devuelve `()` para `MEDIDO·NACIONAL` — x = ∅ DECLARADO, que es
    precisamente lo que `MEDIDO·PARCIAL(x)` no admite. Devuelve `()` para
    cualquier otra clase: no tienen ejes que declarar.
    """
    clase, resto = clasificar(valor)
    if clase is not Clase.MEDIDO_PARCIAL:
        return ()
    if not resto.startswith("("):
        return ()
    cierre = resto.find(")")
    if cierre < 0:
        return ()
    dentro = resto[1:cierre]
    return tuple(e.strip() for e in dentro.split(",") if e.strip())


#: Ejes de hogar de `canon/modelo-decision-v4_0.md` §1.1.A — coordenadas
#: COMPARTIDAS por todas las personas del hogar. Ninguna condicional puede
#: definirse por contraste intra-hogar en estos tres: no es una celda vacía por
#: muestra pequeña, es vacía POR DISEÑO DEL INSTRUMENTO (veredicto de P1).
EJES_HOGAR = ("urbanizacion", "ingreso", "acceso_digital")

#: Ejes de persona del mismo vector: sí varían persona a persona.
EJES_PERSONA = ("formalidad", "edad", "migracion")

#: Los seis del vector de atributos observables, en el orden de §1.1.A.
EJES = ("formalidad", "edad", "urbanizacion", "ingreso", "acceso_digital", "migracion")
