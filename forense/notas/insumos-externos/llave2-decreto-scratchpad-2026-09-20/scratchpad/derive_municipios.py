import json, re, subprocess, unicodedata

def norm(s):
    s = s.strip()
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return s.lower()

decreto_por_estado = {
    "Baja California": ["Ensenada", "Playas de Rosarito", "Tijuana", "Tecate", "Mexicali"],
    "Sonora": ["San Luis Río Colorado", "Puerto Peñasco", "General Plutarco Elías Calles", "Caborca", "Altar",
               "Sáric", "Nogales", "Santa Cruz", "Cananea", "Naco", "Agua Prieta"],
    "Chihuahua": ["Janos", "Ascensión", "Juárez", "Praxedis G. Guerrero", "Guadalupe", "Coyame del Sotol",
                  "Ojinaga", "Manuel Benavides"],
    "Coahuila de Zaragoza": ["Ocampo", "Acuña", "Zaragoza", "Jiménez", "Piedras Negras", "Nava", "Guerrero", "Hidalgo"],
    "Nuevo León": ["Anáhuac"],
    "Tamaulipas": ["Nuevo Laredo", "Guerrero", "Mier", "Miguel Alemán", "Camargo", "Gustavo Díaz Ordaz",
                   "Reynosa", "Río Bravo", "Valle Hermoso", "Matamoros"],
}
total_decreto = sum(len(v) for v in decreto_por_estado.values())
print("Total municipios en el decreto (Articulo Primero):", total_decreto)

ent_codes = {"Baja California": "02", "Sonora": "26", "Chihuahua": "08",
             "Coahuila de Zaragoza": "05", "Nuevo León": "19", "Tamaulipas": "28"}

catalogo = {}
for estado, ent in ent_codes.items():
    data = json.load(open(f"scratchpad/mgem_{ent}.json"))
    catalogo[ent] = {norm(r["nom_agem"]): (r["cve_agem"], r["nom_agem"]) for r in data["datos"]}

rows = []
faltantes = []
for estado, muns in decreto_por_estado.items():
    ent = ent_codes[estado]
    for m in muns:
        key = norm(m)
        if key in catalogo[ent]:
            cve, nom_oficial = catalogo[ent][key]
            rows.append((ent, cve, estado, m, nom_oficial))
        else:
            faltantes.append((estado, m))

print("Emparejados:", len(rows), "de", total_decreto)
if faltantes:
    print("SIN EMPAREJAR:", faltantes)

print()
print("ent\tmun\testado\tmunicipio_decreto\tmunicipio_catalogo_inegi")
for r in sorted(rows):
    print("\t".join(r))

# check duplicate (ent,mun) or duplicate municipio name collisions across states
names = [r[3] for r in rows]
from collections import Counter
c = Counter(names)
dupes = {k:v for k,v in c.items() if v>1}
print()
print("Nombres de municipio repetidos entre estados (misma clave textual, distinto ENT/MUN):", dupes)
