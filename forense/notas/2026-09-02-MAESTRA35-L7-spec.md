# COMMIT-1 · Spec congelada · ACTO MAESTRA35-L7 · REGLAS-ACTIVOS-L2

Contra el censo `forense/notas/2026-09-02-MAESTRA35-L7-P0-censo.md`. Cuatro
piezas, todas `EXISTE-SATISFACE`. Regla de señal v2.3 y A-bis 1-4: tasas base
y celdas por ejes son asociaciones dentro de una corrida; escala declarada;
universo restringido no se reconcilia contra el marginal.

**Declaración de proceso, honesta y no ocultada.** A diferencia del
pre-registro ciego de Hito D (ADR-46: una vez que una sesión lee la
estructura de una fuente, no puede pre-registrar hipótesis nuevas contra
ella), este lote es apparatus B-bis/A-bis: el censo P0 exige abrir microdato
para verificar existencia, catálogos y no-degeneración — y construir un
lector nuevo (lección `feedback_lector_nuevo_devuelve_vacio_no_error`) exige
correrlo para verificar que no falla en silencio. Las cuatro definiciones de
abajo se fijaron por su mérito metodológico propio (lectura más literal del
catálogo, reuso de una definición ya validada por un acto previo, exclusión
de una categoría por razón conceptual) — no se ajustó ninguna después de ver
si el resultado "se veía mejor". Donde hubo una decisión con más de una
lectura defendible (P4_10, clasificación de `edo_civil1`), la razón de la
elección se declara ANTES de la cifra de `P1`, no después. Lo que sí se
compromete aquí, en firme: el número que reporte `COMMIT-2` es la salida
literal de estos scripts, ya construidos y ya probados por no-crash/no-
degeneración — no se reescribe ninguna definición entre este commit y el
siguiente.

---

## 1 · Pieza (a) — R7.2 · `civico.denuncia.con_seguro` (ENVIPE 2025)

- **Script:** `tools/medidor_denuncia_seguro_envipe25.py`
- **Variables:** `BP2_1` (cobertura de seguro, `TMod_Vic`), `BP1_20`
  (denuncia), `BPCOD` (tipo de delito, para el universo).
- **Universo:** `BPCOD='01'` (robo total de vehículo) `∧` `BP2_1 ∈ {1,2}`
  (excluye `9` no especificado). n=1 016 de 40 280.
- **Ponderador:** `FAC_DEL`. **Diseño:** `EST_DIS` × `UPM_DIS`.
- **Desenlace:** `BP1_20=='1'` (denunció).
- **Dicotomización del eje:** `BP2_1='1'`→asegurado, `BP2_1='2'`→no asegurado.
- **Escala:** proporción ponderada, bootstrap conglomerado 10 000/seed 42.
- **Eje único** (`cobertura_seguro`, 2 celdas: no asegurado, asegurado),
  **signo esperado: `asc`** (asegurado > no asegurado — línea 179 del modelo:
  "SI es robo de vehículo asegurado ENTONCES sí denuncia"). Cobertura 100%
  del universo declarado.
- **B-bis pre-registro:** `CORROBORADA` si IC95 sin traslape en la dirección
  esperada; `CONTRARIA` si sin traslape en contra; `NO-DISCRIMINA` si
  traslapan. Control de regresión obligatorio: debe reproducir 79.1%/67.2%/
  11.9pp (`hitoD-R7_2-veredicto`/`revision`, 4/ago/2026) — si no reproduce,
  PARA antes de reportar nada nuevo.

## 2 · Pieza (b) — R5.3 · `familia.union.libre` (EDER 2017 + ENADID 2023)

- **Script:** `tools/medidor_union_libre.py`
- **D1 EDER — Variables:** `edo_civil1` (`historiavida.csv`), `anio_nac`,
  `anio_retro`. **Universo:** primer código no-cero por persona
  (`folioviv+foliohog+id_pobla`) en orden de `anio_retro`, restringido a
  `edo_civil1 ∈ LIBRE ∪ DIRECTO` (códigos ambiguos declarados, no forzados).
  n=18 687 de 23 831. **Ponderador:** `factor_per`. **Diseño:** `est_dis` ×
  `upm` (`vivienda.csv`, join por `folioviv`).
  **Dicotomización:** `LIBRE={1,12,13,14,17,18,126}` vs.
  `DIRECTO={2,3,4,26,27,28,46,47,48}` — LIBRE incluye los códigos "posterior
  a Inicio de Unión libre" porque codifican que la unión SÍ empezó libre
  aunque la fila exacta de inicio esté fuera de la ventana del panel;
  verificado que esto no reintroduce censura (0 personas con primer-no-cero
  en la familia de disolución pura `{6,7,8,60,70,80}`).
  **Eje:** cohorte de nacimiento, 4 tramos (`1961-1970`,`1971-1980`,
  `1981-1990`,`1991+`), **signo esperado `asc`** (cohortes más jóvenes, más
  unión libre — baja garantía institucional es tendencia reciente/creciente).
- **D2 ENADID — Variables:** `p3_27_ag` (`TSDEM.csv`), `edad`.
  **Universo:** 15+ `∧` `p3_27_ag ∈ {2,3}` (casada(o) o unión libre —
  excluye soltero/separado/divorciado/viudo del denominador porque la regla
  compara las dos formas institucionales alternativas). n=152 950 de
  277 003. **Ponderador:** `fac_viv`. **Diseño:** `est_dis` × `upm_dis`.
  **Dicotomización:** `p3_27_ag=='3'` (unión libre) vs. `=='2'` (casada).
  **Eje:** tramos de edad (`18-29`,`30-44`,`45-59`,`60+`, proxy de cohorte),
  **signo esperado `desc`** (más jóvenes, más unión libre).
- **Escala (las dos piezas):** proporción ponderada, bootstrap conglomerado
  10 000/seed 42. **B-bis pre-registro:** mismo vocabulario que pieza (a).
  Las dos piezas se reportan **por separado**, no promediadas — miden
  preguntas distintas (tipo de primera unión vs. prevalencia actual).

## 3 · Pieza (c) — R5.2 · `familia.cuidado.reparto_mujeres40` (ENUT 2024)

- **Script:** `tools/medidor_cuidado_enut.py`
- **Variables:** `CUID_ESP_INT_HOG_CON_CP`, `CUID_INT_0A5_CON_CP`,
  `CUID_INT_6A14_CON_CP`, `CUID_INT_60MAS_CON_CP` (`tvar_crea.csv`, ya
  agregadas y validadas por el precedente Y1, reusadas sin redefinir),
  `EDAD`, `SEXO`, `LLAVEHOG`.
- **D1 — horas por sexo × edad (descriptivo, NO proporción de binario):**
  **Universo:** las 74 053 personas de `tvar_crea` (12+). **Ponderador:**
  `FAC_PER`. **Diseño:** `EST_DIS` × `UPM_DIS`. **Desenlace:**
  `horas_cuidado` (continuo, suma de las 4 columnas). **Eje:** sexo × 5
  tramos de edad (`12-17`,`18-29`,`30-39`,`40-59`,`60+`) = 10 celdas — **sin
  signo pre-registrado** (el encargo lo pide como descripción, no como
  prueba dirigida; tope declarado: veredicto máximo `DISCRIMINA`).
- **D2 — proporción del total del hogar (estimador de RAZÓN, no proporción
  de binario):** **Unidad:** HOGAR (`LLAVEHOG`, 29 181). **Ponderador:**
  `FAC_HOG` (`tsdem.csv`, join por `LLAVEHOG`, constante dentro de hogar
  verificado). **Diseño:** `EST_DIS` × `UPM_DIS` (constantes dentro de hogar,
  verificado). **Numerador:** Σ horas_cuidado de integrantes con `SEXO='2' ∧
  EDAD≥40`. **Denominador:** Σ horas_cuidado de TODOS los integrantes del
  hogar. **Escala:** r̂ = Σ(w·num)/Σ(w·den), bootstrap conglomerado
  10 000/seed 42 sobre la razón (`wratio_ic_conglomerado`, este script —
  mismo esquema de resampleo que `wprop_ic_conglomerado`, generalizado).
  Reportado sobre TODOS los hogares (hogares sin carga contribuyen 0/0,
  correctamente, sin sesgar la razón) y, como cifra descriptiva adicional,
  sobre el subconjunto con `total_hogar>0`.
- **B-bis pre-registro para D2:** no hay eje de múltiples celdas para
  aplicar CORROBORADA/CONTRARIA (es una sola razón poblacional); se reporta
  r̂ con IC95 y se contrasta, como contexto declarado (no como veredicto
  adjudicado), contra el share poblacional de mujeres 40+ en el universo
  (26.57%, ya censado en P0 §3).

## 4 · Pieza (d) — R1.1 · `dinero.ahorro.horizonte_corto` (ENIF 2024)

- **Script:** `tools/medidor_horizonte_enif24.py`
- **Variables:** `P4_10` (horizonte), `P3_13` (seguridad social),
  `P5_1_1..6`/`P5_6_1..9` (ahorro informal/formal — reusadas de
  `medidor_ahorro_enif24.py`, no redefinidas).
- **Universo:** personas 18+ elegidas `∧` `P3_13 ∈{1..7}` `∧` `P4_10∈{1..5}`.
  n=9 031 de 13 502.
- **Ponderador:** `FAC_PER`. **Diseño:** `EST_DIS` × `UPM_DIS`.
- **Desenlace 1 — horizonte_corto:** `P4_10=='1'` (principal, lectura más
  literal: "menos de una semana / no tiene ahorros"). **Sensibilidad
  predeclarada:** `P4_10∈{'1','2'}` (<1 mes, convención de "fragilidad
  financiera" de reportes CNBV) — se reporta, no reemplaza al principal.
- **Desenlace 2 — ahorra_solo_informal:** idéntico a `MAESTRA35-L1·P2`
  (informal `∧` `¬`formal), reusado por import directo, no transcrito.
- **Eje único** (`formalidad`/seguridad social, idéntico por import a
  `EJES_P2` de `MAESTRA35-L1`, 2 celdas: sin/con seguridad social),
  **signo esperado `desc`** (sin seguridad social → p más alta, para AMBOS
  desenlaces — el compuesto SI-ENTONCES de la regla predice los dos).
  Cobertura del eje 68.97% del universo 18+ (universo restringido, A-bis 4,
  ya declarado por `L1`, reverificado aquí).
- **Escala:** proporción ponderada, bootstrap conglomerado 10 000/seed 42.
- **B-bis pre-registro:** mismo vocabulario, aplicado independientemente a
  cada uno de los tres desenlaces (horizonte_corto, horizonte_corto-sens,
  ahorra_solo_informal) contra el mismo eje.

---

**El primer resultado que produzca cada uno de estos cuatro procedimientos,
ya congelados arriba, es el que se reporta en `COMMIT-2`.** Si alguno sale
degenerado o revela un defecto de la spec, se corrige hacia adelante en un
`COMMIT-3` propio de esa pieza — nunca reescribiendo este commit ni el de
resultados ya escrito.
