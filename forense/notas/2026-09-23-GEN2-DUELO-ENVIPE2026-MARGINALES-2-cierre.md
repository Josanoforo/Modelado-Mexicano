# GEN2-DUELO-ENVIPE2026-MARGINALES-2 · cierre

Encargo: `forense/encargos/2026-09-22-GEN2-DUELO-ENVIPE2026-MARGINALES-2.md`
(sello de cuerpo `eaf54ead…`). ADR raíz: `ADR-260922-GEN2-DUELO-ENVIPE2026-MARGINALES-2-0f2c-01`.
Modelo: Sonnet 5 (encargo sugería Opus; decisión explícita del usuario,
confirmada por pregunta directa antes de tocar cualquier archivo).

## 1 · Universo — verificado, no supuesto

El encargo proponía nueve celdas. Verificado contra el árbol
(`forense/prereg-caja/DUELO-ENVIPE2026-MARGINALES-spec-v1_0.md` §0):

- `civico.denuncia.con_seguro × sexo` y `× edad`: **NO-CONSTRUIBLE**.
  Ningún `RESULT` con esos ejes existe para `con_seguro` en ningún CALC
  del árbol (`milpa/tramite-ola5-propuesta-v0.yaml:1993-2033` declara
  `ejes_ausentes: "ninguno adicional propuesto"`; confirmado en las 116
  llaves de `CALC-ARBITRO-MARGINALES-ENVIPE2025-0001/resultados.json`).
- `civico.denuncia.con_seguro` nacional: piso 2025 existe y se cita, pero
  **el retador es NO-CONSTRUIBLE** — `CALC-PISOS-ENVIPE2024-EJES-0002`
  nunca computó el total nacional para esta regla (sólo los dos ejes de
  cobertura), así que sólo hay un punto sellado (2025) y TENDENCIA-SERIE
  exige ≥ 2.
- «Demás reglas ENVIPE con serie sellada (`CALC-ENVIPE-SERIE-*`)»: **0**.
  Es una sola regla (`p_c1_u1`/no-denunciado), ya adjudicada por completo
  en `GEN2-DUELO-ENVIPE2026-EJECUCION-1` COMMIT-3.
- `civico.denuncia.con_seguro × cobertura_seguro` (asegurado,
  no_asegurado): **construibles** — exactamente 2 olas selladas cada
  una (2024, 2025), el mínimo exacto que exige TENDENCIA-SERIE.

## 2 · §6 del encargo — decisión y ejecución

TENDENCIA-SERIE vivía sólo dentro de `tools/encig_origen_movil.py`
(`PISOS = ("PERSISTENCIA", "TENDENCIA-2", "TENDENCIA-3",
"TENDENCIA-SERIE")`), no como herramienta reutilizable. Pregunta a
usuario vía `AskUserQuestion`; respuesta: «Extraer a tools/duelo/
(recomendado)». Extraída a `tools/duelo/tendencia_serie.py` (41 líneas).
`tests/test_tendencia_serie.py` reproduce byte a byte (delta ≤ 1e-9) el
piso sellado de `CALC-ENCIG-ORIGEN-MOVIL-0001` en las cuatro olas donde
es construible (2019, 2021, 2023, 2025, celda nacional).

## 3 · Cableado corregido (D-18)

La spec humana §3 citaba `tools/celda_d/marginales_reproduccion.py::
carga_ola()` como el guardián `reservada=True` a heredar. Al escribir
`ADJUDICACION-0001` se encontró que esa función está hard-codeada al
universo de `evasión_norma` (`COLUMNAS_TMOD` no trae `BPCOD` ni
`BP2_1`): no sirve para `con_seguro`. Extenderla habría requerido su
propia firma de mesa (precedente: `GEN2-GUARDIAN-ENVIPE-EJES-IC-1`,
20/sep/2026, «2 si extendemos») — fuera de alcance de este acto.
Corrección: `ADJUDICACION-0001` trae su propia
`carga_universo_con_seguro()`, código nuevo que reutiliza sólo la
utilidad genérica `_lee_miembro` (encoding utf-8/latin-1, normalización
de `\r`) sin tocar el archivo ajeno ni su guardia. Declarado en
`spec.yaml::etiquetas.cableado_nota` y en el commit de COMMIT-3a; no
toca estimando, umbral, candidatos ni B-bis (D-18).

## 4 · Adjudicación — genérica, reutilizada

`tools/duelo/cruces_familia.py::adjudica()` ("no sabe qué es ENVIPE")
recibió `R` real y los dos candidatos (piso, retador) como `Celda` con
sus réplicas bootstrap, y devolvió `ΔMAE`/IC95/veredicto sin que este
acto reimplementara la comparación. El bootstrap de UPM-en-estrato de
`R` usa la misma receta que `wprop_ic_conglomerado`
(`tools/calibracion_mordida_encig_serie.py`) — verificado por igualdad
EXACTA del vector de réplicas (no sólo percentiles cercanos) en
`tests/test_duelo_envipe2026_marginales_adjudicacion.py`. El vocabulario
de `adjudica()` (`VENCE-RETADOR`/`PROPUESTA-CON-RESERVA`/`NADIE-VENCE`/
`NO-ADJUDICABLE`) se mapeó al de la spec-v1_0.md §3
(`VENCE-AL-PISO`/`PROPUESTA-CON-RESERVA`/`NO-VENCE`/`C-PISO-ADOPTADO`/
`INDECIDIBLE`), distinguiendo `NO-VENCE` de `C-PISO-ADOPTADO` por el
signo del punto de `ΔMAE` dentro del bucket "IC cruza cero".

## 5 · Resultado

| celda | R 2026 [IC95] n | piso 2025 (error) | retador (error) | ΔMAE pp [IC95] | veredicto |
|---|---|---|---|---|---|
| asegurado | 0.813647 [0.774077,0.848569] n=348 | 0.790906 (−2.27pp) | 0.806814 (−0.68pp) | +1.591 [−11.111,+6.121] | `NO-VENCE` |
| no_asegurado | 0.683494 [0.651727,0.713947] n=466 | 0.672014 (−1.15pp) | 0.708324 (+2.48pp) | −1.335 [−10.070,+4.469] | `C-PISO-ADOPTADO` |

Con `n≈350-460` delitos por celda el bootstrap es ancho; ningún `ΔMAE`
despeja el umbral heredado de 0.5pp en ningún sentido. `R` cae dentro del
IC95 tanto del piso como del retador en las dos celdas (cobertura, no
vencimiento — reportado por separado, sin colapsar, per v2.16 §4).

## 6 · Verificación de «hecho» (encargo §1)

- Tres commits en orden: ✓ (`tests/test_duelo_envipe2026_marginales_historial.py`,
  `merge-base --is-ancestor` sobre los SHA reales).
- `verify` REPRODUCE en los dos CALC: ✓ (`CONTEXTO=IDENTICO` en ambos).
- Ningún acceso a `envipe2026_csv` antes de COMMIT-3: ✓ (mismo test;
  `EMISIONES-0001/medidor.py` no importa `zipfile` ni cita
  `envipe2026_csv`).
- Veredicto por celda con vocabulario cerrado: ✓.
- `decisiones.tsv` con la fila que consume exactamente lo emitido:
  ✓ (`reserva:envipe2026-consumida-por-duelo-marginales-2`).

## 7 · Firma de mesa §2

`FP-260922-GEN2-DUELO-ENVIPE2026-MARGINALES-2-b05c-01`: mesa selló
verbatim el texto propuesto por dirección el 22/sep/2026, autorizando
`CALC-DUELO-ENVIPE2026-MARGINALES-ADJUDICACION-0001` como único código
para la lectura de la reserva restante de ENVIPE 2026 de este acto.

## 8 · Colisión de depósito, no de ejecución

`origin/main` (PR #1016, `[COLA] TANDA-5-ENCARGOS-C`) ya tenía un
depósito **sin sellar** del mismo `.md` de encargo (con un apéndice
mecánico T-YAMEDIDO que el mío no trae — añadido al archivar por esa
sesión, "no es texto de dirección"). Verificado: ningún `CALC-DUELO-
ENVIPE2026-MARGINALES-*` ni `.cuerpo.sha256` existía en `origin/main`
antes de este acto — el depósito de la COLA nunca se ejecutó
(su propio PR lo declara: "Ninguno se ejecutó"). Resuelto el conflicto
de merge manteniendo mi versión sellada (`SELLO_COINCIDE`, candidato
`archivo-entero`, verificado con `sella_sha256.py --verifica --cuerpo`
tras el merge) — el sello nunca se toca para hacer pasar un verificador
(A.3). `tests/check.py --baseline` corrió VERDE después del merge.

## 9 · Suite

`python3 tests/check.py --baseline` → **VERDE, 0 FAIL** (ver salida
cruda en el commit de cierre).
