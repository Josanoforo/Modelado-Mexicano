#!/usr/bin/env python3
"""arma_grupos_pendientes_4.py -- ACTO GEN2-PENDIENTES-4: la agrupación de las NC «encargo por escribir» en
encargos PROPUESTOS. Es la decisión del supervisor (no de los investigadores): cada encargo es coherente
y ejecutable en UNA sesión, de UN solo entorno, con hasta cuatro piezas afines (D-11). Los investigadores
propusieron claves de lote (`lote`); este mapa las refina con el contenido de cada fila.

Entrada: un JSON {id: {lote, entorno, que_falta, hecho}} de las filas ABSORBER finales.
Salida: `grupos-pendientes-4.json` = {"encargos": {ROTULO: {"entorno","modelo","modo","piezas":{P: [ids]}}}}.
Falla en voz alta si alguna fila queda sin asignar o asignada dos veces.

    python3 arma_grupos_pendientes_4.py <absorber.json> <salida.json>
"""
import json
import sys

# clave corta de fila -> se resuelve al id completo (sufijo «-<hhhh>-<NN>» del libro; o id numérico exacto)
ENCARGOS = {
    "GEN2-TUBERIA-CENSO-Y-DEPENDENCIAS-1": {"entorno": "NUBE", "modelo": "Opus", "modo": "ABIERTO", "piezas": {
        "P1 · dependencias declaradas en requirements y CI": ["308c-03", "01aa-03", "NC-0332", "e897-04"],
        "P2 · censo de tests regenerado con ejecución real": ["8796-06", "2868-06", "19a3-06", "2518-04", "2d37-10", "3a49-06", "3fc6-03", "NC-0439"],
        "P3 · guardia de huérfanos que no salta lo ya instalado": ["NC-0381", "NC-0403"]}},
    "GEN2-TUBERIA-CORRIDA0-2": {"entorno": "NUBE", "modelo": "Opus", "modo": "ABIERTO", "piezas": {
        "P1 · caché y derivación compartida": ["baca-02", "c6d9-06", "NC-0298"],
        "P2 · ensayo y guardas de valor": ["6c10-02", "996b-08", "NC-0292"],
        "P3 · vista, canal y registro": ["18fa-02", "822a-03", "c133-02", "c133-04", "1997-03", "f18c-01"],
        "P4 · citas, manifiesto y delta": ["NC-0303", "NC-0395", "fa42-03", "NC-0048"]}},
    "GEN2-TUBERIA-TESTS-Y-CHECK-2": {"entorno": "NUBE", "modelo": "Opus", "modo": "ABIERTO", "piezas": {
        "P1 · tests que dependen del estado vivo del libro": ["NC-0396", "NC-0398", "NC-0450", "247d-02"],
        "P2 · contrato de verify y tablas de identidad": ["NC-0438", "NC-0449", "19a3-02", "7ef3-01"],
        "P3 · check.py, suite y canal de WARN": ["baca-03", "8e53-02", "6e60-07"],
        "P4 · comandos de dirección (acto.md, revisa.md)": ["9a2c-01", "6e60-02"]}},
    "GEN2-PISOS-DOMINIOS-Y-REGLAS-2": {"entorno": "CAJA", "modelo": "Opus", "modo": "ABIERTO", "piezas": {
        "P1 · serie ENSU por sexo, edad y ciudad": ["5916-02", "5916-03", "5916-04"],
        "P2 · salud y bienestar (ENSANUT 2018/2020 y afirmaciones sin CALC)": ["6d56-02", "6d56-03", "7cd0-04"],
        "P3 · pisos por NSE AMAI, consumo y empleo": ["e773-03", "2d37-03", "NC-0385"],
        "P4 · oferta financiera junto a los pisos de crédito y ahorro": ["dea2-03", "8dbe-03"]}},
    "GEN2-PISOS-DOMINIOS-Y-REGLAS-3": {"entorno": "CAJA", "modelo": "Opus", "modo": "ABIERTO", "piezas": {
        "P1 · transiciones ENOE y ámbitos y series ENDIREH": ["e422-02", "6a2c-03", "6a2c-02"],
        "P2 · política, LAPOP y SICEE": ["d459-02", "d459-03", "ac7b-07"],
        "P3 · familia, religión y regla contrastada": ["2a0e-03", "0d4a-04", "3cf7-01", "7cd0-06"],
        "P4 · árbitro de marginales con n ampliado": ["ed7d-03"]}},
    "GEN2-CALC-ALTERNOS-LOTE-2": {"entorno": "CAJA", "modelo": "Opus", "modo": "ABIERTO", "piezas": {
        "P1 · M19 con AP5_4 de ENVIPE 2025 y p17/p18 de CSES": ["795b-07", "795b-08"],
        "P2 · intervalo de L en C3 (retrospectivo) y árbitro 3D re-medido": ["NC-0307", "NC-0448"]}},
    "GEN2-RELEVO-TRAMITE-CAJA-2": {"entorno": "CAJA", "modelo": "Opus", "modo": "ABIERTO", "piezas": {
        "P1 · relevo de RES-0051/0052 (L8CONV) sin literal GEN1": ["a157-17", "a157-18", "a157-19"],
        "P2 · remesas ENIGH 2020 (spec sucesora v1.1)": ["2385-06"],
        "P3 · relevo de M13, M19, M22 y M05/M23": ["e760-10", "72d9-03"]}},
    "GEN2-CURACION-CORPUS-2": {"entorno": "CAJA", "modelo": "Opus", "modo": "ABIERTO", "piezas": {
        "P1 · reservas por módulo y payloads fuera de reserva_respondentes": ["7813-03", "01aa-01", "NC-0246"],
        "P2 · inventarios de reactivos y filas ciegas": ["3a49-02", "0d4a-03", "43d6-04", "NC-0260", "NC-0136"],
        "P3 · cola y payloads con hash (INPC, CONAPO, Intercensal, licencias)": ["e422-03", "7813-01", "0d4a-02", "3a49-03", "1997-02"],
        "P4 · CNBV y Banxico NO-ACCESIBLE con dato ya obtenido": ["8dbe-01", "8dbe-02"]}},
    "GEN2-ADQUISICION-DOCUMENTAL-1": {"entorno": "NUBE", "modelo": "Sonnet", "modo": "ABIERTO", "piezas": {
        "P1 · documentos y calendario de INEGI (ENIGH 2024, ENVIPE 2027, tabulados)": ["dd08-02", "7045-02", "2d37-05"],
        "P2 · constancias documentales NO-ENCONTRADO": ["43d6-06", "81e1-08"],
        "P3 · sondas de fuente mexicana (ledger de tandas, BNPL/CAT)": ["NC-0037", "NC-0164"],
        "P4 · corroboración externa de auditoría post hoc": ["39d2-03"]}},
    "GEN2-C1-SUCESORES-2011-2021-1": {"entorno": "CAJA", "modelo": "Opus", "modo": "RÍGIDO", "piezas": {
        "P1 · sucesores ENDIREH 2011/2021 y contrafactual": ["157c-02", "facd-02", "2385-02", "beee-04"],
        "P2 · lote 4 ENDIREH 2021 (767 identidades)": ["0c1f-03", "627e-09", "fb50-03"],
        "P3 · ENBIARE escalas -P y llaves ENCIG-MOR": ["2385-03", "2385-01"],
        "P4 · hueco v1.2 fuera de corte y IC del lote 1": ["9d28-02", "beee-06"]}},
    "GEN2-REPLAYS-Y-RECIBOS-CAJA-1": {"entorno": "CAJA", "modelo": "Opus", "modo": "RÍGIDO", "piezas": {
        "P1 · replays con corpus montado": ["8c5c-13", "970c-01"],
        "P2 · recibos técnicos con red": ["9d28-03", "8c5c-08"]}},
    "GEN2-CORRECCION-C3-1": {"entorno": "NUBE", "modelo": "Sonnet", "modo": "ABIERTO", "piezas": {
        "P1 · tablas y normalización de columnas de los reports": ["26bb-03", "8c5c-05", "8c5c-12"],
        "P2 · evidencia circular y firewall genético": ["627e-11", "627e-13", "627e-15", "627e-17", "8c5c-06"],
        "P3 · recibos de PR codex fusionados sin nota": ["ad01-04", "9d28-01", "ed83-01"],
        "P4 · cascada de archivo de RECIBO-ASTRA6-2": ["627e-05"]}},
    "GEN2-MARCADOR-Y-SERIES-2": {"entorno": "NUBE", "modelo": "Sonnet", "modo": "ABIERTO", "piezas": {
        "P1 · crosswalk y enlaces del marcador": ["c09b-02", "c09b-04", "c6f4-01", "c6f4-02", "96ee-02"],
        "P2 · ENUT núcleo y serie ENCIG": ["9f24-02", "9f24-03", "852f-02"],
        "P3 · pisos, identidad de escala y proyección del canal": ["NC-0346", "NC-0413", "63db-02", "7ef3-03"]}},
    "GEN2-PRODUCTO-CANON-2": {"entorno": "NUBE", "modelo": "Sonnet", "modo": "ABIERTO", "piezas": {
        "P1 · informe (Clopper-Pearson por ola, detalle por celda y sello de D-A)": ["48d4-04", "7357-02", "NC-0218"],
        "P2 · catálogo y «Dónde cambió el mexicano»": ["afe1-02", "facd-03", "2385-05"],
        "P3 · mapa de dominios y tablero": ["43d6-05", "NC-0055"],
        "P4 · guardia de IC declarado en toda emisión": ["48d4-03"]}},
    "GEN2-TRAMITE-ARCHIVO-2": {"entorno": "NUBE", "modelo": "Sonnet", "modo": "ABIERTO", "piezas": {
        "P1 · retro-sello y cola vieja": ["NC-0287", "0eca-02"],
        "P2 · ADR, L0 y trazabilidad de actos ya fusionados": ["NC-0339", "NC-0272", "NC-0285", "NC-0299"],
        "P3 · hoja de firma por contrato de C1": ["fb50-01"]}},
    "GEN2-FALSADOR-PLANTILLA-V22-1": {"entorno": "NUBE", "modelo": "Sonnet", "modo": "ABIERTO", "piezas": {
        "P1 · medición del falsador a tres meses del sello (no lanzar antes del 21/dic/2026)": ["NC-0418"]}},
}


def resuelve(clave, ids):
    if clave.startswith("NC-"):
        return [clave] if clave in ids else []
    return [i for i in ids if i.endswith("-" + clave)]


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    ab = json.load(open(sys.argv[1], encoding="utf-8"))
    ids = sorted(ab)
    asignado, errores, salida = {}, [], {"encargos": {}}
    for rot, d in ENCARGOS.items():
        piezas = {}
        for p, claves in d["piezas"].items():
            for c in claves:
                r = resuelve(c, ids)
                if len(r) != 1:
                    errores.append(f"{rot} · {p} · «{c}» resuelve a {len(r)} ids: {r}")
                    continue
                if r[0] in asignado:
                    errores.append(f"{r[0]} asignado dos veces: {asignado[r[0]]} y {rot}")
                asignado[r[0]] = rot
                piezas.setdefault(p, []).append(r[0])
        salida["encargos"][rot] = {"entorno": d["entorno"], "modelo": d["modelo"], "modo": d["modo"], "piezas": piezas}
    sin = [i for i in ids if i not in asignado]
    print(f"ABSORBER: {len(ids)} · asignadas: {len(asignado)} · encargos: {len(ENCARGOS)} · sin asignar: {len(sin)} · errores: {len(errores)}")
    for i in sin:
        print("  SIN ASIGNAR:", i, "|", ab[i].get("lote"), "|", (ab[i].get("que_falta") or "")[:80])
    for e in errores:
        print("  ERROR:", e)
    for rot, d in salida["encargos"].items():
        n = sum(len(v) for v in d["piezas"].values())
        print(f"  {rot}: {n} NC · {len(d['piezas'])} piezas · {d['entorno']} · {d['modelo']}")
    json.dump(salida, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return 1 if (sin or errores) else 0


if __name__ == "__main__":
    sys.exit(main())
