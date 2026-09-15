# ENVIPE 2025 · evasión de norma percibida inútil o extractiva — pre-registro congelado de `CALC-EVASION-NORMA-0001`

### `prereg-caja-ENVIPE-EVASION-NORMA` · **v1.0** · 15 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/ENVIPE-EVASION-NORMA-spec-v1_0.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-ENVIPE-EVASION-NORMA`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Registro, en el esquema `D-15`, de una medición **ya corrida y sellada**: `evade_norma_envipe2025` / `cumple_norma_envipe2025` (`tramite.evasion_norma`, `milpa/tramite.yaml:474-475`), medida por `ACTO MAESTRA34-L5` (`tools/medidor_evasion_norma_envipe25.py`) y sellada por `ACTO MAESTRA35-N1 · SELLA-L5-Y-RECIBOS` (firma b1, mesa, 2/sep/2026). Releva `CORR-0007` — `RES-0025` y `RES-0026` — dos de los ocho `RESULT` de esa corrida. |
> | **QUÉ NO ES** | No es la misma pieza que `CALC-ENVIPE-0001`/`prereg-caja-ENVIPE-DENUNCIA` (releva `RES-0027`/`RES-0028`, otra regla, otro desenlace, mismo payload) — son dos `CALC` distintos sobre el mismo `envipe2025_csv`, ya declarados **no comparables entre sí** por la propia regla (`milpa/tramite.yaml:513`, distinta unidad, ponderador y denominador). No mide `RES-0039..0042` (denuncia condicional a seguro): esa apertura sigue `PROPUESTA; NO FIRMADA` (`forense/prereg-caja/ENVIPE-DENUNCIA-SEGURO-propuesta-v1_0.md`, `NC-0088`) — declaración explícita en §3 de por qué este acto no la resuelve. No re-ejecuta el medidor. No toca `milpa/tramite.yaml` (`E.3`). |
> | **VERIFICAS ASÍ** | CAJA (o cualquier sesión con el repo) confirma que `sha256sum data/raw/envipe2025_csv.zip` (o el payload resuelto por manifiesto) da `8a7a99fd90ce9d03229759ba0ad84db4fba98b5bb1f5c85eef7d718b007816fa`, y que `evade_norma_envipe2025 + cumple_norma_envipe2025 = 1.0` dentro de tolerancia (`0.562774 + 0.437226 = 1.000000`, exacto). |

**Acto:** `ACTO GEN2-SPECS-DEMANDA-2`, 15/sep/2026, entorno **NUBE** (`cloud_default`, `data/raw` ausente, corpus `montado=NO`), sobre `origin/main = da9b47a361143d408cd9fd9c20d17b101c4fe381`.

**Regla consumidora:** `tramite.evasion_norma` (`milpa/tramite.yaml:464`), `situacion: enfrenta_norma_percibida_inutil_o_extractiva`, `tier: FUERTE` (subió de `MEDIA` por firma b1).

---

## 0 · A.8 — qué ya existe

### 0.1 · `ya_medido.py`, salida cruda

```
$ python3 tools/ya_medido.py tramite.evasion_norma
  resuelto por canon: (id de motor sin R-n propio explícito en §7 -- fuente: modelo:3.3)
  -- milpa/tramite.yaml -- :464-522  situacion=enfrenta_norma_percibida... tier=FUERTE
     evade_norma_envipe2025 p=0.562774 clase="MEDIDO·p(tasa base ponderada, unidad delito)"
     cumple_norma_envipe2025 p=0.437226 clase="MEDIDO·p(tasa base ponderada, unidad delito)"
     [TASA-EJECUTADA vía enmienda_envipe2025, sellada ACTO MAESTRA35-N1]
  -- milpa/tramite-ola5-propuesta-v0.yaml -- :742-802 (id tramite.evasion_norma_envipe2025)
  -- data/corrida0 (RESULT + ejecución + sello) -- (sin CALC propio: 0 filas en data/corrida0/CALC-*/spec.yaml)
  -- forense/notas/*-L*-*.md -- 2026-09-02-MAESTRA34-L5-P3-spec.md, 2026-09-02-MAESTRA34-L5-P0-censo.md
  ========================================
  MEDIDA-EN: tramite.yaml, tramite-ola5-propuesta-v0.yaml (sin CALC que la releve)
```

Mismo hueco exacto que `CORR-0017`: medida, sellada, cargada al motor —
**sin** contrato `D-15`/`spec.yaml` en el registro GEN2. `CORR-0007` la
lista bajo `SIN-CANDIDATO-EN-EL-REGISTRO` porque el registro busca `CALC`,
no busca `milpa/`.

### 0.2 · Corrección de premisa del mapa-19 (A.8, antes de lanzar nada)

`data/corrida0/mapa-demanda-19-corr-v1_0.tsv` (fila `CORR-0007`, escrita por
`ACTO GEN2-SPECS-DEMANDA-1`) dice de `RES-0025`/`RES-0026`: *"no tienen
nada"*. Verificado contra `milpa/tramite.yaml` y
`data/corrida0/demanda-resultados.tsv` (arriba): **es falso en la letra**.
`RES-0025`/`RES-0026` **sí** tienen valor legacy medido
(`0.562774`/`0.437226`, `ACTO MAESTRA35-N1`, 2/sep/2026) — lo que les
faltaba, y sigue faltando hasta este documento, es la capa 2 del registro
GEN2, exactamente como `CORR-0017`. El mapa **no se edita** (es artefacto a
mano, no derivado, pero tampoco se re-escribe a mitad de tanda sin
comando): la corrección se registra aquí y se propaga a la fila del mapa en
el cierre de este mismo acto (§`Actualizar mapa-demanda-19`).

---

## 1 · Payload y medición original

| campo | valor |
|---|---|
| payload | `envipe2025_csv`, `sha256=8a7a99fd90ce9d03229759ba0ad84db4fba98b5bb1f5c85eef7d718b007816fa` |
| script original | `tools/medidor_evasion_norma_envipe25.py` (`ACTO MAESTRA34-L5`, spec congelada `forense/notas/2026-09-02-MAESTRA34-L5-P3-spec.md`) |
| unidad | DELITO (no persona) |
| universo | delitos con `BP1_20 ∈ {1,2}` en `tmod_vic_envipe2025`; `n=40 280`, sin pérdida |
| desenlace | `evade_norma = 1` ⟺ `BP1_20==2` Y `BP1_23 ∈ {04,05,06,08}` (conjunta, no condicional — reserva declarada en `milpa/tramite.yaml:513`) |
| ponderador | `FAC_DEL` |
| diseño | `EST_DIS` × `UPM_DIS`, bootstrap de conglomerado, `n_boot=10000`, `seed=42` (`wprop_ic_conglomerado`, misma función que `S7-L17`) |
| numerador | 21 761 |
| estratos | 739 |
| UPM | 10 694 |
| población expandida | 35 595 875 delitos |
| punto | `evade_norma_envipe2025 = 0.562774`, IC95 `[0.551982, 0.573448]` |
| complemento | `cumple_norma_envipe2025 = 0.437226` — **contado directamente** (`1 - 0.562774 = 0.437226`, coincide exacto: el complemento binario de una partición de dos es aritméticamente igual a `1-p`, no hay tercera categoría) |

---

## 2 · Reservas heredadas, no re-abiertas

`milpa/tramite.yaml:519` declara, verbatim: el estimando es la **conjunta**
`P(no denunció ∧ razón de norma inútil | enfrentó la norma)`, **no** la
condicional que el texto de la regla sugiere — `BP1_23` solo se pregunta a
quien no denunció, así que la condicional pura no es estimable con esta
fuente. `sancion_creible: false` es premisa jurídica externa, no medición
de ENVIPE. Ninguna de las dos reservas se resuelve aquí: se heredan tal
cual, con su cita.

---

## 3 · Lo que este acto declara y NO resuelve — `RES-0039..0042`

`CORR-0007` tiene, además de las dos parejas ya relevadas
(`RES-0027`/`RES-0028` por `CALC-ENVIPE-0001`, `RES-0025`/`RES-0026` por
esta spec), **cuatro** `RESULT` sin cubrir: `RES-0039..0042` (denuncia
condicionada a seguro, unidad delito, `BPCOD=01`). Inventario por archivo
(`A.15`):

| archivo | qué dice | por qué no basta |
|---|---|---|
| `forense/prereg-caja/ENVIPE-DENUNCIA-SEGURO-propuesta-v1_0.md` | `Estado: PROPUESTA; NO FIRMADA; NO EJECUTAR NI ADOPTAR` — dos opciones (A estrecha descriptiva, recomendada; B redefinición de motor), cada una con universo/capas/ponderador/diseño propios | Ejecutar cualquiera de las dos sin firma de mesa violaría la propia advertencia del documento — no es un hueco técnico, es una elección que el documento dice explícitamente que la mesa debe tomar |
| `NC-0088` (`forense/no-corrido.tsv`) | necesidad abierta que la propuesta de arriba responde | Sigue `ABIERTA`: este acto no la cierra porque cerrarla exige la firma que no está |
| `tools/medidor_denuncia_seguro_envipe25.py` | "cobertura técnica localizada, no autoridad para correr ni adoptar" (cita textual de la propuesta) | El script existe; lo que falta es la decisión, no el instrumento |

**Declaración explícita:** este acto **no** escribe una spec nueva para
`RES-0039..0042` ni elige entre la Opción A/B en nombre de mesa — hacerlo
sería tomar la decisión que el propio documento de `NC-0088` reserva
explícitamente para mesa, exactamente el tipo de atajo que `A.8` existe
para no tomar. Queda `DECISIÓN-DE-MESA-PENDIENTE`, sin cambio de estado.

---

## 4 · `resultados` que releva esta spec

`RES-0025` (`tramite.evasion_norma:evade_norma_envipe2025`), `RES-0026`
(`:cumple_norma_envipe2025`). `CORR-0007` queda con **6 de 8** `RESULT`
relevados tras este acto (los 2 de `CALC-ENVIPE-0001` + los 2 de esta pieza
+ los 2 ya contados; residuo: los 4 de `RES-0039..0042`, §3).

## 5 · Qué NO hace este acto

No re-corre `tools/medidor_evasion_norma_envipe25.py`. No cambia
`milpa/tramite.yaml` (`E.3`). No firma ni elige entre las opciones A/B de
`NC-0088`. No calcula el `medidor.py` de este `CALC`: es transcripción de
una corrida ya sellada, no medición nueva — mismo criterio que `CORR-0017`.

**El primer resultado que produjo este procedimiento —en `ACTO
MAESTRA34-L5`, no aquí— es el que se reporta.**
