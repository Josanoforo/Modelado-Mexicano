# M-1 · Mapa e inventario de 24 payloads ENSANUT 2024 (commit único — reconocimiento, no estimación, no adjudicación)

Encargo M-1 recibido el 5/ago/2026. Perímetro declarado: `data/manifiesto.yaml` (campos
`usado_para` y `nota`), este archivo, `forense/hallazgos.md`. Sin tocar `canon/` ni
`forense/hitoD-preregistro-v2_0.md`, sin adjudicar ninguna ficha.

## ARRANQUE

1 · **REPO.** Clon existente en `/home/pc0/Modelado-Mexicano`, pero sentado en una rama
ajena (`sesion/cal-conf-faseb-pos4-envipe-paso1`, mergeada, `?? data/raw`) — no se arrancó
ahí. Worktree nuevo: `/home/pc0/mm-m1-ensanut`, rama `sesion/m1-ensanut-mapa`, creado desde
`origin/main`.

2 · **SHA.** `git rev-parse HEAD` del worktree nuevo = `16d9dbd...` = `git rev-parse
origin/main` en el momento de arrancar (Merge PR #130). Sin diferencia que refrescar.

3 · **data/raw.** Ausente en el worktree fresco → enlazada a `/home/pc0/mm-corpus/raw`
(patrón ya usado por el resto de worktrees activos). Pero: **los 24 payloads de este acto
NO viven ahí.** Ver hallazgo de entorno abajo.

4 · **ENTORNO (firma de tres partes, v2.5 A.2).**
`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` = `sin_variable` (esperado para Ubuntu pc0).
`curl -s -o /dev/null -w "%{http_code}" --max-time 10 https://www.inegi.org.mx/` = `200`.
`ls data/raw/ | head -1` → corpus `data_raw` montado (157 archivos, ninguno ENSANUT —
esperado, ver abajo). `python3 -c "import pandas"` → `pandas 2.3.3` disponible.

5 · **ESPEJO.** No se derivó ninguna cifra de espejo del proyecto; todo lo reportado abajo
sale del clon de (1) o de archivos abiertos directamente en `/mnt/c/Users/PC0/Descargas MX`.

## Hallazgo de entorno: la raíz `descargas_mx` no es `data/raw`, y no está configurada por defecto

Los 24 payloads del encargo tienen `raiz: descargas_mx` en el manifiesto (no `data_raw`).
Esa raíz es "carpeta de descargas curada por el autor" (`tests/manifiesto.py:65`), resuelta
por `data/raices.local.yaml` — gitignorado, per-máquina, **ausente en un worktree fresco**.
En esta máquina resuelve a `/mnt/c/Users/PC0/Descargas MX` (montaje WSL del lado Windows).
El archivo no existía en `mm-m1-ensanut` al arrancar; se encontró la configuración ya
replicada en otros 11 worktrees de esta misma máquina (`grep` de
`data/raices.local.yaml` bajo `/home/pc0`) y se copió aquí, sin inventar ninguna ruta.
Con la raíz configurada, verificación exhaustiva por `tests/manifiesto.py --verifica --id
<id>` — **una invocación por id, regla A.1 v2.5** — de los 24 ids: **24/24 COINCIDE**
(sha256 y tamaño contra `data/manifiesto.yaml`). El corpus está montado y es íntegro; la
premisa del encargo ("está en disco y nadie lo ha abierto") se sostiene, solo que "en disco"
significaba una raíz de terceros no auto-descubrible, no `data/raw`.

## Los 24 payloads: notas escritas en `data/manifiesto.yaml` (campo `nota`)

Las 24 entradas (`1_vfinal_cuestionario_hogar_ensanut_2024_etiquetas_cuestionarios` …
`utilizadores_ensanut2024_w_stata_stata`) ya traen su nota de 2-4 líneas en el manifiesto —
qué es, unidad de observación, módulos, para qué sirve. No se duplica el texto aquí; el
manifiesto es la fuente. Se generaron leyendo cada archivo directamente en esta sesión, en 5
grupos de trabajo sin solape de archivos:

- Grupo A: Cuestionario Hogar (PDF) + NSE_Hogar + hogar_w_ICB (catálogo+csv) — 5 payloads.
- Grupo B: Cuestionario Utilizadores (PDF) + utilizadores_w (catálogo+csv+stata) — 4 payloads.
- Grupo C: Cuestionario Adultos (PDF) + adultos_w (catálogo+csv_csv) + integrantes_w_ICB (catálogo+csv) — 5 payloads.
- Grupo D: Cuestionario Niños 0-9 + Adolescentes (PDF) + menores_w (catálogo+csv+stata) + adolescentes_w (csv+stata) — 7 payloads.
- Grupo E: NSE_Integrantes (catálogo+csv) + Índice de Bienestar (docx) — 3 payloads.

Herramientas: `pdftotext -layout` para los 5 cuestionarios PDF, `pandas`/`openpyxl` para
`.xlsx`/`.csv.zip`, `zipfile`+regex sobre el XML interno para el `.docx` (no hay
`python-docx` instalado en este entorno).

**Hallazgo transversal, ya anotado en `indice_de_bienestar_cuestionarios`:** "ICB" (Índice
de Bienestar) y "NSE" no son dos constructos — es el mismo índice (PCA sobre 8 variables de
vivienda/bienes, primer componente principal = `indice1`, dicotomizado en `nseF`/`nse5F`),
documentado en `Indice de Bienestar.Cuestionarios.docx` y replicado en los archivos NSE_* e
`*_w_ICB`.

### Defectos de corpus encontrados (regla de señal v2.3: una línea cada uno, no se investigan más)

- `adultos_ensanut2024_w_catlogo_csv_csv`: pese al nombre/extensión `.csv.csv.zip`, el
  archivo interno es `adultos_ensanut2024_w.Catálogo.xlsx`, **byte-idéntico** (mismo
  sha256) al catálogo `adultos_ensanut2024_w_catlogo`. No existe microdato csv de personas
  adultas entre los 24 payloads de este acto — solo el diccionario, duplicado y mal
  nombrado.
- `adolescentes_ensanut2024_w_csv_csv`/`_stata_stata`: no traen catálogo de etiquetas
  propio entre los 24 payloads (a diferencia de menores/adultos/utilizadores/hogar). La
  cabecera del csv solo trae códigos (`d0101`, …) — hay que cruzar contra el PDF del
  cuestionario de adolescentes para interpretar columnas y categorías.

## Las cuatro preguntas

**Meta-hallazgo primero, porque cambia cómo leer las tres secciones siguientes: `R4.1` y
`R9.1` (ambas filas) ya tienen veredicto `D` sellado desde el 4/ago/2026** (Encargo Z, Nota
23, `forense/hitoD-preregistro-v2_0.md:1062-1063`, detalle en
`forense/notas/2026-08-04-z4-veredicto-r4-1-r9-1.md`), **y `R9.2` también** (mismo día,
`forense/notas/2026-08-04-z6-veredicto-r9-2.md`). Este acto NO reabre ni contradice esos
veredictos — no toca `hitoD-preregistro-v2_0.md`, por perímetro. Lo que sigue es
reconocimiento a nivel de variable, un peldaño *debajo* de la adjudicación, y en los tres
casos es **consistente** con el motivo que Encargo Z ya documentó, con detalle adicional
que la ficha Z no necesitó abrir (Z decidió por "chequeo barato" sin abrir microdato fila-
por-persona).

### R9.1, fila 2 — "no consultó a nadie" (excluida de Utilizadores)

**Existe en el instrumento.** `H0404` (pregunta 4.4 de la Sección IV del Cuestionario
Hogar, "PARA QUIENES TUVIERON NECESIDADES DE SALUD"): *"¿(USTED/NOMBRE) buscó atención por
esa necesidad de salud?"* — 1 Sí (pasa a 4.6) / 2 No. `H0404=No` es exactamente la
población "no consultó a nadie". El propio cuestionario confirma el mecanismo de exclusión
que la ficha Z ya documentó: nota de programador junto a 4.6 —
*"SOLO LOS QUE CONTESTARON QUE SI RECIBIERON ATENCIÓN (RESPUESTAS A PREGUNTA 4.6)
CONTESTARÁN EL CUESTIONARIO DE UTILIZADORES (UNA MUESTRA DE ELLOS)"*. Variable distinta y
posterior en la misma cadena: `H0406` (4.6, "¿fue atendido(a)…?") captura a quien SÍ buscó
pero NO fue atendido — no es el mismo caso.

**Pero no está en ningún microdato de los 24 payloads.** `H0404` es un ítem por integrante
de Sección IV; ninguno de los dos archivos de hogar (`hogar_ensanut2024_w_icb_csv_csv`,
`nse_hogar_ensanut_2024_csv_csv`) lo trae como columna — ambos son de nivel hogar/informante
y de Sección IV solo incluyen `h0400`/`h0400a`/`h0400b` (conocimiento de IMSS-BIENESTAR).
Tampoco está en `integrantes_ensanut2024_w_icb_csv_csv` (roster + programas de bienestar +
índice de condición de bienestar, sin variables de utilización de salud). **Existe en el
instrumento, no es alcanzable en la microdato de ninguno de los 24 payloads registrados en
este acto** — sería necesario un archivo de personas/Sección IV completa que no está entre
los 24, si es que existe como descarga separada de ENSANUT (no verificado, fuera de
perímetro).

### R9.1, fila 1 — acceso documentado (<2km, sin costo, espera <1 día)

Ninguno de los tres componentes existe como umbral cuantitativo — consistente con lo que
la ficha Z ya decidió (*"no existe variable de distancia en km, solo tiempo de traslado"*):

- **Distancia:** no existe medición en km en ningún cuestionario abierto (Hogar, Adultos,
  Utilizadores). Lo único relacionado: opción 03 de motivo de no búsqueda (`H0405`, Hogar):
  *"Está muy lejos el lugar más cercano donde se brinda atención"* — categórico, no umbral.
  El tiempo de traslado (`U02xx`, mencionado en la ficha Z como `U0204`) vive en el
  Cuestionario de Utilizadores, Sección II ("tiempos de traslado/espera/consulta") — no en
  Hogar, y ese cuestionario excluye por diseño a quien no consultó a nadie (misma exclusión
  de la fila 2, arriba).
- **Costo:** no existe pregunta transaccional directa sobre el evento de atención. Lo
  encontrado son motivos categóricos (`H0405` opción 04 "Es caro/No tenía dinero", `H0407`
  opciones 08/09 sobre no saber que había que pagar / no poder cubrir el costo) y una
  opinión general no ligada al evento (`H0308B`, Sección III: *"los servicios públicos de
  salud son gratuitos en México"*, Likert 1-5).
- **Espera:** no existe umbral en días/horas. Solo categorías cualitativas dentro de listas
  de motivos: `H0405` opción 10 y `H0407` opción 11, ambas *"tiempo de espera… muy largo"*,
  condicionadas a no haber buscado/no haber sido atendido — no aplicable a quien sí fue
  atendido.

Ninguna de `H0405x`/`H0407x` está en los dos csv de hogar de este acto; `H0308B` sí está
(`hogar_ensanut2024_w_icb_csv_csv`, columna `h308b`).

### R4.1 — prestador de primera atención por afiliación

**Existe, con 24 categorías.** Variable `u0201` (Utilizadores, pregunta 2.1, Sección II):
*"¿En qué institución de salud (USTED/NOMBRE) se/te atendió/atendiste o recibió/recibiste
atención?"*. Categoría 12, **"Consultorios pertenecientes a farmacias/Farmacias con
consultorio médico"**, es exactamente el concepto de "farmacia con consultorio" que pide el
encargo — categoría única, no colapsada con "farmacia" a secas (que no existe como opción
separada) ni con consultorio privado en domicilio (16) o en torre/clínica (15). En el
microdato, `u0201=12` tiene 351 de 3,223 observaciones. La variable de afiliación
(`uh0310_m`, importada de la pregunta 3.10 de Hogar) vive en el mismo archivo de
Utilizadores — el cruce prestador × afiliación es técnicamente posible sin fusionar con
Hogar, aunque las categorías de `uh0310_m` no están decodificadas en el catálogo de
Utilizadores (solo inferibles de la matriz de correspondencia impresa en el PDF).

**Esto no cambia el veredicto `D` ya sellado.** La ficha Z documentó explícitamente que la
existencia/calidad de la variable de prestador es *"irrelevante para el veredicto"* — `R4.1`
cae por ausencia de diseño panel antes/después anclado a un evento fechado de mejora de
acceso, no por falta de la variable de prestador. Este hallazgo confirma con más detalle
justo la pieza que la ficha Z ya dijo que no importaba.

### R9.2 — cobertura de servicios preventivos con disponibilidad verificada

Sección X del Cuestionario de Adultos ("PROGRAMAS PREVENTIVOS", 10 pruebas de detección:
Papanicolaou, VPH, exploración de mama, mastografía, sobrepeso/obesidad, perímetro de
cintura, glucosa, presión arterial, colesterol/triglicéridos, antígeno prostático). Pregunta
ancla 10.1, idéntica para las 10: *"Durante los últimos 12 meses, un médico u otro
profesional de la salud le realizó… [prueba]"* — **uso/recepción autorreportada**, no
verificación de disponibilidad. La sub-pregunta 10.1b (motivo de no realización) trae
códigos que tocan percepción de no-disponibilidad ("no tenían el equipo", "no le
ofrecieron"), y en vacunación (Sección IX) existe *"¿le dijeron que no había vacunas?"" —
pero en los tres casos es lo que la persona recuerda que le dijeron, no un registro
administrativo o inventario de clínica verificado por tercero.

**Consistente con el veredicto `D` ya sellado** (`forense/notas/2026-08-04-z6-veredicto-r9-2.md`):
la única fuente candidata para abasto/alcance de campaña verificado por tercero era DGIS —
el propio prestador, excluido por definición del Umbral. Este hallazgo confirma, a nivel de
variable, que ENSANUT tampoco resuelve esa pieza: todas sus preguntas de servicios
preventivos, incluidas las que tocan disponibilidad percibida, son autorreporte del
entrevistado.

## Cierre

Contador de falsación: **0 movido** — este acto es reconocimiento/inventario, no
adjudicación; exento del módulo de auditoría de rigor extremo por función (Bloque A,
instrucciones-proyecto-v2_5.md:119, "no va en… manifiestos"). Las 24 notas del manifiesto
quedan escritas para que la siguiente sesión no tenga que reabrir ningún archivo. Si otra
sesión quiere reabrir `R4.1`/`R9.1`/`R9.2`, tendría que declarar explícitamente por qué
reabre veredictos ya sellados el 4/ago/2026 — no es este acto quien lo decide.
