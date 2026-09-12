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
  sus microdatos XLSX de 2022, 2023 y 2024. La página enlaza un informe
  2021, pero no una base 2021; no se cuenta como microdato descargable.
- Control local: `python3 tools/busca_reactivos.py --palabra ahorro --limite 50`.
  El índice local contiene tenencia, monto y frecuencia en las familias ya
  examinadas; no mostró una secuencia tenencia→duración que resolviera la
  categoría.
- A.8: `rg -in "iieg|inclusión financiera.*jalisco|Base-Inclusión-Financiera|
  ds_inclusión" data/manifiesto.yaml
  data/curacion-registro/cola-adquisicion-registro.tsv` no produjo coincidencias.
- Verificación de contenido: se descargaron dos veces los tres XLSX públicos
  2022–2024. Cada par fue idéntico y los tres contenedores pasaron
  `python3 -m zipfile -t`. En 2022 `ahorro` pregunta si la persona o algún
  miembro del hogar ahorra en una institución financiera y `cubrir_gastos`
  conserva «Menos de una semana/ No tiene ahorros». En 2023–2024 las
  equivalentes son `P6` y `P14`; `P15` no es horizonte (en 2024 es sexo).

## Descarga, corpus y lectura

Los tres pares estables se incorporaron al corpus compartido bajo
`data/raw/iieg_inclusion_financiera_jalisco/` y se registraron con procedencia
en `data/manifiesto.yaml`:

| ola | id de manifiesto | bytes | SHA-256 |
|---:|---|---:|---|
| 2022 | `iieg_inclusion_financiera_jalisco_2022_xlsx` | 80,389 | `09a60f56b3031d8317bf85b2b67ff55b1913c9d0ea229211cf05e34b108a622f` |
| 2023 | `iieg_inclusion_financiera_jalisco_2023_xlsx` | 117,962 | `d86673ceb06fdd5b497e6aa1df4e519f83ea892d20578cb45cf6f477312066b7` |
| 2024 | `iieg_inclusion_financiera_jalisco_2024_xlsx` | 119,644 | `236f885980eb10648dff7e3c129c87368d469abb92b15c2190ae9d9a1cd2c7fe` |

La incorporación acredita que la fuente fue obtenida y leída; no que la
necesidad esté cubierta. La evaluación de uso falla por concepto, población y
unidad, de modo que los bytes quedan como evidencia negativa versionada y no
como sucesor calculado o adoptado.

## Candidata y clasificación

`IIEG_EIF_JALISCO_2022_2024` es una fuente pública nueva respecto del corpus y
queda enlazada al mandato `GEN2-38` bajo el alcance
`AUTORIZADA-POR-ALCANCE:Jonas/2026-09-11/GEN2-38/IIEG_EIF_JALISCO_2022_2024`.
El IIEG publica informes y microdatos por ola en su página de estudios. La ola
2024 acredita hogar en Jalisco, levantamiento telefónico y una base pública.

Clasificación: `EXISTE-NO-SATISFACE`. `ahorro`/`P6` sólo identifica ahorro
institucional de algún integrante del hogar, mientras `cubrir_gastos`/`P14`
sigue colapsando ausencia y menos de una semana; además, la unidad es hogar,
la cobertura es Jalisco y el diseño es muestra aleatoria simple telefónica,
no persona adulta nacional con diseño ENIF. Se adquirió como evidencia
pertinente, pero no se registra como cobertura de NC-0126 ni habilita una
emisión.

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
