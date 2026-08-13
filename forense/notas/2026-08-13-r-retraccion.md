# ACTO R-RETRACCIÓN · Retiro del registro ISSP/ZA6980 de ACTO R (#190) — 2026-08-13

## Qué se quitó y por qué

`git show ddecf23 --stat` (verificado, no de memoria): 4 archivos, +134 líneas. De `data/manifiesto.yaml` (+78) se retiran las tres entradas que añadió — `za6980_issp2017sn_cuestionario_mx_pdf`, `za6980_issp2017sn_datos_v2_0_0_sav_zip`, `za6980_issp2017sn_datos_v2_0_0_dta_zip` —, y de `data/universo-puertas-2026-08-12.tsv` (+1) la fila `GESIS_ISSP_SocialNetworks_2017_ZA6980` (`EXISTE-NO-SATISFACE`).

Sustituidas por el registro de ACTO R″ (PR #193, fusionado en `main`): 3 módulos (ZA5900, ZA6980, ZA7600) contra 1 (solo ZA6980), 16 payloads contra 3, ids incompatibles entre ramas para los mismos bytes — `za6980_q_mx` (R″) y `za6980_issp2017sn_cuestionario_mx_pdf` (R) son el mismo PDF, mismo sha256 (`61bc0c80…544f2ed`), dos ids. La fila de puerta no se retira sin reemplazo: `GESIS_ISSP` (línea 100 de `universo-puertas-2026-08-12.tsv`, escrita por R″) ya cubre los 3 módulos con `EXISTE-SATISFACE`. La fila `ISSP`/`gap_mapeo_map_b` (línea 69, de MAP-B) es otra cosa — un placeholder de crosswalk, no una puerta institucional — y no se toca, mismo criterio que ya declaró la nota de ACTO R en su §4.

**Mecanismo real, sin maquillar:** el retiro de bytes no ocurre en el commit de este acto. Ya había ocurrido en `70cbb8c` — la fusión de `origin/main` sobre esta rama, después de que ENCARGO X cerrara PR #193, resolviendo el conflicto de estos dos archivos a favor de la versión completa de `main`. Verificado: `grep -cE "issp2017sn" data/manifiesto.yaml` ya daba `0` en `70cbb8c`, antes de este commit. Este acto no vuelve a tocar esos dos archivos — formaliza, con esta nota y la línea de `hallazgos.md`, una retracción que en bytes ya estaba hecha por otra vía.

El commit `ddecf23` se conserva íntegro en la historia. Su nota, `forense/notas/2026-08-13-r-registro-issp-za6980.md`, no se borra.

## No fue error, fue incompleto

ACTO R identificó el módulo sin ambigüedad citando la portada del PDF (su nota, §1: *"Mexico / ISSP 2017 – Social Networks and Social Resources"*), corrigió la premisa del propio encargo contra `relaciones.tsv` real (§2: 7 necesidades candidatas, no 3 — N12/N13/N14 ya con fuente `CONFIRMADA` distinta), y clasificó bien (`EXISTE-NO-SATISFACE`, con razón nombrada, no un default conservador). Lo que le faltó no fue rigor: fue alcance — un módulo de tres, porque el encargo que ejecutó solo nombraba uno.

## Causa raíz

De encargo, no de ejecutor, según mesa: se despachó ENCARGO-R cuando ya existía ENCARGO-R″ corregido (los 3 módulos, incluido ZA5900, que ACTO R no tenía manera de conocer) y sin lanzar. Dos encargos vigentes para la misma adquisición, uno desactualizado — declarado por mesa, no derivado de este acto.

## Verificación de cierre

```
$ python3 -c "
import yaml, collections
d = yaml.safe_load(open('data/manifiesto.yaml'))
por_archivo = collections.defaultdict(list)
por_sha = collections.defaultdict(list)
for e in d:
    if e.get('archivo'): por_archivo[e['archivo']].append(e['id'])
    if e.get('sha256'): por_sha[e['sha256']].append(e['id'])
print('total entradas:', len(d))
print('duplicados por archivo:', {k:v for k,v in por_archivo.items() if len(v)>1})
print('duplicados por sha256:', {k:v for k,v in por_sha.items() if len(v)>1})
"
total entradas: 554
duplicados por archivo: {'endireh2016/bd_mujeres_endireh2016_sitioinegi_dbf.zip': ['endireh_2016_bd_mujeres_endireh2016_sitioinegi_dbf', 'endireh_2016_bd_mujeres_endireh2016_sitioinegi_dbf_redescarga']}
duplicados por sha256: {}
```

El único duplicado por `archivo` es preexistente (ENDIREH, 2026-08-05/06), ajeno a ISSP, ya reportado en PR #193. Cero duplicados por `sha256` en las 554 entradas.

```
$ python3 tests/check.py --baseline
22 FAIL · 104 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json
```
