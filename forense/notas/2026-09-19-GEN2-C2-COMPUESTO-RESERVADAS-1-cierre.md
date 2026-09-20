# ACTO GEN2-C2-COMPUESTO-RESERVADAS-1 — nota de cierre

19/sep/2026 · base `8e455bd6` · NUBE · cero microdato
Encargo (A.3): `forense/encargos/2026-09-19-GEN2-C2-COMPUESTO-RESERVADAS-1.md`
Spec congelada: `forense/prereg-caja/C2-COMPUESTO-RESERVADAS-spec-v1_0.md`

---

## 1 · Qué ganó el motor, derivado

**Nada adoptado. 206 celdas disponibles para exploración, ninguna en uso.**

| cifra | valor | de dónde sale |
|---|---|---|
| pares `RESERVADA` examinados | 22 | `RESULT-C2COMP-N-PARES-RESERVADA-EXAMINADOS` |
| filas dictaminadas (par × desenlace) | 36 | `RESULT-C2COMP-N-FILAS-DICTAMEN` |
| filas `EMITIBLE` | 25 | `RESULT-C2COMP-N-FILAS-EMITIBLES` |
| filas `NO-EMITIBLE` | 11 | `RESULT-C2COMP-N-FILAS-NO-EMITIBLES` |
| pares emitibles en **al menos** un desenlace | 16 de 22 | `RESULT-C2COMP-N-PARES-EMITIBLES` |
| pares emitibles en **ningún** desenlace | 6 de 22 | `RESULT-C2COMP-N-PARES-NO-EMITIBLES-EN-NINGUN-DESENLACE` |
| celdas emitidas | 206 | `RESULT-C2COMP-N-CELDAS-EMITIDAS` |
| celdas **con IC** | **0** | `RESULT-C2COMP-N-CELDAS-CON-IC` |
| celdas **adoptadas** por este acto | **0** | `adoptados_activos` 46 → 46 (delta 0) |
| grupos `EMITIDA-SIN-EVALUAR` en el marcador | 16 de 22 | `marcador-segmento.tsv`, columna `emision` |
| grupos que siguen `RESERVADA` | **22 de 22** | mismo TSV, columna `estado` — emitir no consume |

Las 206 nacen `EMITIDA-SIN-EVALUAR`. **Lo que el motor ganó es cobertura de
exploración, no estimación.** Una emisión no pasa a adoptada por uso: sólo
por piloto fuera de muestra o por firma de mesa con alcance declarado.

## 2 · Afirmación → comando

Ninguna cifra de esta nota se tecleó a mano; cada una sale del comando de
su fila.

| afirmación | comando |
|---|---|
| La compuerta **no** había fusionado al abrir | `git grep -l -i "MARCADOR-PISOS-ENLACE" origin/main` → 0 de 5 769 · `git ls-remote --heads origin \| grep -ci "PISOS-ENLACE"` → 0 de 7 ramas · PR abiertos (MCP GitHub, `state=open`) → 0 de 4 |
| La compuerta **sí** fusionó durante el acto, verificada **por producto** | `git diff --stat 8e455bd6 origin/main -- tools/marcador_segmento.py` → 559 líneas cambiadas (no por `grep` del rótulo: `ADR-277` midió un falso positivo con ese comando) |
| 16 grupos `EMITIDA-SIN-EVALUAR` **y** los 22 siguen `RESERVADA` | `awk -F'\t' 'NR>2{print $9"\t"$10}' data/corrida0/marcador-segmento.tsv \| sort \| uniq -c` → `16 RESERVADA+EMITIDA-SIN-EVALUAR`, `6 RESERVADA`, y 22 `RESERVADA` en total |
| Los dos espacios de id no se tocan | `set(celdas) & set(emitidas_sin_evaluar)` → `set()` (20 adoptadas vs 206 emitidas) |
| La guardia D-14 **se puede disparar** | dos mutantes inyectados en `milpa/src/estimadores_segmento.py` (la vía por defecto devolviendo emitidas; una emitida rotulada `ADOPTADO-POR-FIRMA`) → `FAILED (failures=1)` cada uno; restaurado → `Ran 30 tests … OK` |
| El careo que la firma cita como adjunto no está en el árbol | `git ls-tree -r --name-only HEAD \| grep -ic "CAREO-PILOTO"` → 0 de 5 769 |
| `EMITIDA-SIN-EVALUAR` / `C2-COMPUESTO` no existían antes | `git grep -l -E "EMITIDA-SIN-EVALUAR\|C2-COMPUESTO" 8e455bd6` → 0 de 5 769 |
| 22 `RESERVADA` + 1 `CONSUMIDA-SIN-PILOTO` en el marcador | `awk -F'\t' 'NR>2{print $9}' data/corrida0/marcador-segmento.tsv \| sort \| uniq -c` |
| 25 `EMITIBLE` / 11 `NO-EMITIBLE`, 206 celdas | `python3 tools/c2_compuesto.py dictamen` |
| 206 emisiones, cero IC | `python3 tools/c2_compuesto.py emisiones` |
| El CALC reproduce su propio sello | `python3 tools/corrida0.py verify CALC-C2-COMPUESTO-RESERVADAS-0001` → `VERIFY: REPRODUCE (CONTEXTO=IDENTICO · RESULTADO=REPRODUCE)` |
| El procedimiento reproduce **el C2 ya sellado** | `RESULT-C2COMP-CONTROL-ARBITRO = REPRODUCE`, `…-CONTROL-DELTA-MAX-ABS = 0.0`, `…-CONTROL-N-CELDAS = 8` |
| `T-RESERVA` sigue verde | `python3 tests/test_marcador_segmento.py` → `PASA -- 6 casos` |
| `adoptados_activos` no se movió **por este acto** | `python3 tools/corrida0.py status` sobre el mismo `HEAD` de merge, con `git stash` y sin él → **46** en ambos (delta 0). El **36 → 46** lo produjo `PR #883`, medido en `8e455bd6` (36) y en `origin/main` = `51d53f2a` (46) |
| La spec pasa el contrato del registro | `python3 tools/corrida0.py spec-check CALC-C2-COMPUESTO-RESERVADAS-0001` → `0 OK · 0 FAIL · 317 718 filas examinadas` |
| Las guardias del acto corren | `python3 tests/test_c2_compuesto.py` → `Ran 22 tests … OK` (cableado como `T32-ter T-C2-COMPUESTO`) |

## 3 · Por qué 6 pares no se emitieron

* **5 pares de ENIF** (todos los que incluyen `formalidad`) — A-bis 4: el
  eje tiene `cobertura: 0.689676` y `universo_restringido: true`; vive en
  el universo de quien trabaja y no reconcilia contra el marginal
  poblacional ni contra el nacional. Como ENIF tiene dos desenlaces, son
  **10 de las 11 filas** `NO-EMITIBLE`.
* **1 par de ENUT** (`reparto_hogar × sexo_edad`) — `reparto_hogar` es un
  estimador de **razón** sobre 29 181 hogares (`FAC_HOG`); `sexo_edad` una
  **media de horas/semana** sobre 74 053 personas 12+ (`FAC_PER`), con
  valores hasta 28.31 donde el logit no existe. Sin desenlace binario
  común, sin nacional, distinta unidad, distinto universo, distinto
  ponderador — y `sexo_edad` ya es un eje compuesto. Cinco causas
  independientes; el dictamen reporta la primera.

Los tres casos que dirección nombró se cumplieron sin forzarse. El
tercero (`p = 0` o `1`) no se materializó: **ningún** marginal de los 22
pares cae ahí, verificado celda por celda.

## 4 · Tres hallazgos que no se resolvieron en silencio

1. **La unidad la pone el árbitro, no el marcador** — *resuelto aguas
   arriba*. Cuando se detectó (base `8e455bd6`), el marcador escribía
   `unidad_dato = persona` para ENCIG mientras el árbitro declaraba
   `TRÁMITE`; la emisión heredó la del árbitro y el dictamen conservó
   **las dos columnas** en vez de elegir por su cuenta. `PR #883` corrigió
   `_unidad_dato()` para leer el `payload`, y el marcador ya publica
   `tramite`/`delito`. El caso del test **no se borró** al desaparecer la
   discrepancia: lo que fija es **de quién** se hereda la unidad, y eso
   vale igual ahora que coinciden.
2. **El par no se parte por la primera `x`.** `escolaridad_proxyxsexo`
   tiene una `x` adentro del nombre del eje; partirlo por el separador da
   (`escolaridad_pro`, `yxsexo`) y **pierde el par entero** — un par
   emitible de 8 celdas de ENVIPE. Se parte contra los nombres de eje que
   la regla declara. Caso pinado en `tests/test_c2_compuesto.py`.
3. **`cuenta_gen2` lo bajó la máquina, no el ejecutor.** La spec
   **propone** `SI`, como el encargo pide; el registro aplica la regla E.1
   (`ACTO GEN2-T9`, D-1) y lo deja en `NO` con motivo mecánico: el input
   `IN-MOTOR-NACIONALES = milpa/tramite.yaml` es legacy GEN1. No se forzó
   ni se quitó el input: pinar la procedencia de los cuatro nacionales
   vale más que un contador. Queda a mesa, con fila `NC`.

## 5 · P3, que empezó diferida y terminó corrida

La compuerta no había fusionado al abrir, así que P1 y P2 corrieron sin
tocar `tools/marcador_segmento.py`. Fusionó como **`PR #883`** mientras
este acto corría: se verificó **por producto** (559 líneas cambiadas en
ese archivo entre `8e455bd6` y `origin/main`), se trajo a la rama y P3 se
ejecutó completa.

* **Emitir no consume, y se ve en el archivo.** `emision` es **columna
  propia**, nunca un valor dentro de `estado`: 16 grupos son
  `RESERVADA` **y** `EMITIDA-SIN-EVALUAR` a la vez, y los **22** siguen
  `RESERVADA`.
* **La separación es estructural, no una bandera.** Las 206 emisiones
  viven en clave aparte del YAML (`emitidas_sin_evaluar`) y con espacio
  de ids propio (`CRUCE-EMITIDA::…`), con **cero solape** contra las 20
  adoptadas — ni un merge de diccionarios mal escrito podría aliasar un
  id adoptado.
* **El lector no puede filtrar por accidente.** `estimador_de_celda(...)`
  devuelve sólo adoptadas; las emitidas salen **únicamente** con
  `incluir_no_evaluadas=True`, y la respuesta **siempre** trae `estado`,
  fijado en el lector y **no heredado del YAML** — un YAML mal derivado no
  puede hacer pasar una emisión por adoptada.
* **La guardia D-14 se verificó por mutación**, porque una guardia que no
  se puede disparar no es guardia: los dos defectos que existe para
  atrapar la hacen fallar, y el original pasa.
* **De paso**: el lector reparseaba el YAML entero en cada llamada (20 →
  226 entradas al incorporar las emisiones). Caché por `(ruta, mtime_ns,
  tamaño)`, que una re-derivación invalida: de más de dos minutos a 3.4 s.

**Sigue sin hacer**: no abrió microdato (`data/raw` ausente, no se pidió)
· no derivó ni miró `R` de ningún cruce · **no adoptó** · no propagó IC ·
no evaluó C2 · no eligió el cruce del piloto 3.

## 6 · Auditoría

Un C2 compuesto **supone** que no hay interacción entre los dos ejes en
escala logit; **no lo mide**. Donde la interacción sea real — edad ×
escolaridad en gobierno digital, brecha de acceso por cohorte — la
emisión estará **sesgada hacia el centro precisamente en las celdas más
vulnerables**: mayores con baja escolaridad, localidades chicas sin
cuenta. Es donde un lector aplicado más se equivocaría, y por eso cada
emisión lleva `supuesto: sin-interaccion` encima. Rótulo prohibido:
`independencia`.

Los ejes son **marcadores de estructura** (ingreso, formalidad, oferta
institucional), **no rasgos culturales**. La rejilla **no ve región ni
condición indígena**: límite declarado, no omisión.

Clase de evidencia **(a)**. Escala **proporción**; unidad por fila;
**ningún número cruza unidad**.

**Lectura peligrosa por simple:** *"el motor ya estima todos los
segmentos"*. Estima **bajo un supuesto** que dos pilotos no refutaron y
que **ninguno ha probado en estos cruces** — y sólo en 16 de 22 pares,
con cero intervalos de confianza y en un estado que el motor,
deliberadamente, no puede confundir con adopción.
