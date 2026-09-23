"""Origen móvil: sin mezcla de eras ni salto sobre trimestre ausente."""
import unittest

from tools.dominios.enoe.persistencia import derivar


class OrigenMovil(unittest.TestCase):
    def test_pasos_y_tendencia(self):
        def fila(ola, era, p, conducta="empleo_informal"):
            return {"ola": ola, "era": era, "conducta": conducta, "eje": "nacional",
                    "segmento": "NAC", "unidad": "proporcion", "punto": p,
                    "ic95_lo": p - .05, "ic95_hi": p + .05}
        datos = [fila("2019T3", "clasica", .4), fila("2019T4", "clasica", .5),
                 fila("2020T1", "clasica", .6), fila("2020T3", "enoen", .7),
                 fila("2020T4", "enoen", .8),
                 fila("2019T3", "clasica", .5, "ingreso_ocupado_nominal")]
        salida = derivar(datos)
        self.assertEqual([(r["ola_origen"], r["ola_destino"]) for r in salida],
                         [("2019T3", "2019T4"), ("2019T4", "2020T1"),
                          ("2020T3", "2020T4")])
        self.assertIsNone(salida[0]["pronostico_tendencia"])
        self.assertAlmostEqual(salida[1]["pronostico_tendencia"], .6)
        self.assertTrue(all(r["ic_predictivo"] is None for r in salida))


if __name__ == "__main__":
    unittest.main()
