"""P2 · GEN2-PISOS-Y-ADENDAS-1: deriva la constancia congelada (D-22(4)) que sustituye al
`tools/marcador_segmento.py` VIVO en CALC-PISO-PERSISTENCIA-ERROR-0002.

Uso: python3 p2_deriva_constancia.py <árbol exportado del commit 24afe8b9> <salida.json>
El árbol se obtiene con `git archive 24afe8b90751e9206124e5dfaa6ee2d34e9d835a | tar -x -C <dir>`:
es el árbol exacto sobre el que corrió CALC-PISO-PERSISTENCIA-ERROR-0001 (ejecucion.json.git_commit).
Guarda exactamente lo que el medidor 0001 consumía del módulo: las filas MARGINAL con
resultado_id de deriva()["filas"] (campos que celdas() lee), las filas de la tabla de identidad
que esas filas citan (lee_tabla_identidad(), por cell_id) y NORMALIZA_UNIT_TABLA.
No lee ningún resultados.json del CALC 0001."""
import hashlib, importlib.util, json, sys
from pathlib import Path
arbol, salida = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
COMMIT = "24afe8b90751e9206124e5dfaa6ee2d34e9d835a"
spec = importlib.util.spec_from_file_location("marcador_segmento_24afe8b9", arbol / "tools" / "marcador_segmento.py")
M = importlib.util.module_from_spec(spec); sys.modules[spec.name] = M; spec.loader.exec_module(M)
CAMPOS_FILA = ("celda_id", "tipo", "regla_o_eje_origen", "eje_o_par", "categoria", "unidad_dato", "estado",
               "piso", "piso_ic95", "piso_fuente", "resultado_id", "R", "R_ic95inf", "R_ic95sup")
CAMPOS_TABLA = ("cell_id", "source_instrument", "outcome", "source_edition", "target_edition",
                "source_reference_period", "target_reference_period", "unit")
v = M.deriva()
filas = [{k: f[k] for k in CAMPOS_FILA} for f in v["filas"] if f["tipo"] == "MARGINAL" and f["resultado_id"]]
citados = {f["resultado_id"] for f in filas}
tabla = [{k: t.get(k, "") for k in CAMPOS_TABLA} for t in M.lee_tabla_identidad() if t["cell_id"] in citados]
tabla.sort(key=lambda t: t["cell_id"])
insumos = {}
for rel in ["tools/marcador_segmento.py", "milpa/tramite-ola5-propuesta-v0.yaml",
            "forense/prereg-caja/PISOS-REJILLA-arbitro-metadatos-v1_0.tsv"]:
    insumos[rel] = hashlib.sha256((arbol / rel).read_bytes()).hexdigest()
doc = {
    "constancia": "marcador-segmento derivado en el commit del sello de CALC-PISO-PERSISTENCIA-ERROR-0001",
    "commit": COMMIT,
    "generador": "forense/notas/2026-09-28-GEN2-PISOS-Y-ADENDAS-1/p2_deriva_constancia.py",
    "sha256_insumos_en_el_commit": insumos,
    "normaliza_unit_tabla": {k: v2 for k, v2 in sorted(M.NORMALIZA_UNIT_TABLA.items())},
    "filas_marginales": filas,
    "tabla_identidad": tabla,
}
salida.parent.mkdir(parents=True, exist_ok=True)
salida.write_text(json.dumps(doc, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
print(f"filas_marginales={len(filas)} tabla_identidad={len(tabla)} sha256={hashlib.sha256(salida.read_bytes()).hexdigest()}")
