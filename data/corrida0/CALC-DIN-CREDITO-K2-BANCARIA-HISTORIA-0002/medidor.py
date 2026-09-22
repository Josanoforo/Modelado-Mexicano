from __future__ import annotations
"""El primer resultado que produzca este procedimiento es el que se reporta.

Descriptivo rotulado de K2-familia BANCARIA («tarjeta de crédito bancaria»)
por ola de ENIF —2012, 2015, 2018, 2021—, con su FRONTERA (FP-404 (2),
firmada): en 2024 el ítem 6.2.2 se amplía a «u otra institución financiera»
(CAMBIO-DE-INSTRUMENTO), así que **no se compara 2021↔2024** y la cifra del
corpus «bancaria +5.2 pp desde 2021» no se cita sin esa frontera. ENIF 2024
está RESERVADA (decisiones.tsv `reserva:enif2024-credito`) y **no se abre**:
su nivel se emite como texto `RESERVADA-NO-MEDIDA`.

Reutiliza por bytes el medidor sellado de los pisos históricos (input
`MEDIDOR-HISTORIA`: lectura CSV/DBF, join, mapa por ola, cortes de -0003) y
el mapa v1.1 (v1.0 + rol `k2_bancaria`). Por ola: nivel nacional entre toda
persona elegida (P) y entre tenedores de algún producto formal (K1 = 1),
IC95 bootstrap de UPM (10 000 réplicas, PCG64(42)), un plan por ola.
Spec: forense/prereg-caja/DIN-CREDITO-K2-BANCARIA-HISTORIA-spec-v1_0.md.
"""
import types
from pathlib import Path
import pandas as pd

PREFIJO = "DIN-CREDITO-K2-BANCARIA-HISTORIA"
OLAS = ("2012", "2015", "2018", "2021")
N_SOPORTE = 200
FRONTERA = ("FP-404 (2) FIRMADA: la familia bancaria no se compara 2021<->2024 (6.2.2 de 2024 amplía «tarjeta de crédito "
            "bancaria» a «u otra institución financiera»: CAMBIO-DE-INSTRUMENTO); niveles 2012-2021 rotulados con el texto "
            "«tarjeta de crédito bancaria» idéntico en las cuatro olas; poblaciones 18-70 (2012-2018) y 18+ (2021)")


def _bytes(ent):
    b = ent.get("bytes")
    return b if b is not None else Path(ent["ruta_absoluta"]).read_bytes()


def _modulo(inputs, iid, nombre):
    mod = types.ModuleType(nombre)
    exec(compile(_bytes(inputs[iid]), nombre, "exec"), mod.__dict__)
    return mod


def medir(inputs, contrato):
    H = _modulo(inputs, "MEDIDOR-HISTORIA", "medidor_historia")
    m = H._modulo_0003(inputs)
    comp = {(f["conducta"], f["ola"]): f for f in H._tsv(inputs["CREDITO-COMPARABILIDAD-TEXTO"])}
    k2_2024 = comp[("K2", "2024")]
    if k2_2024["veredicto"] != "CAMBIO-DE-INSTRUMENTO" or "BANCARIA" not in k2_2024["alcance_del_veredicto"].upper():
        raise RuntimeError("la tabla de comparabilidad debe declarar K2·2024 CAMBIO-DE-INSTRUMENTO por la familia bancaria (FP-404)")
    out = {}
    P = f"RESULT-{PREFIJO}"
    for ola in OLAS:
        mapa = H._mapa(inputs, ola)
        if not mapa.get("k2_bancaria", {}).get("variables", "").strip():
            raise RuntimeError(f"mapa sin rol k2_bancaria para {ola}")
        f = comp[("K2", ola)]
        if f["veredicto"] not in ("MISMO-INSTRUMENTO", "CAMBIO-MENOR"):
            raise RuntimeError(f"K2·{ola} no es positivo en la tabla: {f['veredicto']}")
        var = mapa["k2_bancaria"]["variables"].strip()
        if var not in f["reactivo"]:
            raise RuntimeError(f"{ola}: el reactivo {var!r} no está en la fila K2·{ola}")
        # sólo los roles que esta corrida necesita: llave, diseño, ponderador, filtro/batería y bancaria
        roles = {r: mapa[r] for r in ("llave", "ponderador", "diseno", "sexo", "edad", "credito_filtro", "credito_bateria", "k2_bancaria")}
        for r in mapa:
            if r not in roles:
                roles[r] = dict(mapa[r], variables="")
        d, rv, diag = H._carga(inputs, ola, roles)
        pond = rv["ponderador"][0]; est, upm = rv["diseno"]
        d["_w"] = pd.to_numeric(d[pond].str.strip(), errors="coerce")
        d["_est"] = d[est].str.strip(); d["_upm"] = d[upm].str.strip()
        pr = d[rv["credito_bateria"]].apply(m._code)
        if "credito_filtro" in rv:
            fl = d[rv["credito_filtro"]].apply(m._code)
            tenedor = pr.eq("1").any(axis=1) | fl.eq("1").any(axis=1)
            sin_producto = fl.eq("2").all(axis=1)
        else:
            tenedor = pr.eq("1").any(axis=1)
            sin_producto = pr.eq("2").all(axis=1)
        c = m._code(d[var])
        y = H._dicot(c, "1", "2")
        y.loc[sin_producto & c.eq("")] = 0.0
        y_ten = y.where(tenedor, pd.NA)
        todos = pd.Series("todos", index=d.index, dtype="object")
        axes = {"nacional": (todos, ("todos",))}
        cells = m._cells(f"{PREFIJO}-{ola}-BANCARIA", y, axes) + m._cells(f"{PREFIJO}-{ola}-BANCARIA-ENTRE-TENEDORES", y_ten, axes)
        res = m._estimate(d, cells, int(contrato["parametros"]["bootstrap_replicas"]), int(contrato["seed"]["valor"]))
        for cell in cells:
            rid = cell["base"]
            res[rid + "-SOPORTE"] = "OK" if res[rid + "-N"] >= N_SOPORTE else f"BAJO-N-MENOR-{N_SOPORTE}"
        out.update(res)
        design = d["_w"].notna() & (d["_w"] > 0) & d["_est"].ne("") & d["_upm"].ne("")
        out[f"{P}-{ola}-FILAS-PERSONAS"] = int(len(d))
        out[f"{P}-{ola}-TENEDORES-N"] = int(tenedor.sum())
        out[f"{P}-{ola}-BANCARIA-INDEFINIDO-N"] = int(y.isna().sum())
        out[f"{P}-{ola}-UPM-EN-PLAN"] = int(len(sorted((d.loc[design, "_est"] + "\t" + d.loc[design, "_upm"]).unique())))
        out[f"{P}-{ola}-REACTIVO"] = f"{var}: {f['texto_literal'][:120]}"
        out[f"{P}-{ola}-VEREDICTO-TEXTO"] = f["veredicto"]
        out[f"{P}-{ola}-UNIDAD"] = "P"
        for k, v in diag.items():
            out[f"{P}-{ola}-{k}"] = v
    out[f"{P}-2024-BANCARIA"] = "RESERVADA-NO-MEDIDA (reserva:enif2024-credito; PARO a del encargo)"
    out[f"{P}-2024-VEREDICTO-TEXTO"] = k2_2024["veredicto"]
    out[f"{P}-DIFERENCIA-2021-2024"] = "NO-SE-COMPARA: " + FRONTERA
    out[f"{P}-CIFRA-DEL-CORPUS-MAS-5-2-PP"] = "NO-SE-CITA sin la frontera FP-404 (2): 2024 mide otra familia («u otra institución financiera»)"
    return out
