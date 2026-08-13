# ENCARGO P·LOTE-2 · el lote firmado por evidencia, no por palanca · archivado per convención A.3

**SHA de redacción:** `dcc4f6a` + PR #197 fusionado (SONDA-1).
**Entorno asignado:** CAJA con red y corpus compartido. NO en nube (no alcanza dominios de datos ni tiene los bytes). NO lanzado en los dos.
**Estado:** VIVO al archivarse este texto (13/ago/2026, sesión de ejecución de este mismo acto). La firma de mesa para §1 llegó en un segundo turno de la misma conversación (verbatim, íntegra, abajo) — el acto no arrancó hasta que llegó.

---

## Texto del encargo, tal como se lanzó

Archivado per forense/encargos/convencion.md (A.3) como primer commit, antes del ARRANQUE.

### §0 · Veredicto sobre PR #197, y qué hereda este acto

PR #197 se fusiona sin ajuste. Perímetro exacto (4 archivos, append puro, 0 filas ajenas), A.4 en las 15 filas con universo_declarado real, A.5 con N intentos y salida cruda, A.6 respetada. Los tres pendientes que dejó no son defectos suyos: son traspasos que este acto absorbe, y cada uno está declarado en su nota per P4.

| # | traspaso de SONDA-1 | dónde vive hoy | qué hace este acto |
|---|---|---|---|
| T1 | La cola tiene un DOI mal transcrito en palanca 31 (s41597-025-04999-0 → 404 real; el correcto es s41597-025-04918-9, verificado byte a byte) | nota de SONDA-1 §5, sin editar la cola (fuera de su perímetro) | lo corrige en la cola, §5.1 |
| T2 | 15 fuentes tienen ahora dos filas contradictorias en el puntero: la vieja `gap_mapeo_map_b` con NO-ENCONTRADO (universo = dos tablas internas) y la nueva con sondeo de portal | puntero, 114 filas; declarado stale a propósito | NO las retira (es acto tipo MAP-B) — escribe la regla de lectura, §5.2 |
| T3 | 7 de 9 dominios exigen override de sandbox. SONDA-1 lo declara como límite de la caja, no del portal | nota de SONDA-1, §"allowlist de red" | lo verifica ANTES de congelar el lote, ARRANQUE punto 4-bis |

### §1 · LA FIRMA — mesa la pega verbatim al lanzar; sin ella el acto no arranca

SONDA-1 midió y reordenó. La firma del PLAN v1 (GDELT·11 · ENCOAP·17 · WB_ENTERPRISE·9) resultó, medida: un acierto de tres — GDELT no satisface (base global sin recorte México), ENCOAP limpia, WB_ENTERPRISE con registro pendiente.

Propuesta de SONDA-1, verbatim de su §8:

(A) Agente-ejecutable de punta a punta, cero fricción — 6 fuentes, sirven 7 necesidades (N2, N3, N17, N25, N28, N29, N30): ENCOAP·17 · CNGMD·28 · Banxico_EncuestaCompetenciasFinancieras·33 · JPAL_CorruptionInformation·30 · Zenodo_ElectoralPrecinctLevel·31 · OSF_InteractingAsEquals·12

(B) Carril usuario+navegador, no agente — el patrón que cerró ISSP y WVS tres veces: WorldBank_LargeScaleFinancialEducation·23 y WorldBank_ParentalEmpowerment·35 (cuenta NADA ya activa — solo iniciar sesión y clic) · WORLD_BANK_ENTERPRISE_SURVEY·9 (cuenta nueva, gratuita) · MASS_MOBILIZATION·14 / openICPSR_Microcredit·25 / OECD_TrustSurvey·36 / Cenfri_Microinsurance·38 (reto anti-bot que un navegador real resuelve solo; recetas en el puntero)

(C) Decisión de ingeniería ANTES de cualquier descarga — no es lote: GDELT·11 (>2.5 TB/año) y UCDP·16 (decenas de archivos). Ambas 100 % libres pero globales. Bajarlas sin definir primero el mecanismo de recorte a México es gastar la caja en peso muerto.

Sin esta firma pegada, el acto no arranca. Este documento deja las candidatas medidas; la decisión es de mesa.

### §2 · PERÍMETRO Y CONCURRENCIA

ESCRIBE: el corpus compartido (/home/pc0/mm-corpus/raw, no solo el worktree) · data/manifiesto.yaml (por su vía, §4.2) · data/universo-puertas-2026-08-12.tsv (SOLO filas nuevas, jamás editar ajenas) · data/cola-adquisicion-2026-08-12.tsv (SOLO el campo url_conocida de la palanca 31, §5.1) · data/curacion-universo/decisiones-adquisicion.tsv (por decide_acquisition.py, §4.3) · data/INFRAESTRUCTURA-v1_0.md (una línea, §5.2) · forense/notas/ (1) · forense/encargos/ (A.3) · forense/hallazgos.md (append, merge local siempre — editor web prohibido).

NO ESCRIBE: data/curacion-registro/relaciones.tsv (es del Carril A) · canon/** · milpa/** · tools/** · tests/** · ninguna fila ajena de ningún TSV.

Si te encuentras escribiendo fuera de la primera lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.

En paralelo, verifica cuáles siguen vivos antes de arrancar: CENSO-v1.1 · APERTURA-ISSP · ADR-provisionalidad · CENSO-EXPLOTACIÓN · ALIAS-P · CAPA3-RECONCILIA. Ninguno toca corpus, manifiesto ni puertas. CAPA3-RECONCILIA sí toca relaciones.tsv, que este acto no toca. Sin colisión.

Carga: ALTA (descarga real). Medido 13/ago: 15 GiB + 4 GiB swap, 3 sesiones = 1.73 GiB. El límite es el pico por acto, no el número de sesiones. No lo corras junto con otro acto de microdato pesado.

════════ ARRANQUE ════════

1 · REPO. Clon existente. Ruta absoluta · git log -1 --format="%h %s" · git status. No desde el home. Worktree propio.

2 · SHA. Base dcc4f6a + #197. Verifica que #197 fusionó (git log --oneline -- data/universo-puertas-2026-08-12.tsv, debe traer el commit de SONDA-1). Si no, PARA.

3 · data/raw Y corpus compartido. Este acto descarga: data/raw se enlaza al corpus compartido, no se crea local. `ln -s /home/pc0/mm-corpus/raw data/raw` y `readlink -f data/raw`. Copia data/raices.local.yaml si el worktree no lo hereda. ⚠️ Al cerrar, verifica PR#77: que los payloads quedaron en el corpus compartido, no solo en tu worktree. Ningún test lo atrapa.

4 · ENTORNO. `echo "[$CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE]"` → sin variable · `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` → 200. NUNCA curl -I. Si da 403 host_not_allowed, entorno equivocado: PARA.

4-bis · OVERRIDE DE SANDBOX — traspaso T3, y puede tirar la mitad del lote. SONDA-1 midió: de los 9 dominios de este lote, solo 2 están en el allowlist directo (www.inegi.org.mx → palancas 17/28; www.banxico.org.mx → palanca 33). Los otros 7 exigieron override en su sesión. Tres de las 6 fuentes "cero fricción" del grupo A viven en dominios sin allowlist (povertyactionlab.org, zenodo.org, osf.io). Sondea cada dominio del lote firmado, SIN override, y reporta el código crudo antes de congelar nada. Luego con override. Se declara por fuente: el resultado sin override es el primer dato; el resultado con override es el que se reporta (A.5). Si un dominio del lote no es alcanzable ni con override, esa fuente sale del lote y va al carril usuario — dilo, no la fuerces.

5 · ESPEJO. Ninguna cifra del espejo.

PREMISAS (script, crudas):

```bash
set -u; cd "$(git rev-parse --show-toplevel)"
ls data/cola-adquisicion-*.tsv | sort | tail -1
awk -F'\t' 'NR>1' data/universo-puertas-2026-08-12.tsv | wc -l      # esperado 114 tras #197
python3 -c "import yaml;t=open('data/manifiesto.yaml',encoding='utf-8').read().split(chr(10));i=0
while t[i].startswith('#') or not t[i].strip(): i+=1
print('entradas', len(yaml.safe_load(chr(10).join(t[i:]))))"        # base del contador, crudo
```

Y las dos lecturas obligatorias, íntegras — sus barreras ya están mapeadas, NO las re-descubras: forense/notas/2026-08-12-acto-sonda1-mapa-barreras.md (§5 por fuente, §6 las filas de puerta con sus recetas, §7 PRISMA, §8 la propuesta) y forense/notas/2026-08-12-acto-p-lote1-adquisicion.md (§5 Cloudflare de GESIS, §11 el patrón descargas_mx).

════════════════════════════════════════

### §3 · COMMIT 1 — el lote congelado, antes de tocar red

Las filas de la cola, verbatim (las 8 columnas) para cada fuente firmada, copiadas del TSV, no de este encargo.
La fila de puerta de SONDA-1 para cada una, con su clasificacion_a4, su condicion_acceso y su universo_declarado — es el mapa de barreras y ya está pagado.
El criterio de cierre A.4 por fuente. EXISTE-SATISFACE para esta adquisición exige las cuatro a la vez: (a) payload íntegro en el corpus compartido; (b) sha256 en manifiesto.yaml por su vía; (c) decisión de adquisición por la vía del motor — el TSV de cola nunca se edita a mano para esto; (d) ficha/puerta en el conducto. Si (a)-(c) sí y (d) no → EXISTE-NO-SATISFACE, diciendo qué ficha se buscó. Registro gratuito se hace y no es NO-ACCESIBLE; pago o afiliación institucional sí, con receta manual.
El resultado de 4-bis por dominio, congelado aquí.
Pre-registro de falsación (B-bis). SONDA-1 verificó portada y GET -r 0-0, no descarga completa. Que una fuente falle al bajar íntegra no refuta su sondeo: son dos hechos distintos —"la puerta responde" y "el payload bajó íntegro"— y se reportan con palabras distintas. Un lote que cierre con 3 de 5 está dentro de lo esperado.

Cierra con: "el primer resultado que produzca este procedimiento es el que se reporta."

### §4 · COMMIT 2 — la ejecución

Por fuente, en este orden:

4.1 · Sonda A.5 en sesión sobre la URL de la cola. Falla ⇒ NO OBTENIDO POR ESTE AGENTE EN N INTENTOS + los N intentos con salida cruda + receta manual <1 min. Prohibido concluir nada de un portal desde conocimiento de entrenamiento. Y no te creas la portada: SONDA-1 encontró en INEGI un contentUrl señuelo a prueba.pdf (soft-404 de 2,263 bytes fijos). Verifica todo payload con GET -r 0-0 y compara el tamaño real.

4.2 · Descarga al corpus compartido, luego sha256 por la vía correcta — y aquí hay una trampa medida. tests/manifiesto.py --registra solo resuelve contra data/raw/ (verificado leyendo cmd_registra: no tiene parámetro --raiz). Para cualquier otra raíz, la única vía que funciona es --escanea <raiz> --grupo + --promueve inmediatos, en pares por grupo — nunca N --escanea seguidos de un --promueve al final (defecto de acumulación que ACTO P documentó). Y valores de más de 78 caracteres disparan el defecto de plegado YAML del staging: se parchan después vía escribir_manifiesto() importada del propio script, nunca tecleados a mano.

4.3 · Decisión de adquisición por la vía del motor. tools/curador_registro/decide_acquisition.py existe y funciona; el índice A.7 lo marca "stale — le faltan las 2 decisiones más recientes". Verifica que sigue corriéndose antes de usarlo. Si el motor no tiene vía para algo: hallazgo + EN-ESPERA-DE-VIA. Jamás editar el TSV a mano.

4.4 · Ficha/puerta al conducto — fila nueva por payload adquirido; la fila de sondeo de SONDA-1 no se edita, se añade la de adquisición.

4.5 · PRISMA de 7 cifras: intentadas / sondeadas-200 / bajadas / íntegras / con-ficha / no-accesibles / no-obtenidas. Y verificación PR#77 con el listado del corpus compartido a la vista.

### §5 · LOS TRES TRASPASOS — lo que este acto cierra y que el anterior no podía

**5.1 · T1 · El DOI mal transcrito de la cola**

data/cola-adquisicion-2026-08-12.tsv, palanca 31 (ELECTORAL_PRECINCT_LEVEL_DATABASE_FOR_MEXICAN_MUNICIPAL_ELECTION): url_conocida dice https://www.nature.com/articles/s41597-025-04999-0 → 404 real de Nature, confirmado por SONDA-1 con cookie-jar para descartar bucle de consentimiento. El correcto es s41597-025-04918-9, con título coincidente exacto y Zenodo verificado por API (1 archivo, 739,952,144 bytes, access_right=open).

Corrige SOLO ese campo, SOLO esa fila. Mecanismo: split/join por \t, nunca csv.writer — corrompió 7 filas ajenas de universo-puertas el 13/ago por re-citar comillas. Verifica con git diff --unified=0 que el diff toque exactamente una línea y un campo. Cita la nota de SONDA-1 §5 como procedencia.

⚠️ Si la palanca 31 no está en el lote firmado, corrígela igual — es un dato falso en una tabla vigente y cuesta un minuto. Decláralo como corrección fuera del lote.

**5.2 · T2 · Las 15 fuentes con dos filas contradictorias**

Tras #197 el puntero tiene 114 filas, y 15 fuentes que SONDA-1 sondeó conservan su fila vieja gap_mapeo_map_b diciendo NO-ENCONTRADO — cuyo universo_declarado es, verbatim y en las 62: "buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL". Su universo son dos tablas internas del programa, no un portal. SONDA-1 las dejó intactas a propósito y lo declaró; retirarlas es un acto tipo MAP-B.

Este acto NO las retira. Escribe la regla de lectura, una vez, donde quien lea el puntero la va a ver: en data/INFRAESTRUCTURA-v1_0.md, Dominio 2, una línea:

"Cuando dos filas describen la misma fuente, manda la de fecha_sondeo más reciente cuyo universo_declarado cite un portal, no una tabla interna del programa. Las 62 filas gap_mapeo_map_b declaran universo interno por construcción (MAP-B, 13/ago) y quedan superadas por cualquier sondeo de portal posterior. Retirarlas es acto propio."

Deriva el 15 y el 62 en sesión; las cifras de arriba son del 13/ago. No añadas un campo al esquema ni un test. Es una regla de lectura, y su costo es una línea.

**5.3 · T3 · El override**

Ya está en el ARRANQUE 4-bis. Lo que va en la nota al cierre: por dominio, el código sin override y el código con override, crudos. Es la medición del perímetro real de la caja y hoy solo existe como observación de paso en la nota de SONDA-1.

### §6 · EL CONDUCTO DE ESTE ACTO — declarado, per P4

| estación | ¿la alcanza? |
|---|---|
| 1 · exploración | SÍ — sonda, descarga, apertura de portada |
| 2 · tabla consolidada | SÍ — manifiesto, puntero de puertas, decisiones-adquisicion |
| 3 · receta | NO, y va la línea: "no se enlaza ninguna fila de relaciones.tsv porque es del Carril A, un solo escritor. Este acto deja en su nota la lista payload → fuente → relacion_id candidatos, derivada por comando, para que ENLACE-2 la consuma sin re-derivarla." Esa lista es obligatoria, no opcional — es lo que ABRIR-4 no dejó y por eso su hallazgo tardó cinco días en verse. |
| 4 · contrato del motor | NO: "este acto no produce especificación de producción; la produce el acto de estimación que use estos payloads." |

### §7 · CONTADOR

Payloads nuevos íntegros en el corpus compartido, y necesidades cuyo estado cambia por ellos. No capa2 — este acto no toca relaciones.tsv; su lista de §6 es lo que la moverá después.

Y la línea honesta: si el lote cierra con 2 de 5, eso es el resultado. SONDA-1 verificó puertas, no descargas íntegras — son dos hechos distintos y este acto es el primero que mide el segundo.

### §8 · NO HACE

No toca relaciones.tsv. No abre nada a nivel variable (es acto posterior, por demanda). No retira las 15 filas viejas del puntero. No baja GDELT ni UCDP salvo que la firma de §1 lo diga explícitamente y con mecanismo de recorte definido. No edita el TSV de cola salvo el campo de §5.1. No fuerza ninguna fuente que su dominio no alcance — la manda al carril usuario y lo dice.

---

## La firma de mesa (§1), llegada en el segundo turno — verbatim

VENTANA 4 · P·LOTE-2 — la firma

Pega esto en el hueco de §1:

```
Lote 2 = ENCOAP·17 · CNGMD·28 · Banxico_EncuestaCompetenciasFinancieras·33 ·
         Zenodo_ElectoralPrecinctLevel·31 · OSF_InteractingAsEquals·12

Fuera del lote, con razón: JPAL_CorruptionInformation·30 — del grupo A, sin
objeción; queda para el siguiente lote por ser la de menor palanca de las seis.
Nada del grupo B ni del C entra a este acto.

GDELT·11 y UCDP·16: NO se tocan en este acto. Se adopta la lectura de SONDA-1
§8: 100% libres pero globales, sin mecanismo de recorte a México definido;
bajarlas completas es peso muerto. Su tratamiento es un acto de ingeniería
propio, no un lote de descarga.
```

Y una advertencia que ya está en tu punto 4-bis y que quiero que trates como paro real: de los cinco firmados, solo tres viven en dominios con allowlist directo (ENCOAP y CNGMD en inegi.org.mx, Banxico en banxico.org.mx). Zenodo y OSF exigieron override en la sesión de SONDA-1. Sondea los cinco dominios sin override primero, reporta el código crudo, luego con override. Si Zenodo u OSF no alcanzan ni con override, salen del lote y van al carril usuario — dilo, no los fuerces. El lote firmado admite cerrar con tres.

Y la corrección de §5.1 va aunque la palanca 31 salga del lote: el DOI de ELECTORAL_PRECINCT_LEVEL_DATABASE en data/cola-adquisicion-2026-08-12.tsv es falso (404 real). El correcto es s41597-025-04918-9, verificado byte a byte por SONDA-1. Un campo, una fila, split/join, git diff --unified=0 a la vista.

---

**Nota de la sesión ejecutora:** antes de aceptar esta firma se verificaron en frío los cinco pre-requisitos que el encargo exige (PR #197 MERGED en origin/main como `5f90757`; 114 filas en el puntero con el commit de SONDA-1 presente; entorno CAJA correcto, sin variable de nube, INEGI 200; sin colisión con los únicos dos PR abiertos, #198 y #199; ningún worktree P·LOTE-2 preexistente) antes de pasarle la decisión a mesa. Esa verificación se hizo en la conversación, no en este repo, y queda referenciada aquí por transparencia del proceso — el resultado operativo (los cinco checks) se re-deriva de todos modos en las PREMISAS de este mismo acto, en frío, contra el estado real del worktree.
