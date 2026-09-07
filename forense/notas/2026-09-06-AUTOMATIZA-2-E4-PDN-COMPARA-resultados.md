# ACTO AUTOMATIZA-2-E4 · PDN-COMPARA — resultados

Encargo verbatim: `forense/encargos/2026-09-06-AUTOMATIZA-2-E4-PDN-COMPARA.md`.

## ARRANQUE

0. **Guard de rama.** `git ls-remote --heads origin | grep -i "automatiza-2\|pdn-compara"`
   antes de crear rama: sin coincidencia. Rama `acto/automatiza-2-e4-pdn-compara`
   creada y empujada de inmediato (`git push -u origin
   acto/automatiza-2-e4-pdn-compara`, confirmado con un segundo
   `ls-remote` tras el push).
1. **Repo.** `/home/pc0/mm-adq`, clon existente (no se clonó uno nuevo).
   Al arrancar, `HEAD` estaba en la rama `acto/maestra38-cron-3`
   (`92a7d406`) — un acto YA CERRADO (`PR #562 MERGED`, verificado con
   `git merge-base --is-ancestor 92a7d406 origin/main` → sí es ancestro, y
   `gh pr list --head acto/maestra38-cron-3 --state all` → `MERGED`). No
   se siguió trabajando sobre esa rama.
2. **SHA / main se movió.** Al llegar, `origin/main = 957a3080`. Durante
   la sesión, `git fetch origin` reportó `957a3080..33702a09 main`: 65
   commits nuevos mientras se trabajaba (actividad concurrente de otra(s)
   sesión(es) en otras cajas — `ACTO AUTOMATIZA-1-E1 ·
   PERIMETRO-FISICO-DE-RAICES`, `MAESTRA38-C1 · RE-ASIENTO`, etc.). No es
   PARO: se re-derivó. El trabajo ya hecho (uncommiteado) se guardó con
   `git stash push -u`, se creó `acto/automatiza-2-e4-pdn-compara` desde
   el `origin/main` fresco (`33702a09`), se empujó vacía, y se hizo
   `git stash pop` — auto-merge limpio, sin conflictos (los cambios de
   `AUTOMATIZA-1-E1` caen en regiones de `tests/manifiesto.py` disjuntas
   de las que toca este acto). Ver "Re-derivación por el perímetro" abajo.
3. **data/raw.** Presente (symlink a `/home/pc0/mm-corpus/raw`, `397`
   entradas de primer nivel). `data/raices.local.yaml` presente
   (`descargas_mx` → `/mnt/c/Users/PC0/Descargas MX`).
4. **Entorno.**
   - `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` = `` (vacío) → `sin_variable`, esperado.
   - `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` → `200`.
   - `ls data/raw/ | head -1` → no vacío (corpus montado) — este acto no
     abre microdato directamente, pero sí lee payloads reales de
     `data/raw/` para las cuatro comparaciones de aceptación.
   - `/mnt/c` (raíz `descargas_mx`) NO es legible dentro del sandbox de
     Bash de esta sesión (`allowWithinDeny` no lo incluye) pero SÍ lo es
     fuera de él (`ls "/mnt/c/Users/PC0/Descargas MX"` con
     `dangerouslyDisableSandbox` listó archivos reales) — es una
     restricción del tool-sandbox de esta sesión, no de la máquina; la
     comparación de `pdn_s3v2` (única de las cuatro cuya referencia vive
     en `descargas_mx`) se corrió con el sandbox deshabilitado para
     confirmarlo de verdad, no solo `NO-DISPONIBLE` por no poder leer la
     raíz.
5. **Espejo.** No se derivó ninguna cifra del espejo del proyecto; todo lo
   de abajo sale de comandos corridos en el clon de (1).

## Premisa "tras C1 fusionado"

El encargo declara este acto como posterior a un "C1" fusionado, y declara
también "no hay dependencia de datos". No hay línea `COMPUERTA:` / `GATED
a` / `Estado: GATED a` en el encargo (verificado leyendo el texto completo)
— no es una compuerta formal bajo `.claude/commands/acto.md` §2, así que
no dispara el protocolo de verificación de compuerta.

Aun así, se buscó el rastro de un "C1" de la serie `AUTOMATIZA-2` (misma
convención que la serie `AUTOMATIZA-1` -- `AUTOMATIZA-1-E1`,
`AUTOMATIZA-1-E2` y `AUTOMATIZA-1-E3`, ya fusionados: `PR #568`, `#569`,
`#572`) para verificar la premisa contra el árbol, no solo contra el rótulo:
`git log --oneline --all | grep -i automatiza`, `grep -rn "AUTOMATIZA-2"`
sobre `canon/`, `forense/`, `.tsv` — **sin ningún resultado** salvo los
archivos que este mismo acto crea. No se encontró un "AUTOMATIZA-2-C1" en
el árbol. Dado que (a) no hay compuerta formal que bloquee, (b) el propio
encargo declara "no hay dependencia de datos", y (c) el contenido de este
acto (comparador de sha256/miembros de zip) no lee ni depende de ningún
artefacto que un hipotético "C1" hubiera debido producir, se procedió sin
bloquear — pero se declara la premisa como NO VERIFICADA (no CUMPLIDA, no
INCUMPLIDA: simplemente no se encontró rastro), para que mesa la resuelva
si "C1" se refiere a algo fuera de este árbol (otra caja, un PR aún sin
fusionar en otra rama, o una re-etiquetación).

## A.8 — re-verificación del bloque [ADQ-PDN] citado por el encargo

Contra la base pre-existente del acto (`92a7d406`, antes de cualquier
edición de este acto):

```
$ git show 92a7d406:tools/adquiere_cron.sh | sed -n '202,231p'
DIA_MES_A5="$(date +%-d)"
if [ "$DIA_MES_A5" -ge 1 ] && [ "$DIA_MES_A5" -le 3 ]; then
  ADQ_PDN_DIR="data/raw/pdn_bulk_$(date +%Y_%m)"
  mkdir -p "$ADQ_PDN_DIR"
  for PAR in \
    "s1:https://drive.google.com/uc?export=download&id=1RSYOwWabsWqtxt7VNHIjf-yt1P5bPSbE" \
    "s2:https://drive.google.com/uc?export=download&id=1KWcst_YLI5YVlKnzmd3Xm5prAP4NVhAD" \
    "s3P:https://drive.google.com/uc?export=download&id=1i-HjNju04xdKThHgGDAzHb97GdF_cqS8" \
    "s6:https://drive.google.com/uc?export=download&id=1OM-P1JAp7PKeGL_InRYOQ1UO5Vpcs9Oi"; do
    SIS="${PAR%%:*}"; URL="${PAR#*:}"
    DEST="${ADQ_PDN_DIR}/pdn_${SIS}_$(date +%Y-%m-%d).zip"
    if curl -sS -A "..." --max-time 300 -L -o "$DEST" "$URL" 2>>"$LOGFILE"; then
      SHA_NUEVO="$(sha256sum "$DEST" | cut -d' ' -f1)"
      log "[ADQ-PDN] ${SIS}: re-bajado a ${DEST}, sha256=${SHA_NUEVO} (comparar a mano contra data/manifiesto.yaml; este paso no re-registra automáticamente)"
    else
      log "[ADQ-PDN] ${SIS}: PARO-RED, no se pudo re-bajar desde ${URL}"
      rm -f "$DEST"
    fi
    sleep 1
  done
  SALIDA_ESCANEO_PDN="$(python3 tests/manifiesto.py --escanea descargas_mx 2>&1 || true)"
  ...
  commit_censo_linea "$(printf '%s\n\n%s' "$LINEA_PDN" "$SALIDA_ESCANEO_PDN")" "$LINEA_PDN" "[ADQ-PDN] ${FECHA}"
else
  ...
fi
```

Coincide con la cita del encargo línea por línea (gate día 1-3, cuatro
URLs de Drive, `DEST` bajo `data/raw/pdn_bulk_<Y_m>/`, sha crudo, log
"comparar a mano", `PARO-RED`, `--escanea descargas_mx` a la raíz
equivocada, `commit_censo_linea`). **Confirmado, no heredado.**

Referencias únicas en `data/manifiesto.yaml` (`grep -n "id: pdn_"` +
lectura de cada entrada):

```
- id: pdn_s3v2          archivo: PDN_S3v2.zip                    raiz: descargas_mx  sha256: 923d0dd0...adb
- id: pdn_s1_2026_09_06 archivo: pdn_bulk_2026_09/pdn_s1_...zip  raiz: data_raw      sha256: cff2a5fb...2d4
- id: pdn_s2_2026_09_06 archivo: pdn_bulk_2026_09/pdn_s2_...zip  raiz: data_raw      sha256: db8fda58...2e8
- id: pdn_s6_2026_09_06 archivo: pdn_bulk_2026_09/pdn_s6_...zip  raiz: data_raw      sha256: 1a787b34...2db
```

Cada `id` aparece exactamente una vez (`grep -c "^- id: <id>$"` = 1 para
las cuatro). Coincide con las "referencias unívocas" que el encargo
declara.

## Re-derivación por el perímetro (main se movió)

`ACTO AUTOMATIZA-1-E1 · PERIMETRO-FISICO-DE-RAICES` (fusionado mientras
este acto estaba en curso) introdujo `RAICES_ESCANEABLES =
frozenset({"data_raw", "descargas_mx"})` y `raiz_escaneable(nombre)`:
ningún automatismo general del corpus hace I/O físico (walk/stat/hash/
open) sobre una raíz fuera de ese conjunto. `comparar_sha_manifiesto` SÍ
hace I/O físico sobre la raíz registrada de la entrada (para la segunda
señal `miembros_zip`) — se re-derivó para respetar `raiz_escaneable()`
antes de resolver esa raíz, igual que `cmd_verifica`/`cmd_escanea` ya
lo hacen. No afecta el resultado principal (`estado`/`sha_real`), que se
calcula contra `ruta_archivo` (la ruta que el propio caller ya resolvió,
nunca una raíz del manifiesto). Las dos raíces que este acto usa de
verdad (`data_raw`, `descargas_mx`) están ambas dentro de
`RAICES_ESCANEABLES`, así que ningún caso real cambia de resultado; es
una guardia para el caso general, no una corrección de un defecto
observado.

## COMMIT 1 — comparador + prueba

```
$ python3 tests/test_compara_sha.py
OK   test_archivo_ilegible
OK   test_id_duplicado_sin_referencia_univoca
OK   test_id_inexistente_sin_referencia_univoca
OK   test_miembro_cambiado_miembros_zip_distinto
OK   test_referencia_sin_sha256
OK   test_sha_distinto_mismos_miembros_cambio_de_contenido
OK   test_sha_igual_coincide

todo OK
```

## COMMIT 2 — cron + registro + cascada

`bash -n tools/adquiere_cron.sh` → sin salida (sintaxis válida). Lógica
del bloque (mapeo `SIS_DESCARGA`→`SIS_LOGICO`, tabla de ids, unión de las
cuatro líneas) verificada aparte con un script que simula `curl`/
`--compara-sha` (sin red, sin tocar el árbol real) — mapeo `s3P`→`s3`
correcto, `PARO-RED` intacto, las cuatro líneas se unen en un solo
`contenido` multilínea. **No se forzó una corrida end-to-end real del
cron** (enmienda 3 del encargo: "sin corrida artificial"; la ventana
natural es 1-3/oct).

## Aceptación — cuatro comparaciones sobre payloads reales de A4/A5

```
$ python3 tests/manifiesto.py --compara-sha --id pdn_s1_2026_09_06 --archivo data/raw/pdn_bulk_2026_09/pdn_s1_2026-09-06.zip
estado=COINCIDE id=pdn_s1_2026_09_06 sha_manifiesto=cff2a5fb...2d4 sha_real=cff2a5fb...2d4 miembros_zip=IGUAL

$ python3 tests/manifiesto.py --compara-sha --id pdn_s2_2026_09_06 --archivo data/raw/pdn_bulk_2026_09/pdn_s2_2026-09-06.zip
estado=COINCIDE id=pdn_s2_2026_09_06 sha_manifiesto=db8fda58...2e8 sha_real=db8fda58...2e8 miembros_zip=IGUAL

$ python3 tests/manifiesto.py --compara-sha --id pdn_s6_2026_09_06 --archivo data/raw/pdn_bulk_2026_09/pdn_s6_2026-09-06.zip
estado=COINCIDE id=pdn_s6_2026_09_06 sha_manifiesto=1a787b34...2db sha_real=1a787b34...2db miembros_zip=IGUAL

$ python3 tests/manifiesto.py --compara-sha --id pdn_s3v2 --archivo data/raw/pdn_bulk_2026_09/pdn_s3P_2026-09-06.zip
estado=COINCIDE id=pdn_s3v2 sha_manifiesto=923d0dd0...adb sha_real=923d0dd0...adb miembros_zip=IGUAL
```

COINCIDE ×4, `miembros_zip=IGUAL` ×4 — la de `pdn_s3v2` (referencia en
`descargas_mx`) se corrió con el tool-sandbox de esta sesión deshabilitado
(ver ARRANQUE punto 4); sin eso, `miembros_zip` habría salido
`NO-DISPONIBLE` por no poder leer `/mnt/c` desde este sandbox de
sesión — no un defecto del comparador.

```
$ bash -n tools/adquiere_cron.sh   # sin salida
$ python3 tests/check.py --baseline
...
3 FAIL · 174 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado accf688c6ad98f9b3264b4bf0343431d5649e666)
```

(El conteo de WARN subió de 171→174 frente a la corrida inicial de este
acto por los 65 commits ajenos que aterrizaron mientras tanto — la línea
base sigue VERDE, que es lo que exige la aceptación.)

## Cascada

`tools/cierre_acto.py` (Fase A, preflight, sin flags) corrido antes de
`--aplica`. Detalle en el propio commit de cascada.
