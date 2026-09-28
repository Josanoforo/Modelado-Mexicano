# Renombre de entrada/ por T02 (después de lanzar; contenido y sha sin cambio)

`prepara_residuales.py` escribió en `<paq>/entrada/` los nombres `allowlist.json`, `allowlist.canon.sha256`, `identidad.json`, `tolerancia-v2.json`, `prompt.md` y `FIRMAS-Y-ACCESO.md`. Al cierre se renombraron con `git mv` al prefijo del paquete (`enbiare-l3r--`, `encodat-l3r--`, `encuci-l3r--`, `enigh-l3r--`) porque T02 prohíbe nombres normalizados repetidos en el árbol. Los bytes no cambian: el sha canónico de cada allowlist citado en las anclas de exportación sigue valiendo. Dentro de cada paquete entregado el nombre fue `FIRMAS-Y-ACCESO.md`.

## Duplicados retirados del árbol (T02), con su sustituto

- `<paq>/entrada/<abrev>--tolerancia-v2.json` (4): bytes idénticos a `endireh-pisos-2016-pareja-fisica-0002/entrada/tolerancia-v2.json` (`{"abs": "1e-10", "rel": "0"}`); están en el commit `1f089cc0` y cada copia viaja además dentro de `<paq>/comparacion/<abrev>--congelado.tar.gz`, que es la que usó `compare_v3`.
- `lanzamiento-residuales/settings-reconstructor.json`: idéntico a `lanzamiento/settings-reconstructor.json`.
- `lanzamiento-residuales/lanza-aislado.sh`: igual a `lanzamiento/lanza-aislado.sh` salvo la ruta de settings (`/home/pc0/c1-sucesores-rec/settings-reconstructor.json`). Los cuatro lanzamientos: `claude` 2.1.284, 120 turnos máximo, prompt en `<paq>/entrada/<abrev>--prompt.md`.
