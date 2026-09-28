# Auditoría de los lotes de lectura · GEN2-MAPA-INSTRUMENTOS-ALTERNOS-1

Los cuatro archivos `lote_{A,B,C,D}.tsv` los recolectaron lectores en Sonnet (uno por lote), leyendo solo el texto extraído con `pdftotext -layout` de documentos del corpus y el índice `tools/busca_reactivos.py`. Ninguno abrió bases ni leyó cifras. El dictamen de cada fila del mapa lo emitió el hilo principal (Opus), no los lectores. La columna `verifica_en` del mapa apunta a `lote_X:i`, que es la fila `i` (base 0, sin contar la cabecera) de estos archivos.

## Verificación hecha por el hilo principal

- Muestra de verbatim contra la fuente, con página: lote A (9.2 y 9.3 de ENCRIGE, p. 20; 6.1 de ENVE, p. 9; 1.19 del módulo ENVE, p. 3; 10.8 de ENCRIGE, p. 23), lote B (EXC18 en las tres olas de LAPOP; `BP1_23` en el FD de ENVIPE 2025, p. 73, y de 2026, p. 75; `SEGUR3M`, p. 11), lote C (`MEX_2018` en el codebook, l. 5469; `E3016_1`; notas de país de `E3012_LH`/`E3012_UH`, l. 18831 y 18977; `P104` en los catálogos de ENIGH 2020 y 2022) y lote D (`P6_1_5` de ENSAFI; `AP6_3_12`, `AP7_3_5`, `AP7_9` y `AP7_14` de ENCUCI; CoDi en ENDUTIH).
- Verificación mecánica de las 49 filas del mapa que traen texto de pregunta: cada fragmento aparece en el documento fuente (texto plegado); 0 fallas. Control positivo: una pregunta inventada, sembrada en la fila 2, se detecta como falla.

## Correcciones a lo que dijeron los lectores

1. **Lote D, fila 20 (M19, ENCUCI 2020): el NO-ENCONTRADO es falso.** El FD de ENCUCI 2020 (Secc. V, p. 24–25) trae la batería 5.1 «¿cuánto confía en…?» en escala de 0 a 10: `AP5_1_1` «la mayoría de las personas», `AP5_1_2` «la mayoría de las personas que conoce», `AP5_1_3` «… que viven en…» y `AP5_1_4` «los servidores públicos». El mapa usa esta batería. La frase del lector se conservó y se rotuló como CORREGIDA.
2. **Lote B, M05 (ENCIG): faltó la experiencia de corrupción.** El lector trajo percepción (3.2, 3.3) y confianza (A.1), pero no la sección VIII: `P8_1`, `P8_2` («¿Recuerda a algún conocido… que haya vivido una experiencia…?»), `P8_3_1..P8_3_3` y `P8_4` por trámite (estructura 2023, p. 35–36 y 61; 2025, p. 37 y 62). La agregó el hilo principal.
3. **Lote A, fila 35 (ENVE 2016): el «esquema» traía unos 12 registros de muestra.** El extractor del hilo principal incluyó los miembros `*_esq_2016.csv`, que además de encabezados traen filas de ejemplo. Es la ola 2016 (no reservada; ENVE figura como EXPUESTA en F5 E04). No se derivó ninguna cifra y el texto se recortó a los encabezados.
4. **A.4, dos frases «No existe…»** en notas de lector (lote C, catálogo ENIGH 2018; lote D, M19) se reescribieron como NO-ENCONTRADO al archivarlas aquí. Es el único cambio frente a los archivos del scratchpad.
5. **Lote D, barrido «CoDi».** `--palabra CoDi` pliega y encuentra «código» (2 171 candidatas). El hilo principal repitió la búsqueda con `--regex "Cobro Digital|\(CoDi\)"`: 15 candidatas (ENIF 2021 `P7_2`; ENIF 2024 `P7_2_1`/`P7_3_1`; ENDUTIH 2023/2024/2025 `P7_32_6`).
