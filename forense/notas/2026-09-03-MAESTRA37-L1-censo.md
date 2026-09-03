# MAESTRA37-L1 · P0 — censo de la raíz `descargas_mx` (COMMIT-1)

Censo por **disco**, no por el rótulo `raiz:` del manifiesto (enmienda de
dirección recibida a mitad de acto, 3/sep/2026, precedente ADR-273/286):
se recorre `data/raices.local.yaml → descargas_mx` (`/mnt/c/Users/PC0/Descargas MX`)
archivo por archivo, se calcula `sha256` completo de cada uno, y se cruza
**por sha256** (no por nombre) contra `data/manifiesto.yaml`. Metadato
puro — ningún byte de contenido se abrió en este paso, solo hashing y
`Path.suffix`.

Script: `censo_p0_v2.py` (efímero, no forma parte del perímetro tocado —
la lógica relevante queda documentada aquí verbatim para reproducibilidad).

## Resultado — tres clases, no colapsadas

| clase | n archivos en disco | qué significa |
|---|---|---|
| `DECLARADO-descargas_mx` | 150 (138 `payload_id` únicos) | el sha256 del archivo coincide con una entrada del manifiesto cuya `raiz:` es `descargas_mx`. 8 `payload_id` tienen más de una copia física en disco (duplicados exactos, mismo sha) |
| `DECLARADO-OTRA-RAIZ` | 73 | el sha256 coincide con una entrada del manifiesto, pero esa entrada **no** declara `raiz: descargas_mx` (73/73 sin ninguna clave `raiz:` — bloque `(default)`). Éste es el recuento re-derivado por este acto, no el heredado de FP-259 (que citaba 77): **73, no 77** — declarado el propio, no el heredado, por instrucción de dirección |
| `SIN-REGISTRO` | 1 (`descargas.php`, 141 181 bytes, ext `.php`) | ningún sha256 del manifiesto coincide. No es un payload de datos: nombre y extensión son consistentes con una página HTML/PHP guardada por error del navegador, no con un microdato o catálogo. No se abre para confirmarlo (fuera de perímetro; sería abrir un byte) |

Total de archivos bajo el disco de `descargas_mx`: **224**
(150 + 73 + 1).

Los 138 `payload_id` de `DECLARADO-descargas_mx` son exactamente los 138
que `grep -c "raiz: descargas_mx" data/manifiesto.yaml` cuenta en el
manifiesto — el censo por disco reproduce el censo por manifiesto para
esta clase, más el hallazgo nuevo de duplicados físicos.

## Clasificación por extractor (sobre las 223 filas `DECLARADO-*`, excluye `SIN-REGISTRO`)

| clase_extractor | n | qué extractor las despacha hoy |
|---|---|---|
| `DESPACHADO-INSPECT_ASSETS` | 211 | `tools/curador_registro/inspect_assets.py` (zip/pdf/xlsx/xls/html/csv/tsv/txt/json/xml) vía `tools/inventario_reactivos.py` |
| `DESPACHADO-EXT` | 9 | formatos estadísticos (.dta/.sav/.por/.sas7bdat/.xpt/.dbf/.rdata/.rds) — el *tipo* de formato ya tiene extractor en `tools/inventario_reactivos_ext.py`, aunque ese script hoy fija su propio perímetro por `cobertura-composicion-v1_0.tsv` causa B y no acepta `--raiz` (ver P1) |
| `SIN-EXTRACTOR-DECLARADO` | 3 | `.docx` (2, sobre las 138 `DECLARADO-descargas_mx`: `indice_de_bienestar_cuestionarios`, `tc_oecd_trust_survey_pum_2021_2023_2025`) y `.php` (1, el `SIN-REGISTRO`). No se inventa extractor — tope declarado en `tools/inventario_reactivos.py:9` |

Por extensión, sobre los 138 `payload_id` `DECLARADO-descargas_mx` (censo
por manifiesto, ADR-320 P0 original antes de la enmienda de disco):
`.zip`=50 · `.pdf`=49 · `.xlsx`=10 · `.xls`=10 · `.dta`=5 · `.txt`=4 ·
`.xml`=3 · `.sav`=3 · `.docx`=2 · `.csv`=2. Los 138 sha256 del manifiesto
coinciden con el sha256 en disco en el 100% de los casos (0 `AUSENTE`, 0
`sha discrepante`).

## `DECLARADO-OTRA-RAIZ` — qué son las 73

Las 73 son archivos físicamente presentes en el árbol `descargas_mx` cuyo
contenido (por sha256) ya está registrado en el manifiesto bajo otra
entrada — es decir, el mismo byte-idéntico vive ahí Y en otra ruta que el
manifiesto sí etiquetó con una raíz distinta (o sin raíz declarada,
bloque `(default)`, que el propio manifiesto documenta como resuelto
contra `data/raw`). Este acto **no reclasifica ni edita `raiz:`** en el
manifiesto — eso sigue siendo de mesa (FP-259). El inventario de P1 los
cubre igual que a los 138, con `payload_id` tomado del manifiesto.

## Formulaciones congeladas — las 25 reglas de Ola 6

Verbatim, copiadas de `forense/notas/2026-09-03-mapeo-ola6-N5.md`
(`ACTO MAESTRA34-N5`), sin editar. Se corren tal cual contra la tabla
nueva en P2 — no se mejoran, no se agregan formulaciones nuevas.

### `trabajo` (§3.2, 4 reglas)
- `trabajo.jerarquia.deferencia_iniciativa_suprimida`: `--regex "jefe\|superior jerarquic\|obedec"` · `--palabra iniciativa --palabra "opinar en el trabajo"` · `--regex "(no \|)se (atreve\|puede).{0,30}(jefe\|patron)\|contradecir"`
- `trabajo.liderazgo.benevolencia_legitima`: `--regex "su jefe.{0,40}(trata\|apoya\|ayuda\|preocup)"` · `--palabra "satisfaccion con su trabajo" --palabra "satisfecho con su trabajo"` · `--regex "trato.{0,30}(jefe\|patron\|supervisor)\|..."`
- `trabajo.prestaciones.formalidad_pesa_mas_que_salario`: `--palabra infonavit --palabra aguinaldo` · `--regex "prestacion(es)?\b"` · `--regex "(salario\|sueldo\|ingreso).{0,40}prestacion\|prestacion.{0,40}(salario\|sueldo)"`
- `trabajo.rotacion.joven_urbano_sin_culpa`: `--regex "cambi\w+ de (empleo\|trabajo)\|dej\w+ (su\|el) (empleo\|trabajo)"` · `--palabra "por que dejo" --palabra "motivo por el que dejo"` · `--regex "busc\w+ (otro\|un) (empleo\|trabajo)"`

### `salud` (§3.4, 5 reglas)
- `salud.atencion.leve_sin_imss`: `--regex farmacia` · `--palabra automedic` · `--regex "(donde\|lugar).{0,40}(se atendio\|atencion medica\|consulta)"` · `--regex "grave\|gravedad\|severidad"`
- `salud.atencion.grave`: `--regex "(imss\|issste\|centro de salud\|hospital publico\|seguro popular\|insabi)"` · `--regex "(atenc\|atend\|consult).{0,35}(imss\|issste\|salubridad\|privad\|publico)"` · `--regex "grave\|gravedad\|severidad"`
- `salud.prevencion.hombre_sin_permiso`: `--regex "(chequeo\|revision\|examen).{0,30}(medic\|general\|prostata\|prevent)"` · `--regex "(no (fue\|acudio\|asistio)\|pospus\|dejo de ir).{0,30}(medico\|consulta\|clinica)"` · `--regex "prestacion(es)?\b"`
- `salud.adherencia.desabasto_vs_cuidadora`: `--regex "(dejo\|abandon\|interrump).{0,30}(tratamiento\|medicament)"` · `--regex "surti\w+.{0,25}(medicament\|receta)\|receta.{0,25}surti"` · `--regex "farmacia"`
- `salud.consumo.sellos_precio_similar`: `--regex "sello\w*.{0,30}(product\|alimento\|etiquet)\|etiquetado frontal"` · `--regex "grave\|gravedad\|severidad"` (control) · `--regex farmacia` (control)

### `tiempo` (§3.6, 4 reglas)
- `tiempo.puntualidad.formal_vs_social`: `--palabra puntual --palabra "llega tarde" --palabra retraso` · `--regex "(posterg\|pospon\|dejar para despues)"` · `--regex "recordatorio\|le recordaron\|mensaje.{0,20}cita"`
- `tiempo.compromiso.si_voy_incierto`: `--regex "cortes\|quedar bien\|pena decir"` · `--regex "decir que no\|rechaz\w+.{0,30}(invitacion\|peticion)"` · `--palabra puntual --palabra "llega tarde"`
- `tiempo.bomberazo.recursos_escasos_urgencias`: `--regex "(posterg\|pospon\|dejar para despues)"` · `--regex "(dejo\|abandon\|interrump).{0,30}(tratamiento\|medicament)"` · `--palabra retraso`
- `tiempo.cumplimiento.recordatorio_baja_barrera`: `--regex "recordatorio\|le recordaron\|mensaje.{0,20}cita"` · `--regex "(no (fue\|acudio\|asistio)\|pospus\|dejo de ir).{0,30}(medico\|consulta\|clinica)"` · `--regex "(chequeo\|revision\|examen).{0,30}(medic\|prevent)"`

### `cooperación` (§3.8, 4 reglas)
- `cooperacion.comite.monitoreo_sancion_visible`: `--regex "comite\w*"` · `--regex "(participa\|pertenece\|miembro).{0,40}(organizacion\|asociacion\|comite\|grupo)"` · `--regex "(coopera\w+\|aport\w+).{0,35}(obra\|comunidad\|colonia\|vecin)"`
- `cooperacion.tanda.conoce_organizadora`: `--palabra tanda --palabra tandas` · `--regex "tanda.{0,40}(organiz\|quien\|conoce\|confia)\|(organiz\|quien).{0,25}tanda"` · `--regex "(fraude\|no le pagaron\|perdio.{0,20}tanda\|riesgo.{0,20}tanda)"`
- `cooperacion.confianza.puente_personal`: `--regex "confia\w*.{0,35}(desconocid\|gente\|personas\|vecin)"` · `--regex "paisano\|correligionario\|conocido en comun"` · `--regex "(participa\|pertenece\|miembro).{0,40}(organizacion\|asociacion)"`
- `cooperacion.faena.sancion_social_pueblo_mestizo`: `--palabra faena --palabra tequio --palabra "cooperacion vecinal"` · `--regex "(coopera\w+\|aport\w+).{0,35}(obra\|comunidad\|colonia\|vecin)"` · `--regex "comite\w*"`

### `información` (§3.9, 4 reglas)
- `informacion.credibilidad.allegado_confianza`: `--regex "(confia\|cree).{0,35}(informacion\|noticia\|medios\|redes sociales)"` · `--regex "(se entera\|se informa\|donde obtiene).{0,35}(noticia\|informacion)"` · `--regex "verific\w+.{0,30}(informacion\|noticia)\|noticia\w*.{0,25}fals"`
- `informacion.deferencia.costo_acceso_experto`: `--regex "(consulto\|acudio\|pregunto).{0,35}(especialista\|experto\|medico\|profesional)"` · `--regex "(atenc\|atend\|consult).{0,35}(imss\|issste\|privad\|publico)"` · `--regex "(chequeo\|revision\|examen).{0,30}(medic\|prevent)"`
- `salud.vacunacion.disponible` *(id con dominio equivocado, en `§3.9`)*: `--regex "vacun\w+"` · `--regex "(no.{0,15}vacun\|por que no.{0,20}vacun)"` · `--regex "(atenc\|atend\|consult).{0,35}(imss\|issste\|privad\|publico)"`
- `informacion.escuela.miedo_a_caer_clase_media`: `--regex "escuela.{0,25}(privad\|publica\|particular)\|..."` · `--regex "nivel de vida.{0,30}(padres\|hijos)\|mejor\w*.{0,25}que sus padres"` · `--regex "(participa\|pertenece\|miembro).{0,40}(organizacion)"`

### `comunicación` (§3.10, 4 reglas)
- `comunicacion.rechazo.indirecto_face`: `--regex "decir que no\|rechaz\w+.{0,30}(invitacion\|peticion)"` · `--palabra favor --palabra "le pidio"` · `--regex "cortes\|quedar bien\|pena decir"`
- `comunicacion.retroalimentacion.privada_publica_capital_social`: `--regex "(regan\|critic\|llam\w+ la atencion).{0,35}(publico\|frente a\|delante de)"` · `--regex "conflicto.{0,30}(trabajo\|jefe\|companer)"` · `--regex "desacuerdo\|discusion con"`
- `comunicacion.inseguridad.ver_oir_callar`: `--regex "(no denuncio\|por miedo).{0,35}(represalia\|autoridad\|denunciar)"` · `--regex "denunci\w+"` · `--regex "no dijo nada\|prefirio callar\|guardar silencio"`
- `comunicacion.directividad.regional_generacional`: `--regex "(dice lo que piensa\|expresa\w* su opinion\|se queda callad)"` · `--regex "asertiv\|directo al hablar\|habla claro"` · `--regex "exig\w+.{0,30}explicacion\|pedir\w*.{0,25}explicacion"`

`la frase que este acto congela, verbatim (2026-09-03): «el primer resultado que produzca este procedimiento es el que se reporta».`
