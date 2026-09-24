#!/usr/bin/env python3
"""u0busca: busca reactivos en los inventarios del repo (mismo cargador que
tools/busca_reactivos.py) y RESUELVE cada acierto a ids de data/manifiesto.yaml:
payload (dato) y documento fuente del texto (FD/diccionario), con sha256.

Uso:
  u0busca.py -q "deprimid" -q "triste|abatid" [--encuesta ensanut] [--ola 2024] [--limite 40]
  Cada -q es una consulta independiente; '|' separa sinónimos (OR) dentro de la consulta.
  Plegado: minúsculas y sin acentos, substring sobre texto_reactivo, variable_id y contexto.
Salida: TSV por consulta + banner A.13 (identidades examinadas y con texto).
"""
import argparse, importlib.util, sys, yaml
REPO = str(__import__("pathlib").Path(__file__).resolve().parents[4])
spec = importlib.util.spec_from_file_location("br", REPO + "/tools/busca_reactivos.py")
br = importlib.util.module_from_spec(spec); spec.loader.exec_module(br)
RESERVA_TXT = ("enoe_2026", "enoe2026", "envipe2026", "envipe_2026", "enco_", "enco20", "enco/")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-q", action="append", required=True)
    ap.add_argument("--encuesta"); ap.add_argument("--ola")
    ap.add_argument("--limite", type=int, default=40)
    ap.add_argument("--solo-con-texto", action="store_true", default=True)
    a = ap.parse_args()
    M = yaml.safe_load(open(REPO + "/data/manifiesto.yaml", encoding="utf-8"))
    por_archivo = {e["archivo"]: e for e in M if isinstance(e, dict) and e.get("archivo")}
    fuentes = sorted(set(br.TABLAS) - {"contexto_v1_0"})
    filas = []; vistos = set(); nrev = ntex = 0
    for f in fuentes:
        for n, row in enumerate(br.lee_filas(br.TABLAS[f]), start=1):
            ident = (row["payload_id"], row["archivo_miembro"], (row["variable_id"] or "").lower())
            if ident in vistos: continue
            vistos.add(ident); nrev += 1
            if (row.get("texto_reactivo") or "").strip(): ntex += 1
            filas.append((f, n, row))
    print(f"# u0busca A.13: {len(fuentes)} tablas ({','.join(fuentes)}); {nrev} identidades revisadas, {ntex} con texto")
    enc = br.plegar(a.encuesta) if a.encuesta else None
    ola = br.plegar(a.ola) if a.ola else None
    cols = ["consulta","tabla_inv","instrumento","ola","payload_archivo","payload_id","payload_sha256","payload_raiz","reserva","archivo_miembro","variable_id","texto_reactivo","texto_tipo","fuente_texto","fuente_id","fuente_sha256","referencia_fuente"]
    for q in a.q:
        terms = [br.plegar(t.strip()) for t in q.split("|") if t.strip()]
        hits = []
        for f, n, row in filas:
            if enc and enc not in br.plegar(row["instrumento"]): continue
            if ola and ola not in br.plegar(row["ola"]) and ola not in br.plegar(row["payload_id"]): continue
            tx = row.get("texto_reactivo") or ""
            blob = br.plegar(tx) + " " + br.plegar(row["variable_id"] or "") + " " + br.plegar(row.get("contexto_busqueda") or "")
            if any(t in blob for t in terms):
                if a.solo_con_texto and not tx.strip(): continue
                hits.append((f, n, row))
        print(f"# consulta {q!r}: {len(hits)} aciertos con texto; mostrando {min(len(hits), a.limite)}")
        print("\t".join(cols))
        for f, n, row in hits[: a.limite]:
            tx = row.get("texto_reactivo") or ""
            pe = por_archivo.get(row["payload_id"], {})
            fe = por_archivo.get(row.get("fuente_texto") or "", {})
            res = pe.get("estado_reserva", "")
            low = (row["payload_id"] + " " + (pe.get("id") or "")).lower()
            if any(t in low for t in RESERVA_TXT): res = (res + " ALERTA-RESERVA-ENCARGO").strip()
            vals = [q, f"{f}:{n}", row["instrumento"], row["ola"], row["payload_id"], pe.get("id", "SIN-ID-MANIFIESTO"),
                    pe.get("sha256", ""), pe.get("raiz", "data_raw") if pe else "", res, row["archivo_miembro"], row["variable_id"],
                    (tx or "").replace("\t", " ").replace("\n", " "), row.get("texto_tipo", ""), row.get("fuente_texto", ""),
                    fe.get("id", ""), fe.get("sha256", ""), row.get("referencia_fuente", "")]
            print("\t".join(str(v) for v in vals))

if __name__ == "__main__":
    main()
