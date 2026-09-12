# GEN2-39 · Reactivos residuales y búsqueda útil — cierre

Fecha de ejecución: 11/sep/2026  
Entorno: CAJA, Windows/WSL2  
Worktree: `/home/pc0/mm-gen2-reactivos-residuales-busqueda-util`  
Rama: `acto/gen2-reactivos-residuales-busqueda-util`  
Base integrada: `origin/main=e4c25385e218e7e30c4cc45ecdff65a6fcaa36a5`  
PR: #742  
Implementación e índice: `de1d2ed6846dfc566c4c78834980810f15b7bb63`

## Resultado

El buscador vigente ya consume `data/inventario-reactivos-contexto-v1_1.tsv`. El acto conserva las filas acreditadas de v1.0 y agrega 20,653 identidades lógicas con correspondencia exacta por instrumento, ola, tabla/miembro y variable. No se modificaron índices históricos, servicios, cron, adquisición, motor, `consulta_gen2` ni F5.

| Familia | Filas físicas | Con texto v1.0 | Con texto v1.1 | Ganadas | Residual |
|---|---:|---:|---:|---:|---:|
| ENVIPE | 31,140 | 1,248 | 20,703 | 19,455 | 10,437 |
| ENNViH | 17,181 | 17,176 | 17,176 | 0 | 5 |
| ENCUCI | 458 | 2 | 400 | 398 | 58 |
| ENIF | 6,747 | 3,572 | 4,372 | 800 | 2,375 |
| ENSAFI | 369 | 369 | 369 | 0 | 0 |
| **Total** | **55,895** | **22,367** | **43,020** | **20,653** | **12,875** |

El conteo lógico pasa de 22,350 a 43,003 identidades; las 17 filas físicas adicionales son espejos históricos sombreados por sucesor. Los 43,020 textos publicados se separan en 21,869 `PREGUNTA_DICCIONARIO`, 17,177 `ETIQUETA_VARIABLE`, 3,963 `DESCRIPCION_ADMINISTRATIVA` y 11 `PREGUNTA_COMPLETA`. Una etiqueta o descripción acreditada no se presenta como pregunta literal.

## Reparaciones y procedencia

- El extractor XLS/XLSX conserva la pregunta vigente al recorrer subítems; así deja de perder filas subordinadas.
- El lector de PDF usa geometría de palabra y tablas multipágina, acepta las pequeñas diferencias de línea base observadas y conserva página y tabla en cada referencia.
- La identidad de tabla distingue, entre otros casos, `TPer_Vic1` de `TPer_Vic2`; no hay propagación entre olas ni fallback cruzado por el mero nombre de variable.
- ENIF 2021 se lee del XLSX contenido en el ZIP oficial ya manifestado: el PDF del mismo paquete no expone esa estructura como tabla extraíble.
- El caché se identifica por instrumento, formato, hash de fuente y versión del extractor; la publicación es atómica. La segunda ejecución dio 22 aciertos, 0 fallos de caché y hashes de salida idénticos.

No fue necesaria una descarga nueva ni OCR. Se reutilizaron documentos públicos y metadatos ya presentes en el corpus compartido; no se abrieron valores de personas. En ENVIPE 2015 se inspeccionó además la página del descriptor que salta de los sufijos `_01` a `_03`: la ausencia visual de cinco variables se conserva como `PREGUNTA_NO_LOCALIZADA`, no se rellena por analogía.

Versión y hashes de consumo:

- extractor `reactivos-contexto-1.1.7`: `b463e4c49496ce0754853bf416d453fcb0ad5224cf52b3cdfc1281b2eb948329`;
- índice v1.1: `8ce2e0777dd381d00e8f1bafeb867dae4e0449de5b7ecc85c2599f64e7665f20`;
- residual v1.1: `45f496d6d1966fa34d1fb3c9fedec490198987b233bfeae79e827296142287e2`.

Comando reproducible desde otro worktree con el corpus resuelto por el mecanismo vigente:

```bash
python3 tools/actualiza_reactivos_contexto.py
```

## Utilidad demostrada

Las comparaciones usan explícitamente `contexto_v1_0` como antes y `contexto` como índice vigente.

| Consulta | Antes | Después | Identidad y fuente nueva |
|---|---:|---:|---|
| ENCUCI 2020, `donar alimentos` | 0 | 2 | `AP6_1A_2` y `AP6_1_2`, `PREGUNTA_DICCIONARIO`, `FD_ENCUCI2020.pdf`, página 37, tabla `ENCUCI_2020_SEC_6_7_8` |
| ENVIPE 2012, `autoridad militar o naval` | 0 | 1 | `Tmod_Vic.DBF/BP1_32_6`, `PREGUNTA_DICCIONARIO`, `fd_envipe2012.xls`, hoja `TMod_Vic`, fila 317 |
| ENIF 2021, `tienda o comercio como Oxxo` | 0 | 2 espejos físicos | `TModulo/P10_7`, `PREGUNTA_DICCIONARIO`, `enif_2021_estructura_del_archivo.xlsx`, hoja `TModulo`, fila 1285 |

El hallazgo ENIF es un canal de acceso/transacción —retiro, depósito, pago de crédito o servicios— y no acredita por sí mismo ahorro, tenencia de producto, suficiencia científica ni causalidad. Del mismo modo, recuperar texto no resuelve automáticamente NC-0122, NC-0126 u otra demanda científica.

Controles de conservación: `tanda` en ENNViH permanece 52→52 y `atraso` en ENSAFI permanece 3→3. La variable repetida `BP1_23` conserva su objeto: en 2012 pregunta por la razón de no denuncia; en 2013 y 2015 la redacción añade «no denunció o no denunciaron» y cada fila mantiene su propia ola, tabla y fuente. La auditoría no halló referencias con tabla incompatible, identidades indeterminadas ni alteraciones de los campos exactos previamente publicados.

## Desenlace del residual

`data/reactivos-contexto-residual-v1_1.tsv` agrupa 12,875 filas físicas en 6,091 objetos accionables:

| Motivo acreditado | ENCUCI | ENVIPE | ENIF | ENNViH | Total |
|---|---:|---:|---:|---:|---:|
| Correspondencia ambigua | 26 | 2,616 | 0 | 0 | 2,642 |
| Etiqueta técnica no acreditada | 32 | 2,631 | 16 | 0 | 2,679 |
| Fila auxiliar sin reactivo | 0 | 5,105 | 2,357 | 0 | 7,462 |
| Pregunta no localizada | 0 | 85 | 2 | 5 | 92 |

Cada grupo conserva instrumento, ola, miembro/tabla, variables de ejemplo y acción siguiente. Las auxiliares siguen en el denominador: no se ocultaron llaves o ponderadores para elevar cobertura. Los cinco ENNViH no localizados son `cr09_1i`, `cr29_1j`, `cv19_1h`, `es20` y `es21`.

### NC-0100

El subconjunto DBF llega a 1,272/1,304: ENVIPE 2012 queda 400/400, 2013 queda 410/419 y 2015 queda 462/485. Se recuperaron 791 de las 823 filas pendientes. `NC-0100` permanece ABIERTA por 32 identidades: nueve de 2013 y 23 de 2015. En 2015, `AP5_3_02`, `AP5_4_02`, `AP5_5_02`, `AP5_6_02` y `AP5_7_1` no aparecen en el descriptor oficial inspeccionado; el resto requiere acreditar etiquetas técnicas o desambiguar correspondencias. La siguiente acción exacta vive en la fila actualizada de NC-0100.

### NC-0136

`NC-0136` permanece ABIERTA por las 12,875 filas del lote y por los 81 grupos históricamente ciegos fuera de estas cinco familias. Esos 81 grupos no se suman al denominador de 55,895 ni se presentan como filas. El negativo del buscador sólo significa que no hay texto acreditado en los índices consultados: no demuestra inexistencia de una variable ni insuficiencia/suficiencia científica.

## Concurrencia y solapamiento operativo

Por error declarado del operador, dos sesiones trabajaron simultáneamente sobre el mismo encargo 39. El PR #742 nació como punto de relevo con `8b27cb7`; los dos ajustes locales posteriores que no habían entrado en ese punto se revisaron e integraron en `de1d2ed`. Este cierre consolida ambas entregas del 39 en una sola rama y un solo PR. No incorpora ni modifica la rama `acto/gen2-demanda-contratos-ejecucion-nc0165`, que corresponde al encargo 40.

Para 40 y el servicio fusionado por #739, la identidad de implementación consumible es `de1d2ed`, el comando es el indicado arriba y el índice operativo es v1.1 con 20,653 identidades ganadas. La espera de consumo por 40 no bloquea este PR.

## Verificación

- `python3 -m unittest tests.test_reactivos_contexto`: 11/11 correctas.
- segunda actualización: 22/22 objetos desde caché, 0 misses, salidas idénticas;
- comparación antes/después ejecutada sobre documentos reales;
- integración de NC idempotente y limitada a dos filas;
- contador científico: cero; ninguna adopción, parámetro, CALC o RESULT.

## NO-CORRIDO / RESERVAS

- `NC-0100`: acreditar las 32 identidades DBF restantes con correspondencia exacta; no copiar texto por nombre entre olas.
- `NC-0136`: continuar los 81 grupos externos y los 12,875 residuales del lote conforme a su causa explícita.

