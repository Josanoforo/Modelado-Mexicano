# ENCARGO · ACTO GEN2-TUBERIA-RUTINAS-AUTOMERGE-1 · Los cuatro PR diarios de rutina fusionan solos cuando la suite está VERDE y tocan solo sus archivos — mesa deja de ser el botón de la máquina

> ENTORNO: **NUBE**. Hook; si no coincide, PARA.

CABECERA · SHA `3f48be30` · una sola sesión · MODELO: Opus (CI + regla de clases: P5 del plan) · MODO: **ABIERTO** · CONTADOR: cero mediciones; PR de rutina por día que esperan a mesa: 4 → 0 (medido en la semana siguiente) · ids raíz de acto.

## 1 · OBJETIVO
Que los PR de las rutinas diarias (`derivados/*`, `censo/*`, `adq/*`, `claude/tramite-*` digesto/despacho) se fusionen sin mesa cuando (i) la suite está VERDE por FAIL, (ii) el diff toca **solo** los archivos que esa rutina tiene declarados, (iii) no tocan sellos ni tablero, y (iv) la huella en `forense/rutinas.tsv` existe. Todo lo demás sigue exigiendo merge humano. «Hecho» = `forense/rutinas-clases-v1_0.tsv` con una fila por rutina (`rama · archivos permitidos · condición`); un job de CI que, cumplidas las cuatro condiciones, fusiona con el mensaje `[auto-merge rutina]` y falla en voz alta si una rutina toca un archivo fuera de su clase; prueba con un PR sintético de cada clase; los cuatro PR del día siguiente entran solos (`git log --merges` con ese mensaje).

## 2 · FIRMAS DE MESA
*Propuesta de dirección (P5 del plan, «clases de auto-merge»), mesa sella o borra:* «Las rutinas diarias fusionan solas bajo las cuatro condiciones de §1; cualquier PR que no sea rutina, o una rutina que toque un archivo fuera de su clase, sigue exigiendo mi merge.» Sin texto → PARA (nada que instalar).

## 3 · LO QUE DIRECCIÓN SABE
- `[EJECUTADO]` Merges de rutina en los últimos 4 días: `derivados/2026-09-1[89]`, `-22`, `censo/…`, `adq/…`, `claude/tramite-…` — cuatro por día, todos fusionados a mano por mesa; cada uno toca 1–2 archivos propios (`data/curacion-universo/derivados/`, `forense/censo/`, `data/curacion-registro/cola-adquisicion-registro.tsv`, `forense/digesto/`, `forense/rutinas.tsv`). `[LEÍDO]` `.github/workflows/verify.yml` tiene guardas de enrutamiento de PR (`enrutamiento-pr`) y el job de push a `main`; no hay auto-merge.
- `[SUPUESTO]` El repositorio permite merge por token de Actions con la protección de rama actual (mesa no ha contestado 8e53-04). Si resulta falso, el acto deja el job listo y una línea para mesa: qué permiso falta.
- ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
`grep -n "auto-merge\|automerge" .github/workflows/*.yml` → 0; NC `TUBERIA-CIERRE-SIN-CHOQUE-2-8e53-04` (protección de rama) ABIERTA. Ramas vivas: E11 y METRICA-RECTORA pueden tocar `verify.yml` — este acto añade un workflow **propio** (`automerge-rutinas.yml`), no edita `verify.yml`.

## 5 · PIEZAS
- **P1 · Clases.** `forense/rutinas-clases-v1_0.tsv`: rutina · patrón de rama · archivos permitidos (glob) · qué NO puede tocar (sellos, tablero, `milpa/`, `tools/`). Derivado de los diffs reales de los últimos 10 PR de cada rutina, no de memoria.
- **P2 · Job.** Workflow propio disparado por `pull_request` de esas ramas: comprueba las cuatro condiciones por comando; fusiona; si falla una, comenta el PR con la condición que falló y no fusiona. Test con PR sintético por clase (uno que cumple, uno que toca un archivo prohibido).
- **P3 · Huella y regla.** Línea en `hallazgos.md` (`PARA-v2.17`): «una rutina que toca fuera de su clase no es rutina: es un acto y pasa por mesa». Nota con la tabla de clases y el permiso de GitHub que exige.

## 6 · LATITUD
DECIDES TÚ: nombre del workflow, cómo comprobar «solo sus archivos». PREGUNTAS A MESA: ¿el auto-merge aplica también al carril Codex descriptivo (`codex/*` con recibo automático)? Recomendación: **no** por ahora — Codex no escribe tablero y su recibo es humano. NO DECIDES: §7.

## 7 · PAROS
a) no aplica · b) fusionar algo que toque sellos o tablero · c) no aplica · d) no aplica · e) caja · f) inalcanzable (permiso de GitHub) → el entregable es decirlo.

## 8 · COMPUERTAS
«Prueba con PR sintético en rama antes de activar — protege: borrar (un auto-merge mal acotado es un borrado sin ojos).»

## 9 · PERÍMETRO
Propio: `.github/workflows/automerge-rutinas.yml` (nuevo) · `forense/rutinas-clases-v1_0.tsv` (nuevo) · `tests/test_rutinas_clases.py` (nuevo) · `forense/hallazgos.md` · nota · `canon/L0/<raíz>.md`. Ajeno: `verify.yml`, sellos, tablero. «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · NO HACE · SUCESORES · CIERRE
No fusiona actos, no toca Codex, no cambia la política de cero ramas. Sucesor: P5 completo (clases para recibos Codex) si mesa lo quiere. Auditoría: no aplica. Cierre por /acto.


