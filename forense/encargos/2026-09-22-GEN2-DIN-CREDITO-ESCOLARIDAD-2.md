# ENCARGO · ACTO GEN2-DIN-CREDITO-ESCOLARIDAD-2 · El eje escolaridad de crédito 2024, medido bien: un CALC nuevo con el mapa `niv` correcto, contra el sellado como oro en las 12 celdas sanas

> ENTORNO: **CAJA** — abre ENIF 2024. El hook imprime ENTORNO-DERIVADO; si no coincide, PARA en una línea.

CABECERA · SHA `ccd7c0eb` · una sola sesión · MODELO: Opus · MODO: **RÍGIDO** desde COMMIT-1 (spec congelada; la latitud es logística) · CONTADOR: +1 corrida sellada y registrada, `cuenta_gen2 = SI`, **no adopta**; `celdas_validadas` puede subir si las 4 celdas de escolaridad × 9 conductas entran con veredicto (reportado, no prometido) · CALC-id reservado: `CALC-DIN-CREDITO-PREDICCION-2024-ESCOLARIDAD-0002` (sucesor, nunca edición del `-0001`) · FP/ADR/NC: raíz de acto.

## 1 · OBJETIVO
Que las 4 celdas de escolaridad (`hasta_primaria / secundaria / media_superior / superior`) × 9 conductas de crédito 2024 tengan medición correcta con cadena GEN2, y que el CALC sellado `-ADJUDICACION-0001` quede con su eje escolaridad rotulado `VENCIDO-EN-ALCANCE → sucesor` sin editarlo (E.3). «Hecho» = `python3 tools/corrida0.py verify CALC-DIN-CREDITO-PREDICCION-2024-ESCOLARIDAD-0002` → `REPRODUCE · IDENTICO`; las 12 celdas no-escolaridad del `-0002` reproducen las del `-0001` dentro de tolerancia (oro); `grep -c ESCOLARIDAD-0002 data/corrida0/corridas.tsv` → 1.

## 2 · FIRMAS DE MESA
- `FP-260922-GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-2-3-95ec-01`, opción **(a)** — *propuesta de dirección, mesa la sella con el lanzamiento o la borra*: «Un acto sucesor escribe un CALC nuevo con el mapa `niv` corregido y re-sella A.10 con universo actualizado para escolaridad; el `-0001` no se edita y sus 12 celdas siguen vigentes.» Sin texto → PARA (el acto entero: sin firma no hay sucesor).
- Ya en el repo: `FP-260921-…-COMMIT-1-7866-01` (K6-P-TENEDORES) si mesa la ratifica en E5; si no, las 9 conductas son las que el `-0001` ya midió, sin cambio.

## 3 · LO QUE DIRECCIÓN SABE
- `[LEÍDO]` `data/corrida0/CALC-DIN-CREDITO-PREDICCION-2024-ADJUDICACION-0001/medidor.py:79-80` («niv (2024, 00-11 + 99) -> los mismos cuatro cubos que `_school()` usaba sobre P3_1_1 (2021, 0-9)») y `:154` (`code = {c: m._code(d[c]) …}` incluye `niv`): `_code` quita el cero inicial y `01`…`09` colapsan mal contra un mapa de dos dígitos. `NC-260922-…-95ec-01`: «el marginal correcto de escolaridad … no entró a ninguna comparación cuantitativa».
- `[EXISTE]` `…-EMISIONES-0001/` (los candidatos) y `…-ADJUDICACION-0001/` (12/16 celdas vigentes). No sé si el defecto también afecta a las emisiones o solo a la adjudicación: **el acto lo lee**; si afecta a las emisiones, el `-0002` re-emite escolaridad también (rama prevista, dentro del OBJETIVO).
- `[SUPUESTO]` La reserva de ENIF 2024 para este lote ya está consumida (COMMIT-2/3 del `-0001` midió sobre ella); re-medir un eje no la rompe más. Si resulta falso —queda alguna celda no derivada—, PARO a) para esa celda y se declara.
- ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
`ls -d data/corrida0/CALC-DIN-CREDITO-PREDICCION-2024*` → dos CALC, ningún `ESCOLARIDAD`; `grep -c "ESCOLARIDAD-0002" data/corrida0/corridas.tsv forense/no-corrido.tsv` → 0. Ramas vivas: ninguna.

## 5 · PIEZAS
- **COMMIT-1 · spec congelada sin abrir microdato:** el mapa `niv` 2024 → cuatro cubos, **por texto del catálogo** (`catalogos/niv.csv`, A.15c), con los códigos de dos dígitos intactos; todo lo demás heredado verbatim del `-0001` (candidatos, criterio, `INDECIDIBLE`, universo, `FAC_ELE`, seed) y el `-0001` declarado **oro** para las 12 celdas sanas (E.5). `spec-check` VERDE; D-22 sintético con un caso `niv=01` y otro `niv=10`.
- **COMMIT-2 · corrida:** las 16 celdas × 9 conductas; verificación de que las 12 sanas reproducen el oro (tolerancia declarada) — si no reproducen, el hallazgo es ese y el acto para en f) con el diff pegado.
- **COMMIT-3 · cierre:** registro en la vista y asiento de replay en el mismo acto (E.7); enmienda fechada en el `-0001` (nota, no archivo sellado) y en la celda-D/FP: eje escolaridad `VENCIDO-EN-ALCANCE → -0002`; NC-…-95ec-01 CERRADA.
- «si `[SUPUESTO]` resulta falso»: dicho arriba.

## 6 · LATITUD
DECIDES TÚ: nombres, orden, enlazar `data/raw`, dependencias, ≤ 10 líneas adyacentes declaradas. PREGUNTAS A MESA: si el catálogo `niv` 2024 tiene un código sin cubo evidente (p. ej. «normal», «técnica»), ¿cubo por texto según el árbitro (recomendado, con cita) o celda `NO-CONSTRUIBLE`? — y sigues con los demás. NO DECIDES: §7.

## 7 · PAROS
a) abrir dato reservado fuera del código autorizado (ninguno previsto) · b) editar el `-0001` o forzar · c) adoptar · d) cambiar estimando/universo/criterio del `-0001` (solo el mapa `niv`) · e) nube · f) inalcanzable · g) el código congelado en COMMIT-1 no corre → no se parcha.

## 8 · COMPUERTAS
«Firma (a) presente en el lanzamiento — protege: congelar spec.» Ninguna otra.

## 9 · PERÍMETRO
Propio: `forense/prereg-caja/DIN-CREDITO-ESCOLARIDAD-2-spec-v1_0.md` (+ sidecar, `spec.yaml`) · `data/corrida0/CALC-DIN-CREDITO-PREDICCION-2024-ESCOLARIDAD-0002/` · derivados por comando · `replay-evidencia.tsv` (asiento) · nota · tablero al cierre · `canon/L0/<raíz>.md`. Ajeno: los dos CALC `-0001` (solo lectura), `milpa/`, celdas-D ajenas. Otro acto en vuelo: ninguno verificado; **E2 y E3 son de caja: no corren a la vez que éste** (comparten derivados). «Si te encuentras escribiendo fuera de esta lista, PARA.» Perímetro de cierre permanente (D-21).

## 10 · NO HACE · SUCESORES · CIERRE
No adopta, no toca el `-0001`, no cambia candidatos. Sucesor: la adopción de lo que gane, por mesa. Auditoría: no aplica (afirma sobre el aparato; la afirmación sobre México ya la hizo el `-0001`). Cierre por /acto.

## NO-CORRIDO / RESERVAS

| qué (verbatim del encargo) | por qué | impacto | sucesor |
|---|---|---|---|
| COMMIT-3 · «registro en la vista»; «Hecho»: «`grep -c ESCOLARIDAD-0002 data/corrida0/corridas.tsv` → 1» | DECISIÓN-DE-MESA-PENDIENTE: la firma P4 (derivados no viajan en PR, guarda `enrutamiento-pr`) choca con E.7, y el job de main no re-deriva `corridas/resultados/usos.tsv`. La re-derivación local se midió (exit 0, 0 transiciones de replay, `usos.tsv` idéntico, +21 CALC ajenos sellados sin fila) y se revirtió | la corrida queda «sellada en disco, no registrada» en la vista publicada; verificada, asentada en `replay-evidencia.tsv` y contada por `corrida0 status` | `FP-260922-GEN2-DIN-CREDITO-ESCOLARIDAD-2-0af9-01` · `NC-260922-GEN2-DIN-CREDITO-ESCOLARIDAD-2-0af9-01` |
| CONTADOR · «`celdas_validadas` puede subir si las 4 celdas de escolaridad × 9 conductas entran con veredicto (reportado, no prometido)» | DECISIÓN-DE-MESA-PENDIENTE: el veredicto entró (ADJ16), pero la métrica sólo lee el marcador y las celdas-D, y esta línea no pasa por ahí | `celdas_validadas` = 92, sin cambio | `NC-260922-GEN2-DIN-CREDITO-ESCOLARIDAD-2-0af9-02` (mesa) |

Nada más: la rama «si afecta a las emisiones, re-emite» no se tomó porque su condición es falsa (nota §0), y la pregunta de LATITUD §6 no hizo falta (nota §0).
Adendas de este encargo: `forense/encargos/2026-09-22-GEN2-DIN-CREDITO-ESCOLARIDAD-2-ADENDA-1.md` (firma de mesa del lanzamiento).

## CONSUMIDO

Ejecutado por ACTO GEN2-DIN-CREDITO-ESCOLARIDAD-2 en **PR #1005** (rama `acto/gen2-din-credito-escolaridad-2`), ADR `ADR-260922-GEN2-DIN-CREDITO-ESCOLARIDAD-2-0af9-01`. El PR queda para que mesa lo fusione.
