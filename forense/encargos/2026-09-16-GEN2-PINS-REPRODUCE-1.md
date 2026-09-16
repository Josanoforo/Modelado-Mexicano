# ENCARGO · ACTO GEN2-PINS-REPRODUCE-1

**Archivado verbatim (0-bis A.3).** Llegó como descripción de tarea de la
sesión de NUBE del 16/sep/2026, sin encargo previo commiteado en
`forense/encargos/` (convención violada por el origen del texto, no por
este acto — este commit la resuelve). No se edita: lo que este acto midió
contra él, incluidas las cifras que no reconciliaron contra el árbol vivo,
va en la nota de cierre, no aquí.

---

NUBE · ACTO GEN2-PINS-REPRODUCE-1 (Sonnet; materializar los pines REPRODUCE en el registro)

•	P1 · Materializar los 11 pins REPRODUCE en el registro con el escritor canónico (decisiones, cita corrida0_* en el consumidor, usos con verbo de enlace explícito): son bin 1 por la regla de bloque; tu merge del PR los adopta — sin firma individual.
	•	P2 · Los otros 78 slots con oferta (los 89 menos los 11): bin por slot con delta por script; bin 1 al PR, bin 2 a tu lista con delta, bin 3 en bloque con tabla.
	•	P3 · Los 118 sin oferta — el diagnóstico que falta: para cada uno, su corrida natural, si existe spec para ella, y por qué las 80 selladas no la cubren (estimando distinto, universo distinto, nombre distinto). Entregable: la demanda real de medición, derivada, que es lo que MEDICION-DEMANDA-3 debe correr — hoy nadie lo sabe.
	•	Contador: es el único acto que puede mover 207, 189 y 18 a la vez. Perímetro: registro derivado vía escritor, decisiones, milpa citas (solo bin 1), nota. Concurrencia: F6-PANEL-CAJA-1 (caja, panel — sin archivo común).

## NO-CORRIDO / RESERVAS

Cuatro piezas no ejecutadas o parciales, cada una con su fila `NC`. Detalle
completo en `forense/notas/2026-09-16-GEN2-PINS-REPRODUCE-1-cierre.md`.

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| Citar en `milpa/tramite.yaml` los 3 slots restantes del bloque `REPRODUCE` (`RES-0050/0051/0052`, `participa_p0_minimo/maximo/media`, `CALC-L8-CONVERSION-0001`) | `PARO-PREMISA` — `corrida0.py status` para con `USO-NO-APTO`: el único insumo de esa `CALC` (`data/l8-resultados-tipo-boleta-v1_0.json`) no está en el whitelist mecánico de linaje de `tools/corrida0.py`, y `milpa/src/linaje.py` niega aptitud a todo `MEDICION-GEN2` con origen `INDETERMINADO`. Reproducido en árbol limpio, no es efecto de este acto; corregirlo excede el perímetro (ampliar el whitelist o editar el `spec.yaml` sellado) | `dependencias_numericas_legacy_activas` se queda en 183 en vez de 180; `RES-0050/0051/0052` siguen `LISTADO-PARA-MESA-REPRODUCE` sin cita, pese a que su `CALC` ya reproduce GEN1 exacto | `NC-0253` |
| Disposición de mesa sobre `RES-0043`/`RES-0044` (`CALC-EDER-0003`, `NO-APLICA-ESTIMANDO-DISTINTO`) | `DECISIÓN-DE-MESA-PENDIENTE` — no son bin 1; `milpa/` ya los cita como eje de corroboración, no de reemplazo | `RES-0043/0044` siguen `LISTADO-PARA-MESA` (bare) hasta que mesa decida | `NC-0254` |
| P2 del encargo — bin 1/2/3 sobre "los 78 slots con oferta (89 menos los 11)" | `PARO-PREMISA` — "89"/"11" son la cifra de `RELEVO-USOS-1` sobre 23/82 corridas selladas; hoy son 80/82 y ninguna combinación de las categorías vivas de `data/corrida0/relevo-usos-v1_0.tsv` (`YA-ADOPTADO=22 · LISTADO-PARA-MESA=9 · CANDIDATO-GEN2=12 · NO-ADOPTABLE-POR-VEREDICTO-SELLADO=8 · CONFLICTO-ENTRE-CANALES=2 · VETADO-POR-DECISION=1 · SIN-CANDIDATO=153`) reconstruye 89 ni 78 | los 12 `CANDIDATO-GEN2` (el análogo vivo más cercano) siguen sin delta por script ni bin | `NC-0255` |
| P3 del encargo — diagnóstico de "los 118 sin oferta" y la demanda real que `MEDICION-DEMANDA-3` debe correr | `DECISIÓN-DE-MESA-PENDIENTE` — hoy son 153 `SIN-CANDIDATO`, no 118; `MEDICION-DEMANDA-3` ya tiene alcance reservado (y mucho más chico) por la ENMIENDA FECHADA de `GEN2-SPECS-DEMANDA-1` — ejecutar P3 tal cual lo redefiniría sin que mesa lo decidiera | la demanda real de medición para los 153 slots sin oferta sigue sin diagnosticar | `NC-0256` |
