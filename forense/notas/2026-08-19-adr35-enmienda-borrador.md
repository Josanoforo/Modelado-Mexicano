# Enmienda propuesta a ADR-35 — BORRADOR, NO EJECUTADA

Producida por `ACTO REFUTACIONES-SIN-OBJETO` (`forense/encargos/2026-08-19-REFUTACIONES-SIN-OBJETO.md §3`), ejecutando la letra de `FP-56`/`ADR-110(a)`/`ADR-111(c)`: *"ADR-35 declara la frontera del prestamista"*. Este texto **no sella nada**: es el borrador que sube a mesa como punto de retorno de este acto. Referenciado desde `FP-61` (`forense/firmas-pendientes.tsv`).

## Por qué hace falta

`ref.A.04` ("los pobres no pagan") es `FUERTE` en `forense/corrida-refutaciones.md §3` y sigue **sin objeto**: el modelo no tiene entidad prestamista. `ADR-35` (28/jul/2026) declaró esa frontera explícitamente y a propósito:

> *"El motor **sigue sin entidad prestamista**. Modela al decisor. El hallazgo mejor sostenido del corpus sobre crédito —el riesgo vive en el fondeo y el gobierno corporativo del prestamista, no en el deudor— no se puede representar aquí, y su refutación sigue sin objeto. **Ampliar al lado de la oferta es una decisión distinta y mayor, que este ADR NO toma.**"*

Darle objeto a `ref.A.04` en el sentido que `FP-56`/`(a)` pide —ampliar el modelo, no retirar la refutación— exige exactamente la decisión que `ADR-35` nombró y dejó fuera. Este acto no la toma por su cuenta: sería el ejecutor resolviendo una pregunta que el propio ADR reservó a mesa.

## El texto de la enmienda, tal como se propone

**ADR-35(b) · Se amplía el alcance del motor al lado de la oferta de crédito, con entidad `prestamista`, para dar objeto a `ref.A.04`.**

Entra una entidad `prestamista` al espacio de atributos del motor, distinta del agente-decisor de §1.1.A, con al menos:

- `fondeo` — estructura de financiamiento de la entidad (deuda, capital, subsidio), variable declarada, sin forma funcional fijada aquí.
- `gobierno_corporativo` — proxy de supervisión/regulación de la entidad, variable declarada, sin forma funcional fijada aquí.
- `tasa_ofrecida` / `cat` — ya existe como parámetro del lado del decisor (§3.1, techo cuantificado de disposición a pagar, ADR-35 original); se declara aquí el enlace, sin duplicar el número.

**Lo que esta enmienda NO hace, si se sella tal cual:** no calibra `fondeo` ni `gobierno_corporativo` — quedan `[HIPÓTESIS]`, forma PENDIENTE, igual que las siete de `ADR-114`. No reabre las dos reglas de `§3.1` que `ADR-35` original ya selló del lado del decisor. No decide si `prestamista` entra a `D` (§1.1.F) — eso depende de si algún generador la multiplica, acto propio posterior.

**Lo que esta enmienda exige si se sella:** un mecanismo estructural nombrado y con fuente para cualquier diferencial que el `prestamista` introduzca (mismo criterio de §1.5, ADR-28.c), y un reactivo verificado antes de fijar forma funcional — no basta con declarar la entidad para que la refutación "pase"; corribles no es pasadas (mismo principio que `ADR-114` aplica a las otras siete).

## Las tres opciones que mesa tiene delante, sin aplanar

1. **Sellar esta enmienda tal cual** — `ref.A.04` gana objeto, con la misma disciplina de "declarar, no calibrar" que `ADR-114` aplicó a las otras siete.
2. **Sellar una versión acotada** — por ejemplo, solo `fondeo` sin `gobierno_corporativo`, o solo como modificador transversal del generador de crédito existente en vez de entidad propia — si mesa juzga que la entidad completa es alcance mayor de lo que este acto puede escalar sin más discusión.
3. **No sellar** y declarar el alcance del motor explícitamente acotado al decisor, con `ref.A.04` retirada de la batería por alcance declarado — la vía `(b)` que `MESA-19AGO` ya descartó por firma para las otras siete, pero que sigue disponible para ésta específicamente, porque `ADR-35` la frontera **ya la declaró antes** de que existiera la firma de `(a)`.

Ninguna de las tres se ejecuta aquí. La fila de tablero es `FP-61`.
