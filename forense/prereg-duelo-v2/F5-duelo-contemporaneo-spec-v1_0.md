# `F5-DUELO-CONTEMPORANEO` — spec congelada del duelo de la misma generación (primera mitad) — v1.0

**Acto:** `GEN2-F5-RECAPTURA-L` (CAJA, Ubuntu/WSL de mesa, Opus). Redactado contra
`origin/main = ffeeca2c` (PR #667), 9/sep/2026. **CONTADOR: cero** — este documento
congela el contrato; ninguna celda se captura hasta que esté commiteado (COMMIT-1).
Sucede a `prereg-corrida-v1_0.md` y `PAQUETE-L-v1_1.md` (el contrato heredado) sin
reescribirlos — ninguno de los dos se edita. Sucede también, por lo que corrige,
a `PAQUETE-L-v1_2.md` (paquete mecánico de 14 celdas del marco v1.2, sellado pero
nunca lanzable con corpus real: su placeholder de contexto documental y sus 176/224
hardcodeados son exactamente lo que este acto reemplaza en `runner_l_cli.py`, con
enmienda fechada, no por reescritura silenciosa).

**Firma de mesa que autoriza este diseño (verbatim, 9/sep/2026):** *"Ya habíamos
decidido no hacerlo a través de API, solo quiero asegurar que las llamadas que me
compartes son dentro de una caja en ubuntu sin acceso al corpus etc, necesito eso
turbo blindado, así que avancemos."* — y la elección de diseño que dirección
propuso y mesa avanzó: **transferencia como pregunta primaria, uso documental como
secundaria pre-registrada, re-captura ya.** Esto satisface la compuerta que
`PLAN-DE-OBRA-GEN2-v1_1` F5 exige ("mesa elige antes de capturar cuál pregunta se
contesta... y las dos no se mezclan en una afirmación única").

**Estado de la COMPUERTA declarada en el encargo, dicho aquí sin adornos.** El
encargo declara: *"COMPUERTA: GATED a PR del ACTO GEN2-RETIRO-CRON-LEGADO
fusionado (fila de caja; además garantiza que ningún cron dispare a media
captura)."* Verificado en esta sesión, contra GitHub y contra el crontab real de
esta caja, ANTES de escribir esta spec: **ese PR no existe** — ni fusionado, ni
abierto, ni en rama, en ningún punto del árbol o del repositorio remoto. La línea
de crontab legado (`30 7 * * 1-5 cd /home/pc0/mm-adq && ./tools/adquiere_cron.sh`)
sigue instalada hoy en esta caja (verificado con `crontab -l`). Mesa, informada de
este hallazgo, autorizó una desviación acotada y por escrito (patrón ya usado en
este programa: [[feedback-partial-gate-deviation]]): **P1 (este documento) y P2
(el blindaje) proceden ahora; P3 (las 224 invocaciones reales) queda diferido
hasta que la compuerta se resuelva** — por el PR de `GEN2-RETIRO-CRON-LEGADO`, o
por otra decisión explícita de mesa. Nada de lo que sigue invoca `claude`;
**CONTADOR: cero** se mantiene íntegro en este acto.

**ENMIENDA (misma sesión, ~15:37, no se reescribe el párrafo de arriba — regla de
enmienda fechada, no de silencio).** `PR #668 · ACTO GEN2-RETIRO-CRON-LEGADO` se
fusionó mientras este acto redactaba P1/P2 (merge `cc1cfe2`, ~15:16) — **la
compuerta que el párrafo de arriba encontró incumplida YA se cumple.** Verificado
de nuevo, empíricamente, en esta misma caja: `crontab -l` ya no trae la línea de
`adquiere_cron.sh` (solo el bloque de comentario y el `PATH=`). El hallazgo del
párrafo de arriba fue correcto **en el momento en que se hizo** — no se corrige
hacia atrás, se declara que el estado cambió. **P3 sigue sin ejecutarse en este
acto**: la decisión de lanzarlo ahora que la compuerta se despejó es de mesa, no
de esta sesión — el encargo autorizó explícitamente P1+P2, no P3, y 224
invocaciones reales con captura sellada e inamovible no es una expansión de
alcance que se autoconceda.

---

## 0 · Perímetro y qué NO hace este documento

Toca: `forense/prereg-duelo-v2/` (esta spec, `L-spec-v1_3.json`/`.sha256`,
`paquete-corpus-F5-v1_0/`, la enmienda fechada a `runner_l_cli.py`) ·
`forense/notas/` · `forense/no-corrido.tsv` (append) · `0-bis` · cascada al cierre
de la pieza que corresponda. NO toca `milpa/`, `CALC-*`, las capturas históricas de
`corridas-L/` (424 archivos v1_1/v1_2, ni se renombran ni se re-corren), ni el
marcador. No llama a ningún API ni maneja ninguna key. No adjudica la tesis ni corre
el marcador — eso es `ACTO GEN2-F5-DUELO-CALC`, sucesor. No amplía `k` ni celdas
sobre la marcha. No mete al paquete-corpus nada fuera de su lista cerrada (§3). No
decide `margen_utilidad_pp`.

---

## A.8 · Verificación de existencia, contra el árbol (no contra el encargo)

Verificado en esta sesión, contra `ffeeca2c` y contra la caja real:

| Afirmación del encargo | Verificado | Evidencia |
|---|---|---|
| `runner_l_cli.py` EXISTE con los invariantes (k=8, dos variantes, sufijo -M, versión por `claude --version`) | SÍ, y además trae DOS enmiendas previas no citadas por el encargo (dimensión dinámica, `MAESTRA34-N4`; `sha256_prompt`/`params` restaurados, `L-CORRIDAS-v1_2`) y una tercera (`P4/D3`, sufijo `__<SPEC_VERSION>`) — hash antes de esta spec: `b2c3965851423d07f164d11da914972742924e70bfb5f9f71cc8f70ad5aeb7e3` | `git log --oneline -- forense/prereg-duelo-v2/runner_l_cli.py`; `sha256sum` corrido en esta sesión |
| `marco-M-sorteado-v1_3.tsv` (14 celdas) EXISTE | SÍ — 15 líneas (1 cabecera + 14 filas, todas `elegible_v1_1=SI`) | lectura directa |
| Los seis `CALC-R-CIV-M-*` GEN2 + `corridas-R/` EXISTEN | SÍ | `data/corrida0/CALC-R-CIV-M-{01,02,04,10,12,13}/` |
| `PAQUETE-L-v1_1.md` y `prereg-corrida-v1_0.md` EXISTEN, contrato heredado | SÍ, leídos íntegros | lectura directa |
| Capturas GEN2 del marco v1_3: NO-ENCONTRADO | CONFIRMADO — las 424 capturas existentes (`corridas-L/`) son v1_1/v1_2, pre-GEN2 | `NC-0077`: *"435 payloads posteriores a la ventana de captura (1-2/sep/2026)"* — cifra citada verbatim, verificada contra la fila real de `forense/no-corrido.tsv` |
| Marcador INCONCLUSO (#651) es el estado que este duelo sucede | CONFIRMADO | PR #651, `ACTO GEN2-C0-D-CORRECTIVO`, fusionado 2026-09-09T05:13:40Z: `RESULT-C0D-ADJUDICACION-HALLAZGO = INCONCLUSO`, `RESULT-C0D-ADJUDICACION-SUCESOR = NC-0077` (reutilizada, "acto de re-captura L_CORPUS con corpus GEN2") |

**Hallazgo adicional de esta sesión, no anticipado por el encargo:** las 14 celdas
de `marco-M-sorteado-v1_3.tsv` son, ID por ID, universo por universo, las mismas 14
de `marco-M-sorteado-v1_2.tsv` — el único de los seis campos transportados a
`L-spec` que difiere es `conducta` en `TRA-M-02/03/07` (`paga_mordida` →
`paga_mordida_encig2025`, `ACTO MAESTRA38-M13`). `L-spec-v1_2.json` existía;
`L-spec-v1_3.json` **no existía** y se generó en este acto (§1) reimportando,
sin editar, la misma plantilla mecánica sellada (`derivar_pregunta_l`,
`genera_l_spec_v1_1.py`) — mismo patrón que `PAQUETE-L-v1_2.md` §1-bis ya usó para
v1.2. `runner_l_cli.py` ya deriva su dimensión de la spec cargada (enmiendas
previas) — apuntarlo a `L-spec-v1_3.json` no requería, por sí solo, ninguna edición
adicional. **Lo que sí requería edición** (§2, §4): el placeholder literal de
contexto para `L+corpus` (`"[contexto tierizado -- no construido en este acto]"`),
que nunca se había reemplazado por contenido real en ninguna corrida anterior — ni
v1.1 ni v1.2 llegaron a `--correr`.

---

## 1 · `L-spec-v1_3.json` — generado, sellado, hasheado

`forense/prereg-duelo-v2/L-spec-v1_3.json` — 14 celdas, generadas mecánicamente
desde `marco-M-sorteado-v1_3.tsv` vía `derivar_pregunta_l()` de
`genera_l_spec_v1_1.py` (importado por ruta, sin editar ni una línea — mismo patrón
reproducible que `PAQUETE-L-v1_2.md` §1-bis documentó para v1.2). `sha256`:
`5df1010179326c80169e1ff07c97e8c518ebd5a15e458afba7002b5adaaba5f4`
(`L-spec-v1_3.sha256`, adjunto).

Las 14 celdas (id · conducta · universo (resumido) · encuesta · ola):

```
CIV-M-01 · denuncia_con_miedo_o_desconfianza · ENVIPE · 2012
CIV-M-02 · denuncia_con_miedo_o_desconfianza · ENVIPE · 2013
CIV-M-04 · denuncia_con_miedo_o_desconfianza · ENVIPE · 2015
CIV-M-10 · denuncia_con_miedo_o_desconfianza · ENVIPE · 2021
CIV-M-12 · denuncia_con_miedo_o_desconfianza · ENVIPE · 2023
CIV-M-13 · denuncia_con_miedo_o_desconfianza · ENVIPE · 2024
DIN-M-01 · tiene_ahorros                     · ENNViH/MxFLS · 2002 (ola 1)
FAM-M-01 · recibe_dinero_familiares_para_vejez · ENIF · 2018
FAM-M-05 · recibe_remesas                    · ENIGH · 2016
FAM-M-06 · recibe_remesas                    · ENIGH · 2018
FAM-M-07 · recibe_remesas                    · ENIGH · 2020
TRA-M-02 · paga_mordida_encig2025            · ENCUCI · 2020
TRA-M-03 · paga_mordida_encig2025            · ENCIG · 2013
TRA-M-07 · paga_mordida_encig2025            · ENCIG · 2021
```

`14 celdas × 2 variantes × k=8 = 224 invocaciones` (§4).

---

## 2 · (a) Pregunta PRIMARIA — TRANSFERENCIA, corte temporal por celda

**Regla (encargo, verbatim):** *"para cada celda de ola X, L_CORPUS recibe
únicamente material permitido por el corte temporal de X — un documento que
contenga cifras de la ola X o posteriores queda EXCLUIDO de esa celda."*

**Operacionalización, fijada aquí antes de construir el paquete:** un documento del
corpus se excluye de la celda (encuesta E, ola X) si contiene al menos una cita
identificable de E con año ≥ X del calendario real de olas de E, **o** si contiene
una cita de E sin año determinable. La segunda cláusula es deliberadamente
conservadora — una cita sin fecha no se asume anterior a X solo porque sería
conveniente que lo fuera.

**Calendario real de olas por encuesta** — derivado de `data/manifiesto.yaml`
(los IDs de payload realmente adquiridos), no supuesto ni de memoria externa:

| Encuesta | Olas disponibles en el corpus adquirido |
|---|---|
| ENVIPE | 2011–2025 (anual) |
| ENCIG | 2011, 2013, 2015, 2017, 2019, 2021, 2023, 2025 (bienal) |
| ENIF | 2012, 2018, 2021, 2024 |
| ENIGH (Nueva Serie) | 2012, 2014, 2016, 2018, 2020, 2022 (bienal) |
| ENCUCI | 2020 (única ola adquirida) |
| ENNViH/MxFLS | ola 1 (2002), ola 2 (2005-06), ola 3 (2009-12) |

**Cómo se determinaron las citas por documento, sin adivinar.** Los 37 documentos
de `corpus/reports/` + `corpus/forense/` (el corpus GEN2 adoptado, `PLAN-DE-OBRA-
GEN2-v1_1` F5) se leyeron ÍNTEGROS, uno por uno, por 37 sesiones independientes
(workflow paralelo, cada una ciega a las demás), cada una extrayendo TODA cita de
las seis encuestas con su año/ola tal como aparece en el texto y un snippet verbatim
verificable. El resultado completo vive en
`forense/prereg-duelo-v2/paquete-corpus-F5-v1_0/manifiesto.json` (`razones_exclusion`
por documento, con la cita que motivó cada exclusión). Ningún documento se excluyó
por juicio de "relevancia temática" — solo por la regla mecánica de arriba.

**Resultado por celda** (documentos incluidos / excluidos de 37 totales):

| Celda | Encuesta·ola | Incluidos | Excluidos | Documentos excluidos (razón resumida) |
|---|---|---:|---:|---|
| CIV-M-01 | ENVIPE 2012 | 31 | 6 | citan ENVIPE ≥2012 o sin año — ver manifiesto |
| CIV-M-02 | ENVIPE 2013 | 31 | 6 | ídem |
| CIV-M-04 | ENVIPE 2015 | 31 | 6 | ídem |
| CIV-M-10 | ENVIPE 2021 | 31 | 6 | ídem |
| CIV-M-12 | ENVIPE 2023 | 31 | 6 | ídem |
| CIV-M-13 | ENVIPE 2024 | 31 | 6 | ídem |
| DIN-M-01 | ENNViH/MxFLS 2002 | 37 | 0 | el corpus no cita ENNViH/MxFLS en ninguna parte — celda sin exclusión, declarado, no supuesto |
| FAM-M-01 | ENIF 2018 | 32 | 5 | citan ENIF ≥2018 |
| FAM-M-05 | ENIGH 2016 | 33 | 4 | citan ENIGH ≥2016 o sin año |
| FAM-M-06 | ENIGH 2018 | 33 | 4 | citan ENIGH ≥2018 o sin año |
| FAM-M-07 | ENIGH 2020 | 33 | 4 | citan ENIGH ≥2020 o sin año |
| TRA-M-02 | ENCUCI 2020 | 32 | 5 | citan ENCUCI 2020 (única ola — cualquier cita excluye) |
| TRA-M-03 | ENCIG 2013 | 31 | 6 | citan ENCIG ≥2013 o sin año |
| TRA-M-07 | ENCIG 2021 | 31 | 6 | citan ENCIG ≥2021 o sin año |

La lista completa de documentos incluidos/excluidos, por celda, con hash individual
de cada documento y hash de bundle, vive en `manifiesto.json` (§3).

**M y B bajo el mismo corte.** El marcador `M` y el corredor `B` no reciben corpus
documental (son cálculo/regla, no elicitación con contexto) — el corte temporal no
les aplica mecánicamente, pero se declara aquí que ninguno de los dos usa, para
esta comparación, información de la propia ola evaluada o posteriores más allá de
lo que su propia cadena ya documenta (`milpa/tramite.yaml`, `procedencia.yaml`) —
consistente con que su rol aquí es secundario, sin veto (§5).

---

## 3 · Paquete-corpus — lista cerrada, con hash individual y de bundle

`forense/prereg-duelo-v2/paquete-corpus-F5-v1_0/` — congelado en este COMMIT-1,
contiene:

- `manifiesto.json` — por celda: documentos incluidos/excluidos (rutas relativas a
  este directorio) + razón de cada exclusión; `documentos`: sha256 individual de
  cada uno de los 37; `bundle_sha256`: `79d054cc186c06e3f07569c44896163efeef890de908f3ee64d5689ee15e95e0`
  (sha256 del JSON canónico `{ruta: sha256}` de los 37 documentos, orden
  determinista).
- `documentos/` — copia verbatim, sin edición, de los 37 archivos de
  `corpus/reports/` + `corpus/forense/` (el corpus GEN2 adoptado íntegro —
  `PLAN-DE-OBRA-GEN2-v1_1` F5). La copia existe para que P2 pueda mover este
  directorio COMPLETO a la caja aislada sin que esa caja necesite ruta al clon
  (`corpus/` vive dentro del clon; el paquete-corpus no).

**Exclusiones universales — categorías que NUNCA entran al paquete-corpus, con su
razón, aunque ninguna de las cinco exista físicamente dentro de `corpus/`:**

| Categoría excluida | Razón |
|---|---|
| `data/corrida0/CALC-R-*` | Contiene los valores objetivo (`R`) que el duelo existe para comparar — verlos rompería la ceguera del brazo `L_CORPUS`. |
| `forense/prereg-duelo-v2/corridas-R/` | Mismo motivo — es el archivo de resultados del árbitro. |
| La serie del cierre DBF (`data/corrida0/CALC-R-*/ejecucion.json`, `resultados.json`) | Mismo motivo, formato distinto. |
| Resultados del marcador (`scoreboard-*.md`, `agregado-*-resultado.json`) | Revelarían, indirectamente, el signo del hallazgo previo (`corpus-empeora`, `PLAN-DE-OBRA-GEN2-v1_1` §1) — contaminaría la elicitación con una expectativa. |
| Esta misma conversación de dirección (el encargo, las decisiones tomadas en esta sesión) | No existe para la caja — el blindaje de P2 (§6) es de aislamiento físico, no de promesa (firma de mesa, verbatim: *"necesito eso turbo blindado"*). |

Ninguna de las cinco vive dentro de `corpus/`, así que la exclusión ya está
satisfecha por construcción (el paquete-corpus solo lee de `corpus/reports/` y
`corpus/forense/`) — la tabla existe para que quede dicho, no porque hiciera falta
filtrar nada activamente.

---

## 4 · Mecánica de captura — 224 invocaciones, orden, reintentos

`runner_l_cli.py`, enmendado en este acto (§7), gobierna la mecánica. Invariantes,
sin cambio salvo lo que esta sección fija:

- `14 celdas × 2 variantes (L-solo, L+corpus) × k=8 = 224 invocaciones`.
- Cliente: Claude Code CLI en modo print (`claude -p --model opus --output-format
  json --system-prompt "<mínimo fijo>" --tools "" --max-turns 1`, prompt de
  celda entregado por **stdin**, no por `argv` — ENMIENDA F5-2, §8: con
  contexto de hasta 600 000 caracteres el argumento excedía el límite
  por-argumento de `execve`), CERO API. Prompt de sistema reemplazado por la
  cadena mínima fija ya sellada
  (`SISTEMA_MINIMO`). Sin `--add-dir`, sin herramientas de archivo sobre el clon.
- `contexto_corpus` para `L+corpus`: ensamblado real desde `paquete-corpus-F5-v1_0`
  (§3), documentos concatenados en orden alfabético de ruta, presupuesto de
  **600 000 caracteres** por invocación. **Declarado sin rodeos: con 31–37
  documentos de ~35 KB promedio, el presupuesto se agota en las 14 celdas — cada
  invocación `L+corpus` ve un PREFIJO alfabético de sus documentos permitidos, no
  el corpus completo de esa celda.** El corte es determinista (mismo orden
  siempre, fijado antes de capturar, ciego a qué documento resulta más o menos
  favorable) y se registra por invocación (`contexto_corpus_metadata`:
  `documentos_incluidos`, `truncado`, `truncado_en_documento`) — el límite se
  declara en cada captura, nunca en silencio (`PLAN-DE-OBRA-GEN2-v1_1` F5:
  *"«acceso al corpus» no promete que todos sus bytes quepan en contexto"*).
- **Orden contrabalanceado, semilla declarada.** `orden_captura()` permuta las 224
  tuplas con `random.Random(42).shuffle()` — semilla 42, la misma ya sellada en
  todo bootstrap de `scoring-adv1-m3.py` (`FP-168`), reutilizada aquí para un
  propósito distinto pero análogo (determinismo declarado, no una segunda
  semilla arbitraria). Ni todas las `L-solo` antes que todas las `L+corpus`, ni
  celda por celda en el orden del marco.
- **Reintentos acotados y contados.** Hasta 2 reintentos por captura (3 intentos
  totales), `timeout=180s` por intento. Agotados, la captura se escribe con
  `estado_captura=RECHAZADO_TRAS_REINTENTOS` — no se pierde la fila, no se tumba
  el lote. Un rechazo de CONTENIDO (el modelo responde pero se abstiene o dice "no
  lo sé") **no** es un rechazo técnico y **no** se reintenta — cuenta como corrida
  válida, mismo principio de `pipeline-L-adv1-m2.py` ("cero descartes").
- Sesiones stateless independientes: una invocación = una captura, sin memoria
  entre celdas ni entre brazos (ya garantizado por `claude -p --max-turns 1`, una
  invocación de proceso por captura).

**Embudo de P3 (a reportar, no ejercido en este acto):** éxitos, reintentos,
rechazos y truncamientos — por brazo, sobre las 14 celdas completas, no solo sobre
las celdas donde un brazo tuvo éxito (un brazo que se abstiene en celdas difíciles
se reporta con cobertura sobre TODO el marco).

---

## 5 · (e) Escala de adjudicación EXHAUSTIVA, pre-declarada (B-bis)

**No se inventa un procedimiento nuevo — se adapta el ya sellado.**
`procedimiento-scoring-v1_2.md` §§1-3 fija, para la comparación `L_SOLO_vs_M`:
unidades `z = (punto−R)/EE(R)`, banda de indiferencia `delta=0.5` (misma constante
que `banda-tost-margen-v1_0.md` deriva de `ADV1-M3`), bootstrap `seed=42,
nivel_ic=0.95, replicas=10000` (`FP-168`). Su §7 (D4) añade una métrica secundaria
en puntos porcentuales (`err_pp`, `MAE_pp`) cuando `z` no discrimina. La pregunta
de ESTE duelo (`L_SOLO` vs `L_CORPUS`, no `L` vs `M`) no estaba sellada — se
construye aquí reutilizando exactamente el mismo aparato.

**Cantidades, por celda con `R`/`EE(R)` computado y ambos brazos disponibles:**

```
z_LSOLO   = (agregado(L-solo)   − R) / EE(R)
z_LCORPUS = (agregado(L+corpus) − R) / EE(R)
```

`agregado(brazo)` = mediana de las k=8 corridas de ese brazo/celda
(`agregar_continua`/`agregar_categorica`, `pipeline-L-adv1-m2.py` §5, sin
reinventar).

**Cantidad pareada primaria — desviación ABSOLUTA respecto a `R` (no signada, a
propósito: esta pregunta es "¿quién se acerca más a la verdad?", no "¿hacia
dónde se desvía cada uno?" — por eso se aparta de la forma signada de
`procedimiento-scoring-v1_2.md` §3, que existía para una pregunta distinta):**

```
dif_abs_pareada = |z_LCORPUS| − |z_LSOLO|
```

Negativo: `L+corpus` más cerca de `R` que `L-solo`. Positivo: al revés. Se
bootstrapea la media de `dif_abs_pareada` sobre el universo pareado (celdas con
`z_LSOLO` **y** `z_LCORPUS` definidos, excluyendo `VERIFICACION-NO-PUNTUA` bajo
F-DD — mismo criterio que `procedimiento-scoring-v1_2.md` §5), con los mismos tres
parámetros sellados (`seed=42`, `nivel_ic=0.95`, `replicas=10000`) y el mismo
`delta=0.5` reutilizado, nunca un segundo bootstrap con otros números.

**Precedencia, declarada ANTES de ver dato — GANA/PIERDE/EMPATE/INCONCLUSO:**

| Condición sobre `[ic_lo, ic_hi]` de `dif_abs_pareada` | Veredicto |
|---|---|
| `ic_hi < −0.5` (todo el IC por debajo de `−δ`) | **GANA L_CORPUS** — el corpus reduce el error absoluto respecto a `R` más allá del margen material |
| `ic_lo > 0.5` (todo el IC por encima de `+δ`) | **PIERDE L_CORPUS** (gana `L_SOLO`) — el corpus incrementa el error absoluto; posible repetición del hallazgo "corpus-empeora" ya observado bajo el diseño `L`-vs-`M` (`PLAN-DE-OBRA-GEN2-v1_1` §1), esta vez bajo la comparación que sí lo adjudica |
| `−0.5 ≤ ic_lo` y `ic_hi ≤ 0.5` (todo el IC dentro de la banda) | **EMPATE** (equivalencia TOST) — el corpus no cambia materialmente la distancia a `R` |
| Cualquier otro traslape (el IC cruza un límite de la banda sin quedar enteramente de un lado) | **INCONCLUSO** — no se puede afirmar dirección ni equivalencia con la confianza pre-registrada |
| Universo pareado vacío o `n<3` | **INCONCLUSO por construcción**, declarado, no defecto — mismo precedente que `SIN_CELDAS_PAREADAS` (`procedimiento-scoring-v1_0.md` §6) |

**INCONCLUSO es una salida VÁLIDA, no un fallo del diseño** — es exactamente lo
que el encargo pide declarar antes de capturar, y exactamente el estado que este
duelo hereda del marcador (#651) sin prometer resolverlo por fuerza.

**Secundaria, no gatante — mismo patrón D4 (`procedimiento-scoring-v1_2.md` §7),
en puntos porcentuales:** `err_pp = 100·(punto−R)`, `MAE_pp` por brazo, comparación
pareada `|err_pp_LCORPUS| − |err_pp_LSOLO|`, reporta `L_CORPUS-MENOR-ERROR-PP` /
`L_SOLO-MENOR-ERROR-PP` / `INDETERMINADO` — **nunca** sustituye ni reabre el
veredicto primario de la tabla de arriba.

**`M` y `B`, secundarios, sin poder de veto** (`PLAN-DE-OBRA-GEN2-v1_1` F5). Se
reportan `z_M` y, si `B` tiene fila para alguna de las 14 celdas (hoy: ninguna,
`procedimiento-scoring-v1_2.md` §4), su misma forma — como contexto, nunca
gatando la primaria de arriba.

**Prohibido ampliar `n` tras ver el signo** sin diseño secuencial pre-registrado
— dicho aquí, antes de que exista un solo resultado.

---

## 6 · (f) Incertidumbre — tres fuentes separadas, con su límite declarado

1. **Celdas/panel.** Capturada por el bootstrap de §5 sobre el universo pareado de
   hasta 14 celdas — la misma mecánica que `procedimiento-scoring-v1_2.md` ya
   sella (`generar_indices_bootstrap`, `derivar_seed_scope`). Límite declarado:
   con pocas celdas puntuables, el IC puede ser ancho — eso es información, no
   defecto (§5, fila `n<3`).
2. **Réplicas de captura.** Cada celda/brazo agrega k=8 corridas por mediana
   (§5) — la dispersión entre esas 8 (IQR, q10/q90) se reporta junto al agregado
   pero **no se propaga** dentro del intervalo de confianza de `dif_abs_pareada`
   (que bootstrapea sobre celdas, no sobre réplicas individuales). Límite
   declarado explícitamente: el IC de §5 subestima la incertidumbre total en la
   medida en que la dispersión entre réplicas sea grande frente a la dispersión
   entre celdas — no se inventa una forma de combinarlas que este documento no
   pueda verificar contra un precedente sellado.
3. **Error del árbitro `R`, condicional.** `z` trata `EE(R)` como fijo/conocido —
   la misma aproximación que `procedimiento-scoring-v1_2.md` §1 ya hace y declara.
   Límite heredado, no nuevo: si `EE(R)` tiene su propio error de muestreo no
   capturado, el IC de §5 es condicional a que `R` quede fijo como está, no
   incondicional sobre su propia incertidumbre.

Ninguna de las tres fuentes se mezcla en un solo número sin declarar cuál es cuál.

---

## 7 · (g) Contaminación declarada

Los valores `R` de las seis celdas con árbitro ya calculado están en el repo
público del programa (`data/corrida0/CALC-R-CIV-M-*/resultados.json`) y en la
memoria de dirección — **por eso el blindaje de P2 es de aislamiento físico, no de
promesa.** Ningún documento del paquete-corpus (§3) contiene esos valores (la
tabla de exclusiones universales los cubre por categoría completa, no por
inspección caso por caso). La sesión que ejecute `--correr` (P3, diferido) debe
correr desde un directorio que no tenga, físicamente, ruta al clon ni al corpus de
microdatos — verificable, no prometido (P2, evidencia obligatoria §5-P2 más abajo).

---

## 8 · Enmienda a `runner_l_cli.py` — tabla de re-sellado

Regla de enmienda de `prereg-corrida-v1_0.md:110` (no se sobreescribe una tabla de
hashes — se agrega fila fechada, hash viejo → hash nuevo, razón). La tabla vive
aquí, no dentro del propio script (un script no puede citar su propio hash sin
volverse circular):

| Acto | hash viejo | hash nuevo |
|---|---|---|
| `MAESTRA33-E17 · L-ENMIENDA-CLI` (creación) | — | `1ae70bc2b55e6aa129f742d1d3914e13b6b0f2e0b860109edfd2d650967f4086` |
| `MAESTRA34-N4` (firma DR-a, dimensión dinámica) | `1ae70bc2…` | `0c10e9ab95350ce2b3596216eeda0c23e270bce492177bd14c5657c6e28598e2` |
| `L-CORRIDAS-v1_2` (firma DL-(1), `sha256_prompt`/`params`) | `0c10e9ab…` | `7ac9852e22201bc61218d2ccfb501e97efc76b51d55261abf213388257e04e4b` |
| `P4 (D3)`, commit `e8a95d0`, `FP-235`/`FP-240` (sufijo `__<SPEC_VERSION>`) | `7ac9852e…` | `b2c3965851423d07f164d11da914972742924e70bfb5f9f71cc8f70ad5aeb7e3` |
| **ENMIENDA F5** (este acto: contexto real de `L+corpus`, orden contrabalanceado, reintentos acotados y contados) | `b2c39658…` | `2f1983eb687dd2f4dbcc04378e3dafb6e055e2f24e1c5201ef15583c39acb8ad` |
| **ENMIENDA F5-2** (medida en P3, no supuesta: `OSError: [Errno 7] Argument list too long` en la primera invocación `L+corpus` real — el prompt con contexto de hasta 600 000 caracteres excedía el límite por-argumento de `execve`; el prompt ya no viaja en `argv`, se entrega por `stdin`, verificado empíricamente con `claude -p` antes de aplicar) | `2f1983eb…` | **`54c994b22111df70f60da599b6ffa0dacd8a62c55fcc5a217ff6cab79cdbaca5`** |

**Regresión obligatoria de la última fila, corrida en este acto:** `--dry-run` con
`L-spec-v1_1.json` → 176 rutas (verde, sin cambio de conteo); `L-spec-v1_2.json` →
224 (verde, sin cambio de conteo); `L-spec-v1_3.json` → 224, con `contexto_corpus`
real (no placeholder) para las 112 invocaciones `L+corpus` (verde, comportamiento
nuevo, esperado). Ninguna de las tres cambió su conteo de rutas respecto al
comportamiento previo a esta enmienda — el cambio es aditivo (contexto real,
orden, reintentos), no una re-arquitectura.

---

## 9 · Cierre de P1

**El primer resultado que produzca este procedimiento es el que se reporta.**

COMMIT-1: esta spec + `L-spec-v1_3.json`/`.sha256` + `paquete-corpus-F5-v1_0/`
(manifiesto + 37 documentos) + la enmienda a `runner_l_cli.py` de §8 (ya aplicada
y verificada por regresión). P3 (las 224 invocaciones, COMMIT-2+) queda
explícitamente diferido a que la COMPUERTA se resuelva — ver `0-bis`/
`## NO-CORRIDO / RESERVAS` de la nota de cierre de este acto.
