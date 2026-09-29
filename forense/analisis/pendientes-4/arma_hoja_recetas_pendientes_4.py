#!/usr/bin/env python3
"""arma_hoja_recetas_pendientes_4.py -- ACTO GEN2-PENDIENTES-4 · P3: arma `hoja-recetas-pendientes-4.md`
(la hoja de recetas de mesa: acciones con identidad real, una acción física = una fila = una receta de un
minuto) y `recetas-pendientes-4.json` ({NC: fecha} para el dueño `MESA-ACCION (<fecha>)`).

Una acción con identidad (correo, solicitud con datos reales, registro con cuenta, montar un disco, activar
una función de GitHub, generar un .ots) NO es una pieza de un encargo: el ejecutor no la puede hacer (ADENDA-1).
Se deduplica por acción física: varias NC del libro pueden pedir el mismo envío. Contraste con R46–R49 y con
las seis solicitudes (a)–(f) de OBTENCION-EXTERNA-1 (`forense/analisis/hoja-firmas-21/decisiones-21.tsv`,
`forense/analisis/obtencion-externa-1/`): las que son ese mismo objeto se marcan con su renglón.

    python3 arma_hoja_recetas_pendientes_4.py <recetas-final.json> <hoja.md> <recetas.json>
"""
import csv
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
MANANA = "2026-09-29"    # R46, R47, R49 y R51: mesa las difirió «para mañana» el 28/sep (FP …8560-…, TRAMITE-FIRMAS-21)
SEMANA = "2026-10-05"

# (id de acción, título, claves de acción de los investigadores que se funden, fecha, renglón/objeto contra el que se deduplicó)
ACCIONES = [
    ("A01", "Generar el sello externo (.ots) del manifiesto de sellos", ["OTS-SELLO-EXTERNO-2", "SELLO-EXTERNO-OTS-TSA-MANIFIESTO"], SEMANA, "FP fde0-02 FIRMADA («mesa genera el .ots»)"),
    ("A02", "Activar GitHub Pages desde main/docs y comprobar que sirve", ["R49-PAGES", "R49-PUBLICACION-GITHUB-PAGES"], MANANA, "R49"),
    ("A03", "Poner los metadatos del repo (About y vista previa social)", ["R49-METADATOS-REPO"], MANANA, "R49"),
    ("A04", "Registrarse con la identidad de mesa en las fuentes de R46 (EMOVI/CEEY, WVS, IFPS, MCPS, LAPOP)", ["R46-REGISTROS-CON-IDENTIDAD"], MANANA, "R46"),
    ("A05", "Montar el disco externo (o el remoto cifrado) y dar la ruta del respaldo del corpus", ["R47-RESPALDO-CORPUS-FUERA-DE-MAQUINA"], MANANA, "R47"),
    ("A06", "Pegar la v2.17 de las instrucciones en el proyecto de Claude y subir la PLANTILLA v2.2", ["R51-PEGADO-V217"], MANANA, "R51"),
    ("A07", "Enviar las solicitudes (a)–(f) de OBTENCION-EXTERNA-1 (Banxico, IECM y Segob por PNT; correos; Delaney)", ["R48-ENVIAR-SEIS-SOLICITUDES-OE1", "OE1-SOL-b-IECM-PNT", "OE1-SOL-c-SEGOB-MECANISMO-PNT"], SEMANA, "R48 = solicitudes (a)–(f) de OBTENCION-EXTERNA-1; la NC 81e1-04 añade una línea a la (c)"),
    ("A08", "Pedir por acceso institucional los dos papers de pago de OBTENCION-EXTERNA-1 P3", ["ACCESO-INSTITUCIONAL-PAPERS-PAGO-OE1-P3"], SEMANA, "distinta de las (a)–(f): son dos PDF de pago"),
    ("A09", "Presentar a INEGI la solicitud ENCIG evento × canal (y, en la misma visita, el listado de UPM de ENVIPE)", ["INEGI-CONTACTO-EXP21-04-ENCIG-EVENTO-CANAL", "EXP21-04-INEGI-ENCIG-NC-0153", "INEGI-CONTACTO-ENVIPE-ROSTER-UPM"], SEMANA, "expediente 04 de EXPEDIENTES-ACCESO-21; no es ninguna de (a)–(f)"),
    ("A10", "Pedir a INEGI la regla oficial de varianza de los 39 estratos singleton de ENOE 2024T4", ["INEGI-SOLICITUD-VARIANZA-SINGLETON-ENOE2024T4"], SEMANA, "distinta de A09"),
    ("A11", "Pedir a INEGI la llave LLAVE→UPM/estrato (o pesos replicados) de ENDIREH 2003", ["SOLICITUD-INEGI-ENDIREH2003-LLAVE-UPM-ESTRATO"], SEMANA, "acuse por adenda de OBTENCION-EXTERNA-2"),
    ("A12", "Presentar los expedientes de acceso ICPSR 35024, OECD Trust PUM y ENJUVE", ["EXPEDIENTES-ACCESO-21-ICPSR-OECD-IMJUVE", "CORREO-OECD-TRUST-PUM"], SEMANA, "el correo OECD de NC-0061 es el mismo envío que el de NC-0151"),
    ("A13", "Enviar la solicitud combinada ENNViH DIN+S6 (pesos replicados o servicio de varianza)", ["CORREO-ENNVIH-DIN-S6"], SEMANA, "expediente 03 de EXPEDIENTES-ACCESO-21"),
    ("A14", "Escribir al CEEY por el cuadro y el denominador de la cifra de movilidad desde pobreza", ["CORREO-CEEY-CIFRA-POBREZA"], SEMANA, "misma institución que R46 pero otra acción (no es un registro)"),
    ("A15", "Escribir al autor de «Do Workers Value Formal Jobs?» por el Appendix C y los datos", ["CORREO-AUTOR-DO-WORKERS-VALUE-FORMAL-JOBS"], SEMANA, "el correo sale del PDF del payload (corpus de caja)"),
    ("A16", "Registrarse y bajar Pew «Religion in Latin America» 2014", ["REGISTRO-PEW-RELIGION-LATAM-2014"], SEMANA, "no está en R46"),
    ("A17", "Solicitar EMIF Norte/Sur al COLEF (formulario con identidad)", ["EMIF-COLEF-REGISTRO-FORMULARIO"], SEMANA, "no está en R46"),
    ("A18", "Bajar desde una red doméstica los cortes REDECO previos a 2025", ["RED-EXTERNA-REDECO-CORTES-PREVIOS-2025"], SEMANA, "necesita red que la caja no tiene"),
    ("A19", "Buscar la metodología 2012 de ENCUP en el portal de Segob", ["NAVEGADOR-ENCUP2012-METODOLOGIA-SEGOB"], SEMANA, "acción de navegador"),
    ("A20", "Abrir el DOI de Benjamini–Hochberg 1995 y copiar la frase que distingue FDR de FWER", ["ABRIR-DOI-BENJAMINI-HOCHBERG-1995"], SEMANA, "acceso institucional"),
    ("A21", "Adjuntar al chat de un acto de trámite los tres archivos fuente (transfer de Astra, plan de visibilización, informe y revisión del mapa)", ["ADJUNTAR-ZIP-TRANSFER-ASTRA-20260927", "ADJUNTAR-PLAN-VISIBILIZACION-20260923", "ADJUNTAR-INFORME-Y-REVISION-MAPA-20260927"], SEMANA, "un solo gesto; cada archivo con su sha256 (A.3)"),
    ("A22", "Aportar la evidencia de /raw y el launcher del lote 1 de C1 (rótulo CIEGA-POR-SEPARACIÓN)", ["ASTRA-EVIDENCIA-LOTE1-RAW-Y-LAUNCHER"], SEMANA, "reserva declarada por el recibo de ASTRA6-1"),
]

EXCLUIR_CLAVES = {"SOLICITUD-LM-INEGI-ENCRIGE2020-MICRODATO"}

MANUAL_NC = {
    # NC-0056: convenios y credenciales personales de tandas; los verificadores rechazaron cerrarla («ninguna firma nombra NC-0056»)
    "NC-0056": ("A23", "Convenios y credenciales personales de tandas (tanda.mx/tandamas.mx, Tanda+) y Findex individual",
                "Los tres son personales y no se negocian desde el repo: (1) convenio institucional con tanda.mx/tandamas.mx y con Tanda+ (equipo@tandamas.mx); (2) trámite presencial; (3) cuenta gratuita del Banco Mundial para Findex individual. Con identidad de mesa: escribir o presentarse; guardar el acuse en `forense/expedientes-acceso/` y avisar la ruta.",
                SEMANA, "NC-0061 es el correo a tandas de la misma familia; FP-286 difiere lo comercial (D17/D18)"),
}


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        return 2
    fin_p, hoja_md, rec_json = sys.argv[1:4]
    rec = json.load(open(fin_p, encoding="utf-8"))
    # la solicitud de microdato ENCRIGE 2020 cuelga de la decisión D16 (R10: «opcional, la decide mesa aparte»): no es receta
    for i in [i for i, r in rec.items() if r["clave"] in EXCLUIR_CLAVES]:
        print(f"  {i}: pasa al renglón D16 de la hoja de decisiones (no es receta)")
        del rec[i]
    por_clave = {}
    for i, r in rec.items():
        por_clave.setdefault(r["clave"], []).append((i, r))
    usadas, fechas = set(), {}
    out = ["# Hoja de recetas de mesa · GEN2-PENDIENTES-4", "",
           "Acciones con identidad real (correos, solicitudes, registros, un disco, una función de GitHub, un `.ots`): un ejecutor no las puede hacer. "
           "Están **deduplicadas por acción física** (varias NC pedían el mismo envío) y contrastadas contra R46–R49 y las seis solicitudes (a)–(f) de `GEN2-OBTENCION-EXTERNA-1`. "
           "Cada NC de esta hoja lleva `MESA-ACCION (<fecha>)` como dueño; la fecha es la que mesa ya fijó (R46, R47, R49 y R51 difieridas al 29/sep) o el corte semanal (5/oct). "
           "El acuse de cada solicitud entra por adenda del acto que la registra, no por un trámite aparte (A.12). "
           "Generada por `arma_hoja_recetas_pendientes_4.py`.", ""]
    for aid, titulo, claves, fecha, dedup in ACCIONES:
        ncs, recetas, destinos = [], [], []
        for c in claves:
            for i, r in por_clave.get(c, []):
                ncs.append(i); usadas.add(i)
                if r["receta"]:
                    recetas.append(str(r["receta"]).strip())
                if r.get("destino"):
                    destinos.append(str(r["destino"]).strip())
        if not ncs:
            sys.exit(f"{aid}: ninguna NC para {claves}")
        for i in ncs:
            fechas[i] = fecha
        out += [f"## {aid} · {titulo}", "", f"**Cierra ({len(ncs)}):** " + ", ".join(f"`{i}`" for i in ncs),
                f"**Fecha:** {fecha} · **Deduplicada contra:** {dedup}", "", "**Receta de un minuto.**", ""]
        vistos = []
        for t in recetas:
            if t not in vistos:
                vistos.append(t)
        for t in vistos:
            out.append(f"- {t}")
        if destinos:
            out += ["", "**Destino / acuse.** " + " · ".join(dict.fromkeys(destinos))]
        out.append("")
    for i, (aid, titulo, receta, fecha, dedup) in MANUAL_NC.items():
        fechas[i] = fecha
        usadas.add(i)
        out += [f"## {aid} · {titulo}", "", f"**Cierra (1):** `{i}`", f"**Fecha:** {fecha} · **Deduplicada contra:** {dedup}", "", "**Receta de un minuto.**", "", f"- {receta}", ""]
    faltan = sorted(set(rec) - usadas)
    sin_jsn = [i for i in faltan]
    open(hoja_md, "w", encoding="utf-8").write("\n".join(out) + "\n")
    json.dump(fechas, open(rec_json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"recetas: {len(rec)} filas de investigador + {len(MANUAL_NC)} manual → {len(ACCIONES) + len(MANUAL_NC)} acciones físicas · NC con fecha: {len(fechas)} · sin acción: {len(sin_jsn)}")
    for i in sin_jsn:
        print("  SIN ACCIÓN:", i, "|", rec[i]["clave"])
    return 1 if sin_jsn else 0


if __name__ == "__main__":
    sys.exit(main())
