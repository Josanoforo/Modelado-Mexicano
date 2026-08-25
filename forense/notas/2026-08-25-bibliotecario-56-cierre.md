# ACTO BIBLIOTECARIO-56 — la prueba pendiente del marco (`FP-93`), corrida

**Cierre.** 25/ago/2026 · Entorno **UBUNTU** · Modelo Opus · Encargo: `forense/encargos/2026-08-25-BIBLIOTECARIO-56.md` · ADR: **`ADR-163`** (candidateado, a re-verificar por quien fusione — es la **tercera** renumeración de este acto) · Base `21ab042`, fusionada a `e70b424`, `a5f1bf6` y `7848b97` durante el acto.

> **Nota de nombre de archivo.** El encargo pide la nota como `2026-08-25-bibliotecario-56.md` {cita-ilustrativa}. Se escribe con sufijo `-cierre` porque el nombre literal colisiona bajo `T02` con el propio encargo archivado (`2026-08-25-BIBLIOTECARIO-56.md`): `T02` normaliza a minúsculas y quita todo lo que no sea alfanumérico, así que los dos nombres caen en `20260825bibliotecario56md`. Es la autocolisión encargo↔nota ya documentada; la convención de la casa (`-cierre` en la nota) la resuelve sin inventar nada.

---

## 1 · Arranque, y la firma de entorno de tres partes (`A.2`)

| Parte | Comando | Salida |
|---|---|---|
| 1 · variable | `echo $CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` | `sin_variable` → **UBUNTU**, no nube |
| 2 · sonda de red | `curl -s -o /dev/null -w "%{http_code} %{size_download}" https://www.inegi.org.mx/` | `200`, **153 606** bytes |
| 3 · corpus | `ls data/raw/ \| head -1` y `\| wc -l` | `2005trim1_csv.zip`, **321** entradas → montado, **sin `PARO`** |

`data/raw` se enlazó a mano en el worktree nuevo (`ln -s /home/pc0/mm-corpus/raw data/raw`): un worktree recién creado no lo hereda.

---

## 2 · La premisa del encargo: el «56» es correcto, el rótulo no

El encargo y la propia `FP-93` dicen *«las 56 filas `PENDIENTE-BIBLIOTECARIO`»* y mandan re-derivar el conteo. Re-derivado:

```
awk -F'\t' 'NR>1{split($10,a,"::"); gsub(/^ +| +$/,"",a[1]); print a[1]}' \
    forense/marco-candidatas-piloto-v1_0.tsv | sort | uniq -c
   →  6 NO   ·   50 PENDIENTE-BIBLIOTECARIO   ·   4 SI
```

**Son 50 con la etiqueta literal, no 56**, y así ha sido desde que el marco nació: el mismo comando sobre `89a76ed` (`ACT-PIL-2 T2+T3`, el commit que lo creó) y sobre `21ab042` da el mismo reparto. `MARCO-SATURA-CODEX` no lo tocó, como su propio cierre declaró.

**El 56 reconcilia y no es error de cuenta.** `forense/notas/2026-08-20-act-pil-2-marco.md:191` lo dice verbatim: *«Resultado: **4 `SI`** (con evidencia positiva en la mano), **0 `NO` por búsqueda**, **56 `PENDIENTE-BIBLIOTECARIO`**»*. Las 6 filas escritas `NO` lo están **por aserto estructural, declarado explícitamente como «no búsqueda exhaustiva»** — y por eso el acto que las escribió las contaba como pendientes del bibliotecario. El universo del filtro (i) es `60 − 4 SI = 56`, y sobre esas 56 corrió este acto.

Se reportan **los dos números por separado** en todo el registro. Ni una fila del marco se añadió, quitó ni reordenó.

---

## 3 · Los dos pasos, ejecutados y contados (`A.13`)

### Paso 1 — los índices

`data/indice-descarga-masiva-2026-08-05.tsv` (**7 930** filas) y `data/indice-canastas-2026-08-08.tsv` (**17 163** filas), filtrados por `programa` + `anio` según el mapeo de cada fila del marco.

- **32** pares `programa + año` localizados, para 47 de las 56 filas.
- **945** archivos candidatos distintos en las canastas `tabulados` e `indicadores`.
- **922** tras dos exclusiones **declaradas antes de bajar nada**: (a) los `*_english_*`, traducción del mismo tabulado; (b) la versión `_xlsx.zip` de los paquetes de indicadores, redundante con la `_csv.zip` del mismo id.
- Las 9 filas restantes (5 de ECF Banxico/CNBV, 3 documentales, y `DIN-02`/`DIN-03` que sí son de INEGI pero sin tabulados indexados) se tratan en §5.

### Paso 2 — abrir el archivo y buscar la cifra dentro

- **922 de 922** archivos descargados y **validados por contenido**, no por código HTTP (`zipfile.testzip()` / magic bytes): 3 quedaron truncados en una interrupción y se re-bajaron.
- **929 MB**, **3 806** libros, **46 645** hojas leídas.
- **14 `.zip` con `.xls` heredado** (los paquetes trimestrales de la ENOE, 296 archivos cada uno) que `openpyxl` no abre: se leyeron con **`xlrd 2.0.2`**, traído como rueda desde `files.pythonhosted.org` y descomprimido en `scratchpad` con `sys.path.insert` — **sin `pip install`, sin tocar el entorno de Python del usuario**. Sin esto, la ENOE 2024 y la ENOEN 2022 habrían dado un negativo falso sobre 0 archivos examinados, que es exactamente lo que `A.13` prohíbe.
- El mnemónico de cada fila se resolvió a **texto verbatim del reactivo** contra el FD o el diccionario del corpus antes de buscar: **47 de 56** (las 9 restantes no son de INEGI y su FD no vive aquí). Ejemplos: `P8_3_1` → *«¿Un(a) servidor(a) público(a) … intentó apropiarse o le solicitó de forma directa algún beneficio…?»* (`encig23_estructura_base_datos.pdf`, pág. 36); `TRAB_NO_REM_CUID_HOG` → *«Trabajo no remunerado de cuidado a integrantes del hogar»* (`enut2024_fd.xlsx`, `TVAR_CREA` fila 45).

### La regla de adjudicación, escrita antes de aplicarla

- **`SI`** — existe un cuadro publicado que cruza **la variable de la fila** con **su eje de condicionamiento**, y se cita archivo, hoja, fila y cifra. Es la receta literal que `ACT-PIL-2` le dejó escrita a mesa: *«buscar el cuadro que cruce la variable con el eje de condicionamiento de la fila; si el cruce exacto no está listado, la celda es `NO`»*.
- **`NO`** — el paso 1 localizó archivos, el paso 2 los abrió, y ese cruce no existe: sólo un **compuesto** que subsume el reactivo, **otro eje**, **otro corte** del mismo eje, o una **razón derivada** que nadie enuncia. Va con el conteo de hojas y cadenas examinadas.
- **`PENDIENTE-FUERA-DE-INDICE`** — el paso 1 no puede producir candidatos porque el publicador no es INEGI (§5).

Diferencias de **normalización** o de **base poblacional** entre lo publicado y lo que pide la fila no cambian el veredicto, pero se escriben en la celda (`TIC-07` publica composición por sexo y no prevalencia dentro de cada sexo; `SFT-09` publica 15–49 y la fila pide 15–54; `EMP-06` publica 12+ y la fila pide 15+; `EMP-05` sale del cuestionario básico y la fila cita el ampliado).

---

## 4 · El resultado, fila por fila

**24 `SI` · 24 `NO` · 8 `PENDIENTE-FUERA-DE-INDICE`.**

| id | encuesta · ola | variable | veredicto | cifra o razón, en corto |
|---|---|---|---|---|
| `CIV-01` | ENCIG · 2023 | `P8_3_1` | NO | el cuadro 4.10 de IV_corrupcion_encig2023_est.xlsx publica el COMPUESTO 'experiencia con algun acto de corrupcion' por tipo de tramite (5 383 732 caso |
| `CIV-02` | ENCIG · 2023 | `P11_1_02` | **SI** | hoja 6.1 fila 34 'Policias': Mucha confianza = 2 074 650 absolutos y 3.9527 por ciento sobre 52 486 649 |
| `CIV-03` | ENCIG · 2021 | `P9_1` | NO | 0 coincidencias de 'cinco anos', 'recuerda' e 'insinuado' |
| `CIV-04` | ENCIG · 2019 | `P5_10A` | **SI** | hoja 2.9 fila 12, servicio de metro o tren ligero: 'Satisfecha' = 4 406 652 y 57.4863 por ciento sobre 7 665 566 usuarios, por entidad federativa |
| `CIV-05` | ENCUCI · 2020 | `AP5_4_2` | **SI** | hoja 2.25 fila 20 'Libertad de voto': Muy frecuente = 57 216 644 y 59.336 por ciento sobre 96 427 583, por sexo, region, edad y dominio |
| `CIV-06` | ENCUCI · 2020 | `AP5_3_8` | **SI** | hoja 2.17 fila 26 'Instituto Nacional Electoral': Mucha confianza = 18 090 304 y 18.761 por ciento sobre 96 427 583 |
| `CIV-07` | ENVIPE · 2023 | `BP1_20` | **SI** | hoja 3.1 fila 11: 'Delitos denunciados' = 2 926 213 y 10.9048 por ciento sobre 26 834 278 delitos ocurridos en 2022, por entidad federativa |
| `CIV-08` | ENVIPE · 2023 | `AP4_4_03` | NO | el corte por espacio fisico ('la calle') solo se publica para la Ciudad de Mexico, cuaderno IX cuadros 9.25 a 9.28 |
| `CIV-09` | ENVIPE · 2023 | `AP5_6_02` | **SI** | indicador 6200028491 'Porcentaje de personas de 18 anos y mas que identifica a la Policia Preventiva Municipal y considera muy efectivo el trabajo de  |
| `CIV-10` | ENVIPE · 2018 | `AP5_6_04` | **SI** | indicador 6200028494 'Porcentaje de personas de 18 anos y mas que identifica a la Policia Federal y considera muy efectivo el trabajo de esta', nacion |
| `CIV-11` | ENVIPE · 2025 | `AP4_4_01` | NO | mismo hallazgo que CIV-08: 'su casa' como espacio fisico solo aparece en el cuaderno IX de la Ciudad de Mexico (9.25 a 9.28), no en el nacional |
| `CIV-12` | ENPOL · 2021 | `P3_21_1` | **SI** | hoja 3.56 fila 11 'Intentaron apropiarse o le pidieron de forma directa' = 33 281.788 y 92.2329 por ciento de las 36 084.521 victimas de corrupcion en |
| `DIN-01` | ENIF · 2018 | `P5_4` | NO | el cuadro 4.6 cruza tenencia por TAMANO DE LOCALIDAD ('Cuenta o tarjeta de nomina' 52.4995 por ciento) y el 4.7 cruza por sexo pero CONDICIONADO a ya  |
| `DIN-02` | ENIF · 2015 | `P6_4` | NO | no hay tabulados publicados de ENIF 2015 en el universo indexado |
| `DIN-03` | ENIF · 2012 | `P7_1` | NO | no hay tabulados publicados de ENIF 2012 en el universo indexado |
| `DIN-04` | ENIF · 2024 | `P4_4_6` | NO | el reactivo SI se publica ('Utilizo su tarjeta de credito o solicito un credito' = 3 809 307 y 10.971 por ciento nacional, por sexo) pero el eje de la |
| `DIN-05` | ENFIH · 2019 | `P8_1_1` | NO | el reactivo SI se publica ('Caja de ahorro de conocidos o del trabajo' = 2 179 557, mujeres 1 034 219) pero el corte publicado es 'De 1 a 14 999 habit |
| `DIN-06` | ENFIH · 2019 | `P8_8_2` | **SI** | hoja 6.4 fila 14 'Tarjeta de credito bancaria': Total 10 807 422, Mujeres 5 150 365 sobre 45 937 254 mujeres de 18 anos y mas |
| `DIN-07` | Encuesta de Competencias Financieras ( · 2019 | `SF2` | *fuera de índice* | el publicador de la fila es Banxico/CNBV: el diseno de dos pasos de FP-93 no puede alcanzarla POR CONSTRUCCION, no por fallo de busqueda. Necesita un  |
| `DIN-08` | Encuesta de Competencias Financieras ( · 2019 | `SF7` | *fuera de índice* | publicador Banxico/CNBV, fuera del alcance del diseno de dos pasos |
| `DIN-09` | Encuesta de Competencias Financieras ( · 2021 | `SF5` | *fuera de índice* | publicador Banxico/CNBV, fuera del alcance del diseno de dos pasos |
| `DIN-10` | Encuesta de Competencias Financieras ( · 2021 | `SF13` | *fuera de índice* | publicador Banxico/CNBV, fuera del alcance del diseno de dos pasos |
| `DIN-11` | ENIF · 2018 | `P5_3` | NO | 0 coincidencias de 'cuentas que no cobran comisiones' |
| `DIN-12` | Encuesta de Competencias Financieras ( · 2021 | `SF10e` | *fuera de índice* | publicador Banxico/CNBV, fuera del alcance del diseno de dos pasos |
| `SFT-01` | ENASIC · 2022 | `P4_13` | **SI** | Cuadro 2.7 fila 13: 'Si necesita que le brinden cuidado complementario' = 1 873 714 y 33.3049 por ciento sobre 5 625 946 personas con discapacidad o d |
| `SFT-02` | ENASIC · 2022 | `P4_12` | **SI** | Cuadro 2.22 fila 13: 'Promedio de horas diarias que se queda sola(o)' = 7.0511 para personas con discapacidad o dependencia |
| `SFT-03` | ENASIC · 2022 | `P7_12_2` | **SI** | Cuadro 5.15 fila 21: 'El cuidado de las y los integrantes del hogar es solo responsabilidad de la mujer', De acuerdo = 6 799 257 y 8.474 por ciento so |
| `SFT-04` | ENASEM · 2018 | `H16D_18` | NO | los cuadros 2.3 a 2.7 publican 'condicion de limitacion o imposibilidad para realizar actividades basicas', no el reactivo de AYUDA RECIBIDA que cita  |
| `SFT-05` | ENASEM · 2021 | `H14_21` | NO | identico a SFT-04: se publica limitacion o imposibilidad para vestirse (con nota al pie que la excluye), no el reactivo de ayuda recibida |
| `SFT-06` | ENASEM · 2024 | `F55_24` | NO | 0 coincidencias de 'hermanos' ni de 'compartir las responsabilidades' |
| `SFT-07` | ENUT · 2019 | `P6_10_7` | NO | lo publicado es la ACTIVIDAD clasificada 'Gestion y administracion' (70 101 571 personas, tasa de participacion 70.5887), agregado de la clasificacion |
| `SFT-08` | ENUT · 2024 | `TRAB_NO_REM_CUID_HOG` | **SI** | Cuadro_2.2.1 fila 34 'Trabajo no remunerado de cuidado a integrantes del hogar': 75 325 111 personas, tasa 69.8557 y PROMEDIO DE HORAS SEMANALES 18.86 |
| `SFT-09` | ENADID · 2023 | `P8_10` | **SI** | Cuadro 5.3 fila 13 'Usuarias actuales' = 17 805 045 mujeres |
| `SFT-10` | ENDIREH · 2021 | `P14_3_11` | **SI** | hoja 14.1 fila 33 'La ha ignorado, no la toma en cuenta o no le brinda carino' = 7 034 078 y 14.8557 por ciento |
| `SFT-11` | ENBIARE · 2021 | `PA3_02` | **SI** | hoja T2_EUM fila 19 'Salud': promedio de satisfaccion = 8.3211 (18 a 29 anos 8.9708 |
| `SFT-12` | ENBIARE · 2021 | `PC1_1` | **SI** | hoja T1_EUM fila 77 'Cuido o atendio en casa a personas que no pueden valerse por si mismas' = 30 881 704 (hombres 11 813 969, mujeres 19 067 735) |
| `TIC-01` | ENOE · 2024 1er trimestre | `p3i` | NO | 0 coincidencias de 'sindicato' en todo el paquete publicado de la ENOE 2024 |
| `TIC-02` | ENOE · 2024 1er trimestre | `p3j` | **SI** | hoja Total_424 filas 149 a 154 '4.6 Disponibilidad de contrato escrito': sin contrato escrito 17 483 432 de 40 868 290, abierto por areas mas y menos  |
| `TIC-03` | ENOE · 2024 1er trimestre | `p2d6` | NO | el medio de busqueda de empleo no se publica |
| `TIC-04` | ENOEN · 2022 2do trimestre (EN | `p3d` | NO | lo publicado es la clasificacion DERIVADA 'posicion en la ocupacion' (empleadores frente a trabajadores por cuenta propia), no el reactivo p3d |
| `TIC-05` | ENTI · 2022 | `P1` | **SI** | hoja 'Nacional ' fila 54 '1.6 Condicion de ocupacion / Ocupados' = 2 333 129 sobre 28 413 429 de 5 a 17 anos, por sexo (hombres 1 611 673, mujeres 721 |
| `TIC-06` | ENTI · 2022 | `P2` | NO | 0 coincidencias de 'meses del ano', 'tiempo en este trabajo' ni 'antiguedad' |
| `TIC-07` | ENDUTIH · 2023 | `P7_1` | **SI** | hoja 2023_unal560 fila 14 'Usuarios de internet, segun sexo, 2023' = 97 012 089 (hombres 45 975 725 y 47.3917 por ciento, mujeres 51 036 364 y 52.6083 |
| `TIC-08` | ENDUTIH · 2024 | `P7_15` | NO | 'redes sociales' solo aparece como categoria de USO de internet ('Para acceder a redes sociales') |
| `TIC-09` | ENDUTIH · 2025 | `P7_10_2` | NO | 0 coincidencias de 'bolsas de trabajo' ni de 'busqueda de empleo' |
| `TIC-10` | MOCIBA · 2023 | `P4_01` | **SI** | hoja 1.22 fila 20 'Mensajes ofensivos' = 6 128 677 y 33.3141 por ciento de quienes vivieron ciberacoso |
| `TIC-11` | MOCIBA · 2024 | `P3` | **SI** | cuadros 1.13, 1.14 y 1.15 'condicion de recepcion de correo basura o virus para danar sus equipos o informacion' por entidad y grupos de edad, con cua |
| `TIC-12` | ENOE · 2024 1er trimestre | `p3n` | NO | 0 coincidencias de 'como se entero' ni de 'se entero' |
| `EMP-02` | ENAFIN (Encuesta Nacional de Financiam · 2024 | `razon derivada de Creditos` | NO | se publica 'Numero de creditos que solicitaron las empresas, segun aprobados o rechazados, por tamano de empresa': los dos totales, nunca la RAZON. La |
| `EMP-03` | ENAFIN (Encuesta Nacional de Financiam · 2024 | `razon derivada de Total de` | NO | se publica 'Numero de empresas que tuvieron algun credito o financiamiento ... por tamano de empresa' |
| `EMP-04` | ENAFIN (Encuesta Nacional de Financiam · 2024 | `razon derivada de Creditos` | NO | se publica 'Numero de creditos ... segun aprobados o rechazados, por tamano de localidad' |
| `EMP-05` | CPV Censo de Poblacion y Vivienda -- C · 2020 | `SITUA_CONYUGAL` | **SI** | hoja 01 filas 13 y 14: 'Poblacion de 12 anos y mas por tamano de localidad, sexo y grupos quinquenales de edad segun situacion conyugal' |
| `EMP-06` | CPV Censo de Poblacion y Vivienda -- C · 2020 | `SITTRA` | **SI** | hoja 01 fila 9: 'Estimadores de la poblacion de 12 anos y mas ocupada y su distribucion porcentual segun posicion en el trabajo por tamano de localida |
| `DOC-03` | CNBV (desenlace documentado no-encuest · jun 2025 | `razon IMOR_ajustado(Azteca` | *fuera de índice* | el publicador es CNBV/HR Ratings: la prueba de dos pasos de FP-93 no alcanza la fila por construccion. El NO previo por aserto estructural no se toca |
| `DOC-05` | BMV / CNBV, reportes trimestrales de G · 4T2025 | `castigos del ejercicio com` | *fuera de índice* | publicador BMV/CNBV, fuera del alcance del diseno de dos pasos. El NO previo por aserto estructural no se toca |
| `DOC-06` | BMV / HR Ratings, Financiera Independe · 4T2024 parametriza, 4T | `IMOR ajustado de la carter` | *fuera de índice* | publicador BMV/HR Ratings, fuera del alcance |

---

## 5 · Un límite del diseño de `FP-93`, medido y no supuesto

Los dos índices que la firma nombra son **100 % `inegi.org.mx`**, y eso se mide, no se supone:

```
# control positivo
grep -ic inegi data/indice-descarga-masiva-2026-08-05.tsv   → 7930   (de 7930 filas)
grep -ic inegi data/indice-canastas-2026-08-08.tsv          → 17163  (de 17163 filas)
# los publicadores de las 8 filas
'competencias financieras' · 'ecf' · 'banxico' · 'cnbv' · 'gentera' ·
'compartamos' · 'findep' · 'azteca'                          → 0 y 0 en los dos índices
```

Ocho filas quedan por tanto fuera del alcance **por construcción, no por fallo de búsqueda**: `DIN-07`, `DIN-08`, `DIN-09`, `DIN-10`, `DIN-12` (Encuesta de Competencias Financieras, Banxico/CNBV) y `DOC-03`, `DOC-05`, `DOC-06` (CNBV / BMV / HR Ratings). Su `NO` estructural previo **no se toca**; se etiquetan `PENDIENTE-FUERA-DE-INDICE` y abren **`FP-134`**: si mesa quiere un segundo universo de búsqueda fuera de INEGI, y con qué índice.

Un límite más, declarado y no explotado: la canasta `sala_de_prensa` (70 filas, boletines y comunicados por año) **no trae columna `programa`**, así que el filtrado «por programa + año» que `FP-93` diseñó no la alcanza. Un boletín es el caso paradigmático de «cifra publicada»; este acto no extendió el diseño para incluirlo, y lo deja nombrado.

---

## 6 · Qué le hace esto a las cuotas del marco

`ADV1-M1` fija para el filtro (i) un tope de **20 %** de candidatas publicadas — es el control de memoria: si la cifra que el árbitro va a producir ya está publicada, el baseline puede haberla memorizado y el duelo no discrimina.

| Denominador | Publicadas | Porcentaje | Tope | Veredicto |
|---|---|---|---|---|
| Marco completo, `60` | **28** | **46.7 %** | 20 % | **NO CUMPLE** |
| Marcador puntuable (`P1`+`P2`), `50` | **22** | **44.0 %** | 20 % | **NO CUMPLE** |

Reparto por grado de dependencia, re-derivado por comando sobre el archivo ya escrito: `P0` **6 de 10** · `P1` **7 de 17** · `P2` **15 de 33**.

Antes de este acto la cuota se reportaba **CUMPLE con `4 = 6.7 %`**. Esa cifra era correcta **dado lo que se sabía**: sólo se habían contado las 4 filas con evidencia positiva en la mano, y las 56 restantes estaban declaradas indeterminadas. Ejecutada la prueba, la cuota se pasa por un factor de **2.3**.

**El ejecutor mide y no decide.** `FP-133` queda `ABIERTA` con las cuatro salidas nombradas, sin recomendar ninguna:

1. **Podar** filas `SI` hasta el tope y re-congelar el marco (rompe el pre-registro si se hace después del sorteo; antes, no).
2. **Subir el tope** con razón escrita.
3. **Redefinir el filtro (i)**: que «publicada» signifique *la cifra exacta de la celda* y no *el cuadro que cruza la variable con el eje*. Con la lectura estricta, varias de las 24 `SI` bajarían a `NO` (las celdas están en la propia columna, con la diferencia de normalización o de base anotada: `TIC-07`, `SFT-09`, `EMP-05`, `EMP-06`, `SFT-11`, `TIC-11`).
4. **Aceptar el marco como está** y declarar el sesgo de memoria como limitación del piloto.

Y una consecuencia operativa que este acto no ejecuta pero sí nombra: **con la cuota rota, el sorteo de `ACT-PIL-3` no debería correr.**

---

## 7 · Dos hallazgos que este acto no estaba buscando

**(a) El hueco del filtro (iii) es menor de lo que `FP-80` declaró.** `FP-80` dice que «el CV del árbitro no existe antes de que exista el árbitro», con `EMP-01` como única excepción del marco. Abriendo los tabulados aparece que **INEGI publica indicadores de precisión con CV para varias celdas del marco**: ENDUTIH 2023 trae `CV 0.9305` (hombres) y `0.8629` (mujeres) para la celda de `TIC-07`; el cuestionario ampliado del CPV 2020 trae `CV 0.351` para la de `EMP-06`; ENCUCI 2020, ENTI 2022, ENASIC 2022, ENVIPE y ENPOL publican cuadernos `_cv`/`_err`/`_int` completos junto a cada cuadro de estimaciones. **No se toca la columna `cv_arbitro`** — está fuera del perímetro de este encargo — pero queda dicho: el filtro (iii) está más cubierto de lo que el marco supone, y quien lo cierre tiene material.

**(b) La celda de `SFT-03` está publicada al cuarto decimal.** `ENASIC 2022`, `P7_12_2`, cuadro 5.15 de `01EST_T5 Percep sobre cuidados`: *«El cuidado de las y los integrantes del hogar es solo responsabilidad de la mujer»*, **De acuerdo = 6 799 257 = 8.474 %** sobre 80 237 061 personas de 15 a 60 años, abierto por sexo (8.1786 % mujeres, 8.8068 % hombres). Es el mismo instrumento y la misma familia de reactivos sobre los que trabajaron `ENASIC-SPLIT` y `PROD-P638`. El filtro (i) mordió justo donde tenía que morder.

---

## 8 · Perímetro, verificado por comando

El marco cambió en **56 líneas de 60** y en **una sola columna**. Comparación campo a campo entre `HEAD` y el árbol:

```
columnas que cambiaron (0-index): [9] -> nombre: ['publicada']
filas: 60   ·   campos por fila: 17 en todas
```

Los **929 MB** descargados viven en `scratchpad`, **no** en el repo ni en `data/raw`: este acto **no registra ningún payload nuevo** en `data/manifiesto.yaml` y por tanto no ejerce `A.1` ni `A.7`. Fuera del marco sólo se tocaron `forense/firmas-pendientes.tsv`, `canon/gobernanza-v1_15.md`, `canon/estado-programa-v1_10.md`, esta nota y el encargo.

**Concurrencia — cuatro movimientos de `main` durante el acto, y tres renumeraciones.** La rama apareció fusionada con `origin/main` por una sesión concurrente que este acto no ordenó (`e70b424`; `git reflog` lo muestra: *«merge origin/main: Fast-forward»*), y `origin/main` volvió a moverse dos veces más: a `a5f1bf6` (`PR #328`, `PR #329`) y a `7848b97` (`PR #331`, `PR #332`). Dos fusiones a mano, con **conflictos reales** las dos veces: (1) en `forense/firmas-pendientes.tsv`, `BANDAS-DOC-6` marcó `FP-94` como ejecutada en la misma región donde este acto marcó `FP-93` — resuelto por unión, conservando las dos; (2) en el tablero, en `gobernanza` y en `estado` a la vez, porque `ACTO EVAL-COMPARTAMOS-LLAVE3` tomó **`ADR-162`**, **`FP-131`** y **`FP-132`**, exactamente los tres números que este acto ya había escrito. Renumerado a `ADR-163`, `FP-133` y `FP-134`, re-derivado por comando sobre `origin/main = 7848b97` (máximo `162`, únicos `162`, sin huecos) — misma regla de la casa: renumera quien fusiona segundo. El número de ADR se re-derivó cuatro veces en total: `160` al arrancar (mal, ver abajo), `162` tras la primera fusión, `162` de nuevo tras la segunda, **`163`** tras la tercera.

**Un tropiezo propio, y la regla que lo atrapó.** El primer intento de derivar el máximo de ADR usó `grep -oE '^\*\*ADR-[0-9]+' | sort -t- -k2 -n | tail -3` y devolvió `156 · 157 · 158`, cuando el árbol ya tenía `160`: `sort -t-` parte en el **primer** guion, así que el campo 2 de `**ADR-158` es `ADR` y no `158`, y el orden numérico se calcula sobre un campo vacío. La re-derivación con un regex explícito dio `máximo 160, únicos 160, sin huecos`. Si se hubiera creído la primera salida, `T15` habría fallado por hueco en la secuencia.

---

## 9 · Lo que este acto deliberadamente NO hace

- **No poda ninguna fila** del marco ni re-congela nada: la cuota rota es una medición, y qué hacer con ella es firma de mesa (`FP-133`).
- **No escribe `marco-candidatas-piloto-v1_1.tsv`.** La saturación de `FP-82` sigue sin ejecutar, con sus dos `PARO` previos, y este acto no la intenta.
- **No toca `cv_arbitro` ni `n_no_ponderado`** pese al hallazgo (a): están fuera del perímetro.
- **No corre el sorteo de `ACT-PIL-3`.**
- **No abre un segundo universo de búsqueda** fuera de INEGI (`FP-134`).
- **No registra payloads.** Los 922 archivos publicados se bajaron para leerlos, no para incorporarlos al corpus.

---

## 10 · Cascada

| Archivo | Qué cambió |
|---|---|
| `forense/marco-candidatas-piloto-v1_0.tsv` | columna `publicada`, 56 celdas, con veredicto `A.4`, universo examinado y cifra |
| `forense/firmas-pendientes.tsv` | `FP-93` → `FIRMADA` + `ejecutada_en`; `FP-133` y `FP-134` nuevas, `ABIERTAS` |
| `canon/gobernanza-v1_15.md` | `ADR-163` y su fila de bitácora |
| `canon/estado-programa-v1_10.md` | línea de candidatas del marco con el reparto de `publicada`; conteo de ADR `162`→`163`; recifrado de suite |
| `forense/notas/2026-08-25-bibliotecario-56-cierre.md` | esta nota |
| `forense/encargos/2026-08-25-BIBLIOTECARIO-56.md` | encargo archivado, `CONSUMIDO` |

**Suite.** `LÍNEA BASE: VERDE`, núcleo **19 FAIL · 147 WARN** (`CHECK_SELFCHECK_CHILD=1 python3 tests/check.py`, iterado a punto fijo y verificado con `--baseline`). El movimiento propio de este acto es **`+1 WARN` y cero `FAIL`**: `T22` sube de 23 a 24 por las dos filas `ABIERTA` que abre (`FP-133`, `FP-134`), que es exactamente lo que `A.12` existe para hacer visible. `T02` se evitó por construcción (sufijo `-cierre`), `T03` por la marca `{cita-ilustrativa}` pegada a la única cita a un archivo que no existe, `T15` por recifrar las tres citas vivas a `163 ADR`. Aparte, y medido **antes** de escribir una sola línea: la base ya venía `ROJO` con dos entradas `T16` heredadas (la línea de `estado` declaraba `145 WARN` y la corrida real daba `146`); se corrigieron en el mismo paso de recifrado, así que este acto **cierra en verde una base que recibió en rojo**.
