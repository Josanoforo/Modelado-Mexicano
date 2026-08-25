# Sorteo real de `ACT-PIL-3` — `ACTO B` (`SORTEA`), resultados

**Pre-registro del primer commit — antes de correr el PRNG.**

- `SHA_A` (merge de `PR #353`, ACTO A `CONGELA-SORTEA`, ancestro verificado de `HEAD`): `887508aded1ea817bfc1081f2807527db28cbcc0`.
- Protocolo de semilla: `sorteo-act-pil-3-v2-PROPUESTA.md` §3.2, implementado literal en `sorteo_v2.py:semilla_desde_sha_merge`.
- Invocación exacta a ejecutar:
  ```python
  from sorteo_v2 import cargar_marco, sortear, semilla_desde_sha_merge

  SHA_A = "887508aded1ea817bfc1081f2807527db28cbcc0"
  semilla = semilla_desde_sha_merge(SHA_A, "ACT-PIL-3-v1")
  marco = cargar_marco()  # marco-congelado-piloto-v1_0.tsv, assert n=50
  resultado = sortear(marco, n_sorteo=15, cuota_max=3, semilla=semilla)
  ```
- Semilla derivada (§3.2, `derivar_seed_scope(int(sha256(SHA_A_hex).hexdigest(), 16) % 2**63, "ACT-PIL-3-v1")`): `174266824551963846210387427777144587800`.
- La semilla anulada `867948c` (`ADR-135(d)`) NO se reutiliza bajo ninguna circunstancia (§3.4), aunque el marco fuera idéntico.

**El primer resultado que produzca este procedimiento es el que se reporta.**
