"""ENIF 2024: exclusión por oferta entre no usuarios de cuenta, al lado del
marginal de ahorro formal (familias 2027 ENIF, firma E4 asignada por mesa).

El primer resultado que produzca este procedimiento es el que se reporta.
Spec humana: forense/analisis/familias-2027/astra6-enif/
DIN-OFERTA-EXCLUSION-ENIF2024-spec-v1_0.md. Lector, punto y bootstrap se
importan por bytes del medidor sellado del piso (CALC-ENIF-0001); aquí sólo
se fijan universo, pase, clases y la guardia de ola.
"""
from __future__ import annotations

import hashlib
import types
import zipfile
from pathlib import Path

ZIP_ID = "enif_2024_enif_2024_bd_csv"
ZIP_SHA = "00e4b0b42775276b2da236a5bba8c64dc5a92c289908a4727dec93dc7684f039"
BASE = "data/corrida0/CALC-ENIF-0001/medidor.py"
BASE_SHA = "6ac67a014b0ea46ecf5966595a8ce0c0a9bf818ea8f809163c78fd3870208e02"
OLA = "2024"
RAIZ = Path(__file__).resolve().parents[3] if "__file__" in globals() else Path(".")
MIEMBRO = "TMODULO.csv"
P = "RESULT-DIN-OFERTA-EXCLUSION-ENIF2024-CUENTA-UB-"

TENENCIA = [f"P5_4_{i}" for i in range(1, 10)]
PASADO, NUNCA, EX = "P5_19", "P5_20", "P5_21"
COLS = ["FAC_PER", "EST_DIS", "UPM_DIS", "EDAD_V", PASADO, NUNCA, EX] + TENENCIA

# (oferta, preferencia, otro->submotivo): texto verbatim en la spec §2.
CLASES_NUNCA = ({1, 2, 4}, {5, 6}, {3: "DESCONFIANZA-O-SERVICIO",
                7: "INGRESO-INSUFICIENTE", 8: "DESCONOCIMIENTO",
                9: "IMPUESTOS", 10: "OTRA"})
CLASES_EX = ({5, 6}, {1, 2, 3}, {4: "MALA-EXPERIENCIA", 7: "FRAUDE",
             8: "IMPUESTOS", 9: "OTRA"})
SUBMOTIVOS = sorted(set(CLASES_NUNCA[2].values()) | set(CLASES_EX[2].values()))
METRICAS = (["OFERTA", "PREFERENCIA", "OTRO-NS", "COBERTURA",
             "PASE-ESTRUCTURAL", "NO-RESPUESTA"]
            + ["SUB-" + s for s in SUBMOTIVOS] + ["SIN-CUENTA-UB"])
CONTEOS = ["N-FILAS", "N-UB", "N-PESO-INVALIDO", "N-SIN-DISENO",
           "N-USO-DESCONOCIDO", "N-EDAD-FUERA", "NO-USUARIOS-N",
           "NUNCA-N", "EX-USUARIOS-N", "BATERIA-OBS-N", "ESTRATOS-UPM-UNICA"]
TEXTOS = ["ESTADO", "METODO-IC", "ENCODING", "COLUMNAS-AUSENTES"]


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _guardia(inputs, contrato):
    """Una sola variable de agrupación: el id de payload. Antes de leer."""
    ids = {k for k, v in inputs.items()
           if isinstance(v, dict) and v.get("origen", "manifiesto") == "manifiesto"}
    if ids != {ZIP_ID}:
        raise ValueError(f"GUARDIA: inputs de manifiesto {sorted(ids)} != [{ZIP_ID}]")
    if str(contrato.get("parametros", {}).get("ola")) != OLA:
        raise ValueError("GUARDIA: ola distinta de 2024")
    if _sha(inputs[ZIP_ID]["ruta_absoluta"]) != ZIP_SHA:
        raise ValueError("GUARDIA: sha256 del payload no es el fijado")
    if _sha(RAIZ / BASE) != BASE_SHA:
        raise ValueError("GUARDIA: sha256 del medidor base no es el fijado")


def _base():
    m = types.ModuleType("enif0001")
    exec(compile((RAIZ / BASE).read_bytes(), BASE, "exec"), m.__dict__)
    return m


def _entero(s):
    t = (s or "").strip()
    return int(t) if t.isdigit() else None


def _vacio(estado, conteos, textos):
    out = {P + m + s: None for m in METRICAS for s in ("-P", "-IC-LO", "-IC-HI")}
    out.update({P + k: int(conteos.get(k, 0)) for k in CONTEOS})
    out.update({P + k: str(textos.get(k, "")) for k in TEXTOS})
    out[P + "ESTADO"] = estado
    return out


def medir(inputs, contrato):
    _guardia(inputs, contrato)
    b = _base()
    replicas = int(contrato["parametros"]["bootstrap_replicas"])
    seed = int(contrato["seed"]["valor"])
    with zipfile.ZipFile(inputs[ZIP_ID]["ruta_absoluta"]) as zf:
        filas, n, ausentes, enc = b._abre(zf, MIEMBRO, COLS)
    textos = {"ENCODING": enc, "COLUMNAS-AUSENTES": ",".join(ausentes),
              "METODO-IC": ""}
    if ausentes:
        return _vacio("NO-ESTIMABLE-COLUMNA-AUSENTE:" + ",".join(ausentes),
                      {"N-FILAS": n}, textos)
    ix = {c: i for i, c in enumerate(COLS)}
    c = {k: 0 for k in CONTEOS}
    c["N-FILAS"] = n
    base_w, base_e, base_u, base_nou = [], [], [], []
    coh = []  # (w, est, upm, clase, submotivo, observado, pase)
    for r in filas:
        w = b._peso(r[ix["FAC_PER"]])
        if w is None:
            c["N-PESO-INVALIDO"] += 1
            continue
        c["N-UB"] += 1
        edad = _entero(b._cod(r[ix["EDAD_V"]]))
        if edad is None or not 18 <= edad <= 98:
            c["N-EDAD-FUERA"] += 1
        e, u = b._llave(r[ix["EST_DIS"]]), b._llave(r[ix["UPM_DIS"]])
        if e is None or u is None:
            c["N-SIN-DISENO"] += 1
            continue
        t = [b._cod(r[ix[v]]) for v in TENENCIA]
        if all(x == "2" for x in t):
            no_user = True
        elif any(x == "1" for x in t):
            no_user = False
        else:
            c["N-USO-DESCONOCIDO"] += 1
            continue
        base_w.append(w); base_e.append(e); base_u.append(u); base_nou.append(no_user)
        if not no_user:
            continue
        pasado = b._cod(r[ix[PASADO]])
        if pasado == "2":
            pase, clases, cod = "NUNCA", CLASES_NUNCA, _entero(b._cod(r[ix[NUNCA]]))
            c["NUNCA-N"] += 1
        elif pasado == "1":
            pase, clases, cod = "EX", CLASES_EX, _entero(b._cod(r[ix[EX]]))
            c["EX-USUARIOS-N"] += 1
        else:
            pase, clases, cod = "ESTRUCTURAL", None, None
        clase, sub = "OTRO-NS", None
        obs = False
        if clases is not None and cod is not None:
            if cod in clases[0]:
                clase, obs = "OFERTA", True
            elif cod in clases[1]:
                clase, obs = "PREFERENCIA", True
            elif cod in clases[2]:
                sub, obs = clases[2][cod], True
        coh.append((w, e, u, clase, sub, obs, pase))
    c["NO-USUARIOS-N"] = len(coh)
    c["BATERIA-OBS-N"] = sum(1 for x in coh if x[5])
    if not coh:
        return _vacio("NO-ESTIMABLE-COHORTE-VACIA", c, textos)
    w = [x[0] for x in coh]; est = [x[1] for x in coh]; upm = [x[2] for x in coh]
    ys = {"OFERTA": [x[3] == "OFERTA" for x in coh],
          "PREFERENCIA": [x[3] == "PREFERENCIA" for x in coh],
          "OTRO-NS": [x[3] == "OTRO-NS" for x in coh],
          "COBERTURA": [x[5] for x in coh],
          "PASE-ESTRUCTURAL": [x[6] == "ESTRUCTURAL" for x in coh],
          "NO-RESPUESTA": [x[6] != "ESTRUCTURAL" and not x[5] for x in coh]}
    for s in SUBMOTIVOS:
        ys["SUB-" + s] = [x[4] == s for x in coh]
    out = {}
    metodo = unica = None
    for m, y in ys.items():
        p, _ = b._p(w, y)
        lo, hi, _, _, unica, metodo, _ = b._ic(w, y, est, upm, replicas, seed)
        out[P + m + "-P"], out[P + m + "-IC-LO"], out[P + m + "-IC-HI"] = p, lo, hi
    p, _ = b._p(base_w, base_nou)
    lo, hi, *_ = b._ic(base_w, base_nou, base_e, base_u, replicas, seed)
    out[P + "SIN-CUENTA-UB-P"], out[P + "SIN-CUENTA-UB-IC-LO"], out[P + "SIN-CUENTA-UB-IC-HI"] = p, lo, hi
    c["ESTRATOS-UPM-UNICA"] = int(unica or 0)
    textos["METODO-IC"] = str(metodo)
    out.update({P + k: int(v) for k, v in c.items()})
    out.update({P + k: str(v) for k, v in textos.items()})
    out[P + "ESTADO"] = "CONSTRUIBLE"
    return out
