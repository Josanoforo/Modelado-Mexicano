- **SHA de redacción:** `dcc4f6a`
- **Entorno asignado:** cualquiera, SIN red, SIN corpus. Firma de nube `cloud_default` sin sonda (ADR-59(b)). NO en los dos.
- **Estado:** CONSUMIDO — ejecutado por el acto de este mismo commit, rama `claude/censo-explotacion-adr-9rq3xo`, PR #201 (https://github.com/Josanoforo/Modelado-Mexicano/pull/201). Ver `data/censo-explotacion-2026-08-13.tsv` y `forense/notas/2026-08-13-censo-explotacion.md`.

---

Texto completo del encargo, tal como se lanzó (verbatim):

---

ENCARGO A · CENSO DE EXPLOTACIÓN — el contador que el ADR instituye, medido por primera vez

* SHA de redacción: `dcc4f6a`. Entorno: cualquiera, SIN red, SIN corpus. Firma de nube `cloud_default` sin sonda (ADR-59(b)). NO en los dos.
* Entrada 4 del registro de recálculo. Repo-only.

§0 · Por qué
El ADR de provisionalidad —que se está sellando ahora mismo— instituye un contador: `payloads con apertura registrada / payloads en manifiesto`, hoy 8 de 550 = 1.45%. Ese contador nunca se ha derivado con una receta probada, y su ausencia es lo que dejó al programa mirar el 0.09% de su universo durante meses sin notarlo.
Este acto lo deriva, lo prueba, y —lo que más vale— produce la lista nominal de qué payload sirve a qué necesidad y cuál no sirve a ninguna. Eso es lo que ningún artefacto del repo tiene hoy.
§1 · PERÍMETRO
ESCRIBE: `data/censo-explotacion-2026-08-13.tsv` (nuevo) · `forense/notas/2026-08-13-censo-explotacion.md` (1) · `forense/hallazgos.md` (append, merge local siempre) · `forense/encargos/2026-08-13-censo-explotacion.md` (A.3).
NO ESCRIBE: `data/manifiesto.yaml` · `data/curacion-registro/**` · `data/inventarios/**` · `canon/**` · `milpa/**` · `tools/**` · `tests/**` · ningún TSV existente. Fuera de la lista, PARA.
En paralelo: los tres en vuelo. Perímetros disjuntos salvo `hallazgos.md` (`merge=union`; GitHub no lo honra — merge local, `main` HACIA la rama, editor web prohibido).
§2 · ARRANQUE
1 · REPO. Clon existente, ruta absoluta, `git log -1 --format="%h %s"`, `git status`. No desde el home. Worktree propio. 2 · SHA. Base `dcc4f6a`. Tres actos vivos pueden moverla. Refresca y reporta. No es PARO. 3 · `data/raw`. AUSENTE NO ES PARO y aquí es parte del diseño: este acto mide el manifiesto, no el disco. Decláralo y salta. 4 · ENTORNO. Declara cuál. Sin red — salta la sonda. 5 · ESPEJO. Ninguna cifra del espejo.
PREMISAS (script, crudas):
```bash
set -u; cd "$(git rev-parse --show-toplevel)"
python3 -c "import yaml,sys;t=open('data/manifiesto.yaml',encoding='utf-8').read().split(chr(10));i=0
while t[i].startswith('#') or not t[i].strip(): i+=1
m=yaml.safe_load(chr(10).join(t[i:]));print('entradas',len(m),'con payload',sum(1 for e in m if e.get('archivo') and e.get('sha256')))"
ls data/*variables*.tsv                        # los TSV de apertura que existan HOY
ls data/censo-explotacion-*.tsv 2>/dev/null && echo "YA EXISTE - PARA"
```
§3 · COMMIT 1 — la definición, antes de contar
Cuatro estados, cerrados, y el criterio de cada uno escrito antes de aplicarlo:

* `EXPLOTADO` — el payload aparece en un TSV de apertura a nivel variable con reactivo hallado (columna `variable_encontrada` no vacía).
* `ABIERTO-SIN-HALLAZGO` — aparece en un TSV de apertura y su celda es `NO-ENCONTRADO`/`EXISTE-NO-SATISFACE`. Se abrió. Cuenta distinto de no haberlo mirado.
* `REFERENCIADO-NO-ABIERTO` — alguna fila de `relaciones.tsv` lo cita por `id_manifiesto`, pero ningún TSV de apertura lo toca.
* `SIN-DEMANDA` — ninguna fila de `relaciones.tsv` lo alcanza y ningún TSV de apertura lo toca.

La receta se prueba antes de creerla (v2.3). Corre tu regla contra tres casos donde la respuesta se conoce y pega la salida: `ensafi2023_bd_csv_zip` (ABRIR-4 lo abrió → `ABIERTO-SIN-HALLAZGO` o `EXPLOTADO`, dilo) · `enbiare2021_fd_pdf` (ABRIR-4 halló `PB1_01`/`PB2_1` → `EXPLOTADO`) · `latinobarometro2024_bd_stata` (microdato en manifiesto, nadie lo cita → `SIN-DEMANDA`, y verifica que tu regla no lo pierda por el acento del canónico `LATINOBARÓMETRO` contra el id sin acento).
La trampa de identidad, declarada. Cruzar payload↔fuente por subcadena produce falsos positivos medidos: `SE` casa con el "se" de "falsador", `PI` con "estimación propia", `INE` con "diccionario". Usa frontera de letra y normaliza acentos, o declara qué regla usaste y qué falsos positivos deja.
Alcance del universo, declarado (A.4): los payloads con `archivo`+`sha256` del manifiesto en el SHA de tu sesión, y los TSV de apertura que existan ese día. Si APERTURA-ISSP fusiona mientras corres, dilo y decide: o lo incluyes y re-derivas, o declaras el corte. No lo escondas.
Cierra con: "el primer resultado que produzca este procedimiento es el que se reporta."
§4 · COMMIT 2 — el censo
`data/censo-explotacion-2026-08-13.tsv`, una fila por payload:

```
id_manifiesto · archivo · raiz · tamano_bytes · usado_para_declara_uso ·
necesidades_que_lo_citan · tsv_de_apertura_que_lo_toca · estado · universo_declarado
```

Cuatro cifras al cierre, con su comando:

1. `EXPLOTADO` / total — el contador que el ADR instituye.
2. `SIN-DEMANDA` / total — hoy, derivado en esta redacción, ≈321 de 550 (58%). Re-derívalo.
3. `REFERENCIADO-NO-ABIERTO` — la cola real de apertura, ordenada por cuántas necesidades cita cada payload. Este listado es el entregable de mayor rendimiento del acto: dice qué abrir después, por evidencia, no por intuición.
4. Los bloques `SIN-DEMANDA` grandes por prefijo — en esta redacción: `mociba` 48 · `engasto` 46 · `endireh` 41 · `enut` 16 · `banxico` 16 · `enestyc` 15 · `eder` 14. No les inventes canónico ni demanda. Corpus sin necesidad que lo reclame es un hecho, no un defecto: se nombra y se deja.

Suite: `--baseline` VERDE contra `948ad70`. T03: no cites gitignorados entre backticks.
§5 · NO HACE
No abre ningún payload. No toca `relaciones.tsv` ni el manifiesto. No propone qué descargar — mide lo que ya está. No clasifica ningún `SIN-DEMANDA` como sobrante: puede ser demanda futura.
