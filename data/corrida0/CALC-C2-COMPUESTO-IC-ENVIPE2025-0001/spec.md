# IC RÉPLICA POR RÉPLICA PARA LAS 38 EMISIONES C2 COMPUESTAS DE ENVIPE 2025 — spec v1.0

**ACTO GEN2-GUARDIAN-ENVIPE-EJES-IC-1** · 20/sep/2026 · base `1bb9e2c4` · CAJA
Encargo archivado (A.3): `forense/encargos/2026-09-20-GEN2-GUARDIAN-ENVIPE-EJES-IC-1.md`
Sucede a `GEN2-C2-COMPUESTO-IC-ENVIPE2025-1` (PR #907, `PARO-PREMISA`, 0 de 38; `NC-0361`).

Esta spec se congela en el **COMMIT-1** junto con la extensión del guardián
(`tools/celda_d/marginales_reproduccion.py`) y el medidor
(`data/corrida0/CALC-C2-COMPUESTO-IC-ENVIPE2025-0001/medidor.py`), **antes**
de que el medidor abra un solo byte de ENVIPE 2025. El único microdato que
esta sesión ha tocado antes de sellar es el que el control (iii) de P1 abre
por el módulo congelado: `corrida0 verify` de las dos corridas selladas del
piloto 2 (`REPRODUCE` las dos, en proceso aislado).

> **El primer resultado que produzca este procedimiento es el que se
> reporta.** No hay segunda corrida elegible, no hay recorte, no hay
> sustitución de marginales y no hay ajuste post-hoc de la forma.

---

## 0 · Firma de mesa que autoriza (verbatim)

A la propuesta de dirección «extender el guardián por firma — añadir sexo y
edad a sus ejes admitidos, con edad × dominio vetado por nombre — y después
relanzar el IC»:

> «2 si extendemos»

## 1 · Qué gobierna, y qué no se toca

| Papel | Archivo |
|---|---|
| Guardián (único código autorizado a tocar ENVIPE 2025; extendido en P1) | `tools/celda_d/marginales_reproduccion.py` |
| Construcción de los ejes del árbitro (importada, no copiada) | `tools/ejes_maestra35_l1.py` :: `ESC_2DIG`, `SEXO`, `tramos_edad`, `ORD_*` |
| Marginales `R` sellados del árbitro (control B) | `milpa/tramite-ola5-propuesta-v0.yaml:1672-1731`, entrada `tramite.evasion_norma_ejes_envipe2025` |
| Puntos C2 sellados (control A) | `data/corrida0/CALC-C2-COMPUESTO-RESERVADAS-0001/resultados.json` |
| Lista de celdas y pares (derivada, no editada) | `data/corrida0/c2-compuesto-emisiones-v1_0.tsv`, filas `ola = ENVIPE 2025` |
| Forma de C2 (sellada, se importa) | `tests/test_celda_d_c2.py::piso_log_aditivo` |
| Precedente de bootstrap | `data/corrida0/CALC-TRA-EVADE-NORMA-SXD-EMISIONES-0001/spec.yaml:111-114` (seed 42, PCG64) y `:140` (10 000 réplicas) |

**No se toca**: `ejes_maestra35_l1.py`, los dos CALC del piloto 2,
`marcador_segmento.py`, `estimadores-por-segmento.yaml`, ningún payload que
no sea ENVIPE 2025, nada de ENIF. **No se llama `cruce()`**; no se ve, deriva
ni imprime ningún cruce de 2025; no se adopta; no se actualiza el marcador.

## 2 · Universo, unidad, desenlace, ponderador — los del árbitro, verbatim

* **Payload**: `envipe2025_csv` (manifiesto), miembros `tmod_vic` y `tsdem`.
* **Unidad**: el DELITO declarado por la víctima (una fila de `tmod_vic`),
  no la persona. «Mujeres 60+» son delitos sufridos por mujeres de 60 a 96.
* **Universo**: `BP1_20 ∈ {1, 2}` (n sellado por el árbitro: 40 280); las
  demás filas se cuentan y salen. `FAC_DEL` no numérico o ≤ 0 → PARO.
  `EST_DIS`/`UPM_DIS` vacíos → PARO. `ID_PER` no única en `tsdem` → PARO.
* **Desenlace**: `evade_norma := (BP1_20 == "2") ∧ (BP1_23 ∈ {04,05,06,08})`,
  la CONJUNTA, escala proporción en [0, 1].
* **Ponderador**: `FAC_DEL`; toda proporción es razón de totales ponderados.
* **Diseño**: estrato `EST_DIS`, UPM `UPM_DIS`.

## 3 · Los cinco ejes, y de dónde sale cada uno

| eje | columna cruda | tabla | construcción | celdas (orden) |
|---|---|---|---|---|
| `escolaridad_proxy` | `NIV` | `tsdem` vía `ID_PER` | `ESC_2DIG` | hasta primaria · secundaria · media superior · superior |
| `dominio_urbano_rural` | `DOMINIO` | `tmod_vic` | `{U,C,R}` | Rural · Complemento urbano · Urbano |
| `nacional` | — | — | constante | NAC |
| `sexo` | `SEXO` | **`tmod_vic`** | `SEXO` del árbitro | 1 Hombre · 2 Mujer |
| `edad` | `EDAD` | **`tmod_vic`** | `tramos_edad` del árbitro | 18-29 · 30-44 · 45-59 · 60+ (= 60..96) |

**Desviación declarada respecto del encargo (A.8 contra el árbol).** El
encargo dice «`COLUMNAS_TSDEM` gana las dos columnas crudas». El árbitro las
leyó de **`tmod_vic`** (`tools/medidor_evasion_norma_envipe25.py:188`;
`milpa/tramite-ola5-propuesta-v0.yaml:1680`: «sexo y edad viven en tmod_vic
y no necesitan el join»). Para que el control B pruebe que «la extensión mide
lo que el árbitro midió», las columnas se cargan de `tmod_vic`
(`COLUMNAS_TMOD`). Va como fila de `NO-CORRIDO / RESERVAS`.

**Fuera de banda**: `SEXO ∉ {1,2}`, `EDAD < 18`, `EDAD > 96` (97+ y 99 = no
especificado), blanco → `FUERA`: fuera del universo de ese eje, contado
(`meta.sexo_fuera`, `meta.edad_fuera`) y emitido. La pregunta de ENCIG
(¿edad real censurada o no respuesta?) se cuenta, no se resuelve aquí.

## 4 · Los pares y las celdas — re-derivados del dictamen

`data/corrida0/c2-compuesto-dictamen-v1_0.tsv`, filas de
`tramite.evasion_norma_ejes_envipe2025`, veredicto `EMITIBLE`:

| par | celdas |
|---|---|
| `dominio_urbano_rural × sexo` | 3 × 2 = 6 |
| `edad × escolaridad_proxy` | 4 × 4 = 16 |
| `edad × sexo` | 4 × 2 = 8 |
| `escolaridad_proxy × sexo` | 4 × 2 = 8 |
| **total** | **38** |

`edad × dominio_urbano_rural` **no** está en el dictamen (`NC-0328`,
`RESERVA-CONSUMIDA-SIN-PILOTO`) y está **vetado por nombre** dentro de
`cruce()` (`PARES_VETADOS[2025]`). El medidor PARA si el dictamen trajera
ese par. El medidor PARA si el conteo no es 38.

La lista de celdas y su `resultado_id` se leen de
`c2-compuesto-emisiones-v1_0.tsv` (derivado de `RESERVADAS-0001`), no se
teclean. El id de cada RESULT de este CALC reusa el sufijo del sellado:
`RESULT-C2IC25-{P|IC95INF|IC95SUP|REPLICAS-VALIDAS|REPLICAS-SIN-DEFINIR|P-REDERIVADO|CTRL-PUNTO-DELTA}-<sufijo>`.

## 5 · El procedimiento — una variable por llamada

1. `ola = carga_ola(zip, 2025, reservada=True)`.
2. `rep = replicas_compartidas(ola, seed=42, n_rep=10 000)` — **UNA** por
   ola: `n_h` UPM con reemplazo por estrato, `PCG64(42)`, estratos y UPM en
   orden lexicográfico (la receta del piloto 2, citada arriba).
3. Para cada eje `e` de los cinco: `marginal(ola, e, replicas=rep)` — **una
   llamada, un `str`**. Cinco llamadas en total. Ninguna agrupación por más
   de una variable, ningún `crosstab`/`pivot`, ningún `cruce()`.
4. **Punto** de la celda `(a, b)`:
   `C2 = piso_log_aditivo(p_sellado(a), p_sellado(b), p_sellado(NAC))`
   sobre los marginales **sellados** del árbitro (parámetro
   `marginales_sellados`, citados línea a línea), no recalculados. Se emite
   además `P-REDERIVADO` con los marginales re-derivados aquí (diagnóstico).
5. **IC95** de la celda: por réplica `k`,
   `C2_k = expit(logit p_k(a) + logit p_k(b) − logit p_k)` con los tres
   `p_k` de la MISMA réplica `k` del MISMO remuestreo; IC95 = percentiles
   2.5 y 97.5 (`numpy.percentile`, interpolación lineal por defecto) de las
   réplicas válidas.
6. **`p_k ∈ {0, 1}`** en cualquiera de los tres marginales de la réplica: la
   réplica es SIN-DEFINIR — se descarta y se cuenta
   (`REPLICAS-SIN-DEFINIR-<celda>`); el IC sale de las válidas
   (`REPLICAS-VALIDAS-<celda>`); 0 válidas → IC `null`. Sin recorte, sin
   sustitución. Un marginal sellado en {0,1} → celda NO-CONSTRUIBLE (`null`).

## 6 · Dos controles de coherencia — los dos, o no se publica IC

* **A · el punto reproduce el sellado**: para las 38 celdas,
  `|C2 − RESULT-C2COMP-<sufijo>| ≤ 1e-10` (`umbral_control_punto`; misma
  función, mismos marginales sellados). Delta con signo por celda.
* **B · la réplica base reproduce al árbitro**: para los **cinco** ejes,
  `cotejo(marginal(ola, e), R_sellado[e], tol_p = 1e-6, tol_ic = 1e-4)` —
  las tolerancias del piloto 2 (`CALC-TRA-EVADE-NORMA-SXD-EMISIONES-0001/
  spec.yaml`, `control_arbitro_tol_*`). Sexo y edad son la prueba de que la
  extensión mide lo que el árbitro midió; escolaridad, dominio y nacional
  son la prueba de no-regresión sobre datos reales.

`IC-PUBLICADO = SI` sólo si A y B dan `REPRODUCE`. Si alguno falla:
`IC95INF/IC95SUP = null` en las 38, `IC-PUBLICADO = NO`, y los deltas con
signo quedan a la vista. **Nunca se ajusta nada.** Un `NO-REPRODUCE` no
invalida el árbitro: invalida la afirmación de que este medidor lo reproduce.

## 7 · Qué NO mide este IC

Mide el ruido muestral de un estimador que **supone no-interacción en escala
logit** (rótulo obligatorio; rótulo prohibido: «independencia»). No mide el
error de ese supuesto. La composición del delito por sexo y edad (robo en
transporte, extorsión, fraude) carga buena parte de cualquier diferencia en
evasión: la celda no es una persona. Sin región ni condición indígena.
Ninguna cifra esperada. «Ya tiene intervalo» no es «ya está validado».

## 8 · Contador y registro

`cuenta_gen2 = SI` propuesto, nace `PENDIENTE-DE-MESA`; `uso_motor =
NO-ADOPTA-NADA`; `adoptados_activos` no se mueve. Registro en la vista y
asiento de replay en el mismo acto (E.7). `NC-0361` cierra con este acto.
