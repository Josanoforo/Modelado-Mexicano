# ENCARGO · ACTO GEN2-CATALOGO-CONTRATO-Y-TEST-1 · T-REPRO(c) y el contrato del catálogo se contradicen y nadie los leyó juntos: se leen, se hacen consistentes con E.1/E.2, y se propone a mesa el esquema de procedencia que su contrato dejó abierto

> ENTORNO: **NUBE** — código, tests y contratos; cero microdato. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción `3d138c66` (re-deriva al abrir) · una sola sesión, rama propia `acto/gen2-catalogo-contrato-y-test-1` (o la que la plataforma fije: se declara en el 0-bis, D-19) · MODELO: Opus · MODO: ABIERTO · ids con raíz de acto (D-24) · D-21 aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` al pie.
CONTADOR: cero mediciones; no adopta; no releva ninguna llave (eso es de ADOPCION -3/-4 cuando test y contrato coincidan); `T-REPRO(c)` puede cambiar de semántica solo con la evidencia de P1 y sin bajar de exigencia.

## 1 · OBJETIVO
ADOPCION-1 escribió el valor GEN2 del momento M08 en `milpa/catalogo-momentos-v0_1.tsv` y `T-REPRO(c)` falló («valor materializado…»); ADOPCION-2 no escribió nada porque el contrato del catálogo pide **cita lateral** y `T-REPRO(c)` «exige el valor en el propio archivo». Ninguna de las dos lecturas puede ser completa: un test que rechaza el valor materializado y también la cita lateral no deja forma válida de relevar el catálogo. (P1) Leer `tools/corrida0.py:4470` en adelante y `tests/check.py:7724` en adelante: qué compara exactamente T-REPRO(c) (¿valor del archivo = RESULT? ¿contra GEN1? ¿rechaza discrepancia rotulada?), y `forense/analisis/astra4-relevo/contratos-otros-consumidores.md` § Catálogo (l.39-52): qué operación define. Escribir la contradicción con las dos citas. (P2) Hacerlos consistentes con E.1/E.2 en esta dirección, salvo que P1 demuestre otra cosa con evidencia: el catálogo lleva el **valor GEN2 y la cita** (RESULT, CALC, hash) en columnas propias; T-REPRO(c) verifica `valor == RESULT`; la discrepancia con el valor GEN1 anterior se rotula en columna `discrepancia_gen1` (p. ej. `NO-REPRODUCE-GEN1: unidad DELITO`) y **no bloquea**; el test gana un caso positivo (M08 con valor y cita) y uno negativo (valor sin cita; cita sin valor; valor ≠ RESULT). (P3) Procedencia (40 filas): el contrato dice que «la cita RESULT y el respaldo de clase requieren un campo/esquema acordado por mesa» — proponer el esquema con dos opciones y texto de firma (fila FP), sin implementarlo. (P4) Celdas-D: constatar que las seis referencias de código no tienen sucesora adjudicada (ADOPCION-2) y dejarlo escrito como estado, no como deuda.
«Hecho»: nota con la contradicción citada línea a línea (P1) · `T-REPRO(c)` y el contrato del catálogo modificados en el mismo PR, coherentes, con los tres tests (positivo y dos negativos) VERDE · el caso M08 de ADOPCION-1 reproducido en rama: con valor GEN2 + cita + `discrepancia_gen1` rotulada, `T-REPRO(c)` VERDE (sin commitear el catálogo: lo escribe ADOPCION-4 por el escritor) · FP con el esquema de procedencia (dos opciones, recomendación) · `check.py --baseline` VERDE sin `--force`.

## 2 · FIRMAS DE MESA — dadas («firmado», 24/sep/2026), verbatim
- **Decisión 3 de ADOPCION-2 (catálogo):** «Un acto de tubería lee la semántica exacta de T-REPRO(c) y el contrato del catálogo y los hace consistentes con E.1/E.2: el catálogo lleva el valor GEN2 y su cita; el test verifica valor = RESULT; la discrepancia con GEN1 se rotula en columna propia y no bloquea. Si al leerlos resulta que basta aceptar la cita lateral, el acto lo dice con evidencia.» (cierra `FP-…-e0db-03` y `NC-…-ADOPCION-1-ec71-03` en su parte de catálogo)
- **N** (24/sep, ADOPCION-1 §2, vigente): momento 08 unidad DELITO con `NO-REPRODUCE-GEN1` rotulada; momentos 01–02 por cotejo documental; escritor extendido según contratos. Este acto prepara el terreno; el escritor lo aplica ADOPCION-4.
- **E (procedencia):** sin firma; este acto la **propone** (P3), no la ejecuta.

## 3 · LO QUE DIRECCIÓN SABE
- `[EJECUTADO]` `tools/corrida0.py:4470` («T-REPRO (c) compara la cifra que el consumidor MATERIALIZA contra…»); `tests/check.py:7724` (`fail("T-REPRO", f"(c) {consumidor}: valor materializado …")`) y `:7703-7706` ((g) aptitud/origen). `[LEÍDO]` contrato § Catálogo l.44: «la operación revisable es una cita lateral por Mxx con RESULT, CALC, …»; § Procedencia l.34: esquema por acordar.
- `[LEÍDO]` ADOPCION-1 cierre l.18-33: pin M08 vía `i-CRUDO` pasó las cuatro guardas y rompió T-REPRO(c); revertido; dictamen en `decisiones.tsv:catalogo:M08`. ADOPCION-2 cierre: «la cita lateral que pide el contrato no satisface T-REPRO(c)».
- `[SUPUESTO]` que T-REPRO(c) hoy compara el valor materializado contra el valor **legacy** del catálogo (por eso M08 con unidad DELITO falla) y no contra el RESULT: es la hipótesis de dirección; **P1 la confirma o la refuta con la línea exacta**.
- ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
`git log --oneline -5 -- tests/check.py | grep -i 'T-REPRO'` → reporta. `git ls-remote --heads origin | grep -i catalogo` → 0.

## 5 · PIEZAS
P1 · Lectura y contradicción citada. P2 · Test + contrato coherentes, tres casos, reproducción de M08 en rama. P3 · FP del esquema de procedencia (dos opciones, texto). P4 · Estado de celdas-D.

## 6 · LATITUD
Forma de las columnas: tuya. ≤ 10 líneas adyacentes: sí. Pregunta a mesa (sigues con P3/P4): solo si P1 demuestra que T-REPRO(c) protege algo distinto de lo que dirección supone y la dirección propuesta en §1 no aplica — con la evidencia y una alternativa.

## 7 · PAROS — lista cerrada
a) no aplica · b) bajar la exigencia de T-REPRO (aceptar valor sin cita o cita sin valor), tocar un sello, escribir el catálogo (es del escritor, ADOPCION-4) · c) adoptar · d) no aplica · e) CAJA · f) test y contrato ya son coherentes en origin/main (demuéstralo con el caso M08 en verde).

## 8 · COMPUERTAS
«Tres tests: positivo y dos negativos, antes de cambiar el test» protege: **congelar** (un test que se relaja sin casos negativos es un test borrado). «El catálogo no se escribe aquí» protege: **adoptar**.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `tools/corrida0.py` (solo el bloque T-REPRO(c)), `tests/check.py` (solo T-REPRO(c)), `tests/test_corrida0.py` (casos nuevos), `forense/analisis/astra4-relevo/contratos-otros-consumidores.md` (§ Catálogo; § Procedencia solo con la propuesta marcada como tal), `firmas-pendientes.tsv`/`no-corrido.tsv`, nota, L0, cascada. Ajeno: `milpa/catalogo-momentos-v0_1.tsv`, `milpa/tramite.yaml`, `procedencia.yaml`, escritor, CALC. En vuelo: ADOPCION-3 (`tramite.yaml`; no choca), VISTA-NORMALIZADA-2 (`corrida0.py registro`: otro bloque; rebasa si choca), ENCIG-PISOS-GEN2-1 (caja).

## 10 · LO QUE NO HACE · SUCESORES
No releva llaves, no escribe el catálogo ni procedencia. Sucesores: `GEN2-ADOPCION-BLOQUE-Y-PINES-4` (escritor al catálogo con N y a procedencia con el esquema que mesa firme).
