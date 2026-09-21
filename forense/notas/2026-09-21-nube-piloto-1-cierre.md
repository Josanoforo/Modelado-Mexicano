# ACTO GEN2-NUBE-PILOTO-1 · nota de cierre (21/sep/2026)

Encargo: `forense/encargos/2026-09-20-GEN2-NUBE-PILOTO-1.md` (archivado verbatim por 0-bis A.3, sha256 `ed67f208d41058fec391e1059ba267b3451ddde368d25cb6df3aae90d0bb3fc3`). SHA de redacción declarado: `bd9ed2134021c6cd55dbf5e625dbbcb52c63d065`. Base real del acto: `b8438d76a0bee165056e886e2cc743e4c499f50b` (`origin/main`), **8 commits de deriva** desde el SHA de redacción — no es PARO (§6 del encargo, §4.2 de `/acto`): se refrescó y se re-derivó todo lo que el perímetro toca.

MODO: `RÍGIDO`. No se tocó `spec.yaml`, `medidor.py` ni ningún `sello.*` de `CALC-ENIF-0001`.

---

## 1 · Resultado, en una línea

`RESULTADO = REPRODUCE` · `CONTEXTO = DISTINTO` (razón: `dependencias_distintas`), en `milpa-inegi`, sobre un payload que bajó el descargador de la pieza 1, con su fila en `forense/replay-evidencia.tsv` en este mismo acto. **«Hecho» según el encargo: satisfecho.**

**No generaliza** — verbatim, como mesa pidió: *un `REPRODUCE` sobre un payload de 3.1 MB en un host no demuestra que 18.4 GB en 200 hosts funcionen. El piloto prueba que el carril existe, nada más.*

---

## 2 · ARRANQUE (salida cruda del hook, A.2 en tres partes)

```
ENTORNO-DERIVADO = NUBE
senal-corpus: montado=NO archivos_examinados=0
senal-nube-env: CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default
red: PERMITIDA (http_code=200, http_connect=200, x_deny_reason=ausente, via_proxy=SI)
head-vs-origin/main: detras=0 adelante=0 (sin fetch)
worktrees: 1
es-worktree: NO
ramas-locales-con-commits-propios: 0/2
data-raw-en-este-worktree: NO
```

Sonda cruda independiente: `curl_inegi_http_code=200` · `ls data/raw | head -1` vacío, `archivos_examinados=0` (A.13).

Compuerta (e) del encargo: **satisfecha** — `ENTORNO-DERIVADO = NUBE` y `red: PERMITIDA`. `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` sigue diciendo `cloud_default` dentro de `milpa-inegi`: **la variable no discrimina el entorno, la línea `red:` sí**. Eso es exactamente lo que hace que FP-67 quede acotada y no sustituida (pieza 3): el negativo de agosto se midió sobre la misma variable.

`data/raw` ausente al arrancar — no es PARO (§6): se creó. No hay corpus compartido que enlazar en esta caja.

---

## 3 · Premisas verificadas, y las tres que cayeron

Verificadas y en pie (`[LEÍDO]`/`[EJECUTADO]` comprobadas de pasada; `[REPORTADO]` verificado a fondo, que era mío):

- `data/manifiesto.yaml`: **1 629 entradas / 1 624 con payload**. ✔
- Entrada del piloto: `id`, `archivo`, `sha256 00e4b0b4…f039`, `tamano_bytes 3131148`, `url_origen` — los cinco campos idénticos a lo que el encargo declara. ✔
- `data/corrida0/CALC-ENIF-0001/`: 7 artefactos; `sello.json` fija `medidor.py = 6ac67a01…`; `spec.yaml` declara `miembro_usado: TMODULO.csv` y `IN-ENIF-SPEC-SELLADA` como insumo **de repo**, sin descarga. ✔
- La fila de replay existente se declara a sí misma `HEREDADO-DEL-REGISTRO-PUBLICADO` / `EVIDENCIA-HISTORICA · NO es verify nuevo ni validación independiente` (línea 52). ✔ El verify de este acto es, en efecto, el primero nuevo y el primero fuera de CAJA.
- `tools/corrida0.py::cmd_verify` en la línea 2652, toma sólo `calc_id`. ✔
- `tests/manifiesto.py`: 1 740 líneas, **0** coincidencias de `urllib|requests|urlopen|httpx`. ✔
- `http.server`/`HTTPServer`/`socketserver` en `tests/` y `tools/`: `NO-ENCONTRADO`, **universo 367 archivos `.py`** (A.13). El arnés se escribió. ✔
- Los **4** ids con `estado_reserva` son los cuatro que el encargo nombra. ✔
- `FP-67` sigue `CERRADA` (A.17, re-verificada por lectura de la fila 68 de `forense/firmas-pendientes.tsv`, no de memoria). ✔
- `[REPORTADO] milpa-inegi permite www.inegi.org.mx`: **CIERTO**, medido, no heredado. ✔
- Descarga por id en el repo: `NO-ENCONTRADO` confirmado con mi acceso. Los archivos con red siguen siendo específicos de fuente; `tools/barrido_descargas_vs_manifiesto.py` sigue en 80 líneas y de solo lectura. ✔

**Cayeron tres.** Ninguna toca qué se mide ni una firma de mesa — las tres son logística o censo, el OBJETIVO siguió alcanzable, se replantearon y se declaran (v2.15 §2, `/acto` §4.2):

1. **`raiz: None` literal en la entrada del piloto** → **FALSA**. La entrada **no trae la clave `raiz` en absoluto**. Censo sobre las 1 629 entradas: **1 013 con la clave ausente · 0 con valor nulo**. Qué hice en su lugar: el contrato del encargo («ausente y presente-con-valor-nulo se resuelven explícitamente y se declara cuál se usó») se implementó **igual, con las dos ramas**, porque el contrato es de mesa y la rama nula puede nacer mañana de un `--registra`; lo que se corrige es la cifra. `resuelve_raiz_declarada` imprime cuál aplicó, y la corrida real imprimió `clave 'raiz' AUSENTE -> data_raw (integrada)`.
2. **«22 ids `banxico_sie_*`, nueve con `url_origen` que termina en `.do`»** → **FALSA en las dos cifras, cierta en el fondo**. Los `banxico_sie_*` son **nueve** (los `banxico*` son 25); y ninguna de sus URLs *termina* en `.do` — lo que termina en `.do` es la **ruta**, seguida de query string (`…Action.do?sector=21&accion=consultarCuadro&idCuadro=CF881&locale=es`). Qué hice en su lugar: **el caso de prueba que mesa firmó se conserva y se prueba contra el manifiesto real** (`test_los_nueve_banxico_sie_del_manifiesto_real_salen_no_accesible`, los nueve salen `NO-ACCESIBLE`), con la cifra corregida en el propio test. La regla de clasificación no se ajustó para que cuadrara: se derivó del universo real de `url_origen` (`.php`=162 · `SIN-EXTENSION`=450 · `.aspx`=46 · `.do`=9 · esquema vacío=76 …) antes de escribirla.
3. **`cmd_verify` «devuelve 0 en REPRODUCE»** → **imprecisa**. Con `RESULTADO=REPRODUCE` y `CONTEXTO=DISTINTO` devuelve **1** (`REPLICA-RESULTADO · CONTEXTO-DISTINTO`). No cambia nada del acto —el veredicto se lee de los dos ejes, no del código de salida— pero un sucesor que gatee por `rc == 0` se llevaría un falso negativo. Anotado en `forense/hallazgos.md`.

---

## 4 · Pieza 1 · el descargador (COMMIT-1, `4333b14`)

`tests/manifiesto.py --descarga --id <id>` (repetible). Vive ahí y no en herramienta nueva (D-14): extiende el punto de entrada que ya gobierna el manifiesto y **hereda** la resolución de raíz y el contraste de `sha256` de `--verifica`; añade un **cuarto** estado (`DESCARGADO-AHORA`) sin tocar los tres de A.1.

Decisiones que tomé por latitud, y las declaro:

- **La comprobación de redirección es relativa, no una lista de hosts.** El código compara el host final contra el **host que la propia entrada del manifiesto declara**; distinto → `PARO-REDIRECCION` con el host final exacto y la cadena completa. La lista de hosts permitidos la impone el entorno (firma 8) y el código no la duplica: una constante `HOST_MESA = "www.inegi.org.mx"` existe sólo para **nombrarla en el mensaje de paro**, nunca para autorizar. Así la regla es la de mesa y, de paso, el arnés puede correr contra `127.0.0.1` sin abrir una segunda puerta.
- **`urllib` con redirecciones desactivadas** y seguimiento manual, tope 5: es la única forma de ver cada salto en vez del destino final.
- **Descarga a un temporal dentro de la raíz de destino**, `os.replace` sólo tras verificar el `sha256`. Un `sha256` discordante borra el temporal y **no deja nada** en la raíz (probado: el directorio queda vacío).
- **Query string ⇒ `NO-ACCESIBLE`.** Cubre los nueve servlets del SIE por su forma real, no por el sufijo que el encargo suponía.
- `--timeout` con defecto 120 s, sin reintentos: el piloto es un archivo y un host; los reintentos son del sucesor de escala.

D-22: el punto de entrada corrió **de punta a punta** contra un `http.server` de la stdlib antes de la primera descarga real — archivo bueno · `sha256` discordante · redirección a otro host · `404` · redirección al mismo host (se sigue) · guardia de reserva · id inexistente · las dos ramas de `raiz` · «no acepta una URL suelta» · «no escribe en el manifiesto». **17/17 VERDE.** Cableado en `.github/workflows/verify.yml` en el mismo commit (D-21).

Lo que el descargador **no** hace: no se niega ante `enif_2024_enif_2024_bd_csv`. La reserva de la sección de crédito de ENIF 2024 se protege **en el medidor** (firma 4); un descargador que la bloqueara estaría protegiendo lo que no le toca.

---

## 5 · Pieza 2 · el piloto (COMMIT-2, `e7395e9`)

Descarga, salida cruda:

```
enif_2024_enif_2024_bd_csv: raíz resuelta = data_raw [clave 'raiz' AUSENTE -> data_raw (integrada)]
enif_2024_enif_2024_bd_csv: DESCARGADO-AHORA -- sha256 VERIFICADO contra data/manifiesto.yaml
  (00e4b0b42775276b2da236a5bba8c64dc5a92c289908a4727dec93dc7684f039) · 3131148 bytes ·
  host final: www.inegi.org.mx · cadena: www.inegi.org.mx
```

Sin redirección: el host final coincide con el declarado. **No hay host nuevo que reportar a mesa** (firma 1). Bytes exactos contra el manifiesto: 3 131 148.

Verify, **dos ejes por separado** (E.3) — salida cruda íntegra en `forense/evidencia-replay-nube-2026-09-21.txt`:

```
[1/5 SELLO] COINCIDE -- sello y todos los archivos que cubre coinciden
[2/5 SPEC.YAML] IDENTICO
[3/5 INPUT COINCIDE] enif_2024_enif_2024_bd_csv (manifiesto)
[3/5 INPUT COINCIDE] IN-ENIF-SPEC-SELLADA (repo)
[4/5 CONTEXTO] codigo=IDENTICO  commit_informativo=DISTINTO (FP-358: no gatea)
                parametros=IDENTICO  seed=IDENTICO  dependencias=DISTINTO
CONTEXTO: DISTINTO  razon: dependencias_distintas
VERIFY: REPLICA-RESULTADO · CONTEXTO-DISTINTO   (CONTEXTO=DISTINTO · RESULTADO=REPRODUCE)
```

**188 `RESULT REPRODUCE`, 0 discordantes.** `CONTEXTO=DISTINTO` es lo que mesa anticipó, y **no degrada el RESULTADO**.

**La primera corrida del verify dio `NO-EJECUTABLE`**, y queda asentada: `ModuleNotFoundError: No module named 'numpy'`. `numpy` es la única `dependencias_materiales` que la spec sellada declara, e instalar una dependencia es latitud explícita del encargo (§6). Se instaló (`numpy 2.4.6`) y se reejecutó. **No es PARO (g)**: el código congelado sí corre — lo que faltaba era el entorno, no el código; nada congelado se parcheó. Y **`NO-EJECUTABLE` no se escribe como `NO-REPRODUCE`** (E.3): se reporta como lo que fue, una caja sin la dependencia.

E.7 — fila nueva en `forense/replay-evidencia.tsv` **en el mismo acto**, escrita en texto plano `split`/`join` (ADR-123(h)), 14 columnas verificadas. La fila heredada de 2026-09-09 **no se editó ni se borró**; la nueva declara en `alcance` qué la distingue.

**CONTADOR: 146 → 147 filas de datos**, exactamente como el encargo declara. `cuenta_gen2` **no se movió** (este acto no sella corrida nueva; verificado con `corrida0.py status`).

---

## 6 · Pieza 3 · el asiento de FP-67

`FP-402`, `ABIERTA`. Acota `FP-67` a su universo medido (A.10) por firma 6. **La fila `FP-67` no se editó**: sigue `CERRADA` y sigue mandando mientras mesa no firme. Lo medido: FP-67 estableció el bloqueo contra una caja `cloud_default` con red por defecto; en nube con red `Custom` el egreso a INEGI **no** está bloqueado, y el carril entero (descarga verificada + verify `REPRODUCE`) corre. FP-67 queda **vencida en alcance** para ese territorio — no refutada, no borrada, no vigente para él.

Lo que FP-402 **no** pide: no sustituir FP-67, y no generalizar a escala. Eso es `NUBE-PILOTO-2`.

---

## 7 · Contadores movidos

- `forense/replay-evidencia.tsv`: **146 → 147** filas de datos.
- `forense/firmas-pendientes.tsv`: **+1** (`FP-402`, `ABIERTA`).
- `cuenta_gen2`: **sin mover**, como el encargo veda.
- Mediciones sobre México producidas por este acto: **0** — verifica un carril, no afirma nada sobre México. Por eso el módulo de auditoría de rigor extremo no aplica (§5 de las instrucciones, y el propio encargo §10).
