# ENCARGO · ACTO MESA-CONCILIACION-E01

**Fecha de la decisión:** 10 de septiembre de 2026.

**Autoridad:** mesa/dirección, mensaje externo recibido en la sesión que
ejecuta este acto. El merge de mesa perfecciona el asiento; este archivo no
autoriza un merge automático.

**Base declarada por dirección:** `e81aa27bf3999989fc029a18e49352f27088e230`,
posterior a PR #683, con PR #684 abierto.

**Base real al lanzamiento:** `002e7190bdacb6906345d422a49b8026b0a73107`,
merge de PR #684. La diferencia se incorpora: el diagnóstico L v1.4 ya es
canon y ENCARGO-E02 parte de él; ningún otro alcance de ENCARGO-E01 cambia.

**Worktree:** `/home/pc0/mm-mesa-conciliacion-e01`.

**Rama:** `acto/mesa-conciliacion-e01`.

**Entorno:** repo-only. Cero microdatos, cero llamadas a modelos y cero
descargas sustantivas.

## Instrucción de mesa que se registra

> Ok, sobre lo que no hay que decidir otra vez. Si necesitamos asentar algo
> en el repositorio necesitamos un encargo que lo asiente y lo deje cerrado
> con toda su cadena para evitar que otra revisión vuelva a traerlo sobre la
> mesa o siga apareciendo como decisión pendiente. D01 - Si vamos a hacer
> esto vamos a hacerlo bien, 3/14 no son nada, aunque si efectivamente no hay
> ganador no hay ganador, se dice y no pasa nada pero me parece que hay que
> correr lo faltante para identificar si existe ganador con las familias
> restantes. D02 - A. D03- No me preocupa tanto la nomenclatura o el indicador
> nuevo y medir solicitud sino como el motor usará estos elementos, si es
> necesario separarlos los separamos. D04 - Conservamos el cálculo anterior
> como historico pero ahora si lo hacemos bien, A/A. D05 A y B la celda
> adicional hace sentido sobre el universo poblacional. D06 - Nos vamos con
> A. D07 - A pero sin presupuesto limitado, vamos a darle. D08- A pero dejemos
> B para que sonda y cron de adquisición revisen si existe. D-09 - A. D10-A-
> D11- Benchmark web de como se manejan este tipo de datos, revisemos papers y
> edge cases. D12-Serie temporal pero si es porque no tenemos datos y los
> podemos conseguir los conseguimos. D13 - A. D14- B. D15 -A. D16- benchmark
> web como la anterior que haremos benchmark web. D17- Todo lo que sea
> obtención de datos las movemos, la idea es robustecer nuestro proceso de
> decisión y asignación correcta. D18- ahorita no invertiremos, lo dejamos en
> B, pero desbloquemos el encargo para búsqueda académica dirigida. D19 -
> Unifiquemos. D20- revisión historica te refieres a Gen1? o a datos más
> antiguos? Para candidatas de conciliación, necesitamos explorar más el
> repo? lo hacemos y decidimos.

Los identificadores D01–D21 son referencias locales de esta instrucción, no
una numeración global. D21 no recibió respuesta y no se inventa.

## Traducción operativa autorizada

| decisión | objeto | instrucción ejecutable | sucesor |
|---|---|---|---|
| D01 | NC-0146 | completar las familias restantes; una conclusión sin ganador es válida | ENCARGO-E02 → ENCARGO-E03 |
| D02 | NC-0147 | tolerancia numérica prospectiva separada del margen sustantivo | ENCARGO-E03 |
| D03 | NC-0137/0138/0139 | diseñar el uso del motor y separar solicitud/entrega cuando el proceso lo necesite | ENCARGO-E04 |
| D04 | NC-0124 | A/A: `P4_10 {1,2}` y seguridad social `{1..4}` frente a `{7}`, residual visible; histórico intacto | ENCARGO-E05 |
| D05 | NC-0128 | conservar dominio actual y añadir celda de no trabajadores | ENCARGO-E05 |
| D06 | NC-0127 | rótulo «desconfianza o mal servicio», con compatibilidad si hace falta | ENCARGO-E04 |
| D07 | NC-0107 | no adoptar tasas discrepantes; usar variantes validadas por unidad; sin límite presupuestario artificial | ENCARGO-E04 |
| D08 | NC-0111 | acotar el dato ENCIG actual y buscar una tasa general | ENCARGO-E04 + ENCARGO-E09 |
| D09 | NC-0105 | identidad y procedencia por conducta/ola | ENCARGO-E04 |
| D10 | NC-0121/0122 | aceptar el proxy descriptivo del canal del último producto entre personas con fintech | ENCARGO-E04 |
| D11 | NC-0085 | benchmark cumplido; reconstrucción acotada y propuesta concreta, sin adopción automática | ENCARGO-E11 |
| D12 | NC-0087/0093/0101 | completar la serie temporal y adquirir sólo insumos realmente faltantes | ENCARGO-E08 + ENCARGO-E09 |
| D13 | FP-361 | S6 sucesora documenta el join por hogar ya reparado | ENCARGO-E06 |
| D14 | FP-363 | S12 sucesora compara receptores de forma descriptiva/asociativa | ENCARGO-E07 |
| D15 | NC-0043 | conservar R10.3 histórica y declarar no evaluable la cláusula con las olas examinadas | ENCARGO-E06 |
| D16 | FP-371 | benchmark cumplido; recuperar diseño y formular recomendación sustentada | ENCARGO-E09 + ENCARGO-E11 |
| D17 | FP-314 y accesos | avanzar obtención, reutilizando solicitudes y verificando identidades | ENCARGO-E09 |
| D18 | FP-286/343 y tandas | diferir inversión comercial; habilitar búsqueda académica dirigida | ENCARGO-E09 |
| D19 | NC-0114/0115/0120 | unificar calendario, configuración y operación SONDA/adquisición | ENCARGO-E10 |
| D20 | NC-0041 | revisión acotada del fundamento temporal de PR #621 bajo RUTINAS-2 P1 | ENCARGO-E01 |

## Contrato común aplicable a ENCARGO-E01–ENCARGO-E11

- Un encargo, un worktree y una rama; `origin/main` es el estado consolidado
  y un PR abierto sólo es propuesta.
- Verificar identidad por objeto y texto, no sólo por número. Reutilizar
  evidencia compatible y preservar artefactos sellados.
- Decisión y ejecución son cierres distintos: quitar la pregunta ya resuelta,
  mantener la obligación de ejecución y su sucesor.
- Toda medición sucesora congela spec, entradas/hashes, unidad, universo,
  exclusiones y tratamiento de faltantes antes de mirar resultados.
- No alterar R o M históricos para favorecer un brazo. Las mejoras futuras no
  contaminan la evaluación congelada.
- Validación dirigida y gate vigente; los fallos heredados ajenos no amplían
  el perímetro.
- Entrega: resultado, archivos, pruebas, cierres y residuales. Push/PR conforme
  al encargo; merge exclusivamente de mesa.

## ENCARGO-E01 · Asiento y conciliación

### Resultado

Las decisiones D01–D20 dejan de aparecer como preguntas sin respuesta; los
trabajos no ejecutados continúan como obligaciones explícitas ENCARGO-E02–ENCARGO-E11. Las
candidatas históricas se cierran sólo cuando su objeto exacto está acreditado.

### Perímetro

`forense/no-corrido.tsv`, `forense/firmas-pendientes.tsv`,
`data/corrida0/decisiones.tsv`, este A.3, los dos benchmarks, nota de cierre,
digesto derivado, rótulo, ADR y L0. `tools/digesto_tramite.py` sólo se cambia si
se reproduce un defecto material que el mecanismo vigente no cubra.

### Conciliaciones autorizadas por evidencia

- FP-234: F-DD v1.1 fue ejecutada por MAESTRA35-N2 y la reserva quedó levantada
  para DIN-M-01 por `d2`; cerrar con ese alcance.
- NC-0018: los 14 CALC-R vigentes existen; cerrar depósito/corrida, no adopción
  al motor.
- NC-0019: el corredor sucesor v1.3 corrió 224 posiciones; cerrar la obligación
  histórica sin decir que v1.2 corrió. NC-0146 conserva el problema científico.
- NC-0063/0071: `CALC-0003-v4 cuenta_gen2=SI` ya está en decisiones.
- NC-0095: codificación R tiene sucesora sellada por FP-370.
- NC-0092/0102: cerrar sólo el uso de R por identidad en CALC-TRIADA-0001; no
  inferir adopción al motor.
- NC-0040: las huellas reales marcadas y los PR `[REVISA]` de
  `forense/rutinas.tsv` acreditan la consulta exigida.
- NC-0032: publicaciones reales en días distintos se acreditan por los commits
  `f0f6bb7` (9/sep) y `fe5d131` (10/sep); no se inventa continuidad diaria.
- NC-0067: T-YAMEDIDO usa UTC y tiene fixture de cambio de día.
- NC-0103: transcribir la firma exacta de las specs CIV-M-01/02/04 a
  `decisiones.tsv`, y sólo después cerrar.
- NC-0132: ADR-441 y su rótulo están reconciliados en canon.
- NC-0041: conservar el veredicto histórico de #621; registrar que su razón
  temporal común no basta bajo RUTINAS-2 P1. Una huella se juzga en su SHA;
  una compuerta vigente se rederiva antes de actuar. No reabrir PR #619/#621.

NC-0029 y NC-0104 conservan sus residuales. FP-324/328/332 y NC-0037 no se
cierran en bloque. Las ejecuciones de FP-361/363 siguen en NC-0065/0064, sin
duplicarlas. NC-0140 y NC-0145 ya estaban cerradas y sólo se citan.

### Benchmarks externos

Se archivan como anexos operativos, sin convertirlos en firma de adopción. La
identidad de los originales entregados por dirección queda acreditada por hash:

- `forense/notas/BENCHMARK-D11-COMPLEMENTOS-Y-USO-EN-MOTOR.md`; original
  `sha256 cfd7fd8dc426612e55c5c6887b4da4cca2d8a99221188b9e254a0aa9657a0cbf`.
- `forense/notas/BENCHMARK-D16-DISENO-MUESTRAL-E-INCERTIDUMBRE.md`; original
  `sha256 9cb2aaab01aab9abb3222ec0c67ad9fae3aec1f3e97059361b4e8199ff34dac9`.

### A.8 · consulta de medición para R10.3

La consulta dirigida se ejecutó antes del cierre administrativo:

```text
$ python3 tools/ya_medido.py R10.3
=== ya_medido: R10.3 ===
resuelto por canon: R10.3 -> id `comunicacion.inseguridad.ver_oir_callar`
MEDIDA-EN: L18, tramite-ola5-propuesta-v0.yaml
```

Esto acredita la medición histórica que se conserva. No demuestra que la
cláusula sucesora sea evaluable con LAPOP 2019/2021/2023; ese alcance continúa
en `NC-0043`/`ENCARGO-E06`.

## NO-CORRIDO / RESERVAS

- ENCARGO-E02–ENCARGO-E11 no se ejecutan en este acto. Quedan autorizados y con los sucesores
  identificados en `forense/no-corrido.tsv` y la nota de cierre.
- No se abren microdatos, no se llama a modelos, no se compra información, no
  se toca el scheduler real y no se modifican consumidores del motor.
- D21 sigue sin decisión. Una cosecha F6 definitiva requiere evidencia futura;
  este acto no proclama ganador.

---

## CONSUMIDO

PR #685, rama `acto/mesa-conciliacion-e01`, primer commit `9e45c45`.

Resultado: D01–D20 asentadas; D21 no inventada; catorce NC cerradas por
evidencia exacta; FP-234 ejecutada; FP-314/361/363 firmadas con sus ejecuciones
visibles en NC-0151/0065/0064; FP-371 permanece abierta. El universo termina en
69 NC abiertas y 75 cerradas. Los originales D11/D16 se archivan íntegros y
conservan los hashes declarados arriba.

Validación: pruebas dirigidas del digesto/estado en verde;
`tests/check.py --baseline` VERDE, sin entradas nuevas frente al baseline;
`git diff --check` limpio; `cierre_acto.py --sin-suite` reconcilia 454 ADR,
una FP abierta, rótulo presente y cero NC huérfanas. La vista de mesa presenta
NC-0103 y FP-361 como ya resueltas y no vuelve a pedirlas.

No se ejecutó ENCARGO-E02–ENCARGO-E11, no se fusionó el PR y no se aplicó la
derivación global de `corridas.tsv`: su dry-run mostró 35 transiciones de replay
y no sustituye la evidencia efectiva que conserva abierta NC-0104.
