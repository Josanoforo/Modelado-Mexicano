# `GEN2-F5-CONTRATO-TRIADA` — nota de decisión

**Fecha:** 10/sep/2026 · **Entorno:** NUBE, cero microdato/cero captura/cero
cálculo de errores finales · **Base:** `origin/main = eab46ed` (`PR #674`
fusionado) · **Encargo:** `forense/encargos/2026-09-10-GEN2-F5-CONTRATO-TRIADA.md`
(A.3, verbatim) · **Producto:** `forense/prereg-duelo-v2/F5-contrato-triada-spec-v1_0.md`
+ `forense/prereg-duelo-v2/universo-triada-v1_0.tsv`.

---

## 1 · Qué decide esta firma de mesa, en una frase

Para el siguiente duelo, la pregunta que el contrato debe poder adjudicar
deja de ser "¿transfiere `L_CORPUS` mejor que `L_SOLO` bajo corte
temporal?" y pasa a ser **"en el mismo panel y contra el mismo árbitro,
¿cuál de los tres — `L_SOLO`, `L_CORPUS`, `M` — rinde mejor?"** —
transferencia queda secundaria, no eliminada. Esta nota documenta por qué
eso es una firma nueva y no una edición de la spec histórica, y qué
insumos quedaron pendientes al congelar el contrato.

## 2 · Por qué spec sucesora, no enmienda

`F5-duelo-contemporaneo-spec-v1_0.md` es COMMIT-1 de `ACTO
GEN2-F5-RECAPTURA-L` — congeló el contrato **antes de capturar** las 224
invocaciones, y ese acto de congelamiento-antes-de-capturar es
irreversible por construcción: las capturas ya existen, selladas, bajo
esa spec. Reescribirla para cambiar la pregunta primaria sería alterar,
retroactivamente, el contrato bajo el cual un dato ya se produjo — exacto
el defecto que la disciplina de specs pre-registradas de este programa
existe para prevenir. La firma de mesa lo dice explícitamente: *"no
reescribe la spec histórica F5 v1.0; nace una spec sucesora."* El nuevo
documento (`F5-contrato-triada-spec-v1_0.md`) reutiliza sin reescribir
todo lo que sigue siendo válido bajo la nueva pregunta (universo de
captura, `k=8`, agregación por mediana, aparato de bootstrap, banda
numérica `δ=0.5`) y solo cambia lo que la firma de mesa cambia: el orden
de preguntas, el tercer contendiente, la unidad de la métrica (pp en vez
de `z`), y las reglas de contaminación/cobertura explícitas para tres
contendientes en vez de dos.

## 3 · Lo que este acto SÍ derivó hoy

- **`U0`** — las 14 celdas del marco, fijas.
- **`UR`** — 6/14 celdas con árbitro `R` sellado
  (`CIV-M-01/02/04/10/12/13`), por censo directo de
  `data/corrida0/CALC-R-CIV-M-*/`. Las 8 restantes no tienen `R`
  calculado — ausencia de insumo, no descarte de juicio.
- **Verificación de contaminación de la ruta obvia** (calibración directa
  del motor) sobre las 6 celdas de `UR`: `M` calibra
  `civico.denuncia.miedo_desconfianza` de `envipe2025_csv`; `R` de cada
  celda lee el `Tmod_Vic.DBF` de su propia ola (2012–2024) — objetos
  distintos, y la propia regla del motor (`milpa/tramite.yaml:488`)
  declara por escrito que los dos números no son comparables. **Hallazgo:
  las 6 celdas de `UR` no muestran contaminación por esta vía**, con la
  salvedad explícita de que esta verificación se repite contra el
  snapshot real de `M` (`ENCARGO 4/5`) antes de aceptar cada celda en
  `U3` — no se hereda de este censo por default.
- **La regla completa y ejecutable de `U3`**, incluida la condición de
  contaminación, aunque su membresía final no se puede cerrar hoy (§4).
- **El techo de `U3`**: `|U3| ≤ |UR| = 6` — ninguna de las 8 celdas sin
  árbitro puede entrar bajo ninguna circunstancia futura; eso ya queda
  cerrado en este commit.
- **La secundaria de transferencia bajo `M`**: aplicando la misma regla
  mecánica de corte que la primaria de `F5 v1.0` §2 usa para documentos,
  las 6 celdas de `UR` (y de hecho `FAM-M-05/06/07` y `TRA-M-03/07`)
  calibran `M` de una ola **posterior** a la que evalúan
  (`ENVIPE 2025`/`ENIGH 2022`/`ENCIG 2025`) — bajo la regla del contrato,
  las 6 celdas de `UR` quedarían `M-NO-COMPARABLE-EN-TRANSFERENCIA` si un
  sucesor ejecutara la secundaria hoy con la calibración de `M` que existe
  actualmente. Esto es un dato citado, no una predicción.

## 4 · Lo que este acto NO pudo cerrar, y por qué (no es omisión silenciosa)

`U3` no tiene membresía final porque dos de sus tres condiciones de
entrada dependen de insumos que este mismo lote de encargos aún no
produce:

1. **Extractor de `valor_extraido` validado para el formato real de
   `corridas-L/*__v1_3.json`.** `NC-0142` (abierta por `ACTO
   GEN2-F5-DUELO-CALC`, `PR #674`) ya midió que el único extractor
   existente (`tools/extrae_l_v1_1.py`) produce contaminación medida
   (0/96 capturas reales traen el encabezado que busca; su *fallback*
   capturó cifras que el propio modelo declaró explícitamente que no
   eran la estimación pedida). Mientras `NC-0142` siga abierta, ninguna
   celda tiene "punto válido" de `L_SOLO`/`L_CORPUS` bajo la regla de
   este contrato.
2. **Snapshot sellado de `M` de `ACTO GEN2-ENCARGO-4/5`.** No ejecutado
   al momento de este commit — es sucesor nombrado por el propio encargo
   de este acto.

Esta nota, junto con `## NO-CORRIDO / RESERVAS` del encargo archivado, es
la declaración explícita de ese hueco — no un silencio que un lector
tendría que inferir. El precedente que esta acta sigue es el mismo de
`ACTO GEN2-F5-DUELO-CALC` (`NC-0142`): calcular y congelar el
procedimiento hasta donde el insumo alcanza, declarar el resto como
sucesor citado, y no inventar un atajo (un extractor improvisado, un
snapshot de `M` sustituto) para cerrar el número hoy.

## 5 · Consistencia con `PLAN-DE-OBRA-GEN2-v1_1`

`PLAN-DE-OBRA-GEN2-v1_1` §2 F5 exige que "mesa elige antes de capturar
cuál pregunta se contesta... y las dos no se mezclan en una afirmación
única" — la elección original (transferencia primaria) ya se hizo antes
de capturar (`F5 v1.0`, COMMIT-1 de `RECAPTURA-L`) y las 224 capturas ya
existen bajo esa elección. Esta firma de mesa no reabre esa elección de
captura — reordena qué **pregunta de análisis** se responde primero sobre
el mismo dato ya capturado, lo cual es exactamente lo que una spec
sucesora (no una enmienda) está para hacer sin violar la regla de "elegir
antes de capturar": no se está recapturando nada, y la pregunta de
transferencia sigue disponible, ahora como secundaria, sin haberse
mezclado nunca con la primaria en una sola afirmación.

## 6 · Sucesores

- `ENCARGO 3/5` y `ENCARGO 4/5` — el segundo produce el snapshot de `M`
  que cierra la segunda condición pendiente de `U3`.
- El acto que resuelva `NC-0142` (extractor validado) — prerrequisito de
  la primera condición pendiente.
- `ENCARGO 5/5` — presumible ejecutor de P2 bajo este contrato, una vez
  que los dos insumos de arriba existan.
