# ACTO GEN2-SOCIALES-SUCESORAS · cierre

## Resultado útil

S6 v1.4 hace reproducible el enlace de diseño por hogar; S13 v1.1 limita correctamente la cláusula histórica; S12 v1.2 y CALC-0001-v2 miden la composición alineado/no alineado entre receptores sin convertirla en efecto causal ni sustituir el resultado histórico.

| obligación | evidencia | cerrada/residual | siguiente acción |
|---|---|---|---|
| S6 / NC-0065 | `S6-L16-spec-v1_4.md`: `m:1` por `folio`, guardia lossless, cobertura de v4 y 0 faltantes analíticos de diseño | CERRADA; FP-332 permanece fuera de alcance | usar v1.4 en corridas futuras; no repetir v4 |
| S13 / NC-0043 | `S13-R10-3-spec-v1_1.md` + consumidor corregido | CERRADA; 2004 `NO-DISCRIMINA`, R10.3 `[FUERTE]`, sin réplica ≥2019 | reexaminar sólo con fuente nueva que mida denuncia original o nueva decisión de mesa |
| S12 / NC-0064 | `S12-CSES-spec-v1_2.md`; CALC-0001-v2, sello `9cb42c7c2153e9a27a311c18d979be7f0d601fd00441a5ac4b9ec2c53f4a977b` | CERRADA; amenaza limitada por n<10 | no adoptar al motor; interpretar sólo descriptiva/asociativamente |

## Resultado S12

| rama | bruto alineado / no alineado | pesos alineado / no alineado | P alineado (IC95) | delta composición (IC95) | límite |
|---|---:|---:|---:|---:|---|
| OFERTA | 17 / 25 | 16.290029 / 26.666026 | 0.379225 [0.217138, 0.559718] | -0.241549 [-0.565724, +0.119435] | IC contiene 0 |
| AMENAZA | 6 / 8 | 6.140545 / 7.855312 | 0.438740 [0.213933, 0.654954] | -0.122520 [-0.572134, +0.309907] | ambas categorías n<10 |

Receptores declarados/analíticos/excluidos: OFERTA 58/42/16; AMENAZA 24/14/10. La selección en receptores y la retrospectividad impiden una lectura causal.

## Pruebas y validación

- `spec-check CALC-0001-v2`: 8 OK, 0 FAIL, 317,718 filas de inventario examinadas.
- `preflight`: VERDE; payload y spec por hash coincidentes.
- `run`: 38 RESULT, sello válido; `verify`: REPRODUCE 38/38, contexto idéntico.
- `tests/test_calc0001_v2.py`: verde.
- Validación independiente: tabulación directa del SAV, sin importar `medidor.py`, coincide exactamente en 17/25 y 6/8, y dentro de `1e-12` en pesos y proporciones.

`CALC-0001-v2` cuenta GEN2 por D14/FP-363 con objeto explícito. No se incorpora ninguna tasa al motor y ningún tier cambia. Entrega: PR #688. ADR candidato 455 colisiona con el candidato del PR #687; se renumera si ese PR fusiona primero.
