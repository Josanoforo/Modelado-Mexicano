# ACTO MAESTRA32-E16 · MEDIDOR-FAMILISMO-APOYO -- cierre

31/ago/2026. Corrida única de `tools/medicion_familismo.py` contra `data/raw/eder2017/eder2017_bases_csv.zip` (sha256 `bcc7eb90c2d016976fd8ba24528ce614bf4db0c29a1e3e0cf674bdfb024de0e3`) y `data/raw/endireh2016/bd_mujeres_endireh2016_sitioinegi_csv.zip` (sha256 `02c06ab73a53942ddb575e3e35d8c1dd775406277b74e0605735e3eced4e6f10`). "el primer resultado que produzca este procedimiento es el que se reporta."


## 1 · n por universo

- EDER: `vivienda.csv` 23548 filas -- 8858 excluidas (tipo_adqui en blanco: renta/prestada, no aplica la pregunta de financiamiento). `historiavida.csv` colapsado a 23831 personas (panel persona-año); 8944 sin folioviv en el universo de theta (excluidas).
  - Universo final: theta=1 n=623, theta=0 n=14264 (total 14887).
- ENDIREH: `TB_SEC_IV.csv`/`TB_SEC_XVIII.csv` 111256 filas cada una (universo bd_mujeres, mujeres 15+). P18_4 excluidos: {'blanco': 92840, 'no_tiene(5)': 1748, 'no_especificado(9)': 1}.
  - Universo final: theta=1 n=3177, theta=0 n=13490 (total 16667).

## 2 · beta_hat e IC por instrumento

- **EDER (primaria):** +0.0041 [IC95% 0.0029,0.0054]
- **ENDIREH (robustez):** -0.0461 [IC95% -0.0745,-0.0181]

Escala: diferencia de proporciones ponderada del desenlace (theta=1 - theta=0), proporción [0,1]. IC95 por bootstrap de conglomerados (UPM dentro de estrato), B=10000 (EDER/ENDIREH principal) / B=2000 (celdas condicionadas), seed=42.

## 3 · tabla condicionada (un eje a la vez, celdas n>=30)

### EDER
- **sexo:**
  - 1: +0.0064 [0.0040,0.0089] (n1=276, n0=6441)
  - 2: +0.0023 [0.0013,0.0033] (n1=347, n0=7823)
- **edad:**
  - 15-29: +0.0061 [0.0032,0.0094] (n1=176, n0=3823)
  - 30-44: +0.0035 [0.0018,0.0055] (n1=275, n0=6610)
  - 45-59: +0.0031 [0.0014,0.0051] (n1=172, n0=3831)
- **urbano/rural:**
  - 0: +0.0035 [0.0018,0.0055] (n1=265, n0=6091)
  - 1: +0.0045 [0.0029,0.0063] (n1=358, n0=8173)
### ENDIREH
- **edad:**
  - 60+: -0.0461 [-0.0741,-0.0174] (n1=3177, n0=13490)
  - (única celda con n>=30 en ambos brazos de theta -- ver nota abajo)
- **urbano/rural:**
  - 0: -0.0148 [-0.0579,0.0300] (n1=964, n0=3557)
  - 1: -0.0546 [-0.0886,-0.0212] (n1=2213, n0=9933)

**Nota sobre el eje edad en ENDIREH (verificada, no es un defecto del
script):** `P18_4` trae un patrón de salto fuertemente sesgado por edad
-- de las 92,840 filas en blanco (excluidas en §1), las edades van de 15
a 98 años con moda en 30-39 (25,174 casos) y 20-29 (22,142); el universo
que SÍ recibió la pregunta (18,416 mujeres con código 1-4) queda
concentrado casi en su totalidad en 60+ años. Verificado por código:
`edad_de` (TSDem.EDAD) de las filas en blanco de P18_4 tiene mínimo 15 y
máximo 98, con la mayoría bajo 50 años -- el patrón de salto de la
Sección XVIII (probablemente condicionado a "¿tiene usted nietos(as) o
sobrinos(as)?" en P18_1-3, no citado en este acto) selecciona
estructuralmente hacia mujeres mayores. Por eso el condicionamiento por
edad en ENDIREH colapsa a una sola celda con soporte -- no hay error de
join (el traslape ID_MUJ entre `TB_SEC_IV`/`TB_SEC_XVIII`/`TSDem` es
111,256/111,256, completo), es la estructura real del cuestionario.

## 4 · veredicto (a) -- ajuste de constructo

financia_8 (EDER, ADR: texto_reactivo extraído de `eder2017_fd.pdf` #91): "¿Para pagar o empezar a construir esta vivienda, el dueño tuvo préstamo de un familiar, amigo o prestamista?" -- mide recepción de préstamo con fuente compuesta (familiar + amigo + prestamista comercial), específico al financiamiento de vivienda, no apoyo económico familiar genérico. p4_8_2/p4_8_3 (ENDIREH, texto extraído de `fd_endireh2016_dbf.pdf`): "¿usted recibe dinero de familiares o conocidos que viven en Estados Unidos de América/dentro del país...?" -- mide recepción de dinero con fuente compuesta (familiares + conocidos), sin restricción de propósito. **Veredicto: VÁLIDA en ambos instrumentos** -- "familiar" es nombrado explícitamente y en primer lugar en las dos fuentes, cumple la regla pre-registrada (apoyo económico familiar recibido/obtenido, préstamo/dinero de familiares); la contaminación con no-familia (amigo/prestamista/conocidos) es una reserva declarada, NO dispara PROXY bajo la regla tal como está escrita en el encargo. Circularidad: el desenlace NO es transformación del mismo reactivo en ninguno de los dos instrumentos -- corresidencia con familiar adulto (EDER) y carga de cuidado de nietos/sobrinos (ENDIREH) son constructos distintos de "recibir dinero/préstamo", mismo criterio que excluyó ENIF p9_9_4 por circularidad.

**FALSADOR: NO DISPARADO** -- ningún instrumento marcó PROXY.

## 5 · veredicto (e) -- B-bis, ADR-57(a) y rótulo

Signo ASIGNADO de G5.familismo_apoyo (canon/modelo-decision-v4_0.md:459): **positivo (0.50)**.
- EDER: β̂ +0.0041, distinguible de cero al 95%.
- ENDIREH: β̂ -0.0461, distinguible de cero al 95%.
- Signos entre EDER y ENDIREH: DISCORDANTES -- ADR-57(a): concordancia o discordancia son ambas informativas, ninguna corrobora ni refuta el ASIGNADO.
- Rótulo escrito en `coeficientes_generador_sellados`: `ASOCIACION-MEDIDA·MARGINAL·DISCORDANTE-ENTRE-INSTRUMENTOS`. Solo la primaria (EDER) lleva `valor_ejecutable`; ENDIREH queda en `reserva` como robustez, por regla de escritura del encargo.
