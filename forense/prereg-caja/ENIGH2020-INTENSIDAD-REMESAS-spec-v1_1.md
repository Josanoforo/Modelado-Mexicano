# ENIGH2020-INTENSIDAD-REMESAS · especificación humana sucesora v1.1 · tolerancia de coma flotante

`ACTO GEN2-C1-SUCESORES-Y-LOTE-3`, P2, renglón R33 (`FP-260928-GEN2-ASTRA-CONTINUIDAD-C1-1-26a2-05`). Redactada el 28/sep/2026. **Solo spec**: este acto no corre el CALC. Lo corre `GEN2-RELEVO-TRAMITE-CAJA-2`, que además escribe el `spec.yaml` sucesor.

Firma de mesa, verbatim (28/sep/2026, `forense/encargos/2026-09-28-GEN2-TRAMITE-FIRMAS-21-ADENDA-1.md`, R33 (1)): «Queda el NO-PASA formal de los dos RESULT de remesas ENIGH2020. Autorizo una spec sucesora con tolerancia absoluta 1e-10 para su próxima validación; la spec sellada no se edita.»

## 1 · Padre

- `CALC-ENIGH2020-INTENSIDAD-REMESAS-0001`, sellado. `spec.md` sha256 `340f59bd91a973ad3ac42b036bc2dcb7c49fdedf2b6b1b6af8263776370d777f`; `spec.yaml` sha256 `65ae9bdb9aa0a0dbef6179f0d63885fb0d2293b52d50980be085974c240a6d2a`. Ninguno de los dos se edita.
- Sucesor: `CALC-ENIGH2020-INTENSIDAD-REMESAS-0002`, con `repite_de: CALC-ENIGH2020-INTENSIDAD-REMESAS-0001` en la raíz del `spec.yaml` y `spec_md` apuntando a este archivo con su sha256.

## 2 · Qué cambia

Un solo campo: la tolerancia de comparación del sucesor.

| | Padre (`spec.yaml` L51) | Sucesor |
|---|---|---|
| RESULT `tipo: flotante` y `tipo: proporcion` | `{tipo: determinista, exacto_por_seed: true, abs: 0.0}` | `abs 1e-10`, `rel 0` |
| RESULT `tipo: entero` | exacto | exacto (sin cambio) |
| RESULT `tipo: texto` | exacto | exacto (sin cambio) |

La tolerancia se aplica igual al punto y a los extremos de IC (`…-IC-LO`, `…-IC-HI`), porque el sucesor fija semilla y generador (`seed: {aplica: true, valor: 20260916, rng: numpy.PCG64}`) igual que el padre.

**Por qué.** En la validación del lote 2 de C1, `RESULT-ENIGH20-REMINT-PARTICIPACION-AGREGADA` y `RESULT-ENIGH20-REMINT-REMESAS-MEDIA` dieron NO-PASA por Δ −4.4e−16 y −1.8e−12 bajo tolerancia 0.0 (`data/corrida0/validaciones-independientes.tsv`, las dos filas de `CALC-ENIGH2020-INTENSIDAD-REMESAS-0001`). Son diferencias de orden de suma en coma flotante, no de estimando. Con abs 1e−10 caben las dos. Esa tolerancia es la misma que el padre ya usa para `tolerancia_prevalencia` (L45), y la misma que el lote 3 de C1 aplica a los paquetes de su familia.

## 3 · Qué no cambia

Todo lo demás es verbatim del padre, y el padre es la autoridad para ello: universo, filtros, ponderador, transformación, estimando, variables, `parametros` (incluidos `tolerancia_prevalencia: 1.0e-10`, `tolerancia_componente_pesos: 0.01`, `bootstrap_replicas: 2000`, `metodo_ic`, `tratamiento_upm_unica`), semilla, insumos con su hash (`enigh2020_nc_csv` sha256 `47417cac13da7dce3a710d86c5767564101086a51666ec674acf27740e0701d4`; `CALC-B-0001/resultados.json` sha256 `87e20e5aa2923fcc4b206734fa13ec321d3b036d61edd48eb0efd5bd369f263d`) y la lista de los 45 RESULT, cada uno con el prefijo `RESULT-ENIGH20-REMINT-`. El medidor del sucesor es el del padre, citado por sha256; no se reescribe.

## 4 · Lo que esta spec no hace

- No cambia el NO-PASA de los dos RESULT del padre: queda formal (firma R33).
- No adopta cifras. `cuenta_gen2` del sucesor lo resuelve la mesa como en el padre (`PENDIENTE-DE-MESA`).
- No abre ENIGH 2024: ni la reserva ni sus aperturas parciales se tocan.
- No escribe el `spec.yaml` ni corre el CALC. Eso es de `GEN2-RELEVO-TRAMITE-CAJA-2`.

## 5 · Módulo de auditoría (v2.16)

- **¿Cuántos contadores mueve?** Cero. Es una spec, no una medición.
- **¿PROSPECTIVA o RETROSPECTIVA?** RETROSPECTIVA: ENIGH 2020 es una ola vista y el valor sellado se conoce.
- **¿Qué unidad tiene cada cifra?** La misma que en el padre: hogar (conteos, masas expandidas, proporciones de hogares) y pesos de 2022 por trimestre normalizado (media y mediana de remesas). Ninguna se promedia con cifras de persona.
- **¿En qué escala está cada cantidad y contra qué se compara?** La tolerancia 1e−10 es absoluta y se aplica en la escala nativa de cada RESULT. En proporciones equivale a 1e−8 puntos porcentuales. En pesos es una fracción de centavo.
- **¿Qué sería peligroso leído simplista?** Leer que «ahora pasa» equivale a que las remesas estén bien medidas. La tolerancia nueva solo separa ruido de coma flotante de desacuerdo. La validez del estimando es otra pregunta (E.2) y esta spec no la toca.

El primer resultado que produzca este procedimiento es el que se reporta.
