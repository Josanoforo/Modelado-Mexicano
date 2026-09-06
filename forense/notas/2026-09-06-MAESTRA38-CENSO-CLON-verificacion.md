# 2026-09-06 · MAESTRA38-CENSO-CLON · verificación (re-corrida de --escanea)

Re-corrida real de `tests/manifiesto.py --escanea` sobre un árbol de prueba
(tmpdir, sin red ni corpus) con un clon git dentro: una carpeta
`l2-lista/.git/HEAD` + tres archivos (`registrado.csv`, ya en el
manifiesto de la fixture; `nuevo_a.csv`/`nuevo_b.csv`, no). Construido y
corrido con el propio `manifiesto.py` importado como módulo (mismo camino
de código que usa `tests/test_manifiesto_clon.py`), no una simulación.

Comando (equivalente a `--escanea data_raw` sobre esa raíz):

```
Escaneado: raíz 'data_raw' (/tmp/censo_clon_demo/data/raw)
Entorno: Linux 6.18.44-fc-v24 (x86_64) · Python 3.11.15

Total en disco: 4 · nuevos: 0 · ya registrados: 1 · conflicto de nombre: 0 · fuera de alcance de dato: 0 · clones: 1

CLONES (1):
  CLON l2-lista · commit a1b2c3d4e5f60718293a4b5c6d7e8f9012345678 · 3 archivos
    l2-lista/registrado.csv -- ya registrado como 'l2-lista-registrado'

GRUPOS de datos detectados (0), por tanda de descarga (mtime en disco):

Escrito: .../data/manifiesto-staging.yaml (0 entrada(s) staging de la raíz 'data_raw' + 0 preservada(s) de otras). Nada se promovió a .../data/manifiesto.yaml.
```

Confirma COMMIT-2 exactamente: **1 línea CLON**, **0 nuevos**, **1 ya
registrado** (listado bajo el CLON, no suelto), **0 entradas de staging**
para los archivos del clon. `nuevo_a.csv`/`nuevo_b.csv` no aparecen en
ningún lado del reporte ni del staging — nunca fueron candidatos.

Mismo caso, con aserciones, en `tests/test_manifiesto_clon.py`
(`python3 tests/test_manifiesto_clon.py` → `OK`).

## CONTADOR

Falsos «nuevos» por clon: 136 (censo real del 6/sep, L2-LISTA) → 0 en el
siguiente censo que recorra esa raíz con este `--escanea`. Medición
pendiente del próximo censo real (`forense/censo-raiz/*.txt`); esta nota
solo fija la verificación mecánica sobre el árbol de prueba.
