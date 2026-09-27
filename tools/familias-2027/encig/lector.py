"""ENCIG: lector de dos outcomes, marco completo y bootstrap conjunto.

COMMIT-1 previo al microdato. No importa productores históricos ni libro vivo.
No segmenta: la única agrupación es la llave de diseño (EST_DIS, UPM_DIS).
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
from pathlib import Path
import zipfile

import numpy as np

FAMILIAS = ("PAGO-DIGITAL", "SOLICITUD-MORDIDA")
PERSONA = "encig2025_01_sec1_A_3_4_5_8_9_10.csv"
EVENTO = "encig2025_04_sec_7.csv"
COLS = {
    "persona": ("ID_PER", "P8_3_1", "FAC_P18", "EST_DIS", "UPM_DIS"),
    "evento": ("ID_PER", "ID_TRA", "NT_TIPO", "N_TRA", "P7_3", "FAC_TRA", "EST_DIS", "UPM_DIS"),
}


def codigo(v):
    try:
        return int(v.strip())
    except (ValueError, AttributeError):
        return None


def peso(v):
    try:
        w = float(v.strip().replace(",", ""))
        return w if np.isfinite(w) and w > 0 else None
    except (ValueError, AttributeError):
        return None


def lee_zip(path, miembros):
    """Solo abre dos miembros explícitos; nunca extrae ni descubre columnas."""
    if set(miembros) != set(COLS) or len(set(miembros.values())) != 2:
        raise ValueError("GUARDIA-MIEMBROS")
    blancos = ({"persona": PERSONA, "evento": EVENTO},
               {"persona": PERSONA.replace("2025", "2027"), "evento": EVENTO.replace("2025", "2027")})
    if miembros not in blancos:
        raise ValueError("GUARDIA-LISTA-BLANCA")
    tablas = {}
    with zipfile.ZipFile(path) as z:
        for rol, base in miembros.items():
            matches = [n for n in z.namelist() if n.split("/")[-1] == base and not n.startswith("__MACOSX/")]
            if len(matches) != 1 or ".." in Path(matches[0]).parts:
                raise ValueError("GUARDIA-MIEMBRO-AUSENTE-O-AMBIGUO:" + rol)
            with z.open(matches[0]) as b:
                rows = csv.DictReader(io.TextIOWrapper(b, encoding="utf-8-sig"))
                if not set(COLS[rol]).issubset(rows.fieldnames or []):
                    raise ValueError("NO-COMPARABLE-COLUMNAS:" + rol)
                # Proyección explícita antes de construir el marco analítico.
                tablas[rol] = [{k: row[k] for k in COLS[rol]} for row in rows]
    return tablas


def etiqueta(lo, hi, banda):
    if lo is None or hi is None or not np.isfinite([lo, hi]).all() or lo > hi:
        return "NO-ESTIMABLE"
    if -banda <= lo and hi <= banda:
        return "COMPATIBLE-CON-TOLERANCIA"
    if hi < -banda or lo > banda:
        return "DESVÍO-MATERIAL"
    return "INDETERMINADO"


def estima(tablas, reglas):
    """Estima dominios sobre el marco persona completo, sin recortar UPM."""
    if set(tablas) != set(COLS):
        raise ValueError("GUARDIA-TABLAS")
    marco, por_persona = {}, {}
    for row in tablas["persona"]:
        key = (row["EST_DIS"].strip(), row["UPM_DIS"].strip())
        pid = row["ID_PER"].strip()
        if not pid or pid in por_persona:
            raise ValueError("NO-COMPARABLE-LLAVE-PERSONA")
        if not all(key):
            raise ValueError("NO-ESTIMABLE-MARCO-INCOMPLETO")
        por_persona[pid] = key
        marco.setdefault(key, np.zeros((2, 2)))  # familia x numerador/denominador
    diag = [{"n": 0, "residuo_n": 0, "residuo_peso": 0.0, "peso_potencial": 0.0,
             "sin_peso": 0, "sin_diseno": 0, "clusters": set(), "w2": 0.0} for _ in FAMILIAS]
    llaves = set()
    for rol, fam, weight, outcome, validos, unos in (
        ("evento", 0, "FAC_TRA", "P7_3", {1, 2, 4, 5, 6}, {4, 5}),
        ("persona", 1, "FAC_P18", "P8_3_1", {1, 2}, {1}),
    ):
        d = diag[fam]
        for row in tablas[rol]:
            if rol == "evento":
                event_key = (row["ID_TRA"].strip(), row["NT_TIPO"].strip())
                if not all(event_key) or event_key in llaves:
                    raise ValueError("NO-COMPARABLE-LLAVE-EVENTO")
                llaves.add(event_key)
                if codigo(row["N_TRA"]) != 1:
                    continue
            key = (row["EST_DIS"].strip(), row["UPM_DIS"].strip())
            if key != por_persona.get(row["ID_PER"].strip()):
                raise ValueError("NO-COMPARABLE-DISENO-PERSONA-EVENTO")
            w, y = peso(row[weight]), codigo(row[outcome])
            if w is None:
                d["sin_peso"] += 1
                continue
            d["peso_potencial"] += w
            if y not in validos:
                d["residuo_n"] += 1
                d["residuo_peso"] += w
                continue
            d["n"] += 1
            d["w2"] += w * w
            d["clusters"].add(key)
            marco[key][fam] += (w * (y in unos), w)
    keys = sorted(marco)
    totals = np.array([marco[k] for k in keys], dtype=float).reshape((-1, 2, 2))
    strata = {}
    for i, (h, _) in enumerate(keys):
        strata.setdefault(h, []).append(i)
    single = sum(len(v) == 1 for v in strata.values())
    rng = np.random.Generator(np.random.PCG64(reglas["seed"]))
    replicas = np.zeros((reglas["replicas"], 2, 2))
    for indices in strata.values():
        n = len(indices)
        draws = rng.integers(n, size=(reglas["replicas"], n))
        # Misma multiplicidad de UPM para personas y eventos.
        replicas += totals[indices][draws].sum(axis=1)
    salida = {"joint_design": True, "marco": {"estratos": len(strata), "upm": len(keys),
              "estratos_upm_unica": single}, "metodo": "BOOTSTRAP-UPM-MARCO-COMPLETO", "familias": {}}
    for j, name in enumerate(FAMILIAS):
        d = diag[j]
        domain = d.pop("clusters")
        total = totals[:, j, :].sum(axis=0)
        p = float(total[0] / total[1]) if total[1] > 0 else None
        good = replicas[:, j, 1] > 0
        vector = [float(a / b) if b > 0 else None for a, b in replicas[:, j, :]]
        vals = np.array([x for x in vector if x is not None])
        d.update(estratos=len({h for h, _ in domain}), upm=len(domain),
                 estratos_upm_unica_dominio=sum(sum(a == h for a, _ in domain) == 1 for h in {a for a, _ in domain}),
                 residuo_fraccion=d["residuo_peso"] / d["peso_potencial"] if d["peso_potencial"] else None,
                 n_efectivo_kish=float(total[1] ** 2 / d["w2"]) if d["w2"] else None,
                 replicas_validas=int(good.sum()), masa_denominador=float(total[1]))
        gate = (p is not None and d["n"] >= reglas["min_n"] and d["estratos"] >= reglas["min_estratos"]
                and d["upm"] >= reglas["min_upm"] and d["sin_peso"] == 0
                and d["residuo_fraccion"] <= reglas["residuo_max"][name] and single == 0
                and len(vals) >= reglas["min_replicas"] and good.mean() >= reglas["fraccion_replicas"])
        ic = [float(x) for x in np.quantile(vals, [0.025, 0.975])] if len(vals) and not single else [None, None]
        salida["familias"][name] = {"p": p, "ic": ic, "replicas": vector, "soporte": d,
                                      "estado": "ESTIMABLE" if gate else "NO-ESTIMABLE"}
    return salida


def abrir_futuro(path, metadata, reglas, pisos):
    """No lee el ZIP hasta verificar identidad y autorización de la ola única.

    El registro de autorización debe recibirse del circuito de mesa; esta función
    no lo crea, no descarga, no cambia reservas y no lo sustituye por un flag.
    """
    required = {"instrumento": "ENCIG", "ola": "2027", "estado_reserva": "RESERVADA",
                "unidad_persona": "PERSONA", "unidad_evento": "PAGO-LUZ",
                "peso_persona": "FAC_P18", "peso_evento": "FAC_TRA",
                "solicitud_si": [1], "solicitud_no": [2], "digital": [4, 5],
                "no_digital": [1, 2, 6], "universo": "URBANO-100MIL-18PLUS"}
    if any(metadata.get(k) != v for k, v in required.items()):
        return {"estado": "NO-COMPARABLE"}
    if metadata.get("miembros") != {"persona": PERSONA.replace("2025", "2027"),
                                    "evento": EVENTO.replace("2025", "2027")}:
        return {"estado": "NO-COMPARABLE"}
    auth = metadata.get("autorizacion", {})
    if (auth.get("acto") != "ASTRA6-C2-ENCIG-1" or auth.get("ola") != "encig_2027"
            or auth.get("familias") != list(FAMILIAS) or auth.get("apertura") != "UNICA"
            or not auth.get("asiento_firmado") or not metadata.get("cuestionario_sha256")
            or not metadata.get("descriptor_sha256")):
        raise PermissionError("APERTURA-NO-AUTORIZADA")
    # La identidad de código autorizada es exacta, incluyendo esta guardia.
    if auth.get("codigo_sha256") != hashlib.sha256(Path(__file__).read_bytes()).hexdigest():
        raise PermissionError("CODIGO-NO-AUTORIZADO")
    # El campo debe apuntar a un asiento real revisado por mesa, con bytes
    # identificados, no solo a una afirmación dentro del JSON del operador.
    asiento = Path(auth["asiento_firmado"])
    if (not asiento.is_file() or "forense" not in asiento.parts or "encargos" not in asiento.parts
            or auth.get("asiento_sha256") != hashlib.sha256(asiento.read_bytes()).hexdigest()):
        raise PermissionError("ASIENTO-NO-ACREDITADO")
    permiso = "AUTORIZO-APERTURA: encig_2027; ASTRA6-C2-ENCIG-1; UNICA; PAGO-DIGITAL,SOLICITUD-MORDIDA"
    if permiso not in asiento.read_text(encoding="utf-8"):
        raise PermissionError("ASIENTO-SIN-OBJETO-DE-APERTURA")
    if metadata.get("payload_sha256") != hashlib.sha256(Path(path).read_bytes()).hexdigest():
        raise PermissionError("IDENTIDAD-OLA")
    try:
        gold = estima(lee_zip(path, metadata.get("miembros", {})), reglas)
    except ValueError as exc:
        estado = "NO-ESTIMABLE" if str(exc).startswith("NO-ESTIMABLE") else "NO-COMPARABLE"
        return {"estado": estado, "razon": str(exc)}
    for name, f in gold["familias"].items():
        if f["estado"] != "ESTIMABLE":
            f["dictamen"] = "NO-ESTIMABLE"
            f["d"] = None
            f["ic_d"] = [None, None]
            f["fraccion_en_banda"] = None
        else:
            p0 = pisos["familias"][name]["p0"]
            ds = np.array([r - p0 for r in f["replicas"] if r is not None])
            f["d"] = f["p"] - p0
            f["ic_d"] = [float(x) for x in np.quantile(ds, [0.025, 0.975])]
            f["fraccion_en_banda"] = float(np.mean(np.abs(ds) <= reglas["banda"]))
            f["dictamen"] = etiqueta(*f["ic_d"], reglas["banda"])
    return gold


def medir(inputs, contrato):
    """Auxiliar histórico autorizado. Nunca abre una ola por nombre descubierto."""
    par = contrato["parametros"]
    if par["modo"] != "HISTORICO-ABIERTO" or set(inputs) != {"encig25_base_datos_csv"}:
        raise PermissionError("GUARDIA-INPUTS")
    source = inputs["encig25_base_datos_csv"]
    if source["sha256"] != par["payload_sha256"]:
        raise PermissionError("IDENTIDAD-HISTORICA")
    try:
        tablas = lee_zip(source["ruta_absoluta"], {"persona": PERSONA, "evento": EVENTO})
        gold = estima(tablas, par)
    except ValueError as exc:
        estado = "NO-ESTIMABLE" if str(exc).startswith("NO-ESTIMABLE") else "NO-COMPARABLE"
        gold = {"joint_design": False, "razon": str(exc), "familias": {
            name: {"p": None, "replicas": [], "ic": [None, None], "estado": estado,
                   "soporte": {k: None for k in ("n", "estratos", "upm", "residuo_n", "residuo_fraccion", "n_efectivo_kish")}}
            for name in FAMILIAS}}
    # Tabla propia sellada vía REF (conducto nativo); solo agregados y réplicas.
    folder = Path(__file__).resolve().parent / "tablas"
    folder.mkdir(exist_ok=True)
    artifact = folder / "replicas.json"
    content = (json.dumps(gold, sort_keys=True, allow_nan=False, separators=(",", ":")) + "\n").encode()
    if artifact.exists():
        if artifact.read_bytes() != content:
            raise RuntimeError("ARTEFACTO-SELLADO-DISCREPA-NO-SE-REESCRIBE")
    else:
        artifact.write_bytes(content)
    sha = hashlib.sha256(artifact.read_bytes()).hexdigest()
    result = {"RESULT-ENCIG-AUX-REPLICAS": f"REF:data/corrida0/{par['calc_id']}/tablas/replicas.json#sha256:{sha}"}
    for name, f in gold["familias"].items():
        prefix = "RESULT-ENCIG-AUX-" + name
        result[prefix + "-P"] = f["p"]
        result[prefix + "-ESTADO"] = f["estado"]
        for k in ("n", "estratos", "upm", "residuo_n", "residuo_fraccion", "n_efectivo_kish"):
            result[prefix + "-" + k.upper().replace("_", "-")] = f["soporte"][k]
    return result


def resultados_futuros(payload):
    """Cara escalar del resultado; el payload conserva el vector por réplica."""
    values = {}
    for name in FAMILIAS:
        f = payload.get("familias", {}).get(name, {})
        prefix = "RESULT-FAMILIA-2027-ENCIG-" + name
        estado = f.get("dictamen", payload.get("estado", "NO-ESTIMABLE"))
        d = f.get("d")
        support = f.get("soporte", {})
        items = {"R": f.get("p"), "D": d, "ABS-D": abs(d) if d is not None else None,
                 "IC-D-LO": f.get("ic_d", [None, None])[0], "IC-D-HI": f.get("ic_d", [None, None])[1],
                 "FRACCION-EN-BANDA": f.get("fraccion_en_banda"), "DICTAMEN": estado,
                 "N": support.get("n"), "N-EFECTIVO-KISH": support.get("n_efectivo_kish"),
                 "RESIDUO-FRACCION": support.get("residuo_fraccion")}
        values.update({prefix + "-" + k: v for k, v in items.items()})
    return values
