"""P1 · GEN2-PISOS-Y-ADENDAS-1: genera data/corrida0/CALC-ENCIG2023-CONFIANZA-PISOS-0001/spec.yaml.
`resultados:` sale de esquema_resultados() del medidor (no a mano). Se corre una vez antes del COMMIT-1."""
import hashlib, importlib.util, sys
from pathlib import Path
import yaml
RAIZ = Path(__file__).resolve().parents[3]
CALC = "CALC-ENCIG2023-CONFIANZA-PISOS-0001"
D = RAIZ / "data/corrida0" / CALC
SPEC_MD = RAIZ / "forense/prereg-caja/ENCIG2023-CONFIANZA-PISOS-spec-v1_0.md"
s = importlib.util.spec_from_file_location("m", D / "medidor.py"); m = importlib.util.module_from_spec(s); s.loader.exec_module(m)

def tipo(rid):
    if rid.endswith(("-P", "-IC-LO", "-IC-HI")):
        return {"tipo": "proporcion", "permite_no_estimable": True}
    if rid.endswith("-EE"):
        return {"tipo": "flotante", "permite_no_estimable": True}
    return {"tipo": "entero"}

def unidad(rid):
    for suf, u in (("-IC-LO", "IC95 de diseño, límite inferior"), ("-IC-HI", "IC95 de diseño, límite superior"),
                   ("-EE", "error estándar bootstrap"), ("-P", "proporción ponderada [0,1] de mucha o algo de confianza"),
                   ("-N", "personas sin ponderar con respuesta 1-4"), ("-N-NO-APLICA", "personas sin ponderar"),
                   ("-N-NSNR", "personas sin ponderar"), ("-N-OTRO", "personas sin ponderar")):
        if rid.endswith(suf):
            return u
    if rid.endswith(("-UPM",)): return "UPM de diseño"
    if rid.endswith("-ESTRATOS"): return "estratos de diseño"
    return "filas"

res = []
for rid in m.esquema_resultados():
    r = {"id": rid, **tipo(rid), "unidad": unidad(rid)}
    res.append(r)
spec = {
    "calc_id": CALC,
    "spec_md": "../../../forense/prereg-caja/ENCIG2023-CONFIANZA-PISOS-spec-v1_0.md",
    "spec_md_sha256": hashlib.sha256(SPEC_MD.read_bytes()).hexdigest(),
    "script": f"data/corrida0/{CALC}/medidor.py",
    "dependencias_materiales": ["numpy", "pandas"],
    "etiquetas": {
        "generacion": "GEN2", "tipo": "PISO-POR-SEGMENTO-DESDE-MICRODATO", "cuenta_gen2": "SI", "adopta": "NO",
        "uso_motor": "NO-ADOPTA-NADA", "agrupacion": "UNA-SOLA-VARIABLE",
        "marca": "DESCRIPTIVO -- pisos por eje; RETROSPECTIVO; nada se evalua contra R en este CALC",
        "unidad_transferencia": "PERSONA", "fuente_acto": "GEN2-PISOS-Y-ADENDAS-1",
        "encargo": "forense/encargos/2026-09-28-GEN2-PISOS-Y-ADENDAS-1.md",
        "firmas": "H4 (a), mesa 28/sep/2026 (FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-27)",
        "ola": "ENCIG 2023; ENCIG 2025 fuera (PARO a del encargo: seccion XI no abierta por su arbitro)",
        "cuenta_gen2_nota": "CONTADOR del encargo: cuenta_gen2 = SI para P1; no adopta",
    },
    "inputs": [{"id": "encig23_base_datos_csv", "origen": "manifiesto",
                "sha256": "af733d867a568cbb0dadef4a5a793b02488a71728d1157860f14501f3d4c393d", "funcion": "DATO",
                "nota": "encig23_base_datos_csv.zip; miembros encig2023_01_sec_11.csv y encig2023_02_residentes_sec_2.csv"}],
    "variables": [{"archivo": m.M_SEC11, "variable": v, "rol": r} for v, r in
                  [("ID_PER", "llave"), ("CVE_ENT", "eje-entidad"), ("EST_DIS", "estrato"), ("UPM_DIS", "upm"), ("FAC_P18", "ponderador")]]
                 + [{"archivo": m.M_SEC11, "variable": f"P11_1_{i}", "rol": "desenlace"} for i in m.ITEMS]
                 + [{"archivo": m.M_RES, "variable": v, "rol": r} for v, r in
                    [("ID_PER", "llave"), ("SEXO", "eje-sexo"), ("EDAD", "eje-edad"), ("NIV", "eje-escolaridad")]],
    "universo": "Persona 18+ en ciudades de 100 mil habitantes y mas (informante seleccionado, seccion XI); FAC_P18>0 finito, EST_DIS y UPM_DIS no vacios.",
    "filtros": "Un eje a la vez; nunca cruces. Codigo invalido fuera solo del eje afectado. Tamano de localidad NO-CONSTRUIBLE (spec §3.6).",
    "ponderador": "FAC_P18 sin normalizar",
    "transformacion": "P11_1_nn (entero): 1-2 -> 1; 3-4 -> 0; 5, 9, otro -> fuera del denominador (contados aparte, nacional).",
    "estimando": "Proporcion ponderada de mucha o algo de confianza por institucion (25) x celda de eje (43), ENCIG 2023, con IC95 de diseno.",
    "seed": {"aplica": True, "valor": 20260928, "rng": "numpy.PCG64"},
    "parametros": {"bootstrap_replicas": 2000,
                   "metodo_ic": "bootstrap UPM con reposicion dentro de estrato sobre el marco entero; replicas compartidas; percentiles 2.5/97.5; contrato conservador (denominador 0 en alguna replica -> IC/EE nulos)"},
    "tolerancia": {"tipo": "flotante", "abs": 1.0e-10, "razon": "bootstrap determinista por semilla; mismo payload; sumas float64"},
    "resultados": res,
}
hdr = ("# CALC-ENCIG2023-CONFIANZA-PISOS-0001 -- contrato ejecutable de la spec humana (D-15). COMMIT-1, antes de abrir microdato.\n"
       "# El primer resultado que produzca este procedimiento es el que se reporta.\n")
(D / "spec.yaml").write_text(hdr + yaml.safe_dump(spec, allow_unicode=True, sort_keys=False, width=110), encoding="utf-8")
print(len(res), "resultados")
