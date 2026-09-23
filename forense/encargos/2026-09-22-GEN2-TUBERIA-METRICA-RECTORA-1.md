# ENCARGO · ACTO GEN2-TUBERIA-METRICA-RECTORA-1 · v1.1 · `celdas_validadas` DEJA DE VIVIR EN UN SOLO ARCHIVO: UNA DERIVACIÓN, UNA SPEC, IMPRESA EN TODAS PARTES, MOVIDA POR CADA ACTO POR COMANDO Y CON GUARDIA DE MONOTONÍA

**v1.1 sustituye a la redacción del 22/sep**, que no se lanzó. Cuatro correcciones de TUBERÍA, cada una verificada contra `main` `3f48be30`: (1) el contrato de `--json` usa las sub-cifras que **existen** —`adoptadas` no existe y su definición sigue sin sellar—; (2) el aviso de P3 deja de ser un WARN, porque la firma del 21/sep retira ese canal; (3) el conteo de ramas vivas se corrige; (4) se declara la concurrencia con los sucesores de `#980`.

**CABECERA** · SHA de redacción `3f48be30` (= `main`; re-deriva al abrir; si `main` se movió no es PARO) · **ENTORNO: NUBE**, `cloud_default`, con credenciales de Git y publicación de PR · **cero microdato**: cuenta sellos · una sola sesión, rama propia (D-17) · **MODELO SUGERIDO: Opus** · **MODO: ABIERTO** · **COMPUERTA: una** (§8) · **CONTADOR: cero mediciones.** La métrica **no cambia de valor** por este acto: **92 @ `3f48be30`** antes y después —o el que derive, reportado— · vehículo: `/acto`.

**EL PR NO SE FUSIONA EN ESTE ACTO**: queda propuesto; mesa central fusiona.

**IDS.** Todo con raíz de acto, `ADR` incluido: `ADR-<AAMMDD>-GEN2-TUBERIA-METRICA-RECTORA-1-<hhhh>-<NN>`. No se renumera nada.

---

## 1 · OBJETIVO

Que `celdas_validadas` sea la métrica rectora **de hecho**: una sola derivación importable, con su spec, impresa por `corrida0 status`, `digesto --mesa`, el tablero y el inventario, movida por cada acto por comando, con sus sub-cifras visibles y una guardia de monotonía.

**«Hecho»**, todo por comando sobre el commit final con `main` fusionado:

1. `python3 tools/celdas_validadas.py --json` devuelve el **mismo diccionario** que hoy devuelve `tablero_programa._celdas_validadas()` —`total_celdas_validadas`, `desglose_por_clase`, `prospectividad_del_marcador` con sus cinco claves (`PROSPECTIVA`, `RETROSPECTIVA`, `IDENTICO-EMISOR-ES-ARBITRO`, `SIN-EMISION`, `EMITIDA-SIN-R`), `NO_CUENTAN`, y los demás campos que ya trae— **más** un bloque `universo` con el SHA y la lista de archivos leídos. `--linea` imprime la línea de una sola fila.
2. `python3 tools/corrida0.py status | grep -c "^celdas_validadas="` → **1**, con las sub-cifras en líneas propias.
3. `python3 tools/digesto_tramite.py --mesa --stdout` la abre en su **primera línea**.
4. `grep -rn "def _celdas_validadas" tools/` → **0** fuera del módulo nuevo: una sola función.
5. La cabecera del `ADR` de **este** acto lleva `celdas_validadas: 92 → 92 (Δ0) @ <sha>`, escrita por `cierre_acto.py` y derivada por comando.
6. `tests/test_celdas_validadas_spec.py` y `tests/test_celdas_validadas_monotonia.py` en verde y **cableados** en `verify.yml` como bloqueantes; `tests/test_celdas_validadas.py` (el de `GEN2-SENAL-1`) sigue en verde.
7. La compuerta de §8 pasa: la derivación da **el mismo resultado** antes y después de moverla, en el mismo SHA.

## 2 · FIRMAS DE MESA

Ya selladas, se citan: plan de aceleración P2 («métrica rectora `celdas_validadas` … derivada, con sus dos sub-cifras»); `GEN2-SENAL-1` P1 (el test de la métrica); `GEN2-MARCADOR-E-INFORME-1` (#969: derivación desde sellos, 73 → 92); **la firma del 21/sep que veda sumar PROSPECTIVA y RETROSPECTIVA en una sola cifra** (la cita la propia nota de `prospectividad_del_marcador`); v2.16 E.4 («`celdas_validadas` cuenta toda celda-D con veredicto sellado: validada es predicha antes y comparada después, no acertada»); D-16 (ninguna cabecera aserta totales sin su SHA); D-14 (no se construye contador nuevo: se cablea el que existe).

**Y la firma del 21/sep sobre el canal de WARN**, punto (5): *«El canal de WARN se retira. Cada familia pasa a FAIL acotado a los archivos que el PR toca, o a un contador del tablero derivado por comando; lo que no sea ninguna de las dos se borra.»* Este acto **no añade ningún WARN**.

**No entra en este acto** —queda como propuesta para mesa—: *«Las dos sub-cifras son PROSPECTIVA (la que rige) y ADOPTADAS (estimador adoptado por firma).»* `adoptadas` no existe como derivación y nadie ha dicho de qué fuente sale. Cuando mesa la selle con su fuente, es una pieza propia.

## 3 · LO QUE SE SABE — con rótulo

- `EJECUTADO` · **Dónde vive hoy:** `grep -rn celdas_validadas tools/ tests/ .github/ .claude/` → sólo `tools/tablero_programa.py` (la función en la línea 297, `put(…)` en la 825, la línea impresa en la 851) y `tests/test_celdas_validadas.py`. `corrida0.py`, `digesto_tramite.py` y `cierre_acto.py`: **0** menciones. `tools/celdas_validadas.py`: no existe.
- `EJECUTADO` · **Lo que la función ya devuelve**, sobre `3f48be30`, en **0.1 s**: `total_celdas_validadas = 92` (`desglose_por_clase`: cruce contra R 35 + persistencia t−1 contra R 57; más 12 del duelo tres nacional, fuera del total); `prospectividad_del_marcador`: **PROSPECTIVA 20 · RETROSPECTIVA 59 · IDENTICO 89 · SIN-EMISION 30 · EMITIDA-SIN-R 16**, que coinciden con #969; `NO_CUENTAN`: 89 idénticas y 2 de formalidad; universo: *214 filas de `data/corrida0/marcador-segmento.tsv` + 3 CALC sellados*. **Las sub-cifras ya existen**: este acto las imprime, no las inventa.
- `EJECUTADO` · **`adoptadas` no está** entre las claves que la función devuelve.
- `EJECUTADO` · `canon/estado-programa-v1_15.md` cita la métrica **a mano** en seis sitios, con el `92` escrito (líneas ~713-734).
- `LEÍDO` · `tests/test_celdas_validadas.py:36` lee `["celdas_validadas"]["valor"]` del JSON del tablero, y en la línea 60 compara `total_celdas_validadas`: el contrato **no puede cambiar de forma**.
- `EJECUTADO` · Hay filas `VENCIDO-EN-ALCANCE` en los registros de mesa (cuatro menciones en `data/corrida0/decisiones.tsv` y `forense/*.tsv`): la guardia de monotonía tiene dónde buscarlas.
- `EJECUTADO` · **Ramas vivas al redactar: cinco** —`acto/gen2-duelo-envipe2026-marginales-2`, `acto/gen2-tramite-cola-vieja-1`, `claude/dazzling-planck-c7lxuj`, `claude/new-session-ceszds`, `derivados/2026-09-22`—. **Ninguna toca** `tablero_programa.py`, `corrida0.py`, `digesto_tramite.py`, `cierre_acto.py`, `verify.yml` ni `estado-programa`. Re-deriva y declara el conteo al abrir (A.13).
- `LEÍDO` · **Sucesores de `#980` que tocarán lo mismo**: `#980` ejecutó sólo P-A (T16 fuera, subconjunto rápido) y dejó **P-B, P-C y P-D** como NO-CORRIDO. El sucesor de **P-C** —retiro del canal de WARN— añadirá contadores en `tools/tablero_programa.py`; el de **P-D** —derivados fuera de los PR— tocará `verify.yml` y tratará `forense/tablero/TABLERO-PROGRAMA.md` como archivo derivado. Hoy **P-D no existe**: `verify.yml` no tiene job con `contents: write`, así que los derivados siguen viajando en los PR.
- `EJECUTADO` · El canal de WARN emite hoy **~49 800** avisos en la suite completa (T-REPRO 49 166), el doble que ayer. Es la razón de que P3 no añada uno más.
- `SUPUESTO` · Sacar la función a un módulo no cambia su valor. Lo verifica la compuerta de §8; si difiere, **PARO** con el `diff`: el hallazgo sería que había dos derivaciones.
- `SUPUESTO` · La monotonía vale: un veredicto sellado no se borra (E.3). La única bajada legítima es una fila `VENCIDO-EN-ALCANCE` de mesa (A.10); el test la busca **por objeto** antes de fallar.

## 4 · YA HECHO / YA DECIDIDO — por OBJETO (A.8)

`ls tools/ | grep -i celdas_validadas` → 0. `grep -c celdas_validadas tools/corrida0.py tools/digesto_tramite.py tools/cierre_acto.py` → 0 / 0 / 0. La derivación **EXISTE-SATISFACE** en `tablero_programa.py` y se **mueve**, no se reescribe. Su impresión en `status`, `digesto` y el `ADR`: **NO-ENCONTRADO**. Una spec de la métrica: **NO-ENCONTRADO**.

## 5 · PIEZAS — resultado esperado, no receta

**P0 · 0-bis.** Este encargo verbatim **desde el `.md` recibido**, con su sello de cuerpo. Chequeo de duplicado **por contenido** (¿alguna rama viva archiva ya este encargo?). Antes de tocar nada, guarda `python3 -c "import sys; sys.path.insert(0,'tools'); import json, tablero_programa as T; print(json.dumps(T._celdas_validadas(), sort_keys=True))"` en la nota: es la línea base de la compuerta.

**P1 · Módulo y spec.**
- `tools/celdas_validadas.py`: la función de `tablero_programa.py` **movida, no reescrita**, con su CLI (`--json`, `--linea`) y el bloque `universo` (SHA y archivos leídos). `tablero_programa.py` la **importa** y borra su copia local.
- `forense/prereg-caja/METRICA-CELDAS-VALIDADAS-spec-v1_0.md` más su `spec.yaml` (D-15): definición, fuentes (`data/curacion-registro/celdas-d/*.yaml`, `data/corrida0/marcador-segmento.tsv`, los CALC de duelos), la regla del rótulo PROSPECTIVA/RETROSPECTIVA por orden de sellos (v2.16 §4), qué **no cuenta** (IDENTICO, formalidad sin error medido) y por qué, y que **PROSPECTIVA y RETROSPECTIVA no se suman** (firma del 21/sep).
- `tests/test_celdas_validadas_spec.py`: la spec y el módulo coinciden en un caso **sintético** con una celda de cada clase.

**P2 · Impresión.**
- `corrida0 status`: `celdas_validadas=92`, y en líneas propias `celdas_validadas_prospectiva=`, `celdas_validadas_retrospectiva=` y `celdas_emitidas_sin_r=` —esta última **como demanda**: son emisiones que esperan su R—.
- `digesto --mesa`: primera línea `celdas_validadas N (prospectiva P · retrospectiva R) @ SHA`.
- El tablero la imprime importando el módulo. **El generador del inventario de 004 la lee del mismo JSON**: se deja una nota a 004; ese generador no se edita aquí.

**P3 · Cada acto la mueve, y lo declara.**
- `cierre_acto.py`, en la cascada: `Δceldas_validadas` = derivación en el commit final − derivación en el commit de 0-bis, escrita en la cabecera del `ADR`: `celdas_validadas: 92 → 92 (Δ0) @ <sha>`. Lleva su SHA, así que no es una cabecera que aserte un total (D-16).
- **Si un acto con `cuenta_gen2 = SI` cierra con Δ = 0 y su `CONTADOR` no lo declara, `cierre_acto.py` se niega a cerrar**, con un mensaje que diga qué escribir. Es un defecto que su autor corrige, y la comprobación vive **en el cierre de ese mismo acto**: queda acotada a él por construcción, sin WARN y sin tocar la suite (firma del 21/sep, punto 5).

**P4 · Guardias, cableadas.**
- `tests/test_celdas_validadas_monotonia.py`: para los últimos **N** merges del primer padre de `main` (N lo decide el ejecutor y lo declara), la métrica **no baja** sin una fila `VENCIDO-EN-ALCANCE` que lo explique, buscada por objeto. La derivación cuesta 0.1 s por commit: N puede ser generoso.
- Los dos tests nuevos, **cableados en `verify.yml` como bloqueantes**: un test que nadie corre es decoración (`NC-0331`).

**P5 · Cabeceras y cierre.** En la cabecera de era de `canon/estado-programa-v1_15.md`, **una línea**: la cifra con `@ SHA` y *«derivada por `tools/celdas_validadas.py`»*. Las seis citas a mano de §3 **no se reescriben**: quedan como historia de su SHA. Fragmento `canon/L0/<ADR-raíz>.md`. Nota de cierre con la tabla **dónde se imprime · comando**. `## NO-CORRIDO / RESERVAS` al final; `## CONSUMIDO` con el PR real.

## 6 · LATITUD

**Decides tú:** los nombres de los campos nuevos (sin cambiar los que ya existen), N de la guardia, el formato de la línea. **Preguntas a mesa, y sigues:** si al mover la función el valor difiere, cuál es la fuente —recomendado: la que cuenta desde sellos, #969—. Un obstáculo reversible y barato se resuelve y se declara (D-19).

**Concurrencia.** Si al abrir o al cerrar ya está en vuelo o fusionado el sucesor de P-C o el de P-D de `#980`, fusiona `main` hacia la rama y re-aplica: este acto sólo **importa** el módulo en `tablero_programa.py` y añade **dos pasos** a `verify.yml`. Si el sucesor de P-D ya sacó el tablero de los PR, **no commitees** `TABLERO-PROGRAMA.md`: lo regenera el job; si todavía no existe, se regenera y viaja como hoy.

## 7 · PAROS — lista cerrada

a) La compuerta de §8 falla (el valor cambia al moverse) · b) tocar sellos, celdas-D o CALC —se leen— · c) adoptar · d) cambiar la definición sellada en #969, o sumar PROSPECTIVA y RETROSPECTIVA · e) añadir un WARN a la suite · f) abrir microdato · g) objetivo inalcanzable. **Fuera de esta lista no se para.**

## 8 · COMPUERTA

**Igualdad antes/después en el mismo SHA** (P0 → P1): el JSON de la derivación, con claves ordenadas, idéntico antes y después de moverla, salvo el bloque `universo`, que es nuevo. **Protege: borrar** —una métrica que cambia al moverse es una métrica borrada—.

## 9 · PERÍMETRO

Propio: `tools/celdas_validadas.py` (nuevo) · `tools/tablero_programa.py` (importa; borra la función local) · `tools/corrida0.py` (sólo las líneas de `status`) · `tools/digesto_tramite.py` (sólo la primera línea de `--mesa`) · `tools/cierre_acto.py` (el Δ en la cabecera y la negativa a cerrar de P3) · `forense/prereg-caja/METRICA-CELDAS-VALIDADAS-spec-v1_0.md` y su `spec.yaml` · `tests/test_celdas_validadas*.py` · `.github/workflows/verify.yml` (**dos pasos**) · la cabecera de era de `canon/estado-programa-v1_15.md` (**una línea**) · `forense/encargos/`, `forense/notas/`, `forense/hallazgos.md`, `forense/no-corrido.tsv` · `canon/L0/<ADR-raíz>.md` · y la cascada. Más D-21.

`tools/corrida0.py` y `tools/digesto_tramite.py` son de dirección: este encargo, redactado por dirección, **autoriza** las líneas indicadas y nada más.

**Ajeno:** celdas-D, marcador, CALC, el generador de 004, `tests/check.py`, `tools/verifica_sidecars.py`. **Si te encuentras escribiendo fuera de esta lista, PARA.**

## 10 · NO HACE · SUCESORES · CIERRE

No cambia el valor, no redefine la métrica, no adopta, no suma sub-cifras que la firma separa, no añade WARN. **Sucesores:** 004 lee el JSON; el informe v1.3 la cita por comando; y, cuando mesa selle la propuesta de `adoptadas` **con su fuente**, una pieza propia la deriva. Auditoría de rigor: no aplica (aparato). Cierre por `/acto`.

## NO-CORRIDO / RESERVAS

- **004 (generador del inventario) no se edita** para leer el nuevo JSON de `tools/celdas_validadas.py` — razón: `FUERA-DE-PERÍMETRO` (el perímetro §9 sólo deja "una nota a 004", no editarlo). Impacto: el inventario de 004 sigue leyendo la ruta vieja hasta que un acto propio lo actualice. Sucesor: `DIFERIDO-A:acto propio de 004, nota dejada en esta cascada (forense/notas/2026-09-22-GEN2-TUBERIA-METRICA-RECTORA-1-cierre.md)`.
- **La propuesta `adoptadas` (sub-cifra de estimador adoptado por firma) no se deriva** — razón: `DECISION-DE-MESA-PENDIENTE` (§2/§6 del encargo: no existe fuente sellada ni definición). Impacto: `celdas_validadas.py --json` no trae `adoptadas`. Sucesor: `SIN-ASIGNAR` hasta que mesa selle la propuesta con su fuente.
- **`python3 tools/ci_guardias.py --censo` no corre en verde** — razón: `NO-VERIFICABLE-AQUÍ` (defecto preexistente y ajeno: `tests/test_consulta_gen2` cuelga y `ci_guardias.py:192` tiene un `TypeError: can only concatenate str (not "bytes") to str` al reportar el timeout — ninguno de los dos archivos está en el perímetro §9 de este acto). Impacto: el censo automático de huérfanos no corrió sobre este árbol; los dos tests nuevos se cablearon EXPLÍCITAMENTE en `verify.yml` (más fuerte que quedar huérfanos para que `ci_guardias` los descubra), así que no dependen de ese censo para entrar a CI. Sucesor: `SIN-ASIGNAR` (reparar `ci_guardias.py`/`test_consulta_gen2` es un acto propio, ajeno a la métrica rectora).
- **`forense/tablero/TABLERO-PROGRAMA.md` no se regeneró en este acto** — razón: `FUERA-DE-PERÍMETRO` (lo regenera `/deriva`, no está en la lista de PERÍMETRO §9). Impacto: ninguno sobre la cifra (la compuerta §8 probó que el valor no cambia); el archivo derivado se re-emite en la próxima corrida de `/deriva`. Sucesor: `SUSTITUIDO-POR:/deriva` (corrida diaria ya existente, ningún acto nuevo necesario).

## CONSUMIDO
