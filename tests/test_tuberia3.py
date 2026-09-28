"""ACTO GEN2-TUBERIA-3 · huérfano (D-21). Atrapa: P1 worktrees del canal en el
tmpfs sin prune; P2 contador legacy movido sin definición; P3 `status` que dice
otra cosa que `demanda` tras el dictamen. Ejecutar: pytest -q tests/test_tuberia3.py"""
import re
import shutil
import subprocess
import sys
import tempfile
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
