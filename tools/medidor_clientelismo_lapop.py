#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ACTO MAESTRA35-L9 · REGLAS-ACTIVOS-L3 — piezas (a) y (a') sobre LAPOP Mexico.

(a)  R7.7 `civico.clientelismo.turnout_no_vote_choice` — LAPOP 2019.
     La oferta de dadiva (`clien1na`) mueve la ASISTENCIA (`vb2`) y no la
     ELECCION (`vb3n`). Dos piernas, una corrida.
(a') R7.3 `civico.voto.agencia_con_secreto` / R7.6 `civico.voto.clientelar_si_observable`
     — LAPOP 2023. La transferencia (`mexwf1_19`) mueve la intencion de voto
     por el oficialismo (`vb20`) solo donde el voto NO se percibe secreto
     (`countfair3`).

Las dos olas viven en la raiz `descargas_mx` de `data/manifiesto.yaml`, no en
`data/raw` — un worktree nuevo la resuelve con `data/raices.local.yaml`
(gitignorada). Este modulo tambien exporta el cargador y el bootstrap de
conglomerado que usa `medidor_protesta_lapop.py`.

Uso:
    python3 tools/medidor_clientelismo_lapop.py --censo
    python3 tools/medidor_clientelismo_lapop.py --mide --json data/l9-clientelismo-v1_0.json
"""
import argparse, hashlib, json, os, random, sys

RAICES_LOCAL = "data/raices.local.yaml"
SEED = 42
REPLICAS = 10000

# Los payloads que este acto abre, por id de data/manifiesto.yaml.
PAYLOADS = {
    "2019": ("mexico_lapop_americasbarometer_2019_v1_0_w",
             "Descargas Manuales/Mexico LAPOP AmericasBarometer 2019 v1.0_W.dta"),
    "2021": ("mex_2021_lapop_americasbarometer_v1_2_w",
             "Descargas Manuales/MEX_2021_LAPOP_AmericasBarometer_v1.2_w.dta"),
    "2023": ("mex_2023_lapop_americasbarometer_v1_0_w",
             "Descargas Manuales/MEX_2023_LAPOP_AmericasBarometer_v1.0_w.dta"),
    "2006": ("518939279mexico_lapop_final_2006_data_set_092906",
             "Descargas Manuales/518939279mexico_lapop_final 2006 data set 092906.dta"),
}


def raiz(nombre="descargas_mx"):
    """Resuelve una raiz de data/manifiesto.yaml. PARA si no esta configurada:
    un worktree nuevo nace sin data/raices.local.yaml y un `no existe` que en
    realidad es `no configurada` es el falso negativo que A.13 persigue."""
    if not os.path.exists(RAICES_LOCAL):
        raise SystemExit(
            f"PARO: falta {RAICES_LOCAL}. La raiz '{nombre}' no esta configurada en "
            f"este worktree — esto NO es 'el payload no existe'. Escribe el archivo "
            f"con la linea `{nombre}: <ruta>` (valor de la casa en "
            f"forense/notas/2026-08-06-map1b-censo-raices.md:68).")
    for linea in open(RAICES_LOCAL, encoding="utf-8"):
        linea = linea.split("#")[0].strip()
        if linea.startswith(nombre + ":"):
            return linea.split(":", 1)[1].strip()
    raise SystemExit(f"PARO: {RAICES_LOCAL} no define '{nombre}'.")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def carga(ola):
    """Devuelve (DataFrame, meta, ruta, sha256). Verifica el payload por
    identidad (sha256 contra el manifiesto), no por nombre de archivo."""
    import pyreadstat
    pid, rel = PAYLOADS[ola]
    path = os.path.join(raiz(), rel)
    if not os.path.exists(path):
        raise SystemExit(f"PARO: payload ausente en disco: {path} (id {pid})")
    df, meta = pyreadstat.read_dta(path)
    return df, meta, path, sha256(path)


def sha_manifiesto(pid):
    """El sha256 que data/manifiesto.yaml declara para ese id, o None."""
    import re
    txt = open("data/manifiesto.yaml", encoding="utf-8").read()
    for ent in re.split(r"\n(?=- id: )", txt):
        m = re.match(r"- id: (\S+)", ent)
        if m and m.group(1) == pid:
            s = re.search(r"\n  sha256: (\S+)", ent)
            return s.group(1) if s else None
    return None


# ───────────────────────────── estimador ─────────────────────────────

def _cod(v):
    """LAPOP codifica los faltantes como 'a'/'b'/'c' (NS/NR/Inaplicable) y
    pyreadstat los entrega como NaN o como str. Devuelve int o None."""
    if v is None:
        return None
    if isinstance(v, str):
        s = v.strip()
        return int(s) if s.isdigit() else None
    try:
        if v != v:      # NaN
            return None
        return int(v)
    except (TypeError, ValueError):
        return None


def prop_bootstrap(filas, replicas=REPLICAS, seed=SEED):
    """filas: lista de (estrato, upm, peso, y) con y en {0,1}.

    Proporcion ponderada + IC95 por bootstrap de conglomerado: se remuestrean
    con reemplazo las UPM DENTRO de cada estrato (el diseno de LAPOP y de las
    ENIF/ENCUCI de INEGI), nunca las personas — remuestrear personas ignora el
    efecto de diseno y estrecha el IC de mentira.
    """
    filas = list(filas)
    if not filas:
        return None
    por_upm = {}
    for est, upm, w, y in filas:
        por_upm.setdefault((est, upm), []).append((w, y))
    estratos = {}
    for (est, upm) in por_upm:
        estratos.setdefault(est, []).append((est, upm))

    def punto(claves):
        num = den = 0.0
        for k in claves:
            for w, y in por_upm[k]:
                den += w
                num += w * y
        return num / den if den else None

    p_hat = punto(list(por_upm))
    rng = random.Random(seed)
    reps = []
    for _ in range(replicas):
        claves = []
        for est, lst in estratos.items():
            n = len(lst)
            if n < 2:                      # estrato singleton: entra tal cual
                claves.extend(lst)
                continue
            claves.extend(lst[rng.randrange(n)] for _ in range(n))
        p = punto(claves)
        if p is not None:
            reps.append(p)
    reps.sort()
    lo = reps[int(0.025 * len(reps))]
    hi = reps[min(len(reps) - 1, int(0.975 * len(reps)))]
    n_upm = len(por_upm)
    return {
        "p": p_hat,
        "ic95": [lo, hi],
        "n": len(filas),
        "numerador": sum(1 for _e, _u, _w, y in filas if y == 1),
        "n_estratos": len(estratos),
        "n_upm": n_upm,
        "estratos_singleton": sum(1 for l in estratos.values() if len(l) < 2),
        "replicas": len(reps),
        "poblacion_expandida": sum(w for _e, _u, w, _y in filas),
    }


def diff_bootstrap(filas_a, filas_b, replicas=REPLICAS, seed=SEED):
    """Diferencia de proporciones p(A) - p(B) con el MISMO remuestreo de UPM
    para las dos ramas: A y B comparten estrato/UPM, y tratarlas como
    independientes sobreestima la varianza de la diferencia (mismo argumento
    que tests/svystat.py::diff_ultimate_cluster hace para la version analitica).
    """
    marc = [(e, u, w, y, "A") for e, u, w, y in filas_a] + \
           [(e, u, w, y, "B") for e, u, w, y in filas_b]
    if not marc:
        return None
    por_upm = {}
    for est, upm, w, y, g in marc:
        por_upm.setdefault((est, upm), []).append((w, y, g))
    estratos = {}
    for (est, upm) in por_upm:
        estratos.setdefault(est, []).append((est, upm))

    def punto(claves):
        n_a = d_a = n_b = d_b = 0.0
        for k in claves:
            for w, y, g in por_upm[k]:
                if g == "A":
                    d_a += w; n_a += w * y
                else:
                    d_b += w; n_b += w * y
        if not d_a or not d_b:
            return None
        return n_a / d_a - n_b / d_b

    d_hat = punto(list(por_upm))
    rng = random.Random(seed)
    reps = []
    for _ in range(replicas):
        claves = []
        for est, lst in estratos.items():
            n = len(lst)
            if n < 2:
                claves.extend(lst)
                continue
            claves.extend(lst[rng.randrange(n)] for _ in range(n))
        d = punto(claves)
        if d is not None:
            reps.append(d)
    reps.sort()
    return {
        "d": d_hat,
        "ic95": [reps[int(0.025 * len(reps))],
                 reps[min(len(reps) - 1, int(0.975 * len(reps)))]],
        "replicas_validas": len(reps),
        "replicas_pedidas": replicas,
    }


# ───────────────────────────── P0 · censo A.4 ─────────────────────────────

# Lo que el censo busca, por regla. Un `None` en `hallado` lo llena la corrida.
CENSO_ITEMS = {
    "2019": ["clien1na", "clien1n", "clien4a", "clien4b", "vb2", "vb3n", "vb10",
             "vb20", "prot3", "vic1ext", "ur", "estratosec", "cct1b",
             "mexwf1_19", "wt", "upm", "estratopri", "cluster", "q1", "q2",
             "ed", "q10new"],
    "2021": ["clien1na", "clien1n", "vb2", "vb3n", "prot3", "countfair3",
             "mexwf1_19", "wt", "upm", "estratopri"],
    "2023": ["clien1na", "clien1n", "countfair1", "countfair3", "vb2", "vb3n",
             "vb20", "mexwf1_19", "ur", "estratosec", "wt", "upm",
             "estratopri", "strata"],
    "2006": ["PROT1", "PROT2", "VIC1", "UR", "TAMANO", "ESTRATOPRI", "UPM"],
}


def censo(olas=("2019", "2021", "2023", "2006")):
    """Censo A.4: item, codigos, denominador, ponderador, diseno, unidad.
    Reporta MARGINALES; no cruza ninguna variable contra el desenlace."""
    salida = []
    for ola in olas:
        pid, _rel = PAYLOADS[ola]
        df, meta, path, sha = carga(ola)
        sha_man = sha_manifiesto(pid)
        print(f"\n{'=' * 78}\nLAPOP MEXICO {ola} · id {pid}")
        print(f"  archivo   : {path}")
        print(f"  sha256    : {sha}")
        print(f"  manifiesto: {sha_man}  -> {'COINCIDE' if sha == sha_man else 'DIFIERE'}")
        print(f"  filas={len(df)}  columnas={len(df.columns)}")
        for var in CENSO_ITEMS[ola]:
            if var not in df.columns:
                print(f"    {var:12s} NO-ENCONTRADO en esta ola")
                salida.append({"ola": ola, "var": var, "estado": "NO-ENCONTRADO"})
                continue
            s = df[var]
            cods = [_cod(v) for v in s]
            validos = sum(1 for c in cods if c is not None)
            marg = {}
            for c in cods:
                if c is not None:
                    marg[c] = marg.get(c, 0) + 1
            etq = meta.column_names_to_labels.get(var, "")
            vlab = meta.variable_value_labels.get(var, {}) or {}
            print(f"    {var:12s} n_val={validos:5d} ({validos / len(df):5.1%})  "
                  f"distintos={len(marg):3d}  {str(etq)[:58]}")
            salida.append({"ola": ola, "var": var, "estado": "EXISTE",
                           "etiqueta": str(etq), "n_validos": validos,
                           "n_filas": len(df), "marginal": marg,
                           "codigos": {str(k): str(v) for k, v in vlab.items()}})
    return salida


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--censo", action="store_true")
    ap.add_argument("--mide", action="store_true")
    ap.add_argument("--json")
    a = ap.parse_args()
    if a.censo:
        filas = censo()
        if a.json:
            json.dump(filas, open(a.json, "w", encoding="utf-8"),
                      ensure_ascii=False, indent=1)
            print(f"\nescrito {a.json}")
        return
    if a.mide:
        from medidor_clientelismo_lapop_med import mide   # COMMIT-2
        mide(a.json)
        return
    ap.print_help()


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    main()
