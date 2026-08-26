> segunda corrida divergente del mismo encargo, sin fusionar — se preserva para adjudicación por ficha

# Encargo PASE-FALSADORES — un pase único: "¿este falsador pide algo que puede existir?" sobre las fichas restantes sin vía en curso

*(Archivado por el propio acto conforme a `A.3`. Texto verbatim del encargo recibido de dirección el 25/ago/2026; no se edita.)*

- **Estado:** `CONSUMIDO` — 25/ago/2026, produce `forense/notas/2026-08-25-pase-falsadores.md`, fila de tablero `FP-158`, y esta nota.

---

SHA de redacción: `9e9132d`. Dirección, 25/ago/2026. ENTORNO: NUBE (`cloud_default`). FIRMA: ninguna — este acto pregunta y propone; mesa decide después, ficha por ficha. CONTADOR: cero por diseño.

Por qué existe (mandato de mesa): R2.1 demostró que un falsador puede estar sobre-diseñado — registrado en una forma que ningún estudio del mundo real corre — y que entonces su `D` describe nuestra redacción, no a México. Antes de gastar más búsquedas, cada ficha restante contesta UNA pregunta. Y el candado que mesa fijó rige también aquí: distinguir re-especificar (misma sustancia, nivel donde el dato vive) de ajustar-para-pasar (cambiar la sustancia hasta que algo la confirme) — este acto bosqueja lo primero y tiene prohibido lo segundo.

════ ARRANQUE ════
1. Verifica que estás en el repo correcto.
2. Verifica el SHA actual de HEAD contra `9e9132d` (informa si difiere, pero continúa).
3. Si data/raw está ausente, está OK, continúa.
4. Entorno NUBE (cloud_default): sin acceso a microdatos locales, salta la sonda de datos. Si necesitas usar web para verificar existencia puntual de una fuente/dataset, sé estricto: SIN-FETCH de contenido real si no tienes WebFetch confiable, documenta intentos y salida cruda, da recetas de 1 minuto para que un humano lo verifique, y NUNCA inventes datos de memoria del modelo.
5. Cero cifras "del espejo" (no inventes estadísticas de México de memoria — si necesitas un número real, dilo como pendiente de verificación, no lo inventes).
6. Los veredictos negativos (SIN-DATO-GENUINO) deben venir con conteo de qué se buscó + un control positivo de referencia (ej. estándar `#359` si aplica, o análogo).

═══ EXISTENCIA Y ALCANCE (dirección, contra `9e9132d`) ═══
F0: deriva la lista de fichas a revisar, NO la heredes de memoria. Busca en el repo (probablemente en `forense/` o similar) las fichas del preregistro de falsadores que:
  (a) NO tienen veredicto aún en el Registro (el README dice 20 de 27 con veredicto — busca el README relevante),
  (b) NO tienen ya una vía/proceso en curso.

EXCLUYE explícitamente, citando la fuente en el repo:
  - `R3.4` (tiene vía en curso: `#359`/`FP-157`)
  - `R2.1` (tiene vía en curso: `R21-FALSADOR-V2`)
  - `R10.1` (spec v2 ya sellada `FP-128`, `CORRE-R10.1` pendiente de lanzar pero ya en curso)
  - `R10.3` — SE LISTA PERO SE EXCLUYE: su cierre ético fue decisión/firma de mesa y NO se reabre. Se nombra solo para declarar el hueco, no ocultarlo.

Fichas esperadas tras el filtro (verifica contra lo que encuentres en el repo, puede diferir — si difiere, usa lo que encuentres y repórtalo): `R2.2`, `R8.2`, `R10.2` (las tres hoy marcadas `NO-ACCESIBLE`/propietarias en el repo) + cualquier otra ficha sin veredicto y sin vía en curso que encuentres.

Verifica que ningún pase idéntico ya exista: corre `grep -ril "pase.falsador" forense/` (o el path correcto que encuentres) con conteo de resultados, y repórtalo en tu nota.

═══ LA PREGUNTA, POR FICHA — VEREDICTO TRIPLE ═══
Para cada ficha en el alcance derivado, lee la ficha ÍNTEGRA (estructura SI→ENTONCES→PORQUE, el falsador, el umbral, los confusores, la escala) y clasifícala en UNO de estos tres veredictos:

1. EJECUTABLE-TAL-CUAL — el dato que el falsador pide existe o es verosímilmente accesible: nombra la fuente/instrumento/reactivo concreto si puedes identificarlo. `NO-ACCESIBLE` con costo/trámite conocido también cuenta aquí (escribe el trámite).

2. RE-ESPECIFICABLE — el diseño registrado en la ficha pide algo que nadie corre en el mundo real, pero la SUSTANCIA (la relación causal/empírica que el falsador quiere probar) es contrastable en OTRO nivel: bosqueja (sin firmar, sin re-escribir la ficha oficial) una operacionalización v2 — qué nivel, qué variable, qué confusores, qué letra máxima honesta se puede alcanzar (si la vía resultante es solo correlacional en vez de causal, dilo explícitamente, como se hizo en R1.4/R2.1-v2), qué fuente candidata serviría, y qué letra/rigor se pierde al degradar el diseño. IMPORTANTE: bosquejar no es lo mismo que re-especificar oficialmente — la enmienda real la firma la mesa después, tú solo propones.

3. SIN-DATO-GENUINO — ni el diseño registrado ni ninguna re-especificación honesta tienen manera de conseguir dato: describe exactamente qué tendría que existir en el mundo para que esto fuera falsable, y si existe una vía "llave en mano" clase (iii) (partnership tipo Compartamos/Resguarda u organización similar con acceso privilegiado a datos), estima su costo aproximado (orden de magnitud, no cifra falsa).
   Para las tres fichas propietarias (`R2.2`, `R8.2`, `R10.2` o las que encuentres marcadas NO-ACCESIBLE), la pregunta se afina: ¿la inejecutabilidad es DEL MUNDO (el dato es privado por naturaleza, punto final) o DEL FALSADOR (la ficha pide específicamente el corte privado/propietario cuando la misma sustancia podría contrastarse con una fuente pública)? Esta distinción es el entregable central para esas tres.

REGLAS DURAS (candado de mesa, aplica también aquí):
- Prohibido "ajustar para pasar": no cambies la sustancia de lo que el falsador afirma para que algo la confirme. Solo re-especificar (mismo fenómeno, nivel donde el dato realmente vive).
- No mides nada, no corres ningún estudio real — esto es un pase de triage documental.
- No modificas las fichas oficiales del preregistro ni el Registro de veredictos.
- No abres más vías en curso.

═══ CIERRE — QUÉ DEBES PRODUCIR ═══
1. Un archivo nuevo `forense/notas/2026-08-2X-pase-falsadores.md` (reemplaza 2X por el día correcto de hoy, 25 en formato correspondiente al estilo de archivos existentes en forense/notas/ — revisa el patrón de nombres ahí primero) que contenga:
   - Tabla: ficha × veredicto × bosquejo/fuente/letra-alcanzable × qué-falta
   - Un párrafo por ficha, en LENGUAJE LLANO, dirigido a "mesa" (los humanos que deciden): qué es la ficha, qué compra cada opción de veredicto, qué NO compra.
   - El resultado del grep de duplicados con su conteo.
   - Declaración explícita de las fichas excluidas (R3.4, R2.1, R10.1, R10.3) con la cita de por qué.

2. Actualiza el tablero de seguimiento del proyecto (busca dónde vive — probablemente un README, un TABLERO.md, o similar con filas de estado tipo A.12) agregando EXACTAMENTE UNA fila nueva de estado `ABIERTA` con texto tipo: "mesa decide por ficha el destino de {lista de fichas revisadas}". No agregues más filas.

3. Si el repo usa ADRs (Architecture Decision Records) o notas de decisión cortas para este tipo de encargo, agrega un ADR corto documentando que se corrió este pase (busca el patrón/carpeta de ADRs existente en el repo primero).

4. Si hay una suite de pruebas/validación con modo `--baseline` (busca scripts en el repo, probablemente Python, quizás en forense/ o scripts/), córrela para confirmar que no rompiste nada estructural. Si no existe tal cosa, sáltalo y anótalo.

5. Marca el encargo como `CONSUMIDO` en donde sea que el repo trackee encargos activos (busca el patrón — puede ser un archivo de encargos/tickets).

PROHIBIDO en este acto: no re-especifiques oficialmente ninguna ficha, no midas nada con datos reales, no toques el contenido de las fichas del preregistro ni el Registro de veredictos, no abrongas más filas en el tablero que la única exigida, no inventes cifras estadísticas de México.

---

## Cierre

- HEAD real al ejecutar: `c6a5ab3` (difiere de `9e9132d`, declarado, se continuó por instrucción del propio encargo).
- Alcance derivado (F0): `R2.2`, `R8.2`, `R10.2` — coincide exactamente con lo esperado por el encargo. Exclusiones verificadas contra `forense/hitoD-preregistro-v2_0.md` y `forense/firmas-pendientes.tsv` (`FP-157` para R3.4, `FP-128` para R10.1); `R2.1`/`R10.3` excluidas por cita directa del propio encargo, no re-verificadas más allá de eso en este acto.
- Grep de duplicados: `grep -ril "pase.falsador" forense/` → 0 resultados antes de este acto.
- Sin ADR nuevo — ver "Nota sobre ADR" en `forense/notas/2026-08-25-pase-falsadores.md` (este acto no tiene firma de mesa; un ADR sin firma no es un ADR).
- Tablero: fila `FP-158` nueva, `ABIERTA`, única fila agregada.
- Suite: `python3 tests/check.py --baseline` → `19 FAIL · 128 WARN`, LÍNEA BASE VERDE (sin entradas nuevas frente a `tests/baseline.json`), corrido después de escribir la nota y antes de este cierre.
- No se tocó ninguna ficha del preregistro ni el Registro de veredictos. No se abrió ninguna vía en curso nueva.
