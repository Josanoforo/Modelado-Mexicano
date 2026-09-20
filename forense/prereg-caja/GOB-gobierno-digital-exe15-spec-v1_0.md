# PILOTO 3 · `gobierno_digital` ENCIG 2025 · `edad × escolaridad` · spec v1.0

**Pre-registro de caja.** `ACTO GEN2-CELDA-D-PILOTO-3-P0`, 20/sep/2026, rama
`claude/lucid-lamport-32k9t3`. Congelada **sin microdato**: ninguna cifra de ENCIG 2025
se leyó para escribirla.

---

## 0 · DOS CONDICIONES SUSPENSIVAS (adenda de mesa, 20/sep/2026)

Esta spec está congelada pero **no habilitada**. Las dos condiciones son parte del
pre-registro y viajan con él:

> **(S1) `COMMIT-2` no corre hasta que `NC-0355` cierre con `MISMO-INSTRUMENTO` o
> `CAMBIO-MENOR`.**
> `NC-0355` es la compuerta de contenido por texto (`P0`): redacción del reactivo `P7_3`,
> opciones y códigos, filtro `N_TRA`, flujo y catálogo de trámites, en 2021, 2023 y 2025.
> Si cierra con `CAMBIO-DE-INSTRUMENTO`, **esta spec se retira sin correr**
> (`SUPERADO`, `n_resultados = 0`): no se enmienda, no se adapta, no se reusa.

> **(S2) Primera lectura de caja, antes que `P0`: qué significan `97`/`98`/`99` por ola.**
> Si alguno de los tres es **edad real censurada**, `F1-bis` está sacando población del
> universo, y eso **se reporta a mesa antes de emitir**. La rejilla sellada del árbitro
> (`60-96`) **no se toca aquí**: este acto no reabre una rejilla congelada, sólo advierte.

Quien ejecute el `COMMIT-2` verifica las dos antes de tocar un archivo de datos.

## 1 · Qué se estima

`p(adopta canal digital | edad, escolaridad)` en **ENCIG 2025**, sobre el universo de
**trámites realizados**.

- **Unidad de análisis: TRÁMITE**, no persona. Quien hizo doce trámites contribuye doce
  veces. Es la unidad que pone el árbitro, y la que llevan los `RESULT` sellados de 2021
  y 2023 (`unidad: "trámites"`).
- **Universo:** `N_TRA == '01'` (pago ordinario del servicio de luz).
- **Desenlace:** `adopta = P7_3 ∈ {4,5}` (internet/app · cajero o kiosco inteligente);
  `no adopta = {1,2,6}` (instalaciones · banco o tienda · módulos móviles);
  **fuera del universo** `{3}` (teléfono, canal remoto atendido) y `{7,8,9,blanco}`.
- **Ponderador:** `FAC_TRA`. **Diseño:** `EST_DIS × UPM_DIS`.
- **Llave:** `(ID_TRA, NT_TIPO)`, sin deduplicar.

Contrato idéntico al de las specs selladas de 2021 y 2023 y al de
`tools/medidor_gobierno_digital_encig25.py:12-14,36`. **Esa identidad de códigos se
declara y NO cierra `S1`** (A.15; `ADR-546`): la compuerta es de texto.

## 2 · La rejilla, y por qué es ésta

**Cruce: `edad × escolaridad`**, elegido por regla, no por preferencia — `P2` del acto,
reproducible con:

```
python3 forense/notas/2026-09-20-p2-seleccion-f1bis.py
```

- `edad`: `18-29` · `30-44` · `45-59` · `60-96`
- `escolaridad` (`NIV` agregado): `HASTA-PRIMARIA {0,1,2}` · `SECUNDARIA {3}` ·
  `MEDIA-SUPERIOR {4,5,6,7}` · `SUPERIOR {8,9}`

Rejilla **idéntica, palabra por palabra, a la congelada en las dos olas históricas**
(`CALC-ENCIG2023-CRUCES-HISTORICOS-0002/spec.yaml:32,37` y
`CALC-ENCIG2021-CRUCES-HISTORICOS-0003/spec.yaml:31,36`). La banda superior cierra en
**96**: `97`/`98`/`99` quedan fuera del universo del cruce — ver `S2`.

**16 celdas · 15 `PUNTUADA` · 1 `FUERA-DE-SOPORTE` declarada ex ante.**
`18–29 × HASTA-PRIMARIA` es la única celda bajo `n ≥ 200` y lo es en las dos olas
(n = 110 en 2021, 70 en 2023). Se declara **antes** de ver 2025, y la razón de que sea
escasa es estructural —la cobertura escolar subió— no dato faltante.

**Firma que la habilita: `F1-bis`** (mesa, 20/sep/2026; `FP-389` FIRMADA). El residuo de
edad queda fuera del universo, contado y reportado (107 trámites / masa 571 754 en 2023;
104 / 672 707 en 2021); la coherencia se verifica contra los marginales **recalculados
sobre ese mismo universo**, no contra los sellados con otro denominador; un cruce es
elegible si a lo más un tercio de sus celdas carece de `n ≥ 200` por ola.

## 3 · Candidatos

| id | rol | qué es |
|---|---|---|
| **C2** | **PISO A VENCER** | persistencia compuesta con marginales de 2025, **réplica por réplica**, calculada por esta spec |
| C2-compuesto | control | `CALC-C2-COMPUESTO-RESERVADAS-0001` — ya emitido, **punto sin IC**. Se compara contra el C2 de esta spec como **control**, no como piso |
| C1a | referencia | persistencia compuesta con marginales de **2023** |
| C1b | referencia | `p₂₃(a,b)` directo |
| **S½** | retador (Astra) | `C2 + ½·δ₂₃(a,b)` |
| **Sλ** | retador (Opus) | `C2 + λ·δ̄(a,b)`, `δ̄ = (δ₂₁+δ₂₃)/2` |

`C1a`/`C1b` **no son piso a vencer**: el CALC de persistencia dice `CAMBIA` para ENCIG
(0/10, MAE 10.838 pp), y la persistencia no puede acotar lo que se movió once puntos. Se
reportan para medir cuánto.

### 3.1 · `λ`, derivada y congelada aquí

`λ = τ̂²/(τ̂²+σ̄²)`, `τ̂² = max(0, Var_entre(δ̄) − σ̄²)`, con
`Var(δ̄ₐᵦ) = (EE₂₁² + EE₂₃²)/4` por celda. Derivada de los `DELTA`/`DELTA-EE` **sellados**
sobre las **15 celdas `PUNTUADA`**:

| cantidad | valor |
|---|---:|
| `k` | 15 |
| `media(δ̄)` | +0.011039613453273386 |
| `Var_entre(δ̄)` | 0.028257826067646673 |
| `σ̄²` | 0.003001124084482884 |
| `τ̂²` | 0.02525670198316379 |
| **`λ` congelada** | **0.8937949410086089** |

`τ̂² > 0`: el `max(0, ·)` no ata. Control con 16 celdas, **no congelado**: `0.8310509043319922`.
**`λ` no se teclea**: se deriva con el comando de §2 y se pega aquí. La corrección de
momentos es deliberada — el `λ` del diseño original contaba ruido como señal.

## 4 · Soporte y adjudicación (reglas de la casa, escaladas)

- Celda **`PUNTUADA`** si `n ≥ 200` en **2021, 2023 y 2025**. El tercer requisito sólo se
  puede verificar en el `COMMIT-2`: una celda hoy `PUNTUADA` puede caer a
  `FUERA-DE-SOPORTE` allí, y eso **no es una sorpresa sino el contrato**.
- **`FUERA-DE-SOPORTE` global** si fallan **≥ 5 de 15**.
- Por celda, **`INDECIDIBLE`** con las dos condiciones del programa verbatim
  (`CAREO-ADV-DUELO-diseno-v2:38`).
- Un retador **gana** sólo si vence a `C2` en **≥ ¾ de las `PUNTUADA`**.

### 4.1 · Lectura secundaria pre-registrada

`ΔMAE = MAE(C2) − MAE(j)` con IC **réplica por réplica**, respetando estrato, UPM,
ponderador y agrupación de trámites por persona.

### 4.2 · `B-bis`, sellada aquí

- Nadie vence **y** límite superior de `ΔMAE ≤ 0.5 pp` → **corroborada**, acotada a
  cruces de dos ejes estructurales en tres dominios.
- Nadie vence **pero** el IC aún admite `> 0.5 pp` → **falsador débil**, aunque sea la
  tercera vez.
- **Si ambas lecturas caben, manda `falsador débil`.**
- Un retador vence → limita a `C2` **sólo** en este desenlace, rejilla y ola; `C2` sigue
  adoptado en `DIN` y `TRA` (A.10).
- `Sλ` vence y `S½` no, o al revés → el hallazgo es **sobre cuánto encoger**, y se
  reporta así.

## 5 · Lo que esta spec NO autoriza

- **No adjudica** y no corona a nadie: adoptar es de mesa.
- **No re-rotula** `CALC-PISO-PERSISTENCIA-ERROR-0001`. El `+11 pp` sigue sin atribución
  entre adopción digital real y cambio de instrumento hasta que `S1` cierre.
- **No toca** el marcador, la rejilla del árbitro, ni los CALC sellados.
- Las **7 celdas con IC95 de δ que excluye 0** (2023) se usaron **sólo** para verificar
  que la condición de no-piloto no dispara. **No son evidencia confirmatoria
  independiente**: se leen después de seleccionar entre celdas y entre cruces. Ese límite
  es parte del pre-registro y no se debilita en el `COMMIT-3`.

## 6 · Auditoría (afirma sobre México)

El universo son **trámites realizados**, lo que excluye a quien no tuvo contacto con el
Estado —más rural, más informal—. `edad × escolaridad` en gobierno digital es, antes que
actitud hacia el Estado, **brecha de acceso, conectividad y alfabetización digital por
cohorte**; edad y escolaridad son marcadores de cohorte y acceso, no de confianza.

Lo peligroso leído simplista: **`«+11 pp» = «los mexicanos ya confían en el gobierno
digital»`**. Ni el signo ni la magnitud autorizan esa lectura, y hasta que `S1` cierre
ni siquiera está establecido que el `+11 pp` sea conducta y no instrumento. Evidencia
clase (a).
