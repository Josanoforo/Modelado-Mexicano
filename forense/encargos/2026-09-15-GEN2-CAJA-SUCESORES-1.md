# ACTO GEN2-CAJA-SUCESORES-1 · lo que RELEVO y FIRMAS no pudieron cerrar sin corpus

Encargo de mesa, 15/sep/2026, CAJA (Opus dispacha; ejecuta esta sesión de
CAJA). Archivado verbatim (0-bis A.3) por el propio acto.

---

CAJA · ACTO GEN2-CAJA-SUCESORES-1 (Opus; lo que RELEVO y FIRMAS no pudieron cerrar sin corpus)

P1 · NC-0211 — corrida0.py registro --verifica --escribe en caja, sobre main fresco: es lo que materializa el relevo en el registro derivado; sin esto el 207 no baja aunque se firme todo.
P2 · NC-0215 — adopción sucesora: declarar el pin por CALC y correr tools/relevo_usos.py + corrida0 delta (la regla de bloque ya está sellada; esto es su ejecución en el entorno que puede).
P3 · NC-0169 — ENSANUT: corrida0 con corpus montado hasta que RES-0063/0064 emitan (el registro existe; la emisión no).
P4 · NC-0208 — relanzar el runner F5 apuntando al verificador v1.2 hasta que --verify imprima OK (como v1.1 hizo con v1.0). Sin llamadas: solo verify.
Opcional si sobra sesión: NC-0202 (re-intentar el curl/WebFetch que nube no pudo). Firma de contador embebida. Perímetro: registro derivado, usos, F5 runner; no toca milpa ni cola.

## NO-CORRIDO / RESERVAS

Dos filas: la adopción del bloque `REPRODUCE` que P2/P3 pinearon, y un
hallazgo colateral que la re-derivación de P2 sacó a la luz.

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| adopción en `milpa/tramite.yaml` de los 9 slots `REPRODUCE` (P2/P3: RES-0036/0037/0038/0045/0050/0051/0052/0063/0064) | `FUERA-DE-PERIMETRO` — el encargo dice «no toca milpa ni cola» | `dependencias_numericas_legacy_activas` se queda en 189 hasta que un acto con `milpa/` en su perímetro escriba las 9 citas; RES-0043/0044 (`CALC-EDER-0003`) quedan `NO-APLICA-ESTIMANDO-DISTINTO`, presentados a mesa | `NC-0243` |
| conflicto de procedencia RES-0047/RES-0049 (`CALC-ENIF-0001` vs `CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1`) | `CONFLICTO-DE-PROCEDENCIA-SIN-DISCREPANCIA-NUMERICA` — hallazgo colateral de re-derivar `relevo_usos.py`, no pedido por el encargo | ninguno sobre la cifra adoptada (idéntica en ambos CALC); queda sin resolver cuál CALC es la fuente canónica del pin | `NC-0244` |

## CONSUMIDO

Ejecutado por **`PR #800`** (`ACTO GEN2-CAJA-SUCESORES-1`, 15/sep/2026, CAJA),
rama `acto/gen2-caja-sucesores-1`, sobre `origin/main = 0cdbd72` al arrancar
(merge de `PR #789`). **ADR-521.** Cierre en
`forense/notas/2026-09-15-GEN2-CAJA-SUCESORES-1-cierre.md`.

Las cuatro `NC` (0211, 0215, 0169, 0208) se cierran; el opcional (0202) se
declara sin cerrar `NC-0156`. Perímetro respetado: cero adopción en
`milpa/`, cero edición de `spec.yaml` sellado. Abre `NC-0243`/`NC-0244`.
La rama absorbió tres merges de `origin/main` durante el acto (la más
activa: `0cdbd72` → `d762730`); cada uno se re-verificó con
`tests/check.py --baseline` en árbol limpio antes de continuar.

`tests/check.py --baseline`: **LÍNEA BASE VERDE.**
