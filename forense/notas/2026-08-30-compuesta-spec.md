# MAESTRA32-E8 · MEDICION-COMPUESTA — spec congelada (COMMIT-1)

Escrita ANTES de abrir un solo archivo de microdato. Contra árbol `2799132` (fetch+ff-merge confirmado; `git log -1` = `2799132 Merge pull request #397...`).

## §0 · Input de dirección que levanta la compuerta (verbatim, 30/ago/2026)

> INPUT DE DIRECCIÓN — maestra-32, 30/ago/2026 — levanta la compuerta de MAESTRA32-E8 y reordena el carril CAJA.
>
> 1. La compuerta "GATED a que MAESTRA32-E3 fusione" era de SECUENCIA de carril, no de DATOS: E8 no consume ningún producto de E3 (E8 abre ENCUCI 2020 SEC_4_5 y ENVIPE 2025 TPer_Vic1+BP1_23, ya medidas el 4/ago; E3 inventaría .dta/.sav/.rdata/.dbf de otros payloads). Se levanta. Tu PARO fue correcto y queda registrado como el entregable de arranque.
>
> 2. Orden nuevo del carril CAJA: E8 (este acto, ahora) → E3 (solo cuando el merge de E8 esté visible en main). La serie estricta dentro del carril se mantiene. E11 · COBERTURA-15 corre en NUBE en paralelo; compartidos, solo la cascada; renumera quien fusiona segundo.
>
> 3. Al archivar el encargo (paso 0-bis) añade en la CABECERA, sin tocar el cuerpo: "Enmienda in situ 30/ago/2026 (dirección): compuerta 'E3 fusionado' LEVANTADA — era de secuencia, no de datos; carril CAJA reordenado E8 → E3; input verbatim en la nota de cierre §0." Pega este input completo como §0 de forense/notas/2026-08-30-compuesta-cierre.md y cítalo en el ADR.
>
> 4. Completa el ARRANQUE antes de nada más: faltan el punto 3 (data/raw: existe / enlazada a <ruta>), el punto 4 con los dos valores crudos (CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE y la sonda curl, con A.13) y el punto 5. A.2 tercera parte es PARO-relevante aquí: `ls data/raw/ 2>/dev/null | head -1` debe mostrar el corpus compartido; si no, PARA y repórtalo.
>
> 5. Todo lo demás del encargo rige sin cambio: 0-bis → COMMIT-1 (spec congelada, frase de sello) → COMMIT-2. Ignora cualquier mención a pyreadstat: es de E3, no de E8. A.1 para los dos payloads: una invocación por --id. PR desde esta rama; ADR y FP re-derivados al escribir.

Nota: el input dice "peguen §0 en la nota de cierre"; esta spec la trae también porque se escribió en el mismo tramo y ambas notas deben ser autocontenidas para el ADR. La nota de cierre (COMMIT-2) repite §0 verbatim como su propia §0.

## Arranque (resumen, detalle completo en la respuesta de la sesión)

1. REPO: `/home/pc0/Modelado-Mexicano` (clon existente). Rama de trabajo `acto/maestra32-e8-medicion-compuesta`, creada sobre `main` tras `git fetch origin main && git merge --ff-only origin/main` (`main` estaba en `2c0d4c8`, avanzó limpio a `2799132`, sin commits locales perdidos — `git status` limpio antes y después).
2. SHA: coincide con el declarado por el encargo (`2799132`). Sin divergencia que re-derivar.
3. data/raw: existe, symlink a `/home/pc0/mm-corpus/raw`. `ls data/raw/ | head -1` → `2005trim1_csv.zip` (corpus compartido, no vacío).
4. ENTORNO: `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=<sin_variable>` (esperado). `curl -s -o /dev/null -w "%{http_code}" --max-time 10 https://www.inegi.org.mx/` → `200`. Ambos positivos; A.13 no aplica a un veredicto positivo.
5. ESPEJO: no usado. Toda cifra de esta nota y de la de cierre sale de `/home/pc0/Modelado-Mexicano`, comandos citados.

## (a) Fuentes y universos, re-derivados

### Payloads (A.1, verificación de hash — una invocación por --id)

```
$ python3 -c "import hashlib; print(hashlib.sha256(open('data/raw/BD_ENCUCI2020_dbf.zip','rb').read()).hexdigest())"
0414fd59e2afcc36294530687c721e8e86bd04e76ad95bfce4b7b2e70853f283
```
manifiesto.yaml `id: encuci2020_bd_dbf` declara `sha256: 0414fd59e2afcc36294530687c721e8e86bd04e76ad95bfce4b7b2e70853f283` — **coincide**.

```
$ python3 -c "import hashlib; print(hashlib.sha256(open('data/raw/envipe2025_csv.zip','rb').read()).hexdigest())"
8a7a99fd90ce9d03229759ba0ad84db4fba98b5bb1f5c85eef7d718b007816fa
```
manifiesto.yaml `id: envipe2025_csv` declara `sha256: 8a7a99fd90ce9d03229759ba0ad84db4fba98b5bb1f5c85eef7d718b007816fa` — **coincide**. Este es el payload que ACTO C abrió de verdad el 4/ago (no `envipe_2025_bd_envipe_2025_csv`, el de la canasta masiva DESC-1, sin abrir — son dos ids distintos, ver manifiesto.yaml líneas 306-325 y 8612-8619).

Estructura confirmada por script (`zipfile.namelist()`):
- `BD_ENCUCI2020_dbf.zip` → tabla dbf `ENCUCI_2020_SEC_4_5` (no releída fila por fila hoy; el 4/ago ya la explotó, esta spec re-usa su universo y lo re-deriva en COMMIT-2 contra el mismo dbf).
- `envipe2025_csv.zip` → contiene `tper_vic1_envipe2025/conjunto_de_datos/conjunto_de_datos_tper_vic1_envipe2025.csv` (91,183 filas de datos + 1 header, columna `ID_PER` presente, columnas `AP5_4_01..11` presentes) y `tmod_vic_envipe2025/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe2025.csv` (columna `BP1_23` y `ID_PER` presentes). **Nota de formato**: ambos CSV usan terminador de línea `\r` puro (estilo Mac clásico), sin `\n` — confirmado con `chunk.find(b'\n') == -1` y `chunk.find(b'\r')` encontrando el separador de filas. `tools/medicion_compuesta.py` debe leerlos con `newline=''` y separar por `\r`, o el parser de csv estándar fallará silenciosamente (una sola "fila" gigante). Esto es un rasgo del payload de origen, no un defecto del corpus.
- `AP7_3_05..15` (disparadores "no denunciante") viven en `tper_vic2_envipe2025/conjunto_de_datos/conjunto_de_datos_tper_vic2_envipe2025.csv`, no en TMod_Vic ni en TPer_Vic1 — confirmado por columnas del header. El universo de G4 requiere unir TRES tablas por `ID_PER`: TPer_Vic1 (θ), TPer_Vic2 (disparadores AP7_3), TMod_Vic (desenlace BP1_23), tal como usó el 4/ago.

### G1.radio_confianza

- Ponderador: **FAC_SEL**. Estrato: `EST_DIS`. UPM: `UPM_DIS`. Fuente: `forense/notas/2026-08-04-w-coeficientes-generador-paso1.md` §1.1/§3.1. Instrumento único (`ENCUCI_2020_SEC_4_5.dbf`, sin join).
- Universo: contacto `AP5_16_1..10` (al menos un `'1'`) → **13,435 de 21,519** el 4/ago (cita: `forense/notas/2026-08-04-w-coeficientes-generador-paso1.md` líneas 117-118). Se re-deriva en COMMIT-2 contra el mismo dbf; falsador del acto aplica si la diferencia >2%.
- Ítems: `AP5_1_1/2/3`, escala 0-10; confía = `{06..10}`, no confía = `{00..05}`, excluido `99` (no sabe/no responde).
- Desenlace: `tramite.mordida.discrecional` = 1 si `AP5_17='1'` o `AP5_18='1'`; 0 si ambas `='2'`; excluida la fila si alguna de las dos queda en `'9'` sin poder decidir el desenlace.
- IC del β̂ marginal por ítem (4/ago): **analítico**, no bootstrap — `se(β̂) = sqrt(se₁² + se₂²)` sobre grupos disjuntos, `IC95% = β̂ ± 1.96·se`, calculado con el estimador de conglomerados definitivos (`tests/svystat.py::prop_ultimate_cluster`, mismo estrato/UPM de arriba). El compuesto de este acto reusa el mismo método para el β̂ del compuesto (comparabilidad directa con el 4/ago, punto (c) de la spec del encargo).

### G4.confianza_institucional[justicia]

- Ponderador: **FAC_ELE** (no `FAC_ELE_AM`). Estrato: `EST_DIS`. UPM: `UPM_DIS`. Fuente: `forense/notas/2026-08-04-encargo-e-envipe-g4-paso1.md` §5-§10, §13.3. Join `ID_PER` entre TPer_Vic1 (θ), TPer_Vic2 (disparadores) y TMod_Vic (desenlace).
- Universo: disparadores `AP7_3_05..15` (no denunciantes) → 14,285 con al menos una fila calificante en TMod_Vic (`BPCOD` ∈ {05..15}, `BP1_23` no blanco) → **13,023 con desenlace binario** el 4/ago (1,262 excluidas por `BP1_23` ∈ {09,99}). Se re-deriva en COMMIT-2; falsador del acto aplica si la diferencia >2%.
- Ítems: `AP5_4_01/02/03/05/06/07/11` (7 instituciones), dicotomizados por ítem — confía = `{1,2}`, no confía = `{3,4}`, excluidos `9`/blanco — **cada ítem con su propio universo** ("identifica la institución"), tal como marca la premisa del encargo. El compuesto primario (ver (b)) se calcula solo sobre personas que identifican ≥4 de 7, así que su universo es la intersección declarada en (b), distinta del universo por ítem individual.
- Desenlace `BP1_23`: colapsado a nivel persona con precedencia declarada el 4/ago — 1 si alguna fila califica `{01,02,06,08}` (miedo/desconfianza institucional); 0 si alguna fila califica `{03,04,05,07}` (razón práctica, no desconfianza) y ninguna calificó en el paso anterior; excluida si solo quedan filas `{09,99}`.
- IC (4/ago): mismo método analítico que G1 (`prop_ultimate_cluster`), no bootstrap.

### FP-168 (método de IC del compuesto, punto (c) de la spec del encargo)

`forense/firmas-pendientes.tsv` línea 166 confirma FP-168 abierta: "Mesa fija nivel_ic y seed del bootstrap de scoring-adv1-m3.py... ninguno de los dos tiene cita en el árbol". Mesa dictó "benchmark web" (ADR-224, `canon/gobernanza-v1_15.md`); dirección corrió el benchmark y mesa firmó verbatim: **nivel_ic=0.95, seed=42** (cita: `canon/gobernanza-v1_15.md` — bootstrap percentil 95% con ≥10,000 remuestreos es la práctica dominante 2025-2026; bootstrap pareado por ítem/celda preferible al IC por brazo; `seed=42` es convención cultural sin propiedad estadística especial).

Puesto que las notas del 4/ago fijan su IC con el método **analítico** `prop_ultimate_cluster` (no bootstrap) para los β̂ por ítem, y ese método es directamente aplicable al β̂ del compuesto (mismo diseño muestral, misma fórmula, sin necesidad de remuestreo), esta spec usa **el método analítico del 4/ago** para el β̂ primaria y secundaria de ambos pares — cumple la comparabilidad exigida por (c) del encargo ("el mismo método que la nota del 4/ago... para comparabilidad") sin necesitar el bootstrap de FP-168. El bootstrap `B=10,000, seed=42` queda documentado aquí como respaldo declarado si `prop_ultimate_cluster` no pudiera aplicarse a algún caso de robustez (secundaria de caso completo con universo pequeño); se usa solo si ese caso ocurre, y se declara en la nota de cierre si se invoca.

## (b) Definición del compuesto

**G1** — primaria: media de `AP5_1_1/2/3` en escala 0-10, dividida entre 10 → θ ∈ [0,1] (usa toda la información, "sum score" estándar de la literatura). Secundaria: proporción de los 3 ítems con valor ≥6 (comparable ítem a ítem con el corte del 4/ago). Universo: mismo universo de contacto que arriba (13,435 re-derivado); fila excluida si algún ítem del compuesto queda en `99`.

**G4** — primaria: proporción de instituciones identificadas en las que la persona confía, calculada solo entre quienes identifican ≥4 de 7 instituciones (umbral declarado aquí, no ajustable tras ver el dato). Secundaria: caso completo — solo personas que identifican las 7 de 7. Universo base: mismo universo de disparadores/desenlace que arriba (13,023 re-derivado), intersectado con el criterio de identificación (≥4/7 para la primaria, 7/7 para la secundaria).

La primaria es la candidata a `valor_ejecutable`; la secundaria es lectura de robustez y se reporta en la nota de cierre, no se escribe al ejecutable.

## (c) Estimador

Modelo lineal de probabilidad ponderado (por `FAC_SEL` en G1, `FAC_ELE` en G4) del desenlace binario sobre θ compuesta continua en [0,1]: `desenlace ~ β₀ + β̂·θ`. Unidades: cambio en la proporción del desenlace por unidad completa de θ (0→1) — mismas unidades que "diferencia de proporciones (θ=1 − θ=0)" del 4/ago, sin cambio de escala (θ ya está en [0,1], no hay que reescalar el β̂ resultante).

IC95%: método analítico `prop_ultimate_cluster` (mismo que el 4/ago), declarado arriba en §FP-168. Si algún caso de robustez no admite ese método (n insuficiente para el estimador de conglomerados, celdas vacías tras el filtro ≥4/7 o 7/7), se declara explícitamente en la nota de cierre y se usa el respaldo bootstrap percentil `B=10,000, seed=42` (FP-168), citando cuál caso lo disparó.

## (d) Consistencia interna

α de Cronbach sobre `AP5_1_1/2/3` (G1, escala 0-10 tratada como continua) y KR-20 equivalente sobre `AP5_4_01/02/03/05/06/07/11` (G4, dicotómicos) — ninguno de los dos fue calculado el 4/ago (confirmado: ninguna mención de "Cronbach" ni "KR-20" en ninguna de las dos notas del 4/ago). Se calcula por primera vez en COMMIT-2.

Regla pre-registrada, congelada aquí antes de ver el dato: **α < 0.50 ⇒ el compuesto NO se escribe al ejecutable, se reporta como hallazgo de dimensionalidad. α ≥ 0.50 ⇒ se escribe.**

## (e) Condicionamiento

Mismo patrón que el 4/ago, un eje a la vez, celdas con n≥30:
- G1 → formalidad, edad, ingreso (mismos ejes que `Encargo X`, recontado por ADR-61).
- G4 → edad, dominio (mismos ejes disponibles en el universo de G4, ver `valor_origen` de `G4.exposicion_violencia` en `coeficientes_generador_sellados`, que comparte universo y celdas con este par).

Diagnóstico, no compuerta: no gatea la escritura del ejecutable, alimenta `reserva:`.

## (f) B-bis — veredictos pre-registrados, antes de ver el dato

- IC que incluye 0 ⇒ se escribe igual, con sufijo `·NO-DISTINGUIBLE-DE-CERO` en el rótulo y línea explícita en el ADR (mesa puede vetar al recibir; se abre FP nueva si ocurre).
- Signo discordante entre el β̂ compuesto y los β̂ por ítem individuales ⇒ hallazgo, se escribe igual, discordancia declarada en `reserva:`.
- Inversión bajo condicionamiento (esperada en G1, dado el precedente de `Encargo X`/ADR-61: 33/39 celdas invierten) ⇒ va a `reserva:` verbatim, mismo patrón que ACTO E1 usó para `G1.confianza_institucional`.

## Sección A — coeficientes_generador_sellados (estado hoy, verificado con yaml.safe_load contra 2799132)

6 entradas: G1/confianza_institucional (`valor_ejecutable: -0.0645`), G3/familismo_apoyo (`+0.0279`), G4/exposicion_violencia (`0.16614`), G3/horizonte_temporal (`0.0876`, ADR-225/CAL-G3) — **4 con valor_ejecutable**. Sin `valor_ejecutable`, rótulo `SELLADO-ESCALA·SIN-AGREGACION`: `gen: G1, coef: radio_confianza` y `gen: G4, coef: confianza_institucional` — **estos son los 2 pares que este acto llena**. Campos existentes por entrada: `gen, coef, clase, valor_origen, unidad_origen, [valor_ejecutable], [ic], [escala], rotulo, reserva, fuente`. COMMIT-2 añade a las 2 entradas sin campo ejecutable: `valor_ejecutable`, `ic`, `escala`, `definicion_compuesto`, `alpha` (nuevos campos, mismo patrón de "agregar sin reemplazar" de ADR-220), y actualiza `rotulo`/`reserva` con el resultado — el `valor_origen`/`unidad_origen`/`rotulo` previo NO se borra, queda como historia (A.10); el rótulo pasa de `SELLADO-ESCALA·SIN-AGREGACION` a `ASOCIACION-MEDIDA·COMPUESTO·MARGINAL[·NO-DISTINGUIBLE-DE-CERO]` en el campo nuevo, no se sobreescribe el string viejo salvo que el proyecto use un único campo `rotulo` — en ese caso se reemplaza el valor de `rotulo` (transición de estado, no historia paralela) y el string SELLADO- anterior queda citado en `reserva:` para trazabilidad.

## Sello

El primer resultado que produzca este procedimiento es el que se reporta. Un tercer commit puede decir que la spec estaba mal; nunca se edita hacia atrás.
