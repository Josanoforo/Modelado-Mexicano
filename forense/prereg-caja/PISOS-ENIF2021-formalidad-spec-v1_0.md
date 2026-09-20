# PISOS ENIF 2021 · eje `formalidad` · tres desenlaces · spec v1.0

El primer resultado que produzca este procedimiento es el que se reporta.

ACTO GEN2-PISOS-ENIF2021-FORMALIDAD-1 (19/sep/2026, CAJA). CALC reservado:
`CALC-PISOS-ENIF2021-FORMALIDAD-0001`. Encargo archivado por A.3 en
`forense/encargos/2026-09-19-GEN2-PISOS-ENIF2021-FORMALIDAD-1.md`. Compuerta:
`#908` fusionado (`8a842af`), cuyo dictamen §2.1 se confirma aquí por lectura
propia, no se hereda.

## 0 · Exposición declarada (ADR-46)

- Leídos antes de congelar: FD y cuestionario de ENIF 2021 y ENIF 2024
  (estructura), el yaml del árbitro (`milpa/tramite-ola5-propuesta-v0.yaml`,
  entradas `dinero.ahorro.via_informal_ejes_enif2024` y
  `dinero.ahorro.horizonte_corto_ejes_enif2024`, con sus `p` de 2024 a la
  vista), `tools/medidor_ahorro_enif24.py:145`, la spec v2.1 y el medidor de
  `CALC-PISOS-ENIF2021-EJES-0003`.
- NO abierto: ningún microdato de ENIF 2021 ni de ENIF 2024. La sesión es
  ciega respecto de `P3_10`, `P4_10` y de cualquier cruce de 2021.
- Cifra esperada: ninguna.

## 1 · P0(a) · El eje, leído por texto en las dos olas

FD 2021: `enif_2021_fd_pdf.zip` → `enif_2021_estructura_del_archivo.xlsx`,
hoja `TModulo`, filas 84–91. FD 2024: `enif_2024_fd.xlsx`, hoja `TMODULO`,
filas 138–146. Cuestionarios: `enif_2021_cuestionario.pdf` p. 7
(DERECHOHABIENCIA, 3.10) y `enif_2024_cuestionario.pdf` p. 7
(DERECHOHABIENCIA, 3.13). Lectura propia (no la tabla del dictamen de #908;
coincide con ella):

| código | ENIF 2021 · `P3_10` «3.10 Por parte de su trabajo, ¿usted tiene derecho a los servicios médicos...» | ENIF 2024 · `P3_13` «3.13 Por parte de su trabajo, ¿usted tiene derecho a los servicios médicos...» |
|---|---|---|
| 1 | del IMSS o Seguro Social? | del Seguro Social (IMSS)? |
| 2 | del ISSSTE Federal o Estatal? | del ISSSTE? |
| 3 | de PEMEX, SEDENA o SEMAR? | del ISSSTE estatal? |
| 4 | de un seguro médico privado? | de PEMEX, Defensa o Marina? |
| 5 | de otra institución? | de un seguro privado de gastos médicos? |
| 6 | No tiene servicio médico (incluye Seguro Popular, Instituto de Salud para el Bienestar) | de otra institución? |
| 7 | — | Entonces, ¿carece de derecho a servicios médicos por parte de su trabajo (incluye IMSS-Bienestar, antes Seguro Popular, Instituto de Salud para el Bienestar)? |
| 9 | No sabe | No sabe |
| b | Blanco por secuencia | Blanco por secuencia |

Misma pregunta (texto idéntico), misma instrucción («LEA HASTA OBTENER UNA
RESPUESTA AFIRMATIVA Y CIRCULE UN SOLO CÓDIGO»), mismo residual único
(«no tiene» 2021 / «carece de derecho» 2024, ambos con la glosa del Seguro
Popular/INSABI, IMSS-Bienestar en 2024). **Única diferencia de contenido:**
el ISSSTE federal y estatal es un solo código en 2021 (`2`) y dos en 2024
(`2`, `3`); por eso el residual es `6` en 2021 y `7` en 2024. No mueve la
dicotomía del árbitro («con seguridad social» = derecho por el trabajo a
cualquiera de las instituciones; «sin» = el residual), porque la partición
ocurre DENTRO del lado «con» y la unión de los códigos afirmativos es la
misma en ambas olas. Cambio menor de rótulo que tampoco la mueve: «seguro
médico privado» (2021) vs «seguro privado de gastos médicos» (2024), ambos
código afirmativo.

**Mapa 2021 congelado:** `P3_10 ∈ {1,2,3,4,5}` → «con seguridad social»;
`P3_10 = 6` → «sin seguridad social»; `9` (no sabe) y blanco por
secuencia → fuera del universo, contados. Cualquier otro valor → fuera del
universo, contado como fuera de catálogo. El árbitro 2024 hace lo homólogo
con `P3_13 ∈ {1..6}` → con, `7` → sin (`tools/medidor_ahorro_enif24.py:145`;
universo yaml `:2164` `P3_13∈{1..7}`).

**Filtro de flujo (quién llega a la pregunta).** 2021, cuestionario pp. 6–7:
3.5 códigos `1,2` → PASE A 3.7; 3.5 `3..8` → 3.6; 3.6 `1..5` → 3.7; 3.6 `6`
(no ayudó ni trabajó) → PASE A 3.11; 3.7 `1` (sin pago) → PASE A 3.11; 3.7
`2..5` → 3.8a; 3.8a «no recibe ingresos» → PASE A 3.10; 3.8b/3.9 → 3.10.
Universo de 3.10 = (`P3_5∈{1,2}` ∨ `P3_6∈{1..5}`) ∧ `P3_7∈{2..5}`.
2024, cuestionario pp. 6–7: 3.8 `1,2` → PASE A 3.10; 3.8 `3..9` → 3.9; 3.9
`7` (no hizo alguna actividad por un ingreso) → PASE A 3.14; 3.10 `6` (sin
pago) → PASE A 3.14; 3.10 `1..5` → 3.11a; 3.11a «no recibe ingresos» → PASE A
3.13. Universo de 3.13 = (`P3_8∈{1,2}` ∨ `P3_9∈{1..6}`) ∧ `P3_10∈{1..5}`.
**Mismo filtro en las dos olas**: quien trabajó o tuvo trabajo el mes pasado
(o lo verificó por actividad) y no es trabajador(a) sin pago. Diferencias
de forma sin efecto en el universo: la verificación de actividad parte
«vendió o hizo algún producto» (2021, un código) en dos (2024); el «sin
pago» es código `1` en 2021 y `6` en 2024; los nemónicos se corren tres
posiciones (3.5→3.8, 3.7→3.10, 3.10→3.13). Diagnóstico declarado en §4: el
medidor cuenta las filas con `P3_10` no blanco que el filtro de flujo no
alcanza y viceversa; se reporta, no se corrige.

## 2 · P0(b) · El desenlace `horizonte_corto`, leído por texto

FD 2021 hoja `TModulo` filas 228–234; FD 2024 hoja `TMODULO` filas 291–297.
Cuestionarios p. 9 en ambas olas (4.10, sin PASE que la condicione; el FD
no lista código `b` en ninguna ola → se pregunta a toda persona elegida).

| código | ENIF 2021 · `P4_10` «4.10 Si usted dejará de recibir ingresos, ¿Por cuánto tiempo podría cubrir sus gastos con sus ahorros?» | ENIF 2024 · `P4_10` (mismo texto; «¿por» en minúscula) |
|---|---|---|
| 1 | Menos de una semana/ No tiene ahorros | idem |
| 2 | Al menos una semana, pero menos de un mes | idem |
| 3 | Al menos un mes, pero menos de tres meses | idem |
| 4 | Al menos tres meses, pero menos de seis meses | idem |
| 5 | Seis meses o más | idem |
| 8 | No responde | idem |
| 9 | No sabe | idem |

Mismo texto, mismas siete opciones, mismos códigos, mismo nemónico, sin
filtro en ninguna ola. **Dictamen (b): CONSTRUIBLE.** Las dos celdas de
`horizonte_corto × formalidad` se miden; el acto mide las seis.

## 3 · Rejilla (leída del yaml del árbitro, no tecleada)

`milpa/tramite-ola5-propuesta-v0.yaml` (`origen: repo`, sha256 en
`spec.yaml`): eje `formalidad` de `dinero.ahorro.via_informal_ejes_enif2024`
(desenlaces `ahorra_solo_informal` y `informal_cualquiera`, yaml:1474,
:1547) y de `dinero.ahorro.horizonte_corto_ejes_enif2024` (yaml:2170). El
medidor lee las categorías de esas entradas y falla si no son exactamente
dos por desenlace; el test `tests/test_pisos_enif2021_formalidad.py` prueba
que la tabla de identidad emitida coincide con esa rejilla.

Seis celdas = 3 desenlaces × {sin seguridad social, con seguridad social}.

## 4 · Procedimiento congelado

- Payload: `enif2021_csv` (manifiesto), miembro
  `conjunto_de_datos_tmodulo_enif_2021.csv`, lectura idéntica a
  `CALC-PISOS-ENIF2021-EJES-0003` (`_csv`, `utf-8-sig`/`latin-1`, `dtype=str`).
- Desenlaces `ahorra_solo_informal` (D9) e `informal_cualquiera`:
  **importados, no copiados**, del medidor sellado de
  `CALC-PISOS-ENIF2021-EJES-0003` (`origen: repo`, sha256 fijado en
  `spec.yaml`; el módulo se carga desde los bytes verificados): `_known_any`
  sobre `P5_1_1..6` y `_formal` sobre `P5_4_1..9` × `P5_7_1..9` por posición;
  D9 = informal ∧ ¬formal; indefinido cuando alguna de las dos lo es.
- Desenlace `horizonte_corto` = `P4_10 == "1"` («menos de una semana / no
  tiene ahorros», lectura literal, la misma que el árbitro yaml:2175); válido
  si `P4_10 ∈ {1..5}`; `8`, `9`, blanco → indefinido.
- Eje `formalidad`: mapa de §1. Universo de cada celda = `P3_10 ∈ {1..6}` ∧
  desenlace definido. Ningún filtro de edad ni de otro eje (el archivo es de
  persona elegida 18+).
- Ponderador `FAC_ELE`; diseño `EST_DIS × UPM_DIS`; bootstrap de UPM con
  reemplazo dentro de estrato, 10 000 réplicas, `numpy.PCG64(42)`, un solo
  plan de réplicas compartido por todas las celdas (`_estimate` importado de
  -0003). IC = percentiles 2.5/97.5.
- Por celda: `-P`, `-IC-LO`, `-IC-HI`, `-N`, `-DEN-W`, `-B-VALIDAS`.
- Control de coherencia (A-bis 4): por desenlace, la celda `UNIVERSO-TRABAJA`
  (todo `P3_10 ∈ {1..6}` con desenlace definido) y
  `COHERENCIA-DELTA-NUM-W` = |num_w(total) − num_w(sin) − num_w(con)|, que
  debe ser ≈ 0. NO se compara contra el nacional de -0003 (otro universo).
- Conteo de excluidos: `P3_10` = 9, blanco, fuera de catálogo; por desenlace,
  indefinidos dentro del universo `P3_10 ∈ {1..6}`.
- Diagnóstico de flujo (declarado aquí, §1): `FLUJO-TRABAJA-N` = filas con
  (`P3_5∈{1,2}` ∨ `P3_6∈{1..5}`) ∧ `P3_7∈{2..5}`; `FLUJO-DISCORDANCIA-N` =
  filas donde ese filtro y «`P3_10` no blanco» difieren. Se reporta; el
  universo se define por `P3_10`, como el árbitro lo hace por `P3_13`.
- Ejecución diagnóstica previa: ninguna. La primera corrida es la que se
  reporta.

## 5 · Lo que esta spec no hace

No mide el error de persistencia de estas celdas; no adopta; no reabre el
dictamen A-BIS-4 (formalidad NO-EMITIBLE en el C2 compuesto por universo
restringido); no toca ENIF 2024, `tools/pisos_ejes.py`, los
`CALC-PISOS-ENIF2021-EJES-*` ni la tabla de identidad de la rejilla.
