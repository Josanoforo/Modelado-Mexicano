ENCARGO FINAL · ACTO MAESTRA38-M13 · M-POR-CELDA v1.3
MODELO
Claude Opus Ultracode.
NATURALEZA
Trabajo sustantivo de modelo.
No es AUTOMATIZA.
Este encargo incorpora:

* la propuesta de dirección `M-POR-CELDA`;
* `ENMIENDA-1 · ACTO MAESTRA38-M13 · PIEZA 2 RE-EMITE POR EL CAMINO REAL`;
* la revisión final contra `origin/main`.

La enmienda gobierna donde corrigió el camino real de M, salvo las correcciones explícitas de este documento.
Está autorizado ejecutar, abrir PR y dejarlo listo para mesa.
Claude NO fusiona.
0 · OBJETIVO
Corregir el enlace M de tres celdas TRA del marco vigente para que dejen de consumir el valor histórico ASIGNADO:

```text
tramite.mordida.discrecional
→ paga_mordida
→ p = 0.62

```

y consuman la conducta medida ya existente y sellada en el motor:

```text
tramite.mordida.discrecional
→ paga_mordida_encig2025
→ p = 0.085118
→ clase MEDIDO*

```

Celdas afectadas exclusivamente:

```text
TRA-M-02
TRA-M-03
TRA-M-07

```

No buscar diversidad de M artificialmente.
La corrección se hace porque el par `(regla, conducta)` correcto ya existe medido en `milpa/tramite.yaml`, no porque produzca un benchmark más favorable.
M permanece CIEGO A R durante toda la fase de enlace y reemisión.
1 · AUTORIDAD Y LANZAMIENTO
Al comenzar:

```bash
git fetch origin main
git rev-parse origin/main

```

`origin/main` vigente es autoridad.
El SHA observado al redactar este encargo fue:

```text
3d6dee33...

```

pero NO se hereda.
Re-derivar todo al arrancar.
Usar `/acto`.
Si `CIERRA-AUTOMATIZA-E6 · TABLERO-VIVO` sigue abierto y no fusionado, esperar su fusión antes de iniciar M13, porque ambos actos pasan por gobernanza/estado y no conviene crear una colisión artificial de ADR.
M13 NO modifica el tablero directamente.
2 · PREMISA CORREGIDA POR ENMIENDA-1
El agregado no consulta M vivo desde `milpa/tramite.yaml`.
La cadena real es:

```text
marco
  ↓
tools/emite_m.py::emite_celda()
  ↓
milpa.src.emisor.emitir_binaria()
  ↓
corridas-M/M-<id>*.json
  ↓
agregado_v1_2.py::_leer_m()

```

`agregado_v1_2.py` lee primero:

```text
M-<id>.json

```

y, si no existe:

```text
M-<id>__v1_2.json

```

Por tanto:

```text
cambiar conducta en el marco
SIN reemitir M
=
cero cambio efectivo en el agregado

```

Este acto debe reemitir las tres TRA por el camino real.
3 · CORRECCIÓN MATERIAL ADICIONAL
`ola_calibracion` DEBE RESOLVERSE POR CONDUCTA
La enmienda presupone que:

```text
paga_mordida_encig2025
→ ola_calibracion ENCIG 2025

```

pero `tools/emite_m.py` vigente no garantiza eso.
Hoy `cita_ola_calibracion()` resuelve fundamentalmente por regla.
Para:

```text
tramite.mordida.discrecional

```

existe un fallback/fijo histórico:

```text
ENCIG 2023

```

que corresponde a:

```text
paga_mordida

```

No a todas las conductas que posteriormente convivieron dentro de esa regla.
Resultado requerido
Hacer el resolver conducta-aware.
Contrato conceptual:

```python
cita_ola_calibracion(regla_id, conducta, lineas_tramite)

```

Prioridad

1. Buscar una enmienda exacta de esa regla cuyo `aplica_a` contenga la `conducta` exacta y que declare `ola_calibracion`.
2. Si existe exactamente una:
usar esa calibración y su cita real.
3. Si existen cero:
conservar el mecanismo histórico de la regla.
4. Si existen más de una:
PARO por ambigüedad.

No fuzzy matching.
No prefijos.
No “primera MEDIDO”.
No inferencia por parecido de nombre.
4 · CASOS QUE DEBEN QUEDAR DEMOSTRADOS
Sobre `tramite.mordida.discrecional`:

```text
paga_mordida
→ ENCIG 2023

```

sin cambio respecto del comportamiento histórico.

```text
paga_mordida_encuci2020
→ ENCUCI 2020

```


```text
paga_mordida_encig2025
→ ENCIG 2025

```

El valor exacto de la cadena de calibración se lee del YAML vigente, no se vuelve a teclear en una segunda fuente salvo que la arquitectura existente obligue.
La cita debe seguir apuntando al texto real de `milpa/tramite.yaml`.
5 · PRUEBA PERMANENTE JUSTIFICADA
Este defecto es material porque puede cambiar F-DD y decidir si una celda puntúa.
Añadir una prueba pequeña para el resolver de calibración.
Debe proteger al menos:

```text
paga_mordida               → ENCIG 2023
paga_mordida_encuci2020     → ENCUCI 2020
paga_mordida_encig2025      → ENCIG 2025

```

Y conservar la regresión vigente de:

```text
M-TRA-M-01
M-TRA-M-02

```

sobre el camino histórico.
La regresión P2 de `tools/emite_m.py` debe PASAR antes de crear cualquier JSON v1.3.
Si falla:

```text
PARO
cero M-v1_3 escritos

```

No ajustar el resultado para hacerlo pasar.
6 · COMMIT 1
RESOLVER DE CALIBRACIÓN
Primer commit sustantivo:

```text
fix emite-m: resuelve ola_calibracion por conducta

```

Incluye:

```text
tools/emite_m.py
test dirigido mínimo

```

No crea todavía:

* marco v1.3;
* M v1.3;
* agregado;
* benchmark.

Después:

```bash
python3 tools/emite_m.py

```

o la invocación de regresión equivalente vigente.
La regresión histórica debe quedar sin divergencia sustantiva nueva.
7 · MARCO M v1.3
MISMO UNIVERSO, MISMO SORTEO, NUEVO ENLACE PARA 3 CELDAS
Crear:

```text
forense/prereg-duelo-v2/marco-M-sorteado-v1_3.tsv

```

a partir de:

```text
marco-M-sorteado-v1_2.tsv

```

Invariantes
Debe conservar:

```text
14 celdas
mismos 14 IDs
mismo orden
mismas encuestas
mismas olas
mismo universo
mismo R
mismo L
mismo sorteo
misma elegibilidad

```

No crear un nuevo sorteo.
No crear por defecto:

```text
marco-M-congelado-v1_3.tsv

```

porque el universo congelado y la selección no cambian.
v1.3 es una corrección de enlace M POST-SORTEO sobre tres celdas seleccionadas.
8 · CAMBIO AUTORIZADO DE ENLACE
Para:

```text
TRA-M-02
TRA-M-03
TRA-M-07

```

cambiar:

```text
conducta = paga_mordida

```

a:

```text
conducta = paga_mordida_encig2025

```

La regla permanece:

```text
tramite.mordida.discrecional

```

9 · CONSISTENCIA INTERNA DEL MARCO
No dejar columnas que contradigan el nuevo enlace.
El objetivo sustantivo es UNA decisión:

```text
(regla, conducta)
tramite.mordida.discrecional / paga_mordida
→
tramite.mordida.discrecional / paga_mordida_encig2025

```

Pero las consecuencias mecánicas de esa decisión también deben reconciliarse.
Antes de escribir, Opus debe listar qué columnas de las tres filas dependen del enlace.
Como mínimo revisar:

```text
frase_discriminacion
conducta
ola_calibracion
razon
grado_DD
razon_DD

```

y cualquier otra que afirme literalmente:

```text
paga_mordida
p = 0.62
ENCIG 2023

```

Si la afirmación deja de ser verdadera con el nuevo enlace, actualizarla.
No cambiar campos que describen otra cosa.
En particular no cambiar mecánicamente sin demostrar necesidad:

```text
variable
ponderador
cv_arbitro
grado_sellado
grado_transferencia
encuesta
ola
universo

```

`grado_DD` esperado en las tres sigue siendo:

```text
P1 PUNTUA

```

pero su razón debe citar la calibración correcta de ENCIG 2025.
Control
Las otras 11 celdas deben ser idénticas a v1.2.
Producir una comprobación mecánica de:

```text
11/11 filas no afectadas = idénticas

```

Para las tres TRA, enumerar exactamente qué columnas cambiaron.
10 · CASO ESPECIAL TRA-M-02
TRA-M-02 es:

```text
ENCUCI 2020

```

Existe dentro de la misma regla:

```text
paga_mordida_encuci2020
p = 0.125822
ola_calibracion = ENCUCI 2020

```

NO usarla en este acto.
Razón:
bajo F-DD produciría:

```text
P0 VERIFICACION

```

porque la celda y la calibración serían la misma encuesta/ola.
Este acto selecciona exactamente:

```text
paga_mordida_encig2025

```

como transferencia externa.
No fallback.
No “elige la MEDIDO que permita puntuar”.
La correspondencia está decidida antes de abrir R.
Si `paga_mordida_encig2025` no puede emitirse exactamente:
PARO.
11 · REEMISIÓN M v1.3
ANTES de abrir:

```text
corridas-R/
espec-R-ciega-v1_2.tsv
agregado-v1_2-resultado.json
scoreboard factual con R

```

reemitir exclusivamente:

```text
TRA-M-02
TRA-M-03
TRA-M-07

```

por:

```python
tools.emite_m.emite_celda(...)

```

usando:

```text
fuente_acto =
ACTO MAESTRA38-M13 · EMITE-M-v1_3

```

y:

```text
marco_nombre =
marco-M-sorteado-v1_3.tsv

```

Crear:

```text
corridas-M/M-TRA-M-02__v1_3.json
corridas-M/M-TRA-M-03__v1_3.json
corridas-M/M-TRA-M-07__v1_3.json

```

No editar.
No sobrescribir.
No borrar:

```text
M-TRA-M-02.json
M-TRA-M-03.json
M-TRA-M-07.json

```

La historia queda intacta.
12 · VERIFICACIÓN OBLIGATORIA DE LOS 3 JSON
Cada nuevo JSON debe cumplir:

```text
regla == tramite.mordida.discrecional
conducta == paga_mordida_encig2025
p == 0.085118
valor_punto == 0.085118
clase empieza con MEDIDO
estado_M == EMITE
ola_calibracion empieza con ENCIG 2025
grado_DD == P1 PUNTUA
ciego_a_R == SI

```

Y:

```text
cita_p

```

debe citar la conducta `paga_mordida_encig2025`.

```text
cita_ola_calibracion

```

debe citar la calibración de la enmienda ENCIG2025, no el fallback ENCIG2023.
Esperado por celda
TRA-M-02:

```text
ENCUCI 2020 vs ENCIG 2025
→ transferencia de instrumento
→ P1

```

TRA-M-03:

```text
ENCIG 2013 vs ENCIG 2025
→ transferencia de ola
→ P1

```

TRA-M-07:

```text
ENCIG 2021 vs ENCIG 2025
→ transferencia de ola
→ P1

```

Si alguna devuelve P0:

```text
PARO

```

No sustituir por otra conducta.
13 · COMMIT 2
MARCO + REEMISIÓN
Segundo commit:

```text
m13: enlaza TRA a paga_mordida_encig2025 y reemite M v1.3

```

Incluye únicamente lo necesario:

```text
marco-M-sorteado-v1_3.tsv
3 JSON M-v1_3

```

más cualquier artefacto mecánico estrictamente exigido por el acto.
No agregar R/L.
14 · NOTA DE ALCANCE
La enmienda pedía insertar una nota en:

```text
enlace-M-v1_1.md

```

Ese archivo no existe en `main`.
No crear un v1.1 únicamente para alojar esa frase.
No editar retroactivamente `enlace-M-v1_0.md`, que documenta un enlace histórico anterior.
La sustancia debe quedar en:

1. `razon`/`razon_DD` de TRA-M-02 donde corresponda;
2. el `## CONSUMIDO` del encargo M13;
3. el scoreboard v1.3 si ayuda a interpretar la diferencia.

Conservar esta afirmación sustantiva:

```text
paga_mordida_encuci2020 (0.125822, MEDIDO, calibrada en ENCUCI 2020)
NO se usa para TRA-M-02 porque bajo F-DD sería P0 VERIFICACION.
M13 usa paga_mordida_encig2025 como enlace externo exacto.

```

15 · AGREGADO v1.3
Sólo DESPUÉS de sellar los tres JSON M y demostrar ceguera a R:
crear:

```text
forense/prereg-duelo-v2/agregado_v1_3.py

```

Principio
No copiar/reimplementar el agregado sellado.
Reutilizar el camino v1.2 en la mínima extensión posible.
Preferencia:

```text
agregado_v1_3
→ importa/reutiliza agregado_v1_2
→ cambia marco + resolución de M

```

No editar:

```text
agregado_v1_1.py
procedimiento-scoring-v1_1.md
scoring-adv1-m3.py

```

16 · RESOLUCIÓN M v1.3
Para cada celda, buscar en este orden:

```text
1. M-<id>__v1_3.json
2. M-<id>.json
3. M-<id>__v1_2.json

```

Primera coincidencia exacta.
No otra heurística.
Para las tres TRA debe usar:

```text
__v1_3

```

Para las demás debe reproducir las fuentes de v1.2.
Añadir al resultado:

```json
"fuente_M_por_celda": {
  "TRA-M-02": "corridas-M/M-TRA-M-02__v1_3.json",
  ...
}

```

Debe contener exactamente los 14 IDs del universo.
17 · INVARIANTE DE COMPARABILIDAD
v1.3 cambia UNA dimensión:

```text
M de TRA-M-02/03/07

```

Debe conservar:

```text
universo = 14
IDs = mismos 14
R = mismos archivos/valores
L = mismo L-extraido-v1_2.tsv
delta = mismo
nivel_ic = mismo
seed = mismo
replicas = mismas
F-DD = misma regla
procedimiento = mismo

```

No “limpiar” durante M13 nombres heredados o scope IDs de bootstrap si eso cambia la corriente de remuestreo.
Queremos comparar:

```text
v1.2 vs v1.3

```

con la misma mecánica y sólo el cambio M pre-registrado.
18 · RESULTADO
Ejecutar:

```bash
python3 forense/prereg-duelo-v2/agregado_v1_3.py

```

Crear:

```text
agregado-v1_3-resultado.json

```

No reproducir ni imponer antes las cifras orientativas de dirección.
Las notas del tipo:

```text
z ≈ ...

```

son expectativa no vinculante.
El primer resultado real del script gobierna.
19 · CONTROLES v1.2 → v1.3
Verificar mecánicamente:
A
Los 14 IDs son iguales.
B
R por celda es idéntico.
C
L por celda es idéntico.
D
M de las 11 celdas no afectadas es idéntico.
E
Sólo:

```text
TRA-M-02
TRA-M-03
TRA-M-07

```

cambian su fuente M y valor M.
F
`fuente_M_por_celda` prueba esa afirmación.
Si otra celda cambia:

```text
PARO

```

antes de interpretar el benchmark.
20 · SCOREBOARD v1.3
Crear:

```text
forense/prereg-duelo-v2/scoreboard-v1_3-AGREGADO.md

```

No editar ni borrar v1.2.
Debe declarar de forma prominente:

```text
mismo universo de 14
mismos R
mismos L
mismo procedimiento
único cambio sustantivo:
enlace y reemisión M para TRA-M-02/03/07

```

Reportar:

* resultados por celda;
* agregado M;
* L_SOLO;
* L_CORPUS;
* comparación principal;
* comparación secundaria;
* F-DD;
* fuentes M v1.3.

Sin interpretación causal nueva.
21 · BENCHMARK DE MOTORES
Actualizar:

```text
forense/benchmark/BENCHMARK-MOTORES-COMPARABLES.md

```

sólo después de disponer del resultado v1.3.
Actualizar las cifras que dependan del agregado.
Especialmente corregir cualquier texto que siga describiendo:

```text
TRA-M-* = 0.62

```

como estado actual del benchmark.
Conservar historia de v1.2.
No borrar el hallazgo que motivó M13.
Explicar:

```text
v1.2 reveló que TRA consumía el ASIGNADO histórico.
v1.3 re-enlaza esas tres celdas a la conducta medida preexistente.

```

No declarar victoria de M si el intervalo no la sostiene.
22 · TABLERO
M13 no toca:

```text
forense/tablero/TABLERO-PROGRAMA.md

```

El tablero tiene su propio acto `TABLERO-VIVO`.
Evitar conflicto de ramas y doble mantenimiento.
Si después del merge M13 el bloque derivado del tablero necesita refresco, se hace por el mecanismo de E6, no copiando cifras manualmente dentro de este acto.
23 · COMMIT 3
AGREGADO + LECTURA
Tercer commit sustantivo:

```text
m13: agrega M v1.3 y actualiza benchmark comparable

```

Incluye:

```text
agregado_v1_3.py
agregado-v1_3-resultado.json
scoreboard-v1_3-AGREGADO.md
BENCHMARK-MOTORES-COMPARABLES.md

```

No incluir ruido ajeno.
24 · PRUEBAS Y VERIFICACIÓN
Antes del cierre:
Resolver
Prueba dirigida de calibración por conducta.
Emisor
Regresión P2 histórica:

```text
PASA

```

Nuevos M
Tres JSON cumplen contrato exacto.
Marco

```text
14 IDs v1.2 == 14 IDs v1.3
11 filas no afectadas idénticas
3 filas con diff limitado a enlace y consecuencias mecánicas

```

Agregado
Dos ejecuciones:

```bash
python3 forense/prereg-duelo-v2/agregado_v1_3.py
sha256sum agregado-v1_3-resultado.json
python3 forense/prereg-duelo-v2/agregado_v1_3.py
sha256sum agregado-v1_3-resultado.json

```

mismo hash.
Baseline

```bash
python3 tests/check.py --baseline

```

sin regresión material nueva.
No `--freeze`.
Entrega
Después del último push:

```bash
python3 tools/verifica_head_remoto.py

```

debe devolver:

```text
PR_HEAD_SINCRONIZADO

```

25 · PARO MATERIAL
PARO si ocurre cualquiera:

1. `paga_mordida_encig2025` no existe exactamente en el motor.
2. Su valor ya no es `0.085118` y el cambio no está explicado por `main`.
3. Su clase no es `MEDIDO*`.
4. No puede resolverse unívocamente su `ola_calibracion`.
5. La regresión histórica P2 falla.
6. Alguno de los tres M nuevos queda P0.
7. Emitir requiere abrir R previamente.
8. El marco v1.3 cambia IDs, sorteo o universo.
9. Una de las 11 celdas no afectadas cambia.
10. R o L cambian entre agregado v1.2 y v1.3.
11. El resultado requiere modificar el procedimiento sellado.
12. Aparece necesidad de elegir una conducta según cuál mejora contra R.

No “resolver” un PARO ampliando automáticamente el perímetro.
Reportar la evidencia exacta.
26 · FUERA DE PERÍMETRO
No:

* reestimar microdatos;
* modificar `milpa/tramite.yaml`;
* modificar probabilidades;
* cambiar R;
* cambiar L;
* cambiar procedimiento scoring;
* cambiar delta;
* cambiar seed;
* cambiar réplicas;
* cambiar sorteo;
* añadir celdas;
* tocar CIV/FAM/DIN para “hacer variar M”;
* activar corredor E;
* cambiar tiers;
* optimizar benchmark;
* borrar resultados anteriores.

27 · PREGUNTA QUE ESTE ACTO SÍ RESPONDE
No:
¿cómo hacemos que M tenga más variedad?
Sí:
¿qué ocurre cuando las tres celdas TRA dejan de consumir una conducta ASIGNADA y consumen la conducta MEDIDA exacta que dirección decidió enlazar, manteniendo todo lo demás constante?
Eso convierte una medición ya existente en movimiento real del marcador.
28 · CRITERIO DE ÉXITO
Antes:

```text
regla contiene MEDIDO ENCIG2025
        ↓
marco apunta a paga_mordida
        ↓
emisor entrega 0.62 ASIGNADO
        ↓
agregado consume 0.62

```

Después:

```text
regla contiene MEDIDO ENCIG2025
        ↓
marco v1.3 apunta a paga_mordida_encig2025
        ↓
resolver usa calibración de ESA conducta
        ↓
emisor entrega 0.085118 MEDIDO
        ↓
M-v1.3 queda materializado
        ↓
agregado consume M-v1.3
        ↓
benchmark muestra el impacto real

```

29 · CIERRE
Aplicar la cascada vigente de `/acto`.
El `## CONSUMIDO` debe declarar:

1. SHA de `origin/main` de partida;
2. resolver de calibración corregido;
3. regresión histórica;
4. tres filas M re-enlazadas;
5. tres JSON v1.3;
6. fuente M por las 14 celdas;
7. comparación v1.2 → v1.3;
8. resultado real, sin sustituirlo por expectativa;
9. baseline;
10. HEAD remoto sincronizado;
11. reservas materiales si quedaron.

Abrir un solo PR.
NO fusionar.
Mesa fusiona.
REGLA DE PARADA
Una vez que:

```text
3 TRA usan el MEDIDO correcto
+
agregado v1.3 lo consume
+
benchmark registra el efecto

```

M13 termina.
No aprovechar el acto para corregir otros M repetidos.
La posible repetición de CIV/FAM se analiza después sólo si el resultado de M13 o una decisión de dirección demuestra que su enlace es materialmente incorrecto.
