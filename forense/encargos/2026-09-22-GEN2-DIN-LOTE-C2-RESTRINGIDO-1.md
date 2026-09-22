# ENCARGO · ACTO GEN2-DIN-LOTE-C2-RESTRINGIDO-1 · Piso para los cinco pares con `formalidad` del lote ENIF 2024: un C2 restringido a quien trabaja, sellado aparte con su universo, como la Q1 de COMMIT-1 preveía

> ENTORNO: **CAJA** — abre ENIF 2024 solo para los marginales del universo restringido. Hook; si no coincide, PARA.

CABECERA · SHA `ccd7c0eb` · una sola sesión · MODELO: Opus · MODO: **RÍGIDO** desde COMMIT-1 · CONTADOR: +1 corrida sellada y registrada, `cuenta_gen2 = SI`, **no adopta**; da piso a 5 pares (celdas: las que la spec derive) → `celdas_validadas` puede subir cuando el lote los evalúe (no aquí) · CALC-id reservado: `CALC-C2-RESTRINGIDO-IC-ENIF2024-0001` · ids raíz de acto.

## 1 · OBJETIVO
Que los 5 pares `formalidad × {sexo, edad, escolaridad, localidad, cuenta_formal}` —hoy `NO-EMITIBLE` en el C2 compuesto por universo restringido (A-bis 4)— tengan piso: marginales **del universo de quien trabaja** (`P3_13` válido), forma log-aditiva, réplicas, IC, escala declarada, **universo restringido escrito en cada RESULT**. Habilita: que el lote ENIF 2024 evalúe 14/14 pares y no 9. «Hecho» = `verify CALC-C2-RESTRINGIDO-IC-ENIF2024-0001` → `REPRODUCE`; cada RESULT lleva `universo = trabajadores (P3_13 ≠ blanco/9), cobertura declarada`; ninguna comparación con el marginal poblacional en el CALC (A-bis 4).

## 2 · FIRMAS DE MESA
- `FP-260921-GEN2-DIN-LOTE-ENIF2024-COMMIT-2-3-8e53-02`, opción **B** — *propuesta de dirección, mesa sella o borra*: «Los 5 pares NO-EMITIBLE por universo restringido de formalidad se sellan aparte con un C2-restringido a quien trabaja, con su universo declarado en cada RESULT, nunca comparado contra el marginal poblacional.» Sin texto → PARA.
- Cita, ya sellada: `FP-260921-…-COMMIT-1-6c10-02` (Q1) registra el hallazgo: «C2 sellado cubre 9 de 14 pares (68 celdas); formalidad×… NO-EMITIBLE en el dictamen sellado».

## 3 · LO QUE DIRECCIÓN SABE
- `[LEÍDO]` FP `…6c10-02` y `…8e53-02` (texto de arriba). `[EXISTE]` `data/corrida0/CALC-C2-COMPUESTO-IC-ENIF2024-0001/` — no sé en qué archivo vive el dictamen `NO-EMITIBLE` (`grep -c NO-EMITIBLE resultados.json` → 0): **el acto lo localiza por objeto** (dictamen del CALC, nota de cierre del lote).
- `[LEÍDO]` crosswalk fila `formalidad`: árbitro corta por ENIF `P3_13`, universo trabajadores, cobertura 0.689676 (`FP-376`).
- `[SUPUESTO]` Los marginales restringidos por eje (sexo, edad, escolaridad, localidad, cuenta_formal **dentro de** quien trabaja) no están sellados. Si resultara que sí (un CALC del lote los trae), el acto los cita como oro y solo compone.
- ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
`ls -d data/corrida0/CALC-C2-*` → reporta; `grep -rl "C2-RESTRINGIDO\|C2 restringido" forense/ data/corrida0/` → al redactar solo las dos FP. Ramas vivas: ninguna.

## 5 · PIEZAS
- **COMMIT-1:** spec congelada: universo (`P3_13` por texto en el FD 2024), los cinco pares y sus categorías idénticas al lote, marginales restringidos a derivar, forma `expit(logit p(a|T) + logit p(b|T) − logit p(T))`, réplicas, seed, tolerancias; **prohibición explícita** de derivar cruces (solo marginales del universo T); D-22 sintético.
- **COMMIT-2:** marginales restringidos + composición + IC; registro y asiento en el mismo acto (E.7).
- **P3:** nota: qué pares quedan con piso; qué pierde el marcador por segmento si consume estos pisos (universo restringido no reconciliable con el poblacional, A-bis 4) — para que el lote lo lea al evaluar.
- «si `[SUPUESTO]` resulta falso»: dicho arriba.

## 6 · LATITUD
DECIDES TÚ: cómo derivar los marginales restringidos (misma receta que el árbitro, `FAC_PER`, `EST_DIS`/`UPM_DIS`), nombres, orden, ≤ 10 líneas adyacentes. PREGUNTAS A MESA: si `cuenta_formal × formalidad` resulta degenerado (colineal por definición), ¿se declara `NO-CONSTRUIBLE` (recomendado) o se emite? — y sigues. NO DECIDES: §7.

## 7 · PAROS
a) derivar un cruce de ENIF 2024 (solo marginales) · b) editar el C2 compuesto o forzar · c) adoptar · d) cambiar forma/universo congelados · e) nube · f) inalcanzable · g) código congelado no corre.

## 8 · COMPUERTAS
«Firma B presente — protege: congelar spec.» «No hay otro acto de caja en vuelo — protege: borrar (derivados compartidos).»

## 9 · PERÍMETRO
Propio: `forense/prereg-caja/C2-RESTRINGIDO-ENIF2024-spec-v1_0.md` (+ sidecar, yaml) · `data/corrida0/CALC-C2-RESTRINGIDO-IC-ENIF2024-0001/` · derivados por comando · `replay-evidencia.tsv` · nota · tablero · `canon/L0/<raíz>.md`. Ajeno: `CALC-C2-COMPUESTO-IC-ENIF2024-0001` (lectura), los CALC del lote, `milpa/`. Otro acto en vuelo: ninguno verificado; no correr a la vez que E1/E3. «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · NO HACE · SUCESORES · CIERRE
No evalúa los pares (eso es el lote), no adopta, no compara contra el poblacional. Sucesor: el lote ENIF 2024 consume estos pisos en su siguiente evaluación. Auditoría: no aplica. Cierre por /acto.
