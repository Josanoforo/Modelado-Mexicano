# Acto 1 · Portada derivada + T19 — nota de cierre

**Fecha:** 4/ago/2026 · **Contra:** `origin/main` = `4b27869` (PR #95) · **Tipo:** (1) para todo lo verificado contra archivo abajo; (3) para las dos decisiones de juicio (premisa 5, MESA-M4).

Registro de lo que el encargo pedía como "nota forense... con nota fechada y cuerpo de PR como registro (R0)": tres divergencias de juicio frente al texto del encargo, y lo que quedó encontrado-pero-fuera-de-perímetro. No es un ADR — este acto no sella ninguno.

---

## 1 · Premisas — las siete se sostuvieron, sin re-derivar nada

Verificadas contra archivo antes de ejecutar (ADR-39). Detalle de cómo se verificó cada una está en los tres cuerpos de commit; resumen:

1. Emisiones del bloque de veredictos = 12 · fichas = 11 (7D·1B·2A·1E) — exacto, parser `_VEREDICTO_CANONICO` aplicado a mano contra `forense/hitoD-preregistro-v2_0.md` líneas 1002-1013.
2. `grep -c 'clase: "MEDIDO·PARCIAL' milpa/procedencia.yaml` = 9 — exacto, y cruzado contra el propio desglose de `modelo:725` (9+0+2+3=14).
3. Coeficientes en escala = 0 de 15 — `modelo §2.2`: "Los quince coeficientes son ASIGNADO. Ninguno es medido"; los tres β̂ de `procedencia.yaml: coeficientes_generador_medidos` llevan cada uno su propio campo `adr57_a` que los excluye.
4. `modelo:277/621/725` ya decían "9 de 14"; la cabecera (línea 11, el párrafo de changelog "v4.0 — 3/ago/2026") era la única en "8 de 14" — confirmado, ver commit 2(b).
5. Ver §2 abajo — no se sostuvo tal como estaba redactada.
6. "v3.4" aparece exactamente una vez en el archivo de `estado` previo al renombre de este acto (`estado-programa-v1_9.md`, línea 8, VERIFICAS ASÍ); el cuerpo (§0) ya listaba v4.0 — confirmado.
7. Último ADR = 58 — confirmado (`gobernanza:637`, y `gobernanza §0.1` lo nombra "el último es **ADR-58**").

---

## 2 · Premisa 5 — la clasificación sugerida no se sostuvo bajo lectura completa

El encargo proponía: "≈821 (tabla de §6) VIGENTE, ≈636 y contexto de 64 narrativa histórica" — y pedía explícitamente derivarlo del contexto, no de esos números de línea.

Leídas las cuatro apariciones completas de "8 de 27" en `modelo`:

- **L21** — `> **v3.4 — 30/jul/2026...**`, un párrafo de changelog versionado y fechado, con su propio "2 de 27" correcto-cuando-se-escribió. Inequívocamente histórico. (No estaba entre las cuatro que la premisa 5 discutía — se confirma aquí por completitud.)
- **L64** (`§0.1`) — "Estado de falsación de las REGLAS del motor... **8 de 27 corridas archivadas**", en tiempo presente, sin marco "as of fecha", con dos rondas de correcciones "*(Corregido 4/ago/2026 — ...)*" ya aplicadas (2→3→4→8) antes de este acto.
- **L636-637** (`§7 · Estado de validación`) — el párrafo abre con "**Marcador honesto, actualizado al 30 de julio de 2026**", lo que en primera lectura sugiere snapshot congelado. Pero el mismo párrafo ya lleva las mismas dos rondas de "Corregido / Corregido de nuevo, 4/ago/2026" que L64 — es decir, el propio documento ya trató este marcador como vivo, no como historia fechada, dos veces antes de este acto.
- **L821** (módulo de auditoría de rigor extremo, no "tabla de §6" — §6 termina antes de §7, que empieza en L632 y sigue hasta después de L821) — tabla con columna "Heredado, con receta ejecutable — corridas actualizado 4/ago/2026", inequívocamente viva.

**Conclusión:** L64, L636-637 y L821 son las tres vigentes; solo L21 es histórica. Las tres se corrigieron a 11 de 27 en el commit 2(c), con `R5.1`→`A`, `R5.2`→`A`, `R1.2`→`E` añadidas a cada lista y nota fechada nueva, mismo patrón que las correcciones 2→3→4→8 ya usaban. Si la mesa quería que L64/636 quedaran como históricas por alguna razón que esta lectura no capturó, es reversible — pero dejarlas en "8 de 27" mientras L821 decía "11" habría sido una contradicción interna nueva, del mismo tipo que T19 existe para prevenir.

---

## 3 · [MESA-M4] — aplicada la recomendación, no confirmada por mesa

El encargo dejó `[CONSERVAR-ETIQUETADO / RETIRAR — mesa escribe aquí]` sin llenar, con recomendación CONSERVAR-ETIQUETADO. Los tres commits ya asumían ese resultado ("[MESA-M4] aplicado al 4 de 144" no es condicional en el texto del encargo). Se aplicó CONSERVAR-ETIQUETADO en README, AVISO-DE-ALCANCE y no se tocó el titular en `modelo` (que ya lo tenía congelado y etiquetado desde el 31/jul). **Sigue pendiente de confirmación de mesa** — si la decisión real es RETIRAR, las cuatro líneas que llevan `[MESA-M4]` (README ×1, AVISO ×2) se revierten a una frase sin el titular, sin tocar nada más de este acto.

---

## 4 · Efecto lateral del renombre — declarado, no corregido

El renombre de `estado-programa-v1_9.md` a `v1_10.md` deja 13 citas bare-backtick al nombre viejo colgando: 12 en `forense/` (append-only) y 1 en un ADR ya sellado de `gobernanza` (`gobernanza:498`, ilustra un comando de verificación pasado, no un puntero vivo). Ninguna se edita. T03 sube de 18 a 31 WARN (84→97 total). `--baseline` queda ROJO con 9 entradas nuevas (la clave del baseline incluye la ruta del archivo — `estado-programa-v1_10.md` no es `estado-programa-v1_9.md`, así que hasta un WARN preexistente sin relación con el renombre, ej. el fragmento de ejemplo `...-v3_0.md`, cuenta como "nuevo" bajo la ruta nueva).

Mismo patrón, ya precedentado: el renombre de `modelo` v3.4→v4.0 (Encargo A) dejó 6 citas colgando en `gobernanza`+`estado`, declaradas y no ejecutadas (`forense/hallazgos.md`, entrada "DETENTE 3"). Aquí se sigue el mismo criterio. Detalle completo, con la lista exacta de archivo:línea, en el cuerpo del commit 2 y en `forense/hallazgos.md` (entrada de esta fecha).

Las dos autodeclaraciones de FAIL/WARN vigente de `estado` (antes L128 y L220) se actualizaron a `18 FAIL · 97 WARN` — la cifra real, verificada con `python3 tests/check.py` corrido sin `--strict`/`--baseline`/`--freeze` — para que T16 no fallara por una causa (el renombre) ajena a lo que T16 vigila.

---

## 5 · Encontrado, fuera del perímetro nombrado — no corregido aquí

- **`README.md`, sección "Deudas abiertas", `S3`:** "48 de 49 reglas... sin falsación pre-registrada corrida" — no cuadra contra ningún estado real del programa que se haya podido reconstruir (49−11=38 hoy; 49−2=47 con el "2 de 27" que este mismo README tenía antes de este acto). El encargo nombraba el bloque "Estado del modelo" y la tabla de Estructura, no "Deudas abiertas" — no se tocó, para no exceder lo que los tres commits declaran que hacen. Debería derivarse a `38 de 49` en un acto de seguimiento.
- **`canon/estado-programa-v1_10.md`, `§L5`/`§S3` (antes líneas 93 y 120):** "8 de 27 corridas archivadas" / "19 de 27 sin corrida" / "41 de 49 reglas... sin corrida" — stale contra el mismo `11 de 27` real. **Ya registrado**, no se re-registra aquí: `forense/hallazgos.md`, entrada del sello de ADR-58 (2026-08-04, penúltima antes de esta), lo declaró a propósito fuera de perímetro de ese acto ("estado (solo rider)"), y el encargo de Acto 1 tampoco lo nombró — el propio encargo limita las "cuatro superficies" a README, AVISO y las *cabeceras* de `estado`/`modelo`, no sus cuerpos.
- **`canon/gobernanza-v1_15.md:358,649`:** mismas cifras `8 de 27`/`19 de 27` en la "Fuente única" de Hito D y la tabla de deuda declarada — `gobernanza` no está en el perímetro de este acto en absoluto (ni la premisa 5 lo nombra, ni el perímetro del encargo lo lista salvo para "referencias vigentes" del grep de rename, que es un caso distinto).

Ningún test lee ninguna de las líneas de este apartado — no impiden medir. Quedan para el próximo acto que abra `estado-programa`/`gobernanza`/`modelo-decision` con perímetro de cascada completa, exactamente el criterio que la entrada de ADR-58 ya fijó.

---

## 6 · Verificación de cierre — cruda

```
python3 tests/check.py             → 18 FAIL · 97 WARN (T19a/b/c en verde)
python3 tests/check.py --baseline  → LÍNEA BASE ROJO, 9 entradas nuevas (rename cascade, §4 arriba), 3 ya no aparecen
grep -c "de 27" README.md          → 1 (README.md:36, "**11 de 27** corridas del Hito D... — **7D·1B·2A·1E**")
grep -rln "estado-programa-v1_9\|estado-programa-v1\.9" --include="*.md" --include="*.py" .
                                    → 0 referencias VIGENTES. Lo que queda, todo clasificado histórico o
                                      intencional, ninguno editado:
                                        - forense/* (17 archivos): append-only, exentas por diseño (una de
                                          ellas es esta misma nota, que nombra el archivo viejo al explicar
                                          el rename).
                                        - canon/gobernanza-v1_15.md:498: prosa de un ADR ya sellado (ADR-51),
                                          ilustra un comando de verificación pasado, no un puntero vivo.
                                        - canon/modelo-decision-v4_0.md:828: nota histórica sobre el rename
                                          de `modelo` v3.4→v4.0 (cascada declarada y no ejecutada de OTRO
                                          acto) — fuera del perímetro de `modelo` en este acto (cabecera +
                                          premisa 5 solamente).
                                        - canon/estado-programa-v1_10.md:7: `REEMPLAZA A` — cita intencional
                                          del nombre inmediatamente anterior, mismo patrón que usan `modelo`
                                          y `gobernanza` en su propia cabecera.
```

`tests/baseline.json` no se tocó.
