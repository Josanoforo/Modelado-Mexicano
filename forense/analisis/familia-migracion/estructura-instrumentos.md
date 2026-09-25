# Informe de estructura · ENADID 2009/2014/2018, ENASIC 2022, Pew GAS · ACTO GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1

Sólo metadatos (25/sep/2026, CAJA): lista de miembros de cada ZIP (envoltura, A.7),
cabecera de cada CSV (primera línea), descriptor de campos de cada DBF (nombres, sin
registros) y `pyreadstat.read_sav(metadataonly=True)` de los `.sav` de Pew. Ningún valor de
registro leído. ENADID 2023 y Pew Spring 2025: no se abrió ni su cabecera (reservadas); Pew
2025 sólo se copió y se hasheó al espejo durable.

## Payloads y sha256 (verificados contra `data/manifiesto.yaml` por id)

| id | archivo en raíz | miembros usados |
|---|---|---|
| `cc1_inegi_enadid_2009__base_datos_enadid09_dbf` | `corpus-completo/inegi/enadid/2009/base_datos_enadid09_dbf.zip` | `tr_viv_hog.dbf` (91 217 registros según cabecera DBF), `tr_sdem.dbf` (343 887) |
| `cc1_inegi_enadid_2014__base_datos_enadid14_dbf` | `corpus-completo/inegi/enadid/2014/base_datos_enadid14_dbf.zip` | `thogar.DBF` (94 422), `TSDem.dbf` (348 450) |
| `enadid2018_bd_csv_zip` | `ENADID/2018/base_datos_enadid18_csv.zip` | `THogar.csv` (con BOM), `TSdem.csv` |
| `enasic2022_bd_csv_zip` | `enasic2022/enasic_2022_bd_csv.zip` | `THOGAR.csv`, `TCSDEMPO.csv` |
| `pew_gas_spring{2013,2015,2017,2018,2023}` | `descargas_mx: UNIVERSO-2026-09/PEW/pew_gas_spring<año>.zip` | el único `.sav` de cada ZIP |

`cc1_inegi_enadid_2014__base_datos_enadid_2014_2018_csv` NO es la ENADID 2014 completa: sus
miembros llevan sufijo `_PE` y pesan ~1/40 de las tablas DBF (p. ej. `TSdem_PE.csv` 2.4 MB
vs `TSDem.dbf` 55.8 MB) → no se usa; se usa el DBF.

Espejo durable: los siete ZIP de Pew se copiaron de `descargas_mx` a
`/home/pc0/mm-corpus/descargas_mx_espejo/UNIVERSO-2026-09/PEW/`; `sha256sum` idéntico al
manifiesto en los siete (incluida 2025, que no se abre).

## Columnas (cabeceras), sólo las que usa la lista cerrada

- ENADID 2018 `THogar.csv`: `llave_hog, tam_loc, p2_5, fac_viv, tip_hog, cls_hog, sexo_jefe, edad_jefe, niv_jefe, migra_ho, est_dis, upm_dis` (FD 2018: `CLS_HOG` 1 nuclear, 2 ampliado, 3 compuesto, 4 familiar no esp., 5 unipersonal, 6 corresidentes, 9 no esp.; `MIGRA_HO` 1 con migrantes, 2 sin, 9 no esp.).
- ENADID 2018 `TSdem.csv`: `llave_hog, paren, sexo, edad, niv, p3_21` (situación conyugal).
- ENADID 2014 `thogar.DBF`: `LLAVE_HOG, TLOC, TOT_PER, FAC_VIV, UPM_DIS, EST_DIS, CLS_HOG, MIG_HOG, SEXO_JEFE, EDAD_JEFE, NIV_JEFE`.
- ENADID 2014 `TSDem.dbf`: `LLAVE_HOG, PAREN, SEXO, EDAD, NIV, P3_20`.
- ENADID 2009 `tr_viv_hog.dbf`: `CONTROL, VIV_SEL, HOGAR, TAM_LOC, PERS_HOG, UPM_DIS, ESTDIS, FAC_VIV, MIGRA_HO, CLS_HOG, SEXO_JEF, EDAD_JEF, NIV_JEF` (FD 2009: `TAM_LOC` 1 < 2 500 … 4 ≥ 100 mil — orden inverso a 2014/2018; `CLS_HOG` escrito H1…H9; `MIGRA_HO` «migración a EUA»).
- ENADID 2009 `tr_sdem.dbf`: `CONTROL, VIV_SEL, HOGAR, SEXO, EDAD, NIV, P3_19, PAR_AGRUP` (sin factor de diseño propio más que `FAC_VIV`, sin estrato ni UPM → del hogar). `NIV` 2009: 00 ninguno, 01 preescolar, 02 primaria, 03 secundaria, 04 preparatoria, 05 normal, 06 técnica, 07 licenciatura, 08 maestría, 09 doctorado.
- ENASIC `THOGAR.csv`: `LLAVEHOG, HN_C, HN_C60MA, SEXO_JEFE, EDAD_JEFE, UPM_DIS, EST_DIS, FAC_HOG`; `TCSDEMPO.csv`: `LLAVESDE` (= `LLAVEHOG` + renglón, 8 posiciones), `LLAVEHOG, PAREN, SEXO, EDAD, NIV, P4_42, P4_44, P4_44A, P4_45`.
- Pew: ver lista cerrada §2 (nombres por ola) y el código de México por ola.

## Lo que la estructura mostró y cambia el diseño

1. ENADID persona no trae factor propio en ninguna ola: el factor es `FAC_VIV` (el FD lo
   declara «a nivel vivienda»); todo piso de persona se pondera con él.
2. `MIGRA_HO` 2009 ≠ `MIG_HOG`/`MIGRA_HO` 2014/2018 (EUA vs internacional): la conducta de
   migración tiene dos olas → sin IC calibrado.
3. ENASIC sin tamaño de localidad; Pew sin PSU en 2013 y 2023.
