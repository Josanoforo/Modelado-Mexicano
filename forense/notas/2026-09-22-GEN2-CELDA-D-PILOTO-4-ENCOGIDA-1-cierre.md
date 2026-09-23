# Piloto 4 · cierre de medición · 22/sep/2026

**Veredicto: FALSADOR DÉBIL en los cuatro cruces y en B-bis agregado.**
Se puntuaron las 38 celdas de `evasion_norma` ENVIPE 2025 (unidad DELITO,
FAC_DEL); ninguna quedó fuera de soporte 2025. C2 no fue vencido por C7
ni por C-ENCOGIDA. Este acto no adopta ni cambia el piso vigente.

## Secuencia y elegibilidad

- Spec humana `445531a3`; código y tests COMMIT-1 `5939e9d4`; corrección
  de semilla antes de emitir `c2eb888c`.
- COMMIT-2 `eb7f7c25`: emisiones selladas desde ENVIPE 2023/2024 y
  marginales 2025, con reserva del cruce 2025 probada (`DERIVADO=NO`).
  `verify` y proceso aislado: `REPRODUCE`, contexto `IDENTICO`.
- La enmienda `7ffa0a0e` documenta el plazo posterior de Jonás: C-ASTRA
  debía estar en `origin/main` antes de COMMIT-2. #1031 seguía abierto
  y sus cuatro CALC no estaban en main: la ventana se perdió. El HEAD
  avanzó de `7130ce2e5` a `159dc874` sin modificar los CALC científicos.
  La decisión posterior de Jonás habría permitido solo comparación
  secundaria, sin ampliar las ocho comparaciones primarias de B-bis;
  no se ejecuta aquí ni se incorpora a posteriori. Los 38 puntos ASTRA
  locales coinciden con el hash de sus `resultados.json`, pero su
  `admisibilidad.tsv` seguía `PENDIENTE-DE-CAJA`. El recibo paralelo
  `GEN2-RECIBO-ASTRA-1` de main invoca el plazo antiguo COMMIT-1;
  para este piloto prevalece la instrucción posterior y explícita de
  Jonás (antes de COMMIT-2). El resultado práctico de exclusión coincide.
- COMMIT-3a `3f066b33`: SHA256 de los dos insumos de COMMIT-2 fijados;
  `preflight VERDE` antes de abrir R. COMMIT-3 `de93beef`: R y
  adjudicación sellados. `verify` y proceso aislado: `REPRODUCE`,
  contexto `IDENTICO`; 685 RESULT, C2 recalculado coincide exactamente
  con el punto sellado. Los asientos están en `forense/replay-evidencia.tsv`
  y su evidencia aislada en
  `forense/analisis/gen2-celda-d-piloto-4-encogida-1/evidencia-replay.json`.

## Dictamen por cruce

`ΔMAE = MAE(C2) - MAE(retador)` en pp, con IC95 de réplicas comunes de R
y puntos emitidos fijos. El IC condicional despejaría victoria solo si
su límite inferior superara 0.5 pp. Los IC propios de las emisiones son
otro objeto. El conteo de celdas es descriptivo. No se emparejó ningún
sorteo ASTRA con R.

| Cruce | Puntuadas | n2025 min–max | MAE C2 pp | ΔMAE C7 pp (IC95) | ΔMAE C-ENCOGIDA pp (IC95) | B-bis |
|---|---:|---:|---:|---|---|---|
| dominio × sexo | 6/6 | 1 833–14 688 | 0.709 | 0.121 [−0.953, 1.014] | 0.307 [−0.773, 0.946] | FALSADOR-DÉBIL |
| edad × escolaridad proxy | 16/16 | 301–7 365 | 2.693 | 0.419 [−0.269, 1.018] | 0.351 [−0.067, 0.520] | FALSADOR-DÉBIL |
| edad × sexo | 8/8 | 2 156–7 992 | 0.426 | −0.187 [−0.640, 0.508] | 0.104 [−0.309, 0.335] | FALSADOR-DÉBIL |
| escolaridad proxy × sexo | 8/8 | 1 579–8 857 | 1.631 | 0.335 [−0.343, 0.789] | 0.439 [−0.197, 0.524] | FALSADOR-DÉBIL |

En los cuatro cruces el IC incluye cero para ambos retadores; al menos
un IC por cruce aún admite una mejora mayor de 0.5 pp. Por §3.1 de la
spec, el agregado es `FALSADOR-DEBIL`. La corrección de COMMIT-1 en
`7ffa0a0e` quitó la rama que habría declarado `GANA` por conteo de
celdas o por despejar solo cero. Se aplicó antes de abrir R.

## Controles y límites

El control de 13 marginales de ENVIPE 2025 en las emisiones dio
`DELTA-P-MAX=0` y `DELTA-IC-MAX=0.002801844`; su RESULT dice
`NO-REPRODUCE`. La causa es que `tools/celda_d/marginales_reproduccion.py`
calcula `ic95` marginal con `wprop_ic_conglomerado` dentro de
`_celda_estimada`, mientras el CALC de marginales sellado llama al
bootstrap propio `m._estimate`. El control compara IC obtenidos por
recetas distintas; el punto de C2 sí coincide exactamente. El IC de
ΔMAE del dictamen usa réplicas de R del árbitro, no ese IC marginal.
La discrepancia no cambia ninguna categoría de este piloto. Se conserva
el RESULT sellado y la reserva técnica sobre equivalencia de intervalos.

`spec-check` del árbitro: 11 variables OK. Tests del piloto: 12/12;
validador de celdas-D: 3/3. Cuatro celdas-D nuevas registran los cruces
y su `champion_actual: NINGUNO`. La vista del marcador se consultó en
modo lectura; no adopta ni levanta reserva automáticamente.

La primera ejecución de `corrida0 registro --escribe --lote` **paró sin
escribir** por `REPLAY-PISADO` (NC-0094): habría cambiado 26 campos de
replay de 13 corridas ajenas. Tras integrar `origin/main`, su nueva
función `_acota_vistas_al_lote` conserva byte a byte las filas ajenas
ya publicadas. El mismo comando escribió las vistas con los dos CALC
propios (`1 130 + 685` RESULT, replay `REPRODUCE/IDENTICO`). Se comprobó
que **0 filas de corridas o resultados previamente publicadas cambiaron**.
La proyección añadió también 25 885 RESULT nuevos de otros CALC que
ya estaban sellados en el árbol, por diseño del generador; cinco filas
`SPEC-FIJADA` ajenas pasaron a corridas efectivas. No se alteró ningún
RESULT ni sello científico ajeno.
