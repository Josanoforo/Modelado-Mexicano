> **NOTA DE INCORPORACIÓN · 12/ago/2026.** Documento de mesa del 12/ago, base de ADR-70. Redactado en el hilo de dirección y nunca commiteado — el propio acto que lo ejecutó lo halló ausente (ADR-70(e) primera versión). Entra verbatim por CABLEADO-100. No se edita.

# PROPUESTA · Remediación de la brecha documental — "el conocimiento que no sube"
### v0.1 · 12/ago/2026 · propuesta sin sello; mesa aprueba lanzando los dos encargos adjuntos o los enmienda

| | |
|---|---|
| **EL DEFECTO, NOMBRADO** | Conocimiento que el programa YA tiene muere antes de llegar al punto donde se usa. Quince sesiones de mordidas, misma clase: la restricción de red falsa que moldeó meses de diseño (nadie la sondeó) · el 5/5 RESPONDE sobre fuentes "sin payload" (4/ago) · las 17 condiciones "no existe" de segunda mano (v2.6) · mi hallazgo ENUT con conclusión más ancha que su universo (10/ago) · ENSAFI/ENFIH "formato no verificado" en el inventario cuando el registro las tenía íntegras · ADR-52A/54 cerrados sobre un régimen de 5 instrumentos en un universo de 958 programas · y el caso que lo destiló: **ENASIC `NO_DETERMINADO` con el dato publicado en una ficha RNM que `explora1` había documentado como navegable cinco días antes** — el acto hizo todo bien salvo saber que había un tercer sitio |
| **LA CAUSA RAÍZ** | No es rigor insuficiente — es que el conocimiento no tiene un **conducto obligatorio**. Para usarse, un descubrimiento debe pasar por cuatro estaciones: **(1) exploración** (nota de acto) → **(2) tabla consolidada** (universo-puertas / activos T0) → **(3) receta** (paso obligatorio de la especificación) → **(4) contrato del motor** (campo que `validate` exige). ENASIC murió entre 1 y 2 (la RNM está 4 veces en `exploracion-puertas-2026-08-07.tsv` y **0 en `universo-puertas-2026-08-08.tsv`** — verificado 12/ago); la restricción de red murió antes de 1; el hallazgo ENUT murió en la declaración de universo. Cada mordida es una estación sin conducto |
| **QUÉ PROPONE** | Instrumentar las cuatro estaciones con lo MÍNIMO que las conecta — dos piezas de dato, un campo de esquema, una regla de cierre de acto — y usarlas de inmediato en tres actos que cierran la brecha sobre lo ya calculado. Nada de capa nueva, nada de auditoría recurrente |

## 1 · Las cuatro piezas de la estructura
**P1 · La RNM entra a la tabla consolidada de puertas** *(data-only)*. **P2 · Las fichas RNM de las fuentes activas entran como ACTIVOS del universo T0** *(data-only, maquinaria existente; alcance: solo fuentes con producción, ficha de Hito D o celda-D viva)*. **P3 · Un campo, no una capa: `documentacion_fuente`** en el contrato de producción, con validación del motor — el enforcement. **P4 · La regla de conducto:** toda nota de exploración que descubra una puerta, capacidad o restricción cierra su acto subiendo la fila a la tabla consolidada — o declarando en una línea por qué no.

## 2 · Los tres actos que usan la estructura
**U1 · E4b′** — re-corrida con el periodo de la ficha 922 → primera θ de `familismo_obligacion`. **U2 · EV-1** — indicadores oficiales de precisión (CV/EE/IC) descargados con sha256 y cruce oficial-vs-propio pre-registrado → primera validación externa. **U3 · DOC-BACKFILL** — las cuatro preguntas del transfer sobre las fuentes que sostienen celdas vivas, acotado por compuerta.

## 3 · Falsador y caducidad (v2.3)
**Métrica**: por producción, campos críticos resueltos por documentación oficial citada vs. inferidos — derivable del campo con un grep. **Falsador declarado**: si en los próximos tres meses aparece un `NO_DETERMINADO` cuya respuesta estaba en una puerta ya consolidada, la estructura falló y se rediseña. **Caducidad**: si en tres meses el campo no evitó ni un defecto ni resolvió un dato, P3-P4 se retiran y se anota — la regla de señal manda sobre esta propuesta como sobre todo lo demás.

## 4 · Qué NO hace
No audita cierres negativos históricos en bloque (30/jul). No añade capa a `relaciones.tsv`. No toca el piloto celda-D ni las ramas vivas. No promete que el universo completo vuelva todo calculable — las filas 10 y 14 del censo siguen siendo estructurales.
