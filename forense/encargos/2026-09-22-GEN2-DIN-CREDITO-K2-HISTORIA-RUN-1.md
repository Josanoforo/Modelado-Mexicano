# ENCARGO · ACTO GEN2-DIN-CREDITO-K2-HISTORIA-RUN-1 · La quinta corrida de crédito histórico, ya congelada, corre sobre microdato y entra a la vista

> ENTORNO: **CAJA** — abre ENIF 2012/2015/2018/2021 (ya abiertas por `#943` y `GEN2-DIN-CREDITO-HISTORIA-1`); **no abre ENIF 2024** (`exposicion_historica: CIEGO-A-2024-NO-ABIERTA`). Hook; si no coincide, PARA.

CABECERA · SHA `ccd7c0eb` · una sola sesión · MODELO: **Sonnet** (D-13: receta sin juicio — el código está congelado; sube a Opus si el conducto rechaza una rama) · MODO: **RÍGIDO** (spec y medidor congelados en COMMIT-1 por `GEN2-DIN-CREDITO-HISTORIA-1`) · CONTADOR: +1 corrida sellada y registrada, `cuenta_gen2 = SI` (etiqueta ya en el CALC), `adopta = NO` · CALC: `CALC-DIN-CREDITO-K2-BANCARIA-HISTORIA-0001` tal como está, o `-0002` si el conducto exige CALC nuevo (rama prevista) · ids raíz de acto.

## 1 · OBJETIVO
Que el descriptivo rotulado de K2-bancaria 2012–2021 (frontera `FP-404 (2)`) exista como RESULT GEN2 sobre microdato, sellado y en la vista. «Hecho» = `verify <CALC>` → `REPRODUCE`; `ejecucion.json` con `firma_entorno` de caja y `medidor_ejecutado_al_congelar` distinto de «solo sintético»; fila en `corridas.tsv`; asiento en `replay-evidencia.tsv`.

## 2 · FIRMAS DE MESA
- `FP-260921-GEN2-DIN-CREDITO-HISTORIA-1-ff56-02` — *propuesta de dirección, mesa sella o borra*: «Se autoriza el `run` de la quinta corrida congelada (`CALC-DIN-CREDITO-K2-BANCARIA-HISTORIA-0001`) como acto propio con contador propio; cuenta, no adopta.» Sin texto → PARA.
- Ya en el CALC: `cuenta_gen2_firma: PROPUESTA DE DIRECCIÓN (encargo GEN2-DIN-CREDITO-HISTORIA-1 §2) … FP-404 (2) FIRMADA`.

## 3 · LO QUE DIRECCIÓN SABE
- `[EJECUTADO]` `ejecucion.json` del CALC: `exit_code 0`, `estado_al_congelar: COMMIT-1 SIN CORRIDA`, `medidor_ejecutado_al_congelar: SI — sobre los cuatro payloads sintéticos de los tests hermanos (120 réplicas) …; NUNCA sobre microdato en este CALC`, `tipo: DESCRIPTIVO-ROTULADO-CON-FRONTERA`; `resultados.json` trae **92 RESULT del sintético**; `corridas.tsv` ya tiene 1 fila con su id.
- `[SUPUESTO]` `run` se negará sobre el `-0001` porque ya hay `sello.json` (E.3: «run se niega; no existe --force»). Si es así, rama prevista: **CALC nuevo `-0002`** con la misma `spec.yaml` (sha idéntico, citado) y `medidor.py` idéntico, y el `-0001` queda como constancia de COMMIT-1 con enmienda fechada. Si `run` acepta porque el sello era de spec y no de corrida, se corre el `-0001` y se declara.
- ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
`grep -c "K2-BANCARIA-HISTORIA" data/corrida0/corridas.tsv` → 1 (COMMIT-1); `grep -c "K2-BANCARIA-HISTORIA-0002"` → 0. Ramas vivas: ninguna.

## 5 · PIEZAS
- **P1 · Verificación de sello:** `preflight` VERDE con payload `COINCIDE` en caja (D-22 (1)); sha de `spec.yaml` y `medidor.py` pegados; **ninguna edición**.
- **P2 · `run` y `verify`:** sobre el `-0001` o el `-0002` según §3; 92 RESULT (o los que la spec declare — se deriva) con tipo, unidad, tolerancia; rotulado `DESCRIPTIVO` y frontera `FP-404 (2)` en cada RESULT.
- **P3 · Vista:** registro y asiento en el mismo acto (E.7); `status` antes/después; nota corta.

## 6 · LATITUD
DECIDES TÚ: enlazar `data/raw`, dependencias, orden. PREGUNTAS A MESA: ninguna prevista. NO DECIDES: §7.

## 7 · PAROS
a) abrir ENIF 2024 · b) editar spec/medidor congelados o forzar · c) adoptar · d) cambiar cualquier parámetro congelado · e) nube · f) inalcanzable · **g) el código congelado no corre → no se parcha; PARO y el diff del error es el entregable.**

## 8 · COMPUERTAS
«Firma ff56-02 presente — protege: abrir dato.» «No hay otro acto de caja en vuelo — protege: borrar.»

## 9 · PERÍMETRO
Propio: el CALC (`-0001` o `-0002`) · derivados por comando · `replay-evidencia.tsv` · nota · tablero · `canon/L0/<raíz>.md`. Ajeno: `CALC-DIN-CREDITO-PISOS-ENIF2018-0001` (oro, lectura), specs del acto padre. Otro acto en vuelo: ninguno verificado; no correr a la vez que E1/E2. «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · NO HACE · SUCESORES · CIERRE
No adopta, no abre 2024, no cambia nada congelado. Sucesor: `FP-…ff56-01` (recorte 18-70) es otro acto, no éste. Auditoría: no aplica (rotulado descriptivo; la afirmación la hace la lectura, no la corrida). Cierre por /acto.

## NO-CORRIDO / RESERVAS

- **qué:** P3 · «Vista: registro y asiento en el mismo acto (E.7)» y el criterio de «hecho» «fila en `corridas.tsv`» · **por qué:** DIFERIDO-A:acto TUBERIA — desde #984, `verify.yml:542-546` impide que un PR toque un derivado, y el job de push a main que firmó mesa (`FP-260922-GEN2-PENDIENTES-CAJA-1-c09b-02`, opción (a)) todavía no corre `registro` (`verify.yml:369-370` exige `--lote`). El asiento sí viaja (`forense/replay-evidencia.tsv`, REPRODUCE/IDENTICO). Proyección en seco: `-0001` `SUPERADO→-0002`, `-0002` `SELLADA · GEN2 · cuenta_gen2=SI` · **impacto:** la corrida queda «sellada en disco, no registrada»; `corrida0 status` la cuenta (158 → 159), la vista publicada no; ningún contador de adopción se mueve · **sucesor:** `NC-260922-GEN2-DIN-CREDITO-K2-HISTORIA-RUN-1-ef6f-01` → acto TUBERIA (job de push a main); hasta entonces, mesa: `registro --verifica --escribe --lote CALC-DIN-CREDITO-K2-BANCARIA-HISTORIA-0002` sobre main.
