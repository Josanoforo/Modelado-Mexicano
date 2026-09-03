# ENCARGO · ACTO MAESTRA36-A1 · ESCANEA-RECURSIVO-Y-REGISTRA-DESCARGAS

**SHA de redacción:** 9af8407 (origin/main, merge PR #494) · 2/sep/2026, dirección (Fable) · instrucciones v2.12
**Entorno asignado:** UBUNTU (caja de mesa). NO se lanza en NUBE.
**Estado:** VIVO

> Archivado verbatim por A.3 (0-bis). El texto de abajo es el que llegó a la sesión:
> primero el encargo, después la ENMIENDA DE DIRECCIÓN que dirección escribió a mitad
> de acto (2/sep/2026, contra el mismo 9af8407) y que sustituye P2 y precisa P1.

---

## Texto del encargo, verbatim

ENCARGO · ACTO MAESTRA36-A1 · ESCANEA-RECURSIVO-Y-REGISTRA-DESCARGAS

SHA de redacción: 9af8407 (origin/main, merge PR #494) · 2/sep/2026, dirección (Fable) · instrucciones v2.12 · Estado: LISTO PARA LANZAR — COMPUERTA: ninguna. Este acto ABSORBE el «relanzar A1» del transfer maestra-35 §5.6 y §7: los crosstabs del Mexico Panel viven en una subcarpeta y caen en el mismo defecto que este acto repara; no se lanza un A1 aparte.

ENTORNO ASIGNADO: UBUNTU (caja de mesa, con /mnt/c/Users/PC0/Descargas MX montada y data/raices.local.yaml presente). NO se lanza en NUBE: no tiene los bytes. MODELO SUGERIDO: Opus (P1 lleva regresión y P2/P3 llevan juicio A.4).

Invoca /acto: el ARRANQUE (5 puntos + A.2 de tres partes), la compuerta, el 0-bis y la cascada de cierre los ejecuta la skill. La tercera parte de A.2 aquí es ls "$(python3 -c 'import yaml;print(yaml.safe_load(open("data/raices.local.yaml"))["descargas_mx"])')" | head -1; si raices.local.yaml no existe o descargas_mx no resuelve, es PARO de entorno (A.2), no de encargo.

CARRILES: en paralelo corren, en NUBE, /despacha → MAESTRA34-N3 · AGREGA-2 → N5 (perímetro forense/prereg-duelo-v2/corridas-L/, scoreboards) y, cuando dirección lo escriba, MAESTRA36-N10 · SELLA-L9-L11 (perímetro milpa/tramite-ola5-propuesta-v0.yaml, milpa/tramite.yaml, canon/modelo-decision). Ninguno toca tests/manifiesto.py ni data/manifiesto.yaml. El cron [ADQ] de las 07:30 sí escribe data/manifiesto.yaml y data/curacion-registro/: no lanzar este acto entre 07:25 y 08:00, y si al cerrar origin/main trae un [ADQ] nuevo, fusionar antes de la cascada y re-derivar los contadores.

FIRMAS DE MESA — verbatim, 2/sep/2026. El ejecutor propaga, no decide (SELLA-3).

«Estuve bajando información pero creo que no se hizo un barrido completo, ya había bajado varias cosas y me las volvieron a pedir. Pero creo que ya se por qué, tenemos dos carpetas de descargas. C:\Users\PC0\Descargas MX\Descargas Manuales y C:\Users\PC0\Descargas MX posiblemente se corrió la estructura de codex solo para 1 carpeta. Necesito que se revisen las dos.»

Lectura de dirección de la firma (no es firma, es lectura): «revisar las dos» = inventariar las dos rutas contra el manifiesto por contenido y registrar lo que falte. La firma NO autoriza registrar archivos ajenos al proyecto ni editar entradas existentes.

═══ VERIFICACIÓN DE EXISTENCIA (A.8) — contestada por quien escribe, contra 9af8407 ═══

(1) ESTRUCTURA. data/INFRAESTRUCTURA-v1_0.md:22-23 gobierna data/manifiesto.yaml (tests/manifiesto.py --registra/--promueve) y data/manifiesto-staging.yaml (--escanea <RAIZ>); :368 declara data/raices.local.yaml gitignorada. Cola y relaciones: data/curacion-registro/ (D1–D3). Este encargo toca las tres tablas y el índice (§0.11 del transfer: todo encargo que produzca artefactos en data/ lo lleva).

(2) CONTENIDO — comando y salida cruda:

grep -n -E 'os\.walk|rglob' tests/manifiesto.py → 0 líneas (1 archivo examinado). sed -n '660,663p' tests/manifiesto.py → for nombre in sorted(os.listdir(ruta)): … if not os.path.isfile(ruta_abs): continue. El escáner de staging no entra a subcarpetas. → NO-ENCONTRADO (escaneo recursivo en manifiesto.py; universo: tests/manifiesto.py íntegro).
sed -n '125,131p' tests/corpus.py → os.walk(ruta_raiz) + rel = os.path.normpath(os.path.relpath(ruta_abs, ruta_raiz)). El recorrido recursivo con ruta relativa a la raíz ya existe y es la convención vigente de archivo (T2/ADR sobre las 49 entradas Descargas Manuales/…, canon/gobernanza-v1_15.md:2453). → EXISTE-NO-SATISFACE: corpus.py lista huérfanos por ruta, no dedup por sha256 y no escribe staging. La reparación de P1 reutiliza esa convención, no inventa otra.
Manifiesto, por regex sobre data/manifiesto.yaml (1 070 ids, 1 065 con sha256): entradas raiz: descargas_mx = 106; prefijo Descargas Manuales/ = 49; basename sin carpeta = 57. Subcarpeta academico/icpsr35024/crosstabs/ (transfer §7): grep -c 'crosstabs' data/manifiesto.yaml → reporta el valor al arrancar; dirección espera 0.
grep -iE 'escanea|subcarpeta|Descargas Manuales' forense/firmas-pendientes.tsv → 0 filas (1 archivo, 247 filas examinadas): ninguna FP abierta cubre esto. forense/hallazgos.md:406 (18/ago) registra el síntoma (49 contados dos veces) sin nombrar la causa (listdir).
Universos declarados por actos previos sobre la misma raíz: A4 (1/sep) 122 archivos; A1-2 (1/sep) 160 con find -type f; A1-3 (2/sep) 190. Tres cifras distintas el mismo par de días = tres mecanismos distintos, no tres corpus.

(3) COBERTURA RETROACTIVA. git log --diff-filter=A --format=%ad --date=short -- tests/manifiesto.py → 2026-09-01 (fecha del archivo en su ruta actual; el --escanea es anterior y llegó por movimiento). Las 49 entradas con prefijo nacieron el 18/ago por corrección T2, después de REG-LOTE3 (PR #225) que las registró sin prefijo: todo lo registrado antes del 18/ago pudo entrar sin ruta relativa. P0 lo mide, no lo supone.

SPEC CONGELABLE POR PIEZA (un PR, un ADR, un recibo — D-11)

P0 · BARRIDO (solo lectura, primero, con salida commiteada). Correr el script del Anexo como tools/barrido_descargas_vs_manifiesto.py (créalo del anexo, verbatim) sobre las DOS rutas de la firma, en ese orden. Pega la salida cruda íntegra en forense/notas/2026-09-0X-MAESTRA36-A1-P0-barrido.md con: archivos examinados por ruta (A.13), REGISTRADO / NO-REGISTRADO / MISMO-NOMBRE-OTRO-SHA, y — a mano, sin script — una tabla que clasifique cada NO-REGISTRADO en (a) dato del proyecto con fila de cola identificable, (b) dato del proyecto sin fila, (c) ajeno o dudoso. La clase (c) no se registra: se lista y va a FP. Frase de sello: «el primer resultado que produzca este procedimiento es el que se reporta». Si NO-REGISTRADO = 0 con examinados > 0 en ambas rutas, el acto sigue con P1 y P2 queda vacío, declarado.

P1 · --escanea recursivo, con regresión antes de usarlo. En tests/manifiesto.py:660: sustituir os.listdir+isfile por os.walk sobre la raíz, y "archivo": nombre por la ruta relativa os.path.normpath(os.path.relpath(ruta_abs, ruta)) — misma convención que tests/corpus.py:131. El filtro de extensiones para RAICES_QUE_EXIGEN_GRUPO se aplica igual por archivo. Control de regresión, antes de tocar código: --escanea descargas_mx sobre el árbol sin parchar → staging A; sobre una copia temporal de la raíz sin subcarpetas (rsync/cp solo del nivel superior a /tmp/raiz-plana, apuntada por un raices.local.yaml temporal) el parche debe producir staging byte-idéntico a A salvo el campo mtime/fecha_descarga si difiere por la copia — si difiere en archivo o sha256, PARO de pieza. Después, tests/corpus.py sobre la raíz real: el conteo C1 (huérfanos) debe bajar exactamente en el número de NO-REGISTRADO que P2 registre; C3 no debe subir. No se re-escriben las 106 entradas existentes.

P2 · Registro por las tres capas Codex, solo clases (a) y (b) de P0. Por archivo: tests/manifiesto.py --registra con archivo = ruta relativa a la raíz (la que P0 imprimió), raiz: descargas_mx, url_origen cuando P0/la cola lo dé; A.7 con dos hashes solo si el formato trae token/timestamp (los XML DescargaMasiva sí; un .dta/.zip no). --verifica una invocación por --id (A.1), salida cruda pegada, tres respuestas sin colapsar (AUSENTE · raíz-no-configurada · hash-discordante). Cola: fila de data/curacion-registro/cola-adquisicion-registro.tsv → OBTENIDO con ids_manifiesto, editada por línea, nunca con csv round-trip (§0.8, defecto medido por el cron); relaciones.tsv + procedencia + utilidad para clase (a); clase (b) entra al manifiesto y al registro como activo sin necesidad, sin inventarle N. tools/vista_cola_adquisicion.py regenera la vista (T26); baseline.json del curador recifrado con validador {"ok": true}. Anti-PR#77: la raíz descargas_mx ES el corpus compartido — verificar con --verifica desde el clon principal, no solo desde el worktree.

P3 · Evaluación A.4 de lo registrado contra lo que la cola espera. Para cada fila de cola que P2 movió a OBTENIDO, una línea con vocabulario A.4 (EXISTE-SATISFACE / EXISTE-NO-SATISFACE con qué falta / NO-ENCONTRADO con universo). Objetos que dirección espera encontrar y su compuerta aguas abajo: academico/icpsr35024/crosstabs/* (T1–T5 y export_crudo_mesa_2026-09-02.txt, T5_lista_W2.txt; si T6–T9 ya están, dilo) → abre MAESTRA36-L12 · MPS-2012-CROSSTABS; OECD Trust (B4: si solo hay Stat.Links/xlsx de reporte, es EXISTE-NO-SATISFACE para microdato y NO-ACCESIBLE para el microdato mismo — exige solicitud a govtrustinfo@oecd.org, verificado 2/sep en la página de acceso); Bauchet 2014 (B5: comparar contra SSRN id 2474620; A1-3 ya reportó dos PDF que no eran el pedido); CompraNet/ComprasMX (EXT_OF_07, fila 63: si mesa bajó algo de cnetassets/datos_abiertos_contratos_expedientes/, registrar y anotar que la etiqueta de la fila dice EXT_OF_07 pero su contenido es EXT-OF-05 del mapa). Nada de esto se busca en red: si no está en disco, es NO-ENCONTRADO-EN-DISCO con la ruta examinada, no NO-OBTENIDO.

PERÍMETRO Y CONCURRENCIA Toca: tests/manifiesto.py · tools/barrido_descargas_vs_manifiesto.py (nuevo) · data/manifiesto.yaml · data/manifiesto-staging.yaml (si P1 lo genera; no se commitea lleno) · data/curacion-registro/{cola-adquisicion-registro.tsv, relaciones.tsv, aliases-fuentes.tsv, baseline.json} · data/cola-adquisicion-v1_0.tsv (vista regenerada) · data/INFRAESTRUCTURA-v1_0.md (línea de --escanea recursivo + alta del script) · forense/notas/2026-09-0X-MAESTRA36-A1-*.md · forense/hallazgos.md · forense/firmas-pendientes.tsv · tests/baseline.json (recifrado) · cascada (canon/gobernanza-v1_15.md, canon/registro-rotulos.tsv, canon/estado-programa-v1_11.md L0). NO toca: milpa/**, forense/prereg-duelo-v2/**, canon/modelo-decision*, .claude/commands/**, instrucciones-proyecto*, la raíz downloads, y ninguna de las 106 entradas descargas_mx existentes. Actos en paralelo y sus archivos: ver CARRILES. Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.

FP/ADR CANDIDATOS (derivados contra 9af8407, no heredados) grep -oE '^\*\*ADR-[0-9]+' canon/gobernanza-v1_15.md | grep -oE '[0-9]+' | sort -n | tail -1 → 308, candidato ADR-309. grep -oE '^FP-[0-9]+' forense/firmas-pendientes.tsv | grep -oE '[0-9]+' | sort -n | tail -1 → 256; rango pre-asignado FP-257 (recibo del lote) y FP-258 (clase (c) de P0: archivos en la raíz sin decisión de mesa — solo si la clase no está vacía). Renumera quien fusiona segundo. Trámites que este acto puede cerrar de paso si su tabla lo permite: FP-233 (cron instalado 2/sep → EJECUTADA) y FP-251 (estado v1_11 fusionado → marcar) — solo si mesa lo pide en la línea de lanzamiento; si no, se dejan.

CONTADOR Manifiesto ids 1 070 → 1 070 + N (N = NO-REGISTRADO clases a+b de P0, reportado, no prometido) · filas de cola OBTENIDO +k · universo A.13 de la raíz medido por primera vez con un solo mecanismo (una cifra, no tres). Medición de modelo: cero directo, declarado — este acto es de adquisición e infraestructura de registro.

Lo que este acto NO hace No descarga nada de red (ni con curl ni con navegador). No registra la clase (c) sin firma. No reescribe las 49 entradas con prefijo ni las 57 sin él. No toca downloads. No lanza L12 ni el censo CompraNet: los habilita. No convierte la regla «archivos ajenos en la raíz» en test: nada de esto es verificable desde la suite sin el disco (misma exención que Bloque D).

Sucesores declarados, no lanzados MAESTRA36-L12 · MPS-2012-CROSSTABS (caja; compuerta por producto: ids icpsr35024_crosstabs_* en origin/main:data/manifiesto.yaml) · censo de diccionarios CompraNet (DD_PIC_CONTRATOS_2400703.xlsx, DD_PIC_EXPEDIENTES.xlsx, DD_RUPC_240912.xlsx) para contestar la pregunta de llaves de EXT-OF-05 antes de bajar la serie 2010–2025 · una línea en hallazgos.md: la etiqueta EXT_OF_07 de la fila 63 apunta a contenido EXT-OF-05.

═══ ANEXO · tools/barrido_descargas_vs_manifiesto.py (créalo verbatim; A.3: lo que el encargo necesita va inline) ═══

```python
#!/usr/bin/env python3
"""Barrido A.8 de solo lectura: ¿qué hay en las carpetas de descargas que el
manifiesto NO conoce? Cruza por sha256 (dedup real), no por nombre.

Uso (desde el clon, WSL):
  python3 tools/barrido_descargas_vs_manifiesto.py \
      "/mnt/c/Users/PC0/Descargas MX" "/mnt/c/Users/PC0/Descargas MX/Descargas Manuales"

Si la segunda es subcarpeta de la primera, pásala igual: el reporte lo dice.
No escribe en el manifiesto ni en ninguna otra parte.
"""
import hashlib, os, re, sys

MANIFIESTO = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "manifiesto.yaml")
if not os.path.exists(MANIFIESTO):
    MANIFIESTO = "data/manifiesto.yaml"

def leer_manifiesto(ruta):
    txt = open(ruta, encoding="utf-8").read()
    por_sha, por_nombre = {}, {}
    for ent in re.split(r"\n- id: ", txt)[1:]:
        mid = ent.split("\n", 1)[0].strip()
        sha = re.search(r"^\s+sha256:\s*['\"]?([0-9a-f]{64})", ent, re.M)
        arc = re.search(r"^\s+archivo:\s*(.+)$", ent, re.M)
        raiz = re.search(r"^\s+raiz:\s*(\S+)", ent, re.M)
        if sha:
            por_sha[sha.group(1)] = mid
        if arc:
            base = os.path.basename(arc.group(1).strip().strip("'\""))
            por_nombre.setdefault(base, []).append((mid, raiz.group(1) if raiz else "data_raw"))
    return por_sha, por_nombre

def sha256_de(p, bufsize=1 << 20):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(bufsize), b""):
            h.update(chunk)
    return h.hexdigest()

def main(rutas):
    por_sha, por_nombre = leer_manifiesto(MANIFIESTO)
    print(f"manifiesto: {MANIFIESTO} · entradas con sha256: {len(por_sha)}")
    vistos = set()
    for raiz in rutas:
        raiz = os.path.abspath(raiz)
        print(f"\n=== {raiz}")
        if not os.path.isdir(raiz):
            print("   NO-ACCESIBLE: no es carpeta en esta máquina"); continue
        reg, nuevo, conflicto, n, ya = [], [], [], 0, 0
        for dp, _, fs in os.walk(raiz):
            for f in fs:
                p = os.path.join(dp, f)
                if p in vistos:
                    ya += 1; continue
                vistos.add(p); n += 1
                rel = os.path.relpath(p, raiz)
                try:
                    s = sha256_de(p)
                except OSError as e:
                    print(f"   ERROR-LECTURA {rel}: {e}"); continue
                if s in por_sha:
                    reg.append((rel, por_sha[s]))
                elif f in por_nombre:
                    conflicto.append((rel, por_nombre[f]))
                else:
                    nuevo.append((rel, os.path.getsize(p)))
        print(f"   archivos examinados: {n} · REGISTRADO(sha coincide): {len(reg)} · "
              f"NO-REGISTRADO: {len(nuevo)} · MISMO-NOMBRE-OTRO-SHA: {len(conflicto)}"
              + (f" · ya cubiertos por una raíz anterior (subcarpeta): {ya}" if ya else ""))
        for rel, sz in sorted(nuevo):
            print(f"   NO-REGISTRADO  {sz:>12,d}  {rel}")
        for rel, ids in sorted(conflicto):
            print(f"   MISMO-NOMBRE-OTRO-SHA  {rel}  ↔ {ids}")
    print("\nA.13: los conteos de arriba son por comando os.walk; un 0 en NO-REGISTRADO "
          "con 'archivos examinados' > 0 sí es un negativo.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    main(sys.argv[1:])
```

Probado por dirección contra un caso con respuesta conocida (2 archivos, 1 en subcarpeta → 2 examinados, 2 NO-REGISTRADO; la subcarpeta pasada aparte → 0 examinados, 1 ya cubierto). Nota: la ruta de MANIFIESTO sube dos niveles porque el script vive en tools/.

---

## ENMIENDA DE DIRECCIÓN a mitad de acto, verbatim

ENMIENDA DE DIRECCIÓN a mitad de acto · ACTO MAESTRA36-A1 · 2/sep/2026 · contra 9af8407. Sustituye el texto de P2 y precisa P1. Todo lo demás del encargo sigue vigente.

P1, precisión. El --grupo de --escanea aplica fnmatch sobre el nombre; tras el parche, aplícalo sobre la ruta relativa a la raíz (Descargas Manuales/*.dta, academico/icpsr35024/crosstabs/*), no sobre el basename, y dilo en la ayuda del flag. El control de regresión sobre raíz plana no cambia.

P2, vía correcta (la de las 106 entradas existentes, no --registra). --registra es solo para data/raw/ y no acepta raíz: verificado, 0 líneas de --raiz en tests/manifiesto.py. Para descargas_mx la vía es:

python3 tests/manifiesto.py --escanea descargas_mx --grupo '<patrón sobre ruta relativa>' --url '<url_origen real>' --usado-para '<fila del registro que satisface>', una invocación por grupo de P0 clase (a); para clase (b) sin URL conocida, --escanea sin --url y deja # PENDIENTE. El script deriva sha256/tamaño/fecha_descarga del archivo real (mtime) — nada se teclea. Dedup por sha256: lo que P0 marcó REGISTRADO no debe aparecer como nuevo; si aparece, PARO de pieza y reporta.
python3 tests/manifiesto.py --promueve mueve el staging al manifiesto; lo que no tenga url_origen confirmada queda con url_origen_procedencia marcada, como hizo REG-LOTE3. data/manifiesto-staging.yaml no se commitea lleno.
--verifica una invocación por --id (A.1), salida cruda pegada; las tres respuestas no se colapsan.
Registro de cola: data/curacion-registro/cola-adquisicion-registro.tsv, fila por fuente_canonica, editada por línea: estado_A4A5=OBTENIDO, ids_manifiesto=<ids>, nota con fecha, quién descargó y el comando exacto. Si no existe fila, créala con origen=REGISTRO_MANUAL_A4V1_1:2026-09-02 — es la vía de forense/notas/2026-09-01-A4-v1_1-propuesta-registrar-manual.md, propuesta sin sellar: se cita como vía, no como canon. El vocabulario del registro (OBTENIDO/PENDIENTE/NO-ACCESIBLE/NO-OBTENIDO-POR-ESTE-AGENTE(N)) no se traduce al de A.4; P3 usa A.4 aparte.
Alta en las tres tablas solo para clase (a) con necesidad identificable, siguiendo tools/curador_registro/GUIA-CURADOR-REGISTRO.md §«alta de fuente nueva en tres tablas»: relacion_id importado de baseline.py (nunca reimplementado), OE-/PROV- derivados como ahí dice, +1 relación +1 procedencia +1 utilidad en la misma escritura, fusión declarada si hay más de una procedencia, alias en aliases-fuentes.tsv sin fusionar por defecto. Fuente sin N en necesidad-objeto-modelo.tsv → no se inventa: queda clase (b) y se declara.
Recifra data/curacion-registro/baseline.json y valida en verde, sin excepciones: python3 tools/curador_registro/baseline.py data/curacion-registro → "ok": true; python3 tools/curador_registro/via_capa2.py --root . (lectura) y luego --escribe para promover capa2_manifiesto. Reserva FP-246, vigente: via_capa2.py resuelve id_manifiesto como un id; una fila con lista ; no se promueve ni se contradice — decláralo, no lo fuerces ni parches via_capa2.py (fuera de perímetro).
python3 tools/vista_cola_adquisicion.py regenera data/cola-adquisicion-v1_0.tsv antes del commit (T26).
data/INFRAESTRUCTURA-v1_0.md: línea 23 gana «recursivo, archivo = ruta relativa a la raíz (desde ADR-309)» y el alta de tools/barrido_descargas_vs_manifiesto.py.

Perímetro: se añaden data/curacion-registro/{evidencias.tsv, utilidad-modelo.tsv, fusiones-relaciones.tsv, necesidad-objeto-modelo.tsv} (lectura obligatoria, escritura solo por el paso 5) y data/manifiesto-staging.yaml (temporal). Frase del perímetro sin cambio. Contador sin cambio.

---

## CONSUMIDO

**PR #500** · rama `acto/maestra36-a1-escanea-recursivo` · `ADR-310` · 2/sep/2026 (cierre en la madrugada del 3/sep).

Ejecutado en UBUNTU, caja propia `/home/pc0/mm-maestra36-a1`, contra el SHA de redacción
`9af8407`, que era `origin/main` EXACTO al arrancar. `main` avanzó durante el acto (`PR #495`,
`#496`, `#497`) y se re-fusionó contra `6019bd7` antes de derivar el ADR; el candidato `309` que
este encargo preasignó quedó tomado por `PR #495` (`MAESTRA36-N1`) y se **renumeró a `310`** —
regla de la casa, renumera quien fusiona segundo. `PR #498` entró después y no toca este perímetro.

Las cuatro piezas se ejecutaron. Desviaciones y decisiones que el ejecutor tomó y declaró, para
que esta auditoría no dependa de leer los commits:

- **`FP-258` no se abrió por la clase (c)**: el encargo condicionaba su apertura a que la clase no
  estuviera vacía, y salió **vacía** (0 de 33 objetos). El número se reusó para otro hallazgo
  medido, declarado en la propia fila.
- **`FP-259` se abrió fuera del rango preasignado** (`257`/`258`), por ser una decisión de mesa
  medida y no un residuo. Declarado en la fila.
- **`OECD` quedó `NO-ACCESIBLE` y no `OBTENIDO`**, apartándose del defecto que la enmienda fijaba
  para las filas que P2 mueve: lo hallado es el formulario *Terms of Use*, no el microdato.
- **Cero altas en las tres tablas del curador**: es el resultado de aplicar la regla de la propia
  enmienda («fuente sin `N` → no se inventa»; alta solo para fuente nueva), no un faltante.
- **Se repararon dos defectos de `tests/manifiesto.py` que el encargo no pedía**, ambos dentro del
  perímetro que sí declaraba: el plegado YAML que corrompía el staging (preexistente, y que
  bloqueaba materialmente el `--url`/`--usado-para` que la enmienda ordenaba usar) y la derivación
  de id, que el propio parche de P1 había roto.
- **Las 2 menciones de `ADR-309` que este archivo conserva son de dirección y no se editaron**:
  un encargo archivado por A.3 no se toca ni para corregirle un número.
