#!/usr/bin/env python3
"""Pruebas de ``sorteo_v3.py``: el piso 1 por estrato no vacío (regla 3
completa) y la regresión declarada por el encargo `MAESTRA33-S1`.

No vuelve a probar lo que `tests_sorteo_v2.py` ya prueba (sorteo sin
reposición, cuota dura, determinismo, fallback de infactibilidad como
mecanismo): sólo lo que `sorteo_v3.py` cambia (el reparto de asientos) y
las dos afirmaciones del encargo — regresión byte a byte contra B′ (v1_0)
cuando el piso no liga, y el reporte informativo sobre la semilla de v1_1
(que NO escribe ningún sorteado nuevo — ninguna prueba de este archivo
toca `marco-M-sorteado-v1_1.tsv`)."""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "forense" / "prereg-duelo-v2"


def _cargar(nombre: str, ruta: Path):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = mod
    spec.loader.exec_module(mod)
    return mod


SORTEO_V3 = _cargar("sorteo_v3", DIR / "sorteo_v3.py")
MARCO_M = _cargar("sorteo_marco_m", DIR / "sorteo_marco_m.py")
MARCO_M_V1_1 = _cargar("sorteo_marco_m_v1_1", DIR / "sorteo_marco_m_v1_1.py")
SORTEO_V2 = MARCO_M._SORTEO_V2

Fila = SORTEO_V2.Fila


def _filas(estrato: str, publicadas: list[str], prefijo: str) -> list[Fila]:
    return [
        Fila(id=f"{prefijo}-{i:02d}", estrato=estrato, publicada=pub)
        for i, pub in enumerate(publicadas)
    ]


class TestAsignarAsientosPisoUno(unittest.TestCase):
    """`asignar_asientos_proporcional_v3` — piso 1 por estrato no vacío,
    Hamilton sobre el resto."""

    def test_piso_uno_no_es_solo_un_parche_cuando_v2_ya_daba_al_menos_1(self):
        """Caso 1 de `tests_sorteo_v2.py` (cuotas 6.0/3.6/2.4 -> 6/4/2, v2
        NUNCA deja a nadie en cero aquí). Hallazgo, verificado por cómputo,
        no supuesto: v3 SIGUE dando un reparto distinto (`5/4/3`, no
        `6/4/2`) -- "piso 1 + Hamilton sobre el resto" no es un parche que
        sólo actúa cuando el método puro da 0 en algún estrato, es un
        método de reparto distinto en general (dar 1 "gratis" a cada
        estrato antes de repartir el resto favorece sistemáticamente a los
        estratos chicos frente al Hamilton puro, incluso cuando el piso no
        estaba en riesgo). Documentado también en el docstring del módulo y
        en `reglamento-sorteo-v1_1-PROPUESTA.md` -- no es una sorpresa
        oculta, es una propiedad declarada del método."""
        marco = (
            _filas("dinero|P2|DIFICIL", ["NO"] * 7 + ["SI"] * 3, "A")
            + _filas("dinero|P2|MEDIA", ["NO"] * 4 + ["SI"] * 2, "B")
            + _filas("trabajo|P1|MEDIA", ["NO"] * 3 + ["SI"] * 1, "C")
        )
        estratos = SORTEO_V2._agrupar_por_estrato(marco)
        v2 = SORTEO_V2.asignar_asientos_proporcional(estratos, 12)
        v3 = SORTEO_V3.asignar_asientos_proporcional_v3(estratos, 12)
        self.assertEqual(v2, {"dinero|P2|DIFICIL": 6, "dinero|P2|MEDIA": 4, "trabajo|P1|MEDIA": 2})
        self.assertEqual(v3, {"dinero|P2|DIFICIL": 5, "dinero|P2|MEDIA": 4, "trabajo|P1|MEDIA": 3})
        self.assertEqual(sum(v3.values()), 12)
        self.assertTrue(all(n >= 1 for n in v3.values()))

    def test_piso_liga_replica_exacta_del_hallazgo_fp213(self):
        """Réplica exacta del caso real de `FP-213`/`ADR-248`
        (`sorteo-marco-M-resultados-v1_1.md`, sección «Hallazgo»): 2
        estratos (21 filas / 1 fila), n_sorteo=11 -> cuota_exacta 10.5/0.5,
        empate de fracción en el estrato de 1 fila (0.5). v2 deja ese
        estrato en 0 (pierde el desempate alfabético); v3 le da su piso 1
        y recorta 1 al otro estrato."""
        marco = _filas("PENDIENTE", ["NO"] * 21, "P") + _filas("tramite|P1|MEDIA", ["NO"], "T")
        estratos = SORTEO_V2._agrupar_por_estrato(marco)
        v2 = SORTEO_V2.asignar_asientos_proporcional(estratos, 11)
        v3 = SORTEO_V3.asignar_asientos_proporcional_v3(estratos, 11)
        self.assertEqual(v2, {"PENDIENTE": 11, "tramite|P1|MEDIA": 0})
        self.assertEqual(v3, {"PENDIENTE": 10, "tramite|P1|MEDIA": 1})
        self.assertEqual(sum(v3.values()), 11)

    def test_piso_uno_trivial_con_un_solo_estrato(self):
        """Un solo estrato no vacío: piso 1 + resto siempre coinciden con
        Hamilton puro -- no hay otro estrato con el que comparar fracción."""
        marco = _filas("tramite|P1|MEDIA", ["NO", "NO"], "T")
        estratos = SORTEO_V2._agrupar_por_estrato(marco)
        v2 = SORTEO_V2.asignar_asientos_proporcional(estratos, 2)
        v3 = SORTEO_V3.asignar_asientos_proporcional_v3(estratos, 2)
        self.assertEqual(v2, v3)
        self.assertEqual(v3, {"tramite|P1|MEDIA": 2})

    def test_n_sorteo_menor_a_n_estratos_no_implementado(self):
        """Segunda cláusula de la regla 3 (sorteo sin reposición de qué
        estratos entran) -- declarada NotImplementedError, no aproximada."""
        marco = _filas("a", ["NO"], "A") + _filas("b", ["NO"], "B") + _filas("c", ["NO"], "C")
        estratos = SORTEO_V2._agrupar_por_estrato(marco)
        with self.assertRaises(NotImplementedError):
            SORTEO_V3.asignar_asientos_proporcional_v3(estratos, 2)


class TestSortearV3ConInfactibilidad(unittest.TestCase):
    """El fallback de §2.3 debe seguir aplicando piso 1 (misma regla 3)
    cuando recalcula asientos entre los estratos factibles restantes."""

    def test_infactibilidad_mas_piso_uno_no_forzado_en_estrato_infactible(self):
        marco = (
            _filas("tiempo|P2|MEDIA", ["SI", "SI"], "T")
            + _filas("familia|P2|DIFICIL", ["SI"], "F")
            + _filas("dinero|P2|DIFICIL", ["NO"] * 7 + ["SI"] * 3, "D")
        )
        r = SORTEO_V3.sortear_v3(marco, n_sorteo=12, cuota_max=2, semilla=7)
        self.assertCountEqual(r.estratos_excluidos, ["tiempo|P2|MEDIA", "familia|P2|DIFICIL"])
        self.assertTrue(all(f.estrato == "dinero|P2|DIFICIL" for f in r.resultado))
        ids = [f.id for f in r.resultado]
        self.assertEqual(len(ids), len(set(ids)))


class TestRegresionBPrime(unittest.TestCase):
    """`P1`: "reproduce B' (v1_0) byte a byte si el piso no ligaba ahí".

    B' (`ACTO MAESTRA32-E14`) sorteó con la rama IDENTIDAD de
    `sorteo_marco_m.sortear_marco_m` (`N_elegibles=2 < 15`): no invoca
    `asignar_asientos_proporcional` en absoluto, sólo ordena por `id`. Esa
    rama es de `sorteo_marco_m.py` (no tocado, no es parte de
    `sorteo_v3.py`) y su salida no depende de qué función de reparto de
    asientos esté detrás -- por construcción, coincide byte a byte
    independientemente de v2 o v3, así que NO es la prueba interesante.

    La afirmación no trivial es la de "si el piso no ligaba ahí": que la
    aritmética de reparto de asientos de v3, aplicada al mismo marco de B',
    da EXACTAMENTE el mismo reparto que v2 -- confirmado abajo comparando
    ambas funciones directamente sobre el marco real. NO se compara
    `sortear_v3()` (que sí corre el PRNG) contra la rama identidad de B'
    (que no lo corre): son dos mecanismos distintos por diseño de
    `regla_de_tamano` (N<15), no algo que la regla 3 cambie -- comparar sus
    salidas directamente sería una prueba mal planteada, no una regresión
    real."""

    def test_marco_real_b_prime_carga_2_filas_un_estrato(self):
        marco = MARCO_M.cargar_marco_m()
        self.assertEqual(len(marco), 2)
        self.assertEqual([f.id for f in marco], ["TRA-M-01", "TRA-M-02"])
        estratos = SORTEO_V2._agrupar_por_estrato(marco)
        self.assertEqual(list(estratos), ["tramite|P1|MEDIA"])

    def test_piso_no_liga_en_b_prime_reparto_identico_a_v2(self):
        """El hecho verificado: sobre el marco real de B' (mono-estrato, 2
        filas, `n_sorteo=2`), v3 y v2 reparten asientos idéntico -- "el piso
        no ligaba ahí"."""
        marco = MARCO_M.cargar_marco_m()
        estratos = SORTEO_V2._agrupar_por_estrato(marco)
        asientos_v2 = SORTEO_V2.asignar_asientos_proporcional(estratos, 2)
        asientos_v3 = SORTEO_V3.asignar_asientos_proporcional_v3(estratos, 2)
        self.assertEqual(asientos_v2, asientos_v3)
        self.assertEqual(asientos_v3, {"tramite|P1|MEDIA": 2})

    def test_identidad_de_sorteo_marco_m_reproduce_b_prime_byte_a_byte(self):
        """La rama que B' realmente ejecutó (`sortear_marco_m`, identidad
        por `N<15`) sigue reproduciendo el sellado tal cual -- no editada,
        no depende de v2 ni de v3 (declarado arriba, verificado aquí)."""
        marco = MARCO_M.cargar_marco_m()
        semilla = SORTEO_V2.semilla_desde_sha_merge(
            "f4d9b7f506aa5205231f6e7b355645d1206dd031", "MARCO-M-v1"
        )
        r = MARCO_M.sortear_marco_m(marco, n_sorteo=2, cuota_max=0, semilla=semilla)
        self.assertEqual([f.id for f in r.resultado], ["TRA-M-01", "TRA-M-02"])
        self.assertEqual(r.skips, [])
        self.assertEqual(r.estratos_excluidos, [])


class TestReporteInformativoV1_1(unittest.TestCase):
    """`P1`: "sobre la semilla de v1_1 reporta qué habría cambiado, SIN
    escribir ningún sorteado nuevo (opción A: v1_1 se acepta tal cual)".

    Corre `sortear_v3` sobre el marco-M v1_1 real con la MISMA semilla
    sellada de B″ -- estrictamente de lectura: no escribe
    `marco-M-sorteado-v1_1.tsv` ni ningún archivo `*sorteado*` nuevo, sólo
    compara en memoria contra el resultado ya sellado (releído del propio
    `.tsv` sellado, para no depender de una constante tecleada a mano)."""

    def test_v2_recomputado_coincide_con_el_sellado(self):
        """Control: antes de comparar contra v3, confirma que recomputar
        con v2 (sin editar) coincide con lo que `marco-M-sorteado-v1_1.tsv`
        trae -- si esto fallara, la comparación de abajo no significaría
        nada."""
        marco = MARCO_M_V1_1.cargar_marco_m_v1_1()
        semilla = SORTEO_V2.semilla_desde_sha_merge(
            "af41796f50baad1737987b7e9a1e737c38ab85f2", "MARCO-M-v1_1"
        )
        r_v2 = SORTEO_V2.sortear(marco, n_sorteo=11, cuota_max=2, semilla=semilla)

        import csv

        with (DIR / "marco-M-sorteado-v1_1.tsv").open(encoding="utf-8", newline="") as fh:
            ids_sellados = {renglon["id"] for renglon in csv.DictReader(fh, delimiter="\t")}
        self.assertEqual({f.id for f in r_v2.resultado}, ids_sellados)

    def test_v3_hipotetico_agrega_tra_m_02_quita_civ_m_01(self):
        """El diff real, verificado contra los archivos en el árbol: bajo
        v3 (piso 1), `TRA-M-02` (el estrato `tramite|P1|MEDIA` que la regla
        3 promete y v2 no le dio asiento) entra; `CIV-M-01` -- la fila que
        el PRNG deja fuera del estrato `PENDIENTE` al pasar de 11 a 10
        asientos -- sale. Las otras 10 filas no cambian."""
        marco = MARCO_M_V1_1.cargar_marco_m_v1_1()
        semilla = SORTEO_V2.semilla_desde_sha_merge(
            "af41796f50baad1737987b7e9a1e737c38ab85f2", "MARCO-M-v1_1"
        )
        r_v2 = SORTEO_V2.sortear(marco, n_sorteo=11, cuota_max=2, semilla=semilla)
        r_v3 = SORTEO_V3.sortear_v3(marco, n_sorteo=11, cuota_max=2, semilla=semilla)

        ids_v2 = {f.id for f in r_v2.resultado}
        ids_v3 = {f.id for f in r_v3.resultado}
        self.assertEqual(len(ids_v3), 11)
        self.assertEqual(ids_v3 - ids_v2, {"TRA-M-02"})
        self.assertEqual(ids_v2 - ids_v3, {"CIV-M-01"})
        self.assertEqual(r_v3.skips, [])
        self.assertEqual(r_v3.estratos_excluidos, [])

    def test_este_archivo_no_toca_ningun_sorteado(self):
        """Guarda de perímetro: `marco-M-sorteado-v1_1.tsv` (y cualquier
        otro `*sorteado*`) sin diff después de correr esta suite completa."""
        import subprocess

        salida = subprocess.run(
            ["git", "diff", "--stat", "HEAD", "--", "forense/prereg-duelo-v2/marco-M-sorteado-v1_1.tsv",
             "forense/prereg-duelo-v2/marco-M-sorteado-v1_0.tsv",
             "forense/prereg-duelo-v2/marco-congelado-piloto-v1_0.tsv"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        )
        self.assertEqual(salida.stdout.strip(), "")


if __name__ == "__main__":
    unittest.main()
