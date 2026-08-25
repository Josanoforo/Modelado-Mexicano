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

---

## Resultado (segundo commit — salida íntegra, una sola corrida)

`sortear(marco, n_sorteo=15, cuota_max=3, semilla=174266824551963846210387427777144587800)` sobre `marco-congelado-piloto-v1_0.tsv` (50 filas elegibles, `grado_dependencia ∈ {P1,P2}` ∧ `publicada ∈ {SI,NO}`, `assert` verificado).

### Las 15 filas sorteadas

`estrato` = `categoría|grado_dependencia|dificultad` (columnas del congelado).

| # | id | estrato | grado | publicada |
|---|----|---------|-------|-----------|
| 1 | CIV-08 | civico\|P1\|MEDIA | P1 | NO |
| 2 | TIC-08 | comunicacion\|P2\|MEDIA | P2 | NO |
| 3 | TIC-01 | cooperacion\|P1\|MEDIA | P1 | NO |
| 4 | DIN-11 | dinero\|P1\|FACIL | P1 | NO |
| 5 | DIN-03 | dinero\|P1\|MEDIA | P1 | NO |
| 6 | DOC-06 | dinero\|P2\|DIFICIL | P2 | NO |
| 7 | EMP-02 | dinero\|P2\|DIFICIL | P2 | NO |
| 8 | EMP-04 | dinero\|P2\|DIFICIL | P2 | NO |
| 9 | DIN-05 | dinero\|P2\|MEDIA | P2 | NO |
| 10 | SFT-06 | familia\|P2\|DIFICIL | P2 | NO |
| 11 | SFT-04 | salud\|P2\|MEDIA | P2 | NO |
| 12 | TIC-12 | trabajo\|P1\|MEDIA | P1 | NO |
| 13 | TIC-06 | trabajo\|P2\|MEDIA | P2 | NO |
| 14 | DIN-07 | dinero\|P2\|MEDIA | P2 | SI |
| 15 | EMP-05 | familia\|P2\|MEDIA | P2 | SI |

### Estratos excluidos por infactibilidad (§2.3), con fallback aplicado

- `dinero|P2|FACIL` — 1 asiento liberado por infactibilidad (sin filas `publicada=NO` disponibles en ese estrato); reasignado por el fallback de §2.2/§2.3 (reparto proporcional Hamilton/mayor resto sobre los estratos factibles restantes, misma semilla).
- `familia|P1|DIFICIL` — 1 asiento liberado por infactibilidad (mismo motivo); mismo fallback.

Sin `SKIP` registrado (lista `skips` vacía): la cuota de `publicada=SI` no se agotó antes de cubrir los asientos reasignados.

### Verificación

- `len(resultado) == 15` ✓
- `count(publicada=SI) = 2 ≤ floor(0.20·15) = 3` ✓ (cuota dura cumplida, no al límite)
- Determinismo: misma semilla + mismo congelado (byte a byte, verificado por `sha256sum` contra `CONGELADO-v1_0.sha256` en `F0.2`) ⇒ mismo resultado, por construcción de `random.Random.sample`.

### sha256 de este registro

Se calcula y se declara en el commit que fija esta sección (el hash del archivo en su estado final, no de un contenido futuro).

`sha256` de este registro (calculado sobre el contenido hasta esta línea, antes de añadirla): `120e299799ae34911a85d203c7de6fb036519683a8ecbead938a63b338efd8a2`
