# Nota de cierre · MAESTRA32-E2 · EMPAREJA-MOTOR-TEXTO

Encargo: `forense/encargos/2026-08-28-MAESTRA32-E2-EMPAREJA-MOTOR-TEXTO.md` (dirección, maestra-32, 28/ago/2026, archivado por A.3 antes de ejecutar; redactado contra `main = 2953716`, merge de `PR #391`/`ACTO MAESTRA31-E10 · RECONCILIA-MOTOR`; GATED a que `PR #392`/`ACTO MAESTRA32-E1 · SELLA-ENLACE` fusionara — cumplido, `merge commit 3181d55`, ya presente en la rama al arrancar). Entorno **NUBE** (`cloud_default`); `data/raw` ausente, no usado, no necesario; sin red, sin API, sin microdato.

## 0 · ARRANQUE (las cinco líneas)

1. **REPO** — clon existente en `/home/user/Modelado-Mexicano`, no se clonó ninguno nuevo. `git log -1`: `3181d55 Merge pull request #392 from Josanoforo/claude/maestra32-e1-ranura-enlace-25vzfc`. `git status` al arrancar: rama `claude/maestra32-e2-motor-texto-c5grsj`, árbol limpio.
2. **SHA** — el encargo declara `main = 2953716`; la rama arrancó sobre `3181d55` (`2953716` + merge de `PR #392`/`ACTO MAESTRA32-E1 · SELLA-ENLACE`, confirmado ancestro por `git merge-base --is-ancestor 2953716 HEAD`). Diferencia reportada, no PARO: es exactamente el gate que el propio encargo esperaba que se cumpliera. Nada del perímetro de este acto depende de lo que E1 escribió (E1 tocó `milpa/procedencia.yaml:coeficientes_generador_sellados`, sección nueva al final del archivo, y `milpa/src/matriz.py`/`procedencia.py` — ninguno de los tres insumos de este acto), así que no hubo nada que re-derivar por el movimiento de `main`.
3. **data/raw** — ausente, como se esperaba (`ls data/raw` → `No such file or directory`; `ls data/raw/ 2>/dev/null | head -1` → vacío). No se creó ni se enlazó: este acto no la necesita (los tres insumos están versionados).
4. **ENTORNO** — este acto no toca microdato ni red (declarado en el propio encargo: "No usa red ni API"), así que el punto se saltó en el sentido operativo, pero se corrió la sonda igual por completitud: `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` (el encargo anotaba "esperado: sin_variable" pero la caja sí trae la variable poblada con el nombre del entorno asignado — no es una discrepancia de política de red, es que la caja se identifica a sí misma; no cambia nada del acto). `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` → `000` (sin conexión). Regla A.13 del v2.11: el comando que produjo este negativo no examinó archivos — es un `curl`, no un `grep`; se declara así explícitamente, y de cualquier modo el punto no gobierna nada de este acto porque no hay red ni microdato de por medio.
5. **ESPEJO** — no se derivó ninguna cifra del espejo del proyecto. Toda cifra de este documento sale de comandos corridos contra el clon de (1), reproducidos abajo.

`ls data/raw/ 2>/dev/null | head -1` (A.2, tercera parte) → vacío, como se esperaba.

## 1 · Verificación de premisas (v2.1)

Las cuatro premisas del encargo se re-derivaron por comando antes de escribir COMMIT-1, **no** se heredaron del texto de dirección:

- **Premisa 1** (los 9 pares) — confirmada verbatim contra `forense/estado-motor-v1_0.md:50-52` (§0.4): *"`G2.sens_estatus` · `G2.aversion_riesgo` · `G3.aversion_riesgo` · `G4.horizonte_temporal` · `G4.sens_estatus` · `G5.familismo_apoyo` · `G5.familismo_obligacion` · `G5.radio_confianza` · `G6.deferencia`."* Cruzada además contra `milpa/procedencia.yaml:rutas_estimabilidad_coeficiente.reparto` (línea 1127): `"RUTA-A=5 · RUTA-I=1 · RUTA-C=0 · SIN-RUTA=9"` — los 9 `SIN-RUTA` son exactamente esos 9 pares (verificado leyendo las 15 filas de `detalle`, líneas 1112-1126). `G3.horizonte_temporal` es la única fila `RUTA-I`, confirmado fuera por ser gate de identificación (`estado-motor-v1_0.md` §0.3, no §2 — corrección menor de cita: el encargo apuntaba a "§0.4/§2", el detalle del `GATE·ID-X` vive en §0.3, la lista de los 9 en §0.4; §2 es la sección de intersección/cifras, no donde vive esta lista).
- **Premisa 2** (notas G5) — confirmada verbatim contra `milpa/procedencia.yaml` (abierto con `yaml.safe_load`, nunca `grep` de subcadena): `G5.familismo_apoyo` línea 1123 (`"único candidato (ENIF p9_9_4) excluido por circularidad, marca C3, línea 265-270 arriba"`), `G5.radio_confianza` línea 1125 (`"reactivo (ENCUCI) y desenlace (ENIF) en instrumentos distintos, sin muestra común"`), `G5.familismo_obligacion` línea 1124 (`"sin magnitud asignada (ADR-30); condicional propia solo PROXY CON SUPUESTO DECLARADO, forma PENDIENTE"`). La `marca_c3` completa vive en líneas 271-277 (bloque `RECLASIFICACIÓN v4.0`) y 294-299/314-319 (`condicionales_escalares.radio_confianza.marca_c3` / `.familismo_apoyo.marca_c3`).
- **Premisa 3** (insumos) — re-derivada por comando, no heredada: `data/inventario-reactivos-v1_1.tsv` tiene 178,246 filas de datos (5 líneas de comentario + 1 encabezado + 178,246 filas de datos = 178,252 líneas totales, `wc -l`) y `data/inventario-fd-v1_0.tsv` tiene 17,094 filas de datos (0 comentarios + 1 encabezado = 17,095 líneas totales). Ambas cifras coinciden con las que el encargo declaraba. **Hallazgo adicional, no anticipado por el encargo:** `texto_reactivo` está vacío en el **100% (178,246/178,246)** de las filas de `inventario-reactivos-v1_1.tsv` — esa tabla nunca tuvo texto, solo `variable_id`/`instrumento`/metadata (consistente con su propia cabecera: es sucesora de `ADR-213`, que nunca prometió texto). `inventario-fd-v1_0.tsv` sí tiene texto en el 100% (17,094/17,094) de sus filas. **Esto se declara en la spec §0** porque acota de antemano qué puede producir la vía `via=texto`: solo contra `inventario-fd-v1_0.tsv`. La vía `via=id` corre contra las dos tablas.
- **Premisa 4** (tabla de siete) — confirmada verbatim contra `canon/modelo-decision-v4_0.md:432-440`: G2 → "Ansiedad de estatus, consumo compensatorio (rama estatus)" (línea 436); G3 → "Horizonte corto, ahorro informal, aversión" (línea 437); G4 → "Conducta defensiva, retracción del espacio público" (línea 438); G5 → "Pooling, corresidencia, carga de cuidado" (línea 439); G6 → "Deferencia, iniciativa suprimida, paternalismo" (línea 440).

Las cuatro premisas se sostienen. No hubo PARO.

## 2 · Discrepancias en la "VERIFICACIÓN DE EXISTENCIA" de dirección — reportadas, no bloqueantes

Por instrucción del ARRANQUE ("encontrar que el terreno no es el que el encargo supone es entregable, no interrupción"), se declaran dos imprecisiones de cita encontradas al verificar el punto 2 de la VERIFICACIÓN DE EXISTENCIA del encargo, ninguna cambia la sustancia (el emparejamiento no existía, este acto lo hace por primera vez):

1. **Ruta incorrecta.** El encargo cita `forense/enlace-M-v1_0.md`; el archivo real vive en `forense/prereg-duelo-v2/enlace-M-v1_0.md` (verificado: `ls forense/enlace-M-v1_0.md` → no existe; `ls forense/prereg-duelo-v2/enlace-M-v1_0.md` → existe). El contenido citado (corredor M del duelo, dominio distinto) sí es correcto.
2. **Atribución incorrecta.** El encargo dice: *"las dos notas de `MAESTRA31-E5` que lo declaran sucesor pendiente"*. Verificado por comando (`grep -rn "sucesor" forense/notas/2026-08-27-cruce-inverso*.md`): **cero** hits en las notas propias de `MAESTRA31-E5` — esas notas dicen, en cambio, `"No emparejó por texto ni semántica"` (`cruce-inverso-cierre.md:74`), una negación de alcance, no una declaración de sucesor pendiente. La frase verbatim que el encargo parafrasea — *"ninguno de los dos actos emparejó el texto de este acto contra el motor; eso sigue siendo trabajo de un sucesor"* — vive en **`ADR-215`** (`canon/gobernanza-v1_15.md:3915`), que es el ADR de **`ACTO MAESTRA31-E6 · DICCIONARIOS-FD`**, no de E5. `FP-173` (que sí gatea genéricamente este trabajo, `forense/firmas-pendientes.tsv:171`, columna `gatea`) también fue abierta por E6, no por E5 — y su propio texto trae una referencia cruzada inconsistente ("eso es E5/ADR-214") que mezcla el ADR de E5 (`ADR-214`, `CRUCE-INVERSO`) con el hallazgo que en realidad vive en `ADR-215` (E6). Ninguna de las dos notas de E5 declara "sucesor pendiente" en esas palabras — la cita correcta es `ADR-215`/`FP-173`, ambas de E6.

Ninguna de las dos afecta el objeto del acto: sigue siendo cierto que ningún artefacto anterior emparejó texto del corpus contra el vocabulario del motor, y que `FP-173` (aunque no nombra literalmente "MAESTRA32-E2") gatea genéricamente el trabajo que este acto hace por primera vez.

## 3 · El script de COMMIT-2, íntegro

Implementa, sin desviarse de los términos/criterios, la receta congelada de `forense/notas/2026-08-28-empareja-spec.md`. La clasificación `CANDIDATO`/`DESCARTADO-con-razón` (diccionario `DESCARTES`) es la aplicación del criterio §3.2 de la spec (lectura del recorte tras la búsqueda mecánica) — no es una segunda búsqueda ni cambia ningún término de la lista cerrada.

```python
#!/usr/bin/env python3
# MAESTRA32-E2 · EMPAREJA-MOTOR-TEXTO — COMMIT-2, corrida única (versión
# final). Misma búsqueda mecánica de empareja_run.py (frozen en
# forense/notas/2026-08-28-empareja-spec.md); esta versión añade la
# clasificación CANDIDATO/DESCARTADO-con-razón que el propio §3 de la
# especificación exige tras una lectura del recorte (no es una segunda
# búsqueda ni cambia ningún término), y una columna `razon`.
import csv
import sys
import unicodedata

ROOT = "/home/user/Modelado-Mexicano"


def norm(s):
    if s is None:
        return ""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower()


def load(fn):
    path = f"{ROOT}/{fn}"
    with open(path, encoding="utf-8") as f:
        lines = [l for l in f if not l.startswith("#")]
    rows = list(csv.DictReader(lines, delimiter="\t"))
    return rows


REACTIVOS = load("data/inventario-reactivos-v1_1.tsv")
FD = load("data/inventario-fd-v1_0.tsv")
TABLAS = [("inventario-reactivos-v1_1", REACTIVOS), ("inventario-fd-v1_0", FD)]

TERMINOS_ESTATUS = [
    "estatus", "status", "prestigio", "prestigiosa", "prestigioso",
    "imagen social", "que dirán", "que diran", "aparentar",
    "apariencia social", "ostentar", "ostentación", "ostentacion",
    "posición social", "posicion social", "nivel social", "envidia",
    "comparación social", "comparacion social",
]
DESENLACE_G2 = [
    "ansiedad de estatus", "ansiedad social", "estrés social",
    "estres social", "consumo compensatorio", "consumo conspicuo",
    "gasto en imagen", "compra por estatus", "compra por status",
    "deuda por aparentar", "gasto ostentoso", "compra impulsiva",
]
TERMINOS_AVERSION = [
    "aversión al riesgo", "aversion al riesgo", "tolerancia al riesgo",
    "preferencia por seguridad", "evitar riesgo", "evita el riesgo",
    "riesgo financiero", "disposición a arriesgar",
    "disposicion a arriesgar", "prefiere no arriesgar",
    "toma de riesgos",
]
DESENLACE_G3 = [
    "horizonte corto", "corto plazo", "ahorro informal", "tanda",
    "cundina", "guardadito", "debajo del colchón", "debajo del colchon",
    "sin cuenta bancaria", "ahorro en efectivo", "no planea a futuro",
    "sin planeación", "sin planeacion",
]
TERMINOS_HORIZONTE = [
    "horizonte temporal", "planeación a futuro", "planeacion a futuro",
    "corto plazo", "largo plazo", "futuro cercano",
    "expectativas a futuro", "orientación al futuro",
    "orientacion al futuro",
]
DESENLACE_G4 = [
    "conducta defensiva", "evita salir", "deja de salir",
    "restringe sus salidas", "evita lugares", "miedo a salir",
    "cambió de ruta", "cambio de ruta", "cambio de rutina",
    "retracción", "retraccion", "espacio público", "espacio publico",
    "deja de frecuentar", "autoconfinamiento", "evita transitar",
]
TERMINOS_FAMILISMO_APOYO = [
    "apoyo familiar", "ayuda económica de familiares",
    "ayuda economica de familiares", "dinero de familiares",
    "préstamo familiar", "prestamo familiar", "apoyo de la familia",
    "remesas familiares", "ayuda entre parientes",
    "transferencias familiares",
]
DESENLACE_G5 = [
    "pooling", "corresidencia", "vive con", "hogar extendido",
    "cuidado de familiares", "carga de cuidado", "cuidador", "cuida a",
    "comparte gastos del hogar", "hogar compartido",
    "mudarse con la familia", "se mudó con", "se mudo con",
]
TERMINOS_FAMILISMO_OBLIGACION = [
    "obligación familiar", "obligacion familiar",
    "deber con la familia", "responsabilidad familiar",
    "compromiso familiar", "deber moral con los padres",
    "obligado a ayudar a la familia", "debe cuidar a", "debe mantener a",
]
TERMINOS_RADIO_CONFIANZA = [
    "radio de confianza", "confía en", "confia en",
    "personas que conoce", "vecinos de su colonia", "desconocidos",
    "confianza interpersonal", "círculo de confianza",
    "circulo de confianza",
]
TERMINOS_DEFERENCIA = [
    "deferencia", "obediencia", "obedece", "respeto a la autoridad",
    "no cuestiona", "acata órdenes", "acata ordenes", "sumisión",
    "sumision", "subordinación", "subordinacion",
]
DESENLACE_G6 = [
    "iniciativa suprimida", "no toma la iniciativa",
    "espera instrucciones", "no opina", "se abstiene de proponer",
    "paternalismo", "decisiones tomadas por otros",
    "no participa en las decisiones",
]

BATERIA_CIRCULAR_G5 = {f"p9_9_{i}" for i in range(1, 7)}

PARES = [
    ("G5", "familismo_apoyo", TERMINOS_FAMILISMO_APOYO, DESENLACE_G5),
    ("G5", "radio_confianza", TERMINOS_RADIO_CONFIANZA, DESENLACE_G5),
    ("G5", "familismo_obligacion", TERMINOS_FAMILISMO_OBLIGACION, DESENLACE_G5),
    ("G2", "sens_estatus", TERMINOS_ESTATUS, DESENLACE_G2),
    ("G2", "aversion_riesgo", TERMINOS_AVERSION, DESENLACE_G2),
    ("G3", "aversion_riesgo", TERMINOS_AVERSION, DESENLACE_G3),
    ("G4", "horizonte_temporal", TERMINOS_HORIZONTE, DESENLACE_G4),
    ("G4", "sens_estatus", TERMINOS_ESTATUS, DESENLACE_G4),
    ("G6", "deferencia", TERMINOS_DEFERENCIA, DESENLACE_G6),
]

PLACEHOLDER_INSTRUMENTOS = {"(raiz)", "(sin-instrumento-derivable)"}

# ---------------------------------------------------------------------
# Excepciones DESCARTADO-con-razón: aplicación del criterio §3.2 de la
# especificación congelada (lectura del recorte confirma homónimo, no
# el constructo) sobre los candidatos crudos de la corrida mecánica.
# Clave: (variable_id, instrumento, termino) -> razón.
# ---------------------------------------------------------------------
DESCARTES = {
    ("ESTATUS", "ADQ15_ENAFIN_2024_RNM_INEGI", "estatus"): "homónimo administrativo: campo de estatus de registro/trámite, no sensibilidad al estatus social",
    ("Estatus del cambio", None, "estatus"): "homónimo administrativo: campo de estatus de registro de cambio (ENOE/ENIGH), no sensibilidad al estatus social",
    ("Estatus", None, "estatus"): "homónimo administrativo: campo de estatus de registro/trámite (sin más calificador en el nombre de columna, mismo patrón que las demás variantes ESTATUS*), no sensibilidad al estatus social",
    ("ESTATUS", None, "estatus"): "homónimo administrativo: campo de estatus de registro/trámite, no sensibilidad al estatus social",
    ("code_status", None, "status"): "homónimo administrativo: código de estatus de procesamiento, no sensibilidad al estatus social",
    ("estatus_casilla", None, "estatus"): "homónimo administrativo: estatus de casilla electoral, no sensibilidad al estatus social",
    ("ESTATUS_ ACTA", None, "estatus"): "homónimo administrativo: estatus de acta/documento, no sensibilidad al estatus social",
    ("ESTATUS_ACTA", None, "estatus"): "homónimo administrativo: estatus de acta/documento, no sensibilidad al estatus social",
    ("Estatus: APROBADO", None, "estatus"): "homónimo administrativo: estatus de aprobación de trámite, no sensibilidad al estatus social",
    ("2.2.2.2._BREMS", "ADQ15_CNBV_AhorroFinanciero_Financiamiento", "largo plazo"): "homónimo financiero: plazo de vencimiento de instrumento financiero agregado (macro), no horizonte temporal personal",
    ("2.1.1.2.Valores_bancarios", "ADQ15_CNBV_AhorroFinanciero_Financiamiento", "corto plazo"): "homónimo financiero: plazo de vencimiento de instrumento financiero agregado (macro), no horizonte temporal personal",
    ("2.1.1.3.Valores_privados", "ADQ15_CNBV_AhorroFinanciero_Financiamiento", "corto plazo"): "homónimo financiero: plazo de vencimiento de instrumento financiero agregado (macro), no horizonte temporal personal / ahorro informal",
    ("3.3.1.Créditos", "ADQ15_CNBV_AhorroFinanciero_Financiamiento", "largo plazo"): "homónimo financiero: plazo de vencimiento de crédito externo agregado (macro), no horizonte temporal personal",
    ("3.3.2.Emisión_de_deuda_de_mexicanos_en_el_extranjero", "ADQ15_CNBV_AhorroFinanciero_Financiamiento", "largo plazo"): "homónimo financiero: plazo de vencimiento de deuda agregada (macro), no horizonte temporal personal",
    ("https://www.elystandard.co.uk/news/26460266.man-due-court-deaths-women-a10-crash-near-ely/", "(sin-instrumento-derivable)", "tanda"): "colisión de subcadena espuria: \"tanda\" cae dentro de \"standard\" en una URL de noticia ajena al corpus de reactivos, no es contenido de reactivo",
    ("P28B. Dígame si está usted de acuerdo o en desacuerdo con las siguientes frases Si uno no se cuida a sí mismo la gente se aprovechará", "encup2012", "cuida a"): "homónimo: ítem de autocuidado/confianza generalizada (\"si uno no se cuida a sí mismo la gente se aprovechará\"), no carga de cuidado familiar",
    ("U_POB_ELAB_CUL", "(raiz)", "cuida a"): "homónimo: cuidado de animales/cultivo agrícola, no cuidado de personas",
    ("P2_6_3", "(raiz)", "cuidador"): "mide contratación de cuidador(a) remunerado(a) externo (sustituye a la familia), polo opuesto de \"carga de cuidado\" recayendo en la familia",
    ("P2_1", "mociba2016", "desconocidos"): "homónimo: exposición a spam/virus/contacto de desconocidos en internet (uso de TIC), no radio de confianza interpersonal",
}


def descarte_razon(vid, inst, termino):
    for key in ((vid, inst, termino), (vid, None, termino)):
        if key in DESCARTES:
            return DESCARTES[key]
    return None


def recorte(s, n=200):
    s = (s or "").replace("\t", " ").replace("\n", " ")
    return s if len(s) <= n else s[: n - 1] + "…"


def buscar(terminos, lado, gen, coef):
    salida = []
    n_hits_id = 0
    n_hits_texto = 0
    terminos_norm = [(t, norm(t)) for t in terminos]
    for nombre_tabla, filas in TABLAS:
        for row in filas:
            vid = row.get("variable_id", "")
            vid_n = norm(vid)
            texto = row.get("texto_reactivo", "")
            texto_n = norm(texto)
            inst = row.get("instrumento", "")
            for via, haystack_n in (("id", vid_n), ("texto", texto_n)):
                hit = next((t for t, tn in terminos_norm if tn in haystack_n), None)
                if not hit:
                    continue
                if via == "id":
                    n_hits_id += 1
                else:
                    n_hits_texto += 1
                veredicto = "CANDIDATO"
                razon = ""
                if lado == "desenlace" and gen == "G5" and vid.strip().lower() in BATERIA_CIRCULAR_G5:
                    veredicto = "CIRCULAR-EXCLUIDO"
                    razon = "misma batería ENIF P9_9_1..6 que opera la θ de familismo_apoyo -- marca C3, milpa/procedencia.yaml:314-319"
                else:
                    r = descarte_razon(vid, inst, hit)
                    if r:
                        veredicto = "DESCARTADO-con-razón"
                        razon = r
                salida.append(dict(
                    gen=gen, coef=coef, lado=lado, variable_id=vid,
                    instrumento=inst, texto=recorte(texto), via=via,
                    tabla=nombre_tabla, termino=hit,
                    veredicto_candidato=veredicto, razon=razon,
                ))
    return salida, n_hits_id, n_hits_texto


if __name__ == "__main__":
    todas_filas = []
    resumen = []
    for gen, coef, terminos_theta, terminos_desenlace in PARES:
        filas_theta, hid_t, htx_t = buscar(terminos_theta, "theta", gen, coef)
        filas_desenlace, hid_d, htx_d = buscar(terminos_desenlace, "desenlace", gen, coef)
        todas_filas.extend(filas_theta)
        todas_filas.extend(filas_desenlace)
        print(f"# {gen}.{coef}: theta hits id={hid_t} texto={htx_t} | "
              f"desenlace hits id={hid_d} texto={htx_d}", file=sys.stderr)
        resumen.append((gen, coef, filas_theta, filas_desenlace))

    with open(f"{ROOT}/data/emparejamiento-motor-v1_0.tsv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["gen", "coef", "lado", "variable_id", "instrumento", "texto",
                    "via", "veredicto_candidato", "razon", "tabla", "termino"])
        for row in todas_filas:
            w.writerow([row["gen"], row["coef"], row["lado"], row["variable_id"],
                        row["instrumento"], row["texto"], row["via"],
                        row["veredicto_candidato"], row["razon"], row["tabla"],
                        row["termino"]])

    print("\n# ===== veredicto A.4 por par (co-observación exige instrumento "
          "identificado, NO '(raiz)'/'(sin-instrumento-derivable)') =====",
          file=sys.stderr)
    for gen, coef, ft, fd in resumen:
        cand_theta = sorted({r["instrumento"] for r in ft
                              if r["veredicto_candidato"] == "CANDIDATO"
                              and r["instrumento"] not in PLACEHOLDER_INSTRUMENTOS})
        cand_desenlace = sorted({r["instrumento"] for r in fd
                                  if r["veredicto_candidato"] == "CANDIDATO"
                                  and r["instrumento"] not in PLACEHOLDER_INSTRUMENTOS})
        cand_theta_raiz = sorted({r["instrumento"] for r in ft
                                   if r["veredicto_candidato"] == "CANDIDATO"
                                   and r["instrumento"] in PLACEHOLDER_INSTRUMENTOS})
        cand_desenlace_raiz = sorted({r["instrumento"] for r in fd
                                       if r["veredicto_candidato"] == "CANDIDATO"
                                       and r["instrumento"] in PLACEHOLDER_INSTRUMENTOS})
        co = sorted(set(cand_theta) & set(cand_desenlace))
        n_theta_candidato = sum(1 for r in ft if r["veredicto_candidato"] == "CANDIDATO")
        n_desenlace_candidato = sum(1 for r in fd if r["veredicto_candidato"] == "CANDIDATO")
        print(f"{gen}.{coef}: theta_candidatos_reales={n_theta_candidato} "
              f"(instrumentos={cand_theta}, +placeholder={cand_theta_raiz}) | "
              f"desenlace_candidatos_reales={n_desenlace_candidato} "
              f"(instrumentos={cand_desenlace}, +placeholder={cand_desenlace_raiz}) | "
              f"co_observacion_instrumento_identificado={co}", file=sys.stderr)
    print(f"\n# total filas escritas en data/emparejamiento-motor-v1_0.tsv: {len(todas_filas)}",
          file=sys.stderr)
```

**Nota de proceso, honesta:** la primera corrida (sin la tabla `DESCARTES` ni el filtro de `instrumento` placeholder en la co-observación) se guardó como borrador en el scratchpad de la sesión, no en el repo — nunca se escribió a `data/`. Al inspeccionar sus 715 filas crudas (paso exigido por el criterio §3.2 de la propia spec, no una re-búsqueda) aparecieron los homónimos de abajo; la versión que sí se escribió a `data/emparejamiento-motor-v1_0.tsv` es la de este script, con la clasificación aplicada. Ningún término de búsqueda cambió entre una versión y otra — la lista cerrada de `forense/notas/2026-08-28-empareja-spec.md` es la que corrió, sin editar.

## 4 · Su salida real

```
# G5.familismo_apoyo: theta hits id=0 texto=8 | desenlace hits id=2 texto=38
# G5.radio_confianza: theta hits id=27 texto=6 | desenlace hits id=2 texto=38
# G5.familismo_obligacion: theta hits id=0 texto=0 | desenlace hits id=2 texto=38
# G2.sens_estatus: theta hits id=253 texto=10 | desenlace hits id=0 texto=0
# G2.aversion_riesgo: theta hits id=0 texto=0 | desenlace hits id=0 texto=0
# G3.aversion_riesgo: theta hits id=0 texto=0 | desenlace hits id=1 texto=15
# G4.horizonte_temporal: theta hits id=0 texto=8 | desenlace hits id=0 texto=0
# G4.sens_estatus: theta hits id=253 texto=10 | desenlace hits id=0 texto=0
# G6.deferencia: theta hits id=4 texto=0 | desenlace hits id=0 texto=0

# ===== veredicto A.4 por par (co-observación exige instrumento identificado, NO '(raiz)'/'(sin-instrumento-derivable)') =====
G5.familismo_apoyo: theta_candidatos_reales=8 (instrumentos=['enfih2019'], +placeholder=['(raiz)']) | desenlace_candidatos_reales=37 (instrumentos=['elcos2012', 'enasem2018', 'enasem2021', 'enasem2024', 'enasic2022'], +placeholder=[]) | co_observacion_instrumento_identificado=[]
G5.radio_confianza: theta_candidatos_reales=32 (instrumentos=['encup2012'], +placeholder=['(raiz)']) | desenlace_candidatos_reales=37 (instrumentos=['elcos2012', 'enasem2018', 'enasem2021', 'enasem2024', 'enasic2022'], +placeholder=[]) | co_observacion_instrumento_identificado=[]
G5.familismo_obligacion: theta_candidatos_reales=0 (instrumentos=[], +placeholder=[]) | desenlace_candidatos_reales=37 (instrumentos=['elcos2012', 'enasem2018', 'enasem2021', 'enasem2024', 'enasic2022'], +placeholder=[]) | co_observacion_instrumento_identificado=[]
G2.sens_estatus: theta_candidatos_reales=0 (instrumentos=[], +placeholder=[]) | desenlace_candidatos_reales=0 (instrumentos=[], +placeholder=[]) | co_observacion_instrumento_identificado=[]
G2.aversion_riesgo: theta_candidatos_reales=0 (instrumentos=[], +placeholder=[]) | desenlace_candidatos_reales=0 (instrumentos=[], +placeholder=[]) | co_observacion_instrumento_identificado=[]
G3.aversion_riesgo: theta_candidatos_reales=0 (instrumentos=[], +placeholder=[]) | desenlace_candidatos_reales=13 (instrumentos=['enfih2019'], +placeholder=['(raiz)']) | co_observacion_instrumento_identificado=[]
G4.horizonte_temporal: theta_candidatos_reales=2 (instrumentos=[], +placeholder=['(raiz)']) | desenlace_candidatos_reales=0 (instrumentos=[], +placeholder=[]) | co_observacion_instrumento_identificado=[]
G4.sens_estatus: theta_candidatos_reales=0 (instrumentos=[], +placeholder=[]) | desenlace_candidatos_reales=0 (instrumentos=[], +placeholder=[]) | co_observacion_instrumento_identificado=[]
G6.deferencia: theta_candidatos_reales=4 (instrumentos=['encup2012', 'endireh2003'], +placeholder=[]) | desenlace_candidatos_reales=0 (instrumentos=[], +placeholder=[]) | co_observacion_instrumento_identificado=[]

# total filas escritas en data/emparejamiento-motor-v1_0.tsv: 715
```

## 5 · Hallazgo declarado — corrección de spec (no editada hacia atrás)

El criterio de co-observación de `forense/notas/2026-08-28-empareja-spec.md` §4 ("mismo valor exacto de columna `instrumento`") no anticipó que el universo de valores de `instrumento` incluye dos *placeholders* que no identifican un instrumento real: `(raiz)` (28,799 de 178,246 filas de `inventario-reactivos-v1_1.tsv` — payload en la raíz de `data/raw` sin carpeta contenedora, defecto de etiquetado que `ACTO MAESTRA31-E7 · ETIQUETA` ya documentó y resolvió parcialmente: 80/119 payloads de la raíz, dejando 39 honestamente sin resolver) y `(sin-instrumento-derivable)`. Dos filas que solo comparten uno de estos dos valores **no** acreditan muestra común — "instrumento desconocido" no es "mismo instrumento": podrían venir de payloads completamente distintos. Esto se descubrió al correr la receta (no se podía anticipar sin correrla — es un hecho sobre la composición de columna `instrumento`, no sobre el contenido semántico de los 9 pares), y **reduce** el número de coincidencias reportables (hace el criterio más estricto, no más permisivo) — la dirección del ajuste no favorece ningún resultado en particular. Se aplicó en esta única corrida y se declara aquí, en la cabecera de `data/emparejamiento-motor-v1_0.tsv`, y en este documento. No se editó `forense/notas/2026-08-28-empareja-spec.md` hacia atrás, tal como el propio encargo instruye.

**Efecto concreto:** sin esta corrección, `G5.familismo_apoyo` y `G5.radio_confianza` habrían mostrado `(raiz)` como co-observación aparente (ambos lados tienen candidatos reales etiquetados `(raiz)`) — un artefacto de dos payloads sin instrumento identificado, no evidencia de muestra común. Con la corrección, ambos quedan `EXISTE-NO-SATISFACE` (correcto: cada lado tiene candidatos reales, pero en instrumentos que no coinciden — o, en el caso de `(raiz)`, en instrumentos que no se pueden confirmar que coincidan).

Se corrió también, y no disparó nada esta vez: la exclusión de circularidad de la batería ENIF `P9_9_1..6` para el lado-desenlace de los tres pares G5 (§5 de la spec) — ninguno de los 40 hits crudos de desenlace de G5 cayó en esa batería, así que `CIRCULAR-EXCLUIDO` aparece 0 veces en la tabla final. Se declara explícitamente porque A.13 pide, para cada regla que puede disparar cero, el conteo que prueba que corrió: la regla se evaluó sobre las 715 filas candidatas, 0 cumplieron la condición.

## 6 · Comandos y universo (A.13)

```
$ python3 -c "..."   # premisa 3, inventario-reactivos-v1_1.tsv
total lines 178252 | comment lines 5 | data rows (excl header) 178246

$ python3 -c "..."   # premisa 3, inventario-fd-v1_0.tsv
total lines 17095 | comment lines 0 | data rows (excl header) 17094

$ python3 -c "..."   # texto_reactivo vacío, inventario-fd-v1_0.tsv
filas 17094 vacios 0

$ python3 -c "..."   # texto_reactivo vacío, inventario-reactivos-v1_1.tsv
filas 178246 vacios 178246

$ grep -ni inventario data/INFRAESTRUCTURA-v1_0.md | wc -l
0

$ python3 tests/check.py --baseline   (corrido tras COMMIT-1/COMMIT-2, antes de la cascada)
19 FAIL · 134 WARN — LÍNEA BASE: VERDE, nada nuevo frente a tests/baseline.json
[ ok ] T25 T-ROTULOS
```

El script de §3 se corrió **una sola vez** con la clasificación final (la corrida preliminar sin clasificación, mencionada en la nota de proceso de §3, nunca se escribió a `data/` — no cuenta como una segunda corrida de la receta, es la misma corrida con la lectura de candidatos aplicada antes de persistir el archivo). `filas examinadas` por la corrida: `178246` (`inventario-reactivos-v1_1`) y `17094` (`inventario-fd-v1_0`) — coincide exacto con la premisa 3 re-derivada, no heredada.

## 7 · Veredictos A.4, uno por par, universo declarado

Universo de búsqueda para los 9 pares (idéntico): `data/inventario-reactivos-v1_1.tsv` (178,246 filas) + `data/inventario-fd-v1_0.tsv` (17,094 filas), columnas `variable_id` (vía `id`) y `texto_reactivo` (vía `texto`, con hit real solo posible en `inventario-fd-v1_0.tsv`), lista cerrada de términos de `forense/notas/2026-08-28-empareja-spec.md` §2, criterio de candidato/circularidad/co-observación de sus §3-§5, corregido por el hallazgo de §5 de este documento (co-observación exige instrumento identificado).

1. **`G5.familismo_apoyo` — `EXISTE-NO-SATISFACE`.** θ existe y es real: `enfih2019`, 2 ítems (`P10_1_3`/`P10_1_4`, "¿usted recibió dinero de familiares...?"). Desenlace existe y es real: `enasic2022` (encuesta dedicada al sistema de cuidados — variables `cuidador`/`P4_18`/`P4_29`/etc.), `enasem2018/2021/2024` (`CUIDA_ADULTO_*`/`CUIDA_MENOR_*`, uso del tiempo), `elcos2012` (`NCUIDADORA`). **Falta:** ningún instrumento identificado comparte ambos lados — `enfih2019` no aporta ítems de desenlace, y los instrumentos de desenlace no aportan ítems de θ.
2. **`G5.radio_confianza` — `EXISTE-NO-SATISFACE`.** θ existe y es real: `encup2012`, batería `P30` completa (27 ítems "¿qué tanto confía en...?", incluye "la familia" y "los vecinos" — una operacionalización distinta de la ya anclada ENCUCI 2020, encontrada por esta búsqueda libre de texto). Desenlace existe y es real, mismos instrumentos que el par anterior. **Falta:** el único candidato de desenlace que cayó en `encup2012` (`P28B`, "cuida a") se descartó por homónimo (autocuidado/confianza generalizada, no carga de cuidado) — sin ese candidato, `encup2012` no tiene desenlace real, y ningún otro instrumento identificado aporta ambos lados. Confirma, con un instrumento distinto al anticipado por la nota de B (`ENCUP` en vez de `ENCUCI`), la misma conclusión: reactivo y desenlace en instrumentos distintos, sin muestra común.
3. **`G5.familismo_obligacion` — `EXISTE-NO-SATISFACE`.** θ: `NO-ENCONTRADO` — 0 hits en las dos tablas para los 9 términos de la lista cerrada (`obligación familiar`, `deber con la familia`, etc.), confirmado por el conteo del script (`theta hits id=0 texto=0`). Desenlace existe y es real, mismos instrumentos que arriba. **Falta:** el lado θ completo — ninguna operacionalización de "obligación familiar" (distinta de "apoyo familiar") aparece en el corpus abierto hoy.
4. **`G2.sens_estatus` — `NO-ENCONTRADO`.** θ: 263 hits crudos (`estatus`×262, `status`×1), los 8 `variable_id` únicos son homónimos administrativos en el 100% de los casos (`ESTATUS`/`Estatus`/`Estatus del cambio`/`ESTATUS_ACTA`/`estatus_casilla`/`Estatus: APROBADO`/`code_status` — campos de estatus de trámite/registro/acta/casilla electoral, en `enoe*`/`enigh*`/`endutih*`/`ADQ15_ENAFIN_2024`/`(sin-instrumento-derivable)`), ninguno mide sensibilidad al estatus social — 0 `CANDIDATO` reales. Desenlace: 0 hits (ningún término de "ansiedad de estatus"/"consumo compensatorio" aparece en el corpus). Términos y universo: 18 términos θ + 12 términos desenlace, contra las 195,340 filas de las dos tablas.
5. **`G2.aversion_riesgo` — `NO-ENCONTRADO`.** θ: 0 hits (11 términos: "aversión al riesgo", "tolerancia al riesgo", etc.). Desenlace: 0 hits (comparte lista con G2.sens_estatus, mismo generador).
6. **`G3.aversion_riesgo` — `EXISTE-NO-SATISFACE`.** θ: `NO-ENCONTRADO` — 0 hits (mismos 11 términos de aversión al riesgo que G2, sin resultado en ninguna de las dos tablas). Desenlace existe y es real: `enfih2019` (`C_OTROAF`/`V_OTROAF`/`P9_1_3`/`P9_2_3`, "ahorro informal"/"tanda") — 2 hits crudos descartados (URL espuria con "tanda" dentro de "standard"; dos ítems `ADQ15_CNBV` sobre plazo de instrumentos financieros macro, homónimo de "corto plazo"). **Falta:** el lado θ completo.
7. **`G4.horizonte_temporal` — `EXISTE-NO-SATISFACE`.** θ existe pero solo en instrumento **no resuelto**: `(raiz)`, 2 ítems (`P4_8_4`/`P4_6_4`, "¿se pone metas económicas a largo plazo...?") — adyacentes por numeración al proxy ya conocido para G3 (`ENIF P4_10`, nota de B de `G4.horizonte_temporal`), lo que sugiere fuertemente que también son de ENIF, pero el pipeline de extracción no pudo resolver el instrumento de este payload (mismo defecto de clase que `ACTO MAESTRA31-E7 · ETIQUETA` ya documentó para 39/119 payloads de raíz sin resolver — este acto no reabre esa ruta, solo lo declara). 6 hits crudos adicionales descartados (`ADQ15_CNBV`, plazo financiero macro). Desenlace: `NO-ENCONTRADO`, 0 hits (ningún término de "conducta defensiva"/"retracción del espacio público" aparece en el corpus). **Falta:** el desenlace completo, y el instrumento del único candidato θ real sin resolver.
8. **`G4.sens_estatus` — `NO-ENCONTRADO`.** Mismo patrón que G2.sens_estatus (comparte términos θ): 263 hits crudos, 0 reales; desenlace 0 hits (comparte lista con G4.horizonte_temporal).
9. **`G6.deferencia` — `EXISTE-NO-SATISFACE`.** θ existe y es real, en dos instrumentos: `encup2012` (`P44A`/`P44C`, "los ciudadanos deben obedecer siempre las leyes..." / su inverso) y `endireh2003` (`OBEDECER`, x2 — contexto de autoridad doméstica/marital, no institucional, declarado porque cambia el dominio pero no descalifica el candidato: `modelo-decision:440` describe el generador como "Jerarquía + indulgencia" sin acotarlo a autoridad política). Desenlace: `NO-ENCONTRADO`, 0 hits (ningún término de "iniciativa suprimida"/"paternalismo" aparece en el corpus). **Falta:** el desenlace completo.

**Contador del acto:** 9 de 9 veredictos A.4 sellados con universo declarado. `N = 0` pares con co-observación (0 de 9 `EXISTE-SATISFACE`). Por B-bis del encargo, esto corrobora — ahora contra la capa de texto que los censos de ruta nunca vieron — el mismo techo que `forense/estado-motor-v1_0.md` ya había declarado: informativo de primer orden, no fracaso. Ordena el carril de adquisición: 6 de 9 pares ya tienen media pareja real identificada (todos menos los tres `NO-ENCONTRADO`), con el lado y el instrumento (o su ausencia de resolución) nombrados arriba.

**Estampa (A.10):** todos los veredictos de este documento se sellan sobre corpus abierto al 43.9% (316/720 payloads con filas) + capa FD 32/33, `main = 3181d55` (= `2953716` + `PR #392`/`ACTO MAESTRA32-E1 · SELLA-ENLACE`). Vencen en alcance cuando `MAESTRA32-E3` amplíe el universo — declarado aquí, no descubierto después. El re-sello es `MAESTRA32-E4 · RE-EMPAREJA`, con esta misma spec congelada, sucesor declarado, no lanzado.

## 8 · Falsador del acto — no se disparó

Los 9 pares fueron operacionalizables desde `canon/modelo-decision-v4_0.md` §2.1: los cinco generadores involucrados (G2, G3, G4, G5, G6) nombran un desenlace en la tabla de §2.1 (líneas 436-440), y las 9 θ tienen nombre de constructo derivable de su propio nombre de coeficiente. El falsador exigía ≥3 pares inaplicables por falta de desenlace nombrable — cero pares cayeron en esa categoría. No se reporta hallazgo de especificación del modelo.

## 9 · Ninguna ambigüedad real que requiriera PARO

Las dos discrepancias de §2 (ruta de archivo, atribución E5→E6) se resolvieron por verificación directa sin necesidad de detener el acto — son errores de cita en el texto de dirección, no incertidumbre sobre qué hacer. El hallazgo de §5 (placeholders de `instrumento`) se resolvió aplicando el criterio más estricto (menos permisivo con la co-observación), declarado como corrección de spec, no como PARO.

## 10 · Lo que este acto NO hizo

No midió ningún β̂. No abrió microdato ni `data/raw` (ausente, no creada ni enlazada, no necesaria). No editó `milpa/procedencia.yaml` (ni `ruta:` ni `nota:` de ninguna de las 15 filas — verificado, `git diff --stat` de este acto no toca `milpa/`). No tocó los inventarios existentes (`data/inventario-reactivos-v1_1.tsv`, `data/inventario-fd-v1_0.tsv`) ni sus herramientas (`tools/`, no tocado). No adjudicó el `GATE·ID-X` de `G3.horizonte_temporal` (quedó fuera del objeto, como el encargo instruía). No usó red ni API. No corrigió `forense/notas/2026-08-28-empareja-spec.md` hacia atrás (la corrección de §5 vive en este documento y en la cabecera de la tabla, no en la spec). No convirtió ninguno de los 6 pares `EXISTE-NO-SATISFACE` en `EXISTE-SATISFACE` "completando" el lado que falta — cada uno se reporta exactamente como cayó.
