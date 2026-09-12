#!/usr/bin/env python3
"""Integra el cierre N34 en cola, necesidad y no-corrido sin reserializar TSV.

Idempotente: usa el escritor byte-preservante del registro y regenera la vista
de adquisición desde su fuente de verdad.
"""

from __future__ import annotations

import sys
from pathlib import Path


RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "tools"))

from curador_registro.tsv_crudo import leer_lineas, upsert_fila  # noqa: E402
from vista_cola_adquisicion import build  # noqa: E402


REGISTRO = RAIZ / "data" / "curacion-registro"
COLA = REGISTRO / "cola-adquisicion-registro.tsv"
NECESIDAD = REGISTRO / "necesidad-objeto-modelo.tsv"
NO_CORRIDO = RAIZ / "forense" / "no-corrido.tsv"
VISTA = RAIZ / "data" / "cola-adquisicion-v1_0.tsv"


def campos(path: Path) -> list[str]:
    return leer_lineas(path)[0].split("\t")


def integra() -> None:
    campos_cola = campos(COLA)
    origen = (
        "forense/encargos/cola/2026-09-12-GEN2-POST-726/"
        "36-GEN2-N34-DATOS-PRODUCTO-Y-DANO.md"
    )
    filas_cola = [
        {
            "fila_origen": "forense/notas/2026-09-11-GEN2-N34-DATOS-PRODUCTO-Y-DANO-cierre.md#BANXICO",
            "fuente_canonica": "BANXICO_SATISFACCION_USUARIOS_2019_2024",
            "fuente_canonica_normalizada": "BANXICO_SATISFACCION_USUARIOS_2019_2024",
            "discordancia_alias": "SIN_ALIAS",
            "estado_A4A5": "OBTENIDO",
            "prioridad": "3",
            "url_conocida": "https://www.banxico.org.mx/publicaciones-y-prensa/indicadores-de-satisfaccion-de-los-usuarios-de-ser/servicios-financieros-satis.html",
            "ids_manifiesto": "gen2_banxico_satisfaccion_usuarios_2019_2024_microdatos;gen2_banxico_satisfaccion_usuarios_2019_2024_manual;gen2_banxico_satisfaccion_usuarios_2024_informe",
            "origen": origen,
            "nota": "ACTO GEN2-N34-DATOS-PRODUCTO-Y-DANO (11/sep/2026): XLSX publico 2019-2024, manual e informe obtenidos y verificados dos veces. Microdato persona-ola enlaza cinco categorias de credito, costo subjetivo, pago y problemas en Mexico. EXISTE-SATISFACE para descripcion/asociacion; no lender, CAT ni causalidad. NC-0164 permanece abierta.",
        },
        {
            "fila_origen": "forense/notas/2026-09-11-GEN2-N34-DATOS-PRODUCTO-Y-DANO-cierre.md#SHED",
            "fuente_canonica": "FEDERAL_RESERVE_SHED_2025_BNPL",
            "fuente_canonica_normalizada": "FEDERAL_RESERVE_SHED_2025_BNPL",
            "discordancia_alias": "SIN_ALIAS",
            "estado_A4A5": "OBTENIDO",
            "prioridad": "3",
            "url_conocida": "https://www.federalreserve.gov/consumerscommunities/shed_data.htm",
            "ids_manifiesto": "gen2_federal_reserve_shed_2025_public_csv;gen2_federal_reserve_shed_2025_codebook",
            "origen": origen,
            "nota": "ACTO GEN2-N34-DATOS-PRODUCTO-Y-DANO (11/sep/2026): CSV y codebook publicos obtenidos y verificados dos veces. Co-observa uso BNPL, atraso, cargo extra, sobregiro/NSF y asequibilidad en 12,934 personas. Mecanismo extranjero descriptivo/asociativo; no transportar a Mexico ni tratar como causal.",
        },
        {
            "fila_origen": "forense/notas/2026-09-11-GEN2-N34-DATOS-PRODUCTO-Y-DANO-cierre.md#CFPB",
            "fuente_canonica": "CFPB_BNPL_UNSECURED_DEBT_2025",
            "fuente_canonica_normalizada": "CFPB_BNPL_UNSECURED_DEBT_2025",
            "discordancia_alias": "SIN_ALIAS",
            "estado_A4A5": "OBTENIDO-PARCIAL",
            "prioridad": "3",
            "url_conocida": "https://www.consumerfinance.gov/data-research/research-reports/consumer-use-of-buy-now-pay-later-and-other-unsecured-debt/",
            "ids_manifiesto": "gen2_cfpb_bnpl_unsecured_debt_2025_report",
            "origen": origen,
            "nota": "ACTO GEN2-N34-DATOS-PRODUCTO-Y-DANO (11/sep/2026): PDF oficial obtenido y verificado dos veces; Table 3 reproducida para 892,668 originaciones pay-in-four y default a 120 dias por FICO. OBTENIDO-PARCIAL porque el microdato administrativo no es publico; Estados Unidos, agregado y no causal.",
        },
    ]
    for fila in filas_cola:
        upsert_fila(COLA, fila, campos_cola, clave="fuente_canonica")

    upsert_fila(
        NECESIDAD,
        {
            "necesidad_id": "N34",
            "objeto_modelo_origen": "dinero.credito.baja_friccion_usura_dano_downstream",
            "fuentes_verificacion": "forense/notas/2026-09-11-GEN2-N34-DATOS-PRODUCTO-Y-DANO-cierre.md;data/curacion-registro/relaciones.tsv REL-defde50a805b668d2f395b84/REL-85fc542cc3c6ac0bb4b0d34c/REL-6e66d84d87b1a8d9543fcaa5;forense/notas/2026-08-25-eval-compartamos.md",
            "reserva": "Necesidad propia, NO reutiliza confianza_institucional ni radio_confianza. Compartamos aporta causalidad mexicana estrecha ya ejercida; Banxico aporta producto/costo subjetivo/pago en la misma persona para asociacion mexicana; SHED y CFPB documentan BNPL solo en Estados Unidos. Residual abierto: BNPL o credito digital/lender identificable en Mexico con CAT/tasa o friccion objetiva, dano, negativos y estrategia causal. Cero parametro adoptado por este acto.",
        },
        campos(NECESIDAD),
        clave="necesidad_id",
    )

    upsert_fila(
        NO_CORRIDO,
        {
            "id": "NC-0164",
            "fecha": "2026-09-11",
            "acto": "GEN2-N34-DATOS-PRODUCTO-Y-DANO",
            "pr": "#734",
            "pieza": "N34 · producto/costo y dano del lado consumidor",
            "que_no_se_corrio": "estimandos descriptivos/asociativos Banxico y SHED; busqueda con acceso condicionado; cualquier adopcion o inferencia causal nueva",
            "razon": "El acto adquirio y mapeo evidencia sin preespecificacion para estimar. CFPB Making Ends Meet exige aceptar terminos y no se adquirio; el panel de Di Maggio-Williams-Katz no tiene replica publica localizable.",
            "impacto": "Banxico habilita asociacion mexicana por cinco categorias de credito y SHED habilita mecanismo BNPL extranjero. Ninguna pieza nueva identifica el efecto de BNPL/CAT en Mexico; no se cambia el modelo.",
            "sucesor": "Pre-registrar estimandos Banxico si la mesa los acepta y localizar fuente mexicana con producto BNPL/digital o lender, CAT/tasa/friccion objetiva, dano, negativos y estrategia de identificacion.",
            "estado": "ABIERTA",
            "cerrado_por": "NO-APLICA-MIENTRAS-ABIERTA",
            "fecha_cierre": "NO-APLICA-MIENTRAS-ABIERTA",
        },
        campos(NO_CORRIDO),
        clave="id",
    )

    VISTA.write_text(build(COLA), encoding="utf-8")
    print("integracion N34 aplicada: 3 fuentes, N34 y NC-0164; vista regenerada")


if __name__ == "__main__":
    integra()
