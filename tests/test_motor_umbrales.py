#!/usr/bin/env python3
"""Los 7 umbrales go/no-go de `ADR-68(c)` como ASSERTS EJECUTABLES, con su
texto verbatim -- y `skip`-hasta-datos permitido, texto verbatim obligatorio.

DOS FUENTES, NO UNA. El encargo pide "texto verbatim", y `gobernanza:912`
(ADR-68(c)) sólo dice "se adoptan los siete de Ronda 1 §7 con dos ajustes de
mesa". El texto de los siete vive en
`forense/RONDA1-motor-adaptativo-celda-veredicto-fable-2026-08-11-v1_0.md` §7,
y los dos ajustes en `gobernanza`. La transcripción se compone de las dos y
este test verifica que ambas siguen ahí -- si una se edita, el verbatim deja de
serlo y esto lo dice.
"""

import os
import re

from _motor_arnes import RAIZ, Arnes, cierto, igual, saltar  # noqa: E402

from milpa.src import momentos as MM  # noqa: E402
from milpa.src import motor  # noqa: E402

RONDA1 = os.path.join(
    RAIZ, "forense",
    "RONDA1-motor-adaptativo-celda-veredicto-fable-2026-08-11-v1_0.md")
GOBERNANZA = os.path.join(RAIZ, "canon", "gobernanza-v1_15.md")

#: Los siete, verbatim de Ronda 1 §7. Fragmento textual + qué mide.
UMBRALES = (
    (1, "commit_declaracion` anterior en historia de git a todo resultado",
     "10-15 celdas-D FIN registradas con la clave corregida"),
    (2, "≥1 donde el challenger gana y ≥1 donde el baseline retiene",
     "Discriminación en ambas direcciones"),
    (3, "sin colapsar banda→punto",
     "Heterogeneidad compilable"),
    (4, "≥1 negativo informativo registrado con estado, no con prosa",
     "negativo informativo"),
    (5, "Coherencia conjunta ejecutada",
     "D8"),
    (6, "contadores movidos = 0 salvo ADR",
     "Gobernanza intacta"),
    (7, "horas/celda y bloqueos por clase",
     "Costo medido"),
)

#: Los dos ajustes de mesa, verbatim de `gobernanza` ADR-68(c).
AJUSTES = (
    "empate declarado = empate, no se adjudica",
    "sin escribir en `milpa/`",
)

#: Transversal, verbatim del mismo inciso.
TRANSVERSAL = "cada umbral se evalúa al cierre con conteos derivados por comando a la vista"

#: El gate de semana 1 REDEFINIDO por ADR-68(b) -- no el original.
GATE_SEMANA_1 = "nunca una impresión"


def _leer(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def main():
    a = Arnes("T-MOTOR-UMBRALES")
    ronda1 = _leer(RONDA1)
    gob = _leer(GOBERNANZA)
    seccion = re.search(r"^## 7 · Criterio go/no-go.*?(?=^---)", ronda1,
                        re.M | re.S)

    def test_los_siete_estan_verbatim_en_ronda1():
        cierto(seccion is not None, "no se encontró §7 en el veredicto de Ronda 1")
        txt = seccion.group(0)
        for n, fragmento, _ in UMBRALES:
            cierto(fragmento in txt,
                   f"umbral {n}: el texto verbatim ya no está en Ronda 1 §7 "
                   f"-- {fragmento!r}")

    def test_son_siete_ni_uno_mas():
        txt = seccion.group(0)
        numerados = re.findall(r"^\d+\. ", txt, re.M)
        igual(len(numerados), 7, "umbrales numerados en Ronda 1 §7:")

    def test_los_dos_ajustes_de_mesa_estan_verbatim():
        for frag in AJUSTES:
            cierto(frag in gob,
                   f"ajuste de mesa de ADR-68(c) ya no está verbatim: {frag!r}")

    def test_transversal_verbatim():
        cierto(TRANSVERSAL in gob,
               "la cláusula transversal de ADR-68(c) cambió de texto")

    def test_gate_semana_1_es_el_redefinido():
        cierto(GATE_SEMANA_1 in gob,
               "el gate de semana 1 REDEFINIDO por ADR-68(b) cambió de texto")

    # ── Los umbrales como asserts sobre el estado real ────────────────────
    # `skip`-hasta-datos permitido: en E0 no hay corridas, y cinco de los siete
    # no pueden evaluarse sin ellas. Se dice cuál y por qué, en vez de darlos
    # por buenos.

    def test_umbral_1_commit_declaracion_anterior():
        # Lo verifica en detalle `tests/test_motor_holdout.py::test_c`. Aquí se
        # comprueba la mitad que sí es evaluable hoy: el catálogo existe y está
        # sellado.
        cat = MM.cargar_catalogo()
        cierto(cat.commit_sha, "el catálogo no trae `commit_sha` de sello")
        cierto(len(cat) >= 10,
               f"el umbral (1) pide 10-15 registradas; el catálogo trae "
               f"{len(cat)} momentos")

    def test_umbral_2_discriminacion():
        saltar("exige baseline y challenger EJECUTADOS; E0 no corre ninguno")

    def test_umbral_3_heterogeneidad():
        saltar("exige dry-run de compilación; E0 no compila hacia procedencia")

    def test_umbral_4_negativo_informativo():
        # Éste SÍ es evaluable hoy: la rebanada produce veredictos de estado,
        # no prosa, y al menos uno es negativo.
        salida = motor.correr(semilla=0)
        negativos = [r for r in salida["resultados"]
                     if r["veredicto"] in ("EXISTE-NO-SATISFACE",
                                           "NO-ENCONTRADO")]
        cierto(len(negativos) >= 1,
               "ningún negativo informativo registrado con estado")
        for r in salida["resultados"]:
            cierto(r["veredicto"] in motor.VEREDICTOS,
                   f"{r['celda_id']}: veredicto fuera del vocabulario A.4")

    def test_umbral_5_coherencia_conjunta():
        saltar("D8 exige corrida conjunta; E0 no calibra")

    def test_umbral_6_gobernanza_intacta():
        # Contadores movidos = 0 salvo ADR. El único contador que la rebanada
        # reporta es el de canon, replicado por la fórmula oficial de T19b: si
        # el motor produjera uno propio, aquí se vería.
        salida = motor.correr(semilla=0)
        igual(salida["holdout_reproducidos"], 0,
              "momentos HOLDOUT reproducidos:")
        cierto("contador_condicionales_medidas" in salida,
               "la salida no reporta el contador oficial")

    def test_umbral_7_costo_medido():
        saltar("horas/celda y bloqueos por clase se miden al cierre del piloto")

    for nombre, fn in sorted(locals().items()):
        if nombre.startswith("test_"):
            a.prueba(nombre, fn)
    return a.cerrar()


if __name__ == "__main__":
    raise SystemExit(main())
