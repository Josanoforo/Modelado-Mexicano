# ENCARGO · ACTO GEN2-DUELO-ENVIPE2026-MARGINALES-2 · Lo que quedó reservado de ENVIPE 2026 se predice antes de abrirse: pisos t−1 contra tendencia de serie en las celdas marginales y nacionales que el primer duelo no tocó

> ENTORNO: **CAJA** — abre ENVIPE 2011–2025 (emisiones); ENVIPE 2026 **solo** en COMMIT-3 por el CALC congelado. Hook; si no coincide, PARA.

CABECERA · SHA `3f48be30` · una sola sesión · MODELO: Opus · MODO: **RÍGIDO** desde COMMIT-1 · CONTADOR: +2 corridas selladas (emisiones, adjudicación), `cuenta_gen2 = SI`, **no adopta**; `celdas_validadas` sube por cada celda con veredicto PROSPECTIVA (derivado); la reserva restante de `envipe2026` pasa a CONSUMIDA-POR-DUELO para lo que este CALC emita, y **nada más** · CALC-id reservados: `CALC-DUELO-ENVIPE2026-MARGINALES-EMISIONES-0001`, `…-ADJUDICACION-0001` · ids raíz de acto.

## 1 · OBJETIVO
Que las celdas de ENVIPE 2026 que siguen RESERVADAS —`civico.denuncia.con_seguro` nacional y por eje (sexo, edad, cobertura_seguro) y los nacionales de las demás reglas ENVIPE del modelo con serie sellada (`CALC-ENVIPE-SERIE-*`)— tengan una adjudicación **PROSPECTIVA**: pisos t−1 (los marginales y nacionales 2025 ya sellados como árbitro) contra TENDENCIA-SERIE (mínimos cuadrados en logit sobre la serie previa, sin parámetros — el retador que FP 852f (b) mandó al «siguiente duelo»), emisiones selladas **antes** de abrir 2026, R derivado después. «Hecho» = tres commits en orden (`git log`); `verify` REPRODUCE en los dos CALC; ningún acceso a `envipe2026_csv` antes del commit de COMMIT-3 (test desde el historial, precedente piloto 2 y duelo 1); veredicto por celda con vocabulario cerrado; `decisiones.tsv` con la fila que consume exactamente lo emitido y lista lo que **sigue** reservado.

## 2 · FIRMAS DE MESA
- Ya selladas, se citan: `reserva:envipe2026` («fuera del código que se congele para ello»); `reserva:envipe2026-consumida-por-duelo` (consumo SOLO de `evade_norma` + no-denunciado nacional: **lo demás sigue reservado**); FP `…ENCIG-SERIE-Y-TENDENCIA-1-852f-01` (b) FIRMADA en #1001: «TENDENCIA-SERIE entra como RETADOR, no piso … si la spec del duelo ya está congelada, queda para el siguiente duelo» — este es el siguiente.
- *Propuesta de dirección, mesa sella o borra:* «Se autoriza el COMMIT-3 de este duelo —única lectura de la reserva restante de ENVIPE 2026— exclusivamente por `CALC-DUELO-ENVIPE2026-MARGINALES-ADJUDICACION-0001` congelado, con el sha de emisiones escrito en COMMIT-3a; lo que no emita este CALC sigue RESERVADA.» Sin texto → PARO antes de COMMIT-3; COMMIT-1 y 2 sí.

## 3 · LO QUE DIRECCIÓN SABE
- `[EJECUTADO]` `data/corrida0/decisiones.tsv` fila `reserva:envipe2026-consumida-por-duelo`: consumo limitado a `evade_norma` (nacional, 4 ejes, 24 cruces) y `no-denunciado` nacional. `[EJECUTADO]` `milpa/tramite-ola5-propuesta-v0.yaml`: entradas `civico.denuncia.con_seguro_ejes_envipe2025` (sexo 2, edad 4, cobertura_seguro 2) y `tramite.evasion_norma_envipe2025` (ya consumida). `[EXISTE]` `CALC-ENVIPE-SERIE-2011…2019` (serie anual por regla; no sé qué reglas ni si llega a 2025: **el acto lo lee** y solo entra lo que tenga serie sellada hasta 2025).
- `[LEÍDO]` Duelo 1 (`#1010`, ADR de raíz `f57b`): receta de tres commits, guardián `reservada=True`, test de historial; se copia, no se reinventa. `tools/duelo/cruces_familia.py` implementa C2/P/S1/Sλ/AP; TENDENCIA-SERIE vive en `GEN2-ENCIG-SERIE-Y-TENDENCIA-1` (`tools/` o CALC citado: el acto lo localiza por objeto).
- `[SUPUESTO]` Los reactivos de `denuncia.con_seguro` y de las series no cambiaron de texto en el FD 2026. Verificación **por texto** en COMMIT-1 (el FD 2026 sí se puede abrir: no es microdato); celda con texto distinto → `NO-CONSTRUIBLE`, declarada.
- ADJUNTOS: ninguno.

**Apéndice A.8 (T-YAMEDIDO, mecánico, añadido al archivar — no es texto de dirección):** `python3 tools/ya_medido.py civico.denuncia.con_seguro`
```
=== ya_medido: civico.denuncia.con_seguro ===
  resuelto por canon: civico.denuncia.con_seguro -> R7.2 (canon/modelo-decision-v4_0.md §3, registro congelado + tag **id:**)
  términos de búsqueda (match exacto): civico.denuncia.con_seguro, R7.2

-- milpa/tramite.yaml --
  milpa/tramite.yaml:987  situacion=sufre_delito_asegurable tier=FUERTE p=0.790900  [TASA-EJECUTADA]
      id: civico.denuncia.con_seguro

-- milpa/tramite-ola5-propuesta-v0.yaml --
  (sin apariciones)

-- data/corrida0 (RESULT + ejecución + sello) --
  (sin apariciones)

MEDIDA-EN: tramite.yaml
```
No contradice §3: `civico.denuncia.con_seguro` nacional (P3_13 base) ya tiene tasa ejecutada en `tramite.yaml`; lo que este encargo busca adjudicar es la celda **marginal por eje** (`civico.denuncia.con_seguro_ejes_envipe2025`, sexo/edad/cobertura_seguro) y los nacionales de `CALC-ENVIPE-SERIE-*`, que siguen sin RESULT en `data/corrida0` (confirmado arriba: sin apariciones) — la premisa de RESERVADA del encargo se sostiene.

## 4 · YA HECHO / YA DECIDIDO
`ls -d data/corrida0/CALC-DUELO-ENVIPE2026-MARGINALES*` → 0; `grep -c "MARGINALES-2" forense/encargos/*` → 0. Ramas vivas: ninguna al redactar; **no correr a la vez que E14** (derivados).

## 5 · PIEZAS
- **COMMIT-1:** spec congelada: universo de celdas (las reservadas con serie), pisos t−1 citados por id de RESULT 2025, TENDENCIA-SERIE con su fórmula y ventana (la de 852f), criterio de adjudicación con las condiciones `INDECIDIBLE` verbatim y la comparación primaria = diferencia de error medio con IC por réplica (v2.16 §4), vocabulario `VENCE-AL-PISO / PROPUESTA-CON-RESERVA / NO-VENCE / C-PISO-ADOPTADO`, B-bis; guardián `reservada=True` heredado; verificación por texto del FD 2026. `spec-check` VERDE; D-22 sintético.
- **COMMIT-2:** emisiones ciegas (pisos y tendencia por celda, IC por réplica); sello, asiento; test de historial (sin lectura de 2026).
- **COMMIT-3a:** sha de emisiones en la spec de adjudicación. **COMMIT-3:** R 2026 por el CALC congelado; adjudicación; cobertura por celda y por conglomerado con intervalo binomial; rótulo PROSPECTIVA; fila de consumo de reserva **con la lista de lo que sigue reservado**; celda/marcador para su dueño.
- «si `[SUPUESTO]` resulta falso»: por celda, NO-CONSTRUIBLE; el duelo sigue con las demás.

## 6 · LATITUD
DECIDES TÚ: qué series entran (solo las selladas hasta 2025), orden, cableado D-18. PREGUNTAS A MESA (y sigues hasta 3a): si TENDENCIA-SERIE no está como herramienta reutilizable sino solo dentro de un CALC, ¿se extrae a `tools/duelo/` (recomendado, ≤ 40 líneas, con test contra el CALC que la selló) o se cita por spec? NO DECIDES: §7.

## 7 · PAROS
**a) cualquier lectura de `envipe2026_csv` fuera del CALC de adjudicación en COMMIT-3 — scratch incluido** · b) editar lo congelado o forzar · c) adoptar · d) cambiar estimando, umbral, candidatos o B-bis tras COMMIT-1 · e) nube · f) inalcanzable · g) código congelado no corre.

## 8 · COMPUERTAS
«`preflight` VERDE con `envipe2026_csv` COINCIDE — protege: congelar spec.» «Firma de §2 presente y emisiones en `origin` — protege: abrir dato (COMMIT-3).» «No hay otro acto de caja en vuelo — protege: borrar.»

## 9 · PERÍMETRO
Propio: `forense/prereg-caja/DUELO-ENVIPE2026-MARGINALES-spec-v1_0.md` (+ sidecar, yaml) · los dos CALC nuevos · `tools/duelo/tendencia_serie.py` (si §6) + test · derivados por comando · `replay-evidencia.tsv` · `decisiones.tsv` (una fila) · nota · `canon/L0/<raíz>.md`. Ajeno: los CALC del duelo 1, `tramite.yaml`, el árbitro, el marcador (su dueño consume). «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · NO HACE · SUCESORES · CIERRE
No adopta, no toca cruces (no hay marginales de cruce aquí), no abre lo que no emite. Sucesor: el marcador consume las coberturas PROSPECTIVA; MARGINALES-ADOPCION-3 (ENVIPE 2026) por firma. Auditoría: la spec la trae; la nota la contesta sobre el resultado. Cierre por /acto.


