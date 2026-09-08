<!-- TABLERO-DERIVADO:BEGIN -->
## Estado vivo derivado

- **Procedencia.** SHA `c55320b` · fecha del commit `2026-09-08` · ¿árbol == origin/main? `False`.
- **Motor.** reglas totales `21` · reglas con dato (>=1 conducta MEDIDO*) `20` · reglas sin dato `1` · conductas MEDIDO* `50` · tiers `{'FUERTE': 19, 'MEDIA': 2}`.
- **Corredor.** marco vigente `marco-M-v1_3` sorteado / `marco-M-v1_2` congelado (derivado del árbol) · celdas sorteadas `14` · celdas con M `14` · con R `14` · con L `14` · celdas puntuables (M∩R∩L) `14` · celdas sin cobertura completa `0`.
- **Corpus lógico.** entradas del manifiesto `1569` · filas de registro de curación `135` · filas de relaciones `228` · filas del inventario de reactivos v1.2 `178247`.
- **Gobernanza operativa.** ADR máximo `410` · FP máximo `357` · FP abiertas: FP-349, FP-350, FP-351, FP-352, FP-353, FP-354, FP-355, FP-356, FP-357 · encargos archivados `388` (consumidos `370`) · cola de encargos:
  - `2026-08-31-MAESTRA33-B2-MARCO-M-SORTEA-v1_1.md`: CONSUMIDO
  - `2026-09-01-MAESTRA34-L2-ARBITRA-v1_2.md`: CONSUMIDO
  - `2026-09-01-MAESTRA34-N2-MARCO-M-v1_2.md`: CONSUMIDO
  - `2026-09-01-MAESTRA34-N3-AGREGA-2.md`: LISTO
  - `2026-09-01-MAESTRA34-N5-RE-EVALUA-OLA6.md`: CONSUMIDO
  - `2026-09-02-MAESTRA35-L10-OLA6-SALUD-L1.md`: LISTO
  - `2026-09-07-ENCARGOS-GEN2-en-orden.md`: LISTO
  - `2026-09-07-GEN2-E1-LIMPIEZA-C1.md`: LISTO
  - `2026-09-07-GEN2-E2-C0-A-DEMANDA.md`: GATED
  - `2026-09-07-GEN2-E3-1-ENDURECE-CALC.md`: CONSUMIDO
  - `2026-09-07-GEN2-E3-AUTOMATIZA-GEN2-1.md`: CONSUMIDO
  - `2026-09-07-GEN2-E4-LIMPIEZA-C2-PODA.md`: GATED
  - `2026-09-07-GEN2-E5-0-SPECS-EJECUTABLES.md`: GATED
  - `2026-09-07-GEN2-E5-CALC-0001-0003.md`: GATED
  - `2026-09-07-GEN2-E6-AUTOMATIZA-GEN2-2.md`: CONSUMIDO
  - `2026-09-07-GEN2-E7-READINESS-2.md`: CONSUMIDO
  - `2026-09-08-MAESTRA34-E1-REVISION-FALSADORES.md`: CONSUMIDO
- **GEN2 (derivado de `corrida0 status`).** corridas selladas `0` / requeridas `86` · resultados sellados `0` / activos `205` · pendientes `205` · dependencias numéricas legacy activas `205` · validación independiente `0` · diferencias materiales `0` · NC- abiertas `25` · replays LEGACY-GEN1 sellados `2` (no cuentan). El `0 / N` es la lectura correcta: el aparato se construyó antes que las corridas.
- **GEN2 · medición vs. adopción (ACTO GEN2-PRE-E5 · P3).** sellados `0` · pendientes de adopción (citados en la propuesta, ningún consumidor activo aún) `0` · adoptados por un consumidor activo `0`. Sellar un RESULT no mueve `dependencias_numericas_legacy_activas` por sí solo: solo el consumidor activo que lo adopta la baja.
- **Fuentes.** `milpa/tramite.yaml`, `milpa/tramite-ola5-propuesta-v0.yaml`, `milpa/procedencia.yaml`, `forense/prereg-duelo-v2/` (marcos y corridas M/R/L), `data/manifiesto.yaml`, `data/curacion-registro/cola-adquisicion-registro.tsv`, `data/curacion-registro/relaciones.tsv`, `data/inventario-reactivos-v1_2.tsv`, `canon/gobernanza-v1_15.md`, `forense/firmas-pendientes.tsv`, `forense/encargos/*.md`, `forense/encargos/cola/*.md`.

**Protocolo vigente.** La actualización factual de este bloque se hace con:

```
git fetch origin
python3 tools/tablero_programa.py --actualiza
python3 tests/check.py --baseline
```

El humano solo actualiza la interpretación (las tablas curadas §2.1-2.5 y la narrativa) cuando hay una decisión o un hallazgo que valga la pena registrar. Las recetas antiguas del snapshot histórico (p. ej. `git branch -r` o `awk '$6=="ABIERTA"'`) NO gobiernan esta actualización -- son historia, no el mecanismo vigente.

<!-- TABLERO-DERIVADO:END -->

---

# TABLERO DEL PROGRAMA · Gen 2

**`d48014ed` (origin/main, merge PR #631, 8/sep/2026 13:52 −06:00) · derivado el 8/sep/2026.**

**Este tablero se reconstruyó desde cero para Gen 2.** No traza el origen de los datos de Gen 1 y no lo hará: por E.1 esos valores son historia, no autoridad, y auditarlos hacia atrás sería exactamente el trabajo que la generación nueva existe para no repetir. Lo de Gen 1 que sobrevive aquí está en el **Anexo**, en dos párrafos, como comentario y no como fuente. Los siete contadores que gobernaron los snapshots v1.0 a v1.7 **ya no son la señal** y no vuelven a aparecer.

> Vista derivada, no canon. Instrucciones vigentes **v2.13**. El bloque de arriba lo escribe `tools/tablero_programa.py --actualiza` y describe el árbol clásico; **la señal de Gen 2 es la de §2**, derivada de `tools/corrida0.py status` (E.4: la dice el mecanismo, nunca una persona).

**Estampa de universo (A.10).** Clon nuevo, de cero. `origin/main = HEAD = d48014ed`, árbol limpio. Firma de entorno (A.2), tres partes: `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` = **`sin_variable`** · `inegi.org.mx` → **403** · `data/raw` → **AUSENTE**. **Tercera parte no cumplida: sin corpus** — ninguna corrida GEN2 es ejecutable desde aquí y ningún hash se re-mide (A.1). Espejo del proyecto: no leído. Universo: el árbol de `d48014ed` salvo `.git` y `data/raw`.

---

## 1 · La frontera de generación, derivada

| hecho | valor | comando |
|---|---|---|
| **Gen 1 cierra** | `03bcd6f6` · 7/sep/2026 01:29 · merge **PR #597** | `git log -1 03bcd6f6` |
| **Gen 2 abre** | **PR #600** (`gen2-e2-demanda-derivation`) · 7/sep/2026 **15:09** | `git log --merges --grep='#600'` |
| entre una y otra | 13 h 40 min · dos PR de trámite (#598, #599) que no son de generación | |
| actos GEN2 fusionados desde el corte | **13 de 32 PR** | `git log --merges 03bcd6f6..HEAD \| grep -ci gen2` |

**Todo lo anterior a `03bcd6f6` es LEGACY-GEN1 y no se audita.** Todo lo posterior a PR #600 nace bajo la cadena de E.2.

---

## 2 · La señal — la cadena de procedencia

**Las cifras vivas son las del bloque derivado de arriba, que `--actualiza` refresca. Lo de abajo es la lectura al corte, fechada.**

Íntegra de `python3 tools/corrida0.py status` **al 8/sep, `d48014ed`**. Ninguna cifra tecleada. Si el bloque de arriba y esta tabla discrepan, manda el bloque: se deriva en cada corrida y esta se fecha.

| contador | valor | qué dice |
|---|---|---|
| **`N_resultados_activos`** | **205** | los números que la simulación consume hoy |
| **`N_resultados_sellados`** | **0** | ninguno tiene cadena de procedencia GEN2 |
| **`dependencias_numericas_legacy_activas`** | **205** | el 100% sigue siendo GEN1 |
| **`N_corridas_requeridas`** | **86** | la demanda, derivada hacia atrás desde los consumidores activos |
| **`N_corridas_selladas`** | **0** | |
| `N_resultados_gen2_sellados` | 0 | |
| `N_resultados_gen2_pendientes_adopcion` · `_adoptados_activos` | 0 · 0 | nada esperando merge de mesa, nada adoptado |
| `resultados_con_validacion_independiente` | 0 | el segundo eje de E.2, sin ejercer |
| `diferencias_materiales` | 0 | no hay valor GEN2 contra el que comparar |
| `no_corrido_abiertas` | **25** | deuda declarada, §5 (era 22 antes de fusionar el PR #631) |
| `replays_legacy_sellados` | 2 | **no cuentan** (`cuenta_gen2 = NO`) |
| `corredores_envueltos_legacy` | 8 | envoltura, no medición nueva |

**Un matiz que el bloque vivo aporta y conviene no perder:** sellar un `RESULT` **no baja por sí solo** `dependencias_numericas_legacy_activas`. Solo la baja el consumidor activo que lo adopta. Es decir, los 205 no caen cuando se mida: caen cuando mesa adopte.

**Gen 2 arranca en cero y el cero es correcto.** Es la primera vez que el programa sabe, con comando, cuántos de sus números carecen de procedencia verificable. Ese contador se moverá o no se moverá a la vista, y es lo único que cuenta como avance en esta generación.

---

## 3 · El registro — de dónde sale el cero

| registro | filas | reparto |
|---|---|---|
| `corridas.tsv` | 96 | `DEMANDA` **86** / `OFERTA` 10 · estado `PENDIENTE` **86**, `SELLADA` 6, `SUPERADO→…` 4 · generación `GEN2-PENDIENTE` **86**, `GEN2` 8, `LEGACY-GEN1` 2 |
| `resultados.tsv` | 390 | `DEMANDA` **205** / `OFERTA` 185 · estado `PENDIENTE` **205**, `SELLADA` 122, `SUPERADO→…` 63 · generación `GEN2-PENDIENTE` **205**, `GEN2` 167, `LEGACY-GEN1` 18 |
| `usos.tsv` | 205 | **`activo = SI` en las 205**; un consumidor activo por resultado |
| también en disco | | `demanda-corridas.tsv`, `demanda-resultados.tsv`, `decisiones.tsv` · **13 carpetas `CALC-*` con su `spec.yaml`** |

**Las 122 filas `SELLADA` de `resultados.tsv` no entran al contador**: son oferta de aparato —smoke, replays, envolturas— con `cuenta_gen2 = NO`. E.4 lo manda y el mecanismo lo cumple. Es el aparato negándose a inflar su propio marcador, y es la prueba más limpia de que funciona.

**Qué consumen esos 205 resultados**, por `tipo_uso`: 50 `conducta_p_medido` · 28 `celda_L` · 22 `momento` · 14 `conducta_p_asignado` · 14 `celda_R` · 14 `celda_M` · 14 `celda_AGREGADO` · 13 `asignado_probabilidad` · 12 `condicional_theta` · 8 `coeficiente_asignado` · 7 `coeficiente_ejecutable` · 6 `corte_pi` · 3 `celda_D`.

---

## 4 · El aparato, pieza por pieza

| pieza | estado |
|---|---|
| `corrida0.py` · `demanda` `spec-check` `negativo` `preflight` `run` `verify` `registro` `status` `estado` | **en el árbol y ejercidos** |
| `corrida0.py vigencia` · `delta` | **`[NO-IMPLEMENTADO]`**, declarado en el propio `--help` |
| `entorno.py` · `limpia_arbol.py` · `cierre_acto.py` | en el árbol |
| `forense/no-corrido.tsv` + plantilla de PR (A.14) | en el árbol, 43 filas |
| Plan CORRIDA-0 | `forense/notas/PLAN-FINAL-GEN2-v2_0-2026-09-07.md` **con `.sha256`** |
| Instrucciones v2.13 | en el árbol |
| suite | **3 FAIL · 203 WARN · LÍNEA BASE VERDE** (`dee5fc5`) |
| **los seis checks del GO (E.5)** | **NO-DERIVABLE** — `preflight` responde por `calc_id`; no hay artefacto que los reporte juntos. Universo: `grep` de los seis nombres sobre el plan, `ls` de `forense/notas/*READINESS*` y `*GO*` |

---

## 5 · Deuda declarada — el mecanismo de A.14 funcionando

**22 filas ABIERTA de 43** (21 cerradas), **todas del 8/sep**, **las 22 con sucesor nombrado, ninguna `SIN-ASIGNAR`**.

| razón | abiertas | lectura |
|---|---|---|
| `NO-VERIFICABLE-AQUI` | **7** | entorno sin corpus ni red: no es defecto, es la firma A.2 haciendo su trabajo |
| `FUERA-DE-PERIMETRO` | **5** | el ejecutor se detuvo en el borde en vez de invadirlo |
| `DECISION-DE-MESA-PENDIENTE` | **4** | lo único que necesita a mesa |
| `DIFERIDO-A:C0-D` · `C0-B` · `mesa` | 2 · 1 · 1 | sucesión declarada |
| `PARO-PREMISA` | 1 | una premisa que no se sostuvo contra el árbol |
| `CONTADOR-CERO-DECLARADO` | 1 | un encargo que declaró readiness y no corrida, y lo dijo |

**Esto es lo que A.14 vino a hacer visible.** Antes, siete piezas no ejecutables por entorno y cinco frenadas en el borde del perímetro se habrían perdido en la salida de una conversación. Hoy tienen fila, razón, impacto y sucesor.

**Firmas.** 4 ABIERTA: FP-349, FP-350, FP-351, FP-352, todas del 8/sep. **Ramas.** 1 viva (`acto/gen2-e5-calc-0001-0003`) contra una política de cero; `limpia_arbol.py --reporta` deja el punto D en `NO-VERIFICABLE-SIN-GH` en este entorno.

---

## 6 · Bloqueadores

| id | qué bloquea | dueño | cómo se cierra |
|---|---|---|---|
| **G1** | **El GO de E.5 no es derivable.** E.5 prohíbe lanzar corrida real hasta que los seis checks pasen en `origin/main`, y hoy «podemos lanzar» sería juicio, no derivación | dirección | un `corrida0.py go` o un readiness commiteado |
| **G2** | **`vigencia` y `delta` sin implementar.** E.1 exige que la comparación contra GEN1 se calcule por script y después de medir; hoy no hay herramienta que lo haga | dirección | implementarlos antes de la primera adopción |
| **G3** | **Cuatro filas `DECISION-DE-MESA-PENDIENTE`** en la deuda declarada | mesa | resolver por fila |
| **G4** | **Una rama viva contra la política de cero**, y el verificador no puede comprobar el punto D sin `gh` | mesa | fusionar o borrar; instalar `gh` donde corra el reporte |
| **G5** | **Cuatro firmas ABIERTA** (FP-349 a FP-352) | mesa | firma por fila |

---

## 7 · Discrepancias del propio tablero

| # | qué | estado |
|---|---|---|
| **G-D1** | **CERRADA.** `status` decía «99 corridas» contra 96 filas del TSV. Hoy, con el PR #631 fusionado, **coinciden: 99 y 99**. Dirección lo atribuye a que el 99 era la nota de la rama; esa explicación no cubre que yo lo medí sobre `main`, pero el hecho es que **ya no reproduce** y se cierra por eso | cerrada |
| **G-D2** | La línea base de la suite se recongeló (`accf688` → `dee5fc5`) y los WARN pasaron de 170 a 203. El VERDE es válido; **la serie de WARN no cruza el recongelamiento** | anotar |
| **G-D3** | **RETIRADA — era mía, no del repo.** Afirmé que el bloque vivo describía solo el árbol clásico; el bloque **sí** trae dos líneas `GEN2 (derivado de corrida0 status)`, en el generado y en el commiteado. `tablero_programa.py` importa `corrida0` y lo declara como única fuente. La afirmación salió de un `grep` mío sobre los encabezados en negrita que excluía paréntesis: **un negativo producido por un comando que no examinó lo que decía examinar** (A.13) | corregida aquí |
| **G-D4** | **NUEVA · El cuerpo curado del tablero commiteado sigue siendo v1.1, del 2/sep.** El bloque vivo está al día porque lo regenera `--actualiza`, pero la capa que lo rodea describe el árbol de hace seis días. Verificado: `grep` de `v1_4`, `v1_7`, `v2_0`, `Snapshot v1.7` y `Gen 2` sobre los 3 archivos de `forense/tablero/` → sin resultados | es el ajuste principal, §9 |

*(Las discrepancias D2–D18 de los snapshots de Gen 1 quedan cerradas por corte de generación: describían instrumentación de una capa que ya no es la señal. No se arrastran.)*

---

## 8 · Bitácora de Gen 2

| snapshot | SHA | fecha | señal | qué cambió |
|---|---|---|---|---|
| v2.0 | `fbce146d` | 8/sep 12:37 | 0 de 205 sellados · 0 de 86 corridas | primer tablero de Gen 2; señal migrada a `corrida0 status` |
| v2.1 | `e36c66dc` | 8/sep 13:23 | **0 de 205 · 0 de 86 · 205 dependencias legacy** | **tablero reconstruido desde cero.** Frontera de generación derivada (PR #597 cierra, PR #600 abre). Gen 1 sale del tablero y queda en el Anexo. Bloqueadores renumerados a la serie `G`. Un PR fusionado (#630) sin efecto en la señal |

**El contador no se movió entre v2.0 y v2.1, y no debía**: la ventana fue de un solo PR de trámite. Lo que cambió es qué mide este tablero.

---

## Anexo · LEGACY-GEN1, en dos párrafos

**Qué fue.** Del 29/jul al 7/sep/2026: 40 días, 2 915 commits, 588 PR, 388 ADR. Dejó un motor con 21 reglas y 50 conductas medidas, un corpus de 1 568 payloads con hash, un corredor de 14 celdas con las tres corridas completas y cuatro scoreboards agregados, 48 entradas de acumulador con 38 selladas y ninguna pendiente, 31 reports temáticos y 6 validaciones forenses. Cerró sin deuda de firma.

**Qué se hace con eso.** Nada hacia atrás. Por E.1 esos valores quedan íntegros, no se reescriben, no se declaran falsos, y **no son fuente numérica de GEN2**: no eligen variable, filtro, ponderador, transformación ni alternativa de ninguna corrida nueva. Pueden citarse como referencia histórica o prior conceptual, siempre rotulados. La comparación contra ellos se calcula **después** de medir y por script — y esa herramienta (`delta`) todavía no existe, que es el bloqueador G2. Lo que Gen 1 dejó abierto y Gen 2 puede o no heredar —`coercitivo` sin fuente, el duelo sin adjudicar, Ola 6 sin abrir— es decisión de mesa, no herencia automática.

---

## 9 · Ajustes pendientes en el repo, referentes al tablero

Derivados en esta sesión contra `d48014ed`. Ninguno lo puedo aplicar: este puesto no tiene escritura.

| # | ajuste | evidencia | tamaño |
|---|---|---|---|
| **A1** | **Reemplazar el cuerpo curado de `forense/tablero/TABLERO-PROGRAMA.md`** por el reconstruido de Gen 2, conservando intactos los dos marcadores de apertura y cierre del bloque derivado (si faltan, `--actualiza` se niega) | el cuerpo actual es v1.1, `9cbd8d8`, 2/sep (G-D4) | un PR de trámite |
| **A2** | **Actualizar `tools/tablero_vista.py`**: el del repo (201 líneas) no localiza secciones por título, no tolera cambios de formato y no conoce Gen 2; contra el tablero reconstruido produce una página degradada | mi versión, 555 líneas, con el héroe de la cadena de procedencia | reemplazo de archivo |
| **A3** | **Retirar o derivar `dominios_activos`** (`tools/tablero_programa.py:224`): es la constante `4` con la nota «Ola 6 NO abierta» incrustada. En Gen 2 es un indicador legacy que puede mentir sin avisar | `grep -n dominios_activos` | una línea |
| **A4** | **Normalizar la columna de estado de la cola de adquisición antes de contar**: tres filas traen el id pegado (`SUPERADA-POR REL-2fa1c0…`) y se cuentan como estados distintos | `cola_adquisicion_estados` | una línea |
| **A5** | **Contar tiers por entrada y no por línea**: 49 líneas `tier:` sobre 48 entradas. La entrada `tramite.mordida.con_registro_encig2025` tiene dos, una con indentación 6 | `re.findall(r'^(\s+)tier: ')` → `{4: 48, 6: 1}` | marginal; capa legacy |
| **A6** | **Anotar en `TABLERO-PROGRAMA-v1_1.md` que su contenido ya vive en el canónico**, para que nadie lo lea como una versión aparte | el canónico y él tienen el mismo cuerpo | una línea |

**Lo que NO hace falta tocar, verificado y en contra de lo que yo mismo escribí antes:** el bloque vivo ya lee `corrida0 status`, y `tablero_programa.py` lo declara como única fuente, sin recalcular por su cuenta. Eso está bien hecho.
