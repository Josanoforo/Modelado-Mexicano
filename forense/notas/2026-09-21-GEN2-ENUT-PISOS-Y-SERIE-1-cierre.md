# ACTO GEN2-ENUT-PISOS-Y-SERIE-1 · CIERRE — el dominio cuidado tiene piso, pero del núcleo común, no de la definición sellada; la serie 2009-2024 muestra 2014 ≈ 2019 y un salto uniforme 2019→2024 que el dictamen prerregistrado deja en NO-DECIDIBLE

Encargo archivado por A.3: `forense/encargos/2026-09-21-GEN2-ENUT-PISOS-Y-SERIE-1.md`
(0-bis `308c6843`, sello de cuerpo `67667c8d…`, raíz de acto `308c`). SHA de redacción
`fc13cdcc` = `origin/main` al abrir (delta 0); `main` se movió 5 commits (`#966`) durante el
acto y se fusionó sin conflicto. Entorno **CAJA**: `python3 tools/entorno.py --arranque` →
`ENTORNO-DERIVADO = CAJA · montado=SI archivos_examinados=422 · sin_variable · red 200`.
Worktree `/home/pc0/mm-enut-pisos-serie`, rama `acto/gen2-enut-pisos-y-serie-1`, Opus 5,
sin sub-agentes, **MODO ABIERTO** hasta cada COMMIT-1 y RÍGIDO después (así corrió: ningún
`spec.yaml`, medidor ni módulo se tocó tras `7ebb04de`).

## 0 · Premisas del encargo, verificadas

| premisa | veredicto | evidencia |
|---|---|---|
| `[EXISTE]` «alguien empezó los pisos de ENUT 2019 y no hay CALC sellado… averigua qué acto lo dejó y por qué paró» | **FALSA en su lectura; corregida** | `git log -- forense/prereg-caja/PISOS-ENUT2019-ejes-metadatos-v1_0.tsv` → `094d0566`, `GEN2-PISOS-ENUT2019-EJES-1` (PR #908, MERGED 20/sep 04:20Z, ADR-557). No paró: dictaminó **NO-CONSTRUIBLE por texto** y sus 11 filas son `EXCLUSION-…`. Dirección redactó sin ese veredicto. |
| `[EJECUTADO]` manifiesto: `enut2002_bd_dbf`, `enut2009_bd_dbf`, `enut2014_bd_dbf`, `enut2019_bd_csv`, `enut2019_der_zip` | CIERTA; ENUT 2024 = `enut2024_bd_csv` (+ `enut2024_fd_xlsx`, `enut2024_der_zip`, `enut2024_diccionario_variables_html`) | `grep -n "^- id: enut" data/manifiesto.yaml` (16 ids); 12/12 documentos `COINCIDE` por `tests/manifiesto.py --verifica --id` |
| `[EJECUTADO]` marcador: ENUT 2024 con 11 `SIN-PISO` y 10 `IDENTICO` | CIERTA (y sigue igual al cerrar) | `grep -c ENUT data/corrida0/marcador-segmento.tsv` = 22 (10 NAC IDENTICO, 10 MARG sexo_edad SIN-PISO, 1 MARG razón SIN-PISO, 1 CRUCE RESERVADA); `marcador_segmento.py --json` → `sin_piso=15` antes y después |
| `[LEÍDO]` `reparto_hogar` razón sobre hogares (`FAC_HOG`), `sexo_edad` media | CIERTA | `CALC-ENUT-0001/spec.yaml`, `tools/medidor_cuidado_enut.py:156-240` |
| `[EXISTE]` molde `CALC-PISOS-*-EJES-*` | CIERTA; reusado el estimador (`_estimate`) de `CALC-PISOS-ENVIPE2024-EJES-0002` | `data/corrida0/CALC-PISOS-ENVIPE2024-EJES-0002/medidor.py` |
| `[EJECUTADO]` FP-409 ABIERTA | CIERTA; `CALC-ENUT2024-DISTRIBUCION-HORAS-0002` no se usó como oro | `forense/firmas-pendientes.tsv:397` |
| A.8 `ya_medido familia.cuidado.recae_mujeres_40mas` | `MEDIDA-EN: CALC-ENUT-0001, tramite.yaml` | pegado en la sesión |

## 1 · La bifurcación y la firma de mesa (verbatim)

Pregunta a mesa (§6 del encargo, «si «cuidado» no es construible igual en 2019 y 2024»), con
tres opciones y recomendación. Respuesta de mesa, 21/sep/2026, verbatim de la opción elegida:

> «Núcleo común + CON_CP 2024 como secundario (Recomendado) — Estimando nuevo
> `horas_cuidado_nucleo` (ítems =/≈ de 2014/2019/2024) medido desde ítems crudos en 2019 y
> 2024; en 2024 el mismo medidor reproduce tvar_crea *_CON_CP sumando todos los ítems (oro:
> fórmula INEGI + CALC-ENUT-0001) y reporta CON_CP por eje como secundario. Persistencia
> núcleo↔núcleo; delta núcleo↔CON_CP 2024 declarado como tamaño del cambio de instrumento.
> Serie 2014-2019-2024 (2009 sólo núcleo mínimo, variante declarada en COMMIT-1). Las 21 celdas
> siguen NO-CONSTRUIBLE para CON_CP; el enlace al marcador queda a mesa.»

## 2 · P1 · Comparabilidad por texto (`data/enut-comparabilidad-texto-v1_0.tsv`, 24 filas)

Cero registro de microdato: FD 2009 (pdf), 2014 (xls), 2019/2024 (xlsx), RNM de las cuatro
olas, cuestionario 2009, cabeceras DBF y listados de zip. Lo que fija el diseño:

- **2014 ≡ 2019** en los 24 ítems de cuidado (6.11×11, 6.12×3, 6.13×6 [0-14 anidado],
  6.15×4), mismos textos, filtros y periodo.
- **2024** añade 4 emocionales + 4 esperas «sin hacer otra actividad», exige «de forma
  presente» en el pasivo, parte tres ítems de salud en acompañar/llevar y separa 6-14 de 0-5.
  Controles A.13 sobre 140 filas del FD 2019 y 172 del FD 2014: «consol», «orient», «de forma
  presente», «variables creadas» = 0; «esper» = 4, todas dentro del ítem fusionado de salud.
- **2009** es otra batería: 5.10 dependientes ×6 (TCuidados, una fila por par
  cuidador×dependiente), 5.11 menores de 6 ×3, 5.12 menores de 15 ×5, 5.13 60+ ×2, sin filtro de
  dependencia en 5.11-5.13, y 5.14 «consoló, aconsejó o conversó» (emocional genérico).
- Diseño: 2009/2014 sin `FAC_HOG` (sólo `FAC_VIV`); 2014 llama `EDIS` al estrato; las tablas
  `_indígena`/`_PI` de 2019/2014 son **extracciones** del subconjunto hablante (RNM verbatim:
  «comprende exclusivamente al subconjunto…»), no muestra adicional.

Veredictos: C1 (sellada) `CAMBIO-DE-INSTRUMENTO` fuera de 2024; C2 (núcleo) `CAMBIO-MENOR`
en 2014/2019 y `CAMBIO-DE-INSTRUMENTO` en 2009; C3 (mínimo) `CAMBIO-MENOR` en las tres; C4
razón sigue a su base; C5 trabajo doméstico sólo a nivel de bloque (7 bloques en las 4 olas).

## 3 · COMMIT-1 (`7ebb04de`) y lo que dijo el oro

Spec humana `forense/prereg-caja/ENUT-NUCLEO-ejes-spec-v1_0.md` (sellada `f8481b8a…`),
módulo único `tools/enut_nucleo.py` (guardia de una sola variable: `celdas_de_eje` + auditoría
AST R1-R6 antes de abrir el zip; `groupby` sólo por la llave literal `_llave`; el numerador
«mujer 40+» de la razón vive en `_mujer40` y no produce celda), tres `spec.yaml` generados
desde `catalogo_resultados` (una sola fuente de ids), `tests/test_enut_nucleo_conducto.py`
(cuatro olas sintéticas escritas por el test —CSV y DBF dBase III—, `_valida_outputs` contra
los `spec.yaml` reales, respuesta conocida a 1e-9, celda rara → nulos declarados, 11
mutaciones como control positivo). `preflight` VERDE sobre `7ebb04de` en `origin` antes de
abrir un solo registro.

**Oro (D-22 ampliada), `CALC-ENUT2024-NUCLEO-EJES-0001--7ebb04deaa34`:**
- `ORO-A-R-DELTA = 0.0` — la razón CON_CP recalculada desde `tvar_crea` con FAC_HOG de
  `tsdem` sobre 29 181 hogares es exactamente el `RESULT-ENUT-A-R = 0.22148146779116093` de
  `CALC-ENUT-0001`.
- `VALIDACION-CONCP-*`: |Σ ítems crudos de TMODULO − `*_CON_CP`| máximo 5.7e-14 y **0 personas
  discordantes en los cuatro bloques** (74 053 personas). **La fórmula de INEGI para
  `*_CON_CP` es la suma plana de todos los ítems del bloque**, con `h + min/60` por tramo y
  sin tope — lo que `ADR-557` declaró desconocido queda medido. Consecuencia: una
  reconstrucción desde ítems crudos ES validable, y por eso el núcleo es un estimando y no
  una conjetura.

## 4 · Resultados (los tres CALC `verify` REPRODUCE/IDENTICO; asiento en `replay-evidencia.tsv`)

Media ponderada de horas/semana por persona 12+ (IC95 bootstrap de UPM, 10 000, seed 42):

| celda | MIN 2009 | NUCLEO 2014 | NUCLEO 2019 [IC] | NUCLEO 2024 [IC] | CONCP 2024 | Δ 2019→2024 |
|---|---|---|---|---|---|---|
| nacional | 9.93 | 12.25 | 11.94 [11.63, 12.26] | 8.74 [8.46, 9.02] | 11.10 | −26.8 % |
| hombre | 4.52 | 6.33 | 6.40 [6.18, 6.62] | 4.71 [4.53, 4.89] | 6.64 | −26.4 % |
| mujer | 14.79 | 17.55 | 16.92 [16.47, 17.39] | 12.24 [11.84, 12.64] | 14.97 | −27.7 % |
| 12-17 | 3.28 | 4.80 | 4.59 [4.26, 4.93] | 3.75 [3.46, 4.06] | 5.61 | −18.3 % |
| 18-29 | 13.10 | 15.79 | 15.89 [15.34, 16.46] | 11.61 [11.07, 12.15] | 14.25 | −26.9 % |
| 30-39 | 18.03 | 20.96 | 20.73 [20.02, 21.44] | 16.56 [15.88, 17.26] | 20.70 | −20.1 % |
| 40-59 | 8.01 | 10.19 | 9.86 [9.47, 10.27] | 6.79 [6.45, 7.15] | 8.63 | −31.1 % |
| 60+ | 3.84 | 6.75 | 6.92 [6.46, 7.39] | 4.49 [4.17, 4.81] | 6.01 | −35.1 % |
| hasta primaria | 8.50 | 10.50 | 9.40 [8.99, 9.81] | 6.35 [5.97, 6.74] | 8.19 | −32.4 % |
| secundaria | 11.11 | 13.85 | 13.65 [13.18, 14.12] | 9.68 [9.21, 10.15] | 12.12 | −29.1 % |
| media superior | 11.52 | 12.88 | 12.81 [12.31, 13.32] | 10.10 [9.66, 10.55] | 12.70 | −21.2 % |
| superior | 8.83 | 12.07 | 11.69 [11.11, 12.30] | 8.53 [8.08, 9.02] | 11.09 | −27.0 % |
| urbano | 9.79 | 12.17 | 11.49 [11.15, 11.83] | 8.40 [8.12, 8.69] | 10.74 | −26.8 % |
| rural | 10.43 | 12.55 | 13.55 [12.81, 14.29] | 10.04 [9.29, 10.79] | 12.49 | −25.9 % |

Razón C4 (horas de mujeres 40+ / total del hogar): NUCLEO 2014 0.2184 → 2019 0.2379
[0.2301, 0.2456] → 2024 0.2255 [0.2160, 0.2352]; MIN 2009 0.1973 → 2014 0.2179 → 2019 0.2375
→ 2024 0.2247; CONCP 2024 0.2215 [0.2129, 0.2300] (el sellado: 0.2215 [0.2132, 0.2298]).
Diagnósticos: 0 personas sin `FAC_PER`, 0 hogares con diseño no constante, 0 ítems «Sí» sin
tiempo en las cuatro olas, 1 persona fuera de escolaridad (2024, NIV 99), joins 1:1 completos.

## 5 · P4 · Persistencia, serie y origen móvil (`enut-persistencia-*.tsv`, reglas §5 de la spec)

| conducta | objetivo | cobertura V1 (k/n) | CP95 | MAE V1 | MAE V2 | MAE V3 | dictamen |
|---|---|---|---|---|---|---|---|
| C2 NUCLEO media | 2019 (desde 2014) | 10/14 | [0.419, 0.916] | 0.39 h | — | — | NO-DECIDIBLE |
| C2 NUCLEO media | **2024 (desde 2019)** | **0/14** | [0, 0.232] | **3.13 h** | 2.93 h | — | **NO-DECIDIBLE** |
| C2 NUCLEO razón | 2019 | 0/1 | — | 0.019 | — | — | NO-DECIDIBLE |
| C2 NUCLEO razón | 2024 | 0/1 | — | 0.012 | 0.032 | — | NO-DECIDIBLE |
| C3 MIN media | 2019 (desde 2014) | 10/14 | [0.419, 0.916] | 0.39 h | 2.38 h | — | NO-DECIDIBLE |
| C3 MIN media | 2024 (desde 2019) | 0/14 | [0, 0.232] | 3.14 h | 2.91 h | 4.50 h | NO-DECIDIBLE |
| C3 MIN razón | 2019 | 0/1 | — | 0.020 | 0.001 | — | TENDENCIA |
| C3 MIN razón | 2024 | 0/1 | — | 0.013 | 0.032 | 0.033 | NO-DECIDIBLE |
| C1 CON_CP (21 celdas) | 2024 | — | — | — | — | — | CAMBIO-DE-INSTRUMENTO (por texto) |

Lectura, separada del dictamen mecánico:

1. **2014 → 2019 persiste de hecho aunque el dictamen no lo declare**: 10 de 14 celdas del
   núcleo caen dentro del IC del piso 2014, MAE 0.39 h sobre niveles de 5-21 h. La regla
   prerregistrada exige CP95_lo ≥ 0.5 (≥ 12/14) y 10/14 no alcanza: NO-DECIDIBLE es la palabra
   correcta bajo la regla, y la regla no se ajusta después de ver el dato.
2. **2019 → 2024 no persiste en ninguna celda** y el salto es **uniforme**: −18 % a −35 %,
   mismo signo en las 14 celdas, incluidas hombres, 12-17 y rural. Una conducta que cambia por
   segmento no baja un cuarto en todos los segmentos a la vez; una batería que cambió sí. Los
   cambios que P1 marcó como `CAMBIO-MENOR` por texto (pasivo «de forma presente»; salud
   partida en acompañar/llevar; ítems nuevos que reparten el mismo tiempo declarado) son la
   hipótesis principal — **no medida aquí, y por eso no se dictamina CAMBIO-DE-INSTRUMENTO**:
   el vocabulario §5.3 sólo lo asigna por texto, y eso es de mesa (FP de este acto).
3. **CONCP 2024 ≈ NUCLEO 2019** en casi todas las celdas (11.10 vs 11.94 nacional; 14.97 vs
   16.92 mujeres). Es decir: la definición sellada de 2024 «recupera» por adición de ítems
   (emocionales + esperas + pasivo presente, +2.36 h nacional, +2.73 h mujeres) lo que el
   núcleo pierde entre olas. Coincidencia de dos efectos, no continuidad: no autoriza ninguna
   serie C1 2019→2024.
4. **La razón C4 se mueve poco y con forma**: MIN 0.197 (2009) → 0.218 (2014) → 0.238 (2019)
   es TENDENCIA por la regla (dos cambios del mismo signo fuera de IC), y 2024 (0.225) la
   rompe. El reparto que carga sobre mujeres 40+ no bajó con el salto de nivel: ambos sexos
   perdieron horas en la misma proporción (−26 % / −28 %).
5. Nada de esto es causa (§10 del encargo): niveles y cambios de un autorreporte con
   simultaneidad; el sesgo de recuerdo por sexo no se mide; lo rural sólo lo asoma `TLOC`.

## 6 · Perímetro, contadores, pisadas

- `cuenta_gen2 = SI` en los tres CALC (firma de dirección §2, verbatim en cada `spec.yaml`);
  `N_corridas_selladas` +3, RESULT +829; **no adopta**: `usos.tsv` idéntico a la base
  (231 filas). Pisadas medidas (`git show fc13cdcc:<tsv> | grep -v <propio> | sort` vs disco):
  `corridas.tsv`, `resultados.tsv`, `usos.tsv` **IDENTICO fuera de filas propias**.
- Marcador: no se edita; `sin_piso = 15` antes y después; las 11 filas ENUT `SIN-PISO` siguen
  `NO-CONSTRUIBLE:…` (ADR-557). El enlace del piso del núcleo a esas celdas es de mesa.
- Ningún archivo de TUBERÍA tocado (`git diff --stat fc13cdcc..HEAD -- .github tests/check.py
  .gitattributes .claude/commands tools/cierre_acto.py tools/tablero_programa.py
  tools/estado_comun.py tools/digesto_tramite.py` = vacío, salvo lo que trajo el merge de
  `main`). Tests nuevos censados (3 filas propias en `censo-tests.tsv`); el conducto necesita
  numpy/pandas/dbfread y corre en CAJA (FP-398 a).
- Cero descargas; nada en `data/raw` cambió.

## 7 · Declaración ADR-46

Antes de congelar, la sesión leyó el dictamen ADR-557, `CALC-ENUT-0001` (spec, medidor,
`resultados.json`), `tools/medidor_cuidado_enut.py`, las 10 medias `sexo_edad` del marcador y
los FD/RNM/cuestionario de las cuatro olas; no es ciega respecto de ENUT 2024 (nivel
agregado) ni del reparto por sexo. **Ningún registro de 2009, 2014 ni 2019 se abrió antes de
`7ebb04de`**, y 2019 sólo después de verificar el oro de 2024 (compuerta §8).
