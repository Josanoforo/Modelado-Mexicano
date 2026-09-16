#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/test_adq_demanda_vigente.py -- ENCARGO GEN2-DEMANDA-VIGENTE-ANTES-
DESPACHO (15/sep/2026,
forense/encargos/2026-09-15-GEN2-DEMANDA-VIGENTE-ANTES-DESPACHO.md).

Defecto observado: `data/adq-demanda-activa-v1_0.json` conservaba SHA y
conteos de una corrida de `forense/no-corrido.tsv` anterior porque nada en
`tools/adquiere_cron.sh` volvía a invocar
`adq_investigacion.py --escribe-proyeccion`. El selector real
(`SELECCION-INVESTIGACION` en el cron) ya calcula desde las fuentes
vigentes -- la fotografía publicada era la única pieza que se quedaba
atrás, y sólo importaba para consulta humana/mesa.

Esta prueba congela dos cosas, sin tocar la red, el corpus ni el registro
real:

  1. `cambio_pertinente_proyeccion()` (unidad, rápida): ignora `corte`,
     detecta cualquier otro cambio.
  2. `publica_proyeccion_demanda()` (E2E, con git/gh reales pero un
     "origin" bare local desechable, nunca GitHub): sobre un fixture con
     una copia de los archivos fuente reales,
       a. una fixture que cierra una NC hace que la vista regenerada
          coincida con el registro modificado y se publique
          (commit + push a censo/<fecha>);
       b. repetirlo sin más cambios NO genera un segundo commit;
       c. si el escritor canónico falla, no se publica nada y el archivo
          conserva su contenido anterior.

Corre sola:

    python3 tests/test_adq_demanda_vigente.py
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "tools"))
import adq_investigacion as ADQ  # noqa: E402

RUNNER = RAIZ / "tools" / "adquiere_cron.sh"

FALLOS = []


def afirma(cond, msg):
    if not cond:
        FALLOS.append(msg)


# ───────────────────────────────────────────────────────────────
# 1 · cambio_pertinente_proyeccion -- unidad
# ───────────────────────────────────────────────────────────────

def prueba_solo_corte_no_es_pertinente():
    a = {"corte": "2026-09-14", "total_nc_abiertas": 54, "necesidades": []}
    b = {"corte": "2026-09-15", "total_nc_abiertas": 54, "necesidades": []}
    afirma(ADQ.cambio_pertinente_proyeccion(a, b) is False,
           "un cambio de sólo `corte` no debe marcarse pertinente")


def prueba_cambio_de_conteo_es_pertinente():
    a = {"corte": "2026-09-14", "total_nc_abiertas": 54}
    b = {"corte": "2026-09-15", "total_nc_abiertas": 53}
    afirma(ADQ.cambio_pertinente_proyeccion(a, b) is True,
           "un cambio de total_nc_abiertas debe marcarse pertinente aunque "
           "corte también haya avanzado")


def prueba_cli_compara_proyeccion():
    with tempfile.TemporaryDirectory() as d:
        a = Path(d) / "a.json"
        b = Path(d) / "b.json"
        a.write_text(json.dumps({"corte": "2026-09-14", "x": 1}), encoding="utf-8")
        b.write_text(json.dumps({"corte": "2026-09-15", "x": 1}), encoding="utf-8")
        r = subprocess.run(
            [sys.executable, str(RAIZ / "tools" / "adq_investigacion.py"),
             "--compara-proyeccion", str(a), str(b)],
            capture_output=True, text=True, check=True)
        afirma(r.stdout.strip() == "no",
               f"--compara-proyeccion debe imprimir 'no' cuando sólo cambia "
               f"corte; salida={r.stdout!r}")
        b.write_text(json.dumps({"corte": "2026-09-15", "x": 2}), encoding="utf-8")
        r = subprocess.run(
            [sys.executable, str(RAIZ / "tools" / "adq_investigacion.py"),
             "--compara-proyeccion", str(a), str(b)],
            capture_output=True, text=True, check=True)
        afirma(r.stdout.strip() == "si",
               f"--compara-proyeccion debe imprimir 'si' cuando algo más "
               f"cambia; salida={r.stdout!r}")
        faltante = Path(d) / "no-existe.json"
        r = subprocess.run(
            [sys.executable, str(RAIZ / "tools" / "adq_investigacion.py"),
             "--compara-proyeccion", str(faltante), str(b)],
            capture_output=True, text=True, check=True)
        afirma(r.stdout.strip() == "si",
               f"un ANTES ausente debe leerse como {{}} y contar como cambio; "
               f"salida={r.stdout!r}")


# ───────────────────────────────────────────────────────────────
# 2 · fixture E2E -- publica_proyeccion_demanda con git/gh reales sobre un
#     "origin" bare local desechable (nunca GitHub, nunca el repo real)
# ───────────────────────────────────────────────────────────────

# Archivos fuente reales que `proyecta_demanda` necesita -- la misma lista
# que `fuentes_sha256` declara en el JSON publicado.
_ARCHIVOS_FUENTE = [
    "data/adq-investigacion.yaml",
    "data/corrida0/decisiones.tsv",
    "data/corrida0/demanda-resultados.tsv",
    "data/corrida0/resultados.tsv",
    "data/corrida0/usos.tsv",
    "data/curacion-registro/necesidad-objeto-modelo.tsv",
    "data/curacion-registro/utilidad-modelo.tsv",
    "forense/no-corrido.tsv",
    "forense/prereg-duelo-v2/codificacion-R-v1_2.tsv",
    "forense/prereg-duelo-v2/universo-triada-v1_4.tsv",
]


def _run(cmd, cwd, check=True, env=None):
    r = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, env=env)
    if check and r.returncode != 0:
        raise RuntimeError(f"{cmd} -> {r.returncode}\n{r.stdout}\n{r.stderr}")
    return r


def _crea_fixture(tmp: Path) -> tuple[Path, Path]:
    """Copia sólo lo que `proyecta_demanda` lee, con `tools/adq_investigacion.py`
    real, en un repo git nuevo con un `origin` bare local (nunca GitHub)."""
    work = tmp / "work"
    (work / "tools").mkdir(parents=True)
    (work / "forense" / "censo-raiz").mkdir(parents=True)
    shutil.copy2(RAIZ / "tools" / "adq_investigacion.py", work / "tools" / "adq_investigacion.py")
    shutil.copy2(RAIZ / "tools" / "adq_suficiencia.py", work / "tools" / "adq_suficiencia.py")
    for rel in _ARCHIVOS_FUENTE:
        origen = RAIZ / rel
        destino = work / rel
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origen, destino)
    (work / "data" / "adq-demanda-activa-v1_0.json").write_text(
        (RAIZ / "data" / "adq-demanda-activa-v1_0.json").read_text(encoding="utf-8"),
        encoding="utf-8")
    (work / ".gitignore").write_text("__pycache__/\n", encoding="utf-8")

    env = dict(os.environ)
    env["GIT_AUTHOR_NAME"] = env["GIT_COMMITTER_NAME"] = "fixture"
    env["GIT_AUTHOR_EMAIL"] = env["GIT_COMMITTER_EMAIL"] = "fixture@test.invalid"
    _run(["git", "init", "--quiet", "-b", "main"], work, env=env)
    # Config LOCAL del repo, no variables de entorno: `publica_proyeccion_demanda`
    # se invoca después vía `_corre_bash` (un subprocess nuevo, sin este env), y
    # un runner de CI sin identidad git global ("empty ident name") tumbaba el
    # `git commit` real de la función bajo prueba, no la lógica que se quiere
    # probar -- reproducido en GitHub Actions (PR #801, primer intento de CI).
    _run(["git", "config", "user.email", "fixture@test.invalid"], work, env=env)
    _run(["git", "config", "user.name", "fixture"], work, env=env)
    _run(["git", "add", "-A"], work, env=env)
    _run(["git", "commit", "--quiet", "-m", "fixture inicial"], work, env=env)

    bare = tmp / "origin.git"
    _run(["git", "clone", "--quiet", "--bare", str(work), str(bare)], tmp, env=env)
    _run(["git", "remote", "add", "origin", str(bare)], work, env=env)
    _run(["git", "push", "--quiet", "-u", "origin", "main"], work, env=env)
    return work, bare


def _cierra_una_nc(no_corrido: Path) -> str:
    """Edición de texto plano, línea a línea -- nunca csv.reader/writer
    sobre el archivo completo: este TSV trae campos citados con comillas y
    saltos de línea internos que el módulo `csv` puede desfigurar en un
    round-trip completo (defecto ya medido en este proyecto). Cierra la
    primera fila ABIERTA que encuentra y devuelve su id."""
    lineas = no_corrido.read_text(encoding="utf-8").splitlines(keepends=True)
    for i, linea in enumerate(lineas):
        campos = linea.rstrip("\n").split("\t")
        if len(campos) >= 10 and campos[9] == "ABIERTA":
            campos[9] = "CERRADA"
            if len(campos) > 10:
                campos[10] = "ACTO-FIXTURE-TEST"
            if len(campos) > 11:
                campos[11] = "2026-09-20"
            lineas[i] = "\t".join(campos) + "\n"
            no_corrido.write_text("".join(lineas), encoding="utf-8")
            return campos[0]
    raise AssertionError("no-corrido.tsv de fixture no trae ninguna fila ABIERTA")


def _cuenta_abiertas(no_corrido: Path) -> int:
    total = 0
    for linea in no_corrido.read_text(encoding="utf-8").splitlines()[1:]:
        campos = linea.split("\t")
        if len(campos) >= 10 and campos[9] == "ABIERTA":
            total += 1
    return total


def _corre_bash(cuerpo, cwd, timeout=90):
    """Carga las funciones REALES del runner (seam ADQ_CRON_SOLO_DEFINE=1) y
    corre `cuerpo` en `cwd`. FECHA/LOGFILE/CENSO_DIR se fijan DENTRO de
    `cuerpo`, nunca por variable de entorno: el `source` recalcula esas tres
    variables sin condicional (`FECHA="$(date ...)"`, no `: "${FECHA:=...}"`),
    así que cualquier valor puesto antes de la carga queda pisado -- mismo
    patrón que usa tests/test_adq_cableado.py."""
    env = dict(os.environ)
    env["ADQ_CRON_SOLO_DEFINE"] = "1"
    guion = (f'set -uo pipefail\nsource "{RUNNER}"\n'
             f'cd "{cwd}" || exit 90\n{cuerpo}\n')
    r = subprocess.run(["bash", "-c", guion], cwd=str(RAIZ),
                        capture_output=True, text=True, errors="replace",
                        env=env, timeout=timeout)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def _seam_disponible():
    return "ADQ_CRON_SOLO_DEFINE" in RUNNER.read_text(encoding="utf-8")


def _publica(work: Path, fecha: str, logfile: Path):
    return _corre_bash(
        f'FECHA="{fecha}"; LOGFILE="{logfile}"; CENSO_DIR="forense/censo-raiz"; '
        f'PUBLICACION_FALLIDA=0; '
        f'publica_proyeccion_demanda; '
        f'echo "RC_FALLIDA=${{PUBLICACION_FALLIDA:-0}}"',
        cwd=work)


def prueba_e2e_publica_regenera_y_no_repite():
    if not _seam_disponible():
        FALLOS.append("tools/adquiere_cron.sh no expone ADQ_CRON_SOLO_DEFINE")
        return
    if shutil.which("gh") is None:
        # gh es opcional en la función real (`command -v gh`); sin él la
        # prueba igual cubre commit+push, sólo sin el intento de PR.
        pass
    with tempfile.TemporaryDirectory(prefix="adq-demanda-fixture-") as d:
        tmp = Path(d)
        try:
            work, bare = _crea_fixture(tmp)
        except Exception as e:
            FALLOS.append(f"E2E: no se pudo construir el fixture: {e}")
            return
        no_corrido = work / "forense" / "no-corrido.tsv"
        logfile = tmp / "log.txt"
        fecha = "2026-09-20"

        antes_abiertas = _cuenta_abiertas(no_corrido)
        id_cerrado = _cierra_una_nc(no_corrido)
        despues_abiertas = _cuenta_abiertas(no_corrido)
        afirma(despues_abiertas == antes_abiertas - 1,
               f"la fixture debe cerrar exactamente una NC ({id_cerrado}); "
               f"antes={antes_abiertas} despues={despues_abiertas}")

        rc, salida = _publica(work, fecha, logfile)
        afirma(rc == 0, f"E2E paso 1: publica_proyeccion_demanda salió {rc}\n{salida}")
        afirma("RC_FALLIDA=0" in salida,
               f"E2E paso 1: no debe incrementar PUBLICACION_FALLIDA; salida={salida!r}")

        log_texto = logfile.read_text(encoding="utf-8") if logfile.exists() else ""
        afirma("[ADQ-DEMANDA] " + fecha in log_texto or "proyección regenerada y publicada" in log_texto,
               f"E2E paso 1: el log debe declarar la publicación; log:\n{log_texto}")

        r = _run(["git", "log", f"censo/{fecha}", "--format=%s", "-1"], work, check=False)
        afirma(r.returncode == 0 and r.stdout.strip() == f"[ADQ-DEMANDA] {fecha}",
               f"E2E paso 1: censo/{fecha} debe llevar un commit "
               f"'[ADQ-DEMANDA] {fecha}' como último; encontrado: {r.stdout!r}/{r.stderr!r}")

        r_origen = _run(["git", "log", f"censo/{fecha}", "--format=%s", "-1"], bare, check=False)
        afirma(r_origen.returncode == 0 and r_origen.stdout.strip() == f"[ADQ-DEMANDA] {fecha}",
               f"E2E paso 1: el commit debe haberse empujado al origin bare; "
               f"encontrado: {r_origen.stdout!r}/{r_origen.stderr!r}")

        publicado = json.loads(
            _run(["git", "show", f"censo/{fecha}:data/adq-demanda-activa-v1_0.json"],
                 work).stdout)
        afirma(publicado["total_nc_abiertas"] == despues_abiertas,
               f"E2E paso 1: total_nc_abiertas publicado ({publicado['total_nc_abiertas']}) "
               f"debe coincidir con el no-corrido.tsv modificado ({despues_abiertas})")
        sha_esperado = ADQ.hashlib.sha256(no_corrido.read_bytes()).hexdigest()
        afirma(publicado["sha256_fuente"] == sha_esperado,
               "E2E paso 1: sha256_fuente publicado debe ser el del "
               "no-corrido.tsv realmente usado, no uno heredado")

        r = _run(["git", "rev-parse", "--verify", "main"], work, check=False)
        rama_actual = _run(["git", "branch", "--show-current"], work).stdout.strip()
        afirma(rama_actual == "main",
               f"E2E paso 1: la función debe restaurar el árbol operativo a "
               f"main; quedó en {rama_actual!r}")

        # Paso 2: repetir sin más cambios de insumos -- no debe generar un
        # segundo commit ("evitar commits/PR repetidos solo por una marca
        # de tiempo", ENCARGO 15/sep/2026).
        rc2, salida2 = _publica(work, fecha, logfile)
        afirma(rc2 == 0, f"E2E paso 2: publica_proyeccion_demanda salió {rc2}\n{salida2}")
        n_commits = _run(
            ["git", "rev-list", "--count", f"censo/{fecha}"], work).stdout.strip()
        afirma(n_commits == "2",
               f"E2E paso 2: sin cambios de insumos, censo/{fecha} no debe "
               f"crecer más allá de fixture+1 publicación; commits={n_commits}")
        afirma("sin cambio pertinente" in salida2,
               f"E2E paso 2: debe declarar explícitamente que no hubo cambio "
               f"pertinente; salida={salida2!r}")
        # sólo la proyección: `forense/no-corrido.tsv` sigue intencionalmente
        # sin commitear (es el insumo de la fixture, el cron nunca lo toca).
        estado_proyeccion = _run(
            ["git", "status", "--porcelain", "--",
             "data/adq-demanda-activa-v1_0.json"], work).stdout.strip()
        afirma(estado_proyeccion == "",
               f"E2E paso 2: la proyección debe quedar sin diferencia tras "
               f"descartar la regeneración sin cambios; status={estado_proyeccion!r}")

        # Paso 3: el escritor canónico falla (config corrupta) -- no se
        # publica nada y el archivo conserva su contenido anterior.
        config_real = (work / "data" / "adq-investigacion.yaml").read_bytes()
        (work / "data" / "adq-investigacion.yaml").write_text("{esto: no es válido: :", encoding="utf-8")
        try:
            rc3, salida3 = _publica(work, fecha, logfile)
        finally:
            (work / "data" / "adq-investigacion.yaml").write_bytes(config_real)
        afirma(rc3 == 0,
               f"E2E paso 3: un fallo de regeneración no debe tumbar el "
               f"resto del cron (return 0); salió {rc3}\n{salida3}")
        afirma("RC_FALLIDA=1" in salida3,
               f"E2E paso 3: un fallo de --escribe-proyeccion debe subir "
               f"PUBLICACION_FALLIDA; salida={salida3!r}")
        afirma("PARO-PROYECCION-DEMANDA" in salida3,
               f"E2E paso 3: debe declarar PARO-PROYECCION-DEMANDA, no "
               f"callar el fallo; salida={salida3!r}")
        n_commits3 = _run(
            ["git", "rev-list", "--count", f"censo/{fecha}"], work).stdout.strip()
        afirma(n_commits3 == "2",
               f"E2E paso 3: un fallo de regeneración no debe publicar "
               f"nada nuevo; commits={n_commits3}")
        estado_proyeccion3 = _run(
            ["git", "status", "--porcelain", "--",
             "data/adq-demanda-activa-v1_0.json"], work).stdout.strip()
        afirma(estado_proyeccion3 == "",
               f"E2E paso 3: tras un fallo, la proyección debe quedar sin "
               f"diferencia (conserva su último contenido publicado); "
               f"status={estado_proyeccion3!r}")


# ───────────────────────────────────────────────────────────────

PRUEBAS = [v for k, v in sorted(globals().items()) if k.startswith("prueba_")]


def main():
    for fn in PRUEBAS:
        try:
            fn()
        except Exception as e:
            FALLOS.append(f"{fn.__name__}: EXCEPCIÓN {type(e).__name__}: {e}")
    for f in FALLOS:
        print(f"FAIL {f}")
    print(f"\n{len(PRUEBAS)} pruebas, {len(FALLOS)} fallos")
    return 1 if FALLOS else 0


if __name__ == "__main__":
    sys.exit(main())
