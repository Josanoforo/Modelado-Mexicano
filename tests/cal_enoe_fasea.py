#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/cal_enoe_fasea.py — COMPUERTA 1 de CAL-ENOE Fase A: ¿existe el desenlace?

QUÉ PREGUNTA ESTE SCRIPT, Y NADA MÁS
------------------------------------
`milpa/procedencia.yaml:282-288` (`asignados_coeficiente.unico_calibrable_hoy`)
declara, textual:

    "El panel rotativo trimestral de la ENOE sigue al mismo hogar cinco
     trimestres. Permite observar a los MISMOS sujetos cruzando formal↔informal
     y estimar el cambio de conducta financiera asociado. Es la única
     elasticidad del modelo que México permite estimar con dato público."

La segunda oración contiene una premisa nunca verificada: **que ENOE mide
conducta financiera**. `horizonte_temporal` es un constructo de preferencia
temporal; ENOE es una encuesta de ocupación y empleo. Este script pregunta si
existe en el instrumento de ENOE alguna variable que operacionalice ese
constructo — es decir, si existe DESENLACE. Sin desenlace no hay elasticidad
que estimar, y la ruta de calibración declarada no existe.

Esto NO es CAL-G3. CAL-G3 (`forense/hitoD-preregistro-v2_0.md` Nota 7) está
sellada, su alcance era ENNViH olas 2-3 y su resultado está en la Nota 10. Este
script no la toca, no la enmienda y no la reabre. Por ADR-47
(`canon/gobernanza-v1_15.md`) CAL-ENOE es CALIBRACIÓN, no falsación: no emite
CAL-A/B/C/X y no entra al conteo de corridas archivadas.

QUÉ SE LEYÓ — declarado sin excepción
-------------------------------------
  · SOLO cuestionarios y documentación publicada, en PDF. **Ningún microdato se
    abrió**: ni un .csv, ni un .dta, ni se descomprimió ningún
    `conjunto_de_datos_*`. Los 28 ZIP trimestrales de ENOE/ENOEN registrados en
    `data/manifiesto.yaml` siguen sin inspeccionar por esta sesión.
  · NUEVE cuestionarios, 103 páginas de instrumento, que cubren SIN HUECO la
    ventana completa de los 28 trimestres bajados (2019T1-2026T1, sin 2020T2):
    seis bajados sueltos de la página de ENOE (eras clásica y post-2023) y tres
    más de la era ENOEN (2020T3-2022T4) extraídos del paquete de documentación
    `enoe_n_trim3_2020-trim4_2022.zip`. Ese ZIP trae seis cuestionarios; tres
    resultaron byte-idénticos a los ya bajados sueltos (mismo sha256), así que
    aporta exactamente tres instrumentos nuevos.
  · El precedente de esta lectura es el "Segundo entregable" de la Nota 7
    (29/jul/2026), que ya registró el mismo hallazgo pero con evidencia
    explícitamente más débil, y así lo dijo: *"hallazgo 'no lo encontré', con
    cobertura a nivel de título de grupo, no de variable individual"*. Este
    script sustituye esa cobertura de título por lectura de REACTIVO.

MÉTODO
------
Sobre el texto completo de los nueve cuestionarios se corre un léxico de 45
términos de ahorro / crédito / deuda / planeación / expectativas / preferencia
temporal. **Todo acierto se adjudica**, uno por uno, contra el reactivo en que
vive. La adjudicación está transcrita abajo en `ADJUDICACION` y es verificable
término por término contra los PDF.

La prueba está construida para FALLAR si alguien la contradice: si al re-correr
contra los PDF aparece un acierto que no está en el inventario adjudicado, el
script sale con código 1 y lo nombra. Un desenlace que apareciera después
rompería esta corrida en vez de pasar inadvertido — que es justo lo que la
lección de la batería TB33 (Nota 10, punto (e)) pide de un chequeo previo.

MODOS
-----
    python3 tests/cal_enoe_fasea.py
        Modo transcripción. No necesita los PDF. Imprime el inventario
        adjudicado y el veredicto. Verifica la consistencia interna del
        inventario. Es el modo que corre en cualquier máquina.

    python3 tests/cal_enoe_fasea.py --docs <DIR>
        Modo verificación. Re-deriva todo desde los PDF que encuentre bajo
        <DIR>, RECURSIVAMENTE (los tres de la era ENOEN viven en subcarpetas
        del ZIP de documentación): comprueba los nueve sha256, re-extrae el
        texto con `pdftotext -layout` y vuelve a correr el léxico. FALLA si
        algún hash no coincide, si algún conteo se mueve, o si aparece un
        acierto no adjudicado. Requiere `pdftotext` (poppler-utils).

CÓMO SE REPRODUCE, de cero
--------------------------
  1. Bajar los seis cuestionarios sueltos de la página de ENOE de INEGI
     (públicos, y registrados en `data/manifiesto.yaml` con sha256):
         https://www.inegi.org.mx/contenidos/programas/enoe/15ymas/doc/c_bas_v5.pdf
         https://www.inegi.org.mx/contenidos/programas/enoe/15ymas/doc/c_bas_v7.pdf
         https://www.inegi.org.mx/contenidos/programas/enoe/15ymas/doc/c_amp_v5.pdf
         https://www.inegi.org.mx/contenidos/programas/enoe/15ymas/doc/c_amp_v6a.pdf
         https://www.inegi.org.mx/contenidos/programas/enoe/15ymas/doc/c_sdem_v4.pdf
         https://www.inegi.org.mx/contenidos/programas/enoe/15ymas/doc/c_sdem_v5a.pdf
  2. Bajar el paquete de documentación de la era ENOEN y sacar de él los tres
     cuestionarios de `4. Cuestionarios/` que no estén ya en el paso 1
     (c_bas_v6, c_amp_v6, c_sdem_v5):
         https://www.inegi.org.mx/contenidos/programas/enoe/15ymas/doc/enoe_n_trim3_2020-trim4_2022.zip
  3. python3 tests/cal_enoe_fasea.py --docs <directorio con los nueve PDF>
  Sin dependencias externas: stdlib + `pdftotext` solo en modo verificación.

Salida narrada en `forense/notas/2026-07-31-cal-enoe-fasea.md`.
"""

import io
import os
import re
import sys
import json
import hashlib
import subprocess
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FALLOS = []


# ---------------------------------------------------------------------------
# Los nueve cuestionarios. Los seis primeros llevan sha256 transcrito de
# data/manifiesto.yaml, donde quedaron registrados el 30/jul/2026 con su
# url_origen y su entorno de descarga; su cobertura temporal es la que el
# propio manifiesto declara en el campo `formato` de cada entrada. Los tres
# últimos son de la era ENOEN y su procedencia se detalla en su bloque.
# ---------------------------------------------------------------------------

CUESTIONARIOS = {
    "c_bas_v5": {
        "sha256": "1ab575a4d098991cca2e5a5355b32eb1f91a24d7625ec1778164693532287a3f",
        "tipo": "básico",
        "cobertura": "trimestres 2-3-4 de 2016-2019",
        "manifiesto_id": "enoe_cuestionario_basico_v5_pdf",
        "paginas": 12,
    },
    "c_bas_v7": {
        "sha256": "7ee25f114a493cd4136bb086f7fa3a2f6db1fe7300dc5839ec2a7de9c3efa698",
        "tipo": "básico",
        "cobertura": "trimestres 2-3-4 de 2023-2025",
        "manifiesto_id": "enoe_cuestionario_basico_v7_pdf",
        "paginas": 11,
    },
    "c_amp_v5": {
        "sha256": "4de904621507815e5b7c5af6262fe3202f5df4a0f3c4985d738d9f971dd70491",
        "tipo": "ampliado",
        "cobertura": "trimestre 1 de cada año 2016-2020",
        "manifiesto_id": "enoe_cuestionario_ampliado_v5_pdf",
        "paginas": 15,
    },
    "c_amp_v6a": {
        "sha256": "5e0cc786566fa6c891c53bb14f7e110ce205ff7da43c25a5f781d6b38218046c",
        "tipo": "ampliado",
        "cobertura": "trimestre 1 de cada año 2023-2026",
        "manifiesto_id": "enoe_cuestionario_ampliado_v6a_pdf",
        "paginas": 14,
    },
    "c_sdem_v4": {
        "sha256": "0c918e799a8ed1d3764b1e0a390a868138228cbec82b5aa723f4b3a2e2f2d00f",
        "tipo": "sociodemográfico",
        "cobertura": "trimestre 2 de 2016 a trimestre 1 de 2020",
        "manifiesto_id": "enoe_cuestionario_sociodemografico_v4_pdf",
        "paginas": 2,
    },
    "c_sdem_v5a": {
        "sha256": "e306c67a6551c08c3c4d65586a09cee1356e7017699c54deed6fdfe9c73708cf",
        "tipo": "sociodemográfico",
        "cobertura": "a partir de trimestre 1 de 2023",
        "manifiesto_id": "enoe_cuestionario_sociodemografico_v5a_pdf",
        "paginas": 10,
    },
    # --- era ENOEN (2020T3-2022T4) -------------------------------------------
    # Estos tres NO están registrados por separado en data/manifiesto.yaml:
    # viajan dentro de `enoe_n_trim3_2020-trim4_2022.zip`, cuyo sha256 SÍ está
    # registrado (id enoen_trim3_2020_trim4_2022_documentacion_zip,
    # 2a25ab364e282cf1caff5a45b29ba104a26a38d7fda88fe1720b89ae299f7ed1). La
    # ruta dentro del ZIP es `4. Cuestionarios/<tipo>/<trimestres>/<archivo>`.
    # El ZIP trae seis cuestionarios; los otros tres (c_amp_v5, c_bas_v5,
    # c_sdem_v4) resultaron BYTE-IDÉNTICOS a los ya listados arriba — mismo
    # sha256, verificado — así que la era ENOEN aporta exactamente estos tres
    # instrumentos nuevos y ninguno más.
    "c_bas_v6": {
        "sha256": "81ecf71165eef4b8bb78d2848bc0e199eaa279e5a8869ee4794d5aee37eb9153",
        "tipo": "básico",
        "cobertura": "ENOEN · trim. 3-4 de 2021 y 2-3-4 de 2022",
        "manifiesto_id": "enoen_trim3_2020_trim4_2022_documentacion_zip (dentro del ZIP)",
        "paginas": 13,
    },
    "c_amp_v6": {
        "sha256": "823c012e656182c1b9eff5b68dbf3d7d1b634463d638692a5ea04f9be12d3329",
        "tipo": "ampliado",
        "cobertura": "ENOEN · trimestre 1 de 2022",
        "manifiesto_id": "enoen_trim3_2020_trim4_2022_documentacion_zip (dentro del ZIP)",
        "paginas": 15,
    },
    "c_sdem_v5": {
        "sha256": "2e81f1f34063d3b8fc0aa38c420fdd9eccb7ec0356c5e388399c0e73f7bfc1d0",
        "tipo": "sociodemográfico",
        "cobertura": "ENOEN · trim. 3 de 2021 al trim. 4 de 2022",
        "manifiesto_id": "enoen_trim3_2020_trim4_2022_documentacion_zip (dentro del ZIP)",
        "paginas": 11,
    },
}


# ---------------------------------------------------------------------------
# El léxico. 44 términos. Se busca sobre texto normalizado (minúsculas, sin
# diacríticos) con frontera de palabra a la izquierda, de modo que `retiro`
# no capture `retirose` pero sí `retiro`/`retiró`, y `sar` no capture `pasar`.
#
# Criterio de construcción, declarado: cubre las CUATRO familias con las que
# la literatura operacionaliza preferencia temporal en encuesta de hogar —
# (i) acervo y vehículo de ahorro, (ii) crédito y deuda, (iii) horizonte de
# planeación declarado, (iv) expectativas sobre el futuro — más los nombres
# propios de las instituciones mexicanas de cada familia. No se estrecha para
# que el resultado salga; se ensancha para que, si hay algo, caiga dentro.
# ---------------------------------------------------------------------------

LEXICO = [
    # (i) ahorro: acervo y vehículo
    "ahorr", "tanda", "alcanci", "cooperativa", "caja popular", "afore",
    "invers", "invert", "patrimoni", "herenc",
    # (ii) crédito y deuda
    "credit", "microcredit", "prestam", "deuda", "endeud", "empen", "hipotec",
    "tarjeta de credito", "mensualidad", "abono", "plazos", "agiotist",
    "fiado", "infonavit", "fovissste",
    # instituciones financieras y de aseguramiento
    "banco", "bancari", "aseguradora", "seguro", "financ", "remesa",
    # (iii) horizonte de planeación declarado
    "planea", "planific", "previs", "largo plazo", "corto plazo",
    "posterga", "impacien", "paciencia", "presupuest", "retiro",
    # (iv) expectativas
    "futuro", "expectativ",
    # estatus de retiro (frontera del constructo: se incluye para adjudicarlo,
    # no porque se espere que sea desenlace)
    "pension", "jubil",
]


# ---------------------------------------------------------------------------
# INVENTARIO ADJUDICADO. Conteo por término y por cuestionario, y la clase a
# la que pertenece cada acierto. Transcrito de la lectura del 31/jul/2026;
# verificable contra los PDF con `--docs`.
#
# Las nueve clases, y por qué NINGUNA es horizonte_temporal:
#
#  A · PRESTACIÓN QUE OTORGA EL PATRÓN (ampliado 3l/3m). El enunciado literal
#      es "En este trabajo, ¿a ... le dan, AUNQUE NO UTILICE, ...?". Mide
#      provisión del empleador, y el "aunque no utilice" excluye por diseño
#      del instrumento la toma o el uso por parte del sujeto. Además es casi
#      colineal con la exposición: la prestación laboral es ingrediente de la
#      definición operativa de formalidad, así que usarla de desenlace sería
#      regresar formalidad sobre sí misma.
#  B · ACCESO A INSTITUCIÓN DE SALUD POR EL TRABAJO (6d/7d/9k). IMSS, ISSSTE,
#      Pemex/naval/militar, Seguro Popular. Es el marcador de formalidad, es
#      decir LA EXPOSICIÓN, no un desenlace.
#  C · CONDICIÓN DE ACTIVIDAD / MOTIVO DE SEPARACIÓN. "pensionado o jubilado",
#      "se pensionó, jubiló o se retiró de su negocio", "lo forzaron a
#      pensionarse". Estatus laboral.
#  D · FUENTE DE INGRESO DERIVADA DE UN TRABAJO ANTERIOR. "pensión o
#      jubilación", "seguro de desempleo", "seguro de separación individual".
#      Origen del ingreso, no conducta de ahorro.
#  E · MOTIVO DE CIERRE O PARO DE LA UNIDAD ECONÓMICA. "Exceso de deudas o se
#      declaró en quiebra", "Falta de crédito para seguir operando", "Falta de
#      materias primas, financiamiento o clientes". Es lo más cercano a deuda
#      en toda la ENOE, y aun así es un motivo declarado sobre un NEGOCIO ya
#      cerrado, retrospectivo, no una medida de endeudamiento del hogar.
#  F · APOYO DE GOBIERNO RECIBIDO (sección X). "apoyo para realizar una
#      actividad por su cuenta (Procampo, microcréditos)". Recepción de
#      programa, no decisión de tomar crédito.
#  G · INSTRUCCIÓN AL ENTREVISTADOR. "Vender o empeñar sus bienes" aparece en
#      un recuadro ATENCIÓN que ordena corregir la secuencia si el informante
#      da eso como su trabajo. No es reactivo ni genera variable.
#  H · DESCRIPTOR DE LA UNIDAD ECONÓMICA. "cadena comercial, bancaria o de
#      servicios". Sector del empleador.
#  I · NOMBRE PROPIO DE PROGRAMA. "Jóvenes Construyendo el Futuro" — único
#      acierto de "futuro" en los seis cuestionarios.
# ---------------------------------------------------------------------------

ADJUDICACION = {
    "afore":     {"conteo": {"c_amp_v5": 1, "c_amp_v6a": 1, "c_amp_v6": 1}, "clase": "A",
                  "reactivo": "3m opción 4 · fondo de retiro (SAR o Afore)"},
    "ahorr":     {"conteo": {"c_amp_v5": 1, "c_amp_v6a": 1, "c_amp_v6": 1}, "clase": "A",
                  "reactivo": "3m opción 7 · préstamos personales y/o caja de ahorro"},
    "bancari":   {"conteo": {"c_bas_v5": 1, "c_bas_v7": 1,
                             "c_amp_v5": 1, "c_amp_v6a": 1, "c_bas_v6": 1, "c_amp_v6": 1}, "clase": "H",
                  "reactivo": "4c · cadena comercial, bancaria o de servicios"},
    "credit":    {"conteo": {"c_amp_v5": 2, "c_amp_v6a": 2, "c_amp_v6": 2}, "clase": "A+E",
                  "reactivo": "3m opción 1 · crédito para vivienda (Infonavit, "
                              "Fovissste) [A]; 9c · falta de crédito para seguir "
                              "operando [E]"},
    "microcredit": {"conteo": {"c_amp_v5": 1, "c_amp_v6a": 1, "c_amp_v6": 1}, "clase": "F",
                  "reactivo": "10 opción 2 · apoyo para realizar una actividad "
                              "por su cuenta (Procampo, microcréditos)"},
    "deuda":     {"conteo": {"c_amp_v5": 1, "c_amp_v6a": 1, "c_amp_v6": 1}, "clase": "E",
                  "reactivo": "9b opción 01 · exceso de deudas o se declaró en quiebra"},
    "empen":     {"conteo": {"c_bas_v5": 1, "c_bas_v7": 1,
                             "c_amp_v5": 1, "c_amp_v6a": 1, "c_bas_v6": 1, "c_amp_v6": 1}, "clase": "G",
                  "reactivo": "recuadro ATENCIÓN tras la pregunta 3 · "
                              "'Vender o empeñar sus bienes' → corrige la secuencia"},
    "financ":    {"conteo": {"c_bas_v5": 1, "c_bas_v7": 1,
                             "c_amp_v5": 1, "c_amp_v6a": 1, "c_bas_v6": 1, "c_amp_v6": 1}, "clase": "E",
                  "reactivo": "5f/5g opción 08 · falta de materias primas, "
                              "financiamiento o clientes"},
    "fovissste": {"conteo": {"c_amp_v5": 1, "c_amp_v6a": 1, "c_amp_v6": 1}, "clase": "A",
                  "reactivo": "3m opción 1 · crédito para vivienda (Infonavit, Fovissste)"},
    "infonavit": {"conteo": {"c_amp_v5": 1, "c_amp_v6a": 1, "c_amp_v6": 1}, "clase": "A",
                  "reactivo": "3m opción 1 · crédito para vivienda (Infonavit, Fovissste)"},
    "futuro":    {"conteo": {"c_amp_v6a": 1, "c_amp_v6": 1}, "clase": "I",
                  "reactivo": "10 opción 1 · beca de capacitación (jóvenes "
                              "construyendo el futuro)"},
    "jubil":     {"conteo": {"c_bas_v5": 2, "c_bas_v7": 2,
                             "c_amp_v5": 3, "c_amp_v6a": 3, "c_bas_v6": 2, "c_amp_v6": 3}, "clase": "C+D",
                  "reactivo": "2e · pensionado o jubilado [C]; 9d opción 4 · se "
                              "pensionó, jubiló o se retiró de su negocio [C]; "
                              "9i-bis opción 3 · pensión o jubilación [D]"},
    "pension":   {"conteo": {"c_bas_v5": 2, "c_bas_v7": 2,
                             "c_amp_v5": 4, "c_amp_v6a": 4, "c_bas_v6": 2, "c_amp_v6": 4}, "clase": "C+D",
                  "reactivo": "mismos reactivos que `jubil`, más 9c opción 05 · "
                              "lo forzaron a renunciar o a pensionarse [C]"},
    "prestam":   {"conteo": {"c_amp_v5": 1, "c_amp_v6a": 1, "c_amp_v6": 1}, "clase": "A",
                  "reactivo": "3m opción 7 · préstamos personales y/o caja de ahorro"},
    "retiro":    {"conteo": {"c_bas_v5": 1, "c_bas_v7": 1,
                             "c_amp_v5": 2, "c_amp_v6a": 2, "c_bas_v6": 1, "c_amp_v6": 2}, "clase": "A+C",
                  "reactivo": "3m opción 4 · fondo de retiro (SAR o Afore) [A]; "
                              "9d opción 4 · se retiró de su negocio [C]"},
    "seguro":    {"conteo": {"c_bas_v5": 1, "c_bas_v7": 1,
                             "c_amp_v5": 8, "c_amp_v6a": 8, "c_bas_v6": 1, "c_amp_v6": 8}, "clase": "A+B+D",
                  "reactivo": "6d/7d/9k · el Seguro Social (IMSS) y demás "
                              "instituciones médicas [B]; 10b · Seguro Popular "
                              "[B]; 3m opciones 5 y 6 · seguro de vida y seguro "
                              "privado de gastos médicos [A]; 9i-bis opciones 4 "
                              "y 5 · seguro de desempleo, seguro de separación "
                              "individual [D]"},
}

# Términos del léxico con CERO aciertos en los seis cuestionarios. Se listan
# porque el cero es el hallazgo: son los que nombran directamente el
# constructo, y ninguno aparece.
CERO_ACIERTOS_ESPERADOS = [
    "tanda", "alcanci", "cooperativa", "caja popular", "invers", "invert",
    "patrimoni", "herenc", "endeud", "hipotec", "tarjeta de credito",
    "mensualidad", "abono", "plazos", "agiotist", "fiado", "banco",
    "aseguradora", "remesa", "planea", "planific", "previs", "largo plazo",
    "corto plazo", "posterga", "impacien", "paciencia", "presupuest",
    "expectativ",
]

# Secciones de cada instrumento, transcritas de los encabezados en romanos.
# Ninguna es de finanzas del hogar. La del ampliado que más se le acerca —
# X. APOYOS ECONÓMICOS — resultó ser recepción de transferencias de gobierno
# y remesas en los últimos tres meses, es decir FUENTE DE INGRESO.
# Los instrumentos de la era ENOEN (c_bas_v6, c_amp_v6) llevan las mismas
# secciones más una "II. NO OCUPADOS" explícita, que en las versiones clásicas
# va sin encabezado propio. Ninguna sección nueva es de finanzas del hogar.
SECCIONES = {
    "básico (v5, v6, v7)": [
        "I. Condición de ocupación", "III. Contexto laboral",
        "IV. Características de la unidad económica",
        "V. Jornada y regularidad laboral", "VI. Ingresos y atención médica",
        "VII. Trabajo secundario", "VIII. Búsqueda de otro trabajo",
        "IX. Otras actividades",
    ],
    "ampliado (v5, v6, v6a)": [
        "I. Condición de ocupación", "III. Contexto laboral",
        "IV. Características de la unidad económica",
        "V. Jornada y regularidad laboral", "VI. Ingresos y atención médica",
        "VII. Trabajo secundario", "VIII. Búsqueda de otro trabajo",
        "IX. Antecedentes laborales", "X. Apoyos económicos",
        "XI. Otras actividades",
    ],
    "sociodemográfico (v4, v5, v5a)": [
        "I. Identificación geográfica / control de vivienda / domicilio",
        "II. Resultado de la entrevista", "III. Datos del personal operativo",
        "IV. Supervisión",
        "V. Residentes de la vivienda e identificación de hogares",
        "VI. Características sociodemográficas", "VII. Ausentes definitivos",
        "VIII. Nuevos residentes", "IX. Observaciones",
    ],
}


def norm(s):
    """Minúsculas sin diacríticos, para que `crédito` y `credito` sean el
    mismo término y el resultado no dependa de cómo el extractor de PDF
    resolvió los acentos."""
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def cuenta(texto, termino):
    return len(re.findall(r"\b" + re.escape(norm(termino)), norm(texto)))


def fail(msg):
    FALLOS.append(msg)


# ---------------------------------------------------------------------------
# Modo transcripción: consistencia interna
# ---------------------------------------------------------------------------

def verifica_inventario():
    """El inventario tiene que ser internamente coherente: todo término
    adjudicado está en el léxico, todo término de cero-esperado está en el
    léxico y NO está adjudicado, y ningún cuestionario citado es desconocido."""
    for t in ADJUDICACION:
        if t not in LEXICO:
            fail(f"término adjudicado '{t}' no está en LEXICO")
        for q in ADJUDICACION[t]["conteo"]:
            if q not in CUESTIONARIOS:
                fail(f"término '{t}' cita un cuestionario desconocido: '{q}'")
    for t in CERO_ACIERTOS_ESPERADOS:
        if t not in LEXICO:
            fail(f"término de cero-esperado '{t}' no está en LEXICO")
        if t in ADJUDICACION:
            fail(f"término '{t}' está a la vez en ADJUDICACION y en "
                 f"CERO_ACIERTOS_ESPERADOS")
    cubiertos = set(ADJUDICACION) | set(CERO_ACIERTOS_ESPERADOS)
    for t in LEXICO:
        if t not in cubiertos:
            fail(f"término '{t}' del léxico no está ni adjudicado ni declarado "
                 f"con cero aciertos — el inventario está incompleto")


# ---------------------------------------------------------------------------
# Modo verificación: re-deriva todo desde los PDF
# ---------------------------------------------------------------------------

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for bloque in iter(lambda: fh.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def extrae(path):
    r = subprocess.run(["pdftotext", "-layout", path, "-"],
                       capture_output=True)
    if r.returncode != 0:
        fail(f"pdftotext falló sobre {os.path.basename(path)}: "
             f"{r.stderr.decode('utf-8', 'replace')[:200]}")
        return ""
    return r.stdout.decode("utf-8", "replace")


def verifica_contra_pdf(docdir):
    print(f"  directorio de documentos: {docdir}")
    print()
    # Búsqueda RECURSIVA: los tres cuestionarios de la era ENOEN viven en
    # subcarpetas (`4. Cuestionarios/<tipo>/<trimestres>/`) cuando se extrae el
    # ZIP de documentación conservando su estructura.
    encontrados = {}
    for base, _dirs, archivos in os.walk(docdir):
        for a in archivos:
            if a.lower().endswith(".pdf"):
                encontrados.setdefault(a[:-4], os.path.join(base, a))

    textos = {}
    problemas_de_lectura = False
    for nombre, meta in sorted(CUESTIONARIOS.items()):
        path = encontrados.get(nombre)
        if path is None:
            fail(f"falta el PDF {nombre}.pdf bajo {docdir}")
            problemas_de_lectura = True
            continue
        got = sha256(path)
        ok = got == meta["sha256"]
        print(f"  sha256 {nombre:12s} {'OK ' if ok else 'NO COINCIDE'} {got[:16]}…")
        if not ok:
            fail(f"{nombre}.pdf: sha256 {got} != {meta['sha256']} "
                 f"registrado en data/manifiesto.yaml ({meta['manifiesto_id']})")
            problemas_de_lectura = True
            continue
        textos[nombre] = extrae(path)
    # Solo un problema de LECTURA aborta la comparación -- no se puede comparar
    # contra un texto que no se pudo extraer. Una inconsistencia del inventario
    # NO la aborta: se reportan ambas cosas, nunca una enmascarando a la otra.
    if problemas_de_lectura:
        print()
        print("  no se compara el inventario: falta texto de al menos un PDF.")
        return
    print()

    # Reconstruye el inventario desde cero y compáralo con el transcrito.
    observado = {}
    for nombre, txt in textos.items():
        for t in LEXICO:
            c = cuenta(txt, t)
            if c:
                observado.setdefault(t, {})[nombre] = c

    for t in sorted(set(observado) | set(ADJUDICACION)):
        obs = observado.get(t, {})
        esp = ADJUDICACION.get(t, {}).get("conteo", {})
        if t not in ADJUDICACION:
            fail(f"ACIERTO NO ADJUDICADO — '{t}' aparece en {obs} y no está en "
                 f"el inventario. Léelo en el PDF y adjudícalo antes de "
                 f"volver a citar este script.")
        elif obs != esp:
            fail(f"conteo movido — '{t}': observado {obs}, transcrito {esp}")

    for t in CERO_ACIERTOS_ESPERADOS:
        if t in observado:
            fail(f"'{t}' se declaró con cero aciertos y aparece en "
                 f"{observado[t]} — el inventario está mal")

    if not FALLOS:
        print(f"  inventario re-derivado desde los {len(CUESTIONARIOS)} PDF: "
              f"idéntico al transcrito.")


# ---------------------------------------------------------------------------
# Salida
# ---------------------------------------------------------------------------

def main():
    docdir = None
    if "--docs" in sys.argv:
        i = sys.argv.index("--docs")
        if i + 1 >= len(sys.argv):
            print("uso: cal_enoe_fasea.py [--docs <directorio con los seis PDF>]")
            return 2
        docdir = sys.argv[i + 1]

    print("=" * 78)
    print("CAL-ENOE · FASE A · COMPUERTA 1 — ¿existe el desenlace en ENOE?")
    print("=" * 78)
    print()
    print("Constructo buscado : horizonte_temporal (preferencia temporal / "
          "conducta financiera)")
    print("Instrumento leído  : los seis cuestionarios de ENOE registrados en "
          "data/manifiesto.yaml")
    print("Microdato abierto  : ninguno")
    print()

    print("-" * 78)
    print("INSTRUMENTO LEÍDO")
    print("-" * 78)
    total_pag = 0
    for nombre, m in sorted(CUESTIONARIOS.items()):
        print(f"  {nombre:12s} {m['tipo']:17s} {m['paginas']:3d} pág   {m['cobertura']}")
        total_pag += m["paginas"]
    print(f"  {'':12s} {'':17s} {total_pag:3d} pág   TOTAL")
    print()

    print("-" * 78)
    print("SECCIONES DEL INSTRUMENTO — ninguna es de finanzas del hogar")
    print("-" * 78)
    for inst, secs in SECCIONES.items():
        print(f"  {inst}")
        for s in secs:
            print(f"      · {s}")
    print()

    print("-" * 78)
    print(f"LÉXICO: {len(LEXICO)} términos · ACIERTOS ADJUDICADOS")
    print("-" * 78)
    for t in sorted(ADJUDICACION):
        a = ADJUDICACION[t]
        n = sum(a["conteo"].values())
        print(f"  [{a['clase']:>5s}] {t:18s} {n:3d} aciertos · {a['reactivo']}")
    print()
    print(f"  Términos del léxico con CERO aciertos en los seis cuestionarios: "
          f"{len(CERO_ACIERTOS_ESPERADOS)}")
    print("   ", ", ".join(CERO_ACIERTOS_ESPERADOS))
    print()
    print("  Los TRES cuestionarios sociodemográficos (c_sdem_v4, c_sdem_v5, "
          "c_sdem_v5a) no")
    print(f"  registran UN SOLO acierto de los {len(LEXICO)} términos. Son lista "
          "de personas,")
    print("  parentesco, sexo, edad, lugar de nacimiento, alfabetismo y nivel de "
          "instrucción.")
    print()

    verifica_inventario()

    if docdir:
        print("-" * 78)
        print("VERIFICACIÓN CONTRA LOS PDF")
        print("-" * 78)
        verifica_contra_pdf(docdir)
        print()

    print("=" * 78)
    if FALLOS:
        print(f"FALLA · {len(FALLOS)} problema(s)")
        print("=" * 78)
        for f in FALLOS:
            print(f"  · {f}")
        return 1

    print("COMPUERTA 1 · NO PASA — no existe el desenlace")
    print("=" * 78)
    print("""
  Ninguna de las nueve clases de acierto mide preferencia temporal ni conducta
  financiera del sujeto. Lo más cercano que existe en todo el instrumento es la
  batería 3m del cuestionario AMPLIADO, y falla por tres razones a la vez:

    1 · Mide al PATRÓN, no al sujeto. El enunciado es "¿a ... le dan, aunque no
        utilice ...?". El "aunque no utilice" excluye por diseño la conducta.
    2 · Es casi colineal con la EXPOSICIÓN. La prestación laboral es
        ingrediente de la definición operativa de formalidad; usarla de
        desenlace sería regresar formalidad sobre sí misma.
    3 · Vive solo en el AMPLIADO, que se levanta en el trimestre 1 de cada año.

  No se estira el constructo para que algo case: lo más cercano a "conducta
  financiera" en ENOE es un catálogo de PRESTACIONES y un catálogo de FUENTES
  DE INGRESO. Ninguna de las dos cosas es horizonte temporal, y decir que lo
  son sería la asignación disfrazada de medición que CAL-G3 punto (2) existe
  para no repetir.

  CONSECUENCIA — se registra, NO se ejecuta aquí:
  `milpa/procedencia.yaml:282-288` (`unico_calibrable_hoy`) afirma que ENOE
  permite "estimar el cambio de conducta financiera asociado". La premisa es
  falsa a nivel de reactivo. La corrección de esa declaración y su cascada es
  decisión de MESA: este script no toca procedencia.yaml, ni el modelo, ni
  ADR alguno.

  Las compuertas 2 (enlace del panel a cinco trimestres), 3 (poder) y 4
  (población interrogada) NO se evalúan: son condicionales a que exista
  desenlace, y no existe. Descartar con rigor es el entregable.
""")
    return 0


if __name__ == "__main__":
    sys.exit(main())
