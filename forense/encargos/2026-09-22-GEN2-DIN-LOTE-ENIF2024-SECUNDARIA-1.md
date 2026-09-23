# ENCARGO · ACTO GEN2-DIN-LOTE-ENIF2024-SECUNDARIA-1 · Los cinco pares con `formalidad` del lote ENIF 2024 se adjudican en su propio estrato de universo T, con el C2 restringido como piso — sin tocar la frase de producto de las 44

> ENTORNO: **CAJA** — abre ENIF 2024 solo por el CALC de adjudicación congelado. Hook; si no coincide, PARA.

CABECERA · SHA `3f48be30` · una sola sesión · MODELO: Opus · MODO: **RÍGIDO** · CONTADOR: +1 corrida sellada (adjudicación secundaria), `cuenta_gen2 = SI`, **no adopta**; `celdas_validadas` sube por las celdas del estrato T con veredicto (derivado; **rótulo RETROSPECTIVA si R de esos cruces ya fue derivado en COMMIT-3 del lote — el acto lo verifica**) · CALC-id reservado: `CALC-DIN-LOTE-ENIF2024-ADJUDICACION-T-0001` · ids raíz de acto.

## 1 · OBJETIVO
Ejecutar la opción A de `FP-260922-GEN2-DIN-LOTE-C2-RESTRINGIDO-1-4e12-01` (FIRMADA): enmienda con archivo propio a la spec del lote + un CALC de adjudicación **SECUNDARIO** para los 5 pares `formalidad × {sexo, edad, escolaridad, localidad, cuenta_formal}` en un estrato «universo T» que nunca se suma al ΔMAE primario ni a la frase de las 44 celdas; C2R citado de `CALC-C2-RESTRINGIDO-IC-ENIF2024-0001`; réplicas re-derivadas dentro del lote con el mismo procedimiento; régimen ARBITRO-2024 (firma Q2, `…6c10-04`). «Hecho» = `verify` REPRODUCE; los RESULT del estrato T llevan `universo = trabajadores (P3_13)`, `estrato = T`, y **ninguno** aparece en el ΔMAE primario del lote (`grep` sobre el CALC primario: 0); el rótulo PROSPECTIVA/RETROSPECTIVA declarado por celda según el orden de sellos.

## 2 · FIRMAS DE MESA
Ya selladas, se citan: FP `…4e12-01` opción A (asentada en #1003); FP `…6c10-04` Q2 (régimen ARBITRO-2024) y `…8e53-02` opción B (los cinco pares con C2R) en #1001. Ninguna nueva.

## 3 · LO QUE DIRECCIÓN SABE
- `[EJECUTADO]` `CALC-C2-RESTRINGIDO-IC-ENIF2024-0001` sellado con asiento (#1003; sin fila en vista hasta E11). `[LEÍDO]` FP `…4e12-01`: «su spec v1.0 congelada los deja NO-ADJUDICABLE-SIN-PISO, así que consumirlos exige un artefacto nuevo … (A) enmienda con archivo propio + CALC de adjudicación SECUNDARIO … estrato «universo T» aparte que nunca se suma al ΔMAE primario».
- `[SUPUESTO]` R de esos 5 pares (cruces `formalidad × eje`) **ya fue derivado** en COMMIT-3 del lote (`GEN2-DIN-LOTE-ENIF2024-COMMIT-2-3`), luego la adjudicación secundaria es RETROSPECTIVA (piso construido después de ver R) y así se rotula; `celdas_validadas` no la cuenta como prospectiva. Si resulta falso —R de esos pares no se derivó—, el acto congela emisiones antes de derivarlo y la adjudicación es PROSPECTIVA: mejor, y se dice.
- ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
`ls -d data/corrida0/CALC-DIN-LOTE-ENIF2024-ADJUDICACION-T*` → 0; enmiendas de la spec del lote: `ls forense/prereg-caja/ | grep -i "lote-enif2024.*ENMIENDA"` → reporta. Ramas vivas: ninguna; no correr a la vez que E13.

## 5 · PIEZAS
- **COMMIT-1:** `DIN-lote-enif2024-spec-v1_0-ENMIENDA-1.md` (archivo propio, la v1.0 intacta) + `spec.yaml` del CALC secundario: los 5 pares, universo T por texto (`P3_13`), C2R por id de RESULT, procedimiento de réplicas idéntico al lote, criterio y `INDECIDIBLE` verbatim, regla de rótulo PROSPECTIVA/RETROSPECTIVA por orden de sellos (v2.16 §4), estrato T fuera del ΔMAE primario por construcción (test). `spec-check` VERDE; D-22.
- **COMMIT-2:** `run` de la adjudicación secundaria; sello; asiento; `verify`.
- **P3:** nota con el veredicto por par, el rótulo, y una línea explícita: «la frase de producto de las 44 celdas no cambia» (comando que lo demuestra).

## 6 · LATITUD
DECIDES TÚ: nombres, orden, cableado D-18. PREGUNTAS A MESA: si `cuenta_formal × formalidad` es degenerado (colineal), ¿NO-CONSTRUIBLE (recomendado) o emitir? NO DECIDES: §7.

## 7 · PAROS
a) derivar cualquier cruce nuevo de ENIF 2024 fuera del CALC congelado · b) editar la spec v1.0 del lote o forzar · c) adoptar · d) cambiar procedimiento congelado · e) nube · f) inalcanzable · g) código congelado no corre.

## 8 · COMPUERTAS
«No hay otro acto de caja en vuelo — protege: borrar.» Orden sugerido: después de E11 (para que la fila entre a la vista sola).

## 9 · PERÍMETRO
Propio: la enmienda (archivo nuevo) · `data/corrida0/CALC-DIN-LOTE-ENIF2024-ADJUDICACION-T-0001/` · derivados por comando · `replay-evidencia.tsv` · nota · `canon/L0/<raíz>.md`. Ajeno: la spec v1.0 del lote, los CALC primarios del lote, `CALC-C2-RESTRINGIDO…` (lectura), `milpa/`. «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · NO HACE · SUCESORES · CIERRE
No cambia el veredicto primario, no adopta. Sucesor: adopción del estrato T por firma si algún par tiene ganador. Auditoría: la spec del lote ya la trae; la nota la contesta para el estrato T (universo restringido: quien trabaja — sesgo de clase declarado). Cierre por /acto.

## NO-CORRIDO / RESERVAS

- **Qué:** `registro --escribe --lote` publicar la fila de `CALC-DIN-LOTE-ENIF2024-ADJUDICACION-T-0001` en `data/corrida0/corridas.tsv`/`resultados.tsv` (vista).
  **Por qué:** `DIFERIDO-A:TUBERIA`. `registro --escribe --lote` sí publicó la fila dentro del worktree del acto (medido: `resultado_replay=REPRODUCE`, sin pisadas ajenas nuevas fuera de las ya diagnosticadas), pero `corridas.tsv`/`resultados.tsv` son `# DERIVADO — NO EDITAR` desde la firma P4 de `GEN2-TUBERIA-EFICIENCIA-1` (21/sep): ningún PR puede tocarlos (`tools/derivados_protegidos.py --toca`, bloqueante en el job `enrutamiento-pr`) y el job de push a `main` no corre `registro` (exige `--lote`, juicio de mesa). Se revirtieron a la versión de `origin/main` antes de empujar. El asiento de E.7 que sí viaja en el PR es `forense/replay-evidencia.tsv` (no es derivado): `resultado_replay=REPRODUCE`, `contexto_replay=IDENTICO`, ya asentado.
  **Impacto:** `N_corridas_selladas` no sube en la vista publicada por este PR; `corrida0 status` sí la cuenta (proyección en memoria). CONTADOR: la corrida queda «sellada en disco, no registrada».
  **Sucesor:** `NC-260922-GEN2-DIN-LOTE-ENIF2024-SECUNDARIA-1-65c3-01` — mesa corre `registro --verifica --escribe --lote CALC-DIN-LOTE-ENIF2024-ADJUDICACION-T-0001` sobre `main`, o el job de TUBERÍA cuando corra `--lote` derivado del diff de `replay-evidencia.tsv`.

## CONSUMIDO

Ejecutado por PR [#1026](https://github.com/Josanoforo/Modelado-Mexicano/pull/1026), ACTO GEN2-DIN-LOTE-ENIF2024-SECUNDARIA-1, 22/sep/2026. `FP-260922-GEN2-DIN-LOTE-C2-RESTRINGIDO-1-4e12-01`: pasa de `PENDIENTE` a `EJECUTADA` por este acto (opción A consumida). `NC-260922-GEN2-DIN-LOTE-C2-RESTRINGIDO-1-4e12-02` (desenlace secundario `informal_cualquiera`) sigue fuera, sin tocar. Este append lo hace `GEN2-TRAMITE-FIRMAS-9` (P1) — el acto original (#1026) se fusionó sin dejar estas dos secciones en el encargo archivado.
