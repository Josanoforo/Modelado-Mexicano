# ENCARGO · ACTO GEN2-TUBERIA-VISTA-NORMALIZADA-4 · Un RESULT es un número con unidad; una lista es una tabla: `valor` sale de la vista por referencia cuando pasa de 1 KB, el conducto lo exige a los CALC futuros, y el canal publica hoy con la guarda a 100 MB que vuelve a 50 en este mismo PR

> ENTORNO: **NUBE** — `registro`, conducto, vistas derivadas en árbol, CI. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción `8358b891` (re-deriva al abrir; el PR de TABLERO-EN-CANAL puede haber fusionado: se hereda) · una sola sesión, rama propia (la que fije la plataforma; se declara en el 0-bis) · MODELO: Opus · MODO: **AUTÓNOMO** (cláusula v1.0 `3fbc487684b77b7f`; `registro`, la guarda de tamaño y el conducto están en el perímetro **propio** de este acto: ningún PARO por «ajeno») · ids con raíz de acto (D-24) · D-21 aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` al pie.
CONTADOR: cero mediciones; no adopta; **ningún valor de ningún RESULT cambia** (el número sigue siendo el mismo; solo cambia dónde vive el texto largo). Contadores de tiempo y tamaño antes/después en la nota. El primer `[deriva]` que este acto provoque es el que mueve la vista de `main` por primera vez desde el 23/sep.

## 1 · OBJETIVO
Diagnóstico de TABLERO-EN-CANAL (24/sep, verificado por dirección): en `main` publicado, la columna `valor` de `resultados.tsv` pesa 1.3 MB (65 287 filas; solo 51 celdas > 1 KB, la mayor 0.05 MB); en el árbol re-derivado pesa 65 MB porque CALC nuevos (ASTRA-5: `CALC-ENOE-PERSISTENCIA-0001` con 11 MB; y otros) guardan listas completas en una celda. Resultado: 92 MB > guarda de 50 → ningún `[deriva]` se abre.
- **COMMIT-A (puente, publica hoy):** guarda de tamaño a 100 MB **con comentario que cita este acto y la fecha de vuelta a 50**; merge → el push dispara el job (30 min) → `[deriva]` abre con `check` VERDE. Es la única vez que la guarda sube; C (sacar corridas del lote) queda descartada por E.7.
- **COMMIT-B (la corrección):** en `registro --escribe`, cualquier `valor` cuya representación supere **1 KB** se escribe a `data/corrida0/<CALC>/tablas/<resultado_id>.<ext>` (`.tsv` si es tabular, `.json` si no; el archivo es derivado del RESULT sellado, no un sello nuevo: se regenera desde `resultados.json`) y la celda `valor` lleva `REF:<ruta>#sha256:<hash>`; `tools/vista.py` (VISTA-2) gana `valor_de(resultado_id)` que resuelve la referencia; los 18 consumidores de la vista pasan por ahí (test). Tamaño resultante pegado; guarda **de vuelta a 50 MB** en este mismo commit.
- **COMMIT-C (el conducto, D-22):** `_valida_outputs` exige a todo CALC nuevo: `valor` escalar (número, cadena corta, booleano) o JSON ≤ 1 KB; una lista o tabla va a `tablas/` dentro del CALC **antes de sellar**, con el RESULT citándola por ruta y sha. Los CALC ya sellados no se tocan (E.3): el conducto los acepta con `WARN` rotulado `VALOR-LARGO-LEGADO` y `registro` los referencia (COMMIT-B). Test con un CALC sintético que emite una lista: sin `tablas/` → rechazado; con `tablas/` → aceptado. Documentar en `data/INFRAESTRUCTURA-v1_0.md` (spec de vistas y conducto, D-15: spec antes que código).
«Hecho» sobre el commit final con origin/main fusionado: un `[deriva]` posterior al COMMIT-A citado por run y PR, con `check` VERDE, fusionado por auto-merge, y `status` en `main` con las vistas del día (los valores los da el derivador) · `resultados.tsv` re-derivado < 50 MB tras COMMIT-B y guarda = 50 (grep pegado) · test de equivalencia: para cada RESULT, `valor_de(id)` antes/después idéntico (incluidos los 51 y los nuevos) · conducto con el test sintético VERDE y `INFRAESTRUCTURA` actualizado · los 18 consumidores adaptados con test · `check.py --baseline` VERDE sin `--force` · FP `…TABLERO-EN-CANAL-1-3dd4-01` cerrada con `DECISIÓN-DADA: A + puente B`.

## 2 · FIRMAS DE MESA — dadas, verbatim
- **Firma de VISTA-NORMALIZADA-2 (24/sep)**: «…ningún archivo derivado vuelve a superar 50 MB; sin Git LFS y sin sacar la vista del canal.» **INTERPRETACIÓN-DECLARADA**: el puente a 100 MB es temporal, dentro de este mismo acto, y vuelve a 50 en COMMIT-B; la intención (vistas pequeñas, sin LFS, sin sacar nada del canal) se preserva.
- **Decisión de dirección 24/sep sobre la FP `3dd4-01`** (comunicada a mesa; mesa veta si no): «Opción A —valor por referencia cuando pasa de 1 KB, y regla en el conducto para CALC futuros—, con la guarda a 100 MB solo hasta que A fusione; C descartada por E.7.»
- **E.3** (sellos no se tocan: los CALC legados se referencian, no se re-sellan) · **E.7** (toda corrida sellada entra a la vista) · **D-22** (el conducto exige forma antes de sellar).

## 3 · LO QUE DIRECCIÓN SABE
`[EJECUTADO]` (`8358b891`) medición de `valor` en el `resultados.tsv` publicado: 1.3 MB / 65 287 filas / 51 celdas > 1 KB / mayor 0.05 MB (ENIGH perfil estructural, ENCUCI respuesta por contacto, ENIGH remesas contexto). `[REPORTADO]` por TABLERO-EN-CANAL (runs 36068464848, 36066873728): re-derivado 92 MB; `valor` 65 MB; `CALC-ENOE-PERSISTENCIA-0001` 11 MB; job muere por 10 min (ya 30) o por guarda; `usos.tsv` re-derivado igual al de `main`. **Verifica los tres números tú con el mismo lote que CI.** `[LEÍDO]` VISTA-2 (#1113): `tools/vista.py`, campos de corrida movidos, guarda 100/50; VISTA-3 (#1121): `KeyError('tolerancia')`. Consumidores: `git grep -l 'resultados.tsv\|valor' -- tools tests` → 18 (VISTA-2 los listó). `[SUPUESTO]` que ningún consumidor necesita el texto largo de `valor` para decidir (son tablas de salida, no insumos de dictamen); si uno sí, pasa por `valor_de()` y se dice.

## 4 · YA HECHO / YA DECIDIDO
`grep -n 'size\|+50M\|+100M' .github/workflows/verify.yml` → reporta la guarda vigente. `ls data/corrida0/*/tablas 2>/dev/null | wc -l` → 0. Las 51 celdas legadas > 1 KB se referencian igual que las nuevas (no se distinguen por antigüedad).

## 5 · PIEZAS
COMMIT-A (guarda 100 + comentario; merge; `[deriva]` citado) → COMMIT-B (`registro` por referencia; `vista.py.valor_de`; consumidores; equivalencia; guarda 50) → COMMIT-C (conducto + test sintético + spec) → cierre de FP `3dd4-01` y NC de TABLERO-EN-CANAL.

## 6 · LATITUD — CLÁUSULA DE AUTONOMÍA v1.0 (`3fbc487684b77b7f`, verbatim en el ADR)
1. Discrepancias encargo↔repo las resuelve el ejecutor y las declara. 2. Firma con letra en choque e intención clara: INTERPRETACIÓN-DECLARADA, se sigue. 3. Lo redactable se redacta, rotulado PROPUESTO-POR-EJECUTOR, con fuente. 4. Bifurcación con opción recomendada: se ejecuta la recomendada. 5. PARO solo por D-19 estricta. 6. Nunca: cifra tecleada, sello reescrito, reserva abierta, fuera de §9 sin declarar. 7. El «Hecho» no se rebaja. Umbral de 1 KB, extensión y formato de `tablas/`: tuyos, declarados en la spec. Si el job vuelve a morir por tiempo con 30 min, `registro --lote` incremental o subir a 60 min: tuyo, declarado. Pregunta a mesa prevista: **ninguna**.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) abrir dato reservado · b) reescribir un sello o un `resultados.json`; `--force`; `--excluye`; sacar corridas del lote · c) mover contadores a mano · d) cambiar un procedimiento de medición · e) CAJA.

## 8 · COMPUERTAS
«`valor_de(id)` idéntico antes/después para todo RESULT» protege: **congelar** (la vista publica lo sellado, sin cambiar un valor). «Guarda vuelve a 50 en COMMIT-B, no después» protege: **borrar** (un GH001 silencioso es una publicación perdida). «Conducto exige forma antes de sellar; los sellados no se tocan» protege: **congelar / borrar** (E.3).

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `tools/corrida0.py` (`registro --escribe`, `_valida_outputs`), `tools/vista.py`, los 18 consumidores, `.github/workflows/verify.yml` (guarda de tamaño; tiempo del job si hace falta), `data/corrida0/*/tablas/` (derivado; `derivados_protegidos.py` lo cubre), `data/INFRAESTRUCTURA-v1_0.md`, tests, `firmas-pendientes.tsv`/`no-corrido.tsv` (estado/append), nota, L0, cascada. Ajeno: `resultados.json` de cualquier CALC, sellos, medidores, `marcador_segmento.py`, el bloque del tablero (TABLERO-EN-CANAL). En vuelo: TABLERO-EN-CANAL-1 (mismo `verify.yml`: si su PR no fusionó, rebasa; su guarda de árbol sucio se conserva), RENDIMIENTO-1 (toca `registro` por rendimiento: **coordinar por commit; equivalencia byte a byte cubre a los dos**), RELEVO-MOTOR-34-1 (diagnostica por qué `usos.tsv` no cuenta las reglas de ADOPCION-4 — no es de este acto).

## 10 · LO QUE NO HACE · SUCESORES
No corrige por qué `adoptados` no sube (RELEVO-MOTOR-34-1), no re-sella CALC con listas (legados: referenciados), no mide. Sucesor: `-5` solo si un consumidor no puede pasar por `valor_de()`.

## NO-CORRIDO / RESERVAS

- **qué:** «un `[deriva]` posterior al COMMIT-A citado por run y PR, con `check` VERDE, fusionado por auto-merge, y `status` en `main` con las vistas del día».
  **por qué:** NO-VERIFICABLE-AQUÍ — requiere el merge de este PR y la corrida del job en el push resultante; el job del push de #1122 (run 36074645794) corre todavía sin COMMIT-B y debe parar en GUARDA-TAMANO.
  **impacto:** la vista de `main` sigue siendo la del 21-23/sep hasta ese `[deriva]`; ningún contador se mueve por esto (`adoptados_activos` = 72 antes y después, medido).
  **sucesor:** NC-260924-GEN2-TUBERIA-VISTA-NORMALIZADA-4-574d-01 (seguimiento tras el merge).

- **qué:** «COMMIT-A (puente, publica hoy): guarda de tamaño a 100 MB».
  **por qué:** SUSTITUIDO-POR:GEN2-TUBERIA-VISTA-NORMALIZADA-4 COMMIT-B — A y B viajan en el mismo PR; con B la vista re-derivada mide 28.9 MB y la guarda se queda en 50. Absorbe: la publicación de hoy. Huérfano: nada.
  **impacto:** ninguno; se evita la ventana a 100 MB.
  **sucesor:** ninguno necesario (NC-…-574d-01 cubre la prueba real).

Discrepancias declaradas (el cuerpo no se edita): `tablas/` ya existía sellada en CALC-EDER2017-PRIMERA-UNION-SEXO-COHORTE-000{1,2} → el derivado va a `valores-vista/`; `derivados_protegidos.py` no cubría archivos sin cabecera → reconocimiento por ruta añadido; B y C en un solo commit. Detalle en `ADR-260924-GEN2-TUBERIA-VISTA-NORMALIZADA-4-574d-01`.

## CONSUMIDO

PR https://github.com/Josanoforo/Modelado-Mexicano/pull/1129 (rama `claude/new-session-e85tdt`). ADR de raíz: `ADR-260924-GEN2-TUBERIA-VISTA-NORMALIZADA-4-574d-01`. El PR no se fusiona en este acto: mesa fusiona.
