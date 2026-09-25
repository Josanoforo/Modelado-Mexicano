# Pisos de canal de compra y conectividad por segmento, ENGASTO 2012 · spec v1.0

**Pre-registro de caja.** `ACTO GEN2-CONSUMO-Y-GASTO-PISOS-1`, 25/sep/2026, CAJA, rama
`acto/gen2-consumo-y-gasto-pisos-1`, 0-bis `2d37b23b`. Encargo:
`forense/encargos/2026-09-25-GEN2-CONSUMO-Y-GASTO-PISOS-1.md` (P2). CALC:
`CALC-ENGASTO-CONSUMO-PISOS-0001`. Congelada en el COMMIT-1, **antes** de leer un solo valor
de microdato ENGASTO (sólo FD y metadatos `.dta`). **El primer resultado que produzca este
procedimiento es el que se reporta.**

## 0 · Premisas verificadas

- `[EJECUTADO]` El encargo dice «ENGASTO 28 payloads» como una canasta. Por identidad son
  **dos olas** (`lista-cerrada-P1.md` §1): 2012 (`engasto2012/`, casa con
  `engasto12_fd.pdf`) y 2013 (`engasto2013/`, sin FD en corpus). **E.6: 2013 RESERVADA.**
  Inputs 2012: `engasto2012_hogar_dta`, `engasto_2012_vivienda_dta`,
  `engasto_2012_lugar_compra_dta`, `engasto2012_gasto_de_consumo_ajustado_dta` (sha256 en
  `spec.yaml`). La medidora PARA si una ruta resuelve a `engasto2013/`.
- `[SUPUESTO→EJECUTADO]` «ENGASTO trae factores y diseño por trimestre» (encargo §3): el FD
  2012 trae `factor_hog` (HOGAR) y `factor_viv`, `est_dis`, `upm` (VIVIENDA); las llaves
  llevan `anio_reg` y `trimestre`, pero el factor es **uno** por hogar y los resultados del
  FD están «anualizados a un año tipo de 365 días» (Anexo A). **Unidad temporal declarada:
  la ola entera (levantamiento 2012 por trimestres), un piso por segmento, no por
  trimestre.**
- `[EJECUTADO]` Llaves: `anio_reg`, `trimestre`, `folio`, `hog_ent_1`, `hog_ent_2` son
  texto (`string`) en las cuatro tablas.

## 1 · Unidad, universo, diseño

Unidad: **hogar** (HOGAR), ponderador `factor_hog`; estrato `est_dis` y UPM `upm` de VIVIENDA
por `anio_reg`+`trimestre`+`folio`. LUGAR_COMPRA por la llave de hogar. Sexo, edad y
escolaridad del jefe (`sexo_je`, `edad_je`, `ned_je`, construidas por INEGI según FD) de
`gasto_de_consumo_ajustado`, una fila distinta por hogar; hogar con valores inconsistentes
entre filas → fuera del eje (`G-JEFE-INCONSISTENTE`). Válido: `factor_hog > 0`, estrato y UPM
no vacíos. Uniones sólo por llaves únicas; no pareados en `G-JOIN-SIN-*`.

## 2 · Conductas (por texto)

`lista-cerrada-P1.md` §3, parte de esta spec: 8 GRAN-COMPRA-*, 10 {producto}-EN-{formato},
COMPRA-INTERNET-ALGUN-RUBRO, COMPRA-INTERNET-SI-CONEXION, TIENE-CELULAR, CONEX-INTERNET (22
proporciones de hogares). Códigos de lugar 01–18; 97 «No especificado» y nulo («no se
realizó la compra», FD) fuera del universo.

## 3 · Ejes (uno a la vez)

TOTAL · SEXO-JEFE · EDAD-JEFE · ESCOLARIDAD-JEFE (`ned_je`, 4 niveles INEGI) · TLOC;
`lista-cerrada-P1.md` §5. Sin DECIL (ENGASTO 2012 no trae ingreso).

## 4 · Estimación

Proporción ponderada con bootstrap de UPM dentro de `est_dis` (certeza para UPM única,
`PCG64(20260925)`, 1 000 réplicas, percentiles 2.5/97.5, contrato conservador), receta común
por sha256. Una ola abierta: **sin IC de persistencia**.

## 5 · Controles, secuencia

Sintético en `tests/test_consumo_pisos_gen2.py`. Oro: ninguno (primer CALC ENGASTO). Control
cruzado post-sello, sin tocar el procedimiento: HOG-TIENE-CELULAR y HOG-CONEX-INTERNET
ENIGH 2016 frente a TIENE-CELULAR y CONEX-INTERNET ENGASTO 2012 (orden y dirección, no
igualdad: cuatro años y definiciones distintas).

## 6 · Auditoría (afirma sobre México)

**Oferta antes que preferencia:** «dónde compra» es primero dónde **hay** (TLOC, cadena en la
localidad); la nota no lee la gran compra en tianguis rural como gusto. ENGASTO 2012 no mide
oferta de establecimientos: NO-CONSTRUIBLE. **Escala:** hogares; la gran compra es la
respuesta de un informante por hogar. **Antigüedad:** 2012 describe el México de 2012; no se
extrapola a 2026 (comercio en línea). **Cifra escrita a mano:** ninguna.

El primer resultado que produzca este procedimiento es el que se reporta.
