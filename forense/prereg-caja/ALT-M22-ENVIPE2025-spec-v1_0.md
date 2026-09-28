# M22 · ENVIPE 2025 · no denuncia por miedo, por entidad de residencia, unidad delito

El primer resultado que produzca este procedimiento es el que se reporta.

Acto `GEN2-CALC-ALTERNOS-LOTE-1` (0-bis `795b1053`), fila 60 de
`canon/mapa-instrumentos-alternos-v1_0.tsv` («serie por entidad de no
denuncia por miedo, unidad delito»). Firma R08 A2 (b), 28/sep/2026: «M22
(ENVIPE 2025, no denuncia por miedo por entidad)». Un CALC:
`CALC-ALT-M22-ENVIPE2025-0001`. No adopta; no es retador; sin θ.

## Apertura: sólo lo que ya se abrió de ENVIPE 2025

Encargo §7 (a): ENVIPE 2025 «fuera del árbitro» es PARO. Este CALC lee sólo
columnas ya abiertas por CALC sellados de 2025: `BPCOD`, `BP1_20`, `BP1_23`,
`FAC_DEL`, `EST_DIS`, `UPM_DIS`, `ID_PER` de `TMOD_VIC`
(`CALC-ARBITRO-MARGINALES-ENVIPE2025-0001`) y `CVE_ENT` de `TPER_VIC2`
(`CALC-REGION-ENVIPE-DENUNCIA-U4-2025-0001`, que ya estimó por las 32
entidades de residencia). No se abre ninguna otra columna (en particular,
`AP5_4_*` de `TPER_VIC1` queda sin abrir: fila 57 del mapa DIFERIDA).

## Qué ya está medido y no se repite (E.5)

`CALC-REGION-ENVIPE-DENUNCIA-U4-2025-0001` estimó la clase C2 (miedo o
desconfianza, `BP1_23 ∈ {01,02,06,08}`) con unidad **persona** U4 por
entidad. Este CALC es otro estimando: unidad **delito**, clase **miedo**
(`{01, 02}`), ponderador `FAC_DEL`. La codificación del universo se toma
verbatim de esa spec (`REGION-ENVIPE2025-DENUNCIA-U4-spec-v1_0.md` §1).

## Estimando, unidad, escala, universo

- **Unidad:** delito (fila de `TMOD_VIC`).
- **Universo:** delitos personales `BPCOD ∈ {05..15}`, no denunciados
  `BP1_20 = 2`, con razón principal `BP1_23 ∈ {01..08}`; `09`, `99` y
  blanco fuera y contados. `FAC_DEL` > 0, `EST_DIS`/`UPM_DIS` presentes.
  `ID_PER` debe ser único en `TPER_VIC2` (guardia: si no, error); una fila
  de `TMOD_VIC` sin enlace se cuenta (`fuera_por_sin_enlace`) y queda fuera
  del universo, sin imputarle entidad.
- **Reactivo (A.15):** «1.23 ¿Cuál fue la razón principal por la que no
  denunció o no denunciaron el delito ante el Ministerio Público o Fiscalía
  Estatal?». Evento **MIEDO** := `{01 miedo al agresor, 02 miedo a que lo
  extorsionaran}` (etiquetas del mapa, fila 60).
- **Escala:** proporción ponderada de delitos en [0, 1].
- **Celdas:** nacional y las 32 `CVE_ENT` de residencia de la víctima (no de
  ocurrencia). n mínimo 30 delitos por celda; debajo, `NO-ESTIMABLE`.

## Ponderador y diseño

`FAC_DEL` (factor del delito), estrato `EST_DIS`, UPM `UPM_DIS` de
`TMOD_VIC`. IC95 bootstrap UPM en estrato, 2 000 réplicas, semilla PCG64
`20260928`. Lectura por `corpus_loader.cargar` (caché con constancia).

## Agregador (E.1)

Razón de sumas de `FAC_DEL` por celda.

## Qué pasa si el falsador no refuta

R10.3 pide el efecto de la **protección efectiva a testigos**; ENVIPE no la
mide (mapa: «falta el tratamiento … y su fecha»). Este CALC es un piso
descriptivo de exposición por entidad; no puede refutar ni corroborar
R10.3 y se rotula así. Cualquier unión con un calendario de programas de
protección (OBTENCION-EXTERNA-1) es de otro acto.

## Auditoría v2.16

- **Unidad:** delito (no persona). **Escala:** proporción.
- **RETROSPECTIVA:** ENVIPE 2025, año de referencia 2024.
- **¿Incentivo o psicología?** Motivo declarado (miedo): mezcla riesgo
  percibido (incentivo) y disposición; no se separan.
- **¿Clase media urbana?** Nacional con dominio estatal; entidades con
  pocos delitos quedan NO-ESTIMABLE.
- **HOLDOUT gastado: `M22`** (censo C2: 0 menciones de M22/R10.3 en 140
  archivos, control positivo 66). `holdout_gastado = M22`.
