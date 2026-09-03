# MAESTRA37-N2 · control congelado antes de editar (COMMIT-1 de cada pieza)

Comandos corridos contra `8f49eab8` (rama `claude/fp-258-fp-246-repair-vmy8j5`, antes de
tocar ningún archivo de `tools/curador_registro/` ni `tools/vista_cola_adquisicion.py`).

## P1 · FP-258 — round-trip csv de `cola-adquisicion-registro.tsv`

```
$ wc -l data/curacion-registro/cola-adquisicion-registro.tsv
112 data/curacion-registro/cola-adquisicion-registro.tsv
```

```python
import csv, io
path = "data/curacion-registro/cola-adquisicion-registro.tsv"
with open(path, newline='', encoding='utf-8') as f:
    rows = list(csv.reader(f, delimiter='\t'))
buf = io.StringIO()
w = csv.writer(buf, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
for r in rows:
    w.writerow(r)
out_lines = buf.getvalue().split('\r\n')
with open(path, encoding='utf-8') as f:
    orig_lines = f.read().split('\n')
print(len(rows), "rows")            # 112 rows
print(len(orig_lines), "orig lines")  # 113 (línea vacía final por split)
print(len(out_lines), "out lines")    # 113
diffs = [i+1 for i,(a,b) in enumerate(zip(orig_lines,out_lines)) if a != b]
print(diffs)
```

Salida cruda: `112 rows / 113 orig lines / 113 out lines / diffs = [29, 47, 63, 94]`.

**Coincide con lo dictado** (`29, 47, 94` declaradas por la fila `FP-258` del tablero; `63`
es la fila de CompraNet editada línea por línea por `ACTO MAESTRA36-A2`, `ADR-314`, y no
estaba en el hallazgo original — creció de 3 a 4). No se re-normaliza ninguna: el control
se congela tal cual, con las 4 líneas y sin tocarlas.

Control de qué difiere exactamente (comillas), fila 29 y 47 (guardado para la nota de
cierre, no reproducido aquí verbatim por longitud — ver `git diff` del round-trip si se
necesita el detalle carácter a carácter).

## P2 · FP-246 — filas de `relaciones.tsv` con `;` en `id_manifiesto`

```
$ python3 - <<'PY'
import csv
with open("data/curacion-registro/relaciones.tsv", newline='', encoding='utf-8') as f:
    r = csv.reader(f, delimiter='\t')
    header = next(r)
    idx = header.index('id_manifiesto')
    idx2 = header.index('capa2_manifiesto')
    cnt = 0
    for row in r:
        if ';' in row[idx]:
            cnt += 1
            print(row[idx], row[idx2])
    print("total con ; :", cnt)
PY
```

Salida cruda:

```
ine_mge_2016_edomex_acuerdo_pdf;ine_mge_2016_edomex_seccion_municipio_xlsx;ine_mge_2016_edomex_municipios_xlsx;ine_mge_2016_coahuila_acuerdo_pdf;ine_mge_2016_ocho_entidades_catalogos_7z SI
iec_coahuila_2023_gubernatura_x_municipio_xlsx;iec_coahuila_2023_gubernatura_x_casilla_xlsx;iec_coahuila_2023_diputaciones_x_distrito_xlsx;iec_coahuila_2023_diputaciones_x_casilla_xlsx;iec_coahuila_2024_ayuntamientos_x_municipio_xlsx;iec_coahuila_2024_ayuntamientos_x_casilla_xlsx;iec_coahuila_calendario_integral_pel_2024_pdf SI
ieem_edomex_2023_gubernatura_x_municipio_xlsx;ieem_edomex_2023_tablas_gubernatura_zip;ieem_edomex_2023_gubernatura_x_casilla_xlsx;ieem_edomex_2024_ayuntamientos_x_municipio_xlsx;ieem_edomex_2024_tablas_ayuntamientos_zip;ieem_edomex_2024_ayuntamientos_x_seccion_xlsx;ieem_edomex_2024_ayuntamientos_x_casilla_xlsx SI
ieebc_bc_2016_municipes_x_casilla_xlsx;ieebc_bc_2019_computo_x_casilla_mun_xls;ieebc_bc_2021_computo_x_casilla_mun_xls;ieebc_bc_2024_computo_x_casilla_mun_xls SI
ieez_zacatecas_2016_ayuntamientos_x_municipio_htm;ieez_zacatecas_2016_eleccion_x_casilla_xls SI
ieech_chihuahua_2016_ayuntamientos_x_casilla_xlsx;ieech_chihuahua_2018_ayuntamientos_x_casilla_xlsx;ieech_chihuahua_2021_ayuntamientos_x_casilla_xlsx;ieech_chihuahua_2024_ayuntamientos_x_casilla_xlsx SI
total con ; : 6
```

**Coincide exactamente con lo dictado** (6 filas, todas `capa2_manifiesto = SI`, conteo por
columna con `csv`/`awk`, no por subcadena — ninguna otra fila del archivo tiene `;` en una
columna distinta que produzca falso positivo por `grep`).

## Control de la salida actual de `via_capa2.py` (modo lectura, sin `--escribe`)

```
$ python3 tools/curador_registro/via_capa2.py
Filas en relaciones.tsv: 211
Estados de verificación (verificar_entrada(), antes de diffs): COINCIDE=0 NO_COINCIDE=0 AUSENTE=54 SIN_PAYLOAD=0 RAIZ_NO_CONFIGURADA=14
Diffs propuestos (capa2_manifiesto): 0
...
cero payloads verificables — ¿está data/raw montada?
$ echo "EXIT:$?"
EXIT:1
```

`data/raw` no está montada en esta sesión (nube) — esperado (ARRANQUE punto 3, A.2). Las 6
filas con lista hoy caen en la rama `ID_NO_EN_MANIFIESTO` (`por_id.get(idm)` con `idm` la
cadena completa `;`-unida, que nunca es clave de `manifiesto.yaml`) y por eso ni siquiera
entran a `estados_verificacion` — es exactamente el defecto que `FP-246` describe: no
"COINCIDE=0 con ≥1 fila con id_manifiesto" (que el script ya vigila y hace fallar con
exit 1), sino un subconjunto que ni se examina.

Este control se congela ANTES de tocar `tools/curador_registro/via_capa2.py`,
`tools/vista_cola_adquisicion.py` o crear `tools/curador_registro/tsv_crudo.py`.
