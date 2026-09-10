#!/usr/bin/env python3
"""Snapshot congelado de M para las 14 celdas del marco -- ACTO GEN2-M-SNAPSHOT-TRIADA
(ENCARGO 4/5), 10/sep/2026.

Congela la identidad del motor vigente (P1), re-deriva en vivo cada una de
las 14 celdas del universo con `tools.emite_m.emite_celda` (misma funcion,
no reimplementada) y la compara campo a campo contra el archivo de
`corridas-M/` que la resolucion v1.3 ya establecida por `ACTO MAESTRA38-M13`
(marco-M-sorteado-v1_3.tsv fuente_M_por_celda / M-POR-CELDA-v1_3, encargo
`forense/encargos/2026-09-07-MAESTRA38-M13-M-POR-CELDA-v1_3.md` §16) resuelve
para esa celda -- orden `M-<id>__v1_3.json > M-<id>.json > M-<id>__v1_2.json`,
primera coincidencia exacta.

Identidad de campo == identidad de estado material del motor (el emisor es
puro y determinista sobre `milpa/tramite.yaml` + `milpa/procedencia.yaml`):
si TODO campo no exento coincide, el archivo existente se REUTILIZA (se cita
su hash y procedencia, no se reescribe). Si algun campo no exento difiere, la
celda se marca REEMITIR y este acto se detiene sin escribir un M nuevo bajo
un valor no verificado -- la regla de eleccion es solo por identidad de
snapshot, nunca por cercania a R (P2 del encargo).

CIEGO A R: este script jamas abre `forense/prereg-duelo-v2/corridas-R/` ni
ninguna columna de valor de R -- ver `archivos_abiertos()`.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.emite_m import (  # noqa: E402
    CORRIDAS_M,
    RUTA_CANDIDATOS_V1_1,
    RUTA_TRAMITE,
    emite_celda,
    leer_por_id,
)
from milpa.src.emisor import cargar_reglas  # noqa: E402

DUELO = REPO_ROOT / "forense" / "prereg-duelo-v2"
MARCO_V1_3 = DUELO / "marco-M-sorteado-v1_3.tsv"
FUENTE_ACTO = "ACTO GEN2-M-SNAPSHOT-TRIADA (ENCARGO 4/5), 10/sep/2026 -- snapshot/verificacion, no re-emision comiteada"

# Las 14 celdas del universo U0 (F5-contrato-triada-spec-v1_0.md §1.1)
U0 = [
    "CIV-M-01", "CIV-M-02", "CIV-M-04", "CIV-M-10", "CIV-M-12", "CIV-M-13",
    "DIN-M-01",
    "FAM-M-01", "FAM-M-05", "FAM-M-06", "FAM-M-07",
    "TRA-M-02", "TRA-M-03", "TRA-M-07",
]

# Celdas de UR (F5-contrato-triada-spec-v1_0.md §1.2) -- con arbitro R sellado.
UR = {"CIV-M-01", "CIV-M-02", "CIV-M-04", "CIV-M-10", "CIV-M-12", "CIV-M-13"}

# Campos exentos de comparacion byte a byte (mismos exentos que la regresion
# P2 de tools/emite_m.py: `fuente` cita el acto que corre, por construccion
# distinto entre la emision original y esta verificacion).
CAMPOS_EXENTOS = {"fuente", "archivos_abiertos"}
# Campos donde solo el NUMERO DE LINEA de la cita puede correr, Y ADEMAS
# (extension de este script sobre tools/emite_m.py::_compara_cita_con_linea)
# puede haberse anexado provenance GEN2 (`corrida0_resultado_id` /
# `corrida0_generacion` + comentario de adopcion) DESPUES del dict original
# {conducta, p, clase} -- verificado hallazgo real de este acto: varias
# reglas del motor fueron enriquecidas por actos GEN2-LOTE-*/PRIMERA-SILLA
# con una remedicion independiente (corrida0) que declara explicitamente
# "el `p` NO se movio: se declara de donde viene", con delta de
# reproduccion del orden de 1e-7/1e-8 al redondeo publicado. Se tolera SOLO
# si el texto original aparece INTACTO como prefijo del texto vivo (mismo
# ruta, mismo conducta/p/clase) -- cualquier otra diferencia es FALLA.
CAMPOS_CITA_LINEA = {"cita_p", "cita_ola_calibracion"}
# Campo cuyo VALOR SUSTANTIVO (no la ruta de marco citada dentro del texto)
# es lo que importa -- mismo patron que tools/emite_m.py::_CAMPOS_SOLO_VALOR.
CAMPOS_SOLO_VALOR_SIN_RUTA_MARCO = {"correcciones_aplicadas_por_referencia"}
# Campos que un original mas viejo puede traer de mas (anotacion narrativa
# especifica de esa celda, p.ej. DIN-M-01/aviso_F_DD) que el emisor generico
# de hoy no reproduce -- declarados, no fatales, no invalidan identidad de
# (regla, conducta, p, valor_punto, clase, estado_M, grado_DD).
CAMPOS_NARRATIVOS_OPCIONALES = {"aviso_F_DD", "razon_DD_marco"}


def sha256_archivo(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=REPO_ROOT, capture_output=True,
                           text=True, check=True).stdout.strip()


def archivo_resuelto_v1_3(id_celda: str) -> Path | None:
    """Orden de resolucion sellado por MAESTRA38-M13 §16:
    M-<id>__v1_3.json > M-<id>.json > M-<id>__v1_2.json, primera coincidencia."""
    for nombre in (f"M-{id_celda}__v1_3.json", f"M-{id_celda}.json", f"M-{id_celda}__v1_2.json"):
        candidato = CORRIDAS_M / nombre
        if candidato.exists():
            return candidato
    return None


def compara_cita_con_linea(original: str, regenerado: str) -> tuple[bool, str]:
    import re
    patron = re.compile(r"^(?P<ruta>.+?):(?P<linea>\d+)\s*--\s*(?P<texto>.*)$", re.S)
    m_o, m_r = patron.match(original), patron.match(regenerado)
    if not m_o or not m_r:
        return False, "no calza '<ruta>:<linea> -- <texto>'"
    if m_o.group("ruta") != m_r.group("ruta"):
        return False, "ruta citada diverge"
    if m_o.group("texto") == m_r.group("texto"):
        return True, "OK" if m_o.group("linea") == m_r.group("linea") else "OK (linea corrida, texto identico)"
    texto_o = m_o.group("texto")
    # El original cierra su dict con '}'; si el motor le anexo despues mas
    # claves (corrida0_resultado_id/corrida0_generacion) dentro del MISMO
    # dict, el cierre '}' del original ya no es el ultimo caracter del vivo
    # -- se compara el original SIN su '}' final como prefijo del vivo, y se
    # exige que el vivo, tras ese prefijo, continue con una coma (mas claves
    # en el mismo dict) antes de cerrar en algun '}' posterior.
    nucleo_o = texto_o[:-1] if texto_o.rstrip().endswith("}") else texto_o
    if m_r.group("texto").startswith(nucleo_o) and m_r.group("texto")[len(nucleo_o):].lstrip().startswith(","):
        return True, ("OK-CON-PROVENANCE-ANEXADA (el dict original {conducta,p,clase} aparece intacto "
                       "como prefijo del dict vivo, que le anexa mas claves -- milpa/tramite.yaml fue "
                       "enriquecido con una remedicion GEN2/corrida0 de este mismo p DESPUES de la "
                       "emision original; el `p` no se movio, se declara de donde viene)")
    return False, "texto citado diverge mas alla de una provenance anexada al final"


def compara_correccion_sin_ruta_marco(original: str, regenerado: str) -> tuple[bool, str]:
    import re
    limpio = lambda s: re.sub(r"marco-M-sorteado-v1_\d+\.tsv", "marco-M-sorteado-vX.tsv", s)
    if limpio(original) == limpio(regenerado):
        return True, "OK (solo difiere el nombre de marco citado, version esperada)"
    return False, "diverge en sustancia, no solo en el nombre del marco citado"


def identidad_del_motor() -> dict:
    return {
        "commit": git("rev-parse", "HEAD"),
        "commit_fecha": git("log", "-1", "--format=%cI", "HEAD"),
        "hash_tree_milpa": git("rev-parse", "HEAD:milpa"),
        "hash_emisor_py": sha256_archivo(REPO_ROOT / "milpa" / "src" / "emisor.py"),
        "hash_tramite_yaml": sha256_archivo(REPO_ROOT / "milpa" / "tramite.yaml"),
        "hash_procedencia_yaml": sha256_archivo(REPO_ROOT / "milpa" / "procedencia.yaml"),
        "hash_emite_m_py": sha256_archivo(REPO_ROOT / "tools" / "emite_m.py"),
        "hash_marco_v1_3": sha256_archivo(MARCO_V1_3),
        "hash_candidatos_v1_1": sha256_archivo(RUTA_CANDIDATOS_V1_1),
        "python": sys.version.split()[0],
        "fecha_snapshot": datetime.now(timezone.utc).isoformat(),
        "referencia_historica": {
            "acto": "PR #674 (ACTO GEN2-F5-DUELO-CALC)",
            "commit_674": "eab46ed24a60ff94835831698648ca8df1c07da7",
            "diff_milpa_674_a_HEAD": git("diff", "--stat", "eab46ed24a60ff94835831698648ca8df1c07da7..HEAD", "--", "milpa/") or "(vacio -- milpa/ identico)",
        },
    }


def archivos_abiertos() -> list[str]:
    return [
        "milpa/tramite.yaml  [lectura via emisor.cargar_reglas]",
        "milpa/procedencia.yaml  [lectura via emisor (import del modulo)]",
        "canon/modelo-decision-v4_0.md  [lectura via emisor (import del modulo)]",
        f"{MARCO_V1_3.relative_to(REPO_ROOT)}  [lectura]",
        f"{RUTA_CANDIDATOS_V1_1.relative_to(REPO_ROOT)}  [lectura]",
        "forense/prereg-duelo-v2/corridas-M/M-*.json  [lectura, verificacion de identidad]",
    ]


def evalua_firewall(fila: dict, registro_vivo: dict) -> tuple[str, str]:
    """LIMPIO-DE-OBJETIVO / CONTAMINADO-POR-OBJETIVO / INDETERMINADO-POR-PROCEDENCIA.

    Regla (P3 del encargo): contaminada si algun valor que M consume ES
    exactamente el arbitro de esa celda, la misma ola/variable objetivo, o
    una materializacion directa de ella. Se decide por cadena documentada
    (que objeto concreto alimenta a cual), nunca por cercania numerica.

    Señal mecanica disponible hoy: `grado_DD` (F-DD, ADR-237) ya compara
    (encuesta,ola) de la celda contra `ola_calibracion` de la conducta que
    M emite para ella. `P0 VERIFICACION` == misma encuesta+ola == la
    calibracion de M ES la misma ola que la celda evalua (materializacion
    directa del objetivo) -> CONTAMINADO-POR-OBJETIVO. `P1 PUNTUA` == ola
    distinta -> LIMPIO-DE-OBJETIVO por esta via. No decide sola: para las
    6 celdas de UR se declara ademas la cadena de payload (M vs R) citada
    verbatim de `F5-contrato-triada-spec-v1_0.md` §1.4 (payload distinto,
    no-comparabilidad declarada por escrito en la propia regla).
    """
    grado_DD = registro_vivo["grado_DD"]
    if grado_DD.startswith("P0"):
        return ("CONTAMINADO-POR-OBJETIVO",
                f"F-DD={grado_DD}: la ola_calibracion de M coincide con (encuesta,ola) de la "
                f"propia celda -- {registro_vivo['razon_grado_DD']}")
    if not grado_DD.startswith("P1"):
        return ("INDETERMINADO-POR-PROCEDENCIA",
                f"grado_DD inesperado (ni P0 ni P1): {grado_DD!r}")

    id_celda = fila["id"]
    if id_celda in UR:
        return ("LIMPIO-DE-OBJETIVO",
                f"F-DD={grado_DD} (ola_calibracion != ola de la celda) Y censo directo de payload "
                f"(F5-contrato-triada-spec-v1_0.md §1.4): M calibra de payload_manifiesto_id "
                f"'envipe2025_csv' (milpa/tramite.yaml, regla civico.denuncia.miedo_desconfianza); "
                f"R de {id_celda} se computa de Tmod_Vic.DBF de su propia ola "
                f"({fila['ola']}) -- objetos de payload distintos, no-comparabilidad declarada por "
                f"escrito en la propia regla (milpa/tramite.yaml:488). Ningun valor consumido por M "
                f"es el arbitro de esta celda ni una materializacion directa de su ola/variable.")
    return ("LIMPIO-DE-OBJETIVO",
            f"F-DD={grado_DD} (ola_calibracion != (encuesta,ola) de la celda); {id_celda} no tiene "
            f"arbitro R sellado (fuera de UR, NO-EXISTE-ARBITRO, no AUSENTE) -- no hay resultado R "
            f"que M pudiera haber consumido para esta celda. Verificado solo por la via mecanica de "
            f"F-DD; no cierra la pregunta para siempre si en el futuro se calcula R para esta celda.")


def main() -> int:
    identidad = identidad_del_motor()
    reglas_por_id = {r.id: r for r in cargar_reglas()}
    lineas_tramite = RUTA_TRAMITE.read_text(encoding="utf-8").splitlines()
    candidatos = leer_por_id(RUTA_CANDIDATOS_V1_1)
    filas_v1_3 = leer_por_id(MARCO_V1_3)

    celdas = []
    todas_identicas = True
    for id_celda in U0:
        fila = dict(filas_v1_3[id_celda])
        archivo_existente = archivo_resuelto_v1_3(id_celda)
        if archivo_existente is None:
            celdas.append({"id_celda": id_celda, "estado": "SIN-ARCHIVO-EXISTENTE-PARA-COMPARAR"})
            todas_identicas = False
            continue

        original = json.loads(archivo_existente.read_text(encoding="utf-8"))
        vivo = emite_celda(fila, reglas_por_id, lineas_tramite, candidatos,
                            fuente_acto=FUENTE_ACTO, marco_nombre="marco-M-sorteado-v1_3.tsv")

        divergencias = []
        notas_declaradas = []
        for campo in sorted(set(original) | set(vivo)):
            if campo in CAMPOS_EXENTOS:
                continue
            if campo not in original or campo not in vivo:
                if campo in CAMPOS_NARRATIVOS_OPCIONALES and campo not in vivo:
                    notas_declaradas.append(
                        f"{campo}: presente solo en el original (anotacion narrativa especifica de "
                        f"esa celda; el emisor generico de hoy no la reproduce, no invalida identidad "
                        f"de p/regla/conducta) = {original[campo]!r}")
                    continue
                divergencias.append(f"{campo}: presente solo en {'vivo' if campo not in original else 'original'}")
                continue
            if campo in CAMPOS_CITA_LINEA:
                ok, msg = compara_cita_con_linea(original[campo], vivo[campo])
                if ok:
                    if "PROVENANCE" in msg:
                        notas_declaradas.append(f"{campo}: {msg}")
                else:
                    divergencias.append(f"{campo}: original={original[campo]!r} vivo={vivo[campo]!r} ({msg})")
                continue
            if campo in CAMPOS_SOLO_VALOR_SIN_RUTA_MARCO:
                ok, msg = compara_correccion_sin_ruta_marco(original[campo], vivo[campo])
                if ok:
                    notas_declaradas.append(f"{campo}: {msg}")
                else:
                    divergencias.append(f"{campo}: original={original[campo]!r} vivo={vivo[campo]!r} ({msg})")
                continue
            if original[campo] != vivo[campo]:
                divergencias.append(f"{campo}: original={original[campo]!r} vivo={vivo[campo]!r}")

        identico = not divergencias
        todas_identicas = todas_identicas and identico
        firewall_estado, firewall_razon = evalua_firewall(fila, vivo)

        celdas.append({
            "id_celda": id_celda,
            "punto_M": vivo["p"],
            "regla": vivo["regla"],
            "conducta": vivo["conducta"],
            "clase": vivo["clase"],
            "estado_M": vivo["estado_M"],
            "ola_calibracion": vivo["ola_calibracion"],
            "grado_DD": vivo["grado_DD"],
            "identidad_confirmada": identico,
            "divergencias_vs_snapshot_previo": divergencias,
            "notas_declaradas_no_fatales": notas_declaradas,
            "corrida_M": "REUTILIZADA" if identico else "REEMITIR-REQUERIDO-NO-EJECUTADO",
            "archivo_fuente": str(archivo_existente.relative_to(REPO_ROOT)),
            "archivo_fuente_sha256": sha256_archivo(archivo_existente),
            "archivo_fuente_procedencia": original.get("fuente"),
            "en_UR": id_celda in UR,
            "estado_firewall": firewall_estado,
            "razon_firewall": firewall_razon,
            "razon_exclusion": "" if firewall_estado == "LIMPIO-DE-OBJETIVO" else firewall_razon,
        })

    salida = {
        "acto": "ACTO GEN2-M-SNAPSHOT-TRIADA (ENCARGO 4/5)",
        "identidad_del_motor": identidad,
        "regla_de_eleccion": "identidad de snapshot (campo a campo contra el estado material vigente del motor), nunca cercania a R",
        "contador_gen2": "SI",
        "ciego_a_R": "SI -- este script jamas abrio forense/prereg-duelo-v2/corridas-R/ ni ninguna columna de valor de R",
        "archivos_abiertos": archivos_abiertos(),
        "todas_las_14_celdas_identicas_al_estado_previo": todas_identicas,
        "celdas": celdas,
    }
    salida_path = DUELO / "snapshot-M-triada-v1_0.json"
    salida_path.write_text(json.dumps(salida, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")

    print(f"IDENTIDAD DEL MOTOR: commit={identidad['commit'][:12]} tree_milpa={identidad['hash_tree_milpa'][:12]}")
    print(f"diff milpa/ (674..HEAD): {identidad['referencia_historica']['diff_milpa_674_a_HEAD']!r}")
    for c in celdas:
        if "estado" in c:
            print(f"  {c['id_celda']}: {c['estado']}")
            continue
        print(f"  {c['id_celda']}: p={c['punto_M']} identidad_confirmada={c['identidad_confirmada']} "
              f"firewall={c['estado_firewall']} fuente={c['archivo_fuente']}")
    print(f"\nTODAS IDENTICAS AL SNAPSHOT PREVIO: {todas_identicas}")
    print(f"Sellado: {salida_path.relative_to(REPO_ROOT)}")
    return 0 if todas_identicas else 1


if __name__ == "__main__":
    raise SystemExit(main())
