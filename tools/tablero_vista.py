#!/usr/bin/env python3
"""tablero_vista.py -- vista visual del TABLERO DEL PROGRAMA, para leerse en diez segundos.

No es una segunda fuente. Toda cifra sale de (a) TABLERO-PROGRAMA.md, (b) la salida
--json de tools/tablero_programa.py, o (c) git y los TSV del repo, derivados aqui.
Ninguna cifra esta escrita en este archivo.

Uso:
    python3 tools/tablero_programa.py --json > /tmp/ind.json
    python3 tools/tablero_vista.py TABLERO-PROGRAMA.md /tmp/ind.json salida.html

Reglas (instrucciones v2.12): v2.1 cifras derivadas · A.10 estampa de universo con SHA ·
A.13 los negativos declaran cuantos archivos examinaron.
"""
from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from datetime import date

# ── utilidades ────────────────────────────────────────────────────────────
def sh(cmd: str) -> str:
    return subprocess.run(cmd, shell=True, capture_output=True).stdout.decode("utf-8", "replace").strip()


def sin_md(s: str) -> str:
    s = re.sub(r"`([^`]*)`", r"\1", s)
    s = re.sub(r"\*\*([^*]*)\*\*", r"\1", s)
    s = re.sub(r"\*([^*]*)\*", r"\1", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    return s.strip()


def seccion(md: str, marca: str) -> str:
    if not marca or marca not in md:
        return ""
    cuerpo = md.split(marca, 1)[1]
    for corte in ("\n## ", "\n### "):
        cuerpo = cuerpo.split(corte)[0]
    return cuerpo


def marca_por_titulo(md: str, *palabras: str):
    """Devuelve el encabezado (como marcador de corte) cuya línea contiene alguna palabra."""
    for ln in md.splitlines():
        if ln.startswith("#"):
            bajo = ln.lower()
            if any(p in bajo for p in palabras):
                return ln
    return None


def tabla(md: str, marca: str):
    """Filas de la primera tabla de la seccion, como dicts encabezado->celda."""
    filas = []
    for ln in seccion(md, marca).splitlines():
        ln = ln.strip()
        if not ln.startswith("|"):
            continue
        if re.fullmatch(r"\|[\s:\-|]+\|", ln):
            continue
        filas.append([c.strip() for c in ln.strip("|").split("|")])
    if not filas:
        return []
    cab = [sin_md(c) for c in filas[0]]
    return [dict(zip(cab, f)) for f in filas[1:]]


def e(s) -> str:
    return html.escape(str(s))


# Nombres de lectura para las siete señales. Es prosa de presentación: los valores,
# los deltas y todo lo demás siguen saliendo del tablero, nunca de aquí.
HUMANO_GEN2 = {
    "N_corridas_requeridas": "Corridas que la demanda exige",
    "N_corridas_selladas": "Corridas selladas",
    "N_resultados_activos": "Números que el modelo consume",
    "N_resultados_sellados": "Con cadena de procedencia sellada",
    "N_resultados_pendientes": "Todavía sin cadena",
    "dependencias_numericas_legacy_activas": "Dependencias legacy activas",
    "N_resultados_gen2_sellados": "Resultados Gen 2 sellados",
    "N_resultados_gen2_pendientes_adopcion": "Esperando adopción de mesa",
    "N_resultados_gen2_adoptados_activos": "Adoptados y en uso",
    "resultados_con_validacion_independiente": "Con validación independiente",
    "diferencias_materiales": "Diferencias materiales contra legacy",
    "no_corrido_abiertas": "Piezas no corridas, abiertas",
    "replays_legacy_sellados": "Replays legacy (no cuentan)",
    "corredores_envueltos_legacy": "Corredores envueltos legacy",
}

HUMANO = {
    "S1": "Reglas cargadas sin medir",
    "S2": "Celdas del duelo listas para puntuar",
    "S3": "¿Se abrió la Ola 6?",
    "S4": "Valores del motor medidos con dato",
    "S5": "Resultados esperando tu firma",
    "S6": "Segmentos con intervalo medido",
    "S7": "Payloads oficiales registrados",
}


# ── ficha ─────────────────────────────────────────────────────────────────
def main() -> None:
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(2)
    ruta_md, ruta_json, destino = sys.argv[1], sys.argv[2], sys.argv[3]
    gen2 = json.load(open(sys.argv[4], encoding="utf-8")) if len(sys.argv) > 4 else None
    md = open(ruta_md, encoding="utf-8").read()
    ind = {k: v["valor"] for k, v in json.load(open(ruta_json, encoding="utf-8")).items()}

    sha = ind["sha"]
    primero = sh("git log --reverse --format=%ad --date=short | head -1")
    ultimo = ind["fecha_commit"]
    dias = (date.fromisoformat(ultimo) - date.fromisoformat(primero)).days
    dias_activos = int(sh("git log --format=%ad --date=short | sort -u | wc -l") or 0)

    # ── el motor: 49 casillas, tres estados, todos derivados ──────────────
    m = re.search(r"(\d+)\s*reglas\D+(\d+)\s*en per", ind["modelo_reglas_canon"])
    canon, perimetro = int(m.group(1)), int(m.group(2))
    con_dato = ind["motor_reglas_con_dato"]
    sin_dato = len(ind["motor_reglas_sin_dato"])
    fuera = canon - con_dato - sin_dato

    # ── la señal: §1 del entregable ───────────────────────────────────────
    señales = []
    filas_senal = tabla(md, marca_por_titulo(md, "la señal")) or tabla(md, "## 1 ·")
    cab = [c.lower() for c in (filas_senal[0].keys() if filas_senal else [])]
    arroba = [i for i, c in enumerate(cab) if c.startswith("@")]
    i_val = max(arroba) if arroba else 1            # Gen 1: antes|ahora|Δ · Gen 2: contador|valor|qué
    i_delta = (cab.index("δ") if "δ" in cab else i_val + 1) if arroba else None
    for r in filas_senal:
        cols = list(r.values())
        if len(cols) <= i_val:
            continue
        etiqueta = sin_md(cols[0])
        mm = re.match(r"(S\d)\s*·\s*(.+)", etiqueta)
        clave, nombre = (mm.group(1), mm.group(2)) if mm else ("", etiqueta)
        nombre = re.sub(r"\s*\([^)]*\)\s*$", "", nombre)
        crudo = sin_md(cols[i_val])
        cabeza = re.split(r"\s+—\s+|;\s*", crudo, maxsplit=1)
        if " (" in cabeza[0]:
            jefe, resto = cabeza[0].split(" (", 1)
            cabeza = [jefe, "(" + resto + (". " + cabeza[1] if len(cabeza) > 1 else "")]
        delta = sin_md(cols[i_delta]) if (i_delta is not None and len(cols) > i_delta) else "—"
        señales.append({
            "clave": clave, "nombre": HUMANO.get(clave) or HUMANO_GEN2.get(etiqueta.strip()) or (nombre[0].upper() + nombre[1:]),
            "valor": cabeza[0].strip(),
            "cola": cabeza[1].strip() if len(cabeza) > 1 else "",
            "delta": delta, "quieto": delta in {"0", "="},
            "mueve": sin_md(cols[-1]),
        })
    quietos = sum(1 for s in señales if s["quieto"])
    movidos = len(señales) - quietos
    titulo_senal = ("la cadena de procedencia de Gen 2" if not arroba else
                    f"{movidos} de {len(señales)} se movieron desde el corte anterior"
                    if movidos > quietos else
                    f"{quietos} de {len(señales)} sin moverse desde el corte anterior")

    # ── el corredor: las celdas del sorteo, leídas del TSV ────────────────
    ids = [l.split("\t")[0] for l in
           open("forense/prereg-duelo-v2/marco-M-sorteado-v1_2.tsv", encoding="utf-8").read().splitlines()[1:]
           if l.strip() and not l.startswith("#")]
    sin_lmr = set(ind["celdas_sin_LMR"])
    dominio_nombre = {"TRA": "Trámite", "CIV": "Cívica", "DIN": "Dinero", "FAM": "Familia"}
    corredor = {}
    for i in ids:
        corredor.setdefault(i[:3], []).append({"id": i, "puntuable": i not in sin_lmr})

    # ── el corpus: crecimiento del manifiesto, derivado por git ───────────
    d0, d1 = date.fromisoformat(primero), date.fromisoformat(ultimo)
    pasos = 9
    curva = []
    for k in range(pasos):
        f = date.fromordinal(d0.toordinal() + round(k * (d1 - d0).days / (pasos - 1)))
        c = sh(f'git show $(git rev-list -1 --before="{f} 23:59" HEAD):data/manifiesto.yaml 2>/dev/null | grep -c "^- id: "')
        curva.append((f, int(c or 0)))

    cola = ind["cola_adquisicion_estados"]
    cola_orden = sorted(cola.items(), key=lambda kv: -kv[1])
    cola_total = sum(cola.values())

    # ── quién tiene la pelota: §5, agrupada por dueño ─────────────────────
    pelota = {}
    for r in tabla(md, marca_por_titulo(md, "bloqueador", "quién tiene")):
        c = list(r.values())
        txt = sin_md(c[1])
        txt = re.sub(r"^NUEVO\s*·\s*", "", txt)
        partes = re.split(r"(?<=[a-z\)\d])\.\s+", txt, maxsplit=1)
        def campo(*claves, pos=None):
            for k in claves:
                for h, v in r.items():
                    if k in h.lower():
                        return sin_md(v)
            return sin_md(c[pos]) if pos is not None and abs(pos) < len(c) else ""
        dueño = (campo("dueñ", "dueno", pos=2) or "sin dueño").split("/")[0].strip().lower()
        pelota.setdefault(dueño, []).append({
            "id": sin_md(c[0]), "titulo": partes[0].rstrip("."),
            "detalle": partes[1] if len(partes) > 1 else "",
            "cierre": campo("cierra", "cómo", "como", pos=-1),
            "desde": campo("desde", pos=None),
        })
    orden_dueño = ["mesa", "dirección", "ejecutor", "fuente", "proceso"]
    pelota_ord = [(d, pelota[d]) for d in orden_dueño if d in pelota] + \
                 [(d, v) for d, v in pelota.items() if d not in orden_dueño]

    # ── los días: hitos sellados ──────────────────────────────────────────
    def col(r, *nombres, pos=None):
        for n in nombres:
            for k, v in r.items():
                if n in k.lower():
                    return sin_md(v)
        vals = list(r.values())
        return sin_md(vals[pos]) if pos is not None and abs(pos) <= len(vals) else ""

    hitos = [{"n": col(r, "#", pos=0), "que": col(r, "hito", pos=1),
              "fecha": col(r, "fecha", "pr", "sello", pos=2), "dejo": col(r, "dejó", "dejo", pos=-1)}
             for r in tabla(md, marca_por_titulo(md, "hito"))]
    m_tit = re.match(r"#+\s*(.+)", marca_por_titulo(md, "hito") or "")
    titulo_hitos = sin_md(m_tit.group(1)) if m_tit else "Hitos sellados"
    curso = [{"que": col(r, "hito", pos=1), "acto": col(r, "acto", pos=2)}
             for r in tabla(md, marca_por_titulo(md, "en curso"))]

    # ── detalle técnico: las tablas del entregable, tal cual ──────────────
    import markdown as MD
    tecnico = ""
    for marca, titulo in (("## 2 ·", "Indicadores derivados, con su comando"),
                          ("## 4 ·", "Pipeline"),
                          ("## 7 ·", "Discrepancias entre el tablero y el canon"),
                          ("## 8 ·", "Bitácora")):
        try:
            cuerpo = md.split(marca, 1)[1].split("\n## ")[0]
            cuerpo = cuerpo.split("\n", 1)[1]
        except IndexError:
            continue
        h = MD.markdown(cuerpo, extensions=["tables", "fenced_code"])
        h = h.replace("<table>", '<div class="scroll"><table>').replace("</table>", "</table></div>")
        tecnico += f"<h3>{e(titulo)}</h3>{h}"

    # ── curva svg ─────────────────────────────────────────────────────────
    W, H = 900, 150
    mx = max(v for _, v in curva) or 1
    pts = [(round(i * W / (len(curva) - 1), 1), round(H - v / mx * (H - 14), 1)) for i, (_, v) in enumerate(curva)]
    linea = " ".join(f"{'M' if i == 0 else 'L'}{x},{y}" for i, (x, y) in enumerate(pts))
    area = linea + f" L{W},{H} L0,{H} Z"
    marcas = "".join(f'<circle cx="{x}" cy="{y}" r="3.5"/>' for x, y in pts)

    # ── html ──────────────────────────────────────────────────────────────
    if gen2:                       # Gen 2: una casilla por número activo del modelo
        sell = gen2["N_resultados_sellados"]
        act = gen2["N_resultados_activos"]
        pend = act - sell
        estados = ["dato"] * sell + ["falta"] * pend
        casillas = "".join(f'<i class="c {c}" style="--d:{k*3}ms"></i>' for k, c in enumerate(estados))
        lead = (f'De <span class="g">{act}</span> números que el modelo consume hoy, '
                f'<span class="g maiz">{sell}</span> tienen cadena de procedencia sellada '
                f'y <span class="g frijol">{pend}</span> siguen siendo GEN1.')
        leyenda_html = (f'<li><i class="i-dato"></i>con cadena GEN2 sellada <b>{sell}</b></li>'
                        f'<li><i class="i-falta"></i>dependencia legacy activa <b>{pend}</b></li>')
        nota_parcela = (f'Cada casilla es un resultado activo. La demanda derivada son '
                        f'<b>{gen2["N_corridas_requeridas"]}</b> corridas, de las que '
                        f'<b>{gen2["N_corridas_selladas"]}</b> están selladas. Los '
                        f'<b>{gen2["replays_legacy_sellados"]}</b> replays legacy no cuentan, por regla.')
    else:
        casillas = "".join(
            f'<i class="c {cls}" style="--d:{k*9}ms"></i>' for k, cls in enumerate(
                ["dato"] * con_dato + ["falta"] * sin_dato + ["fuera"] * fuera))
        lead = (f'De <span class="g">{canon}</span> reglas del modelo, '
                f'<span class="g maiz">{con_dato}</span> viven en el motor con dato medido '
                f'y <span class="g frijol">{sin_dato}</span> sigue esperando una fuente.')
        leyenda_html = (f'<li><i class="i-dato"></i>medida con microdato <b>{con_dato}</b></li>'
                        f'<li><i class="i-falta"></i>cargada sin dato <b>{sin_dato}</b></li>'
                        f'<li><i class="i-fuera"></i>aún fuera del motor <b>{fuera}</b></li>')
        nota_parcela = (f'Cada casilla es una regla del modelo de decisión. {perimetro} están en el '
                        f'perímetro falsable: el subconjunto que el programa se comprometió a poder refutar.')

    tarjetas = "".join(f"""
      <article class="s {'neutra' if s['delta'] == '—' else ('quieta' if s['quieto'] else 'viva')}">
        <p class="s-n">{e(s['nombre'])}</p>
        <p class="s-v{' chico' if not re.match(r'^[0-9]', s['valor']) else ''}">{e(s['valor'])}</p>
        {f'<p class="s-c">{e(s["cola"])}</p>' if s['cola'] else ''}
        {'' if s['delta'] == '—' else '<p class="s-d">' + ('sin cambio' if s['quieto'] else 'cambió ' + e(s['delta'])) + '</p>'}
        <p class="s-m"><b>Lo mueve</b> {e(s['mueve'])}</p>
      </article>""" for s in señales)

    plots = ""
    for dom in [d for d in ("TRA", "CIV", "DIN", "FAM") if d in corredor] + \
               [d for d in corredor if d not in ("TRA", "CIV", "DIN", "FAM")]:
        celdas = corredor[dom]
        listas = sum(1 for c in celdas if c["puntuable"])
        plots += f"""
        <div class="plot">
          <p class="plot-h">{e(dominio_nombre.get(dom, dom))} <b>{listas}<span>/{len(celdas)}</span></b></p>
          <div class="plot-g">{''.join(f'<i class="q {"ok" if c["puntuable"] else "no"}" title="{e(c["id"])}"></i>' for c in celdas)}</div>
        </div>"""

    barras = "".join(
        f'<div class="tramo t{k}" style="flex:{v}" title="{e(n)}: {v}"><span>{v}</span></div>'
        for k, (n, v) in enumerate(cola_orden))
    leyenda = "".join(
        f'<li><i class="t{k}"></i>{e(n.lower().replace("-", " "))} <b>{v}</b></li>'
        for k, (n, v) in enumerate(cola_orden))

    bloques = ""
    for dueño, items in pelota_ord:
        bloques += f"""
        <section class="due">
          <h3>{e(dueño)}<span>{len(items)}</span></h3>
          <ul>{''.join(f'<li><p class="b-t">{e(i["titulo"])}</p><p class="b-c">Se cierra: {e(i["cierre"])}</p></li>' for i in items)}</ul>
        </section>"""

    linea_t = "".join(f"""
      <li><span class="f">{e(h['fecha'])}</span>
          <p class="t">{e(h['que'])}</p>
          <p class="q">{e(h['dejo'])}</p></li>""" for h in hitos)

    corredor_abre = "" if not gen2 else "<!--"
    corredor_cierra = "" if not gen2 else "-->"
    hitos_abre = "" if hitos else "<!--"
    hitos_cierra = "" if hitos else "-->"
    doc = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tablero del programa · {e(sha)}</title>
<style>
:root{{
  --tierra:#131E1A; --surco:#1B2823; --borde:#2B3B34;
  --cal:#EFEBE0; --niebla:#94A59B;
  --maiz:#E4B25A; --frijol:#C56A46; --agua:#6FB3AE; --hoja:#8CA85C;
  --sans:"Helvetica Neue",Inter,Arial,system-ui,sans-serif;
  --serif:Charter,"Iowan Old Style",Georgia,serif;
  --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--tierra);color:var(--cal);font-family:var(--serif);
  font-size:17px;line-height:1.6;-webkit-font-smoothing:antialiased}}
.w{{max-width:980px;margin:0 auto;padding:0 26px}}
h2{{font-family:var(--sans);font-size:13.5px;font-weight:600;letter-spacing:.09em;
  text-transform:uppercase;color:var(--niebla);margin:0 0 20px;
  padding-bottom:9px;border-bottom:1px solid var(--borde)}}
b,strong{{font-weight:600}}
.num{{font-family:var(--sans);font-variant-numeric:tabular-nums;font-weight:600;letter-spacing:-.02em}}

/* portada */
.cab{{padding:64px 0 0}}
.marca{{font-family:var(--sans);font-size:12.5px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--niebla);margin:0 0 40px}}
.lead{{font-size:clamp(25px,3.6vw,38px);line-height:1.32;margin:0 0 26px;max-width:25ch;font-weight:400}}
.lead .g{{font-family:var(--sans);font-weight:600;font-size:1.22em;letter-spacing:-.03em;
  font-variant-numeric:tabular-nums}}
.lead .maiz{{color:var(--maiz)}} .lead .frijol{{color:var(--frijol)}}
.meta{{font-family:var(--sans);font-size:13px;color:var(--niebla);display:flex;flex-wrap:wrap;
  padding:22px 0 0;border-top:1px solid var(--borde);margin-top:34px}}
.meta span{{margin:0 28px 6px 0}}
.meta b{{color:var(--cal);font-variant-numeric:tabular-nums}}

section.blk{{padding:66px 0 0}}

/* parcela de reglas */
.parcela{{display:flex;flex-wrap:wrap;margin:36px 0 20px;max-width:690px}}
.c{{flex:none}}
.c{{width:17px;height:17px;margin:0 6px 6px 0;border-radius:2px;background:var(--borde)}}
.c.dato{{background:var(--maiz)}} .c.falta{{background:var(--frijol)}}
.c.fuera{{background:transparent;box-shadow:inset 0 0 0 1px var(--borde)}}
@media (prefers-reduced-motion:no-preference){{
  .parcela.germina .c{{opacity:0;transform:translateY(5px);animation:brota .5s ease-out var(--d) forwards}}
  @keyframes brota{{to{{opacity:1;transform:none}}}}
}}
.leyenda{{display:flex;flex-wrap:wrap;list-style:none;padding:0;margin:0;
  font-family:var(--sans);font-size:13.5px;color:var(--niebla)}}
.leyenda li{{display:flex;align-items:center;margin:0 30px 8px 0}}
.leyenda i{{width:11px;height:11px;border-radius:2px;flex:none;margin-right:9px}}
.leyenda b{{color:var(--cal);font-variant-numeric:tabular-nums;margin-left:7px}}
.i-dato{{background:var(--maiz)}} .i-falta{{background:var(--frijol)}}
.i-fuera{{box-shadow:inset 0 0 0 1px var(--borde)}}
.nota{{color:var(--niebla);font-size:15.5px;max-width:62ch;margin:22px 0 0}}

/* señal */
.rej{{display:grid;grid-template-columns:repeat(auto-fit,minmax(215px,1fr));grid-gap:14px;gap:14px}}
.s{{background:var(--surco);border-radius:6px;padding:18px 18px 16px;display:flex;flex-direction:column;
  border-top:3px solid var(--borde)}}
.s.quieta{{border-top-color:var(--frijol)}}
.s.neutra{{border-top-color:var(--agua)}}
.s.viva{{border-top-color:var(--hoja)}}
.s-n{{font-family:var(--sans);font-size:13.5px;color:var(--niebla);margin:0;line-height:1.35}}
.s-v{{font-family:var(--sans);font-size:38px;font-weight:600;letter-spacing:-.03em;margin:8px 0 0;
  font-variant-numeric:tabular-nums;line-height:1}}
.s-v.chico{{font-size:25px;letter-spacing:-.01em;line-height:1.15}}
.s-c{{font-size:13.5px;color:var(--niebla);margin:6px 0 0;line-height:1.4;
  overflow-wrap:anywhere;font-family:var(--sans)}}
.s-d{{font-family:var(--sans);font-size:12.5px;margin:12px 0 0;color:var(--frijol);font-weight:600}}
.s.viva .s-d{{color:var(--hoja)}}
.s-m{{font-size:13.5px;color:var(--niebla);margin:12px 0 0;padding-top:11px;
  border-top:1px solid var(--borde);line-height:1.45}}
.s-m b{{color:var(--cal);font-family:var(--sans);font-size:12px;letter-spacing:.05em;text-transform:uppercase;margin-right:5px}}

/* corredor */
.plots{{display:grid;grid-template-columns:repeat(auto-fit,minmax(195px,1fr));grid-gap:16px;gap:16px}}
.plot{{background:var(--surco);border-radius:6px;padding:17px 18px}}
.plot-h{{font-family:var(--sans);font-size:14px;color:var(--niebla);margin:0 0 14px;
  display:flex;justify-content:space-between;align-items:baseline}}
.plot-h b{{font-size:23px;color:var(--cal);font-variant-numeric:tabular-nums;letter-spacing:-.02em}}
.plot-h b span{{font-size:14px;color:var(--niebla);font-weight:400}}
.plot-g{{display:flex;flex-wrap:wrap}}
.q{{width:22px;height:22px;border-radius:3px;margin:0 5px 5px 0}}
.q.ok{{background:var(--agua)}}
.q.no{{box-shadow:inset 0 0 0 1.5px var(--borde)}}

/* corpus */
.curva{{width:100%;height:auto;display:block;margin:0 0 8px;overflow:visible}}
.curva path.a{{fill:var(--hoja);opacity:.14}}
.curva path.l{{fill:none;stroke:var(--hoja);stroke-width:2.2;stroke-linejoin:round}}
.curva circle{{fill:var(--tierra);stroke:var(--hoja);stroke-width:2}}
.ejes{{display:flex;justify-content:space-between;font-family:var(--sans);font-size:12.5px;
  color:var(--niebla);border-top:1px solid var(--borde);padding-top:9px}}
.barra{{display:flex;height:42px;margin:34px 0 16px}}
.tramo+.tramo{{margin-left:3px}}
.tramo{{border-radius:3px;display:flex;align-items:center;justify-content:center;
  font-family:var(--sans);font-size:13px;font-weight:600;color:var(--tierra);min-width:26px}}
.t0{{background:var(--hoja)}} .t1{{background:var(--maiz)}} .t2{{background:var(--frijol)}}
.t3{{background:var(--agua)}} .t4{{background:var(--niebla)}}
.leyenda i.t0{{background:var(--hoja)}} .leyenda i.t1{{background:var(--maiz)}}
.leyenda i.t2{{background:var(--frijol)}} .leyenda i.t3{{background:var(--agua)}}
.leyenda i.t4{{background:var(--niebla)}}

/* pelota */
.dues{{display:grid;grid-template-columns:repeat(auto-fit,minmax(285px,1fr));grid-gap:16px;gap:16px;align-items:start}}
.due{{background:var(--surco);border-radius:6px;padding:18px 20px 6px}}
.due h3{{font-family:var(--sans);font-size:14px;letter-spacing:.08em;text-transform:uppercase;
  margin:0 0 14px;display:flex;justify-content:space-between;align-items:center;color:var(--cal)}}
.due h3 span{{font-size:13px;color:var(--niebla);background:var(--tierra);border-radius:20px;
  padding:2px 10px;letter-spacing:0}}
.due ul{{list-style:none;padding:0;margin:0}}
.due li{{padding:13px 0;border-top:1px solid var(--borde)}}
.b-t{{margin:0;font-size:15.5px;line-height:1.45}}
.b-c{{margin:6px 0 0;font-size:13.5px;color:var(--niebla);font-family:var(--sans);line-height:1.45}}

/* tiempo */
.tl{{list-style:none;padding:0;margin:0;border-left:1px solid var(--borde)}}
.tl li{{position:relative;padding:0 0 26px 26px}}
.tl li::before{{content:"";position:absolute;left:-4.5px;top:9px;width:8px;height:8px;
  border-radius:50%;background:var(--maiz)}}
.tl .f{{font-family:var(--sans);font-size:12.5px;color:var(--maiz);letter-spacing:.05em}}
.tl .t{{margin:3px 0 0;font-size:16.5px;line-height:1.42}}
.tl .q{{margin:3px 0 0;font-size:14px;color:var(--niebla);width:auto;height:auto;box-shadow:none}}

/* fold técnico */
details{{margin:66px 0 0;border-top:1px solid var(--borde);padding-top:22px}}
summary{{cursor:pointer;font-family:var(--sans);font-size:13.5px;letter-spacing:.08em;
  text-transform:uppercase;color:var(--niebla)}}
summary:hover{{color:var(--cal)}}
details h3{{font-family:var(--sans);font-size:15px;margin:38px 0 10px;color:var(--maiz)}}
details table{{border-collapse:collapse;width:100%;font-size:13px;font-family:var(--sans)}}
details th,details td{{border:1px solid var(--borde);padding:7px 9px;text-align:left;vertical-align:top}}
details th{{color:var(--niebla);font-weight:600}}
details code{{font-family:var(--mono);font-size:12px;color:var(--agua)}}
details pre{{background:#0D1613;padding:14px;border-radius:5px;overflow-x:auto;font-size:12px}}
details pre code{{color:var(--niebla)}}
details p{{font-size:15px;max-width:72ch}}
details blockquote{{border-left:2px solid var(--borde);margin:0;padding-left:16px;color:var(--niebla)}}
.scroll{{overflow-x:auto;margin:12px 0}}

footer{{margin:70px 0 0;padding:22px 0 70px;border-top:1px solid var(--borde);
  font-size:14px;color:var(--niebla);max-width:70ch}}
footer code{{font-family:var(--mono);font-size:12.5px;color:var(--agua)}}
@media (max-width:560px){{
  .lead{{max-width:none}} .q{{width:18px;height:18px}}
}}
</style></head><body>
<div class="w">

<header class="cab">
  <p class="marca">Psicología del Mexicano Contemporáneo</p>
  <p class="lead">{lead}</p>
  <div class="parcela">{casillas}</div>
  <ul class="leyenda">{leyenda_html}</ul>
  <p class="nota">{nota_parcela}</p>
  <div class="meta">
    <span>Corte <b>{e(sha)}</b></span>
    <span><b>{e(ultimo)}</b></span>
    <span><b>{dias}</b> días desde el primer commit</span>
    <span><b>{dias_activos}</b> con trabajo</span>
    <span><b>{ind['manifiesto_ids']:,}</b> payloads en el corpus</span>
  </div>
</header>

<section class="blk">
  <h2>La señal — {titulo_senal}</h2>
  <div class="rej">{tarjetas}</div>
</section>

{corredor_abre}<section class="blk">
  <h2>El corredor: celdas listas para puntuar</h2>
  <div class="plots">{plots}</div>
  <p class="nota">Una celda puntúa cuando tiene las tres corridas: el modelo, el lenguaje y el árbitro
     sobre microdato. {ind['celdas_puntuables_LMR']} de {len(ids)} las tienen.</p>
</section>

<section class="blk">
  <h2>El corpus, día por día</h2>
  <svg class="curva" viewBox="0 0 {W} {H}" preserveAspectRatio="none" role="img"
       aria-label="Crecimiento del manifiesto de payloads">
    <path class="a" d="{area}"/><path class="l" d="{linea}"/>{marcas}
  </svg>
  <div class="ejes"><span>{curva[0][0]} · {curva[0][1]}</span><span>{curva[-1][0]} · {curva[-1][1]:,} payloads</span></div>
  <div class="barra">{barras}</div>
  <ul class="leyenda">{leyenda}</ul>
  <p class="nota">Las {cola_total} fuentes de la cola de adquisición, por su estado real.
     Ninguna se declara inexistente: se declara dónde se buscó.</p>
</section>

<section class="blk">
  <h2>Quién tiene la pelota</h2>
  <div class="dues">{bloques}</div>
</section>

{hitos_abre}<section class="blk">
  <h2>{e(titulo_hitos)}</h2>
  <ol class="tl">{linea_t}</ol>
  {'<p class="nota">En curso: ' + '; '.join(e(c['que']) + ' (' + e(c['acto']) + ')' for c in curso) + '.</p>' if curso else ''}
</section>{hitos_cierra}

<details>
  <summary>Detalle técnico — cada cifra con el comando que la produjo</summary>
  {tecnico}
</details>

<footer>
  <p>Vista generada por <code>tools/tablero_vista.py</code> desde
  <code>{e(ruta_md)}</code> y la salida <code>--json</code> de <code>tools/tablero_programa.py</code>.
  Ninguna cifra está escrita a mano en esta página: si algo aquí discrepa del tablero, el defecto
  está en el generador. El canon sigue siendo <code>canon/estado-programa-v1_10.md</code> y
  <code>canon/gobernanza-v1_15.md</code>.</p>
</footer>
</div>
<script>
// Único momento de movimiento de la página: la parcela germina al cargar.
// Va por clase para que, si el script no corre, las casillas se vean igual.
var p=document.querySelector('.parcela'); if(p) p.classList.add('germina');
</script>
</body></html>
"""
    open(destino, "w", encoding="utf-8").write(doc)
    print(f"escrito: {destino} · {len(doc):,} bytes · corte {sha} · {canon} reglas "
          f"({con_dato} con dato / {sin_dato} sin dato / {fuera} fuera) · "
          f"{len(señales)} señales ({quietos} quietas) · {len(ids)} celdas · "
          f"{len(hitos)} hitos · {sum(len(v) for _, v in pelota_ord)} bloqueadores en {len(pelota_ord)} dueños")


if __name__ == "__main__":
    main()
