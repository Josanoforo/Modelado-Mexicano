# CAL-CONF Fase B — posición 4, ENVIPE paso 1: ¿trae `TPer_Vic1` reactivo de `exposicion_violencia`?

Contadores movidos: 0

Sin módulo de auditoría — no afirma nada sobre México (v2.3)

*4 de agosto de 2026.*

**Resultado de este acto, dicho antes que nada: LA FUENTE NO TIENE EL DATO —
descriptor recorrido completo (Sección IV y Sección V de `TPer_Vic1`,
ENVIPE 2025), ninguna candidata sirve contra la frase-criterio.** Este acto
no mide nada y no mueve el contador (sigue en **8/14**); no desbloquea paso
2 sobre esta fuente — cierra la pregunta sobre `TPer_Vic1` específicamente,
con argumento por cada descarte. Es uno de los dos actos nombrados de la
condición de caducidad de ADR-52 A para `exposicion_violencia` — a
diferencia de los dos intentos previos del mismo acto (`PR #61` y su
reemisión), **este sí abrió el descriptor**: es un acto "examinado y
descartado con argumento", no un bloqueo de entorno.

---

## 0 · Verificación de entorno (protocolo §0, antes del diseño)

```
$ python3 tests/bitacora.py --abre
HEAD:  268d9dfc6b158849d2e49fe0824a8d2e93017850  ==  origin/main  (sin divergencia)
check.py --baseline:        exit=0 · LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json
validador_registro_ids.py:  exit=0 · OK — 49 reglas, 27 en perímetro, 49 IDs verificados
Versión de instrucciones vigente: v2.3 (instrucciones-proyecto-v2.md, línea 1)

$ echo "${CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE:-sin_variable}"
sin_variable

$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/
200

$ ls data/raw | wc -l
133   (incluye fd_envipe2025.pdf, cuest_principal_envipe2025.pdf, cuest_modulo_envipe2025.pdf)
```

Sin `cloud_default` en la variable de entorno; INEGI **responde** — a
diferencia de los dos intentos previos del mismo acto (`PR #61` y su
reemisión), ambos `000`/`403` de política de proxy al `CONNECT`, registrados
en `forense/hallazgos.md` (entradas 04/ago/2026, líneas 74 y 79). El
checkout de trabajo de esta sesión (`/home/pc0/Modelado-Mexicano`, con
`data/raices.local.yaml` y `data/raw` simbólico a `/home/pc0/mm-corpus/raw`)
tiene `data/raw` poblado — distinto de un clon efímero donde `data/raw`
está ausente por diseño (`.gitignore`: `data/raw/`, `data/raices.local.yaml`),
trampa que §0 del encargo anticipa ("todo reportará AUSENTE aunque el
manifiesto lo registre"). **Entorno correcto para este acto, confirmado
antes de leer nada.**

Rama nueva desde `origin/main` actualizado tras `git fetch`:
`sesion/cal-conf-faseb-pos4-envipe-paso1` (268d9df). No se reusó el
checkout de esta misma carpeta como estaba (rama
`sesion/sens-estatus-examen-descriptor`, ya fusionada en `main` — confirmado
con `git merge-base HEAD origin/main` antes de escribir nada nuevo sobre
ella).

## 1 · Premisas (§1 del encargo), verificadas contra HEAD

| # | Verificación | Resultado |
|---|---|---|
| PD-1 | `grep -n exposicion_violencia canon/modelo-decision-v4_0.md` | Confirmado (`:269`): *"Sin reactivo verificado — búsqueda abierta"*, único de esa clase tras ADR-54 (`sens_estatus` cerró por precedente). Reparto **8+1+2+3**, control de suma en `:278`, `:725` |
| PD-2 | `forense/hallazgos.md` (entrada 04/ago/2026, línea 72) + `hitoE §15` | Confirmado: `BP1_20`/`BP1_23`/`BP1_28` retirados por `PR #57` — miden conducta de denuncia condicionada a victimización (`TMod_Vic`, `RESUL_H='A'` en el 100%), no exposición |
| PD-3 | `hitoE §14.3` (fila 4, corregida por §15, `:1247`) | Confirmado: **PENDIENTE DE VERIFICACIÓN**, textual |
| PD-4 | `canon/gobernanza-v1_15.md:527` (ADR-52 A) + `forense/hallazgos.md` (línea 79) | Confirmado: *"posición 4 rehecha sobre `TPer_Vic1`"* nombra `PR #61` + su reemisión como **un** acto, no dos, hacia la caducidad de tres |
| PD-5 | `grep -n exposicion_violencia canon/modelo-decision-v4_0.md milpa/procedencia.yaml` | Confirmado: `modelo:394` y `procedencia:476` — `G4` usa `exposicion_violencia 0.70`. ⚠️ La cita del encargo `procedencia.yaml:441` **es falsa contra HEAD** — línea 441 es la nota de `tramite.gobierno_digital.coercitivo`; la escala 0.35–0.70 vive en **`:498`** (`riesgos_cruzados`). (Esta discrepancia ya está registrada en `forense/hallazgos.md`, línea 74, de un intento anterior — no es hallazgo nuevo de este acto, se re-verifica independientemente y coincide) |
| PD-6 | `forense/hallazgos.md` (entrada 04/ago/2026, línea 77) | Confirmado: ENDIREH paso 1 (`PR #67`) encontró candidato parcial (universo mujeres 15+, 11 variables en `TB_VD`), sin adjudicar; C3 pasa, C2 abierto |

Las seis premisas (1) se sostienen. Se procede.

## 2 · El criterio, escrito antes de abrir nada

**Frase-criterio:** *exposición a violencia sufrida por la persona
(antecedente), en cualquier periodo de referencia, condicionada al vector
de atributos observables de `canon` §1.1.A — distinta de percepción o
actitud sobre inseguridad, y distinta de conducta posterior a la
victimización (denuncia, búsqueda de ayuda, medidas defensivas).*

Tres distinciones (§2 del encargo), declaradas antes de mirar el
descriptor:

1. **Exposición a violencia** (lo que se busca) → **SIRVE si aparece**.
2. **Denuncia o conducta posterior a la victimización** (lo que ya se
   retiró en `BP1_20/23/28`) → **NO SIRVE si aparece**.
3. **Percepción/actitud de inseguridad** (constructo distinto; en parte ya
   cubierto por `confianza_institucional[justicia]`, que entra a `G4` con
   su propio coeficiente) → **NO SIRVE si aparece**.

## 3 · Insumos y verificación de payload

```
$ python3 tests/manifiesto.py --verifica --id envipe2025_fd_pdf
envipe2025_fd_pdf [data_raw]: COINCIDE -- sha256 y tamaño (2284580 bytes) verificados

$ python3 tests/manifiesto.py --verifica --id envipe2025_cuest_principal_pdf
envipe2025_cuest_principal_pdf [data_raw]: COINCIDE -- sha256 y tamaño (1264383 bytes) verificados

$ python3 tests/manifiesto.py --verifica --id envipe2025_cuest_modulo_pdf
envipe2025_cuest_modulo_pdf [data_raw]: COINCIDE -- sha256 y tamaño (930409 bytes) verificados
```

Los tres ya estaban **registrados** en `data/manifiesto.yaml`
(`:1750`, `:1763`, `:1776`) con `url_origen` bajo el patrón `/doc/` ya
probado por otras fuentes; no hizo falta descarga — estaban también **en
disco**, y `--verifica` confirma que ambos hechos coinciden (distinción
que §0 del encargo exige no confundir). No se abrió `cuest_modulo_envipe2025.pdf`
— fuera del alcance de este acto (insumos declarados: FD + cuestionario
principal).

`pdftotext -layout` sobre ambos PDF (herramienta del sistema, no
adivinada). `fd_envipe2025.pdf` → 7 207 líneas; `cuest_principal_envipe2025.pdf`
→ 987 líneas.

## 4 · Localización de la tabla dentro del FD

```
$ grep -n "Tabla T" fd.txt
314   Tabla TVivienda
549   Tabla THogar
659   Tabla TSDem
858   Tabla TPer_Vic1      <- Contenido: 240 variables · Llave UPM+VIV_SEL+HOGAR+R_SEL
2885  Tabla TPer_Vic2      <- 149 variables (victimización en hogar y personal)
4417  Tabla TMod_Vic       <- 137 variables (delitos del módulo; aquí viven BP1_20/23/28, líneas 5049-5152)
```

`TPer_Vic1` (`fd.txt:858-2885`) declara su propio contenido: *"Variables
correspondientes a la percepción de seguridad pública y el desempeño
institucional"* — dos secciones del cuestionario: **Sección IV. Percepción
sobre seguridad pública** (`AP4_1`…`AP4_12`, vars 16-111) y **Sección V.
Desempeño institucional** (`AP5_...`, vars 112-240). Confirmado que
`BP1_20`/`BP1_23`/`BP1_28` (el reactivo retirado) **no viven en `TPer_Vic1`**
— están en `TMod_Vic` (`fd.txt:5049-5152`): el encargo redirige la búsqueda
a una tabla distinta de la del intento anterior, no repite el mismo
terreno.

Leído completo: Sección IV (`fd.txt:108-694`) y Sección V (`fd.txt:695-2027`,
grep dirigido sobre el texto completo — ver §6). Cruzado contra el
cuestionario principal (`cuest.txt`), que reproduce la Sección IV
literalmente (`cuest.txt:274-475`) y confirma con su propia tarjeta de
control **CC2**: *"le preguntaré sobre la percepción de su seguridad
personal y la de su entorno"* (`cuest.txt:415-416`) — el instrumento mismo
etiqueta este bloque como percepción, no como exposición.

## 5 · Candidatos, por descriptor literal — ninguno sirve

**Universo, todas las filas:** persona seleccionada del hogar (`R_SEL`),
sin restricción adicional de edad más allá de 18+ (llave `UPM+VIV_SEL+HOGAR+R_SEL`,
`fd.txt:264-266`).

| Variable(s) | Tabla · sección | Wording literal (FD / cuestionario) | Universo | Catálogo | Distinción |
|---|---|---|---|---|---|
| `AP4_5_01`…`AP4_5_18`/`_99` (18 sub-ítems, incl. `AP4_5_06` "violencia policiaca", `AP4_5_11` "disparos frecuentes", `AP4_5_13` "secuestros", `AP4_5_14` "homicidios", `AP4_5_15` "extorsiones") | `TPer_Vic1` §IV, preg. 4.5 | *"¿Sabe usted o ha escuchado si en los alrededores de su vivienda suceden o se dan las siguientes situaciones?"* (`fd.txt:295`, `cuest.txt:335`) | Persona seleccionada | 0=no declarada / 1=Sí (multi-respuesta) | **(3) Percepción/actitud** — conocimiento o rumor sobre el entorno, no exposición personal. El propio verbo ("sabe o ha escuchado") excluye vivencia directa. **NO SIRVE** |
| `AP4_6_1` (robo/asalto), `AP4_6_2` ("lesiones por una agresión física"), `AP4_6_3` (extorsión/secuestro) | `TPer_Vic1` §IV, preg. 4.6 | *"En lo que resta de 2025... ¿cree que a usted le pueda ocurrir...?"* (`fd.txt:380-403`) | Persona seleccionada | 1 Sí / 2 No / 3 No aplica / 9 NS-NR | **(3) Percepción/actitud** — expectativa subjetiva de riesgo futuro ("cree que... le pueda ocurrir"), no un hecho ocurrido. **NO SIRVE** |
| `AP4_7_1`/`_2`/`_3` | `TPer_Vic1` §IV, preg. 4.7 | *"¿Considera que... la seguridad pública... mejorará/seguirá igual/empeorará?"* | Persona seleccionada | 1-4 escala, 9 NS-NR | **(3) Percepción/actitud** — expectativa de tendencia, ni siquiera sobre violencia sufrida. **NO SIRVE** |
| `AP4_8_1`…`_6` / `AP4_9_1`…`_6` (incl. `AP4_8_4`/`AP4_9_4` "pandillerismo violento", `AP4_8_5`/`AP4_9_5` "robos", `AP4_8_6`/`AP4_9_6` "delincuencia en alrededores de escuelas") | `TPer_Vic1` §IV, preg. 4.8/4.9 | *"¿En su (COLONIA/LOCALIDAD) han tenido problemas de...?"* / *"¿Se han organizado los vecinos para resolverlos?"* | Persona seleccionada | 1 Sí / 2 No / 3 No aplica / 9 NS-NR | **(3) Percepción/actitud** — problema del entorno declarado por el respondente, no evento sufrido por él/ella; la segunda mitad (4.9) es organización vecinal, ni exposición ni desenlace de `G4` con nombre propio. **NO SIRVE** |
| `AP4_10_01`…`_16` | `TPer_Vic1` §IV, preg. 4.10 | *"Durante 2024, por temor a ser víctima de algún delito..., ¿dejó de [salir de noche / llevar dinero en efectivo / ...]?"* | Persona seleccionada | 1 Sí / 2 No / 3 No aplica / 9 NS-NR | **(3) Percepción/actitud → conducta**, pero la conducta es evitación motivada por **miedo**, no por exposición sufrida — y es conceptualmente la retracción del espacio público que `G4` **produce**, no lo que **consume** como antecedente (ver C2, §7). **NO SIRVE como `exposicion_violencia`** |
| `AP4_11_01`…`_11` (incl. `AP4_11_09` "adquirir armas de fuego") | `TPer_Vic1` §IV, preg. 4.11 | *"Durante 2024, para protegerse de la delincuencia, ¿en este hogar se realizó alguna medida como...?"* | Hogar (persona informante) | 1 Sí / 2 No / 9 NS-NR | Misma clase que `AP4_10` — conducta defensiva de protección, no exposición; `AP4_11_09` es el ítem más próximo en espíritu a "autodefensa" (ver C2). **NO SIRVE como `exposicion_violencia`** |
| `AP5_...` (toda la Sección V, vars 112-240) | `TPer_Vic1` §V, "Desempeño institucional" | *"¿Por qué identifica a la (al, los) (AUTORIDAD)?"* — razones: contacto directo, la ha visto, se la han platicado, medios (`fd.txt:779-800` y ss.) | Persona seleccionada | 1 Sí / 2 No / 9 NR | Constructo distinto por completo — reconocimiento/confianza en autoridades (`confianza_institucional`, ya parámetro aparte del modelo), no exposición a violencia. **NO SIRVE** |

**Búsqueda dirigida adicional** (`grep -i` sobre las 2 028 líneas de
`TPer_Vic1`): `presenci|testig|escuch|agres|golpe|amenaz|violenci|conoce
a alguien|algún familiar|vecino|disparo|balacera|enfrentamiento` — todos
los resultados caen dentro de las filas de la tabla de arriba (§4.5, §4.6,
§4.8/9, §5.8) o son ruido de paginación repetida del PDF (encabezados
"INEGI. Encuesta..." que el `grep` también captura por coincidencia
parcial de "violenci" en "Percepción sobre Seguridad Pública" — verificado
línea por línea, ninguno es un ítem nuevo). **No hay, en `TPer_Vic1`,
ningún ítem que pregunte por un hecho de violencia sufrida por la persona
misma, en ningún periodo de referencia.**

## 6 · Chequeo C3 (circularidad contra Tabla B)

```
$ grep -in "envipe" forense/notas/2026-07-31-inventario-segmentacion.md
```

**Sí aparece** — línea 4: ENVIPE es una de las **8 fuentes** de Tabla B
(`"ENIGH, ENIF, ENVIPE, ENOE, ENCUCI, ENCIG, ENSANUT, ENUT"`), y se usa en
varias filas de segmentación: `AP3_8`/`AP3_10` (condición de actividad,
línea 47, eje 1 parcial), `EDAD` (línea 60), `DOMINIO` (línea 73), `ESTRATO`
(línea 86), `AP4_9_1..6` (línea 246, organización vecinal, tangencial),
`AP5_2_1..4` (línea 262, confianza generalizada por vínculo), `BP1_23`
(línea 299, "callar" parcial) y, explícitamente, `BP1_20`+`BP1_23`+`BP2_1`+`BP1_28`
como el reactivo de las reglas `civico.denuncia.sin_seguro`/`con_seguro`
(línea 353, "Sí").

**A diferencia de ENDIREH (C3 pasó, cero resultados), aquí C3 sí importa
en principio** — pero como este acto **no adjudica ninguna candidata de
`TPer_Vic1`** (§5, todo NO SIRVE), la circularidad no llega a materializarse
sobre `exposicion_violencia`: no hay número que verificar contra Tabla B
porque no hay número. **Declarado para que quede registrado, no para
cerrar nada**: si una sesión futura reabriera alguno de los ítems de §5
como candidato (p. ej. bajo un reencuadre distinto de la distinción 3),
tendría que resolver C3 variable por variable contra las filas citadas
arriba antes de adjudicarlo.

## 7 · Chequeo C2 (mismo instrumento observa desenlaces de `G4`)

Los tres desenlaces enrutados por `G4` (`grep -n "PORQUE G4"
canon/modelo-decision-v4_0.md`): `civico.protesta.agravio_urbano`
(`:490`), `civico.autodefensa.agravio_rural` (`:491`),
`comunicacion.inseguridad.ver_oir_callar` (`:517`).

**No descartable con certeza — declarado ABIERTO**, misma disciplina que
ENDIREH paso 1. Lo que sí se verificó, dentro de `TPer_Vic1` y del
cuestionario principal completo (`cuest.txt`, 987 líneas, `grep`
dirigido sobre "protesta|autodefensa|linchamiento|justicia por propia
mano|ronda|guardia comunitaria|manifestaci|marcha|bloqueo|callar" — un
solo resultado, ajeno, línea 498, sobre programas de sensibilización para
denunciar): **ninguna variable de `TPer_Vic1` ni del cuestionario principal
lleva el wording literal de los tres IDs.** El vecino más próximo es
`AP4_11_09` ("adquirir armas de fuego", protección del hogar) — conducta
individual de armamento defensivo, no la organización rural de
`autodefensa.agravio_rural`; y `AP4_10`/`AP4_11` en conjunto son la misma
familia de conducta defensiva/evitación que `G4` **produce** como
desenlace, lo que hace más urgente, no menos, declarar C2 sin cerrar: si
`exposicion_violencia` se terminara midiendo con un candidato de otra
tabla de ENVIPE (`TMod_Vic`, `TPer_Vic2`, no abiertas por este acto), y
`AP4_10`/`AP4_11` se usaran para operacionalizar un desenlace de `G4` en
el mismo instrumento, el riesgo de identificación conjunta (C2) recaería
sobre esa combinación, no sobre `TPer_Vic1` aislado. **No se leyeron
`TMod_Vic`/`TPer_Vic2`/Sección VI-VII** (fuera del perímetro declarado de
este acto — insumos: FD + cuestionario principal, tabla `TPer_Vic1`) —
por lo que C2 no se puede cerrar aquí, ni falta que hiciera, dado que §5
ya no adjudica ninguna candidata.

## 8 · Ejes de atributos disponibles (canon §1.1.A)

No re-derivado desde cero — citado de `forense/notas/2026-07-31-inventario-segmentacion.md`,
que ya deriva disponibilidad de ENVIPE por eje (líneas citadas):

| Eje (canon §1.1.A) | ¿ENVIPE lo trae? | Cita |
|---|---|---|
| 1. Formalidad laboral | **Parcial** — `AP3_8`/`AP3_10` (condición de actividad, posición ocupacional), sin afiliación IMSS/ISSSTE | línea 47 |
| 2. Edad | **Sí** — `EDAD`, directa | línea 60 |
| 3. Urbanización | **Sí** — `DOMINIO` (U/C/R), variable de diseño muestral; categorización más gruesa que `tam_loc` de ENIGH (3 vs. 4 niveles), mismo eje | línea 73 |
| 4. Ingreso | **Parcial** — `ESTRATO` (1-4) es estrato del área por AGEB, no ingreso declarado por hogar/persona | línea 86 |
| 5. Acceso digital | **No** — único uso de "internet" es como modalidad del delito o canal de denuncia; sin variable de tenencia/uso propio | línea 99 |
| 6. Condición migratoria | **No** — sin variable de migración; único proxy débil es antigüedad residencial (`AP4_1`), declarado insuficiente | línea 112 |

**Dos ejes disponibles con confianza** (edad, urbanización), **dos
parciales** (formalidad laboral, ingreso — ambos a nivel de proxy más
débil que ENIGH), **dos sin equivalente confirmado** (acceso digital,
migración). Mismo patrón de disponibilidad mixta que ENDIREH paso 1, con
huecos en ejes distintos (ENDIREH: sin formalidad ni migración; ENVIPE:
sin acceso digital ni migración, más débil también en formalidad/ingreso).

## 9 · Declaración de contaminación (ADR-46)

**Este acto SÍ abrió el FD y el cuestionario principal de ENVIPE 2025**
(`fd_envipe2025.pdf` completo vía `pdftotext`, lectura dirigida y por
sección de `TPer_Vic1`; `cuest_principal_envipe2025.pdf` completo). **Esta
sesión y esta máquina, mientras retengan este contexto, quedan
inhabilitadas para pre-registrar contra ENVIPE** (ADR-46, unidad =
sesión). No se abrió microdato (`envipe2025_csv.zip` no se descomprimió) —
la inhabilitación es sobre estructura/contenido del instrumento, no sobre
filas de datos; se declara igual, conservador.

## 10 · Veredicto (vocabulario §3 del encargo)

**LA FUENTE NO TIENE EL DATO.** Descriptor recorrido completo de `TPer_Vic1`
(Secciones IV y V, ~225 variables sustantivas más las de identificación),
ninguna candidata sirve, con argumento por cada descarte (§5). No se
adjudicó nada, no se movió el contador (**8/14**), no se editó `hitoE §14.3`
— la fila 4 sigue **PENDIENTE DE VERIFICACIÓN** hasta que otra fuente o
tabla la resuelva.

**Nota para mesa, declarada y no decidida por este acto:** a diferencia de
los dos intentos previos del mismo acto nombrado en ADR-52 A (`PR #61` y
su reemisión, ambos **NO ALCANZABLE**, sin examinar nada), **este sí
examinó el descriptor y lo descartó con argumento** — la misma forma que
cerró `aversion_riesgo` (ENIF `P5_23`/`24`, candidato examinado y
descartado) y, por precedente, `sens_estatus` (ADR-54). Si ese precedente
aplica aquí, la "búsqueda sobre `TPer_Vic1`" quedaría cerrada por
argumento en vez de seguir contando actos hacia la caducidad de tres —
pero esa es exactamente la decisión que ADR-52 A reserva a mesa, no a
quien ejecuta el acto, y este documento no la toma. Lo que sí es un hecho
verificable: de los "dos actos en curso" que `gobernanza:527` nombra para
`exposicion_violencia`, **el otro (barrido ENDIREH/ENSU) ya no está en
curso** — concluyó con candidato parcial (`forense/hallazgos.md`, línea
77) — y este, el de `TPer_Vic1`, concluye aquí con NO SIRVE argumentado.
Ninguno de los dos es ya "en curso sin resultado"; ambos tienen veredicto
escrito. Queda en mesa decidir qué sigue: nombrar un tercer acto (otra
tabla de ENVIPE, `TMod_Vic`/`TPer_Vic2`, con su propia disciplina de
contaminación ya gastada en esta sesión para ENVIPE en general — ver §9),
adjudicar el candidato parcial de ENDIREH, o declarar `exposicion_violencia`
`NO DETERMINABLE EN ESTE RÉGIMEN` por la vía del precedente.

## 11 · Qué NO se hizo

- No se abrió `cuest_modulo_envipe2025.pdf` ni ningún microdato
  (`envipe2025_csv.zip`).
- No se leyeron `TMod_Vic`, `TPer_Vic2` ni las Secciones VI/VII del
  cuestionario (victimización en hogar/personal) — fuera del perímetro
  declarado (tabla `TPer_Vic1`).
- No se resolvió C2 (§7) — declarado abierto, no fabricado.
- No se tocó `canon/` ni `milpa/`.
- No se editó `hitoE §14.3` ni su fila 4 — la adenda de esta nota vive en
  `hitoE §19` (append-only), no en el cuerpo.
- No se decidió si este acto cierra la búsqueda por precedente (§10) —
  eso es de mesa.
- No se registró ninguna entrada nueva en `data/manifiesto.yaml` — los
  tres PDF de ENVIPE 2025 ya estaban registrados y verificados.

## 12 · Límite de lectura declarado

Leído completo (`pdftotext -layout`): `data/raw/fd_envipe2025.pdf`
(7 207 líneas — `TPer_Vic1`, líneas 858-2885, leída en su totalidad;
`TVivienda`/`THogar`/`TSDem`/`TPer_Vic2`/`TMod_Vic` solo localizadas por
encabezado, no leídas); `data/raw/cuest_principal_envipe2025.pdf`
(987 líneas, completo). Leído: `canon/modelo-decision-v4_0.md:260-280`
(paso 5, ADR-52 A), `:365-400` (tabla de generadores/coeficientes),
`:490-491`, `:517` (`PORQUE G4`); `canon/gobernanza-v1_15.md:525-527`
(ADR-52 A); `forense/hitoE-campana-medicion-v2_0.md §14.3` (fila 4),
`§15`, `§18`; `forense/hallazgos.md` (entradas 04/ago/2026, líneas 72,
74, 77, 79); `forense/notas/2026-07-31-inventario-segmentacion.md`
(grep dirigido: "envipe", no lectura completa de las 41 filas). No
abierto: `data/manifiesto-staging.yaml`. `python3 tests/check.py`
corrido tras la última edición de esta nota — resultado en la nota de
cierre de sesión (`bitácora`), no re-tecleado aquí.
