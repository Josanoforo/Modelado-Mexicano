# Sorteo del marco-M v1.2 — `ACTO MAESTRA34-N2 · MARCO-M-v1_2` (P2), resultados

## Pre-registro del primer commit (antes de correr el PRNG)

- **`SHA_A` derivado, no heredado.** El encargo lo fija por construcción:
  `semilla_desde_sha_merge(<SHA del merge de MAESTRA34-N1>, "MARCO-M-v1_2")` —
  *"deriva, no heredes"*. `SHA_A = ec3cf0f2d98346205fafa7ece756ca5875cb5707`,
  verificado: `git log -1 --format="%H %s" ec3cf0f` →
  `ec3cf0f2d98346205fafa7ece756ca5875cb5707 Merge pull request #449 from
  Josanoforo/claude/maestra34-n1-launch-z95iaw`, que es el merge de
  `MAESTRA34-N1` — el mismo cuya fusión abre la compuerta de este acto.
- **`scope_id = "MARCO-M-v1_2"`** (dado literal por el encargo). Distinto de
  `"MARCO-M-v1_1"`, `"MARCO-M-v1"` y `"ACT-PIL-3-v1"`, así que la semilla no
  puede coincidir con ninguna anterior por construcción (§3.4 del reglamento).
- **Semilla**: `sorteo_v2.semilla_desde_sha_merge(SHA_A, "MARCO-M-v1_2")` —
  misma función sellada (`sorteo_v2.py:191`, `ADR-178`/`FP-150`), importada sin
  editar vía `sorteo_marco_m_v1_1.py` → **`34240453437400889519083420438742062585`**.
- **`N_elegibles`**: leído de `CONGELADO-M-v1_2.sha256` → `N_elegibles=27`.
  `sha256` recomputado de `marco-M-congelado-v1_2.tsv`
  (`a6d6e94c9402dc2096da31a1c7aa6f57e7273148bce3dae02fdcc90f7a5a0208`) coincide
  byte a byte con el declarado ahí. **Control PASA** — sin este control no hay
  corrida.
- **Cargador: ningún módulo nuevo.** `marco-M-congelado-v1_2.tsv` conserva el
  nombre de columna `elegible_v1_1` (el encargo exige "columnas idénticas"), así
  que `sorteo_marco_m_v1_1.cargar_marco_m_v1_1(ruta=…, ruta_sha=…)` — que ya
  acepta rutas por parámetro — lo lee tal cual, con su verificación de `sha256`
  y su `assert len(filas) == N_elegibles`. No se edita ni se duplica
  `sorteo_v2.py`, `sorteo_v3.py`, `sorteo_marco_m.py` ni
  `sorteo_marco_m_v1_1.py` (precedente `ADR-178`).
- **Mecanismo: `sorteo_v3`, no `sorteo_v2`.** El encargo lo fija
  (*"sorteo_v3 bajo reglamento v1.1"*). Es el cambio real frente a `v1_1`, que
  delegó en `sorteo_v2.sortear`: `sorteo_v3.sortear_v3` reparte asientos con
  **piso 1 por estrato no vacío** + Hamilton sobre el resto
  (`asignar_asientos_proporcional_v3`), en el reparto inicial *y* en el fallback
  de infactibilidad.
- **Regla de tamaño** (`ADR-231` §e, fijada por `MAESTRA32-E13` antes de ver
  ningún `N`; misma función `regla_de_tamano`, no editada): `N≥30 → n_sorteo=15`;
  `15≤N<30 → n_sorteo=ceil(N/2)`; `N<15 → sin sorteo`. Con `N_elegibles=27`:
  **`n_sorteo = ceil(27/2) = 14`**; **`cuota_max = floor(0.20·14) = 2`**.
  `27 ≥ 15`: el PRNG **sí** corre.
- **Estratos, leídos del congelado (no reclasificados aquí).** Dos no vacíos:
  `PENDIENTE` (26 filas) y `tramite|P1|MEDIA` (1 fila, `TRA-M-02`). Las 5 filas
  nuevas elegibles (`FAM-M-03`..`FAM-M-07`) entran a `PENDIENTE`, que es lo que
  hacen todas las celdas de transferencia censadas desde `MAESTRA32-E15` — este
  acto **no** inventa una estratificación mejor, igual que `v1_1` no lo hizo.
  `publicada=SI` en 0 de 27, así que la cuota no puede morder (`0 ≤ 2`).
- **Reparto de asientos que la regla 3 obliga, calculado antes de la corrida.**
  `n_sorteo=14 ≥ n_estratos_no_vacios=2` → aplica la primera cláusula (la
  segunda, no implementada en `sorteo_v3.py`, no se alcanza y no se aproxima en
  silencio). Piso 1 a cada estrato; `resto = 14−2 = 12`; cuotas exactas del
  resto `PENDIENTE = 12·26/27 = 11.5556`, `tramite|P1|MEDIA = 12·1/27 = 0.4444`;
  pisos `11` y `0`; `restantes = 1` al de mayor fracción (`PENDIENTE`, `.5556`).
  **Asientos esperados: `PENDIENTE = 13`, `tramite|P1|MEDIA = 1`.** Ningún
  estrato no vacío en cero — que es justo la invariante que el encargo manda
  verificar (*"Ningún estrato no vacío sin asiento — si ocurre, PARO: bug de v3,
  es entregable"*).
- **Clasificación F-DD por celda**: ya congelada en la columna `grado_DD` de
  `marco-M-congelado-v1_2.tsv` (P1). No se re-deriva aquí — sería redescubrir lo
  que el sello de P1 ya adjudicó. Este acto **reporta** el `grado_DD` real de
  cada celda sorteada, no lo asume.
- **Invocación exacta a ejecutar:**
  ```python
  import importlib.util, sys
  from pathlib import Path
  D = Path("forense/prereg-duelo-v2").resolve()

  def _load(nombre, archivo):
      spec = importlib.util.spec_from_file_location(nombre, D / archivo)
      mod = importlib.util.module_from_spec(spec)
      sys.modules[nombre] = mod
      spec.loader.exec_module(mod)
      return mod

  mm = _load("sorteo_marco_m_v1_1", "sorteo_marco_m_v1_1.py")   # cargador, sin editar
  v3 = _load("sorteo_v3", "sorteo_v3.py")                        # mecanismo, sin editar

  SHA_A = "ec3cf0f2d98346205fafa7ece756ca5875cb5707"
  semilla = mm.semilla_desde_sha_merge(SHA_A, "MARCO-M-v1_2")
  marco = mm.cargar_marco_m_v1_1(
      ruta=D / "marco-M-congelado-v1_2.tsv",
      ruta_sha=D / "CONGELADO-M-v1_2.sha256",
  )   # filtra elegible_v1_1=='SI', verifica sha256 y assert de conteo
  n_sorteo, cuota_max = mm.regla_de_tamano(len(marco))
  resultado = v3.sortear_v3(marco, n_sorteo=n_sorteo, cuota_max=cuota_max, semilla=semilla)
  ```
- **Semillas anteriores de la misma familia — no reutilizadas bajo ninguna
  circunstancia** (§3.4; `scope_id` distinto las separa por construcción):
  semilla anulada `867948c` (`ADR-135(d)`); `ACTO B` original
  `174266824551963846210387427777144587800` (`scope_id="ACT-PIL-3-v1"`); B′
  `63114853283919194858838455602446543838` (`"MARCO-M-v1"`); B″
  `34354141898495593251517379743390345279` (`"MARCO-M-v1_1"`).

**El primer resultado que produzca este procedimiento es el que se reporta.**
