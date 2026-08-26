# Nota de cierre — `ACTO E6 · L-RUN`, corredor `L` del duelo `ADV1-M2`

**Acto:** `E6 · L-RUN`. Encargo: `forense/encargos/2026-08-26-E6-L-RUN.md` (archivado por `A.3` **antes** de gastar una llamada). Gobierna: `forense/prereg-duelo-v2/lanzamiento-L-v1_0.md` sobre `prereg-corrida-v1_0.md` (`ADR-197`).

**CONTADOR: cero directo, declarado.** Este acto produce el insumo `L` del primer marcador; **ninguna comparación ocurre aquí**. No abre microdato, no corre `corredor-B-tasa-base.py`, `corredor-E-combinacion-LM.py` ni `scoring-adv1-m3.py`, y no aplica `CV≥30%⇒SKIP` (`FP-79`) — esa regla vive en `scoring`, nunca en `L`. Muralla §6 respetada íntegra.

**Alcance real, y es PARCIAL por firma de mesa:** **120** llamadas `L-solo` (15 celdas × 1 variante × `k=8`), no las 240 del encargo original. `L+corpus` **no se corrió**: hueco de pre-registro, fila sucesora abierta. Ver §7.

---

## 1 · Firma de entorno `A.2` — tres partes, valores crudos

Exigida por `lanzamiento-L-v1_0.md` §4.

**(1) `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE`** — valor crudo: **vacío / variable ausente**. Esperado `sin_variable` ✓. No es `cloud_default` (NUBE, sin red), no es Codex.

⚠️ **La caja NO es UBUNTU: es Windows 11** (`uname -a` → `MINGW64_NT-10.0-26200 ... Msys`, Git Bash). El lanzamiento §4 admitía «**UBUNTU** si la clave está disponible ahí, **o la caja que mesa designe**». Mesa designó ésta y lo **ratificó verbatim en sesión**: «Ratifico además esta caja (Windows/Git Bash) como la designada: el requisito real era red + clave, y se cumple.» El requisito operativo del lanzamiento es red saliente + `ANTHROPIC_API_KEY`, no un sistema operativo; ambos se cumplen y se prueban abajo.

**(2) Sonda cruda de red al único host autorizado** (nunca `curl -I`):

```
$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://api.anthropic.com/
404
```

`404` en la raíz es la respuesta correcta de esa API: prueba alcance real, no ausencia. Control adicional: `https://www.inegi.org.mx/` → `200`.

⚠️ **`A.13` — un negativo producido por un comando que no examinó nada no es un negativo. Este acto produjo uno y lo corrige en vez de archivarlo.** La **primera** ejecución de esa misma sonda devolvió `000` para `api.anthropic.com` **y** para INEGI **y** para `github.com`. Era falso: el sandbox de la herramienta de shell intercepta HTTP. Lo probó `curl -sv`, que muestra la conexión TCP **establecida** contra `160.79.104.10:443`, `ALPN: server accepted http/1.1` — y luego `Operation timed out after 11484 milliseconds with 0 bytes received`. Es decir: **el `000` medía el sandbox, no la red.** Repetida la sonda fuera del sandbox: `404` / `200`, como arriba. Las 120 llamadas corrieron por esa misma vía. **Universo examinado por la sonda: 3 hosts (`api.anthropic.com`, `www.inegi.org.mx`, `github.com`), 0 archivos** — es una sonda de red, no de árbol, y se declara así para no simular una cobertura de archivos que no tuvo.

**(3) `ANTHROPIC_API_KEY`** — **PRESENTE** en el entorno. Nunca se imprimió su valor ni se escribió a disco. Verificada por presencia (`test -n`) y confirmada por uso: `GET /v1/models` → **HTTP 200**.

**Único destino de red del acto:** `api.anthropic.com`. Excepción declarada, inevitable y ajena a la elicitación: `git fetch` / `git push` contra `github.com`, sin los cuales no hay base contra la que trabajar ni `PR` que entregar. Ninguna consulta a INEGI salvo la sonda de control de `A.2`; **cero descargas de microdato**.

---

## 2 · Arranque — las cinco líneas

**1 · REPO.** Clon **existente**, no se clonó ninguno nuevo: `C:\Users\PC0\Documents\GitHub\Modelado-Mexicano`. La sesión abrió en el home (`C:\Users\PC0`) y **se cambió al clon antes de tocar nada**; el home no es repo (`fatal: not a git repository`, pese a alojar un `.git` inerte). Se descartó un segundo árbol, `C:\Users\PC0\Documents\ChatGPT\Modelado Mexicano`, divergente en `578/1448` commits — no se leyó ni se derivó cifra alguna de él.

**2 · SHA — `main` SE MOVIÓ, y no es `PARO`.** El encargo declara `8b317d3`; verificado vivo (`git cat-file -t` → `commit`) y **ancestro** de la punta. Punta real al arrancar: **`cd6d10c`** (26/ago 13:04), es decir `8b317d3` **+2 commits**: `PR #375` / `1f1ae68`, `ACTO E5-SELLA-FP164-OCTAVA` (`ADR-204`). Es `E5` concurriendo, exactamente donde el encargo anticipó colisión.

Re-derivado en consecuencia, no supuesto: **el máximo `ADR` ya no es `203` sino `204`**.

```
$ grep -o 'ADR-[0-9]\{1,3\}' canon/gobernanza-v1_15.md | sed 's/ADR-//' | sort -n | tail -1
204
```

El perímetro `forense/prereg-duelo-v2/` **no cambió** entre `8b317d3` y `cd6d10c` — los seis pines de §0 se re-derivaron igual (§3). Trabajo sobre rama `acto/e6-l-run` sacada de `origin/main`; `main` local diverge (4 commits de julio, superados aguas arriba) y **no se tocó**.

**3 · `data/raw`.** `ls -d data/raw` → `No such file or directory`. **AUSENTE, no es paro.** Este acto **no la toca y no descarga nada**, así que la trampa de `PR #77` (payloads que se quedan en el worktree y no llegan al corpus compartido) **no aplica**: no hay payload que extraviar.

**4 · ENTORNO.** Ver §1 (firma `A.2` completa).

**5 · ESPEJO.** Ninguna cifra de esta nota sale del espejo del proyecto. Todas salen del clon de (1), con el comando a la vista.

**Suciedad preexistente, declarada y no commiteada:** al llegar, `git status` mostraba 4 archivos modificados **solo en el bit de modo** (`100755→100644`; `git diff --stat` → `0 insertions(+), 0 deletions(-)`) — `forense/rescate/curador-untracked-20260807/tools/curador_registro/{curador.py,run_curador.sh,supervisor.py}` y `tools/registra_enoe_pre2019.sh`. Artefacto de Windows, ajeno a este acto y **fuera de perímetro**: no se corrigió y no entró a ningún commit (todo `git add` de este acto es por ruta explícita, nunca `-a`).

---

## 3 · Compuerta de hashes §0 — **ABIERTA, 6 de 6**, salida cruda

Ejecutado desde `forense/prereg-duelo-v2/`:

```
a772a4bc48b724c33ea82fc41877594fa74b89eb267c2ca74401ed5fe3a45b1d *pipeline-L-adv1-m2.py
14dbf289fc2c66d95e6c8c92a80d459c0dde0a873e740ac5064ed5886a94ebf1 *corredor-B-tasa-base.py
7752ced239fdc6d5a0a6a15921b7ae0c72661740237e6d047f17fe1d6b63767d *corredor-E-combinacion-LM.py
beec0e1c2e86605bb751601a36c312e34ade4a82a8204e0ab96527beba8e0efb *scoring-adv1-m3.py
140b00a80f57e82caa72a15277d77dfef143becf6bbda6da696d325fbf251c11 *sorteo-resultados-v1_0.md
3a0dcf0138493f40777b4f457bbe0a473e6cf830d6d0c7dc265ad8320c3742e2 *marco-congelado-piloto-v1_0.tsv
```

Los seis coinciden carácter por carácter con la tabla de `lanzamiento-L-v1_0.md` §0. El congelado coincide además con `CONGELADO-v1_0.sha256`:

```
$ cat CONGELADO-v1_0.sha256
3a0dcf0138493f40777b4f457bbe0a473e6cf830d6d0c7dc265ad8320c3742e2  marco-congelado-piloto-v1_0.tsv
5fc0b7b616cff132cb27976c5169a8dc9ae4b98a6cd323db509c6738de031487  sorteo-act-pil-3-v2-PROPUESTA.md
```

**Sin discordancia ⇒ `A.7` no aplica, y la regla de enmienda de `prereg-corrida-v1_0.md:110` no se activa** — no se abrió ninguna fila `## F1 · enmienda`.

Verificación extra, del documento que gobierna a este acto: `sha256sum lanzamiento-L-v1_0.md` → `372624171ebef11b7f209fbcb5e4e7c2817f80e4aa147ea225e3804a5e24e4af`, que **coincide con el prefijo `372624171ebef11b…` que el encargo pinea**. El documento ejecutado es el documento declarado.

**Los seis pines siguen intactos al cerrar el acto** — re-verificado después de las 120 llamadas (§8).

---

## 4 · Costura del marco — verificada por comando, no supuesta

Dirección detectó que `cargar_specs_desde_marco` (`pipeline-L-adv1-m2.py:96-118`) lee `forense/marco-candidatas-piloto-v1_0.tsv` (el **original**) mientras el pin de §0 cubre `forense/prereg-duelo-v2/marco-congelado-piloto-v1_0.tsv` (el **congelado** de `ADR-179`, que corrigió `DIN-09`). Este acto lo verifica.

**Resultado: los dos archivos son el mismo, byte a byte.**

```
$ sha256sum forense/marco-candidatas-piloto-v1_0.tsv forense/prereg-duelo-v2/marco-congelado-piloto-v1_0.tsv
3a0dcf0138493f40777b4f457bbe0a473e6cf830d6d0c7dc265ad8320c3742e2 *forense/marco-candidatas-piloto-v1_0.tsv
3a0dcf0138493f40777b4f457bbe0a473e6cf830d6d0c7dc265ad8320c3742e2 *forense/prereg-duelo-v2/marco-congelado-piloto-v1_0.tsv

$ diff forense/marco-candidatas-piloto-v1_0.tsv forense/prereg-duelo-v2/marco-congelado-piloto-v1_0.tsv
(vacío)
```

Diff **fila a fila** por las 15 `id_celda` sorteadas, además del diff de archivo completo:

```
--- encabezados ---
1eca7d3757af75d1e98812104b6461e0 *-
1eca7d3757af75d1e98812104b6461e0 *-
--- diff fila a fila por id_celda sorteada ---
(fin del diff)
FILAS EXAMINADAS (A.13): 15 de 15 ids sorteadas, contra 60 filas de datos en cada marco
DIFERENCIAS: 0
```

**`A.13` — el negativo declara su cobertura:** 15 filas comparadas de 15 sorteadas, sobre 60 filas de datos por archivo, encabezado incluido (mismo `md5`). No es un "no encontré diferencias" sin universo.

`DIN-09` **no está entre las 15**, verificado por comando y no por memoria (`grep -c '^DIN-09$'` sobre la lista sorteada → `0`) — y aun así su fila resultó **idéntica en ambos archivos**, comprobado imprimiéndola entera desde los dos. La costura es **inocua hoy**: leer el marco original devuelve exactamente el congelado. **Sigo, sin elegir marco.**

---

## 5 · Invariantes de la corrida — citados del lanzamiento §1, no recordados

| Parámetro | Valor usado | Fuente |
|---|---|---|
| `modelo_id` | `claude-opus-4-6` | RANURA DE MESA del encargo, valor sellado `F2(a)`; mesa no lo sustituyó |
| `version_declarada` | *(ver §6 — `r.model` de la primera llamada, congelada)* | `lanzamiento` §3 |
| `fecha_congelacion` | `2026-08-26` | `prereg-corrida-v1_0.md` `F2(a)` |
| `temperatura` | `1.0` | `F2(a)` — ver la adaptación declarada de §6 |
| `k_corridas` | `8` | `F2(b)`, punto medio de `[5,10]`; validado por `__post_init__` |
| `variante` | `L-solo` únicamente | **FIRMA DE MESA en sesión** — ver §7 |
| descartes | **CERO** | `F2(d)` |

**La RANURA es válida y se verificó, no se supuso.** `claude-opus-4-6` existe y está disponible para esta clave: aparece en `GET /v1/models` (HTTP 200) junto a `claude-opus-5`, `claude-opus-4-8`, `claude-opus-4-7`, `claude-sonnet-5`, `claude-fable-5`. Se comprobó **antes** de lanzar, precisamente para no descubrir un `model_not_found` a mitad de una corrida pagada.

**Las 15 celdas**, en el orden del sorteo (`sorteo-resultados-v1_0.md`, tabla "Las 15 filas sorteadas"), que es el orden real de ejecución:

`CIV-08, TIC-08, TIC-01, DIN-11, DIN-03, DOC-06, EMP-02, EMP-04, DIN-05, SFT-06, SFT-04, TIC-12, TIC-06, DIN-07, EMP-05`

Las 15 se resolvieron a su `SpecCelda` **por `cargar_specs_desde_marco`**, no a mano: `marco leído: 60 filas; 15/15 ids sorteadas resueltas`.
---

## 6 · El driver — `llamar_modelo`, y la única adaptación que el SDK forzó

`pipeline-L-adv1-m2.py` **no se tocó**. Se comprobó al cerrar, no se dio por hecho: su `sha256` sigue siendo `a772a4bc…3a45b1d` y `git status` sobre los cinco archivos pineados (pipeline, prereg, sorteo, los dos marcos) devuelve **vacío**. El módulo del repo se **importa tal cual** (`importlib.util.spec_from_file_location`, porque el nombre lleva guiones) y se le **monkeypatchea en memoria** el único hueco que su autor dejó — exactamente lo que `lanzamiento` §3 autoriza («copia de trabajo o monkeypatch»). El driver vive **fuera del repo** (`C:\Users\PC0\Documents\_e6-l-run-driver\driver_l_run.py`) porque el perímetro de este encargo no lo admite; por eso va **verbatim aquí**, que es su único sitio legítimo en el árbol.

Se usaron las funciones del pipeline sin reescribir ninguna: `cargar_specs_desde_marco`, `construir_prompt`, `ParametrosCorredorL` y **`correr_celda`** — el bucle de las `k=8` corridas es el del repo (`:189-206`), no una reimplementación.

### 6.1 · Adaptación declarada: `temperature` fuera de la firma del SDK

**No es un cambio de parámetro. El valor sellado `F2(a)` viaja intacto.**

La primera ejecución murió **antes de gastar una sola llamada**:

```
TypeError: Messages.create() got an unexpected keyword argument 'temperature'
```

Causa medida, no supuesta: el SDK instalado (`anthropic 1.1.0`, el oficial —
`pip show` → `anthropic-sdk-python`) **retiró `temperature` de la firma tipada** de `Messages.create()`. Introspección de la firma real: `max_tokens`, `messages`, `model`, `cache_control`, `container`, `inference_geo`, `metadata`, `output_config`, `service_tier`, `stop_sequences`, `stream`, `system`, `thinking`, `tool_choice`, `tools`, `user_profile_id`, `extra_*`, `timeout` — **sin `temperature`, sin `top_p`, sin `top_k`**.

**La API sí lo acepta**, verificado con `curl` crudo contra el único host autorizado:

```
$ curl -s https://api.anthropic.com/v1/messages -H "x-api-key: ***" \
    -H "anthropic-version: 2023-06-01" -H "content-type: application/json" \
    -d '{"model":"claude-opus-4-6","max_tokens":16,"temperature":1.0,...}'
{"model":"claude-opus-4-6", ... "stop_reason":"max_tokens", ...}
HTTP=200
```

Así que el valor sellado se pasa por `extra_body`, que lo inserta verbatim en el cuerpo JSON. **Que `extra_body` llega de verdad al cable no se supuso: se probó con una sonda diseñada para fallar.**

```python
c.messages.create(..., extra_body={'temperature': 999})
→ status: 400
→ 'temperature: range: 0..1'
```

Si `extra_body` se estuviera perdiendo, `999` habría pasado con `200`. La API lo **validó y lo rechazó** ⇒ el parámetro llega y es honrado. `temperatura = 1.0` (tope del rango válido) es lo que corrió.

**Ratificado por mesa en sesión, verbatim:** «`extra_body`: RATIFICADO como adaptación declarada, no cambio de parámetro. Tu sonda de `temperature=999` → 400 prueba que el 1.0 sellado llega al cable.»

### 6.2 · El bloque, tal como corrió

```python
_cliente = anthropic.Anthropic()  # exige ANTHROPIC_API_KEY en el entorno

def llamar_modelo(prompt, params):
    intento = 0
    while True:
        try:
            r = _cliente.messages.create(
                model=params.modelo_id, max_tokens=MAX_TOKENS,   # 1024, §3
                extra_body={"temperature": params.temperatura},  # 1.0 sellada
                messages=[{"role": "user", "content": prompt}],
            )
            texto = "".join(b.text for b in r.content
                            if getattr(b, "type", "") == "text")
            if _estado["version_declarada"] is None:
                _estado["version_declarada"] = r.model      # congelada aquí
            elif r.model != _estado["version_declarada"]:
                _anota_incidencia({"tipo": "deriva_version_declarada", ...})
            ...  # respaldo inmediato de la llamada al ledger crudo
            return texto
        except _TRANSPORTE as exc:        # SOLO transporte reintenta
            intento += 1
            _anota_incidencia({"tipo": "error_transporte", ...})
            if intento >= 5:
                raise
            time.sleep(min(60, 2 ** intento))
        except anthropic.APIStatusError as exc:
            if getattr(exc, "status_code", 0) >= 500:   # 5xx = transporte
                ...
            else:
                raise                                    # 4xx NO se reintenta

pipe.llamar_modelo = llamar_modelo   # el módulo del repo queda intacto en disco
```

Con `_TRANSPORTE = (APIConnectionError, APITimeoutError, InternalServerError, RateLimitError)`.

**Contrato de `pipeline-L-adv1-m2.py:176-181`, punto por punto:**
1. *Fijar `modelo_id`/`version`/`temperatura` exactamente como en `params`* — sí; `version_declarada` se toma de `r.model` de la **primera** llamada y se congela en las 120 capturas, con detector de deriva armado.
2. *No reintentar en caso de rechazo salvo error de transporte* — sí. **Un rechazo de contenido es corrida válida**: se captura como cualquier otra, con su `texto_crudo` íntegro, y **no** se relanza. Solo los errores de transporte reintentan, y cada reintento se anota (llamada, hora, error).
3. *Devolver el texto crudo sin post-proceso* — sí; `texto_crudo` va íntegro a la captura.

**Respaldo anti-pérdida.** Cada llamada se vuelca de inmediato a un *ledger* crudo (`ledger-crudo.jsonl`) fuera del repo, con hora, `r.model` devuelto, `stop_reason`, `sha256` del prompt y texto. Ninguna llamada pagada podía perderse por un fallo posterior del proceso. El driver además **reanuda por celda**: si las 8 capturas de una celda ya existen, la salta — de modo que un `PARO` a mitad no re-cobra lo ya corrido ni duplica un índice.

### 6.3 · Ceguera — verificada, no asumida

`lanzamiento` §2: cada llamada individual **es** la sesión limpia; el modelo solo ve lo que `construir_prompt` arma con los seis campos de `SpecCelda`. Comprobado por lectura del prompt real renderizado (`CIV-08`), buscando las palabras que delatarían fuga del árbol:

```
'arbitr': False   'banda': False   'margen': False   'corpus': False
'prereg': False   'sorteo': False  'ADV1'  : False
```

Prompt de `CIV-08` tal como salió (`sha256_prompt` = `96f2285eae5c7cc5…`), sin una palabra añadida:

```
Estás respondiendo como estimador de una cantidad encuestable en México.
No tienes acceso a ningún documento adjunto de este proyecto de investigación.
Encuesta: ENVIPE (ola 2023).
Universo: población de 18 años y más (TPer_Vic1).
Variable/reactivo: AP4_4_03 (proporción ponderada).
Escala de respuesta: binaria.
Da tu mejor estimación puntual y, si la escala es continua, un intervalo de
confianza subjetivo. Si no conoces el dato, dilo explícitamente -- no
inventes una cifra plausible. Cita la fuente de tu estimación si la tienes
(sonda canario: fuente textual declarada, ver M1).
```

Integridad de codificación comprobada aparte (`U+FFFD` ausente, `repr()` del universo con acentos correctos): lo que se vio mojibake en consola era la *codepage* de Windows, no el dato — el marco se lee con `encoding="utf-8"` dentro de la función del pipeline.
---

## 7 · El hueco `L+corpus` — por qué este acto es PARCIAL

**Hallazgo, no incidente.** Detectado **antes de gastar una sola llamada**, mientras se preparaba el driver.

`ParametrosCorredorL.__post_init__` (`pipeline-L-adv1-m2.py:72-73`) lanza `ValueError` ante cualquier `L+corpus` sin `corpus_id_si_aplica`:

```python
if self.variante == "L+corpus" and not self.corpus_id_si_aplica:
    raise ValueError("L+corpus exige declarar el corpus_id_si_aplica.")
```

y `PLANTILLA_L_CORPUS` (`:140-142`) exige además un `contexto_corpus` **que entra al prompt**:

```
Contexto adicional (corpus tierizado, {corpus_id}): {contexto_corpus}
```

**Ninguno de los dos está definido en punto alguno del árbol.** Barrido con el comando a la vista:

```
$ grep -rn "corpus_id" --include=*.md --include=*.py --include=*.tsv .
forense/prereg-duelo-v2/pipeline-L-adv1-m2.py:66  corpus_id_si_aplica: str | None = None  # hash/ruta del corpus tierizado
forense/prereg-duelo-v2/pipeline-L-adv1-m2.py:72      if self.variante == "L+corpus" and not self.corpus_id_si_aplica:
forense/prereg-duelo-v2/pipeline-L-adv1-m2.py:73          raise ValueError("L+corpus exige declarar el corpus_id_si_aplica.")
forense/prereg-duelo-v2/pipeline-L-adv1-m2.py:74      if self.variante == "L-solo" and self.corpus_id_si_aplica:
forense/prereg-duelo-v2/pipeline-L-adv1-m2.py:142  Contexto adicional (corpus tierizado, {corpus_id}): {contexto_corpus}
forense/prereg-duelo-v2/pipeline-L-adv1-m2.py:154      corpus_id=params.corpus_id_si_aplica, contexto_corpus=contexto_corpus,
```

**`A.13` — cobertura del negativo:** 6 aciertos, **los seis dentro del propio `pipeline-L-adv1-m2.py`**, cero fuera. Universo examinado: el árbol completo del repo bajo `.`, todos los `*.md`, `*.py` y `*.tsv` versionados. No lo fija `lanzamiento-L-v1_0.md` §1 ni §5, no lo fija `prereg-corrida-v1_0.md` `F2`, no lo fija el encargo, y **no estaba ni siquiera abierto en `mesa-pendientes.md`** — cuyas tres secciones (§1 «el falsador no refute», §2 precedencia de las cinco casillas, §3 definición de `⊕`) están las tres **RESUELTAS**. Es un hueco que nadie había visto.

**Por qué el ejecutor no podía taparlo.** `contexto_corpus` no es metadato: es **texto que entra al prompt**. Elegir qué rebanada del corpus acompaña a cada celda es una decisión de diseño con consecuencia directa sobre el resultado, y tomarla habría violado a la vez el `PROHIBIDO` del encargo («meter una palabra al prompt fuera de `construir_prompt`») y la regla rectora de `forense/prereg-duelo-v2/mesa-pendientes.md`:

> «cuando el texto fuente no especifica con claridad una decisión que un acto de escritura necesitaría tomar por su cuenta, el acto documenta las opciones y para — no decide en lugar de mesa»

y el precedente exacto que `canon/glosario-v5_6.md` ya sentó para un caso idéntico: **«Registrar el hueco es el entregable; rellenarlo sería el fallo.»**

**Resolución de mesa, en sesión, verbatim:**

> «FIRMA DE MESA — E6/L-RUN, hueco L+corpus: elijo correr HOY únicamente las 120 llamadas L-solo (comparación principal, FP-162) y AUTORIZO su gasto. L+corpus no se corre en este acto: abre fila nueva en forense/firmas-pendientes.tsv (A.12) que documente el hueco (corpus_id_si_aplica + contexto_corpus sin definir en el árbol) y los tres caminos tal como los tienes escritos, sin elegir ninguno — el contexto del prompt no se improvisa.»

Ejecutado: fila **`FP-165`** (`ABIERTA`), id re-derivado por conteo entero del máximo real del tablero, no tecleado de memoria. Los **tres caminos quedan escritos y ninguno elegido**.

### 7.1 · Consecuencia aguas abajo — declarada para que `E7` no pare en falso

`ADR-141` selló el operador `⊕` como

```
E = mediana_por_cuantil({L-solo, L+corpus, M})
```

— **tres** corredores, no dos, y con una razón explícita en la cabecera de `corredor-E-combinacion-LM.py`: *la mediana solo está bien definida con tres o más componentes*.

Por tanto: **mientras `L+corpus` no exista, el corredor `E` no puede correr.** No es un fallo de `E7`; es la consecuencia mecánica de este hueco. Mesa lo instruyó así, verbatim: «el corredor E (ADR-141) exige los tres corredores, así que E queda bloqueado hasta que mesa selle esa fila o re-selle ⊕ — que E7 no pare en falso por esto.»

**Lo que NO queda bloqueado**, y por eso este acto entrega valor real: `L-solo` está corrida y capturada; es la `comparacion_principal_id` **FIRMADA** (`FP-162`), la única que gatea las cinco casillas de `ADV1-M5` (`prereg-corrida-v1_0.md` `F0.1`/`F2(g)`). El corredor `B`, el árbitro `R` y los hashes `F1` siguen su curso sin esta firma. `L+corpus` era **auxiliar y no-gating** por firma previa de la propia mesa.

### 7.2 · Segundo defecto textual, reportado y NO corregido aquí

`lanzamiento-L-v1_0.md` §5 afirma que `valor_extraido` lo derivan «`agregar_continua`/`agregar_categorica`, **las únicas funciones que lo derivan**». **Es materialmente falso.** Ambas funciones (`pipeline-L-adv1-m2.py:215-243`) reciben `list[float]` / `list[str]` **ya extraídas** y solo **agregan**; ninguna de las dos toca `texto_crudo`. **El pipeline no contiene extractor alguno.** Quien lo dice es el propio pipeline, en la línea que pone el campo en `None`:

```python
valor_extraido=None,  # el parseo real lo hace la sesión ejecutora
                      #   -- pipeline-L-adv1-m2.py:201
```

Es decir: el pipeline **delega** el parseo en la sesión ejecutora. Esta nota reporta la contradicción; **no edita el lanzamiento**, que está fuera del perímetro de este acto. Su corrección textual viaja en la fila sucesora, por instrucción de mesa: «La afirmación falsa de lanzamiento §5 se reporta en nota y ADR — no edites el lanzamiento, está fuera de tu perímetro; su corrección textual viaja en la fila sucesora.»
---

## 8 · La corrida — 120 llamadas, cero descartes

**Orden de ejecución:** por celda del sorteo, `L-solo`, índices `1..8`, estrictamente secuencial. `indice` es «orden de ejecución real» (`pipeline-L-adv1-m2.py:168`), así que no se paralelizó nada: paralelizar habría vaciado de significado ese campo.

```
marco leido: 60 filas; 15/15 ids sorteadas resueltas
[01/15] CIV-08: k=8 ...   ok · 8 capturas · vacias=0 · acumulado=8   · 127s
[02/15] TIC-08: k=8 ...   ok · 8 capturas · vacias=0 · acumulado=16  · 263s
[03/15] TIC-01: k=8 ...   ok · 8 capturas · vacias=0 · acumulado=24  · 376s
[04/15] DIN-11: k=8 ...   ok · 8 capturas · vacias=0 · acumulado=32  · 510s
[05/15] DIN-03: k=8 ...   ok · 8 capturas · vacias=0 · acumulado=40  · 637s
[06/15] DOC-06: k=8 ...   ok · 8 capturas · vacias=0 · acumulado=48  · 777s
[07/15] EMP-02: k=8 ...   ok · 8 capturas · vacias=0 · acumulado=56  · 903s
[08/15] EMP-04: k=8 ...   ok · 8 capturas · vacias=0 · acumulado=64  · 1045s
[09/15] DIN-05: k=8 ...   ok · 8 capturas · vacias=0 · acumulado=72  · 1170s
[10/15] SFT-06: k=8 ...   ok · 8 capturas · vacias=0 · acumulado=80  · 1347s
[11/15] SFT-04: k=8 ...   ok · 8 capturas · vacias=0 · acumulado=88  · 1479s
[12/15] TIC-12: k=8 ...   ok · 8 capturas · vacias=0 · acumulado=96  · 1632s
[13/15] TIC-06: k=8 ...   ok · 8 capturas · vacias=0 · acumulado=104 · 1762s
[14/15] DIN-07: k=8 ...   ok · 8 capturas · vacias=0 · acumulado=112 · 1910s
[15/15] EMP-05: k=8 ...   ok · 8 capturas · vacias=0 · acumulado=120 · 2037s
FIN · llamadas=120 · version_declarada='claude-opus-4-6' · 2037s
```

**Incidencias: NINGUNA.** El archivo de incidencias quedó **vacío**: `0` errores de transporte, `0` reintentos, `0` deriva de `version_declarada` entre llamadas. Ningún índice se saltó ni se duplicó. **No hay nada que anotar en la lista de reintentos porque no hubo ninguno** — se declara explícitamente en vez de omitir la sección.

**Rechazos de contenido: `0` duros.** Ninguna de las 120 respuestas volvió vacía (`texto_crudo` mínimo = `1423` caracteres, mediana `1997`, máximo `2886`). Hubo respuestas que **declaran no tener el dato** — ésas son corridas válidas con texto, se capturan enteras y se cuentan (§10), que es precisamente lo que `F2(d)` exige.

### 8.1 · `version_declarada` — lo que el proveedor devolvió, y su límite

`version_declarada = "claude-opus-4-6"`, tomada de `r.model` de la **primera** llamada y congelada en las 120 capturas. Verificado: el bloque `params` es **idéntico byte a byte en los 120 archivos** (un solo bloque distinto contado sobre los 120).

⚠️ **Límite declarado, porque `ADV1-M2` pide «modelo+versión fijados» y aquí versión no añade información:** el proveedor devuelve el mismo alias que se le pidió (`claude-opus-4-6`), **no** una cadena de *build* fechada del tipo `claude-opus-4-…-20260815` que el comentario de `pipeline-L-adv1-m2.py:60` anticipaba. `version_declarada` queda entonces **tan específica como `modelo_id` y no más**. No se inventó una fecha de *build* para rellenar el hueco — `prereg-corrida-v1_0.md:73` lo prohíbe expresamente («no se inventa una fecha de build que este acto no puede observar»). Lo que se registra es lo observado.

### 8.2 · Verificación de integridad de las capturas

```
archivos: 120
esquema §5 exacto en todos: True | desviaciones: []
texto_crudo vacio (rechazos duros): 0
bloques params DISTINTOS: 1 (debe ser 1 = congelado)
   x120 {"fecha_congelacion": "2026-08-26", "k_corridas": 8, "modelo_id": "claude-opus-4-6",
         "temperatura": 1.0, "variante": "L-solo", "version_declarada": "claude-opus-4-6"}
sha256_prompt distintos: 15 (debe ser 15 = uno por celda)
```

Los 15 `sha256_prompt` distintos confirman lo que importa: **un prompt por celda, idéntico en sus 8 corridas** — la dispersión que se reporta abajo es del modelo, no de un prompt que cambiara entre corridas.

### 8.3 · Los seis pines, re-derivados DESPUÉS de las 120 llamadas

```
a772a4bc48b724c33ea82fc41877594fa74b89eb267c2ca74401ed5fe3a45b1d *pipeline-L-adv1-m2.py
14dbf289fc2c66d95e6c8c92a80d459c0dde0a873e740ac5064ed5886a94ebf1 *corredor-B-tasa-base.py
7752ced239fdc6d5a0a6a15921b7ae0c72661740237e6d047f17fe1d6b63767d *corredor-E-combinacion-LM.py
beec0e1c2e86605bb751601a36c312e34ade4a82a8204e0ab96527beba8e0efb *scoring-adv1-m3.py
140b00a80f57e82caa72a15277d77dfef143becf6bbda6da696d325fbf251c11 *sorteo-resultados-v1_0.md
3a0dcf0138493f40777b4f457bbe0a473e6cf830d6d0c7dc265ad8320c3742e2 *marco-congelado-piloto-v1_0.tsv
```

Idénticos a los de §3. `git status` sobre pipeline, prereg, sorteo, lanzamiento y los dos marcos: **vacío**. El acto corrió 120 llamadas sin mover un byte de lo congelado.

### 8.4 · Conteo `A.13` de cierre — sobre los archivos, no sobre el *ledger*

```
$ ls forense/prereg-duelo-v2/corridas-L | wc -l
120

$ ls forense/prereg-duelo-v2/corridas-L | sed 's/__.*//' | sort -u | wc -l
15                                                    # celdas distintas

$ ls forense/prereg-duelo-v2/corridas-L | sed 's/^[^_]*__//; s/__.*//' | sort -u
L-solo                                                # 1 variante

$ ls forense/prereg-duelo-v2/corridas-L | sed 's/.*__//; s/\.json//' | sort -u | tr '\n' ' '
01 02 03 04 05 06 07 08                               # 8 indices

$ ls forense/prereg-duelo-v2/corridas-L | sed 's/__.*//' | sort | uniq -c
      8 CIV-08     8 DIN-03     8 DIN-05     8 DIN-07     8 DIN-11
      8 DOC-06     8 EMP-02     8 EMP-04     8 EMP-05     8 SFT-04
      8 SFT-06     8 TIC-01     8 TIC-06     8 TIC-08     8 TIC-12
```

**`15 × 1 × 8 = 120`**, verificado por patrón y no por confianza: 8 exactos en cada una de las 15 celdas, ningún índice ausente, ninguno repetido.

El conteo se hace sobre **los 120 archivos de `corridas-L/`**, que son el entregable — **no** sobre el *ledger* crudo del driver, que es respaldo anti-pérdida y fuente de horas/`stop_reason`, y que durante la corrida iba **adelantado** respecto de las capturas (el *ledger* escribe por llamada; las capturas, al cerrar cada celda). Confundir uno con otro habría dado un censo falso a mitad de corrida.

**El total esperado por el encargo original era 240.** Este acto entrega **120** y lo declara en el título, en el resumen y aquí: la mitad `L+corpus` **no se corrió** por la firma de mesa de §7, no por fallo.
---

## 9 · Extractor de `valor_extraido` — CONGELADO ANTES DE APLICARSE

**Este bloque se commitea ANTES de correr el extractor sobre las 120 capturas.** Es la condición que mesa puso al autorizarlo, verbatim: «Congela las reglas del extractor en un commit propio ANTES de aplicarlas sobre las 120 […] y declara ahí el número exacto de capturas que ya habías leído al congelar.»

### 9.1 · Por qué hace falta un extractor, y por qué no estaba pre-registrado

`lanzamiento-L-v1_0.md` §5 dice que `valor_extraido` lo derivan «`agregar_continua`/`agregar_categorica`, las únicas funciones que lo derivan». **Es falso** (§7.2): ambas reciben listas **ya extraídas** y solo agregan; ninguna toca `texto_crudo`. **El pipeline no contiene extractor.** Lo que sí contiene es la delegación explícita, en la línea donde pone el campo en `None`:

```python
valor_extraido=None,  # el parseo real lo hace la sesión ejecutora
                      #   -- pipeline-L-adv1-m2.py:201
```

Este bloque es esa delegación, ejercida de forma mecánica. **La prohibición del encargo que sí rige — «llenar `valor_extraido` a mano» — queda respetada:** ninguna respuesta se lee y se teclea; se aplican reglas fijas de formato, idénticas a las 120, y cada captura registra qué regla disparó.

### 9.2 · LIMITACIÓN, escrita como limitación y no escondida

**Estas reglas se congelan TARDE: después de que las 120 corridas ya existían, no antes.** El pre-registro no las contiene y no hay forma de fingir que sí.

**Capturas ya leídas por el ejecutor al momento de congelar: `2` de `120`.** Ambas de `CIV-08`, variante `L-solo`:

- `CIV-08__L-solo__01.json` — **parcial**, los primeros `1200` caracteres.
- `CIV-08__L-solo__02.json` — **íntegra**.

Ninguna otra captura se leyó antes de fijar estas reglas. Lo demás que el ejecutor vio durante la corrida fueron conteos (`ok · 8 capturas · vacias=0`), horas, `stop_reason` y longitudes — **nunca texto de respuesta**. La cifra `2/120` es exacta, no una estimación.

**Consecuencia honesta:** las reglas se diseñaron habiendo visto el formato de salida de `1.7 %` del material. Eso es más que cero y mucho menos que un extractor ajustado a los datos. Se declara para que quien lea el marcador sepa exactamente qué garantía tiene y cuál no.

**Ninguna cifra se corrige, se descarta ni se ajusta.** Cero descartes rige también aquí: una captura de la que no se extrae valor **no se elimina** — se queda con `valor_extraido: null` y se cuenta como tal.

### 9.3 · Las reglas, verbatim

Reconocedores:

```python
NUM   = r"\d{1,3}(?:[.,]\d{1,2})?"
PCT   = rf"(?<![\d.,])(?:~|≈|aprox\.?\s*)?({NUM})\s*%"
RANGO = rf"(?<![\d.,])({NUM})\s*(?:%\s*)?(?:-|–|—|\s+a\s+|\s+y\s+)\s*({NUM})\s*%"
```

Una «cifra puntual» es un porcentaje que **no** cae dentro del tramo de un rango. `sin_acentos()` normaliza para comparar claves (NFD, se descartan las marcas diacríticas).

**Orden estricto de prioridad. La primera que dispara gana; ninguna posterior se evalúa.**

| Regla | Condición | Valor |
|---|---|---|
| `R0-vacia` | `texto_crudo` vacío o solo espacios | `null` |
| `R1-punto-central` | oración que contiene `punto central`, `mejor punto`, `punto medio` o `mi punto` | primera cifra puntual de esa oración |
| `R2-estimacion-puntual` | oración con `estimacion puntual`, `estimo puntual`, `valor puntual` o `punto estimado` | primera cifra puntual de esa oración |
| `R3-negrita` | primer tramo `**…**` que contenga una cifra puntual | esa cifra |
| `R4-primer-porcentaje` | cualquier cifra puntual del texto | la primera |
| `R5-punto-medio-de-rango` | no hay cifra puntual, pero sí un rango | **punto medio mecánico** `(a+b)/2`, redondeado a 4 decimales |
| `R6-sin-dato-declarado` | no hay cifra alguna y el texto declara explícitamente no tener el dato (12 fórmulas: `no cuento con el dato`, `no tengo el dato`, `no conozco el dato`, `no dispongo del dato`, `no tengo acceso al dato`, `no puedo dar una cifra`, `no puedo ofrecer una cifra`, `no se el dato`, `desconozco el dato`, `no tengo una cifra`, `no tengo datos`, `no cuento con datos`) | `null` |
| `R7-sin-cifra` | ninguna de las anteriores | `null` |

`R5` es la única regla que **deriva** un número en vez de leerlo. Se marca como tal en la traza de cada captura y se cuenta aparte en el resumen, para que nadie confunda un punto medio calculado con un punto declarado por el modelo.

**Sonda canario `fuente_citada`**, mismo esquema de prioridad:

| Regla | Condición | Valor |
|---|---|---|
| `F0-vacia` | texto vacío | `null` |
| `F1-seccion-fuente` | hay encabezado `Fuente`/`Fuentes` (`#`, negrita o `:`) | primera línea no vacía bajo él, recortada a 500 caracteres |
| `F2-linea-fuente` | una línea empieza con `Fuente:`/`Fuentes:` | lo que sigue a los dos puntos, recortado a 500 |
| `F3-publicador-mencionado` | el texto nombra `inegi`, `banxico`, `cnbv`, `conapo`, `coneval` o `imss` sin rotular sección | la primera línea que lo menciona, recortada a 500 |
| `F4-sin-fuente` | ninguna de las anteriores | `null` |

### 9.4 · Elección de agregado — la dicta `escala`, no el ejecutor

`prereg-corrida-v1_0.md` `F2(c)` fija el agregado según el campo `escala` de la `SpecCelda`, y así se aplica, llamando a las funciones del pipeline **sin reescribirlas**:

- `binaria` y `continua (…)` → **`agregar_continua`** → mediana + `q10` + `q90` + IQR (`q75-q25`). **12 celdas.**
- `categorica k=N` → **`agregar_categorica`** → moda + `self_consistency` (moda/n) + distribución completa. **3 celdas** (`TIC-12` k=10, `TIC-06` k=3, `EMP-05` k=8).

**Observación declarada, que no altera la regla:** el `estimador` de esas tres celdas categóricas es, de hecho, una *proporción* (`TIC-06` lo dice literal: «proporcion ponderada (categoria 'Tiene menos de un anio en este trabajo')»). Podría argumentarse que merecen agregado continuo. **No se hace ese cambio:** el pre-registro llavea el agregado a `escala`, y `escala` dice `categorica`. Se aplica lo pre-registrado y se reporta la tensión; resolverla es de mesa, no de este acto.

### 9.5 · Cierre de la congelación

Las reglas de §9.3 y §9.4 quedan fijadas en este commit. No se modificarán después de ver sus resultados: si el conteo por regla resulta feo, se reporta feo.

> **El primer resultado que produzca este procedimiento es el que se reporta.**
---

## 10 · Resultado del extractor y agregado por celda × variante

**Sin comparar contra nada.** Aquí no hay `R`, ni `B`, ni banda, ni marcador. Son las respuestas de `L-solo` y su dispersión interna, que es lo que `ADV1-M2` manda reportar.

### 10.1 · Conteo por regla — las 120 capturas

| Regla | Disparos |
|---|---|
| `R1-punto-central` | **0** |
| `R2-estimacion-puntual` | 13 |
| `R3-negrita` | 28 |
| `R4-primer-porcentaje` | 22 |
| `R5-punto-medio-de-rango` | **40** |
| `R6-sin-dato-declarado` | 15 |
| `R7-sin-cifra` | 2 |
| `R0-vacia` | 0 |

**Totales: 120 capturas · 103 con valor · 17 sin valor · 118 con fuente citada.**

Tres lecturas que el conteo obliga a declarar, y no a suavizar:

1. **`R5` disparó 40 veces — un tercio del material.** Es la única regla que **deriva** un número (punto medio de un rango) en vez de leer uno declarado. Que sea la regla más frecuente significa que **el modelo prefiere responder con rango antes que con punto**, pese a que el prompt pide «tu mejor estimación puntual». No es un defecto del extractor: es un hallazgo sobre el corredor `L`. Un tercio de los valores de `L-solo` son puntos medios calculados por el ejecutor, no estimaciones puntuales del modelo, y quien lea el marcador debe saberlo.
2. **`R1` no disparó nunca.** La regla de máxima prioridad (`punto central`, `mejor punto`) resultó inútil sobre este material. Se deja escrita tal como se congeló, sin retocarla — la promesa era que el primer resultado es el que se reporta.
3. **`R4` disparó 22 veces**, es decir el valor salió del *primer porcentaje del texto* sin más rótulo. Es la regla más débil de las que producen valor y conviene tratarla como tal.

### 10.2 · Agregado pre-registrado por celda

| celda | escala | agregado (`§5` del pipeline, llaveado por `escala`) | val/cap | fuente |
|---|---|---|---|---|
| `CIV-08` | binaria | **`agregar_continua`** — mediana=62.0 · q10=23.5 · q90=68.5 · IQR=37.0 · n=7 | 7/8 | 8/8 |
| `TIC-08` | binaria | **`agregar_continua`** — mediana=32.5 · q10=20.0 · q90=35.0 · IQR=12.5 · n=6 | 6/8 | 8/8 |
| `TIC-01` | binaria | **`agregar_continua`** — mediana=61.0 · q10=24.0 · q90=64.0 · IQR=10.0 · n=8 | 8/8 | 8/8 |
| `DIN-11` | binaria | **`agregar_continua`** — mediana=31.5 · q10=12.0 · q90=33.0 · IQR=18.4 · n=8 | 8/8 | 8/8 |
| `DIN-03` | binaria | **`agregar_continua`** — mediana=34.5 · q10=32.5 · q90=37.5 · IQR=4.5 · n=5 | 5/8 | 8/8 |
| `DOC-06` | continua (porcentaje) | **`agregar_continua`** — mediana=80.0 · q10=12.5 · q90=80.0 · IQR=65.5 · n=8 | 8/8 | 7/8 |
| `EMP-02` | continua (proporcion) | **`agregar_continua`** — mediana=90.0 · q10=17.5 · q90=90.0 · IQR=0.0 · n=8 | 8/8 | 8/8 |
| `EMP-04` | continua (proporcion) | **`agregar_continua`** — mediana=86.0 · q10=80.0 · q90=90.0 · IQR=10.0 · n=8 | 8/8 | 8/8 |
| `DIN-05` | binaria | **`agregar_continua`** — mediana=27.5 · q10=22.5 · q90=37.5 · IQR=2.5 · n=7 | 7/8 | 8/8 |
| `SFT-06` | binaria | **`agregar_continua`** — mediana=34.0 · q10=34.0 · q90=34.0 · IQR=0.0 · **n=2** | **2/8** | 7/8 |
| `SFT-04` | binaria | **`agregar_continua`** — mediana=11.0 · q10=4.0 · q90=26.0 · IQR=9.0 · n=6 | 6/8 | 8/8 |
| `TIC-12` | categorica k=10 | **`agregar_categorica`** — moda=`1.0` · self_consistency=**0.250** · n=8 · distribución={`1.0`:2, `5.0`:1, `40.0`:1, `47.5`:1, `50.0`:1, `55.0`:1, `60.0`:1} | 8/8 | 8/8 |
| `TIC-06` | categorica k=3 | **`agregar_categorica`** — moda=`50.0` · self_consistency=0.500 · n=6 · distribución={`45.0`:1, `47.5`:2, `50.0`:3} | 6/8 | 8/8 |
| `DIN-07` | binaria | **`agregar_continua`** — mediana=26.25 · q10=3.0 · q90=33.5 · IQR=29.0 · n=8 | 8/8 | 8/8 |
| `EMP-05` | categorica k=8 | **`agregar_categorica`** — moda=`25.0` · self_consistency=0.500 · n=8 · distribución={`22.0`:2, `25.0`:4, `47.0`:2} | 8/8 | 8/8 |

### 10.3 · Los valores crudos, por celda, en orden de índice

```
CIV-08: [61.0, 23.5, 30.0, 74.8, 62.0, 68.5, 67.0]          CV = 0.336
TIC-08: [35.0, 35.0, 22.5, 20.0, 35.0, 30.0]                CV = 0.209
TIC-01: [24.0, 64.0, 59.0, 63.0, 53.0, 64.0, 56.5, 63.0]    CV = 0.226
DIN-11: [12.0, 31.0, 35.0, 32.0, 14.0, 32.4, 33.0, 31.0]    CV = 0.308
DIN-03: [37.5, 34.5, 33.0, 32.5, 37.5]                      CV = 0.061
DOC-06: [80.0, 80.0, 80.0, 80.0, 80.0, 14.5, 80.0, 12.5]    CV = 0.454
EMP-02: [90.0, 90.0, 90.0, 90.0, 90.0, 17.5, 90.0, 90.0]    CV = 0.296
EMP-04: [87.0, 90.0, 85.0, 90.0, 80.0, 80.0, 90.0, 80.0]    CV = 0.051
DIN-05: [42.0, 27.5, 22.5, 37.5, 25.0, 27.5, 27.5]          CV = 0.219
SFT-06: [34.0, 34.0]                                        CV = 0.000
SFT-04: [14.0, 26.0, 8.0, 5.0, 4.0, 40.0]                   CV = 0.802
TIC-12: [40.0, 5.0, 47.5, 50.0, 1.0, 55.0, 60.0, 1.0]
TIC-06: [50.0, 47.5, 47.5, 50.0, 45.0, 50.0]
DIN-07: [25.0, 33.5, 20.0, 40.0, 3.0, 32.0, 3.0, 27.5]      CV = 0.557
EMP-05: [25.0, 22.0, 25.0, 25.0, 47.0, 22.0, 47.0, 25.0]
```

⚠️ **El `CV` de arriba es DIAGNÓSTICO y nada más.** Se imprime porque la dispersión es el resultado que `ADV1-M2` exige reportar. **NO se aplica `CV≥30%⇒SKIP`** — `FP-79` vive en `scoring`, jamás en `L` (`lanzamiento` §6). Ninguna celda se marcó, se excluyó ni se trató distinto por su `CV`. Si alguna cae en `SKIP` aguas abajo, caerá allí, con el `CV` del **árbitro**, no con éste.

### 10.4 · Hallazgos propios de esta corrida

**(a) `SFT-06` es el caso extremo de abstención: 6 de 8 corridas declararon no tener el dato.** Su agregado descansa sobre `n=2`, con `IQR=0.0` que parece consenso perfecto y no lo es — es un `n` de dos. **Se reporta con el `n` a la vista precisamente para que nadie lea ese `0.0` como acuerdo.** Cero descartes: las 6 abstenciones están capturadas, con su texto íntegro, y cuentan.

**(b) La dispersión no es ruido menor: en varias celdas cambia el orden de magnitud.** `DOC-06` alterna entre `80.0` (cinco veces) y `~13` (dos veces); `EMP-02` da `90.0` siete veces y `17.5` una; `DIN-07` va de `3.0` a `40.0`. Son bimodalidades, no dispersión gaussiana alrededor de un centro — la mediana las oculta y el `IQR` a veces también (`EMP-02` tiene `IQR=0.0` **con** un valor a `17.5`). El `q10`/`q90` es lo que las delata, y por eso el pre-registro pide los cuatro cuantiles y no solo la mediana.

**(c) `CIV-08` — el hallazgo que mesa pidió dejar escrito.** Dos corridas del mismo prompt leyeron `AP4_4_03` como **reactivos distintos**: la corrida 1 lo interpretó como percepción de inseguridad en el mercado (~67–73 %) y la corrida 2 como *«dejó de usar joyas»* (~23.5 %). No es que el modelo dude del valor: **duda de qué pregunta le están haciendo**, y responde con seguridad a preguntas diferentes. La dispersión resultante (`IQR=37.0`, `q10=23.5`, `q90=68.5`) no mide incertidumbre sobre una cantidad — mide desacuerdo sobre cuál cantidad es. Mesa lo ordenó capturar sin tocar nada, verbatim: «Que dos corridas lean AP4_4_03 como constructos distintos es exactamente lo que ADV1-M2 existe para exhibir.» Nada se re-preguntó y nada se tocó del prompt.

**(d) La sonda canario casi siempre dispara: 118 de 120 citan fuente.** Y la fuente citada es casi siempre INEGI o el publicador correcto. Conviene no leer eso como señal de acierto: **citar la fuente correcta y acertar la cifra son cosas distintas**, y varias de las respuestas que citan INEGI correctamente son las mismas que traen los valores extremos de la bimodalidad de (b). Este acto no puede decir cuál de las dos ramas está bien — eso lo dirá `R`, y `R` no ha corrido.

**(e) El modelo prefiere rangos a puntos** (§10.1, `R5` = 40/120), pese a que el prompt pide explícitamente estimación puntual. Es una observación sobre la elicitación misma, no sobre las cifras.

### 10.5 · Tensión declarada en las tres celdas categóricas

`TIC-12`, `TIC-06` y `EMP-05` tienen `escala = categorica k=N`, así que el pre-registro llavea su agregado a `agregar_categorica` — y así se aplicó. Pero su `estimador` es una **proporción**, y lo que el modelo devuelve son números. Consecuencia visible en la tabla: la «moda» de `TIC-12` es la cadena `'1.0'` con `self_consistency = 0.250`, que es un artefacto de tratar porcentajes como etiquetas de categoría, no una moda categórica en sentido útil.

**No se cambió la regla.** El pre-registro dice `escala`, y `escala` dice `categorica`. Se aplica lo pre-registrado, se reporta el artefacto, y **la resolución es de mesa** — encaja en la fila sucesora junto con las otras dos correcciones textuales del lanzamiento.
---

## 11 · FIRMA DE MESA definitiva sobre el hueco `L+corpus` — `FP-165` abierta y cerrada FIRMADA en el mismo acto

En §7 este acto **abrió** el hueco y **paró** ante él, sin elegir. Mesa cierra ahora la disyuntiva. La firma llegó en sesión, y va aquí **verbatim**:

> **FIRMO: el programa no hará más llamadas API; `L+corpus` NO se ejecutará. Abre la fila sucesora y ciérrala FIRMADA en el mismo acto con esta decisión — los tres caminos documentados, elegido: no-ejecución. Consecuencia declarada: el corredor `E` (`ADR-141`) queda inejecutable tal como está sellado; en `E7` la columna `E` se reporta inejecutable citando esta fila, y re-sellar `⊕` queda como opción futura de mesa, no ejercida hoy.**

### 11.1 · Qué se eligió, y qué NO — contra los tres caminos tal como se escribieron

Los tres caminos quedan en `FP-165` **tal como se le presentaron a mesa**, sin una sola edición retroactiva. Contra ellos, la elección se lee así:

| Camino, verbatim de la fila | Elegido | Qué significa hoy |
|---|---|---|
| **(a)** PARO de `L+corpus` — corre solo `L-solo`, y `L+corpus` queda para un acto sucesor una vez que mesa selle los dos campos | **SÍ, en su forma TERMINAL** | Corre `L-solo` (120 capturas, entregadas). `L+corpus` no corre — y **sin el acto sucesor que (a) preveía**: mesa cierra la puerta a nuevas llamadas API del programa |
| **(b)** mesa sella `corpus_id_si_aplica` y `contexto_corpus`, y un acto sucesor corre las 120 faltantes | **NO** | Los dos campos siguen **SIN DEFINIR** en el árbol. El hueco no se tapa: se declara permanente |
| **(c)** mesa re-sella el operador `⊕` de `ADR-141` para que `E` se defina sobre los corredores que SÍ existen | **NO — opción futura, no ejercida hoy** | `ADR-141` y `corredor-E-combinacion-LM.py` **no se tocan**. Queda disponible para un acto propio de mesa, que este no es |

**La elección es «no-ejecución», y por eso no se la rotula «(a)» a secas.** (a) contemplaba un acto sucesor; esta firma lo cancela. Registrarla como (a) habría dejado en el tablero una promesa de corrida que mesa acaba de retirar.

**Contexto declarado del cierre, porque cambia lo que el lector puede esperar:** la clave de API quedó **revocada** y esta sesión de cierre corre por suscripción, con **cero llamadas API**. No es que `L+corpus` esté aplazada por falta de tiempo: está **cancelada**, y la fila lo dice con esas palabras.

### 11.2 · La fila, abierta y cerrada en el mismo commit

`FP-165` entra a `forense/firmas-pendientes.tsv` ya `FIRMADA`, con `firmada_en` = la firma verbatim de arriba y `ejecutada_en` = `ADR-206`. **El tablero pasa de `0` `ABIERTA` a `0` `ABIERTA`** — la fila no se queda abierta ni un commit, que es exactamente lo que la firma mandó («ábrela y ciérrala FIRMADA en el mismo acto»).

El id se re-derivó **por conteo entero** de la columna 1 contra el árbol ya fusionado, no tecleado de memoria:

```
max FP: 164 · filas: 160 · huecos historicos: [137, 138, 139, 140]
→ fila nueva: FP-165   (sin colision tras fusionar origin/main)
```

### 11.3 · Consecuencia aguas abajo, escrita para que `E7` no pare en falso

`ADR-141` selló `⊕` sobre **tres** corredores:

```
E = mediana_por_cuantil({L-solo, L+corpus, M})
```

con la razón explícita en la cabecera de `corredor-E-combinacion-LM.py`: *la mediana solo está bien definida con tres o más componentes*. Con `L+corpus` cancelada, **el corredor `E` queda INEJECUTABLE tal como está sellado**. Ya no es un bloqueo temporal a la espera de una firma — es un estado terminal mientras `⊕` no se re-selle.

**Instrucción de mesa para `E7`, literal:** la columna `E` **se reporta INEJECUTABLE citando esta fila**. Eso es **reporte, no `PARO`**: `E7` corre, y donde iría `E` escribe la razón y la cita a `FP-165` / `ADR-206`.

**Lo que NO queda tocado**, y por eso este acto entrega valor real: `L-solo` está corrida y capturada, y es la `comparacion_principal_id` **FIRMADA** (`FP-162`), la única que gatea las cinco casillas de `ADV1-M5` (`prereg-corrida-v1_0.md` `F0.1`/`F2(g)`). El corredor `B`, el árbitro `R` y los hashes `F1` siguen su curso. `L+corpus` era **auxiliar y no-gating** por firma previa de la propia mesa.

**Lo que este acto NO hace, y conviene decirlo porque la tentación era grande:** no re-sella `⊕`, no edita `corredor-E-combinacion-LM.py`, no toca `ADR-141`, no toca el pre-registro ni el lanzamiento, y no inventa una definición de `E` sobre dos corredores. Re-sellar `⊕` es acto de mesa, y mesa dijo expresamente que hoy **no** lo ejerce.

### 11.4 · Las dos correcciones textuales que quedaban «para la fila sucesora»

§7.2 y §10.5 reportaron dos defectos del texto gobernante y los mandaron «a la fila sucesora»: (i) `lanzamiento-L-v1_0.md` §5 afirma en falso que `agregar_continua`/`agregar_categorica` derivan `valor_extraido`; (ii) las tres celdas `categorica k=N` cuyo `estimador` es en realidad una proporción. **Ninguna de las dos se corrige aquí**, y ahora hace falta decir dónde quedan: `FP-165` cierra sobre la **no-ejecución de `L+corpus`**, que es lo que mesa firmó, y **no** absorbe esas dos correcciones. Quedan **reportadas en esta nota y en `ADR-206`, sin fila propia**, porque abrir filas que mesa no pidió sería decidir en su lugar. Están escritas, fechadas y citables; el día que mesa quiera corregir el texto del lanzamiento, el hallazgo ya está levantado.

---

## 12 · Cierre del acto — conteo `A.13`, pines, suite, perímetro

### 12.1 · Conteo `A.13` de cierre, re-ejecutado sobre los 120 archivos ya commiteados

No se copió de §8.4: se volvió a correr al cerrar, después de fusionar `origin/main`.

```
$ ls forense/prereg-duelo-v2/corridas-L | wc -l
120

$ ls forense/prereg-duelo-v2/corridas-L | sed 's/__.*//' | sort -u | wc -l
15                                                    # celdas distintas

$ ls forense/prereg-duelo-v2/corridas-L | sed 's/^[^_]*__//; s/__.*//' | sort -u
L-solo                                                # 1 variante

$ ls forense/prereg-duelo-v2/corridas-L | sed 's/.*__//; s/\.json//' | sort -u | tr '\n' ' '
01 02 03 04 05 06 07 08                               # 8 indices

$ ls forense/prereg-duelo-v2/corridas-L | sed 's/__.*//' | sort | uniq -c
      8 CIV-08     8 DIN-03     8 DIN-05     8 DIN-07     8 DIN-11
      8 DOC-06     8 EMP-02     8 EMP-04     8 EMP-05     8 SFT-04
      8 SFT-06     8 TIC-01     8 TIC-06     8 TIC-08     8 TIC-12

$ git status --short forense/prereg-duelo-v2/corridas-L
(vacio — las 120 estan commiteadas, ninguna modificada ni sin rastrear)
```

**`15 × 1 × 8 = 120`**, verificado por patrón: 8 exactos en cada una de las 15 celdas, ningún índice ausente, ninguno repetido. **Universo examinado: los 120 archivos de `corridas-L/`, que son el entregable** — no el *ledger* crudo del driver, que es respaldo y quedó también en 120 líneas. **El total del encargo original era 240; este acto entrega 120** y lo declara aquí, en el título y en §7: la mitad `L+corpus` no se corrió y ya no se correrá (§11).

Integridad de los campos poblados en `COMMIT-B`, re-verificada al cerrar:

```
archivos: 120 | con valor: 103 | sin valor: 17 | con fuente: 118
sha256_prompt distintos: 15   (debe ser 15 = uno por celda)
bloques params distintos: 1   (debe ser 1  = congelado)
```

### 12.2 · Los seis pines, re-derivados por TERCERA vez — después de las 120 llamadas y después del merge

```
a772a4bc48b724c33ea82fc41877594fa74b89eb267c2ca74401ed5fe3a45b1d *pipeline-L-adv1-m2.py
14dbf289fc2c66d95e6c8c92a80d459c0dde0a873e740ac5064ed5886a94ebf1 *corredor-B-tasa-base.py
7752ced239fdc6d5a0a6a15921b7ae0c72661740237e6d047f17fe1d6b63767d *corredor-E-combinacion-LM.py
beec0e1c2e86605bb751601a36c312e34ade4a82a8204e0ab96527beba8e0efb *scoring-adv1-m3.py
140b00a80f57e82caa72a15277d77dfef143becf6bbda6da696d325fbf251c11 *sorteo-resultados-v1_0.md
3a0dcf0138493f40777b4f457bbe0a473e6cf830d6d0c7dc265ad8320c3742e2 *marco-congelado-piloto-v1_0.tsv
```

Idénticos a §3 y a §8.3. `git status` sobre pipeline, prereg, sorteo, lanzamiento, los dos marcos y `corredor-E-combinacion-LM.py`: **vacío**. Ni el merge ni el cierre movieron un byte de lo congelado.

### 12.3 · Precisión sobre las incidencias — el archivo no quedó vacío: nunca llegó a crearse

§8 dijo «el archivo de incidencias quedó **vacío**». Al cerrar se comprueba y se corrige la palabra: `incidencias.jsonl` **no existe** — el driver solo lo abre al anotar la primera incidencia, y nunca hubo ninguna. `0` errores de transporte, `0` reintentos, `0` deriva de `version_declarada`. La conclusión no cambia; la evidencia es más fuerte que la que se escribió.

### 12.4 · `main` se movió por SEGUNDA vez en el acto — y el `ADR` se renumeró, como estaba anunciado

Al arrancar, `main` estaba en `cd6d10c` (§2). Al cerrar, `origin/main` está en **`102742b`** (`PR #376`, `ACTO CORRE-R10.1-v2` Fase B), que trae **`ADR-205`** y mueve el Hito D de `24` a `25` de `27`. El encargo y la firma de mesa anticiparon exactamente esto: «candidatea `205`, **renumera si colisiona**».

Colisionó. Fusionado `origin/main` en `acto/e6-l-run` (merge limpio, sin conflictos), el máximo se re-derivó **por conteo entero contra el árbol ya fusionado**, nunca a mano ni por `sort -t- -k2 -n` (que parte en el primer guion y devuelve un máximo falso):

```
re.findall(r'ADR-(\d+)') sobre canon/gobernanza-v1_15.md
max ADR: 205 · huecos: []      # y grep -c de bloques '^**ADR-' → 205: maximo == conteo
→ este acto toma ADR-206
```

**Regla de la casa aplicada, la misma de `ADR-199`…`ADR-205`:** quien fusiona primero se queda con el número; quien fusiona segundo renumera al resolver el merge y **conserva íntegra la contribución ajena** — el bloque de `ADR-205` y todo `PR #376` quedan **sin tocar**.

### 12.5 · Suite — `tests/check.py --baseline`, y la adaptación de medición que Windows obligó a declarar

**Resultado: `**20 FAIL · 127 WARN**`. Línea base: `ROJO` con UNA entrada nueva, y esa entrada NO es de este acto.**

```
LÍNEA BASE: ROJO — 1 entradas nuevas frente a tests/baseline.json (HEAD congelado e24d033…)
  · T02: nombre normalizado colisiona: data/curacion-registro/baseline.json · tests/baseline.json
```

**Que esa entrada es heredada no se afirma: se midió.** Se creó un *worktree* limpio de `origin/main` (`102742b`, sin una sola línea de este acto) y se corrió ahí la misma suite:

```
$ git worktree add <tmp>/wt-originmain origin/main
$ cd <tmp>/wt-originmain && python tests/check.py --baseline
  20 FAIL · 127 WARN
  LÍNEA BASE: ROJO — 1 entradas nuevas … · T02: … data/curacion-registro/baseline.json · tests/baseline.json
```

Misma cifra, misma única entrada. **La rama de este acto deja la suite exactamente donde la encontró: cero entradas nuevas atribuibles a `E6`.** La colisión `T02` es deuda del corpus, fuera del perímetro de este encargo, y **no se toca** — corregirla exigiría renombrar un archivo de `data/` o `tests/baseline.json`, ninguno de este acto.

**Las cuatro entradas que este acto SÍ introdujo se corrigieron antes de commitear**, y así se midieron:

| Entrada nueva | Causa | Corrección |
|---|---|---|
| `T22` × 2 — encargo y nota «traen marcador de ranura/pendiente-de-mesa que ninguna fila cita» | ambos textos traen la RANURA DE MESA y la firma | `FP-165` los cita **por nombre** en su columna `dónde`, que es el mecanismo que el propio test pide («añade la fila, `A.12`») |
| `T25` × 2 — rótulo pelado `E6` | dirección rotuló este encargo `E6`, y el encargo se archiva **verbatim** (`A.3`) | `E6` censado en `canon/registro-rotulos.tsv` como HABITANTE adicional del espacio `E`, con su colisión declarada; los dos archivos entran a `_T25_ARCHIVOS_CONOCIDOS`. **Extensión mínima de perímetro por desviación mecánica del CI del propio acto**, mismo precedente exacto que `E4` (`ADR-202`) y `E5` (`ADR-204`). El texto de dirección no se edita para complacer a un test |

⚠️ **Adaptación de MEDICIÓN, declarada — no toca el corpus ni un solo archivo del repo.** La suite se corrió en la caja Windows/Git Bash designada por mesa, y ahí `tests/check.py` da un falso rojo masivo por dos causas **medidas**, no supuestas:

1. **Separador de rutas.** `rel()` (`tests/check.py:31-32`) usa `os.path.relpath`, que en Windows devuelve `\`; las listas blancas `_T22_ARCHIVOS_CONOCIDOS` / `_T25_ARCHIVOS_CONOCIDOS` y **todo `tests/baseline.json`** están escritos con `/` (autoría Linux). Efecto medido: **+53 `FAIL` de `T22` y +183 de `T25`**, todos por separador, ninguno por contenido.
2. **Codepage de la consola.** `_suite_real()` lanza la suite en subproceso con `text=True`, que en Windows decodifica con `cp1252`; la salida es UTF-8 (`═`, `·`) ⇒ `UnicodeDecodeError` en el hilo lector ⇒ `r.stdout is None` ⇒ `T16` revienta con `TypeError` antes de comparar nada.

Se corrigen **desde fuera**, sin editar `tests/check.py` por esto: `PYTHONUTF8=1` (modo UTF-8 para padre e hijo) y un `sitecustomize.py` en el `PYTHONPATH`, **fuera del repo**, que normaliza **solo el separador** que devuelve `os.path.relpath` — la única llamada que `check.py` le hace (`grep -n relpath tests/check.py` → 1 acierto, línea 32).

```python
# sitecustomize.py, fuera del repo. Normaliza el separador y nada mas.
import os, os.path
_orig = os.path.relpath
def relpath(path, start=os.curdir):
    return _orig(path, start).replace(os.sep, "/")
os.path.relpath = relpath
```

Que la adaptación **mide** el corpus y no lo maquilla queda probado por el control del *worktree* limpio: con el mismo `sitecustomize`, `origin/main` da la misma cifra y la misma única entrada nueva. **No se corrió `--freeze` en ningún momento**; la línea base congelada no se movió.

### 12.6 · Perímetro real del acto, contra el declarado

| Archivo | Autorizado por | Tocado |
|---|---|---|
| `forense/prereg-duelo-v2/corridas-L/**` (120 nuevos) | encargo, lista original | sí |
| `forense/notas/2026-08-26-l-run-cierre.md` | encargo, lista original | sí |
| `forense/encargos/2026-08-26-E6-L-RUN.md` | `A.3` | sí |
| `canon/gobernanza-v1_15.md` | encargo, lista original | sí (`ADR-206` + cabecera de conteo) |
| `canon/estado-programa-v1_10.md` | encargo, lista original | sí (recifrado `§L0`) |
| `forense/firmas-pendientes.tsv` | **FIRMA DE MESA** que amplió el perímetro en un archivo | sí (`FP-165`) |
| `canon/registro-rotulos.tsv` · `tests/check.py` (solo la lista blanca de `T25`) | **extensión mínima por desviación mecánica del CI**, precedente `E4`/`E5`, declarada aquí | sí |

**Fuera del perímetro y NO tocado:** `pipeline-L-adv1-m2.py`, `prereg-corrida-v1_0.md`, `lanzamiento-L-v1_0.md`, `sorteo-resultados-v1_0.md`, los dos marcos, `corredor-B-tasa-base.py`, `corredor-E-combinacion-LM.py`, `scoring-adv1-m3.py`, `milpa/**`, `canon/modelo-decision-v4_0.md`, `data/**`. **La suciedad preexistente de §2** (4 archivos con solo el bit de modo cambiado) sigue sin corregir y **no entró a ningún commit**: todo `git add` de este acto fue por ruta explícita, nunca `-a`.

### 12.7 · Las partes de la nota — una sola nota, nada suelto

La nota se redactó en seis partes dentro del directorio del driver, **fuera del repo**. Están **ensambladas en este único archivo**, verificado por comparación byte a byte (`diff` vacío entre la concatenación de las seis y el archivo commiteado). **Ninguna parte se commitea suelta**, ni el directorio del driver entra al repo: lo que de él tiene valor probatorio va **verbatim** en §13.

---

## 13 · Apéndice — el driver y el extractor, verbatim

§6 prometió que el driver iría verbatim en la nota, «porque es su único sitio legítimo en el árbol»; §6.2 mostró solo su bloque central, con elisiones. Aquí va **completo**, y con él el extractor cuyas reglas §9 congeló. Ambos viven en `C:\Users\PC0\Documents\_e6-l-run-driver\`, fuera del repo, y **no se commitean como archivos**: el perímetro del encargo no los admite. Se pegan para que la corrida sea auditable sin ellos.

Los otros archivos del directorio del driver, declarados y **no pegados** porque no produjeron ni una línea de lo commiteado: `preflight.py` (sonda de entorno y de `GET /v1/models`, previa a la primera llamada), `resumen.py` (imprime los conteos por regla y el agregado de §10 a partir de las capturas ya escritas), `abre_fp165.py` (redactó la fila `FP-165` en su forma `ABIERTA`), `ledger-crudo.jsonl` (respaldo anti-pérdida, 120 líneas), `trazas-extraccion.json` (qué regla disparó en cada captura) y `version_declarada.txt` (`claude-opus-4-6`).

### 13.1 · `driver_l_run.py`, íntegro

```python
#!/usr/bin/env python3
"""
E6 · L-RUN — driver del corredor L, duelo ADV1-M2.

Vive FUERA del repo a proposito: el perimetro del encargo E6 no admite este
archivo, y el lanzamiento-L §3 autoriza expresamente "copia de trabajo o
monkeypatch". `pipeline-L-adv1-m2.py` del repo se IMPORTA TAL CUAL y no se
edita: se le monkeypatchea el unico hueco que su autor dejo, `llamar_modelo`.

Alcance de esta corrida, por FIRMA DE MESA del 26/ago/2026:
    15 celdas x 1 variante (L-solo) x k=8 = 120 llamadas.
    L+corpus NO se corre (hueco de pre-registro: corpus_id_si_aplica y
    contexto_corpus sin definir en el arbol). Fila sucesora en
    forense/firmas-pendientes.tsv.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

# --------------------------------------------------------------------------
# Rutas. El repo se pasa por argv[1]; nada se adivina.
# --------------------------------------------------------------------------
REPO = Path(sys.argv[1]).resolve()
PIPELINE = REPO / "forense" / "prereg-duelo-v2" / "pipeline-L-adv1-m2.py"
MARCO = REPO / "forense" / "marco-candidatas-piloto-v1_0.tsv"
SALIDA = REPO / "forense" / "prereg-duelo-v2" / "corridas-L"
AQUI = Path(__file__).resolve().parent
LEDGER = AQUI / "ledger-crudo.jsonl"       # respaldo inmediato de cada llamada
INCIDENCIAS = AQUI / "incidencias.jsonl"   # errores de transporte y reintentos

# --------------------------------------------------------------------------
# Invariantes citados, no recordados. Cualquier cambio aqui es violacion de
# la RANURA DE MESA / lanzamiento §1.
# --------------------------------------------------------------------------
MODELO_ID = "claude-opus-4-6"
TEMPERATURA = 1.0
K_CORRIDAS = 8
FECHA_CONGELACION = "2026-08-26"
VARIANTE = "L-solo"
MAX_TOKENS = 1024

# Las 15 celdas, copiadas literal de sorteo-resultados-v1_0.md, en el orden
# del sorteo (el encargo manda: "orden: por celda del sorteo").
CELDAS = [
    "CIV-08", "TIC-08", "TIC-01", "DIN-11", "DIN-03",
    "DOC-06", "EMP-02", "EMP-04", "DIN-05", "SFT-06",
    "SFT-04", "TIC-12", "TIC-06", "DIN-07", "EMP-05",
]

# --------------------------------------------------------------------------
# Import del pipeline del repo, SIN TOCARLO. El nombre lleva guiones, asi que
# no es importable por `import`; se carga por spec.
# --------------------------------------------------------------------------
_spec = importlib.util.spec_from_file_location("pipeline_L_adv1_m2", PIPELINE)
pipe = importlib.util.module_from_spec(_spec)
sys.modules["pipeline_L_adv1_m2"] = pipe  # dataclasses lo exige antes de exec
_spec.loader.exec_module(pipe)

# --------------------------------------------------------------------------
# El bloque del lanzamiento §3, pegado tal cual, mas SOLO lo que el propio
# lanzamiento manda anadir: capturar r.model y congelarlo.
# --------------------------------------------------------------------------
import anthropic  # noqa: E402

_cliente = anthropic.Anthropic()  # exige ANTHROPIC_API_KEY en el entorno

# Estado de sesion: version_declarada se fija en la PRIMERA llamada y se congela.
_estado = {"version_declarada": None, "n_llamadas": 0}

# Errores que SI son de transporte -> unico caso en que se reintenta.
_TRANSPORTE = (
    anthropic.APIConnectionError,
    anthropic.APITimeoutError,
    anthropic.InternalServerError,
    anthropic.RateLimitError,
)


def _anota_incidencia(payload: dict) -> None:
    with INCIDENCIAS.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False) + "\n")


def llamar_modelo(prompt, params):
    """Implementacion real. Contrato verbatim del docstring que reemplaza
    (pipeline-L-adv1-m2.py:176-181): (1) fija modelo_id/version/temperatura
    exactamente como en params, (2) NO reintenta salvo error de transporte,
    (3) devuelve el texto crudo sin post-proceso."""
    intento = 0
    while True:
        try:
            r = _cliente.messages.create(
                model=params.modelo_id, max_tokens=MAX_TOKENS,
                # ADAPTACION DECLARADA, no cambio de parametro: el SDK
                # anthropic 1.1.0 retiro `temperature` de la firma tipada de
                # Messages.create (TypeError: unexpected keyword argument).
                # La API SI lo acepta para claude-opus-4-6 -- verificado por
                # curl crudo (HTTP 200) y probado por sonda extra_body con
                # temperature=999 -> 400 "temperature: range: 0..1", lo que
                # demuestra que extra_body llega al cable y es validado.
                # El valor sellado F2(a) viaja intacto: 1.0.
                extra_body={"temperature": params.temperatura},
                messages=[{"role": "user", "content": prompt}],
            )
            # sin reintentos salvo error de transporte; un rechazo de contenido
            # ES corrida valida
            texto = "".join(
                b.text for b in r.content if getattr(b, "type", "") == "text"
            )
            # version_declarada: r.model de la PRIMERA llamada, congelada.
            if _estado["version_declarada"] is None:
                _estado["version_declarada"] = r.model
            elif r.model != _estado["version_declarada"]:
                _anota_incidencia({
                    "tipo": "deriva_version_declarada",
                    "hora": datetime.now(timezone.utc).isoformat(),
                    "congelada": _estado["version_declarada"],
                    "devuelta_ahora": r.model,
                })
            _estado["n_llamadas"] += 1
            # respaldo inmediato: ninguna llamada pagada se pierde por un
            # fallo posterior del proceso
            with LEDGER.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps({
                    "n": _estado["n_llamadas"],
                    "hora": datetime.now(timezone.utc).isoformat(),
                    "model_devuelto": r.model,
                    "stop_reason": getattr(r, "stop_reason", None),
                    "sha256_prompt": hashlib.sha256(
                        prompt.encode("utf-8")).hexdigest(),
                    "texto_crudo": texto,
                }, ensure_ascii=False) + "\n")
            return texto
        except _TRANSPORTE as exc:
            intento += 1
            _anota_incidencia({
                "tipo": "error_transporte",
                "hora": datetime.now(timezone.utc).isoformat(),
                "intento": intento,
                "clase": type(exc).__name__,
                "error": str(exc)[:500],
            })
            if intento >= 5:
                raise
            time.sleep(min(60, 2 ** intento))
        except anthropic.APIStatusError as exc:
            # 5xx no cubierto arriba -> transporte; 4xx -> NO se reintenta
            if getattr(exc, "status_code", 0) >= 500:
                intento += 1
                _anota_incidencia({
                    "tipo": "error_transporte_5xx",
                    "hora": datetime.now(timezone.utc).isoformat(),
                    "intento": intento,
                    "status": exc.status_code,
                    "error": str(exc)[:500],
                })
                if intento >= 5:
                    raise
                time.sleep(min(60, 2 ** intento))
            else:
                raise


# EL monkeypatch. El modulo del repo queda intacto en disco.
pipe.llamar_modelo = llamar_modelo


def main() -> int:
    SALIDA.mkdir(parents=True, exist_ok=True)

    # specs desde el marco, por la funcion del pipeline -- no se reconstruye
    # a mano ninguna spec (lanzamiento §1).
    todas = pipe.cargar_specs_desde_marco(MARCO)
    por_id = {s.id: s for s in todas}
    faltan = [c for c in CELDAS if c not in por_id]
    if faltan:
        print(f"PARO: ids sorteadas ausentes del marco: {faltan}")
        return 2
    print(f"marco leido: {len(todas)} filas; 15/15 ids sorteadas resueltas")

    # params para la PRIMERA llamada. version_declarada aun no es observable
    # (el lanzamiento lo dice explicito: se toma de r.model al correr), asi que
    # arranca con un centinela y se recongela en cuanto el proveedor responde.
    # llamar_modelo solo consume modelo_id y temperatura -> el centinela no
    # entra a ninguna llamada.
    params_semilla = pipe.ParametrosCorredorL(
        modelo_id=MODELO_ID,
        version_declarada="PENDIENTE-r.model-primera-llamada",
        fecha_congelacion=FECHA_CONGELACION,
        temperatura=TEMPERATURA,
        k_corridas=K_CORRIDAS,
        variante=VARIANTE,
    )

    t0 = time.time()
    for n_celda, id_celda in enumerate(CELDAS, start=1):
        spec = por_id[id_celda]
        rutas = [
            SALIDA / f"{id_celda}__{VARIANTE}__{i:02d}.json"
            for i in range(1, K_CORRIDAS + 1)
        ]
        if all(p.exists() for p in rutas):
            print(f"[{n_celda:02d}/15] {id_celda}: ya completa, se salta")
            continue

        prompt = pipe.construir_prompt(spec, params_semilla)
        sha_prompt = hashlib.sha256(prompt.encode("utf-8")).hexdigest()

        print(f"[{n_celda:02d}/15] {id_celda}: k={K_CORRIDAS} ...", flush=True)
        try:
            corridas = pipe.correr_celda(spec, params_semilla)
        except Exception:
            print(f"PARO en {id_celda}:\n{traceback.format_exc()}")
            return 3

        version = _estado["version_declarada"]
        for r, ruta in zip(corridas, rutas):
            captura = {
                "id_celda": id_celda,
                "variante": VARIANTE,
                "indice": r.indice,
                "texto_crudo": r.texto_crudo,
                "valor_extraido": None,
                "fuente_citada": None,
                "timestamp": r.timestamp,
                "params": {
                    "modelo_id": MODELO_ID,
                    "version_declarada": version,
                    "fecha_congelacion": FECHA_CONGELACION,
                    "temperatura": TEMPERATURA,
                    "k_corridas": K_CORRIDAS,
                    "variante": VARIANTE,
                },
                "sha256_prompt": sha_prompt,
            }
            ruta.write_text(
                json.dumps(captura, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        n_vacias = sum(1 for r in corridas if not r.texto_crudo.strip())
        print(f"    ok · {len(corridas)} capturas · vacias={n_vacias} "
              f"· acumulado={_estado['n_llamadas']} "
              f"· {time.time()-t0:.0f}s", flush=True)

    print(f"FIN · llamadas={_estado['n_llamadas']} "
          f"· version_declarada={_estado['version_declarada']!r} "
          f"· {time.time()-t0:.0f}s")
    (AQUI / "version_declarada.txt").write_text(
        str(_estado["version_declarada"]), encoding="utf-8")
    return 0


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("PARO: ANTHROPIC_API_KEY ausente del entorno.")
        raise SystemExit(2)
    raise SystemExit(main())
```

### 13.2 · `extractor.py`, íntegro — las reglas de §9.3 tal como corrieron

```python
#!/usr/bin/env python3
"""
E6 · L-RUN — extractor de `valor_extraido` / `fuente_citada` (COMMIT-B).

POR QUE EXISTE ESTE ARCHIVO, declarado.
`lanzamiento-L-v1_0.md` §5 dice que `valor_extraido` "lo llena la sesion
ejecutora despues, con el parseo del pipeline; nunca a mano
(`agregar_continua`/`agregar_categorica` son las unicas funciones que lo
derivan)". Esa ultima clausula es materialmente FALSA y se reporta, no se
obedece a ciegas: `agregar_continua`/`agregar_categorica`
(`pipeline-L-adv1-m2.py:215-243`) reciben `list[float]` / `list[str]` YA
extraidas y solo AGREGAN; ninguna de las dos toca `texto_crudo`. El pipeline
no contiene extractor alguno. Quien lo dice es el propio pipeline, en el
comentario de la linea que pone el campo en None:

    valor_extraido=None,  # el parseo real lo hace la sesion ejecutora
                          #   -- pipeline-L-adv1-m2.py:201

Es decir: el pipeline DELEGA el parseo en la sesion ejecutora. Este archivo
es esa delegacion, ejercida de forma MECANICA y DETERMINISTA -- reglas fijas
en orden de prioridad, aplicadas identicamente a las 120 capturas, sin que
ninguna respuesta se lea y se teclee a mano. La prohibicion del encargo
("llenar valor_extraido a mano") queda respetada; lo que no existe y por eso
no puede usarse es un extractor pre-registrado.

Cada captura registra que regla disparo, y el resumen por celda declara el
conteo por regla. Ninguna cifra se corrige, se descarta ni se ajusta.
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path


def sin_acentos(s: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", s)
        if unicodedata.category(c) != "Mn"
    ).lower()


# Un porcentaje suelto: 23.5% / 23,5% / 23 % / ~23.5%
NUM = r"\d{1,3}(?:[.,]\d{1,2})?"
PCT = re.compile(rf"(?<![\d.,])(?:~|≈|aprox\.?\s*)?({NUM})\s*%")
# Un rango: 22-25% / 22–25 % / entre 22 y 25%
RANGO = re.compile(
    rf"(?<![\d.,])({NUM})\s*(?:%\s*)?(?:-|–|—|\s+a\s+|\s+y\s+)\s*({NUM})\s*%"
)

NO_DATO = [
    "no cuento con el dato", "no tengo el dato", "no conozco el dato",
    "no dispongo del dato", "no tengo acceso al dato", "no puedo dar una cifra",
    "no puedo ofrecer una cifra", "no se el dato", "desconozco el dato",
    "no tengo una cifra", "no tengo datos", "no cuento con datos",
]


def _spans_de_rango(texto: str) -> list[tuple[int, int]]:
    return [m.span() for m in RANGO.finditer(texto)]


def _cifras_puntuales(texto: str) -> list[tuple[float, int]]:
    """Porcentajes que NO forman parte de un rango. Devuelve (valor, pos)."""
    rangos = _spans_de_rango(texto)
    out = []
    for m in PCT.finditer(texto):
        a, b = m.span()
        if any(ra <= a and b <= rb for ra, rb in rangos):
            continue
        out.append((float(m.group(1).replace(",", ".")), a))
    return out


def _oraciones_con(texto: str, claves: list[str]) -> list[str]:
    plano = sin_acentos(texto)
    trozos = re.split(r"(?<=[.\n])", texto)
    return [
        t for t in trozos
        if any(k in sin_acentos(t) for k in claves)
    ]


def extraer_valor(texto: str) -> tuple[float | None, str]:
    """Devuelve (valor, regla). Reglas en orden estricto de prioridad."""
    if not texto or not texto.strip():
        return None, "R0-vacia"

    # R1 · el modelo nombra explicitamente su punto central
    for tro in _oraciones_con(texto, ["punto central", "mejor punto",
                                      "punto medio", "mi punto"]):
        c = _cifras_puntuales(tro)
        if c:
            return c[0][0], "R1-punto-central"

    # R2 · el modelo rotula "estimacion puntual"
    for tro in _oraciones_con(texto, ["estimacion puntual", "estimo puntual",
                                      "valor puntual", "punto estimado"]):
        c = _cifras_puntuales(tro)
        if c:
            return c[0][0], "R2-estimacion-puntual"

    # R3 · primer porcentaje suelto en negrita
    for m in re.finditer(r"\*\*([^*]{1,200}?)\*\*", texto, re.S):
        c = _cifras_puntuales(m.group(1))
        if c:
            return c[0][0], "R3-negrita"

    # R4 · primer porcentaje suelto del texto
    c = _cifras_puntuales(texto)
    if c:
        return c[0][0], "R4-primer-porcentaje"

    # R5 · solo hay rango declarado -> punto medio MECANICO, declarado
    r = RANGO.search(texto)
    if r:
        a = float(r.group(1).replace(",", "."))
        b = float(r.group(2).replace(",", "."))
        return round((a + b) / 2, 4), "R5-punto-medio-de-rango"

    # R6 · el modelo declara explicitamente que no tiene el dato
    plano = sin_acentos(texto)
    if any(k in plano for k in NO_DATO):
        return None, "R6-sin-dato-declarado"

    return None, "R7-sin-cifra"


ENC_FUENTE = re.compile(
    r"(?:^|\n)\s*(?:#{1,6}\s*)?\**\s*fuentes?\b\s*\**\s*:?\s*\n",
    re.I,
)


def extraer_fuente(texto: str) -> tuple[str | None, str]:
    """Sonda canario: la fuente que el modelo declara, verbatim y recortada."""
    if not texto or not texto.strip():
        return None, "F0-vacia"

    # F1 · seccion titulada "Fuente"/"Fuentes"
    m = ENC_FUENTE.search(texto)
    if m:
        resto = texto[m.end():]
        for linea in resto.split("\n"):
            l = linea.strip().lstrip("-*•· ").strip()
            if l and not l.startswith("#"):
                return l[:500], "F1-seccion-fuente"

    # F2 · linea que empieza con "Fuente:" en cualquier punto
    for linea in texto.split("\n"):
        pl = sin_acentos(linea).strip().lstrip("-*•· ").strip()
        if pl.startswith("fuente:") or pl.startswith("fuentes:"):
            l = linea.strip().lstrip("-*•· ").strip()
            return l.split(":", 1)[1].strip()[:500] or None, "F2-linea-fuente"

    # F3 · el modelo nombra al publicador sin rotular seccion
    plano = sin_acentos(texto)
    for pub in ["inegi", "banxico", "cnbv", "conapo", "coneval", "imss"]:
        if pub in plano:
            for linea in texto.split("\n"):
                if pub in sin_acentos(linea):
                    return linea.strip().lstrip("-*•· ").strip()[:500], "F3-publicador-mencionado"

    return None, "F4-sin-fuente"


def main() -> int:
    carpeta = Path(sys.argv[1])
    trazas = []
    n = 0
    for ruta in sorted(carpeta.glob("*.json")):
        d = json.loads(ruta.read_text(encoding="utf-8"))
        val, regla = extraer_valor(d["texto_crudo"])
        fue, reglaf = extraer_fuente(d["texto_crudo"])
        d["valor_extraido"] = val
        d["fuente_citada"] = fue
        ruta.write_text(
            json.dumps(d, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        trazas.append({
            "archivo": ruta.name, "id_celda": d["id_celda"],
            "indice": d["indice"], "valor": val, "regla": regla,
            "fuente_regla": reglaf, "tiene_fuente": fue is not None,
        })
        n += 1
    (Path(__file__).resolve().parent / "trazas-extraccion.json").write_text(
        json.dumps(trazas, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"capturas procesadas: {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

---

**Cierre.** `ACTO E6 · L-RUN` queda **CONSUMIDO-PARCIAL**: entrega `120` capturas `L-solo` con cero descartes y conteo `A.13`, y cierra `FP-165` **FIRMADA** con la decisión de **no-ejecución** de `L+corpus`. La consecuencia — corredor `E` inejecutable tal como `ADR-141` lo selló — queda escrita aquí, en la fila y en `ADR-206`, para que `E7` la **reporte** y no pare en falso. Re-sellar `⊕` sigue siendo opción de mesa; hoy no se ejerce.
