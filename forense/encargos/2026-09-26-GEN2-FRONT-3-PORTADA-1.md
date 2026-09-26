# ENCARGO · ACTO GEN2-FRONT-3-PORTADA-1 · La portada del repo se vuelve ejecutiva y vendible: raíz con nueve archivos y las carpetas, todo lo histórico en `archivo/` y lo normativo en `gobierno/` con un índice que resuelve cada cita sellada, README de una pantalla escrito por dirección, metadatos y vista previa del repo, y la landing alineada palabra por palabra

> ENTORNO: **NUBE** — raíz, `docs/`, `archivo/`, `gobierno/`, referencias operativas. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción `34949751` (re-deriva al abrir) · una sesión, rama propia (la que fije la plataforma; se declara) · MODELO: Opus · MODO: **AUTÓNOMO-AMPLIO** (cláusula v1.0 `3fbc487684b77b7f`) · ids con raíz de acto (D-24) · D-21 aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` con esas palabras.
CONTADOR: cero mediciones; no adopta; ninguna cifra del README sin comando (patrón de FRONT-1, invisible en el render); contador propio: archivos de primer nivel (55 → ≤ 12) y enlaces rotos (0).

## 1 · OBJETIVO
- **P1 · Raíz limpia con índice de redirección.** `git mv` (nunca `rm`) de: `instrucciones-proyecto-v2.md`, `v2_4` … `v2_15` y sus `-HISTORIA`/`-DELTA`/`.sha256` → `archivo/instrucciones/`; `propuesta-*`, `PROPUESTA-*`, `revision-*` → `archivo/propuestas/`; `instrucciones-proyecto-v2_16.md`, `-HISTORIA.md` y sus `.sha256` → `gobierno/` (junto con `PLANTILLA-ENCARGO`, `CLAUSULA-AUTONOMIA`, `MEMORIA-OPERATIVA` cuando CABLEADO la cree: se enlazan, no se duplican). `archivo/INDICE.md` gana la tabla **nombre citado → ruta actual → commit del movimiento**, y un resolvedor de una línea (`tools/resuelve_cita.py <nombre>`) que cualquier lector o test usa. Las **referencias operativas** (`tools/`, `tests/`, `.claude/`, `CLAUDE.md` con su `@import`, `AGENTS.md`, `docs/`) se actualizan en el mismo PR; las **citas en texto sellado** (`canon/`, `forense/notas`, ADR) **no se editan**: las resuelve el índice. Test `tests/test_portada.py`: raíz ≤ 12 archivos de primer nivel; toda cita a un nombre movido en `canon/`+`forense/` resuelve por el índice; 0 enlaces relativos rotos en `docs/` y `README`. Quedan en raíz: `README.md`, `LICENSE`, `CITATION.cff`, `CONTRIBUTING.md`, `AUTHORSHIP.md`, `AVISO-DE-ALCANCE.md`, `USO-ACEPTABLE.md`, `AGENTS.md`, `CLAUDE.md`, `requirements*.txt` (hasta que CABLEADO deje `pyproject.toml`; si ya está, solo `pyproject.toml`).
- **P2 · README de una pantalla** (texto de dirección en §11, verbatim; cifras por comando en comentarios invisibles; sin tabla técnica: eso vive en `docs/estado.md`, nueva, que hereda la sección «Estado derivado» y «La prueba» del README actual con sus comandos). Badges derivados sin servicio externo: `docs/data/badges/*.json` generados por el mismo derivador del README (`tools/readme_derivado.py`) y consumidos por shields.io `endpoint` desde la URL cruda de `main`; si shields no es aceptable, badges estáticos generados como SVG en `docs/data/badges/` (sin red).
- **P3 · Metadatos y vista previa del repo.** Descripción (una línea de §11), `topics` (mexico, inegi, benchmark, survey-data, reproducible-research, behavioral-science, spanish), homepage = URL de Pages, imagen de vista previa social (`docs/assets/social-preview.png`, 1280×640, generada por comando desde la portada del one-pager: título, tagline, tres cifras derivadas, sin logos ajenos). Si la credencial de la sesión permite `gh repo edit`, se aplica y se pega la respuesta; si no, receta de un minuto para mesa (Settings → General → Social preview / About) en la nota y fila FP.
- **P4 · Landing alineada.** `docs/index.md` dice lo mismo que el README (mismo tagline, mismas tres cifras, mismos tres botones: Leer el informe · Consultar el catálogo · Verificar en 5 minutos); navegación en `_config.yml`: Inicio · Informe · Catálogo · Consultar · Verificar · Reto · Contacto (los demás quedan enlazados desde «Más»); `docs/guia-lectura-publica.md` y `docs/estado.md` como segundo nivel. Si PRODUCTO-CONSULTA-1 ya dejó `docs/consultar.md`, el botón apunta ahí; si no, a `docs/catalogo.md` y se cambia por puntero después.
- **P5 · `CONTRIBUTING.md` y `CONTRIBUTING` para externos**: cómo se cita, cómo se verifica, cómo se reta (enlace a `docs/reto.md`), qué no se acepta (cifras sin RESULT, PR a `canon/` sin acto), y que el desarrollo interno va por `/acto`; tres párrafos, sin jerga interna.
«Hecho» sobre el commit final con origin/main fusionado: `ls -1 | grep -v '/' | wc -l` ≤ 12 · `archivo/INDICE.md` con una fila por archivo movido y `tools/resuelve_cita.py` con test · `tests/test_portada.py` VERDE (raíz, citas, enlaces) · README nuevo con test de cifras derivadas VERDE (heredado de FRONT-1) · `docs/estado.md`, `docs/index.md`, `_config.yml`, `CONTRIBUTING.md` actualizados · badges y vista previa generados por comando · metadatos aplicados o receta + FP · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA
- **Dadas:** D2 (Benchmark del Mexicano; benchmark auditable; dónde ganan los otros), F-FRONT-1/2/3 (nombre, términos, Pages), A.9 (la versión vigente de instrucciones está sellada cuando está en el proyecto y en el repo: **la ruta en el repo no es parte del sello; `gobierno/` la conserva íntegra con su sha**; el ADR lo declara).
- **Dada el 26/sep/2026 («Firmado»), verbatim; viaja aquí y la asienta este acto:** «Los archivos históricos y normativos salen de la raíz con git mv; una cita por nombre en texto sellado no se edita: la resuelve archivo/INDICE.md y tools/resuelve_cita.py. La raíz queda con ≤ 12 archivos de primer nivel.»

## 3 · LO QUE DIRECCIÓN SABE
`[EJECUTADO]` (`34949751`) raíz: 55 entradas, 36 `.md` (20 de instrucciones, 11 propuestas/revisiones); README 67 líneas con cifras derivadas por comentario (FRONT-1, #1083) y tabla técnica de seis evaluaciones; `docs/` con 17 archivos (índice, informe, catálogo, verificar, reto, one-pager, deck, tablero, protocolo, sello externo, sesiones, glosario, guía de lectura, contacto). `[LEÍDO]` nota de FRONT-1 §P3: 48 candidatos cotejados por `rg -l -F`; referencias en `canon/gobernanza-v1_15.md` (v2_10: 35; v2_11: 22), `forense/agente-revisor-v1_0.md` (v2_12: 62), y consumidores operativos; `archivo/INDICE.md` explica el aplazamiento. `[EJECUTADO]` referencias desde `tools tests .claude canon docs forense/encargos`: v2_12 (22), v2_10 (11), motor-matriz (8), celda-v0_5 (8), v2_6 (8), v2_16 (6, incluido el `@import` de `CLAUDE.md`) — **solo las operativas se editan**. `[SUPUESTO]` que ningún test lee una instrucción vieja por ruta absoluta para decidir algo (si uno sí, se apunta a la ruta nueva; es operativo, no sello).

## 4 · YA HECHO / YA DECIDIDO
`ls archivo/` → solo `INDICE.md`. `ls gobierno/ 2>/dev/null` → no existe. `ls docs | grep -c estado.md` → 0. FRONT-1 (#1083) y FRONT-2 (#…): README GEN2, one-pager, deck, reto, tabla de piso — se conservan; este acto reordena y reescribe la portada, no el contenido de `docs/`.

## 5 · PIEZAS
Las agrupa la sesión; sugerencia: P1 (con su test) → P2 → P4 → P5 → P3.

## 6 · LATITUD — CLÁUSULA DE AUTONOMÍA v1.0 + AMPLITUD
1–7 verbatim. Nombres de carpeta, forma del resolvedor, diseño de la vista previa: tuyos. Si un movimiento rompe una herramienta operativa que no aparece en el inventario, se corrige en el mismo PR y se declara. Pregunta a mesa prevista: **ninguna**.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) no aplica · b) `git rm` de algo con sha en el canon; editar una cita en texto sellado; tocar sellos o vistas · c) teclear una cifra en README, badges o vista previa · d) no aplica · e) CAJA.

## 8 · COMPUERTAS
«`git mv` y nunca `rm`; citas selladas intactas, resueltas por índice con test» protege: **borrar / reescribir**. «Toda cifra visible del frente por comando y test» protege: **congelar** (§2 regla de oro). «v2.16 conserva su sha en `gobierno/`» protege: **congelar** (A.9).

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: raíz (movimientos), `archivo/`, `gobierno/`, `tools/resuelve_cita.py`, `tools/readme_derivado.py` (badges), `README.md`, `CONTRIBUTING.md`, `docs/index.md`, `docs/estado.md`, `docs/_config.yml`, `docs/assets/`, `docs/data/badges/`, referencias operativas en `tools/ tests/ .claude/ CLAUDE.md AGENTS.md`, `tests/test_portada.py`, FP/NC, nota, L0, cascada. Ajeno: `canon/`, `forense/notas`, ADR (solo lectura), CALC, vistas, CI. En vuelo: CABLEADO-SESIONES-1 (edita `CLAUDE.md`, `AGENTS.md`, crea `canon/MEMORIA-OPERATIVA.md`: **coordinar — quien fusiona segundo rebasa; si CABLEADO ya movió reglas a `canon/REGLAS-DE-LECTURA.md`, este acto las enlaza desde `gobierno/`**), PRODUCTO-CONSULTA-1 (`docs/consultar.md`, `docs/reto.md`: se enlaza, no se edita), CIERRE-SEMANAL-1 (`canon/`; no choca).

## 10 · LO QUE NO HACE · SUCESORES
No cambia contenido de informe, catálogo ni reto; no publica en redes (mesa). Sucesores: FRONT-4 cuando el reto reciba entregas; FIRMAS-20 asienta metadatos y vista previa si los aplica mesa.

## 11 · README — texto de dirección (verbatim; ⟨⟩ = cifra por comando en comentario invisible; enlaces relativos)
```
# Benchmark del Mexicano

**Lo que la gente dijo en la última encuesta oficial, por segmento, con intervalo calibrado — y la prueba pública de que ningún modelo lo ha mejorado.**

⟨N⟩ corridas selladas · ⟨N⟩ predicciones verificadas antes de que INEGI publicara la ola · ⟨N⟩ de 31 dominios con medición · todo reproducible desde este repo.

**[Leer el informe](docs/informe.md) · [Consultar el catálogo](docs/catalogo.md) · [Verificar en cinco minutos](docs/verificar.md)**

## La prueba en una frase
En ⟨seis⟩ evaluaciones prospectivas, sobre ⟨cuatro⟩ instrumentos oficiales y ⟨N⟩ celdas de población, la predicción más simple —repetir lo que la gente dijo en la ola anterior— nunca fue superada, con intervalo que despejara el umbral fijado de antemano, por ninguno de los modelos construidos aquí ni por un retador externo. No es un fracaso del modelado: es el hallazgo. El comportamiento reportado del mexicano es estable entre olas en los dominios medidos, y cualquier producto que prometa detectar cambios grandes entre encuestas debería probarse contra esta línea base antes de venderse. Detalle y dictámenes: [docs/estado.md](docs/estado.md).

## Para quién
- **Banca, fintech y seguros:** el piso por segmento con su margen de error y, al lado, la medida de exclusión por oferta — no hay otra en México.
- **Gobierno y evaluación:** qué cambió de verdad entre olas y qué fue el cuestionario, por conducta y por entidad.
- **Agencias e insights:** la línea base contra la que medir cualquier gemelo digital del consumidor mexicano; hay un [reto público](docs/reto.md).
- **Academia:** sellos verificables, microdato oficial, pre-registro y validación independiente.

## Qué no hacemos
No respondemos preguntas que las encuestas oficiales no hicieron. No prometemos detectar cambios de conducta entre olas. No medimos compras observadas ni marcas. No vendemos gemelos digitales. Dónde ganan los otros y por qué, en el [informe](docs/informe.md).

## Cómo funciona, en tres líneas
Cada cifra nace con su especificación sellada antes de abrir el dato, su código fijado, sus insumos con hash y su resultado con unidad e intervalo. Cada ola nueva entra reservada y solo la abre código congelado de una prueba pre-registrada. Los sellos se atestiguan con un tercero de tiempo. Todo esto se verifica desde un clon limpio: [docs/verificar.md](docs/verificar.md).

## Cita, licencia y contacto
Uso no comercial libre con atribución; uso comercial por acuerdo. Cita: `CITATION.cff` (DOI: ⟨Zenodo⟩). Límites y alcance: [AVISO-DE-ALCANCE.md](AVISO-DE-ALCANCE.md) · [USO-ACEPTABLE.md](USO-ACEPTABLE.md). Contacto: el correo de `CITATION.cff`. Cómo contribuir o retar: [CONTRIBUTING.md](CONTRIBUTING.md).

<sub>Este README deriva sus cifras por comando; si una no coincide con `python3 tools/corrida0.py status`, el README está mal, no el contador. Gobierno del programa: [gobierno/](gobierno/) · histórico: [archivo/](archivo/).</sub>
```
Descripción del repo (una línea): «Benchmark auditable del comportamiento del mexicano con encuestas oficiales: pisos por segmento con intervalo calibrado, predicciones selladas antes de cada ola, todo reproducible.»

## NO-CORRIDO / RESERVAS

- **P4 · «mismas tres cifras» en `docs/index.md`** — la landing lleva las tres cifras de la prueba (seis evaluaciones · cuatro instrumentos · 137 celdas), no la línea de cifras del README. · `DIFERIDO-A:SIN-ASIGNAR` — dos de esas tres cifras salen de `corrida0 status` y el job guardias (`verify.yml`, ajeno a este acto) solo hace commit de `README.md`: en la landing envejecerían en silencio. · Impacto: la landing no muestra corridas ni predicciones; ningún contador se mueve. · Sucesor: SIN-ASIGNAR (`NC-260926-GEN2-FRONT-3-PORTADA-1-8914-01`).
- **P3 · metadatos del repo y vista previa social aplicados** — `DIFERIDO-A:GEN2-TRAMITE-FIRMAS-20` — sin `gh` ni herramienta MCP de edición del repo; la imagen y el texto se generaron por comando y la receta de un minuto está en la nota §P3. · Impacto: la tarjeta del repo sigue igual; ningún contador se mueve. · Sucesor: `FP-260926-GEN2-FRONT-3-PORTADA-1-8914-03` (`NC-…-8914-02`).
- Reservas, sin fila NC: (1) la receta de «hecho» `ls -1 | grep -v '/' | wc -l` cuenta carpetas (21 con la raíz limpia); el conteo de archivos (`ls -p | grep -v /`) da 11 y es lo que mide `tests/test_portada.py` (hallazgo). (2) Dos cifras del texto verbatim §11 se reformularon por firma de mesa en sesión (FP `…-8914-02`, FIRMADA). (3) `check.py --baseline` @ `4761ce3a`: `LÍNEA BASE: VERDE`, 123 WARN nuevos frente a 120 en `34949751`; los tres de más son los mismos T03 de `propuesta-motor-adaptativo-celda-v0_1.md`, re-rotulados por su ruta nueva en `archivo/propuestas/`. (4) `canon/MEMORIA-OPERATIVA.md` y `docs/consultar.md` no existen en `origin/main`: `gobierno/` y el botón «Consultar» se repuntan cuando CABLEADO-SESIONES-1 y PRODUCTO-CONSULTA-1 los dejen.

## CONSUMIDO

Ejecutado por PR #1164 (rama `claude/new-session-7p7kao`; 0-bis `89148f00`, movimiento `1734006a`, índice `4761ce3a`, cascada `b071a7a2`, merge de `origin/main` `162d2d17`). ADR `ADR-260926-GEN2-FRONT-3-PORTADA-1-8914-01`; nota `forense/notas/2026-09-26-GEN2-FRONT-3-PORTADA-1-cierre.md`. Sobre `efbce3fb` (con `origin/main` @ `2b97d517` fusionado): `python3 tests/check.py --baseline` → `LÍNEA BASE: VERDE`; `tests/test_portada.py` OK (raíz 11 archivos, índice 35 filas, 0 enlaces rotos); `tests/test_readme_derivado.py` 6/6 OK (README 287 corridas, re-derivado tras el merge); `tests/test_arnes_sesion.py` 13/0. PRODUCTO-CONSULTA-1 (#1163) dejó `docs/consultar.md` antes del cierre: el botón «Consultar el catálogo» (README y landing) y la navegación apuntan ahí (rama prevista en P4).

Tras el cierre, `origin/main` recibió CABLEADO-SESIONES-1 (#1165) y ASTRA6 (#1166); se fusionó de nuevo sin conflicto. `CLAUDE.md` conserva `@gobierno/instrucciones-proyecto-v2_16.md` y los `@canon/MEMORIA-OPERATIVA.md` / `@canon/REGLAS-DE-LECTURA.md` de CABLEADO, que `gobierno/README.md` ahora enlaza (§9). Con eso, la reserva (4) de arriba queda resuelta en lo que toca a CABLEADO.
