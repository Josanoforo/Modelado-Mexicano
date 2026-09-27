# GEN2-CIERRE-SEMANAL-1 · nota de cierre (26/sep/2026)

`ADR-260926-GEN2-CIERRE-SEMANAL-1-dea2-01` · encargo `forense/encargos/2026-09-26-GEN2-CIERRE-SEMANAL-1.md` (SHA de redacción `34949751`) · NUBE (hook: `ENTORNO-DERIVADO = NUBE`, corpus montado=NO, examinados=0) · MODO AUTÓNOMO-AMPLIO · un PR, rama `claude/new-session-bjfemh`.

**Contadores (primera línea del módulo de auditoría):** cero mediciones y cero adopciones propias. El catálogo **ejecuta** adopciones ya firmadas (FIRMAS-19 J1–J10, `…afe1-01`). `celdas_validadas` 219 → 219 (Δ0).

## Qué se entregó

| pieza | archivo | derivación | test |
|---|---|---|---|
| P1 catálogo v1.2 | `canon/catalogo-del-mexicano-v1_2.{md,tsv}` | `python3 forense/analisis/catalogo/genera_catalogo_v1_2.py` | `tests/test_catalogo_v1_2.py` |
| P2 informe v1.4 | `canon/informe-programa-v1_4.md` | `forense/analisis/informe-v1_4/cifra.py <clave>` + `corrida0 status` | `tests/test_informe_derivado.py` (toma el más nuevo) |
| P3 estado v1.17 | `canon/estado-programa-v1_17.md` | comandos en §17 | `tests/test_estado_derivado.py` (toma el más nuevo) |
| P4 tabla de piso v1.1 | `canon/tabla-de-piso-v1_1.tsv` | `python3 tools/genera_tabla_piso_v1_1.py --escribe` | `tests/test_catalogo_v1_2.py` |
| derivador compartido | `tools/deriva_cifras.py` | refresca `N <!-- deriva: cmd -->` en `docs/` | `tests/test_frente_publico_2.py` |

Cifras del catálogo, por comando: 43 188 estimadores <!-- comando: python3 forense/analisis/informe-v1_4/cifra.py cat:estimadores -->, 7 296 de ellos con reserva de ancho <!-- comando: python3 forense/analisis/informe-v1_4/cifra.py cat:estado_adopcion:ADOPTADO-CON-RESERVA-DE-ANCHO -->, 45 firmas distintas citadas <!-- comando: python3 forense/analisis/informe-v1_4/cifra.py cat:firmas_citadas -->. Hay 13 dominios medidos <!-- comando: python3 forense/analisis/informe-v1_4/cifra.py cat:dominios_medidos --> en 14 de 31 reports <!-- comando: python3 forense/analisis/informe-v1_4/cifra.py cat:reports_medidos -->, y 1 FP de adopción pendiente (ENSU) <!-- comando: python3 forense/analisis/informe-v1_4/cifra.py cat:pendientes_de_firma -->.

## Premisas y discrepancias (cláusula de autonomía, puntos 1, 2 y 4)

- **`[SUPUESTO]` ENSU y COLA-LOTE-1 fusionan durante el acto.** ENSU fusionó (`PR #1162`) y se trajo por `git merge origin/main`; su FP de adopción `…5916-01` sigue ABIERTA, así que por §2 **no entra y se lista como pendiente**. COLA-LOTE-1 no fusionó: se cita «en curso, rama `acto/gen2-cola-lote-1`».
- **Estado v1.17 contra «versiones previas sin diff».** `T01` admite una sola versión viva de `estado-programa`. Se siguió el precedente firmado por mesa en v1.12–v1.16: **v1.16 se retira del árbol sin editarse** (recuperable por SHA; v1.17 la hereda verbatim, con diff vacío en el cuerpo). El puntero `RUTA_ESTADO_PROGRAMA` (T52) y los punteros de `tools/cierre_acto.py`, sus tests, `censo_evaluaciones.py` y las skills `acto`/`revisa` apuntan a v1_17. INTERPRETACIÓN-DECLARADA: retirar no es editar.
- **«611 afirmaciones sin programa».** En `canon/mapa-dominios-v1_1.tsv` la cifra es `estado_corpus_v1_1 = INSTRUMENTO-SIN-EQUIVALENCIA`: el instrumento que cita la afirmación no tiene programa equivalente en el corpus. `PROGRAMA-NO-OBTENIDO` son solo 10. El informe lo rotula así (INTERPRETACIÓN-DECLARADA).
- **«legacy 146 → 67».** El 146 se cita del 24/sep (`ADOPCION-BLOQUE-Y-PINES-2`) y el 67 sale de `status` hoy.
- **Oferta de DINERO-SERIES.** Ese acto no produjo columna de oferta (su P4 terminó en `PARO-ENTORNO`, NC `8dbe`). La columna del catálogo sigue siendo la de ENIF crédito, y así se declara.
- **Vistas del 23/sep.** Las cifras de `status` no dependen de las vistas: `status` reconstruye el registro en memoria. No se re-corrió `registro --escribe` (nota al pie del informe).
- **Defectos adyacentes (D-21):**
  - `tests/test_frente_publico_2.py` exigía que la tabla de piso v1.0, que es histórica, igualara el contador vivo (72 ≠ 81, rojo también en `main`). Se quitó esa aserción.
  - `docs/one-pager.md` traía 3 cifras desfasadas (246 → 287 corridas, entre otras). Se refrescaron con el derivador.
  - Dos filas del catálogo salían `SIN-DOMINIO` porque su primer consumidor era una fila de `milpa/catalogo-momentos-v0_1.tsv`. Ahora toman el dominio de otro consumidor.
  - Los derivados de `v1_2/` llevan sufijo `-v1_2` por `T02`.
  - `GEN2-PRODUCTO-CONSULTA-1` (`PR #1163`) fusionó durante el acto, y el encargo lo había previsto («si toca `docs/`, rebasar»). Su `tools/benchmark.py` toma el catálogo de N mayor, así que el export de Pages y `docs/ejemplos.md` quedaban en v1.1: se regeneraron con `benchmark.py exporta` y `benchmark.py ejemplos`. `docs/data/catalogo-v1_1.json` se conserva.
  - El clon era superficial. Se corrió `git fetch --unshallow` para que corrieran los comandos `git log --merges` heredados.

## Receta de release `v2026.09.2`, para mesa (P5)

- **Tag:** `v2026.09.2`
- **Título:** Benchmark del Mexicano — catálogo v1.2, informe v1.4, estado v1.17 (cierre del 22–26/sep)
- **Dos líneas derivadas:**
  1. Catálogo del mexicano v1.2: 43 188 estimadores adoptados, cada uno con su firma de mesa citada por id <!-- comando: python3 forense/analisis/informe-v1_4/cifra.py cat:estimadores -->. Cubre 13 dominios en 14 de los 31 reports del corpus <!-- comando: python3 forense/analisis/informe-v1_4/cifra.py cat:dominios_medidos && python3 forense/analisis/informe-v1_4/cifra.py cat:reports_medidos -->. Ninguna fila tiene piso heredado de legacy <!-- comando: python3 forense/analisis/informe-v1_4/cifra.py cat_origen:HEREDADO-DE-LEGACY -->. Todo es retrospectivo.
  2. 219 celdas validadas (20 prospectivas, reportadas aparte) sobre 287 corridas selladas. Las dependencias legacy activas bajaron de 146 a 67 en la semana <!-- comando: python3 tools/corrida0.py status | grep -E "^(celdas_validadas|celdas_validadas_prospectiva|N_corridas_selladas|dependencias_numericas_legacy_activas)=" -->.
- **Qué sube a Zenodo:** el tag completo. Mesa activa la integración GitHub → Zenodo y decide el DOI (pendiente en `FP-260923-GEN2-FRONT-1-4296-01`, ABIERTA). `CITATION.cff` va sin cambios.
- Este acto **no publica en Zenodo**: la publicación y el DOI quedan para mesa, con esta receta.

## Módulo de auditoría de rigor extremo

- **¿Cuántos contadores movió este trabajo?** Ninguno del marcador. Los del catálogo se mueven porque se ejecutan adopciones ya firmadas.
- **¿Pobreza, informalidad o violencia confundidas con cultura?** Las reglas SI-ENTONCES heredadas de v1.1 leen primero estructura y oferta. Las filas nuevas son descriptivas y sin regla.
- **¿Sobregeneralización desde la clase media urbana?** WVS, Latinobarómetro y PEW tienen muestras pequeñas y sin diseño completo. Entran con reserva de ancho, y su «clase» es subjetiva, no NSE AMAI.
- **¿Qué cambia con foco rural o indígena?** Lo mismo que en v1.1. Lo indígena-comunal sigue fuera por diseño.
- **¿Qué parece psicológico y es incentivo?** Sin cambio respecto a v1.1: la denuncia con seguro y la denuncia de violencia.
- **¿Evidencia débil con intuición fuerte?** Los PORQUE de v1.1, con tier propio. No se añadieron reglas.
- **¿Qué afirmación sobre el corpus se escribió a mano?** Ninguna cifra: cada una sale de un comando o de una plantilla con test. Las frases «en curso» y «ABIERTA» se verificaron contra `origin/main` y `firmas-pendientes.tsv`.
- **¿Deuda asumida que caducó?** La tabla de piso v1.0 como contador vivo, y el «catálogo en construcción» del README. Las dos se corrigieron.
- **¿Escala de cada cantidad?** Está en la columna `unidad`. El consumo ENIGH/ENGASTO es por hogar.
- **¿PROSPECTIVA y RETROSPECTIVA mezcladas?** No. Todo el catálogo es RETROSPECTIVO. Las familias 2027 y las celdas prospectivas se nombran aparte.
- **¿Unidades promediadas?** No.
- **¿Qué sería peligroso leído simplista?** Leer «43 188 estimadores» como 43 188 hallazgos independientes. Casi todos son celdas ENOE de trimestre × eje × segmento.

## Suite

`python3 tests/check.py --rapido`: 0 FAIL. Los tests propios y los heredados que tocan los cuatro documentos se re-corrieron localmente; el resultado está en el cuerpo del PR. `check.py --baseline` completo lo juzga el CI.
