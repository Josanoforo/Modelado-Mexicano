# P4 · Los 9 puntos L dejan de parecer candidatos a pin — rótulo sucesor `RE-DERIVADO-CON-ESTIMANDO-DISTINTO` (v1_1)

**Acto:** GEN2-RELEVO-TANDA-4 · **Fecha:** 21/sep/2026 · **Base de redacción del encargo:** `deddfd42`
**Encargo:** `forense/encargos/2026-09-21-GEN2-RELEVO-TANDA-4.md`, P4.
**Antecesor:** `forense/analisis/relevo-tanda-3/P6-los-9-L-con-diferencia-v1_0.md`.

> **Este archivo NO edita el `v1_0`.** El `v1_0` es un análisis fechado y se conserva
> verbatim (A.10 · PARO (d) de este encargo). Todo lo que sigue es sucesor: adopta el
> rótulo que el `v1_0` recomendó en su §4.2 y declara lo medido allí, sin re-derivar la
> tabla ni cambiar un solo número de aquella sesión.

---

## 1 · Qué decide este sucesor

Firma de dirección **7bf5-03**, bajo el mandato de mesa del 21/sep/2026, verbatim
`[LEÍDO: forense/encargos/2026-09-21-GEN2-RELEVO-TANDA-4.md:16]`:

> «Gobierna la mediana que la spec sellada declara; la media de GEN1 queda como
> historia (E.1). El relevo de L exige un CALC propio que mida desde las capturas. Los
> 9 se re-rotulan para que no parezcan candidatos a pin.»

En consecuencia, para los nueve slots `RES-0137`, `RES-0138`, `RES-0142`, `RES-0143`,
`RES-0147`, `RES-0148`, `RES-0152`, `RES-0157`, `RES-0162`:

**Rótulo vigente: `RE-DERIVADO-CON-ESTIMANDO-DISTINTO`.**
**Rótulo anterior: `REHECHO-CON-DIFERENCIA` — historia, no vigente.**

## 2 · Qué dice el rótulo nuevo, y por qué el viejo mentía

`REHECHO-CON-DIFERENCIA` afirma una cosa: *la misma medición, con otro número*. Leído
así, un delta pequeño parece un problema de tolerancia y el slot parece **candidato a
pin**. Lo medido en el `v1_0` dice otra cosa, y son **dos** diferencias independientes,
no una:

1. **Agregador distinto.** El legacy es la **media** de las réplicas `EXTRAIBLE`
   (reproduce exacta en 9 de 9, `v1_0` §1); la spec sellada de `CALC-TRIADA-0001`
   declara **mediana**. Por 7bf5-03 gobierna la mediana y la media queda como historia
   (E.1).
2. **Conjunto de extracción distinto.** GEN1 agrega `L-extraido-v1_2.tsv` (extractor
   v1.2); GEN2 re-extrae de las **224 capturas** con `tools/extrae_l_v1_3.py`. Si el
   agregador fuera la única diferencia, GEN2 tendría que ser la mediana de ESAS mismas
   réplicas: coincide en **1 de 9** (`v1_0` §1).

Dos de las cinco dimensiones del estimando (universo y agregador) **no casan**
(`v1_0` §3). Por A-bis.4 no se aparean: son dos estimandos distintos que coinciden de
cerca. `RE-DERIVADO-CON-ESTIMANDO-DISTINTO` es exactamente eso y nada más.

## 3 · Consecuencia operativa: no son pineables, y no por una guarda que se pueda aflojar

Los nueve son `RESULT-TRIADA-*`. No entran por ninguna de las tres vías vigentes tras
este acto:

| vía | por qué no |
|---|---|
| `i-CRUDO` | `CALC-TRIADA-0001` no mide desde un insumo crudo con hash: ingiere `snapshot-M-triada-v1_0.json`. |
| `ii-CONDUCTA-GEN2` | ninguna conducta de `milpa/tramite.yaml` declara hoy un `RESULT-TRIADA-*` de L con `corrida0_generacion: GEN2`. |
| `iii-DERIVADO-DE-GEN2` (nueva, P3) | la clase exige que **TODO** lo ingerido sea RESULT de un CALC GEN2 sellado. `snapshot-M-triada-v1_0.json` es un número de GEN1: `RECHAZADO-DERIVADO-INGIERE-AJENO`. 4.1 («ingerir un número GEN1 no cuenta nunca») queda intacta. |

La clase (iii) abierta en este mismo acto **no** los alcanza — se dice aquí porque la
pregunta obvia al abrir una puerta nueva es si los nueve caben por ella. No caben, y
`tests/test_pines_mesa.py::test_iii_rechaza_derivado_que_ademas_ingiere_gen1` es la
prueba por mutación de que no cabrán mañana sin que alguien afloje la guarda a
propósito.

**El contador no se mueve por este sucesor:** los nueve ya contaban como legacy y
siguen contando. Este archivo re-rotula, no releva.

## 4 · Dónde vive cada rótulo (universo declarado, A.4)

`[EJECUTADO: git grep -n "REHECHO-CON-DIFERENCIA" sobre el árbol completo]` — 20
apariciones, en seis objetos:

| objeto | qué se hace |
|---|---|
| `forense/analisis/relevo-reconcilia-1/reconcilia-173-v1_0.tsv` (9 filas) | **no se toca**: análisis fechado (A.10). Su token queda como historia; este sucesor es la lectura vigente. |
| `forense/analisis/relevo-reconcilia-1/reconcilia_relevo.py` | **no se toca**: es el derivador de aquel `v1_0`; re-emitiría el token histórico si se volviera a correr sobre el mismo universo, lo que es correcto para un `v1_0`. |
| `forense/analisis/relevo-reconcilia-1/INFORME-relevo-reconcilia-1-v1_0.md` | **no se toca** (A.10). Su §«Aparte» lee el delta como una sola diferencia; el `v1_0` de TANDA-3 §1 ya lo corrigió como hallazgo, no como reescritura. |
| `forense/analisis/relevo-tanda-3/P6-los-9-L-con-diferencia-v1_0.md` | **no se toca** (PARO (d)). Este archivo es su sucesor. |
| `data/adq-demanda-activa-v1_0.json`, `forense/no-corrido.tsv` NC-0425 / NC-260921-…-7bf5-03 | derivados / registros de deuda; el sucesor del rótulo se declara aquí y la NC se re-apunta en el cierre de este acto. |
| `canon/registro-rotulos.tsv` | **se censa aquí** el rótulo nuevo, con el viejo declarado como antecesor (D-6 / ADR-128). |

**La vista no los ofrece como candidatos a pin** `[EJECUTADO: corrida0.py status]`: el
único campo que `status` nombra celda por celda es
`legacy_marco_M_celdas_M_pendientes`, que tras este acto vale `DIN-M-01` — solo campo
`M`, ningún `L`. Los nueve aparecen únicamente dentro del agregado
`legacy_marco_M_por_campo__L=28`, que es un conteo, no una oferta.

## 5 · Lo que este acto NO hace, y quién lo hereda

El relevo de los nueve exige un **CALC propio que mida L desde las 224 capturas** con
el extractor y el agregador declarados — no `CALC-TRIADA-0001`, que ingiere. Este acto
**no lo construye** (§10 del encargo lo prohíbe explícitamente): queda como
`## NO-CORRIDO / RESERVAS` con razón `DIFERIDO-A` y **sin dueño asignado**, y su fila
entra a `forense/no-corrido.tsv`. Mientras ese CALC no exista, los nueve siguen
`LEGACY-GEN1` con el rótulo de este sucesor, que es la afirmación honesta: no es que
fallen una tolerancia, es que nadie ha medido todavía el mismo estimando en GEN2.
