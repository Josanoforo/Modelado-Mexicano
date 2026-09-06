# ACTO MAESTRA38-LOTE-ENSANUT · L16 + L17 — resultados

`origin/main = 693ea23` (SHA de redacción). Rama `acto/maestra38-lote-ensanut`.
Encargo archivado en `forense/encargos/2026-09-06-MAESTRA38-LOTE-ENSANUT.md`.
Ejecuta en paralelo con `ACTO MAESTRA38-L2` (`data/l2-*`) — no se tocó
ningún archivo de ese perímetro.

## A.8 — arranque

- Specs selladas verificadas por `.sha256`:
  - `forense/prereg-caja/S6-L16-spec-v1_0.md` → `317e42c3becca6402aa0848f9cd5a4ace2af784ea174024c7dab0687db724b9f` (COINCIDE)
  - `forense/prereg-caja/S7-L17-spec-v1_0.md` → `f3aea086cee60e59fa3858334eaa6e00218e30a0b19c67fb37ae806fd586830f` (COINCIDE)
- `tools/ya_medido.py salud.atencion.grave` → `MEDIDA-EN: S6` (antes de este
  acto, `NUNCA-MEDIDA` — la spec S6 es la única cita previa de una corrida
  real; este acto es la primera corrida).
- `tools/ya_medido.py salud.vacunacion.disponible` → `NUNCA-MEDIDA` (antes de
  este acto).
- Los 4 payloads `ENSANUT2024-v2026-09-01/{integrantes_ensanut2024_w_icb,
  utilizadores_ensanut2024_w,adultos_ensanut2024_w,adolescentes_ensanut2024_w}.stata.stata.zip`
  se localizaron en `descargas_mx` (`/mnt/c/Users/PC0/Descargas MX/ENSANUT2024-v2026-09-01/`,
  raíz declarada en `data/manifiesto.yaml` con `raiz: descargas_mx`) y su
  `sha256` coincide EXACTO con el `manifiesto.yaml`/spec §6 en los cuatro
  casos (ver salida de los dos `tools/medidor_l1*.py` abajo).

## Frase de sello

**«el primer resultado que produzca este procedimiento es el que se
reporta»** — aplicada literalmente: los scripts se corrieron una sola vez,
sin ajuste posterior de cortes o umbrales, salida cruda abajo.

## L16 · `salud.atencion.grave` (R4.4) — Rama B (ENSANUT2024)

`python3 tools/medidor_l16_atencion_grave.py`:

```
ACTO MAESTRA38-L16 · salud.atencion.grave (R4.4) · Rama B ENSANUT2024
payload : integrantes_ensanut2024_w_icb.dta · sha256(dta) = 8417d9ae7395eace68caca449afe2c048a2318b2f87c488ab7ab7c4c1aafd6d6
payload : utilizadores_ensanut2024_w.dta · sha256(dta) = 707f590099d66cde948674b74202d4e8c10831c00b3925f6bcf219ceed968d72
integrantes: 36,021 filas · utilizadores: 3,223 filas
H0409A no-nulo (algún requerimiento reportado): 7,645
  de esos, grave (hospitalizacion/urgencias, {2,3}): 644 · no-grave ({1,4}): 7,001
utilizadores con u0201 clasificable publico/privado: 3,125 de 3,180 con u0201 no-nulo (55 fuera de la dicotomia)
join FOLIO_I (H0409A no-nulo × u0201 clasificable): 5,289 filas
  grave (2,3): n=423 · publico=280 (66.1939% crudo, no ponderado)
  no-grave (1,4): n=4866 · publico=2835 (58.2614% crudo, no ponderado)

Falsador B-bis (Rama B) — proporcion INSTITUCION_PUBLICA por celda H0409A
  grave: p̂(publico) = 52.2295%  IC95 = [36.8248%, 69.8407%]  n=423 · estratos=3 · UPM=208
  no_grave: p̂(publico) = 52.5159%  IC95 = [48.5995%, 56.6960%]  n=4,866 · estratos=3 · UPM=447

diferencia p̂(grave) - p̂(no-grave) = -0.2864%  IC95_aprox = [-17.2835%, 16.7107%]
VEREDICTO Rama B (falsador B-bis, salud.atencion.grave): NO-DISCRIMINA
```

**Corte usado (construido contra el codebook, no asumido):** `H0409A` ∈
{2 hospitalización, 3 urgencias} = grave; {1 consulta externa, 4 otros} =
no-grave. El texto de `H0402`/`H0409A-D` NO contiene literalmente "grave" ni
"crónico complejo" (confirmado, spec §2.1 ya lo advertía) — este corte es la
interpretación más directa del `PORQUE` de la regla ("la complejidad excede
al consultorio"), declarada, no forzada. `INSTITUCION_PUBLICA` (`u0201`) =
{1 IMSS, 2 ISSSTE, 3 PEMEX, 4 Defensa, 5 Marina, 6 SSA, 8 DIF, 9 Cruz
Roja/Verde, 10 Instituto Nal. Salud, 26 IMSS-BIENESTAR}; `PRIVADO` = {12-19};
55 filas fuera de la dicotomía (ONG/tradicional/otro/no-sabe/psicológico),
excluidas y contadas.

**Veredicto:** `NO-DISCRIMINA`. Primera falsación real de `R4.4` sobre datos
(era `NUNCA-MEDIDA`). Las dos celdas rondan 52% de atención pública casi
idénticas; el IC95 de la diferencia (aproximado, ver nota de método abajo)
contiene 0 con margen amplio.

**Rama A (ENNVIH+ENDIREH): NO corrida.** El ponderador del libro `bx`/2002
(única fuente de `es09` con el texto literal "GRAVE") tiene tres candidatos
sin resolver por el inventario (`fac_3a_px`/`fac_3b_px`/`fac_4_px`, spec
§1.3) y no hay codebook de `ENNVIH` en el corpus para desambiguar. **PARO
parcial, declarado** — no se adivinó el ponderador. La spec permite (y
exige) reportar las dos ramas por separado cuando ambas tienen codebook
accesible; aquí solo Rama B lo tiene sin ambigüedad.

## L17 · `salud.vacunacion.disponible` (R9.2) — Rama B (primaria) + Rama C

`python3 tools/medidor_l17_vacunacion_disponible.py`:

```
Rama B (primaria) — razon de no vacunacion, adultos_ensanut2024_w
payload : adultos_ensanut2024_w.dta · sha256(dta) = 4bb4ceeb97005d77466d9bb3329f8b0528e3df5f534925fc6f3b659646096efc
personas en el .dta: 12,924
total de menciones 'Si' (persona x vacuna x razon): 254 (179 personas distintas)
desglose por razon: no_habia_vacunas=152, enfermo=47, no_estaba_quien_aplica=28, no_derechohabiente=16, otra_razon=11

p̂(RAZON_LOGISTICA) = 77.7762%  IC95 = [67.2777%, 85.7561%]  n=254 menciones · estratos=3 · UPM=140
VEREDICTO Rama B (falsador B-bis primario, salud.vacunacion.disponible): CORROBORADA

Rama C (corroboracion de tasa) — adolescentes_ensanut2024_w
payload : adolescentes_ensanut2024_w.dta · sha256(dta) = e36db7a5c267d30e236dc58f5ed73dfa278f011939a754437f33889a8d9a93f0
personas en el .dta: 3,730
  d0321j: n=69 n_si=60 numerador<10 en alguna celda -> NO-ESTIMABLE
  d0321p: p̂(aceptó) = 56.2390%  IC95 = [39.9606%, 71.9754%]  n=66 -> NO-DISCRIMINA
  d0508:  p̂(aceptó) = 37.1580%  IC95 = [33.3836%, 41.0952%]  n=3,094 -> CONTRARIA (mayoria NO acepta)
  d05041: p̂(aceptó) = 59.3244%  IC95 = [55.5192%, 63.1826%]  n=2,974 -> CORROBORADA (mayoria acepta)
  d05051: p̂(aceptó) = 34.6854%  IC95 = [31.6861%, 37.7482%]  n=2,941 -> CONTRARIA (mayoria NO acepta)
```

**Hallazgo del codebook (reasignación letra/dígito, declarada):** la spec
§2 asumía letra=vacuna, dígito=razón; el `.dta` confirma lo contrario —
**letra = razón** (a=no había vacunas, b=no derechohabiente, c=no estaba
quien aplica, d=enfermo, e=otra razón), **dígito = vacuna** (1=Influenza,
2=Neumococo, 3=Tétanos, 4=Otra). Reasignada contra las etiquetas de valor
del `.dta`, no contra el orden que el inventario sugería (la spec ya
advertía que el inventario "no despliega la asignación en una fila
legible").

**Veredicto Rama B (primaria): `CORROBORADA`.** Primera prueba directa del
`PORQUE` de `R9.2` en todo el corpus: 180 de 254 menciones (70.9% crudo,
77.78% ponderado) son logísticas (suministro/personal), IC95 excluye 50%
por arriba con margen amplio. `ENSANUT2024` no ofrece ninguna categoría
explícitamente actitudinal — restricción del instrumento, declarada.

**Rama C (descriptiva, sin antecedente propio):** mixta — 2 de 4 reactivos
estimables por encima de 50% (Tdap prenatal `NO-DISCRIMINA`, tétanos
antes-10-años `CORROBORADA`), 2 por debajo (VPH y tétanos desde-10-años,
ambos `CONTRARIA` descriptivo). No pondera contra el veredicto de Rama B,
que es la primaria según la spec (§4).

**Rama A (ENNVIH): NO corrida** — mismo pendiente de ponderador ambiguo que
L16, más la reserva de diseño §0.3 (`ce19d_2`/`hs16d_2` posiblemente
post-tratamiento, no confirmable sin codebook de `ENNVIH`). PARO parcial,
declarado; no bloquea el veredicto de Rama B.

## Nota de método — IC95 de la diferencia (L16)

El estimador de la casa (`wprop_ic_conglomerado`, bootstrap de conglomerado
por estrato/UPM, 10 000 réplicas, semilla 42 — verbatim de
`tools/calibracion_mordida_encig_serie.py`) da el IC95 de cada celda por
separado. La diferencia grave−no-grave se reporta con un IC aproximado
(combinación normal de los SE de cada celda, `se = (hi-lo)/(2·1.96)`), NO
un bootstrap conjunto sobre la resta — declarado, no presentado como
bootstrap directo. Dado el amplio solapamiento de ambos IC (52.2% vs
52.5%), la aproximación no cambia el veredicto: cualquier método razonable
da `NO-DISCRIMINA` aquí.

## Contador de salud (A.8/CONTADOR)

`forense/notas/2026-09-03-MAESTRA37-L3-BIS-veredictos.md:255` declara
**«`EXISTE-SATISFACE` en `salud`: 2 de 5» (`salud.atencion.grave` y
`salud.atencion.desabasto`, R4.3)** — antes de este acto. Este lote **mide
falsadores** sobre dos ids que ya tenían `EXISTE-SATISFACE` sellado
(`salud.atencion.grave` por `L3`/`L3-BIS`; `salud.vacunacion.disponible`
por `N5`/`N10`) — no clasifica ningún id nuevo como `EXISTE-SATISFACE`.
**El contador de salud permanece en 2 de 5.** No se cruza el umbral de
≥3/5 y por tanto **NO se dispara `ABRE-CANDIDATO-CON-RESERVA`** — no
corresponde escribirlo en esta nota. Si mesa considera que una Rama B
`CORROBORADA` (L17) debe contar aparte del tally de clasificación
`EXISTE-SATISFACE`, esa es una decisión de D8, no de este acto.

## PARO parcial declarado (ambas piezas)

Rama A de ambas specs (`ENNVIH` 2002/2005/2009 + `ENDIREH` 2016) **no se
corrió**: el ponderador del libro `bx`/2002 tiene tres candidatos sin que
el inventario baste para resolverlo, y no hay codebook de `ENNVIH`
registrado en el corpus. No es un defecto de esta pieza — la spec S6 §1.3
ya declaraba esta ambigüedad antes de que caja abriera ningún archivo. Se
reporta como entregable, no como fallo: **una pieza que PARA no tumba el
lote** (L16 y L17 sí produjeron veredicto sobre Rama B/C).

## `tests/check.py --baseline`

Ver cascada en el commit de cierre.

## Perímetro tocado

`data/l16-*`/`data/l17-*`: no se generó ningún artefacto de datos separado
más allá de los `.dta` extraídos a `/tmp` (no versionados) — los resultados
viven íntegros en `milpa/tramite-ola5-propuesta-v0.yaml` (append) y esta
nota. `tools/medidor_l16_atencion_grave.py`, `tools/medidor_l17_vacunacion_disponible.py`
(nuevos). No se tocó `data/l2-*` (perímetro de `MAESTRA38-L2`, en paralelo).

## CONSUMIDO

Ver `## CONSUMIDO` en `forense/encargos/2026-09-06-MAESTRA38-LOTE-ENSANUT.md`.
