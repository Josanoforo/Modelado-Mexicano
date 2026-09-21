#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/test_descarga_manifiesto.py -- arnés de `tests/manifiesto.py --descarga`.

ACTO GEN2-NUBE-PILOTO-1, pieza 1. D-22: «congelado» exige que el punto de
entrada haya corrido al menos sobre datos sintéticos; un medidor cuyas pruebas
solo ejercitan guardias y constantes no es un COMMIT-1. Por eso los cuatro
primeros escenarios levantan un servidor HTTP local de la stdlib y corren el
subcomando ENTERO por subproceso, con su propio `--root` y su propio
manifiesto -- no llaman a las funciones internas.

No había precedente que reutilizar: ningún archivo de `tests/` ni `tools/`
usaba `http.server`/`HTTPServer`/`socketserver` al redactar esto (universo: los
dos árboles completos, 0 coincidencias).

Escenarios de red (servidor local, nunca sale de 127.0.0.1):
  1 · archivo bueno           -> DESCARGADO-AHORA, el payload queda en la raíz
  2 · sha256 discordante      -> SHA-DISCORDANTE, el payload NO entra a la raíz
  3 · redirección a otro host -> REDIRECCION-A-OTRO-HOST, host exacto reportado
  4 · 404                     -> NO-OBTENIDO (A.5), con receta manual

Casos de regla, sin tocar la red:
  5 · los nueve ids `banxico_sie_*` del manifiesto real salen NO-ACCESIBLE
  6 · las cuatro entradas con `estado_reserva` salen RESERVADO (E.6)
  7 · `enif_2024_enif_2024_bd_csv` NO es rechazado por la guardia (firma 4)
  8 · `raiz` ausente / nula / declarada se resuelven sin colapsar
  9 · el subcomando no expone ningún parámetro de URL (firma 8)
"""
from __future__ import annotations

import hashlib
import http.server
import io
import os
import subprocess
import sys
import tempfile
import threading
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFIESTO_PY = os.path.join(ROOT, "tests", "manifiesto.py")
MANIFIESTO_REAL = os.path.join(ROOT, "data", "manifiesto.yaml")

sys.path.insert(0, os.path.join(ROOT, "tests"))
import manifiesto as M  # noqa: E402

FALLOS = []
PASOS = []


def check(nombre, cond, detalle=""):
    (PASOS if cond else FALLOS).append(f"{nombre}: {detalle}")
    print(("PASS " if cond else "FAIL ") + nombre + (f" -- {detalle}" if detalle else ""))


# --------------------------------------------------------------------------
# Servidor local
# --------------------------------------------------------------------------
CONTENIDO_BUENO = b"col_a,col_b\n1,2\n" * 64
SHA_BUENO = hashlib.sha256(CONTENIDO_BUENO).hexdigest()


class _Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a):  # silencio
        pass

    def do_GET(self):
        if self.path == "/bueno.csv":
            self.send_response(200)
            self.send_header("Content-Length", str(len(CONTENIDO_BUENO)))
            self.end_headers()
            self.wfile.write(CONTENIDO_BUENO)
        elif self.path == "/otro_contenido.csv":
            cuerpo = "esto no es lo que el manifiesto selló\n".encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Length", str(len(cuerpo)))
            self.end_headers()
            self.wfile.write(cuerpo)
        elif self.path == "/redirige.csv":
            self.send_response(302)
            self.send_header("Location",
                             "https://cdn-espejo.example.org/enif_2024_bd_csv.zip")
            self.end_headers()
        else:
            self.send_error(404, "no existe")


def arranca_servidor():
    srv = http.server.HTTPServer(("127.0.0.1", 0), _Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, f"http://127.0.0.1:{srv.server_address[1]}"


def raiz_temporal(entradas):
    tmp = tempfile.mkdtemp(prefix="descarga-arnes-")
    os.makedirs(os.path.join(tmp, "data", "raw"))
    with io.open(os.path.join(tmp, "data", "manifiesto.yaml"), "w",
                 encoding="utf-8") as f:
        f.write("# manifiesto sintético del arnés -- no es el del repo\n")
        yaml.safe_dump(entradas, f, allow_unicode=True, sort_keys=False)
    return tmp


def corre(tmp, *ids, extra=()):
    cmd = [sys.executable, MANIFIESTO_PY, "--descarga", "--root", tmp,
           "--intentos", "1", "--tiempo-espera", "10"]
    for i in ids:
        cmd += ["--id", i]
    cmd += list(extra)
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def main():
    srv, base = arranca_servidor()
    try:
        entradas = [
            {"id": "sint_bueno", "archivo": "sint_bueno.csv",
             "url_origen": f"{base}/bueno.csv", "sha256": SHA_BUENO,
             "tamano_bytes": len(CONTENIDO_BUENO), "usado_para": "arnés"},
            {"id": "sint_discordante", "archivo": "sint_discordante.csv",
             "url_origen": f"{base}/otro_contenido.csv", "sha256": SHA_BUENO,
             "tamano_bytes": len(CONTENIDO_BUENO), "usado_para": "arnés"},
            {"id": "sint_redirige", "archivo": "sint_redirige.csv",
             "url_origen": f"{base}/redirige.csv", "sha256": SHA_BUENO,
             "tamano_bytes": len(CONTENIDO_BUENO), "usado_para": "arnés"},
            {"id": "sint_404", "archivo": "sint_404.csv",
             "url_origen": f"{base}/no_existe.csv", "sha256": SHA_BUENO,
             "tamano_bytes": len(CONTENIDO_BUENO), "usado_para": "arnés"},
            {"id": "sint_reservado", "archivo": "sint_reservado.csv",
             "url_origen": f"{base}/bueno.csv", "sha256": SHA_BUENO,
             "tamano_bytes": len(CONTENIDO_BUENO),
             "estado_reserva": "RESERVADA-NO-ABIERTA-NO-INDEXAR-L",
             "usado_para": "arnés"},
        ]
        tmp = raiz_temporal(entradas)

        # 1 · archivo bueno, de punta a punta
        rc, out = corre(tmp, "sint_bueno")
        destino = os.path.join(tmp, "data", "raw", "sint_bueno.csv")
        check("1 · archivo bueno -> DESCARGADO-AHORA",
              rc == 0 and "DESCARGADO-AHORA" in out, f"rc={rc}")
        check("1 · el payload quedó en la raíz con el sha256 del manifiesto",
              os.path.exists(destino) and M.sha256_de(destino) == SHA_BUENO)
        check("1 · la raíz ausente se resolvió explícito a data_raw",
              "AUSENTE -> data_raw" in out)
        # segunda corrida: ya está -> no se vuelve a bajar
        rc2, out2 = corre(tmp, "sint_bueno")
        check("1 · segunda corrida -> EXISTE-SATISFACE (no re-descarga)",
              rc2 == 0 and "EXISTE-SATISFACE" in out2, f"rc={rc2}")

        # 2 · sha256 discordante
        rc, out = corre(tmp, "sint_discordante")
        d2 = os.path.join(tmp, "data", "raw", "sint_discordante.csv")
        check("2 · sha discordante -> SHA-DISCORDANTE", rc == 1 and "SHA-DISCORDANTE" in out,
              f"rc={rc}")
        check("2 · el payload NO entró a la raíz", not os.path.exists(d2))
        check("2 · el temporal queda para inspección",
              os.path.exists(d2 + ".parcial"))

        # 3 · redirección a otro host
        rc, out = corre(tmp, "sint_redirige")
        check("3 · redirección -> REDIRECCION-A-OTRO-HOST",
              rc == 1 and "REDIRECCION-A-OTRO-HOST" in out, f"rc={rc}")
        check("3 · reporta el host final exacto",
              "cdn-espejo.example.org" in out)
        check("3 · no dejó nada en la raíz",
              not os.path.exists(os.path.join(tmp, "data", "raw", "sint_redirige.csv")))

        # 4 · 404
        rc, out = corre(tmp, "sint_404")
        check("4 · 404 -> NO-OBTENIDO", rc == 1 and "NO-OBTENIDO" in out, f"rc={rc}")
        check("4 · el fallo se declara del agente, con receta manual (A.5)",
              "NO OBTENIDO POR ESTE AGENTE EN 1 INTENTO(S)" in out
              and "receta manual de un minuto" in out)

        # 6 · guardia E.6 sobre la entrada reservada sintética
        rc, out = corre(tmp, "sint_reservado")
        check("6 · estado_reserva -> RESERVADO, sin tocar la red",
              rc == 1 and "RESERVADO" in out, f"rc={rc}")

        # ---- casos de regla, contra el manifiesto REAL, sin red ------------
        _cab, reales = M.leer_manifiesto(MANIFIESTO_REAL)
        by = {e.get("id"): e for e in reales}

        # 5 · los ids banxico_sie_*
        sie = [e for e in reales if str(e.get("id", "")).startswith("banxico_sie_")]
        clases = {e["id"]: M.clasifica_url_origen(e.get("url_origen"))[0] for e in sie}
        check("5 · universo banxico_sie_* examinado (A.13)", len(sie) == 9,
              f"{len(sie)} ids (el encargo declaraba 22; medido: 9)")
        check("5 · los nueve salen NO-ACCESIBLE sin tocar la red",
              sie and all(v == "NO-ACCESIBLE" for v in clases.values()),
              f"{sorted(set(clases.values()))}")
        # La premisa que cae: ninguno "termina en .do". La regla se decide
        # sobre urlsplit().path, no sobre la URL cruda.
        terminan_en_do = [e["id"] for e in sie
                          if str(e.get("url_origen", "")).endswith(".do")]
        check("5 · ninguno termina literalmente en '.do' (premisa corregida)",
              len(terminan_en_do) == 0, f"{len(terminan_en_do)} de {len(sie)}")

        # 6-bis · las cuatro entradas reservadas reales
        reservadas = [e["id"] for e in reales if e.get("estado_reserva")]
        check("6 · universo de entradas con estado_reserva (A.13)",
              len(reservadas) == 4, f"{sorted(reservadas)}")

        # 7 · el piloto NO es rechazado por la guardia (firma 4)
        piloto = by.get("enif_2024_enif_2024_bd_csv")
        check("7 · el id del piloto existe en el manifiesto", piloto is not None)
        check("7 · el piloto NO tiene estado_reserva: el descargador no lo bloquea",
              piloto is not None and not piloto.get("estado_reserva"))
        check("7 · el piloto clasifica DESCARGABLE",
              piloto is not None
              and M.clasifica_url_origen(piloto.get("url_origen"))[0] == "DESCARGABLE")

        # 8 · resolución explícita de `raiz`
        check("8 · raiz ausente -> data_raw, declarado",
              M.resolver_raiz_declarada({})[0] == M.RAIZ_INTEGRADA
              and "AUSENTE" in M.resolver_raiz_declarada({})[1])
        check("8 · raiz presente-con-valor-nulo -> data_raw, declarado aparte",
              M.resolver_raiz_declarada({"raiz": None})[0] == M.RAIZ_INTEGRADA
              and "NULO" in M.resolver_raiz_declarada({"raiz": None})[1])
        check("8 · raiz declarada se respeta",
              M.resolver_raiz_declarada({"raiz": "descargas_mx"})
              == ("descargas_mx", "DECLARADA"))

        # 9 · no hay puerta por URL (firma 8)
        ayuda = subprocess.run([sys.executable, MANIFIESTO_PY, "--help"],
                               capture_output=True, text=True).stdout
        rc, out = corre(tmp)  # sin --id
        check("9 · --descarga sin --id es error explícito, no descarga nada",
              rc == 1 and "NO acepta una URL suelta" in out, f"rc={rc}")
        check("9 · la ayuda de --descarga dice que no acepta una URL suelta",
              "NO acepta una URL suelta" in " ".join(ayuda.split()))
        fuente = io.open(MANIFIESTO_PY, encoding="utf-8").read()
        check("9 · cmd_descarga no lee ningún parámetro de URL del argparse",
              "a.url" not in fuente.split("def cmd_descarga")[1])

    finally:
        srv.shutdown()

    print()
    print(f"RESUMEN: {len(PASOS)} PASS · {len(FALLOS)} FAIL")
    if FALLOS:
        for f in FALLOS:
            print("  FAIL " + f)
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
