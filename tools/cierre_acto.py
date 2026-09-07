#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools/cierre_acto.py -- preflight + reconciliador mecánico del cierre de
un acto (ACTO AUTOMATIZA-1-E3 · CIERRE-MECANICO, 7/sep/2026,
`forense/encargos/2026-09-07-AUTOMATIZA-1-E3-CIERRE-MECANICO.md`, ELEMENTO 3).

QUÉ ES Y QUÉ NO ES. Un preflight + reconciliador de conteos mecánicos, no
un autor de gobernanza. `python3 tools/cierre_acto.py` = dry-run por
defecto (Fase A, nunca escribe). `--aplica` = Fase B, reconciliación
mecánica segura y todo-o-nada.

Principio de diseño: el tool no incrementa por adelantado un ADR que no
existe. Primero el humano crea la entrada ADR, la anotación L0, el rótulo
si corresponde, `## CONSUMIDO` cuando corresponda. Después el tool
reconcilia los derivados mecánicos (cabecera de gobernanza, conteo de L0,
fila `gobernanza` de la tabla de nombres estables de `estado-programa`)
contra la realidad del árbol -- ya con la entrada humana escrita, el ADR
real es mayor que lo que esos tres contadores todavía declaran, y el tool
sólo los sube al valor real. Idempotente: correrlo dos veces seguidas sin
cambios en el árbol no escribe nada la segunda vez.

Tercer contador (`ACTO AUTOMATIZA-2-B · CIERRA-TERCER-CONTADOR`,
`forense/encargos/2026-09-07-AUTOMATIZA-2-B-CIERRA-TERCER-CONTADOR.md`):
la fila `| **\`gobernanza\`** | \`gobernanza-v1.15.md\` | N ADR, protocolo
de cambio |` de `canon/estado-programa-v1_12.md` §0 es una tercera cita
viva del mismo número, que ya requirió recifrado manual repetido antes de
esta pieza. `canon/estado-programa-v1_12.md` se lee UNA vez y se escribe
UNA vez: las sustituciones de `L0` y de la tabla se aplican en secuencia
sobre el mismo buffer en memoria, nunca en dos ciclos independientes de
read/write.

Reutiliza `tools/estado_comun.py` (`es_abierta`, `lee_tablero`,
`ramas_remotas_presentes`, `adr_max`, `fp_max`) -- no las reimplementa.

Escritura atómica (`--aplica`): cada archivo objetivo se escribe primero a
un temporal en el mismo directorio y se confirma con `os.replace()` --
un proceso interrumpido a medio camino nunca deja un archivo real con
contenido parcial. Los dos temporales se preparan ANTES de confirmar
ninguno, así que una interrupción mientras se preparan no toca ningún
archivo real; si el segundo `os.replace()` falla después de que el
primero ya confirmó, el reporte lo dice explícitamente en vez de afirmar
"0 archivos escritos".

Fuera de perímetro (decide el humano, no este tool): redactar el ADR,
insertar la anotación L0, decidir el significado de un rótulo nuevo,
escribir `que_significa`/`donde_vive` de `canon/registro-rotulos.tsv`,
firmar FP, decidir pendientes, fusionar/aprobar el PR, crear encargos,
recifrar `tests/baseline.json`.

Uso:
    python3 tools/cierre_acto.py                    # Fase A, dry-run
    python3 tools/cierre_acto.py --encargo <ruta>    # + reporta ## CONSUMIDO de ese archivo
    python3 tools/cierre_acto.py --aplica            # Fase B, todo-o-nada
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile

import estado_comun as EC

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _ruta_gobernanza(raiz):
    return os.path.join(raiz, "canon", "gobernanza-v1_15.md")


def _ruta_estado(raiz):
    return os.path.join(raiz, "canon", "estado-programa-v1_12.md")


def _ruta_registro_rotulos(raiz):
    return os.path.join(raiz, "canon", "registro-rotulos.tsv")


def _corre(cmd, raiz=None, timeout=60):
    """Ejecuta y devuelve (rc, stdout, stderr). Nunca lanza: un comando que
    no corre es un hallazgo del preflight, no una caída del tool."""
    try:
        p = subprocess.run(cmd, cwd=raiz or RAIZ, capture_output=True, text=True,
                           timeout=timeout)
        return p.returncode, (p.stdout or ""), (p.stderr or "")
    except FileNotFoundError as e:
        return 127, "", f"comando no encontrado: {e}"
    except subprocess.TimeoutExpired:
        return 124, "", f"tiempo agotado ({timeout}s)"


def _leer(ruta):
    with open(ruta, encoding="utf-8") as f:
        return f.read()


# ─────────────────────────────────────────────────────────────────
# Fase A · inspección (nunca escribe)
# ─────────────────────────────────────────────────────────────────

def inspeccion_git(raiz=RAIZ):
    _, head, _ = _corre(["git", "rev-parse", "HEAD"], raiz)
    _, head_asunto, _ = _corre(["git", "log", "-1", "--format=%s", "HEAD"], raiz)
    _, origin_main, _ = _corre(["git", "rev-parse", "origin/main"], raiz)
    rc_anc, _, _ = _corre(["git", "merge-base", "--is-ancestor", "origin/main", "HEAD"], raiz)
    ramas_todas, fuente = EC.ramas_remotas_presentes(raiz)
    ramas = [r for r in ramas_todas if r and r != "main"]
    return {
        "head": head.strip(),
        "head_asunto": head_asunto.strip(),
        "origin_main": origin_main.strip(),
        "head_deriva_de_main": rc_anc == 0,
        "ramas_presentes": ramas,
        "ramas_fuente": fuente,
    }


def _rama_trae_adr(rama, candidato, raiz=RAIZ):
    """True/False si se puede verificar; None si los objetos de esa rama no
    están accesibles localmente sin un fetch nuevo -- nunca se afirma
    ausencia sin evidencia (una rama puede existir sin haber redactado
    aún su ADR, o sin que este clon tenga sus objetos)."""
    ref = f"refs/remotes/origin/{rama}"
    rc, salida, _ = _corre(["git", "show", f"{ref}:canon/gobernanza-v1_15.md"], raiz)
    if rc != 0:
        return None
    return f"**ADR-{candidato}" in salida


def inspeccion_adr(ramas_presentes, raiz=RAIZ):
    real = EC.adr_max(raiz)
    candidato = real + 1
    por_rama = {r: _rama_trae_adr(r, candidato, raiz) for r in ramas_presentes}
    return {"real": real, "candidato": candidato, "candidato_en_rama": por_rama}


def inspeccion_fp(raiz=RAIZ):
    real = EC.fp_max(raiz)
    _, filas, _ = EC.lee_tablero(raiz)
    abiertas = [f.get("id", "?") for f in (filas or []) if EC.es_abierta(f.get("estado", ""))]
    return {"max": real, "abiertas": abiertas}


# Ancla de la cabecera: "### `gobernanza` · **v1.15** · <fecha> · **N ADR**"
CABECERA_ADR_RE = re.compile(r"(### `gobernanza`.*?\*\*)(\d+)( ADR\*\*)")
# Ancla de L0: primeras palabras fijas de la línea + el conteo, antes de la
# primera anotación "*(...)*" -- nunca se toca lo que sigue.
L0_ADR_RE = re.compile(r"(\*\*L0 · Gobierno — completo y al día\.\*\* )(\d+)( ADR)")
# Ancla de la fila `gobernanza` de la tabla de nombres estables (§0 de
# `estado-programa`). La celda cita el nombre COSMÉTICO con punto
# (`gobernanza-v1.15.md`, ADR-36) -- nunca el filename físico con guion
# bajo (`gobernanza-v1_15.md`) -- y no se ancla por número de línea.
TABLA_ADR_RE = re.compile(
    r"(\| \*\*`gobernanza`\*\* \| `gobernanza-v1\.15\.md` \| )(\d+)( ADR, protocolo de cambio \|)"
)


def inspeccion_gobernanza(adr_real, raiz=RAIZ):
    gob = _leer(_ruta_gobernanza(raiz))
    est = _leer(_ruta_estado(raiz))
    anclas_cab = list(CABECERA_ADR_RE.finditer(gob))
    anclas_l0 = list(L0_ADR_RE.finditer(est))
    anclas_tabla = list(TABLA_ADR_RE.finditer(est))
    cabecera_declara = int(anclas_cab[0].group(2)) if len(anclas_cab) == 1 else None
    l0_declara = int(anclas_l0[0].group(2)) if len(anclas_l0) == 1 else None
    tabla_declara = int(anclas_tabla[0].group(2)) if len(anclas_tabla) == 1 else None
    return {
        "adr_real": adr_real,
        "cabecera_declara": cabecera_declara,
        "cabecera_anclas": len(anclas_cab),
        "l0_declara": l0_declara,
        "l0_anclas": len(anclas_l0),
        "tabla_declara": tabla_declara,
        "tabla_anclas": len(anclas_tabla),
    }


def inspeccion_rotulo(raiz=RAIZ):
    """Best-effort: el rótulo esperado se deriva del nombre de la rama
    actual (no hay otra fuente mecánica confiable sin que el llamador lo
    declare) -- se reporta, nunca se decide con esto."""
    _, rama, _ = _corre(["git", "branch", "--show-current"], raiz)
    rama = rama.strip()
    rotulo_esperado = rama.split("/")[-1].upper() if rama else None
    ya_censado = False
    ruta_registro = _ruta_registro_rotulos(raiz)
    if rotulo_esperado and os.path.exists(ruta_registro):
        ya_censado = rotulo_esperado in _leer(ruta_registro)
    return {"rama": rama, "rotulo_esperado": rotulo_esperado, "ya_censado": ya_censado}


_MARCADOR_CONSUMIDO = re.compile(r"^## CONSUMIDO\s*$", re.M)


def inspeccion_consumido(ruta_encargo):
    """Presencia/ausencia de la sección `## CONSUMIDO` -- ancla de LÍNEA
    (`^## CONSUMIDO$`, mismo patrón que `digesto_tramite.py::seccion_d`,
    `grep -L '^## CONSUMIDO'`), no una búsqueda de substring en cualquier
    parte del texto: un encargo puede mencionar la frase en prosa (como
    éste mismo, al describir el mecanismo) sin que eso sea la sección."""
    if not ruta_encargo:
        return {"ruta": None, "estado": "no especificado (--encargo)"}
    ruta_abs = ruta_encargo if os.path.isabs(ruta_encargo) else os.path.join(RAIZ, ruta_encargo)
    if not os.path.exists(ruta_abs):
        return {"ruta": ruta_encargo, "estado": "ARCHIVO_NO_EXISTE"}
    presente = bool(_MARCADOR_CONSUMIDO.search(_leer(ruta_abs)))
    return {"ruta": ruta_encargo, "estado": "PRESENTE" if presente else "AUSENTE"}


def corre_baseline(raiz=RAIZ):
    rc, out, err = _corre([sys.executable, "tests/check.py", "--baseline"], raiz, timeout=300)
    salida = (out + err)
    lineas = [l for l in salida.splitlines() if l.strip()]
    verde = "LÍNEA BASE: VERDE" in salida
    return {"codigo": rc, "verde": verde, "ultimas_lineas": lineas[-8:]}


def fase_a(raiz=RAIZ, ruta_encargo=None, corre_suite=True):
    git = inspeccion_git(raiz)
    adr = inspeccion_adr(git["ramas_presentes"], raiz)
    fp = inspeccion_fp(raiz)
    gob = inspeccion_gobernanza(adr["real"], raiz)
    rotulo = inspeccion_rotulo(raiz)
    consumido = inspeccion_consumido(ruta_encargo)
    suite = corre_baseline(raiz) if corre_suite else None

    print("=== FASE A · INSPECCIÓN (dry-run, nunca escribe) ===")
    print()
    print("GIT")
    print(f"  HEAD: {git['head']} {git['head_asunto']!r}")
    print(f"  origin/main: {git['origin_main']}")
    print(f"  HEAD deriva de origin/main: {git['head_deriva_de_main']}")
    print(f"  Ramas remotas presentes (≠ main): {git['ramas_presentes'] or '(ninguna)'}")
    print(f"    fuente: {git['ramas_fuente']}")
    print("    NOTA: una rama presente no implica PR abierto ni trabajo sin fusionar.")
    print()
    print("ADR")
    print(f"  Real (comando de la casa): {adr['real']}")
    print(f"  Candidato: {adr['candidato']}")
    if adr["candidato_en_rama"]:
        print("  ¿Candidato ya redactado en alguna rama remota accesible?")
        for rama, estado in adr["candidato_en_rama"].items():
            txt = "SI" if estado is True else "NO" if estado is False else "NO-VERIFICABLE (objetos no accesibles localmente sin fetch)"
            print(f"    {rama}: {txt}")
    print()
    print("FP")
    print(f"  Máximo: {fp['max']}")
    print(f"  Filas ABIERTA ({len(fp['abiertas'])}): {', '.join(fp['abiertas']) or '(ninguna)'}")
    print()
    print("GOBERNANZA (conteos)")
    print(f"  ADR reales: {gob['adr_real']}")
    print(f"  Cabecera declara: {gob['cabecera_declara']} (canon/gobernanza-v1_15.md, {gob['cabecera_anclas']} ancla(s))")
    print(f"  L0 declara: {gob['l0_declara']} (canon/estado-programa-v1_12.md, {gob['l0_anclas']} ancla(s))")
    print(f"  Tabla estado declara: {gob['tabla_declara']} (canon/estado-programa-v1_12.md, {gob['tabla_anclas']} ancla(s))")
    reconciliar = []
    if gob["cabecera_anclas"] == 1 and gob["cabecera_declara"] != gob["adr_real"]:
        reconciliar.append(f"gobernanza {gob['cabecera_declara']}→{gob['adr_real']}")
    if gob["l0_anclas"] == 1 and gob["l0_declara"] != gob["adr_real"]:
        reconciliar.append(f"L0 {gob['l0_declara']}→{gob['adr_real']}")
    if gob["tabla_anclas"] == 1 and gob["tabla_declara"] != gob["adr_real"]:
        reconciliar.append(f"tabla estado {gob['tabla_declara']}→{gob['adr_real']}")
    print(f"  Reconciliación necesaria: {' · '.join(reconciliar) if reconciliar else 'ninguna (ya coinciden)'}")
    print()
    print("RÓTULO DEL ACTO (best-effort, derivado de la rama actual)")
    print(f"  Rama: {rotulo['rama']!r} -> esperado: {rotulo['rotulo_esperado']}")
    print(f"  ¿Ya en canon/registro-rotulos.tsv?: {'SI' if rotulo['ya_censado'] else 'AUSENTE'}")
    if rotulo["rotulo_esperado"] and not rotulo["ya_censado"]:
        print(f"  RÓTULO: {rotulo['rotulo_esperado']} · registro: AUSENTE · "
              f"requiere humano: que_significa = ? · donde_vive = ?")
    print()
    print("## CONSUMIDO")
    print(f"  Encargo: {consumido['ruta']} -> {consumido['estado']}")
    print()
    if suite is not None:
        print("SUITE")
        print("  Comando: python3 tests/check.py --baseline")
        print(f"  Código: {suite['codigo']} -- {'VERDE' if suite['verde'] else 'ROJO/NO-VERDE'}")
        print("  Últimas líneas:")
        for l in suite["ultimas_lineas"]:
            print(f"    {l}")
        print()
    print("REQUIERE JUICIO HUMANO (siempre, este tool no lo hace)")
    print("  - Redactar el texto del ADR (motivo, incisos, qué cierra/abre)")
    print("  - Insertar la anotación nueva en L0 (antes de la anterior)")
    print("  - Decidir el significado de un rótulo nuevo (que_significa/donde_vive)")
    print("  - Firmar filas de FP")
    print("  - Decisiones de mesa sobre pendientes")
    print("  - Un T25 nuevo en la suite (rótulo pelado): decidir prefijo o censarlo")
    print("  - Fusionar/aprobar el PR")
    return {"git": git, "adr": adr, "fp": fp, "gobernanza": gob, "rotulo": rotulo,
            "consumido": consumido, "suite": suite}


# ─────────────────────────────────────────────────────────────────
# Fase B · --aplica (todo-o-nada, sólo cabecera + dígitos de L0)
# ─────────────────────────────────────────────────────────────────

def _solo_digitos_cambiaron(original, candidato, patron):
    """True si `candidato` difiere de `original` EXACTAMENTE en el grupo 2
    (los dígitos) de la primera coincidencia de `patron`, y en nada más."""
    m_orig = patron.search(original)
    m_new = patron.search(candidato)
    if not m_orig or not m_new:
        return False
    return (original[:m_orig.start(2)] == candidato[:m_new.start(2)] and
            original[m_orig.end(2):] == candidato[m_new.end(2):])


def _prepara_temp(ruta, contenido):
    """Escribe `contenido` en un archivo temporal en el MISMO directorio que
    `ruta` (requisito de `os.replace` para que el rename sea intra-
    filesystem, luego atómico) y devuelve su ruta -- todavía no toca
    `ruta`. Separar "preparar" de "confirmar" (`_confirma_temp`) deja
    listos los dos archivos objetivo ANTES de reemplazar ninguno: un
    proceso interrumpido mientras se preparan los temporales no toca
    ningún archivo real."""
    directorio = os.path.dirname(ruta) or "."
    fd, ruta_tmp = tempfile.mkstemp(dir=directorio, prefix=".cierre_acto-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(contenido)
    except BaseException:
        try:
            os.remove(ruta_tmp)
        except OSError:
            pass
        raise
    return ruta_tmp


def _confirma_temp(ruta_tmp, ruta):
    """Reemplazo atómico (`os.replace`): `ruta` nunca queda con contenido
    parcial -- o el viejo completo, o el nuevo completo."""
    os.replace(ruta_tmp, ruta)


def fase_b_aplica(raiz=RAIZ):
    ruta_gob = _ruta_gobernanza(raiz)
    ruta_est = _ruta_estado(raiz)
    adr_real = EC.adr_max(raiz)
    gob_texto = _leer(ruta_gob)
    # canon/estado-programa-v1_12.md se lee UNA sola vez; L0 y la fila de
    # tabla se reconcilian en secuencia sobre el mismo buffer en memoria
    # (nunca dos ciclos independientes de read/write) y el archivo se
    # escribe UNA sola vez, al final, con las dos correcciones ya aplicadas.
    est_texto = _leer(ruta_est)

    anclas_cab = list(CABECERA_ADR_RE.finditer(gob_texto))
    anclas_l0 = list(L0_ADR_RE.finditer(est_texto))
    anclas_tabla = list(TABLA_ADR_RE.finditer(est_texto))

    problemas = []
    if len(anclas_cab) != 1:
        problemas.append(f"cabecera de gobernanza: {len(anclas_cab)} ancla(s) (se requiere exactamente 1)")
    if len(anclas_l0) != 1:
        problemas.append(f"L0: {len(anclas_l0)} ancla(s) (se requiere exactamente 1)")
    if len(anclas_tabla) != 1:
        problemas.append(f"tabla estado: {len(anclas_tabla)} ancla(s) (se requiere exactamente 1)")
    if problemas:
        print("APLICACION_ABORTADA · 0 archivos escritos")
        for p in problemas:
            print(f"  · {p}")
        return 1

    cab_actual = int(anclas_cab[0].group(2))
    l0_actual = int(anclas_l0[0].group(2))
    tabla_actual = int(anclas_tabla[0].group(2))

    if cab_actual == adr_real and l0_actual == adr_real and tabla_actual == adr_real:
        print(f"sin cambios -- cabecera, L0 y tabla estado ya declaran {adr_real}, igual al real")
        return 0

    def _sustituye(texto, m, valor):
        return texto[:m.start(2)] + str(valor) + texto[m.end(2):]

    gob_candidato = _sustituye(gob_texto, anclas_cab[0], adr_real) if cab_actual != adr_real else gob_texto

    # L0 primero, tabla después -- ambas sobre el mismo buffer encadenado.
    # Cada paso se valida contra el buffer que lo precede inmediatamente
    # (no contra est_texto original en el segundo paso), porque el patrón
    # de la tabla debe re-ubicarse en el texto YA modificado por L0.
    est_tras_l0 = _sustituye(est_texto, anclas_l0[0], adr_real) if l0_actual != adr_real else est_texto
    if est_tras_l0 != est_texto and not _solo_digitos_cambiaron(est_texto, est_tras_l0, L0_ADR_RE):
        print("APLICACION_ABORTADA · 0 archivos escritos")
        print("  · L0: el cambio construido no se limita a los dígitos del conteo")
        return 1

    anclas_tabla_tras_l0 = list(TABLA_ADR_RE.finditer(est_tras_l0))
    if len(anclas_tabla_tras_l0) != 1:
        print("APLICACION_ABORTADA · 0 archivos escritos")
        print(f"  · tabla estado: {len(anclas_tabla_tras_l0)} ancla(s) tras aplicar L0 (se requiere exactamente 1)")
        return 1
    est_candidato = (_sustituye(est_tras_l0, anclas_tabla_tras_l0[0], adr_real)
                      if tabla_actual != adr_real else est_tras_l0)
    if est_candidato != est_tras_l0 and not _solo_digitos_cambiaron(est_tras_l0, est_candidato, TABLA_ADR_RE):
        print("APLICACION_ABORTADA · 0 archivos escritos")
        print("  · tabla estado: el cambio construido no se limita a los dígitos del conteo")
        return 1

    if gob_candidato != gob_texto and not _solo_digitos_cambiaron(gob_texto, gob_candidato, CABECERA_ADR_RE):
        print("APLICACION_ABORTADA · 0 archivos escritos")
        print("  · cabecera de gobernanza: el cambio construido no se limita a los dígitos del conteo")
        return 1

    # Todo validado -- recién ahora se escribe, los dos archivos o ninguno.
    # Primero se preparan TODOS los temporales (si algo falla aquí, ningún
    # archivo real se tocó); sólo después se confirman los reemplazos --
    # así el archivo real nunca queda con contenido parcial, y la ventana
    # entre "nada escrito" y "todo escrito" se reduce a los dos renames
    # atómicos consecutivos, no a dos escrituras completas consecutivas.
    temps = []
    try:
        if gob_candidato != gob_texto:
            temps.append((_prepara_temp(ruta_gob, gob_candidato), ruta_gob))
        if est_candidato != est_texto:
            temps.append((_prepara_temp(ruta_est, est_candidato), ruta_est))
    except OSError as e:
        print("APLICACION_ABORTADA · 0 archivos escritos")
        print(f"  · error de E/S al preparar los temporales: {e}")
        return 1

    confirmados = []
    try:
        for ruta_tmp, ruta_destino in temps:
            _confirma_temp(ruta_tmp, ruta_destino)
            confirmados.append(ruta_destino)
    except OSError as e:
        # Los temporales ya estaban listos (ver arriba): si esto falla, es
        # un error de E/S al hacer el rename, no una validación fallida.
        # `confirmados` dice exactamente cuáles de los dos ya quedaron
        # escritos antes del fallo -- nunca se afirma "0 archivos" si no
        # es cierto.
        print(f"ERROR DE E/S AL CONFIRMAR -- ya escrito: {confirmados or '(ninguno)'} · falló: {e}")
        return 1

    cambios = []
    if cab_actual != adr_real:
        cambios.append(f"gobernanza {cab_actual}->{adr_real}")
    if l0_actual != adr_real:
        cambios.append(f"L0 {l0_actual}->{adr_real}")
    if tabla_actual != adr_real:
        cambios.append(f"tabla estado {tabla_actual}->{adr_real}")
    print("APLICADO: " + " · ".join(cambios))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--aplica", action="store_true",
                     help="Fase B: reconciliación mecánica todo-o-nada (por defecto: dry-run)")
    ap.add_argument("--encargo", default=None,
                     help="ruta al encargo del acto, para reportar presencia/ausencia de ## CONSUMIDO")
    ap.add_argument("--sin-suite", action="store_true",
                     help="omite correr tests/check.py --baseline en la Fase A (más rápido)")
    a = ap.parse_args()

    if a.aplica:
        return fase_b_aplica()
    fase_a(ruta_encargo=a.encargo, corre_suite=not a.sin_suite)
    return 0


if __name__ == "__main__":
    sys.exit(main())
