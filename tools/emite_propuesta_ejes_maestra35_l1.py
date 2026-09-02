#!/usr/bin/env python3
"""ACTO MAESTRA35-L1 · emite las tres entradas de propuesta de P2, P3 y P4.

Existe para que las 55 celdas con IC no se transcriban a mano al YAML: importa
los tres `main_ejes()` y serializa lo que devuelven. El bootstrap tiene seed
fija (42), asi que estos numeros son BIT A BIT los mismos que imprimio la
corrida unica de cada pieza -- no es un reintento, es la misma corrida
serializada; el acto lo verifica por diff contra la salida impresa.

Uso: python3 tools/emite_propuesta_ejes_maestra35_l1.py > bloque.yaml
"""
import contextlib
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import medidor_ahorro_enif24 as m_enif          # noqa: E402
import medidor_evasion_norma_envipe25 as m_env  # noqa: E402
import medidor_gobierno_digital_encig25 as m_enc  # noqa: E402

SHA = {
    "enif": "00e4b0b42775276b2da236a5bba8c64dc5a92c289908a4727dec93dc7684f039",
    "encig": "47daf2f732366ad842b7f60c784be9d61db68a00ae1a693980ec6a683e0d9e12",
    "envipe": "8a7a99fd90ce9d03229759ba0ad84db4fba98b5bb1f5c85eef7d718b007816fa",
}
MID = {"enif": "enif_2024_enif_2024_bd_csv", "encig": "encig25_base_datos_csv",
       "envipe": "envipe2025_csv"}


def celdas_yaml(res, sangria):
    s = " " * sangria
    out = []
    for r in res:
        out.append(f"{s}- eje: {r['eje']}")
        out.append(f"{s}  cobertura: {r['cobertura']:.6f}")
        if r["cobertura"] < 0.90:
            out.append(f"{s}  universo_restringido: true   "
                       f"# A-bis 4: no reconcilia contra el marginal poblacional")
        out.append(f"{s}  signo_pre_registrado: "
                   f"{r['signo'] if r['signo'] else 'null'}")
        out.append(f"{s}  veredicto: \"{r['veredicto']}\"")
        out.append(f"{s}  monotonia: \"{r['monotonia']}\"")
        out.append(f"{s}  nota: >-")
        for linea in _envuelve(r["nota"], 66):
            out.append(f"{s}    {linea}")
        out.append(f"{s}  celdas:")
        for c in r["celdas"]:
            if c["n"] == 0:
                out.append(f"{s}    - {{celda: \"{c['celda']}\", n: 0}}")
                continue
            out.append(
                f"{s}    - {{celda: \"{c['celda']}\", p: {c['p']:.6f}, "
                f"ic95: [{c['lo']:.6f}, {c['hi']:.6f}], n: {c['n']}, "
                f"numerador: {c['n_num']}, estratos: {c['n_est']}, "
                f"upm: {c['n_upm']}}}")
    return out


def _envuelve(texto, ancho):
    palabras, linea, salida = texto.split(), "", []
    for p in palabras:
        if len(linea) + len(p) + 1 > ancho:
            salida.append(linea)
            linea = p
        else:
            linea = f"{linea} {p}".strip()
    if linea:
        salida.append(linea)
    return salida


def main():
    silencio = io.StringIO()
    with contextlib.redirect_stdout(silencio):
        p2 = m_enif.main_ejes()
        p3 = m_enc.main_ejes()
        p4 = m_env.main_ejes()

    L = []
    A = L.append
    A("  # ══════════════════════════════════════════════════════════════════")
    A("  # ACTO MAESTRA35-L1 · RECORRE-Y-SEGMENTA · 2/sep/2026")
    A("  # Tres entradas NUEVAS: los disparadores de tres reglas ya medidas por")
    A("  # MAESTRA34-L5, ahora MEDIDOS por ejes de segmentación. Ninguna se")
    A("  # carga al motor: el sello es de mesa, en RH. La cuarta pieza de este")
    A("  # acto (P1) es una enmienda in situ, arriba, no una entrada nueva.")
    A("  # Codificación de cada eje: censo P0 (forense/notas/"
      "2026-09-02-MAESTRA35-L1-P0-censo.md),")
    A("  # leída del FD o del catálogo de cada payload. Spec congelada:")
    A("  # forense/notas/2026-09-02-MAESTRA35-L1-spec.md.")
    A("  # Cada celda es una ASOCIACIÓN, no un coeficiente (A-bis 1); un IC")
    A("  # estrecho con signo esperado NO autoriza leer un efecto (A-bis 2).")
    A("  # ══════════════════════════════════════════════════════════════════")

    A("  - id: dinero.ahorro.via_informal_ejes_enif2024")
    A("    entrada_nueva: true")
    A("    acto: \"MAESTRA35-L1 · P2\"")
    A("    fuente_regla: \"dinero.ahorro.via_informal — mecanismo G3 / "
      "informal_sin_puente\"")
    A("    payload: ENIF 2024 · TMODULO.csv · unidad = PERSONA elegida 18+")
    A("    ponderador: FAC_PER")
    A("    estrato: EST_DIS")
    A("    upm: UPM_DIS")
    A("    estimador: \"bootstrap conglomerado estratificado, 10 000 réplicas, "
      "seed 42\"")
    A("    desenlaces:")
    for etiqueta, res in p2.items():
        clave = ("principal" if "PRINCIPAL" in etiqueta else "secundario")
        defin = ("alguna P5_1_1..P5_1_6 == '1' Y ninguna P5_6_1..P5_6_9 == '1'"
                 if clave == "principal"
                 else "alguna P5_1_1..P5_1_6 == '1'")
        A(f"      {clave}:")
        A(f"        definicion: \"{defin}\"")
        A(f"        nombre: \"{etiqueta.split(' (')[0]}\"")
        A("        ejes:")
        L.extend(celdas_yaml(res, 10))
    A("    hallazgo: >")
    for linea in _envuelve(HALLAZGO_P2, 68):
        A(f"      {linea}")
    A("    situacion: PENDIENTE-DE-MESA")
    A("    tier: PENDIENTE-DE-MESA")
    A(f"    sha256_payload: \"{SHA['enif']}\"")
    A(f"    payload_manifiesto_id: {MID['enif']}")
    A("")

    A("  - id: tramite.gobierno_digital.util_sin_coercion_ejes_encig2025")
    A("    entrada_nueva: true")
    A("    acto: \"MAESTRA35-L1 · P3\"")
    A("    fuente_regla: \"tramite.gobierno_digital.util_sin_coercion — "
      "desenlace y universo EXACTOS de MAESTRA34-L5 P1, sin tocar la "
      "dicotomización\"")
    A("    payload: \"ENCIG 2025 · encig2025_04_sec_7.csv · unidad = TRÁMITE "
      "(quien pagó doce veces contribuye doce veces)\"")
    A("    universo: \"N_TRA=='01'; adopta = P7_3 ∈ {4,5}; no adopta {1,2,6}; "
      "fuera {3,7,8,9,blanco}; n = 20 203\"")
    A("    llave_a_los_ejes: \"ID_TRA --(sec_7)--> ID_PER --> "
      "encig2025_02_residentes_sec_2.csv · 0 huérfanos\"")
    A("    ponderador: FAC_TRA")
    A("    estrato: EST_DIS")
    A("    upm: UPM_DIS")
    A("    ejes:")
    L.extend(celdas_yaml(p3, 6))
    A("    ejes_ausentes: >")
    for linea in _envuelve(AUSENTES_P3, 68):
        A(f"      {linea}")
    A("    hallazgo: >")
    for linea in _envuelve(HALLAZGO_P3, 68):
        A(f"      {linea}")
    A("    situacion: PENDIENTE-DE-MESA")
    A("    tier: PENDIENTE-DE-MESA")
    A(f"    sha256_payload: \"{SHA['encig']}\"")
    A(f"    payload_manifiesto_id: {MID['encig']}")
    A("")

    A("  - id: tramite.evasion_norma_ejes_envipe2025")
    A("    entrada_nueva: true")
    A("    acto: \"MAESTRA35-L1 · P4\"")
    A("    fuente_regla: \"tramite.evasion_norma — desenlace y universo "
      "EXACTOS de MAESTRA34-L5 P3\"")
    A("    payload: \"ENVIPE 2025 · tmod_vic · unidad = DELITO\"")
    A("    universo: \"BP1_20 ∈ {1,2}; evade_norma = BP1_20=='2' Y BP1_23 ∈ "
      "{04,05,06,08} — la CONJUNTA, no la condicional; n = 40 280\"")
    A("    llave_a_los_ejes: \"ID_PER (tmod_vic -> tsdem) · 0 huérfanos; "
      "sexo y edad viven en tmod_vic y no necesitan el join\"")
    A("    ponderador: FAC_DEL")
    A("    estrato: EST_DIS")
    A("    upm: UPM_DIS")
    A("    ejes:")
    L.extend(celdas_yaml(p4, 6))
    A("    ejes_ausentes: >")
    for linea in _envuelve(AUSENTES_P4, 68):
        A(f"      {linea}")
    A("    hallazgo: >")
    for linea in _envuelve(HALLAZGO_P4, 68):
        A(f"      {linea}")
    A("    situacion: PENDIENTE-DE-MESA")
    A("    tier: PENDIENTE-DE-MESA")
    A(f"    sha256_payload: \"{SHA['envipe']}\"")
    A(f"    payload_manifiesto_id: {MID['envipe']}")
    print("\n".join(L))


HALLAZGO_P2 = (
    "El mecanismo G3 / informal_sin_puente sobrevive en DOS ejes y se rompe "
    "en los demás, y la rotura es informativa. Contra el desenlace PRINCIPAL "
    "(ahorro exclusivamente informal), localidad y formalidad salen "
    "CORROBORADAS con IC95 sin traslape y en el signo pre-registrado. "
    "Escolaridad sale CONTRARIA por la regla de precedencia de la spec: sus "
    "celdas EXTREMAS sí van en el signo esperado (0.3516 en hasta-primaria vs "
    "0.2604 en superior), pero el par hasta-primaria -> secundaria va limpio "
    "en sentido opuesto (0.3516 -> 0.4156, IC95 sin traslape), el eje es NO "
    "MONÓTONO y CONTRARIA manda. Leer solo los extremos habría dado "
    "CORROBORADA: la regla de precedencia atrapó exactamente el caso para el "
    "que se escribió. Contra el desenlace SECUNDARIO (ahorro informal de "
    "cualquier tipo, que NO está anidado en la tenencia de cuenta y por eso "
    "es el falsable), el mecanismo se cae entero: escolaridad, formalidad y "
    "cuenta salen las tres CONTRARIA, y localidad NO-DISCRIMINA. Quien tiene "
    "cuenta ahorra informalmente MÁS (0.5979 vs 0.4935), no menos; quien "
    "tiene seguridad social por su trabajo también (0.6447 vs 0.6041); y el "
    "ahorro informal SUBE con la escolaridad (0.4141 -> 0.6401). La lectura "
    "que estos números soportan es que el ahorro informal en México no es un "
    "sustituto de la exclusión formal sino un COMPLEMENTO del ahorro formal; "
    "lo que el desenlace exclusivo capta no es 'ahorrar informalmente' sino "
    "la AUSENCIA de la pata formal, que el cuestionario gatea por tenencia de "
    "cuenta. Todo esto es asociación dentro de una corrida, no efecto.")
HALLAZGO_P3 = (
    "Los dos ejes con signo pre-registrado salen CORROBORADOS y el eje sin "
    "signo no discrimina. Escolaridad es el gradiente más limpio de todo el "
    "lote: 0.3920 en hasta-primaria, 0.5646 en secundaria, 0.6786 en media "
    "superior, 0.8129 en superior, monótono y con los cuatro IC95 sin "
    "traslape entre consecutivos. Edad va en el signo esperado entre extremos "
    "(0.7518 en 18-29 vs 0.4758 en 60+) aunque no es monótona en el primer "
    "par (30-44 mide 0.7747, más alto que 18-29, con IC95 traslapados: no es "
    "un par limpio en contra y por eso no dispara la precedencia). Sexo no "
    "discrimina. La regla util_sin_coercion tenía disparadores ASIGNADOS y "
    "sin medir; ahora tiene dos medidos. Sigue siendo asociación: quien tiene "
    "más escolaridad adopta más, y este acto NO dice que la escolaridad cause "
    "la adopción.")
HALLAZGO_P4 = (
    "Los cuatro ejes DISCRIMINAN y ninguno puede corroborar: así se "
    "pre-registró, por la fuente y no por el resultado. El único gradiente "
    "grande es el de dominio, y apunta al revés de la corazonada que el "
    "encargo había escrito sobre el corte de 15 000: la evasión de norma es "
    "MÁS alta en lo urbano (0.5927) que en lo rural (0.4033), con complemento "
    "urbano en medio (0.5221) y los tres IC95 sin traslape. Como el eje NO es "
    "el corte de 15 000 -- ENVIPE no publica umbral y R <-> 'menor de 15 000' "
    "no está verificado en ninguna fuente del payload --, esto NO se reporta "
    "como CONTRARIA a la predicción del encargo: si mesa acepta leer R como "
    "localidad pequeña, el signo esperado quedaría invertido, y esa lectura "
    "es de mesa, no del ejecutor. Escolaridad, que entra como PROXY de la "
    "formalidad laboral ausente, discrimina sin patrón monótono (0.4932 / "
    "0.5674 / 0.5434 / 0.5901): consistente con que subsistencia y cinismo "
    "empujen en sentidos opuestos, que es justo por lo que la regla no "
    "predice signo ahí. Hombres evaden más que mujeres (0.5974 vs 0.5307).")
AUSENTES_P3 = (
    "tamaño de localidad y formalidad laboral, ambos NO-ENCONTRADO y ninguno "
    "sustituido. El primero por diseño muestral: el universo de ENCIG es la "
    "población de 18 años y más en ciudades de 100 mil habitantes o más (FD, "
    "pág. 1). El segundo por ausencia de ítem: la tabla de residentes cierra "
    "en POS (posición en la ocupación) y el FD no trae prestaciones ni "
    "seguridad social — sondas con control positivo sobre 4 540 líneas.")
AUSENTES_P4 = (
    "formalidad laboral y tamaño de localidad al corte de 15 000, ambos "
    "NO-ENCONTRADO. La formalidad porque ni el FD (7 207 líneas) ni el "
    "cuestionario principal (987 líneas) traen ítem de prestaciones o "
    "seguridad social — se usa escolaridad como PROXY, dicho proxy, que es la "
    "salida que el propio encargo declaró. El corte de 15 000 porque ENVIPE "
    "2025 no publica TLOC ni umbral alguno: 6 diccionarios (2 225 líneas) y "
    "el FD solo dan DOMINIO como U/C/R sin población. No se inventa el corte.")

if __name__ == "__main__":
    main()
