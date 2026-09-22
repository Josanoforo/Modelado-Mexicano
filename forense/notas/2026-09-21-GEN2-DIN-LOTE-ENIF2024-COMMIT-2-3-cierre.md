# Nota de cierre · `ACTO GEN2-DIN-LOTE-ENIF2024-COMMIT-2-3` · 21/sep/2026 · CAJA

**Qué se probó.** La prueba prospectiva más grande del programa: 14 cruces de ENIF
2024 (`ahorra_solo_informal`, 96 celdas nominales, 8 contendientes), congelada en
`#979` (spec humana v1.0 sellada `64bb52f2…`, régimen `PILOTO-1`, 13 492 personas
2024) y abierta aquí por primera vez. Dos corridas selladas en `origin`, en el
orden que E.6 exige: `CALC-DIN-LOTE-ENIF2024-EMISIONES-0001`
(`--8e53d38b30c6`, COMMIT-2) antes que `CALC-DIN-LOTE-ENIF2024-ADJUDICACION-0001`
(`--7645dcf1301a`, COMMIT-3), con COMMIT-3a en commit propio entre las dos
(`spec.yaml:10702`, sólo el sha256 de `emisiones_selladas`/`emisiones_sello`).
`verify` de las dos: `REPRODUCE`/`IDENTICO`. Guardia AST **PASA** (0
violaciones); el veto probado sobre `(localidad, edad)` —el único par que la
spec **no** autoriza en ENIF 2024— se disparó correctamente
(`ReservaRota: par (localidad, edad) NO autorizado en ENIF 2024`), confirmando
que el guardián distingue los 14 pares reales de un par cualquiera.

## 1 · Qué salió

**Veredicto primario (regla v0.3, 5 pares primarios `edadxescolaridad`,
`edadxsexo`, `escolaridadxlocalidad`, `escolaridadxsexo`, `localidadxsexo`; 44
celdas, 43 puntuadas, 1 sin soporte):** retador primario `R2` (interacción
histórica 2021↔2024 encogida al piso, λ=1/2 fija) — `MAE(C2 piso)=1.8729 pp`,
`MAE(R2)=1.3931 pp`, `ΔMAE = 0.4798 pp`, `IC95=[0.0975, 0.7151]`. Como
`0 < IC95inf(0.0975) ≤ 0.5`: **`VEREDICTO-PRIMARIO = PROPUESTA-CON-RESERVA`**
— no `VENCE-RETADOR`. Cobertura: R dentro del IC de R2 = 88.6 %, R2 dentro del
IC de R = 97.7 % (C2: 75.0 % / 84.1 %). Conteo 3/4 (descriptivo, no adjudica):
R2 yerra menos que C2 celda a celda en 22/43 (51.2 %).

Secundarias sobre los mismos 44: `P2` (piso 2024 sin interacción) `ΔMAE=-0.42
pp` `IC95=[-2.09,-0.001]` → `NADIE-VENCE`; `R1` `ΔMAE=0.57 pp`
`IC95=[-0.29,0.83]` → `NADIE-VENCE`; `R3` (raking IPF) `ΔMAE=0.61 pp`
`IC95=[-0.23,0.90]` → `NADIE-VENCE`. Ninguna secundaria vence ni cae en reserva.

**Grupos secundarios `CUENTA-FORMAL`** (4 pares EMITIBLE, 28 celdas) **y
`FORMALIDAD`** (4 pares `NO-EMITIBLE`, 24 celdas, sólo `P2` descriptivo):
`NO-ADJUDICABLE-SIN-PISO` para `C2/R1/R2/R3` — no existe comparador `R` fuera
de los 5 pares primarios en este CALC; `P2` sale `SIN-PISO-SOLO-COBERTURA`
(`MAE=2.34 pp` y `3.24 pp` respectivamente, puramente descriptivo). Por par:
**9/14 `ADJUDICADO`** (los `EMITIBLE`), **5/14 `SIN-PISO-SOLO-P2`** (los
`NO-EMITIBLE` por `formalidad` con universo restringido a 68.97 %, A-bis 4).

**B-bis (falsación pre-registrada, §10 de la spec):** `NO-CAE-EN-NINGUNA-FILA`
— razón mecánica: *"cobertura de C2 < 80 % en algún par primario (refuta el
argumento de producto)"*. `ADJUDICA-SOLO = NO`: la lectura la cierra mesa, no
este acto.

**Fila L (LLM, §2 del encargo):** el medidor congelado reproduce el texto de
COMMIT-1 (`NO-ENTRA-EN-ESTE-CALC…`, `RESULT-DIN-LOTE24-EM-G-L-ESTADO`); la
firma de mesa de **este** encargo la registra como **`NO-EMITE — nadie corrió
el mecanismo`** (no una derrota): L1/L2 no se corrieron por presupuesto, y la
pregunta sigue abierta en la fila L del duelo ENVIPE 2026 y en el marcador
retrospectivo del piloto 1.

## 2 · Con qué certeza

`REPRODUCE`/`IDENTICO` en las dos corridas (tolerancia declarada: bootstrap
seed 42, abs 1e-10). Nulos: 364/2184 en emisiones y 338/2913 en adjudicación,
**todos** concentrados en las 5 familias `NO-EMITIBLE` por `formalidad`
—exactamente las que la propia spec declara antes de abrir el dato, ningún
nulo nuevo—. Compuerta P2 (§5 del encargo) verificada por comando: los 68
celdas de los 9 pares `EMITIBLE` tienen soporte (`SOPORTE-2021=SI` y `N24≥200`)
y ningún candidato (`C2/P2/R1/R2/R3`) sale nulo en ellas; los 85 marginales
`M24` tampoco. `EMISIONES-DELTA-P-MAX=0.0` (adjudicación reprodujo las
emisiones antes de derivar R) y `EMISIONES-R-EXISTIA=NO` (R no se derivó antes
de COMMIT-2, orden E.6 intacto). El único IC que despeja 0 sin despejar 0.5 es
el de `R2` sobre los 5 primarios — la reserva es del propio umbral
pre-registrado, no de un defecto de medición.

## 3 · Qué NO significa este resultado

- **Acceso, ingreso y oferta antes que preferencia.** ENIF mide tenencia y uso
  de productos financieros: la brecha entre `C2` y `R2`, y entre pisos y
  candidatos en general, puede venir de oferta bancaria, sucursales, requisitos
  de ingreso o cobertura de red — no es evidencia directa de que las personas
  *prefieran* ahorrar formal o informalmente. Ningún número de este acto separa
  oferta de preferencia.
- **Persona elegida, no hogar.** La unidad es el adulto 18+ seleccionado en el
  hogar (`FAC_PER`/`FAC_ELE`), un individuo por vivienda encuestada — no el
  hogar ni el total de adultos del hogar.
- **No comparable con ENCIG ni con ENVIPE.** Los pp de este lote están en la
  escala de `ahorra_solo_informal` de ENIF (proporción de personas); ENCIG mide
  trámites/corrupción y ENVIPE mide delitos — unidades distintas (persona vs.
  trámite vs. delito, A-bis 3/§4 v2.16). Ningún `ΔMAE` de aquí se compara
  numéricamente contra los de esos programas.
- **`PROPUESTA-CON-RESERVA` no es adopción.** E.2: la adopción es por merge de
  mesa. Este acto sella y mide; no adopta ningún candidato ni mueve
  `adoptados_activos`.

## 4 · La línea para θ

**¿`R2` venció al piso? No — limpiamente no.** El `IC95inf` de `R2` (0.0975
pp) está por encima de cero pero no despeja el umbral de 0.5 pp
(`VENCE-RETADOR` exige `IC95inf > 0.5`): el veredicto primario es
`PROPUESTA-CON-RESERVA`, no `VENCE-RETADOR`. Por §4 v2.16 (`θ` generador de
retadores, calibrado sólo como retador pre-registrado de una celda-D, emite
sólo donde adjudique): **`θ` no emite en ninguna de estas 14 celdas todavía**
— la interacción histórica 2021↔2024 encogida (`R2`) es una propuesta con
reserva sobre los 5 pares primarios, pendiente de que mesa decida si el margen
de 0.10–0.72 pp basta para adoptarla como retador de `θ`, o si se queda
acotada al piso.

## 5 · Cadena de identidad (D-22)

`script_blob_sha256` idéntico en las dos corridas
(`e8cae318bddb71da7ecdb8a35f987bb3530aa6073002b69ece8260011a65ed45`,
`MEDIDOR-IDENTICO-A-TOOLS=SI`); `spec_md_sha256` `EN-MAIN-COINCIDE` contra
`64bb52f2…` en las dos; inputs de ADJUDICACION incluyen
`emisiones_selladas=7018bd35…` y `emisiones_sello=5dc484f2…`, fijados en
COMMIT-3a y verificados `COINCIDE` en el preflight subsecuente. Asientos en
`forense/replay-evidencia.tsv`: dos filas nuevas (`REPRODUCE`/`IDENTICO`),
`corrida0 estado` confirma `SELLADA` en las dos.

## 6 · Sucesores y pendientes de mesa

- La lectura B-bis (`NO-CAE-EN-NINGUNA-FILA`) y el veredicto
  `PROPUESTA-CON-RESERVA` quedan para que mesa decida si adopta `R2` como
  retador de `θ` sobre los 5 pares primarios, o si pide una ronda con más
  soporte / L1-L2 corridos.
- `FP-260921-GEN2-DIN-LOTE-ENIF2024-COMMIT-2-3-8e53-01` (Q: ¿se corre L1/L2
  con presupuesto dedicado, dado que la reserva ya no protege esta ola una vez
  medida?) y `FP-260921-GEN2-DIN-LOTE-ENIF2024-COMMIT-2-3-8e53-02` (Q: ¿los 5
  pares `NO-EMITIBLE` por `formalidad` se sellan aparte con `C2-restringido a
  quien trabaja`, como F2 preveía en la Q1 de COMMIT-1?) van a mesa.
