"""Lector material conjunto: no resuelve rutas ni abre miembros ajenos."""
import csv
import io
import json
import math
import hashlib
import zipfile
from collections import Counter

import numpy as np

FORMAL = tuple(f"P5_6_{j}" for j in range(1, 10))
INFORMAL = tuple(f"P5_1_{j}" for j in range(1, 7))
COLS = ("LLAVEMOD", "FAC_PER", "EST_DIS", "UPM_DIS", "EDAD_V") + FORMAL + INFORMAL
SEED = 20260926
REPLICAS = 2000
PISOS_HASH = {'CALC-ENIF-0001': '2a90c52e532e0c8f17ff87f31c70567f7810f337274f895f3a4623d08f4c57e6', 'CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1': '16a03f136bf70db92ad0031230e1e5191f317f32c0e9181c18a9be61109364bd'}


def clasifica(lo, hi, banda=0.02):
    if not (math.isfinite(lo) and math.isfinite(hi) and lo <= hi):
        return "NO-ESTIMABLE"
    if -banda <= lo and hi <= banda:
        return "COMPATIBLE-CON-TOLERANCIA"
    if hi < -banda or lo > banda:
        return "DESVÍO-MATERIAL"
    return "INDETERMINADO"


def guardia(meta, reservada=False, autorizada=False, agrupacion=None):
    if agrupacion is not None:
        raise ValueError("una sola agrupación nacional; cruces prohibidos")
    if reservada and not autorizada:
        raise PermissionError("reserva sin autorización de ola")
    esperado = {"unidad": "persona18+", "peso": "FAC_PER", "formal": list(FORMAL),
                "informal": list(INFORMAL), "periodo": "ultimos12meses"}
    if any(meta.get(k) != v for k, v in esperado.items()):
        raise ValueError("NO-COMPARABLE: descriptor o estimando cambió")


def lee_zip(origen):
    with zipfile.ZipFile(origen) as z:
        miembros = [n for n in z.namelist() if n.rsplit("/", 1)[-1].upper() == "TMODULO.CSV"]
        if len(miembros) != 1:
            raise ValueError("miembro TMODULO único requerido")
        raw = z.read(miembros[0])
    try:
        txt = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        txt = raw.decode("latin-1")
    reader = csv.DictReader(io.StringIO(txt))
    names = {n.strip().upper(): n for n in reader.fieldnames or []}
    if set(COLS) - set(names):
        raise ValueError("NO-ESTIMABLE: columnas ausentes")
    # Proyección explícita: el lector nunca entrega una variable ajena.
    return [{c: r[names[c]].strip() for c in COLS} for r in reader]


def estima(rows, replicas=REPLICAS):
    clusters = {}
    total = np.zeros(5)
    sw2 = 0.
    faltas = Counter()
    codigos = Counter()
    masa_codigos = Counter()
    llaves = set()
    for r in rows:
        if not r["LLAVEMOD"] or r["LLAVEMOD"] in llaves:
            raise ValueError("NO-ESTIMABLE: llave ausente o duplicada")
        llaves.add(r["LLAVEMOD"])
        try:
            edad = int(r["EDAD_V"])
            w = float(r["FAC_PER"].replace(",", ""))
        except (ValueError, TypeError):
            raise ValueError("NO-ESTIMABLE: edad/peso ilegible")
        if edad not in set(range(18, 96)) | {97, 98}:
            raise ValueError("NO-COMPARABLE: universo no 18+")
        if not math.isfinite(w) or w <= 0:
            faltas["peso"] += 1
            continue
        f = any(r[c] == "1" for c in FORMAL)
        i = any(r[c] == "1" for c in INFORMAL)
        for c in FORMAL + INFORMAL:
            permitido = {"1", "2", "b", ""} if c in FORMAL else {"1", "2"}
            if r[c] not in permitido:
                codigos[c + ":" + r[c]] += 1
                masa_codigos[c + ":" + r[c]] += w
        v = np.array([w, w*f, w*i, w*(f and i), w*(f or i)])
        total += v
        sw2 += w*w
        e, u = r["EST_DIS"], r["UPM_DIS"]
        if not e or not u:
            faltas["diseno"] += 1
        else:
            clusters.setdefault(e, {}).setdefault(u, np.zeros(5))[:] += v
    if total[0] <= 0:
        raise ValueError("NO-ESTIMABLE: denominador vacío")
    rng = np.random.default_rng(SEED)
    acumulado = np.zeros((replicas, 5))
    unicas = 0
    for upms in clusters.values():
        a = np.asarray(list(upms.values()))
        n = len(a)
        unicas += n == 1
        multiplicidad = rng.multinomial(n, np.full(n, 1/n), size=replicas)
        acumulado += multiplicidad @ a
    valido = acumulado[:, 0] > 0
    reps = acumulado[valido, 1:] / acumulado[valido, :1]
    n = len(rows) - faltas["peso"]
    soporte = (n >= 10000 and len(clusters) >= 150 and
               sum(map(len, clusters.values())) >= 1000 and not faltas and not unicas
               and len(reps) >= 1000 and len(reps)/replicas >= .95)
    return {"p": (total[1:]/total[0]).tolist(), "replicas": reps.tolist(),
            "n": n, "estratos": len(clusters), "upm": sum(map(len, clusters.values())),
            "unicas": unicas, "faltas": dict(faltas), "codigos": dict(codigos),
            "masa_codigos": dict(masa_codigos),
            "masa": total[0], "soporte": bool(soporte),
            "n_efectivo": float(total[0]**2/sw2)}  # Kish de pesos, no precisión de diseño.


def escenarios(puntos, replicas):
    """Potencia de clasificación local: ruido conjunto histórico, piso fijo."""
    if not replicas:
        return {"escenarios": [], "mde80": [None, None], "correlacion_muestral": None,
                "supuesto": "NO-ESTIMABLE: sin réplicas de diseño; ninguna potencia fabricada"}
    r = np.asarray(replicas)[:, [0, 2]]
    p = np.asarray(puntos)[[0, 2]]
    ruido = r-p
    salidas = []
    for escala in (.75, 1., 1.5):
        for temporal in (0., .005, .01):
            # Deriva compartida crea dependencia temporal explícita; no es serie estimada.
            rng = np.random.default_rng(SEED+1)
            deriva = rng.normal(0, temporal, size=(len(ruido), 1))
            for delta in (0., .01, .02, .03, .04, .05):
                errores = delta + escala*ruido + deriva
                limites = np.quantile(escala*ruido, [.025, .975], axis=0)
                etiquetas = [[clasifica(e[j]+limites[0,j], e[j]+limites[1,j])
                              for j in range(2)] for e in errores]
                filas = []
                for j in range(2):
                    c = Counter(x[j] for x in etiquetas)
                    filas.append({k: c[k]/len(etiquetas) for k in
                                  ("COMPATIBLE-CON-TOLERANCIA", "INDETERMINADO", "DESVÍO-MATERIAL")})
                salidas.append({"escala_se": escala, "sd_deriva": temporal,
                                "delta": delta, "familias": filas,
                                "ambas_informativas": sum(all(k != "INDETERMINADO" for k in x)
                                                           for x in etiquetas)/len(etiquetas)})
    mde = []
    limites = np.quantile(ruido, [.025, .975], axis=0)
    for j in range(2):
        candidatos = [float(d) for d in np.arange(0, .101, .0005)
                      if np.mean(d+ruido[:, j]+limites[0, j] > .02) >= .8]
        mde.append(candidatos[0] if candidatos else None)
    return {"escenarios": salidas, "mde80": mde,
            "correlacion_muestral": float(np.corrcoef(ruido.T)[0, 1]) if np.all(np.std(ruido, axis=0)>0) else None,
            "supuesto": "ruido empírico conjunto ENIF2024; deriva compartida hipotética; no cobertura nominal acreditada"}


def medir(inputs, contrato):
    esperado = {"enif_2024_enif_2024_bd_csv"}
    if set(inputs) != esperado:
        raise PermissionError("input fuera de lista blanca histórica")
    inp = inputs[next(iter(esperado))]
    resultado = estima(lee_zip(inp["ruta_absoluta"]))
    if resultado["codigos"]:
        raise ValueError("NO-COMPARABLE: código histórico fuera descriptor")
    out = {"RESULT-FAMILIA-ENIF-ORO-"+k.upper(): resultado[k] for k in
           ("n", "estratos", "upm", "unicas", "masa")}
    for j, nombre in enumerate(("FORMAL", "INFORMAL", "AMBAS", "UNION")):
        out["RESULT-FAMILIA-ENIF-ORO-"+nombre+"-P"] = resultado["p"][j]
    out["RESULT-FAMILIA-ENIF-ORO-SOPORTE"] = "SI" if resultado["soporte"] else "NO"
    out["RESULT-FAMILIA-ENIF-ORO-REPLICAS"] = json.dumps(resultado["replicas"], separators=(",", ":"))
    out["RESULT-FAMILIA-ENIF-ORO-AUDITORIA"] = json.dumps({k: resultado[k] for k in
                                                        ("faltas", "codigos", "masa_codigos", "n_efectivo")}, sort_keys=True)
    out["RESULT-FAMILIA-ENIF-ORO-POTENCIA"] = json.dumps(escenarios(resultado["p"], resultado["replicas"]), sort_keys=True)
    return out


def evaluar_futuro(inputs, contrato):
    """Entrada única para ambas familias; la metadata se revisa antes del ZIP."""
    if set(inputs) != {"enif_2027", *PISOS_HASH}:
        raise PermissionError("identidad de ola futura incorrecta")
    if contrato.get("estado") != "RESERVADA" or not contrato.get("autoridad_ola"):
        raise PermissionError("estado o autorización de ola ausente")
    guardia(contrato.get("metadatos", {}), True, True, contrato.get("agrupacion"))
    if contrato.get("comparabilidad_cotejada") is not True:
        raise ValueError("NO-COMPARABLE: cotejo de cuestionario pendiente")
    pisos = {}
    for parent, sha in PISOS_HASH.items():
        raw = inputs[parent]["bytes"]
        if hashlib.sha256(raw).hexdigest() != sha:
            raise PermissionError("piso congelado discordante")
        obj = json.loads(raw)
        pisos[parent] = obj.get("resultados", obj)
    fijos = {"AHORRO-FORMAL": pisos["CALC-ENIF-0001"]["RESULT-ENIF-AHO-B-P-FORMAL-P"],
             "HORIZONTE-AHORRO": pisos["CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1"]["RESULT-HVD-A-AMBAS-VIAS"]}
    r = estima(lee_zip(inputs["enif_2027"]["ruta_absoluta"]))
    out = {}
    for j, familia in ((0, "AHORRO-FORMAL"), (2, "HORIZONTE-AHORRO")):
        p0 = fijos[familia]
        d = np.asarray(r["replicas"])[:, j]-p0 if r["replicas"] else np.array([])
        lo, hi = np.quantile(d, [.025, .975]) if len(d) else (None, None)
        out[familia] = {"p": r["p"][j], "d": r["p"][j]-p0,
                        "abs_d": abs(r["p"][j]-p0), "lo": float(lo) if lo is not None else None,
                        "hi": float(hi) if hi is not None else None,
                        "fraccion_banda": float(np.mean(abs(d) <= .02)) if len(d) else None, "d_k": d.tolist(),
                        "estado": clasifica(lo, hi) if r["soporte"] else "NO-ESTIMABLE"}
    return {"familias": out, "soporte": {k: r[k] for k in
                                           ("n", "estratos", "upm", "unicas", "faltas", "codigos", "masa_codigos", "n_efectivo")}}


def medir_futuro(inputs, contrato):
    """Salidas planas D-22; ids definidos antes de cualquier R futura."""
    r = evaluar_futuro(inputs, contrato)
    out = {}
    for fam, valores in r["familias"].items():
        prefijo = "RESULT-FAMILIA-ENIF-FUTURO-"+fam+"-"
        for campo in ("p", "d", "abs_d", "lo", "hi", "fraccion_banda", "estado"):
            out[prefijo+campo.upper().replace("_", "-")] = valores[campo]
        out[prefijo+"D-K"] = json.dumps(valores["d_k"], allow_nan=False, separators=(",", ":"))
    out["RESULT-FAMILIA-ENIF-FUTURO-SOPORTE"] = json.dumps(r["soporte"], allow_nan=False, sort_keys=True)
    return out
