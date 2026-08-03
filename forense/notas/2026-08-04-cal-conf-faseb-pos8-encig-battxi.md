# CAL-CONF Fase B, posición 8 — paso 1: ¿la batería XI de ENCIG cubre los seis componentes de `confianza_institucional`?

*4 de agosto de 2026.*

⚠️ **CONTAMINACIÓN DE MICRODATO, declarada para esta sesión.** Esta sesión
abre el instrumento de **ENCIG 2021** (`encig21_cuestionario.pdf`,
`encig21_estructura_base_datos.pdf`) — descriptor y cuestionario, no
microdato (no se abrió `encig2021_csv.zip`). Por ADR-46(3) queda
**inhabilitada para pre-registrar contra ENCIG**; por ADR-46(4) el
conservador declara más exploración, no menos, así que la declaración cubre
el instrumento completo leído, no solo la sección XI. Ver cierre en §4.

**Procedencia.** Tipo (1) para todo lo verificado contra archivo en esta
sesión (`encig21_cuestionario.pdf`, `encig21_estructura_base_datos.pdf`,
`forense/hitoE-campana-medicion-v2_0.md` §14.3, `canon/modelo-decision-v4_0.md`
§1.3, `forense/notas/2026-07-31-cal-conf-fasea.md`). Tipo (3), no
re-verificada aquí, la premisa de procedencia del encargo (verificación por
"maestra #17" contra `main` en `53fb810`) y la cita literal de
`modelo:396`.

**Sesión-tipo: Ubuntu.** `data/raw` es symlink compartido
(`/home/pc0/mm-corpus/raw`) montado en el worktree de esta sesión
(`mm-cal-conf-pos8`, rama `sesion/cal-conf-faseb-pos8-encig-battxi`, sobre
`origin/main` = `2a218a1`, PR #57 ya fusionado). Los dos PDF ya estaban en
disco; sha256 y tamaño verificados contra `data/manifiesto.yaml` antes de
abrir nada:

| Payload | sha256 | Tamaño | Verificación |
|---|---|---|---|
| `encig2021_cuestionario_pdf` | `9ee829815e8dca5ebe562b26afb006dcec475840bf27a206a0b838534041e45a` | 1 918 370 B | **Coincide** |
| `encig2021_estructura_base_datos_pdf` | `365c031bf48af4c6d65a8e5422c6cf0362500efd37cd0e924e3c1fe38b965dd2` | 2 612 238 B | **Coincide** |

No aplica §1-bis (variante nube): esta sesión corrió Ubuntu, con `data_raw`
montado, así que no hubo sonda de alcanzabilidad ni descarga.

---

## 1 · Batería XI completa — Sección XI "Confianza en instituciones", pregunta 11.1

Extraída con `pdftotext -layout` sobre ambos PDF. 25 ítems, un solo formato
de respuesta ("¿cuánta confianza le generan…", 1 Mucha confianza / 2 Algo de
confianza / 3 Algo de desconfianza / 4 Mucha desconfianza / 5 No aplica / 9
No sabe). Código de variable de `encig21_estructura_base_datos.pdf` §XI
(p. sección "XI. CONFIANZA EN INSTITUCIONES"), descriptor literal de
`encig21_cuestionario.pdf` p. 22.

| Ítem | Código | Descriptor literal |
|---|---|---|
| 01 | `P11_1_1` | Universidades públicas? |
| 02 | `P11_1_2` | Policías? |
| 03 | `P11_1_3` | Hospitales públicos? |
| 04 | `P11_1_4` | Presidencia de la República y Secretarías de Estado? |
| 05 | `P11_1_5` | Empresarios? |
| 06 | `P11_1_6` | Gubernatura de su estado/Jefatura de gobierno (CDMX)? |
| 07 | `P11_1_7` | Compañeros del trabajo (Jefes o subordinados)? |
| 08 | `P11_1_8` | Presidencias municipales de su estado/Alcaldías (CDMX)? |
| 09 | `P11_1_9` | Parientes como tíos, primos, sobrinos, etc.? |
| 10 | `P11_1_10` | Sindicatos? |
| 11 | `P11_1_11` | Vecinos? |
| 12 | `P11_1_12` | Cámaras de Diputados y Senadores? |
| 13 | `P11_1_13` | Medios de comunicación? |
| 14 | `P11_1_14` | Institutos electorales? |
| 15 | `P11_1_15` | Comisiones de derechos humanos? |
| 16 | `P11_1_16` | Escuelas públicas de nivel básico? |
| 17 | `P11_1_17` | Jueces y Magistrados? |
| 18 | `P11_1_18` | Instituciones religiosas, su iglesia o grupo religioso? |
| 19 | `P11_1_19` | Partidos políticos? |
| 20 | `P11_1_20` | Guardia Nacional? |
| 21 | `P11_1_21` | Ejército y Marina? |
| 22 | `P11_1_22` | Ministerio Público? |
| 23 | `P11_1_23` | Servidores públicos o empleados de gobierno? |
| 24 | `P11_1_24` | Organizaciones de la Sociedad Civil (ONG'S)? |
| 25 | `P11_1_25` | Organismos Autónomos Públicos/Descentralizados (CONAPRED, INE, CNDH, INEGI, etc.)? |

**No enumerado como cobertura aparte:** la pregunta de seguimiento 11.1a
(`P11_1A_1`…`P11_1A_25`, "¿cuál de las dos/tres calificaciones le otorga en
11.1?") repite la misma lista de 25 instituciones — es una aclaración sobre
la respuesta ya dada en 11.1, no un ítem adicional de confianza. No aporta
cobertura que 11.1 no tenga.

---

## 2 · Veredicto por componente, contra `canon/modelo-decision-v4_0.md` §1.3 (ADR-28.b)

| Componente | Veredicto | Ítem(s) ENCIG · código · descriptor literal |
|---|---|---|
| **Salud** | **CUBIERTO** | Ítem 03 · `P11_1_3` · "Hospitales públicos?" |
| **Educación** | **CUBIERTO** | Ítem 01 · `P11_1_1` · "Universidades públicas?" — Ítem 16 · `P11_1_16` · "Escuelas públicas de nivel básico?" |
| **Financiera** | **NO CUBIERTO** | Ningún ítem de los 25. El único candidato por cercanía temática es ítem 05 `P11_1_5` "Empresarios?" — descarta por descriptor: "empresarios" es confianza en un actor social (personas que emprenden/dirigen negocios), no en una institución de servicios financieros. El componente financiera ya tiene candidata verificada en otro instrumento —ENIF, Sección 11 "Confianza y protección de personas usuarias de servicios financieros", `P11_1_1`-`P11_1_5` (`forense/notas/2026-07-31-cal-conf-fasea.md`, fila Financiera)—, y ENCIG no trae nada equivalente: ni bancos, ni SOFOM/SOFIPO, ni aseguradoras, ni Afores, ni CONDUSEF/CNBV. |
| **Seguridad-FFAA** | **CUBIERTO** | Ítem 20 · `P11_1_20` · "Guardia Nacional?" — Ítem 21 · `P11_1_21` · "Ejército y Marina?" |
| **Justicia-policía** | **CUBIERTO** | Ítem 02 · `P11_1_2` · "Policías?" — Ítem 17 · `P11_1_17` · "Jueces y Magistrados?" — Ítem 22 · `P11_1_22` · "Ministerio Público?" |
| **Electoral-partidos** | **CUBIERTO** | Ítem 14 · `P11_1_14` · "Institutos electorales?" — Ítem 19 · `P11_1_19` · "Partidos políticos?" (Ítem 12 · `P11_1_12` · "Cámaras de Diputados y Senadores?" es adyacente — legislativo, no estrictamente electoral-partidos; no se cuenta como necesario para el veredicto, que ya está CUBIERTO por 14 y 19) |

**Resultado: 5 de 6 CUBIERTO, 1 de 6 (financiera) NO CUBIERTO.** Ningún
veredicto se resolvió por parecido de nombre: educación, seguridad-FFAA,
justicia-policía y electoral-partidos ya estaban además verificados —con la
misma cita de ítem/código— en `forense/notas/2026-07-31-cal-conf-fasea.md`
(Fase A, 31/jul), que esta nota confirma releyendo el cuestionario
directamente en vez de heredar la fila sin abrir el PDF.

---

## 3 · Conclusión — rama escrita antes de mirar la tabla de §2

El encargo declara las dos ramas por adelantado: si los seis quedan
CUBIERTOS, P4 es corrible y el paso 2 es una medición Ubuntu sobre ENCIG. Si
alguno queda NO CUBIERTO, ese es el resultado de P4 en este régimen.

**Sale la segunda rama.** `financiera` queda NO CUBIERTO en ENCIG. La
batería XI, por sí sola, no cierra los seis componentes en un solo
instrumento — cubre cinco. Completar `financiera` exige ENIF (`P11_1_1`-
`P11_1_5`), un instrumento distinto, con muestra, ponderador y universo
propios.

**P4 no es corrible en este régimen, y esto es su resultado, no una tarea
pendiente.** La evaluación de `hitoE §14.3` posición 8 ya lo anticipaba: P4
compara *entre* componentes, y una dispersión entre componentes medidos en
instrumentos distintos exige fabricar la conjunta que `modelo` §1.1.C
prohíbe. Esta sesión cierra la pregunta que esa evaluación dejó abierta —
"¿lo resuelve ENCIG solo?"— con NO: ENCIG cubre salud, educación,
seguridad-FFAA, justicia-policía y electoral-partidos, pero no financiera.
No hay ningún instrumento único en el corpus que traiga los seis
componentes en la misma batería. El límite es del mismo tipo que las 2 de
`§14.4` (`sens_estatus`, `aversion_riesgo`): no se colapsa a "P4 no existe",
se registra como **NO DETERMINABLE EN ESTE RÉGIMEN sin fabricar una
conjunta prohibida**, con el faltante nombrado (financiera) para que quede
verificable, no solo declarado.

No aplica la rama de ejes `x` de co-observación (era condicional a los seis
CUBIERTOS).

---

## 4 · Declaración de contaminación, al cierre (ADR-46)

Esta sesión leyó el instrumento de ENCIG 2021 (`encig21_cuestionario.pdf`,
`encig21_estructura_base_datos.pdf`) completo en su sección XI y de forma
dirigida en el resto de la estructura de variables (búsqueda de `P11_1`,
`BATER`, `XI`). Por ADR-46(3) queda **inhabilitada para pre-registrar contra
ENCIG**. El pre-registro del paso 2 —si algún día una fuente única
resolviera los seis componentes— lo escribe otra sesión limpia, igual que
se aplicó en `PR #57`.

## 5 · Fuera de perímetro, y por qué no se tocó

No se abrió microdato de ENCIG (`encig2021_csv.zip`). No se decidió si `G1a`
se desdobla — es mesa, paso 3. No se tecleó ninguna cifra de `modelo:396`
como dato verificado: la cita "Marina 89% / partidos 23.9%" no aparece en
esta nota salvo por referencia, porque no se usó ni se contrastó aquí. No se
tocó `data/manifiesto.yaml` (los dos ids ya estaban registrados). No se
abrió ENIF, ENVIPE ni ENCUCI en esta sesión — la fila `Financiera` de §2 cita
la verificación ya hecha en `forense/notas/2026-07-31-cal-conf-fasea.md`, no
una re-apertura.
