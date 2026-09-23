# Cierre · ASTRA5-U3-POLITICA-COMPLETAR

**Rama** `claude/astra5-politica-completar-1`, en el worktree
`/home/pc0/mm-astra5-politica-1`. **0-bis** `d459637e`, con el encargo
verbatim y su sello de cuerpo `8071e9b2…`. **Entorno** CAJA WSL2, corpus
montado (`tools/entorno.py --arranque`: `ENTORNO-DERIVADO = CAJA`, red
permitida). **Modelo** Opus 5.5 en toda la ejecución. **ADR**
`ADR-260923-ASTRA5-U3-POLITICA-COMPLETAR-d459-01`.

## Continuidad y premisa «después de integrar #1084»

La sesión anterior dejó el 0-bis apilado sobre #1084, que seguía abierto,
y se cerró por error. Al retomar se revisó primero lo ya hecho: árbol
local, commits de la rama, ramas y PR vivos, y las lecturas de la sesión
previa. Con eso se evitó repetir trabajo.

Después, por instrucción del usuario, se sincronizó #1084 con `main`. El
merge local salía limpio gracias a `merge=union`; GitHub lo marcaba
`CONFLICTING`. Se auditaron duplicados por llave en los siete archivos que
tocaban ambos lados: ninguno. El guardia `test_readme_derivado` falló por
las cifras derivadas del README y se reparó con `71d87100`, siguiendo el
patrón de `baba52ac`. Con el CI 7/7 en verde se fusionó #1084 en
`72595501`, y esta rama incorporó `main`. Así se cumplió la premisa antes
de medir.

## EJECUTADO / LEÍDO / REPORTADO

- **EJECUTADO**, dos COMMIT-1 antes de abrir valores (`9ce97ca6`,
  `36254e39`) y un COMMIT-2 por CALC. Seis CALC sellados, todos con verify
  `REPRODUCE`/`IDENTICO` y asiento en `forense/replay-evidencia.tsv`:
  - `CALC-LAPOP-PISOS-2004-0002`
  - `CALC-LAPOP-PISOS-2006-0001`
  - `CALC-LAPOP-PISOS-2019-0002`
  - `CALC-LAPOP-PISOS-2021-0001`
  - `CALC-LAPOP-PISOS-2023-0001`, con `RESULT-LAPOP-PISOS-2023-POL001`
  - `CALC-INE-PISOS-SICEE-0002`

  **Dos primeras corridas fallaron antes del sello** y no escribieron nada:
  - `CALC-LAPOP-PISOS-2004-0001`: el diagnóstico de `wt`, vacío en las
    1 556 filas, dio `NaN`.
  - `CALC-INE-PISOS-SICEE-0001`: la regla congelada se detuvo ante un
    `null` publicado.

  Ambos quedan congelados sin editar. Sus sucesores (spec v1_1, COMMIT-1
  propio) cambian sólo ese manejo; estimando, umbral y universo quedan
  iguales. Antes de congelar el sucesor SICEE se hizo una verificación de
  parseo, sin calcular tasas, que la spec v1_1 declara.

  `preflight` VERDE en los ocho CALC congelados. Pruebas sintéticas: 12
  casos, incluido el conducto `corrida0._valida_outputs` con las tres
  ramas terminales (`ESTIMADA`, `NO-ESTIMABLE`, `ESCALA-DISCREPANTE`) por
  CALC. Están censadas como huérfanas en `censo-tests.tsv`, sin editar
  `verify.yml` ni `check.py` (D-21).
- **LEÍDO**:
  - Contrato U0 POL-001 en #1079 (`corte-politica-v1_0.tsv`).
  - Reportes técnicos LAPOP 2004, 2006, 2019, 2021 y 2023.
  - Cuestionarios LAPOP 2004, 2019, 2021 y 2023.
  - Etiquetas de variables y de valores (metadatos) de las cinco olas.
  - Cabeceras del XLSX ENCUP 2012 y cuestionario ENCUP 2012.
  - Estructura (llaves, no cifras) del JSON SICEE.
  - Manifiesto por id, archivo y url.
  - Censo de raíz del 23/sep.
- **REPORTADO**: `forense/analisis/dominios/politica/RESULTADOS-ASTRA5-U3-COMPLETAR.md`
  (tres tablas separadas, RESULT/CALC/hash, enlace U0, límites, tier,
  falsadores y auditoría) y tres dictámenes:
  - `lapop-dictamen-olas-v1_0.tsv` (59 filas)
  - `encup-diseno-dictamen-v1_0.md`
  - `ine-objetos-restantes-v1_0.tsv` (159 ids en 7 grupos)

**Verificación de insumos.** Los seis payloads medidos tienen el sha256
recalculado en disco igual al del manifiesto (COINCIDE); LAPOP viene de la
raíz `descargas_mx`. Licencia LAPOP: clic, uso no transferible. Sólo se
publican agregados y ningún microdato entra al repo. **Reservas.** Se
buscó una reserva que nombre LAPOP o SICEE en `decisiones.tsv`,
`decisiones-humanas.tsv`, `firmas-pendientes.tsv` y `no-corrido.tsv`
(1 450 líneas): cero reservas de datos. Las dos menciones que aparecen son
reservas interpretativas `ACOTADA-CON-RESERVA`. Control positivo: 24
menciones de reserva ENCO/ENVIPE 2026 en los mismos archivos. Las olas
entraron al manifiesto el 13/ago y el 6/sep, antes de la regla E.6 de «ola
nueva nace reservada». No se abrió ENCO, ENVIPE 2026, la última ola ENOE,
WVS ni ENCUCI.

**Contaminación declarada (ADR-46).** Esta sesión y la anterior leyeron
metadatos y estructura (etiquetas, cabeceras, llaves) antes de congelar,
nunca valores de los estimandos. Tras las fallas se leyeron sólo
conteos de vacíos de las variables de diseño 2004 y los campos nulos de
SICEE. Después del sello se leyó el conteo de `b18` 2021 con diseño
completo, para documentar el universo.

**Contador inicial/final**, derivado con `corrida0 status` (base
`060cc956` frente a `HEAD`):

| contador | inicial | final |
|---|---:|---:|
| `N_corridas_selladas` | 222 | 228 |
| `N_resultados_gen2_sellados` | 65 574 | 65 587 |
| `no_corrido_abiertas` | 260 | 262 |
| `N_resultados_gen2_adoptados_activos` | 72 | 72 |
| `celdas_validadas` | 219 | 219 |

Las filas de la vista quedan **selladas en disco, no registradas** hasta el
canal del push a `main` (NC -d459-04). El README se refrescó con las dos
cifras derivadas que su guardia exige. No se tocaron tablero, milpa, motor
ni vistas globales. `data/INFRAESTRUCTURA-v1_0.md` no se modifica: indexa
tablas de maquinaria del registro, no productos de análisis por dominio, y
no contiene ninguna tabla `dominios/`.

**FP de mesa previas, re-verificadas ABIERTAS (A.17), con evidencia nueva
y sin firmarlas aquí:**
- `FP-260923-ASTRA5-U3-POLITICA-df0d-01` (INE, universo de participación):
  cuenta ahora con la serie SICEE y el dictamen de objetos.
- `-df0d-02` (ENCUP, diseño): el dictamen dice qué falta.
- `-df0d-03` (LAPOP, equivalencia por ola): el dictamen ya existe.

## NO-CORRIDO / RESERVAS

Véase la misma sección en el encargo archivado y las filas
`NC-260923-ASTRA5-U3-POLITICA-COMPLETAR-d459-01` a `-05` de
`forense/no-corrido.tsv`. Cierra `NC-260923-ASTRA5-U3-POLITICA-df0d-02`
(sustituida por -d459-01) y `-df0d-03` (dictamen hecho).

## Recibo para mesa

Tres instrumentos separados, sin unir personas y secciones. Candidatos
medidos o dictaminados, por instrumento:
- **LAPOP**: cinco olas, cada reactivo de interés, eficacia, confianza,
  tolerancia y oferta, medido o marcado «ausente».
- **ENCUP**: sin diseño acreditable; se conserva descriptivo.
- **INE**: producto administrativo conservado, serie nacional SICEE
  medida y 159 objetos restantes dictaminados.

Pendiente de mesa: el merge (adopción) y las tres FP citadas arriba.
