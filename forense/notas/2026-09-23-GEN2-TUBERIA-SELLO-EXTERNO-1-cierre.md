# Nota de cierre · GEN2-TUBERIA-SELLO-EXTERNO-1

CONTADOR: cero mediciones movidas. No adopta. No toca ningún `sello.json`/sidecar — los lee y los censa.

## ARRANQUE

- REPO: `/home/user/Modelado-Mexicano`, HEAD al 0-bis `cfce8cd3`.
- SHA de redacción del encargo `7ca31cb4`; base al arrancar `origin/main = 7722b9c1`, 0 commits detrás (guard 0.a). Árbol limpio (0.b).
- Guard 0.c (duplicado): `git ls-remote --heads origin | grep -i sello-externo` → sin coincidencia; `git worktree list` → 1 solo worktree, este; `search_pull_requests` (GitHub) con `SELLO-EXTERNO` y `sello-externo` → `total_count: 0`. Sin duplicado.
- Guard 0.d: `python3 tools/limpia_arbol.py --reporta` → 1 worktree, 1 rama local ya fusionada y viva (`claude/new-session-gvf1ln`, la de origen), base al día, `fuera_de_politica: NO-VERIFICABLE-SIN-GH`.
- `python3 tools/entorno.py --arranque`: `ENTORNO-DERIVADO = NUBE` (coincide con lo que el encargo declara — no PARO), corpus no montado, 0 archivos examinados. Este acto no toca microdato ni `data/raw`.
- ESPEJO: no se usó — todas las cifras salen del clon de este worktree.

## Verificación de la premisa `[SUPUESTO]` de §3 (red)

```
$ curl -s -o /dev/null -w "http_code=%{http_code} http_connect=%{http_connect}\n" --max-time 10 https://a.pool.opentimestamps.org
http_code=000 http_connect=403
(igual para alice.btc.calendar.opentimestamps.org, freetsa.org, www.digicert.com)
```

Confirmado también con el cliente real (`pip install --break-system-packages opentimestamps-client` sí tuvo egress a PyPI):

```
$ ots stamp forense/sellos/manifiesto-sellos-2026-09-23.tsv
Submitting to remote calendar https://a.pool.opentimestamps.org
Submitting to remote calendar https://b.pool.opentimestamps.org
Submitting to remote calendar https://a.pool.eternitywall.com
Submitting to remote calendar https://ots.btc.catallaxy.com
Failed to create timestamp: need at least 2 attestations but received 0 within timeout
```

TSA (mecanismo b):

```
$ openssl ts -query -data forense/sellos/manifiesto-sellos-2026-09-23.tsv -sha256 -cert -out /tmp/manifiesto.tsq
$ curl ... https://freetsa.org/tsr ...
connect_rejected (the egress proxy denied the CONNECT (organization policy))
```

La premisa cae: sin egress a ningún calendario OTS ni TSA pública. El encargo (§3) ya previó esta rama («si ninguno responde, el fallback P2-c»); esto es logística de red, no toca qué se mide ni una firma de mesa — no es PARO.

## P1 · Manifiesto

`tools/sello_externo.py manifiesto --escribe --fecha 2026-09-23`:

```
ESCRITO forense/sellos/manifiesto-sellos-2026-09-23.tsv filas=342 sha256-manifiesto=57b108879c7fe96b26d79cce81897066fbe35d6c893f7e8d55ac28809f52a777
```

Universo: `ls data/corrida0/CALC-*/sello.json | wc -l` → 226; `ls forense/prereg-caja/*.sha256 | wc -l` → 116; 226+116 = 342, coincide con §3 del encargo (`226 + 116`). 342/342 filas resolvieron `commit`/`pr`/`merged_at`/`firma_gpg_*` — 0 `NO-ACCESIBLE`. Las 342 firmas GPG de merge son de la misma llave `B5690EEEBB952194` (estado `E`: sin llave pública local para verificar, no es lo mismo que una firma inválida).

Determinismo: dos corridas seguidas sobre el mismo árbol dieron el mismo `sha256-manifiesto` (verificado dos veces: antes y después de añadir las columnas `firma_gpg_*`).

`python3 tests/test_sello_externo.py` → `OK -- test_sello_externo.py: 3 pruebas, 0 fallos` (fixture de repo git sintético propio).

## P2 · Atestación

(a) OpenTimestamps: intentado, sin egress (arriba). (b) TSA RFC 3161: intentado, sin egress (arriba). (c) Fallback sin red, el que funcionó: la firma GPG del merge de cada sello ya vive en el manifiesto (columnas `firma_gpg_estado`/`firma_gpg_keyid`); `docs/sello-externo.md` deja la receta para que mesa firme, desde su propia máquina y con su propia llave, un tag GPG sobre el commit que trae este manifiesto (`git tag -s sellos-2026-09-23 <commit> -m "sha256=57b10887..."`). Esa firma de mesa es el activo de terceros que faltaba y que esta sesión no puede producir sin su llave privada.

## P3 · Receta para un tercero

`docs/sello-externo.md`. Probada desde un clon limpio en esta misma sesión:

```
$ rm -rf /tmp/verifica-sello && git clone -q /home/user/Modelado-Mexicano /tmp/verifica-sello
$ cd /tmp/verifica-sello && git checkout -q acto/gen2-tuberia-sello-externo-1
$ sha256sum forense/sellos/manifiesto-sellos-2026-09-23.tsv
7d210e93350d31efb2f12578382aed80678d9fe804c9d6026969a711f184961e  forense/sellos/manifiesto-sellos-2026-09-23.tsv
$ git log -1 --format="%G? %GK" $(git log --diff-filter=A --format=%H -1 -- data/corrida0/CALC-0001/sello.json)
E B5690EEEBB952194
```

(El clon usó una ruta local porque esta sesión de nube no tiene egress directo a `github.com` fuera del remoto ya configurado del worktree; para un tercero con red normal el comando es el mismo con la URL HTTPS del repo.)

## P4 · Futuro y FP

`tools/sello_externo.py stamp --desde <manifiesto-anterior> --fecha <fecha>` deja el delta listo (probado en `tests/test_sello_externo.py::prueba_stamp_solo_delta`). Este acto no edita `.claude/commands/acto.md` ni CI — lo propone. Fila `FP-260923-GEN2-TUBERIA-SELLO-EXTERNO-1-cfce-01`.

## Perímetro de cierre

- `forense/sellos/` nuevo, registrado en el manifiesto.
- `docs/sello-externo.md` nuevo.
- `python3 tools/verifica_sidecars.py` → `FAIL: 0 — VERDE`.
- `python3 tests/check.py --rapido` → `0 FAIL · 340 WARN` (los WARN son deuda ya existente, no de este acto).
- Rótulo `GEN2-TUBERIA-SELLO-EXTERNO-1` censado en `canon/registro-rotulos.tsv`.
- Sin rótulos M/E pelados nuevos en el encargo — T25 no aplica.
