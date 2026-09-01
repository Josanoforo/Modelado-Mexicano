# Cierre · `ACTO MAESTRA33-E11 · CRITERIOS-Y-VENCIMIENTOS`, 1/sep/2026

Encargo: `forense/encargos/2026-09-01-MAESTRA33-E11-CRITERIOS-Y-VENCIMIENTOS.md`
(dirección, maestra-33, formato corto v2.12, archivado por A.3 antes de
ejecutar; `SHA de redacción c7fa424`). Ejecutado con la skill `/acto`
(`ADR-237`, D-10) en entorno **NUBE** (`cloud_default`).

## ARRANQUE

1. **Repo.** Clon existente, `/home/user/Modelado-Mexicano`,
   `claude/maestra33-e11-criterios-lzmrvc`. `git log -1` al arrancar:
   `02ec20b Merge pull request #429 from
   Josanoforo/claude/scoring-v1-1-proposal-dybe4i`. `git status`: limpio.
2. **SHA.** `origin/main` al arrancar = `02ec20b`, tres commits después
   de `c7fa424` (`Merge pull request #430`, trámite digesto). Diferencia:
   `c7fa424..02ec20b` toca únicamente `canon/estado-programa-v1_10.md`,
   `canon/gobernanza-v1_15.md`, `canon/registro-rotulos.tsv` (cascada de
   `ACTO MAESTRA33-E10`) — ninguno de los tres colisiona con el
   perímetro de este acto (son, precisamente, los tres archivos de
   cascada que este mismo cierre vuelve a tocar). Rama de trabajo ya
   arrancaba en `02ec20b` = tip literal de `origin/main`: sin refresco
   necesario.
3. **`data/raw`.** Ausente — raíz gitignorada, no enlazada en este
   contenedor. Este acto no abre microdato.
4. **Entorno**, tres partes (A.2): `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE`
   = `cloud_default` (no `sin_variable`, desviación ya vista en otros
   actos de esta sesión, sin consecuencia — el acto es forense/canon,
   no toca microdato). Sonda de red,
   `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10
   https://www.inegi.org.mx/` → `000` (conexión rechazada por política
   del proxy de egress, `connect_rejected`). `ls data/raw/ 2>/dev/null`
   → vacío, corpus compartido no montado (esperado en nube). Ninguna de
   las tres describe el dato — declarado, sin consecuencia porque este
   acto no mide sobre México.
5. **Espejo.** No consultado; toda cifra de este cierre sale del clon
   de (1).

## COMPUERTA

`COMPUERTA: PR #429 (E10) fusionado; si no, cero commits.`

`git fetch origin main` → `origin/main` en `02ec20b`. `git log --oneline
origin/main | grep -c "#429"` → `2` (título del merge commit + su propia
línea de fusión). `git log -1 --format="%h %s" origin/main` →
`02ec20b Merge pull request #429 from
Josanoforo/claude/scoring-v1-1-proposal-dybe4i` — el propio `HEAD` de
`origin/main` **es** el merge commit de `PR #429`. **CUMPLE.** Continúa
al paso 3.

## 0-bis A.3

Primer commit del acto: `354b5ce`, el encargo verbatim en
`forense/encargos/2026-09-01-MAESTRA33-E11-CRITERIOS-Y-VENCIMIENTOS.md`.
Ningún paso sustantivo antes de este commit.

## P0 · Propaga

**FP-190 (firma 3, verbatim «3. De acuerdo, pasan a extrerno/adquisicion
de datos y asigna el área»).** `ACTO MAESTRA33-S1` ya había cerrado fase
2-A y enrutado las 6 filas a `data/cola-adquisicion-v1_0.tsv`
(`fp190-1`..`fp190-6`), pero dejó sin responder a qué **área** iban.
Firma 3 responde: ADQUISICIÓN DE DATOS (externa al motor) — única
lectura con apoyo textual («pasan a extrerno/adquisicion de datos»).
Enmienda fechada añadida a `FP-190` en el tablero; la fila sigue
`ABIERTA` en general (lanzamiento de `REGLAS-OLA5-v0` y su sello,
aparte, sin tocar).

**EMP-05 → R5.3 / TIC-01.** Verificado contra el árbol, no heredado:
`canon/modelo-decision-v4_0.md:537` (`familia.union.baja_garantia_
institucional`, 3ª regla de §3.5, generador `G5`) es la lectura
temáticamente más cercana a EMP-05 (situación conyugal, `ENDIREH`) y no
cita `G#` en su cláusula `PORQUE` — confirmado leyendo la línea, sin
`G#` explícito, tal como el encargo declaraba. `TIC-01` verificado
contra `forense/prereg-duelo-v2/cobertura-15-v1_0.tsv:15`: dominio
propio `SI` (`modelo-decision-v4_0.md:562`, `cooperacion.comite.
monitoreo_sancion_visible`) pero **sin cita `G#` en el `PORQUE`** →
veredicto `EXISTE-NO-SATISFACE`, `SIN-CITA-G#-EXPLICITA` — cita sin uso,
sin generador, confirmado. Ambas notas añadidas como campo
`uso_en_motor` a las entradas ya existentes de `TIC-01`/`EMP-05` en
`milpa/procedencia.yaml::candidatas_theta_citadas_fp190` (sin tocar sus
campos medidos).

**`corresidencia_actual` (firma 4, verbatim «4. Dato informativo.»).**
Nueva sección `milpa/procedencia.yaml::thetas_informativas` — clase
distinta de `coeficientes_generador_medidos` (exige `gen: G#`) y de
`candidatas_theta_citadas_fp190` (cita sin medir): esta theta **sí** está
medida (`p=0.057531`, `IC95% [0.051297,0.063913]`, `n=9397`, `EDER 2017`,
universo `parentesco propio in {Jefe, Cónyuge}`, escala `[0,1]`) y mesa
la clasifica informativa, no candidata a regla. `milpa/tramite-ola5-
propuesta-v0.yaml`: entrada `familia.corresidencia.adulto_familiar_
actual` (`ACTO MAESTRA33-C1`) pasa `situacion: PENDIENTE-DE-MESA` →
`APARCADA`, cuerpo intacto (`p`/`ic95`/`n`/`ponderador`/`universo`/
`fuente` sin tocar, mismo principio que las demás enmiendas de ese
archivo).

**FP-179 (firma 6, verbatim «6. Tachemos los dos … deja claro y
estipulado cuales quedan pendientes»).** (1) y (2) re-confirmadas
`EJECUTADAS`, sin cambio de fondo. **C7** — (5) verificada contra
`ADR-134` (`canon/gobernanza-v1_15.md`): **CONFIRMA**. `ADR-134`
(`ACTO APERTURA-ENFIH-ENSAFI`, 20/ago/2026) derivó las celdas objetivo
de `coef-universo-v1_0.tsv` y buscó en `ENSAFI 2023`/`ENFIH 2019` con
protocolo pre-registrado (0 de 8 `EXISTE-SATISFACE`) — ejecuta la
palanca que (5) pedía, nueve días antes de que `FP-179` la registrara
como `CONSUMIDA-PREEXISTENTE`: consistente con esa nota, no reconciliado
en silencio. **C8** — `FP-217`, deriva de (3) (mediciones diferidas de
`FP-172`, encargo aún sin redactar), `vence: 2026-09-07`. **C9** —
`FP-218`, deriva de (4) (re-estimación compuesta) — **tensión declarada,
no resuelta**: la propia fila `FP-179` ya anota (4) `CONSUMIDA` (β̂
compuesto, `ACTO MAESTRA32-E8`, 30/ago/2026); `FP-218` abre la fila que
firma 6 pidió (`vence: 2026-09-08`) declarando esa tensión para que mesa
diga si cierra sin trabajo o si falta un paso que este acto no localizó
en el árbol. Ninguna de las dos filas se resuelve por este acto — mesa
decide, `LO QUE NO HACE` no autoriza cerrar en su lugar.

**FP-212/214/215 (firma 7, verbatim «7. Se cierra.»).** `ABIERTA` →
`FIRMADA` las tres. Ninguna gateaba nada vivo (columna `gatea` de las
tres: recibos informativos) — cerrar es acusar recibo, no autorizar un
paso nuevo; ninguna trae `ejecutada_en` porque ninguna tenía un paso
pendiente que ejecutar.

## P1 · Enmienda fechada, `canon/motor-nucleo-medible-v1_0.md` §3

`A.8` confirmado contra el árbol: `NO-ENCONTRADO` antes de este acto
(criterios de apertura de dominio y de activación del corredor E
ausentes del documento, verificado leyendo sus 124 líneas previas).
Nueva §3, dos sub-criterios, **no** sustituye ni relaja F-ALCANCE (§1):

- **3.a Ola 6** (firma 9, verbatim «9. Si pero dejando claro cuando se
  abren o bajo qué criterios se abren»): scoreboard agregado con `L`
  sobre los 4 activos **y** ≥2 encuestas en corpus con ≥3 reglas
  candidatas `EXISTE-SATISFACE` por `/mapea` **y** caja libre. Primera
  evaluación: al primer agregado con `L`, o `15/sep/2026`, lo primero —
  recibo `FP-220`.
- **3.b Corredor E** (firma 10, verbatim «10. Banca, pero deja claro los
  criterios de avance»): `L` y `M` con puntos en ≥8 celdas comunes **y**
  scoring v1_1 sellado. Revisión: al publicarse el agregado, o
  `30/sep/2026`, lo primero — recibo `FP-221`.

Ninguno de los dos criterios se evalúa como cumplido por este acto —
hoy no existe agregado con `L` (`L-CORRIDA-v1_1`/`FP-219` sigue
pendiente) ni scoring v1_1 sellado (`mesa-pendientes.md` §5 sigue sin
firma). `LO QUE NO HACE`: este acto no abre ningún dominio, no activa el
corredor `E`, no toca la puerta general de F-ALCANCE §1.

## P2 · Digesto v1.2

`tools/digesto_tramite.py`: nueva función `bloque_vencimientos()`, que
lee el mismo tablero que la sección A (`lee_tablero`), parsea
`vence:\s*(\d{4}-\d{2}-\d{2})` en la columna `gatea` de filas `ABIERTA`,
y **abre** el digesto (antes de la sección A) con `VENCIDAS` (días de
retraso) y `vencen esta semana` (ventana de 7 días desde `--fecha`,
hoy incluido). Texto neutralizado con la misma `neutraliza()`/`Cuenta`
que el resto del digesto. Verificado con dos corridas manuales
(`--fecha 2026-09-01 --stdout --sin-suite` y `--fecha 2026-09-10`, ver
diff de salida en el propio commit): con `2026-09-01`, `FP-219`/`FP-217`
caen en "vencen esta semana"; con `2026-09-10`, `FP-219`/`FP-217`/
`FP-218` caen en `VENCIDAS` con 6/3/2 días de retraso respectivamente.
Determinismo no roto: misma `--fecha` + mismo árbol → misma salida
(no se corrió doble-`diff`, pero la función no lee reloj ni aleatorio
fuera de `hoy`, mismo patrón que el resto del módulo).

`tests/check.py::t22_firmas`: nueva `_t22_retraso_txt()`, mismo regex,
mismo campo `gatea`; el `WARN` de T22(a)/(c) ahora trae ` · VENCIDA hace
N días` / ` · vence en N días` cuando aplica. Verificado directamente
(`t22_firmas()` corrida aislada, ver salida citada abajo) — `FP-219`
mostró `vence en 3 días` a la fecha real del sistema (`2026-09-01`).
`senal()` (no `fail()`/`warn()`) sostiene ambos WARN — **fuera de la
comparación de línea base** por diseño (`tests/check.py:40-46`), así
que ninguna de las dos filas nuevas ni el texto añadido pueden producir
un `FAIL` nuevo por este cambio.

`forense/agente-tramite-v1_0.md` §2: una línea nueva que manda leer el
bloque **Vencimientos** antes que la sección A — perímetro explícito del
encargo ("runbook de trámite §2").

**Fuera de `tools/digesto_tramite.py` (nombrado por el encargo) y
`tests/check.py` (no nombrado por archivo, pero "el WARN de T22" de P2
vive únicamente ahí) — declarado, no una desviación de perímetro
silenciosa.**

## P3 · Filas con vencimiento

Seis filas nuevas en el tablero (`FP-217`..`FP-222`, ver P0 para
`FP-217`/`FP-218`): `FP-219` `L-CORRIDA-v1_1` (mesa, `vence:
2026-09-04`), `FP-220` `EVALUACION-OLA6` (dirección, `vence:
2026-09-15`), `FP-221` `REVISION-CORREDOR-E` (dirección, `vence:
2026-09-30`), `FP-222` `REVISION-FALSADORES` (dirección, `vence:
2026-09-30`). `SELLO-SCORING-v1_1` **no** abre fila nueva —
`ACTO MAESTRA33-E10` ya abrió `forense/prereg-duelo-v2/mesa-
pendientes.md` §5; este acto le añade una línea `**Vence:**
2026-09-03` ahí mismo, tal como el encargo pidió ("no dupliques").

## Cascada

1. **ADR.** `grep -oE '^\*\*ADR-[0-9]+' canon/gobernanza-v1_15.md |
   grep -oE '[0-9]+' | sort -n | tail -1` → `257`, sin huecos →
   candidato **`ADR-258`**, contiguo. Ningún otro acto en vuelo conocido
   al escribir esto.
2. **Cabecera.** Entrada nueva en `canon/gobernanza-v1_15.md` §4.
3. **Recifrado L0.** `canon/estado-programa-v1_10.md`: `257` → `258
   ADR` en la línea `L0` (anotación nueva insertada antes de la de
   `ADR-257`) **y** en la tabla de artefactos (línea 27, `| gobernanza |
   ... | 257 ADR |` → `258 ADR`) — dos citas, no una; `T15` (censo de
   consistencia por comando) atrapó la segunda cuando la primera edición
   de este cierre solo tocó `L0`, declarado.
4. **`registro-rotulos`.** `canon/registro-rotulos.tsv`: rótulo
   `MAESTRA33-E11` censado (espacio E).
5. **T25.** Dos archivos nuevos traen `E10` pelado — habitante ya
   censado del espacio E (`ACTO MAESTRA33-E10`), ninguna mención es un
   marcador nuevo: el encargo (cita "PR #429 (E10)" en su cabecera de
   `COMPUERTA`) y esta misma nota de cierre (cita verbatim del encargo
   más la discusión del propio hallazgo T25). Ambos añadidos a
   `_T25_ARCHIVOS_CONOCIDOS` (`tests/check.py`) con el comentario que
   explica de dónde sale cada mención; el encargo **no** se edita (A.3,
   verbatim) — esta nota si pudo reescribirse para reducir menciones,
   pero la cita verbatim de `COMPUERTA` se conserva tal cual por la
   misma razón que el encargo.
6. **`python3 tests/check.py --baseline`: VERDE**, `19 FAIL · 168 WARN`,
   sin entrada nueva frente a `tests/baseline.json`
   (`HEAD` congelado `c6a0d72f`). Dos hallazgos nuevos del propio
   cierre, ambos corregidos en el camino, declarados: el `FAIL` de `T15`
   (segunda cita de conteo de ADR, tabla de artefactos, sin recifrar) y
   el de `T25` (dos archivos con `E10` pelado sin censar).
7. **Anti-PR#77.** No aplica — este acto no descargó nada
   (`CONTADOR: cero`).
8. **`## CONSUMIDO`** — añadido al encargo archivado, con el PR de este
   acto.
9. **Push + PR.** `git push -u origin claude/maestra33-e11-criterios-
   lzmrvc`; **un** PR contra `main`, sin fusionar por este acto.

## CONTADOR

**Cero, declarado.** Ningún corredor (`M`/`R`/`L`) corrido, ningún
script de scoring o de emisión ejecutado, ningún microdato abierto.
Este acto es canon/tablero/herramienta — insumo y bookkeeping, no
medición sobre México.

## Lo que este acto NO hace (verificado contra el propio encargo)

No abre ningún dominio de Ola 6 (`milpa/tramite.yaml` sin diff,
verificado — `git diff --stat -- milpa/tramite.yaml` vacío). No activa
el corredor `E` (`forense/prereg-duelo-v2/corredor-E-combinacion-LM.py`
sin diff). No corre `L` (`forense/prereg-duelo-v2/corridas-L/` sin
archivo nuevo). No cambia la puerta de activación sellada de F-ALCANCE
§1 (texto de §1 intacto, verificado — la enmienda es §3, nueva, no una
edición de §1). No inventa firmas — las siete propagadas (3, 4, 5, 6,
7, 9, 10) son verbatim del encargo; firmas 1/2/8 de la ronda de mesa del
1/sep, si existen, no se citan ni se infieren aquí.
