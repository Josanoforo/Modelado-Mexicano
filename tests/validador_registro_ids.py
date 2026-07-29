#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validador del registro congelado de IDs (Hito D) · 29/jul/2026

NO está cableado a `tests/check.py` — se corre a mano:
    python3 tests/validador_registro_ids.py

Por qué no está en la suite todavía: la suite tiene una línea base fija
(18 FAIL · 111 WARN, verificada el 29/jul/2026 contra HEAD). Añadir este
test a `check.py` movería esa línea base en el mismo momento en que el
registro de IDs se está congelando por primera vez — no se podría saber
si un cambio en el conteo viene de una regresión real o de que el test
es nuevo. Orden correcto: primero el registro se congela (esta sesión),
después, en una sesión aparte, se decide cablear este validador a la suite
contra una línea base ya estable con el test incluido.

Qué valida, a diferencia del contador de PASO 0 (que DERIVA IDs por
posición): este script NO deriva nada. Compara el archivo contra el
REGISTRO CONGELADO declarado abajo (copia de `modelo §7`, tabla
"Registro congelado de IDs") y falla si:
  (1) un ID deja de apuntar a la misma regla (el ancla de texto ya no
      aparece en la sección que le corresponde),
  (2) el tier de esa regla cambió respecto al registrado,
  (3) el conteo de reglas por sección cambió (se agregó o quitó una regla
      sin actualizar el registro),
  (4) el perímetro (suma de tiers en {FUERTE, FUERTE como correlación,
      FUERTE / MEDIA, MEDIA-FUERTE}) ya no da 27,
  (5) aparece un tier fuera del vocabulario sancionado de 7 etiquetas.

**La identidad de cada ID es el texto (subcadena de su `SI`), no la línea.**
El número de línea que se reporta en los mensajes de FALLA es diagnóstico
—para que quien lea el error sepa dónde mirar—, nunca la clave de búsqueda:
`REGISTRO` no contiene números de línea en absoluto, y el emparejamiento
(línea 187) es `anchor in texto_de_la_regla`, dentro de la sección que
corresponde. Si el archivo se reedita y las reglas se desplazan, el ID
sigue el texto, no la posición — es la propiedad que el registro congelado
existe para garantizar (ver `modelo §7`, PASO 2 de la sesión del 29/jul).
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

VOCABULARIO_SANCIONADO = {
    "[FUERTE]", "[MEDIA]", "[MEDIA-FUERTE]", "[HIPÓTESIS]",
    "[FUERTE como correlación]", "[FUERTE / MEDIA]", "[MEDIA / HIPÓTESIS]",
}
PERIMETRO = {
    "[FUERTE]", "[FUERTE como correlación]", "[FUERTE / MEDIA]", "[MEDIA-FUERTE]",
}

# ─────────────────────────────────────────────────────────────────────
# REGISTRO CONGELADO — copia de `modelo §7`, tabla "Registro congelado
# de IDs" (v3.3, cambio 35). Si esta tabla cambia en `modelo`, este
# bloque se actualiza a mano y en el mismo commit — nunca se recomputa
# automáticamente, ese es el punto del registro congelado.
#   anchor: substring estable tomado del propio texto de la regla,
#   suficiente para identificarla sin ambigüedad dentro de su sección.
# ─────────────────────────────────────────────────────────────────────
REGISTRO = [
    ("R1.1", "3.1", "[FUERTE]", "el ingreso es volátil/informal"),
    ("R1.2", "3.1", "[FUERTE]", "hay empleo formal e ingreso estable"),
    ("R1.3", "3.1", "[FUERTE]", "canal de confianza personal** (recomendación"),
    ("R1.4", "3.1", "[FUERTE como correlación]", "movilidad real bloqueada"),
    ("R1.5", "3.1", "[MEDIA]", "seguro de depósito visible"),
    ("R1.6", "3.1", "[MEDIA]", "efectivo o tarjeta de alto CAT"),
    ("R1.7", "3.1", "[MEDIA]", "baja fricción de acceso"),
    ("R2.1", "3.2", "[FUERTE]", "jerarquía tradicional/empresa familiar"),
    ("R2.2", "3.2", "[MEDIA-FUERTE]", "liderazgo es **benévolo**"),
    ("R2.3", "3.2", "[MEDIA]", "prestaciones formales (IMSS, Infonavit)"),
    ("R2.4", "3.2", "[MEDIA]", "trabajador es joven urbano"),
    ("R3.1", "3.3", "[FUERTE]", "trámite es presencial con funcionario discrecional"),
    ("R3.2", "3.3", "[FUERTE]", "trámite se digitaliza"),
    ("R3.3", "3.3", "[MEDIA]", "norma se percibe como inútil"),
    ("R3.4", "3.3", "[MEDIA-FUERTE]", "coercitiva y con riesgo fiscal"),
    ("R4.1", "3.4", "[FUERTE]", "padecimiento es leve-moderado y no hay IMSS"),
    ("R4.4", "3.4", "[MEDIA]", "síntoma es grave o crónico complejo"),
    ("R4.2", "3.4", "[FUERTE]", "hombre trabajador sin permiso laboral"),
    ("R4.3", "3.4", "[FUERTE / MEDIA]", "hay desabasto + gasto de bolsillo alto"),
    ("R4.5", "3.4", "[MEDIA]", "producto tiene sellos"),
    ("R5.1", "3.5", "[FUERTE]", "ingreso volátil / ausencia de Estado"),
    ("R5.2", "3.5", "[FUERTE]", "se trata de cuidado (mayores, niños, enfermos)"),
    ("R5.3", "3.5", "[MEDIA]", "baja garantía institucional del matrimonio"),
    ("R5.4", "3.5", "[MEDIA / HIPÓTESIS]", "cortejo es urbano-joven-conectado"),
    ("R6.1", "3.6", "[MEDIA]", "cita es formal-laboral con checador"),
    ("R6.2", "3.6", "[HIPÓTESIS]", "invitación social y decir \"no\""),
    ("R6.3", "3.6", "[MEDIA]", "recursos escasos y urgencias compitiendo"),
    ("R6.4", "3.6", "[MEDIA]", "cita médica/trámite con costo por faltar"),
    ("R7.1", "3.7", "[FUERTE]", "votante percibe que el acto **pesa**"),
    ("R7.2", "3.7", "[FUERTE]", "delito no tiene cobertura de seguro"),
    ("R7.3", "3.7", "[FUERTE]", "Y NO** hay proximidad/focalización del reparto"),
    ("R7.6", "3.7", "[MEDIA]", "proximidad/focalización del reparto** **O**"),
    ("R7.7", "3.7", "[MEDIA]", "dádiva o transferencia **Y** el partido puede monitorear"),
    ("R7.8", "3.7", "[HIPÓTESIS]", "se vive como derecho**"),
    ("R7.9", "3.7", "[MEDIA]", "atribución va al líder"),
    ("R7.4", "3.7", "[MEDIA-FUERTE]", "entorno es **urbano con espacio público disponible**"),
    ("R7.5", "3.7", "[MEDIA-FUERTE]", "se suma a **autodefensa**"),
    ("R8.1", "3.8", "[FUERTE]", "comité con liderazgo confiable + monitoreo"),
    ("R8.2", "3.8", "[FUERTE]", "conoce personalmente a la organizadora"),
    ("R8.3", "3.8", "[FUERTE]", "hay un puente personal (conocido en común"),
    ("R8.4", "3.8", "[MEDIA]", "pueblo mestizo con faena/cooperación normada"),
    ("R9.3", "3.9", "[MEDIA]", "información la reenvía un **allegado de confianza**"),
    ("R9.1", "3.9", "[FUERTE]", "experto formal es accesible, cercano y asequible"),
    ("R9.2", "3.9", "[FUERTE]", "vacuna/servicio está disponible"),
    ("R9.4", "3.9", "[MEDIA]", "hogar es clase media con miedo a caer"),
    ("R10.1", "3.10", "[FUERTE]", "hay que emitir un rechazo"),
    ("R10.2", "3.10", "[MEDIA-FUERTE]", "da retroalimentación negativa"),
    ("R10.3", "3.10", "[FUERTE]", "contexto es de inseguridad/autoridad no confiable"),
    ("R10.4", "3.10", "[MEDIA]", "interlocutor es norteño/joven-urbano"),
]
PERIMETRO_ESPERADO = 27
TOTAL_ESPERADO = 49


def newest_modelo():
    import glob
    hits = sorted(glob.glob(os.path.join(ROOT, "canon", "modelo-decision-v*.md")))
    if not hits:
        return None
    return hits[-1]


def parse_rules(path):
    text = io.open(path, encoding="utf-8").read()
    lines = text.split("\n")
    section_starts = []
    start = end = None
    for i, l in enumerate(lines):
        m = re.match(r"^### (3\.\d+) ", l)
        if m:
            if start is None:
                start = i
            section_starts.append((i, m.group(1)))
        if l.startswith("## 4 ") and start is not None:
            end = i
            break
    if end is None:
        end = len(lines)

    def section_for(idx):
        cur = None
        for i, sec in section_starts:
            if i <= idx:
                cur = sec
            else:
                break
        return cur

    tier_re = re.compile(r"`(\[[^\]]*\])`")
    rules = []  # (global_line_1indexed, section, tier, text)
    for offset in range(start, end):
        l = lines[offset]
        if not l.lstrip().startswith("- **SI**"):
            continue
        m = tier_re.search(l)
        tier = m.group(1) if m else None
        rules.append((offset + 1, section_for(offset), tier, l))
    return rules


def main():
    path = newest_modelo()
    if not path:
        print("ERROR: no se encontró canon/modelo-decision-v*.md", file=sys.stderr)
        return 1

    rules = parse_rules(path)
    ok = True

    # (1) vocabulario sancionado
    for ln, sec, tier, _ in rules:
        if tier is None:
            print(f"FALLA: regla sin tier detectable en L{ln}")
            ok = False
        elif tier not in VOCABULARIO_SANCIONADO:
            print(f"FALLA: tier fuera del vocabulario sancionado en L{ln}: {tier}")
            ok = False

    # (2) total y perímetro derivados del archivo real
    total_real = len(rules)
    perimetro_real = sum(1 for _, _, t, _ in rules if t in PERIMETRO)
    if total_real != TOTAL_ESPERADO:
        print(f"FALLA: total de reglas es {total_real}, se esperaban {TOTAL_ESPERADO}")
        ok = False
    if perimetro_real != PERIMETRO_ESPERADO:
        print(f"FALLA: perímetro es {perimetro_real}, se esperaban {PERIMETRO_ESPERADO}")
        ok = False

    # (3) cada ID del registro sigue apuntando a la misma regla, mismo tier
    rules_by_section = {}
    for ln, sec, tier, text in rules:
        rules_by_section.setdefault(sec, []).append((ln, tier, text))

    seen_lines = set()
    for rid, sec, tier_esperado, anchor in REGISTRO:
        candidatos = [r for r in rules_by_section.get(sec, []) if anchor in r[2]]
        if not candidatos:
            print(f"FALLA: {rid} — el ancla de texto ya no aparece en §{sec}: "
                  f"{anchor!r}")
            ok = False
            continue
        if len(candidatos) > 1:
            print(f"FALLA: {rid} — el ancla de texto es ambigua en §{sec} "
                  f"({len(candidatos)} reglas la contienen): {anchor!r}")
            ok = False
            continue
        ln, tier_real, _ = candidatos[0]
        if tier_real != tier_esperado:
            print(f"FALLA: {rid} (L{ln}) — tier cambió de {tier_esperado} a {tier_real}")
            ok = False
        seen_lines.add(ln)

    # (4) conteo del registro coincide con conteo real (nada se agregó/quitó sin registrarlo)
    if len(REGISTRO) != TOTAL_ESPERADO:
        print(f"FALLA: el registro congelado tiene {len(REGISTRO)} filas, "
              f"se esperaban {TOTAL_ESPERADO}")
        ok = False

    unregistered = [(ln, sec, tier, text[:70]) for ln, sec, tier, text in rules
                     if ln not in seen_lines]
    if unregistered:
        print(f"FALLA: {len(unregistered)} regla(s) en el archivo sin ID "
              f"en el registro congelado:")
        for ln, sec, tier, snippet in unregistered:
            print(f"    L{ln}  §{sec}  {tier}  {snippet}")
        ok = False

    perimetro_registrado = sum(1 for _, _, t, _ in REGISTRO if t in PERIMETRO)
    if perimetro_registrado != PERIMETRO_ESPERADO:
        print(f"FALLA: el registro congelado marca {perimetro_registrado} "
              f"reglas de perímetro, se esperaban {PERIMETRO_ESPERADO}")
        ok = False

    if ok:
        print(f"OK — {path[len(ROOT)+1:]}")
        print(f"  {total_real} reglas · {perimetro_real} en perímetro · "
              f"{len(REGISTRO)} IDs verificados, todos con ancla y tier consistentes")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
