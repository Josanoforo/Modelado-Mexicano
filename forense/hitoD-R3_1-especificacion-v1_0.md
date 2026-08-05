# HITO D · Falsador `R3.1` — especificación pre-registrada, congelada antes de abrir microdato
### `hitoD-R3.1-especificacion` · **v1.0** · 4 de agosto de 2026

> ⚠️ **Congelado ANTES de abrir `encig23_base_datos_csv.zip`.** Este documento se cierra y se commitea antes de leer una sola fila de `encig2023_04_sec_7.csv` o `encig2023_05_sec_8.csv`. Todo lo que sigue se deriva de la ficha ya sellada (`forense/hitoD-preregistro-v2_0.md`, Nota 14, líneas 731-787) y de `data/raw/encig23_estructura_base_datos.pdf` (documentación/diccionario, no microdato) y de `forense/hitoD-R3_2-veredicto-v1_0.md` (veredicto ya archivado de la ficha hermana, mismo par de tablas). No se abrió el ZIP de microdatos para escribir nada de este documento.

---

## 1 · Regla de selección de pregunta — resuelta contra el diccionario, sin abrir microdato

La ficha (línea 760-765) fija tres formas en orden, evaluadas antes de abrir nada:

**1. Candidata primaria** — ¿existe en ENCIG 2023 un ítem o cruce que, DENTRO de trámites presenciales, distinga testigo, folio de queja o posibilidad de identificar al servidor? Revisado exhaustivamente contra `encig23_estructura_base_datos.pdf`, secciones VII (`encig2023_04_sec_7`, ítems `P7_1`…`P7_12A`) y VIII (`encig2023_05_sec_8`, ítem `P8_4`) — las dos únicas tablas que la restricción de lectura de `data/manifiesto.yaml:40` permite abrir para `R3.1`/`R5.1`/`R7.2`:

- `P7_10`/`P7_11` (*"¿Se quejó ante alguna institución de gobierno...?"* / *"¿Ante quién?"*) es lo más cercano — pero mide **si la persona presentó una queja**, una conducta posterior a un problema ya percibido, no si el trámite ofrecía **estructuralmente** un testigo, folio o posibilidad de identificar al servidor antes/durante el acto. Es el constructo que `P9_7`/`P9_8` (Sección IX, general, no por trámite) también mide y tampoco sirve por la misma razón.
- `P7_4_01`…`P7_4_11` (problemas del trámite: filas largas, requisitos, ventanillas, información incorrecta, costos, horarios) son de **calidad de servicio**, no de discrecionalidad/anonimato del funcionario.
- Ningún ítem de `P7_1`…`P7_12A` ni de `P8_1`…`P8_4` pregunta por nombre/identificación del servidor, número de folio de la gestión o presencia de testigo.

**Veredicto de este paso: la candidata primaria NO EXISTE.** No es hallazgo nuevo — la ficha misma (líneas 743-744) ya había verificado, contra el mapa de evidencia y el glosario, que este eje no tiene entrada propia en ningún lado del corpus; este documento extiende esa misma ausencia al diccionario de microdato.

**2. Respaldo 1** — usar el **tipo de trámite** (`N_TRA`) como proxy de discrecionalidad, por conocimiento externo al instrumento. **Se declara ejecutable** — ver clasificación §2. Por la letra explícita de la ficha (línea 762): *"este respaldo degrada automáticamente el veredicto a B, nunca a A"*. Se usa este camino.

**3. Respaldo 2** — no se evalúa: el Respaldo 1 ya es ejecutable, y la ficha ordena evaluar en secuencia (líneas 760-764), no en paralelo.

**Obligación de reporte cumplida** (línea 765): la lista completa de ítems revisados contra el criterio 1/2 es la de arriba — ninguno adicional cumplía.

---

## 2 · Clasificación de `N_TRA` — declarada por conocimiento externo, ANTES de ver ninguna fila

Catálogo completo de `N_TRA` (`encig23_estructura_base_datos.pdf`, tabla de `encig2023_05_sec_8`, códigos 01-21 + 22A-22E). Clasificación en dos grupos mutuamente excluyentes según si la aprobación/gestión del trámite depende del **juicio caso-por-caso de un funcionario individual, sin sistema estándar de folio/comprobante conocido públicamente** (ALTA) o es una **transacción reglada contra una tarifa/criterio publicado, con folio/comprobante/cita inherente al proceso** (BAJA), aunque no esté digitalizada. Códigos que mezclan ambos mecanismos bajo un solo `N_TRA`, o que no encajan limpio en el marco "trámite ante funcionario que aprueba/niega", se **excluyen** — no se fuerza una clasificación que el propio código no sostiene:

| `N_TRA` | Trámite | Clasificación | Razón |
|---|---|---|---|
| 01 | pago ordinario de luz | **BAJA** | tarifa fija, recibo |
| 02 | pago ordinario de agua | **BAJA** | tarifa fija, recibo |
| 03 | pago de predial | **BAJA** | tarifa fija (valor catastral), recibo |
| 04 | pago de tenencia/impuesto vehicular | **BAJA** | tarifa fija, recibo |
| 05 | vehiculares (verificación, refrendo, licencia, cambio propietario, reemplacamiento, revista) | *excluido* | mezcla registro reglado (refrendo/cambio propietario) con inspección de juicio (verificación de contaminantes) bajo un solo código — heterogéneo |
| 06 | fiscales (SAT/Hacienda, RFC, aduana importación) | *excluido* | mezcla declaración reglada (SAT/RFC) con clasificación/valoración discrecional (aduana) bajo un solo código — heterogéneo |
| 07 | citas médicas programadas IMSS/ISSSTE | **BAJA** | cita con folio |
| 08 | atención médica de urgencia | *excluido* | el mecanismo de "aprobar/evitar procedimiento" de la ficha no encaja limpio en triage médico de urgencia |
| 09 | educación pública (inscripción, becas, cambio escuela, certificados) | **BAJA** | matrícula/folio escolar reglado |
| 10 | Registro Civil (actas nacimiento/defunción/matrimonio/divorcio) | **BAJA** | acta con folio por diseño |
| 11 | servicios municipales (pavimentación, alumbrado, mantenimiento, pipas) | **ALTA** | solicitud informal, sin folio público estándar, priorización discrecional del funcionario municipal |
| 12 | locales (permisos vía pública, conexión/regulación agua-drenaje) | **ALTA** | permiso discrecional, sin folio público estándar |
| 13 | uso de suelo/construcción/demolición/Registro Público Propiedad | **ALTA** | permiso de aprobación discrecional (documentado como foco de mordida en la propia Nota 6/§2.8 de `R3.2`) |
| 14 | créditos vivienda (INFONAVIT/FOVISSSTE) / programas sociales (Bienestar, becas, LICONSA) | **BAJA** | criterio de elegibilidad reglado, expediente/folio |
| 15 | conexión/reconexión/fallas técnicas CFE | **BAJA** | orden de servicio/reporte de falla con folio |
| 16 | pasaporte SRE | **BAJA** | cita con folio |
| 17 | Ministerio Público/Fiscalía (averiguación previa/carpeta de investigación) | **ALTA** | discrecionalidad fiscal de iniciar/dar seguimiento (documentado en `R3.2`/§2.8) |
| 18 | juzgado/tribunal (familiar, laboral, penal) | **ALTA** | juicio caso-por-caso de personal judicial (documentado en `R3.2`/§2.8) |
| 19 | llamada de emergencia a la policía | *excluido* | no es un trámite de aprobación/negación ante funcionario en el sentido que la ficha nombra |
| 20 | contacto con policías (tránsito, infracciones, detenciones) | **ALTA** | discrecionalidad del oficial en el momento, sin folio/testigo por diseño del encuentro — el escenario de mordida más documentado en México |
| 21 | abrir empresa/negocio | *excluido* | bundle de sub-trámites de mecanismo mixto (registro formal RFC vs. licencias locales discrecionales), no distinguible con este código |
| 22A-22E | otros trámites | *excluido* | catch-all genérico, no clasificable |

**ALTA discrecionalidad** = {11, 12, 13, 17, 18, 20} (6 códigos) · **BAJA discrecionalidad** = {01, 02, 03, 04, 07, 09, 10, 14, 15, 16} (10 códigos) · **Excluidos** = {05, 06, 08, 19, 21, 22A, 22B, 22C, 22D, 22E} (10 códigos).

Esta clasificación es una **decisión pre-registrada de quien ejecuta el falsador**, no un hecho medido por INEGI ni derivado de ninguna fila del microdato — se declara explícitamente como tal, mismo criterio que la ficha ya fijó para el umbral `ASIGNADO` (línea 752).

---

## 3 · Universo, variables, y "pareada por tipo de trámite" — definiciones exactas

- **Universo:** filas de `encig2023_04_sec_7` con `P7_3 = 1` ("Instalaciones de gobierno" — presencial estricto, mismo corte que `R3.2` llamó "presencial") **y** `N_TRA` en {ALTA} ∪ {BAJA} de §2. Se excluyen filas con `N_TRA` en el conjunto excluido y filas con `P7_3 ≠ 1`.
- **Llave de unión:** `CVE_ENT+UPM+V_SEL+R_ELE+N_TRA` entre `encig2023_04_sec_7` y `encig2023_05_sec_8` — la llave documentada (`encig23_estructura_base_datos.pdf`, ambas tablas). **Duplicados por `NT_TIPO`** (hasta 3 instancias por llave en `sec_7`, ausente en `sec_8`): se aplica la misma disciplina que `R3.2` (§2.6.4) — instancias con `P7_3` consistente entre sí se colapsan sin pérdida; instancias con `P7_3` divergente entre sí se **excluyen** del cruce por no poder atribuir sin ambigüedad la modalidad al desenlace de `sec_8`. No se re-deriva el conteo de `R3.2` (7,101 colapsadas / 543 excluidas): ese conteo era sobre el universo completo de `R3.2` (todas las modalidades); aquí se recalcula sobre el subconjunto `P7_3=1` ∩ clasificado, que es distinto y se reporta en el commit 2.
- **Desenlace (`y`):** `P8_4` de `encig2023_05_sec_8`, unido por la llave de arriba. Dos interpretaciones, **idénticas a las que `R3.2` ya validó y no se re-deciden aquí** (§2.6.3 de `hitoD-R3.2`): **(a) restrictiva** — filas con `P8_4` en blanco se excluyen del universo (denominador = solo quienes ya tienen valor no-blanco); **(b) NA→0** — filas con `P8_4` en blanco se codifican `y=0`. Ambas se reportan, no se elige una.
- **Ponderadores — los tres regímenes, ninguno elegido de antemano:** sin ponderar (`w=1`), `FAC_TRA` (declarado para `encig2023_04_sec_7`), `FAC_P18` (declarado para `encig2023_05_sec_8`) — misma asignación tabla→ponderador que `hitoD-R3.2` ya verificó contra el diccionario para este mismo par de tablas; no se re-verifica byte a byte, se cita como hecho ya archivado.
- **Estrato/UPM:** `EST_DIS`/`UPM_DIS` (diseño), consistentes entre los tres regímenes de ponderador — mismo campo que `svystat.py: prop_ultimate_cluster` espera como `(estrato, upm, peso, y)`.
- **Ejes:** exposición = clasificación ALTA/BAJA de §2 (binaria, entre grupos, DENTRO de `P7_3=1`); desenlace = `P8_4` binario (interpretaciones a/b arriba).
- **Dicotomización:** ALTA vs. BAJA por trámite (§2); presencial estricto = `P7_3=1` únicamente (códigos 2,3,4,5,6,7,8,9 de `P7_3` no entran a ningún grupo, mismo tratamiento que `R3.2` dio a los códigos intermedios).
- **"Pareada por tipo de trámite" para efectos de esta corrida:** dado que el Respaldo 1 agrupa trámites completos en ALTA/BAJA (no compara el mismo `N_TRA` en dos condiciones), **no hay pareo por tipo de trámite individual posible bajo este camino** — es precisamente la razón, declarada por la ficha misma (línea 762), de que el techo de este camino sea `B`. Como chequeo de confundidor 1 (composición de trámites, línea 768), se reporta adicionalmente la incidencia por `N_TRA` individual dentro de cada grupo (mismo espíritu que `R3.2 §2.7`), sin que esto cambie el techo de veredicto ya fijado arriba.

---

## 4 · Resolución de la tensión textual entre la fila `A` de la escala y la línea 762 de la ficha

La fila `A` de la escala (línea 784) dice *"pareada por tipo de trámite cuando sea posible (**vía candidata primaria o Respaldo 1**)"* — lectura literal que permitiría `A` también por Respaldo 1. La línea 762, escrita en la misma ficha, dice sin ambigüedad: *"este respaldo degrada automáticamente el veredicto a B, **nunca a A**"*. Las dos frases, tomadas juntas, son contradictorias para el caso Respaldo-1-con-pareo.

**Resolución, declarada aquí antes de correr nada:** la línea 762 gobierna. Es más específica (habla exclusivamente de Respaldo 1, no de la escala en general), fue declarada primero en el cuerpo de la ficha (antes de llegar a la escala) como consecuencia explícita del propio Respaldo 1, y la regla de precedencia de la ficha (línea 785) resuelve por "condición propia explícita" de cada camino — la condición propia de Respaldo 1 (línea 762) ya fija su techo independientemente de lo que diga el texto de la fila `A`. Se lee el paréntesis de la fila `A` como una referencia incompleta (qué caminos pueden **alimentar** la comparación pareada, no una promesa de que Respaldo 1 sola basta para `A`), no como una segunda regla que compite con 762. **Consecuencia operativa: esta corrida no puede producir `A`, sin importar la magnitud de la brecha encontrada.** Solo `B` o `C` son alcanzables. Se declara el hueco textual para que mesa lo revise; no se edita la ficha (fuera de perímetro).

---

## 5 · Pre-registro de falsación — qué significa que NO se refute

**Si el resultado cae en `B`** (brecha presente, dirección predicha, sin pareo por tipo de trámite individual — techo de este camino): la regla **no se refuta**, queda **acotada** — hay señal de que la discrecionalidad dentro de lo presencial tiene su propio patrón, distinto del canal que `R3.2` ya midió, pero sin aislar los confundidores 1-3 de la línea 767-770 al nivel que `A` exigiría. Es corroboración débil, no fuerte.

**Si el resultado cae en `C`** (brecha ausente o invertida): se **refuta el componente de discrecionalidad** específicamente — el driver sería el canal (presencial/digital), ya cubierto por `R3.2`, y esta regla se retira como afirmación independiente. Esto no reabre `R3.2` ni cambia su veredicto archivado.

**Si el resultado no encaja limpio en ninguna de las dos** (p. ej., el intervalo de confianza de la brecha ALTA-vs-BAJA cruza cero, sin que la dirección sea clara — situación análoga a la reserva de `R5.2`/Nota 18, o al hueco de escala que `R1.2`/Nota 19 encontró): se declara así explícitamente en el commit 2, sin forzar una fila. La ficha de `R3.1` fue sellada como Nota 14, **antes** de la fila `E` prospectiva que ADR-58/Nota 26 añadió — y Nota 26 declara textualmente que no aplica retroactivamente a fichas ya selladas salvo la excepción nombrada de `R1.2`. Si aparece ese desenlace aquí, **no se usa la fila `E`** por analogía; se reporta el hueco a mesa, mismo criterio que `R1.2`.

**Reserva declarada de antemano:** un punto que satisface la lectura de "brecha presente" pero cuyo IC95% no despega claramente de cero no se adjudica como `B` limpio — se reporta como `B` con la reserva escrita, mismo criterio que `R5.2`/Nota 18 aplicó a `A`.

---

## 6 · Validación del estimador — límite declarado

`tests/svystat.py: prop_ultimate_cluster` no se modifica; ya está respaldado contra tres casos de referencia (E-3, PR #97). No se re-verifica aquí.

**No existe ancla externa publicada para el estimando específico de esta ficha** (brecha de incidencia de mordida entre trámites presenciales de alta y baja discrecionalidad) — la propia ficha ya lo verificó (líneas 742-744: ninguna entrada en el mapa de evidencia de `Psicología_Política` ni en el glosario nombra este eje). Se declara como límite, no se fuerza una comparación contra un número que mide otra cosa (p. ej. el 14% agregado nacional de "experiencia de corrupción" ya citado por `R3.2`/Nota 4 — es un agregado distinto, no un ancla para este contraste). **Sustituto de validación de canalización (pipeline), no de estimando:** se reporta, en el commit 2, la incidencia presencial agregada de este mismo universo (`P7_3=1`, sin distinguir ALTA/BAJA) contra el techo de 13.38% ya archivado por `hitoD-R3.2` — si la canalización de datos (unión, filtros, ponderadores) está bien construida, el agregado de este acto debe ser consistente en orden de magnitud con ese número ya publicado en este mismo corpus, aunque no sea un ancla académica externa.

---

## 7 · Qué NO hace este acto

No descarga nada (payloads ya en `data/raw`, hash verificado contra `data/manifiesto.yaml` antes de este documento). No toca `data/manifiesto.yaml`, `canon/`, ni sella ADR. No escribe en `## Registro de veredictos archivados` de `hitoD-preregistro-v2_0.md` — el resultado del commit 2 es una **propuesta de fila**, con su razón, para que mesa adjudique. Al abrir `encig23_base_datos_csv.zip` en el próximo commit, esta sesión queda inhabilitada para pre-registrar ninguna otra ficha contra ENCIG (ADR-46).

---

**el primer resultado que produzca este procedimiento es el que se reporta.**
