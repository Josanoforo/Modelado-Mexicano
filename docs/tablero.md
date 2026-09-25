---
title: Tablero del programa
---

# Tablero del programa

[Portada]({{ '/' | relative_url }}) · [Verificar]({{ '/verificar.html' | relative_url }})

Este bloque lo escribe únicamente el job `guardias` de CI
(`.github/workflows/verify.yml`) sobre `origin/main`, en el mismo commit
`[deriva]` que actualiza
[`forense/tablero/TABLERO-PROGRAMA.md`](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/forense/tablero/TABLERO-PROGRAMA.md).
Esta página es una copia, no una segunda fuente: la escribe el mismo
comando (`tools/tablero_programa.py --actualiza`), en el mismo commit,
sobre el mismo árbol. Ver
[`docs/PROTOCOLO-TABLERO.md`](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/docs/PROTOCOLO-TABLERO.md)
para qué hacer (y qué no hacer) con lo que sigue.

<!-- TABLERO-DERIVADO:BEGIN -->
## Estado vivo derivado

- **Celdas validadas (métrica rectora, firma de mesa 20/sep/2026).** `219` celdas con predicción emitida antes de ver el dato y error sellado contra R (cruce `162` + persistencia `57`). **No es «N aciertos»: es N celdas con error CONOCIDO.** Tres clases, sin fundir:
  - *cruce vs R* · `DIN.ahorro_solo_informal.enif2024.localidad_x_edad` · n `8` · champion `C2` · error mediano `1.011` pp (máx `4.278` pp) · brecha `0` años (misma ola) · escala cruda del CALC `PROPORCION` · `data/corrida0/CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0002/resultados.json`
  - *cruce vs R* · `DIN.credito_k1.enif2024.marginal16` · n `16` · champion `PERSISTENCIA` · error mediano `4.747` pp (máx `4.747` pp) · brecha `0` años (misma ola) · escala cruda del CALC `AGREGADO-POR-CONDUCTA (sin grid de cruce; MAE_PP y N-CELDAS-PUNTUADAS del champion, no error por celda)` · `data/corrida0/CALC-DIN-CREDITO-PREDICCION-2024-ESCOLARIDAD-0002/resultados.json`
  - *cruce vs R* · `DIN.credito_k2_automotriz.enif2024.marginal16` · n `15` · champion `PERSISTENCIA` · error mediano `0.341` pp (máx `0.341` pp) · brecha `0` años (misma ola) · escala cruda del CALC `AGREGADO-POR-CONDUCTA (sin grid de cruce; MAE_PP y N-CELDAS-PUNTUADAS del champion, no error por celda)` · `data/corrida0/CALC-DIN-CREDITO-PREDICCION-2024-ESCOLARIDAD-0002/resultados.json`
  - *cruce vs R* · `DIN.credito_k2_departamental.enif2024.marginal16` · n `16` · champion `PERSISTENCIA` · error mediano `2.584` pp (máx `2.584` pp) · brecha `0` años (misma ola) · escala cruda del CALC `AGREGADO-POR-CONDUCTA (sin grid de cruce; MAE_PP y N-CELDAS-PUNTUADAS del champion, no error por celda)` · `data/corrida0/CALC-DIN-CREDITO-PREDICCION-2024-ESCOLARIDAD-0002/resultados.json`
  - *cruce vs R* · `DIN.credito_k2_nomina.enif2024.marginal16` · n `16` · champion `PERSISTENCIA` · error mediano `1.016` pp (máx `1.016` pp) · brecha `0` años (misma ola) · escala cruda del CALC `AGREGADO-POR-CONDUCTA (sin grid de cruce; MAE_PP y N-CELDAS-PUNTUADAS del champion, no error por celda)` · `data/corrida0/CALC-DIN-CREDITO-PREDICCION-2024-ESCOLARIDAD-0002/resultados.json`
  - *cruce vs R* · `DIN.credito_k3.enif2024.marginal16` · n `16` · champion `PERSISTENCIA` · error mediano `2.218` pp (máx `2.218` pp) · brecha `0` años (misma ola) · escala cruda del CALC `AGREGADO-POR-CONDUCTA (sin grid de cruce; MAE_PP y N-CELDAS-PUNTUADAS del champion, no error por celda)` · `data/corrida0/CALC-DIN-CREDITO-PREDICCION-2024-ESCOLARIDAD-0002/resultados.json`
  - *cruce vs R* · `DIN.credito_k5.enif2024.marginal16` · n `16` · champion `PERSISTENCIA` · error mediano `2.232` pp (máx `2.232` pp) · brecha `0` años (misma ola) · escala cruda del CALC `AGREGADO-POR-CONDUCTA (sin grid de cruce; MAE_PP y N-CELDAS-PUNTUADAS del champion, no error por celda)` · `data/corrida0/CALC-DIN-CREDITO-PREDICCION-2024-ESCOLARIDAD-0002/resultados.json`
  - *cruce vs R* · `DIN.credito_k6_p_tenedores.enif2024.marginal16` · n `16` · champion `PERSISTENCIA` · error mediano `4.462` pp (máx `4.462` pp) · brecha `0` años (misma ola) · escala cruda del CALC `AGREGADO-POR-CONDUCTA (sin grid de cruce; MAE_PP y N-CELDAS-PUNTUADAS del champion, no error por celda)` · `data/corrida0/CALC-DIN-CREDITO-PREDICCION-2024-ESCOLARIDAD-0002/resultados.json`
  - *cruce vs R* · `GOB.gobierno_digital.encig2025.edad_x_escolaridad` · n `15` · champion `C2` · error mediano `2.861` pp (máx `12.282` pp) · brecha `0` años (misma ola) · escala cruda del CALC `PUNTOS-PORCENTUALES` · `data/corrida0/CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001/resultados.json`
  - *cruce vs R* · `GOB.gobierno_digital.encig2025.edad_x_sexo` · n `8` · champion `C2` · error mediano `0.922` pp (máx `1.806` pp) · brecha `0` años (misma ola) · escala cruda del CALC `PUNTOS-PORCENTUALES` · `data/corrida0/CALC-ENCIG-DUELO-2025-ADJUDICACION-0002/resultados.json`
  - *cruce vs R* · `GOB.gobierno_digital.encig2025.escolaridad_x_sexo` · n `8` · champion `C2` · error mediano `0.868` pp (máx `2.014` pp) · brecha `0` años (misma ola) · escala cruda del CALC `PUNTOS-PORCENTUALES` · `data/corrida0/CALC-ENCIG-DUELO-2025-ADJUDICACION-0002/resultados.json`
  - *cruce vs R* · `TRA.evade_norma.envipe2025.escolaridad_x_dominio` · n `12` · champion `C2` · error mediano `1.224` pp (máx `5.436` pp) · brecha `0` años (misma ola) · escala cruda del CALC `PUNTOS-PORCENTUALES` · `data/corrida0/CALC-TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0002/resultados.json`
  - *persistencia t−1 vs R* · `ENCIG 2025 · encig2025_04_sec_7.csv · unidad = TRÁMITE (quien pagó doce veces contribuye doce veces)` · n `10` · error mediano `11.826` pp (máx `13.358` pp) · **brecha `2` años** · PERSISTE `0` / CAMBIA `10`
  - *persistencia t−1 vs R* · `ENIF 2024 · TMODULO.csv · unidad = PERSONA elegida 18+` · n `32` · error mediano `2.145` pp (máx `5.196` pp) · **brecha `3` años** · PERSISTE `16` / CAMBIA `16`
  - *persistencia t−1 vs R* · `ENVIPE 2025 · tmod_vic (conjunto_de_datos) · unidad = DELITO` · n `2` · error mediano `2.767` pp (máx `3.849` pp) · **brecha `1` años** · PERSISTE `2` / CAMBIA `0`
  - *persistencia t−1 vs R* · `ENVIPE 2025 · tmod_vic · unidad = DELITO` · n `13` · error mediano `2.34` pp (máx `5.361` pp) · **brecha `1` años** · PERSISTE `6` / CAMBIA `7`
  - *duelo de tres, nacional* · n `12` · MAE `M` `4.987` pp · `L_SOLO` `3.957` pp · `L_CORPUS` `3.889` pp · veredicto `SIN-GANADOR-UNICO` · NO se suma a las otras dos clases (otro universo, otro estimando) · `CALC-TRIADA-0002/resultados.json`
  - *sub-cifra del dominio DINERO* · cruce n `8` (error mediano `1.011` pp) · persistencia n `32` (error mediano `2.145` pp) · ENIF 2024; la brecha de persistencia es de 3 años y no se promedia con las de 1 y 2 años de ENVIPE/ENCIG
  - *NO cuentan* · `89` filas `IDENTICO` (M == R porque `EMISOR=ARBITRO`: el mismo número copiado, no una predicción contrastada) · `2` celdas de `formalidad` con piso y sin `error_piso_pp` (su error es un CALC sucesor) · universo examinado: 243 filas de data/corrida0/marcador-segmento.tsv + 3 CALC sellados
- **Procedencia.** SHA `3ed94f0b` · fecha del commit `2026-09-25` · ¿árbol == origin/main? `True`.
- **Motor.** reglas totales `25` · reglas con dato (>=1 conducta MEDIDO*) `24` · reglas sin dato `1` · conductas MEDIDO* `56` · tiers `{'FUERTE': 20, 'MEDIA': 5}`.
- **Marcador por segmento.** filas por estado: ADOPTADO-POR-FIRMA `52` · CONSUMIDA-SIN-PILOTO `1` · DIAGNOSTICO `8` · EVALUADA `57` · IDENTICO `89` · NO-COMPARABLE `2` · RESERVADA `19` · SIN-PISO `15` (total `243`) · cobertura de piso `111 / 243` · valor añadido / evaluadas `0 / 52` · celdas `emision = EMITIDA-SIN-EVALUAR` `13 / 243` · `veto_pisos_activo` `True`.
- **Corridas selladas que no cuentan todavía.** por `cuenta_gen2`: `False` 1 · `NO` 18 · `NO-DERIVACION-CONTEXTUAL` 1 · `NO-SIN-FIRMA-DE-OBJETO` 1 · `PENDIENTE-DE-CASCADA-DIFERIDA` 2 · `PENDIENTE-DE-INTEGRACION-SERIAL` 2 · `PENDIENTE-DE-MESA` 15 · `SI` 230 (selladas total `270`) · `PENDIENTE-DE-MESA`:
  - `CALC-EDER2017-PRIMERA-UNION-SEXO-COHORTE-0002--18e3c08247d5`: `NO-VERIFICADO`
  - `CALC-ENFIH2019-COBERTURA-SALDOS-CATPOS-0001--f22dc8014aec`: `NO-VERIFICADO`
  - `CALC-ENFIH2019-COBERTURA-SALDOS-CATPOS-0002--cd853c64a584`: `NO-VERIFICADO`
  - `CALC-ENIGH-DUELO-ORIGEN-MOVIL-0001--8cf894b01d4b`: `REPRODUCE`
  - `CALC-ENIGH2016-INTENSIDAD-REMESAS-0001--db3e1d99cc39`: `REPRODUCE`
  - `CALC-ENIGH2016-PERFIL-ESTRUCTURAL-0001--268b0658db7c`: `REPRODUCE`
  - `CALC-ENIGH2016-REMESAS-CONTEXTO-0001--d1a27b7d702b`: `REPRODUCE`
  - `CALC-ENIGH2018-INTENSIDAD-REMESAS-0001--f0d2fa594560`: `REPRODUCE`
  - `CALC-ENIGH2018-PERFIL-ESTRUCTURAL-0001--0a3f34eaea63`: `REPRODUCE`
  - `CALC-ENIGH2018-REMESAS-CONTEXTO-0001--4604b387eeb2`: `REPRODUCE`
  - `CALC-ENIGH2020-INTENSIDAD-REMESAS-0001--d41b466457b6`: `REPRODUCE`
  - `CALC-ENIGH2020-PERFIL-ESTRUCTURAL-0001--ff84ff36db65`: `REPRODUCE`
  - `CALC-ENIGH2020-REMESAS-CONTEXTO-0001--0fcfbe663035`: `REPRODUCE`
  - `CALC-RELEVO-ENCIG23-P83-0001-v1_1--66cfff97600b`: `REPRODUCE`
  - `CALC-WBES2023-PRECISION-INTERACCIONES-0001--7f2a0899f700`: `NO-VERIFICADO`
- **Corredor LEGACY (eje x = ∅, GO-MARCADOR).** el marcador por segmento es la línea de arriba. marco vigente `marco-M-v1_3` sorteado / `marco-M-v1_2` congelado (derivado del árbol) · celdas sorteadas `14` · celdas con M `14` · con R `14` · con L `14` · celdas puntuables (M∩R∩L) `14` · celdas sin cobertura completa `0`.
- **Corpus lógico.** entradas del manifiesto `2461` · filas de registro de curación `206` · filas de relaciones `231` · filas del inventario de reactivos v1.2 `178247`.
- **Gobernanza operativa.** ADR máximo del espacio numérico CERRADO `593` · FP máximo del mismo espacio `409` · ids con raíz de acto (época vigente) `{'ADR': 114, 'FP': 139, 'NC': 361}` · FP abiertas: FP-260921-GEN2-CORPUS-INTEGRIDAD-Y-RESPALDO-1-3d56-01, FP-260923-GEN2-TRAMITE-FIRMAS-12-c3fa-05, FP-260923-GEN2-FRONT-1-4296-01, FP-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-01, FP-260925-GEN2-CATALOGO-V1-1-1-afe1-01 · encargos archivados `753` (consumidos `675`) · instrucciones vigentes `v2.16` · cola de encargos (solo estados != CONSUMIDO; consumidos `61`):
  - `2026-09-07-ENCARGOS-GEN2-en-orden.md`: GATED
  - `2026-09-08-GEN2-SONDA-3-PILOTO-CAJA.md`: LISTO
  - `2026-09-10-GEN2-POST-685/00-LEEME-LANZAMIENTO-POST-685.md`: GATED
- **NC abiertas por razón (token A.14, prefijo exacto).** abiertas `356` · por token: `DECISIÓN-DE-MESA-PENDIENTE` 46 · `DIFERIDO-A` 82 · `FUERA-DE-PERÍMETRO` 57 · `NO-VERIFICABLE-AQUÍ` 19 · `PARO-ENTORNO` 2 · `PARO-PREMISA` 34 · `SUSTITUIDO-POR` 5 · prosa (sin token reconocible) `111`.
- **GEN2 (derivado de `corrida0 status`, valores EN ÁRBOL; vistas del árbol distintas de HEAD: `data/corrida0/corridas.tsv, data/corrida0/resultados.tsv, data/corrida0/pines-sellados-resueltos.tsv, data/corrida0/usos.tsv, data/corrida0/marcador-segmento.tsv`).** adoptados activos `128` · pendientes de adopción `10` · corridas selladas `272` / requeridas `87` · resultados sellados `79352` / activos `211` · pendientes `211` · dependencias numéricas legacy activas `137` · validación independiente `215` · diferencias materiales `0` · NC- abiertas `356` · replays LEGACY-GEN1 sellados `5` (no cuentan). El `0 / N` es la lectura correcta: el aparato se construyó antes que las corridas.
- **Legacy activas por consumidor (desglose aditivo del contador de arriba).** motor `25` · procedencia `40` · catalogo de momentos `23` · marco del duelo `43` · celdas D `6` · otro `0` — suman `137`, el total. Los cinco consumidores son RELEVABLES: ninguno se declara fuera del contador. Cuántos de ellos ya tienen medición GEN2 sellada que la vista no enlaza se deriva en `forense/analisis/relevo-reconcilia-1/reconcilia-173-v1_0.tsv`.
- **Relevadas por pin de mesa, por vía (firma 4.1, 21/sep/2026 — las clases NO se funden).** vía (i) desde insumo crudo con hash `14` · vía (ii) lectura de una conducta ya GEN2 `13`. Marco del duelo, lo que sigue legacy por campo: R `0` · M `1` · L `28` · AGREGADO `14`. Celdas M todavía legacy, **nombradas**: `DIN-M-01` — `DIN-M-01` es el recordatorio de que `tiene_ahorros` espera el acceso a ENNViH. El canal vive en `data/corrida0/pines-de-mesa.tsv` y cada fila pasa las cuatro guardas de 4.1 antes de mover el contador (`T32-quater T-PINES-MESA`).
- **GEN2 · medición vs. adopción (ACTO GEN2-PRE-E5 · P3).** sellados `78747` · pendientes de adopción (citados en la propuesta, ningún consumidor activo aún) `10` · vetados por decisión vigente (sellados, pero una firma prohíbe adoptarlos: no son cola) `4` · adoptados por un consumidor activo `128`. Sellar un RESULT no mueve `dependencias_numericas_legacy_activas` por sí solo: solo el consumidor activo que lo adopta la baja.
- **Fuentes.** `milpa/tramite.yaml`, `milpa/tramite-ola5-propuesta-v0.yaml`, `milpa/procedencia.yaml`, `forense/prereg-duelo-v2/` (marcos y corridas M/R/L), `data/manifiesto.yaml`, `data/curacion-registro/cola-adquisicion-registro.tsv`, `data/curacion-registro/relaciones.tsv`, `data/inventario-reactivos-v1_2.tsv`, `canon/gobernanza-v1_15.md`, `forense/firmas-pendientes.tsv`, `forense/encargos/*.md`, `forense/encargos/cola/*.md`.

**Protocolo vigente.** La actualización factual de este bloque se hace con:

```
git fetch origin
python3 tools/tablero_programa.py --actualiza
python3 tests/check.py --baseline
```

El humano solo actualiza la interpretación (las tablas curadas §2.1-2.5 y la narrativa) cuando hay una decisión o un hallazgo que valga la pena registrar. Las recetas antiguas del snapshot histórico (p. ej. `git branch -r` o `awk '$6=="ABIERTA"'`) NO gobiernan esta actualización -- son historia, no el mecanismo vigente.

<!-- TABLERO-DERIVADO:END -->
