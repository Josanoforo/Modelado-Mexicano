# Recibo · CALC-ISSP2017-REDES-APOYO-COTIDIANO-0001

## Identidad

- Worktree: `/home/pc0/mm-gen2-issp2017-redes-apoyo-cotidiano-cli-1`.
- Rama: `codex/gen2-issp2017-redes-apoyo-cotidiano-cli-1`.
- Base `origin/main`: `8e455bd6a3870566d6776fef19834c4da16d2fa9`.
- COMMIT-1 de congelamiento: `b6365529136d86851034ef7a8bf36209452dc66b`.
- COMMIT-2 de ejecución/resultados/sello: `999c8b7`.
- Corrida: `CALC-ISSP2017-REDES-APOYO-COTIDIANO-0001--b6365529136d`.
- Spec YAML: `9cb213fdbd4889353103715f0399e82df76995f9da226ce54b49807f12e039df`.
- Medidor: `d5ed6e8cb3467ac06435ead0445e610483bfbdb5f954788cad184a8b7c5a2cf4`.
- Sello: `1fabda5512179a1e32a8a1d00d6c710a3b4b7b2834cbfc988b90bec8b76c705f`.

## Secuencia ejecutada

```bash
python3 -m unittest tests.test_issp2017_redes_apoyo_cotidiano
python3 tools/corrida0.py spec-check CALC-ISSP2017-REDES-APOYO-COTIDIANO-0001
python3 tools/corrida0.py preflight CALC-ISSP2017-REDES-APOYO-COTIDIANO-0001
python3 tools/corrida0.py run CALC-ISSP2017-REDES-APOYO-COTIDIANO-0001
python3 tools/corrida0.py verify CALC-ISSP2017-REDES-APOYO-COTIDIANO-0001
python3 data/corrida0/CALC-ISSP2017-REDES-APOYO-COTIDIANO-0001/control_independiente.py \
  --dta-zip '/mnt/c/Users/PC0/Descargas MX/ZA6980_v2-0-0.dta.zip' \
  --distribution forense/analisis/issp2017-redes-apoyo-cotidiano-cli-1/distribucion-item-sexo.csv \
  --family forense/analisis/issp2017-redes-apoyo-cotidiano-cli-1/agregado-familia-item-sexo.csv \
  --counts forense/analisis/issp2017-redes-apoyo-cotidiano-cli-1/conteo-situaciones-ninguno.csv \
  --matrix forense/analisis/issp2017-redes-apoyo-cotidiano-cli-1/matriz-coocurrencia-ninguno.csv \
  --output forense/analisis/issp2017-redes-apoyo-cotidiano-cli-1/control-independiente.json
python3 tools/corrida0.py registro --lote CALC-ISSP2017-REDES-APOYO-COTIDIANO-0001
```

Resultados: 7/7 pruebas sintéticas; spec-check 14/14; preflight VERDE; run
exit=0; sello COINCIDE; verify `REPRODUCE/IDENTICO` para 22/22 RESULT y 5/5
inputs; control separado `CONTROL-INDEPENDIENTE-OK`, delta máximo
`4.93e-13`.

## Registro

El registro se ejecutó en seco. Proyecta exactamente 1 corrida y 22 RESULT
propios, pero también 20 filas de `usos.tsv` ajenas a este encargo (adopciones
de pisos C2). Escribir habría ampliado el perímetro y aceptado derivados
ajenos. Por ello no se usó `--escribe`; la publicación canónica queda
**PENDIENTE** con el asiento dirigido ya agregado a `forense/replay-evidencia.tsv`.

No se modificaron `corridas.tsv`, `resultados.tsv`, `usos.tsv`, milpa, motor,
canon, decisiones, NC globales, workflows ni el CALC monetario. No hubo merge
ni adopción. `cuenta_gen2=PENDIENTE-DE-MESA`.
