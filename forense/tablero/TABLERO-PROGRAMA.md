<!-- TABLERO-DERIVADO:BEGIN -->
## Estado vivo derivado

- **Procedencia.** SHA `b7164889` · fecha del commit `2026-09-19` · ¿árbol == origin/main? `True`.
- **Motor.** reglas totales `22` · reglas con dato (>=1 conducta MEDIDO*) `21` · reglas sin dato `1` · conductas MEDIDO* `46` · tiers `{'FUERTE': 20, 'MEDIA': 2}`.
- **Marcador por segmento.** filas por estado: ADOPTADO-POR-FIRMA `20` · CONSUMIDA-SIN-PILOTO `1` · DIAGNOSTICO `8` · IDENTICO `89` · RESERVADA `22` · SIN-PISO `21` · SOLO-PISO `53` (total `214`) · cobertura de piso `73 / 214` · valor añadido / evaluadas `0 / 20` · celdas `emision = EMITIDA-SIN-EVALUAR` `16 / 214` · `veto_pisos_activo` `True`.
- **Corridas selladas que no cuentan todavía.** por `cuenta_gen2`: `NO` 13 · `NO-DERIVACION-CONTEXTUAL` 1 · `NO-SIN-FIRMA-DE-OBJETO` 1 · `PENDIENTE-DE-CASCADA-DIFERIDA` 2 · `PENDIENTE-DE-INTEGRACION-SERIAL` 2 · `PENDIENTE-DE-MESA` 17 · `SI` 78 (selladas total `114`) · `PENDIENTE-DE-MESA`:
  - `CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0001--39bf1af3cdac`: `REPRODUCE`
  - `CALC-EDER2017-PRIMERA-UNION-SEXO-COHORTE-0002--18e3c08247d5`: `NO-VERIFICADO`
  - `CALC-ENADID2023-UNION-SEXO-EDAD-0004--28ecceb6d292`: `REPRODUCE`
  - `CALC-ENCRIGE-CARGA-INTENSIDAD-0001--55259dbe975f`: `REPRODUCE`
  - `CALC-ENCRIGE-CORRUPCION-DESCRIPTIVA-0001--4cbeaa28dc49`: `REPRODUCE`
  - `CALC-ENFIH2019-COBERTURA-SALDOS-CATPOS-0001--f22dc8014aec`: `NO-VERIFICADO`
  - `CALC-ENFIH2019-COBERTURA-SALDOS-CATPOS-0002--cd853c64a584`: `NO-VERIFICADO`
  - `CALC-ENIGH2022-REMESAS-CONTEXTO-0001--b7eeb4840ff2`: `REPRODUCE`
  - `CALC-ENSAFI2023-ESTRATEGIAS-CONJUNTAS-0001-v1_1--b76b950ff9df`: `REPRODUCE`
  - `CALC-ENUT2024-DISTRIBUCION-HORAS-0002--66a1f09471c3`: `REPRODUCE`
  - `CALC-ENVIPE-RES0028-U4-DERIVADO-0001--65d0408e0b71`: `REPRODUCE`
  - `CALC-ISSP2017-CONSISTENCIA-APOYO-FAMILIAR-0001--3f8b5bc3bc29`: `REPRODUCE`
  - `CALC-ISSP2017-REDES-APOYO-COTIDIANO-0001--b6365529136d`: `REPRODUCE`
  - `CALC-PISOS-ENIF2021-FORMALIDAD-0001--977c5ddae965`: `REPRODUCE`
  - `CALC-WBES2023-CORRUPCION-DESCRIPTIVA-0001--b87ec1bf2ad5`: `REPRODUCE`
  - `CALC-WBES2023-PRECISION-0001--7ab4bf6255e0`: `REPRODUCE`
  - `CALC-WBES2023-PRECISION-INTERACCIONES-0001--7f2a0899f700`: `NO-VERIFICADO`
- **Ramas presentes en origin.** **2 rama(s) presente(s) en origin (política de cero)**:
  - `acto/gen2-limpieza-ramas-locales-2`: 7 delante / 18 detrás de main · último commit `2026-09-19`
  - `claude/vigilant-ritchie-7zuufs`: 6 delante / 7 detrás de main · último commit `2026-09-20`
- **Corredor LEGACY (eje x = ∅, GO-MARCADOR).** el marcador por segmento es la línea de arriba. marco vigente `marco-M-v1_3` sorteado / `marco-M-v1_2` congelado (derivado del árbol) · celdas sorteadas `14` · celdas con M `14` · con R `14` · con L `14` · celdas puntuables (M∩R∩L) `14` · celdas sin cobertura completa `0`.
- **Corpus lógico.** entradas del manifiesto `1629` · filas de registro de curación `155` · filas de relaciones `231` · filas del inventario de reactivos v1.2 `178247`.
- **Gobernanza operativa.** ADR máximo `561` · FP máximo `397` · FP abiertas: FP-386, FP-387, FP-388, FP-393, FP-394, FP-395, FP-396, FP-397 · encargos archivados `572` (consumidos `521`) · instrucciones vigentes `v2.14` · cola de encargos (solo estados != CONSUMIDO; consumidos `36`):
  - `2026-09-07-ENCARGOS-GEN2-en-orden.md`: GATED
  - `2026-09-08-GEN2-SONDA-3-PILOTO-CAJA.md`: LISTO
  - `2026-09-10-GEN2-POST-685/00-LEEME-LANZAMIENTO-POST-685.md`: GATED
  - `2026-09-10-GEN2-POST-685/07-GEN2-SONDA-CRON-PRODUCCION.md`: GATED
  - `2026-09-11-GEN2-F5-DOCUMENTAL-EJECUCION-PENDIENTE.md`: GATED
  - `2026-09-11-GEN2-POST-693/00-LEEME-LANZAMIENTO-POST693.md`: GATED
  - `2026-09-11-GEN2-POST-693/10-GEN2-ENVIPE-VALIDACION-Y-LECTURA.md`: GATED
  - `2026-09-11-GEN2-POST-693/11-GEN2-CORRUPCION-UNIDAD-Y-FUENTE-GENERAL.md`: GATED
  - `2026-09-11-GEN2-POST-694/00-DECISIONES-Y-PARALELOS-POST694.md`: GATED
  - `2026-09-11-GEN2-POST-701/00-LEEME-LANZAMIENTO-POST701.md`: GATED
  - `2026-09-11-GEN2-POST-701/REVISION-CANDADOS-GEN1-GEN2-2026-09-11.md`: GATED
  - `2026-09-11-GEN2-POST-707/00-LEEME-PARALELOS-POST707.md`: GATED
  - `2026-09-11-GEN2-POST-707/07R-GEN2-PRODUCCION-Y-FALLO-POST707.md`: GATED
  - `2026-09-11-GEN2-POST-707/21-GEN2-EXPEDIENTES-ACCESO-LISTOS.md`: GATED
  - `2026-09-11-GEN2-POST-707/22-GEN2-VALIDACION-R-ENVIPE-CSV.md`: GATED
  - `2026-09-11-GEN2-POST-707/ADENDA-18-CONSUMOS-Y-BENCHMARK.md`: GATED
  - `2026-09-11-GEN2-POST-723/00-LEEME-LANZAMIENTO-POST723.md`: GATED
  - `2026-09-11-GEN2-POST-723/27-GEN2-ENSAFI-MEDICION-DESCRIPTIVA-CON-DISENO.md`: GATED
  - `2026-09-11-GEN2-POST-723/28-GEN2-IMOR-CONTEXTO-TEMPORAL-POR-REGIMEN.md`: GATED
  - `2026-09-11-GEN2-POST-723/29-GEN2-CONSULTA-OPERATIVA-CON-CONTRATO.md`: GATED
  - `2026-09-11-GEN2-POST-723/30-GEN2-VALIDACION-INDEPENDIENTE-PARAMETROS-ACTIVOS.md`: GATED
  - `2026-09-11-GEN2-POST-723/31-GEN2-F5-DOCUMENTAL-EJECUCION-PARA-FIRMA.md`: GATED
  - `2026-09-12-GEN2-POST-726/00-LEEME-PARALELOS-POST726.md`: GATED
  - `2026-09-12-GEN2-POST-739/00-LEEME-LANZAMIENTO-POST739.md`: GATED
  - `2026-09-12-GEN2-POST-739/39-GEN2-REACTIVOS-PENDIENTES-Y-BUSQUEDA-UTIL.md`: GATED
  - `2026-09-12-GEN2-POST-741/00-LEEME-PARALELOS-41-43.md`: GATED
  - `2026-09-12-GEN2-POST-741/41-GEN2-BANXICO-PRODUCTO-ATRASO-Y-COSTO.md`: GATED
  - `2026-09-12-GEN2-POST-741/43-GEN2-SHED-BNPL-DANO-Y-UNIVERSOS.md`: GATED
- **NC abiertas por razón (token A.14, prefijo exacto).** abiertas `140` · por token: `DECISIÓN-DE-MESA-PENDIENTE` 3 · `DIFERIDO-A` 11 · `FUERA-DE-PERÍMETRO` 5 · `NO-VERIFICABLE-AQUÍ` 2 · `PARO-ENTORNO` 4 · `PARO-PREMISA` 16 · `SUSTITUIDO-POR` 1 · prosa (sin token reconocible) `98`.
- **GEN2 (derivado de `corrida0 status`).** corridas selladas `102` / requeridas `86` · resultados sellados `7287` / activos `210` · pendientes `210` · dependencias numéricas legacy activas `173` · validación independiente `215` · diferencias materiales `0` · NC- abiertas `140` · replays LEGACY-GEN1 sellados `5` (no cuentan). El `0 / N` es la lectura correcta: el aparato se construyó antes que las corridas.
- **GEN2 · medición vs. adopción (ACTO GEN2-PRE-E5 · P3).** sellados `6686` · pendientes de adopción (citados en la propuesta, ningún consumidor activo aún) `12` · vetados por decisión vigente (sellados, pero una firma prohíbe adoptarlos: no son cola) `2` · adoptados por un consumidor activo `57`. Sellar un RESULT no mueve `dependencias_numericas_legacy_activas` por sí solo: solo el consumidor activo que lo adopta la baja.
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

> Vista derivada, no canon. Instrucciones vigentes: ver `instrucciones_vigentes` en el bloque derivado de arriba (`ADR-544` sella el lado repo, con reserva de A.9 sobre el lado proyecto — ver enmienda en `canon/gobernanza-v1_15.md`). El cuerpo curado deja de escribir la versión a mano (P2, `GEN2-TABLERO-SENAL-1`). El bloque de arriba lo escribe `tools/tablero_programa.py --actualiza` y describe el árbol clásico; **la señal de Gen 2 es la de §2**, derivada de `tools/corrida0.py status` (E.4: la dice el mecanismo, nunca una persona).

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
| Plan CORRIDA-0 | **Plan vigente: `PLAN-DE-OBRA-GEN2 v1.1` (sellado por merge del PR #652 · `forense/notas/PLAN-DE-OBRA-GEN2-v1_1-2026-09-09.md`)** — corrige NC-0083 (ACTO GEN2-OPERACION-1, 9/sep/2026): esta fila citaba `forense/notas/PLAN-FINAL-GEN2-v2_0-2026-09-07.md` **con `.sha256`**, anterior al PR #652; se cita por firma concreta, no por "versión más alta" |
| Instrucciones v2.14 | en el árbol (actualizado 19/sep/2026, `ACTO GEN2-RECIBO-CODEX-3`; `instrucciones-proyecto-v2_13.md` retirada por T01) |
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
| **G2** | **`vigencia` y `delta` sin implementar** — sigue así; ver `NC-0091` (`ABIERTA`, `GEN2-FIRMAS-ADOPCION-1`/`PR #656`: «Implementar delta» · `DECISION-DE-MESA-PENDIENTE`) para la decisión pendiente concreta. Corrección (ACTO GEN2-OPERACION-1, 9/sep/2026): decisiones POSTERIORES a este bloqueador ya consolidaron dos adopciones activas (`ADR-432 · ACTO GEN2-FIRMAS-ADOPCION-1`, `PR #655`: `CALC-C0D-MARCADOR-v3` y `CALC-ENVIPE-0001`, `cuenta_gen2=SI`, adoptadas por consumidor real). Esas dos adopciones **no** requirieron `delta`/`vigencia` (E.1 exige la comparación contra GEN1 sólo para lo que hereda de GEN1, no para toda adopción) — el bloqueador sigue vivo para la comparación GEN1, no bloqueó estas dos | dirección | implementarlos antes de la primera adopción que sí compare contra GEN1; mesa resuelve `NC-0091` |
| **G3** | **Filas `DECISION-DE-MESA-PENDIENTE`** en la deuda declarada — cifra viva: ver bloque derivado (`nc_por_razon`) | mesa | resolver por fila |
| **G4** | **Ramas contra la política de cero** — cifra viva: ver bloque derivado (línea «Ramas presentes en origin») | mesa | fusionar o borrar |
| **G5** | **Firmas ABIERTA** — cifra viva: ver bloque derivado (línea «Gobernanza operativa», `FP abiertas`) | mesa | firma por fila |
| **G6** | **NUEVA (14/sep, ACTO GEN2-DOCS-ALINEACION-2).** Fila de cita, no bloqueo — los cuatro hitos mayores de la semana del 9–12/sep, para que este tablero deje de describir solo el mundo del 9/sep: **triada, veredicto citado** — `CALC-TRIADA-0002` termina `SIN-GANADOR-UNICO` sobre `U3=12/14` (`forense/notas/2026-09-10-GEN2-F5-COMPLETA-cierre.md`, `PR #690`); **R-completa** — `UR=14/14` congelado, ocho `CALC-R` nuevos sellados (`forense/encargos/2026-09-09-GEN2-R-COMPLETA-MARCO.md`, `PR #690`); **validación independiente** — 16/16 PASA sobre parámetros activos, implementación separada (`forense/notas/2026-09-11-GEN2-VALIDACION-INDEPENDIENTE-PARAMETROS-ACTIVOS-cierre.md`, `PR #731`; el acumulado vivo `resultados_con_validacion_independiente=199` es del bloque derivado de arriba, no de este acto solo); **delta implementado** — `corrida0.py delta` deja de ser `NO-IMPLEMENTADO` (`delta_comparacion.py`, `PR #733`); `vigencia` sigue declarado y vacío | dirección | ninguno — es registro, no pendiente |
| **G7** | **NUEVA (14/sep, ACTO GEN2-DOCS-ALINEACION-2).** El mapa `31/39/40/41/42/43` que la ADENDA de dirección pidió, con triple distinción — verificado contra el árbol, no contra la prosa del despacho del 12/sep (`forense/encargos/cola/2026-09-12-GEN2-POST-741/00-LEEME-PARALELOS-41-43.md`): **31** (F5 documental, `DIN-M-01`/`TRA-M-07`) — **pausado**, `LISTO PARA FIRMA; NO AUTORIZA LLAMADAS POR SU MERA ENTREGA` (`forense/encargos/cola/2026-09-11-GEN2-POST-723/31-GEN2-F5-DOCUMENTAL-EJECUCION-PARA-FIRMA.md`); **39** (reactivos pendientes/búsqueda útil) — **fusionado**, `PR #742` (`forense/encargos/2026-09-12-GEN2-REACTIVOS-PENDIENTES-Y-BUSQUEDA-UTIL.md` `## CONSUMIDO`); **40** (conciliación NC-0165/demanda/ruteo) — **CORREGIDO tras revisión adversarial del PR (comentario de `/revisa`, 14/sep): fusionado, `PR #744`** (`git show 1518a15 --stat` → rama `acto/gen2-demanda-contratos-ejecucion-nc0165`, ficha en `forense/notas/2026-09-14-GEN2-CONCILIACION-TANDA-2-P3-censo.md:130` cita exacta `#744 -> 2026-09-12-GEN2-DEMANDA-CONCILIADA-Y-EJECUCION-NC0165.md`; el nombre de rama resuelve la identidad que la primera redacción de esta fila declaró `NO-VERIFICABLE-AQUÍ` — `ACTO GEN2-DEMANDA-CONTRATOS-EJECUCION-NC0165`/`ADR-491` SÍ es "encargo 40"); **41** (Banxico) — **fusionado**, **`PR #746`** (corregido: la redacción original de esta fila citaba `PR #744`, que en realidad es el 40 de arriba — confirmado por `git log --oneline origin/main \| grep -iE "Merge pull request #(742\|744\|745\|746\|747)\b"`, `ADR-492`); **42** (MOTRAL 2015/N35, "despachado, PR #747" según el propio LEEME) — **fusionado**, `PR #747` (`ADR-493`); **43** (SHED 2025 BNPL) — **fusionado**, `PR #745` (`canon/registro-rotulos.tsv`, `ADR-494`). `NC-0166` (falta el paquete reproducible del DCE mexicano de N35) se conserva con su vía propia — no se duplica aquí | dirección | ninguno — las seis celdas quedan con identidad y PR confirmados |

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

### 9.7 · 19–20/sep

Una frase por hecho, cada una con su comando. Sin narrativa.

- **Pisos en rejilla.** `forense/prereg-caja/PISOS-REJILLA-arbitro-metadatos-v1_0.tsv` entra como tabla de identidad `cell_id → consumer/axis/category/outcome/unit/status` (`GEN2-PISOS-REJILLA-CLI-1`, PR #871) — `ls forense/prereg-caja/PISOS-REJILLA-arbitro-metadatos-v1_0.tsv`.
- **Marcador.** `tools/marcador_segmento.py` se rediseña sobre el diseño de mesa `MARCADOR-SEGMENTO-diseno-direccion-v1_0` + delta v1.1 — `cat forense/encargos/2026-09-19-GEN2-MARCADOR-REDISENO-1.md | head -5`.
- **46 adoptados.** `estado = ADOPTADO-POR-FIRMA` en `data/corrida0/marcador-segmento.tsv` (cifra viva: ver `marcador_segmento.por_estado` en el bloque derivado, hoy `20` — la cifra de este ítem es histórica del 19/sep y no se reescribe) — `grep -c ADOPTADO-POR-FIRMA data/corrida0/marcador-segmento.tsv`.
- **Error de persistencia por instrumento.** Celda-D piloto 3 lo trae como hallazgo de partida — `cat forense/encargos/2026-09-19-GEN2-CELDA-D-PILOTO-3.md`.
- **Corrección de `familia.union.libre`.** regla en `milpa/tramite.yaml` con ajuste citado en `forense/encargos/2026-09-19-GEN2-FAM-UNION-ESTIMANDO-1.md` — `grep -n "familia.union.libre" milpa/tramite.yaml`.
- **Emisión C2 compuesta.** `forense/encargos/2026-09-19-GEN2-C2-COMPUESTO-RESERVADAS-1.md` derrota el universo III (cruce) del marcador — `ls forense/encargos/2026-09-19-GEN2-C2-COMPUESTO-RESERVADAS-1.md`.
- **PARO del piloto 3.** `forense/encargos/2026-09-19-GEN2-CELDA-D-PILOTO-3.md` cierra por hallazgo, no por objeto cumplido — `grep -n "PARO" forense/encargos/2026-09-19-GEN2-CELDA-D-PILOTO-3.md`.
- **Salida del carril Codex.** rama Codex sin PR (`…marcador-adopcion-cli-1`) invisible para mesa durante horas — defecto real que abre este mismo encargo (`GEN2-TABLERO-SENAL-1`, Gate D-14 (b)) — `git ls-remote --heads origin | grep -i marcador-adopcion-cli-1`.

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
