# Pisos por segmento ENADID 2009 / 2014 / 2018 (hogares, arreglos de residencia, vejez, pareja, migración) · spec v1.0

**Pre-registro de caja.** `ACTO GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1`, 25/sep/2026, CAJA,
rama `acto/gen2-familia-cuidados-y-migracion-pisos-1`, 0-bis `2a0ebb63`. Encargo:
`forense/encargos/2026-09-25-GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1.md` (P2). CALC:
`CALC-ENADID-FAMILIA-HOGARES-0001`. Congelada en el COMMIT-1, **antes** de leer un solo
valor de registro de ENADID (sólo cabeceras y descriptores de campo). **El primer resultado
que produzca este procedimiento es el que se reporta.**

## 0 · Premisas verificadas

- `[EJECUTADO]` ENADID en el manifiesto por id: 2009 (`cc1_inegi_enadid_2009__base_datos_enadid09_dbf`),
  2014 (`cc1_inegi_enadid_2014__base_datos_enadid14_dbf`), 2018 (`enadid2018_bd_csv_zip`),
  2023 (`enadid2023_base_datos_csv`, reservada), además de 1992/1997 (fuera, lista §1).
  Presentes en `data/raw` (A.13: 3 archivos examinados por ruta del manifiesto).
- `[EJECUTADO]` Estructura: `forense/analisis/familia-migracion/estructura-instrumentos.md`.
- `[EJECUTADO]` Lo ya medido se cita (E.5): `CALC-ENADID-0001`,
  `CALC-ENADID2023-UNION-SEXO-EDAD-0001..0004`; ninguno deriva las conductas de §2.
- **E.6:** ENADID 2023 reservada para estas conductas (lista §1, INTERPRETACIÓN-DECLARADA).
  El medidor PARA si un id `enadid2023*` llega como input.

## 1 · Unidad, universo, diseño

Dos unidades, declaradas y nunca promediadas entre sí: **hogar** (tabla de hogares) y
**persona residente** (tabla sociodemográfica). Factor `FAC_VIV` (el único publicado),
estrato `ESTDIS`(2009)/`EST_DIS`, UPM `UPM_DIS` (llaves opacas). Hogar válido: factor > 0,
estrato y UPM no vacíos. Persona: se toma factor, diseño, tamaño y clase de hogar de su
hogar por llave (`LLAVE_HOG`; 2009 `CONTROL`+`VIV_SEL`+`HOGAR`); llave repetida en la tabla
de hogares o persona sin hogar válido → fuera (`G-<ola>-PERSONA-SIN-HOGAR`).

## 2 · Conductas (por texto)

Tabla en `forense/analisis/familia-migracion/lista-cerrada-P1.md` §2 (ENADID), parte de
esta spec: 5 de hogar y 6 de persona, todas proporciones. `CLS_HOG` 2009 se lee quitando
la «H» inicial. Edad válida 0–130 (999 fuera).

## 3 · Ejes (uno a la vez)

Lista cerrada §3. Escolaridad: 2014/2018 HASTA-PRIMARIA {00,01,02}, SECUNDARIA {03, 05
técnico con secundaria}, MEDIA-SUPERIOR {04 normal básica, 06, 07}, SUPERIOR {08–11};
2009 HASTA-PRIMARIA {00–02}, SECUNDARIA {03}, MEDIA-SUPERIOR {04 preparatoria, 05 normal,
06 técnica}, SUPERIOR {07–09}; 99 y blanco fuera. TLOC: 2014/2018 1 ≥ 100 mil … 4 < 2 500;
2009 invertido (4 ≥ 100 mil … 1 < 2 500). Condición de pareja: unido (casado o unión libre)
/ no unido (demás códigos válidos).

## 4 · Estimación

Razón ponderada Σw·y/Σw con bootstrap de UPM dentro de estrato (UPM única = certeza,
`PCG64(20260925)`, 2 000 réplicas, percentiles 2.5/97.5, bloques de 50, contrato
conservador), receta común `tools/dominios/salud/pisos_diseno.py` por sha256; lectores
`tools/dominios/familia/lectores.py` por sha256. **IC calibrado de persistencia** (método
de `CALC-ENIF-PERSISTENCIA-IC-CALIBRADO-0001`, igual que #1124): τ² por (conducta, eje) =
media de Δ² en logit entre olas consecutivas 2009→2014→2018; IC = expit(logit p ±
1.96·√(ee_m² + τ²)) sobre el piso 2018. Conducta con < 3 olas (migración: 2014, 2018) → sin
IC calibrado.

## 5 · Controles, secuencia

Sintético en `tests/test_familia_pisos_gen2.py` (DBF y CSV fabricados con los mismos
miembros y columnas; todas las ramas terminales por el conducto que sella). Oro: no hay
piso GEN2 previo de estas conductas en ENADID 2009–2018 (`ls data/corrida0 | grep -ic enadid`
= 5 al COMMIT-1, todos 2023 o `CALC-ENADID-0001`). Ninguna ejecución diagnóstica.

## 6 · Auditoría (afirma sobre México)

**Contadores:** este CALC cuenta (`cuenta_gen2: SI`, `adopta: NO`). **Escala/unidad:** hogar
y persona nunca se mezclan; «vive solo» es de personas 60+, «unipersonal» de hogares.
**Estructura ≠ cultura:** un hogar ampliado o un joven de 30 que vive con sus padres es
primero vivienda, ingreso y mercado laboral (adaptación racional posible), no «familismo»;
la nota no lo lee como rasgo. **Clase:** gradiente por escolaridad del jefe = estructura.
**Rural/urbano:** TLOC siempre al lado. **Marcos importados:** «familismo» es evidencia (b) —
no se usa para leer estos pisos (a). **Unión libre:** su alza es un cambio de forma legal de
la unión, no evidencia de inestabilidad por sí sola. **Firewall genético:** ninguna
segmentación por ascendencia. **Cifra a mano:** ninguna.

El primer resultado que produzca este procedimiento es el que se reporta.
