# ACTO O · La cola de adquisición, derivada y congelada

`ENCARGOS · ADQUISICIÓN`, 12/ago/2026 (`forense/encargos/2026-08-12-adenda-adquisicion.md`). Base declarada `origin/main = cfed849 o posterior`; base real de esta sesión `origin/main = f8eb2e3` (merge PR #182) — `git merge-base --is-ancestor cfed849 origin/main` confirma que es posterior, sin deriva que re-derivar. Worktree `/home/pc0/mm-o-cola-adquisicion`, rama `acto-o/cola-adquisicion`. Re-fetch inmediatamente antes de escribir esta nota: `origin/main` seguía en `f8eb2e3`, sin avance.

**Nada se descarga en este acto.** Es puro escritorio: lee `data/curacion-registro/relaciones.tsv`, el censo de los 15 coeficientes, el mapa necesidad→objeto, la propuesta del piloto FIN y los cuatro mapas externos ya en el repo; deriva un TSV nuevo.

---

## 0 · ARRANQUE

1. **REPO.** Clon existente `/home/pc0/Modelado-Mexicano`; worktree nuevo `/home/pc0/mm-o-cola-adquisicion` (`git worktree add ... origin/main`). `git log -1`: `f8eb2e3 Merge pull request #182 from Josanoforo/claude/new-session-xer383`. `git status`: árbol limpio al abrir.
   - `git worktree add` emitió dos veces `error: could not write config file .git/config: Device or resource busy` — contención conocida de este entorno ([[project-modelado-mexicano-git-config-contention]]: dozens de worktrees comparten el mismo `.git/config` de la base). Verificado independientemente de ese texto: `git log -1` del worktree nuevo sí quedó en `f8eb2e3`, `git status` limpio, `git worktree list` lo lista — la creación en sí no falló, solo la escritura de metadato de tracking (irrelevante aquí porque el push de cierre usa refspec explícito, no depende de tracking).
2. **SHA.** `origin/main = f8eb2e3`; `git merge-base --is-ancestor cfed849 origin/main` → `YES`. Re-verificado antes de escribir esta nota: sin avance.
3. **data/raw.** Ausente al crear el worktree (esperado, gitignorado). Enlazado: `ln -s /home/pc0/mm-corpus/raw data/raw` (mismo destino que usa la base clon). No se usó — este acto no abre microdato ni corpus compartido.
4. **ENTORNO.** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` sin definir → firma Ubuntu-con-red (`sin_variable`). El acto no requiere red ("O: cualquiera de los dos... no necesita red") — no se hizo sonda `curl`, por instrucción explícita del propio encargo.
5. **ESPEJO.** No se usó. Toda cifra de esta nota sale de `git show`/lectura directa de este worktree, con el comando a la vista donde aplica.

**Regla A.3 aplicada primero.** El texto completo del encargo (los cuatro actos O/P/Q/R) se archivó en `forense/encargos/2026-08-12-adenda-adquisicion.md` como *primer commit* de este acto, antes de lo que sigue — convención de `forense/encargos/convencion.md`. Estado ahí: `CONSUMIDO (parcial)` — solo O. La búsqueda de "ADENDA-ADQUISICIÓN del plan v1.0" como archivo separado no encontró nada (`grep -i adquisici forense/recovery-plan-v1_0.md` → vacío): el propio encargo es la adenda: no cita un archivo ausente, se declara a sí mismo.

---

## 1 · Premisas (verbatim del encargo)

```bash
set -u; cd "$(git rev-parse --show-toplevel)"
awk -F'\t' 'NR==1{for(i=1;i<=NF;i++){if($i~/capa2/)a=i}} NR>1 && $a=="NO_REFERENCIADO"' data/curacion-registro/relaciones.tsv | wc -l
```
→ **105** (columna real: `capa2_manifiesto`, posición 10 de 19; el encargo esperaba "~105" — coincide exacto).

```bash
ls forense/censo-estimabilidad-coeficientes-v1_0.md data/catalogo-fuentes-v2_0.md >/dev/null && echo "PASA insumos" || echo "PARA insumos"
```
→ **PASA insumos**.

---

## 2 · Discrepancia declarada: el encargo dice "N1-N15", el registro real usa N1-N33

El texto del encargo especifica la columna `n_necesidades_servidas (N1-N15)`. La búsqueda real en `data/curacion-registro/relaciones.tsv` (`awk -F'\t' 'NR>1{print $2}' | sed 's/N//' | sort -n | uniq`) da rango **N1 a N33**, no N1-N15. Terreno distinto del que el encargo supone — se reporta, no se interrumpe (Bloque D: "encontrar que el terreno no es el que el encargo supone es entregable, no interrupción").

`data/curacion-registro/necesidad-objeto-modelo.tsv` (33 filas, ya en el repo, sin tocar aquí) resuelve el rango completo:
- **N1-N15** — 1:1 con las 15 filas de `forense/censo-estimabilidad-coeficientes-v1_0.md §5` (mismo orden G1→G6; verificado por comparación directa, no supuesto).
- **N16-N20** — objetos de regla (`tramite.*`, `dinero.*`, `civico.*`), no coeficientes.
- **N21-N33** — fichas de falsación de Hito D (`R1.4` … `R10.3`).

Esta nota usa el rango real (N1-N33) para `n_necesidades_servidas`. No se re-escribe el encargo; se declara la diferencia como este mismo párrafo lo hace.

**BARRIDO-COMPLETO (N1-N33) no es la fuente de este rango.** Ese barrido es categoría D — nunca llegó a commit, vive solo en una máquina sin PR (`git ls-remote --heads origin` no tiene la rama). El rango N1-N33 que sí se usó aquí viene de `necesidad-objeto-modelo.tsv`, que **sí** está en `origin/main` — archivo distinto, no depende del trabajo no commiteado.

---

## 3 · Método — cuatro reglas derivadas, cada una con su comando

**3.1 · `fuente_canonica` y agrupación.** `relaciones.tsv` filtrado a `capa2_manifiesto=="NO_REFERENCIADO"` (105 filas), agrupado por `fuente_canonica_normalizada` → **54 fuentes distintas**. Cada fuente puede tener 1-14 filas (una por `necesidad_id` que sirve); ISSP es la más ancha (14 filas, 7 necesidades).

**3.2 · `destraba_sin_ruta`.** Cruce mecánico, no narrativo: `necesidad-objeto-modelo.tsv` columna `reserva` marca **NINGUNA** (búsqueda no cerrada por ADR) vs. `"ADR-52/54 permanece cerrada"` para cada una de N1-N15. Cruzado contra la columna `Ruta` de `censo-estimabilidad-coeficientes-v1_0.md §5`:

| Fila censo | Necesidad | Ruta | Reserva | ¿Abierta? |
|---|---|---|---|---|
| 3 | N3 | SIN-RUTA | ADR-54 cerrada | NO |
| 4 | N4 | SIN-RUTA | ADR-52 cerrada | NO |
| 6 | N6 | SIN-RUTA | ADR-52 cerrada | NO |
| **10** | **N10** | SIN-RUTA | NINGUNA | **SÍ** |
| 11 | N11 | SIN-RUTA | ADR-54 cerrada | NO |
| **12** | **N12** | SIN-RUTA | NINGUNA | **SÍ** |
| **13** | **N13** | SIN-RUTA | NINGUNA | **SÍ** |
| **14** | **N14** | SIN-RUTA | NINGUNA | **SÍ** |
| **15** | **N15** | SIN-RUTA | NINGUNA | **SÍ** |

`destraba_sin_ruta` = **SÍ (fila censo N, necesidad)** si la fuente sirve N10/N12/N13/N14/N15; **NO** en cualquier otro caso — incluida una fuente que solo toca N3/N4/N6/N11 (SIN-RUTA pero *cerrada*: acquirir más no destraba nada, la búsqueda de reactivo ya se cerró formalmente). **5 fuentes caen en esa zona ciega de la columna** — tocan un SIN-RUTA cerrado y ninguno abierto, así que su `destraba_sin_ruta` es un `NO` correcto pero no dice "esta fuente es irrelevante al censo": `ISSP` (también toca N12/13/14 abiertas, por eso su fila real es SÍ), `GPS` (solo N4/N6 cerradas), `INTERACTING_AS_EQUALS_REDUCES_PARTISAN_POLARIZATION_IN_MEXICO` (solo N3 cerrada), `MICROCREDIT_IMPACTS_COMPARTAMOS_RCT` y `MICROCREDIT_IMPACTS_RANDOMIZED_MICROCREDIT_PROGRAM_PLACEMENT_EXP` (ambas solo N3 cerrada) — declarado aquí para que "NO" no se lea como "sin relación con el censo".

**Resultado: 5/54 fuentes con `destraba_sin_ruta` ≠ NO** — las que aparecen en el corte propuesto (§5) en las primeras cuatro posiciones.

**3.3 · `destraba_condicional_faltante`.** `relaciones.tsv` columna `evidencia_ref` (formato `MAIN:<archivo>:L<línea>`) apunta a una de cinco fuentes; se unió por número de línea (1-indexado, header=línea 1) contra la columna de condición faltante de cada una:

| Archivo (evidencia_ref) | Filas NO_REFERENCIADO | Columna URL | Columna condición faltante |
|---|---|---|---|
| `data/mapa-ext-general-2026-08-06.tsv` | 36 | `URL_primaria` (5) | `qué_condición_sigue_faltando` (21) |
| `data/mapa-fuentes-externas-consolidado-2026-08-06.tsv` | 35 | *(no tiene)* | `condicion_faltante` (17) |
| `data/mapa-ext-academico-2026-08-06.tsv` | 16 | `url_primaria` (10) | `condicion_faltante` (21) |
| `data/mapa-fuentes-2026-08-06.tsv` | 14 | *(no tiene — solo `n_urls_portal`/`slug_portal`, sin URL literal)* | *(no tiene esta columna — es rollup por fuente, no detalle por variable)* |
| `forense/notas/2026-08-08-verif3.md` | 4 (3 fuentes) | prosa | prosa |

Las 14 filas contra `mapa-fuentes-2026-08-06.tsv` (fuentes: `ENIF`, `SERIES_SPEI_CODI_BANXICO`, `AHORRO FINANCIERO Y FINANCIAMI`, `BDIF`, `ENAFIN`, `PI`, `LAPOP`, `LATINOBARÓMETRO`) **no tienen `condicion_faltante` mecánicamente disponible** — la columna no existe en ese archivo (es el rollup de 13 columnas por fuente, no el detalle de 21-23 columnas por variable). Su valor en la cola es literalmente `NO`, y eso **refleja ausencia de dato consultable, no confirmación de que no falte nada** — declarado aquí para no confundir "no lo sé" con "está completo". Notable: dos de estas ocho son `LAPOP` y `LATINOBARÓMETRO`, ambas sirviendo N30 (R8.3) — el hueco de dato es justo donde más pesaría saber.

Las 3 fuentes de `verif3.md` (`ACLED`, `SICS`, `SE`) se leyeron a mano (no hay columna que unir en una nota en prosa) y se citan con línea exacta en el script de derivación — declarado como excepción al método mecánico, no oculto:
- `ACLED` (`verif3.md:105-112`): agregado mes×año, sin admin1/admin2/estado/municipio ni coordenadas.
- `SICS` (`verif3.md:190-198`, `EXISTE-NO-SATISFACE`): conteos nacionales agregados por ejercicio fiscal, sin identificador de comité.
- `SE` (`verif3.md:250-258`): 45 páginas de percepción 0-100, sin variable de frecuencia conductual.

El texto de condición se etiqueta por `necesidad_id` cuando la fuente sirve más de una (p. ej. `N12:… || N13:…`), para no perder cuál hueco corresponde a cuál necesidad al fusionar varias filas de `relaciones.tsv` en una sola fila de fuente.

**Resultado: 43/54 fuentes con `destraba_condicional_faltante` ≠ NO.**

**Cruce contra la sub-investigación de N16-N33** (fork de esta misma sesión, sobre `forense/hitoD-preregistro-v2_0.md` y `forense/notas/2026-08-08-barrido1.md`): confirma condición faltante nombrada y abierta para N17/N19/N20/N21/N30 — coincide con lo que el cruce mecánico de esta sección ya encontró para las fuentes que tocan esas necesidades (`ACLED`/`GDELT`/`CSES`/etc. en N17; `ENCOAP`/`OECD`/`ISSP` en N30). Dos hallazgos de esa sub-investigación **no verificados a fondo** (declarado, no se inventa certeza): el mecanismo exacto de bloqueo de N22 y N27 más allá de estar en la lista "ocho D probable" de `hitoD-preregistro`. No cambia ninguna fila de la cola — ninguna fuente de las 54 depende solo de N22/N27 para su `destraba_condicional_faltante` (`MEXICO_ENTERPRISE_SURVEYS_COMPONENTE_PANEL_CANDIDATO_2006_2010`, `SE` y `WORLD_BANK_ENTERPRISE_SURVEY_MEXICO_2023` tocan N22, pero las tres ya tienen condición propia vía el mapa externo).

Hallazgo adicional de la sub-investigación, fuera del perímetro de este acto pero declarado: `necesidad-objeto-modelo.tsv` registra N17 (`tramite.gobierno_digital.*`) y N24 (`R3.4`) como necesidades separadas, pero `hitoD-preregistro-v2_0.md:872` indica que ambas resuelven a la misma ficha `R3.4` — colisión ya nombrada en ese archivo, no introducida aquí. No se corrige `necesidad-objeto-modelo.tsv` (fuera de perímetro); se declara para que quien abra P/Q/R no cuente esa necesidad dos veces si una sola fuente sirviera ambas.

**3.4 · `celda_piloto_FIN`.** `propuesta-motor-adaptativo-celda-v0_3.md §5` fija el gate de semana 1 del piloto FINANZAS DEL HOGAR sobre "las necesidades N3-N20" (trámites como fallback nombrado del mismo piloto, no automático — de ahí que el rango incluya N16-N20, no solo los coeficientes de finanzas). `celda_piloto_FIN = SÍ` si la fuente sirve alguna necesidad en {N3..N20}, `NO` en otro caso. **26/54 SÍ.** Nota: ninguna de las 54 fuentes es `ENSAFI`/`ENFIH` (las dos fuentes que el propio piloto usa) — esas ya están `capa2=SI` o `SI_O_REFERENCIADO`, fuera del universo NO_REFERENCIADO de este acto; `celda_piloto_FIN` aquí marca relevancia de dominio, no pertenencia a las 20 relaciones `CANDIDATA` que el piloto ya tiene abiertas.

**3.5 · `url_conocida`.** Del mismo cruce por línea que 3.3, columna `URL_primaria`/`url_primaria` cuando el archivo la tiene y el valor empieza con `http`. **22/54 con URL conocida.** `ISSP` tiene tres URLs distintas (GESIS, tres módulos distintos) — la cola deja solo la primera (`.../social-networks/2017`, la que corresponde a N12/N13/N30) para que la columna quede usable por `curl` sin anotación; las otras dos (`.../social-inequality/2019`, `.../family-and-changing-gender-roles/2012`) quedan declaradas aquí, no en el TSV.

**3.6 · `clasificacion_a4_previa`.** Directo de `relaciones.tsv`: `clasificacion_relacion`+`reason_code` agregados por fuente (`CANDIDATA(APERTURA_INDETERMINADA)` cuando la fuente es uniforme; conteo tipo `CANDIDATAx3+NEGATIVAx1` cuando mezcla clases entre sus necesidades). **39/54 puramente CANDIDATA**, **6/54 tocan NO_ACCESIBLE** en alguna de sus relaciones — a esas la vía de adquisición no es "descargar", es la declaración de A.6/A.5 que P ya prevé (no se fuerza pago/afiliación).

**3.7 · `palanca`.** Orden lexicográfico exacto del encargo: `sin_ruta > condicional > n_necesidades > piloto` (cada uno descendente — tener la propiedad pesa más que no tenerla), con `fuente_canonica` alfabético como desempate estable. `palanca` es el rango resultante, 1 (máxima prioridad) a 54. Verificado permutación completa de 1..54 sin huecos ni repetidos.

---

## 4 · Verificación de integridad del TSV

```
55 líneas (1 header + 54 filas) · 8 columnas en cada una · csv.reader no encuentra fila mal formada
palanca == permutación de 1..54 · 54 fuente_canonica únicas
```

---

## 5 · Corte propuesto — lotes 1-3, ≤5 fuentes cada uno (mesa firma al fusionar)

| Palanca | Fuente | Necesidades | `destraba_sin_ruta` | Piloto FIN | URL conocida |
|---|---|---|---|---|---|
| 1 | ISSP | 7: N2,N3,N12,N13,N14,N28,N30 | SÍ (fila 12,13,14) | SÍ | gesis.org/.../social-networks/2017 |
| 2 | ESTUDIOS_DE_RECHAZOS_Y_CORPUS_PRAGMATICO_DE_FELIX_BRASDEFER | 2: N15,N31 | SÍ (fila 15) | SÍ | pragmatics.indiana.edu/.../Encdeserv.html |
| 3 | WVS | 2: N5,N15 | SÍ (fila 15) | SÍ | VACIO |
| 4 | EARLY_CHILDHOOD_EDUCATION_PROGRAM_IMPACT_EVALUATION_2012_2014 | 1: N13 | SÍ (fila 13) | SÍ | microdata.worldbank.org/catalog/2661 |
| 5 | IMPACT_EVALUATION_OF_MOBILE_PEDAGOGICAL_TUTORS_2016 | 1: N15 | SÍ (fila 15) | SÍ | microdata.worldbank.org/catalog/6667 |
| 6 | GPS | 5: N2,N4,N5,N6,N17 | NO* | SÍ | gps.econ.uni-bonn.de |
| 7 | CSES | 4: N17,N25,N26,N27 | NO | SÍ | cses.org/data-download/cses-module-5 |
| 8 | MEXICO_ENTERPRISE_SURVEYS_COMPONENTE_PANEL_CANDIDATO_2006_2010 | 3: N22,N23,N32 | NO | NO | VACIO |
| 9 | WORLD_BANK_ENTERPRISE_SURVEY_MEXICO_2023 | 3: N22,N23,N32 | NO | NO | microdata.worldbank.org/catalog/6453 |
| 10 | ACLED | 2: N17,N27 | NO | SÍ | VACIO |
| 11 | GDELT | 2: N17,N27 | NO | SÍ | gdeltproject.org/data.html |
| 12 | INTERACTING_AS_EQUALS_REDUCES_PARTISAN_POLARIZATION_IN_MEXICO | 2: N3,N17 | NO* | SÍ | nature.com/articles/s41562-024-02043-y |
| 13 | MASS_MOBILIZATION_DATA_PROJECT_EVENTOS_MEXICO | 2: N17,N27 | NO | SÍ | VACIO |
| 14 | MASS_MOBILIZATION_PROTEST_DATA | 2: N17,N27 | NO | SÍ | massmobilization.github.io |
| 15 | MASS_MOBILIZATION_PROTEST_DATA_MEXICO | 2: N17,N27 | NO | SÍ | VACIO |

`*` = toca un SIN-RUTA cerrado (§3.2), no uno abierto — declarado, no oculto por el NO.

**Lote 1 (palanca 1-5):** las cinco fuentes que tocan un SIN-RUTA genuinamente abierto (N10/12/13/14/15) — el único grupo donde adquirir directamente destraba un coeficiente de generador hoy sin ruta. `ISSP` es además la única con 7 necesidades servidas — máxima densidad de la cola.

**Lote 2 (palanca 6-10):** `n_necesidades_servidas` alto (3-5) o `WORLD_BANK`/`MEXICO_ENTERPRISE_SURVEYS` (mismo par N22/N23/N32, R2.1/R2.2/R10.2 — "dato organizacional propietario" por la sub-investigación de N16-N33, así que su valor real puede ser menor de lo que el conteo sugiere; mesa puede querer bajar su prioridad pese al palanca mecánico).

**Lote 3 (palanca 11-15):** familia `MASS_MOBILIZATION_*`/`GDELT`/`ACLED` — cinco fuentes de eventos de protesta/conflicto que se solapan casi por completo en necesidades (N17/N27) y en método (bases de eventos georreferenciados); probable que **una sola** valga la pena abrir primero y las otras cuatro se reevalúen después con lo que esa primera arroje — mesa decide, esta cola no colapsa duplicados de dominio.

Nada de este corte obliga hasta que mesa lo firme al fusionar (regla del propio ACTO O).

---

## 6 · Lo que este acto NO hace

No descarga nada — `data/raw` se enlazó por higiene de ARRANQUE, nunca se leyó. No corre `tests/manifiesto.py`. No cambia `capa2_manifiesto` de ninguna fila de `relaciones.tsv`. No ejecuta P, Q ni R — quedan pendientes, gateados en esta misma cola (`forense/encargos/2026-08-12-adenda-adquisicion.md`, estado `CONSUMIDO (parcial)`). No corrige la colisión N17/N24 de `necesidad-objeto-modelo.tsv` (declarada en §3.3, fuera de perímetro). No re-abre ningún cierre ADR-52/54 (§3.2 los cita, no los reconsidera).

---

## 7 · Contadores

**0** — este acto ordena, no mide. Ningún contador de Hito D, coeficientes o probabilidades del motor se mueve. El "contador" propio de O es la cola misma: 54 filas nuevas, 0 antes.
