"""Regresiones dirigidas de ACTO GEN2-MOTOR-USOS-Y-COMPLEMENTOS."""
from __future__ import annotations

import unittest
import csv
from pathlib import Path
import sys

import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from milpa.src import emisor  # noqa: E402


class MotorUsosComplementos(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reglas = {r.id: r for r in emisor.cargar_reglas()}

    def test_encuci_no_aplica_sin_contacto(self):
        regla = self.reglas["tramite.mordida.discrecional"]
        fuera = emisor.emitir_transicion(regla, "solicitud", {})
        self.assertEqual("NO_COVERAGE", fuera.estado)
        dentro = emisor.emitir_transicion(
            regla, "solicitud",
            {"contacto_funcionario_ultimos_12_meses": True,
             "respuesta_solicitud_entrega_valida": True})
        self.assertEqual("EMITE", dentro.estado)
        self.assertAlmostEqual(0.106319, dentro.valor_punto)

    def test_encuci_separa_solicitud_entrega_y_union(self):
        regla = self.reglas["tramite.mordida.discrecional"]
        contexto = {"contacto_funcionario_ultimos_12_meses": True,
                    "respuesta_solicitud_entrega_valida": True}
        ps = {evento: emisor.emitir_transicion(regla, evento, contexto).valor_punto
              for evento in ("solicitud", "entrega", "union")}
        self.assertEqual({"solicitud": 0.106319,
                          "entrega": 0.073640,
                          "union": 0.126006}, ps)
        self.assertNotEqual(ps["entrega"], 1.0 - ps["solicitud"])

    def test_encuci_cuatro_combinaciones_y_faltantes(self):
        esperados = {
            (0, 0): 0, (1, 0): 1, (0, 1): 1, (1, 1): 1,
            (1, None): 1, (None, 1): 1,
            (0, None): None, (None, 0): None, (None, None): None,
        }
        for (s, e), union in esperados.items():
            with self.subTest(solicitud=s, entrega=e):
                estado = emisor.estado_encuci_solicitud_entrega(s, e)
                self.assertEqual((s, e, union),
                                 (estado["solicitud"], estado["entrega"],
                                  estado["union"]))

    def test_alias_encuci_y_complemento_comparten_padre(self):
        regla = self.reglas["tramite.mordida.discrecional"]
        union = emisor.emitir_binaria(regla, "paga_mordida_encuci2020")
        normal_nuevo = emisor.emitir_binaria(
            regla, "sin_solicitud_y_sin_entrega_encuci2020")
        normal_alias = emisor.emitir_binaria(regla, "tramite_normal_encuci2020")
        self.assertEqual("solicitud_o_entrega_mordida_encuci2020",
                         union.valor_categoria)
        self.assertEqual(normal_nuevo, normal_alias)
        self.assertEqual(union.valor_punto + normal_nuevo.valor_punto, 1.0)
        self.assertEqual(union.valor_categoria, normal_nuevo.derivado_de)

    def test_encig_se_limita_al_grupo_observado(self):
        regla = self.reglas["tramite.mordida.con_registro"]
        conducta = "paga_mordida_encig2025_digital_r2"
        self.assertEqual("NO_COVERAGE",
                         emisor.emitir_binaria_en_contexto(
                             regla, conducta,
                             {"canal_p7_3": "digital_registrado"}).estado)
        emitida = emisor.emitir_binaria_en_contexto(
            regla, conducta,
            {"p8_4_observado": True,
             "canal_p7_3": "digital_registrado"})
        self.assertAlmostEqual(0.029868, emitida.valor_punto)
        antigua = next(s for s in regla.entonces
                       if s.conducta == "paga_mordida_encig2025_digital")
        self.assertIn("NO-ADOPTAR-NC-0107", antigua.uso_motor)

    def test_encig_r2_es_proxy_y_no_probabilidad_por_evento(self):
        regla = self.reglas["tramite.mordida.con_registro"]
        contexto = {"p8_4_observado": True,
                    "canal_p7_3": "digital_registrado"}
        descriptiva = emisor.emitir_binaria_en_contexto(
            regla, "paga_mordida_encig2025_digital_r2", contexto,
            uso_solicitado="consulta_descriptiva")
        self.assertEqual("EMITE", descriptiva.estado)
        self.assertEqual("proxy_descriptivo", descriptiva.rol_uso)
        self.assertIn("no es tasa general ni probabilidad empírica",
                      descriptiva.uso_motor)

        evento = emisor.emitir_binaria_en_contexto(
            regla, "paga_mordida_encig2025_digital_r2", contexto,
            uso_solicitado="probabilidad_evento")
        self.assertEqual("NO_COVERAGE", evento.estado)
        self.assertIn("probabilidad_evento", evento.detalle)

        # La ruta histórica conserva su resultado para replays y baseline.
        historica = emisor.emitir_binaria_en_contexto(
            regla, "paga_mordida_encig2025_digital_r2", contexto)
        self.assertEqual(descriptiva.valor_punto, historica.valor_punto)

    def test_enif_corrige_rotulo_y_preserva_alias(self):
        regla = self.reglas["dinero.ahorro.seguro_deposito_enif2024"]
        alias = emisor.emitir_binaria(
            regla,
            "desconfianza_como_razon_principal_conoce_proteccion_enif2024")
        self.assertIn("desconfianza_o_mal_servicio", alias.valor_categoria)
        fuera = emisor.emitir_binaria_en_contexto(
            regla, alias.valor_categoria,
            {"sin_cuenta": True, "conoce_proteccion_ipab": False})
        self.assertEqual("NO_COVERAGE", fuera.estado)

    def test_enigh_declara_2022_y_no_promedia_olas(self):
        regla = self.reglas["familia.seguro.volatilidad_ausencia_estado"]
        recibe = emisor.emitir_binaria(regla, "recibe_remesas")
        no_recibe = emisor.emitir_binaria(regla, "no_recibe_remesas")
        self.assertEqual(1.0, recibe.valor_punto + no_recibe.valor_punto)
        self.assertEqual("recibe_remesas", no_recibe.derivado_de)
        self.assertIn("ENIGH2022", regla.fuente)
        self.assertIn("no se promedia", next(
            s.uso_motor for s in regla.entonces
            if s.conducta == "recibe_remesas"))

    def test_res0028_es_resto_del_recorte_y_complemento_dependiente(self):
        regla = self.reglas["civico.denuncia.miedo_desconfianza"]
        fuera = emisor.emitir_binaria_en_contexto(
            regla, "denuncia_por_otra_razon",
            {"victima_18_mas": True, "delito_no_denunciado": True})
        self.assertEqual("NO_COVERAGE", fuera.estado)
        contexto = {"victima_18_mas": True, "delito_no_denunciado": True,
                    "bp1_23_en_01_08": True}
        padre = emisor.emitir_binaria_en_contexto(
            regla, "denuncia_con_miedo_o_desconfianza", contexto)
        resto = emisor.emitir_binaria_en_contexto(
            regla, "denuncia_por_otra_razon", contexto)
        self.assertEqual(1.0, padre.valor_punto + resto.valor_punto)
        self.assertEqual(padre.valor_categoria, resto.derivado_de)
        salida = next(s for s in regla.entonces
                      if s.conducta == "denuncia_por_otra_razon")
        self.assertIn("ni categoría literal 09", salida.evento)
        self.assertIn("NO significa algún delito", salida.evento)
        self.assertEqual("complemento_dependiente", salida.rol_uso)
        self.assertIn("NC-0085", salida.uso_motor)

    def test_res0028_persona_con_razones_mixtas_no_es_alguna_otra(self):
        # Una persona con delitos 01 y 04 pertenece tanto al grupo padre como
        # al conjunto de códigos residuales. El complemento del indicador
        # padre es 0; "alguna razón residual" daría 1 y es otro estimando.
        razones = {"01", "04"}
        indicador_padre = int(bool(razones & {"01", "02", "06", "08"}))
        alguna_razon_residual = int(bool(razones & {"03", "04", "05", "07"}))
        complemento_del_padre = 1 - indicador_padre
        self.assertEqual((1, 1, 0),
                         (indicador_padre, alguna_razon_residual,
                          complemento_del_padre))

        regla = self.reglas["civico.denuncia.miedo_desconfianza"]
        salida = next(s for s in regla.entonces
                      if s.conducta == "denuncia_por_otra_razon")
        self.assertEqual("denuncia_con_miedo_o_desconfianza",
                         salida.complemento_de)
        self.assertIn("padre=1, complemento=0", salida.uso_motor)

    def test_replicas_del_complemento_no_son_otro_sorteo(self):
        q, replicas_q = emisor.complementar_replicas(
            0.30, (0.25, 0.31, 0.35))
        self.assertEqual(0.70, q)
        for p_b, q_b in zip((0.25, 0.31, 0.35), replicas_q):
            self.assertEqual(1.0, p_b + q_b)

    def test_vista_corrida0_no_cuenta_complemento_como_medicion(self):
        with (RAIZ / "data/corrida0/demanda-resultados.tsv").open(
                encoding="utf-8", newline="") as f:
            next(f)  # cabecera de procedencia de la vista derivada
            filas = {r["resultado_id"]: r
                     for r in csv.DictReader(f, delimiter="\t")}
        for padre, complemento in (("RES-0005", "RES-0006"),
                                   ("RES-0027", "RES-0028")):
            with self.subTest(complemento=complemento):
                self.assertEqual("conducta_p_derivado",
                                 filas[complemento]["tipo"])
                self.assertEqual(filas[padre]["corrida_natural"],
                                 filas[complemento]["corrida_natural"])

    def test_proxy_fintech_no_se_atribuye_al_producto(self):
        doc = yaml.safe_load((RAIZ / "milpa" / "procedencia.yaml").read_text())
        fila = next(f for f in doc["asignados_probabilidad"]
                    if f["regla"] == "dinero.credito.scoring_alternativo")
        proxy = fila["proxy_canal_enif2024"]
        self.assertIn("último producto", proxy["etiqueta"])
        self.assertIn("NO-CALIBRA", proxy["uso_motor"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
