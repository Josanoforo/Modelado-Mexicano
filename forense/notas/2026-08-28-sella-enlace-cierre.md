# Cierre · ACTO MAESTRA32-E1 · SELLA-ENLACE — 28/ago/2026

Encargo: `forense/encargos/2026-08-28-MAESTRA32-E1-SELLA-ENLACE.md` (dirección, maestra-32, archivado por `A.3` antes de ejecutar). Base: `main = 2953716` (merge de `PR #391`/`ACTO MAESTRA31-E10 · RECONCILIA-MOTOR`). Entorno **NUBE** (`cloud_default`), repo-only, sin red, sin API, sin microdato — declarado, no verificado con sonda de red porque este acto no la necesita.

**Firmas de mesa ejecutadas, las tres, sin decidir ninguna:** `M-ENLACE=A` (enlace identidad sellado), `M-176` (`FP-176` firmada verbatim), `M-AGREGA=(a)` (vector completo por ítem, sin agregación, para los 2 pares multi-ítem). `M-LECTURAS` llegó vacía y se deja vacía — no era de este acto llenarla.

**ADR usado: `ADR-220`.** Re-derivado por comando contra `canon/gobernanza-v1_15.md` (no tecleado): `grep -oE '^\*\*ADR-[0-9]+' canon/gobernanza-v1_15.md | grep -oE '[0-9]+' | sort -n | tail -1` → `219`, sin huecos (`sort -u | wc -l` → 219, mismo número) → candidato `220`, contiguo, sin PR en vuelo conocido que lo compita al escribir esto. Verificado tras escribir la entrada: `220` únicos, `0` huecos, `0` duplicados (script de verificación en la sección de "Comandos y universo" abajo).

---

## 1 · Resumen de lo hecho, paso por paso

0. Encargo `forense/encargos/2026-08-28-MAESTRA32-E1-SELLA-ENLACE.md` reconstruido y archivado íntegro, con las tres ranuras rellenas como llegaron firmadas y `M-LECTURAS` vacía.
1. Leídos íntegros `milpa/src/matriz.py`, `milpa/src/procedencia.py`, `milpa/src/clases.py` antes de tocar nada. Confirmado: `B` se construye desde `asignados_coeficiente.detalle` con clave compuesta `(generador, coeficiente)` (`matriz.cargar_B`), y la vía sancionada para que una entrada nueva entre al motor es el campo `clase:` por entrada, resuelto por prefijo más largo (`clasificar()` en `clases.py`, invocado desde `procedencia._recorrer`) — `BLOQUES_CON_CLASE_IMPLICITA` es la vía alterna para bloques SIN `clase:` por entrada (como `asignados_coeficiente`), y no aplica aquí porque cada entrada nueva trae su propio `clase:` copiado verbatim del origen. Confirmado por ejecución real, no solo lectura de código (ver §3).
2. `ADR-220` escrito en `canon/gobernanza-v1_15.md`, con las tres firmas citadas verbatim, el enlace identidad declarado, y las reservas de `ADR-57(a)`/`A-bis` en el cuerpo (no en nota al pie). Cabeceras de conteo (`gobernanza:2`, `estado-programa:27`, `estado-programa:105`) recifradas de `219` a `220`, con marca `{cita-historica}` en la transición anterior, mismo patrón que todos los ADR de esta serie.
3. Enmienda in situ, 28/ago/2026, en `canon/modelo-decision-v4_0.md` §2.2 — mismo patrón que la enmienda de `G1a` (`gobernanza` §4, `ADR-52 B`). No borra "los quince coeficientes son `ASIGNADO`"; declara desde `ADR-220` que 3 de los 15 tienen además `valor_ejecutable` en el ejecutable, rotulados `ASOCIACION-MEDIDA`, y que los 10 restantes quedan `SOLO-SIGNO·NO-COMPARABLE`.
4. Script Python (íntegro en §2 abajo) corrido UNA vez contra el archivo real. Deriva los 5 pares `RUTA-A` cruzando sección B (`rutas_estimabilidad_coeficiente.detalle`) contra sección A (`coeficientes_generador_medidos`), calcula `valor_ejecutable` para los 3 uni-valor (regla mecánica de sufijo `pp`), y escribe `coeficientes_generador_sellados:` al final de `milpa/procedencia.yaml`. Verificado por `diff`: 0 líneas removidas, 72 líneas añadidas al final, nada más tocado. Verificado por `yaml.safe_load` completo antes y después.
5. `milpa/src/matriz.py`: `cargar_B` construye las 15 celdas como siempre (fallback intacto) y luego sobre-escribe solo las celdas de pares con `valor_ejecutable` en la sección nueva. `milpa/src/procedencia.py`: comentario nuevo junto a `BLOQUES_CON_CLASE_IMPLICITA` documentando por qué el bloque nuevo NO entra ahí (cada entrada trae su propio `clase:`) — cero cambio de comportamiento, solo declaración. Ver el hallazgo del §4 (defecto preexistente que este paso descubrió, no causó).
6. `tests/test_matriz_sellados.py` nuevo — 6 pruebas, las tres particiones (3 con override real, 10 con fallback exacto, 2 multi-ítem que no se consumen). `6/6 ok`.
7. `python3 tests/check.py --baseline` → **VERDE** (ver §5).
8. Cascada: `forense/firmas-pendientes.tsv` (`FP-176`→`FIRMADA`, `FP-177`→`FIRMADA`, `FP-149` con nota añadida), `canon/estado-programa-v1_10.md` §L0 (recifrado, con la línea de coeficientes ejecutables 0→3 incluida en el mismo párrafo), `canon/registro-rotulos.tsv` (fila `MAESTRA32-E1` censada), `tests/check.py` `_T25_ARCHIVOS_CONOCIDOS` (el encargo, único archivo de este acto que trae el rótulo pelado — verificado con el mismo regex del test, ver §5), esta nota.

---

## 2 · El script del paso 4, íntegro

Ruta en este acto: `/tmp/claude-0/-home-user-Modelado-Mexicano/c0865581-155c-5b89-89e0-279531f0ee2a/scratchpad/sella_enlace_paso3.py` (scratchpad de la sesión, no versionado — se pega íntegro aquí porque el encargo lo exige, no vive en el repo).

```python
#!/usr/bin/env python3
"""ACTO MAESTRA32-E1 · SELLA-ENLACE -- Paso 3/4 del encargo.

Deriva, por yaml.safe_load (nunca grep/sed de subcadena), los 5 pares
RUTA-A de milpa/procedencia.yaml y escribe la seccion nueva
`coeficientes_generador_sellados:` AL FINAL del archivo, sin tocar
ninguna otra linea.

Regla de unidad (mecanica, declarada, sin adivinar):
  - si el numero trae sufijo "pp" -> valor_ejecutable = numero / 100
  - si no trae sufijo -> ya es proporcion, valor_ejecutable = numero
  - cualquier otro caso -> PARO (RuntimeError), no se adivina

Se ejecuta UNA vez contra el archivo real. Salida impresa aqui se pega
verbatim en forense/notas/2026-08-28-sella-enlace-cierre.md.
"""
import re
import sys

import yaml

RUTA = "milpa/procedencia.yaml"


def adr_num_actual(ruta_gobernanza="canon/gobernanza-v1_15.md"):
    """Maximo ADR existente en gobernanza -- re-derivado, no tecleado.

    Este script se corre DESPUES de que el paso 2 del encargo (ADR nuevo)
    ya escribio su entrada en gobernanza -- por eso el maximo actual ES
    el ADR de este acto, sin sumar 1. Si el maximo no coincide con lo que
    la nota de cierre declara, es señal de que el orden de pasos se violo.
    """
    with open(ruta_gobernanza, encoding="utf-8") as fh:
        texto = fh.read()
    nums = [int(n) for n in re.findall(r"^\*\*ADR-(\d+)", texto, re.M)]
    if not nums:
        raise RuntimeError("PARO: no se encontro ningun `**ADR-N` en gobernanza")
    return max(nums)


# Patron generico: PRIMER "NUMERO(pp)? [IC95% ...]" que aparezca en el
# texto. Para betas con desglose posterior (edad/dominio/...), el
# marginal siempre aparece primero en la prosa de origen -- verificado
# a mano contra las 3 entradas uni-valor antes de confiar en el primer
# match (ver nota de cierre).
_PAT_VALOR_IC = re.compile(
    r"([+-]?\d+(?:\.\d+)?)(pp)?\s*\[IC95%\s*([^\]]+)\]"
)


def extraer_valor_ic(texto):
    m = _PAT_VALOR_IC.search(texto)
    if not m:
        raise RuntimeError(f"PARO: no se encontro patron NUMERO(pp)?[IC95%...] en: {texto!r}")
    numero, sufijo_pp, ic = m.group(1), m.group(2), m.group(3)
    return numero, sufijo_pp, ic


def a_valor_ejecutable(numero_str, sufijo_pp):
    valor = float(numero_str)
    if sufijo_pp == "pp":
        return valor / 100.0
    if sufijo_pp is None:
        return valor
    raise RuntimeError(f"PARO: sufijo de unidad no reconocido: {sufijo_pp!r}")


def rotulo_marginal_o_condicional(clase_origen):
    low = clase_origen.lower()
    tiene_marginal = "marginal" in low
    tiene_condicional = "condicional" in low
    if tiene_condicional and not tiene_marginal:
        return "CONDICIONAL"
    if tiene_marginal and not tiene_condicional:
        return "MARGINAL"
    raise RuntimeError(
        f"PARO: clase de origen no declara marginal/condicional de forma "
        f"no ambigua: {clase_origen!r}"
    )


def resolver_clave_seccion_a(gen, coef, claves_a):
    """gen.coef (de la seccion B) -> clave real en la seccion A.

    Regla mecanica en dos pasos, ninguno inventado para esta ocasion:
      1) match directo `{gen}_{coef}` (cubre 4 de los 5 pares RUTA-A).
      2) si no hay match directo, unico candidato que empiece con
         `{gen}_{coef}_` (cubre el calificador extra de
         G4_confianza_institucional_justicia, ya resuelto por ADR-219/
         ACTO MAESTRA31-E10 contra canon/modelo-decision-v4_0.md:458).
    Si ninguna regla produce EXACTAMENTE un candidato, PARO.
    """
    directo = f"{gen}_{coef}"
    if directo in claves_a:
        return directo
    prefijo = f"{directo}_"
    candidatos = [k for k in claves_a if k.startswith(prefijo)]
    if len(candidatos) == 1:
        return candidatos[0]
    raise RuntimeError(
        f"PARO: no se pudo resolver la clave de seccion A para {gen}.{coef} "
        f"-- directo={directo!r} no existe y hay {len(candidatos)} "
        f"candidatos por prefijo: {candidatos}"
    )


def main():
    with open(RUTA, encoding="utf-8") as fh:
        texto_original = fh.read()
    crudo = yaml.safe_load(texto_original)

    if "coeficientes_generador_medidos" not in crudo:
        raise RuntimeError("PARO: no existe `coeficientes_generador_medidos` (seccion A) en el archivo")
    if "rutas_estimabilidad_coeficiente" not in crudo:
        raise RuntimeError("PARO: no existe `rutas_estimabilidad_coeficiente` (seccion B) en el archivo")

    sec_a = crudo["coeficientes_generador_medidos"]
    sec_b = crudo["rutas_estimabilidad_coeficiente"]["detalle"]

    ruta_a_pares = [(fila["gen"], fila["coef"]) for fila in sec_b if fila.get("ruta") == "RUTA-A"]
    if len(ruta_a_pares) != 5:
        raise RuntimeError(
            f"PARO: se esperaban 5 pares RUTA-A, se encontraron "
            f"{len(ruta_a_pares)}: {ruta_a_pares}"
        )
    print(f"[paso 1] pares RUTA-A encontrados ({len(ruta_a_pares)}): {ruta_a_pares}")

    adr_n = adr_num_actual()
    print(f"[paso 1] ADR ya sellado (paso 2 del encargo) para `escala:` = ADR-{adr_n}")

    claves_a = list(sec_a.keys())

    MULTI_ITEM = {("G1", "radio_confianza"), ("G4", "confianza_institucional")}

    salidas = []
    for gen, coef in ruta_a_pares:
        clave_a = resolver_clave_seccion_a(gen, coef, claves_a)
        entrada = sec_a[clave_a]
        clase_origen = entrada["clase"]
        beta_hat = entrada["beta_hat"]
        fuente_nota = f"coeficientes_generador_medidos.{clave_a}, 4/ago/2026"
        reserva = entrada.get("adr57_a", "").strip() if isinstance(entrada.get("adr57_a"), str) else ""

        if (gen, coef) in MULTI_ITEM:
            salida = {
                "gen": gen,
                "coef": coef,
                "clase": clase_origen,
                "valor_origen": beta_hat,
                "unidad_origen": (
                    "pp (por ítem, ver valor_origen)"
                    if "pp" in beta_hat
                    else "proporción (diferencia de proporciones, sin sufijo pp, por ítem)"
                ),
                "rotulo": "SELLADO-ESCALA·SIN-AGREGACION",
                "reserva": reserva,
                "fuente": fuente_nota,
            }
            print(f"[paso 1] {gen}.{coef} (<- {clave_a}): MULTI-ITEM, sin valor_ejecutable (M-AGREGA=(a))")
        else:
            numero, sufijo_pp, ic = extraer_valor_ic(beta_hat)
            valor_ejecutable = a_valor_ejecutable(numero, sufijo_pp)
            rotulo_tipo = rotulo_marginal_o_condicional(clase_origen)
            salida = {
                "gen": gen,
                "coef": coef,
                "clase": clase_origen,
                "valor_origen": beta_hat,
                "unidad_origen": "pp" if sufijo_pp == "pp" else "proporción (diferencia de proporciones, sin sufijo pp)",
                "valor_ejecutable": valor_ejecutable,
                "ic": f"IC95% {ic}",
                "escala": f"proporción ponderada [0,1], enlace identidad (ADR-{adr_n})",
                "rotulo": f"ASOCIACION-MEDIDA·{rotulo_tipo}",
                "reserva": reserva,
                "fuente": fuente_nota,
            }
            print(
                f"[paso 1] {gen}.{coef} (<- {clave_a}): valor_origen={numero}"
                f"{sufijo_pp or ''} -> valor_ejecutable={valor_ejecutable!r} "
                f"({rotulo_tipo})"
            )
        salidas.append(salida)

    n_con_ejecutable = sum(1 for s in salidas if "valor_ejecutable" in s)
    n_multi = sum(1 for s in salidas if "valor_ejecutable" not in s)
    print(f"[paso 1] total: {len(salidas)} pares -- {n_con_ejecutable} con valor_ejecutable, {n_multi} multi-item sellados sin agregar")
    if n_con_ejecutable != 3 or n_multi != 2:
        raise RuntimeError(
            f"PARO: se esperaban 3 uni-valor + 2 multi-item, se obtuvieron "
            f"{n_con_ejecutable} + {n_multi}"
        )

    banner = (
        "\n"
        "# ══════════════════════════════════════════════════════════════════\n"
        "# COEFICIENTES DE GENERADOR SELLADOS · ACTO MAESTRA32-E1 · SELLA-ENLACE\n"
        f"# · 28/ago/2026 · ADR-{adr_n} · firmas de mesa M-ENLACE=A / M-176 /\n"
        "# M-AGREGA=(a) (ver forense/encargos/2026-08-28-MAESTRA32-E1-SELLA-\n"
        "# ENLACE.md y forense/firmas-pendientes.tsv FP-176/FP-177).\n"
        "#\n"
        "# Los 5 pares RUTA-A de rutas_estimabilidad_coeficiente.detalle,\n"
        "# cruzados contra coeficientes_generador_medidos (seccion A). NO\n"
        "# reemplaza ni edita asignados_coeficiente.detalle -- los valores\n"
        "# ASIGNADO de esa seccion siguen siendo lo que el modelo declara;\n"
        "# esta seccion es el override que milpa/src/matriz.py consulta\n"
        "# primero cuando un par trae `valor_ejecutable`.\n"
        "#\n"
        "# Rotulo ASOCIACION-MEDIDA (M-176, firma verbatim en el ADR citado\n"
        "# arriba): estos beta_hat NO son coeficientes identificados --\n"
        "# ADR-57(a) ya establecio, para G1/G3, que condicionar revierte el\n"
        "# signo del marginal en la mayoria de las celdas; esta firma trae a\n"
        "# G4 al mismo tratamiento. Los 2 pares multi-item quedan\n"
        "# SELLADO-ESCALA·SIN-AGREGACION (M-AGREGA=(a)): vector integro por\n"
        "# item, sin valor_ejecutable, no se consumen en matriz.py.\n"
        "# ══════════════════════════════════════════════════════════════════\n"
    )
    bloque_yaml = yaml.safe_dump(
        {"coeficientes_generador_sellados": salidas},
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
        width=100000,  # una linea por escalar largo -- mismo estilo que el resto del archivo
    )

    texto_nuevo = texto_original
    if not texto_nuevo.endswith("\n"):
        texto_nuevo += "\n"
    texto_nuevo += banner + bloque_yaml

    # Verificacion antes de escribir: el texto ORIGINAL no cambia ni un byte
    # salvo el apendice.
    assert texto_nuevo.startswith(texto_original), "PARO: el prefijo original se alteró"

    with open(RUTA, "w", encoding="utf-8") as fh:
        fh.write(texto_nuevo)

    # Re-verificacion: el archivo completo sigue siendo yaml.safe_load-able.
    with open(RUTA, encoding="utf-8") as fh:
        crudo_final = yaml.safe_load(fh.read())
    assert "coeficientes_generador_sellados" in crudo_final
    assert len(crudo_final["coeficientes_generador_sellados"]) == 5
    print(f"[paso 2] {RUTA} reescrito -- yaml.safe_load OK, "
          f"{len(crudo_final['coeficientes_generador_sellados'])} entradas en la seccion nueva")
    print(f"[paso 2] lineas originales: {texto_original.count(chr(10))} -- "
          f"lineas nuevas totales: {texto_nuevo.count(chr(10))}")


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
```

## 3 · Su salida real (una sola corrida, contra el archivo real)

```
[paso 1] pares RUTA-A encontrados (5): [('G1', 'confianza_institucional'), ('G1', 'radio_confianza'), ('G3', 'familismo_apoyo'), ('G4', 'exposicion_violencia'), ('G4', 'confianza_institucional')]
[paso 1] ADR ya sellado (paso 2 del encargo) para `escala:` = ADR-220
[paso 1] G1.confianza_institucional (<- G1_confianza_institucional): valor_origen=-0.0645 -> valor_ejecutable=-0.0645 (MARGINAL)
[paso 1] G1.radio_confianza (<- G1_radio_confianza): MULTI-ITEM, sin valor_ejecutable (M-AGREGA=(a))
[paso 1] G3.familismo_apoyo (<- G3_familismo_apoyo): valor_origen=+0.0279 -> valor_ejecutable=0.0279 (MARGINAL)
[paso 1] G4.exposicion_violencia (<- G4_exposicion_violencia): valor_origen=+16.614pp -> valor_ejecutable=0.16614 (CONDICIONAL)
[paso 1] G4.confianza_institucional (<- G4_confianza_institucional_justicia): MULTI-ITEM, sin valor_ejecutable (M-AGREGA=(a))
[paso 1] total: 5 pares -- 3 con valor_ejecutable, 2 multi-item sellados sin agregar
[paso 2] milpa/procedencia.yaml reescrito -- yaml.safe_load OK, 5 entradas en la seccion nueva
[paso 2] lineas originales: 1187 -- lineas nuevas totales: 1259
```

Antes de esta corrida real se corrió el mismo script contra una copia (`cp milpa/procedencia.yaml` + `cp canon/gobernanza-v1_15.md` con un `ADR-220` de mentira anexado solo para el ensayo) para verificar la lógica sin arriesgar el archivo real — la copia de ensayo se descartó, nunca se commiteó, y el script no cambió entre el ensayo y la corrida real salvo el arreglo de un espacio final en el banner (cosmético, verificado con `diff` contra la versión de ensayo).

---

## 4 · Hallazgo declarado — defecto preexistente, fuera de perímetro

Al escribir el test nuevo se intentó, primero, construir `Procedencia` vía `P.cargar()` (la ruta normal). **`P.cargar()` falla hoy, en `HEAD = 2953716`, ANTES de que este acto tocara nada**, con `ClaseDesconocida: ningún prefijo conocido casa con 'EVIDENCIA_EXPERIMENTAL_TERCEROS'` — la clase de la octava clase de procedencia (`EVIDENCIA_EXPERIMENTAL_TERCEROS`, sellada por `ADR-204` (`ACTO SELLA-FP164-OCTAVA`), 26/ago/2026) nunca se agregó a `Clase` en `milpa/src/clases.py`. Verificado con `git stash` (revertir a `HEAD` limpio) + correr `tests/test_motor_procedencia.py`, `tests/test_motor_matriz.py` y `tests/test_motor_clases.py` uno por uno: **los tres fallan igual, con el mismo traceback, en el árbol sin ningún cambio de este acto.**

Esto es un defecto real, pero **fuera del perímetro de `ACTO MAESTRA32-E1`**: `clases.py` no está en su lista de archivos, y el propio encargo prohíbe improvisar fuera de perímetro. Además, `tests/check.py` (la suite que sí gobierna verde/rojo) **nunca invoca** `test_motor_*.py` — son scripts independientes, no parte de su batería de T-tests — así que este defecto no mueve la línea base de `check.py` en ninguna dirección. Se declara aquí, con prominencia, para que quede escrito antes de que alguien lo redescubra como "regresión nueva": no lo es.

`milpa/src/matriz.py:cargar_B` nunca llamó a `P.cargar()` — solo lee `procedencia.crudo` — así que el defecto no afecta el override de este acto. El test nuevo (`tests/test_matriz_sellados.py`) construye `Procedencia` a mano (`yaml.safe_load` directo + `P.Procedencia(crudo=crudo)`), evitando la ruta rota, documentado en su propio docstring.

Verificado por separado, aislando `_recorrer` solo sobre el bloque nuevo (sin atravesar el resto del árbol, donde vive el defecto): produce exactamente 5 `Entrada`, las cinco con `clase=Clase.MEDIDO_BETA` — confirma que la vía per-entrada (`clase:` copiado verbatim, resuelto por prefijo) SÍ funciona para la sección nueva, sin ningún cambio de código en `procedencia.py` más allá del comentario documental.

---

## 5 · Comandos y universo (A.13 — todo negativo con cuántos archivos examinó)

```
$ grep -oE '^\*\*ADR-[0-9]+' canon/gobernanza-v1_15.md | grep -oE '[0-9]+' | sort -n | tail -1
220
$ grep -oE '^\*\*ADR-[0-9]+' canon/gobernanza-v1_15.md | grep -oE '[0-9]+' | sort -u | wc -l
220
```
Universo: 1 archivo (`canon/gobernanza-v1_15.md`), 220 líneas `**ADR-N` encontradas, 220 únicas, 0 huecos, 0 duplicados (verificado con el mismo script Python usado para T15, corrido a mano).

```
$ python3 -c "import re,glob; ..."   # script de verificación de citas '<N> ADR' vivas
bad count: 0
```
Universo: 8 archivos (`canon/*.md`, `ls canon/*.md | wc -l` → 8), cero citas vivas de "N ADR" que no coincidan con 220 (las históricas, marcadas `{cita-historica}`, se excluyen por diseño del propio test — 27 ocurrencias históricas contadas, todas exentas).

```
$ python3 tests/test_matriz_sellados.py
```
`6/6 ok, 0 saltadas` — universo: `milpa/procedencia.yaml` real (1259 líneas, 20 claves de primer nivel, 5 entradas en `coeficientes_generador_sellados`), `asignados_coeficiente.detalle` real (6 filas-generador, 15 pares).

```
$ python3 tests/check.py --baseline
```
`19 FAIL · 134 WARN` — **LÍNEA BASE: VERDE, nada nuevo frente a `tests/baseline.json`** (`HEAD` congelado `e24d033ed3c095f1e81c2fbb8248f108e9d3ef65`; 5 entradas de la línea base ya no aparecen, mejora no forzada). Antes de la corrida final, una corrida intermedia mostró 2 entradas nuevas (`T22`/`T25`, ambas del encargo archivado) — corregidas (fila en `firmas-pendientes.tsv` citando el encargo en su columna `dónde`, y el encargo censado en `_T25_ARCHIVOS_CONOCIDOS`), re-corrido, verde.

```
$ diff <(git show HEAD:forense/firmas-pendientes.tsv) forense/firmas-pendientes.tsv   # vía csv, no línea a línea
```
173 filas antes, 173 filas después, exactamente 3 cambiadas (`FP-149`, `FP-176`, `FP-177`) — verificado por comparación estructural fila por fila con `csv.reader`, no por `diff` de texto (el TSV tiene campos con saltos de línea embebidos que confunden un `diff` línea a línea).

```
$ python3 -c "import yaml; d=yaml.safe_load(open('milpa/procedencia.yaml')); ..."
```
`milpa/procedencia.yaml` completo sigue siendo `yaml.safe_load`-able tras el apéndice: 20 claves de primer nivel, `coeficientes_generador_sellados` con 5 entradas.

**Conteo final (universo declarado, 15 pares generador×coeficiente, mismo denominador que `ADR-219`/`forense/estado-motor-v1_0.md`):**

| Categoría | N | Detalle |
|---|---|---|
| Con `valor_ejecutable` escrito (0→3) | 3 | `G1.confianza_institucional -0.0645` · `G3.familismo_apoyo 0.0279` · `G4.exposicion_violencia 0.16614` |
| `SELLADO-ESCALA·SIN-AGREGACION` (sin `valor_ejecutable`) | 2 | `G1.radio_confianza` (3 ítems) · `G4.confianza_institucional` (7 ítems, vía `G4_confianza_institucional_justicia`) |
| `SOLO-SIGNO·NO-COMPARABLE`, sin cambio | 10 | el resto — historia intacta, ningún campo tocado |
| **Suma** | **15** | cuadra con `rutas_estimabilidad_coeficiente.detalle` (verificado) |

`FP-176`/`FP-177`: `ABIERTA` → `FIRMADA`, ambas. `FP-149`: sigue `FIRMADA`, gana nota añadida en `ejecutada_en` sin borrar el texto previo.

---

## 6 · Ninguna ambigüedad real encontrada que requiriera PARO

Los cinco pares `RUTA-A` casaron limpio contra la sección A (cuatro por nombre directo, uno por el único candidato de prefijo — el mismo caso que `ADR-219` ya había resuelto). Las tres reglas de unidad (sufijo `pp` vs. sin sufijo) resolvieron sin ambigüedad en los tres pares uni-valor. El único hallazgo digno de PARO fue el defecto preexistente de `clases.py` (§4), que no bloquea ningún paso de este acto porque vive fuera de la ruta que este acto usa (`cargar_B` no pasa por `P.cargar()`).

## 7 · Lo que este acto NO hizo

No estimó nada nuevo, no re-corrió ninguna medición del 4/ago, no tocó la sección A original de `procedencia.yaml` ni ningún valor `ASIGNADO` de `asignados_coeficiente.detalle` (verificado: 0 líneas removidas en el `diff`), no agregó los 2 pares multi-ítem, no tocó `clases.py` (el hallazgo del §4 se declara, no se corrige), no usó red ni API, no adjudicó `M-LECTURAS` (queda vacía).
