"""ACTO GEN2-TUBERIA-3 · huérfano (D-21). Atrapa: P1 worktrees del canal en el
tmpfs sin prune; P2 contador legacy movido sin definición; P3 `status` que dice
otra cosa que `demanda` tras el dictamen. Ejecutar: pytest -q tests/test_tuberia3.py"""
import os
import re
import shutil
import signal
import subprocess
import sys
import tarfile
import tempfile
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "tools"))
sys.path.insert(0, str(RAIZ))

from tests import test_corrida0 as T  # noqa: E402

C = T.C  # el MISMO módulo que parchean las fixtures (otra copia no vería los parches)

DERIVA = RAIZ / "tools" / "deriva_cron.sh"


def _funcion_sh(nombre: str) -> str:
    m = re.search(rf"^{nombre}\(\) \{{\n.*?^\}}\n", DERIVA.read_text(encoding="utf-8"), re.S | re.M)
    assert m, f"función {nombre} ausente en deriva_cron.sh"
    return m.group(0)


def test_p1_derivador_sin_tmp():
    assert DERIVA.read_text(encoding="utf-8").count("/tmp") == 0


def test_p1_retira_y_poda_worktree_aunque_falle():
    with tempfile.TemporaryDirectory(dir=RAIZ.parent) as d:
        d = Path(d)
        repo = d / "repo"
        sh = lambda *a: subprocess.run(a, cwd=repo, check=True, capture_output=True, text=True)
        repo.mkdir()
        sh("git", "init", "-q")
        sh("git", "-c", "user.email=a@b", "-c", "user.name=t", "commit", "-q", "--allow-empty", "-m", "x")
        huerfano = d / "wt-huerfano"
        sh("git", "worktree", "add", "-q", "--detach", str(huerfano))
        shutil.rmtree(huerfano)  # huérfano prunable: directorio borrado, registro vivo
        vivo = d / "wt-vivo"
        sh("git", "worktree", "add", "-q", "--detach", str(vivo))
        (vivo / "universo.json").write_text("{}")  # trabajo sin empujar
        script = (f'SOURCE_REPO_DIR="{repo}"; LOGFILE="{d}/log"; ESTADO_DIR="{d}/estado"; RUN_ID=r1; '
                  f'CONSERVA_WORKTREE=1; log() {{ :; }}\n{_funcion_sh("poda_worktrees")}\n'
                  f'{_funcion_sh("retira_worktree")}\nretira_worktree "{vivo}"\n')
        subprocess.run(["bash", "-c", script], check=True)
        assert not vivo.exists()
        assert (d / "estado" / "evidencia-r1" / "no-versionados.tgz").exists()  # el trabajo no se pierde
        listado = sh("git", "worktree", "list").stdout.strip().splitlines()
        assert len(listado) == 1, listado  # solo el principal: cero prunables


def _con_dictamen(tmp: Path, lineas: list[str]):
    (tmp / "demanda-dictamen-v1_0.tsv").write_text(
        "# DERIVADO\ncorrida_id\tresultado_id\tdictamen\tcita\tsucesor\n" + "\n".join(lineas) + "\n",
        encoding="utf-8")
    C.SALIDA = tmp


def test_p3_status_lee_el_dictamen_y_legacy_no_se_mueve():
    res = [T._fila_demanda(f"RES-000{i}", f"c:r{i}:x", cid)
           for i, cid in ((1, "CORR-0001"), (2, "CORR-0001"), (3, "CORR-0002"))]
    corr = [T._fila_corrida("CORR-0001", ["RES-0001", "RES-0002"]), T._fila_corrida("CORR-0002", ["RES-0003"])]
    salida0 = C.SALIDA
    try:
        with T._arbol_registro(res=res, corr=corr, calcs=[]) as tmp:
            C.SALIDA = tmp  # sin vista: cuenta como antes
            antes = C.status(imprime=False)
            _con_dictamen(tmp, ["CORR-0002\tCORRIDA\tCORRIDA-NO-REQUERIDA\tc\ts",
                                "CORR-0001\tRES-0001\tNO-RELEVAR-X\tc\ts"])
            despues = C.status(imprime=False)
            no_req, cerrados = C._reduccion_por_dictamen(["CORR-0001", "CORR-0002"],
                                                         [("CORR-0001", "RES-0001"), ("CORR-0001", "RES-0002"),
                                                          ("CORR-0002", "RES-0003")])
    finally:
        C.SALIDA = salida0
    assert (no_req, cerrados) == (1, 1)
    assert antes["N_corridas_requeridas"] == 2 and antes["N_resultados_pendientes"] == 3
    assert despues["N_corridas_requeridas"] == antes["N_corridas_requeridas"] - no_req
    assert despues["N_resultados_pendientes"] == antes["N_resultados_pendientes"] - cerrados
    # P2: el dictamen no toca el contador legacy (DEFECTO-DE-CONTEO: no se mueve sin definición)
    assert despues["dependencias_numericas_legacy_activas"] == antes["dependencias_numericas_legacy_activas"] == 3


# ── Pieza B (P2/P3) · las vistas de demanda viajan por el canal ─────────────
# Defecto que atrapa (medido 28/sep): demanda-corridas.tsv y demanda-resultados.tsv
# no estaban en el `git add` del job derivados; `status` sobre el árbol
# comprometido decía pendientes 158 y `corrida0 demanda` decía 63. Contrato
# estático sobre el YAML: correr el job entero costaría más que el defecto (D-14).
import contextlib  # noqa: E402
import io  # noqa: E402

import yaml  # noqa: E402

import derivados_protegidos as DP  # noqa: E402

VERIFY = RAIZ / ".github" / "workflows" / "verify.yml"
VISTAS_DEMANDA = ("data/corrida0/demanda-corridas.tsv", "data/corrida0/demanda-resultados.tsv")


def _codigo_paso_derivados() -> str:
    """El script del paso de `derivados` que publica las vistas, sin las líneas de comentario."""
    wf = yaml.safe_load(VERIFY.read_text(encoding="utf-8"))
    pasos = [p for p in wf["jobs"]["derivados"]["steps"] if "corrida0.py registro" in p.get("run", "")]
    assert len(pasos) == 1, f"se esperaba un paso con `corrida0.py registro`, hay {len(pasos)}"
    return "\n".join(l for l in pasos[0]["run"].splitlines() if not l.lstrip().startswith("#"))


def test_p2_job_deriva_demanda_una_vez_antes_de_lo_que_la_lee():
    codigo = _codigo_paso_derivados()
    assert codigo.count("tools/corrida0.py demanda") == 1, "demanda se deriva exactamente una vez"
    en = codigo.index("tools/corrida0.py demanda")
    for lector in ("tools/marcador_segmento.py --escribe", "tools/corrida0.py registro",
                   "tools/resuelve_citas.py tabla", "tools/tablero_programa.py --actualiza",
                   "tools/readme_derivado.py --escribe"):
        assert en < codigo.index(lector), f"demanda debe correr antes de {lector}"
    assert en < codigo.index("while :; do"), "una vez antes del bucle de trozos, no por trozo"
    # si demanda no deriva, el canal sigue y deja las dos vistas como estaban comprometidas
    assert f"git checkout -q -- {' '.join(VISTAS_DEMANDA)}" in codigo


def test_p2_git_add_del_commit_deriva_incluye_las_dos_vistas_de_demanda():
    lineas = [l for l in _codigo_paso_derivados().splitlines()
              if l.lstrip().startswith("git add --") and "data/corrida0/corridas.tsv" in l]
    assert len(lineas) == 1, f"una sola línea `git add` de vistas, hay {len(lineas)}"
    campos = lineas[0].split()
    for vista in VISTAS_DEMANDA:
        assert vista in campos, f"{vista} debe viajar en el commit [deriva]"


def test_p2_guardias_de_derivados_aceptan_las_vistas_de_demanda():
    import tablero_programa as TP  # perezoso: al importarse hace os.chdir(RAIZ)
    rutas, _examinados = DP.lista_derivados()
    for vista in VISTAS_DEMANDA:  # la lista sale de la cabecera DERIVADO, nunca tecleada
        assert vista in rutas, f"{vista} perdió la cabecera DERIVADO: --solo-derivados rechazaría el [deriva]"
    # el guardián del tablero (que corre tras `demanda` en el mismo job) las tolera sucias
    assert TP._sucios_ajenos("".join(f" M {v}\n" for v in VISTAS_DEMANDA)) == []
    assert TP._sucios_ajenos(f" M {VISTAS_DEMANDA[0]}\n M tools/x.py") == ["tools/x.py"]
    # y --solo-derivados acepta un commit que toca sólo esas dos (copias de las vistas reales)
    with tempfile.TemporaryDirectory(dir=RAIZ.parent) as d:
        repo = Path(d)
        git = lambda *a: subprocess.run(["git", "-c", "user.email=a@b", "-c", "user.name=t", *a],
                                        cwd=repo, check=True, capture_output=True, text=True).stdout.strip()
        git("init", "-q")
        for rel in (*VISTAS_DEMANDA, "tools/x.py"):
            (repo / rel).parent.mkdir(parents=True, exist_ok=True)
            (repo / rel).write_bytes((RAIZ / rel).read_bytes() if rel in VISTAS_DEMANDA else b"x = 1\n")
        git("add", "-A")
        git("commit", "-q", "-m", "base")
        base = git("rev-parse", "HEAD")
        for rel in VISTAS_DEMANDA:
            (repo / rel).write_text((repo / rel).read_text(encoding="utf-8") + "RES-9999\n", encoding="utf-8")
        git("commit", "-q", "-am", "[deriva] demanda")
        solo = git("rev-parse", "HEAD")
        (repo / "tools/x.py").write_text("x = 2\n", encoding="utf-8")
        git("commit", "-q", "-am", "ajeno")
        con_ajeno = git("rev-parse", "HEAD")
        raiz0 = DP.RAIZ
        DP.RAIZ = str(repo)
        try:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                assert DP.main(["--solo-derivados", base, solo]) == 0
                assert DP.main(["--solo-derivados", base, con_ajeno]) == 1  # un archivo ajeno sí se rechaza
        finally:
            DP.RAIZ = raiz0


def test_p3_status_coincide_con_demanda_cuando_las_vistas_estan_al_dia():
    """`cmd_demanda` REAL escribe las vistas del fixture y `status` las lee: mismos
    N_corridas_requeridas y N_resultados_pendientes, con la reducción por dictamen activa."""
    res = [T._fila_demanda(f"RES-000{i}", f"c:r{i}:x", cid)
           for i, cid in ((1, "CORR-0001"), (2, "CORR-0001"), (3, "CORR-0002"))]
    corr = [T._fila_corrida("CORR-0001", ["RES-0001", "RES-0002"]), T._fila_corrida("CORR-0002", ["RES-0003"])]
    salida0 = C.SALIDA
    originales = (C._construye_filas_demanda, C._corridas, C._yaml_safe_load)
    try:
        with T._arbol_registro(res=res, corr=corr, calcs=[]) as tmp:
            _con_dictamen(tmp, ["CORR-0002\tCORRIDA\tCORRIDA-NO-REQUERIDA\tc\ts",
                                "CORR-0001\tRES-0001\tNO-RELEVAR-X\tc\ts"])
            C._construye_filas_demanda = lambda asigna=None: (res, [], {}, {})  # el fixture ES la demanda
            C._corridas = lambda *a, **k: corr
            C._yaml_safe_load = lambda *a, **k: []  # sin leer el manifiesto real
            buf = io.StringIO()
            try:
                with contextlib.redirect_stdout(buf):
                    rc = C.cmd_demanda(None)
            finally:
                C._construye_filas_demanda, C._corridas, C._yaml_safe_load = originales
            st = C.status(imprime=False)
    finally:
        C._construye_filas_demanda, C._corridas, C._yaml_safe_load = originales
        C.SALIDA = salida0
    dem = dict(re.findall(r"^(N_corridas_requeridas|N_resultados_pendientes) = (\d+)", buf.getvalue(), re.M))
    assert rc == 0 and set(dem) == {"N_corridas_requeridas", "N_resultados_pendientes"}, buf.getvalue()[:300]
    assert int(dem["N_corridas_requeridas"]) == st["N_corridas_requeridas"]
    assert int(dem["N_resultados_pendientes"]) == st["N_resultados_pendientes"]
    # la reducción por dictamen estaba activa (si no, la igualdad no probaría nada)
    assert st["N_corridas_requeridas"] < len(corr) and st["N_resultados_pendientes"] < len(res)


# ── Pieza B (revisión adversarial) · CORR posicional ────────────────────────
# Defecto que atrapa (medido 28/sep sobre el comando del job): con la demanda al día, `registro
# --lote` congelaba por corrida_id las filas DEMANDA de corridas.tsv mientras resultados.tsv traía
# los pares frescos: 122 de 236 RES apuntaban a una corrida cuya fila publicada no los listaba
# (los CORR son posicionales: 25 slots nuevos movieron 145 de 211 RES). Y el dictamen, llaveado
# también por CORR, se desalinea igual (158 pendientes contra 63).

def _demanda(pares):
    """[(RES, CORR)] -> (filas de demanda-resultados, filas de demanda-corridas) del fixture."""
    res = [T._fila_demanda(rid, f"c:{rid}:x", corr) for rid, corr in pares]
    corr = [T._fila_corrida(c, [rid for rid, cc in pares if cc == c]) for c in sorted({c for _, c in pares})]
    return res, corr


def _incoherentes_demanda() -> list[str]:
    """RES DEMANDA de resultados.tsv que la fila de su corrida en corridas.tsv no lista."""
    corridas = {f["corrida_id"]: f for f in C._leer_tsv_derivado(C.VISTA_CORRIDAS)}
    return [f"{r['corrida_id']}/{r['resultado_id']}" for r in C._leer_tsv_derivado(C.VISTA_RESULTADOS)
            if r["origen"] == "DEMANDA"
            and r["resultado_id"] not in re.split(r"[,;]", corridas[r["corrida_id"]]["resultados_ids"])]


def _publica_v1_y_registra_v2(lote: list[str], con_nueva: bool):
    """Publica la demanda v1 y luego registra con la demanda v2 (un slot nuevo al frente corre los
    CORR). Devuelve (incoherentes, fila OFERTA ajena tras el registro, fila OFERTA nueva o None)."""
    v1 = _demanda([("RES-0001", "CORR-0001"), ("RES-0002", "CORR-0002")])
    v2 = _demanda([("RES-0009", "CORR-0001"), ("RES-0001", "CORR-0002"), ("RES-0002", "CORR-0003")])
    etq = {"generacion": "GEN2", "cuenta_gen2": "SI"}
    vistas0 = (C.VISTA_CORRIDAS, C.VISTA_RESULTADOS, C.VISTA_USOS)
    try:
        with T._arbol_registro(res=v1[0], corr=v1[1],
                               calcs=[{"calc_id": "CALC-FIX-VIEJA", "valores": {"RESULT-A": 1.0}, "etiquetas": etq}]) as tmp:
            C.VISTA_CORRIDAS, C.VISTA_RESULTADOS, C.VISTA_USOS = (tmp / "corridas.tsv", tmp / "resultados.tsv", tmp / "usos.tsv")
            C.registro(escribe=True, imprime=False)
            assert _incoherentes_demanda() == []  # control: la v1 publicada es coherente
            filas = list(C._leer_tsv_derivado(C.VISTA_CORRIDAS))
            for f in filas:
                if f["spec_id"] == "CALC-FIX-VIEJA":
                    f["resultado_replay"], f["contexto_replay"] = "NO-REPRODUCE", "DISTINTO"  # drift ajeno
            C._escribe(C.VISTA_CORRIDAS, C.COLS_VISTA_CORRIDAS, filas)
            C._escribe(C.DEMANDA_RESULTADOS, C.COLS_RESULTADOS, v2[0])
            C._escribe(C.DEMANDA_CORRIDAS, C.COLS_CORRIDAS, v2[1])
            if con_nueva:
                T._sella_calc_fixture(tmp / "CALC-FIX-NUEVA", "CALC-FIX-NUEVA", {"RESULT-C": 3.0}, etq)
            C.registro(escribe=True, imprime=False, lote=lote)
            por_spec = {f["spec_id"]: f for f in C._leer_tsv_derivado(C.VISTA_CORRIDAS)}
            return _incoherentes_demanda(), por_spec["CALC-FIX-VIEJA"], por_spec.get("CALC-FIX-NUEVA")
    finally:
        C.VISTA_CORRIDAS, C.VISTA_RESULTADOS, C.VISTA_USOS = vistas0


def test_p2_registro_con_lote_refresca_filas_demanda_y_congela_oferta_ajena():
    incoherentes, vieja, nueva = _publica_v1_y_registra_v2(["CALC-FIX-NUEVA"], con_nueva=True)
    assert incoherentes == [], f"filas DEMANDA congeladas con CORR viejo: {incoherentes}"
    assert vieja["resultado_replay"] == "NO-REPRODUCE"  # lo ajeno de OFERTA sigue congelado byte a byte
    assert nueva is not None  # y el lote sí escribió lo suyo


def test_p2_registro_con_lote_centinela_refresca_demanda_en_estado_estable():
    """El job, sin CALC pendientes pero con la demanda re-derivada, corre `registro --lote DEMANDA-REFRESCO`."""
    incoherentes, vieja, nueva = _publica_v1_y_registra_v2(["DEMANDA-REFRESCO"], con_nueva=False)
    assert incoherentes == [], f"filas DEMANDA congeladas con CORR viejo: {incoherentes}"
    assert vieja["resultado_replay"] == "NO-REPRODUCE" and nueva is None


def test_p3_dictamen_desalineado_se_detecta_con_los_dos_tsv_frescos():
    v1 = _demanda([("RES-0001", "CORR-0001"), ("RES-0002", "CORR-0002")])
    v2 = _demanda([("RES-0009", "CORR-0001"), ("RES-0001", "CORR-0002"), ("RES-0002", "CORR-0003")])
    ids = lambda d: [c["corrida_id"] for c in d[1]]  # noqa: E731
    pares = lambda d: [(f["corrida_natural"], f["resultado_id"]) for f in d[0]]  # noqa: E731
    salida0 = C.SALIDA
    try:
        with T._arbol_registro() as tmp:
            assert C._dictamen_desalineado(ids(v1), pares(v1)) is None  # sin vista de dictamen: no hay contra qué
            _con_dictamen(tmp, [f"{c}\tCORRIDA\tCORRIDA-NO-REQUERIDA\tc\ts" for c in ids(v1)]
                          + [f"{c}\t{r}\tNO-RELEVAR-X\tc\ts" for c, r in pares(v1)])
            assert C._dictamen_desalineado(ids(v1), pares(v1)) == (0, 0, 0)  # alineado con la demanda que dictaminó
            # la demanda avanzó un slot; el dictamen no: 3 pares y 1 corrida sin fila, 2 filas huérfanas
            assert C._dictamen_desalineado(ids(v2), pares(v2)) == (3, 1, 2)
    finally:
        C.SALIDA = salida0


def test_p3_job_avisa_dictamen_desalineado_sin_detener_el_canal_y_refresca_la_demanda_en_estado_estable():
    codigo = _codigo_paso_derivados()
    assert "grep -q '^dictamen_alineado = NO' /tmp/demanda-derivada.out" in codigo
    assert codigo.index("dictamen_alineado = NO") > codigo.index("tools/corrida0.py demanda")
    assert 'gh issue create --title "$TITULO_DIC"' in codigo  # NC automática, con el patrón dedupe del bloque
    assert codigo.count("gh issue list --state open --search \"$TITULO_DIC in:title\"") == 1
    # estado estable: sin LOTE pero con la demanda distinta de HEAD, se refrescan sus filas DEMANDA
    assert "git diff --quiet HEAD -- data/corrida0/demanda-corridas.tsv data/corrida0/demanda-resultados.tsv" in codigo
    assert "tools/corrida0.py registro --escribe --lote DEMANDA-REFRESCO" in codigo


# ── Pieza C (P1, revisión adversarial) · el cierre del canal frente a fallos reales ──
# Defectos que atrapa, reproducidos con el script REAL: (1) un `log` que falla (disco lleno) o un
# `mkdir` que falla abortaba finalizar/retira_worktree antes de borrar el worktree y de cambiar
# el código de salida; (2) un worktree huérfano con directorio VIVO (SIGKILL/OOM) no lo recogía
# nadie (`prune` solo quita registros sin directorio): ~1 GB por kill duro; (3) una salida sin la
# bandera (commit rechazado, SIGTERM) borraba el worktree sin evidencia. Costo de no atraparlos:
# el disco que el acto quería liberar y trabajo sin empujar perdido (D-14). Los stubs sustituyen
# solo lo que MIDE (suite, universo, tablero, registro); el script, git, flock y tar son los reales.

_STUBS = {
    "tests/check.py": (
        "import os, sys, time\n"
        "modo = os.environ.get('STUB_SUITE', '')\n"
        "if modo:\n"
        "    open('universo-PARCIAL.json', 'w').write('{}')  # trabajo sin empujar\n"
        "if modo == 'cuelga':\n"
        "    open(os.environ['STUB_LISTO'], 'w').write('1'); time.sleep(120)\n"
        "print('LÍNEA BASE: VERDE')\n"),
    "tools/curador_registro/snapshot_universe.py": (
        "import pathlib, sys\n"
        "out = pathlib.Path(sys.argv[sys.argv.index('--output-dir') + 1])\n"
        "(out / 'snapshot-t0.json').write_text('{}'); (out / 'universo-declarado-t0.tsv').write_text('h\\n')\n"),
    "tools/deriva_resumen.py": (
        "import pathlib, sys\n"
        "pathlib.Path(sys.argv[sys.argv.index('--salida') + 1]).write_text('{}')\n"),
    "tools/tablero_programa.py": "print('ok')\n",
    "tools/corrida0.py": "print('ok')\n",
    ".gitignore": "data/raw\ndata/raw/\n",
    "forense/tablero/TABLERO-PROGRAMA.md": "t\n",
    "data/curacion-universo/snapshot-t0.json": "{}\n",
}


class _Canal:
    """Repo fuente con origin local y corpus, con el derivador REAL copiado a su tools/."""

    def __init__(self, d: Path):
        self.d, self.src = d, d / "src"
        self.wt, self.tmp, self.estado, self.log = d / "wt", d / "tmp", d / "log" / "estado", d / "log" / "2026-09-28.log"
        git = lambda *a: subprocess.run(["git", *a], cwd=self.src if self.src.exists() else d,
                                        check=True, capture_output=True, text=True).stdout
        git("init", "-q", "--bare", "origin.git")
        git("clone", "-q", str(d / "origin.git"), str(self.src))
        git("config", "user.email", "a@b"), git("config", "user.name", "t")
        for rel, txt in {**_STUBS, "tools/deriva_cron.sh": DERIVA.read_text(encoding="utf-8")}.items():
            (self.src / rel).parent.mkdir(parents=True, exist_ok=True)
            (self.src / rel).write_text(txt, encoding="utf-8")
        git("add", "-A"), git("commit", "-q", "-m", "base"), git("branch", "-M", "main"), git("push", "-q", "-u", "origin", "main")
        (d / "corpus").mkdir()
        (d / "corpus" / "x").write_text("x")
        (self.src / "data" / "raw").symlink_to(d / "corpus")
        (d / "bin").mkdir()
        (d / "bin" / "gh").write_text("#!/bin/sh\nexit 0\n")  # gh falso: sin PR abierto ni fusionado; crea el PR
        (d / "bin" / "gh").chmod(0o755)
        self.git = git

    def env(self, run_id: str, **extra) -> dict:
        return {**os.environ, "DERIVA_LOG_ROOT": str(self.d / "log"), "DERIVA_WORKTREES_DIR": str(self.wt),
                "DERIVA_TMPDIR": str(self.tmp), "DERIVA_FECHA": "2026-09-28", "DERIVA_DISPARADOR": "fixture",
                "DERIVA_RUN_ID": run_id, "PATH": f"{self.d / 'bin'}:{os.environ['PATH']}", **extra}

    def lanza(self, run_id: str, **extra) -> subprocess.Popen:
        return subprocess.Popen(["bash", str(self.src / "tools" / "deriva_cron.sh")], env=self.env(run_id, **extra),
                                cwd=self.d, start_new_session=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    def corre(self, run_id: str, **extra) -> tuple[int, str]:
        p = self.lanza(run_id, **extra)
        salida, _ = p.communicate(timeout=90)
        return p.returncode, salida

    def espera_a_media_suite(self, run_id: str) -> subprocess.Popen:
        listo = self.d / f"listo-{run_id}"
        p = self.lanza(run_id, STUB_SUITE="cuelga", STUB_LISTO=str(listo))
        for _ in range(300):
            if listo.exists():
                return p
            time.sleep(0.1)
        os.killpg(p.pid, signal.SIGKILL)
        raise AssertionError("la suite falsa no llegó a arrancar: " + p.communicate()[0][-400:])

    def worktrees(self) -> list[str]:
        return [l for l in self.git("worktree", "list", "--porcelain").splitlines() if l.startswith("worktree ")]

    def evidencia(self, nombre: str) -> list[str]:
        return sorted(tarfile.open(self.estado / nombre / "no-versionados.tgz").getnames())


def test_p1_cierre_es_best_effort_con_disco_lleno_y_conserva_el_codigo_de_salida():
    casos = [  # (CONSERVA_WORKTREE, CIERRE_ESCRITO, ESTADO_DIR inescribible): las tres rutas de cierre + mkdir roto
        (1, 1, False), (0, 1, False), (0, 0, False), (1, 1, True)]
    for conserva, cierre, sin_estado in casos:
        with tempfile.TemporaryDirectory(dir=RAIZ.parent) as d:
            d = Path(d)
            repo = d / "repo"
            sh = lambda *a: subprocess.run(a, cwd=repo, check=True, capture_output=True, text=True)
            repo.mkdir()
            sh("git", "init", "-q")
            sh("git", "-c", "user.email=a@b", "-c", "user.name=t", "commit", "-q", "--allow-empty", "-m", "x")
            vivo = d / "wt-vivo"
            sh("git", "worktree", "add", "-q", "--detach", str(vivo))
            (vivo / "universo.json").write_text("{}")
            (d / "archivo").write_text("no es directorio")  # mkdir -p bajo un archivo falla
            estado = d / "archivo" / "estado" if sin_estado else d / "estado"
            script = (
                f'export DERIVA_CRON_SOLO_DEFINE=1 DERIVA_LOG_ROOT="{d}/log" DERIVA_WORKTREES_DIR="{d}/wt" '
                f'DERIVA_TMPDIR="{d}/tmp" DERIVA_RUN_ID=r1 DERIVA_FECHA=2026-09-28\n'
                f'source "{DERIVA}"  # trae `set -euo pipefail` y el `log` REAL (tee)\n'
                f'SOURCE_REPO_DIR="{repo}"; LOGFILE=/dev/full; ESTADO_DIR="{estado}"\n'
                f'WORKTREE_TEMP="{vivo}"; CONSERVA_WORKTREE={conserva}; CIERRE_ESCRITO={cierre}\n'
                f'export TMPDIR="$TMPDIR_BASE/run-r1"; mkdir -p "$TMPDIR"; touch "$TMPDIR/x"\n'
                f'{_funcion_sh("finalizar")}trap finalizar EXIT\nexit 7\n')
            r = subprocess.run(["bash", "-c", script], capture_output=True, text=True, timeout=60)
            etiqueta = f"conserva={conserva} cierre={cierre} sin_estado={sin_estado}: {r.stderr[-300:]}"
            assert r.returncode == 7, etiqueta  # el cierre no pisa el código de salida de la corrida
            assert not vivo.exists(), etiqueta
            assert not (d / "tmp" / "run-r1").exists(), etiqueta
            assert len(sh("git", "worktree", "list").stdout.strip().splitlines()) == 1, etiqueta
            if not sin_estado and (conserva or not cierre):  # bandera o salida sin huella: el trabajo se respalda
                assert (estado / "evidencia-r1" / "no-versionados.tgz").exists(), etiqueta


def test_p1_e2e_kill_duro_deja_huerfano_y_la_corrida_siguiente_lo_recoge_con_evidencia():
    with tempfile.TemporaryDirectory(dir=RAIZ.parent) as d:
        c = _Canal(Path(d))
        a = c.espera_a_media_suite("A")
        os.killpg(a.pid, signal.SIGKILL)  # OOM/corte: ni trap ni cierre
        a.communicate()
        huerfanos = [p for p in c.wt.iterdir() if p.name.startswith("modelado-deriva-")]
        assert len(huerfanos) == 1 and (huerfanos[0] / "universo-PARCIAL.json").exists()  # directorio VIVO
        assert (c.tmp / "run-A").is_dir() and len(c.worktrees()) == 2
        for nombre in ("modelado-deriva-2026-09-27-bbbbbb", "ajeno"):  # otro huérfano vivo y un worktree que no es del canal
            c.git("worktree", "add", "-q", "--detach", str(c.wt / nombre))
            (c.wt / nombre / "trabajo.json").write_text("{}")
        rc, salida = c.corre("B")
        assert rc == 0, salida[-600:]
        assert [p.name for p in c.wt.iterdir()] == ["ajeno"], list(c.wt.iterdir())  # solo se recoge lo del canal
        assert not list(c.tmp.glob("run-*")) and len(c.worktrees()) == 2
        assert c.evidencia(f"evidencia-B-huerfano-{huerfanos[0].name}") == ["universo-PARCIAL.json"]  # no se pierde
        assert c.evidencia("evidencia-B-huerfano-modelado-deriva-2026-09-27-bbbbbb") == ["trabajo.json"]  # los dos, en una pasada
        assert not (c.estado / "evidencia-B").exists()  # la corrida sana no deja evidencia propia


def test_p1_e2e_commit_rechazado_y_sigterm_guardan_evidencia_antes_de_borrar():
    with tempfile.TemporaryDirectory(dir=RAIZ.parent) as d:
        c = _Canal(Path(d))
        hook = c.src / ".git" / "hooks" / "pre-commit"
        hook.write_text("#!/bin/sh\nexit 1\n")
        hook.chmod(0o755)
        rc, salida = c.corre("C")  # un pre-commit rechaza el commit del [deriva]
        assert rc == 2, salida[-600:]
        assert "motivo=PARO-PUBLICACION" in c.log.read_text(encoding="utf-8")  # llegó a su PARO, no abortó a medias
        assert "universo-2026-09-28.json" in (c.estado / "evidencia-C" / "cambios.patch").read_text(encoding="utf-8")
        assert list(c.wt.iterdir()) == [] and len(c.worktrees()) == 1
        hook.unlink()
        d_ = c.espera_a_media_suite("D")
        try:
            os.kill(d_.pid, signal.SIGTERM)  # solo al bash: el trap EXIT corre y no hay huella
            d_.wait(timeout=30)
        finally:
            os.killpg(d_.pid, signal.SIGKILL)  # la suite falsa hereda el lock: fuera
        assert c.evidencia("evidencia-D") == ["universo-PARCIAL.json"]
        assert list(c.wt.iterdir()) == [] and len(c.worktrees()) == 1
