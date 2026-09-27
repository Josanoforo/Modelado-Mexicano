# Propuesta de tolerancias C1 lote2

PROPUESTO-POR-EJECUTOR · NUEVO · PENDIENTE-DE-ADOPCIÓN. No modifica contratos congelados ni simula tolerancia previa. No se ejecutó comparación ni se miraron diferencias.

Opción recomendada: mesa adopta antes de entregar objetivos la siguiente regla para estos ocho paquetes. Proporciones, medias e intervalos se conservan en su escala nativa, declarada en estimandos.tsv.

- Conteos enteros: identidad exacta.
- Puntos deterministas de razón ponderada: error absoluto ≤ 1e-8 en escala nativa; no convertir proporción a porcentaje sin declarar factor100.
- Intervalos/EE de bootstrap: 1e-8 sólo si el método humano fija inequívocamente orden de población/UPM/estrato, RNG, semilla, número de réplicas y percentil. La misma semilla sin el mismo plan no satisface la regla.
- Cuando falta identidad de plan aleatorio, estos campos quedan NO-EVALUADO hasta contrato nuevo de equivalencia estadística escrito y adoptado antes de revelar objetivos. Esta propuesta no inventa un umbral de equivalencia estadística ni acredita toda incertidumbre con la tolerancia del punto.

Fundamento: precisión numérica para funciones deterministas sobre mismos insumos autorizados; incertidumbre de simulación requiere contrato propio. El criterio no depende de diferencias observadas, ni se usa para modificar mediciones anteriores.

| paquete | estimadores originales | acción documental restante |
|---|---:|---|
| endutih-empleo-15mas-2023-0001 | 46 | Cuestionario oficial adquirido, cobertura por P2/P3 |
| endutih-empleo-15mas-2024-0001 | 46 | Sin faltante documental original |
| endutih-empleo-15mas-2025-0001 | 46 | Cuestionario oficial adquirido, cobertura por P2/P3 |
| endutih-pisos-2023-0001 | 470 | Cuestionario oficial adquirido, cobertura por P2/P3 |
| endutih-pisos-2024-0001 | 470 | Sin faltante documental original |
| endutih-pisos-2025-0001 | 470 | Cuestionario oficial adquirido, cobertura por P2/P3 |
| mociba-pisos-2016-0001 | 126 | Cuestionario oficial adquirido, cobertura por P2/P3 |
| mociba-pisos-2017-0001 | 123 | Cuestionario oficial adquirido, cobertura por P2/P3 |

Firma propuesta: «Adopto, antes de revelar valores objetivo de estos ocho paquetes, tolerancia determinista y condiciones de identidad de bootstrap arriba. Los campos aleatorios sin plan idéntico no se comparan hasta criterio independiente previo. No declaro tolerancia preexistente ni adopto resultados.»
