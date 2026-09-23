# ENCARGO · ACTO GEN2-DIN-CREDITO-CELDAS-D-2 · Crédito 2024 entra a `celdas_validadas` con la unidad correcta: una celda-D por conducta adjudicada en `CALC-DIN-CREDITO-PREDICCION-2024-ESCOLARIDAD-0002`, con sus 16 celdas del eje como puntuadas y el -0001 citado como oro

> ENTORNO: **NUBE** — solo RESULT sellados y yaml de registro. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción `ae19a710` (re-deriva al abrir; main movido no es PARO) · una sola sesión, rama propia `acto/gen2-din-credito-celdas-d-2` (D-17) · MODELO: Sonnet · MODO: ABIERTO · ids con raíz de acto (D-24) · perímetro de cierre permanente (D-21) aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` al pie; adendas como `<este-encargo>-ADENDA-N.md`.
CONTADOR: cero corridas; `celdas_validadas` sube por derivación (una por celda-D nueva; el número lo da la lectura del -0002, no se teclea); no adopta (los champions son los que el CALC dictaminó).

## 1 · OBJETIVO
Corregir la premisa que paró a `GEN2-DIN-CREDITO-CELDAS-D-1` (#1047, NC `…e6b2-01`): la fuente que adjudica es el **-0002** (`tipo: ADJUDICACION-GUARDADA-RESERVA`, `sucede_eje_de: -0001`), sus veredictos son por **conducta × candidato** agregando las 16 celdas del eje, y el vocabulario alcanzable es `NADIE-VENCE · PROPUESTA-CON-RESERVA · NO-ADJUDICABLE · NO-CONSTRUIBLE-SIN-RETADOR-HABILITADO` (`spec.yaml:60-63`, `umbral_vence_pp: inf`). Registrar una celda-D por conducta con dictamen, como el piloto 4 registró una por cruce.
«Hecho»: `ls data/curacion-registro/celdas-d/ | grep -c '^DIN\.'` = número de conductas con dictamen en el -0002 (léelo; la nota de COMMIT-2-3 tabula K1, K2-DEPARTAMENTAL, K2-NÓMINA, K2-AUTOMOTRIZ, K3 … — cita la tabla completa) · `status` sube en exactamente ese número · cada yaml cita RESULT del -0002 por id y hash y al -0001 como oro por hash · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA
D3 (23/sep, verbatim «Que cuenten.», asentada por FIRMAS-11). **Propuesta de firma para la unidad (mesa la da verbatim al lanzar o la cambia):** «Crédito 2024 entra a celdas_validadas con una celda-D por conducta adjudicada en CALC-DIN-CREDITO-PREDICCION-2024-ESCOLARIDAD-0002, con las 16 celdas del eje como puntuadas; el -0001 se cita como oro. El dictamen de cada celda-D es el del CALC; PROPUESTA-CON-RESERVA no adopta al retador.» Sin esta firma: §7 f.

## 3 · LO QUE DIRECCIÓN SABE
- `[EJECUTADO]` `spec.yaml` del -0002: l.8 tipo; l.13 sucede al -0001 en el eje escolaridad; l.60-63 umbrales y vocabulario. Nota `forense/notas/nota-2026-09-22-gen2-din-credito-prediccion-2024-commit-2-3.md:52-56`: K1 TENDENCIA-SERIE `PROPUESTA-CON-RESERVA` ΔMAE +1.90 [+0.62, +2.65]; K2-DEPARTAMENTAL, K2-NÓMINA, K2-AUTOMOTRIZ, K3 `NADIE-VENCE`. `[EJECUTADO]` `resultados.json` del -0002: 1 346 RESULT, 406 con `ADJ16` (ΔMAE, IC, MAE persistencia, n celdas por conducta).
- `[LEÍDO]` NC `…CELDAS-D-1-e6b2-01` (#1047): «-0001 tiene 882 RESULT y cero veredictos; los 28 veredictos del -0002 están agregados por conducta × candidato (7 conductas)». Los «7» y «28» los verificas tú por lector JSON con conteo.
- `[LEÍDO]` Convención vigente: el piloto 4 (#1036) registró 4 celdas-D para 4 cruces con 38 celdas puntuadas (`celdas-d/` pasó de 6 a 10). Misma unidad aquí: una por conducta.
- `[EXISTE]` `tools/celdas_validadas.py:197` `_celdas_validadas` (clase CRUCE lee marcador + `margen_material` del yaml; clase PERSIST). **Cita las líneas que decidan si una celda-D de crédito cuenta y por qué clase; si ninguna clase la admite, es NC a TUBERÍA con la línea, no un parche.**
- ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
#1047 no escribió yaml (PARO). `ls celdas-d | grep -ci DIN` → 0. `git ls-remote --heads origin | grep celdas-d` → reporta.

## 5 · PIEZAS
- **P1 · Tabla fuente.** Por lector JSON: conducta → candidato → dictamen → ΔMAE, IC, MAE piso, n celdas elegibles/puntuadas, ids de RESULT. Va en la nota antes del primer yaml. Conductas sin dictamen (NO-ADJUDICABLE / NO-CONSTRUIBLE): se registran igual, con ese dictamen — el silencio no es un valor (E.5).
- **P2 · Yaml por conducta.** Esquema de las celdas-D del piloto 4; estimando (marginal ENIF 2024, persona 18–70, [0,1]); emisión = RESULT del -0002 (y de `…EMISIONES-0001` si la spec lo cita) por id/hash; R = -0001 por hash; dictamen verbatim del CALC; marcador PROSPECTIVA o RETROSPECTIVA-MECÁNICA según el orden de sellos (§3: `exposicion_historica: ENIF-2024-CREDITO-YA-ABIERTA-POR-0001` — léelo y decide con cita; no se colapsa); `champion_actual` = C2 piso (nadie venció; K1 con reserva no adopta); `registrado_por: GEN2-DIN-CREDITO-CELDAS-D-2`.
- **P3 · Derivación, test, cierre.** `status` antes/después; test huérfano (RESULT citados existen); cerrar `…CELDAS-D-1-e6b2-01` y `…ESCOLARIDAD-2-0af9-02` con `DECISIÓN-DADA` y este acto.

## 6 · LATITUD
Formato libre dentro del esquema. Pregunta a mesa (sigues): si `_celdas_validadas` no admite la clase y hay que decidir entre extender el contador (TUBERÍA) o registrar sin contar.

## 7 · PAROS — lista cerrada
a) no aplica · b) editar un CALC, un yaml ajeno o `marcador-segmento.tsv` a mano · c) cambiar `champion_actual` respecto al dictamen, adoptar · d) no aplica · e) CAJA · f) mesa no dio la firma de unidad, o las celdas-D ya existen.

## 8 · COMPUERTAS
«Tabla fuente por lector JSON antes del primer yaml» protege: **adoptar** (métrica rectora). «Dictamen verbatim del CALC; `champion_actual` = piso» protege: **adoptar**.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `data/curacion-registro/celdas-d/DIN.*.yaml`, test propio, `no-corrido.tsv` (append/estado), nota, L0, cascada. Ajeno: CALC, marcador, `tools/celdas_validadas.py`. En vuelo: ASTRA-ENVIPE-ADJUDICACION-1 (toca celdas-D del piloto 4), CANAL-REPARACION-1, MOTOR-DEUDA-LOTE-1; union en TSV.

## 10 · LO QUE NO HACE · SUCESORES
No re-mide, no adopta. Sucesor: `GEN2-DIN-CREDITO-SERIE-LECTURA-1` (en cola) cita estas celdas-D; el informe v1.3 cita K1 como «propuesta con reserva», no como victoria.

## NO-CORRIDO / RESERVAS

- **Qué:** P3 — decidir si `tools/celdas_validadas.py` se extiende con una
  cuarta clase para admitir la unidad "conducta agregada" (crédito).
  **Por qué:** `DECISIÓN-DE-MESA-PENDIENTE` — `tools/celdas_validadas.py`
  es ajeno al perímetro de este acto (§9); extenderlo es trabajo de
  TUBERÍA. **Impacto:** `celdas_validadas` no sube por las 9 celdas-D de
  crédito (92 antes y después; quedan en `clase_1_celdas_d_sin_contar`
  con motivo declarado). **Sucesor:** `GEN2-TUBERIA-CELDAS-D-CONDUCTA-1`
  (diferido, `SIN-ASIGNAR` hasta que mesa decida) — fila
  `NC-260923-GEN2-DIN-CREDITO-CELDAS-D-2-f6a3-02`, `forense/no-corrido.tsv`.

