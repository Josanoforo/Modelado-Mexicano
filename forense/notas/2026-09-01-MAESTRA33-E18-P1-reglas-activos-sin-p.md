# P1 · MAESTRA33-E18 — reglas SI-ENTONCES de los 4 dominios ACTIVOS sin p medida

Encargo: `forense/encargos/2026-09-01-MAESTRA33-E18-MAPEO-ACTIVOS.md` (SHA de
redacción `ce5e10d`, base real de este acto `b827824`, ver ARRANQUE). Dominios
ACTIVOS: trámite (§3.3), cívico (§3.7), dinero (§3.1), familia (§3.5) de
`canon/modelo-decision-v4_0.md` §3.B ("Las 49 reglas SI-ENTONCES").

## Método (comando, no juicio)

1. `grep -n "id:" milpa/tramite.yaml` → 8 objetos con `id:` (coincide con
   A.8(1): "milpa/tramite.yaml (8, vía FP-200-style con sello de mesa)").
2. `grep -n "p:" milpa/tramite.yaml` → localiza las entradas con probabilidad
   (`ASIGNADO` o `MEDIDO·p(tasa base ponderada)`).
3. Por cada uno de los 8 objetos, se leyó su bloque completo para decidir si
   la `p` que trae está **atada a una regla SI-ENTONCES del modelo** (mismo
   `situacion`/`si.disparadores` que un `id` de §3.B) o si es una **tasa base
   incondicional** declarada explícitamente `disparadores: {}` /
   `disparadores_estado: PENDIENTE-DE-MESA` con el comentario textual del
   propio YAML: *"sin cita SI-ENTONCES en canon/modelo-decision-v4_0.md
   (líneas 428-473, §2.1-2.2) ... NO se inventa"*.
4. Resultado del paso 3: de los 8 objetos, **5 traen `si.disparadores`
   poblado** (los 5 de trámite) y **3 son tasa base sin disparador**
   (`civico.denuncia.miedo_desconfianza`, `dinero.ahorro.tiene_ahorros`,
   `familia.apoyo.recibe_dinero_familiares` — el propio YAML declara, en sus
   comentarios de líneas 186-191, que buscó cita SI-ENTONCES contra §2.1-2.2
   y dio 0 coincidencias, y que las 49 reglas viven en §3.B, "fuera del
   alcance que el encargo autoriza" que las escribió). **Ninguna de las tres
   está atada a un `id` de §3.B** — no hay match de texto ni de mecanismo
   contra ninguna de las 20 reglas de dinero/cívico/familia listadas abajo.
5. De los 5 objetos de trámite: solo `tramite.mordida.discrecional` tiene una
   entrada `MEDIDO·p(...)` (la enmienda ENCUCI2020, `FP-200=b`) — las otras
   4 traen únicamente `p: ..., clase: ASIGNADO` (mesa, sin calibración).
   `ASIGNADO` no es "p medida" bajo el criterio del encargo (A.8(2): la
   lista es de reglas "sin p medida" — `MEDIDO` es el único estado que
   cuenta como medida).

**Conclusión del método:** de las **24 reglas** SI-ENTONCES de los 4 dominios
ACTIVOS (ver tabla), **23 no tienen ninguna `p` medida atada** y **1**
(`tramite.mordida.discrecional`) sí la tiene (la enmienda ENCUCI2020). Las
3 `p` MEDIDO de trámite/cívico/dinero/familia que sí existen en el YAML no
mapean a ninguna regla de la lista — son tasas base de generador, declaradas
huérfanas de regla por el propio archivo.

## Tabla — 24 reglas, PORQUE, generador, tier, estado de p

| # | dominio | id(s) | PORQUE (mecanismo) | generador | tier | p medida (yaml) |
|---|---|---|---|---|---|---|
| 1 | trámite | `tramite.mordida.discrecional` | trampa social: cada quien paga porque supone que los demás pagan | G1 | FUERTE | **SÍ** — `paga_mordida_encuci2020` p=0.125822, MEDIDO·p(tasa base ponderada), ENCUCI2020, n=13435 (enmienda FP-200=b) |
| 2 | trámite | `tramite.mordida.con_registro` | el registro rompe la trampa social | G1 | FUERTE | NO — solo ASIGNADO (0.88/0.12) |
| 3 | trámite | `tramite.evasion.norma_inutil_sancion_improbable` (yaml: `tramite.evasion_norma`) | cálculo ante institución de baja calidad | (no declarado en yaml `porque.generador`; modelo no cita G explícito) | MEDIA | NO — solo ASIGNADO (0.66/0.34) |
| 4 | trámite | `tramite.gobierno_digital.coercitivo` + `tramite.gobierno_digital.util_sin_coercion` | la confianza institucional no predice adopción; la utilidad sí | (no declarado en yaml) | MEDIA-FUERTE | NO — solo ASIGNADO (0.91/0.09 y 0.71/0.29) |
| 5 | dinero | `dinero.ahorro.volatilidad_horizonte_corto` | G3 (volatilidad) + escasez | G3 | FUERTE **(a)** — 🚫 dominio agrícola INEJECUTABLE (`hitoD-R1.1`) | NO — 0 candidatos en yaml |
| 6 | dinero | `dinero.planeacion.formal_estable` | ingreso estable baja el costo esperado de comprometerse a horizonte largo | (no declarado) | FUERTE **(a)** | NO |
| 7 | dinero | `dinero.ahorro.informal_sin_puente` + `dinero.ahorro.con_puente_y_respaldo` | G1 | G1 | FUERTE | NO |
| 8 | dinero | `dinero.consumo.estatus_mediado_por_credito` | G2 | G2 | FUERTE como correlación | NO |
| 9 | dinero | `dinero.ahorro.seguro_deposito_atenua_aversion` | G1 + diseño | G1 | MEDIA | NO |
| 10 | dinero | `dinero.credito.scoring_alternativo` | el precio absorbe el error de predicción del scoring | (no declarado) | MEDIA **(a)**, métrica AUDITADA (CNBV) | NO |
| 11 | dinero | `dinero.credito.baja_friccion_usura_dano_downstream` | advertencia condicional a la estructura, no a la conducta | (no declarado) | MEDIA **(a)** | NO |
| 12 | cívico | `civico.participacion.contingente` | cálculo del peso del acto | (no declarado) | FUERTE **(a)** | NO — `civico.denuncia.miedo_desconfianza` (G4) es tasa base huérfana, no mapea aquí |
| 13 | cívico | `civico.denuncia.sin_seguro` + `civico.denuncia.con_seguro` | miedo + inutilidad percibida (denunciar rinde 0.8%) | (no declarado; yaml usa G4 para su tasa base huérfana) | FUERTE | NO — ver nota arriba: la p=0.294313 MEDIDO de `civico.denuncia.miedo_desconfianza` es tasa base incondicional (universo: víctimas 18+ que no denunciaron), **no** condicional a `sin_seguro`/`con_seguro`; el propio yaml lo declara `disparadores: {}`, sin cita SI-ENTONCES |
| 14 | cívico | `civico.voto.agencia_con_secreto` | no hay monitoreo del voto individual ni sanción creíble por cómo se vota | (no declarado) | FUERTE **(a)** | NO |
| 15 | cívico | `civico.voto.clientelar_si_observable` | cálculo racional bajo incertidumbre sobre el secreto del voto | (no declarado) | MEDIA **(a)** | NO — nota: `milpa/tramite-ola5-propuesta-v0.yaml` es **propuesta**, no sellada como `p` del motor (ver A.8(1); no cuenta como "medida" hasta sello de mesa) |
| 16 | cívico | `civico.clientelismo.turnout_no_vote_choice` | *turnout buying* ≠ *vote-choice buying* | (no declarado) | MEDIA **(a)** | NO |
| 17 | cívico | `civico.transferencia.entitlement_derecho` | el beneficio llega sin intermediario ni corresponsabilidad | (no declarado) | HIPÓTESIS **(a)** | NO |
| 18 | cívico | `civico.transferencia.atribucion_lider` | premio retrospectivo al desempeño e identidad partidista | (no declarado) | MEDIA **(a)**, correlacional, CONFUNDIDO | NO |
| 19 | cívico | `civico.protesta.agravio_urbano` | G4 (destructor selectivo) | G4 | MEDIA-FUERTE **(a)** | NO |
| 20 | cívico | `civico.autodefensa.agravio_rural` | G4 + ausencia de proveedor de seguridad | G4 | MEDIA-FUERTE **(a)** | NO |
| 21 | familia | `familia.seguro.volatilidad_ausencia_estado` | G5 | G5 | FUERTE | NO — `familia.apoyo.recibe_dinero_familiares` (G3, ENIF2024) es tasa base huérfana, no mapea aquí (universo distinto: vejez, `FILTRO_S9_1=2 ∧ EDAD_V<71`, no "volatilidad/ausencia de Estado") |
| 22 | familia | `familia.cuidado.recae_mujeres_40mas` | estructura + guion marianista | (no declarado) | FUERTE | NO |
| 23 | familia | `familia.union.baja_garantia_institucional` | evita costos ante baja garantía | (no declarado) | MEDIA | NO |
| 24 | familia | `familia.cortejo.urbano_joven_apps` | cohorte + exposición | (no declarado) | MEDIA / HIPÓTESIS | NO |

## A.13 — conteo

- Reglas SI-ENTONCES examinadas en los 4 dominios ACTIVOS de
  `canon/modelo-decision-v4_0.md` §3.B: **24** (5 trámite, 7 dinero, 9
  cívico, 4 familia — bullets del documento, contando cada diagonal partida
  con doble `id` como una sola fila de la tabla).
- Con `p` MEDIDO atada por mecanismo/situación: **1** (`tramite.mordida.discrecional`).
- Sin `p` medida (candidatas a P2/P3 de este encargo): **23**.
- `p` MEDIDO en `milpa/tramite.yaml` que **no** mapean a ninguna de las 24
  (tasa base huérfana, declarada así por el propio archivo): **3**
  (`civico.denuncia.miedo_desconfianza`, `dinero.ahorro.tiene_ahorros`,
  `familia.apoyo.recibe_dinero_familiares`).
- `p` ASIGNADO (sin calibración, mesa) que tampoco cuenta como medida: **8**
  entradas `entonces` sobre 4 de las 23 filas (trámite #2-4).

## NO-ENCONTRADO (declarado, no se inventa)

Ninguna de las 23 reglas trae hoy una `p` medida en `milpa/tramite.yaml` ni
en `milpa/tramite-ola5-propuesta-v0.yaml` (propuesta, no sellada). Esta es
la lista que P2/P3 de este encargo mapean contra los inventarios.
