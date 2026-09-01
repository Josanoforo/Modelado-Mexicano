ENCARGO · MAESTRA33-E9 · L-SPEC-v1_1 — invoca /acto
SHA de redacción: a71c9ea. ENTORNO: NUBE — NO CAJA. COMPUERTA: ninguna. MODELO SUGERIDO: Opus.
FIRMA DE MESA (verbatim, 1/sep/2026): "dame los siguientes encargos" — habilita la corrida L que mesa ejecuta fuera del proyecto (D-iii).
A.8 (dirección contra a71c9ea): pipeline-L-adv1-m2.py EXISTE, sellado, escrito para el marco piloto (ids CIV-08…); corridas-L: 120 archivos, 0 del marco-M. Spec L para las 11 celdas v1_1: NO-ENCONTRADO (ls prereg-duelo-v2/ → 0 archivos L-spec*).
P1 · forense/prereg-duelo-v2/L-spec-v1_1.json + .sha256: para las 11 celdas de marco-M-sorteado-v1_1, la pregunta L derivada MECÁNICAMENTE de las columnas conducta, universo, encuesta, ola y escala del marco (sellado antes de que existiera R) — sin texto redactado a mano, sin cifra alguna de corridas-R ni del scoreboard. Declara en cabecera: "al congelar esta spec existían R para 4 celdas (CIV-M-01/06/08/09); ninguna cifra de R entra en la spec ni en los prompts; el modelo L es externo y no ve este repo".
P2 · Cargador propio que alimenta pipeline-L-adv1-m2.py SIN editarlo (mismo patrón que sorteo_v2), con las dos variantes L-solo / L+corpus, k, temperatura y agregado pre-registrado que el script fija — no se cambia ninguno; salida esperada corridas-L/L-<id>-M__<variante>__<k>.json con el esquema de los existentes.
P3 · forense/prereg-duelo-v2/PAQUETE-L-v1_1.md: los comandos exactos que mesa corre en sesión limpia fuera del proyecto (modelo, versión, fecha, temperatura, k), qué archivos produce, cómo los trae al repo (PR "[L] corridas v1_1", que el revisor comenta), y la prohibición de abrir corridas-R o el scoreboard durante la corrida.
PERÍMETRO: L-spec-v1_1.json/.sha256, el cargador (tools/ o prereg-duelo-v2/), PAQUETE-L-v1_1.md, notas, tablero (recibo), A.3, cascada. Frase exacta de perímetro vigente. FP/ADR: deriva. CONTADOR: cero (spec), declarado.
LO QUE NO HACE: NO ejecuta L (ni una celda); no edita el pipeline sellado; no abre corridas-R/ ni scoreboard-v1_1.md (lista archivos abiertos al cierre).

## CONSUMIDO

Ejecutado por `ACTO MAESTRA33-E9 · L-SPEC-v1_1`, 1/sep/2026, `ADR-254`
(candidato). PR contra `main`: `PR #427` (título `[MAESTRA33-E9] L-spec-v1_1`,
sin fusionar por este acto). P1/P2/P3 entregados tal como se pidieron;
CONTADOR cero (ninguna celda `L` corrida); `corridas-R/` y
`scoreboard-v1_1.md` nunca abiertos (solo `ls`, para confirmar los 4 `R`
existentes declarados en la cabecera de `L-spec-v1_1.json`). Detalle:
`forense/notas/2026-09-01-l-spec-v1_1-cierre.md`.
