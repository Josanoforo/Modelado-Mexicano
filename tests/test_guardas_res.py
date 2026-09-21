#!/usr/bin/env python3
"""Las seis guardas G1..G6, PROBADAS POR MUTACION.

ACTO `GEN2-TUBERIA-RES-LLAVE-1`, P6.

Cada caso parte de un estado VALIDO y cambia UNA cosa: la que la guarda
existe para atrapar. Un caso que pasa por la razon equivocada no prueba nada,
asi que cada mutacion comprueba ademas que el motivo cita SU guarda.

Y cada guarda se ejercita tambien sobre el ARBOL REAL: una guarda que solo
corre contra fixtures no es un COMMIT-1 (D-22).
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "tools"))

import ci_guardas_res as G  # noqa: E402
import corrida0  # noqa: E402
import resuelve_citas  # noqa: E402

K1 = "tramite::regla.a::conducta_uno"
K2 = "tramite::regla.a::conducta_dos"
K1_VIEJA = "tramite::regla.a::conducta_uno_vieja"


def _fila(llave, numero, estado=corrida0.REG_VIGENTE):
    return {"llave_logica": llave, "resultado_id": numero, "estado": estado,
            "fecha": "2026-09-21", "commit": "deadbeef"}


# ── G1 ────────────────────────────────────────────────────────────────────

def _registro_git(tmp: Path, filas_base, filas_head):
    """Un repo de verdad con la base en un commit y HEAD en otro."""
    subprocess.run(["git", "init", "-q", "-b", "base", str(tmp)], check=True)
    ruta = tmp / G.RUTA_REGISTRO
    ruta.parent.mkdir(parents=True, exist_ok=True)

    def escribe(filas):
        lineas = ["\t".join(corrida0.COLS_REGISTRO_RES)]
        lineas += ["\t".join(str(f[c]) for c in corrida0.COLS_REGISTRO_RES)
                   for f in filas]
        ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")

    env = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t",
           "PATH": "/usr/bin:/bin"}
    escribe(filas_base)
    subprocess.run(["git", "-C", str(tmp), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(tmp), "commit", "-qm", "base"],
                   check=True, env=env)
    # La ref base tiene que quedar FIJA: si apunta a la rama, avanza con
    # HEAD y la guarda se compara contra si misma -- un PASA vacio.
    subprocess.run(["git", "-C", str(tmp), "tag", "refbase"], check=True)
    escribe(filas_head)
    subprocess.run(["git", "-C", str(tmp), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(tmp), "commit", "-qm", "head"],
                   check=True, env=env)
    return ruta


def test_g1_pasa_cuando_solo_se_añade():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        _registro_git(tmp, [_fila(K1, "RES-0001")],
                      [_fila(K1, "RES-0001"), _fila(K2, "RES-0002")])
        actual = G._parsea_registro(
            (tmp / G.RUTA_REGISTRO).read_text(encoding="utf-8"))
        g = G.g1_registro_inmutable("refbase", repo=tmp, registro_actual=actual)
        assert g.estado == "PASA", g.motivos


def test_g1_falla_si_un_par_de_la_base_cambia_de_numero():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        _registro_git(tmp, [_fila(K1, "RES-0001")], [_fila(K1, "RES-0002")])
        actual = G._parsea_registro(
            (tmp / G.RUTA_REGISTRO).read_text(encoding="utf-8"))
        g = G.g1_registro_inmutable("refbase", repo=tmp, registro_actual=actual)
        assert g.estado == "FALLA"
        assert any("G1" in m and K1 in m for m in g.motivos), g.motivos


def test_g1_no_se_degrada_a_pasa_sin_ref_base():
    g = G.g1_registro_inmutable("no-existe-esta-ref")
    assert g.estado == G.NO_VERIFICABLE
    assert g.estado != "PASA"


# ── G2 ────────────────────────────────────────────────────────────────────

def test_g2_pasa_con_un_retiro_normal():
    g = G.g2_sin_reuso([_fila(K1, "RES-0001"),
                        _fila(K1, "RES-0001", corrida0.REG_RETIRADO),
                        _fila(K2, "RES-0002")])
    assert g.estado == "PASA", g.motivos


def test_g2_falla_si_un_numero_retirado_se_reasigna():
    g = G.g2_sin_reuso([_fila(K1, "RES-0001"),
                        _fila(K1, "RES-0001", corrida0.REG_RETIRADO),
                        _fila(K2, "RES-0001")])
    assert g.estado == "FALLA"
    assert any(m.startswith("G2:") for m in g.motivos), g.motivos


# ── G3 ────────────────────────────────────────────────────────────────────

def _repo_con_spec(tmp: Path, texto_spec: str, filas_base):
    subprocess.run(["git", "init", "-q", "-b", "base", str(tmp)], check=True)
    env = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t",
           "PATH": "/usr/bin:/bin"}
    reg = tmp / G.RUTA_REGISTRO
    reg.parent.mkdir(parents=True, exist_ok=True)
    lineas = ["\t".join(corrida0.COLS_REGISTRO_RES)]
    lineas += ["\t".join(str(f[c]) for c in corrida0.COLS_REGISTRO_RES)
               for f in filas_base]
    reg.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    (tmp / "data/corrida0/CALC-X").mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "-C", str(tmp), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(tmp), "commit", "-qm", "base"],
                   check=True, env=env)
    subprocess.run(["git", "-C", str(tmp), "tag", "refbase"], check=True)
    (tmp / "data/corrida0/CALC-X/spec.md").write_text(texto_spec,
                                                      encoding="utf-8")
    subprocess.run(["git", "-C", str(tmp), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(tmp), "commit", "-qm", "head"],
                   check=True, env=env)


def test_g3_pasa_con_una_cita_que_existe_en_la_base():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        _repo_con_spec(tmp, "releva RES-0001\n", [_fila(K1, "RES-0001")])
        g = G.g3_citas_nuevas("refbase", repo=tmp)
        assert g.estado == "PASA", g.motivos


def test_g3_falla_si_la_spec_tocada_cita_un_res_inexistente_en_la_base():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        _repo_con_spec(tmp, "releva RES-0099\n", [_fila(K1, "RES-0001")])
        g = G.g3_citas_nuevas("refbase", repo=tmp)
        assert g.estado == "FALLA"
        assert any("RES-0099" in m for m in g.motivos), g.motivos


def test_g3_falla_si_la_spec_tocada_cita_corr():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        _repo_con_spec(tmp, "releva CORR-0009\n", [_fila(K1, "RES-0001")])
        g = G.g3_citas_nuevas("refbase", repo=tmp)
        assert g.estado == "FALLA"
        assert any("CORR-0009" in m and "citable" in m for m in g.motivos), \
            g.motivos


# ── G4 ────────────────────────────────────────────────────────────────────

def test_g4_pasa_con_una_cita_a_llave_vigente():
    g = G.g4_sin_citas_colgantes(
        vigentes={K1: "RES-0001"}, retiradas={}, alias={},
        pines=[{"llave_logica": K1}], tabla=[])
    assert g.estado == "PASA", g.motivos


def test_g4_pasa_si_un_alias_declarado_sucede_a_la_llave_citada():
    g = G.g4_sin_citas_colgantes(
        vigentes={K1: "RES-0001"}, retiradas={K1_VIEJA: "RES-0001"},
        alias={K1: (K1_VIEJA,)},
        pines=[], tabla=[{"calc_id": "CALC-X", "token": "RES-0001",
                          "llave_logica": K1_VIEJA}])
    assert g.estado == "PASA", g.motivos


def test_g4_falla_si_el_consumidor_renombro_sin_declarar_el_alias():
    g = G.g4_sin_citas_colgantes(
        vigentes={K1: "RES-0001"}, retiradas={K1_VIEJA: "RES-0009"},
        alias={},                       # LA MUTACION: no hay alias declarado
        pines=[], tabla=[{"calc_id": "CALC-X", "token": "RES-0009",
                          "llave_logica": K1_VIEJA}])
    assert g.estado == "FALLA"
    assert any(m.startswith("G4:") and K1_VIEJA in m for m in g.motivos), \
        g.motivos


def test_g4_falla_si_un_pin_de_mesa_cita_una_llave_que_ya_no_existe():
    g = G.g4_sin_citas_colgantes(
        vigentes={K1: "RES-0001"}, retiradas={}, alias={},
        pines=[{"llave_logica": "marco-M::NO-EXISTE::R"}], tabla=[])
    assert g.estado == "FALLA"
    assert any("pines-de-mesa" in m for m in g.motivos), g.motivos


# ── G5 ────────────────────────────────────────────────────────────────────

def test_g5_falla_si_una_cita_sellada_no_tiene_fila_en_la_tabla():
    """Mutacion sobre el ARBOL REAL: se quita UNA fila de la tabla."""
    tabla = resuelve_citas.lee_tabla()
    assert tabla, "la tabla de P4 debe existir en el arbol"
    sellados = sorted({f["calc_id"] for f in tabla})
    assert G.g5_tabla_completa(tabla, sellados).estado == "PASA"
    mutada = [f for f in tabla if not (f["calc_id"] == tabla[0]["calc_id"]
                                       and f["token"] == tabla[0]["token"])]
    g = G.g5_tabla_completa(mutada, sellados)
    assert g.estado == "FALLA"
    assert any(tabla[0]["token"] in m for m in g.motivos), g.motivos


# ── G6 ────────────────────────────────────────────────────────────────────

def test_g6_pasa_sobre_una_biyeccion():
    g = G.g6_biyeccion(vigentes={K1: "RES-0001", K2: "RES-0002"}, alias={})
    assert g.estado == "PASA", g.motivos


def test_g6_falla_si_un_numero_apunta_a_dos_llaves_vigentes():
    g = G.g6_biyeccion(vigentes={K1: "RES-0001", K2: "RES-0001"}, alias={})
    assert g.estado == "FALLA"
    assert any("un numero, una llave" in m for m in g.motivos), g.motivos


def test_g6_falla_si_el_nombre_viejo_y_el_nuevo_quedan_vivos():
    """El defecto exacto del prototipo v1.0 que mesa señalo."""
    g = G.g6_biyeccion(vigentes={K1: "RES-0001", K1_VIEJA: "RES-0001"},
                       alias={K1: (K1_VIEJA,)})
    assert g.estado == "FALLA"
    assert any("vivos a la vez" in m for m in g.motivos), g.motivos


# ── el arbol real ─────────────────────────────────────────────────────────

def test_las_cuatro_guardas_sin_historia_pasan_en_el_arbol():
    """D-22: una guarda que solo ejercita fixtures no es un COMMIT-1."""
    for g in G.corre():
        assert g.estado == "PASA", (g.id, g.motivos)


def test_el_registro_del_arbol_conserva_la_numeracion_de_la_demanda():
    """Criterio 1, cableado: el registro y la vista no pueden separarse."""
    import csv
    ruta = RAIZ / "data" / "corrida0" / "demanda-resultados.tsv"
    lineas = [l for l in ruta.read_text(encoding="utf-8").splitlines(True)
              if not l.startswith("#")]
    vigentes, _, _ = corrida0.estado_registro_res()
    for f in csv.DictReader(lineas, delimiter="\t"):
        assert vigentes.get(f["llave_logica"]) == f["resultado_id"], f


if __name__ == "__main__":
    fallos = 0
    for nombre, fn in sorted(list(globals().items())):
        if not nombre.startswith("test_") or not callable(fn):
            continue
        try:
            fn()
            print(f"  [ ok ]  {nombre}")
        except Exception as e:                       # noqa: BLE001
            fallos += 1
            print(f"  [FAIL]  {nombre}: {type(e).__name__}: {e}")
    print(f"casos = ... · fallos = {fallos}")
    raise SystemExit(1 if fallos else 0)
