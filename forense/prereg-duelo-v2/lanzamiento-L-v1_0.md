# Lanzamiento del corredor `L` — `ADV1-M2`, duelo `ADV1-M2`

**Acto que lo produce:** `E2-PREP-L-RUN` (NUBE, `cloud_default`, repo-only). Redactado contra `SHA` `186f090`, 26/ago/2026. CONTADOR: cero — este acto no corre ninguna `L`; produce el paquete que el acto sucesor `L-RUN` pega y ejecuta.

**Qué es este documento.** El paquete autocontenido para correr el corredor `L` completo del duelo `ADV1-M2` sin leer nada más del árbol y sin poder violar `forense/prereg-duelo-v2/prereg-corrida-v1_0.md` sin notarlo. Todo lo que sigue es citado verbatim del árbol congelado — nada se redefine ni se relaja aquí. Gobierna: `prereg-corrida-v1_0.md` (`ADR-197`/#367).

**Orden sagrado, repetido porque gobierna todo lo que sigue:** hashes → L → R → scoring. Jamás `R` antes de los hashes. Las sesiones `L` jamás ven `R`.

---

## 0 · Compuerta de hashes — CORRE ESTO PRIMERO

Antes de cualquier llamada al modelo, la sesión ejecutora corre estos seis comandos y compara la salida contra la tabla. **Cualquier discordancia → PARO** — y antes de reportar el paro, aplica `A.7`: di qué campo cambió (no solo que cambió).

```bash
sha256sum pipeline-L-adv1-m2.py
sha256sum corredor-B-tasa-base.py
sha256sum corredor-E-combinacion-LM.py
sha256sum scoring-adv1-m3.py
sha256sum sorteo-resultados-v1_0.md
sha256sum marco-congelado-piloto-v1_0.tsv   # debe coincidir además con CONGELADO-v1_0.sha256
```

Ejecutar desde `forense/prereg-duelo-v2/`. Tabla de referencia — `F1` de `prereg-corrida-v1_0.md:99-108`, re-verificada por `E2-PREP-L-RUN` el 26/ago/2026 (Compuerta Cero de ese acto, salida cruda en `forense/notas/2026-08-26-prep-l-run-cierre.md`):

| Archivo | `sha256` esperado |
|---|---|
| `pipeline-L-adv1-m2.py` | `a772a4bc48b724c33ea82fc41877594fa74b89eb267c2ca74401ed5fe3a45b1d` |
| `corredor-B-tasa-base.py` | `14dbf289fc2c66d95e6c8c92a80d459c0dde0a873e740ac5064ed5886a94ebf1` |
| `corredor-E-combinacion-LM.py` | `7752ced239fdc6d5a0a6a15921b7ae0c72661740237e6d047f17fe1d6b63767d` |
| `scoring-adv1-m3.py` | `beec0e1c2e86605bb751601a36c312e34ade4a82a8204e0ab96527beba8e0efb` |
| `sorteo-resultados-v1_0.md` | `140b00a80f57e82caa72a15277d77dfef143becf6bbda6da696d325fbf251c11` |
| `marco-congelado-piloto-v1_0.tsv` | `3a0dcf0138493f40777b4f457bbe0a473e6cf830d6d0c7dc265ad8320c3742e2` (= `CONGELADO-v1_0.sha256`) |

Si un corredor cambió legítimamente entre este lanzamiento y la corrida real, no se sobreescribe la tabla: se aplica la "regla de enmienda, no de silencio" de `prereg-corrida-v1_0.md:110` — fila nueva fechada bajo `## F1 · enmienda AAAA-MM-DD`, con hash viejo, hash nuevo y razón, y se PARA hasta que mesa lo resuelva.

---

## 1 · Invariantes de la corrida (citados, no repetidos de memoria)

**Las 15 celdas sorteadas**, copiadas literal de `sorteo-resultados-v1_0.md` (tabla "Las 15 filas sorteadas"):

`CIV-08, TIC-08, TIC-01, DIN-11, DIN-03, DOC-06, EMP-02, EMP-04, DIN-05, SFT-06, SFT-04, TIC-12, TIC-06, DIN-07, EMP-05`

Cada `id_celda` se resuelve a su `SpecCelda` (`encuesta`, `ola`, `universo`, `variable`, `estimador`, `escala`, `frase_discriminacion`) leyendo `forense/marco-candidatas-piloto-v1_0.tsv` por `id` — `cargar_specs_desde_marco` (`pipeline-L-adv1-m2.py:96-118`) ya hace esta lectura; no se reconstruye a mano.

**× 2 variantes:** `L-solo`, `L+corpus` (`pipeline-L-adv1-m2.py:65`, `ParametrosCorredorL.variante`).

**× `k=8` corridas por celda×variante** (`prereg-corrida-v1_0.md` F2(b) — punto medio del rango `5-10` que `ADV1-M2` exige; `ParametrosCorredorL.__post_init__`, `pipeline-L-adv1-m2.py:69-71`, rechaza cualquier valor fuera de `[5,10]`).

**= 15 × 2 × 8 = 240 llamadas al modelo en total.**

**`temperatura = 1.0`** (`prereg-corrida-v1_0.md` F2(a) — ni el extremo determinista que suprimiría la dispersión que `ADV1-M2` exige reportar, ni un extremo alto sin razón; default del proveedor, mismo valor que las corridas adversariales previas de `forense/adv-duelo/`).

**`modelo_id`** = el fijado en la RANURA DE MESA del encargo que produjo este documento (`forense/encargos/2026-08-26-E2-PREP-L-RUN.md`). Si esa línea no fue editada por mesa antes de este lanzamiento, el valor sellado es `claude-opus-4-6` (`prereg-corrida-v1_0.md` F2(a) — mismo rol que Opus ocupó en las cuatro corridas adversariales de `forense/adv-duelo/`: estimador ciego de máxima capacidad, no el motor barato).

**`version_declarada`** = la cadena de versión textual que el proveedor devuelva **al momento real de la corrida** (`r.model` de la respuesta real, ver §4) — nunca una fecha de build inventada por este documento, que no puede observarla (`prereg-corrida-v1_0.md:73`).

**`comparacion_principal_id = "L-solo"`** — `FP-162` **FIRMADA** (`forense/firmas-pendientes.tsv`, fila `FP-162`; firma verbatim de mesa 25/ago/2026, sellada `ADR-197`). `L+corpus` corre y se reporta pero es **auxiliar, no-gating**: no adjudica ninguna de las cinco casillas de `ADV1-M5` (`prereg-corrida-v1_0.md` F2(g), F0.1).

**CERO descartes** — `F2(d)` (`prereg-corrida-v1_0.md:97`), implementado en `correr_celda` (`pipeline-L-adv1-m2.py:189-206`): las `k` corridas se registran TODAS, incluidas negativas, ambiguas o de rechazo de contenido. **Un rechazo de contenido es una corrida válida** — se cuenta, no se relanza (`llamar_modelo` docstring, `pipeline-L-adv1-m2.py:176-181`).

**Agregado pre-registrado §5** (`pipeline-L-adv1-m2.py:209-243`, no reinventado aquí):
- Continuas: `agregar_continua` — mediana + `q10`/`q90` + `q25`/`q75` (IQR de dispersión).
- Categóricas/ordinales: `agregar_categorica` — moda + `self_consistency` (moda/n) + distribución completa de las `k` respuestas.

**Plantillas `PLANTILLA_L_SOLO` / `PLANTILLA_L_CORPUS`** (`pipeline-L-adv1-m2.py:128-142`) — **intactas, prohibido añadirles una palabra.** Se construyen mecánicamente vía `construir_prompt` (`pipeline-L-adv1-m2.py:145-155`), parametrizadas únicamente por los campos de `SpecCelda`. Ninguna plantilla menciona árbitro, banda, margen material ni fuente de referencia (verificado por lectura en `prereg-corrida-v1_0.md` F2(f)); la única instrucción sobre procedencia es la sonda canario genérica ("Cita la fuente de tu estimación si la tienes").

---

## 2 · Ceguera — aclarada para que nadie pare en falso

`F0.2`/RANURA 2 del prereg (`prereg-corrida-v1_0.md:33-35`) designa el patrón: **sesiones limpias fuera del proyecto**, análogo a las cuatro corridas adversariales ya archivadas en `forense/adv-duelo/`.

El invariante "ninguna sesión que haya leído este pre-registro corre una celda `L`" (`pipeline-L-adv1-m2.py:9-16,67`) se cumple **por construcción**, no por disciplina de quien ejecuta el script: **cada llamada individual a la API del modelo es la "sesión limpia"** — el modelo solo ve el `prompt` construido por `construir_prompt`, que contiene exclusivamente los seis campos de `SpecCelda` (`encuesta`, `ola`, `universo`, `variable`, `estimador`, `escala`) vía la plantilla congelada. El modelo nunca recibe este lanzamiento, el prereg, el sorteo, el marco congelado ni ningún archivo del árbol.

**La sesión ejecutora** (quien corre `pipeline-L-adv1-m2.py` / el driver que implementa `llamar_modelo`) **SÍ puede, y debe, leer este lanzamiento y el prereg** — necesita sus parámetros para llamar correctamente al modelo. Lo que no puede es meter contexto adicional del árbol dentro del `prompt` que arma `construir_prompt` — esa función ya está congelada y no se toca.

---

## 3 · Implementación de `llamar_modelo` — lista para pegar

`pipeline-L-adv1-m2.py` (repo) **NO se toca**. La función `llamar_modelo` (`pipeline-L-adv1-m2.py:175-186`) lanza `NotImplementedError` por diseño — es el único hueco que la sesión ejecutora rellena, en su copia de trabajo o vía monkeypatch en un driver aparte:

```python
import anthropic
_cliente = anthropic.Anthropic()  # exige ANTHROPIC_API_KEY en el entorno
def llamar_modelo(prompt, params):
    r = _cliente.messages.create(
        model=params.modelo_id, max_tokens=1024,
        temperature=params.temperatura,
        messages=[{"role": "user", "content": prompt}],
    )
    # sin reintentos salvo error de transporte; un rechazo de contenido ES corrida válida
    return "".join(b.text for b in r.content if getattr(b, "type", "") == "text")
```

Además: capturar `r.model` como `version_declarada` **en la primera llamada** de la sesión y **congelarla** (mismo valor) en el JSON de cada corrida posterior — `ADV1-M2` exige "fijados", no un valor que cambie llamada a llamada dentro de la misma corrida.

Contrato que esta implementación debe respetar, verbatim del docstring que reemplaza (`pipeline-L-adv1-m2.py:176-181`): (1) fijar `modelo_id`/`version`/`temperatura` exactamente como en `params`; (2) no reintentar en caso de rechazo salvo error de transporte; (3) devolver el texto crudo sin post-proceso.

---

## 4 · Dónde corre `L-RUN`

**Fuera de NUBE** — este entorno (`cloud_default`) no tiene salida de red, verificado en `E2-PREP-L-RUN` (`curl … https://www.inegi.org.mx/` → `000`). `L-RUN` necesita: una caja con red saliente + `ANTHROPIC_API_KEY` en el entorno. Candidatas, en orden: **UBUNTU** si la clave está disponible ahí, o la caja que mesa designe.

**`api.anthropic.com` es el único destino de red que este acto autoriza.** Ningún otro host, ninguna descarga de microdato, ninguna consulta a INEGI ni a ninguna otra fuente.

**Firma de entorno (A.2, tres partes) que `L-RUN` reporta al arrancar**, mismo patrón que todos los actos de este árbol:
1. `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` — valor crudo del entorno donde corre `L-RUN` (se espera algo distinto de `cloud_default`, porque `cloud_default` no tiene red).
2. Sonda cruda de red — no a INEGI (esto no es un acto de microdato): `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://api.anthropic.com/` (o el `GET` que confirme alcance real al único host autorizado), nunca `curl -I`.
3. `ANTHROPIC_API_KEY` presente en el entorno — reportar solo presencia/ausencia, nunca el valor.

---

## 5 · Capturas (F2(e))

Un JSON por `(id_celda, variante, índice)`, ruta:

```
forense/prereg-duelo-v2/corridas-L/{id_celda}__{variante}__{indice:02d}.json
```

Ejemplo de ruta real: `forense/prereg-duelo-v2/corridas-L/CIV-08__L-solo__01.json`.

Campos por archivo — los de `RespuestaCorrida` (`pipeline-L-adv1-m2.py:166-172`) más el sobre de contexto que la sesión ejecutora agrega:

```json
{
  "id_celda": "CIV-08",
  "variante": "L-solo",
  "indice": 1,
  "texto_crudo": "... salida completa del modelo, sin editar ...",
  "valor_extraido": null,
  "fuente_citada": null,
  "timestamp": "2026-…T…Z",
  "params": {
    "modelo_id": "claude-opus-4-6",
    "version_declarada": "... verbatim de r.model, congelada ...",
    "fecha_congelacion": "2026-08-26",
    "temperatura": 1.0,
    "k_corridas": 8,
    "variante": "L-solo"
  },
  "sha256_prompt": "..."
}
```

`texto_crudo` va **íntegro**, sin post-proceso (contrato de `llamar_modelo`, §3). `valor_extraido` se deja `null` en la captura — **lo llena la sesión ejecutora después, con el parseo del pipeline; nunca a mano** (`prereg-corrida-v1_0.md` F2(e), `agregar_continua`/`agregar_categorica` son las únicas funciones que lo derivan).

> **Enmienda fechada 2026-08-26 (ACTO MAESTRA30-E8, este doc es histórico del corredor `L` — texto viejo intacto arriba, no se reescribe).** La afirmación de arriba es **materialmente falsa**, reportada por `ACTO MAESTRA30-E6 · L-RUN` (`forense/notas/2026-08-26-l-run-cierre.md` §9.1, líneas 317-442): `agregar_continua`/`agregar_categorica` (`pipeline-L-adv1-m2.py:215-243`) reciben `list[float]`/`list[str]` **ya extraídas** y solo **agregan** — ninguna de las dos toca `texto_crudo` ni deriva `valor_extraido` de él. **El pipeline pre-registrado no contiene extractor alguno**; la línea que fija `valor_extraido=None` lo delega explícitamente a un paso posterior. E6 congeló ese extractor aparte, fuera de este pre-registro (`extractor.py`, `forense/notas/2026-08-26-l-run-cierre.md` §13.2), con sus reglas commiteadas antes de aplicarlas sobre las 120 capturas -- ver esa nota para el detalle y la consecuencia honesta (§9, líneas 420-442: las reglas del extractor se diseñaron habiendo visto el formato de salida del material, más que cero y menos que un extractor ajustado a los datos).

**Total esperado: 240 archivos** (15 celdas × 2 variantes × 8 corridas), todos **commiteados**.

---

## 6 · Orden sagrado y muralla

`hashes → L → R → scoring`. El acto `L-RUN`:

- **Jamás** abre microdato (nada bajo `data/raw/`).
- **Jamás** corre `corredor-B-tasa-base.py`, `corredor-E-combinacion-LM.py` ni `scoring-adv1-m3.py` — esos son actos `R`/`E` posteriores, en UBUNTU, con microdato.
- **No aplica** `CV≥30%⇒SKIP` (`FP-79`, `forense/firmas-pendientes.tsv`) — esa regla se aplica en `scoring`, nunca en `L`.

---

## 7 · Qué sigue (mapa de dos líneas)

`L-RUN` (esta caja, fuera de NUBE) → corredores `B`/`E` + árbitro `R` (UBUNTU, microdato) → `scoring-adv1-m3.py` (banda TOST = `0.5·EE(R)`, `FP-163` **FIRMADA**, `ADR-199`) → **PRIMER MARCADOR** del programa, bajo **`PILOTO SIN VEREDICTO`** (D-i) — el piloto puntúa, no adjudica.

---

## 8 · Checklist de mesa antes de lanzar `L-RUN`

- [ ] Caja elegida (con red saliente a `api.anthropic.com`).
- [ ] `ANTHROPIC_API_KEY` presente en esa caja.
- [ ] `modelo_id` confirmado (`claude-opus-4-6` por defecto) o sustituido en la RANURA de `forense/encargos/2026-08-26-E2-PREP-L-RUN.md` **antes** de arrancar.

---

## Lo que este acto (E2-PREP-L-RUN) NO hace

No corre ninguna llamada al modelo. No edita `pipeline-L-adv1-m2.py`, el prereg, el sorteo, el marco congelado ni las plantillas — todo se cita, nada se toca. No abre microdato. No crea `corridas-L/` (la crea `L-RUN` al ejecutar). No añade fila de tablero nueva — la ranura de modelo vive en el encargo/lanzamiento, ya autorizada por `F2(a)` del prereg.
