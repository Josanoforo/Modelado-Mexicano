# `CALC-B-MARCO-ENVIPE-0001` — la línea base temporal `B` sobre la serie ENVIPE de razones de no denuncia, para seis celdas del marco-M

Cara **local** de la spec sellada `forense/prereg-caja/B-MARCO-spec-v1_0.md`
(`prereg-caja-B-MARCO`). Lo que este archivo dice, lo dice la spec sellada primero;
si alguna vez discrepan, manda la sellada. Congelado en el `COMMIT-1` de
`ACTO GEN2-B-MARCO`, antes de abrir microdato. Sucesora de familia de `CALC-B-0001`
(`prereg-caja-B-REMESAS`): misma regla, otro instrumento.

## 1 · Qué mide

Proporción ponderada de delitos cuya razón principal de no denuncia fue miedo al
agresor, miedo a extorsión o desconfianza en la autoridad (`BP1_23` ∈ {01,02,06}
sobre {01..09}; `BP1_21` en 2011), ponderador `FAC_DEL`, **todos** los tipos de
delito de `TMod_Vic` — el estimando que `corridas-R/CIV-M-*.json` declara para las
seis celdas. Olas: 2011, 2012, 2013, 2014, 2015, 2020, 2021, 2022, 2023, 2024, una a
la vez. Sobre esa serie corre `tools/baseline_temporal.py` **sin modificarlo** para
seis objetivos (2012 · CIV-M-01, 2013 · CIV-M-02, 2015 · CIV-M-04, 2021 · CIV-M-10,
2023 · CIV-M-12, 2024 · CIV-M-13) y dos brazos que difieren sólo en
`disponible_desde`: `OPERATIVO` (versión en corpus: `Modified` del CSV; `mtime` del
miembro DBF cuando el payload no trae metadatos) y `PERSISTENCIA` (`periodo_fin`).
`fecha_corte(objetivo) = <objetivo − 1>-12-31`.

## 2 · Qué NO hace

No lee `R`, `M` ni `L` (el error frente al árbitro y el control positivo viven en
`CALC-B-MARCO-MAE-0001`). No usa `BPCOD` ni `BP1_20`. No promedia, no ajusta, no
imputa. Ninguna cifra entra a un veredicto de regla (`T9`).

## 3 · Guardias que PARAN por ola

`N-SIN-DISENO > 0` → IC `null`, `NO-ESTIMABLE-DISENO-INCOMPLETO`; `n < 10` →
`NO-ESTIMABLE`; `p` exactamente `0.0`/`1.0` → `NO-ESTIMABLE-P-DEGENERADA`. Más de un
CSV de datos bajo `<directorio>/conjunto_de_datos/` → la corrida PARA. Una ola no
reportable entra al historial con `p = null` y el selector la excluye.

## 4 · IC95

Bootstrap de UPM con reemplazo dentro de estrato (`EST`/`UPM` en 2011–2014,
`EST_DIS`/`UPM_DIS` en 2015–2024), 2 000 réplicas, semilla `20260908`, `numpy.PCG64`,
implementación verbatim de `CALC-B-0001`.

## 5 · Contaminación declarada (ADR-46)

Total y declarada por el encargo: los `R`/`M`/`L` de las 14 celdas están en el repo.
Esta spec se congeló leyendo sólo estructura (descriptores DBF, cabeceras CSV, FD,
metadatos), nunca valores; la regla es la de la familia y no depende de ninguno.

## 6 · Contador

`cuenta_gen2 = SI` por la FIRMA DE MESA del 14/sep/2026 citada en el encargo
archivado (`forense/encargos/2026-09-14-GEN2-B-MARCO.md`), con objeto: este CALC-B.
El merge de mesa perfecciona la firma.
