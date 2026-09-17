# Recibo de reproducción

## Cadena

- Base: `origin/main` en
  `4273a3a6ff1ed964c019e2fa95136db7956fd4ff`.
- Commit previo a leer columnas monetarias reales:
  `ee963edc1d2bc15a664f2f4107b42f6c914b636c`.
- CALC: `CALC-ENIGH2022-INTENSIDAD-REMESAS-0001`.
- Corrida: `CALC-ENIGH2022-INTENSIDAD-REMESAS-0001--ee963edc1d2b`.
- Spec humana SHA-256:
  `e3e845dbc94b6834594f4aeeb4ea1e3d475ecf15ef3d47e8e3228d27a7e7195c`.
- Spec mecánica SHA-256:
  `8fdd120ad56feb9a8385acee04c094f911106528826e9f6f1cb23ce36d192af3`.
- Medidor SHA-256:
  `428a70368301694c97741bfb625dc19ca48bb4a0a6ded785daa938303fe07ab7`.
- Sello SHA-256:
  `f16f51ff4537d3c8ed47d2d048c28579a49c2be2f97be532f7d0668f7ad89bfb`.

## Verificaciones ejecutadas

1. `python3 -m unittest tests.test_enigh2022_intensidad_remesas` — 5 pruebas,
   `OK` antes de leer el miembro real.
2. `python3 tools/corrida0.py spec-check CALC-ENIGH2022-INTENSIDAD-REMESAS-0001`
   — 7 variables exactas `OK`, 317,718 filas de inventario examinadas.
3. `python3 tests/manifiesto.py --verifica --id ...` para cada PDF — SHA y
   tamaño `COINCIDE`.
4. `python3 tools/corrida0.py preflight ...` — `VERDE` sobre árbol limpio y
   cinco insumos coincidentes.
5. `python3 tools/corrida0.py run ...` — salida `SELLADO`.
6. `python3 tools/corrida0.py verify ...` — `REPRODUCE`, contexto idéntico y
   45 resultados reproducidos.
7. Comprobación independiente con `pandas.read_csv(..., usecols=...)`:
   reproduce n/masas, prevalencia, cinco estadísticos y cero casos `r>y`;
   diferencias de la media sólo en el último redondeo binario (`2e-12`).

## Riesgos cubiertos por fixtures

- pesos desiguales separan media de razones y razón de sumas;
- cero de remesas permanece no receptor;
- ingreso cero y faltante cambian sólo el dominio de participación y se
  cuentan con su masa;
- remesas faltantes/negativas no se convierten en cero;
- llave de hogar duplicada detiene la medición;
- el bootstrap conserva el marco y ceros fuera del dominio;
- diseño incompleto conserva puntos sin fabricar IC;
- mediana ponderada usa inversa izquierda sin interpolación;
- prevalencia reproduce una referencia explícita del padre.

El producto está **EJECUTADO y SELLADO**. Un commit o PR posterior lo deja
PREPARADO para integración, pero no lo vuelve INTEGRADO ni ADOPTADO.
