# Paquete de la corrida `L` — marco-M v1.2, 14 celdas

**Acto que lo produce:** `MAESTRA34-N2 · MARCO-M-v1_2` · P4 (NUBE,
`cloud_default`, repo-only). Redactado contra SHA `8598a72`, ejecutado 2/sep/2026.
**CONTADOR: cero** — este acto no corre ninguna `L`; produce el paquete que mesa
ejecuta en una sesión limpia fuera de este proyecto.

**Orden sagrado:** hashes → L → R → scoring. Las sesiones `L` jamás ven `R`.

> ⚠️ **Este paquete NO se puede lanzar todavía.** Hay un bloqueo mecánico
> identificado y acotado en §6. Todo lo demás está verificado y listo.

---

## 0 · Prohibición explícita — léela antes de arrancar

**Durante esta corrida NO se abre:**

- `forense/prereg-duelo-v2/corridas-R/`
- cualquier `scoreboard-*.md`
- `forense/prereg-duelo-v2/corridas-M/` (incluidos los `*__v1_2.json` que P3 acaba de emitir)
- **`milpa/tramite.yaml`** ← específico de v1.2, ver §5. No es una prohibición
  decorativa: ese archivo contiene la `p` medida de las olas de tres de las
  celdas de este paquete.

---

## 1 · Compuerta de hashes — CORRE ESTO PRIMERO

Desde `forense/prereg-duelo-v2/`. Cualquier discordancia → PARO (A.7), con el
campo que cambió declarado; no se sobreescribe la tabla, se aplica la regla de
enmienda de `prereg-corrida-v1_0.md:110`.

```bash
cd forense/prereg-duelo-v2 && sha256sum \
  pipeline-L-adv1-m2.py carga_l_v1_1.py runner_l_cli.py L-spec-v1_2.json
```

| Archivo | `sha256` sellado por este acto |
|---|---|
| `pipeline-L-adv1-m2.py` | `a772a4bc48b724c33ea82fc41877594fa74b89eb267c2ca74401ed5fe3a45b1d` |
| `carga_l_v1_1.py` | `fb7be78a8ec076e91053fbd2798ea932d4c3ebfed8ed416bcc055fb9b69e4930` |
| `runner_l_cli.py` | `1ae70bc2b55e6aa129f742d1d3914e13b6b0f2e0b860109edfd2d650967f4086` |
| `L-spec-v1_2.json` | `bb49023ba71b5d04b4f8330ac6eed673eba0a7b7cb10c6c93df96c0311934885` (= `L-spec-v1_2.sha256`) |

El hash de `runner_l_cli.py` es **idéntico** al que `PAQUETE-L-v1_1.md` §1
declara — sellado por `ACTO MAESTRA33-E17 · L-ENMIENDA-CLI`, verificado sin
cambio en este acto. **No se copió el archivo a este directorio**: duplicarlo
crearía dos rutas con el mismo `sha256` y el test de hashes duplicados de
`tests/check.py` lo marcaría. Se referencia por ruta y hash, que es lo que la
compuerta necesita.

## 1-bis · Cómo se generó `L-spec-v1_2.json` (reproducible)

No se escribió un generador nuevo: se importó la **misma** plantilla mecánica
sellada (`derivar_pregunta_l` de `genera_l_spec_v1_1.py`) y se aplicó al marco
v1.2. Ningún texto por celda se redactó a mano.

```python
import csv, hashlib, importlib.util, json, sys
from pathlib import Path
D = Path("forense/prereg-duelo-v2").resolve()
spec = importlib.util.spec_from_file_location("g", D / "genera_l_spec_v1_1.py")
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)

with (D / "marco-M-sorteado-v1_2.tsv").open(encoding="utf-8") as fh:
    filas = [f for f in csv.DictReader(fh, delimiter="\t")
             if f["elegible_v1_1"].strip().upper().startswith("SI")]
# celdas = {id, conducta, universo, encuesta, ola, escala,
#           pregunta_L: g.derivar_pregunta_l(...)}  -> L-spec-v1_2.json
```

---

## 2 · Invariantes de la corrida

Idénticos a `PAQUETE-L-v1_1.md` §2 y a `prereg-corrida-v1_0.md` F2 — **no se
re-declaran con otro valor**: `temperatura=1.0` (no declarable por CLI, ver
§4), `k_corridas=8`, variantes `L-solo` y `L+corpus`, agregado mediana +
q10/q90/IQR, **descartes: CERO**, `version_declarada` = la cadena real que
devuelva el proveedor.

**Total: 14 celdas × 2 variantes × 8 corridas = 224 llamadas** (v1.1 eran 176).

Las 14 celdas, verbatim de `marco-M-sorteado-v1_2.tsv` (`elegible_v1_1 = SI`),
copiadas de `L-spec-v1_2.json`:

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
TRA-M-02 · paga_mordida                      · ENCUCI · 2020
TRA-M-03 · paga_mordida                      · ENCIG · 2013
TRA-M-07 · paga_mordida                      · ENCIG · 2021
```

Tres son nuevas del marco v1.2 (`FAM-M-05/06/07`, regla
`familia.seguro.volatilidad_ausencia_estado`) — primera vez que el lado `L` del
duelo recibe celdas de un dominio distinto de `tramite`/`civico`.

**`DIN-M-01` va incluida y no tiene `M`.** El emisor se negó a emitirla (ver
`forense/notas/2026-09-02-marco-M-v1_2-emite-m.md`). `L` y `R` sí se pueden
correr sobre ella; sólo el eje `M`-vs-`L` quedará incompleto hasta que mesa
resuelva F-DD sobre rangos de ola. **No se retira del paquete**: retirarla sería
reescribir un sorteo ya sellado.

---

## 3 · Ceguera del modelo

Cada llamada individual es la "sesión limpia". El modelo sólo ve el prompt que
`construir_prompt` (`pipeline-L-adv1-m2.py`) arma desde `SpecCelda` — nunca este
paquete, ni `L-spec-v1_2.json`, ni el marco, ni `corridas-R/`, ni
`milpa/tramite.yaml`.

Verificado en este acto sobre el prompt real de `FAM-M-05`: no contiene
`tramite.yaml`, `serie_olas`, `milpa/` ni ningún literal de `p`.

---

## 4 · Comando exacto (CLI, sin API key — firma `MAESTRA33-E17`)

Vigente el §4-bis de `PAQUETE-L-v1_1.md`: **sesión de `claude.ai`, cero
`ANTHROPIC_API_KEY`**. El §4 de API directa queda como registro histórico.

**Checklist de mesa antes de lanzar:**

- [ ] `claude auth status` muestra **sesión de `claude.ai`**, no API key. Si muestra API key → PARO.
- [ ] `claude --version` registrado (va en `version_declarada`).
- [ ] Los 4 hashes de §1 coinciden.
- [ ] El bloqueo de §6 está resuelto.

**Comando por corrida** (224 invocaciones), tal como `construir_comando_cli` lo arma:

```bash
claude -p \
  --model opus \
  --output-format json \
  --system-prompt "Responde únicamente a la pregunta. No uses herramientas ni consultes fuentes." \
  --tools "" \
  --max-turns 1 \
  "<prompt de la celda, de construir_prompt(), sin cambio>"
```

**Apuntar el runner a la spec v1.2 — sin editar ningún archivo sellado.**
`carga_l_v1_1.L_SPEC_JSON` es una constante de módulo; se sobreescribe en
runtime:

```python
import importlib.util, sys
from pathlib import Path
D = Path("forense/prereg-duelo-v2").resolve()
s = importlib.util.spec_from_file_location("runner_l_cli", D / "runner_l_cli.py")
r = importlib.util.module_from_spec(s); sys.modules["runner_l_cli"] = r
s.loader.exec_module(r)

r._CARGA.L_SPEC_JSON = D / "L-spec-v1_2.json"   # <- único cambio; NO se edita el .py
```

**Verificado en este acto**: con ese override, `_iter_plan()` produce **224
tuplas, 224 rutas únicas, sin una sola colisión**, 28 pares (celda, variante),
las 14 celdas cubiertas, y `construir_comando_cli` arma el comando correcto
(`claude -p … --tools "" …`). La maquinaria **sí** funciona a 14 celdas.

---

## 5 · Lo que este paquete cierra, específico de v1.2

Las tres celdas nuevas (`FAM-M-05/06/07`) vienen de una regla cuyo `serie_olas`
publica en `milpa/tramite.yaml` **la `p` medida de su propia ola**. Si el lado
`L` viera ese archivo, no estaría estimando: estaría leyendo la respuesta.

El paquete lo cierra por construcción, en dos capas:

1. **La `L-spec` sólo transporta seis campos** (`id`, `conducta`, `universo`,
   `encuesta`, `ola`, `escala`) — nunca `regla`, `razon_DD` ni ninguna columna
   con cifra.
2. **El `universo` de esas tres celdas se redactó deliberadamente sin una sola
   cita** de `milpa/tramite.yaml`, de `serie_olas` ni de la regla, porque
   `universo` viaja **verbatim** dentro de `pregunta_L`. Esa decisión se tomó en
   P1, al escribir el marco, no aquí — está declarada en
   `forense/notas/2026-09-02-marco-M-v1_2-sello.md`.

La sesión `L` corre fuera del proyecto y no ve el repo (D-iii), así que la capa
(2) es defensa en profundidad, no la única.

---

## 6 · BLOQUEO — `runner_l_cli.py` está dimensionado a 11 celdas

**Hallazgo de este acto, no defecto introducido por él.** El encargo asumió que
el paquete v1.2 podía usar `runner_l_cli.py` tal cual. No puede: el runner trae
la dimensión de v1.1 **cableada en cuatro puntos**.

```
runner_l_cli.py:188   total_esperado = 11 * len(VARIANTES) * K_CORRIDAS_SELLADO
runner_l_cli.py:190   assert n_rutas == 176, f"esperaba 176, obtuve {n_rutas}"
runner_l_cli.py:198   print("Total esperado: 176")
runner_l_cli.py:219   assert total == 176, f"total {total} != 176 esperado"
```

Con la spec v1.2 apuntada, `--dry-run` aborta:

```
AssertionError: 224 rutas construidas, esperaba 176
```

**El bloqueo es exclusivamente dimensional.** Todo lo demás ya se verificó en
verde a 14 celdas (§4). No hay ningún otro defecto que arreglar.

**No se parchó aquí, y la razón es de perímetro, no de dificultad.**
`runner_l_cli.py` está sellado por `ACTO MAESTRA33-E17` y **fuera del perímetro**
que este encargo declara; el encargo es explícito: *"Si te encuentras
escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y
saberlo vale más que el atajo."*

**Parche propuesto** (no aplicado), para el acto sucesor que tenga
`runner_l_cli.py` en su perímetro — deriva la dimensión de la spec en vez de
fijarla:

```python
# runner_l_cli.py:188-190
n_celdas = len(cargar_celdas_l_spec())
total_esperado = n_celdas * len(VARIANTES) * K_CORRIDAS_SELLADO
assert n_rutas == total_esperado, f"{n_rutas} rutas construidas, esperaba {total_esperado}"
# se ELIMINA el `assert n_rutas == 176` literal: es la misma comprobacion,
# congelada a un marco concreto. Igual en la linea 219 y en el print de 198.
```

Así el runner deja de romperse en cada versión del marco. Mientras tanto,
`PAQUETE-L-v1_2` queda **completo y sellado pero no lanzable**, y la fila
`L-v1_2` del tablero lo dice.

---

## 7 · Rutas de salida

`forense/prereg-duelo-v2/corridas-L/L-<id>-M__<variante>__<indice>.json`
(p. ej. `L-FAM-M-05-M__L-solo__01.json`), esquema idéntico al del piloto —
verificado contra los `corridas-L/` existentes por el propio `dry_run()`.
