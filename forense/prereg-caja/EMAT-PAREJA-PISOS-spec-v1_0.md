# Pisos de nupcialidad registrada por segmento, EMAT 2010–2023 · spec v1.0

**Pre-registro de caja.** `ACTO GEN2-COLA-LOTE-1`, 25/sep/2026, CAJA, rama `acto/gen2-cola-lote-1`,
0-bis `3a49c186`. Encargo: `forense/encargos/2026-09-25-GEN2-COLA-LOTE-1.md` (pieza P-EMAT). CALC:
`CALC-EMAT-PAREJA-PISOS-0001`. Congelada en el COMMIT-1 de EMAT, **antes** de leer un solo registro
de `MATRIyy.dbf` (sólo descriptores PDF y cabeceras DBF: nombre/tipo/largo de campo).
**El primer resultado que produzca este procedimiento es el que se reporta.**

## 0 · Premisas verificadas

- `[EJECUTADO]` «¿Encuesta de Matrimonio?» (encargo §1): **no**. EMAT es la *Estadística de
  Matrimonios* de INEGI, registro administrativo de los matrimonios civiles inscritos (descriptores
  `descripcion_bd_matrimonios_2010.pdf` … `DBD_Matrimonios_2023.pdf`, dentro de cada ZIP). Unidad:
  matrimonio registrado; no observa uniones libres ni disoluciones (los divorcios son otro registro).
  La lista del encargo «edad a la unión, unión libre vs matrimonio, disolución» se sustituye por lo
  que las cinco afirmaciones PAREJA piden y el registro sostiene (§2). INTERPRETACIÓN-DECLARADA.
- `[EJECUTADO]` Olas en corpus por identidad: `emat2010_2014_bd_dbf_zip` (MATRI10–14),
  `emat2015_2019_bd_dbf_zip` (MATRI15–19), `emat2020_bd_dbf_zip` … `emat2023_bd_dbf_zip`. 2024
  (`cc1_inegi_emat_2024__…`) es la más reciente: **E.6 — RESERVADA**, no es input (guardia).
  2013 y 2014 existen dentro del ZIP 2010–2014.
- `[EJECUTADO]` Estructura de `MATRIyy.dbf` idéntica en las 14 olas (33 campos, cabeceras DBF).
  Códigos por texto del descriptor 2010 y 2023, iguales: `SEXO_CON1/2` 1 Hombre 2 Mujer; `EDAD_CON1/2`
  12…98, 99 No especificada; `GENERO` «Género de matrimonio» 1 hombre–mujer 2 mismo sexo;
  `CONACTCON1/2` «si el o la contrayente trabaja o no al momento del matrimonio» 1 Trabaja 2 No trabaja
  9 No especificada; `ESCOL_CON1/2` 1 Sin escolaridad · 2 1–3 primaria · 3 4–5 primaria · 4 Primaria
  completa · 5 Secundaria · 6 Preparatoria · 7 Profesional · 8 Otra · 9 No especificada; `TAM_LOC_RE`
  17 rangos + 99; `ANIO_REGIS` año de registro (no hay campo de celebración distinto).
- `[EJECUTADO]` PAREJA-002 (tasa de nupcialidad por mil habitantes de 18+) exige población: no hay
  denominador en corpus → no se construye aquí (NC). PAREJA-001/030 comparan con 2013: 2013 está
  abierta y entra en la serie.

## 1 · Unidad, naturaleza, universo

Registro completo: **sin diseño muestral, sin EE ni IC de diseño**; cada celda es P exacta del
registro, N (universo) y CONTEO (numerador). Matrimonio: todas las filas vivas del DBF.
Contrayente: cada matrimonio aporta dos filas (`*_CON1`, `*_CON2`). Diagnósticos por ola: filas,
`ANIO_REGIS` distinto de la ola, `GENERO` fuera de {1,2}, edades 99/fuera de rango, sexo fuera de
{1,2}.

## 2 · Conductas (por texto)

Matrimonio: M-MISMO-SEXO (`GENERO`=2; universo 1–2) · M-CON-MENOR-18 (algún contrayente de 12–17;
universo: ambas edades válidas, o la condición se cumple) · M-AMBOS-TRABAJAN (ambos `CONACT`=1;
universo ambos en 1–2) · M-MISMA-ESCOLARIDAD (`ESCOL_CON1`=`ESCOL_CON2`; universo ambos en 1–7).
Contrayente: C-EDAD-MEDIA (media de edad 12–98) · C-EDAD-{12-19, 20-24, 25-29, 30-34, 35-39, 40-MAS}
(proporción; universo edad válida) · C-TRABAJA (`CONACT`=1; universo 1–2).

## 3 · Ejes (uno a la vez)

Matrimonio: TOTAL · ENT (entidad de registro, 32) · TLOC (localidad de registro: <2 500 = rangos
1–3; 2 500–14 999 = 4–6; 15 000–99 999 = 7–12; 100 000+ = 13–17). Contrayente: TOTAL · SEXO ·
ESCOLARIDAD (primaria o menos 1–4 / secundaria 5 / preparatoria 6 / profesional 7) · TLOC.

## 4 · Persistencia

14 olas: τ² por conducta × eje × categoría (proporciones) = media de Δ² en logit entre olas
consecutivas con p ∈ (0,1) (`tau2` de la receta común). IC calibrado sobre el piso 2023:
expit(logit p ± 1.959964·√τ²) — ee de diseño nulo por ser registro. Parámetro reutilizable
(ids `-TAU2`, `-ICC-LO/-HI`).

## 5 · Controles

Sintético en `tests/test_cola_lote_1_pisos.py`. Control post-sello, sin tocar el procedimiento:
CONTEO de M-MISMO-SEXO 2023 frente a 6 606 (PAREJA-012) y N total 2022 frente a 507 052
(PAREJA-001): el comunicado INEGI y la base pueden diferir por cierre de edición; se reporta la
diferencia, no se ajusta.

## 6 · Auditoría (afirma sobre México)

**Registro ≠ conducta:** mide matrimonios *inscritos* por año de registro; la caída del
registro no es caída de la unión (la unión libre no está). **Unidad:** matrimonio y contrayente son
unidades distintas, ids distintos. **Edad media**: del contrayente al registrar, todas las nupcias
(no distingue primeras). **Cifra escrita a mano:** ninguna.

El primer resultado que produzca este procedimiento es el que se reporta.
