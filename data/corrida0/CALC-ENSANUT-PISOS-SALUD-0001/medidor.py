#!/usr/bin/env python3
"""CALC-ENSANUT-PISOS-SALUD-0001 · pisos por segmento ENSANUT 2021–2024 con IC de diseño
e IC calibrado de persistencia sobre el piso 2024.

ACTO GEN2-SALUD-Y-BIENESTAR-PISOS-1 (24/sep/2026, CAJA). Contrato humano:
forense/prereg-caja/SALUD-ENSANUT-PISOS-spec-v1_0.md, congelado en el COMMIT-1 antes de
ejecutar este archivo sobre ningún payload ENSANUT.

QUÉ ESTIMA. Para cada ola abierta (2021, 2022, 2023, 2024; 2025 RESERVADA, E.6, no es
input) y cada conducta de la lista cerrada P1, la proporción ponderada total y por UN eje
a la vez (SEXO, EDAD, ESTRATO, ESCOLARIDAD); nunca cruces. IC de diseño por bootstrap de
UPM dentro de `est_sel`. Sobre el piso 2024, IC calibrado de persistencia (método de
CALC-ENIF-PERSISTENCIA-IC-CALIBRADO-0001 §4) con τ² por grupo (conducta, eje) de los Δ
logit de 2021→22, 22→23, 23→24.

Lo heredado se ejecuta desde los bytes hasheados de su input: la receta común
`tools/dominios/salud/pisos_diseno.py` (`receta_pisos_salud`).
"""
from __future__ import annotations

import math
import types

import numpy as np

P = "RESULT-ENSANUT-PISOS-SALUD"
OLAS = ("2021", "2022", "2023", "2024")
OLA_PISO = "2024"

# payload por (ola, archivo)
PAYLOADS = {
    ("2021", "ADUL"): "ensanut_2021__ensadul2021_entrega_w_15_12_2021_stata_stata_zip",
    ("2021", "INTE"): "ensanut_2021__integrantes_ensanut2021_w_12_01_2022_stata_stata_zip",
    ("2021", "UTIL"): "ensanut_2021__util2021_entrega_w_14_12_2021_stata_stata_zip",
    ("2021", "ADOL"): "ensanut_2021__ensadol2021_entrega_w_14_12_2021_stata_stata_zip",
    ("2022", "ADUL"): "ensanut_2022__ensadul2022_entrega_w_stata_stata_zip",
    ("2022", "INTE"): "ensanut_2022__integrantes_ensanut2022_w_stata_stata_zip",
    ("2022", "UTIL"): "ensanut_2022__util2022_entrega_w_stata_stata_zip",
    ("2022", "ADOL"): "ensanut_2022__ensadol2022_entrega_w_stata_stata_zip",
    ("2023", "ADUL"): "ensanut_2023__adultos_ensanut2023_w_n_stata_stata_zip",
    ("2023", "INTE"): "ensanut_2023__integrantes_ensanut2023_w_n_stata_stata_zip",
    ("2023", "UTIL"): "ensanut_2023__utilizadores_ensanut2023_w_n_stata_stata_zip",
    ("2023", "ADOL"): "ensanut_2023__adolescentes_ensanut2023_w_n_stata_stata_zip",
    ("2024", "ADUL"): "adultos_ensanut2024_w_stata_stata__v2026_09_01",
    ("2024", "INTE"): "integrantes_ensanut2024_w_icb_stata_stata__v2026_09_01",
    ("2024", "UTIL"): "utilizadores_ensanut2024_w_stata_stata__v2026_09_01",
    ("2024", "ADOL"): "adolescentes_ensanut2024_w_stata_stata__v2026_09_01",
}
INPUTS_REPO = frozenset({"receta_pisos_salud"})

DISENO = ["folio_i", "folio_int", "ponde_f", "est_sel", "upm", "estrato"]
CESD = ["a0211", "a0212", "a0213", "a0214", "a0215", "a0216", "a0217"]
COLS = {
    "ADUL": DISENO + ["sexo", "edad", "a1211", "a0301", "a0401", "a1301", "a1308", "a1311", "a1312"] + CESD,
    "INTE": DISENO + ["h0302", "h0303", "h0317a", "h0401", "h0404", "h0406"],
    "UTIL": DISENO + ["sexo", "edad", "u0201"],
    "ADOL": DISENO + ["sexo", "edad", "d0817"],
}

ESCOL = {"HASTA-PRIMARIA": (1, 2, 6), "SECUNDARIA": (3, 7), "MEDIA-SUPERIOR": (4, 5, 8), "SUPERIOR": (9, 10, 11, 12)}
EJE_CATS = {
    "SEXO": ("HOMBRE", "MUJER"),
    "ESTRATO": ("RURAL", "URBANO", "METROPOLITANO"),
    "ESCOLARIDAD": tuple(ESCOL),
}
EDADES = {
    "ADUL": (("20-39", 20, 39), ("40-59", 40, 59), ("60-MAS", 60, 130)),
    "INTE": (("0-9", 0, 9), ("10-19", 10, 19), ("20-59", 20, 59), ("60-MAS", 60, 130)),
    "UTIL": (("0-19", 0, 19), ("20-59", 20, 59), ("60-MAS", 60, 130)),
    "ADOL": (("10-14", 10, 14), ("15-19", 15, 19)),
}
# conducta -> (archivo, ejes)
CONDUCTAS = {
    "DEPRESION-CESD7": ("ADUL", ("SEXO", "EDAD", "ESTRATO", "ESCOLARIDAD")),
    "IDEACION-SUICIDA-ADULTOS": ("ADUL", ("SEXO", "EDAD", "ESTRATO", "ESCOLARIDAD")),
    "DX-DIABETES": ("ADUL", ("SEXO", "EDAD", "ESTRATO", "ESCOLARIDAD")),
    "DX-HIPERTENSION": ("ADUL", ("SEXO", "EDAD", "ESTRATO", "ESCOLARIDAD")),
    "FUMA-ACTUAL": ("ADUL", ("SEXO", "EDAD", "ESTRATO", "ESCOLARIDAD")),
    "ALCOHOL-12M": ("ADUL", ("SEXO", "EDAD", "ESTRATO", "ESCOLARIDAD")),
    "ALCOHOL-EXCESIVO-30D": ("ADUL", ("SEXO", "EDAD", "ESTRATO", "ESCOLARIDAD")),
    "NECESIDAD-SALUD-3M": ("INTE", ("SEXO", "EDAD", "ESTRATO", "ESCOLARIDAD")),
    "BUSCO-ATENCION": ("INTE", ("SEXO", "EDAD", "ESTRATO", "ESCOLARIDAD")),
    "FUE-ATENDIDO": ("INTE", ("SEXO", "EDAD", "ESTRATO", "ESCOLARIDAD")),
    "ATENCION-CONSULTORIO-FARMACIA": ("UTIL", ("SEXO", "EDAD", "ESTRATO", "ESCOLARIDAD")),
    "ATENCION-CURANDERO-HIERBERO": ("UTIL", ("SEXO", "EDAD", "ESTRATO", "ESCOLARIDAD")),
    "IDEACION-SUICIDA-ADOLESCENTES": ("ADOL", ("SEXO", "EDAD", "ESTRATO")),
}
Q = ("P", "EE", "IC-LO", "IC-HI", "N")
_DIAG = ("FILAS", "FILAS-DISENO-VALIDO", "JOIN-SIN-INTEGRANTE")


class ParoDeGuardia(RuntimeError):
    pass


# ══════════════════════════════ utilidades ══════════════════════════════

def _fin(x):
    if x is None:
        return None
    x = float(x)
    return x if math.isfinite(x) else None


def _modulo_desde_bytes(nombre, fuente):
    mod = types.ModuleType(nombre)
    mod.__file__ = f"<{nombre}>"
    exec(compile(fuente, mod.__file__, "exec"), mod.__dict__)
    return mod


def _guardia_inputs(inputs):
    esperados = INPUTS_REPO | set(PAYLOADS.values())
    if set(inputs) != esperados:
        raise ParoDeGuardia(f"inputs fuera de la lista: {sorted(set(inputs) ^ esperados)}")
    for pid in PAYLOADS.values():
        if "2025" in pid.replace("v2026", ""):
            raise ParoDeGuardia(f"payload reservado en la lista: {pid}")
        if not inputs[pid].get("ruta_absoluta"):
            raise ParoDeGuardia(f"payload `{pid}` sin ruta resuelta")
    if inputs["receta_pisos_salud"].get("bytes") is None:
        raise ParoDeGuardia("receta sin bytes: se exige origen repo")


def cats_edad(arch):
    return tuple(c for c, _, _ in EDADES[arch])


def ejes_de(arch, ejes):
    return {e: (cats_edad(arch) if e == "EDAD" else EJE_CATS[e]) for e in ejes}


def rid(conducta, ola, eje, cat, q):
    return f"{P}-{conducta}-{ola}-{eje}-{cat}-{q}"


# ══════════════════════════════ recodificación ══════════════════════════════

def _serie_edad(edad, arch):
    out = np.full(len(edad), None, dtype=object)
    for c, lo, hi in EDADES[arch]:
        out[(edad >= lo) & (edad <= hi)] = c
    return out


def _serie_map(v, mapa):
    out = np.full(len(v), None, dtype=object)
    for c, codigos in mapa.items():
        out[np.isin(v, codigos)] = c
    return out


def _bin(v, si, no):
    out = np.full(len(v), np.nan)
    out[np.isin(v, si)] = 1.0
    out[np.isin(v, no)] = 0.0
    return out


def conducta_y(nombre, f, R):
    """Valor 0/1 por fila; NaN = fuera del universo del reactivo o sin dato (spec §2)."""
    n = R.num
    if nombre == "DEPRESION-CESD7":
        its = np.column_stack([n(f[c]).to_numpy() for c in CESD])
        ok = np.all(np.isin(its, (1, 2, 3, 4)), axis=1)
        pts = its - 1.0
        pts[:, 5] = 3.0 - pts[:, 5]  # a0216 «disfrutó de la vida», invertido
        s = pts.sum(axis=1)
        edad = n(f["edad"]).to_numpy()
        corte = np.where(edad >= 60, 5.0, 9.0)
        y = np.where(s >= corte, 1.0, 0.0)
        y[~ok] = np.nan
        return y
    if nombre == "IDEACION-SUICIDA-ADULTOS":
        return _bin(n(f["a1211"]).to_numpy(), (1,), (2,))
    if nombre == "IDEACION-SUICIDA-ADOLESCENTES":
        return _bin(n(f["d0817"]).to_numpy(), (1,), (2,))
    if nombre == "DX-DIABETES":
        return _bin(n(f["a0301"]).to_numpy(), (1,), (2, 3))
    if nombre == "DX-HIPERTENSION":
        return _bin(n(f["a0401"]).to_numpy(), (1,), (2, 3))
    if nombre == "FUMA-ACTUAL":
        return _bin(n(f["a1301"]).to_numpy(), (1, 2), (3,))
    if nombre == "ALCOHOL-12M":
        return _bin(n(f["a1308"]).to_numpy(), (1, 2, 3, 4), (5, 6))
    if nombre == "ALCOHOL-EXCESIVO-30D":
        sexo = n(f["sexo"]).to_numpy()
        a8 = n(f["a1308"]).to_numpy()
        h = _bin(n(f["a1311"]).to_numpy(), (1,), (2,))
        m = _bin(n(f["a1312"]).to_numpy(), (1,), (2,))
        y = np.where(sexo == 1, h, np.where(sexo == 2, m, np.nan))
        y[np.isin(a8, (5, 6))] = 0.0  # no bebió en 12 meses: salto del cuestionario
        return y
    if nombre == "NECESIDAD-SALUD-3M":
        return _bin(n(f["h0401"]).to_numpy(), (1,), (2,))
    if nombre == "BUSCO-ATENCION":
        y = _bin(n(f["h0404"]).to_numpy(), (1,), (2,))
        y[n(f["h0401"]).to_numpy() != 1] = np.nan
        return y
    if nombre == "FUE-ATENDIDO":
        y = _bin(n(f["h0406"]).to_numpy(), (1,), (2,))
        y[n(f["h0404"]).to_numpy() != 1] = np.nan
        return y
    if nombre == "ATENCION-CONSULTORIO-FARMACIA":
        u = n(f["u0201"]).to_numpy()
        y = np.where(u == 12, 1.0, 0.0)
        y[~((u >= 1) & (u <= 26))] = np.nan
        return y
    if nombre == "ATENCION-CURANDERO-HIERBERO":
        u = n(f["u0201"]).to_numpy()
        y = np.where(u == 20, 1.0, 0.0)
        y[~((u >= 1) & (u <= 26))] = np.nan
        return y
    raise KeyError(nombre)


def prepara(arch, f, inte, R):
    """Frame con diseño válido y ejes como texto. `inte`: integrantes de la misma ola (para
    ESCOLARIDAD por llave FOLIO_I+FOLIO_INT, m:1), o None si `f` ya es integrantes."""
    f = f.copy()
    n = R.num
    w = n(f["ponde_f"])
    ok = w.gt(0) & f["est_sel"].astype(str).str.strip().ne("") & f["upm"].astype(str).str.strip().ne("")
    ok &= f["est_sel"].notna() & f["upm"].notna()
    diag = {"FILAS": int(len(f)), "FILAS-DISENO-VALIDO": int(ok.sum())}
    f = f[ok.to_numpy()].reset_index(drop=True)
    llave = f["folio_i"].astype(str).str.strip() + "|" + f["folio_int"].astype(str).str.strip()
    if arch == "INTE":
        sexo, edad, esc = n(f["h0302"]), n(f["h0303"]), n(f["h0317a"])
        diag["JOIN-SIN-INTEGRANTE"] = 0
    else:
        sexo, edad = n(f["sexo"]), n(f["edad"])
        if arch == "ADOL":
            esc = np.full(len(f), np.nan)
            diag["JOIN-SIN-INTEGRANTE"] = 0
        else:
            ki = inte["folio_i"].astype(str).str.strip() + "|" + inte["folio_int"].astype(str).str.strip()
            mapa = dict(zip(ki[~ki.duplicated(keep=False)], n(inte["h0317a"])[~ki.duplicated(keep=False)]))
            esc = llave.map(mapa)
            diag["JOIN-SIN-INTEGRANTE"] = int((~llave.isin(mapa.keys())).sum())
    sexo = np.asarray(sexo, dtype=float)
    edad = np.asarray(edad, dtype=float)
    esc = np.asarray(esc, dtype=float)
    ejes = {
        "SEXO": _serie_map(sexo, {"HOMBRE": (1,), "MUJER": (2,)}),
        "EDAD": _serie_edad(edad, arch),
        "ESTRATO": _serie_map(np.asarray(n(f["estrato"]), dtype=float),
                              {"RURAL": (1,), "URBANO": (2,), "METROPOLITANO": (3,)}),
        "ESCOLARIDAD": _serie_map(np.where(edad >= 20, esc, np.nan), ESCOL),
    }
    f["_w"] = np.asarray(w[ok.to_numpy()], dtype=float)
    f["_est"] = f["est_sel"].astype(str).str.strip()
    f["_upm"] = f["upm"].astype(str).str.strip()
    return f, ejes, diag, edad


def universo_edad(arch, edad):
    if arch == "ADUL":
        return edad >= 20
    if arch == "ADOL":
        return (edad >= 10) & (edad <= 19)
    return np.isfinite(edad)


# ══════════════════════════════ cálculo ══════════════════════════════

def mide_ola(ola, frames, R, replicas, semilla):
    out, diags = {}, {}
    inte = frames["INTE"]
    for arch in ("ADUL", "INTE", "UTIL", "ADOL"):
        f, ejes, diag, edad = prepara(arch, frames[arch], None if arch == "INTE" else inte, R)
        diags[arch] = diag
        cond = {}
        for c, (a, _) in CONDUCTAS.items():
            if a != arch:
                continue
            y = conducta_y(c, f, R)
            y[~universo_edad(arch, edad)] = np.nan
            cond[c] = y
        todos = {e: (ejes[e], cats) for e, cats in ejes_de(arch, ("SEXO", "EDAD", "ESTRATO", "ESCOLARIDAD")).items()
                 if arch != "ADOL" or e != "ESCOLARIDAD"}
        res = R.marginales(f, cond, todos, f["_w"].to_numpy(), "_est", "_upm", replicas, semilla)
        out.update(res)
    return out, diags


def calcula(por_ola, diags, R):
    out = {}
    for ola in OLAS:
        for arch, d in diags[ola].items():
            for k in _DIAG:
                out[f"{P}-G-{ola}-{arch}-{k}"] = int(d[k])
    for c, (arch, ejes) in CONDUCTAS.items():
        grupos = [("TOTAL", ("TODOS",))] + list(ejes_de(arch, ejes).items())
        for eje, cats in grupos:
            serie = {}
            for ola in OLAS:
                serie[ola] = {}
                for cat in cats:
                    r = por_ola[ola].get((c, eje, cat)) or {}
                    p = _fin(r.get("p"))
                    serie[ola][cat] = p
                    out[rid(c, ola, eje, cat, "P")] = p
                    out[rid(c, ola, eje, cat, "EE")] = _fin(r.get("ee"))
                    out[rid(c, ola, eje, cat, "IC-LO")] = _fin(r.get("lo"))
                    out[rid(c, ola, eje, cat, "IC-HI")] = _fin(r.get("hi"))
                    out[rid(c, ola, eje, cat, "N")] = int(r.get("n", 0))
            t2, nd = R.persistencia(serie, list(OLAS), cats)
            out[f"{P}-{c}-{eje}-TAU2"] = _fin(t2)
            out[f"{P}-{c}-{eje}-N-DELTAS"] = int(nd)
            for cat in cats:
                lo, hi = R.ic_calibrado(out[rid(c, OLA_PISO, eje, cat, "P")],
                                        out[rid(c, OLA_PISO, eje, cat, "IC-LO")],
                                        out[rid(c, OLA_PISO, eje, cat, "IC-HI")], t2)
                out[rid(c, OLA_PISO, eje, cat, "ICC-LO")] = _fin(lo)
                out[rid(c, OLA_PISO, eje, cat, "ICC-HI")] = _fin(hi)
    return out


def medir(inputs, contrato):
    _guardia_inputs(inputs)
    par = contrato["parametros"]
    replicas = int(par["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    R = _modulo_desde_bytes("receta_pisos_salud", inputs["receta_pisos_salud"]["bytes"])
    por_ola, diags = {}, {}
    for ola in OLAS:
        frames = {arch: R.lee_dta(inputs[PAYLOADS[(ola, arch)]]["ruta_absoluta"], COLS[arch])
                  for arch in ("ADUL", "INTE", "UTIL", "ADOL")}
        por_ola[ola], diags[ola] = mide_ola(ola, frames, R, replicas, semilla)
    out = calcula(por_ola, diags, R)
    out[f"{P}-G-BOOTSTRAP-REPLICAS"] = replicas
    out[f"{P}-G-SEED"] = semilla
    out[f"{P}-G-INPUT-RECETA-SHA256"] = str(inputs["receta_pisos_salud"].get("sha256"))
    out[f"{P}-G-OLA-RESERVADA"] = "2025 -- RESERVADA (E.6), no es input"
    return out


# ══════════════════════════════ esquema ══════════════════════════════

def _fila(i, tipo, unidad):
    f = {"id": i, "tipo": tipo, "unidad": unidad}
    if tipo in ("flotante", "proporcion"):
        f["permite_no_estimable"] = True
    return f


def esquema_resultados():
    f = []
    for ola in OLAS:
        for arch in ("ADUL", "INTE", "UTIL", "ADOL"):
            f += [_fila(f"{P}-G-{ola}-{arch}-{k}", "entero", "filas") for k in _DIAG]
    for c, (arch, ejes) in CONDUCTAS.items():
        grupos = [("TOTAL", ("TODOS",))] + list(ejes_de(arch, ejes).items())
        for eje, cats in grupos:
            for ola in OLAS:
                for cat in cats:
                    f += [_fila(rid(c, ola, eje, cat, "P"), "proporcion", "proporción ponderada"),
                          _fila(rid(c, ola, eje, cat, "EE"), "flotante", "error estándar bootstrap"),
                          _fila(rid(c, ola, eje, cat, "IC-LO"), "proporcion", "IC95 diseño, inferior"),
                          _fila(rid(c, ola, eje, cat, "IC-HI"), "proporcion", "IC95 diseño, superior"),
                          _fila(rid(c, ola, eje, cat, "N"), "entero", "personas sin ponderar")]
            f += [_fila(f"{P}-{c}-{eje}-TAU2", "flotante", "varianza logit entre olas"),
                  _fila(f"{P}-{c}-{eje}-N-DELTAS", "entero", "deltas definidos")]
            for cat in cats:
                f += [_fila(rid(c, OLA_PISO, eje, cat, "ICC-LO"), "proporcion", "IC calibrado persistencia, inferior"),
                      _fila(rid(c, OLA_PISO, eje, cat, "ICC-HI"), "proporcion", "IC calibrado persistencia, superior")]
    f += [_fila(f"{P}-G-BOOTSTRAP-REPLICAS", "entero", "réplicas"),
          _fila(f"{P}-G-SEED", "entero", "semilla"),
          _fila(f"{P}-G-INPUT-RECETA-SHA256", "texto", "sha256"),
          _fila(f"{P}-G-OLA-RESERVADA", "texto", "declaración")]
    return f
