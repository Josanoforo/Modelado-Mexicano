---
description: Censa el universo de un marco-M-sorteado contra corridas-M/R/L y arma la entrada de scoring-adv1-m3.py (sin editarlo). Uso — /score [sufijo del marco, default v1_1]
argument-hint: [v1_1 | v1_0 | ...]
---

# `/score` — censa, no puntúa por sí mismo

Creada por `ACTO MAESTRA33-E8 · SCORE-M-1` (1/sep/2026). Invoca
`tools/score_marco_m.py`, que:

1. Lee `forense/prereg-duelo-v2/marco-M-sorteado-<sufijo>.tsv` (default
   `v1_1`) como universo de celdas.
2. Para cada celda, censa disponibilidad real en el árbol —
   `forense/prereg-duelo-v2/corridas-M/M-<id>.json` (`estado_M ==
   "EMITE"`), `corridas-R/<id>.json` (`estado == "COMPUTADO"`),
   `corridas-L/<id>__L-*__*.json` (≥1 archivo) — sin inventar ni
   re-derivar ninguno de los tres.
3. Excluye del cómputo de puntuables toda celda con `grado_DD` marcada
   `VERIFICACION-NO-PUNTUA` (F-DD, `ADR-237`) y la lista aparte; un marco
   sin columna `grado_DD` (esquema anterior a F-DD) se censa igual, con
   `schema_con_grado_dd: false` declarado.
4. Marca **puntuable** solo la celda con **R presente, más al menos uno
   de M o L** — si falta R, no puntúa aunque tenga M o L.
5. Construye la `entrada.json` de
   `forense/prereg-duelo-v2/scoring-adv1-m3.py` (sellado, nunca editado
   por esta skill): `corredores_activos` = `{(L,solo):1,(M,principal):1}`
   (contrato F1), `nivel_ic=0.95`/`seed=42` (`FP-168`, FIRMADA
   30/ago/2026), `delta` **deliberadamente ausente** — sigue sin cita
   como escalar único de corrida (`procedimiento-scoring-v1_0.md` §3); si
   mesa lo sella, se agrega ahí, no aquí. Las celdas puntuables entran con
   `mediciones: {}` (sin baseline `B` no hay `skill` normalizada legítima
   que poblar, mismo hallazgo de `E9`/`ACTO MAESTRA30-E9`).

## Uso

```
python3 tools/score_marco_m.py                    # marco-M-sorteado-v1_1.tsv
python3 tools/score_marco_m.py --marco v1_0        # marco-M-sorteado-v1_0.tsv
python3 tools/score_marco_m.py --json salida.json  # documento completo a archivo
```

La salida es un documento JSON con `n_celdas_universo`,
`n_verificacion_no_puntua`, `n_puntuables`, el censo celda por celda
(`censo`) y la `entrada_scoring` lista para pasarse a
`scoring-adv1-m3.py` si mesa sella `delta`.

Para producir un tablero legible en Markdown a partir de esta salida
(el patrón de `forense/prereg-duelo-v2/scoreboard-v1_1.md`), correr el
script y volcar el censo a una tabla — esta skill no escribe el
`.md` por sí misma, deja eso al acto que la invoque con fecha propia.

## LO QUE NO HACE

No edita `scoring-adv1-m3.py`. No emite `M`, `R` ni `L` — solo lee lo
que ya existe. No inventa `delta`. No activa el corredor `E`. No cambia
la Configuración sellada (`FP-168`, `M-ENLACE=A`, `M-AGREGA=a′`).
