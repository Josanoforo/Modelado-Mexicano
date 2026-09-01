# ACTO MAESTRA33-C8 · MEDIDOR-FP172-DIFERIDAS — cierre

`SHA de redacción: 5a905b3`. Encargo: `forense/encargos/2026-09-01-MAESTRA33-C8-MEDIDOR-FP172-DIFERIDAS.md`.

## Premisa del encargo, verificada contra el árbol (A.13)

El encargo (A.8) asume que existe una lista de mediciones **diferidas** —
prometidas por `FP-172` (`FIRMADA`, 30/ago/2026) sobre los 42 veredictos
`EXISTE-SATISFACE` de `data/cruce-inverso-v1_1.tsv`, con prioridad "pares
del motor" — y pide tomar las 4 primeras (`D-11`, lote ≤4) para medir en
`COMMIT-2`.

**La premisa no se sostiene contra el árbol real.** Comando:
`python3 tools/deriva_diferidas_fp172.py` (script nuevo de este acto,
`tools/deriva_diferidas_fp172.py`), que:

1. Toma las 42 filas `veredicto_a4=EXISTE-SATISFACE` de
   `data/cruce-inverso-v1_1.tsv`.
2. Parsea `milpa/procedencia.yaml` (1419 líneas) en bloques reales —
   acotados por la siguiente clave a indentación de 2 espacios, no por
   proximidad de línea cruda — y marca cada variable_id como `MEDIDO` si
   aparece dentro de un bloque cuya `clase:` contiene `MEDIDO`.
3. **Resultado bruto: 42/42 caen en algún bloque `MEDIDO`.** Dos de esos
   hits son falsos positivos del detector automático (mención dentro de
   prosa que la excluye explícitamente, no cita real de medición) —
   verificados leyendo el bloque completo a mano, no a ojo sobre el grep:
   - `AP7_1`: cae en el bloque `exposicion_violencia` (línea ~468-470),
     pero el propio texto dice *"colisión de nombre entre encuestas
     distintas, ya documentada, no es la AP7_1 de ENVIPE de este acto"* —
     el `AP7_1` de ENCUCI (trabajo voluntario/comunidad) es un
     mnemónico homónimo, no una medición.
   - `P4_10`: el hit en `familismo_apoyo` es solo una referencia cruzada
     ("...vía P4_10"); su propia entrada en
     `rutas_estimabilidad_coeficiente.detalle` (línea ~1121) la declara
     **SIN-RUTA / SUBDETERMINADA-PERSISTENTE**, bloqueada por decisión
     formal previa (`ACTO ESCALAS-COMPLETAS-P1`, 25/ago/2026) — no
     promovible sin reabrir esa decisión, que está fuera del perímetro
     de este acto.

**Con las dos excepciones aplicadas: 40 de 42 variables EXISTE-SATISFACE
ya tienen una medición real (β̂/θ, IC95%, n, universo) escrita en
`milpa/procedencia.yaml`** — ejecutadas por actos anteriores (CAL-CONF
Fase B ola 1/ola 2, `ACTO COND-ATRIB`, Encargo X, Encargo W1-P, Encargo
E/ENVIPE G4, `ACTO PROC-11`/`PROC-10-bis`, `ACTO PROD-P638`, entre
otros — trazables por `fuente:` de cada bloque). Las 2 restantes
(`AP7_1`, `P4_10`) **no son "diferidas y promovibles"**: una es un
defecto de etiqueta del cruce (colisión de mnemónico entre instrumentos,
no una variable real pendiente de medir) y la otra está formalmente
bloqueada por una decisión previa de mesa/acto que este encargo no tiene
mandato de reabrir.

**Conclusión: la cola diferida que `FP-172(i)` prometía está VACÍA.**
No porque no se haya trabajado — al contrario: entre el 30/ago (firma de
`FP-172`) y hoy (1/sep), una cadena de actos no coordinados con esta cola
(`COND-ATRIB` el más reciente, 30-31/ago) ya midió, uno por uno, todos
los candidatos `EXISTE-SATISFACE` que tenían ruta abierta. `FP-172(i)`
quedó desactualizada por el propio avance del programa, no por omisión.

## P1/P2 — sin ejecución

Con 0 candidatas elegibles, no hay `COMMIT-1` de "frase de sello" por
celda (no hay celda) ni `COMMIT-2` de estimación — no se abre ningún
microdato. `data/raw` se enlazó en el ARRANQUE de este acto
(`/home/pc0/mm-corpus/raw`) pero no se leyó ningún payload: cero
archivos de microdato abiertos, declarado (A.13). Este mismo archivo de
nota, junto con `tools/deriva_diferidas_fp172.py` y su salida, es la
"frase de sello" del hallazgo — declarado antes de cualquier intento de
abrir dato, porque no hay dato que abrir.

## P3 — cierre de FP-217

`FP-217` (deriva de `FP-179(3)`, vence `2026-09-07`) se cierra con este
hallazgo: **CONTADOR: θ medidas +0**, declarado y razonado — no un
`NO-ENCONTRADO` silencioso. Se corrige además el estado operativo de
`FP-172(i)`: la fila de mesa decía "la lista concreta la deriva del tsv
el encargo medidor cuando se redacte" — se derivó, por comando, y la
lista es de longitud 0 sobre candidatas promovibles.

**Qué queda fuera, con nombre, como sucesor `C8-b` (fecha propuesta:
`2026-09-14`, una semana después del vencimiento de `FP-217`):**
- `AP7_1` (ENCUCI, "trabajo voluntario/comunidad") — decisión pendiente
  de mesa: ¿vale la pena re-etiquetar el cruce para dejar de contar esta
  colisión de mnemónico como si fuera una variable EXISTE-SATISFACE
  "nueva"? Es un defecto de la receta de extracción de
  `data/cruce-inverso-v1_1.tsv`, no una medición pendiente.
- `P4_10` — decisión pendiente de mesa: ¿reabre alguien la
  SUBDETERMINACIÓN de `G4.horizonte_temporal` (`ACTO
  ESCALAS-COMPLETAS-P1`, Paso 2) para intentar una escala derivada
  distinta, o queda sellada como está? `C8-b` no mide nada por sí solo —
  solo puede proponer la reapertura, que corresponde a mesa.
- La orden de adquisición ENCUCI/ENIF/ENNViH-MxFLS (`FP-172(ii)`, ya en
  `FP-179(1)`/`(2)`, ambas ya `EJECUTADA`) no se toca — fuera del
  perímetro de C8.

Ninguna variable EXISTE-SATISFACE queda "volando" sin nombre: las 40 ya
medidas están listadas por el script (`medidas`), las 2 excluidas están
arriba con su razón.

## Perímetro respetado

Tocado: `milpa/procedencia.yaml` (sin escritura — cero θ nuevas, cero
diff), `tools/deriva_diferidas_fp172.py` (nuevo), esta nota,
`forense/firmas-pendientes.tsv` (FP-217), `forense/encargos/...` (A.3 +
`## CONSUMIDO`), cascada estándar. No se tocó `milpa/tramite.yaml`, el
marco-M, ni nada del duelo.
