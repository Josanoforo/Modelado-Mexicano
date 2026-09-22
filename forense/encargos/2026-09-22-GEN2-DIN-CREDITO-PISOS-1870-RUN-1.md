# ENCARGO · ACTO GEN2-DIN-CREDITO-PISOS-1870-RUN-1 · El piso de crédito ENIF 2021 recortado a 18-70, ya congelado, corre sobre microdato y entra a la vista

> ENTORNO: **CAJA** — abre ENIF 2021; no abre 2024. Hook; si no coincide, PARA.

CABECERA · SHA `ccd7c0eb` · una sola sesión · MODELO: **Sonnet** · MODO: **RÍGIDO** (spec y medidor congelados por `GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-1`) · CONTADOR: +1 corrida sellada y registrada, `cuenta_gen2 = SI` (etiqueta ya en el CALC, firma de contador 21/sep), `adopta = NO` · CALC: `CALC-DIN-CREDITO-PISOS-ENIF2021-RECORTE1870-0001` o `-0002` si el conducto exige CALC nuevo · ids raíz de acto. **Lote con `GEN2-DIN-CREDITO-K2-HISTORIA-RUN-1` si ambos siguen sin lanzar (D-11: mismo entorno, afines).**

## 1 · OBJETIVO
Que los pisos históricos de crédito (2012/2015/2018, población 18-70 por diseño) y el de 2021 sean conmensurables: el CALC recortado, congelado, corre y entra a la vista. «Hecho» = `verify <CALC>` REPRODUCE; fila en `corridas.tsv`; asiento en `replay-evidencia.tsv`; `ejecucion.json` con `medidor_ejecutado_al_congelar` distinto de «solo sintético».

## 2 · FIRMAS DE MESA
- `FP-260921-GEN2-DIN-CREDITO-HISTORIA-1-ff56-01`, opción **(a)** — *propuesta de dirección, mesa sella o borra*: «Sucesor que corra el mismo medidor genérico sobre ENIF 2021 con `recorte_edad = 18-70` como CALC nuevo, sin editar #943.» El CALC ya existe congelado; la firma autoriza su `run`. Sin texto → PARA.

## 3 · LO QUE DIRECCIÓN SABE
- `[EJECUTADO]` `CALC-DIN-CREDITO-PISOS-ENIF2021-RECORTE1870-0001/ejecucion.json`: `exit_code 0`, `medidor_ejecutado_al_congelar: SI — sobre el payload sintético de tests/test_din_credito_pisos_enif2021.py`, `cuenta_gen2_firma: FIRMA DE CONTADOR (mesa, 21/sep/2026)`, `tipo: PISO-PERSISTENCIA-POR-EJE`; **0** filas en `corridas.tsv` y `replay-evidencia.tsv`. Creado por `GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-1` (`forense/encargos/2026-09-21-…-COMMIT-1.md`).
- `[SUPUESTO]` `run` se negará por `sello.json` → rama: `-0002` con `spec.yaml` y `medidor.py` idénticos (sha citados); el `-0001` queda como constancia con enmienda fechada.
- ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
`grep -c RECORTE1870 data/corrida0/corridas.tsv` → 0. Ramas vivas: ninguna.

## 5 · PIEZAS
- **P1:** `preflight` VERDE con payload COINCIDE; sha de spec/medidor pegados; ninguna edición.
- **P2:** `run` + `verify`; RESULT con tipo, unidad, escala, universo `18-70` en cada uno.
- **P3:** registro y asiento en el mismo acto; `status` antes/después; nota corta; FP → FIRMADA con cita.

## 6 · LATITUD
DECIDES TÚ: enlazar `data/raw`, dependencias. PREGUNTAS A MESA: ninguna prevista. NO DECIDES: §7.

## 7 · PAROS
a) abrir ENIF 2024 · b) editar lo congelado o forzar · c) adoptar · d) cambiar parámetros congelados · e) nube · f) inalcanzable · g) código congelado no corre.

## 8 · COMPUERTAS
«Firma (a) presente — protege: abrir dato.» «No hay otro acto de caja en vuelo — protege: borrar.»

## 9 · PERÍMETRO
Propio: el CALC (`-0001` o `-0002`) · derivados por comando · `replay-evidencia.tsv` · `firmas-pendientes.tsv` (una fila) · nota · `canon/L0/<raíz>.md`. Ajeno: `CALC-DIN-CREDITO-PISOS-ENIF2018-0001` (oro, lectura), #943. «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · NO HACE · SUCESORES · CIERRE
No adopta, no abre 2024. Sucesor: la comparación conmensurada 2012–2021 (lectura, en la conversación de dinero). Auditoría: no aplica. Cierre por /acto.



## NO-CORRIDO / RESERVAS

- **NC-260922-GEN2-DIN-CREDITO-PISOS-1870-RUN-1-009f-01** · qué: «registro --verifica --escribe --lote del -0001» / «fila en corridas.tsv» (ADENDA-1) · por qué: FUERA-DE-PERÍMETRO:GEN2-TUBERIA-EFICIENCIA-1. Su firma del 21/sep §2(2) saca los derivados de todo PR (`verify.yml:542-546`, bloqueante), y el job de main no corre `registro` (`verify.yml:358-391`). Fila medida en seco: `SELLADA · GEN2 · cuenta_gen2=SI · REPRODUCE · IDENTICO` · impacto: la corrida sigue «sellada en disco, no registrada»; `corridas.tsv`/`resultados.tsv` publicados no la muestran (`status` sí, porque re-deriva en memoria) · sucesor: mesa -- `registro --verifica --escribe --lote CALC-DIN-CREDITO-PISOS-ENIF2021-RECORTE1870-0001` sobre main.
- **NC-260922-GEN2-DIN-CREDITO-PISOS-1870-RUN-1-009f-02** · qué: hallazgo de aparato pedido por mesa: «un CI que revierte corridas.tsv/resultados.tsv puede borrar el registro de corridas selladas y dejar el contador mintiendo (E.7)» · por qué: FUERA-DE-PERÍMETRO:GEN2-TUBERIA-EFICIENCIA-1. Evidencia: `344739d1` quitó las filas de `17d27f82`; hoy la vista publicada va 18 corridas atrás (285 filas frente a 303 derivadas; +44/−26 filas de corrida y +21 951/−1 502 RESULT en el diff en seco). `344739d1` protege la regla «los derivados no viajan en un PR»; lo que destruye es la única vía que tenían las filas selladas para llegar a la vista, porque nadie corre `registro` sobre main · impacto: toda corrida sellada desde el 21/sep queda fuera de la vista publicada; quien lee `corridas.tsv` sin re-derivar ve un contador atrasado · sucesor: SIN-ASIGNAR -- dirección redacta el encargo: «qué protege ese revert y qué destruye».
- **NC-260922-GEN2-DIN-CREDITO-PISOS-1870-RUN-1-009f-03** · qué: «asiento en replay-evidencia.tsv con cita a 17d27f82» (ADENDA-1) · por qué: SUSTITUIDO-POR:GEN2-PENDIENTES-CAJA-1 (PR #1004). Absorbe el asiento de `…RECORTE1870-0001--f1469f52d4b3` y el de `…K2-BANCARIA-HISTORIA-0001--78664b318a0c`, los dos `REPRODUCE`/`IDENTICO`. No queda nada huérfano si #1004 se fusiona; si no, falta el asiento de los dos. Este acto retiró su fila propia (`c38af42d`) para no tener dos escritores; su verify queda como corroboración independiente en la nota · impacto: ninguno si #1004 se fusiona · sucesor: GEN2-PENDIENTES-CAJA-1 (PR #1004).
- **NC-260922-GEN2-DIN-CREDITO-PISOS-1870-RUN-1-009f-04** · qué: «K2-BANCARIA-HISTORIA … Va en lote contigo (D-11)» (ADENDA-1) · por qué: DIFERIDO-A:GEN2-DIN-CREDITO-K2-HISTORIA-RUN-1. Mesa no confirmó que la sesión de `~/mm-gen2-din-credito-k2-historia-run-1` esté muerta (respuesta: «termina el encargo»); evidencia a las 14:19: sin commits, sin rama remota, nada modificado después de las 13:46. Este acto no toca K2 · impacto: K2 sigue `NO-CORRIDA` en la vista publicada, aunque tiene `resultados.json` · sucesor: GEN2-DIN-CREDITO-K2-HISTORIA-RUN-1 (si su sesión está muerta, mesa -- `registro --verifica --escribe --lote CALC-DIN-CREDITO-K2-BANCARIA-HISTORIA-0001` sobre main).

## CONSUMIDO

Ejecutado por ACTO GEN2-DIN-CREDITO-PISOS-1870-RUN-1 -- PR #1008 (rama `acto/gen2-din-credito-pisos-1870-run-1`), con la ADENDA-1 de mesa (`2026-09-22-GEN2-DIN-CREDITO-PISOS-1870-RUN-1-ADENDA-1.md`). ADR `ADR-260922-GEN2-DIN-CREDITO-PISOS-1870-RUN-1-009f-01`. Sin run nuevo: verify REPRODUCE/IDENTICO 2941/2941 del `-0001` ya sellado en `17d27f82`. Registro a mesa (NC -01), asiento E.7 en #1004 (NC -03).
