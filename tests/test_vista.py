"""ACTO GEN2-TUBERIA-VISTA-NORMALIZADA-2/-3 -- tools/vista.py.

`join_resultado` reconstruye `tolerancia`/`funciones_dependencia`/
`fuente_replay` (COMMIT-A) y `camino_linaje` (COMMIT-B) para una fila de
`resultados.tsv` que ya no los trae: la regla es "el propio valor manda si
esta presente; si no, se busca (corridas.tsv para los tres primeros,
`_lee_oferta`+`_propaga_envuelto` para `camino_linaje`); si tampoco se
encuentra, un sentinel declarado", nunca un `KeyError`.

`JoinResultado`/`CorridasPorId` son sinteticos, sin tocar `data/corrida0/`
ni disparar el calculo caro de `camino_linaje` (una fila sin `origen`
declarado -- el formato de fixture de estas pruebas, previo a COMMIT-B --
nunca lo dispara; `origen=DEMANDA` es el patron mecanico gratis;
`origen=OFERTA` con `linajes={}` explicito prueba el sentinel sin tocar
disco). `PruebaCaminoLinajeBajoDemanda` es la excepcion: corre CONTRA el
repo real (`_lee_oferta`, ~70s medido 24/sep/2026 sobre ~310 `CALC-*/`) y
por eso es HUERFANA a proposito (D-21: `ci_guardias.py --ejecuta-huerfanos`
la corre, `tests/check.py --rapido` no)."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import vista  # noqa: E402


class JoinResultado(unittest.TestCase):
    def test_campo_ausente_se_completa_desde_la_corrida(self):
        fila = {"resultado_id": "RES-1", "corrida_id": "CORR-1", "valor": "1"}
        corridas = {"CORR-1": {"corrida_id": "CORR-1", "tolerancia": '{"abs": 0.01}',
                                "funciones_dependencia": "f(x)", "fuente_replay": "NO-CORRIDA"}}
        j = vista.join_resultado(fila, corridas)
        self.assertEqual(j["tolerancia"], '{"abs": 0.01}')
        self.assertEqual(j["funciones_dependencia"], "f(x)")
        self.assertEqual(j["fuente_replay"], "NO-CORRIDA")
        # la fila original no se muta
        self.assertNotIn("tolerancia", fila)

    def test_campo_propio_manda_sobre_el_de_la_corrida(self):
        """Formato previo a COMMIT-A, o un fixture sintetico que ya lo
        declara: el valor de la propia fila no se pisa."""
        fila = {"resultado_id": "RES-1", "corrida_id": "CORR-1",
                "tolerancia": "PENDIENTE"}
        corridas = {"CORR-1": {"corrida_id": "CORR-1", "tolerancia": '{"abs": 0.01}'}}
        j = vista.join_resultado(fila, corridas)
        self.assertEqual(j["tolerancia"], "PENDIENTE")

    def test_corrida_ausente_no_revienta(self):
        fila = {"resultado_id": "RES-1", "corrida_id": "CORR-DESCONOCIDA"}
        j = vista.join_resultado(fila, {})
        self.assertEqual(j["tolerancia"], "SIN-CORRIDA-EN-VISTA")
        self.assertEqual(j["funciones_dependencia"], "SIN-CORRIDA-EN-VISTA")
        self.assertEqual(j["fuente_replay"], "SIN-CORRIDA-EN-VISTA")

    def test_corridas_por_id_archivo_ausente_da_diccionario_vacio(self):
        self.assertEqual(vista.corridas_por_id(Path("/no/existe/corridas.tsv")), {})

    def test_fila_sin_origen_no_agrega_camino_linaje(self):
        """Fixture previo a COMMIT-B (sin `origen` declarado, como las tres
        pruebas de arriba): `camino_linaje` no se deriva -- no dispara el
        cache real (`vista._linajes_cache`) por un campo que nadie pidio."""
        fila = {"resultado_id": "RES-1", "corrida_id": "CORR-1"}
        j = vista.join_resultado(fila, {})
        self.assertNotIn("camino_linaje", j)


class CaminoLinajeSintetico(unittest.TestCase):
    """COMMIT-B, sin tocar `data/corrida0/`: el despacho por `origen` y los
    sentinels, con `linajes` explicito para no disparar el cache real."""

    def test_propio_manda_sobre_el_derivado(self):
        fila = {"resultado_id": "RES-1", "corrida_id": "CORR-1",
                "origen": "OFERTA", "camino_linaje": "YA-PUESTO"}
        j = vista.join_resultado(fila, {}, linajes={})
        self.assertEqual(j["camino_linaje"], "YA-PUESTO")

    def test_demanda_es_el_patron_mecanico_sin_oferta(self):
        fila = {"resultado_id": "RES-1", "corrida_id": "CORR-1", "origen": "DEMANDA"}
        j = vista.join_resultado(fila, {}, linajes={})
        self.assertEqual(j["camino_linaje"], "CORR-1/RES-1 -> DEMANDA-PENDIENTE")

    def test_oferta_usa_el_mapa_explicito(self):
        fila = {"resultado_id": "RES-1", "corrida_id": "CORR-1", "origen": "OFERTA"}
        linajes = {("CORR-1", "RES-1"): "CALC-X/RES-1 -> manifiesto:m [REESTIMACION]"}
        j = vista.join_resultado(fila, {}, linajes=linajes)
        self.assertEqual(j["camino_linaje"], linajes[("CORR-1", "RES-1")])

    def test_oferta_sin_cobertura_da_sentinel_declarado(self):
        fila = {"resultado_id": "RES-1", "corrida_id": "CORR-AUSENTE-DE-OFERTA",
                "origen": "OFERTA"}
        j = vista.join_resultado(fila, {}, linajes={})
        self.assertEqual(j["camino_linaje"], vista.SIN_OFERTA_EN_VISTA)


class PruebaCaminoLinajeBajoDemanda(unittest.TestCase):
    """HUERFANA a proposito (D-21): corre `vista.linajes_por_resultado()`
    contra el repo real (`_lee_oferta`, ~310 `CALC-*/`, ~70s medido
    24/sep/2026) -- `tests/check.py --rapido` (presupuesto 15s) no la
    corre; `ci_guardias.py --ejecuta-huerfanos` si.

    El fixture (`tests/fixtures/vista-camino-linaje-muestra500.json`) es
    una muestra de 500 filas REALES de `data/corrida0/resultados.tsv`
    (semilla fija 20260924, ACTO GEN2-TUBERIA-VISTA-NORMALIZADA-3,
    COMMIT-B) con su `camino_linaje` de ANTES de que este acto quitara la
    columna -- verificado entonces, en una sola pasada consistente
    (`_lee_oferta`+`_propaga_envuelto` sobre `decisiones.tsv` en ese mismo
    instante), contra el texto que la maquina de `corrida0.py` escribia.
    Compara ese texto congelado, no `resultados.tsv` actual (que ya no
    trae la columna, y que puede seguir moviendose: `decisiones.tsv` es
    edicion manual de mesa, no un insumo sellado -- 47/65 287 filas de
    OTRAS corridas activamente en curso el 24/sep/2026 ya driftearon
    contra su propio texto publicado en los minutos que tomo medir esto,
    por decisiones de mesa agregadas mientras tanto; ninguna de las 500
    de la muestra es una de ellas)."""

    @classmethod
    def setUpClass(cls):
        ruta = Path(__file__).resolve().parent / "fixtures" / "vista-camino-linaje-muestra500.json"
        with ruta.open(encoding="utf-8") as fh:
            cls.muestra = json.load(fh)
        cls.linajes = vista.linajes_por_resultado()

    def test_500_filas_reales_reproducen_el_texto_original(self):
        fallos = []
        for esperado in self.muestra:
            fila = {"resultado_id": esperado["resultado_id"],
                    "corrida_id": esperado["corrida_id"],
                    "spec_id": esperado["spec_id"],
                    "origen": esperado["origen"]}
            j = vista.join_resultado(fila, {}, linajes=self.linajes)
            if j["camino_linaje"] != esperado["camino_linaje"]:
                fallos.append(esperado["resultado_id"])
        self.assertEqual(fallos, [],
                          f"{len(fallos)}/{len(self.muestra)} no reprodujeron "
                          f"su camino_linaje original: {fallos[:5]}...")

    def test_muestra_cubre_oferta_y_demanda(self):
        origenes = {f["origen"] for f in self.muestra}
        self.assertEqual(origenes, {"OFERTA", "DEMANDA"},
                          "la muestra deberia cubrir ambos origenes reales")


class ConstantesResultado(unittest.TestCase):
    def fixture(self):
        return {"corridas": [{"corrida_id": "C1"}, {"corrida_id": "C2"}],
                "resultados": [
                    {"corrida_id": "C1", "resultado_id": "R1", "spec_id": "S1",
                     "valor": "0.1", "sello": "SÍ", "validacion_ref": "",
                     "delta_legacy": "NO-DECLARADO", "valor_legacy": ""},
                    {"corrida_id": "C1", "resultado_id": "R2", "spec_id": "S1",
                     "valor": "0.2", "sello": "SÍ", "validacion_ref": "informe.md",
                     "delta_legacy": "NO-DECLARADO", "valor_legacy": "3"},
                    {"corrida_id": "C2", "resultado_id": "R3", "spec_id": "S2",
                     "valor": "0.3", "sello": "NO"}], "usos": []}

    def test_roundtrip_celdas_vacias_variables_unicode_y_corrida_unica(self):
        import copy
        original = self.fixture()
        antes = copy.deepcopy(original)
        normal = vista.normaliza_constantes_resultados(original)
        corridas = {f["corrida_id"]: f for f in normal["corridas"]}
        self.assertEqual(original, antes)
        self.assertEqual([vista.restaura_constantes_resultado(f, corridas)
                          for f in normal["resultados"]], original["resultados"])
        self.assertEqual(normal["resultados"][0]["validacion_ref"], "")
        self.assertEqual(normal["resultados"][1]["validacion_ref"], "informe.md")
        self.assertEqual(normal["resultados"][2]["spec_id"], "S2")
        self.assertEqual(vista.normaliza_constantes_resultados(normal), normal)

    def test_lectores_y_consulta_restituyen_los_campos(self):
        import csv
        import tempfile
        import corrida0
        import consulta
        normal = vista.normaliza_constantes_resultados(self.fixture())
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            for nombre, filas in (("corridas", normal["corridas"]), ("resultados", normal["resultados"])):
                campos = sorted({k for f in filas for k in f})
                with (base / (nombre + ".tsv")).open("w", newline="") as fh:
                    w = csv.DictWriter(fh, campos, delimiter="\t")
                    w.writeheader()
                    w.writerows(filas)
            ruta = base / "resultados.tsv"
            for lector in (vista._leer_tsv_derivado, corrida0._leer_tsv_derivado):
                leidas = lector(ruta)
                self.assertEqual(leidas[0]["spec_id"], "S1")
                self.assertEqual(leidas[0]["delta_legacy"], "NO-DECLARADO")
                self.assertEqual(leidas[0]["validacion_ref"], "")
                self.assertEqual(leidas[1]["validacion_ref"], "informe.md")
            fila, _ = consulta.busca_tsv(ruta, "resultado_id", "R2")
            self.assertEqual(fila["sello"], "SÍ")
            fila, _ = consulta.busca_tsv(ruta, "spec_id", "S1")
            self.assertEqual(fila["resultado_id"], "R1")

    def test_metadata_ausente_o_invalida_para_en_voz_alta(self):
        fila = {"corrida_id": "C1", "spec_id": "", "constantes_corrida": "1"}
        with self.assertRaises(ValueError):
            vista.restaura_constantes_resultado(fila, {})
        for texto in ('{"valor":"999"}', '{"spec_id":23}', '[]', '{'):
            with self.assertRaises(ValueError):
                vista.restaura_constantes_resultado(fila, {"C1": {"constantes_resultados": texto}})

    def test_migracion_de_filas_publicadas_fuera_del_lote(self):
        import corrida0
        original = self.fixture()
        legado = {**original,
                  "corridas": [corrida0._rellena_columnas_nuevas(f, ["corrida_id", "constantes_resultados"])
                               for f in original["corridas"]],
                  "resultados": [corrida0._rellena_columnas_nuevas(f, [*f, "constantes_corrida"])
                                 for f in original["resultados"]]}
        normal = vista.normaliza_constantes_resultados(legado)
        corridas = {f["corrida_id"]: f for f in normal["corridas"]}
        self.assertEqual([vista.restaura_constantes_resultado(f, corridas)
                          for f in normal["resultados"]], original["resultados"])


if __name__ == "__main__":
    unittest.main()
