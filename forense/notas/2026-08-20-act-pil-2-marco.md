# Nota · ACTO ACT-PIL-2 · MARCO-M1-A — cierre

**Fecha:** 2026-08-20 · **Rama:** `act-pil-2` · **Encargo:** `forense/encargos/2026-08-20-ACT-PIL-2.md`
**Base:** `7d38cb0` (`origin/main` al arrancar, = el SHA que el encargo declara). `origin/main` se movió a `906203a` durante el acto (`PR #296`, `ACT-PIL-1 · CONTRATO-v0_5`) y se fusionó dentro de esta rama antes de escribir el ADR — por eso este acto renumera de `ADR-129` a `ADR-130`.
**Entorno:** UBUNTU. `data/raw` **enlazada** por este acto.
**ADR:** `ADR-130`. **Contador que nace:** `candidatas del marco: 60 de 60`.

---

## 0 · ARRANQUE (A.2), las cinco partes

| # | Comprobación | Salida cruda |
|---|---|---|
| 1 | REPO | `/home/pc0/Modelado-Mexicano` → `github.com/Josanoforo/Modelado-Mexicano`; worktree del acto `/home/pc0/mm-act-pil-2`, rama `act-pil-2` |
| 2 | SHA | `git rev-parse --short origin/main` → `7d38cb0` = el declarado. `PR #295` fusionado: compuerta confirmada, los cinco filtros de `ADV1-M1` legibles en `forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md` §B |
| 3 | `data/raw` | **la enlacé** — `NO EXISTE` en el worktree nuevo; `ln -s /home/pc0/mm-corpus/raw data/raw` → `data/raw -> /home/pc0/mm-corpus/raw` |
| 4 | ENTORNO (3 crudos) | variable: `sin_variable` (esperado) · `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` → `200` (esperado) · `ls data/raw/ \| head -1` → `20260813130000.export.CSV.zip`, 289 entradas (no vacío, esperado) |
| 5 | ESPEJO | no tocado |

`type grep` → **es una función** que ejecuta `claude -G` con `ARGV0=ugrep` y `-I`. Todo negativo de esta nota usa `command grep` (`/usr/bin/grep`) o `git grep`, y va con control positivo.

`pgrep -af claude` sólo ve mis dos `bash -c`; no ve la sesión de `ACT-PIL-1`, consistente con la cicatriz ya conocida. Perímetros disjuntos por diseño; la única intersección real fue el número de ADR, resuelta por la regla de la casa.

**Una corrección de cifra al encargo, sin consecuencia:** el encargo dice «árbol completo menos `.git`, 1 717 archivos». Ese es el conteo en `5a60e98` (la base de `SELLA-ADV`). En `7d38cb0`, la base de ESTE acto, son **1 725** — los 8 archivos que `SELLA-ADV` añadió. `git ls-tree -r --name-only 7d38cb0 | wc -l` → `1725`; `... 5a60e98 ...` → `1717`.

---

## 1 · T0 · Compuerta de operabilidad — RESUELTO, con archivo y página

La premisa del encargo se verifica primero, sobre el árbol **rastreado** (no el de trabajo):

```
git grep -l -F "CAC-007" 7d38cb0
  forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md
  forense/compass-5-d3f09137-estado-arte-duelo-2026.md
git grep -l -F "INEGI" 7d38cb0 | wc -l        → 279     (control positivo)
```

Exacto: dos archivos, los dos adversariales citando el acuerdo, ninguno con la cifra.

### Los cinco intentos, con su salida

| # | Intento | Salida cruda | ¿Rinde? |
|---|---|---|---|
| 1 | Árbol rastreado completo | arriba | NO |
| 2 | Los dos IPE de precisión del corpus (`ipe_inegi/CV-EE-IC_IPE_Externos_Encuestas_2022_08_26.xlsx`, `enasic2022/IPE_…xlsx`) | volcado completo: 33 filas de plantilla que **definen** `CV`, `ErrorEst`, `Niv_Conf`… y ningún umbral | NO |
| 3 | Los 158 PDF sueltos de `data/raw` → `pdftotext -layout` → grep | `CAC-007` → `EXIT=1`, **0 aciertos**; control positivo: 93 de 158 contienen `INEGI`. `semáforo` → 12 aciertos, **los 12** son la pregunta `P4_7_3` de ENCIG sobre semáforos de calle | PARCIAL |
| 4 | 354 zips, **24 318 entradas**, filtradas por nombre | 3 documentos metodológicos: `enoe_n_diseno_muestral.pdf`, `enoe_n_diseno_conceptual.pdf`, `ELCOS2012_Diseno_muestral.pdf` | PISTA |
| 5 | Extraer esos 3 y greparlos | **1 acierto de `CAC-007`, con la cifra** | **SÍ** |

El intento 3 ya había dado la banda **sin** el acuerdo: `data/raw/enasic2022/889463927082.pdf`, INEGI, *ENASIC 2022. Conociendo la base de datos*, **pág. física 12 (folio 9), §3 «Precisiones estadísticas»** — «Alta, CV en el rango de (0,15) · Moderada, CV en el rango de [15,30) · Baja, CV de 30% en adelante».

### La cifra, con el acuerdo nombrado

> `data/raw/enoe_n_trim3_2020-trim4_2022.zip` :: `3. Metodología/Metodologías/enoe_n_diseno_muestral.pdf`
> INEGI, *Encuesta Nacional de Ocupación y Empleo. Nueva edición. ENOE N. Diseño muestral*, 2021 — **página física 8 de 10, folio impreso 5**, §9 «Homologación de la Semaforización para los Umbrales de Indicadores de precisión estadística».
>
> «*el Comité de Aseguramiento de la Calidad, en la cuarta sesión celebrada el 1 de noviembre de 2018, aprobaron los siguientes umbrales*»
>
> Cuadro **«Umbrales aprobados para la cobertura del CV»**, columna *Viviendas/Hogares/Otras unidades diferentes a las económicas · DGES/DGEGSPJ*:
>
> | Interpretación | Semaforización | Umbral |
> |---|---|---|
> | Alta | Blanco | **[0%, 15%)** |
> | Moderada | Amarillo | **[15%, 30%)** |
> | Baja | Naranja oscuro | **>=30%** |
>
> Pie: «*Umbrales aprobados para el reporte de la precisión de acuerdo con el coeficiente de variación en los tabulados de resultados de los proyectos con muestreo probabilístico (**acuerdo CAC-007/01/2018**)*».
> Nota al pie 2: la fuente original es `http://intranet.inegi.org.mx/calidad/wp-content/uploads/2017/02/Homologacion_de_umbrales.pdf` — **intranet de INEGI, no alcanzable**, y por eso el documento del corpus es hoy la mejor cita disponible.

**Por qué las búsquedas previas no lo veían:** está dentro de un `.zip`, y todas las búsquedas del árbol operan sobre archivos descomprimidos.

**El filtro (iii) NO queda `PENDIENTE-UMBRAL`.** Lo que sí queda abierto —y no se inventa— es **cuál de las tres bandas** significa «bajo el umbral»: `ADV1-M1` dice «el umbral» y el acuerdo aprueba tres. `FP-79`.

### Receta manual para mesa (A.5), por si quiere la fuente primaria

Un minuto en un navegador:

1. Abrir `https://www.inegi.org.mx/programas/enoe/15ymas/#documentacion` (o `#microdatos`).
2. Sección **Metodología → Diseño muestral**; descargar el PDF de la edición «Nueva edición (ENOE N)».
3. Ir a la **página 5** (folio impreso) → §9, cuadro «Umbrales aprobados para la cobertura del CV».
4. Si se quiere la fuente primaria del Comité de Aseguramiento de la Calidad: `Homologacion_de_umbrales.pdf` vive en la **intranet** de INEGI y requiere pedirla por transparencia o a un contacto institucional. El documento público que la cita con la cifra es el que este acto ya pegó.

*(La misma receta no puede correrse por `curl` desde esta caja: ver §5.)*

---

## 2 · T1 · La plantilla, y una decisión de escritura declarada

`forense/marco-candidatas-piloto-v1_0.tsv` nació en **commit propio** (`9c5bdff`), con sus 17 columnas y **cero filas**, antes de enumerar nada. Las columnas salen de `ADV1-M1` verbatim, no de memoria.

**Decisión declarada, no escondida:** `ADV1-M1` pide para el filtro (i) «`SI|NO`, con la prueba del bibliotecario y su resultado». Se conservó **una** sola columna `publicada` —el encargo enumera 17 y «verbatim» gobierna— y la celda lleva la forma `SI|NO|PENDIENTE :: prueba :: resultado`, sin tabs, verificable con `cut -f10`. Si mesa prefiere dos columnas es un cambio de una línea.

El commit cierra con la frase literal que el encargo fija.

---

## 3 · T2 · Enumeración por comando — seis tandas, 60 filas

Ejecutores **Sonnet supervisados** para lo mecánico (cuatro tandas de dominio); las dos tandas restantes las hizo el supervisor. **Ninguna candidata de memoria:** cada fila trae nombre de variable verbatim con archivo y hoja/fila o página del corpus.

| Tanda | n | Dominios | Instrumentos |
|---|---|---|---|
| `CIV` | 12 | cívico, trámite | ENCIG 2019/2021/2023 · ENCUCI 2020 · ENVIPE 2018/2023/2025 · ENPOL 2021 |
| `DIN` | 12 | dinero | ENIF 2012/2015/2018/2024 · ENFIH 2019 · ECF Banxico-CNBV 2019/2021 |
| `SFT` | 12 | salud, familia, tiempo | ENASIC 2022 · ENASEM 2018/2021/2024 · ENUT 2019/2024 · ENADID 2023 · ENDIREH 2021 · ENBIARE 2021 |
| `TIC` | 12 | trabajo, información, comunicación, cooperación | ENOE 2024T1 · ENOEN 2022T2 · ENTI 2022 · ENDUTIH 2023/2024/2025 · MOCIBA 2023/2024 |
| `EMP` | 6 | dinero, familia, trabajo | ENAFIN 2024 (vía su IPE publicado) · CPV 2020 cuestionario ampliado |
| `DOC` | 6 | dinero | desenlaces documentados **no-encuesta**, de `compass-4`: CNBV / BMV / SEC |

### Qué encontró la auditoría del supervisor

Las **60** citas se re-verificaron **una por una**, no por muestreo. Tres clases de defecto, todas corregidas y re-verificadas:

1. **19 filas citaban un archivo de trabajo** (el TSV consolidado de FD o los `.txt` de `pdftotext`) en vez de un archivo del corpus. Re-citadas a `data/raw/...` con hoja+fila (xlsx) o página física (PDF), y re-verificadas de forma independiente por página.
2. **Un ponderador de la tabla equivocada.** El `FD` de ENTI 2022 tiene **siete** variables llamadas `FAC`, una por tabla. La candidata vivía en `ENTI2022_COE1` y citaba el `FAC` del bloque de `SDEM`. Corregido a pág. 59.
3. **Cuatro citas de fila del IPE de ENAFIN corridas un renglón** (*Micro* contra *Pequeña*), detectadas al re-imprimir el bloque de filas. Corregidas.

### Las exclusiones de `DOC`, y por qué

De los 11 casos de `compass-4` entran **6**. **No** entran los cuatro `CONFUNDIDO` (Famsa, Crédito Real, AlphaCredit, CAME) — el propio documento dice que «no permiten aislar la variable conductual». **Tampoco** entran las tandas/ROSCAs: su tasa de default está literalmente `NO ENCONTRADA` en el documento, y una celda sin cifra no tiene árbitro. `DOC-03` es la que más vale del lote: la **razón** entre el IMOR ajustado del segmento popular y el de la tarjeta de la banca múltiple es la pregunta sustantiva completa, y `compass-4` yuxtapone `10.7%` y `13.7%` **sin dividirlos** — nadie la ha enunciado.

### `grado_dependencia`, derivado y no tecleado

`P0` = el par `(encuesta, ola)` aparece en `milpa/procedencia.yaml` como ruta de parametrización de `M`. Derivado por barrido del YAML: **ENCIG 2021, ENCIG 2023, ENCUCI 2020, ENIF 2024, ENVIPE 2025, ENASIC 2022**, más **ENIGH 2022** por lectura **conservadora** de `milpa/catalogo-momentos-v0_1.tsv` (declara ENIGH 2022 nueva serie como universo de los momentos `AJUSTE`, aunque ninguno se ha corrido). `P1` = misma familia, otra ola, o familia nombrada sin ola. `P2` = el resto.

---

## 4 · T3 · El tamaño es 60 — y de dónde sale el 60

**No se para: 60 está dentro de 40-60.** Y se dice sin adorno de dónde sale.

El procedimiento se fijó **antes** de enumerar: 12 candidatas por lote de dominio (4 lotes) más 6 por cada lote del supervisor. `48 + 12 = 60`, que es **exactamente el techo de `ADV1-M1`, por construcción y no por descubrimiento**. El límite **no** fue la oferta del corpus: varios lotes podían dar más, y los que no rindieron lo declararon con comando y salida (ENCUP sin FD propio; ENSAFI sólo con el zip de datos; ENIGH con diccionarios sin texto de reactivo; ENIF 2021 sin FD suelto; ECF 2024 sin manual convertido; ELCOS en `.xls` antiguo que `openpyxl` no abre y sin `xlrd`/`unzip`/`libreoffice` en la caja; ENAPROCE sólo con microdato de ejemplo).

Eso hace del tamaño una función de **mi** parámetro, no del corpus, y por eso va a tablero (`FP-82`): mesa decide si el tope de 12 se justifica o el marco se agranda **antes** del sorteo. Agrandarlo después rompe el pre-registro.

### Cuotas, verificadas por comando

```
N = 60 candidatas
  CUMPLE  | tamano del marco                       |         60 | ADV1-M1: 40-60
  CUMPLE  | publicadas (control de memoria)        |  4 =  6.7% | ADV1-M1: maximo 20%
  CUMPLE  | P2 (fuente distinta o desenlace doc.)  | 33 = 55.0% | ADV1-M1: >=1/3
  CUMPLE  | desenlaces documentados no-encuesta    |          6 | ADV1-M1: >=2 dentro de P2
  CUMPLE  | post-corte u ola retenida              |          9 | ADV1-M1: >=3-5
  CUMPLE  | condicionales/subgrupo (MEDIA+DIFICIL) | 58 = 96.7% | ADV1-M1: cuota sin cifra
  reparto de grado: P0=10 P1=17 P2=33
  dificultad: DIFICIL=14 FACIL=2 MEDIA=44
  estratos distintos: 26 · encuestas distintas: 26
  duplicados (encuesta,ola,variable): 0 · ids unicos: 60 de 60
```

**Las seis cuotas cumplen.** Lo que **no** está bien equilibrado se reporta igual, porque el encargo pide reportar aunque no cumpla:

- **22 de 60 son dominio `dinero`** y **sólo 1 es `cooperacion`**; `informacion` tiene 2. El marco está escorado.
- **`FACIL = 2`** contra `MEDIA = 44` y `DIFICIL = 14`. Casi no hay celdas fáciles, lo que sube el riesgo de la casilla (5) de `ADV1-M5` («ambos lejos de `R`»), que el FFC ya predice como el desenlace más probable.
- **Las 10 `P0` van al anexo de plomería, fuera del marcador**: el marco es de **60**, el **marcador puntuable es de 50**.
- 26 estratos para un piloto de 12-15: el sorteo por round-robin (§6) toca el mayor número posible de estratos, pero **la mitad de los estratos no entrará al piloto**, y eso es una limitación del tamaño, no del sorteo.

### La colisión entre dos filtros de `ADV1-M1`

Al montar apareció algo que el careo no anticipó: **la ola más reciente de una encuesta suele ser justo la que parametrizó el motor.** `CIV-11` (ENVIPE 2025) y `DIN-04` (ENIF 2024) salieron simultáneamente `P0` por el filtro (ii) y «ola retenida» por el filtro (v). No se puede retener una ola que ya se usó. Se resolvió por **regla escrita en el montador**, no a mano: **(ii) gana sobre (v)**, `post_corte` pasa a `NO` en toda fila `P0`. Cuenta de olas retenidas `11 → 9`, sigue sobre el piso.

---

## 5 · Lo que `ADV1-M1` pide y este entorno NO puede cerrar

De los cinco filtros de `ADV1-M1`, este acto ejecuta enteros **(ii)**, **(iv)** y **(v)**. Los otros dos, no — y no se rellenan con números plausibles.

### (i) La prueba del bibliotecario no es ejecutable sin navegador

```
# control negativo: una URL que no puede existir
curl -s -o /dev/null -w "%{http_code} %{size_download}\n" --max-time 15 \
  https://www.inegi.org.mx/programas/xxxxx-no-existe-jamas/9999/     → 200 13370

# control positivo: la red está bien, un producto real sí baja
curl -s -o /dev/null -w "%{http_code} %{size_download} %{content_type}\n" --max-time 30 \
  https://www.inegi.org.mx/contenidos/.../nueva_estruc/889463927082.pdf
                                                    → 200 1390271 application/pdf

# la página de programa no sirve su propio contenido
curl -s https://www.inegi.org.mx/programas/encig/2023/ | command grep -c "tabulado"  → 0
curl -s https://www.inegi.org.mx/sitemap.xml | head -c 800   → UNA sola <url>
```

`www.inegi.org.mx` es una SPA con **soft-404**: devuelve `200` para todo. Un `200` de una URL `/programas/…` **no es evidencia de nada**.

Se corrió **la mitad que sí corre**: criba de mnemónico sobre el árbol rastreado (`git grep -l -F <mnemónico> 7d38cb0`), con la cifra escrita **en cada celda** y etiquetada explícitamente **CRIBA, no prueba** — porque un mnemónico citado en una nota forense no es una cifra publicada por INEGI, y porque la criba está llena de falsos positivos: `P1` → 213 archivos, `P2` → 177, `P3` → 117, `razon` → 232.

Resultado: **4 `SI`** (con evidencia positiva en la mano), **0 `NO` por búsqueda**, **56 `PENDIENTE-BIBLIOTECARIO`**. `FP-81`.

**Receta manual para mesa, un minuto por celda:** abrir `https://www.inegi.org.mx/programas/<programa>/<año>/`, pestaña **Tabulados**, buscar el cuadro que cruce la variable con el eje de condicionamiento de la fila; si el cruce exacto no está listado, la celda es `NO`. Sólo funciona en navegador: la pestaña la arma JavaScript.

### (iii) El CV del árbitro no existe antes de que exista el árbitro

El propio archivo oficial de precisión de ENASIC 2022 que INEGI publica tiene **2 filas con dato y 335 vacías** (derivado con `openpyxl`). Ni la fuente oficial cubre el filtro. La **única** excepción del marco es `EMP-01`, con `CV 5.838` publicado por INEGI en el IPE de ENAFIN 2024 — que además trae **88** filas con CV real y demuestra que el filtro **muerde**: 5 de esas 88 tienen `CV >= 30%` y quedarían fuera por la banda «Baja».

Y el **piso de `n` no ponderado** del mismo filtro **no tiene cifra en ninguna parte del árbol**; además el `n` de una celda **condicional** tampoco se conoce ex ante. `FP-80`.

**Lectura que el marco deja escrita:** `ADV1-M1(iii)` no es una compuerta *ex ante*, es una condición *post-hoc* — salvo que mesa la reinterprete sobre el `n` de la **encuesta** en vez del de la **celda**.

### El choque `ADV1-M1(iii)` contra `ADV1-M3`

`ADV1-M1` obliga a incluir `>=2` desenlaces documentados no-encuesta. `ADV1-M3` puntúa contra `R` **como distribución** y declara `INDECIDIBLE` si `|d_L−d_M| < 0.5·EE(R)`. Un censo administrativo o un estado financiero dictaminado tiene `EE` muestral **cero**: `INDECIDIBLE` **nunca** dispara en las 6 filas que `ADV1-M1` obliga a meter, y el árbitro es puntual. Los dos mecanismos se contradicen exactamente ahí. `FP-83`.

---

## 6 · T4 · El sorteo — escrito, NO corrido

**No se corrió, y el procedimiento se niega a correr solo.** Va aquí verbatim, dentro de la nota, porque `tests/` está fuera de perímetro.

**La semilla es el SHA de 40 hex del commit de *merge* del PR de este acto.** Ese objeto no existe mientras el PR está abierto: es público, verificable contra GitHub, está fuera del control del ejecutor y es posterior al congelamiento del marco. Cualquier otra semilla (fecha, hash del propio TSV, `/dev/urandom`) o bien la controla quien sortea, o bien es anterior al congelamiento — las dos matan el propósito, que es que el set del piloto no lo elija el dueño del motor (`ADV-1`, hallazgo #5).

```python
#!/usr/bin/env python3
"""SORTEO DEL PILOTO -- ADV1-M1. ESCRITO EN ACT-PIL-2, NO CORRIDO AQUI.
Uso en ACT-PIL-3:  python3 sorteo.py <SHA40_DEL_MERGE> forense/marco-candidatas-piloto-v1_0.tsv"""
import sys, hashlib, subprocess
from collections import defaultdict

def cargar(p):
    lns=[l.rstrip("\n") for l in open(p,encoding="utf-8") if l.strip()]
    return lns[0].split("\t"), [l.split("\t") for l in lns[1:]]

def verifica_semilla(sha):
    if len(sha)!=40 or any(c not in "0123456789abcdef" for c in sha.lower()):
        sys.exit("PARA: la semilla debe ser un SHA de 40 hex del commit de merge.")
    padres=subprocess.run(["git","rev-list","--parents","-n","1",sha],
                          capture_output=True,text=True)
    if padres.returncode!=0:
        sys.exit(f"PARA: {sha} no existe en este repo. git fetch origin main primero.")
    n=len(padres.stdout.split())-1
    if n!=2:
        sys.exit(f"PARA: {sha} tiene {n} padre(s); el commit de merge de un PR tiene 2. "
                 "No se sortea con una semilla que no sea el merge del PR de ACT-PIL-2.")
    return sha.lower()

def orden_en_estrato(sha, estrato, filas, ix):
    """Llave determinista sha256(semilla|estrato|id). Reproducible con printf y
    sha256sum en cualquier lenguaje. random.Random() NO se usa: su secuencia no
    esta garantizada entre versiones de Python."""
    return sorted(filas, key=lambda r: hashlib.sha256(
        f"{sha}|{estrato}|{r[ix['id']]}".encode()).hexdigest())

def main():
    if len(sys.argv)<3: sys.exit(__doc__)
    sha=verifica_semilla(sys.argv[1]); ruta=sys.argv[2]
    hdr,filas=cargar(ruta); ix={c:i for i,c in enumerate(hdr)}
    est=defaultdict(list)
    for r in filas: est[r[ix['estrato']]].append(r)          # 1. particion en estratos
    ordenados={k:orden_en_estrato(sha,k,v,ix) for k,v in est.items()}   # 2. orden interno
    # 3. orden GLOBAL: round-robin entre estratos; el orden de los estratos tambien
    #    lo fija la semilla. Round-robin y no muestreo proporcional, para que el
    #    piloto de 12-15 toque el mayor numero posible de estratos -- ADV1-M1 estratifica
    #    precisamente para eso.
    orden_estratos=sorted(ordenados, key=lambda k: hashlib.sha256(f"{sha}|EST|{k}".encode()).hexdigest())
    global_=[]; i=0
    while len(global_)<len(filas):
        for k in orden_estratos:
            if i<len(ordenados[k]): global_.append(ordenados[k][i])
        i+=1
    for n,r in enumerate(global_,1):
        print(f"{n}\t{r[ix['id']]}\t{r[ix['estrato']]}\t{r[ix['encuesta']]}\t{r[ix['variable']]}")
    print(f"\n# semilla={sha}\n# N={len(global_)}\n# estratos={len(ordenados)}", file=sys.stderr)
    print("# Lo no producido se registra SKIP con motivo, al mismo tamano que el marcador (ADV1-M4-iii).",
          file=sys.stderr)

if __name__=="__main__": main()
```

**Las dos guardas, demostradas y no supuestas:**

```
$ python3 sorteo.py
SORTEO DEL PILOTO -- ADV1-M1, "sorteo con semilla publica dentro de estratos".
ESCRITO EN ACT-PIL-2, NO CORRIDO AQUI. Se corre en ACT-PIL-3.
   (imprime el docstring y sale: se niega sin semilla)

$ python3 sorteo.py $(git rev-parse HEAD) forense/marco-candidatas-piloto-v1_0.tsv
PARA: 9c5bdffc67214675889dd1413e05d21ed56f1b2c tiene 1 padre(s); el commit de merge
de un PR tiene 2. No se sortea con una semilla que no sea el merge del PR de ACT-PIL-2.
```

El **corte exacto** dentro de 12-15 lo firma mesa **antes** de correr esto; no lo elige el script.

---

## 7 · Contaminación (`ADR-46`) — declarada hasta dónde

Esta sesión **exploró estructura** del corpus: FD, diccionarios, cuestionarios y documentos metodológicos de 26 encuestas, más los dos IPE de precisión y tres PDF de diseño muestral extraídos de zips.

**Cero microdato de valores.** Los únicos archivos abiertos *dentro* de zips fueron `diccionario_de_datos/*.csv` de ENOE/ENOEN (catálogos de columnas: nombre, ancho, tipo, rango — sin una sola fila de datos) y los tres PDF de metodología. Ninguna estimación, ninguna tabla de frecuencias, ningún `head` de un CSV de microdato.

Bajo `ADR-46` eso **inhabilita a esta sesión** para pre-registrar una *estimación* contra esas fuentes. No toca al corredor `L`, que `ADV1-M2` exige correr en sesión limpia ajena a las celdas de `M`. **El marco es un pre-registro de *specs*, no de estimaciones**, y por eso construirlo aquí es compatible con `ADR-46`; el conservador declara más exploración, no menos.

---

## 8 · Lo que este acto deja abierto

| Fila | Qué |
|---|---|
| `FP-79` | Cuál de las tres bandas de `CAC-007/01/2018` gobierna «CV bajo el umbral». La cifra ya está; falta la elección. |
| `FP-80` | El piso de `n` no ponderado no tiene cifra, y el `n` de una celda condicional no se conoce ex ante. |
| `FP-81` | La prueba del bibliotecario no corre sin navegador; 56 de 60 filas en `PENDIENTE-BIBLIOTECARIO`. |
| `FP-82` | El tamaño 60 es el techo de `ADV1-M1` por construcción; ¿se justifica el tope de 12 por lote o se agranda el marco antes del sorteo? |
| `FP-83` | `ADV1-M1(iii)` contra `ADV1-M3` en las 6 celdas de desenlace no-encuesta: `EE = 0`, `INDECIDIBLE` nunca dispara. |
| `FP-84` | `data/diseno-muestral.yaml` vencido de hecho: 14 de 32 `PENDIENTE` ya tienen payload. |

Además, cinco líneas en `forense/hallazgos.md`.

---

## 9 · Contadores

**Nace: `candidatas del marco: 60 de 60`** (`canon/estado-programa-v1_10.md` §L5). Población de conteo **propia**: cuenta *specs pre-registradas*, no mediciones. Cifra derivada por `awk -F'\t' 'NR>1' forense/marco-candidatas-piloto-v1_0.tsv | wc -l` → `60`, no tecleada.

**Y se declara explícitamente, porque el programa ya pagó una vez por no declararlo** (`FP-68`, `ADR-67(c)`, cicatriz en `estado-programa:99`):

- **NO toca `momentos HOLDOUT reproducidos: 0 de 14`** — verificado por comando: `awk -F'\t' 'NR>1 && $4=="HOLDOUT"' milpa/catalogo-momentos-v0_1.tsv | wc -l` → `14`.
- **NO toca `Hito D: 13 de 27`.**
- Tampoco `11 de 15` (condicionales), `15 coeficientes, cero medidos`, ni `4 de 144`.

Son poblaciones de conteo distintas y ninguna se suma a otra.

**Contadores de medición sobre México movidos por este acto: cero.**

---

## 10 · Suite

```
python3 tests/check.py --baseline
  21 FAIL · 126 WARN
  LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json
  (1 entrada de la línea base ya no aparece — mejora, no baja la cifra sin --freeze)
```

Sin `--freeze`, como el encargo exige. Dos cosas que la suite obligó y que no se escondieron:

- **`T22`: `120 → 126` WARN, `FAIL` sin cambio en 21.** Seis WARN, uno por cada fila `ABIERTA` nueva del tablero. Es el comportamiento correcto del vigía `T-FIRMAS`: **abrir** una fila cuesta un WARN, y por eso la cifra sube cuando un acto declara lo que no cerró. Recifrado en `estado-programa` §207 y §299, que es lo que `T16` vigila.
- **`T25` mordió dos veces.** (1) La **nota** traía 12 rótulos pelados (`ADV1-M1`, `ADV1-M3`, `ADV1-M4`) — corregidos, la nota no es verbatim de nadie. (2) El **encargo archivado** los trae y **no se puede editar**: la convención de `forense/encargos/` exige el texto tal como se lanzó. Se censó en `_T25_ARCHIVOS_CONOCIDOS` (`tests/check.py`, commit propio por A.12, extensión de perímetro declarada en `ADR-130`), que es el mecanismo diseñado para esto — la lista ya contiene ~15 encargos por la misma razón. **No** se añadió fila a `canon/registro-rotulos.tsv`: sus filas 12-13 ya censan `ADV1-M1`…`ADV1-M6` y fijan justo esta regla — *el documento fuente queda verbatim sin prefijo, es la cita la que se prefija*.

---

## 11 · CONSUMIDO

Encargo `ACT-PIL-2 · MARCO-M1-A` → **CONSUMIDO**, archivado en `forense/encargos/2026-08-20-ACT-PIL-2.md`.

