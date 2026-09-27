# Reconstrucción independiente ENBIARE 2021

Se utilizaron exclusivamente las entradas de `/entrada` y los insumos enumerados de `/raw`. No se consultaron resultados esperados, servicios externos ni al preparador. El commit de este directorio congela código propio, cifras y justificaciones antes de cualquier revelación; no se solicita revelación.

`reconstruccion.tsv` conserva las 180 llaves y todas las columnas originales. Tiene 126 razones puntuales `RECONSTRUIDO` y 54 filas `NO-RECALCULABLE-DESDE-SPEC`, sin cifras y con `motivo`. El estado principal se refiere a la estimación puntual; `estado_ic` y `motivo_ic` identifican por separado que ninguno de los 180 intervalos está determinado. No hay bloqueos de acceso ni filas sin intentar.

Se calcula sum(FAC_ELE × respuesta)/sum(FAC_ELE) por dominio, conservando como cadenas las llaves de persona, estrato y UPM. La unión usa exclusivamente FOLIO, VIV_SEL, HOGAR, N_REN y sólo llaves únicas en TSDEM. Las 31 166 personas elegidas tienen unión única y diseño válido. El grupo G-JOIN-SIN-SOCIODEMOGRAFICO tiene cero personas. No se imputó ninguna identidad.

## Límites de la especificación

- El diccionario `enbiare_2021_fd.pdf`, sección TSDEM, pregunta 4.4, identifica EDAD=96 como 96 y más, 97 como menor de 18 de edad no especificada, 98 como adulto de edad no especificada y 99 como no especificado. Existen siete personas con 98. Son adultos para el universo, pero no tienen tramo conocido. Las 48 filas de EDAD quedan sin cifra: excluirlos produciría un estimando condicionado a edad conocida, regla no establecida en el método. No se trata 98 como 98 años.
- Para CESD7, cinco de esos siete adultos tienen clasificación invariante a los dos cortes (puntaje menor de 5 o al menos 9); dos tienen puntaje 6. No se puede escoger su corte. Se dejan sin cifras otras seis filas CESD7 cuyos dominios contienen alguno de esos dos casos. No se excluyen esas respuestas para cambiar silenciosamente el denominador.
- El método pide bootstrap de UPM dentro de estrato, PCG64(20260924), 2000 réplicas y percentiles 2.5/97.5, pero alude a una «receta común por sha256» sin aportar su identidad o contenido y a un «contrato conservador» sin definición. Tampoco fija detalles que afectan los extremos a tolerancia 1e-10 (orden, muestreo, consumo del generador, percentiles y denominadores nulos). No se elige una receta alternativa ni se publican intervalos inventados. La parte de bootstrap no se ejecuta por especificación insuficiente, documentada en cada fila.
- Las 90 filas de seis escalas dicen unidad=proporcion en el TSV, pero metodo.md ordena explícitamente medias 0–10. Se conserva la etiqueta recibida y se añade `unidad_calculada=media` y una observación. No se divide entre diez ni se transforma en prevalencia.

## Identidades y fuentes humanas

Las identidades están expresamente fijadas en metodo.md y conductas.md y corroboradas por el diccionario de estructura y el cuestionario: A1/PA1 satisfacción; A5/PA5 escalera; B1/PB1_01 mayoría de la gente, PB1_02 gente conocida, PB1_04 policía municipal y PB1_11 partidos; B2/PB2_1 y PB2_2 apoyo familiar y amistades; D2/PD2_1–7 CESD7 con inversión de PD2_6 (disfrutó de la vida); D3/PD3_1–2 ansiedad; G6/PG6 religión y G7/PG7 asistencia. La secuencia G6=2 salta a H1; se codifica asistencia cero según el método. SEXO 1/2, NIVEL y TLOC se asignan por los códigos explícitos, nunca por posición o semejanza de cifras.

## Reproducción y custodia

Ejecutar desde este directorio:

```sh
python3 reconstruir.py
python3 verificar.py
```

Requiere Python, NumPy y pandas; las versiones usadas constan en `recibo.json`. Las rutas raw y PDF permanecen externas. `entradas/` conserva las entradas de texto y el manifiesto; `inventario.json` conserva rutas, tamaños y SHA-256 de todos los insumos, incluido el PDF del cuestionario, y de cada entrada interna del ZIP. No se incluyen microdatos, ZIP, PDF ni extracciones textuales de PDF en Git.

El SHA-256 de `/entrada/manifiesto.json` se conserva en `recibo.json`. El script valida los hashes contra el manifiesto y la lista de insumos antes de calcular. La verificación comprueba llaves, ausencia de números en estados no reconstruibles, custodia, límites CESD7, saltos religiosos y dos razones totales mediante aritmética entera independiente. `validacion.txt` registra esa comprobación y la repetibilidad byte a byte de los artefactos.
