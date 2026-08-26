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
