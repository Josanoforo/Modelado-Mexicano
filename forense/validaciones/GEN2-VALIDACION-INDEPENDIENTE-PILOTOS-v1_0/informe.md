# Validación independiente de los tres pilotos celda-D · `GEN2-VALIDACION-INDEPENDIENTE-PILOTOS-v1_0`

**Acto:** `ACTO GEN2-VALIDACION-INDEPENDIENTE-PILOTOS-1`, 21/sep/2026, **CAJA** (Ubuntu/WSL2, corpus montado, `archivos_examinados = 422`), Opus, rama `acto/gen2-validacion-independiente-pilotos-1`, base `origin/main = fc13cdcc` (= SHA de redacción del encargo). Encargo verbatim: `forense/encargos/2026-09-21-GEN2-VALIDACION-INDEPENDIENTE-PILOTOS-1.md` (0-bis `7ef3b678`).

**Contador: cero mediciones nuevas, cero corridas selladas, cero adopciones.** Este acto responde la segunda pregunta de E.2 (¿pasó validación independiente?) para las 35 celdas de los tres pilotos. No re-adjudica (propuesta de dirección, §2 del encargo).

## Veredicto por piloto

| piloto | CALC validados | celdas | R (punto) | R (IC95) | C2 (punto) | marginales | **veredicto** |
|---|---|---|---|---|---|---|---|
| 1 · DIN · ENIF 2024 · `localidad × edad` | `…-EMISIONES-0001`, `…-ARBITRO-CRUCE-0001` | 8 | 8/8 `IDÉNTICO` (`|Δ| ≤ 1e-6`) | 8/8 `COINCIDE` | 8/8 `IDÉNTICO` | 7/7 `IDÉNTICO` | **`COINCIDE`** |
| 2 · TRA · ENVIPE 2025 · `escolaridad × dominio` | `…-EMISIONES-0001`, `…-ARBITRO-CRUCE-0001` | 12 | 12/12 `IDÉNTICO` | 12/12 `COINCIDE` | 12/12 `IDÉNTICO` | 8/8 `IDÉNTICO` | **`COINCIDE`** |
| 3 · GOB · ENCIG 2025 · `edad × escolaridad` | `…-EMISIONES-0002`, `…-ADJUDICACION-0001` | 16 (15 `PUNTUADA`) | 16/16 `IDÉNTICO` | 16/16 `COINCIDE` | 16/16 `IDÉNTICO` | 9/9 `IDÉNTICO` | **`COINCIDE`** |

Los `n` sin ponderar coinciden **exactos** en las 36 celdas y en los 24 marginales. La sensibilidad `R7` del piloto 1 también reproduce (8/8 `IDÉNTICO`). Tabla completa celda por celda: `comparacion.md` / `comparacion.json` (generados por `compara.py`).

**Qué acredita esto, y sólo esto.** Que la cadena *payload → filtro de universo → llave de unión → ponderador → dicotomización → agregación → fórmula log-aditiva* de los seis CALC produce, escrita por segunda vez desde la spec humana y sin mirar el código, los mismos puntos a `1e-6` y los mismos `n`. Si el medidor «leyera mal un filtro», este código lo habría leído distinto salvo que la spec misma lo dicte mal — y lo que la spec dicta se declara en §3.

## Independencia — cómo se probó

1. **No se abrió** `medidor.py`, `adjudicacion.py`, `captura_l.py` ni ningún `.py` de los seis CALC, ni `tests/test_celda_d_c2.py`, `tests/test_marginales_una_variable.py`, `tests/test_piloto3_v11.py`, `tools/celda_d/*`, `tools/calibracion_mordida_encig_serie.py`, `tools/medidor_gobierno_digital_encig25.py`, `tools/ejes_maestra35_l1.py` ni `tools/medidor_evasion_norma_envipe25.py`. Tampoco `spec.yaml`/`spec.md` de los CALC (son la capa ejecutable de la misma spec; la validación se hizo sólo desde la capa humana para que el `[SUPUESTO]` del §3 del encargo quedara probado).
2. **Insumos leídos:** `forense/prereg-caja/DIN-ahorro-solo-informal-lxe8-spec-v1_2.md`, `TRA-evade-norma-sxd12-spec-v1_0.md`, `GOB-gobierno-digital-exe15-spec-v1_1.md` **y** `v1_0.md` (la v1.1 hereda «= v1.0» por sección); descriptor `encig25_estructura_base_datos.pdf` (vía `pdftotext`: `P7_3`, `N_TRA`, `EDAD`, `NIV`, `EST_DIS`, `UPM_DIS`); cabeceras de los cinco CSV; y —para el formato de los códigos, una variable a la vez— conteos de `N_TRA`, `P7_3`, `NIV`, `EDAD` de ENCIG 2025.
3. **Orden del diff:** `valida_pilotos.py` + `resultados_propios.json` se commitearon y empujaron en **`19d35aba`** (13:22:06 −06:00) **antes** de leer ningún `resultados.json`; `compara.py`, `comparacion.*` y este informe van en el commit siguiente. Verificable: `git show 19d35aba --stat`.
4. **Reserva (PARO b):** de ENIF 2024 sólo se construyó `localidad × edad`; de ENVIPE 2025 sólo `escolaridad_proxy × dominio`; de ENCIG 2025 sólo `edad × escolaridad` sobre `N_TRA == 01`. Ningún otro cruce.

## Método de varianza propio (declarado, §6 del encargo)

Bootstrap de conglomerados estratificado, **`numpy.random.default_rng(20260921)`** (no la semilla de los CALC), 10 000 réplicas, `n_h` UPM con reemplazo dentro de cada `EST_DIS`, sorteo sobre **el marco entero del archivo** (ENIF: `TMODULO`; ENVIPE: `tmod_vic` con `BP1_20 ∈ {1,2}`, que es el archivo entero; ENCIG: todas las UPM de `sec_7`) y máscaras de universo/celda aplicadas **dentro** de cada réplica; todas las celdas y marginales de una ola comparten réplicas; IC95 por percentiles 2.5/97.5 (interpolación lineal); estrato con UPM única → multiplicidad fija 1 (0 en ENIF y ENCIG, 23 en ENVIPE 2025, igual que lo sellado).

**Tolerancia del IC, declarada:** `COINCIDE` si `|Δ inf| ≤ 1.0 pp`, `|Δ sup| ≤ 1.0 pp` y razón de semianchos propio/sellado ∈ `[0.80, 1.25]`. Resultado: 36/36 `COINCIDE`; **máximo `|Δ|` de un extremo = 0.59 pp** (`S1xD2`, la celda con `n = 871` y más dispersa) y todas las razones de semiancho dentro de `[0.90, 1.10]`. Con otra semilla y otro plan (el árbitro del piloto 2 remuestrea por celda; los pilotos 1 y 3 sobre el marco entero como aquí), la diferencia observada es la de Monte Carlo + plan, no una discrepancia.

## P3 · causas — nada supera la tolerancia del punto; lo que sí se encontró

Ninguna celda ni marginal supera `1e-6`. Sin `SIN-EXPLICAR`. Tres hechos que la validación deja escritos para que nadie los infiera:

1. **Piloto 1 — los marginales públicos del árbitro no son los del universo de la spec, y el CALC ya lo sabía.** Los marginales re-derivados aquí coinciden `IDÉNTICO` con los `…-G-C2-MARG-*` del CALC de emisiones, y **difieren** de los públicos de `tramite-ola5-propuesta-v0.yaml` citados en la spec §4.2: `L1` −0.018 pp, `L2` +0.120 pp, `E4` −0.011 pp, `NAC` +0.078 pp (`E1..E3` exactos). Causa, hasta la línea: el árbitro público estimó `localidad` sobre las 13 502 filas (sin filtro de edad; `n = 4 646 + 8 856`) y `edad` sobre 13 487 (excluyó 15 filas; `E4 n = 2 896`), mientras la spec v1.2 §3.1 fija **un** universo para todo (`18 ≤ edad ≤ 97`, `TLOC ∈ {1..4}`, `fac_per > 0` → 13 492; `E4 n = 2 901`). Es exactamente el `NO-REPRODUCE` que la spec §0.8 previó y el CALC declaró; **el punto de `C2` sellado usa los públicos** (spec §4.2, «citadas y no recalculadas») y ese punto reproduce aquí `IDÉNTICO`. Cuánto mueve el piso: `C2` con marginales propios vs con públicos difiere ≤ 0.10 pp por celda (`comparacion.json`, filas `C2-REDERIVADO`, 8/8 `IDÉNTICO` contra `…-C2-P-REDERIVADO-*`).
2. **Piloto 3 — la spec humana deja una lectura abierta sobre el universo de los marginales, y la literal es la sellada.** v1.0 §2 («coherencia contra los marginales recalculados sobre ese mismo universo», F1-bis) se leyó como: marginales de `edad`, `escolaridad` y total **sobre el universo del cruce** (edad 18–96 **y** `NIV ∈ 0..9`, 20 088 trámites). Esa lectura reproduce `IDÉNTICO` los nueve marginales y las 16 `C2`. La alternativa —cada eje sobre su propio universo clasificable (20 203 para total y edad; 2 299/4 216/5 582/8 106 para escolaridad)— se calculó también (`C2-ALTERNATIVA-marginales-por-eje`): mueve `C2` **≤ 0.19 pp** por celda (máx. `30-44|HASTA-PRIMARIA`, +0.19 pp; 6/16 quedan `COINCIDE` a 0.05 pp, 10/16 `DIFERENCIA` de 0.05–0.19 pp). No cambia ningún veredicto de celda. Se anota como precisión que un sucesor de spec debería escribir (§4 abajo).
3. **Piloto 3 — S2 verificada:** `EDAD = 97` → 1 trámite (masa 1 381), `98` → 114 (masa 753 862), `99` → 0; fracción de `97` en la banda 60+ = 0.00022 < 1 % → `SIN-RESERVA`, igual que lo sellado. Los 114 de código 98 son «edad no especificada» y salen del universo por F1-bis, no población real.

## P4 · lo que cambia para el producto — con los números propios

| piloto | celdas `PUNTUADA` | MAE(`C2` vs `R`) pp | máx. error pp (celda) | IC95(`C2`) propio contiene `R` |
|---|---|---|---|---|
| 1 · DIN | 8 | **1.467** | 4.375 (`L1xE3`) | 7/8 |
| 2 · TRA | 12 | **1.568** | 5.436 (`S1xD1`) | 11/12 |
| 3 · GOB | 15 | **3.411** | 12.282 (`60-96\|HASTA-PRIMARIA`) | 8/15 |
| **35** | 35 | **2.335** (media ponderada por celdas) | — | **26/35** |

Los tres MAE coinciden con los sellados (`…-G-MAE-C2` = 0.014668 / 1.568 pp; `…-C2-MAE-PP` = 3.411) a la sexta cifra. La cobertura sellada (IC95 de `C2` sellado sobre `R` sellado) da lo mismo: 7/8, 11/12, 8/15.

**Una línea:** «el estimador adjudicado acierta a 1.5 pp» **se sostiene para los pilotos 1 y 2 (1.47 y 1.57 pp) y se matiza en el conjunto de 35 celdas: MAE 2.3 pp, porque el piloto 3 (pago de luz digital, ENCIG 2025) erra 3.4 pp en promedio y 12.3 pp en `60-96 × hasta primaria`**; la cobertura del intervalo del piso es **26 de 35** (74 %), y es la cobertura esperada de un IC que —como las tres specs declaran— **sólo propaga el muestreo de los marginales, no el error de especificación del piso**: en el piloto 3 cae a 8/15. La cifra «18 de 20» que cita el encargo **no se encontró en el árbol** (`git grep -E "18 de 20|18/20"` → 0 fuera del propio encargo; control positivo: `grep "1.5 pp"` → 4 notas) y no se reconstruye desde estas 35 celdas con ninguna de las dos lecturas de cobertura (26/35 con IC de `C2`; con `C2` dentro del IC de `R`: 7/8, 11/12, 12/15 = 30/35): **NO-ENCONTRADO**, se pide a dirección su fuente antes de repetirla.

## Auditoría — el universo real de cada piloto, leído del cuestionario

*Este acto no afirma nada nuevo sobre México; declara quién está dentro de cada cifra.*

- **Piloto 1 (ENIF 2024, persona).** Universo: la **persona elegida** de 18+ del hogar (una por vivienda, `fac_per`), 13 492 de 13 502 (10 con edad 98 fuera). Sesgo de clase que se cuela por construcción del cuestionario y **se hereda, no se corrige** (spec §2.2): `P5_4_k` gatea a `p5_6_k`, así que quien **no tiene la cuenta a su nombre** no responde «ahorró en ella» y entra como «no usó vía formal». Una persona que ahorra en la cuenta de nómina de su pareja cuenta como `ahorra_solo_informal = 1`. El desenlace mide tenencia-y-uso propio, no acceso del hogar.
- **Piloto 2 (ENVIPE 2025, delito).** Universo: **delitos** del módulo de victimización con `BP1_20 ∈ {1,2}` — 40 280 = el archivo entero (0 fuera); unidad delito con `FAC_DEL`: quien sufrió tres delitos pesa tres veces. La persona es el **informante seleccionado** del hogar (18+), no la víctima si fue otro miembro. `BP1_23` en blanco con no-denuncia (130 delitos, sellado) cuenta como `evade_norma = 0`: la conjunta, no la condicional (spec §1). 100 delitos sin escolaridad clasificable (`NIV = 99`/blanco) quedan fuera de las 12 celdas y dentro del nacional y de dominio.
- **Piloto 3 (ENCIG 2025, trámite).** Universo: **pagos ordinarios de luz realizados** (`N_TRA == 01`, 20 392) con canal válido (`P7_3 ∈ {1,2,4,5,6}`, 20 203; 189 fuera por teléfono/no concluido/otro/NS-NR), unido `m:1` a la persona por `ID_PER` (0 huérfanos), y con edad 18–96 y `NIV` clasificable (20 088; 115 fuera por edad 97/98). Quien **no paga la luz, no la tiene contratada a su nombre, o la paga otro del hogar** no está: más rural, más informal, más inquilino. Y quien hizo doce pagos cuenta doce veces (encargo §3). La cifra es de canal de pago del que paga, no de «adopción digital» de la población.

## Lo que la spec humana NO bastó para reproducir (§3 `[SUPUESTO]` del encargo)

El supuesto **se sostiene en lo sustantivo** para los tres pilotos: universo, filtros, códigos, ponderador, diseño, fórmula y rejilla están escritos y con ellos se reproduce a `1e-6`. Huecos menores, todos cubiertos por descriptor/catálogo sin leer código:

| piloto | hueco | cómo se cerró |
|---|---|---|
| 3 | nombre de la variable de edad (`EDAD`) y de escolaridad (`NIV`) en `residentes_sec_2`, y que `EST_DIS`/`UPM_DIS`/`FAC_TRA` viven en `sec_7`; v1.1 §5 nombra los archivos pero no las columnas | descriptor `encig25_estructura_base_datos.pdf` + cabeceras |
| 3 | formato de `N_TRA` (`'01'` con cero a la izquierda) y de `P7_3` (`'1'…'9'`, blanco) — v1.0 §1 escribe `N_TRA == '01'` y `P7_3 ∈ {4,5}` sin decir el tipo | conteo de valores, una variable a la vez |
| 3 | universo de los marginales de `C2` (P3.2 arriba) | lectura literal de F1-bis, alternativa calculada, ≤ 0.19 pp |
| 1 | la spec cita como punto de `C2` los marginales **públicos** y como fuente de réplicas los **re-derivados**; el `R` de la celda usa el universo §3.1 | tal cual está escrito; reproduce |
| 2 | ninguno | — |

Ninguno de los huecos, resuelto de otra manera razonable, mueve un punto más de 0.19 pp ni cambia veredicto alguno. **No es el «hallazgo más importante»** que el encargo temía: las tres specs permiten reproducir sin el código.

## NO-CORRIDO / RESERVAS de esta validación

- El IC de `C2` **no** se validó celda por celda contra tolerancia en los pilotos 1 y 2 (sí en el 3: 16/16 `COINCIDE`); en 1 y 2 se reportan los IC propios de `C2` en `resultados_propios.json` y sirven para la cobertura de P4. Razón: la spec del piloto 1 sella el punto de `C2` con marginales públicos y el IC con re-derivados — dos objetos —; comparar ese IC exige el mismo par, que aquí se reproduce por partes (marginales `IDÉNTICO`).
- `C1`, `C3`, `C6`, `C7`, `S½`, `Sλ`, `I₂₃/I₂₄`, `δ`, `λ` y las adjudicaciones **no** se recalcularon: el encargo pide R y C2. No hay veredicto sobre ellos.
- Precedente de forma seguido: `GEN2-VALIDACION-R-ENVIPE-CSV-v1_0/` (leído; `tools/valida_envipe_independiente.py` no fue necesario).

## Reproducir esta validación

```
python3 forense/validaciones/GEN2-VALIDACION-INDEPENDIENTE-PILOTOS-v1_0/valida_pilotos.py   # ~20 s, escribe resultados_propios.json
python3 forense/validaciones/GEN2-VALIDACION-INDEPENDIENTE-PILOTOS-v1_0/compara.py          # escribe comparacion.{json,md}
```

Payloads (sha256 de los miembros en `resultados_propios.json`): `enif2024_csv.zip` → `conjunto_de_datos_tmodulo_enif2024.csv`; `envipe2025_csv.zip` → `tmod_vic`/`tsdem` 2025 (terminador `\r`); `encig25_base_datos_csv.zip` → `encig2025_04_sec_7.csv`, `encig2025_02_residentes_sec_2.csv`.
