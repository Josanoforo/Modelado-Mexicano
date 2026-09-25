# Sesiones: clon parcial, instalación y herramientas

ACTO GEN2-TUBERIA-RENDIMIENTO-1 (P4, P6). Lo cita `/acto` en su ARRANQUE.
Quien toque `/acto` actualiza este archivo (sucesor declarado en el encargo).

## 1 · Clon parcial para sesiones de nube (P6)

Una sesión que no abre microdato ni toca `corpus/`, `data/curacion-universo/`
ni los inventarios de reactivos (`data/inventario-reactivos-*.tsv`) no
necesita sus blobs:

```
git clone --filter=blob:none --sparse <url-del-repo> Modelado-Mexicano
cd Modelado-Mexicano
git sparse-checkout set canon forense tools tests milpa data/corrida0 .claude .github docs
```

`--filter=blob:none` trae el historial sin contenido; git baja cada blob
cuando algo lo lee (un `git show` viejo, un `checkout` de otra ruta). Para
ampliar el cono: `git sparse-checkout add <ruta>`.

Medido el 24/sep/2026 sobre `origin/main` = `8358b891`, en la nube:

| clon | tiempo | árbol + .git | .git |
|---|---|---|---|
| completo (`git clone` + checkout) | 28.6 s | 712 MB | 134 MB |
| parcial (receta de arriba) | 12.2 s | 601 MB | 80 MB |

`data/corrida0/` (198 MB) queda dentro del cono porque `corrida0.py`, el
marcador y la suite lo leen; es el grueso de lo que queda.

**CAJA no usa esta receta**: el clon de caja es completo y con el corpus
montado (`data/raw`).

## 2 · Instalación con `uv` (P4)

```
pip install uv            # o viene preinstalado
uv pip install --system -r requirements.txt
```

`uv` resuelve e instala de wheels; en particular trae **PyYAML con
libyaml** (`yaml.CSafeLoader`). Un PyYAML de paquete del sistema
(`/usr/lib/python3/dist-packages`, sin libyaml) vuelve `registro` ~4×
más lento (medido: 65.5 s → 16.5 s con libyaml + índice, ver la nota del
acto). Comprobación de un segundo:

```
python3 -c "import yaml; print(hasattr(yaml, 'CSafeLoader'))"   # True
```

## 3 · Consultar sin leer

- Una fila en una línea: `python3 tools/consulta.py result|corrida|celda|payload|fp|nc <id>`.
- Reglas de lectura: `CLAUDE.md` § Reglas de lectura.
- `rg`, `jq`, `yq` están en la imagen de nube y en la CI (`apt`).
