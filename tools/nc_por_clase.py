#!/usr/bin/env python3
"""nc_por_clase.py -- clasifica las NC ABIERTAS de `forense/no-corrido.tsv` POR LO
QUE LES FALTA (ACTO GEN2-SENAL-1 · P2).

El problema que resuelve: `forense/no-corrido.tsv` dice QUÉ no se corrió y POR QUÉ,
pero no dice QUÉ LE FALTA A CADA UNA PARA PODER CERRARSE. Con 157 filas ABIERTAS,
mesa no puede ver de un vistazo cuáles ya tienen su sucesor fusionado (y sólo
esperan que alguien lo verifique), cuáles esperan una firma, y cuáles no tienen
dueño. Sin eso se arrastra deuda ya pagada.

CERO CIFRAS TECLEADAS: toda la evidencia se deriva de
  * `forense/no-corrido.tsv`        -- las filas
  * `forense/firmas-pendientes.tsv` -- el ESTADO REAL de cada FP citada (A.17: un
                                       bloqueador citado por nombre se re-verifica
                                       de estado antes de heredarlo)
  * `forense/encargos/` y `forense/notas/` -- si el acto sucesor existe y si corrió

LO QUE ESTE SCRIPT NO HACE, por diseño: NO cierra nada. Clasificar es mecánico;
cerrar exige evidencia POR PRODUCTO (el archivo, test o fila que la NC pedía existe
hoy en main), y eso lo verifica y lo escribe un humano o un acto, una por una. Un
cierre en bloque por el solo hecho de que un PR fusionó es exactamente el defecto
que esta tabla existe para evitar.

Uso:
    python3 tools/nc_por_clase.py            # escribe el TSV derivado
    python3 tools/nc_por_clase.py --json     # mismo contenido a stdout
"""
from __future__ import annotations

import csv
import glob
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RAIZ)

NC = "forense/no-corrido.tsv"
FP = "forense/firmas-pendientes.tsv"

# ─────────────────────────────────────────────────────────────────────
# DOS ÉPOCAS DE ID `FP`, una sola gramática
# (firma de mesa D-2, 21/sep/2026 · ACTO GEN2-TUBERIA-SUCESOR-1 · P3)
#
#   vieja  `FP-###`                                  — espacio CERRADO.
#   nueva  `FP-<AAMMDD>-<RÓTULO>-<hhhh>-<NN>`        — raíz de acto.
#
# El espacio viejo se CIERRA, no se migra: ningún id viejo cambia de dueño
# y todas sus citas siguen resolviendo. Por eso la gramática acepta las
# dos y no traduce entre ellas.
#
# DEFECTO QUE ATRAPA ESTE ENSANCHAMIENTO, censado por dirección el
# 21/sep/2026: con `FP-\d+` a secas, `estado_fps()` (la lectura del
# tablero de firmas) y `clasifica()` (las FP citadas por una NC) DEJAN DE
# VER cualquier id de la época nueva. No revientan: devuelven menos, en
# silencio. Una NC bloqueada por una FP nueva se clasificaría como
# SIN-ASIGNAR en vez de ESPERA-FIRMA, y mesa vería deuda sin dueño donde
# hay una firma pendiente.
#
# ORDEN DE LA ALTERNACIA, no cosmético: la época nueva va PRIMERO. Un id
# nuevo empieza por `FP-260921…`, que la rama vieja casaría como el
# prefijo `FP-2609` si se le diera la primera oportunidad — partiendo el
# id en dos y produciendo una cita fantasma. El `(?![\d\-A-Za-z])` de la
# rama vieja es el segundo cinturón: un `FP-###` sólo casa cuando de
# verdad termina ahí.
#
# El ancho `{1,3}` de la rama vieja NO está tecleado: es el ancho real
# del espacio ya CERRADO, derivado el 21/sep/2026 de
#   cut -f1 forense/firmas-pendientes.tsv | grep -oE '^FP-[0-9]+' \\
#     | awk -F- '{print length($2)}' | sort | uniq -c
# -> 99 de ancho 2 · 291 de ancho 3 · ninguno más ancho. Como el espacio
# está cerrado (D-2), ese ancho ya no puede crecer, y acotarlo es lo que
# permite RECHAZAR una tercera época inventada (`FP-2609`, `FP-26092`)
# en vez de tragársela como un id viejo largo.
#
# Ejercida por mutación y por gramática en `tests/test_tuberia_ids_union.py`,
# con un id de CADA época pinado en el mismo caso — un patrón ensanchado
# probado sólo contra ids viejos no prueba nada.
# ─────────────────────────────────────────────────────────────────────
RE_FP_NUEVA = r"FP-\d{6}-GEN2(?:-[A-Z0-9]+)+-[0-9a-f]{4}-\d{2}"
RE_FP_VIEJA = r"FP-\d{1,3}(?![\d\-A-Za-z])"
RE_FP = rf"(?:{RE_FP_NUEVA}|{RE_FP_VIEJA})"
SALIDA = "forense/analisis/senal-1/nc-abiertas-por-clase.tsv"

# Tokens de clase (A.16: el marcador de estado vive en el campo, no en la prosa).
T_FUSIONADO = "SUCESOR-YA-FUSIONADO"
T_FIRMA = "ESPERA-FIRMA"
T_ACTO = "ESPERA-ACTO-NOMBRADO"
T_SIN = "SIN-ASIGNAR"
T_BANDEJA = "BANDEJA-TITULAR"
T_NOCLAS = "NO-CLASIFICABLE"


# Verificación POR PRODUCTO hecha a mano en ACTO GEN2-SENAL-1 (P2), fila por fila.
# NO es una constante tecleada de conveniencia: es el asiento de una lectura que
# ya ocurrió, con su razón, para que el siguiente acto no repita el trabajo ni
# confíe en el heurístico. El heurístico clasifica por el TEXTO del campo
# `sucesor`; el cierre exige el PRODUCTO. Este acto midió la distancia entre los
# dos: de las 18 filas que el heurístico marcó SUCESOR-YA-FUSIONADO, CERO
# resistieron la verificación, y las DOS que sí cerraron estaban en otra clase.
# Lección para mesa: el campo `sucesor` no predice si la deuda está pagada.
VERIFICADAS = {
    "NC-0085": "NO-RESUELTA · el sucesor es una ficha; la adopción sigue pendiente",
    "NC-0098": "NO-RESUELTA · U4 en las tres olas DBF sigue sin medirse",
    "NC-0278": "NO-RESUELTA · DIFERIDO-A acto con red; este entorno tiene la red denegada",
    "NC-0289": "NO-RESUELTA · espera pieza de mantenimiento que retire o redefina el contador",
    "NC-0311": "NO-RESUELTA · L+corpus sigue en CERO capturas",
    "NC-0316": "NO-RESUELTA · espera decisión de mesa sobre integración",
    "NC-0320": "NO-RESUELTA · espera tres decisiones de mesa",
    "NC-0321": "NO-RESUELTA · espera adopción de mesa",
    "NC-0326": "NO-RESUELTA · espera decisión de mesa para integración",
    "NC-0335": "NO-RESUELTA · MESA decide disposición",
    "NC-0356": "NO-RESUELTA · piloto 3 no selló COMMIT-3 (CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001 "
               "sólo tiene spec.yaml + adjudicacion.py, sin resultados.json ni sello)",
    "NC-0362": "NO-RESUELTA · espera FP-392 servida renglón por renglón",
    "NC-0363": "NO-RESUELTA · espera FP-391",
    "NC-0366": "NO-RESUELTA · adjudicación de canal por mesa",
    "NC-0367": "NO-RESUELTA · la celda-D del piloto 3 no se escribió",
    "NC-0407": "NO-RESUELTA · COMMIT-2 del piloto 3 sin sellar (verificado en disco)",
    "NC-0408": "NO-RESUELTA · COMMIT-3 del piloto 3 sin sellar (verificado en disco)",
    "NC-0410": "NO-RESUELTA · el par sigue RESERVADA hasta el COMMIT-3",
    "NC-0331": "NO-RESUELTA · parcial: de sus TRES tests sólo test_celda_d_piloto2_consumidor.py "
               "está cableado; test_marginales_una_variable.py NECESITA-DEPENDENCIA(numpy) y "
               "test_celda_d_piloto_consumidor.py es FALLA-DE-VERDAD",
    "NC-0381": "NO-CERRADA A PROPÓSITO · su test existe y el job lo descubre, pero lo SALTA: "
               "NECESITA-DEPENDENCIA(numpy) y numpy no está en requirements.txt (NC-0332 ABIERTA). "
               "El producto no convence: el test sigue sin correr en CI. Se reporta a mesa.",
}


def filas(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def estado_fps() -> dict[str, str]:
    """Estado real de cada FP, leído del tablero de firmas (A.12: se deriva, no
    se recuerda). Devuelve {FP-###: ESTADO}."""
    out = {}
    if not os.path.exists(FP):
        return out
    for r in filas(FP):
        fid = (r.get("id") or "").strip()
        if re.fullmatch(RE_FP, fid):
            out[fid] = (r.get("estado") or "").strip() or "(sin estado)"
    return out


def _indice(patron):
    return {os.path.basename(p): p for p in glob.glob(patron, recursive=True)}


def actos_conocidos():
    """Índice de actos por nombre GEN2-*, derivado de los nombres de archivo de
    `forense/encargos/` (existe el encargo) y `forense/notas/` (corrió y cerró)."""
    enc, notas = {}, {}
    for base, p in _indice("forense/encargos/**/*.md").items():
        for m in re.findall(r"GEN2-[A-Z0-9]+(?:-[A-Z0-9]+)*", base.upper()):
            enc.setdefault(m, p)
    for base, p in _indice("forense/notas/**/*.md").items():
        for m in re.findall(r"GEN2-[A-Z0-9]+(?:-[A-Z0-9]+)*", base.upper()):
            notas.setdefault(m, p)
    return enc, notas


def clasifica(r, fps, enc, notas):
    """Prioridad explícita: una NC puede citar varias cosas, y el token debe
    decir QUÉ LA BLOQUEA HOY, no todo lo que menciona.

      1. BANDEJA-TITULAR  -- la fila misma se enruta a una bandeja/titular.
      2. ESPERA-FIRMA     -- cita una FP que sigue ABIERTA: nada más la desbloquea.
      3. SUCESOR-YA-FUSIONADO (CANDIDATO) -- su acto sucesor tiene nota de cierre.
      4. ESPERA-ACTO-NOMBRADO -- nombra un acto que aún no corrió.
      5. SIN-ASIGNAR      -- lo dice el campo, o el campo está vacío.
      6. NO-CLASIFICABLE  -- prosa sin sucesor accionable; se declara por qué.
    """
    s = (r.get("sucesor") or "").strip()
    razon = (r.get("razon") or "").strip()
    texto = f"{s} {razon}"

    if re.search(r"bandeja|titular", texto, re.I):
        return T_BANDEJA, "la fila se enruta a una bandeja/titular", ""

    citadas = sorted(set(re.findall(RE_FP, texto)))
    abiertas = [f for f in citadas if fps.get(f, "").upper() not in ("FIRMADA", "EJECUTADA")]
    if abiertas:
        det = " · ".join(f"{f}={fps.get(f, 'NO-ENCONTRADA-EN-EL-TABLERO')}" for f in citadas)
        return T_FIRMA, f"espera {', '.join(abiertas)}", det
    if citadas:
        det = " · ".join(f"{f}={fps.get(f, 'NO-ENCONTRADA-EN-EL-TABLERO')}" for f in citadas)
        # todas las FP citadas ya están firmadas: el bloqueador nominal cayó
        nombres = sorted(set(re.findall(r"GEN2-[A-Z0-9]+(?:-[A-Z0-9]+)*", texto.upper())))
        corridos = [n for n in nombres if n in notas]
        if corridos:
            return T_FUSIONADO, f"FP firmada(s) y acto {', '.join(corridos)} con nota de cierre", det
        return T_FUSIONADO, "todas las FP citadas están FIRMADAS; falta verificar el producto", det

    nombres = sorted(set(re.findall(r"GEN2-[A-Z0-9]+(?:-[A-Z0-9]+)*", texto.upper())))
    # el acto que ABRIÓ la NC no es su sucesor
    propio = (r.get("acto") or "").strip().upper()
    nombres = [n for n in nombres if n != propio]
    if nombres:
        corridos = [n for n in nombres if n in notas]
        pendientes = [n for n in nombres if n not in notas]
        if corridos and not pendientes:
            return (T_FUSIONADO, f"acto sucesor {', '.join(corridos)} tiene nota de cierre",
                    " · ".join(f"{n} -> {os.path.basename(notas[n])}" for n in corridos))
        if corridos and pendientes:
            return (T_ACTO, f"parcial: corrió {', '.join(corridos)}; falta {', '.join(pendientes)}",
                    " · ".join(f"{n}={'CORRIÓ' if n in notas else 'NO-CORRIÓ'}" for n in nombres))
        existe = [n for n in pendientes if n in enc]
        return (T_ACTO,
                f"espera {', '.join(pendientes)}"
                + (f" (encargo EXISTE: {', '.join(existe)})" if existe else " (encargo NO-ENCONTRADO)"),
                " · ".join(f"{n}={'encargo EXISTE' if n in enc else 'encargo NO-ENCONTRADO'}"
                           for n in pendientes))

    if not s or re.search(r"\bSIN-ASIGNAR\b", s, re.I):
        return T_SIN, "el campo `sucesor` lo declara SIN-ASIGNAR o está vacío", ""

    if re.search(r"\bmesa\b|dirección|direccion", texto, re.I):
        return T_SIN, "enruta a mesa/dirección sin nombrar acto ni FP: necesita dueño", ""

    return (T_NOCLAS,
            "el campo `sucesor` es prosa sin FP, sin acto GEN2 y sin bandeja: "
            "no hay objeto verificable que decida el cierre", "")


def derivar():
    fps = estado_fps()
    enc, notas = actos_conocidos()
    todas = filas(NC)
    abiertas = [r for r in todas if (r.get("estado") or "").strip() == "ABIERTA"]
    out = []
    for r in abiertas:
        clase, falta, ev = clasifica(r, fps, enc, notas)
        out.append({
            "id": r["id"],
            "fecha": r["fecha"],
            "acto_que_la_abrio": r["acto"],
            "pr": r["pr"],
            "clase": clase,
            "que_le_falta": falta,
            "evidencia_derivada": ev,
            "pieza": (r.get("pieza") or "")[:120],
            "que_no_se_corrio": (r.get("que_no_se_corrio") or "")[:240],
            "sucesor_declarado": (r.get("sucesor") or "")[:240],
            "verificado_por_producto_en_senal_1": VERIFICADAS.get(r["id"], ""),
        })
    return {
        "universo": f"{len(abiertas)} filas ABIERTA de {len(todas)} en {NC}",
        "fps_leidas": len(fps),
        "actos_con_encargo": len(enc),
        "actos_con_nota_de_cierre": len(notas),
        "filas": out,
    }


CAMPOS = ["id", "fecha", "acto_que_la_abrio", "pr", "clase", "que_le_falta",
          "evidencia_derivada", "verificado_por_producto_en_senal_1",
          "pieza", "que_no_se_corrio", "sucesor_declarado"]


def main():
    d = derivar()
    if "--json" in sys.argv:
        print(json.dumps(d, ensure_ascii=False, indent=2))
        return
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    with open(SALIDA, "w", encoding="utf-8", newline="") as f:
        f.write(f"# DERIVADO — NO EDITAR (tools/nc_por_clase.py, ACTO GEN2-SENAL-1 · P2)\n")
        f.write(f"# universo: {d['universo']}\n")
        f.write(f"# `{T_FUSIONADO}` es CANDIDATO: no autoriza cerrar. El cierre exige\n")
        f.write(f"# evidencia POR PRODUCTO, una fila a la vez. Nunca en bloque.\n")
        f.write(f"# ACTO GEN2-SENAL-1 verifico a mano las {len(VERIFICADAS)} candidatas mas probables:\n")
        f.write(f"# CERO de las 18 SUCESOR-YA-FUSIONADO resistieron. Ver columna\n")
        f.write(f"# `verificado_por_producto_en_senal_1`. El campo `sucesor` NO predice el cierre.\n")
        w = csv.DictWriter(f, fieldnames=CAMPOS, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        for r in d["filas"]:
            w.writerow(r)
    from collections import Counter
    c = Counter(r["clase"] for r in d["filas"])
    print(f"{SALIDA}: {len(d['filas'])} filas · {d['universo']}")
    for k, v in sorted(c.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
