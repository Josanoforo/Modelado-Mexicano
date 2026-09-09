# ACTO GEN2-REGISTRO-REPLAY · nota de cierre

**9/sep/2026 · NUBE · rama `claude/funny-ramanujan-puyxic` · encargo:
`forense/encargos/2026-09-09-GEN2-REGISTRO-REPLAY.md` · redactado contra
`4497029a`; re-derivado y ejecutado contra `origin/main` = `66eed1b4f4a3`.**

**CONTADOR: no.** Este acto protege mediciones, no las produce. Ningún `CALC`
nace, ningún sello se toca, ningún número cambia: `status` da lo mismo antes y
después, y las tres vistas derivadas salen **byte a byte idénticas** a las
publicadas.

## 1 · El defecto, reproducido antes de tocar nada

El anexo de la propuesta de Astra, ejecutado verbatim contra `66eed1b4f4a3`:

```
corridas afectadas: 23   campos: 46
  ('CALC-0001--174c269a07b6', 'contexto_replay', 'DISTINTO', 'NO-VERIFICADO')
  ('CALC-0001--174c269a07b6', 'resultado_replay', 'NO-EJECUTABLE', 'NO-VERIFICADO')
  ('CALC-0003-v2--cdebb607728c', 'resultado_replay', 'REPRODUCE', 'NO-VERIFICADO')
  ...
```

23 corridas, 46 campos. Entre lo que se perdía había veredictos **adversos**:
`NO-REPRODUCE / IDENTICO` de `CALC-MOTOR-celdas-semilla` y tres
`NO-EJECUTABLE`. Cambiar `NO-REPRODUCE` por «no verificado ahora» no demuestra
que la discrepancia desapareció: la esconde.

La causa, leída en el código y no supuesta: las dos columnas mezclaban **dos
preguntas distintas** — «qué dijo el replay» (evidencia, histórica) y «puede
esta sesión replayar» (capacidad, de hoy). Con las dos en la misma celda, gana
quien re-derivó al último, y el diff no dice que la causa fue la caja.

## 2 · P1 · La contención, ya mecánica

`registro --escribe` calcula el diff de los dos ejes contra la vista
**publicada** antes de tocar el primer TSV (`_para_si_pisa_replay`, delante de
las tres llamadas a `_escribe`). Si una corrida **ajena al lote autorizado**
cambiaría de veredicto, levanta `ReplayPisado` (subclase de `ParoRegistro`),
lista cada id con su transición, y termina sin escribir ninguna de las tres
vistas. La adenda manual de NC-0094 —pegar el diff, parar si toca ajenas— deja
de depender de que alguien se acuerde.

La única forma de mover un veredicto ajeno es nombrarlo en `--lote`, que es
exactamente la «razón explícita» que la validación (a) exige. **No hay
`--force` y no hay borrado silencioso.** Una corrida que no está en la vista
publicada no tiene veredicto que pisar: registrar un lote nuevo nunca cae aquí.

## 3 · P2 · Evidencia histórica y observación de sesión, separadas

Los dos ejes conservan su vocabulario sellado (E.3) y son **evidencia**. La
limitación de la sesión presente se reporta **aparte**: como aviso y en
`registro --fuentes`, nunca sobreescribiendo la evidencia.

**La fuente es `forense/replay-evidencia.tsv`.** Se eligió archivo aparte
porque la identidad que `sello.json`/`ejecucion.json` ya traen (corrida,
hashes, spec, código, inputs, fecha, entorno) **no alcanza**: les faltan los
dos ejes con sus razones — verificado leyendo `CALC-R-CIV-M-10`, cuyo
`sello.json` tiene cuatro claves de hash y ningún veredicto. Y los bytes
sellados no se editan para alojar metadatos (E.3). Las vistas siguen siendo
derivadas **de esta fuente**; los TSV derivados no se vuelven su propia fuente.

Precedencia, declarada en `_proyecta_replay` y probada una por una:

1. veredicto **concluyente** de esta sesión (`--verifica`) manda. Si contradice
   al asiento, se avisa con **ambos** veredictos y la fecha del asiento;
2. si la sesión **no pudo pronunciarse** (`NO-EJECUTABLE` / `NO-VERIFICABLE`,
   típicamente por falta de corpus) y hay asiento vigente, se proyecta el
   **asiento** y la limitación se reporta aparte. Esta rama es la que impide
   que una caja sin microdato borre lo que otra sí midió — y también arregla el
   segundo defecto de NC-0094 (las 7 filas que cambiaban *con* `--verifica`);
3. asiento vigente sin verificación de hoy → se proyecta el asiento;
4. asiento **no vigente** (cambió spec, blob del script o SHA de inputs) →
   `NO-VERIFICADO` **con la razón**. No se arrastra a la identidad nueva;
5. nada de lo anterior → `NO-VERIFICADO`, que sigue siendo la verdad sin fuente.

`codigo_commit`, `fecha` y `entorno` se asientan como descripción, no como
llave: un commit distinto con el mismo blob no cambia lo que se ejecutó.

### La siembra, declarada

Las 23 filas se sembraron **una vez, a mano**, transcribiendo el veredicto
publicado en `data/corrida0/corridas.tsv@66eed1b4f4a3`, con
`procedencia = HEREDADO-DEL-REGISTRO-PUBLICADO`, `fecha_verificacion =
DESCONOCIDA`, `razones = NO-ARCHIVADA-EN-SU-MOMENTO` y alcance escrito en cada
fila: *«EVIDENCIA-HISTORICA · veredicto publicado, sin salida estructurada de
verify archivada; NO acredita verificación en esta sesión»*.

Esto es, y se dice sin adorno, el **único** punto donde un TSV derivado
alimentó su fuente. Se hizo así porque las dos alternativas eran peores:
destruir la evidencia, o fingir una verificación que nadie corrió. El bucle se
rompe **aquí y una sola vez**, con SHA de origen y alcance en cada fila; de
aquí en adelante el registro lee el asiento, nunca el TSV. Por eso el sembrador
**no vive en `corrida0.py`**: un sembrador automático volvería a lavar el TSV en
cada regeneración. Su código va íntegro en el §6 de esta nota.

Ninguna fila `NO-VERIFICADO` o `NO-CORRIDA` se sembró: eso convertiría la
ausencia de fuente en una fuente.

## 4 · P3 · Las seis validaciones, sobre fixture

En `tests/test_corrida0.py`, sin un solo replay real — el defecto es de
**registro**, y probarlo con 23 reejecuciones de microdato costaría una caja sin
probar nada extra:

| # | caso | test |
|---|---|---|
| (a) | lote nuevo no modifica evidencia ajena; moverla exige nombrarla | `t_replay_a_lote_nuevo_no_toca_evidencia_ajena` |
| (b) | segundo registro sobre el mismo corte = idempotente | `t_replay_b_segundo_registro_idempotente` |
| (c) | sesión sin corpus no borra evidencia de CAJA | `t_replay_c_sesion_sin_corpus_no_borra_evidencia` |
| (d) | cambio de input/spec/código invalida el comprobante como vigente | `t_replay_d_cambio_de_identidad_invalida_el_comprobante` |
| (e) | un `NO-REPRODUCE` posterior queda visible junto a su contexto | `t_replay_e_no_reproduce_posterior_queda_visible` |
| (f) | el caso de las 23 filas: primero el defecto, después la protección | `t_replay_f_caso_23_filas_defecto_y_proteccion` |

Cada uno demuestra **primero el defecto y después la protección**. (c) y (e)
prueban las dos direcciones: ni un éxito viejo tapa un fallo nuevo, ni un éxito
de hoy borra en silencio un `NO-REPRODUCE` asentado.

**Los tests muerden** — comprobado por mutación, no por fe:

- desarmando P1 (`if not ajenas: return` → `if True: return`): fallan (a) y (f);
- desarmando P2 (la rama de evidencia vigente): fallan (c), (d), (e) y (f).

## 5 · Comprobación de que nada se pisó

```
$ python3 tools/corrida0.py registro
SECO data/corrida0/corridas.tsv: sin diferencia con el archivo en disco (110 filas)
SECO data/corrida0/resultados.tsv: sin diferencia con el archivo en disco (1594 filas)
SECO data/corrida0/usos.tsv: sin diferencia con el archivo en disco (205 filas)
```

Ésta es la prueba en producción de que la reparación funciona: **la misma nube
sin corpus que antes borraba 23 veredictos ahora reproduce el TSV publicado
byte a byte.** Por eso este acto no re-deriva ninguna vista — no hay nada que
re-derivar, y así tampoco choca con el acto DBF que corre en CAJA.

`tests/check.py --baseline`: **VERDE**, código 0. Línea base y árbol con el
cambio dan idéntico: `3 FAIL · 1135 WARN`, los tres de `T06`/`T08` (corpus,
ajenos a este acto). Cero FAIL nuevos, cero WARN nuevos.
`tests/test_corrida0.py`: 78 casos, 78 ok, 0 fallos (72 antes + 6 de P3).

## 6 · El sembrador, verbatim

```python
# ACTO GEN2-REGISTRO-REPLAY · P2 · SIEMBRA UNICA de forense/replay-evidencia.tsv.
# Se corre UNA VEZ, a mano, y su salida se versiona. NO vive en corrida0.py a
# proposito: un sembrador automatico volveria a hacer del TSV derivado su
# propia fuente en cada regeneracion, que es justo lo que NC-0094 prohibe.
import json, subprocess
from pathlib import Path
from tools import corrida0 as C

SHA = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                     text=True).stdout.strip()[:12]
NOTA = "forense/notas/2026-09-09-GEN2-REGISTRO-REPLAY-cierre.md"
ALCANCE = ("EVIDENCIA-HISTORICA · veredicto publicado, sin salida estructurada "
           "de verify archivada; NO acredita verificacion en esta sesion")
PROC = f"HEREDADO-DEL-REGISTRO-PUBLICADO · data/corrida0/corridas.tsv@{SHA}"

publicado = {f["corrida_id"]: f for f in C._leer_tsv_derivado(C.VISTA_CORRIDAS)}
filas = []
for d in C._dirs_calc():
    ruta = d / "ejecucion.json"
    if not ruta.exists():
        continue
    ejec = json.loads(ruta.read_text(encoding="utf-8"))
    pub = publicado.get(ejec.get("corrida_id", ""))
    if not pub:
        continue
    # Solo se asienta lo que es EVIDENCIA. NO-VERIFICADO/NO-CORRIDA no lo son:
    # sembrarlos convertiria la ausencia de fuente en una fuente.
    if pub["resultado_replay"] in (C.NO_VERIFICADO, C.NO_CORRIDA):
        continue
    spec_sha, script_sha, inputs = C._identidad_replay(ejec)
    filas.append({
        "calc_id": d.name, "corrida_id": ejec["corrida_id"],
        "resultado_replay": pub["resultado_replay"],
        "contexto_replay": pub["contexto_replay"],
        "razones": "NO-ARCHIVADA-EN-SU-MOMENTO",
        "spec_yaml_sha256": spec_sha, "script_blob_sha256": script_sha,
        "input_sha256_efectivos": inputs,
        "codigo_commit": ejec.get("git_commit") or C.NO_DECLARADO,
        "fecha_verificacion": "DESCONOCIDA",
        "entorno": "NO-DECLARADO-EN-SU-MOMENTO",
        "procedencia": PROC, "alcance": ALCANCE, "nota": NOTA,
    })

filas.sort(key=lambda f: f["calc_id"])
with C.REPLAY_EVIDENCIA.open("w", encoding="utf-8") as fh:
    fh.write("\t".join(C.COLS_REPLAY_EVIDENCIA) + "\n")
    for f in filas:
        fh.write("\t".join(f[c] for c in C.COLS_REPLAY_EVIDENCIA) + "\n")
print(f"sembradas {len(filas)} filas en {C._rel(C.REPLAY_EVIDENCIA)} desde corridas.tsv@{SHA}")
```

Salida: `sembradas 23 filas en forense/replay-evidencia.tsv desde
corridas.tsv@66eed1b4f4a3`.

## 7 · P0 · El insumo, archivado

`forense/notas/2026-09-09-PROPUESTA-MEJORAS-NOTAS-PR631-659-astra.md`, con la
cabecera de procedencia **arriba** del texto intacto. El cuerpo archivado es
byte a byte el original entregado a dirección:
`sha256 = 073107580c507f53094eab0a685f2d65f296a38eb319bec3f802a15f54e073e9`.
Este acto despacha **solo el punto 2** de esa propuesta (§3, integridad del
registro). Los puntos 3, 4 y 5 —identidad por consumidor, tests de conteo y
fecha, calibración del revisor, localización en el derivador— **no se tocaron**
y siguen siendo propuesta, no decisión.

## 8 · Lo que queda abierto

**NC-0097 no se cerró, y no por olvido.** El asiento que pide vive en
`data/corrida0/decisiones.tsv`, que **no está en el perímetro** de este encargo
(«Toca: tools/corrida0.py · tests/ · forense/notas/ · forense/no-corrido.tsv y
forense/firmas-pendientes.tsv · 0-bis · cascada»). Además tiene consecuencia
mecánica medida: `_cuenta_gen2_resuelto` da precedencia a `decisiones.tsv` sobre
la etiqueta de la spec, así que escribir esas tres filas **cambiaría
`motivo_cuenta_gen2` de los tres `CALC-R` en `corridas.tsv`** — obligando a
re-derivar las vistas, que tampoco están en el perímetro y que el acto DBF está
tocando en CAJA ahora mismo. Es exactamente el caso que la regla del encargo
anticipa: «si te encuentras escribiendo fuera de esta lista, PARA — el perímetro
estaba mal calculado y saberlo vale más que el atajo». La propia fila NC-0097 ya
nombra el hogar correcto: `FIRMAS-ADOPCION-1 (o acto con decisiones.tsv en su
perímetro)`. Queda **ABIERTA** con el residuo escrito.

**NC-0098 (nueva).** Los 23 asientos son `HEREDADO`, con
`fecha_verificacion = DESCONOCIDA` y sin las razones del eje CONTEXTO: son
evidencia histórica de alcance limitado, y así se proyectan y se imprimen.
Ninguno es todavía `VERIFY-ESTRUCTURADO`. El mecanismo para producirlos existe
y está probado; lo que falta es que un lote corra `verify` en CAJA y asiente su
salida. Además, las tres vistas no llevan columna de fuente: la cita vive en
`registro --fuentes` y en el asiento, no en el TSV — añadirla exige una
re-derivación global que este acto no tiene autorizada.

**NC-0094 se cierra**: P1 y P2 aterrizaron completos y probados por mutación, y
la comprobación de §5 lo demuestra en el árbol real.
