"""GEN2-ASTRA-CONTINUIDAD-C1-1 · P1. Deriva los asientos de C1 (lote 1 faltantes y lote 2)
para data/corrida0/validaciones-independientes.tsv. Regla declarada antes de escribir
(nota §P1): PASA solo con tolerancia citada satisfecha en punto y ambos extremos del IC;
CONCUERDA-NO-APROBADA si el punto concuerda y la spec no bastó (o no hay tolerancia por
llave); NO-PASA si algo discrepa o nada fue recalculable. Una fila por (spec, RESULT): el
overlay de corrida0 rechaza duplicados; una llave ya asentada no se re-asienta.
Uso: python3 asienta_p1.py [--escribe]"""
import csv, hashlib, sys, collections
from pathlib import Path
R = Path(__file__).resolve().parents[3]
V = R / "data/corrida0/validaciones-independientes.tsv"
T1 = R / "forense/notas/2026-09-27-GEN2-RECIBO-ASTRA6-1/2026-09-27-gen2-recibo-astra6-1--tabla-result-estado-efecto.tsv"
T2 = R / "forense/validacion-independiente/catalogo-1-ejecucion-lote2/lote2-tabla-estimadores.tsv"
C1 = "forense/validacion-independiente/catalogo-1-ejecucion-lote1/comparaciones/{}--comparacion.json"
sha = lambda p: hashlib.sha256((R / p).read_bytes()).hexdigest()
lee = lambda p: list(csv.DictReader(open(p, encoding="utf-8"), delimiter="\t"))
vistos = {(x["spec_id"], x["resultado_id"]) for x in lee(V)}
nuevas, omitidas = [], collections.Counter()

# Lote 1: RESULT sin fila. Todas sus llaves son NO-RECALCULABLE-DESDE-SPEC (0 comparadas).
por = collections.defaultdict(list)
for x in lee(T1): por[(x["calc"], x["result_id"])].append(x)
for (calc, rid), xs in sorted(por.items()):
    if (calc, rid) in vistos: omitidas["lote1-ya-asentada"] += 1; continue
    c = collections.Counter(x["recomendacion"] for x in xs)
    ref = C1.format(xs[0]["paquete"])
    assert set(c) == {"SOSTENER-SIN-CORROBORACION"}, (rid, c)
    nuevas.append([calc, rid, "NO-PASA", ref, sha(ref),
        f"C1-LOTE1-CIEGA-POR-SEPARACION tol=1e-10(spec): recalculadas 0/{len(xs)}; "
        f"SOSTENER-SIN-CORROBORACION {len(xs)} (NO-RECALCULABLE: PAQUETE-SIN-IDENTIDAD-DE-VENTANA, "
        f"NC-260927-GEN2-RECIBO-ASTRA6-1-beee-01; nada comparado, no es discrepancia); de {len(xs)} celdas (GEN2-ASTRA-CONTINUIDAD-C1-1; reserva de red NC-RECIBO-ASTRA6-1-08)"])

# Lote 2: por llave ejecutada; sin tolerancia por llave en la tabla -> nunca PASA.
ref2 = str(T2.relative_to(R)); s2 = sha(ref2)
for x in lee(T2):
    if x["estado_ejecucion"] != "EJECUTADO": omitidas["lote2-apartada-adenda"] += 1; continue
    k = (x["calc"], x["result_id"]); p, ic = x["estado_punto"], x["estado_ic"]
    if p == "NO-RECALCULABLE-DESDE-SPEC": omitidas["lote2-no-reconstruida"] += 1; continue
    if k in vistos: omitidas["lote2-ya-asentada"] += 1; continue
    if p == "COINCIDE" and ic != "DISCREPA":
        d, q = "CONCUERDA-NO-APROBADA", f"punto COINCIDE; IC {ic}; tabla sin tolerancia por llave (regla §5 del encargo: no PASA)"
    else:
        d, q = "NO-PASA", f"punto {p}; IC {ic}"
    if x["instrumento"] in ("ENBIARE", "ENCIG") and p == "COINCIDE":
        q += "; NO-CIEGA-PENDIENTE: alias `estimacion` de dictamen-v2 añadido tras revelar (NC-260927-GEN2-RECIBO-ASTRA6-2-627e-07)"
    nuevas.append([k[0], k[1], d, ref2, s2,
        f"C1-LOTE2 REIMPLEMENTACION-INDEPENDIENTE 1 llave: {q}; spec {x['estado_spec']} (GEN2-ASTRA-CONTINUIDAD-C1-1)"])
    vistos.add(k)

print(collections.Counter(n[2] for n in nuevas), dict(omitidas), len(nuevas))
if "--escribe" in sys.argv:
    with V.open("a", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n"); w.writerows(nuevas)
