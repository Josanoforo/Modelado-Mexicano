# ENCUCI 2020 · respuesta por contacto

`CALC-ENCUCI2020-RESPUESTA-POR-CONTACTO-0001` quedó sellado en la corrida
`CALC-ENCUCI2020-RESPUESTA-POR-CONTACTO-0001--2790c096241f`. El payload
`encuci2020_bd_dbf` coincidió con SHA-256 `0414fd59…f283`. Marco: 21,519
personas, masa 96,427,583, `ID_PER` única, 281 estratos y 3,096 UPM; IC95 por
2,000 bootstrap UPM dentro de estrato. Las tablas completas procesables,
incluidos IC, masas y denominadores, están como JSON determinista en
`resultados.json` bajo los tres RESULT tabulares.

| Contacto | n | Cob. % | Ninguna % | Sólo sol. % | Sólo ent. % | Ambas % | Unión % |
|---|---:|---:|---:|---:|---:|---:|---:|
| Policía/tránsito | 4,087 | 99.89 | 72.70 | 11.22 | 3.64 | 12.44 | 27.30 |
| Ministerio Público | 1,331 | 99.90 | 71.91 | 11.91 | 3.71 | 12.46 | 28.09 |
| Jueces | 853 | 99.97 | 73.64 | 10.67 | 2.47 | 13.22 | 26.36 |
| Salud pública | 9,084 | 99.90 | 87.56 | 5.01 | 2.13 | 5.30 | 12.44 |
| Educación pública | 7,244 | 99.94 | 88.32 | 4.77 | 2.08 | 4.83 | 11.68 |
| Seguridad social/bienestar | 2,632 | 99.96 | 84.54 | 6.16 | 2.69 | 6.61 | 15.46 |
| Gobierno municipal/alcaldía | 3,629 | 99.95 | 81.35 | 7.75 | 2.68 | 8.22 | 18.65 |
| Gobierno estatal/federal | 2,429 | 99.74 | 79.39 | 7.91 | 2.72 | 9.97 | 20.61 |
| Guardia Nacional | 810 | 99.80 | 71.36 | 12.59 | 4.72 | 11.33 | 28.64 |
| Ejército/Marina | 781 | 99.76 | 68.77 | 13.51 | 5.14 | 12.58 | 31.23 |

Las diferencias Sí−No de unión van de −2.08 pp (educación) a 21.95 pp
(policía/tránsito); se presentan completas, con covarianza del mismo sorteo,
en `RESULT-ENCUCI2020-RPC-CONTRASTES-POR-CONTACTO`. Son diferencias de perfil
de persona: los contactos pueden coexistir, y AP5_17/18 no identifican quién
solicitó o recibió ni una misma transacción. Por tanto no son tasas, rankings
ni atribuciones a las autoridades.

`RESULT-…-SOLAPAMIENTO-OTROS-CONTACTOS` entrega 0/1/2+ otros contactos y la
diferencia de cobertura con el subconjunto de vector completo para cada tipo;
explicita el solapamiento que impide interpretar los renglones como universos
de autoridad. Las identidades de partición y unión quedaron en cero (salvo
redondeo float). Prueba sintética: OK; `spec-check`: 16/16 campos OK;
preflight: VERDE. No se abrió otro instrumento ni se hizo adopción o contador:
ambos quedan PENDIENTE-DE-MESA.

## Sucesión v1_1 y control independiente

El sello de `...-0001` se preserva. `CALC-ENCUCI2020-RESPUESTA-POR-CONTACTO-0001-v1_1`
publica `RESULT-ENCUCI2020-RPCV11-VALIDACIONES-POR-CONTACTO`: las diez
particiones son exactamente 0 y las identidades de unión están entre
−5.55e−17 y 5.55e−17 (redondeo binario).

Control independiente reproducible: `python3
forense/analisis/encuci2020-respuesta-por-contacto-cli-2/control_independiente_encuci2020_respuesta_por_contacto.py`.
Lee el DBF y agrega UPM directamente, sin invocar el estimador de proporciones.
Corrige el control previo: construye primero el marco de las 3,096 UPM con
`FAC_SEL` válida; el dominio aporta cero fuera de contacto con salud pública y
AP5_17/18 válidas. Por estrato centra los residuos `z=y-px` y aplica
`m/(m−1) * sum((z−z̄)^2)`.

La salida acredita el estimando publicado `P(solicitud o entrega | contacto
salud pública, AP5_17/18 válidas)`: punto independiente
`0.12442225665637696`, punto RESULT idéntico, delta `0.0`, tolerancia absoluta
`1e-12`, varianza WR `3.8998399149224755e-05` y SE
`0.006244869826443523` (281 estratos). Es control de punto y varianza del
diseño, no una sustitución de los IC bootstrap sellados ni una modificación del
sello anterior.

## Replay y vistas

La verificación oficial dirigida al sucesor
`CALC-ENCUCI2020-RESPUESTA-POR-CONTACTO-0001-v1_1--796156326e60` concluyó
`REPRODUCE` con `CONTEXTO=IDENTICO`: 12/12 RESULT y 1/1 input coinciden. Se
ejecutó sin el límite transitorio de 30 segundos, primero en intérprete
aislado y después mediante la interfaz de registro dirigida:

```text
python3 tools/corrida0.py registro --verifica --escribe --lote CALC-ENCUCI2020-RESPUESTA-POR-CONTACTO-0001-v1_1
```

La evidencia aislada está en
`forense/analisis/encuci2020-respuesta-por-contacto-cli-2/evidencia-replay-dirigido-v1_1.json`.
El asentador propio validó sus huellas de spec, script e input frente a la
corrida sellada antes de incorporar el asiento a
`forense/replay-evidencia.tsv` (fila del sucesor). La proyección canónica se
publicó con:

```text
python3 tools/corrida0.py registro --escribe --lote CALC-ENCUCI2020-RESPUESTA-POR-CONTACTO-0001-v1_1
```

Escribió `corridas.tsv` (229 filas), `resultados.tsv` (8,954) y `usos.tsv`
(228). Las vistas referencian `VERIFY-DIRIGIDO … replay-evidencia.tsv#…v1_1`,
por lo que la corrida SELLADA queda acreditada como `REPRODUCE/IDENTICO`, no
como `NO-VERIFICADO/SIN-FUENTE`. El sello histórico de `...-0001` permanece
sin alteración; no hay adopción ni fusión.
