# Nota de cierre · ACTO MAESTRA32-E6 · ETIQUETA-v1_2 + RE-EMPAREJA-LITE

Encargo: `forense/encargos/2026-08-30-MAESTRA32-E6-ETIQUETA-v1_2.md` (dirección, maestra-32, 30/ago/2026, archivado por A.3 antes de ejecutar; redactado contra `main = 2c0d4c8`, merge de PR #394). Entorno **NUBE** (`cloud_default`); `data/raw` ausente, no usada, no necesaria; sin red, sin API, sin microdato.

## 0 · ARRANQUE (las cinco líneas)

1. **REPO** — clon existente en `/home/user/Modelado-Mexicano`, no se clonó ninguno nuevo. `git log -1`: `2c0d4c8 Merge pull request #394 from Josanoforo/claude/maestra32-e5-firmas-cola-vroay4`. `git status` al arrancar: rama `claude/maestra32-e6-cloud-launch-8qu0hw`, árbol limpio.
2. **SHA** — coincide exacto con lo que el encargo declara (`main = 2c0d4c8`). Sin diferencia que resolver.
3. **data/raw** — ausente, como se esperaba: `ls data/raw` → no existe; `ls data/raw/ 2>/dev/null | head -1` (A.2, tercera parte) → vacío (0 archivos examinados por ese comando — no aplica el punto 3 del acto, este acto no descarga nada). No se creó ni se enlazó: los cuatro insumos declarados están versionados.
4. **ENTORNO** — este acto no toca microdato ni red (no abre ningún payload, no descarga nada); se corrió la sonda igual por completitud, con el mismo tratamiento que `ACTO MAESTRA32-E2`/`E5` ya dieron: `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` (el encargo anotaba "esperado: sin_variable", pero la caja se identifica a sí misma con el nombre del entorno asignado — no es una discrepancia de política de red, mismo hallazgo no-discrepante que `E2`/`E5` ya reportaron). `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` → `000` (sin conexión). Regla A.13 v2.11: el comando que produjo este negativo es un `curl`, examinó **0 archivos** — se declara explícitamente, y de cualquier modo el punto no gobierna nada de este acto.
5. **ESPEJO** — ninguna cifra de este documento se derivó del espejo del proyecto. Toda cifra sale de comandos corridos contra el clon de (1), reproducidos abajo.

## 1 · Verificación de premisas (v2.1) y de la "VERIFICACIÓN DE EXISTENCIA" de dirección

Las tres premisas del encargo se re-derivaron por comando antes de escribir COMMIT-1, no se heredaron del texto de dirección:

- **Premisa 1** — confirmada: `forense/notas/2026-08-27-etiqueta-regla.md` resolvió 80/119, dejó 39 honestos; regla citada íntegra en el COMMIT-1 de este acto.
- **Premisa 2** — confirmada por comando (`data/emparejamiento-motor-v1_0.tsv`, filtrado `variable_id in (P4_8_4,P4_6_4)`): ambas filas traen `instrumento='(raiz)'`, `via=texto`, vienen de `inventario-fd-v1_0.tsv` (`P4_8_4` de `enif_2018_fd.xlsx`/`enif_2024_fd.xlsx`; `P4_6_4` de esos dos más `enif_2015_fd.xlsx`, y también de `endutih2023/2024/2025`, ya resueltos en `v1_0`).
- **Premisa 3** — confirmada: `forense/notas/2026-08-28-empareja-spec.md` existe, congelada, con la co-observación corregida por E2 mismo (`(raiz)`/`(sin-instrumento-derivable)` no acreditan muestra común).

Punto 1 de la VERIFICACIÓN DE EXISTENCIA: `command grep -c "inventario" data/INFRAESTRUCTURA-v1_0.md` → **1** (≥1, confirmado). Punto 2: `data/emparejamiento-motor-v1_0.tsv` re-verificado (arriba); los 28,799/178,246 `(sin-instrumento-derivable)` (contado hoy, coincide exacto) se reparten en **39** `payload_id` distintos (re-derivado, coincide con la descomposición por motivo de `etiqueta-regla.md:68-76`: 16+13+2+3+3+1+1=39); las tres tablas destino (`inventario-fd-v1_1`, `inventario-reactivos-v1_2`, `emparejamiento-motor-v1_1`) NO-ENCONTRADO antes de este acto (`ls data`, 64 entradas — no 63, el encargo citaba la cifra de hace un día, diferencia reportada, no bloqueante — 0 coincidencias con las tres tablas destino).

**Dos discrepancias adicionales encontradas al verificar, declaradas por instrucción del ARRANQUE ("encontrar que el terreno no es el que el encargo supone es entregable, no interrupción"), ninguna bloqueante:**

1. **Rótulo E6/E7 intercambiado frente a lo que el acto anterior había previsto.** `forense/encargos/2026-08-30-MAESTRA32-E5-PROPAGA-FIRMAS-Y-COLA.md` (§"Sucesores declarados, no lanzados") predijo `MAESTRA32-E6 · PILOTO-T1T2` y `MAESTRA32-E7 · ETIQUETA-v1_2`. Este acto es en cambio `MAESTRA32-E6 · ETIQUETA-v1_2` (no `PILOTO-T1T2`) y declara como sucesor `MAESTRA32-E7 · CANDIDATOS-MARCO-M` (no `ETIQUETA-v1_2`). No cambia nada del objeto de este acto — dirección puede reordenar/renombrar actos futuros — pero se declara explícitamente porque contradice por escrito lo que el acto previo había registrado, y ninguna nota posterior lo corrige hasta este documento.
2. **Un payload de los 39 no tiene entrada en `data/manifiesto.yaml`.** `DescargaMasivaOD_582026_171540_NACIONAL_7930url.xml` no aparece en `data/manifiesto.yaml` (verificado: 0 coincidencias por campo `archivo` ni `id`). Sí aparece en `data/manifiesto-staging.yaml` (8 entradas totales), pero con `usado_para`/`url_origen`/`url_origen_sugerida` **vacíos** — no habría cambiado el resultado de la regla v1_2 aunque se hubiera incluido esa tabla, y el encargo cita `data/manifiesto.yaml` (no `-staging`) como fuente. Se declara, no se resuelve: este acto no escribe en ninguna de las dos tablas de manifiesto.

## 2 · COMMIT-1

`forense/notas/2026-08-30-etiqueta-v1_2-spec.md` — regla v1_1 citada tal cual para la capa FD; regla v1_2 nueva (campos `id`/`usado_para`/`nota`/`url_origen` de `data/manifiesto.yaml`, lista cerrada de 44 familias re-derivada de `inventario-reactivos-v1_1.tsv`, adyacencia familia+año sin heurística de substring suelto); control positivo; falsador <50%; B-bis con movimiento solo hacia arriba y re-clavado declarado de las dos claves `DESCARTES` que citaban `(raiz)` literal.

## 3 · COMMIT-2 — corrida única, `tools/etiqueta_v1_2.py`

Script íntegro en el repo (`tools/etiqueta_v1_2.py`, nuevo; no importa ni edita `tools/inventario_reactivos.py`). Salida JSON de la corrida (A.13, cada conteo con su denominador):

```
$ python3 tools/etiqueta_v1_2.py
{
  "fd": {
    "raiz_antes": 4390,
    "resueltos_via_v1_1": 4390,
    "resueltos_via_v1_2": 0,
    "sin_instrumento_derivable_despues": 0,
    "control_positivo_filas_comparadas": 12704,
    "control_positivo_diferencias": 0
  },
  "reactivos": {
    "payloads_39_resueltos": 16,
    "payloads_39_totales": 39,
    "porcentaje_resuelto": 41.03,
    "falsador_menos_de_50pct_disparado": true,
    "filas_resueltas": 6816,
    "filas_sin_resolver_despues": 21983,
    "control_positivo_filas_comparadas": 149447,
    "control_positivo_diferencias": 0
  }
}
```

### 3.1 · Capa FD — 4,390 → 0, 100% vía regla v1_1

Los 10 `payload_id` `(raiz)` de `inventario-fd-v1_0.tsv` (§0 del COMMIT-1) resuelven **los 10** aplicando, por primera vez, la tabla de `forense/notas/2026-08-27-etiqueta-regla.md` §2 sobre el propio `payload_id`:

| payload_id | filas | instrumento resuelto |
|---|---:|---|
| `Censo2020_CAAS_descriptor_bd.xlsx` | 259 | `censo2020` |
| `Censo2020_CEU_descriptor_bd.xlsx` | 116 | `censo2020` |
| `diccionario_cuestionario_ampliado_cpv2020.xlsx` | 201 | `cpv2020` |
| `enif_2015_fd.xlsx` | 520 | `enif2015` |
| `enif_2018_fd.xlsx` | 382 | `enif2018` |
| `enif_2024_fd.xlsx` | 443 | `enif2024` |
| `enut2019_fd.xlsx` | 656 | `enut2019` |
| `enut2024_fd.xlsx` | 885 | `enut2024` |
| `fd_enadid23.xlsx` | 675 | `enadid2023` |
| `fd_enif2012.xlsx` | 253 | `enif2012` |

Ningún payload de la capa FD necesitó la regla v1_2 (0 vía v1_2, 0 `(sin-instrumento-derivable)` restante) — la capa FD nunca había recibido la v1_1 en absoluto (perímetro de `MAESTRA31-E7` fue solo `inventario-reactivos`), así que resolvió limpio. **Efecto directo sobre la premisa 2:** `P4_8_4` ahora `enif2018` (dos filas, `enif_2018_fd.xlsx`/`enif_2024_fd.xlsx` — la de `enif_2018` es la que trae `P4_8_4`, verificado); `P4_6_4` ahora `enif2015`/`enif2018`/`enif2024` según el archivo (más `endutih2023/2024/2025`, sin cambio, ya resueltos).

### 3.2 · Reactivos — 16 de 39 payloads (41.0%), falsador disparado, no se itera

Por motivo (`etiqueta-regla.md:68-76`), lo que resolvió y lo que no:

| motivo | payloads | resueltos | vía |
|---|---:|---:|---|
| `<año>trim<N>_csv.zip` (ENOE) | 16 | **16** | campo `id` del manifiesto trae literal `enoe_YYYY` (p. ej. `id: enoe_2005_1t_csv_microdatos`) — familia `enoe` adyacente al año, ya presente como dato interno declarado |
| `<timestamp>.export.CSV.zip` (GDELT) | 13 | 0 | ningún campo declarado trae familia canónica del corpus — es dato de GDELT, no de una encuesta del corpus |
| `DescargaMasivaOD_*.xml` | 2 | 0 | uno sin entrada en `manifiesto.yaml` (§1.2); el otro (`382026`) tiene `usado_para` sobre el mecanismo de descarga de CPV — sin familia+año adyacente literal (mención de "CPV 2020" no adyacente al patrón exigido; se declara, no se fuerza) |
| `banxico_encuesta_competencias_financieras_*.xlsx` | 3 | 0 | Banxico/CNBV no es una familia del corpus (ninguna encuesta ya etiquetada del corpus se llama "banxico"/"encf") |
| `cses5_*` | 3 | 0 | CSES no es una familia del corpus |
| `ucdp_ged261_csv.zip` | 1 | 0 | UCDP no es una familia del corpus |
| `zenodo_electoral_*.zip` | 1 | 0 | Zenodo/electoral no es una familia del corpus |
| **total** | **39** | **16 (41.0%)** | |

**Falsador de COMMIT-1(d) disparado** (41.03% < 50%): se reporta como hallazgo sobre `data/manifiesto.yaml`, no sobre el corpus — los 23 payloads restantes son, en su mayoría, fuentes externas al programa de encuestas de INEGI/CONEVAL que este corpus etiqueta (GDELT, CSES, UCDP, Banxico, Zenodo); su manifiesto no declara (ni tendría por qué declarar) una "familia canónica" del corpus de encuestas mexicanas, porque no lo son. **No se itera**: no se aflojó el criterio de adyacencia, no se añadieron campos ni familias. 6,816 filas resueltas (16 payloads), 21,983 quedan `(sin-instrumento-derivable)` (23 payloads).

## 4 · Control positivo — 0 diferencias, ambas tablas

```
FD:        12,704 filas comparadas (las que en v1_0 ya tenían instrumento != '(raiz)') -- 0 diferencias
Reactivos: 149,447 filas comparadas (las que en v1_1 ya tenían instrumento != '(sin-instrumento-derivable)') -- 0 diferencias
```

`149,447 = 178,246 − 28,799` y `12,704 = 17,094 − 4,390` — cuadra exacto con los universos declarados en §0 del COMMIT-1.

## 5 · Re-corrida verbatim de la spec de `MAESTRA32-E2` — deltas por par

Script íntegro (idéntico al de `forense/notas/2026-08-28-empareja-cierre.md` §3 — mismos términos, mismo criterio de `CANDIDATO`/circularidad/co-observación —, repuntado a `data/inventario-reactivos-v1_2.tsv` + `data/inventario-fd-v1_1.tsv`, con las dos claves `DESCARTES` re-clavadas declaradas en COMMIT-1 §4):

```python
#!/usr/bin/env python3
# ACTO MAESTRA32-E6 · ETIQUETA-v1_2 -- re-corrida VERBATIM de la busqueda
# mecanica y los criterios de forense/notas/2026-08-28-empareja-spec.md
# (COMMIT-1 de MAESTRA32-E2), identica a "el script de COMMIT-2, integro"
# pegado en forense/notas/2026-08-28-empareja-cierre.md §3 -- NINGUN
# termino/criterio/DESCARTES cambia de significado. Los UNICOS cambios
# frente a ese script:
#   (1) los dos insumos se leen de las tablas reparadas de este acto
#       (data/inventario-reactivos-v1_2.tsv, data/inventario-fd-v1_1.tsv)
#       en vez de v1_1/v1_0;
#   (2) las DOS entradas de DESCARTES cuyo instrumento citado era
#       literalmente "(raiz)" -- ("U_POB_ELAB_CUL","(raiz)","cuida a") y
#       ("P2_6_3","(raiz)","cuidador") -- se re-clavan con el instrumento
#       ya resuelto por este acto (censo2020 y enut2019 respectivamente,
#       verificado abajo). La RAZON de cada descarte no cambia una letra;
#       solo la clave de instrumento, porque el motivo del descarte es de
#       CONTENIDO (homonimo), no de etiqueta -- exactamente el mismo
#       movimiento que ACTO MAESTRA31-E7 ya aplico al cruce-inverso cuando
#       relaboto candidatos de BD_ENCUCI2020_dbf.zip. Sin este re-clavado,
#       las dos filas dejarian de matchear su propia clave (porque ya no
#       existe ninguna fila con instrumento="(raiz)" en ninguna de las dos
#       tablas) y aparecerian como CANDIDATO sin leer -- lo cual violaria
#       el criterio §3.2 de la spec, no lo cumpliria.
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


REACTIVOS = load("data/inventario-reactivos-v1_2.tsv")
FD = load("data/inventario-fd-v1_1.tsv")
TABLAS = [("inventario-reactivos-v1_2", REACTIVOS), ("inventario-fd-v1_1", FD)]

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
# Excepciones DESCARTADO-con-razón: identicas a empareja-cierre.md, salvo
# las DOS claves re-clavadas de "(raiz)" al instrumento ya resuelto por
# este acto (declarado en el preambulo de este archivo).
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
    ("U_POB_ELAB_CUL", "censo2020", "cuida a"): "homónimo: cuidado de animales/cultivo agrícola, no cuidado de personas -- re-clavado de '(raiz)' a 'censo2020' (ACTO MAESTRA32-E6, Censo2020_CAAS_descriptor_bd.xlsx ya resuelto por la regla v1_1 aplicada por primera vez a la capa FD)",
    ("P2_6_3", "enut2019", "cuidador"): "mide contratación de cuidador(a) remunerado(a) externo (sustituye a la familia), polo opuesto de \"carga de cuidado\" recayendo en la familia -- re-clavado de '(raiz)' a 'enut2019' (ACTO MAESTRA32-E6, enut2019_fd.xlsx ya resuelto por la regla v1_1 aplicada por primera vez a la capa FD)",
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


def veredicto_par(n_theta, n_desenlace, co):
    if co:
        return "EXISTE-SATISFACE"
    if n_theta > 0 or n_desenlace > 0:
        return "EXISTE-NO-SATISFACE"
    return "NO-ENCONTRADO"


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

    with open(f"{ROOT}/data/emparejamiento-motor-v1_1.tsv", "w", newline="", encoding="utf-8") as f:
        f.write("# data/emparejamiento-motor-v1_1.tsv -- ACTO MAESTRA32-E6 · ETIQUETA-v1_2, COMMIT-2 (re-corrida)\n")
        f.write("# Re-corrida VERBATIM de la especificacion congelada de MAESTRA32-E2\n"
                "# (forense/notas/2026-08-28-empareja-spec.md, COMMIT-1) sobre las tablas\n"
                "# reparadas por este acto: data/inventario-reactivos-v1_2.tsv +\n"
                "# data/inventario-fd-v1_1.tsv, en vez de v1_1/v1_0. Ningun termino, criterio\n"
                "# de CANDIDATO/circularidad/co-observacion cambio. Detalle de la re-corrida y\n"
                "# de las dos claves DESCARTES re-clavadas: forense/notas/2026-08-30-etiqueta-v1_2-cierre.md.\n")
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
    deltas = []
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
        v = veredicto_par(n_theta_candidato, n_desenlace_candidato, co)
        print(f"{gen}.{coef}: theta_candidatos_reales={n_theta_candidato} "
              f"(instrumentos={cand_theta}, +placeholder={cand_theta_raiz}) | "
              f"desenlace_candidatos_reales={n_desenlace_candidato} "
              f"(instrumentos={cand_desenlace}, +placeholder={cand_desenlace_raiz}) | "
              f"co_observacion_instrumento_identificado={co} | veredicto={v}", file=sys.stderr)
        deltas.append((gen, coef, v, co))
    print(f"\n# total filas escritas en data/emparejamiento-motor-v1_1.tsv: {len(todas_filas)}",
          file=sys.stderr)
    print("\n# DELTAS_JSON", file=sys.stderr)
    import json
    print(json.dumps(deltas, ensure_ascii=False), file=sys.stderr)
```

**Su salida real** — los conteos `theta hits id=`/`texto=` y `desenlace hits id=`/`texto=` de los 9 pares son **byte a byte idénticos** a los de `forense/notas/2026-08-28-empareja-cierre.md` §4 (estructuralmente garantizado: `variable_id`/`texto_reactivo` no cambiaron entre `v1_1→v1_2` ni entre `v1_0→v1_1`, solo `instrumento`; el conjunto de filas que matchea un término fijo no puede cambiar). **715 filas escritas**, igual que `v1_0` — mismo motivo. Lo único que cambia, fila por fila (verificado con diff programático, ver §6): la columna `instrumento` de las filas que antes citaban un placeholder, y la columna `razon` de las dos entradas `DESCARTES` re-clavadas.

## 6 · Deltas por par — tabla completa (antes/después)

| par | veredicto antes (`v1_0`) | veredicto después (`v1_1`) | co-observación antes | co-observación después | movimiento |
|---|---|---|---|---|---|
| `G5.familismo_apoyo` | EXISTE-NO-SATISFACE | EXISTE-NO-SATISFACE | `[]` | `[]` | sin cambio (θ ahora en `enfih2019`/`enif2015`/`enif2024`/`enut2019`/`enut2024` en vez de placeholder; desenlace sin cambio — instrumentos distintos, siguen sin coincidir) |
| `G5.radio_confianza` | EXISTE-NO-SATISFACE | EXISTE-NO-SATISFACE | `[]` | `[]` | sin cambio (θ ahora también en `enif2012`/`enif2015` además de `encup2012`; desenlace sin cambio, sin coincidencia) |
| `G5.familismo_obligacion` | EXISTE-NO-SATISFACE | EXISTE-NO-SATISFACE | `[]` | `[]` | sin cambio (θ sigue en 0 hits reales) |
| `G2.sens_estatus` | NO-ENCONTRADO | NO-ENCONTRADO | `[]` | `[]` | sin cambio |
| `G2.aversion_riesgo` | NO-ENCONTRADO | NO-ENCONTRADO | `[]` | `[]` | sin cambio |
| `G3.aversion_riesgo` | EXISTE-NO-SATISFACE | EXISTE-NO-SATISFACE | `[]` | `[]` | sin cambio (desenlace ahora también en `enif2012`/`enif2015`/`enif2018`/`enif2024` además de `enfih2019`; θ sigue en 0 hits reales) |
| `G4.horizonte_temporal` | EXISTE-NO-SATISFACE | EXISTE-NO-SATISFACE | `[]` | `[]` | sin cambio en veredicto, pero **θ ya no es placeholder**: `enif2018`/`enif2024` (antes solo `(raiz)`) — es el efecto directo de reparar la capa FD; desenlace sigue en 0 hits, así que no co-observa |
| `G4.sens_estatus` | NO-ENCONTRADO | NO-ENCONTRADO | `[]` | `[]` | sin cambio |
| `G6.deferencia` | EXISTE-NO-SATISFACE | EXISTE-NO-SATISFACE | `[]` | `[]` | sin cambio |

**Movimientos: 0 de 9.** Ninguno bajó (cumple B-bis: solo se permite subir o quedarse). **0 `EXISTE-SATISFACE` nuevos** — no se habilita ningún medidor sucesor en caja por este acto. Resultado informativo válido, no cuello de botella de etiqueta: los 6 pares `EXISTE-NO-SATISFACE` lo eran porque θ y desenlace viven en instrumentos genuinamente distintos (o falta un lado por completo), no porque la etiqueta escondiera una coincidencia real — la reparación de `(raiz)`/`39 payloads` sí cambió qué instrumento citan las filas, pero en ningún caso ese instrumento pasó a coincidir con el del otro lado del par. Diff fila-a-fila entre `emparejamiento-motor-v1_0.tsv` y `-v1_1.tsv`: 715/715 filas difieren solo en `instrumento` (para las que antes eran placeholder) y/o `tabla` (nombre de tabla fuente, actualizado de `v1_0`/`v1_1` a `v1_1`/`v1_2`); `razon` cambia solo en las 2 filas `DESCARTES` re-clavadas; ninguna fila nueva, ninguna fila perdida, ningún `variable_id`/`texto`/`via`/`termino` cambió.

## 7 · Intocables — `git diff --stat` vacío, verificado

```
$ git diff --stat -- data/inventario-reactivos-v1_1.tsv data/inventario-fd-v1_0.tsv \
    data/emparejamiento-motor-v1_0.tsv tools/inventario_reactivos.py \
    forense/notas/2026-08-28-empareja-spec.md
(sin salida)
```

## 8 · CONTADOR

Placeholders de instrumento: **FD `4,390 → 0`**; **reactivos `28,799 → 21,983`** (6,816 resueltas, 16/39 payloads, 41.0%, falsador <50% disparado, no se itera). Veredictos de E2 movidos: **0 de 9** — la cifra es la medición, incluido cero.

## 9 · Lo que este acto NO hizo

No midió nada. No abrió microdato ni `data/raw` (ausente, no creada ni enlazada, no necesaria). No cambió `ruta:`/`nota:` en `milpa/procedencia.yaml` (verificado, `git diff --stat` de este acto no toca `milpa/`). No editó `forense/notas/2026-08-28-empareja-spec.md` ni los veredictos originales de `MAESTRA32-E2` (quedan como historia; `emparejamiento-motor-v1_1.tsv` es el re-sello, no una edición hacia atrás). No reabrió `MAESTRA32-E4 · RE-EMPAREJA` (ese es el re-sello por universo ampliado tras los extractores; este es por etiqueta reparada sobre el mismo universo — declarado, dos cosas distintas). No tocó `tools/inventario_reactivos.py` ni ninguna tabla existente fuera del perímetro. No escribió en `data/manifiesto.yaml` ni `data/manifiesto-staging.yaml` (la ausencia de entrada de `DescargaMasivaOD_582026_...` se declaró, no se corrigió — fuera de perímetro). No resolvió el rótulo E6/E7 intercambiado frente a lo que `MAESTRA32-E5` había previsto — solo lo declaró.

## 10 · Cascada

`forense/firmas-pendientes.tsv`: fila nueva `FP-180` (mesa recibe etiqueta v1_2 + deltas del re-emparejamiento). `canon/gobernanza-v1_15.md`: `ADR-223` (candidato re-derivado, máximo `222` sin huecos), cabecera de conteo `222→223`. `canon/estado-programa-v1_10.md`: recifra `222→223` en la tabla de artefactos (línea 27) y en `L0` (línea 105, entrada nueva antepuesta, sin tocar las anteriores). `canon/registro-rotulos.tsv`: fila nueva `E`/`MAESTRA32-E6` — token pelado `E6` colisiona con `MAESTRA31-E6` (`DICCIONARIOS-FD`) y con ningún otro habitante del espacio E; se censa, no se reclama, D-6. `tests/check.py` `_T25_ARCHIVOS_CONOCIDOS`: se añaden los archivos nuevos de este acto que traen el patrón `E6` pelado (verificado por comando cuáles lo traen antes de tocar el test). `data/INFRAESTRUCTURA-v1_0.md`: línea 222 actualizada para citar `inventario-fd-v1_1.tsv`/`inventario-reactivos-v1_2.tsv`/`emparejamiento-motor-v1_1.tsv` en vez de sus predecesoras, con la cita de `ADR-223` añadida.

## 11 · `tests/check.py --baseline` — resultado, T03 nuevo declarado (no editado)

```
$ python3 tests/check.py --baseline
19 FAIL · 136 WARN
[ ok ] T25 T-ROTULOS
LÍNEA BASE: ROJO — 1 entrada nueva frente a tests/baseline.json (HEAD congelado e24d033ed3c095f1e81c2fbb8248f108e9d3ef65)
  · T03: forense/encargos/2026-08-30-MAESTRA32-E6-ETIQUETA-v1_2.md: cita "empareja-spec.md" (sin backticks aquí a propósito, ver nota abajo, para no disparar T03 otra vez), que no existe
(5 entradas de la línea base ya no aparecen -- mejora, no bloquea, no baja la cifra congelada sin --freeze explícito)
```

**T25 pasa limpio** (los tres archivos nuevos con rótulo `E6`/`E7`/`E2`/`E5`/`E3`/`E8` pelado quedaron censados en `_T25_ARCHIVOS_CONOCIDOS`, ver §10). **19 FAIL — sin regresión** frente a la línea base (mismo conteo). **136 WARN — mejora de 1** frente a la corrida previa a este acto (137), por causas ajenas a este acto (no se investigó, fuera de perímetro).

**Un T03 nuevo, mismo defecto de clase que A8-LAND/"v2_6.md" (`canon/gobernanza-v1_15.md:766`) y ACTO MAESTRA31-E9/E10:** `forense/encargos/2026-08-30-MAESTRA32-E6-ETIQUETA-v1_2.md` §"Intocables verificados" cita "empareja-spec.md" (deliberadamente sin backticks en esta misma frase, mismo patrón que `gobernanza-v1_15.md:766` usa para no disparar T03 una segunda vez al discutirlo) sin el prefijo de fecha (`2026-08-28-`) que trae el nombre de archivo real — texto verbatim de dirección (A.3), **no se edita para complacer a un test**, mismo precedente citado arriba. Declarado aquí, no recongelado: `tests/baseline.json` **no se toca** (recongelar exige ADR de mesa, precedente `canon/gobernanza-v1_15.md:1110`; un ejecutor que encuentra drift lo reporta, no lo recongela). Las otras citas bare que corridas previas de este mismo documento encontraron ("empareja-cierre.md", "etiqueta-regla.md", texto propio del ejecutor, no de dirección) se corrigieron a ruta completa antes de esta corrida final — no eran verbatim de nadie, no había razón para dejarlas rotas.

## 12 · Resumen ejecutado (el detalle completo que `## CONSUMIDO` del encargo cita)

Ejecutado en la rama `claude/maestra32-e6-cloud-launch-8qu0hw`. Esta sesión NO abre PR — commitea y pushea a la rama designada, mismo patrón que `MAESTRA32-E2`/`E5` para no repetir el defecto ya visto en el acto E9. Número de PR: N/D desde esta sesión; quien fusione (dirección, u otra sesión con permiso de abrir PR) llena ese campo al abrirlo. Resultado: capa FD reparada 10/10 payloads (100%, primera vez que recibe la regla de etiqueta); 16 de 39 payloads de reactivos resueltos por la regla v1_2 (41.0%, falsador <50% disparado, no iterado); re-corrida verbatim de la spec de `MAESTRA32-E2` con 0 de 9 veredictos movidos (resultado informativo); `ADR-223`; `FP-180` nueva; `tests/check.py --baseline` → 19 FAIL · 136 WARN, T25 verde, 1 T03 nuevo declarado (verbatim de dirección, no editado, no recongelado).
