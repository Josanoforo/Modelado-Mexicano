# Pisos por segmento ENDISEG 2021 (orientación sexual, identidad de género, perfil de la población LGBT+) · spec v1.0

**Pre-registro de caja.** `ACTO GEN2-COLA-COMPLETA-1`, 26/sep/2026, CAJA, rama `acto/gen2-cola-completa-1`,
0-bis `0d4ae74d`. Encargo: `forense/encargos/2026-09-26-GEN2-COLA-COMPLETA-1.md` (§1 (a), cola v1.1:
PAREJA/ENDISEG, GENERO/ENDISEG). CALC: `CALC-ENDISEG-PISOS-2021-0001`. Congelada en el COMMIT-1, **antes** de
leer un solo valor de ENDISEG (sólo el descriptor de archivos y la línea de cabecera de los CSV).
**El primer resultado que produzca este procedimiento es el que se reporta.**

## 0 · Premisas verificadas

- `[EJECUTADO]` Payload `endiseg2021_bd_csv_zip` (manifiesto), sha256 `aca2fad1…` COINCIDE; miembro
  `TMODULO.csv` (cuestionario individual de la persona seleccionada). Descriptor: `endiseg2021_fd_pdf_zip`,
  miembro `ENDISEG 2021 Descriptor de archivos (FD).xlsx` (sha256 del miembro `14ff4781…`), hoja `TMODULO`.
- `[EJECUTADO]` Una sola ola del instrumento: la ENDISEG web 2022 (`cc1_inegi_investigacion_2022__endiseg_web_2022_*`)
  es otro instrumento (encuesta web, no probabilística) y no es input. E.6: se abre 2021 y se declara; sin IC de
  persistencia.
- `[LEÍDO]` El FD no trae una variable derivada «LGBTI+»; INEGI la opera combinando 7.1, 8.1 y 9.1 (filtro
  `FILTRO_10_5`). La definición de §2 es de esta spec.

## 1 · Unidad, universo, diseño

Unidad: **persona seleccionada de 15+** (`P4_1` 15–96). Peso `FACTOR` de TMODULO (FD: 77–88053, factor de la
persona seleccionada; no el de TSDEM). Bootstrap de UPM `UPM_DIS` dentro de estrato `EST_DIS`. Válido: peso > 0,
estrato y UPM no vacíos.

## 2 · Conductas (por texto de pregunta, FD hoja TMODULO)

| conducta | pregunta (texto del FD) | UNO | CERO |
|---|---|---|---|
| ORIENTACION-NO-HETEROSEXUAL | «8.1 Conforme a lo anterior, ¿usted se considera...» (`P8_1`: 1 mujer a la que le gustan solamente las mujeres · 2 hombre al que le gustan solamente los hombres · 3 persona que le gustan tanto hombres como mujeres · 4 mujer que le gustan solamente los hombres · 5 hombre que le gustan solamente las mujeres · 6 con otra orientación) | 1, 2, 3, 6 | 4, 5 |
| IDENTIDAD-NO-CISGENERO | «9.1 Usted se considera:» (`P9_1`: 1 hombre · 2 mujer · 3 tanto hombre como mujer · 4 ni hombre, ni mujer · 5 de otro género) contra «7.1 ¿Cuál es su sexo asignado al nacer?» (`P7_1`: 1 Hombre · 2 Mujer) | `P9_1` ∈ {3,4,5}, o `P9_1` ∈ {1,2} distinto de `P7_1` | `P9_1` = `P7_1` |
| LGBT | derivada: UNO si cualquiera de las dos anteriores es UNO; CERO si ambas son CERO | | |
| VARIACION-INTERSEXUAL | «7.1a ¿Usted nació con alguna variación en su cuerpo referente a su sexo, como en genitales, niveles hormonales u otro?» (`P7_1A`) | 1 Sí | 2 No |
| MEDIA-SUPERIOR-O-MAS | «4.11 ¿Hasta qué año y grado aprobó en la escuela? - NIVEL» (`NIV` 00–10) | 06–10 | 00–05 |
| SOLTERO / UNION-LIBRE / CASADO | «4.2 ¿Actualmente, usted...» (`P4_2`: 1 vive en unión libre · 2 está casada(o) · 3 separada(o) · 4 divorciada(o) · 5 viuda(o) · 6 soltera(o)) | 6 / 1 / 2 | el resto de 1–6 |

Todo otro código (no entiende, no especificado, blanco) queda fuera. LGBT no incluye la variación intersexual
(se mide aparte); la cifra del report (5.1 %) se compara como orden, declarado.

## 3 · Ejes (uno a la vez)

TOTAL · SEXO-AL-NACER (`P7_1`) · EDAD (`P4_1`: 15–19, 20–29, 30–44, 45–59, 60+) · ESCOLARIDAD (`NIV`: hasta
primaria 00–02, secundaria 03–05, media superior 06–07, superior 08–10) · CONYUGAL (`P4_2`: unido 1–2, alguna vez
unido 3–5, soltero 6) · INDIGENA-AUTOADSCRITO (`P4_7` «4.7 Por sus costumbres y tradiciones, ¿usted se considera
indígena?» 1/2) · AFRO-AUTOADSCRITO (`P4_4` 1/2) · LGBT (derivada SI/NO) · ENTIDAD (`ENT` 01–32). El FD no trae
tamaño de localidad (sólo `EST_DIS`, opaco): no hay eje de localidad.

## 4 · Estimación

Razón ponderada Σw·y/Σw con bootstrap de UPM dentro de estrato (UPM única del estrato = de certeza),
`PCG64(20260926)`, 2 000 réplicas, bloques de 50, percentiles 2.5/97.5, contrato conservador (una réplica
degenerada → sin EE ni IC). Receta común por sha256: `tools/dominios/salud/pisos_diseno.py` + motor
`tools/dominios/confianza/motor_pisos.py`. Un eje a la vez; nunca cruces.

## 5 · Controles, secuencia

Sintético en `tests/test_cola_completa_pisos_gen2.py` (todas las ramas terminales por `corrida0._valida_outputs`;
derivada LGBT sobre cuatro casos a mano; guardia que PARA si la ENDISEG web 2022 entra como input). Ninguna
ejecución diagnóstica sobre el dato: la primera corrida es `corrida0 run`.

## 6 · Auditoría (afirma sobre México)

**Escala y unidad:** proporciones de personas de 15+; ninguna se promedia con otra unidad. **Autoidentificación ≠
conducta:** declarar una orientación o identidad en entrevista cara a cara depende del contexto de revelación
(presencia de familiares, región, edad); una prevalencia más alta entre jóvenes es primero disposición a declarar,
no «cambio generacional» de la orientación. **Estructura ≠ cultura:** la soltería o la escolaridad de la población
LGBT+ reflejan edad (más joven) y selección, no «rasgos». **Indígena/afro:** autoadscripción como marcador social
declarado, nunca ascendencia → conducta (firewall genético); el eje se lee como exposición a discriminación
cruzada. **Evidencia:** (a) datos primarios en México. **Temporalidad:** RETROSPECTIVO; ninguna cifra PROSPECTIVA.
**Cifra escrita a mano:** ninguna.

El primer resultado que produzca este procedimiento es el que se reporta.
