#!/usr/bin/env python3
"""Actualiza únicamente las filas de seguimiento del encargo 21.

Es idempotente y preserva byte por byte todas las demás líneas. La cola canónica
usa el writer de la casa; no se toca la vista derivada directamente.
"""

from __future__ import annotations

from pathlib import Path

from curador_registro.tsv_crudo import leer_dicts, upsert_fila


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "forense/expedientes-acceso/2026-09-11-GEN2-EXPEDIENTES-ACCESO-21"
MARKER = "ACTO GEN2-EXPEDIENTES-ACCESO-21 (2026-09-11)"


def update_rows(path: Path, updates: dict[str, dict[str, str]]) -> None:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    fields = lines[0].split("\t")
    seen: set[str] = set()
    for index in range(1, len(lines)):
        values = lines[index].split("\t")
        if not values or values[0] not in updates:
            continue
        if len(values) != len(fields):
            raise ValueError(f"{path}:{index + 1}: {len(values)} campos, se esperaban {len(fields)}")
        row = dict(zip(fields, values))
        row.update(updates[values[0]])
        lines[index] = "\t".join(row[field] for field in fields)
        seen.add(values[0])
    missing = set(updates) - seen
    if missing:
        raise ValueError(f"filas no encontradas en {path}: {sorted(missing)}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def append_once(value: str, addition: str) -> str:
    return value if MARKER in value else f"{value} || {addition}"


def update_tracking() -> None:
    update_rows(
        ROOT / "forense/no-corrido.tsv",
        {
            "NC-0151": {
                "que_no_se_corrio": (
                    "presentar con identidad y compromisos reales los expedientes tecnicos ya listos de "
                    "ICPSR 35024, OECD Trust PUM y ENJUVE; recibir acceso o respuesta. Reuters DNR queda "
                    "diferido por no tener consumidor/reactivo/ano vigente y no se persigue el binario SSRN 2014"
                ),
                "razon": "EXPEDIENTES-TECNICOS-LISTOS; DECISION-DE-MESA-PENDIENTE; RESPUESTA-DE-TERCERO-PENDIENTE",
                "impacto": (
                    "cero envios, concesiones o archivos nuevos; ICPSR completo, OECD PUM y ENJUVE siguen sin "
                    f"obtenerse. Paquete: {PACKAGE}/INDICE-EXPEDIENTES-ACCESO-21.md"
                ),
                "sucesor": (
                    "titular: completar solo datos personales/contractuales verdaderos, presentar y aportar "
                    "acuse; receptor tecnico verifica respuesta/bytes antes de cualquier spec o calculo"
                ),
            },
            "NC-0153": {
                "que_no_se_corrio": (
                    "presentar a INEGI la solicitud tecnica ya lista sobre el enlace ENCIG 8.5 con "
                    "NT_TIPO/P7_3 o alternativa nacional evento x canal con negativos, universo y diseno; recibir respuesta"
                ),
                "razon": "OBTENIDO-PARCIAL; EXPEDIENTE-TECNICO-LISTO; DECISION-DE-MESA-PENDIENTE",
                "impacto": (
                    "la tasa nacional exacta por evento/canal sigue no identificada; no se repite la busqueda de #695 "
                    f"ni se degrada a PENDIENTE. Borrador: {PACKAGE}/04-INEGI-ENCIG-NC-0153.md"
                ),
                "sucesor": (
                    "titular presenta por Contacto INEGI; receptor verifica llave/unidad, negativos, universo, "
                    "ponderacion y diseno antes de congelar calculo"
                ),
            },
            "NC-0156": {
                "que_no_se_corrio": (
                    "presentar la solicitud combinada ENNViH DIN+S6 y recibir pesos replicados con contrato "
                    "completo o servicio oficial de varianza para los cuatro estimandos"
                ),
                "razon": "EXPEDIENTE-TECNICO-LISTO; DECISION-DE-MESA-PENDIENTE; NO-HAY-DISENO-PUBLICO-EJECUTABLE",
                "impacto": (
                    "NC-0156 permanece ABIERTA; puntos DIN y C1/C3/C4 disponibles, IC actuales solo sensibilidad; "
                    f"borrador: {PACKAGE}/03-ENNVIH-DIN-S6.md"
                ),
                "sucesor": (
                    "titular envia con identidad real; al recibir una via operativa, sucesor congela spec en CAJA, "
                    "verifica cobertura/metodo/df/escala y solo despues calcula"
                ),
            },
        },
    )

    fp_path = ROOT / "forense/firmas-pendientes.tsv"
    rows = {row["id"]: row for row in leer_dicts(fp_path)}
    addition_314 = (
        f"{MARKER}: partes tecnicas de ICPSR/OECD/ENJUVE terminadas en {PACKAGE}; Reuters diferido por demanda "
        "no definida. No enviado ni concedido; el residual de acceso efectivo sigue vigente."
    )
    addition_371 = (
        f"{MARKER}: solicitud oficial conjunta DIN+S6 lista en {PACKAGE}/03-ENNVIH-DIN-S6.md; no enviada y sin "
        "respuesta. FP-371 sigue ABIERTA y la recomendacion no cuenta como firma."
    )
    addition_372 = (
        f"{MARKER}: la misma solicitud enumera C1/C3/C4 y alternativas confidenciales ejecutables; no enviada. "
        "FP-372 sigue ABIERTA y no hereda decision alguna de DIN."
    )
    update_rows(
        fp_path,
        {
            "FP-314": {
                "dónde": append_once(
                    rows["FP-314"]["dónde"],
                    f"{MARKER}: {PACKAGE}/INDICE-EXPEDIENTES-ACCESO-21.md",
                ),
                "estado": append_once(rows["FP-314"]["estado"], addition_314),
                "ejecutada_en": append_once(rows["FP-314"]["ejecutada_en"], addition_314),
            },
            "FP-371": {
                "dónde": append_once(rows["FP-371"]["dónde"], f"{MARKER}: {PACKAGE}/03-ENNVIH-DIN-S6.md"),
                "ejecutada_en": append_once(rows["FP-371"]["ejecutada_en"], addition_371),
            },
            "FP-372": {
                "dónde": append_once(rows["FP-372"]["dónde"], f"{MARKER}: {PACKAGE}/03-ENNVIH-DIN-S6.md"),
                "ejecutada_en": append_once(rows["FP-372"]["ejecutada_en"], addition_372),
            },
        },
    )


def update_registry() -> None:
    path = ROOT / "data/curacion-registro/cola-adquisicion-registro.tsv"
    fields = path.read_text(encoding="utf-8-sig").splitlines()[0].split("\t")
    targets = {
        "MEXICO_PANEL_STUDY_2012": {
            "url_conocida": "https://www.icpsr.umich.edu/web/RCMD/studies/35024",
            "addition": (
                f"{MARKER}: RDUA/IDARS actual, justificacion, variables, alternativas insuficientes, custodia, "
                f"elegibilidad y recepcion listos en {PACKAGE}/01-ICPSR-35024-RDUA.md. No enviado, no concedido y "
                "35024-0001-Data.dta completo no obtenido; OBTENIDO conserva solo documentacion/tabulados existentes."
            ),
        },
        "OECD": {
            "url_conocida": "https://www.oecd.org/en/data/datasets/oecd-trust-survey-data.html",
            "addition": (
                f"{MARKER}: formulario DOCX existente completado tecnicamente y correo/recepcion listos en "
                f"{PACKAGE}/02-OECD-TRUST-PUM.md. Identidad, afiliacion real, fechas y firma quedan fuera de Git; "
                "no enviado ni concedido. Indicadores publicos ya obtenidos no se repiten."
            ),
        },
        "ENNVIH_DIN_M_01_DISENO_INFERENCIAL": {
            "url_conocida": "https://www.ennvih-mxfls.org/english/contact.html",
            "addition": (
                f"{MARKER}: una solicitud combinada DIN+S6 pide pesos replicados no geograficos o servicio oficial "
                f"para DIN y C1/C3/C4, con metodos/escalas/df/covarianza, en {PACKAGE}/03-ENNVIH-DIN-S6.md. No "
                "solicita UPM/geografia identificable; no enviada; NC-0156 y FP-371/372 permanecen abiertas."
            ),
        },
        "TASA_GENERAL_SOLICITUD_PAGO_INFORMAL_POR_CANAL_TRAMITES_MEXICO": {
            "url_conocida": "https://www.inegi.org.mx/inegi/contacto.html",
            "addition": (
                f"{MARKER}: pedido final reutiliza #695 y solicita enlace 8.5 con NT_TIPO/P7_3, microdato evento "
                f"con negativos/diseno o tabulado nacional equivalente; {PACKAGE}/04-INEGI-ENCIG-NC-0153.md. No "
                "enviado y sin nueva busqueda general; estado OBTENIDO-PARCIAL se conserva."
            ),
        },
        "ENJUVE": {
            "url_conocida": "https://transparencia.imjuventud.gob.mx/pages/AccesoInformacion.html",
            "addition": (
                f"{MARKER}: solicitud PNT por ola 2000/2005/2010 lista, con microdatos, diccionario, cuestionario, "
                f"diseno/pesos y respuesta separada si una ola no se reconoce; {PACKAGE}/05-IMJUVE-ENJUVE.md. No enviada."
            ),
        },
        "REUTERS_DNR": {
            "url_conocida": "https://reutersinstitute.politics.ox.ac.uk/digital-news-report/2025",
            "addition": (
                f"{MARKER}: cuestionario cruzado con consumidores actuales; ninguno fija ano/reactivo/uso. Solicitud "
                f"individual diferida con alcance minimo y criterio de reapertura en {PACKAGE}/06-REUTERS-DNR-DIFERIDO.md; "
                "no enviada y toplines publicos existentes conservan OBTENIDO-PARCIAL."
            ),
        },
    }
    rows = leer_dicts(path)
    by_source: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        by_source.setdefault(row["fuente_canonica"], []).append(row)
    for source, change in targets.items():
        matches = by_source.get(source, [])
        if len(matches) != 1:
            raise ValueError(f"{source}: se esperaba una fila, hay {len(matches)}")
        row = {field: matches[0][field] for field in fields}
        row["url_conocida"] = change["url_conocida"]
        row["nota"] = append_once(row["nota"], change["addition"])
        # Esta fila era estable en el control csv antes de editarla. Su nota
        # histórica contenía comillas parseadas que upsert_fila escribiría como
        # comillas sueltas; usar apóstrofos conserva el significado y la vuelve
        # estable sin cambiar el control documentado T26-bis de otras filas.
        if source == "MEXICO_PANEL_STUDY_2012":
            row["nota"] = row["nota"].replace('"', "'")
        upsert_fila(path, row, fields, clave="fuente_canonica")


def main() -> None:
    update_tracking()
    update_registry()
    old_index = f"{PACKAGE}/README.md"
    new_index = f"{PACKAGE}/INDICE-EXPEDIENTES-ACCESO-21.md"
    for relative in ("forense/no-corrido.tsv", "forense/firmas-pendientes.tsv"):
        path = ROOT / relative
        content = path.read_text(encoding="utf-8")
        if old_index in content:
            path.write_text(content.replace(old_index, new_index), encoding="utf-8")
    print("OK: 3 NC + 3 FP + 6 filas canonicas actualizadas; otras lineas preservadas")


if __name__ == "__main__":
    main()
