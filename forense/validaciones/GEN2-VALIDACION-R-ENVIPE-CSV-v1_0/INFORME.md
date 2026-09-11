# Informe v1.0 · validación independiente de tres R ENVIPE CSV

**Fecha:** 11 de septiembre de 2026

**Protocolo fijado antes del contraste:** `PROTOCOLO.md`, commit `3896dc5`

**Comando:**

```bash
python3 forense/validaciones/GEN2-VALIDACION-R-ENVIPE-CSV-v1_0/valida_r_envipe.py --write
```

## Veredicto ejecutivo

1. **Validación del punto: `VALIDADO` en 3/3.** Una implementación nueva,
   escrita desde la definición, reconstruyó exactamente identidad, unidad
   DELITO, filtros, `n`, numerador, denominador y punto de los tres R.
2. **Concordancia numérica de la incertidumbre histórica: `CONCUERDA` en
   3/3.** La linealización independiente reproduce los tres EE al orden de
   redondeo de `float64`; los extremos de IC difieren como máximo
   `2.48e-12`, dentro de la tolerancia fijada `2e-10`.
3. **Aptitud inferencial del IC histórico: `NO APROBADA`.** Sus 19/33/20
   estratos de UPM única aparecen después de restringir al dominio `U_R` y
   los 72 dejan de ser singleton al conservar las UPM observables de
   `TVivienda` con contribución cero. No son unidades de certeza acreditadas.
   La documentación oficial tampoco identifica esos estratos concretos como
   certeza.
4. El diagnóstico que conserva las UPM de `TVivienda` cambia los EE, pero es
   **sucesor reproducible, no reemplazo retrospectivo**: los archivos públicos
   de vivienda contienen menos registros que las viviendas seleccionadas que
   documenta INEGI y no incluyen un roster explícito de todas las UPM
   seleccionadas. Por ello no se afirma que el marco de UPM recuperado sea
   completo.

El resultado correcto no es “todo validado”: los puntos quedan validados; el
EE/IC publicado queda reproducido numéricamente y no aprobado para inferencia.

## Resultado por celda

| celda | ENVIPE / hechos | `n` | numerador `Σwy` | denominador `Σw` | punto reconstruido | EE histórico reconstruido | IC95 histórico reconstruido | CV | delta punto / EE contra productor |
|---|---|---:|---:|---:|---:|---:|---|---:|---|
| `CIV-M-10` | 2021 / 2020 | 32 967 | 5 417 077 | 26 433 277 | `0.20493399286059008` | `0.004773432921089039` | `[0.195578236253, 0.214289749469]` | 2.3293 % | `0` / `0` |
| `CIV-M-12` | 2023 / 2022 | 31 012 | 5 298 762 | 25 461 157 | `0.20811159524290275` | `0.004760266232118153` | `[0.198781644871, 0.217441545615]` | 2.2874 % | `0` / `-8.67e-19` |
| `CIV-M-13` | 2024 / 2023 | 33 108 | 5 816 411 | 29 887 247 | `0.19461180215093080` | `0.005391415046889411` | `[0.184044822833, 0.205178781469]` | 2.7703 % | `0` / `0` |

`concordancia_numerica = CONCUERDA` y `validacion_punto = VALIDADO` en las
tres. Los IC de la tabla son la reconstrucción con
`z=1.959963984540054`; los congelados usan extremos que difieren sólo entre
`2.19e-12` y `2.48e-12`.

## Identidad y documentación

Los tres ZIP coinciden en SHA-256 y tamaño con `data/manifiesto.yaml`. El
ejecutable exige una coincidencia literal única del miembro; también hashea el
diccionario y el catálogo internos, y verifica las siete columnas decisivas.

| celda | SHA-256 miembro `TMod_Vic` | SHA-256 diccionario interno | SHA-256 catálogo `BP1_23` |
|---|---|---|---|
| `CIV-M-10` | `a742559fb3d541742ecfd3e65ba019933821fcd92f175530f9748828f4470052` | `ae8a882c88c55c60649bf5fda9ff6f36c7e53269b84adbbdfcbaaf786e57b186` | `a86e80d92a2df176887867b817cf2b6e6e39e564fb243a6ba28a73a2f4cb8562` |
| `CIV-M-12` | `d8cccc7b221b838c391888a24ff965438e66566d6e7250e3bc43b4ac290d4b4d` | `4ab1747a38defdc1373165cf36df24e6c450d702f40cd7e43bbf179eb629dfc8` | `cac94baad1536d099fcfa23359eab1f6086adfb21b3ae2bd77eeac6f8612cd2a` |
| `CIV-M-13` | `74fa26a0b27452db87fa136ebb2678e54746cb0692cf0c4e6d14e3abda48b262` | `8eca6eb0cb557fe2e92af02da9dc6c6098872cead1cf0c0d06e7682c3039d078` | `f6d5c8b979853f727df6e3b9ae63749c9ec37b7dcb56fd2aebecdf7c8ce19390` |

Los cuestionarios de módulo locales coinciden con sus hashes del manifiesto y,
en la página PDF 4 de cada ola, `1.23` pregunta la razón principal de no
denuncia; los catálogos confirman `01..09` y `99`. Los descriptores locales
también coinciden con sus hashes. La metodología primaria consultada fue el
diseño muestral oficial de [ENVIPE 2021](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463902454.pdf),
[ENVIPE 2023](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463912637.pdf)
y [ENVIPE 2024](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463920014.pdf):
diseño probabilístico, estratificado y por conglomerados; estimador de razón y
precisión por Taylor/conglomerados últimos.

## Embudo y frecuencias

| etapa | `CIV-M-10` | `CIV-M-12` | `CIV-M-13` |
|---|---:|---:|---:|
| filas `TMod_Vic` | 37 156 | 35 135 | 37 614 |
| `BPCOD` fuera de `01..15` | 0 | 0 | 0 |
| `BP1_23` blanco | 3 962 | 3 957 | 4 262 |
| `BP1_23=99` | 227 | 166 | 244 |
| otro código | 0 | 0 | 0 |
| `FAC_DEL` inválido/no positivo después de códigos | 0 | 0 | 0 |
| sin `EST_DIS`/`UPM_DIS` | 0 | 0 | 0 |
| **`n(U_R)`** | **32 967** | **31 012** | **33 108** |

Las frecuencias completas de `BP1_23` y `BPCOD 01..15` están en
`frecuencias-codificacion.tsv`; el embudo reproducible, incluidos ceros, está
en `embudo.tsv`. El cero del código `09` permanece dentro del denominador y no
se agregó `BP1_20=2`.

La unidad DELITO también queda comprobada empíricamente: `U_R` contiene
19 953/19 252/19 071 personas distintas; 6 807/6 363/6 900 tienen varios
delitos incluidos y el máximo por persona es 23/24/24. Cada `ID_DEL` es único.
No hubo colapso a persona.

## Diagnóstico de diseño

| celda | UPM en `U_R` / `TMod_Vic` / `TVivienda` | singleton en `U_R` / `TMod_Vic` / `TVivienda` | UPM recuperadas por `TVivienda` | filas `TVivienda` / viviendas seleccionadas oficiales |
|---|---|---|---:|---|
| `CIV-M-10` | 9 903 / 10 332 / 13 195 | 19 / 17 / 0 | 3 292 | 90 335 / 102 297 |
| `CIV-M-12` | 9 745 / 10 183 / 13 085 | 33 / 31 / 0 | 3 340 | 90 383 / 102 362 |
| `CIV-M-13` | 9 654 / 10 096 / 13 080 | 20 / 19 / 0 | 3 426 | 88 020 / 102 287 |

Los 72 singleton de `U_R` tienen más de una UPM en su estrato al mirar
`TVivienda`; por tanto aparecen al restringir el dominio. Ninguna UPM de
`U_R` o `TMod_Vic` falta entre las UPM observadas en `TVivienda`. Eso permite
el diagnóstico siguiente, con puntuación cero para UPM sin observaciones en
`U_R`:

| celda | EE histórico | EE diagnóstico `TVivienda` | delta EE | IC95 diagnóstico |
|---|---:|---:|---:|---|
| `CIV-M-10` | `0.004773432921` | `0.004776073762` | `+0.000002640841` | `[0.195573060299, 0.214294925422]` |
| `CIV-M-12` | `0.004760266232` | `0.004778981578` | `+0.000018715346` | `[0.198744963467, 0.217478227019]` |
| `CIV-M-13` | `0.005391415047` | `0.005395422216` | `+0.000004007169` | `[0.184036968927, 0.205186635375]` |

En estos datos el EE sube entre 0.06 % y 0.39 %, pero esa dirección es un
resultado, no una propiedad. El autocontrol manual del protocolo demuestra que
añadir una UPM de contribución cero también puede reducir el EE. Por eso se
retira la caracterización histórica de “límite inferior garantizado”.

La reserva restante es precisa: `TVivienda` acredita todas las UPM observadas,
pero no trae el roster de selección. Sus filas son 11 962/11 979/14 267 menos
que las viviendas seleccionadas documentadas por INEGI. Esa diferencia puede
ser no respuesta dentro de UPM ya representadas; con lo disponible no se puede
demostrar que ninguna UPM seleccionada completa falte. Falta ese componente,
no el punto ni la reconstrucción numérica del EE histórico.

## Independencia del cálculo y reproducibilidad

El código reutiliza sólo biblioteca estándar para ZIP, CSV y SHA-256. No
importa ni copia `medidor.py`, `tools/arbitra.py`,
`tools/valida_envipe_independiente.py` o
`tests/svystat.py:prop_ultimate_cluster`. Antes del corpus prueba pesos
desiguales, exclusiones, varios delitos por persona, estratos/UPM y singleton.

Dos ejecuciones consecutivas produjeron hashes idénticos:

| artefacto | SHA-256 |
|---|---|
| `evidencia.json` | `6889d0853f55d16ebafe7e45a13f5ec68ceadaa532b0d9aab060fd5d6289b48b` |
| `resumen.tsv` | `bd5d394f19f4ffd9253bda6cd365249ec344276c8de90f82389ca921b1aa67ba` |
| `frecuencias-codificacion.tsv` | `6c54ed3c83e28c0c728e67be64f0bfa46c7846c3982a77b51ca69563e6c1e937` |
| `embudo.tsv` | `f2664bac3312a4baadeff0e58d07a01b104a5c2cdeb03baad20651d3949f5b15` |

## Cierre y residual

`NC-0096` puede cerrar por validación formal ejecutada con veredicto completo:
los tres puntos están validados y la incertidumbre histórica está contrastada.
Ese cierre **no aprueba** el uso inferencial de los IC.

Tras la fusión de `PR #710`, la validación queda vinculada al contrato común
mediante `data/corrida0/validaciones-independientes.tsv`, overlay por RESULT
que verifica referencia y SHA sin reescribir specs ni resultados sellados. La
vista publica 9 RESULT `PASA` (punto, n y denominador de cada ola) y 12
`CONCUERDA-NO-APROBADA` (EE, extremos de IC y CV). El contador
`resultados_con_validacion_independiente` pasa de 0 a 9; no es un contador de
mediciones ni habilita confirmación retenida.

Queda un residual separado:

- `NC-0159`: acreditar el roster completo de UPM seleccionadas —o un servicio oficial de
  varianza— y ejecutar prospectivamente el estimador de dominio que conserva
  contribuciones cero. El diagnóstico `TVivienda` es la propuesta reproducible
  que cambia sólo ese componente.

Ningún `CALC`, spec, resultado o sello congelado fue modificado; ninguna
adopción o firma de consumidor se infiere de esta validación.
