#!/usr/bin/env python3
"""Arnés del subcomando `tests/manifiesto.py --descarga`.

ACTO GEN2-NUBE-PILOTO-1, pieza 1 (21/sep/2026). D-22: «congelado» exige que
el punto de entrada haya corrido al menos sobre datos sintéticos; un medidor
cuyas pruebas sólo ejercitan guardias y constantes no es un COMMIT-1. Por eso
estas pruebas NO mockean urllib: levantan un `http.server` de la stdlib en
127.0.0.1 y corren el punto de entrada real de punta a punta sobre cuatro
escenarios -- archivo bueno · sha256 discordante · redirección a otro host ·
404 -- más el caso de REGLA (los nueve ids `banxico_sie_*`, servlets `.do`,
salen NO-ACCESIBLE sin tocar la red) y las dos ramas de `raiz`.

No hay precedente de arnés HTTP en `tests/` ni en `tools/`: censo del
21/sep/2026 sobre los 367 archivos .py de los dos árboles, 0 coincidencias de
`http.server|HTTPServer|socketserver`. Se escribe aquí por primera vez.

Ninguna prueba de este archivo toca la red externa ni `data/raw` del repo:
todo corre contra un `--root` temporal.
"""
import hashlib
import http.server
import os
import subprocess
import sys
import tempfile
import threading
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFIESTO_CLI = os.path.join(RAIZ, "tests", "manifiesto.py")

sys.path.insert(0, os.path.join(RAIZ, "tests"))
import manifiesto as M  # noqa: E402

CONTENIDO = b"col_a,col_b\n1,2\n" * 64
SHA_BUENO = hashlib.sha256(CONTENIDO).hexdigest()
SHA_FALSO = "0" * 64


class _Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a):  # silencio: el arnés no ensucia la salida
        pass

    def do_GET(self):
        if self.path == "/bueno.zip" or self.path == "/discordante.zip":
            self.send_response(200)
            self.send_header("Content-Length", str(len(CONTENIDO)))
            self.end_headers()
            self.wfile.write(CONTENIDO)
        elif self.path == "/redirige.zip":
            # Redirección a OTRO host (firma 1): el descargador debe parar y
            # reportar el host final exacto.
            self.send_response(302)
            self.send_header("Location", "http://otro-host.invalid:1/bueno.zip")
            self.end_headers()
        elif self.path == "/redirige-mismo-host.zip":
            self.send_response(302)
            self.send_header("Location", "/bueno.zip")
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()


def _escribe_manifiesto(root, entradas):
    import yaml
    os.makedirs(os.path.join(root, "data"), exist_ok=True)
    with open(os.path.join(root, "data", "manifiesto.yaml"), "w",
              encoding="utf-8") as f:
        f.write("# manifiesto sintético del arnés -- ausente = data_raw\n")
        f.write(yaml.safe_dump(entradas, allow_unicode=True, sort_keys=False))
    os.makedirs(os.path.join(root, "data", "raw"), exist_ok=True)


def _corre(root, ids, extra=()):
    cmd = [sys.executable, MANIFIESTO_CLI, "--descarga", "--root", root,
           "--timeout", "20", *extra]
    for i in ids:
        cmd += ["--id", i]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


class ArnesHTTPLocal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
        cls.puerto = cls.srv.server_address[1]
        cls.hilo = threading.Thread(target=cls.srv.serve_forever, daemon=True)
        cls.hilo.start()
        cls.base = f"http://127.0.0.1:{cls.puerto}"

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()
        cls.srv.server_close()

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="descarga-arnes-")
        self.destino = os.path.join(self.tmp, "data", "raw")

    def _entrada(self, id_, ruta, sha, **kw):
        e = {"id": id_, "archivo": f"{id_}.zip", "sha256": sha,
             "tamano_bytes": len(CONTENIDO),
             "url_origen": f"{self.base}{ruta}"}
        e.update(kw)
        return e

    # ── escenario 1 · archivo bueno ────────────────────────────────────
    def test_archivo_bueno_entra_a_la_raiz(self):
        _escribe_manifiesto(self.tmp, [self._entrada("bueno", "/bueno.zip", SHA_BUENO)])
        rc, out = _corre(self.tmp, ["bueno"])
        self.assertEqual(rc, 0, out)
        self.assertIn("DESCARGADO-AHORA", out)
        ruta = os.path.join(self.destino, "bueno.zip")
        self.assertTrue(os.path.exists(ruta), out)
        with open(ruta, "rb") as f:
            self.assertEqual(hashlib.sha256(f.read()).hexdigest(), SHA_BUENO)
        # Segunda corrida: ya está y coincide -> no se vuelve a bajar.
        rc2, out2 = _corre(self.tmp, ["bueno"])
        self.assertEqual(rc2, 0, out2)
        self.assertIn("EXISTE-SATISFACE", out2)

    # ── escenario 2 · sha256 discordante ───────────────────────────────
    def test_sha256_discordante_no_entra_a_la_raiz(self):
        _escribe_manifiesto(self.tmp,
                            [self._entrada("malo", "/discordante.zip", SHA_FALSO)])
        rc, out = _corre(self.tmp, ["malo"])
        self.assertNotEqual(rc, 0, out)
        self.assertIn("EXISTE-NO-SATISFACE", out)
        self.assertIn("sha256 DISCORDANTE", out)
        self.assertFalse(os.path.exists(os.path.join(self.destino, "malo.zip")), out)
        # Y no queda basura: ni el temporal ni un parcial.
        self.assertEqual(sorted(os.listdir(self.destino)), [], out)

    # ── escenario 3 · redirección a otro host ──────────────────────────
    def test_redireccion_a_otro_host_para_y_reporta_el_host_exacto(self):
        _escribe_manifiesto(self.tmp,
                            [self._entrada("redir", "/redirige.zip", SHA_BUENO)])
        rc, out = _corre(self.tmp, ["redir"])
        self.assertNotEqual(rc, 0, out)
        self.assertIn("PARO-REDIRECCION", out)
        self.assertIn("otro-host.invalid:1", out)  # host final exacto, a la vista
        self.assertFalse(os.path.exists(os.path.join(self.destino, "redir.zip")), out)

    def test_redireccion_al_mismo_host_se_sigue(self):
        _escribe_manifiesto(
            self.tmp, [self._entrada("mismo", "/redirige-mismo-host.zip", SHA_BUENO)])
        rc, out = _corre(self.tmp, ["mismo"])
        self.assertEqual(rc, 0, out)
        self.assertIn("DESCARGADO-AHORA", out)

    # ── escenario 4 · 404 ──────────────────────────────────────────────
    def test_404_es_no_accesible_y_no_deja_archivo(self):
        _escribe_manifiesto(self.tmp,
                            [self._entrada("ausente", "/no-existe.zip", SHA_BUENO)])
        rc, out = _corre(self.tmp, ["ausente"])
        self.assertNotEqual(rc, 0, out)
        self.assertIn("NO-ACCESIBLE", out)
        self.assertIn("HTTP 404", out)
        self.assertEqual(sorted(os.listdir(self.destino)), [], out)

    # ── guardia de reserva (E.6) ───────────────────────────────────────
    def test_estado_reserva_se_niega(self):
        _escribe_manifiesto(self.tmp, [
            self._entrada("reservado", "/bueno.zip", SHA_BUENO,
                          estado_reserva="RESERVADO")])
        rc, out = _corre(self.tmp, ["reservado"])
        self.assertNotEqual(rc, 0, out)
        self.assertIn("estado_reserva", out)
        self.assertEqual(sorted(os.listdir(self.destino)), [], out)

    def test_id_inexistente_es_no_encontrado(self):
        _escribe_manifiesto(self.tmp, [self._entrada("bueno", "/bueno.zip", SHA_BUENO)])
        rc, out = _corre(self.tmp, ["no_esta_aqui"])
        self.assertNotEqual(rc, 0, out)
        self.assertIn("NO-ENCONTRADO", out)


class ReglaDeClasificacion(unittest.TestCase):
    """Se clasifica ANTES de tocar la red. Ninguna prueba de esta clase abre
    un socket: `clasifica_url` es una función pura."""

    def test_extension_de_archivo_es_descargable(self):
        for u in ("https://www.inegi.org.mx/a/b/enif_2024_bd_csv.zip",
                  "https://www.inegi.org.mx/x.pdf",
                  "https://www.inegi.org.mx/x.xlsx"):
            self.assertEqual(M.clasifica_url(u)[0], "DESCARGABLE", u)

    def test_servlet_do_no_es_accesible(self):
        clase, motivo = M.clasifica_url(
            "https://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction"
            ".do?sector=21&accion=consultarCuadro&idCuadro=CF881&locale=es")
        self.assertEqual(clase, "NO-ACCESIBLE")
        self.assertIn("query string", motivo)

    def test_los_nueve_banxico_sie_del_manifiesto_real_salen_no_accesible(self):
        """Caso de REGLA que mesa nombró. El encargo lo declaró como «22 ids
        `banxico_sie_*`, nueve con url_origen que termina en .do». Censo del
        21/sep/2026 contra data/manifiesto.yaml (1 629 entradas): los ids
        `banxico_sie_*` son NUEVE, no 22 (`banxico*` son 25), y ninguna de sus
        URLs *termina* en `.do` -- lo que termina en `.do` es la RUTA, seguida
        de query string. La cifra del encargo queda corregida; el caso de
        prueba se conserva, que es lo que mesa firmó."""
        _, entradas = M.leer_manifiesto(os.path.join(RAIZ, "data", "manifiesto.yaml"))
        sie = [e for e in entradas if str(e.get("id", "")).startswith("banxico_sie_")]
        self.assertEqual(len(sie), 9, [e.get("id") for e in sie])
        for e in sie:
            clase, motivo = M.clasifica_url(e.get("url_origen"))
            self.assertEqual(clase, "NO-ACCESIBLE", (e["id"], motivo))

    def test_url_no_http_deja_el_valor_crudo_a_la_vista(self):
        clase, motivo = M.clasifica_url("ftp://ejemplo/x.zip")
        self.assertEqual(clase, "NO-ACCESIBLE")
        self.assertIn("ftp://ejemplo/x.zip", motivo)
        clase, motivo = M.clasifica_url(None)
        self.assertEqual(clase, "NO-ACCESIBLE")
        self.assertIn("None", motivo)

    def test_pagina_sin_extension_no_es_accesible(self):
        clase, motivo = M.clasifica_url("https://www.inegi.org.mx/programas/encuci/2020/")
        self.assertEqual(clase, "NO-ACCESIBLE")
        self.assertIn("catálogo", motivo)


class ResolucionDeRaiz(unittest.TestCase):
    """`raiz` ausente y `raiz` presente-con-valor-nulo son DOS hechos, y el
    código declara cuál aplicó. Prohibido `raiz or 'data_raw'` en silencio."""

    def test_clave_ausente(self):
        nombre, proc = M.resuelve_raiz_declarada({"id": "x"})
        self.assertEqual(nombre, M.RAIZ_INTEGRADA)
        self.assertIn("AUSENTE", proc)

    def test_clave_presente_con_valor_nulo(self):
        nombre, proc = M.resuelve_raiz_declarada({"id": "x", "raiz": None})
        self.assertEqual(nombre, M.RAIZ_INTEGRADA)
        self.assertIn("PRESENTE con valor nulo", proc)

    def test_clave_presente_con_valor(self):
        nombre, proc = M.resuelve_raiz_declarada({"id": "x", "raiz": "descargas_mx"})
        self.assertEqual(nombre, "descargas_mx")
        self.assertIn("PRESENTE con valor", proc)


class SinSegundaPuerta(unittest.TestCase):
    def test_el_subcomando_no_acepta_una_url_suelta(self):
        """Firma de mesa 8: descarga SOLO por id del manifiesto."""
        p = subprocess.run(
            [sys.executable, MANIFIESTO_CLI, "--descarga",
             "https://www.inegi.org.mx/x.zip"],
            capture_output=True, text=True)
        self.assertNotEqual(p.returncode, 0)
        p2 = subprocess.run([sys.executable, MANIFIESTO_CLI, "--descarga",
                             "--url-origen", "https://www.inegi.org.mx/x.zip"],
                            capture_output=True, text=True)
        self.assertNotEqual(p2.returncode, 0, p2.stdout + p2.stderr)
        self.assertIn("exige al menos un --id", p2.stdout + p2.stderr)

    def test_no_escribe_en_el_manifiesto(self):
        """Firma de mesa 2: data/manifiesto.yaml no se toca."""
        import inspect
        fuente = inspect.getsource(M.cmd_descarga) + inspect.getsource(
            M.descarga_verificada)
        for prohibido in ("escribir_manifiesto", "manifiesto-staging"):
            self.assertNotIn(prohibido, fuente)


if __name__ == "__main__":
    unittest.main(verbosity=2)
