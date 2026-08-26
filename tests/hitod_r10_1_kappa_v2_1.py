#!/usr/bin/env python3
"""HITO D · R10.1 — Fase B de ACTO CORRE-R10.1-v2: kappa, consenso, recuento.

Extiende el patron de tests/hitod_r10_1_rechazo_poder.py (COMMIT B) al
esquema de la spec sucesora `forense/hitoD-R10_1-spec-v2_0-PROPUESTA.md`:

  §3.3  Cohen's kappa entre los dos codificadores, en DOS niveles.
  §3.4  Gate: kappa >= 0.60 en Nivel 1 habilita conteo por consenso.
        kappa < 0.60 -> D de instrumento, sin forzar consenso.
  §2.5  Las unidades NO-RECHAZO se EXCLUYEN del denominador de la tasa
        y se REPORTAN con su motivo, por brazo.
  §4.1  Arbol de ramas 1-5 sobre el IC95% de la diferencia.

Todo el computo es puro: no toca data/raw ni la red. Las dos codificaciones
se declaran en el propio archivo para que la corrida sea reproducible a mano.
"""
import os
import sys

from scipy import stats as sps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAL = os.path.join(ROOT, "forense", "notas",
                   "2026-08-26-r10-1-corrida-v2_1-salida.txt")
OUT = open(SAL, "w", encoding="utf8")
UMBRAL_PP = 15.0

# ── CODIFICACION 1 ────────────────────────────────────────────────────
# Ejecutor de ACTO CORRE-R10.1-v2, sellada por sha256 en la Fase A ANTES de
# existir la codificacion 2 (forense/hitoD-R10_1-codificacion1-v2_1.md §1).
# Texto en claro: /home/pc0/mm-corre-r10-1-SELLO/codificacion1-codigos.tsv
# sha256 = dae1048de7e4a04ac8ece168dc3d8f0f6fde64e28675069e9716c4fced33ec90
COD1 = {
    "U01": ("+P", "NO-RECHAZO", "NO-RECHAZO"),
    "U02": ("+P", "INDIRECTO",  "APLAZAMIENTO"),
    "U03": ("+P", "INDIRECTO",  "EXCUSA"),
    "U04": ("+P", "INDIRECTO",  "ALTERNATIVA"),
    "U05": ("+P", "INDIRECTO",  "EXCUSA"),
    "U06": ("+P", "INDIRECTO",  "EXCUSA"),
    "U07": ("-P", "NO-RECHAZO", "NO-RECHAZO"),
    "U08": ("-P", "NO-RECHAZO", "NO-RECHAZO"),
    "U09": ("-P", "DIRECTO",    "DIRECTO"),
    "U10": ("-P", "NO-RECHAZO", "NO-RECHAZO"),
    "U11": ("-P", "DIRECTO",    "DIRECTO"),
    "U12": ("-P", "INDIRECTO",  "ALTERNATIVA"),
}

# ── CODIFICACION 2 ────────────────────────────────────────────────────
# Jonatan Guadarrama, segundo codificador designado por mesa (RANURA 1 del
# lanzamiento v2). Ingesta VERBATIM del relanzamiento del 26/ago/2026, que
# la adjunto con la linea de compuerta F0-B exigida por el encargo.
COD2 = {
    "U01": ("+P", "NO-RECHAZO", "NO-RECHAZO"),
    "U02": ("+P", "NO-RECHAZO", "NO-RECHAZO"),
    "U03": ("+P", "INDIRECTO",  "EXCUSA"),
    "U04": ("+P", "INDIRECTO",  "ALTERNATIVA"),
    "U05": ("+P", "INDIRECTO",  "EXCUSA"),
    "U06": ("+P", "INDIRECTO",  "EXCUSA"),
    "U07": ("-P", "NO-RECHAZO", "NO-RECHAZO"),
    "U08": ("-P", "NO-RECHAZO", "NO-RECHAZO"),
    "U09": ("-P", "DIRECTO",    "DIRECTO"),
    "U10": ("-P", "NO-RECHAZO", "NO-RECHAZO"),
    "U11": ("-P", "INDIRECTO",  "EXCUSA"),
    "U12": ("-P", "INDIRECTO",  "EXCUSA"),
}

# ── CONSENSO (§3.4) ───────────────────────────────────────────────────
# Solo se puebla si el gate de Nivel 1 aprueba. Cada entrada lleva a quien
# se resuelve y por que regla; las unidades sin discrepancia no aparecen.
CONSENSO = {
    "U02": ("NO-RECHAZO", "NO-RECHAZO", "cod2",
            "2.5 dispara: el estudiante nunca niega —pregunta por la "
            "posibilidad de posponer— y la interaccion cierra con el "
            "estudiante ACEPTANDO la contrapropuesta del asesor "
            "('lo analicemos con calma' / 'Me parece bien'). Satisface dos "
            "gatillos literales de 2.5: 'termina aceptando' y 'aplazando sin "
            "resolver hacia el rechazo'. La objecion de cod1 —que 2.5 vaciaria "
            "al subtipo APLAZAMIENTO de 2.2— es de diseno del esquema, no "
            "evidencia sobre este turno: 2.2 conserva los casos donde el "
            "aplazamiento del rechazante es la ultima palabra y el peticionario "
            "desiste."),
    "U11": ("DIRECTO", "DIRECTO", "cod1",
            "Prueba de remocion de 2.1: el primer turno de Lisandro ('todavia "
            "no acabo de comer, y la clase empieza en diez minutos') NO consuma "
            "el rechazo —Jorge sigue insistiendo cuatro turnos mas—; el que lo "
            "consuma es 'Me cay que no puedo, guey, por mas que intente, no..', "
            "tras el cual Jorge desiste. Las razones que cod2 cita son adjuntos "
            "de un turno distinto del acto nuclear. La razon adyacente al acto "
            "nuclear ('no me gusta salir de mi clase') es INTERNA, y 2.2/2.3 "
            "exigen razon EXTERNA para que la negacion deje de contar directa. "
            "La nota del propio cod2 las rotula 'externas/personales'."),
    "U12": ("INDIRECTO", "ALTERNATIVA", "cod1",
            "Nivel 1 ya coincidia (INDIRECTO): esta discrepancia es de Nivel 2 "
            "y NO mueve el denominador ni la tasa. Se resuelve a ALTERNATIVA "
            "porque el cierre de Jorge —'Pues, sale, entons’ te espero'— "
            "responde a la opcion que Omar ofrecio ('ve tu y yo te alcanzo, "
            "termino mi clase'), no a la razon. Reserva: la lectura EXCUSA de "
            "cod2 ('voy retrasado en esta materia', 'primero los deberes') es "
            "defendible y viaja escrita."),
}

MOTIVO_NR = {
    "U01": "2.5 (a) termina aceptando: 'ya si la tengo que tomar, pues la tomo'",
    "U02": "2.5 por consenso: cierra aceptando 'lo analicemos con calma'",
    "U07": "2.5 (a) termina aceptando: acuerdan hora y lugar para los apuntes",
    "U08": "2.5 (a) termina aceptando: 'Pos orale'",
    "U10": "2.5 nombrada en la propia regla (Rechazo 10): 'si salgo antes, pues llego'",
}


def log(m=""):
    print(m)
    OUT.write(m + "\n")


def kappa(a, b):
    """Cohen's kappa sin ponderar. Devuelve (kappa, po, pe, n, categorias)."""
    n = len(a)
    cats = sorted(set(a) | set(b))
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    pe = sum((a.count(c) / n) * (b.count(c) / n) for c in cats)
    k = (po - pe) / (1 - pe) if pe < 1 else float("nan")
    return k, po, pe, n, cats


def matriz(a, b, cats, etiqueta):
    log("    matriz de confusion (%s) — filas cod1, columnas cod2:" % etiqueta)
    anc = max(len(c) for c in cats) + 1
    log("      %-*s | %s" % (anc, "", " ".join("%-*s" % (anc, c) for c in cats)))
    for r in cats:
        fila = [sum(1 for x, y in zip(a, b) if x == r and y == c) for c in cats]
        log("      %-*s | %s" % (anc, r, " ".join("%-*d" % (anc, v) for v in fila)))


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / d
    return (c - h, c + h)


log("=" * 78)
log("HITO D · R10.1 — FASE B de ACTO CORRE-R10.1-v2 · kappa, consenso, recuento")
log("spec: forense/hitoD-R10_1-spec-v2_0-PROPUESTA.md (SELLADA, FP-128)")
log("entorno: UBUNTU · computo puro, sin corpus ni red")
log("=" * 78)
log()

UNI = sorted(COD1)
assert sorted(COD2) == UNI, "las dos codificaciones no cubren las mismas unidades"
for u in UNI:
    assert COD1[u][0] == COD2[u][0], "brazo discrepante en " + u

log("§1 · LAS DOS CODIFICACIONES, LADO A LADO")
log("  %-5s %-6s | %-12s %-13s | %-12s %-13s | %s"
    % ("unid", "brazo", "cod1 N1", "cod1 N2", "cod2 N1", "cod2 N2", "acuerdo"))
for u in UNI:
    p, a1, a2 = COD1[u]
    _, b1, b2 = COD2[u]
    ac = ("N1+N2" if (a1, a2) == (b1, b2)
          else ("solo N1" if a1 == b1 else "NINGUNO"))
    log("  %-5s %-6s | %-12s %-13s | %-12s %-13s | %s"
        % (u, p, a1, a2, b1, b2, ac))
log()

# ── §2 · KAPPA, DOS NIVELES, DOS UNIVERSOS ────────────────────────────
log("§2 · COHEN'S KAPPA (spec §3.3) — dos niveles")
log("  El universo de 11 excluye U10, PRE-REGISTRADA en la Fase A como")
log("  pre-decidida para ambos codificadores: la regla 2.5 nombra 'Rechazo 10'")
log("  dentro del esquema, y el esquema viajo verbatim en el paquete.")
log("  Es DIAGNOSTICO. El gate de §3.4 es el kappa sobre las 12.")
log()

res_k = {}
for etiq, univ in (("12 (gate)", UNI), ("11 (diagnostico, sin U10)",
                                        [u for u in UNI if u != "U10"])):
    for niv, idx in (("Nivel 1", 1), ("Nivel 2", 2)):
        a = [COD1[u][idx] for u in univ]
        b = [COD2[u][idx] for u in univ]
        k, po, pe, n, cats = kappa(a, b)
        res_k[(etiq, niv)] = k
        log("  %-26s %-8s : kappa = %.4f   (Po = %.4f = %d/%d, Pe = %.4f)"
            % (etiq, niv, k, po, round(po * n), n, pe))
        if etiq.startswith("12"):
            matriz(a, b, cats, niv)
log()

K1 = res_k[("12 (gate)", "Nivel 1")]
log("§3 · GATE (spec §3.4) — kappa Nivel 1 sobre las 12 contra 0.60")
log("  kappa(N1, 12) = %.4f" % K1)
log("  Landis & Koch: 0.61-0.80 = acuerdo SUSTANCIAL")
if K1 >= 0.60:
    log("  GATE APROBADO -> se habilita el conteo POR CONSENSO (sin tercer codificador)")
else:
    log("  GATE NO APROBADO -> fila D de instrumento; NO se fuerza consenso")
log()
log("  Control de la reserva pre-registrada: los cuatro kappa caen del mismo")
log("  lado de 0.60?  %s"
    % ("SI — la distincion 12/11 no cambia nada"
       if all((v >= 0.60) == (K1 >= 0.60) for v in res_k.values())
       else "NO — manda el de 12 por spec; el de 11 viaja como reserva"))
for kk, vv in res_k.items():
    log("    %-26s %-8s = %.4f  (%s 0.60)"
        % (kk[0], kk[1], vv, ">=" if vv >= 0.60 else "<"))
log()

if K1 < 0.60:
    log("§4 · RESULTADO: fila D de instrumento. No se cuenta.")
    OUT.close()
    sys.exit(0)

# ── §4 · CONSENSO ─────────────────────────────────────────────────────
log("§4 · CONSENSO UNIDAD POR UNIDAD (spec §3.4, sin tercer codificador)")
FINAL = {}
for u in UNI:
    p, a1, a2 = COD1[u]
    _, b1, b2 = COD2[u]
    if (a1, a2) == (b1, b2):
        FINAL[u] = (p, a1, a2)
        continue
    assert u in CONSENSO, "discrepancia sin resolucion documentada: " + u
    c1, c2, quien, motivo = CONSENSO[u]
    FINAL[u] = (p, c1, c2)
    log("  %s · cod1 = %s/%s   cod2 = %s/%s   -> CONSENSO = %s/%s (a favor de %s)"
        % (u, a1, a2, b1, b2, c1, c2, quien))
    for ln in [motivo[i:i + 70] for i in range(0, len(motivo), 70)]:
        log("      " + ln)
    log()
sin_disc = [u for u in UNI if COD1[u][1:] == COD2[u][1:]]
log("  unidades sin discrepancia alguna (no requieren consenso): %d de %d — %s"
    % (len(sin_disc), len(UNI), " ".join(sin_disc)))
log()

# ── §5 · COBERTURA DEL UNIVERSO Y EXCLUSIONES 2.5 ─────────────────────
log("§5 · COBERTURA DEL UNIVERSO (spec §6: se reportan, no se descartan en silencio)")
for brazo in ("+P", "-P"):
    v = [u for u in UNI if FINAL[u][0] == brazo]
    nr = [u for u in v if FINAL[u][1] == "NO-RECHAZO"]
    log("  brazo %s : %d transcripciones · %d codificables como rechazo · %d NO-RECHAZO"
        % (brazo, len(v), len(v) - len(nr), len(nr)))
    for u in nr:
        log("      %s excluida del denominador — %s" % (u, MOTIVO_NR.get(u, "2.5")))
log()

# ── §6 · TASAS POR BRAZO ──────────────────────────────────────────────
log("§6 · TASAS DIRECTO/INDIRECTO POR BRAZO (denominador sin NO-RECHAZO)")
res = {}
for brazo in ("+P", "-P"):
    v = [u for u in UNI if FINAL[u][0] == brazo and FINAL[u][1] != "NO-RECHAZO"]
    if not v:
        log("  brazo %s : VACIO tras excluir NO-RECHAZO -> rama 3, fila D" % brazo)
        continue
    ind = [u for u in v if FINAL[u][1] == "INDIRECTO"]
    res[brazo] = (len(ind), len(v))
    lo, hi = wilson(len(ind), len(v))
    log("  brazo %s : indirectos %d de %d = %.2f pp   IC95%% Wilson [%.2f, %.2f]"
        % (brazo, len(ind), len(v), 100.0 * len(ind) / len(v), 100 * lo, 100 * hi))
    log("      %s" % "  ".join("%s=%s" % (u, FINAL[u][1][:3]) for u in v))
log()

# ── §7 · DIFERENCIA, IC Y RAMA ────────────────────────────────────────
log("§7 · DIFERENCIA, IC95% Y RAMA DEL ARBOL (spec §4.1)")
if "+P" not in res or "-P" not in res:
    log("  RAMA 3 -> fila D: al menos un brazo vacio")
    OUT.close()
    sys.exit(0)

(i1, n1), (i0, n0) = res["+P"], res["-P"]
p1, p0 = i1 / n1, i0 / n0
d = 100.0 * (p1 - p0)
se = 100.0 * ((p1 * (1 - p1) / n1 + p0 * (1 - p0) / n0) ** 0.5)
w_lo, w_hi = d - 1.96 * se, d + 1.96 * se
log("  tasa(+P) = %.2f pp (%d/%d)   tasa(-P) = %.2f pp (%d/%d)"
    % (100 * p1, i1, n1, 100 * p0, i0, n0))
log("  diferencia (+P menos -P) : %.2f pp" % d)
log("  EE Wald                  : %.2f pp" % se)
log("  IC95%% Wald              : [%.2f, %.2f]" % (w_lo, w_hi))
log()
log("  ADVERTENCIA declarada: con p1 = %.2f el termino Wald del brazo +P es" % p1)
log("  EXACTAMENTE CERO, y Wald es conocido por fallar en el borde. El IC Wald")
log("  de arriba esta ESTRECHADO por un artefacto, no por potencia. Se reporta")
log("  ademas el intervalo de Newcombe (hibrido de Wilson), que no degenera:")
l1, h1 = wilson(i1, n1)
l0, h0 = wilson(i0, n0)
nc_lo = 100.0 * (p1 - p0 - ((p1 - l1) ** 2 + (h0 - p0) ** 2) ** 0.5)
nc_hi = 100.0 * (p1 - p0 + ((h1 - p1) ** 2 + (p0 - l0) ** 2) ** 0.5)
log("  IC95%% Newcombe          : [%.2f, %.2f]" % (nc_lo, nc_hi))
odds, pf = sps.fisher_exact([[i1, n1 - i1], [i0, n0 - i0]])
log("  Fisher exacto 2x2, p = %.4f   tabla [ind, dir]: +P %s / -P %s"
    % (pf, [i1, n1 - i1], [i0, n0 - i0]))
log()

log("  Contra el umbral de %.0f pp:" % UMBRAL_PP)
for nom, lo, hi in (("Wald", w_lo, w_hi), ("Newcombe", nc_lo, nc_hi)):
    cruza = lo < UMBRAL_PP < hi
    log("    IC %-9s [%7.2f, %7.2f] -> %s el umbral"
        % (nom, lo, hi, "CRUZA" if cruza else "NO cruza"))
cruza = (w_lo < UMBRAL_PP < w_hi) or (nc_lo < UMBRAL_PP < nc_hi)
log()

UNIVERSITARIO = True   # Brasdefer/Mexico: role-play elicitado, poblacion universitaria
if abs(d) < UMBRAL_PP and not cruza:
    rama, fila = 1, "A"
elif abs(d) >= UMBRAL_PP and not cruza:
    rama, fila = 2, "B"
elif UNIVERSITARIO:
    rama, fila = 4, "C"
else:
    rama, fila = 5, "no adjudica (sin ruta a C)"
log("  RAMA %d -> fila %s" % (rama, fila))
if rama == 4:
    log("  §4.2: se registra TAMBIEN como 'no adjudica' bajo A-bis. Son respuestas")
    log("  a preguntas distintas: A-bis dice que el numero no decide; C dice que")
    log("  la via es replicar fuera de poblacion universitaria/elicitada.")
    log("  §4.3 precedencia 4: C manda sobre 'no adjudica' puro porque el IC cruza")
    log("  el umbral Y el instrumento es universitario/elicitado.")
    log("  §6 B-bis: 'corroborada' excluida por diseno; 'falsador demasiado debil'")
    log("  (D) NO aplica — ningun brazo quedo vacio (%d y %d)." % (n1, n0))
log()

log("§8 · TECHO DE n, RE-DERIVADO CONTRA LO PRE-DECLARADO (spec §5.1)")
log("  §5.1 declaro ±56.58 pp suponiendo n=6 por brazo y las dos tasas en 50%.")
log("  Denominadores REALES tras excluir NO-RECHAZO por 2.5: +P n=%d, -P n=%d." % (n1, n0))
log("  El techo se cumple y EMPEORA: la exclusion de las 5 unidades NO-RECHAZO")
log("  bajo la regla 2.5 recorta los brazos de 6/6 a %d/%d. El semiancho Newcombe" % (n1, n0))
log("  hacia abajo es %.2f pp. Recodificar mejor la VALIDEZ (defecto 1) no compra"
    % (d - nc_lo))
log("  POTENCIA: §5.2 lo predijo antes de correr y la corrida lo confirma.")
log()
log("=" * 78)
log("VEREDICTO DE LA CORRIDA: fila %s · kappa(N1,12) = %.4f · diferencia %.2f pp"
    % (fila, K1, d))
log("=" * 78)
OUT.close()
print("\nsalida cruda -> " + SAL)
