# GEN2-38 · investigación NC-0126 · continuación IIEG Jalisco

Versión de pregunta: `2026-09-09-horizonte-ahorro-descolapsado-v1`.

Definición buscada: «P4_10 = 1 es una categoría colapsada y el descriptor no
permite descolapsarla». Se requiere tenencia de ahorro separada del horizonte
temporal, para personas adultas en México y con ponderador/diseño comparable a
ENIF 2024.

Estado de entrada: ENIF, EACF, ENSAFI y Findex 2025 ya estaban examinadas. ENIF
colapsa «menos de una semana» con «no tiene ahorros»; EACF no separa ausencia en
SF12; ENSAFI separa tenencia pero mide monto respecto del ingreso, no duración de
cobertura; Findex mide frecuencia. No se repitieron sus descargas.

Modos ejecutados: `CONSTRUCTO` y `HERMANAS`.

## Consultas y resultados

- Búsqueda web real: `site:inegi.org.mx ENFIH cuestionario ahorro cuánto tiempo
  podría cubrir gastos ahorros 2019`. Confirmó que ENFIH 2019 capta tenencia y
  monto de activos financieros, pero no localizó duración condicionada a
  tenencia.
- Búsqueda web real: `México encuesta "cuánto tiempo" "ahorros" cubrir gastos
  cuestionario`. Localizó la Encuesta de Inclusión Financiera de hogares de
  Jalisco del IIEG, además del reactivo ENIF ya agotado.
- Búsqueda web real: `site:iieg.gob.mx "Encuesta inclusión financiera 2022"
  microdatos base de datos`. Localizó la página pública de estudios del IIEG y
  sus microdatos XLSX de 2021, 2022, 2023 y 2024.
- Control local: `python3 tools/busca_reactivos.py --palabra ahorro --limite 50`.
  El índice local contiene tenencia, monto y frecuencia en las familias ya
  examinadas; no mostró una secuencia tenencia→duración que resolviera la
  categoría.
- A.8: `rg -in "iieg|inclusión financiera.*jalisco|Base-Inclusión-Financiera|
  ds_inclusión" data/manifiesto.yaml
  data/curacion-registro/cola-adquisicion-registro.tsv` no produjo coincidencias.
- Verificación de contenido: se descargó dos veces a temporal el XLSX público
  2024 desde `https://iieg.gob.mx/ns/wp-content/uploads/2024/11/Base-Inclusi%C3%B3n-Financiera-2024.xlsx`.
  Ambas copias dieron SHA-256
  `236f885980eb10648dff7e3c129c87368d469abb92b15c2190ae9d9a1cd2c7fe` y
  abrieron como XLSX. La hoja `Datos` tiene 735 registros más encabezado; `P14`
  es tenencia de ahorro (Sí/No) y `P15` conserva literalmente la categoría
  `Menos de una semana/ No tiene ahorros`.

## Candidata y clasificación

`IIEG_EIF_JALISCO_2021_2024` es una fuente pública nueva respecto del corpus y
queda enlazada al mandato `GEN2-38` bajo el alcance
`AUTORIZADA-POR-ALCANCE:Jonas/2026-09-12/GEN2-38/IIEG_EIF_JALISCO_2021_2024`.
El IIEG publica informes y microdatos por ola en su página de estudios. La ola
2024 acredita hogar en Jalisco, levantamiento telefónico y una base pública.

Clasificación: `EXISTE-NO-SATISFACE`. Aunque `P14` permite saber si el hogar
declara ahorrar, `P15` sigue colapsando ausencia y menos de una semana; además,
la unidad es hogar, la cobertura es Jalisco y el diseño es muestra aleatoria
simple telefónica, no persona adulta nacional con diseño ENIF. Por ello no se
creó residual ni se adquirió: los bytes no habilitarían el uso declarado y su
adquisición no corregiría la brecha conceptual.

## Suficiencia y frontera

- identidad: `ACREDITADA` para la evidencia base ENIF;
- conceptual: `NO_ACREDITADA` para NC-0126;
- poblacional: `ACREDITADA` en la evidencia base ENIF; la candidata IIEG no la
  reemplaza porque es sólo Jalisco;
- selección/no respuesta: `ACREDITADA` en la evidencia base ENIF; la candidata
  IIEG queda evaluada aparte como parcial;
- unidad: `ACREDITADA` en la evidencia base ENIF; la candidata IIEG es hogar y
  no sustituye esa unidad;
- temporalidad: `ACREDITADA` (ENIF 2024);
- diseño: `ACREDITADA` en la evidencia base ENIF; el diseño IIEG es sólo
  evidencia incompatible de alcance menor;
- identificación: `NO_APLICA` para el uso descriptivo;
- uso habilitado: `INCOMPATIBLE`; pregunta original: `ABIERTA`.

Negativo acotado: se agotó hoy la pista pública subnacional evidente del IIEG
Jalisco, con búsqueda, A.8 y apertura del microdato 2024. Segunda pasada
crítica: se examinó el reactivo exacto y no sólo un proxy; HTTP 200 no se tomó
como prueba; el XLSX se abrió y se compararon unidad, población, ola, variable
y diseño. No se infiere ausencia fuera de este universo.

Frontera no examinada: otras encuestas estatales no indexadas, módulos
académicos públicos con muestra nacional y nuevas olas posteriores a 2024;
módulos privados permanecen fuera del alcance. Cursor: buscar únicamente una
fuente pública nueva que pregunte primero tenencia y luego duración sólo a
quienes sí ahorran, con unidad persona y cobertura nacional; no repetir ENIF,
EACF, ENSAFI, Findex, ENFIH ni IIEG Jalisco. Próxima revisión: 2026-10-11.
