# Nota de cierre · ACTO GEN2-ENUT-NUCLEO-CELDAS-1 · PARO-PREMISA en el ARRANQUE

Encargo: `forense/encargos/2026-09-22-GEN2-ENUT-NUCLEO-CELDAS-1.md` (0-bis `9f24df72`, verbatim del adjunto, `.cuerpo.sha256` `f0c1a728…`).
Adenda de mesa: `forense/encargos/2026-09-22-GEN2-ENUT-NUCLEO-CELDAS-1-ADENDA-1.md` (sellada al recibirse).
Entorno: CAJA (`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable`), Opus 5.5, sin sub-agentes. **Cero microdato abierto** (ni ENUT 2024 ni 2019): todo lo de abajo se lee de archivos versionados en `origin/main`. `data/raw` no se enlazó porque el acto no llegó a abrir dato.

## 1 · Qué pasó

El ARRANQUE (A.8 por objeto, §4.1 de `/acto`) encontró tres premisas falsas que tocan **qué se mide** y **una firma de mesa**. Por §4.2 de `/acto` el acto paró antes del COMMIT-1 y lo reportó. Mesa aceptó el PARO (ADENDA-1): «Los tres hallazgos son entregable (v2.16 §2)». No se congeló spec, no se reservó ni se selló CALC, y no se tocó el marcador.

Base: SHA de redacción `ccd7c0eb`. Al abrir, `origin/main` estaba en `02eda845`; al reabrir para el cierre, en `0232aad7` (`#1000`). Guard 0.a-0.d en verde: 0 detrás, árbol limpio, cero duplicados por rama, worktree o PR.

## 2 · Las tres premisas que cayeron (evidencia por comando)

**H1 · El CALC-id reservado ya existe, sellado.** Encargo §4: «`ls -d data/corrida0/CALC-ENUT2024-NUCLEO*` → 0; `grep -c "ENUT2024-NUCLEO" data/corrida0/corridas.tsv` → 0».
- En `ccd7c0eb` (el SHA del propio encargo): `git ls-tree -d --name-only ccd7c0eb data/corrida0/ | grep -c CALC-ENUT2024-NUCLEO` → **1**; `git show ccd7c0eb:data/corrida0/corridas.tsv | grep -c ENUT2024-NUCLEO` → **1**.
- `CALC-ENUT2024-NUCLEO-EJES-0001` lo sellaron `GEN2-ENUT-PISOS-Y-SERIE-1` y el PR #976, en los commits `7ebb04de` (COMMIT-1) y `9ec5143d`. La fila de `corridas.tsv` es `CALC-ENUT2024-NUCLEO-EJES-0001--7ebb04deaa34 · SELLADA · GEN2 · cuenta_gen2=SI · COINCIDE · REPRODUCE · IDENTICO`.
- Ese CALC ya trae las 14 celdas NÚCLEO por un eje con IC95 bootstrap de UPM, las mismas que `CALC-ENUT2019-NUCLEO-EJES-0001`:
  - nacional,
  - sexo ×2,
  - edad ×5,
  - escolaridad ×4,
  - localidad ×2,
  - y la razón C4 `RESULT-ENUT2024-RAZON-NUCLEO-NACIONAL-*`.
- Re-sellarlo sería PARO b.
- **Cómo nació el negativo** (atribución de mesa, ADENDA-1: «un `ls | head -5` truncado», A.13). Es consistente con el árbol: en `ccd7c0eb` los directorios `CALC-ENUT*` de `data/corrida0/` ordenan así:
  - `CALC-ENUT-0001`,
  - `-SERIE-2009-2014-NUCLEO-0001`,
  - `CALC-ENUT2019-NUCLEO-EJES-0001`,
  - `CALC-ENUT2024-DISTRIBUCION-HORAS-0001`,
  - `-0002`,
  - **`CALC-ENUT2024-NUCLEO-EJES-0001`** (sexto),
  - `-PARTICIPACION-INTENSIDAD-0001`.

  Un `head -5` lo deja fuera. El `grep -c` que el encargo cita también da 1, no 0.

**H2 · Las celdas del marcador no son marginales de un eje: son cruces sexo × edad.** El encargo trae un `[SUPUESTO]` en §3: «Las 21 celdas del marcador son marginales por un eje (no cruces)».
- La familia `familia.cuidado.reparto_mujeres40_ejes_enut2024` tiene **12 filas** en `data/corrida0/marcador-segmento.tsv`. Se cuentan con `awk -F'\t' '$3 ~ /cuidado/ {print $3" | "$5}' … | sort | uniq -c`:
  - 1 `reparto_hogar · todos los hogares (razón)` (SIN-PISO),
  - **10 `sexo_edad`** («hombre · 12-17» … «mujer · 60+», SIN-PISO),
  - 1 `reparto_hogarxsexo_edad · 10 celdas agrupadas` (RESERVADA).
- Aparte hay 10 filas de `familia.cuidado.recae_mujeres_40mas`, ya IDENTICO.
- Las 10 celdas `sexo_edad` combinan dos variables. `tools/enut_nucleo.py` lleva una guardia de una sola variable por celda: `celdas_de_eje`, `groupby` sólo por `_llave` y la auditoría AST R1-R6. Por eso ni `CALC-ENUT2019-NUCLEO-EJES-0001` ni `CALC-ENUT2024-NUCLEO-EJES-0001` tienen celdas sexo × edad; el control es buscar `SEXO-EDAD`/`MUJER-40`/`HOMBRE-12` en los ids de `resultados.json`, que da 0 en ambos.
- Por lo tanto el piso 2019 del núcleo no existe para esas 10 celdas, aunque se midiera 2024. El encargo prevé la rama («si alguna es cruce, queda RESERVADA… PARO a)»), y aquí son 10 de 11.
- La cifra «21» no sale del árbol, ni de las filas (12) ni de las SIN-PISO (11). La cita el cuerpo de la FP y el ADR de PISOS-Y-SERIE-1; ADR-557 hablaba de «17 marginales». Mesa la corrige por enmienda (ADENDA-1).

**H3 · La firma (a)(b)(c) no estaba presente.** Compuerta §8: «Firma (a)(b)(c) presente — protege: congelar spec».
- `FP-260921-GEN2-ENUT-PISOS-Y-SERIE-1-308c-01` estaba `ABIERTA` (`forense/firmas-pendientes.tsv:421`), y `grep -c 308c data/corrida0/decisiones.tsv` → 0.
- El §2 del encargo es una propuesta de dirección («mesa sella o edita»), y el propio encargo dice «Sin texto → PARA».

## 3 · Hallazgo adicional para el sucesor (no bloquea este cierre)

`data/enut-comparabilidad-texto-v1_0.tsv` (sha256 `9483ecbb…`) entra **fijado por hash** como `IN-COMPARABILIDAD-P1` en tres CALC sellados; `grep -l enut-comparabilidad-texto-v1_0.tsv data/corrida0/*/spec.yaml` los lista:
- `CALC-ENUT2019-NUCLEO-EJES-0001`,
- `CALC-ENUT-SERIE-2009-2014-NUCLEO-0001`,
- `CALC-ENUT2024-NUCLEO-EJES-0001`.

Enmendar **en su sitio** la fila C2×2019 (hoy `CAMBIO-MENOR`) a `CAMBIO-DE-INSTRUMENTO`, como piden P3 y la firma (a), cambia ese hash, y el `verify` de los tres CALC dejaría de casar: es la clase del PARO b. La firma (a) se asienta en `decisiones.tsv` sin tocar el TSV. La fila corregida va en una versión nueva (`-v1_1.tsv`, con su `.meta`) o en una enmienda aparte; se le asigna a `GEN2-ENUT-ENLACE-MARCADOR-1`.

## 4 · Firma de mesa

FIRMA-PENDIENTE-DE-CONFIRMACION

## 5 · Contador

Cero mediciones, cero CALC, no adopta. El marcador no se editó: `sin_piso` no se mueve desde este acto. `cuenta_gen2` no cambia (los tres CALC de PISOS-Y-SERIE-1 ya lo tenían en `SI` en su `spec.yaml`).
