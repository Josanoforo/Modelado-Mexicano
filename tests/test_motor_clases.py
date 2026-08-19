#!/usr/bin/env python3
"""Las CINCO REGLAS del contrato de insumos (insumo 3 del encargo de
MOTOR-3/E0), una por prueba, más el muro de contraste intra-hogar.

Violación de clase = bug de contrato. Esto es lo que lo atrapa.
"""

from _motor_arnes import Arnes, cierto, igual, lanza, saltar  # noqa: E402

from milpa.src import celdas as C  # noqa: E402
from milpa.src import clases as K  # noqa: E402
from milpa.src import procedencia as P  # noqa: E402


def _una(proc, clase):
    xs = proc.por_clase(clase)
    if not xs:
        saltar(f"no hay entradas {clase.value} en el árbol hoy")
    return xs[0]


def main():
    a = Arnes("T-MOTOR-CLASES")
    proc = P.cargar()

    def test_nacional_no_segmenta():
        e = _una(proc, K.Clase.MEDIDO_NACIONAL)
        lanza(K.SegmentacionProhibida, P.segmentar, e, "edad")

    def test_parcial_solo_sus_ejes():
        e = _una(proc, K.Clase.MEDIDO_PARCIAL)
        cierto(e.ejes, "una MEDIDO·PARCIAL(x) sin ejes es una contradicción")
        P.segmentar(e, e.ejes[0])          # su propio eje: pasa
        lanza(K.EjeNoDeclarado, P.segmentar, e, "eje_que_no_declara")

    def test_asignado_sin_banda_no_inventa():
        e = _una(proc, K.Clase.ASIGNADO)
        igual(e.banda, None, "banda de ASIGNADO:")
        igual(e.deuda, "dispersion_no_declarada", "deuda de ASIGNADO:")

    def test_gate_id_detiene():
        e = _una(proc, K.Clase.GATE_ID)
        lanza(K.GateDetiene, P.como_estimando, e)
        lanza(K.GateDetiene, P.segmentar, e, "edad")

    def test_pendiente_no_entra():
        # PENDIENTE ya no aparece como valor de `clase:` en el árbol de hoy
        # (`ACTO COND-ATRIB` movió la última). Se prueba el CONTRATO con una
        # entrada sintética -- probarlo con una real que no existe sería no
        # probarlo. La regla vive igual: se carga, se registra, no consume.
        e = P.Entrada(llave="sintetica", clase=K.Clase.PENDIENTE,
                      crudo="PENDIENTE")
        lanza(ValueError, P.como_estimando, e)
        falso = P.Procedencia(entradas=[e])
        igual(len(falso.consumibles()), 0, "PENDIENTE en consumibles:")

    def test_clase_desconocida_no_adivina():
        lanza(K.ClaseDesconocida, K.clasificar, "CLASE_QUE_NO_EXISTE")
        lanza(K.ClaseDesconocida, K.clasificar, None)

    def test_prefijo_mas_largo_gana():
        c, _ = K.clasificar('MEDIDO·PARCIAL(edad)')
        igual(c, K.Clase.MEDIDO_PARCIAL, "prefijo resuelto:")
        c2, _ = K.clasificar('MEDIDO·NACIONAL')
        igual(c2, K.Clase.MEDIDO_NACIONAL, "prefijo resuelto:")

    def test_beta_sombrero_dos_code_points():
        # `β̂` = U+03B2 + U+0302. Si alguien lo normaliza a un code point, esto
        # deja de casar y el archivo deja de cargarse: por eso se prueba.
        igual(len(K.Clase.MEDIDO_BETA.value), len("MEDIDO·") + 2,
              "code points de `β̂`:")

    def test_intra_hogar_prohibido_al_construir():
        lanza(C.ContrasteIntraHogarProhibido, C.Cortes,
              por_eje={}, firma_m2="x", intra_hogar=("ingreso",))
        # los ejes de persona sí admiten contraste
        C.Cortes(por_eje={}, firma_m2="x", intra_hogar=("edad",))

    def test_corte_pendiente_no_se_inventa():
        igual(C.CORTES_C1.pendientes, ("edad", "migracion"),
              "cortes PENDIENTE:")
        lanza(C.CortesNoSellados, C.celda, edad="30-44")
        C.celda(formalidad="segsoc=1")     # eje sellado: pasa

    for nombre, fn in sorted(locals().items()):
        if nombre.startswith("test_"):
            a.prueba(nombre, fn)
    return a.cerrar()


if __name__ == "__main__":
    raise SystemExit(main())
