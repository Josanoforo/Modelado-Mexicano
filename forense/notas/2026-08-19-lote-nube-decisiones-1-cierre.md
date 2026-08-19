# NOTA · LOTE·NUBE-DECISIONES-1 — cierre

**Acto:** `LOTE·NUBE-DECISIONES-1` · **Encargo:** `forense/encargos/2026-08-19-LOTE-NUBE-DECISIONES-1.md` (archivado, `CONSUMIDO`) · **ADR:** `ADR-126` · **Entorno:** NUBE (`cloud_default`, repo-only) · **Rama:** `claude/lote-nube-decisiones-1-ie9hgl` · **SHA de redacción:** `b4a9b3f` (#292) · **Ejecutado contra:** `b4a9b3f` (re-derivado al arrancar — coincide, sin deriva).

## 0 · ARRANQUE

1. **REPO.** Clon existente, `/home/user/Modelado-Mexicano`. `git log -1`: `b4a9b3f Merge pull request #292`. `git status`: árbol limpio al abrir.
2. **SHA.** `origin/main = b4a9b3f`, exacto contra lo declarado — sin deriva que reportar.
3. **`data/raw`.** No existe (`ls: cannot access 'data/raw': No such file or directory`) — no se toca, no aplica.
4. **ENTORNO.** `env | grep -i -E "entorno|espejo|mirror"` → 0 coincidencias de 132 variables examinadas (conteo de archivos/entradas pegado junto al NO-ENCONTRADO, por la regla nueva). `type grep` → `grep is /usr/bin/grep`, sin envolver (no alias, no función) — `command grep` no fue necesario para ningún veredicto de este lote.
5. **ESPEJO.** No se usó ninguno. Toda cifra de esta nota sale de comandos corridos en este worktree en esta sesión, con el comando a la vista donde importa.

## 1 · Tabla T0–T6

| tarea | fila(s) | veredicto | contador | notas |
|---|---|---|---|---|
| `T0` | — (cherry-pick) | `12e3b6c` aplicado — conflicto real en `firmas-pendientes.tsv` (HEAD tenía `FP-56`…`FP-69`, la rama solo conocía hasta `FP-60`), resuelto conservando `HEAD` + el único cambio sustantivo de la rama (`"este PR"`→`"PR #279"`) | **0** | Commit local re-etiquetado `T0:` por la doctrina del lote |
| `T1` | `FP-66` → `CERRADA` | Fórmula por cadena **NO mordió hoy**: 12 llaves distintas por parser = 12 por cadena. Test nuevo (`test_contador_no_duplica_condicional_por_llave`) blinda contra duplicación futura | **12 de 15, sin cambio** | `contador_condicionales_medidas()` sin tocar (fuera de perímetro, lo consume `motor.py`) |
| `T2` | `FP-62` → `CERRADA`; `FP-70` nueva, `ABIERTA` | **DUPLICA** sobre 16/21 pares (ya ejecutados por `FP-10`/`FP-12`, hoy); **COMPLEMENTA** acotado — 4 parejas `real`-contra-`real` rescatadas como `FP-70` | **0** — sin rescate a producción, solo higiene | Corrección de premisa: la fila citaba `FP-29`, el cierre real es `FP-10`/`FP-12` |
| `T3` | `FP-64` — sigue `ABIERTA`, ampliada | Seis candidatos derivados y descartados; ninguno cruza el criterio. `ENVIPE` nombrado, no propuesto | **0** — paso previo, no adjudica | `R5.1-D2` verificada como estructuralmente-(ii)-pero-sin-etiquetar, no adjudicado |
| `T4` | `FP-65` → `CERRADA` | **ACOTA** `ADR-109(d)`, no lo revoca — corroboración corre sobre objeto distinto (el par, no el ítem) | **`ASIGNADO`→`ASIGNADO`** en `G1a`/`G5` (no `G1b`, que no tiene este coeficiente) | Corrección de premisa: la fila citaba `G1b`, el coeficiente real vive en `G1a`/`G5` |
| `T5` | `FP-67` → `CERRADA` | Asignación trivial confirmada: adquisición va a `UBUNTU` | **0** | Ejecución material en `LOTE-UBUNTU-ADQ-1 T1`, no lanzado aquí |
| `T6` | `FP-68` → `CERRADA`; `FP-69` → `CERRADA` | `ADR-67(c)` gobierna (no hay colisión real); `R5.1-D3` sellada `EJERCIDA_INDECISA` | **Llaves: 1 de 3 → 2 de 3** (no 2 de 2); **Hito D sin cambio, 13 de 27** | Corrección de premisa: el lanzamiento anticipaba "2 de 2"; el denominador ya era 3 antes de esta firma |

Ninguna tarea paró. Ninguna dependencia entre tareas se invocó (el lanzamiento declaraba cero).

## 2 · Las tres correcciones de premisa, en un solo lugar

1. **`FP-62` cita `FP-29`.** Verificado contra el árbol: `FP-29` es la reconciliación de series externas de confianza radial (el 22%, `ADR-111`, `PR #275`) — sin relación temática con `universo-puertas`/`ADR-69`/`ADR-70`. Las filas que sí gobiernan el solape que `FP-62` pregunta son `FP-10` (`ADR-115`) y `FP-12` (`ACTO FUSION-PUERTAS`), ambas cerradas **hoy mismo**, antes de que este lote arrancara.
2. **`FP-65` cita `G1b/radio_confianza`.** Verificado contra `canon/modelo-decision-v4_0.md:435`: `G1b` (*"Difusión por confianza radial"*) está **ya contradicho** por evidencia no relacionada (casos Nu/Kueski-Aplazo) y su coeficiente entero está *"a revisión"* — no tiene `radio_confianza`. El coeficiente real vive en `G1a` (`−0.35`) y `G5` (`0.15`), exactamente los que la ficha congelada ya nombraba.
3. **`FP-69` anticipa "2 de 2".** Verificado por la propia receta de `forense/registro-llaves-identificacion-v1_0.md` §4/§7 (`sed`/`grep`/`awk`, corrida en vivo, salida pegada en el archivo): el denominador **ya** había subido a 3 el 19/ago/2026, al abrir la fila `R5.1-D3` (`ACTO FICHA-R51-D3`), antes e independiente de esta firma. Sellar `B` mueve el numerador de 1 a 2 sobre un denominador que ya era 3 — el resultado correcto es **2 de 3**.

Ninguna de las tres cambia el fondo de lo que dirección pedía; las tres se declaran porque `AGENTS.md` exige distinguir discrepancia material de cosmética, y las tres apuntaban a la fila, el coeficiente o el contador equivocado.

## 3 · Un extremo del perímetro NO ejecutado, declarado por qué

`canon/hitoD-preregistro-v2_0.md` estaba nombrado en la unión de perímetros del lote (`"canon/hitoD-preregistro (T6, append)"`). No se escribió ninguna línea ahí: `ADR-67(c)` (sellado 10/ago) ya establece que un veredicto de diseño por regla de elegibilidad no cuenta como veredicto de `R5.1` para ese bloque, y `T18`/`T20` lo confirman por mecánica independiente (el contador es un `set` de identificadores `RX.Y`, y `R5.1` ya está dentro desde el 4/ago/2026 — una línea `R5.1-D3` no incrementaría nada y no coincidiría con el patrón que el parser reconoce). Escribir ahí para seguir la letra del perímetro habría sido mecánicamente incorrecto. El sello de `FP-69` vive en `forense/registro-llaves-identificacion-v1_0.md` en su lugar — el único archivo donde sellarlo tiene efecto real, y una extensión de perímetro mínima y declarada (ver `ADR-126`, doctrina del lote).

## 4 · Corrupción de tablero evitada, declarada por disciplina

Primer intento de escritura de `FP-70`/`FP-62` usó el módulo `csv` de Python para reescribir `forense/firmas-pendientes.tsv` completo. Verificado antes de continuar (`grep -c '""'` subió de 49 a 52, `git diff` mostró `FP-58`/`FP-61`/`FP-66` reescritas sin haberlas tocado): **exactamente el defecto que `ADR-123(h)` ya había medido y corregido dos veces en este archivo** — el lector canónico del tablero (`_t22_tabla`, `tests/check.py`) hace `l.split("\t")` plano, nunca `csv`, así que el re-entrecomillado que `csv.writer` añade a cualquier campo con `"` literal viaja corrupto. Revertido (`git checkout --`) antes de cualquier commit; las siete escrituras siguientes a este archivo (`FP-62`, `FP-64`, `FP-65`, `FP-66`, `FP-67`, `FP-68`, `FP-69`, `FP-70`) se hicieron con `split`/`join` de texto plano, verificado campo-por-campo (9 columnas, `grep -c '""'` sin cambio en 49) después de cada una.

## 5 · Verificación final

```
$ python3 tests/check.py --baseline
21 FAIL · 118 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json
(1 entradas de la línea base ya no aparecen — mejora, no bloquea)
```

Sin `--freeze`, como el lanzamiento prohíbe. `tests/baseline.json` sin tocar.

## 6 · Lo que este lote NO hizo

No fusionó ninguna rama (`fp57`, `rescate/reconcilia-puertas-local`) — quedan para que mesa las borre al fusionar este lote. No re-corrió ningún diseño ni recalculó ningún estimador. No adjudicó `FP-64` ni `FP-70` (ambas `ABIERTA`, mesa decide). No editó `ADR-109(d)` ni `ADR-110(a)` — los citó. No tocó `data/raw`, `data/`, `corpus/`, `milpa/refutations.yaml`, `milpa/procedencia.yaml`, `canon/modelo-decision-v4_0.md`, `canon/hitoD-preregistro-v2_0.md`. No recongeló `tests/baseline.json`.
