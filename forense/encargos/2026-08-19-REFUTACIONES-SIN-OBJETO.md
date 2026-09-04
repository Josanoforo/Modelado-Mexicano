# ENCARGO · ACTO REFUTACIONES-SIN-OBJETO — ejecutar la letra de D-3 sobre las ocho sin objeto

SHA de redacción: derivar al lanzar (escrito el 18/ago/2026 por `ACTO MESA-19AGO`). Entorno asignado: **NUBE** (repo-only). Estado: **CONSUMIDO** — `ADR-117`, `PR #283`, 19/ago/2026. Origen: firma de mesa D-3 de `MESA-19AGO`, `ADR-110(a)`/`ADR-111(c)` (renumerado al fusionar), fila `FP-56`.

**Ejecutado así, verbatim contra lo firmado:** siete de las ocho refutaciones (todas salvo `ref.A.04`) ganan variable declarada, sin calibrar, en `canon/modelo-decision-v4_0.md §1.1.G` (`ADR-117`). `ref.A.04` sigue sin objeto: exige entidad `prestamista`, que choca con la frontera declarada de `ADR-35`; la enmienda queda redactada y no ejecutada (`forense/notas/2026-08-19-adr35-enmienda-borrador.md`), subida a mesa como `FP-61`. Denominador re-derivado (no anunciado) y propagado a `milpa/refutations.yaml`, `forense/corrida-refutaciones.md`, `canon/estado-programa-v1_10.md`, `canon/glosario-v5_6.md`, `canon/gobernanza-v1_15.md §5` y `README.md:87`. `FP-56`: `FIRMADA` → `CERRADA`.

## 1 · Lo que la mesa firmó (verbatim)

D-3: **`(a) Añadir variables`** — *"Ampliar el modelo (esfuerzo/horas, salud mental, colorismo, prestamista, emprendimiento, canal, religiosidad, ítem actitudinal) para darles objeto. Acto mayor; ADR-35 declara la frontera del prestamista."*

⚠️ Registro de la deliberación, para que no se lea como una sola pasada: en la primera presentación del prompt la mesa marcó `(c) Partir`; en la re-presentación del widget, pedida por la propia mesa, marcó **`(a)`**. **Rige `(a)`** — la última. Ambas quedan en el acta.

## 2 · Los ocho ids, con lo que a cada uno le falta

Enumerados en `forense/corrida-refutaciones.md §3` (la fuente canónica más citada — `estado`, `gobernanza` — nunca los enumera, solo menciona `ref.A.02`; deuda de completitud señalada por `censo-integridad-v1_0.md` C4-05):

| id | tier | qué falta en el modelo |
|---|---|---|
| `ref.A.02` esfuerzo laboral | **MUY_FUERTE** (la única de las 49) | no hay variable de esfuerzo ni de horas; cero reglas |
| `ref.A.04` pobres no pagan | FUERTE | no existe la entidad prestamista (**frontera declarada de ADR-35**) |
| `ref.A.14` no cree en terapia | FUERTE | no hay dominio de salud mental |
| `ref.A.20` emprendimiento vibrante | MEDIA | sin variable de emprendimiento |
| `ref.A.28` e-commerce transformador | MEDIA | sin canal de compra |
| `ref.B.04` colorismo estructural | FUERTE | el tono de piel no es parámetro de ninguno de los seis perfiles |
| `ref.B.06` fatalismo no es religioso | FUERTE | sin parámetro de religiosidad |
| `ref.A.17` líder fuerte ≠ autoritarismo | MEDIA | parcial: §3.2 distingue liderazgo benévolo de autoritario, sin ítem actitudinal |

## 3 · Qué hace este acto

Ejecuta **la letra exacta de `(a)`**: dar objeto, no retirar. Cero retiros con acta — la vía (b) quedó descartada por firma.

1. **Filas de constructo nuevas**, una por hueco, con tier y base declarados o con el hueco de evidencia dicho: esfuerzo/horas, salud mental, colorismo, entidad prestamista, emprendimiento, canal de compra, religiosidad, ítem actitudinal de deferencia a la autoridad.
2. **`ref.A.02` primero.** Es la única `MUY_FUERTE` de la batería, con el dato más contundente del corpus (2,207 h/año, el mayor de la OCDE, 26% sobre el promedio; la baja productividad es déficit de capital, no de esfuerzo) y es la refutación del mito más dañino que existe sobre México. Que no tenga dónde alojarse es el hallazgo, no un detalle de esquema.
3. **`ref.A.04` choca con `ADR-35`, y eso se resuelve por ADR, no por sigilo.** La frontera «el motor modela al decisor, no al oferente» está declarada y vigente (`gobernanza:253`, `glosario:410`, `estado:128`). Darle objeto a `ref.A.04` **exige ampliar al lado de la oferta**, que el propio ADR-35 nombra como *"una decisión distinta y mayor, que este ADR NO toma"*. Este acto **no la toma por su cuenta**: la sube a mesa como su único punto de retorno, con la enmienda a ADR-35 redactada y sin ejecutar.
4. **El denominador se re-deriva, no se anuncia.** Hoy la batería reporta 49 pruebas de las que 8 son inejecutables por construcción y 11 esperan simulador: *"27 de 49 pasan"* es en realidad **27 de 30**. Al ampliar, las ocho pasan de *sin objeto* a *corribles* — y **corribles no es pasadas**: cada una vuelve a la batería con su veredicto pendiente, y el número honesto es el que resulte de correrlas, no el que suene mejor.
5. Propaga el número derivado a los sitios que hoy lo citan: `milpa/refutations.yaml` (`primera_corrida.resultados`, `ocho_sin_objeto`, `lectura_honesta`), `forense/corrida-refutaciones.md`, `canon/estado-programa` (L5 y §deuda), `canon/gobernanza-v1_15.md §5` fila *"Ocho refutaciones sin objeto ⭐"* — abierta desde antes de que el tablero A.12 existiera, y `README.md:87` (S2).

## 4 · Lo que NO hace

No retira ninguna refutación (la vía (b) está descartada por firma) · no corre la batería ampliada (eso es acto propio, con su pre-registro) · **no ejecuta la enmienda a ADR-35**: la redacta y la sube · no calibra ningún parámetro nuevo: darle objeto a una refutación es que exista la variable, no que esté medida.

## INDETERMINADO

Derivado por auditoría 2026-09-03 (ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166). `grep -Fn -- "2026-08-19-REFUTACIONES-SIN-OBJETO.md" canon/gobernanza-v1_15.md` cita ADR-110, ADR-117, pero el bloque mezcla lenguaje de ejecución y de encargo pendiente (o el rótulo del ADR es compartido entre varios encargos sin desenlace individual claro) — rastro parcial, no se decide aquí. Para mesa: verificar manualmente contra ADR-110, ADR-117 en canon/gobernanza-v1_15.md.

## CERRADO-POR-HISTORIA

Regla mecánica (b) de la resolución de mesa sobre FP-290 (2026-09-04):
sin hermano de rótulo compartido con desenlace ya sellado (regla a no
aplicó -- ver tabla en forense/notas/2026-09-03-MAESTRA37-N9-auditoria-encargos.md,
enmienda 2026-09-04), este encargo queda cerrado por antigüedad e
inacción declarada, no por evidencia positiva de ejecución o
sustitución. Si aparece evidencia nueva, esta marca se reabre -- no es
`## CONSUMIDO`.
