# ENCARGO · ACTO GEN2-DEMANDA-DICTAMEN-1 · La demanda pide 105 corridas y 236 RESULT, pero 61 corridas no se pueden decidir (35 sin payload declarado, 4 sin spec, 25 sin instrumento, 22 sin candidato) y 70 de los 236 son celdas del duelo v2 que la regla 6 dejó sin camino de emisión; 33 son θ y asignados de procedencia.yaml, 23 son momentos HOLDOUT. Este acto dictamina cada corrida y cada RESULT pendiente por objeto —payload por id, spec por archivo, consumidor por línea— para que la demanda vuelva a ser una cola de trabajo y no un inventario, y deja la vista `demanda-dictamen-v1_0.tsv` que los lotes de caja consumen

> ENTORNO: **NUBE** — lee manifiesto, specs, `tramite.yaml`, `procedencia.yaml`, `catalogo-momentos`, `prereg-duelo-v2/`, sellos; escribe la vista de dictamen y el registro que la demanda lee. Cero microdato. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción `723b62c1` (re-deriva `corrida0 demanda` al abrir) · una sesión, rama propia; PR por bloque de dictamen · MODELO: **Opus** (cada dictamen es un juicio sobre qué es un objeto y quién lo consume) · MODO: **AUTÓNOMO-AMPLIO** (cláusula v1.0) · ids con raíz de acto · D-21 aplica.
CONTADOR: **cero mediciones; no adopta**. `N_corridas_requeridas` y `N_resultados_pendientes` bajan **solo por dictamen con cita** del vocabulario de abajo (firma 17/sep: el universo real de relevo-usos es el que se dictamina); nunca borrando filas. Declara antes/después por token.

## 1 · OBJETIVO
(P1) **Las 61 corridas indecidibles.** Para cada `INDECIDIBLE-SIN-PAYLOAD-DECLARADO`, `INDECIDIBLE-SIN-SPEC`, `NO-DECLARADO-EN-EL-REGISTRO` (instrumento) y `SIN-CANDIDATO-EN-EL-REGISTRO` (medidor): payload por id en `data/manifiesto.yaml` (A.15, con conteo), instrumento por texto del RESULT legacy y su script (`script_legacy`, `receta_legacy`), spec candidata por archivo, entorno por lo que toca. Dictamen cerrado: `DECIDIBLE (payload id, spec, entorno)` · `SIN-PAYLOAD-EN-CORPUS (qué falta; va a obtención)` · `SIN-ESTIMANDO-RECONSTRUIBLE (el GEN1 no declara qué midió; NO-RELEVAR con cita)`.
(P2) **Los 70 del duelo v2** (`celda_L` 28, `celda_R` 14, `celda_M` 14, `celda_AGREGADO` 14; consumidor `forense/prereg-duelo-v2/marco-M-so…`; medidores `emite_m.py`, `runner_l_c…`, `agregado_v…`, `arbitra.py`): bajo la regla 6 (sin retadores, pilotos ni duelos sobre olas vistas; θ y matriz generan retadores, no emiten) y los sellos del duelo ya adjudicados (seis evaluaciones prospectivas cerradas, transfer 26/sep): `NO-RELEVAR-POR-REGLA-6` · `RELEVAR-COMO-PISO-DESCRIPTIVO (solo R árbitro de ola vista que un consumidor vivo aún cite)` · `DIFERIDO-A-FAMILIAS-2027 (familia, gate)`. Cada uno con la línea del consumidor que lo cita, o «nadie ocupó la fila».
(P3) **Los 33 de `procedencia.yaml`** (`condicional_theta` 12, `asignado_probabilidad` 13, `coeficiente_asignado` 8) y las 10 `celda_D` de `curacion-registro/celdas-d/`: θ es generador de retadores, no camino de emisión (§4) → `NO-RELEVAR-θ` salvo que un consumidor vivo lo cite; asignados y coeficientes → `RELEVAR-DESDE-RESULT (qué RESULT GEN2 lo deriva; clase iii)` o `SIN-BASE-GEN2 (espera relevo de su medido)`; celdas-D → estado del contrato celda-D por archivo.
(P4) **Los 23 momentos** (`catalogo-momentos`): `ESPERA-FIRMA-HOLDOUT` con la letra de la hoja consolidada que lo decide, salvo los de rol AJUSTE (8 en el catálogo): esos, si les falta RESULT, `DECIDIBLE` para caja. Producto final: `data/corrida0/demanda-dictamen-v1_0.tsv` (corrida_id · resultado_id · dictamen · cita · sucesor) registrada en INFRAESTRUCTURA y leída por `corrida0 demanda` (si hoy no la lee, ≤ 10 líneas declaradas o el hallazgo), más una hoja RH con lo que necesita firma (HOLDOUT y las dos o tres bifurcaciones que salgan) para FIRMAS-21/22.

«Hecho», por comando sobre el commit final con `origin/main` fusionado: toda corrida y todo RESULT de la demanda de apertura tiene fila en `demanda-dictamen-v1_0.tsv` (ids sin fila: 0) · ningún dictamen sin `cita` · `corrida0 demanda` en el commit final reporta menos corridas requeridas y la nota cuadra la diferencia por token · `grep -c "no existe"` en la vista = 0 · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA — dadas
§1 (encargos salen de la demanda; contador que no se mueve) · §4 regla 6 y HOLDOUT · firma 17/sep verbatim (registrada en decisiones aplicadas): «MEDICION-DEMANDA-3 se redefine al universo real de relevo-usos-v1_0.tsv: 153 SIN-CANDIDATO…» — este acto aplica esa misma lógica a la demanda entera · E.2 (clase iii para derivados) · A.4/A.15. **No decide**: firmas HOLDOUT, apertura de reservas, adopción.

## 3 · LO QUE DIRECCIÓN SABE
- [EJECUTADO] `723b62c1` · `corrida0 demanda`: N_resultados_pendientes 236, N_corridas_requeridas 105, `clausura_activa_de_payloads` 22. `demanda-corridas.tsv`: instrumento NO-DECLARADO 25; medidor SIN-CANDIDATO 22, `milpa/src/motor.py` 21, `arbitra.py` 14, `emite_m.py` 14, runner/agregado del duelo 28, `momentos.py` 4, `pi.py` 1, `theta.py` 1; entorno NUBE 42, INDECIDIBLE-SIN-PAYLOAD 35, CAJA 24, INDECIDIBLE-SIN-SPEC 4. `demanda-resultados.tsv`: `spec_legacy` NO-DECLARADO 132 de 236; `spec_sha_legacy` NO-DECLARADO 208. Tipos × consumidor: arriba.
- [EJECUTADO] `milpa/catalogo-momentos-v0_1.tsv`: `rol_calibracion` HOLDOUT 15, AJUSTE 8.
- [LEÍDO] Transfer 26/sep §1.5: «la etapa de retadores cerró con resultado … Regla 6 para todo ejecutor». Memoria operativa §3: regla 6 y frente prospectivo.
- [EXISTE] `data/corrida0/relevo-usos-v1_0.tsv`, `mapa-demanda-19-corr-v1_0.tsv` (dictamen anterior de 19 corridas: cítalo, no lo rehagas), `tools/corrida0.py demanda`.

## 4 · YA HECHO / YA DECIDIDO — por objeto
`git ls-tree -r --name-only origin/main forense/encargos | grep -c 'DEMANDA-DICTAMEN\|MEDICION-DEMANDA-4'` → 0. Consumidos y citados: MEDICION-DEMANDA-3, RELEVO-MOTOR-34, RELEVO-CONSUMIDORES-2/3, MAPA-DEMANDA-19 (vista `mapa-demanda-19-corr`), NC-DECISIONES-1 (A1/A2 sobre momentos), MAPA-INSTRUMENTOS-ALTERNOS-1 (HOLDOUT aviso). En vuelo: RELEVO-TRAMITE-CAJA-1 (mide las 10 de orden 1 de tramite.yaml: **no las dictamines como pendientes, cítalas como EN-CURSO**), PISOS-Y-ADENDAS-1, TUBERIA-Y-CURACION-1 (tools/: si `corrida0.py` necesita leer la vista nueva, coordina por archivo), REGLAS-Y-RESULT-1.

## 5 · PIEZAS
P2 primero (es el bloque mayor y el más mecánico bajo regla 6), luego P3, P1, P4. Rama prevista: consumidor cuya línea ya no existe → «nadie ocupó la fila», no derrota; RESULT legacy con `script_legacy` que apunta a archivo borrado → `SIN-ESTIMANDO-RECONSTRUIBLE` con el commit donde desapareció.

## 6 · LATITUD
Vocabulario adicional si lo necesitas (declarado antes de usarlo), orden, PR. PREGUNTA A MESA: ninguna fuera de la hoja. NO DECIDES: nada de §7.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) abrir dato · b) borrar filas de la demanda; editar RESULT legacy, sellos, `tramite.yaml`, `procedencia.yaml` · c) adoptar; relevar por tu cuenta; mover un contador sin dictamen citado · d) no aplica · e) CAJA · f) objetivo inalcanzable.

## 8 · COMPUERTAS
«La demanda baja por dictamen citado, nunca por borrado» protege **borrar** · «θ y duelo no emiten» protege **adoptar** (regla 6) · «HOLDOUT espera firma» protege **abrir dato**.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `data/corrida0/demanda-dictamen-v1_0.tsv` (nueva, registrada en INFRAESTRUCTURA), `tools/corrida0.py` **solo** si la demanda debe leer la vista (≤ 10 líneas, coordinado con TUBERIA-Y-CURACION-1), `forense/analisis/demanda-dictamen-1/` (hoja, tablas), TSV de gobierno (append), nota, L0, cascada. Ajeno: `milpa/`, `prereg-duelo-v2/`, sellos, specs de caja (RELEVO-TRAMITE-CAJA-1). «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · LO QUE NO HACE · SUCESORES · CIERRE
No mide, no releva, no adopta, no abre reservas, no decide HOLDOUT. Sucesores: `RELEVO-TRAMITE-CAJA-2` y `CALC-ALTERNOS-LOTE-1` (consumen la vista), FIRMAS-21/22 (hoja). Sin módulo de auditoría (no afirma sobre México). El cuerpo no lleva campos para rellenar; `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio) y `## CONSUMIDO` las añade /acto. Adendas: `2026-09-28-GEN2-DEMANDA-DICTAMEN-1-ADENDA-N.md`, selladas al recibirse.
