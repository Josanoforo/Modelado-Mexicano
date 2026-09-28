"""A.12: marca FIRMADA las siete FP `f2e5-*` que el encargo
`GEN2-TUBERIA-Y-CURACION-1` ejecuta (C2, D2, F1, G1, H1, H2, H5) -- "una
firma que viaja verbatim en un encargo la asienta el acto que lo ejecuta".

Edición por línea (no csv.DictReader/DictWriter): las celdas de este TSV
traen comillas literales de firmas verbatim, y `tools/estado_comun.py::
lee_tablero` existe precisamente para no perder eso -- esta escritura
respeta la misma razón, tocando solo las columnas `estado`, `firmada_en`,
`ejecutada_en` de las siete filas por `id`, byte a byte en todo lo demás.

Uso: python3 forense/analisis/tuberia-y-curacion-1/marca_firmadas.py [--aplica]
"""
import sys

P = "forense/firmas-pendientes.tsv"
ADR = "ADR-260928-GEN2-TUBERIA-Y-CURACION-1-247d-01"
ADENDA = ("INTERPRETACIÓN-DECLARADA en "
          "2026-09-28-GEN2-TRAMITE-HOJA-FIRMAS-21-1-ADENDA-1.md")

OPCION = {
    "f2e5-09": ("C2", "a"), "f2e5-11": ("D2", "a"), "f2e5-19": ("F1", "a"),
    "f2e5-23": ("G1", "B"), "f2e5-24": ("H1", "a"), "f2e5-25": ("H2", "b"),
    "f2e5-28": ("H5", "a"),
}


def firmada_en(letra, opcion):
    return (f'GEN2-TUBERIA-Y-CURACION-1 §2, 28/sep/2026 -- firma de mesa '
            f'verbatim "firmado" sobre la hoja v2 de dirección ({ADENDA}); '
            f'opción para {letra}: "{opcion}" (hoja NC-DECISIONES-1, '
            f'forense/analisis/nc-decisiones/hoja-2026-09-27.md §{letra}).')


def main():
    with open(P, encoding="utf-8") as f:
        lineas = f.read().split("\n")
    cab = lineas[0].split("\t")
    i_estado = cab.index("estado")
    i_firmada = cab.index("firmada_en")
    i_ejecutada = cab.index("ejecutada_en")
    tocadas = 0
    for i, linea in enumerate(lineas):
        if not linea.startswith("FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-"):
            continue
        campos = linea.split("\t")
        clave = "-".join(campos[0].split("-")[-2:])  # p.ej. f2e5-09
        if clave not in OPCION:
            continue
        letra, opcion = OPCION[clave]
        assert campos[i_estado] == "ABIERTA", (campos[0], campos[i_estado])
        campos[i_estado] = "FIRMADA"
        campos[i_firmada] = firmada_en(letra, opcion)
        campos[i_ejecutada] = ADR
        lineas[i] = "\t".join(campos)
        tocadas += 1
    assert tocadas == len(OPCION), (tocadas, len(OPCION))
    nuevo = "\n".join(lineas)
    print(f"filas tocadas={tocadas} de {len(OPCION)} esperadas")
    if "--aplica" in sys.argv:
        with open(P, "w", encoding="utf-8") as f:
            f.write(nuevo)


main()
