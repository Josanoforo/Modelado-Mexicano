# ACTO GEN2-ENVIPE-VALIDACION-Y-LECTURA · cierre

Fecha: 10 de septiembre de 2026. Entorno: CAJA (Ubuntu/WSL2), corpus
compartido montado, cero descargas, cero llamadas a modelos y cero cambios al
motor. Encargo:
`forense/encargos/2026-09-10-GEN2-ENVIPE-VALIDACION-Y-LECTURA.md`.

## Resultado útil

Una segunda implementación reconstruyó los ocho puntos nuevos de ENVIPE con
`decimal.Decimal`, un lector dBase mínimo y la rama CSV de la biblioteca
estándar. No importa el medidor original, sus funciones estadísticas ni sus
2,000 réplicas bootstrap. Los ocho puntos, los ocho denominadores ponderados y
los ocho tamaños `n` coinciden con los CALC sellados; la diferencia máxima del
punto fue `4.27e-17`, frente a la tolerancia predeclarada `1e-10`.

El objeto validado es la proporción ponderada por `FAC_DEL` de motivos
`01/02/06` entre delitos personales no denunciados con respuesta `01..08`.
Es una composición de motivos con unidad delito. **No es tasa general de
denuncia, no es el complemento de RES-0028 y no se adopta al motor.**

| ola | año hecho | numerador `FAC_DEL` C1 | denominador `FAC_DEL` U1 | n U1 | punto | veredicto |
|---:|---:|---:|---:|---:|---:|---|
| 2011 | 2010 | 4 447 112 | 15 162 820 | 13 015 | 0.293290562046 | COINCIDE |
| 2014 | 2013 | 7 373 206 | 23 020 167 | 16 855 | 0.320293332364 | COINCIDE |
| 2016 | 2015 | 5 262 839 | 19 648 488 | 16 242 | 0.267849566847 | COINCIDE |
| 2017 | 2016 | 5 394 194 | 21 042 047 | 18 905 | 0.256353101008 | COINCIDE |
| 2018 | 2017 | 5 925 066 | 22 584 192 | 19 651 | 0.262354570843 | COINCIDE |
| 2019 | 2018 | 6 048 259 | 21 894 290 | 18 981 | 0.276248236412 | COINCIDE |
| 2020 | 2019 | 4 813 919 | 20 332 684 | 16 164 | 0.236757675475 | COINCIDE |
| 2022 | 2021 | 4 720 900 | 18 929 867 | 16 241 | 0.249388968237 | COINCIDE |

Trazabilidad completa, incluyendo SHA256, miembro ZIP, reactivo, referencias y
diferencias: `data/corrida0/envipe-validacion-independiente-v1_0.tsv`. El
embudo mutuamente excluyente y los excluidos por código están en
`data/corrida0/envipe-validacion-independiente-exclusiones-v1_0.tsv`.

## Instrumento, formatos e incertidumbre

La ficha oficial local `envipe2011/fd_envipe2011.xls`, hoja `TMod_Vic`,
confirma: `BP1_20` en filas 187–190; `BP1_21` y códigos `01..09`,
`88/98/99/blanco` en filas 191–204; `FAC_DEL` en fila 502; `EST/UPM` en
508–510. Su catálogo `BPCOD`, filas 25–39, separa los delitos de hogar `01..03`
de los personales `04..14`. La lectura física recuperó además `BP1_20=07` en
14 delitos personales; el embudo los excluye explícitamente en vez de tratarlos
como no denuncia. La otra rama DBF (2014) y las cuatro ramas CSV produjeron
masa, `n` y punto idénticos a sus referencias.

Para la ola 2019, la linealización directa de la razón por UPM dentro de
estrato dio `EE=0.00670985744423467`, idéntico al EE analítico sellado a la
precisión mostrada. El máximo desfase de extremos fue `2.42e-7`, muy por debajo
del umbral material de `0.002`; seis estratos de U1 tuvieron una sola UPM y se
trataron con aporte de varianza cero. El resultado es **CONCORDANTE**, pero no
se vende como reproducción del IC bootstrap: confirma por otra receta el
alcance analítico en un caso representativo. Tampoco prueba diferencias entre
años; eso exigiría especificar covarianza entre olas. Detalle:
`data/corrida0/envipe-validacion-independiente-incertidumbre-v1_0.tsv`.

## Lectura temporal descriptiva

La serie canónica cubre los años del hecho 2010–2024. Empieza alrededor de
29.3%, alcanza su máximo puntual exploratorio en 2013 (32.0%), desciende 6.39
puntos porcentuales hasta 2016, rebota 1.99 puntos hasta 2018 y cae 3.95 puntos
entre 2018 y 2019. Desde 2019 se mueve en una banda menor, aproximadamente
22.7%–24.9%; 2024 cierra en 23.2%, 6.16 puntos por debajo de 2010. El máximo de
2013 y la caída 2018→2019 son hallazgos exploratorios ya visibles, no contrastes
pre-registrados.

Cambios en mezcla de delitos, experiencia con autoridades, selección de quién
responde y condiciones de levantamiento son hipótesis compatibles, no causas
identificadas. La ola 2011 se marca por el nombre `BP1_21` y sus categorías
residuales propias; el núcleo sustantivo `C1/U1` se conserva, pero esa ruptura
limita una lectura automática de tendencia. Los IC mostrados son los bootstrap
publicados y su solapamiento no constituye prueba formal entre años.

Figura derivada exclusivamente del TSV canónico:

- `forense/notas/figuras/envipe-p-c1-u1-2010-2024.svg`
- `forense/notas/figuras/envipe-p-c1-u1-2010-2024.png`
- `forense/notas/figuras/envipe-p-c1-u1-2010-2024.pdf`

## Alcance y cierre

`NC-0155` cierra porque la reconstrucción cubre exactamente sus ocho puntos y
no es otro replay del medidor. Las specs y ejecuciones selladas conservan
retrospectivamente `validacion_independiente=NO-HECHA`; no se alteraron. El
asiento posterior aplicable es este expediente, su spec congelada, el script y
los tres TSV de evidencia. El control no crea ocho mediciones nuevas ni
acredita los otros 39 RESULT de cada CALC.

El consumidor `acto/gen2-publicacion-post693` existe como rama remota sin PR
localizado al cierre de esta ejecución. Los comprobantes quedan entregados en
esta rama y pueden consumirse por ruta estable tras el merge de mesa, sin
pisar evidencia ajena.
