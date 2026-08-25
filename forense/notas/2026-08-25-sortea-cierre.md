# Cierre `ACTO SORTEA` (Acto B) — sorteo real de `ACT-PIL-3`

**Fecha:** 25/ago/2026. **Entorno:** NUBE (`cloud_default`). **ADR:** `ADR-188` (`canon/gobernanza-v1_15.md`). **Fila de tablero:** `FP-154` (`forense/firmas-pendientes.tsv`), recibe `ejecutada_en`. **Pack padre:** `forense/encargos/2026-08-25-PACK-CONGELA-SORTEA.md`, queda `CONSUMIDO`.

## Compuertas verificadas antes de escribir (F0)

1. `SHA_A` = `887508aded1ea817bfc1081f2807527db28cbcc0` (merge de `PR #353`, `ACTO CONGELA-SORTEA`) — verificado como commit de merge y como ancestro de `HEAD` (`2b7d787`, tras refrescar `main` local, que estaba desactualizado; no fue PARO, así lo permite el arranque §2).
2. Integridad del congelado: `sha256sum` de `marco-congelado-piloto-v1_0.tsv` y de `sorteo-act-pil-3-v2-PROPUESTA.md` contra `CONGELADO-v1_0.sha256` — coinciden byte a byte, sin discrepancia.
3. A.8 en fresco: 0 archivos `*result*` en `forense/prereg-duelo-v2/` (12 examinados antes de correr); `FP-154` `FIRMADA`, `n_sorteo=15`; `tests_sorteo_v2.py` — 12/12 casos pasan (§5 Caso 1/2/3 + determinismo).

## Primer commit — pre-registro de la semilla (antes del PRNG)

`forense/prereg-duelo-v2/sorteo-resultados-v1_0.md` (commit `fb08c2b`): `SHA_A`, invocación exacta (`semilla_desde_sha_merge` → `sortear`), semilla derivada por §3.2 (`174266824551963846210387427777144587800`, vía `derivar_seed_scope` de `scoring-adv1-m3.py:685`, sin reinventar el hash), y el compromiso: el primer resultado que produzca el procedimiento es el que se reporta. `867948c` no se reutiliza.

## Segundo commit — salida íntegra del sorteo (F1)

`forense/prereg-duelo-v2/sorteo-resultados-v1_0.md` (commit `5f61e9a`): 15 filas sorteadas sobre el universo elegible de 50 (`grado_dependencia ∈ {P1,P2}`, `publicada ∈ {SI,NO}`, `assert` verificado). `publicada=SI` = 2, cuota dura `floor(0.20·15)=3` cumplida sin agotarse. Dos estratos excluidos por infactibilidad (`dinero|P2|FACIL`, `familia|P1|DIFICIL`), fallback proporcional de §2.2/§2.3 aplicado exacto. Sin `SKIP`. Sin re-corridas — una sola tirada.

## Registro y gobernanza (F2)

- `ADR-188` (`canon/gobernanza-v1_15.md`): adjudica el set v1 de `ACT-PIL-3` y su semilla pública — **PILOTO SIN VEREDICTO** (D-i del CAREO). CV/`n` se miden solo sobre estas 15 en el acto árbitro (`FP-79`).
- `FP-154.ejecutada_en` = este acto.
- `canon/estado-programa-v1_10.md`: recifrado de ADR (187→188, cabecera y `L0`, tras resolver la colisión con `ADR-186`/`ADR-187` de `PR #357`) y línea de estado del duelo actualizada — «15 celdas sorteadas, semilla pública, `L` pendiente».
- Pack padre `forense/encargos/2026-08-25-PACK-CONGELA-SORTEA.md` marcado `CONSUMIDO`.
- Suite: `tests_sorteo_v2.py` 12/12 antes y después (sin `--freeze`); T22/T25 no aplican en este entorno sin corredor de suite general — este acto solo escribe los archivos de su propio perímetro.

**CONTADOR: cero, declarado.** El sorteo no mide México — habilita a quien lo hará.

## Lo que este acto NO hizo

No corrió `L` (sesiones limpias fuera del proyecto, D-iii/`ADV1-M2` — las lanza mesa). No calculó CV de nada. No tocó el pool de 253 ni reabrió el marco. No adjudicó veredicto de piloto. No repitió el sorteo.

## Perímetro tocado (lista cerrada, sin excedente)

`forense/prereg-duelo-v2/sorteo-resultados-v1_0.md` (nuevo) · `canon/gobernanza-v1_15.md` (`ADR-188`) · `canon/estado-programa-v1_10.md` (recifrado + línea de estado) · `forense/firmas-pendientes.tsv` (`FP-154.ejecutada_en`) · esta nota · `forense/encargos/2026-08-25-PACK-CONGELA-SORTEA.md` (marca `CONSUMIDO`). No se tocó: marco, congelado, `sorteo_v2.py`, reglamento, pool de 253, `tools/`, `milpa/`, `README.md`.
