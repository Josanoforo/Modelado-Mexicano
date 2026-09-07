ENCARGO · ACTO MAESTRA38-M13 · M-POR-CELDA PASOS 1 Y 2 — DIAGNÓSTICO-14 · ENLACE v1.1 · SCORING v1.2 (pp) · AGREGADO v1.3
Cabecera: redactado contra `origin/main = 7e0fb716` (PR #583), 7/sep/2026, dirección (Fable, Maestra 48). Instrucciones vigentes: `instrucciones-proyecto-v2_12.md`. Estado: LISTO PARA LANZAR. COMPUERTA: ninguna de merge (`forense/benchmark/BENCHMARK-MOTORES-COMPARABLES.md` y `agregado-v1_2-resultado.json` ya están en `main`).
ENTORNO ASIGNADO: NUBE (`cloud_default`). NO se lanza en UBUNTU: el agregado no abre microdato — `R` viene de `espec-R-ciega-v1_2.tsv`/resultado sellado, `L` de `L-extraido-v1_2.tsv`, `M` del emisor sobre `milpa/tramite.yaml`. MODELO SUGERIDO: Opus (dos commits, re-corrida pre-registrada).
CARRILES: en paralelo `L16-BIS-2` (caja), `TRAMITE-6` (tablero, cláusulas), `N20-N21` (`forense/prereg-caja/`). Ninguno toca `forense/prereg-duelo-v2/` ni `milpa/src/emisor.py`.
FIRMAS DE MESA — verbatim. El ejecutor propaga, no decide (SELLA-3).

* DM, 1/sep/2026 (ADR-270/276, `milpa/tramite.yaml:44-49`): la regla `tramite.mordida.discrecional` «se conserva como historia — NO se borra —, se sustituye por el MEDIDO de abajo en el cálculo del motor» → `paga_mordida_encig2025 · p 0.085118 · MEDIDO·p(tasa base ponderada)`.
* FP-200=b (mesa, 31/ago, ADR-236): «Las DOS salidas de arriba NO se tocan: siguen ASIGNADAS y siguen siendo lo que emitir_binaria devuelve para `paga_mordida`/`tramite_normal`».
* Benchmark v1.2 §5, D1 FIRMADA por merge de PR #583: «corredor P: no por ahora; se reabre cuando M deje de ser constante dentro de CIV». D4 ABIERTA: «procedimiento-scoring v1.2 con métrica secundaria (pp o Brier), para cuando z/banda no discrimina entre corredores».
* Decisión de dirección incluida en este encargo (D-B; la firma es el merge): D4 = puntos porcentuales (error absoluto en pp, MAE por corredor), `z` sigue siendo la métrica primaria y sellada; enlace v1.1 lee, para las tres celdas `TRA`, la conducta MEDIDA que DM ya firmó.
* Mesa, 6/sep/2026: «mi merge manual es la firma de las decisiones.»

═══ VERIFICACIÓN DE EXISTENCIA (A.8) — contestada por quien escribe ═══ (1) ESTRUCTURA. Gobierna `forense/prereg-duelo-v2/`: `marco-M-sorteado-v1_2.tsv` (14 celdas; columnas `regla`, `conducta` son el enlace celda→(regla, conducta)), `procedimiento-scoring-v1_1.md` + `.sha256` (sellado, intocado), `agregado_v1_2.py` (monkeypatch sobre el módulo base; `parametros_sellados: delta 0.5, nivel_ic 0.95, replicas 10000, seed 42`), `agregado-v1_2-resultado.json`, `L-extraido-v1_2.tsv`, `espec-R-ciega-v1_2.tsv`. Y `milpa/tramite.yaml` (se lee, no se escribe). (2) CONTENIDO, con comando: `python3 -c "import json;d=json.load(open('forense/prereg-duelo-v2/agregado-v1_2-resultado.json'));print({c:d['celdas'][c]['M'] for c in d['celdas']})"` → `TRA-M-02/03/07: 0.62`, `CIV-M-01/02/04/10/12/13: 0.294313`, `FAM-M-05/06/07: 0.045694`, `DIN-M-01: 0.174804`, `FAM-M-01: 0.457707`. `grep -E "TRA-M-0[237]" marco-M-sorteado-v1_2.tsv | cut -f18,19` → `tramite.mordida.discrecional -> paga_mordida`. `grep -n "paga_mordida" milpa/tramite.yaml` → `:50 p: 0.62 ASIGNADO` y `:60 paga_mordida_encig2025 p: 0.085118 MEDIDO`. `emisor.py:476-479` devuelve la primera coincidencia. Veredicto: el enlace v1.0 (26/ago, ADR-208) es VENCIDO EN ALCANCE (A.10) para las celdas TRA: se selló antes de que el motor ganara el MEDIDO (1/sep) y hoy lee un número que el propio motor declara sustituido. `ls forense/prereg-duelo-v2/ | grep -E "v1_3|scoring-v1_2|enlace-M-v1_1|diagnostico"` → 0 de 60 archivos: NO-ENCONTRADO. `grep -rn "M-POR-CELDA" forense canon` → solo en los tres encargos AUTOMATIZA-2 como «siguiente prioridad»: ningún acto lo ha ejecutado. (3) COBERTURA RETROACTIVA. `procedimiento-scoring-v1_1.md` y el enlace v1.0 son del 20–26/ago; la enmienda MEDIDA de mordida es del 1/sep y nunca pasó por el duelo.
SPEC CONGELABLE — tres piezas, todas en `forense/prereg-duelo-v2/`. COMMIT-1 congela las tres antes de correr nada; COMMIT-2 trae resultados; nada se corrige hacia atrás. Pieza 1 · `diagnostico-14-celdas-v1_0.tsv` (receta congelada, sin juicio). Una fila por celda del marco v1.2: `id_celda · regla · conducta · p_emitida · clase (leída de tramite.yaml: MEDIDO/ASIGNADO) · ola_calibracion del motor · ola del árbitro · ¿existe en la regla una enmienda MEDIDA para la misma conducta base? (sí/no, id) · ¿existe entrada _ejes_ en milpa/tramite-ola5-propuesta-v0.yaml cuyo eje coincida con el estrato de la celda? (sí/no, id, valor de esa celda)`. Es la tabla que separa «el motor no sabe» de «el motor sabe y el emisor no lo lee». Solo lee; no cambia nada. Pieza 2 · `enlace-M-v1_1.md` + `marco-M-sorteado-v1_3.tsv`. Copia byte a byte de `marco-M-sorteado-v1_2.tsv` con UN cambio: en `TRA-M-02`, `TRA-M-03`, `TRA-M-07`, columna `conducta` = `paga_mordida_encig2025` (la única enmienda MEDIDA firmada al motor para esa regla). Las 11 celdas restantes no cambian: `miedo_desconfianza`, `tiene_ahorros`, `recibe_dinero_familiares_para_vejez` no tienen enmienda MEDIDA por celda firmada (si la pieza 1 encuentra una, se REPORTA, no se aplica — sería una decisión nueva). `enlace-M-v1_1.md` re-sella el enlace contra el universo nuevo (A.10 corolario 1: v1.0 intacto, enmienda fechada) y declara la limitación de escala/ola: el MEDIDO está calibrado en ENCIG 2025 y los árbitros de TRA-M-03/07 son ENCIG 2013/2021 (A-bis 3: se compara la misma escala — proporción — y se declara el desfase de ola; no se «ajusta»). Pieza 3 · `procedimiento-scoring-v1_2.md` + `.sha256` y `agregado_v1_3.py`. v1.2 = v1.1 verbatim + una sección «Métrica secundaria (D4, pre-registrada)»: `err_pp = 100·(corredor − R)` por celda con signo; `MAE_pp` por corredor sobre las 14; comparación pareada `L-solo vs M` y `L+corpus vs M` por diferencia de `MAE_pp` con el mismo bootstrap (`replicas 10000, seed 42`), IC95; la banda `z` de v1.1 sigue siendo el veredicto primario y no se toca; la secundaria no adjudica «en banda», solo ordena corredores. `agregado_v1_3.py` = monkeypatch sobre v1.2 (mismo patrón que v1.2 sobre v1.1) con `MARCO_TSV → marco-M-sorteado-v1_3.tsv` y la métrica secundaria añadida; escribe `agregado-v1_3-resultado.json` con `parametros_sellados` idénticos + `enlace: v1_1` + `scoring: v1_2`. Expectativa declarada antes de correr (B-bis): con `M(TRA) = 0.085118`, aritmética sobre el JSON v1.2 da `z ≈ −8 / +14 / +6` en TRA (era 98 / 203 / 229) y mediana |z| de `M` ≈ 7.4 (era 11.4); ninguna celda entra en banda ±0.5·EE; si el resultado difiere, se reporta el resultado, no la expectativa. Cierra con «el primer resultado que produzca este procedimiento es el que se reporta».
PERÍMETRO Y CONCURRENCIA Toca: `forense/prereg-duelo-v2/diagnostico-14-celdas-v1_0.tsv` · `enlace-M-v1_1.md` · `marco-M-sorteado-v1_3.tsv` · `procedimiento-scoring-v1_2.md` + `.sha256` · `agregado_v1_3.py` · `agregado-v1_3-resultado.json` · `forense/benchmark/BENCHMARK-MOTORES-COMPARABLES.md` (sección nueva «v1.3», append; el cuerpo v1.2 intacto) · `forense/firmas-pendientes.tsv` (D4 → FIRMADA por merge; recibo) · cascada de cierre. No toca `milpa/**`, ni `procedimiento-scoring-v1_1.md`, ni `enlace-M-v1_0.md`, ni `marco-M-sorteado-v1_2.tsv`, ni capturas `corridas-L/`. En paralelo: `L16-BIS-2`, `TRAMITE-6`, `N20-N21`. Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.
FP/ADR CANDIDATOS — deriva, no heredes. Al redactar: FP máx 330, ADR máx 379 contra `7e0fb716`.
CONTADOR: medición: sí — el marcador `L-solo / L+corpus / M` contra `R` se re-corre como v1.3 con métrica secundaria pre-registrada; mueve `benchmark_version` 1.2 → 1.3 y `D4` ABIERTA → FIRMADA. No mueve tiers ni el motor.
Lo que este acto NO hace. No ejecuta el paso 3 (valor por celda en `evaluar()`: cambio de esquema del motor, ADR-29, `tests/test_emisor_m2.py`) — lo habilita con la pieza 1. No cambia `p` ni `clase` de ninguna regla. No reabre D1. No toca las cuatro conductas que el carril `N2` declaró intocables en `emisor.cargar_reglas()` (ADR-294): el cambio es en el enlace, no en el motor.
Sucesores declarados, no lanzados. `M14` (paso 3, diseño de fase, Fable): reglas con desglose por ejes y `evaluar()` eligiendo celda por segmento — con la pieza 1 como insumo; su señal de éxito es la de D1: «cuando M deje de ser constante dentro de CIV».

## CONSUMIDO

Ejecutado por `ACTO MAESTRA38-M13 · M-POR-CELDA PASOS 1 Y 2`, 7/sep/2026,
Pull Request [#592](https://github.com/Josanoforo/Modelado-Mexicano/pull/592).

Pieza 1 (`forense/prereg-duelo-v2/diagnostico-14-celdas-v1_0.tsv`): censo
de las 14 celdas contra `milpa/tramite.yaml` — solo `TRA-M-02/03/07`
tienen una enmienda MEDIDA con firma de mesa citada por este encargo;
`DIN-M-01` tiene una enmienda análoga (`enmienda_enif2024`) reportada, no
aplicada (ninguna firma de este encargo la cita — sucesor declarado).

Pieza 2 (`forense/prereg-duelo-v2/enlace-M-v1_1.md` +
`marco-M-sorteado-v1_3.tsv`): re-apunta solo `TRA-M-02/03/07` a
`paga_mordida_encig2025`, un único cambio de columna, verificado por
`diff`.

Pieza 3 (`forense/prereg-duelo-v2/procedimiento-scoring-v1_2.md` +
`.sha256`, `agregado_v1_3.py`): scoring v1.1 verbatim + §7 (D4, métrica
secundaria en puntos porcentuales — decisión de dirección: pp, no
Brier). `M` de las tres celdas re-apuntadas calculado en memoria vía
`emitir_binaria`, sin escribir `M-<id>.json` nuevo (fuera de perímetro).

Resultado (`agregado-v1_3-resultado.json`, primera corrida, sin ajustar):
`z_M` en `TRA` `98/203/229` → `−8.08/+14.28/+5.55` (confirma expectativa
B-bis); `comparacion_principal_pareada` (primaria, `z`) sigue
`INDETERMINADO`; `D4` (secundaria, pp) SÍ discrimina —
`M=4.51pp [2.71,6.37]` vs `L_SOLO=11.69pp [4.13,21.72]` vs
`L_CORPUS=19.60pp [9.28,30.92]`, `M-MENOR-ERROR-PP-QUE-L` en los dos
pares pareados. `D1` sin cambio. `BENCHMARK-MOTORES-COMPARABLES.md`
sección `v1.3` (append). `forense/firmas-pendientes.tsv` `FP-333`
(`D4` → FIRMADA por merge; renumerada dos veces — `FP-331` tomada por
`ACTO MAESTRA38-TRAMITE-6`, luego `FP-332` tomada por `ACTO
MAESTRA38-L16-BIS-2`, ambos fusionados primero, regla de la casa).
`canon/gobernanza-v1_15.md` `ADR-383` (renumerado dos veces por la misma
causa: `381`→`382`→`383`), `canon/estado-programa-v1_12.md` L0 + tabla,
`canon/registro-rotulos.tsv` censado. `tests/check.py --baseline` VERDE,
sin FAIL nuevo.

Paso 3 (`evaluar()` por celda/eje, `M14`) y el re-apuntado de `DIN-M-01`
quedan como sucesores declarados, no lanzados por este acto.
