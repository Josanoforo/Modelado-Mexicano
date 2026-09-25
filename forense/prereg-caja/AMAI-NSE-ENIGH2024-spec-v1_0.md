# AMAI-NSE-ENIGH2024 · distribución NSE AMAI nacional por hogares, ENIGH 2024, apertura acotada · spec humana v1.0

El primer resultado que produzca este procedimiento es el que se reporta.

Acto `GEN2-CLASE-AMAI-2` (encargo `forense/encargos/2026-09-25-GEN2-CLASE-AMAI-2.md`). Un CALC: `CALC-AMAI-NSE-ENIGH-2024-0001`, medidor `tools/dominios/amai/enigh2024.py` copiado byte a byte como `medidor.py` del CALC. RETROSPECTIVA; `cuenta_gen2: SI`; `adopta: NO`. Esta spec basta para recalcular sin leer el código (D-15).

## §0 · Autorización y alcance (E.6)

ENIGH 2024 está RESERVADA (`data/corrida0/decisiones.tsv`, clave `reserva:enigh2024`; la fila `reserva:enigh2024-remesas-nacional-liberada` levantó sólo remesas>0 nacional para el duelo y no se toca). Firma **C7** (FIRMAS-16, 24/sep/2026), verbatim: «mesa levanta por escrito la reserva solo para los seis componentes AMAI y la distribución NSE nacional por hogares, con el medidor congelado de CLASE-AMAI-1 y guardia de una sola variable de agrupación; ninguna conducta se abre.»

Este procedimiento lee de `enigh2024_nc_csv` (`enigh2024_ns_csv.zip`, sha256 `7cbf18fee02c58849356e5495fb851ae4d0330743e34d26e35973f9ad5a1155d`) **exactamente** las 16 columnas de §2 y emite **sólo** la distribución nacional de hogares por nivel y por grupo NSE, sus conteos y su validación. Ninguna conducta, ningún ingreso, ningún corte geográfico, ningún otro cruce. Nada en scratch: la única lectura es la corrida del CALC.

## §1 · Regla (sin cambios respecto de CLASE-AMAI-1)

Regla NSE AMAI 2024 tal como la congela `forense/prereg-caja/AMAI-NSE-spec-v1_0.md` §1 (puntos y cortes del Anexo de la nota metodológica AMAI 2024, sha256 `c268c3dc…d89d1`), implementada en `tools/dominios/amai/regla.py` (sha256 declarado en el spec.yaml), y la distribución y validación de `tools/dominios/amai/medidor.py::distribucion` y `::validacion` (medidor de CLASE-AMAI-1, importado sin editar). Unidad: hogar. Hogar con cualquier componente no válido: sin NSE, con conteo reportado. Puntaje 0 → E, masa reportada aparte (INTERPRETACIÓN-DECLARADA heredada).

INTERPRETACIÓN-DECLARADA (cláusula de autonomía, punto 2): los «seis componentes AMAI» de C7 son seis componentes que la regla construye con **ocho** columnas sustantivas (autos = automóviles + camionetas cerradas + pick-up), más las llaves de unión y el diseño/factor que C7 no excluye y sin los cuales no hay distribución por hogares ponderada. Ninguna otra columna.

## §2 · Columnas — lista blanca congelada (por texto de pregunta del descriptor 2024)

Fuente: «ENIGH 2024. Nueva serie. Descripción de la base de datos» (manifiesto `enigh2024_descripcion_base_pdf`, sha256 `1b0c6985…dfdf8a1`), leída con `pdftotext -layout`. Los nombres de 2022 se re-verificaron uno por uno por su texto de pregunta; **uno cambió de nombre**: `num_pickup` (2022) → `num_pick` (2024), #45 de HOGARES, pregunta 3.3 «¿Cuántos tiene?» de camionetas con caja.

| Tabla (miembro) | Columna | Descriptor 2024 | Pregunta / construcción | Componente |
|---|---|---|---|---|
| VIVIENDAS | `folioviv` | #1 | identificador | llave |
| VIVIENDAS | `cuart_dorm` | #10 | Sección I, p. 8 «¿Cuántos cuartos se usan para dormir sin contar pasillos ni baños?» | dormitorios |
| VIVIENDAS | `bano_comp` | #21 | Sección I, p. 19 «¿Cuántos baños tiene esta vivienda con excusado y regadera?» | baños |
| HOGARES | `folioviv`, `foliohog` | #1, #2 | identificadores | llave |
| HOGARES | `conex_inte` | #38 | Sección V, p. 1.3 «¿Este hogar cuenta con internet?» {1 Sí, 2 No} | internet |
| HOGARES | `num_auto` | #41 | Sección V, p. 3.1 automóviles «¿Cuántos tiene?» | autos |
| HOGARES | `num_van` | #43 | Sección V, p. 3.2 camionetas cerradas o con cabina | autos |
| HOGARES | `num_pick` | #45 | Sección V, p. 3.3 camionetas con caja (pick-up) | autos |
| CONCENTRADOHOGAR | `folioviv`, `foliohog` | #1, #2 | identificadores | llave |
| CONCENTRADOHOGAR | `educa_jefe` | #12 | construida de nivelaprob/gradoaprob/antec_esc del jefe, {01..11} (misma construcción que 2022) | escolaridad |
| CONCENTRADOHOGAR | `ocupados` | #20 | construida: personas con `num_trabaj` 1 o 2 y edad ≥ 14 | ocupados |
| CONCENTRADOHOGAR | `factor`, `est_dis`, `upm` | #8, #6, #7 | factor de expansión, estrato, UPM | diseño |

Miembros: `conjunto_de_datos_{viviendas,hogares,concentradohogar}_enigh2024_ns/conjunto_de_datos/…_enigh2024_ns.csv` (listar los miembros del zip es envoltura, A.7). Uniones: concentrado ⋈ hogares por (folioviv, foliohog) 1:1; ⋈ viviendas por folioviv m:1; llave no única → el medidor para. `parametros.columnas_leidas` del spec.yaml repite esta lista en el orden `tabla.columna`; el medidor para si la lista de columnas efectivamente parseadas difiere.

## §3 · Guardias, auditoría y mutación (E.6: la guardia vive en el medidor)

1. **Lector acotado**: `lee_acotado` parsea con `usecols` sólo la lista blanca; pedir otra columna o tabla lanza `GuardiaColumnas` (PARO técnico, encargo §7 a).
2. **Una sola variable de agrupación**: `agrega` sólo agrupa por `nivel` o `grupo` NSE (`GuardiaAgrupacion` si no); `guardia_salida` rechaza todo id que no sea de distribución/validación nacional.
3. **Auditoría estática** `python3 -m tools.dominios.amai.auditoria_enigh2024` (A1 imports · A2 uso del medidor congelado · A3 lectores sólo en `lee_acotado`, con `usecols` · A4 llamadas a `lee_acotado` sólo con `COLUMNAS[...]` · A5 claves literales dentro de lista blanca o derivados · A6 `groupby` sólo en `agrega`). Debe dar `AUDITORIA-VERDE` antes de la corrida.
4. **Mutación** (`tests/test_amai_enigh2024.py`, sintético con columnas señuelo `ing_cor`, `remesas`, `sexo_jefe`, `mat_pisos`, `num_moto`): lectura de otra columna, tabla no autorizada, lista blanca ampliada, agrupación por estrato, id de salida con corte extra, y un fuente mutado por cada regla A1–A6 → todos fallan.

## §4 · Referencia, umbral, supresión — congelados aquí

- **Referencia publicada por AMAI**: AMAI no ha publicado distribución NSE calculada con ENIGH 2024 (NO-ENCONTRADO: `https://www.amai.org/NSE/index.php?queVeo=NSE2024`, consultado 25/sep/2026, sólo muestra «Estimaciones NSE 2022 y Regla AMAI 2024»; la nota metodológica 2024 usa ENIGH 2022). La publicada vigente es la **Figura 1 de la nota AMAI 2024, p. 4 (ENIGH 2022)**, ya en `regla.AMAI_2022_PCT`: E 8.7 · D 25.4 · D+ 14.9 · C− 16.4 · C 15.3 · C+ 12.0 · A/B 7.3 → BAJO 49.0 · MEDIO 31.7 · ALTO 19.3.
- **Umbral**: `APROXIMACION-DESVIADA` si algún grupo (BAJO/MEDIO/ALTO) se desvía **más de 5.0 pp** de la referencia; si no, `APROXIMACION-CONFORME` — la rama de aproximación de `medidor.validacion` con `umbral_desvio_pp: 5.0`, el mismo umbral de CLASE-AMAI-1, que admite la deriva de dos años (nota AMAI, Figura 2). El desvío máximo por nivel se reporta, no adjudica. No se ajusta con el resultado.
- **Supresión (F-U5-2)**: nivel o grupo con < 200 hogares sin ponderar → valor nulo (`SUPRIMIDA-N`, listado en el JSON).
- **Diagnóstico de dominio**: `educa_jefe` fuera de 01..11, `conex_inte` fuera de {1,2} o conteo negativo → el medidor para (guardias de `regla.puntos`). No hay ejecución diagnóstica previa.

## §5 · Salidas

`RESULT-AMAI-NSE-ENIGH-2024-JSON` (columnas leídas, faltantes por componente, distribución, n por celda, suprimidas, validación, sha de módulos) · `-COLUMNAS-LEIDAS` · `-DIST-<nivel|grupo>-P` · `-MASA-PUNTAJE-CERO-P` · `-N-HOGARES-CON-NSE`, `-N-HOGARES-SIN-NSE` · `-VALIDACION-ESTADO` · `-DESVIO-MAX-GRUPO-PP`, `-DESVIO-MAX-NIVEL-PP`. Tolerancia de `verify` 1e-10.

## §6 · Calibración y eje del marcador (P3, derivado, no CALC)

Con el CALC sellado, un derivador (`tools/dominios/amai/calibracion.py`) compara la distribución por grupo de los instrumentos de A4 (`CALC-AMAI-NSE-ENIGH-2022-0001`, `-ENIF-2024-0001`, `-ENDUTIH-2023-0001`, leídos por id) contra la de ENIGH 2024 — descriptivo — y el marcador toma los pisos por NSE de esos tres CALC por id. ENDUTIH 2024–25 y ENIF 2021 no entran (firma A4). Nada de esto adopta.

## Auditoría de rigor extremo

¿Cuántos contadores mueve? Uno: un CALC GEN2 (`cuenta_gen2: SI`); `celdas_validadas` no cambia. NSE AMAI mide bienes y capital escolar del hogar, no clase sociológica ni ingreso; tres componentes (autos, internet, baños) son también oferta de infraestructura, así que un desplazamiento 2022→2024 hacia niveles altos mezcla bienestar con expansión de la red de internet (oferta antes que preferencia). La comparación contra la Figura 1 es contra otra ola: una desviación es deriva o cambio de regla de captura, no error del medidor, y así se rotula. Cifra de unidad hogar; no se promedia con ninguna de persona. RETROSPECTIVA.
