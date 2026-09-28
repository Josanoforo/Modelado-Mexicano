"""GEN2-ASTRA-CONTINUIDAD-C1-1 · P2. Tabla NC de C1 × dictamen × cita. Universo: filas ABIERTA de
forense/no-corrido.tsv con id que contiene ASTRA6-C1, RECIBO-ASTRA6-1/2/3 o RECIBO-ASTRA6-N (al
0-bis 26a2f0d8). Carril asignado por objeto; las de C2/C3/TUBERÍA se listan como AJENA y no se
tocan. Solo lee; las 6 CERRADA se asentaron en no-corrido.tsv por edición de línea (estado,
cerrado_por, fecha_cierre), sin reescribir el TSV."""
import csv
from pathlib import Path
R = Path(__file__).resolve().parents[3]
NC = R / "forense/no-corrido.tsv"
OUT = R / "forense/analisis/astra-continuidad-c1/nc-c1-dictamen-v1_0.tsv"
ACTO = "GEN2-ASTRA-CONTINUIDAD-C1-1"
H2 = "forense/analisis/recibo-astra6-2/hoja-para-mesa-recibo-astra6-2.md"
H4 = "forense/analisis/astra-continuidad-c1/hoja-mesa-c1-v1_0.md"
S = "forense/validacion-independiente/specs-insuficientes-v1_0.tsv"
N2 = "forense/notas/2026-09-27-GEN2-RECIBO-ASTRA6-2/"
N3 = "forense/notas/2026-09-27-GEN2-RECIBO-ASTRA6-3/"
D = {  # sufijo -> (carril, dictamen, cita/razón)
 "6c30-02": ("C1", "CERRADA", N2 + "pr-1166.md (recibo técnico de Claude de #1166, entregado por RECIBO-ASTRA6-2)"),
 "996b-07": ("C1", "CERRADA", N2 + "pr-1166.md (criterios C1 de #1166) y RECIBO-ASTRA6-2 P1 · #1171 (NC 627e-10..12): los dos recibos existen"),
 "9c9e-01": ("C1", "DECISIÓN", "absorbida por IMPEDIMENTOS-LOTE2 (#1200): sus decisiones son FP fb50-01..04 → hoja P4 §c"),
 "9c9e-02": ("C1", "SIGUE-ABIERTA", "DIFERIDO-A:GEN2-RECIBO-ASTRA-PRODUCTO-N — no hay recibo de Claude para #1185 (pr-1185.md NO-ENCONTRADO en forense/notas/*RECIBO-ASTRA6-*)"),
 "beee-01": ("C1", "SIGUE-ABIERTA", "DIFERIDO-A:lote 3 de validación ciega — paquetes -ventana-v1 (#1203) ya traen la ventana; falta el recálculo en sesión sin historial (hoja P4 §a); " + S + " tipo PAQUETE-SIN-IDENTIDAD-DE-VENTANA: 767"),
 "beee-02": ("C1", "SIGUE-ABIERTA", "DIFERIDO-A:GEN2-SPECS-ADENDA-1 — " + S + " D15-RECODIFICACION-AUSENTE: 31 llaves, ADENDA-DE-SPEC"),
 "beee-03": ("C1", "SIGUE-ABIERTA", "DIFERIDO-A:GEN2-SPECS-ADENDA-1 — " + S + " D15-IDENTIDAD-CONTRADICTORIA: 1 llave, ADENDA-DE-SPEC"),
 "beee-04": ("C1", "SIGUE-ABIERTA", "DIFERIDO-A:GEN2-CONTRAFACTUAL-ENDIREH2011-1 (caja); nada nuevo en main"),
 "beee-05": ("C1", "CERRADA", "FP-260927-GEN2-RECIBO-ASTRA6-1-beee-02 FIRMADA (consulta.py fp) y ejecutada por CIERRE-SEMANAL-2 en canon/catalogo-del-mexicano-v1_3.tsv"),
 "beee-06": ("C1", "SIGUE-ABIERTA", "DIFERIDO-A:GEN2-METODO-COMPARACION-INFERENCIAL-1 — gatea las 1 873 (P1 de este acto: por eso ninguna es PASA); ligada a FP 157c-01 (hoja P4 §c)"),
 "beee-07": ("C1", "SIGUE-ABIERTA", "DIFERIDO-A:GEN2-METODO-COMPARACION-INFERENCIAL-1 — misma vara; 10 ACOTAR por publicabilidad"),
 "beee-08": ("C1", "DECISIÓN", "la reserva de red solo se levanta con reconstructor aislado y broker → hoja P4 §a/§d (CONTEXTO-NUEVO-ACREDITADO)"),
 "beee-09": ("C1", "DECISIÓN", "las 92 de 2016 quedaron apartadas en lote 2 (tabla lote2: 92 INTENTO-DIAGNOSTICO-PRESERVADO); permiso de nueva lectura ENDIREH2016 = FP ee49-02 → hoja P4 §c"),
 "ee49-01": ("C1", "DECISIÓN", "FP-260926-ASTRA6-C1-REEMPAQUETA-VENTANA-1-ee49-01 (dictamen en " + H2 + ") → hoja P4 §c"),
 "ee49-02": ("C1", "DECISIÓN", "FP-260926-ASTRA6-C1-REEMPAQUETA-VENTANA-1-ee49-02 (dictamen en " + H2 + ") → hoja P4 §c"),
 "ee49-03": ("C1", "DECISIÓN", "aislamiento real no acreditado; depende de broker/reconstructor → hoja P4 §a"),
 "ee49-04": ("C1", "CERRADA", N2 + "pr-1203.md (recibo técnico de Claude de #1203)"),
 "fb50-01": ("C1", "DECISIÓN", "FP fb50-01 · RECOMENDAR-FIRMAR-CON-CAMBIO (" + H2 + ") → hoja P4 §c"),
 "fb50-02": ("C1", "DECISIÓN", "FP fb50-02 · RECOMENDAR-FIRMAR-CON-CAMBIO → hoja P4 §c"),
 "fb50-03": ("C1", "DECISIÓN", "FP fb50-03 · RECOMENDAR-FIRMAR-CON-CAMBIO → hoja P4 §c"),
 "fb50-04": ("C1", "DECISIÓN", "FP fb50-04 · RECOMENDAR-FIRMAR-TAL-CUAL → hoja P4 §c"),
 "157c-01": ("C1", "DECISIÓN", "FP 157c-01 · RECOMENDAR-FIRMAR-CON-CAMBIO → hoja P4 §c"),
 "157c-02": ("C1", "DECISIÓN", "sucesor ADJUDICACION-PUNTOS-1 fusionó (#1199) y dejó FP 39de-01 ABIERTA → hoja P4 §c"),
 "157c-03": ("C1", "DECISIÓN", "FP 157c-02 · RECOMENDAR-FIRMAR-CON-CAMBIO → hoja P4 §c"),
 "1653-01": ("C1", "CERRADA", N3 + "pr-1229.md (recibo de Claude de #1229); la adopción sigue en FP 1653-01 (hoja P4 §c)"),
 "627e-03": ("C1", "SIGUE-ABIERTA", "DIFERIDO-A:próximo trámite de archivo — duplicada por 8c5c-12; la copia a fuentes/tanda4 está fuera de este perímetro"),
 "627e-04": ("C1", "SIGUE-ABIERTA", "DIFERIDO-A:lote 3 de validación ciega — las 685 siguen sin validación ciega"),
 "627e-05": ("C1", "SIGUE-ABIERTA", "DIFERIDO-A:SIN-ASIGNAR — ADR de ADJUDICACION-PUNTOS-1 en canon/L0: 0 archivos (ls canon/L0 | grep -ic ADJUDICACION-PUNTOS → 0); RECIBO-ASTRA6-3 no lo cerró"),
 "627e-06": ("C1", "SIGUE-ABIERTA", "DIFERIDO-A:Astra — verifica.py sigue exigiendo diff limpio"),
 "627e-07": ("C1", "DECISIÓN", "126 COINCIDE ENBIARE no ciegas (las 4 ENCIG ya tenían PASA de otra validación): asentadas CONCUERDA-NO-APROBADA con rótulo NO-CIEGA-PENDIENTE (P1); mesa decide re-comparar o rotular → hoja P4 §c"),
 "627e-08": ("C1", "DECISIÓN", "2 NO-PASA ENIGH2020 remesas bajo tol 0.0 → hoja P4 §c"),
 "627e-09": ("C1", "SIGUE-ABIERTA", "DIFERIDO-A:lote 3 de validación ciega — 119 NF fuera de -ventana-v1"),
 "8c5c-01": ("C1", "SIGUE-ABIERTA", "NO-VERIFICABLE-AQUÍ — suite v3 fijada a Python 3.14.4/NumPy 2.3.5; nube 3.11.15 sin numpy (tools/entorno.py)"),
 "8c5c-02": ("C1", "CERRADA", "3 filas FP añadidas por este acto (FP-260928-GEN2-ASTRA-CONTINUIDAD-C1-1-26a2-01..03), texto en " + H4 + " §b"),
 "8c5c-03": ("C1", "DECISIÓN", "broker → hoja P4 §a (FP-260928-GEN2-ASTRA-CONTINUIDAD-C1-1-26a2-02)"),
 "8c5c-10": ("C1", "DECISIÓN", "PARO-ENTORNO de ceguera v2 → hoja P4 §a (reconstructor/entorno con namespaces)"),
 "8c5c-11": ("C1", "SIGUE-ABIERTA", "NO-VERIFICABLE-AQUÍ — bytes gzip dependen de entorno; sucesor: p4 verifica sha descomprimido"),
 "8c5c-12": ("C1", "SIGUE-ABIERTA", "DIFERIDO-A:próximo trámite de archivo (fuera de perímetro de este acto)"),
}
AJ = {"996b-01": "C2", "996b-03": "C2", "996b-04": "C2", "996b-08": "TUBERÍA", "627e-01": "C2", "627e-02": "C2",
      "8c5c-04": "C3", "8c5c-05": "C3", "8c5c-06": "C3", "8c5c-07": "C3", "8c5c-08": "C3", "8c5c-09": "C3", "8c5c-13": "C2"}
AJ.update({f"627e-{i:02d}": "C3" for i in range(10, 18)})
filas = list(csv.DictReader(NC.open(encoding="utf-8"), delimiter="\t")); campos = list(filas[0])
uni = [f for f in filas if (f["estado"] == "ABIERTA" or f["cerrado_por"].startswith(ACTO)) and any(t in f["id"] for t in
       ("ASTRA6-C1", "RECIBO-ASTRA6-1", "RECIBO-ASTRA6-2", "RECIBO-ASTRA6-3", "RECIBO-ASTRA6-N"))]
out, sin = [], []
for f in uni:
    k = f["id"][-7:]
    if k in D: c, d, q = D[k]
    elif k in AJ: c, d, q = AJ[k], "AJENA", f"carril {AJ[k]}: la cierra ese acto (encargo §1 P2)"
    else: sin.append(f["id"]); continue
    out.append([f["id"], c, d, q])
w = csv.writer(OUT.open("w", encoding="utf-8", newline=""), delimiter="\t", lineterminator="\n")
w.writerow(["nc_id", "carril", "dictamen", "cita_o_razon"]); w.writerows(out)
from collections import Counter
print("universo", len(uni), "sin_fila", len(sin), sin, Counter((o[1] == "C1", o[2]) for o in out))
