# MC2 · ENUT 2024 · cuidado a dependientes por sexo, participación masculina en cuidados, TNR y trabajo comunitario por sexo · spec v1.0

ACTO GEN2-MEDICION-CARRILES-2, hija ENUT, CAJA, rama `acto/gen2-medicion-carriles-2--enut`. CALC
`data/corrida0/CALC-MC2-ENUT2024-0001` (prueba `tests/test_mc2_enut2024.py`). Todo RETROSPECTIVA. No adopta.

## 0 · Premisas, reserva y lectura previa

- ENUT 2024 es la ola más reciente pero **vista** (CALC sellados `CALC-ENUT2024-*`, `CALC-PDR1-ENUT2024-0001`);
  `motivo_reserva` → vacío. Payload `enut2024_bd_csv`, miembros `tmodulo.csv` y `tvar_crea.csv` (unión 1:1 por `LLAVEMOD`).
- Lectura previa: FD `enut2024_fd_xlsx` (TMODULO §5.10–5.11, §6.11, §6.17; TVAR_CREA) y cabeceras; ningún registro.
- E.5: `CALC-PDR1-ENUT2024-0001` trae TNR y participación en cuidado por sexo y trabajo comunitario por segmento, sin
  diferencia mujer − hombre; `CALC-ENUT2024-PARTICIPACION-INTENSIDAD-0001` sólo nacional; `CALC-ENUT2024-NUCLEO-EJES-0001`
  horas de cuidado por eje con definiciones propias. Nada de lo de abajo está sellado con esta construcción.

## 1 · Variables (A.15) y construcción

Persona 12+ (`tmodulo`), `FAC_PER`, `EST_DIS`, `UPM_DIS`; `SEXO` 1/2; `EDAD_V`; `TLOC` 4 = rural (< 2 500).
- `TRAB_NO_REM_VOL` (TVAR_CREA: «Trabajo no remunerado doméstico, de cuidados y voluntario») y `TRAB_NO_REM_CON_CP`
  («… de cuidado a integrantes del hogar, con cuidados pasivos»); blanco/no numérico = inválido.
- Cuidado a dependientes = `CUID_ESP_INT_HOG_CON_CP` («Cuidados especiales a integrantes del hogar por enfermedad
  crónica, temporal o discapacidad») + `CUID_INT_60MAS_CON_CP` («Cuidado a integrantes del hogar de 60 años y más»);
  CUIDADOR-DEP = > 0. Es la lectura operativa de «cuidadores familiares» (declarado).
- `ESCOLARIDAD` (TVAR_CREA): 1 Sin escolaridad, 2 Básica → HASTA-BASICA; 3 Media superior; 4 Licenciatura, 5 Posgrado → SUPERIOR.
- `P6_17_3` «6.17 … ¿usted hizo actividades o servicios gratuitos para la comunidad como tequio, faena…?» 1/2.
- Razón de la misma réplica: TNR-PROPORCION-HORAS-MUJERES = media(TNR·1[mujer]) / media(TNR).
- IC95: bootstrap de UPM dentro de estrato, 2 000 réplicas, `PCG64(42)`.

## 2 · Pre-registro B-bis (fijado antes del dato)

Nivel: proporciones `c` ∈ IC95 → CONFIRMA; |punto − c| ≤ 0.10 → MATIZA; si no ROMPE. Horas: relativa (≤ 25 % → MATIZA).

| afirmación | estimando y regla |
|---|---|
| FAM-007 | CUIDADOR-DEP-MUJER-PROP vs 0.953 (nivel); «62.3 % no recibe remuneración» no se mide: `PARCIAL` |
| FAM-008 | CUID-INT-MUJER vs 54.3 h y CUID-INT-HOMBRE vs 30.2 h (relativa); ROMPE si MUJER ≤ HOMBRE |
| GEN-012 | TNR-PROPORCION-HORAS-MUJERES vs 0.73 (nivel); lo del PIB (Cuenta Satélite) no es de ENUT: `PARCIAL` |
| GEN-018 | hombres: CUID-PART 18-29 − 60+, URBANO − RURAL, SUPERIOR − HASTA-BASICA: CONFIRMA si los tres IC95-INF > 0; ROMPE si algún punto ≤ 0; MATIZA en otro caso; «pareja económicamente activa» no se mide: `PARCIAL` |
| RURAL-038 | COMUN-PART-DIF-MUJER-HOMBRE: CONFIRMA si IC95-INF > 0; ROMPE si punto ≤ 0; MATIZA en otro caso |
| FAM-039 | **NO-CONSTRUIBLE** en ENUT: §5.11 sólo registra «se dedicó a los quehaceres del hogar o al cuidado de otro familiar» (FD TMODULO P5_11 código 6, recorrido §5.10–5.11); no hay reactivo de «desea trabajar pero no puede por falta de quien cuide» |
| CAPSOC-012 | afirmación de instrumento (texto de 6.17 en 2019/2024): **PISO-SIN-DICTAMEN**, cita `CALC-PDR1-ENUT2024-0001` |

## 3 · Módulo de auditoría v2.16

Unidad persona 12+; RETROSPECTIVA. La brecha de cuidado es división del trabajo con oferta de cuidados escasa, no
rasgo cultural; «nuevas masculinidades» se lee sólo como participación medida, no como identidad. Sin variables de
ascendencia.

El primer resultado que produzca este procedimiento es el que se reporta.
