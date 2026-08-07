# Síntesis consolidada del mapa externo · 2026-08-06

## Alcance y resultado

Se revisaron de manera dirigida fuentes generales, oficiales mexicanas,
académicas, internacionales, civiles y restringidas contra las necesidades
materiales del modelo. No se identificó una fuente adicional ya abierta y
mapeada que cambie automáticamente los cálculos vigentes. Sí se identificaron
fuentes cuya documentación debe abrirse antes de nuevas corridas.

El universo no pretende agotar todos los datos existentes para México. La
consolidación se limita a los cuatro carriles entregados y no abrió web,
microdatos, manifiesto, sellos, modelo ni datos de cálculo.

## Conteos y deduplicación

| Carril | Filas originales |
|---|---:|
| General | 17 |
| Oficial | 18 |
| Académico | 23 |
| Civil | 20 |
| Total antes de deduplicar | 78 |

Se consolidaron siete solapamientos de producto entre general y académico:
Banxico Competencias Financieras, Global Preferences Survey, ENCOAP, ISSP
Redes Sociales, ISSP Familia, CSES México 2018 y Mass Mobilization. Quedaron 71
fuentes o búsquedas únicas antes del filtro material. El mapa final conserva 40
filas: 15 A, 9 B, 10 D y 6 C. Las otras 31 fuentes únicas se excluyeron por no
superar el filtro material y no ser necesarias para evitar búsquedas repetidas.

No se colapsaron productos diferentes por compartir objeto. En particular:

- Cero Desabasto mide reportes ciudadanos y ASF audita desempeño y registros;
- LAOMS, Mass Mobilization, ACLED y GDELT difieren en unidad, curaduría,
  cobertura y granularidad;
- Banxico, IFT, Compartamos, Tanda+ y educación financiera observan piezas
  distintas del mecanismo financiero;
- IECM, CSES, el experimento electoral de 2009, Votar entre Balas e INE tienen
  diseños y unidades electorales diferentes; esta no-equivalencia se conserva
  como criterio de reconciliación y no como una fuente o metarregistro;
- ENASIC, ENUT, ISSP Familia e ISSP Redes Sociales no son equivalentes en
  constructo ni población.

## Correcciones y reservas materiales

- Enterprise Survey conserva su reserva: existe documentación de un archivo o
  componente denominado panel, pero no se afirma longitudinalidad efectiva
  hasta comprobar continuidad de empresas, llave estable, comparabilidad y dos
  observaciones por empresa. El corte 2023 no se presenta como panel.
- Compartamos no se trata como medición directa de `sens_estatus`: solo podría
  usarse así si el codebook exhibe un reactivo explícito.
- ENCOAP es urbano; no se generaliza automáticamente al México rural.
- Cero Desabasto carece todavía de esquema, denominador, cobertura, campaña,
  granularidad y sesgo de captación documentados; no permite aún calcular una
  tasa válida. ASF tampoco garantiza desagregación de unidad/campaña.
- Fuentes de eventos basadas en noticias no se intercambian con bases curadas
  de protesta ni con violencia político-criminal electoral.

## Quince prioridades A

1. ASF 165-DS: abrir PDF y anexos.
2. Banxico Competencias Financieras: abrir manual 2024.
3. IFT Servicios Financieros Digitales: abrir cuestionario.
4. Cero Desabasto: confirmar exportación.
5. Experimento electoral 2009: abrir codebook.
6. Enterprise Surveys panel 2006-2010: verificar llave longitudinal.
7. Compartamos RCT: comprobar texto literal del reactivo de estatus.
8. Evaluación de educación financiera: abrir codebook.
9. ISSP Redes Sociales 2017: abrir cuestionario.
10. ISSP Familia 2012: abrir cuestionario.
11. CSES México 2018: abrir codebook.
12. Mass Mobilization México: confirmar granularidad.
13. Votar entre Balas: verificar encabezados.
14. ENCOAP 2023/2025: abrir cuestionario.
15. Evaluación de educación inicial 2012-2014: abrir codebook.

Cada acción A se limita a documentación, esquema o encabezados. Ninguna
autoriza abrir microdatos.

## Decisiones A/B/C/D

- **A (15):** documentación de bajo costo con posibilidad inmediata de cambiar
  medición, identificación, magnitud o interpretación.
- **B (9):** fuentes materiales pero subordinadas a las A o sin encaje
  inmediato suficiente para gastar apertura en este lote.
- **C (6):** negativos o fuentes que no satisfacen el objeto; se conservan solo
  para evitar búsquedas repetidas y falsas equivalencias.
- **D (10):** GPS, LAOMS, Tanda+, Tanda Ahorro MX, Kantar, NielsenIQ, el estudio
  fintech privado, Mercer, ACLED y GDELT requieren decisión de mesa por acceso,
  contacto, licencia, costo o procesamiento.

## Búsquedas negativas y restringidas

Negativos importantes: no apareció otro panel mexicano hogar-crédito en los
repositorios revisados; no se localizó canal oficial de adquisición/referidos
fintech; México no aparece en la lista final revisada de ISSP Social Inequality
V 2019; UCDP no cubre protesta general; y no apareció denuncia enlazada con
tenencia de seguro. Estas conclusiones acotan el universo declarado, no afirman
inexistencia global ni cubren todo México.

Fuentes restringidas o sujetas a decisión: GPS, LAOMS, Tanda+/Tanda Ahorro,
Kantar, NielsenIQ, Mercer, ACLED y el estudio con fintech no identificada.
Méxicoleaks se excluyó: un microdato de denuncias no sería procedente para este
ciclo.

## Límites y siguiente lote

La revisión documental no verifica valores dentro de archivos, representatividad
no publicada, llaves efectivas ni comparabilidad empírica. Tampoco transforma
una asociación en identificación causal. El siguiente lote recomendado son las
15 aperturas de `data/cola-aperturas-externas-2026-08-06.tsv`, en ese orden,
aplicando la condición de paro de cada fila y sin abrir microdatos.
