# ACTO MAESTRA34-L1 · MORDIDA-SERIE — cierre

Encargo: `forense/encargos/2026-09-01-MAESTRA34-L1-MORDIDA-SERIE.md`
(dirección/Fable, 1/sep/2026, formato corto v2.12, SHA de redacción
`8598a72` = merge PR #447). Entorno UBUNTU (abre microdato ENCIG, A.2).
Firmas de mesa: D2-b (P1+P2+P3 completo), D3-a (P4, con salvaguarda
NO-OBTENIDO).

## ARRANQUE

1. **REPO**: worktree nuevo `/home/pc0/mm-l1-mordida-serie` (rama
   `acto/maestra34-l1-mordida-serie`), creado desde `origin/main` en
   `92fd3f7` — el worktree principal (`/home/pc0/Modelado-Mexicano`)
   estaba parado en una rama WIP ajena (`acto/maestra32-e18-reglas-ola5-fase1`),
   no se usó para no operar sobre premisas falsas ([[feedback_f0_corre_en_la_caja_del_acto]]).
2. **SHA**: `8598a72` es ancestro de `origin/main` (confirmado
   `git merge-base --is-ancestor`). `origin/main` se movió dos veces
   antes de arrancar (`bb54f99`+`92fd3f7`, el propio gesto COLA que
   archivó este encargo) — sin diferencia de perímetro. Se movió una
   TERCERA vez a medio acto (PR #449, `ACTO MAESTRA34-N1`, tomó
   `ADR-274`): perímetro disjunto declarado en CARRILES, confirmado por
   diff (`milpa/tramite.yaml` cargas VERBATIM de otras 2 reglas,
   `milpa/tramite-ola5-propuesta-v0.yaml` solo cabeceras `SELLADA` sobre
   entradas preexistentes) — merge limpio, sin `CONFLICT`, 0 `**ADR-`
   duplicados verificados a mano tras el sync
   ([[feedback_gobernanza_automerge_duplica_adr]]).
3. **data/raw**: ausente al crear el worktree (esperado, raíz gitignorada)
   — enlazada a `/home/pc0/mm-corpus/raw`.
4. **ENTORNO (A.2, tres partes)**: `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE`
   sin definir (`<sin_variable>`, UBUNTU/caja); `curl` a inegi.org.mx →
   `200`; `ls data/raw | head -1` → no vacío (corpus montado, 328
   entradas). Los tres confirman caja, coherente con ENTORNO ASIGNADO.
5. **ESPEJO**: ninguna cifra de este acto sale del espejo del proyecto;
   todas del clon de (1), comandos citados abajo.

**CARRILES**: verificado `gh pr list --state open` → vacío antes de
arrancar (ningún otro acto de caja en vuelo).

## P1 · Calibración ENCIG 2025

Variable `P8_3_1` (sección VIII, "intento de apropiación de algún
beneficio" — verificado contra el diccionario de datos embebido en
2017/2019/2021/2023, ver más abajo; 2025 no trae diccionario propio en
el ZIP, se asume por continuidad estructural, declarado). Codificación
idéntica a TRA-M-07 (1=Sí, 2=No, 9 fuera). Ponderador `FAC_P18`, diseño
`EST_DIS`/`UPM_DIS`. IC95 por bootstrap de conglomerado estratificado
(10 000 réplicas, seed 42, `tools/calibracion_mordida_encig_serie.py`,
estimador idéntico a `tools/tasas_base_ola6_activos.py`).

**Resultado (único, "el primer resultado que produzca este
procedimiento es el que se reporta")**: p=0.085118, IC95=[0.080935,
0.089260], n=40042 (de 40136 filas leídas, 94 fuera de universo),
estratos=442, UPM=9172.

## P2 · Serie histórica ENCIG 2011/2015/2019/2023

Verificación cruzada de semántica de variable contra el diccionario de
datos embebido en cada ZIP (no supuesta por nombre de columna):

| ola | variable | fuente de verificación | nota |
|---|---|---|---|
| 2017/2019/2021/2023 | `P8_3_1` | diccionario embebido, confirmado en las 4 | "intento de apropiación de algún beneficio", 1er ítem de batería de 3 |
| 2015 | `P8_3` (NO `P8_3_1`) | diccionario embebido | `P8_3_1` en 2015 es CONTEO de trámites, no Sí/No — rompe el patrón |
| 2013 (ya público, TRA-M-03) | `P8_3` | cita codificacion-R-v1_0.tsv | mismo patrón que 2015 |
| 2011 | `P4_11` (tabla por-trámite, colapsada a persona) | FD_ENCIG2011.pdf (extraído con pypdf) | pregunta agregada, sin descomponer en los 3 ítems de 2015+ |

**2011 requiere colapso**: `03_ENCIG2011_tramites.dbf` es una tabla
POR-TRÁMITE (hasta 29 filas por persona, `N_TRA`). Se colapsó a persona
(`ENT+CON+V_SEL+N_HOG+R_ELE`, verificado 0 de 24820 personas con
`FAC_P18`/`EST_DIS`/`UPM_DIS` inconsistentes entre sus filas): y=1 si
CUALQUIER fila válida (`P4_11` en {1,2}) de la persona es '1'; se
excluye a la persona solo si TODAS sus filas quedan en blanco (1036 de
24820, 4.2%).

**Resultados** (todas bootstrap-conglomerado excepto donde se cita
"R-json", el método ya sellado de TRA-M-03/05/07 — método distinto,
puntos comparables, ancho de IC95 no homologado, declarado):

| ola | p | IC95 | n | método |
|---|---|---|---|---|
| 2011 | 6.8328% | [6.0955, 7.6391]% | 23784 | bootstrap (este acto) |
| 2013 | 4.4538% | [3.8969, 5.0107]% | 22081 | R-json (TRA-M-03, ya público) |
| 2015 | 4.7684% | [4.3130, 5.2521]% | 26417 | bootstrap (este acto) |
| 2017 | 7.7024% | [7.2671, 8.1378]% | 39085 | R-json (TRA-M-05, ya público) |
| 2019 | 8.4484% | [7.9530, 8.9737]% | 39454 | bootstrap (este acto) |
| 2021 | 7.1815% | [6.7118, 7.6512]% | 39763 | R-json (TRA-M-07, ya público) |
| 2023 | 7.2863% | [6.8865, 7.6988]% | 38838 | bootstrap (este acto) |
| 2025 | 8.5118% | [8.0935, 8.9260]% | 40042 | bootstrap (este acto, = P1) |

Rango de la serie completa (8 olas, 15 años): **4.45%–8.51%**, muy por
debajo del 0.62 ASIGNADO en las 15 olas·años. Extiende ADR-270 (que
citaba solo 3 olas, rango 4.45–7.70%).

## P3 · Censo `tramite.mordida.con_registro`

**Veredicto A.4 (COMMIT-1): EXISTE-SATISFACE.** Ítem: `P7_3` ("¿A qué
tipo de lugar acudió o a qué medio recurrió para realizar el trámite o
pago?"), sección VII de ENCIG 2025 — categorías 1=instalaciones de
gobierno, 2=banco/súper/tienda, 3=líneas telefónicas, 4=Internet
(página web, apps), 5=cajero automático/kiosco, 6=módulos/oficinas
móviles, 7=no concluido, 8=otro, 9=no sabe. Fuente:
`encig25_estructura_base_datos.pdf`, página 54 de 72 (**las 72 páginas
se leyeron completas** con `pypdf`, A.13). Archivo examinado completo:
`encig2025_04_sec_7.csv` (124314 filas, todas leídas).

**COMMIT-2**: `P7_3` vive en `sec_7` (tabla de detalle de UN trámite
por persona), no en `sec_8` (roster completo de trámites, donde vive
`P8_4` — "¿en cuál de los trámites se suscitaron las circunstancias
[corrupción declarada en sección VIII]?", Sí/No por trámite, gateado a
solo 21139 de 1083672 filas: personas que ya declararon alguna práctica
de corrupción). Join por `ID_TRA`: `sec_7` deduplicada (10597
duplicados EXACTOS verificados, mismos valores en las 4 columnas
relevantes) está totalmente contenida en `sec_8` (113717 de 113717).
Unidad de análisis = **trámite**, ponderador `FAC_TRA` (no `FAC_P18`,
declarado — unidad distinta de P1/P2).

Mapeo operacional (juicio de este acto, declarado, no dictado por el
dato): canal con registro automático (`P7_3` en {3,4,5}) ≈
`quien_observa=registro_o_testigos`; canal presencial (`P7_3=1`) ≈
`quien_observa=nadie` (regla discrecional). Categorías 2/6/7/8/9
excluidas por ambigüedad de clasificación (declarado, no forzado).

**Resultado**: presencial p=11.60% IC95=[10.27,13.11]% n=9937,
estratos=381, UPM=2992; digital/registrado p=2.74% IC95=[1.87,3.79]%
n=6337, estratos=361, UPM=2514. **IC95 sin traslape** — primer apoyo
empírico directo, de escala y de orden, al mecanismo "el registro rompe
la trampa social" que la regla `con_registro` ya declaraba sin medir.

Reserva declarada: `P8_4` solo se pregunta a un subconjunto ya
auto-seleccionado (personas con alguna práctica de corrupción
declarada en sección VIII) — esta `p` no es la incidencia sobre el
universo completo de trámites, sino sobre ese subconjunto.

## P4 · Cívica concurrente (D3-a) — NO-OBTENIDO-POR-ESTE-AGENTE (5 intentos)

**COMMIT-1 (diseño congelado antes de bajar nada)**: unidad =
municipio/distrito; desenlace = participación electoral; contraste =
elección local concurrente (mismo día que proceso federal) vs. no
concurrente, mismo estado, años distintos (diseño de
`2026-09-01-MAESTRA33-E18-P3-L1-spec.md:505-507`). Caso candidato
identificado por fuente oficial (TEPJF, ver intento 1-2 abajo): Yucatán
2006 (gubernatorial NO concurrente) vs. 2012 (gubernatorial concurrente
con presidencial) — participación estatal agregada 66.95% → 77.42%,
pero **a nivel estado, no municipio/distrito** como exige el diseño.

**5 intentos de adquisición, cada uno con comando/resultado crudo**:

1. `WebSearch` "elecciones concurrentes no concurrentes mismo estado
   México participación electoral comparación" → localiza
   `Participación electoral en México, 1991-2018` (TEPJF, acervo
   oficial), que identifica a Yucatán y Baja California como los dos
   casos de referencia del país para este contraste.
2. `WebFetch` del PDF del TEPJF — el convertidor de `WebFetch` falla
   ("PDF altamente comprimido y cifrado", contenido binario); **se
   recuperó** el PDF ya descargado por la propia herramienta y se
   extrajo con `pypdf` (10 páginas, 19404 caracteres, íntegro) — el
   documento da participación **estatal agregada** (Yucatán 2006:
   66.95%, 2012: 77.42%, "cuando eligió gobernador el mismo día que
   Presidente de la República"), no municipio/distrito.
3. `WebSearch` "Yucatán elección 2012 gobernador cómputo distrital...
   IEPAC" → localiza el portal oficial `iepac.mx/micrositios/
   resultados-electorales`, pero sin confirmar cobertura de 2006/2012
   en el resultado de búsqueda.
4. `WebSearch` "INE cómputos distritales... Yucatán 2006 2012..." →
   localiza el sistema oficial **SICEE** (Sistema de Consulta de la
   Estadística de las Elecciones, INE) y su documentación declara
   explícitamente cobertura de elecciones **locales desde 2015** —
   2006 y 2012 quedan **fuera de su ventana de cobertura por diseño del
   propio sistema**, no por falla de búsqueda.
5. `WebFetch` directo de `https://sicee.ine.mx/` (para verificar si un
   estado con calendario no sincronizado post-2015, p.ej. Coahuila,
   tiene el contraste dentro de la ventana SICEE) → SPA sin contenido
   real accesible sin navegador (solo el título de la aplicación),
   mismo patrón ya documentado en este proyecto para portales de
   INE/INEGI (`data/manifiesto.yaml:2729`, ENOE).

**Veredicto**: `NO-OBTENIDO-POR-ESTE-AGENTE (5 intentos)`. No es
ausencia del dato — es una barrera de acceso mecánico (sistema oficial
declarado sin cobertura pre-2015 para el par más documentado, y SPA sin
API pública para verificar alternativas post-2015). La pieza **cierra
aquí, sin afectar P1-P3**, tal como el encargo autoriza.

**Receta de navegador, ≤1 minuto** (para el sucesor o un operador
humano):
1. Ir a `https://www.iepac.mx/micrositios/resultados-electorales` y
   buscar "Gobernador 2012" y, si existe, "Gobernador 2006" — el
   archivo histórico de un OPLE estatal puede no compartir la ventana
   de cobertura de SICEE (INE es federal, IEPAC es el archivo del
   propio estado).
2. Alternativa dentro de la ventana SICEE (2015+): revisar si Coahuila,
   México (estado) o Hidalgo — históricamente de calendario no
   sincronizado — tuvieron una elección local NO concurrente después de
   2015 y otra concurrente, vía `https://sicee.ine.mx/` (requiere
   navegador, la SPA no expone datos a un cliente headless).
3. Si ninguna de las dos rutas anteriores da cómputo por
   municipio/distrito en ≤1 minuto, el diseño puede necesitar
   replantearse a nivel ESTATAL (como el propio TEPJF ya lo reporta)
   en vez de municipio/distrito — decisión de mesa, no de este acto.

## Segunda colisión de ADR (post-push)

Tras empujar la rama y abrir `PR #451`, `origin/main` avanzó una cuarta
vez: `PR #450`/`ACTO MAESTRA34-N2 · MARCO-M-v1_2` fusionó y tomó
`ADR-275` (el mismo número que este acto había derivado). Regla de la
casa aplicada por segunda vez en el mismo acto: este acto **renumera a
`ADR-276`**. `git merge origin/main` esta vez **sí dio `CONFLICT`**
(textual, no mecánico: ambos actos añadieron su párrafo `ADR-27x` al
final de la misma sección de `canon/gobernanza-v1_15.md` y de la misma
línea `L0` de `canon/estado-programa-v1_10.md`). Resuelto a mano
conservando **intacto** el párrafo de `MAESTRA34-N2` (`ADR-275`) y
renumerando el de este acto de `275` a `276` en las cuatro citas
(cabecera de `gobernanza`, párrafo de `gobernanza` §4, línea `L0`,
tabla de referencias cruzadas de `estado-programa`) — verificado por
**conteo** de anotaciones antes/después (`*(\`ADR-` openers: `gobernanza`
sin duplicados; `estado-programa` 54→55, exactamente +1), no a ojo
([[feedback_linea_l0_se_duplica_al_resolver_a_mano]]).

## Suite (`/acto` §4.6)

`python3 tests/check.py --baseline`: `T15 T-ADR-COUNT` requirió corregir
una segunda cita del conteo de ADR en `canon/estado-programa-v1_10.md:27`
(tabla de referencias cruzadas, "274 ADR" → "275 ADR" — la línea `L0` por
sí sola no bastaba). Tras corregirla: `[ok] T15`, y `LÍNEA BASE: ROJO —
29240 entradas nuevas`, **todas `T27`**, idéntico al conteo que `ADR-273`
ya documentó como defecto preexistente (`data/raw/raw` symlink
autorreferente, glob recursivo sin guardia de bucle). **Anti-PR#77 /
causación T27**: `git diff --name-only origin/main...HEAD -- data/` →
**0 líneas** — este acto no creó ni tocó un solo archivo bajo `data/`, y
el symlink autorreferente ya existía (`Aug 12`, antes de este acto). No
se repara aquí (fuera de perímetro, ya declarado por `ADR-273`).

## Contador declarado

Prior→MEDIDO +1 (P1, dentro de la propuesta, no del motor). θ
informativas +7 (P2: 2011/2015/2019/2023 nuevas; 2013/2017/2021 ya
públicas se citan, no se re-cuentan). Reglas medidas +1 si P3 se
cuenta (con_registro, condicional a canal) — sí, con reserva de
subconjunto declarada arriba. P4: 0 (no corrió).

## Lo que no hizo

No cargó nada a `milpa/tramite.yaml` (motor, ADR-68(a) vigente). No
re-emitió M de v1_1. No tocó corridas-R de TRA-M-03/05/07 (solo las
citó). No promedió olas. No escribió en `data/curacion-registro/`.
