from __future__ import annotations
"""El primer resultado que produzca este procedimiento es el que se reporta.

K8 «destino del crédito» fuera de ENIF (FP-404 (1), firmada): ENFIH 2019,
destino PRINCIPAL de cada crédito de nómina (8.31, TNomina) y de cada crédito
personal (8.47, TPersonal) vigentes. Unidad PR: una fila por crédito. No es
«el último crédito» ni cubre tarjetas, automotriz, vivienda, educativo ni
grupal, y el catálogo no trae «negocio»: la tabla de comparabilidad
(`K8-TRIANGULACION-TEXTO`) lo declara CAMBIO-DE-INSTRUMENTO y el medidor
lo CONTRASTA antes de leer un registro; ENSAFI 2023 es NO-ESTIMABLE por
texto y aquí no se mide nada de ENSAFI. Se emite rotulado, por familia y
agregado, sin serie con ENIF ni con ENSAFI (PARO d).

Marco: FACTOR de la tabla del crédito (> 0), diseño EDIS × UPM_DIS,
bootstrap de UPM con reemplazo dentro de estrato, 10 000 remuestras
PCG64(42), un solo plan de réplicas; `_estimate`, `_cells` y `_slug`
importados por bytes del medidor sellado de CALC-PISOS-ENIF2021-EJES-0003.
Spec: forense/prereg-caja/DIN-CREDITO-K8-ENFIH2019-spec-v1_0.md.
"""
import io
import types
import zipfile
from pathlib import Path
import pandas as pd

PREFIJO = "DIN-CREDITO-K8-ENFIH2019"
N_SOPORTE = 200
LLAVE = ["FOLIO", "VIV_SEL", "HOGAR", "N_REN"]
FAMILIAS = {"NOMINA": ("TNOMINA.csv", "P8_31"), "PERSONAL": ("TPERSONAL.csv", "P8_47")}
CATALOGO = "123456789"
# destino emitido -> códigos que cuentan 1 (los demás del catálogo cuentan 0; 9 «No sabe» y blanco indefinidos)
DESTINOS = [
    ("CONSUMO", "3"),                 # gastos de comida, personales o pago de servicios (lista de mesa)
    ("EMERGENCIA", "5"),              # atender una emergencia o imprevistos (lista de mesa)
    ("EMERGENCIA-MAS-SALUD", "56"),   # rotulada aparte: salud viaja fuera de la lista de mesa
    ("REFINANCIAR-DEUDA", "4"),       # pagar una deuda (diferente a negocio) (lista de mesa)
    ("LISTA-DE-MESA-ALGUNO", "345"),  # consumo ∪ emergencia ∪ refinanciar (negocio NO-ESTIMABLE)
    ("VIVIENDA", "1"),
    ("VEHICULO", "2"),
    ("SALUD", "6"),
    ("EDUCACION", "7"),
    ("OTRO", "8"),
]


def _bytes(ent):
    b = ent.get("bytes")
    return b if b is not None else Path(ent["ruta_absoluta"]).read_bytes()


def _modulo_0003(inputs):
    src = _bytes(inputs["MEDIDOR-EJES-0003"])
    mod = types.ModuleType("medidor_ejes_0003")
    exec(compile(src, "medidor_ejes_0003", "exec"), mod.__dict__)
    return mod


def _tsv(ent):
    lineas = _bytes(ent).decode("utf-8").splitlines()
    lineas = [l for l in lineas if l and not l.startswith("#")]
    cab = lineas[0].split("\t")
    return [dict(zip(cab, l.split("\t"))) for l in lineas[1:]]


def _comparabilidad(inputs):
    filas = {(f["fuente"], f["edicion"]): f for f in _tsv(inputs["K8-TRIANGULACION-TEXTO"]) if f["conducta"] == "K8"}
    if ("ENFIH", "2019") not in filas or ("ENSAFI", "2023") not in filas:
        raise RuntimeError(f"la tabla de triangulación no trae ENFIH 2019 y ENSAFI 2023: {sorted(filas)}")
    e = filas[("ENFIH", "2019")]
    if e["veredicto"] != "CAMBIO-DE-INSTRUMENTO":
        raise RuntimeError(f"ENFIH 2019 no es CAMBIO-DE-INSTRUMENTO en la tabla: {e['veredicto']} — este medidor no presenta serie")
    for v in ("P8_31", "P8_47"):
        if v not in e["reactivo"]:
            raise RuntimeError(f"el reactivo {v} no está escrito en la fila ENFIH·2019")
    if not e["unidad"].startswith("PR"):
        raise RuntimeError(f"unidad de ENFIH 2019 no es PR: {e['unidad']!r}")
    if "negocio" not in e["componentes_no_estimables"]:
        raise RuntimeError("la tabla debe declarar «negocio» NO-ESTIMABLE en ENFIH 2019")
    s = filas[("ENSAFI", "2023")]
    if s["veredicto"] != "NO-ESTIMABLE":
        raise RuntimeError(f"ENSAFI 2023 debería ser NO-ESTIMABLE por texto: {s['veredicto']}")
    return e, s


def _csv_zip(path, miembro, cols):
    with zipfile.ZipFile(path) as zf:
        names = [n for n in zf.namelist() if n.lower() == miembro.lower()]
        if len(names) != 1:
            raise RuntimeError(f"miembro CSV no único: {miembro}: {names}")
        raw = zf.read(names[0])
    for enc in ("utf-8-sig", "latin-1"):
        try:
            d = pd.read_csv(io.StringIO(raw.decode(enc)), dtype=str, keep_default_na=False, na_filter=False)
        except UnicodeDecodeError:
            continue
        d.columns = [str(x).strip().strip('"').upper() for x in d.columns]
        missing = sorted(set(cols) - set(d.columns))
        if missing:
            raise RuntimeError(f"variables ausentes en {miembro}: {missing}")
        return d[cols].copy()
    raise RuntimeError(f"codificación no reconocida: {miembro}")


def _dicot(code, unos, ceros):
    out = pd.Series(pd.NA, index=code.index, dtype="Float64")
    out.loc[code.isin(list(ceros))] = 0.0
    out.loc[code.isin(list(unos))] = 1.0
    return out


def medir(inputs, contrato):
    m = _modulo_0003(inputs)
    fila, _ensafi = _comparabilidad(inputs)
    z = inputs["enfih2019_bd_csv_zip"]["ruta_absoluta"]
    bloques = []
    diag = {}
    for fam, (miembro, var) in FAMILIAS.items():
        d = _csv_zip(z, miembro, LLAVE + ["CONSEC", var, "EDIS", "UPM_DIS", "FACTOR"])
        if d.duplicated(LLAVE + ["CONSEC"]).any():
            raise RuntimeError(f"{miembro}: llave persona × CONSEC duplicada")
        b = pd.DataFrame({"_w": pd.to_numeric(d["FACTOR"].str.strip(), errors="coerce"),
                          "_est": d["EDIS"].str.strip(), "_upm": d["UPM_DIS"].str.strip(),
                          "_fam": fam.lower(), "_persona": d[LLAVE].agg("\t".join, axis=1),
                          "_code": m._code(d[var])})
        bloques.append(b)
        diag[f"FILAS-{fam}"] = int(len(d))
    big = pd.concat(bloques, ignore_index=True)
    code = big["_code"]
    y = {}
    for nombre, unos in DESTINOS:
        ceros = "".join(sorted(set(CATALOGO) - set("9") - set(unos)))
        y[nombre] = _dicot(code, unos, ceros)
    todos = pd.Series("todos", index=big.index, dtype="object")
    axes = {"nacional": (todos, ("todos",)),
            "familia": (big["_fam"], ("nomina", "personal"))}
    cells = []
    for nombre, _u in DESTINOS:
        cells += m._cells(f"{PREFIJO}-{nombre}", y[nombre], axes)
    out = m._estimate(big, cells, int(contrato["parametros"]["bootstrap_replicas"]),
                      int(contrato["seed"]["valor"]))
    design = big["_w"].notna() & (big["_w"] > 0) & big["_est"].ne("") & big["_upm"].ne("")
    for cell in cells:
        rid = cell["base"]
        out[rid + "-SOPORTE"] = "OK" if out[rid + "-N"] >= N_SOPORTE else f"BAJO-N-MENOR-{N_SOPORTE}"
    for nombre, _u in DESTINOS:
        b = f"RESULT-{PREFIJO}-{nombre}"
        u = design & y[nombre].notna()
        w = big["_w"].where(u, 0.0).astype(float)
        yv = y[nombre].astype("Float64").fillna(0).astype(float)
        num = lambda s: out[f"{b}-{s}-P"] * out[f"{b}-{s}-DEN-W"] if out[f"{b}-{s}-P"] is not None else 0.0
        den = lambda s: out[f"{b}-{s}-DEN-W"]
        partes = ["FAMILIA-NOMINA", "FAMILIA-PERSONAL"]
        d_num = abs(num("NACIONAL-TODOS") - sum(num(p) for p in partes))
        d_den = abs(den("NACIONAL-TODOS") - sum(den(p) for p in partes))
        out[f"{b}-COHERENCIA-FAMILIA-DELTA-NUM-W"] = float(d_num)
        out[f"{b}-COHERENCIA-FAMILIA-DELTA-DEN-W"] = float(d_den)
        tol = 1e-6 * max(den("NACIONAL-TODOS"), 1.0)
        if d_num > tol or d_den > tol:
            raise RuntimeError(f"COHERENCIA rota: {nombre}: Δnum={d_num} Δden={d_den} (tol {tol})")
        out[f"{b}-N-UNIVERSO"] = int(u.sum())
        out[f"{b}-UNIDAD"] = "PR"
        out[f"{b}-CODIGOS-1"] = ",".join(_u)
    P = f"RESULT-{PREFIJO}"
    out.update({
        f"{P}-FILAS-CREDITOS": int(len(big)),
        f"{P}-PERSONAS-CON-CREDITO-N": int(big["_persona"].nunique()),
        f"{P}-NO-SABE-N": int(code.eq("9").sum()),
        f"{P}-BLANCO-O-FUERA-DE-CATALOGO-N": int((~code.isin(list(CATALOGO))).sum()),
        f"{P}-SIN-DISENO-N": int((~design).sum()),
        f"{P}-UPM-EN-PLAN": int(len(sorted((big.loc[design, "_est"] + "\t" + big.loc[design, "_upm"]).unique()))),
        f"{P}-VEREDICTO-TEXTO": fila["veredicto"],
        f"{P}-MATIZ": fila["alcance_del_veredicto"],
        f"{P}-NEGOCIO": "NO-ESTIMABLE: el catálogo de 8.31/8.47 no trae «negocio» (sólo lo excluye en 4)",
        f"{P}-ENSAFI2023": "NO-ESTIMABLE por texto (tabla K8-TRIANGULACION-TEXTO); nada de ENSAFI se lee en esta corrida",
        f"{P}-SERIE": "NO: ENSAFI 2023 y ENFIH 2019 no son comparables entre sí ni con ENIF; se mide ENFIH por separado, rotulado (PARO d)",
    })
    for k, v in diag.items():
        out[f"{P}-{k}"] = v
    return out
