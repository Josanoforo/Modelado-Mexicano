#!/usr/bin/env python3
"""tablero_unico.py -- secciones §11 (carriles) y §12 (pendientes) del tablero único.

Mesa pidió un solo tablero (29/sep): el tablero de carriles y el inventario de
pendientes dejan de ser archivos aparte y entran al TABLERO-PROGRAMA.md, entre
sus propios marcadores. Este script solo deriva; no escribe en el repo.

Uso (desde la raíz del clon):
    python3 tools/tablero_carriles.py > CARR.md      # el tablero de carriles completo, sin escribir
    python3 tablero_unico.py carriles CARR.json CARR_PREVIO.json CARR.md [CARR_SIM.json] > s11.md
    python3 tablero_unico.py pendientes NPC.json NPC_PREVIO.json CARR.json > s12.md
    python3 tablero_unico.py inserta TABLERO.md s11.md s12.md

Entradas: `tools/tablero_carriles.py --json`, `tools/nc_por_clase.py --json` y
`forense/firmas-pendientes.tsv`, las tres leídas tal cual. Ninguna cifra se teclea.
"""
from __future__ import annotations

import collections, csv, json, os, re, subprocess, sys

csv.field_size_limit(sys.maxsize)
sh = lambda c: subprocess.run(c, shell=True, capture_output=True, text=True).stdout.strip()
MARCAS = {"carriles": ("<!-- TABLERO-UNICO:CARRILES:BEGIN -->", "<!-- TABLERO-UNICO:CARRILES:END -->"),
          "pendientes": ("<!-- TABLERO-UNICO:PENDIENTES:BEGIN -->", "<!-- TABLERO-UNICO:PENDIENTES:END -->")}
SEM = {"ROJO": "🔴", "AMARILLO": "🟡", "NARANJA": "🟠", "VERDE": "🟢", "GRIS": "⚪"}
ORDEN_SEM = ["ROJO", "NARANJA", "AMARILLO", "VERDE", "GRIS"]
CAT = ["FIRMA", "RESERVA", "ADQUISICION", "NC-PARO", "CALC", "EDITORIAL"]
CAT_CORTA = {"FIRMA": "F", "RESERVA": "R", "ADQUISICION": "A", "NC-PARO": "N", "CALC": "C", "EDITORIAL": "E"}


def celda(s, n=None):
    s = re.sub(r"\s+", " ", str(s or "")).replace("|", "/")
    # los controles cuentan como rótulo sin serie un «E6» o «M3» suelto; en texto
    # copiado de una fila se separa con un punto medio para no dispararlo
    s = re.sub(r"(?<![A-Za-z0-9_\-\.])([EM])(-?\d+)(?![\w\-])", r"\1·\2", s)
    return s if n is None or len(s) <= n else s[: n - 1].rstrip() + "…"


def cabecera_corte():
    return sh("git rev-parse --short=8 HEAD"), sh("git log -1 --format=%ad --date=format:'%d/%b/%Y %H:%M'")


def fps():
    return {r["id"]: r for r in csv.DictReader(
        (l for l in open("forense/firmas-pendientes.tsv", encoding="utf-8") if not l.startswith("#")), delimiter="\t")}


def dueno_stopper(cat, s, fp):
    if cat == "FIRMA":
        return f"mesa (firma {fp.get(s['id'], {}).get('estado', '¿?')})"
    if cat == "RESERVA":
        return "mesa por escrito o pre-registro (E.6)"
    return celda(s.get("sucesor") or "—", 70)


# ───────────────────────────── §11 · carriles ─────────────────────────────
def carriles(ruta, ruta_prev, ruta_md, ruta_sim=None):
    sha, fecha = cabecera_corte()
    B = json.load(open(ruta)); A = json.load(open(ruta_prev))
    S = json.load(open(ruta_sim)) if ruta_sim else None
    b = {c["carril"]: c for c in B["carriles"]}; a = {c["carril"]: c for c in A["carriles"]}
    fp = fps()
    w = []; o = w.append
    cnt = collections.Counter(c["semaforo"] for c in b.values())
    cnt_a = collections.Counter(c["semaforo"] for c in a.values())
    sig = lambda c: (c.get("siguiente") or {})
    cambia = [k for k in b if k in a and (sig(b[k]).get("categoria"), sig(b[k]).get("id")) != (sig(a[k]).get("categoria"), sig(a[k]).get("id"))]
    cambia_sem = [k for k in b if k in a and b[k]["semaforo"] != a[k]["semaforo"]]
    o(f"_Derivado con `python3 tools/tablero_carriles.py --json` y `python3 tools/tablero_carriles.py` (el markdown completo, "
      f"sin escribir) sobre `origin/main = {sha}` ({fecha}). Un carril es un report temático del corpus. Los umbrales del semáforo "
      "y la precedencia de la siguiente acción viven en un solo sitio, la cabecera de `tools/tablero_carriles.py`, y se copian "
      "tal cual en C.1. Esta sección es el tablero de carriles completo: lo que antes vivía en `forense/tablero/TABLERO-CARRILES.md` "
      "y en su página web está aquí, de C.1 a C.9. Un rótulo de letra y número de otra hoja, copiado de una fila, se muestra con "
      "punto medio (así: «[E·1]», de la hoja de NC-DECISIONES) para no confundirlo con una regla de las instrucciones._\n")
    o("**Semáforos:** " + " · ".join(f"{SEM[s]} {s} {cnt.get(s, 0)}" for s in ORDEN_SEM)
      + f" (corte anterior: " + " · ".join(f"{s} {cnt_a.get(s, 0)}" for s in ORDEN_SEM if cnt_a.get(s)) + "). "
      f"Cambian de semáforo **{len(cambia_sem)}** de {len(b)}; cambian de siguiente acción **{len(cambia)}**.\n")

    herr = {}
    for bloque in ("\n" + open(ruta_md, encoding="utf-8").read()).split("\n## ")[1:]:
        tit, _, cuerpo = bloque.partition("\n")
        # dentro del tablero único los niveles bajan dos: ### → ####, #### → #####
        cuerpo = re.sub(r"^(#{3,4}) ", lambda m: "#" * (len(m.group(1)) + 1) + " ", cuerpo, flags=re.M)
        # mismo criterio que celda(): un «[E1]» de otra hoja no debe leerse como regla de las instrucciones
        cuerpo = re.sub(r"(?<![A-Za-z0-9_\-\.])([EM])(-?\d+)(?![\w\-])", r"\1·\2", cuerpo)
        herr[tit.split(" ⟨")[0].strip()] = cuerpo.strip()
    assert {"Cómo leer", "Resumen", "Carriles", "Cadena de procedencia"} <= set(herr), sorted(herr)
    o("### C.1 · Cómo leer (texto de la herramienta)\n")
    o(herr["Cómo leer"] + "\n")
    o("### C.2 · Los carriles, del más lejos al más cerca\n")
    o("Stoppers por tipo: F firma · R reserva · A adquisición · N NC en paro · C cálculo · E editorial. `SIN-UNION` (afirmaciones "
      "sin instrumento del vocabulario) cuenta como adquisición en todos los carriles; se lee en C.4.\n")
    o("| carril | tema | semáforo | núcleo | núcleo con cifra | reglas con dictamen | stoppers F·R·A·N·C·E | siguiente acción | Δ corte |")
    o("|---|---|---|---|---:|---:|---|---|---|")
    orden = sorted(b.values(), key=lambda c: (ORDEN_SEM.index(c["semaforo"]), -c["afirmaciones"]))
    for c in orden:
        k = c["carril"]; s = sig(c)
        st = "·".join(str(len(c["stoppers"].get(x, []))) for x in CAT)
        d = []
        if k in cambia_sem: d.append(f"semáforo era {a[k]['semaforo']}")
        if k in cambia:
            sa = sig(a[k]); d.append(f"antes {sa.get('categoria', '—')} `{sa.get('id', '—')}`")
        o(f"| {k[-2:]} | {celda(c['titulo'], 60)} | {SEM[c['semaforo']]} {c['semaforo']} | "
          f"{', '.join(c['nucleo'])} | {c['nucleo_con_cifra']}/{len(c['nucleo'])} | "
          f"{round(100 * c['frac_reglas_con_dictamen'])} % de {c['reglas_total']} | {st} | "
          f"{s.get('categoria', '—')} `{s.get('id', '—')}` | {'; '.join(d) or '='} |")
    o("")

    o("### C.3 · Lo que más carriles frena\n")
    o("Cada stopper, contado sobre las tarjetas de los 31 carriles (sin `SIN-UNION`). «Quién lo mueve» sale del campo "
      "sucesor de la fila o, para firmas, de su estado en `forense/firmas-pendientes.tsv`.\n")
    agg = collections.defaultdict(set); ref = {}
    for c in b.values():
        for cat, lst in c["stoppers"].items():
            for s in lst:
                if s["id"] == "SIN-UNION":
                    continue
                agg[(cat, s["id"])].add(c["carril"][-2:]); ref[(cat, s["id"])] = s
    top = sorted(agg.items(), key=lambda kv: (-len(kv[1]), kv[0][1]))[:15]
    o("| stopper | tipo | carriles | cuáles | quién lo mueve | qué es |")
    o("|---|---|---:|---|---|---|")
    for (cat, i), cs in top:
        o(f"| `{i}` | {cat} | {len(cs)} | {', '.join(sorted(cs))} | {dueno_stopper(cat, ref[(cat, i)], fp)} | "
          f"{celda(ref[(cat, i)].get('texto'), 110)} |")
    o("")

    o("### C.4 · `SIN-UNION` y lo que la regla no captura\n")
    su = [c for c in b.values() if any(s["id"] == "SIN-UNION" for s in c["stoppers"].get("ADQUISICION", []))]
    su_sig = [c["carril"][-2:] for c in b.values() if sig(c).get("id") == "SIN-UNION"]
    o(f"`SIN-UNION` aparece como stopper en **{len(su)}** de {len(b)} carriles y es la siguiente acción en **{len(su_sig)}** "
      f"({', '.join(sorted(su_sig)) or '—'}). No es un bloqueo con dueño: cuenta afirmaciones del report que no nombran un "
      "instrumento del vocabulario. La opción de sacarlo de la precedencia espera la firma `FP-260929-GEN2-TUBERIA-TABLERO-INSUMOS-1-c6aa-01`.\n")

    if S:
        s_ = {c["carril"]: c for c in S["carriles"]}
        cnt_s = collections.Counter(c["semaforo"] for c in s_.values())
        o("### C.5 · Con los insumos vigentes — simulación, no es el semáforo oficial\n")
        o("`tools/tablero_carriles.py` lee `canon/catalogo-del-mexicano-v1_3.tsv`, `canon/reglas-contrastadas-v1_0.tsv` y "
          "`familias-2027-estado-v1_1.tsv`; el canon ya tiene v1.4, v1.2 y v1.2 (`docs/data/catalogo-vigente.json` dice v1_4). "
          "Corrida del mismo script con solo esas tres rutas cambiadas (las versiones nuevas solo añaden columnas: el catálogo "
          "`validacion_ciega_lote3` y `holdout_gastado`, familias `reverificacion_v1_2`; reglas, cabecera idéntica):\n")
        o("**Semáforos simulados:** " + " · ".join(f"{SEM[s]} {s} {cnt_s.get(s, 0)}" for s in ORDEN_SEM) + "\n")
        o("| carril | tema | oficial | simulado | núcleo con cifra | reglas con dictamen |")
        o("|---|---|---|---|---|---|")
        for k in sorted(b):
            x, y = b[k], s_[k]
            if (x["semaforo"], x["nucleo_con_cifra"], round(x["frac_reglas_con_dictamen"], 2)) != \
               (y["semaforo"], y["nucleo_con_cifra"], round(y["frac_reglas_con_dictamen"], 2)):
                o(f"| {k[-2:]} | {celda(x['titulo'], 55)} | {SEM[x['semaforo']]} {x['semaforo']} | "
                  f"{SEM[y['semaforo']]} {y['semaforo']} | {x['nucleo_con_cifra']} → {y['nucleo_con_cifra']} | "
                  f"{round(100 * x['frac_reglas_con_dictamen'])} % → {round(100 * y['frac_reglas_con_dictamen'])} % de {y['reglas_total']} |")
        o("")
    o("### C.6 · Adquisición — global (texto de la herramienta)\n")
    o(herr.get("Adquisición — global", "—") + "\n")
    o("### C.7 · Frente 2027 (texto de la herramienta)\n")
    o(herr.get("Frente 2027", "—") + "\n")
    o("### C.8 · Tarjeta de cada carril (texto de la herramienta)\n")
    o("Una tarjeta por carril, en el orden de C.2: cifras por dominio, reglas, stoppers con su sucesor, validación, "
      "editorial y familias 2027. Los `⟨F…⟩` remiten a C.9.\n")
    o(herr["Carriles"] + "\n")
    o("### C.9 · Cadena de procedencia (texto de la herramienta)\n")
    o(herr["Cadena de procedencia"] + "\n")
    print("\n".join(w))


# ───────────────────────────── §12 · pendientes ───────────────────────────
DUENO = {"ESPERA-MESA-DECISION": "MESA-DECISION", "ESPERA-MESA-ACCION": "MESA-ACCION",
         "ESPERA-DIRECCION-ENCARGO": "DIRECCION-ENCARGO", "ESPERA-CANAL": "CANAL", "ESPERA-APERTURA": "APERTURA",
         "ESPERA-ADQUISICION": "ADQUISICION", "ESPERA-ACTO-NOMBRADO": "CAJA", "ESPERA-MESA": "MESA",
         "ESPERA-DIRECCION": "DIRECCION", "EN-CURSO": "EN-CURSO", "ESPERA-FIRMA": "FIRMA", "SIN-ASIGNAR": "SIN-ASIGNAR",
         "VENCIDA-CANDIDATA": "VENCIDA-CANDIDATA"}
ORDEN_D = ["MESA-DECISION", "MESA-ACCION", "DIRECCION-ENCARGO", "CANAL", "APERTURA", "ADQUISICION", "CAJA",
           "MESA", "DIRECCION", "FIRMA", "EN-CURSO", "VENCIDA-CANDIDATA", "SIN-ASIGNAR"]
MUEVE = {"MESA-DECISION": "mesa elige una opción de la hoja de decisiones de PENDIENTES-4",
         "MESA-ACCION": "mesa hace algo con su identidad (acceso, envío, recibo)",
         "DIRECCION-ENCARGO": "dirección revisa y lanza un encargo ya redactado como propuesto",
         "CANAL": "que se fusione el `[deriva]` en cola",
         "APERTURA": "que se abra una ola reservada (pre-registro o mesa por escrito, E.6)",
         "ADQUISICION": "que llegue el payload que nombra la solicitud",
         "CAJA": "que caja corra un encargo ya archivado",
         "MESA": "mesa (dueño sin subtipo)", "DIRECCION": "dirección (dueño sin subtipo)",
         "FIRMA": "una firma abierta", "EN-CURSO": "un acto en vuelo",
         "VENCIDA-CANDIDATA": "dictaminar: su acto ya cerró", "SIN-ASIGNAR": "asignar dueño"}


def pendientes(ruta, ruta_prev, ruta_carr):
    sha, fecha = cabecera_corte()
    npc = json.load(open(ruta)); prev = json.load(open(ruta_prev))
    F = npc["filas"]; fp = fps()
    B = json.load(open(ruta_carr))
    enc_arch = set(os.listdir("forense/encargos"))
    enc_prop = set(os.listdir("forense/encargos/cola/PROPUESTOS")) if os.path.isdir("forense/encargos/cola/PROPUESTOS") else set()
    hoja = "forense/analisis/pendientes-4/hoja-decisiones-pendientes-4.md"
    anclas = {}
    if os.path.exists(hoja):
        for l in open(hoja, encoding="utf-8"):
            m = re.match(r"^#{1,4} (D\d+) · (.+)", l)
            if m:
                anclas[m.group(1)] = m.group(2).strip()
    vista = {}
    if os.path.exists("/home/claude/trabajo-tablero/status.txt"):
        for l in open("/home/claude/trabajo-tablero/status.txt"):
            if "=" in l:
                k, v = l.strip().split("=", 1); vista[k] = v
    dentro = lambda x: re.search(r"\(([^)]*)\)", x["que_le_falta"]).group(1) if re.search(r"\(([^)]*)\)", x["que_le_falta"]) else ""

    def control(x):
        d = DUENO.get(x["clase"], x["clase"]); q = dentro(x); ev = x.get("evidencia_derivada", "")
        if d == "DIRECCION-ENCARGO":
            ok = any(q.lower() in e.lower() for e in enc_prop | enc_arch if e.endswith(".md"))
            return ok, "el encargo que nombra no está redactado ni archivado"
        if d == "MESA-DECISION":
            m = re.search(r"#(D\d+)", q)
            return bool(m and m.group(1) in anclas), "la decisión que cita no está en la hoja"
        if d == "MESA-ACCION" or d == "MESA":
            return bool(re.search(r"\d{4}-\d{2}-\d{2}", q)), "sin fecha"
        if d == "CANAL":
            return vista.get("deriva_en_cola", "0") not in ("0", ""), "no hay `[deriva]` en cola que la cierre"
        if d == "APERTURA":
            if "SIN-FP" in ev:
                return False, "sin FP que abra la ola: excepción ya declarada por INSUMOS-1 (la abre un pre-registro o mesa por escrito)"
            if "[FIRMADA]" in ev:
                return False, "su FP ya está FIRMADA: probablemente ya no espera apertura"
            return True, ""
        if d == "ADQUISICION":
            return "SIN-SOLICITUD" not in ev and bool(ev), "no nombra una solicitud que exista"
        if d == "CAJA":
            m = re.search(r"(forense/encargos/[^)\s]+\.md)", q)
            return bool(m and os.path.exists(m.group(1))), "el encargo que nombra no está archivado"
        return False, "fuera de la lista cerrada de dueños"

    res = [(x, *control(x)) for x in F]
    por = collections.defaultdict(list)
    for x, ok, mot in res:
        por[DUENO.get(x["clase"], x["clase"])].append((x, ok, mot))
    abiertas = [r for r in fp.values() if r["estado"] == "ABIERTA"]
    # carriles que frena cada FP abierta (de las tarjetas del tablero de carriles)
    frena = collections.defaultdict(set)
    for c in B["carriles"]:
        for s in c["stoppers"].get("FIRMA", []):
            frena[s["id"]].add(c["carril"][-2:])
    w = []; o = w.append
    o(f"_Derivado con `python3 tools/nc_por_clase.py --json` y `forense/firmas-pendientes.tsv` sobre `origin/main = {sha}` "
      f"({fecha}); universo: {npc['universo']}. La clase de cada fila es la del clasificador, sin reinterpretar; el control es de "
      "este puesto y dice qué comprueba. No toca el libro ni cierra nada. Esta sección sustituye al inventario PENDIENTES-PROGRAMA "
      "que este puesto entregaba aparte._\n")

    o(f"### P.1 · Firmas de mesa abiertas: {len(abiertas)}\n")

    def plazo(r):
        m = re.search(r"PLAZO (\d{4}-\d{2}-\d{2})", r.get("gatea", ""))
        return m.group(1) if m else ""
    hoy = sh("git log -1 --format=%ad --date=short")
    o(f"Ordenadas por plazo y después por cuántos carriles frenan. «Vence» se compara con la fecha del commit del corte ({hoy}). "
      "Las de PENDIENTES-4 (`12d9-…`) abren con la decisión de su hoja entre corchetes.\n")
    o("| firma | qué se firma | plazo | carriles que frena | creada |")
    o("|---|---|---|---|---|")
    for r in sorted(abiertas, key=lambda r: (plazo(r) or "9999", -len(frena.get(r["id"], ())), r["id"])):
        p = plazo(r)
        pl = (f"**{p} · vence**" if p and p <= hoy else p) or "—"
        cs = sorted(frena.get(r["id"], ()))
        o(f"| `{r['id']}` | {celda(r['qué_se_firma'], 150)} | {pl} | {', '.join(cs) if cs else '—'} | {r['creado']} |")
    o("")

    o(f"### P.2 · Deuda abierta por dueño: {len(F)} filas\n")
    o("| dueño | filas | qué la mueve | control de este puesto | cumplen | no cumplen |")
    o("|---|---:|---|---|---:|---:|")
    exige = {"DIRECCION-ENCARGO": "el encargo que nombra existe (propuesto o archivado)",
             "MESA-DECISION": "la decisión que cita existe en la hoja", "MESA-ACCION": "tiene fecha", "MESA": "tiene fecha",
             "CANAL": "hay un `[deriva]` en cola", "APERTURA": "nombra la FP que abriría la ola y esa FP sigue abierta",
             "ADQUISICION": "nombra una solicitud que existe", "CAJA": "el encargo que nombra está archivado"}
    for d in ORDEN_D + sorted(set(por) - set(ORDEN_D)):
        xs = por.get(d)
        if xs:
            o(f"| {d} | {len(xs)} | {MUEVE.get(d, '—')} | {exige.get(d, 'fuera de la lista cerrada')} | "
              f"{sum(1 for r in xs if r[1])} | {sum(1 for r in xs if not r[1])} |")
    o(f"| **total** | **{len(F)}** | | | **{sum(1 for r in res if r[1])}** | **{sum(1 for r in res if not r[1])}** |\n")

    ids_p = {x["id"]: x for x in prev["filas"]}; ids_n = {x["id"] for x in F}
    cerradas = [i for i in ids_p if i not in ids_n]; nuevas = [x for x in F if x["id"] not in ids_p]
    libro = {r["id"]: r for r in csv.DictReader(
        (l for l in open("forense/no-corrido.tsv", encoding="utf-8") if not l.startswith("#")), delimiter="\t")}
    o("### P.3 · Flujo contra el corte anterior\n")
    o(f"Antes: {prev['universo']}. **Salieron {len(cerradas)}** y **entraron {len(nuevas)}**. Estado hoy de las que salieron: "
      + ", ".join(f"{k} {v}" for k, v in collections.Counter((libro.get(i, {}).get('estado') or 'NO-EN-EL-LIBRO').split(' ')[0]
                                                                for i in cerradas).most_common()) + ".\n")
    if nuevas:
        o("Las que entraron, por acto que las abrió: " + ", ".join(f"{a} {n}" for a, n in collections.Counter(
            x["acto_que_la_abrio"] for x in nuevas).most_common()) + ".\n")

    o("### P.4 · Hallazgos: filas que no pasan el control\n")
    malas = [(x, mot) for x, ok, mot in res if not ok]
    if not malas:
        o("Ninguna.\n")
    g = collections.defaultdict(list)
    for x, mot in malas:
        g[(DUENO.get(x["clase"], x["clase"]), mot)].append(x)
    for (d, mot), xs in sorted(g.items(), key=lambda kv: -len(kv[1])):
        o(f"**{d} · {mot} · {len(xs)}**\n")
        o("| id | qué le falta (clasificador) | evidencia derivada |\n|---|---|---|")
        for x in xs:
            o(f"| `{x['id']}` | {celda(x['que_le_falta'], 110)} | {celda(x.get('evidencia_derivada'), 110) or '—'} |")
        o("")

    o("### P.5 · El detalle, por dueño\n")
    xs = [r[0] for r in por.get("MESA-DECISION", [])]
    if xs:
        o(f"**MESA-DECISION · {len(xs)} filas en {len({re.search(r'#(D\\d+)', dentro(x)).group(1) for x in xs if re.search(r'#(D\\d+)', dentro(x))})} decisiones** "
          f"de `{hoja}` (cada una con opciones, costo y texto de firma en la hoja):\n")
        o("| decisión | tema | filas | ids |\n|---|---|---:|---|")
        gd = collections.defaultdict(list)
        for x in xs:
            m = re.search(r"#(D\d+)", dentro(x)); gd[m.group(1) if m else "¿?"].append(x["id"])
        for dd in sorted(gd, key=lambda s: int(s[1:]) if s[1:].isdigit() else 999):
            o(f"| {dd} | {celda(anclas.get(dd, '—'), 90)} | {len(gd[dd])} | {' '.join('`' + i + '`' for i in gd[dd])} |")
        o("")
    for d, cols in (("MESA-ACCION", ("pieza", "que_no_se_corrio")), ("APERTURA", ("que_le_falta", "evidencia_derivada")),
                    ("ADQUISICION", ("que_le_falta", "evidencia_derivada")), ("CAJA", ("que_le_falta", "que_no_se_corrio")),
                    ("MESA", ("que_le_falta", "que_no_se_corrio")), ("DIRECCION", ("que_le_falta", "que_no_se_corrio")),
                    ("EN-CURSO", ("que_le_falta", "que_no_se_corrio")), ("SIN-ASIGNAR", ("que_le_falta", "que_no_se_corrio"))):
        xs = [r[0] for r in por.get(d, [])]
        if not xs:
            continue
        o(f"**{d} · {len(xs)}**\n")
        o(f"| id | {cols[0].replace('_', ' ')} | {cols[1].replace('_', ' ')} |\n|---|---|---|")
        for x in xs:
            o(f"| `{x['id']}` | {celda(x.get(cols[0]), 100)} | {celda(x.get(cols[1]), 120) or '—'} |")
        o("")
    xs = [r[0] for r in por.get("DIRECCION-ENCARGO", [])]
    if xs:
        ge = collections.defaultdict(list)
        for x in xs:
            ge[dentro(x)].append(x["id"])
        o(f"**DIRECCION-ENCARGO · {len(xs)} filas en {len(ge)} encargos** redactados como propuestos en "
          "`forense/encargos/cola/PROPUESTOS/`:\n")
        o("| encargo propuesto | filas | ¿redactado? | ids |\n|---|---:|---|---|")
        for e_, ids in sorted(ge.items(), key=lambda kv: -len(kv[1])):
            red = "sí" if any(e_.lower() in f.lower() for f in enc_prop) else ("archivado" if any(e_.lower() in f.lower() for f in enc_arch) else "**no**")
            o(f"| {e_} | {len(ids)} | {red} | {' '.join('`' + i.rsplit('-', 2)[-2] + '-' + i.rsplit('-', 1)[-1] + '`' for i in ids)} |")
        o("\nLos ids van abreviados a su sufijo `hhhh-NN`; la fila completa se busca con `grep hhhh-NN forense/no-corrido.tsv`.\n")
    xs = [r[0] for r in por.get("CANAL", [])]
    if xs:
        o(f"**CANAL · {len(xs)}** — se cierran cuando el `[deriva]` en cola se fusione "
          f"(vista publicada: `{vista.get('vista_publicada_fecha', '¿?')}`, `[deriva]` en cola: {vista.get('deriva_en_cola', '¿?')}):\n")
        o("| id | pieza |\n|---|---|")
        for x in xs:
            o(f"| `{x['id']}` | {celda(x.get('pieza'), 120)} |")
        o("")
    print("\n".join(w))


# ───────────────────────────── inserción ──────────────────────────────────
def inserta(ruta_md, s11, s12):
    t = open(ruta_md, encoding="utf-8").read()
    for clave, cuerpo in (("carriles", open(s11, encoding="utf-8").read()), ("pendientes", open(s12, encoding="utf-8").read())):
        b, e = MARCAS[clave]
        assert t.count(b) == 1 and t.count(e) == 1, f"marcadores de {clave}: se esperaba uno de cada"
        t = re.sub(re.escape(b) + r".*?" + re.escape(e), lambda m: f"{b}\n{cuerpo.strip()}\n{e}", t, flags=re.S)
    open(ruta_md, "w", encoding="utf-8").write(t)
    print(f"insertado: {ruta_md} · {len(t):,} bytes")


if __name__ == "__main__":
    f = sys.argv[1] if len(sys.argv) > 1 else ""
    if f == "carriles":
        carriles(*sys.argv[2:6])
    elif f == "pendientes":
        pendientes(*sys.argv[2:5])
    elif f == "inserta":
        inserta(*sys.argv[2:5])
    else:
        print(__doc__); sys.exit(2)
