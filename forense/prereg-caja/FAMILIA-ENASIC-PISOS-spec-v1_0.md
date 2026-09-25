# Pisos por segmento ENASIC 2022 (necesidad de cuidados y quién cuida a las personas de 60+) · spec v1.0

**Pre-registro de caja.** `ACTO GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1`, 25/sep/2026, CAJA,
rama `acto/gen2-familia-cuidados-y-migracion-pisos-1`, 0-bis `2a0ebb63`. CALC:
`CALC-ENASIC-CUIDADOS-VEJEZ-0001`. Congelada en el COMMIT-1, **antes** de leer un solo
valor de registro de ENASIC (sólo cabeceras CSV y FD). **El primer resultado que produzca
este procedimiento es el que se reporta.**

## 0 · Premisas verificadas

- `[EJECUTADO]` ENASIC en el manifiesto por id: una ola, 2022 (`enasic2022_bd_csv_zip`,
  `enasic2022_fd_xlsx`, `enasic_2022_889463927082`, `enasic2022_ipe_cv_ee_ic`), presentes en
  `data/raw`. E.6: una sola ola → no hay historia que reservar; se abre y se declara. Sin IC
  de persistencia.
- `[EJECUTADO]` Estructura: `forense/analisis/familia-migracion/estructura-instrumentos.md`.
- No hay CALC previo de ENASIC (`ls data/corrida0 | grep -ci enasic` = 0 al COMMIT-1).

## 1 · Unidad, universo, diseño

**Hogar** (THOGAR): `FAC_HOG`, `EST_DIS`, `UPM_DIS`; válido si factor > 0 y estrato/UPM no
vacíos. **Persona de 60 a 97+ años** (TCSDEMPO; `EDAD` 97 = «97 y más», 98 fuera): factor y
diseño de su hogar por `LLAVEHOG`. Tamaño de hogar = renglones de TCSDEMPO con esa
`LLAVEHOG`. Cuidador principal: `P4_44` es un número de renglón (01–07); su sexo es el
`SEXO` del renglón `LLAVEHOG`+renglón (2 dígitos) = `LLAVESDE`; sin pareo → fuera
(`G-CUIDADOR-RENGLON-SIN-PAREO`).

## 2 · Conductas (por texto)

Lista cerrada §2 (ENASIC): 2 de hogar, 5 de persona 60+, todas proporciones.

## 3 · Ejes (uno a la vez)

Hogar: SEXO-JEFE · EDAD-JEFE (18–29/30–44/45–59/60+; 98 fuera) · TAMANO-HOGAR. Persona 60+:
SEXO · EDAD (60–69/70–79/80+) · ESCOLARIDAD (`NIV`: HASTA-PRIMARIA {00–02}, SECUNDARIA {03,
05}, MEDIA-SUPERIOR {04, 06, 07}, SUPERIOR {08–11}; 99 fuera) · TAMANO-HOGAR (1/2/3–4/5+) ·
CONDICION-PAREJA (CON-PAREJA-EN-HOGAR = `PAREN` 2, o `PAREN` 1 en hogar con algún `PAREN`
2; SIN = demás). Sin TLOC (ENASIC no lo publica).

## 4 · Estimación

Razón ponderada con bootstrap de UPM dentro de `EST_DIS` (certeza para UPM única,
`PCG64(20260925)`, 2 000 réplicas, percentiles 2.5/97.5, contrato conservador), receta común
y lectores por sha256 (como la spec ENADID §4). Sin persistencia.

## 5 · Controles, secuencia

Sintético en `tests/test_familia_pisos_gen2.py`. Ninguna ejecución diagnóstica.

## 6 · Auditoría (afirma sobre México)

**Contadores:** cuenta (`cuenta_gen2: SI`, `adopta: NO`). **Escala:** «cuidado» en ENASIC es
la semana pasada, por reporte del informante del hogar — no horas ni intensidad (eso es
ENUT, que se cita). **Estructura ≠ cultura:** que el cuidador principal sea hija o mujer
refleja división sexual del trabajo, ingresos y ausencia de oferta pública de cuidados
(`VEJEZ-017`: sin sistema nacional), no un «deber filial» cultural medido; la nota no lo
lee como rasgo. **Oferta antes que preferencia:** la baja proporción de cuidado de otro
hogar o pagado no es preferencia por el cuidado familiar sin la medida de oferta al lado —
no la hay en ENASIC. **Hogar unipersonal:** 4.42 = 3 queda fuera del universo, por lo que
«cuidado por alguien del hogar» es sobre personas que viven acompañadas. **Una ola:**
ninguna tendencia. **Cifra a mano:** ninguna.

El primer resultado que produzca este procedimiento es el que se reporta.
