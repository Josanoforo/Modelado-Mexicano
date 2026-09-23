# ENCUP · dictamen de peso y diseño de la base 2012 y bases disponibles

Acto `ASTRA5-U3-POLITICA-COMPLETAR` (0-bis `d459637e`), 23/sep/2026, CAJA.
Sucede a la NC `NC-260923-ASTRA5-U3-POLITICA-df0d-02` de #1084. Esa NC
decía «peso, estrato y UPM no verificados en el XLSX/descriptor
disponible»; aquí se verifica y se corrige lo que decía.

## Qué trae la base 2012

Payload `encup_2012_base_datos_xlsx` (`data/raw/encup_2012_base_datos_xlsx.xlsx`,
resuelve COINCIDE). Se leyeron sólo los nombres de cabecera de la hoja
`BaseDatos_ENCUP_2012_Final` (3 751 filas × 282 columnas) y las etiquetas de
texto de `Hoja1`, que es la lista de preguntas. Columnas de diseño y peso,
por posición 0-based:

| posición | cabecera | lectura |
|---:|---|---|
| 1 | `Punto` | punto de muestreo; la nota GEN1 `2026-09-01-MAESTRA33-E18-P3-L1-spec.md:486` habla de 375 puntos |
| 2 | `Folio` | identificador de entrevista |
| 4 | `Estado` | entidad |
| 6 | `Municipio` | municipio |
| 7 | `Seccion` | sección electoral |
| 8 | `Tipo de seccion` | tipo de sección |
| 10 | `Número de intentos antes de obtener un éxito:` | registro de campo |
| 280 | `factor` | peso sin definición documentada |
| 281 | `POND` | segundo peso sin definición documentada |

**Corrección a df0d-02:** la base **sí** trae dos columnas de peso, `factor`
y `POND`, igual que ya lo leyeron `forense/hitoD-R8_1-veredicto-v1_0.md:44`
y la nota E18-P3-L1. En cambio, **no** trae ninguna variable de estrato de
diseño.

## Documentación buscada

- **Corpus**: `find -L` sobre `data/raw`, la raíz `descargas_mx` y
  `mm-corpus` con el patrón `encup|cultura.?pol|culturademo|cultdemo|practicas.?ciudad`.
  Resultado: la base 2012 más los cuestionarios 2001, 2003, 2005, 2008 y
  2012. Ningún documento metodológico, nota técnica ni descriptor de
  diseño. Control positivo: el mismo comando lista
  `encup_2012_base_datos_xlsx.xlsx`. En el manifiesto, la búsqueda por
  id/archivo/url con `encup|cultura.?pol|fomentocivico|cultdemo` da 6 ids
  ENCUP (una base y cinco cuestionarios) y 5 ids de la encuesta UNAM.
- **Cuestionario 2012** (`encup_2012_cuestionario_pdf`, pdftotext, 1 179
  líneas): el patrón `muestr|ponder|factor|expansi|estrat|diseño|margen|metodolog`
  no devuelve ninguna línea. Control positivo: `SECCION` aparece una vez,
  en la carátula de identificación (ESTADO, DISTRITO, MUNICIPIO, SECCION,
  TIPO_SEC). El cuestionario no describe el diseño.
- **Internet, sólo para el faltante documental concreto**:
  - Búsqueda web: encuentra la metodología ENCUP **2008** de INEGI
    (`sm_encup08.pdf`), que es otra ola y no tiene base en el corpus. No
    encuentra una nota metodológica 2012.
  - `en.www.inegi.org.mx/programas/encup/2012/`: devuelve sólo un
    encabezado, un cascarón SPA sin documentos.
  - `fomentocivico.segob.gob.mx`: `curl` falla con
    `TLS connect error … unexpected eof`, y falla igual con el control
    positivo, el PDF del cuestionario 2012 que sí se bajó el 4/ago.
  - Resultado: **NO-ACCESIBLE** desde esta caja el 23/sep/2026.
    **NO OBTENIDO POR ESTE AGENTE EN 3 INTENTOS**. Receta manual de un
    minuto: abrir `https://fomentocivico.segob.gob.mx/es/FomentoCivico/ENCUP`
    en un navegador y buscar «metodología 2012» o «nota técnica».

## Dictamen

**Falta diseño acreditable.** Lo que falta, exactamente:

1. Un documento que defina `factor` y `POND`: cuál es el factor de
   expansión, cuál está normalizado, respecto de qué población y con qué
   ajuste de no respuesta o posestratificación.
2. La variable, o la regla documentada, de estratificación.
3. La confirmación de que `Punto`, o `Seccion` dentro de `Estado`, es la
   unidad primaria, y de sus probabilidades de selección.
4. Fechas de levantamiento y tasa de respuesta.

Por eso no se ponderan tasas ni se calculan IC de diseño. `factor` y `POND`
no se usan, porque elegir uno sin documento sería inventar el ponderador.
`CALC-ENCUP-PISOS-2012-0003` (#1084) se conserva como descripción de
entrevistados sin representatividad poblacional ni por entidad. No se abre
CALC ENCUP nuevo.

## Otras bases disponibles

- **ENCUP 2001, 2003, 2005 y 2008**: sólo hay cuestionario, sin base de
  datos. No existe serie ENCUP y no se fabrica una.
- **UNAM-IIJ, «Encuesta Nacional de Cultura Política»** (colección *Los
  mexicanos vistos por sí mismos*; ids `encuesta_nacional_de_cultura_politica*`
  y `descripcion_bases_*`): es **otro instrumento** con otro productor. No
  es ENCUP y no se le atribuyen preguntas ENCUP. Igual que WVS y ENCUCI,
  requiere contrato y asignación propios; aquí no se abre.
