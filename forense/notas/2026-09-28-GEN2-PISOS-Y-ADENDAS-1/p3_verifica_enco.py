"""P3 · F3 3(a) · GEN2-PISOS-Y-ADENDAS-1: verifica por comando los 4 enco_*_reservado
(sha256 + tamaño contra data/manifiesto.yaml) con los tres estados A.1 sin colapsar.
Hashea bytes; no parsea ni lista contenido (E.6: bajar y hashear no es abrir).
La raíz física de `reserva_respondentes` se pasa explícita (no está en raices.local.yaml)."""
import hashlib, os, sys, yaml
RAIZ = sys.argv[1] if len(sys.argv) > 1 else ""
m = yaml.safe_load(open("data/manifiesto.yaml", encoding="utf-8"))
ents = [e for e in m if str(e.get("id","")).startswith("enco_") and e.get("raiz") == "reserva_respondentes"]
print(f"entradas raiz=reserva_respondentes con id enco_*: {len(ents)} · raiz_fisica={RAIZ or '(no configurada)'}")
cuenta = {}
for e in ents:
    if not RAIZ or not os.path.isdir(RAIZ):
        est = "RAIZ-NO-CONFIGURADA"; det = ""
    else:
        p = os.path.join(RAIZ, e["archivo"])
        if not os.path.isfile(p):
            est = "AUSENTE"; det = p
        else:
            h = hashlib.sha256()
            with open(p, "rb") as f:
                for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
            t = os.path.getsize(p)
            ok = h.hexdigest() == e.get("sha256") and t == e.get("tamano_bytes", e.get("tamaño_bytes", t))
            est = "COINCIDE" if ok else "HASH-DISCORDANTE"
            det = f"sha256={h.hexdigest()} manifiesto={e.get('sha256')} bytes={t}"
    cuenta[est] = cuenta.get(est, 0) + 1
    print(f"{e['id']} [reserva_respondentes] {e['archivo']}: {est} {det}")
print("resumen:", " · ".join(f"{k}={v}" for k, v in sorted(cuenta.items())), f"· archivos_examinados={sum(v for k,v in cuenta.items() if k!='RAIZ-NO-CONFIGURADA')}")
