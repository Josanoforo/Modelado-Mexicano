# Nota de cierre · GEN2-WBES2023-PRECISION-1

Fecha local: 2026-09-16, `America/Mexico_City`.

## Estado del producto

- **PREPARADO:** sí. Método, medidor, control y pruebas quedaron fijados en
  `7ab4bf6255e014f8d4ee7d9c79f683bc47af244f` antes de la corrida sellada.
- **EJECUTADO:** sí. Corrida
  `CALC-WBES2023-PRECISION-0001--7ab4bf6255e0` sobre 1,322 establecimientos.
- **SELLADO:** sí. `sello.sha256 =
  e6fd6b0774960cec32a164dd41672d08afd02ee3d7c87da5ea3a1111687fef98`;
  `verify = REPRODUCE` con contexto idéntico.
- **INTEGRADO:** no. La integración depende de revisión y fusión humana del PR.
- **ADOPTADO:** no. No se editó el informe TRA canónico ni registros globales.

## Resultado y decisión habilitada

Los cinco puntos del padre quedan acompañados por EE e IC95 bajo dos escenarios
de singleton, tipados `IC-APROXIMADO-CONDICIONAL-A-SUPUESTOS`. El total 15.24%
tiene IC95 7.82%–27.60% (`certeza`) o 7.40%–28.79% (`average`). La decisión
habilitada es incorporar precisión muestral aproximada a la lectura TRA, con
ambos escenarios visibles, y retirar cualquier lectura de ranking por tamaño.

Una primera invocación no selló nada porque la suma conjunta de pesos `float32`
difería `7.77e-9` del orden de suma sí+no del padre. Se corrigió sólo el orden
de reducción, el test real reprodujo los cinco puntos y entonces se realizó la
corrida sellada.

## Pruebas y verificaciones

- `python3 -m unittest tests.test_wbes2023_precision` — 7 OK, 1 integración
  real omitida antes de ejecutar.
- `WBES_REAL=1 python3 -m unittest tests.test_wbes2023_precision` — 8 OK;
  puntos y denominadores del padre reproducidos.
- `python3 tools/corrida0.py spec-check CALC-WBES2023-PRECISION-0001` — 16
  variables OK, 0 FAIL.
- `python3 tools/corrida0.py preflight CALC-WBES2023-PRECISION-0001` — VERDE.
- `python3 tools/corrida0.py verify CALC-WBES2023-PRECISION-0001` — REPRODUCE.
- `python3 .../control_independiente.py` — 40 campos, máxima diferencia
  `4.65e-13`, COINCIDE.

## Reservas materiales

1. Faltan probabilidades/FPC por celda panel/fresca o réplicas oficiales y un
   tratamiento oficial de los 34 estratos singleton; por eso los IC no son
   `IC-DISEÑO-ACREDITADO`.
2. Los dos escenarios no incorporan incertidumbre adicional de ajustes de
   elegibilidad/no respuesta y ninguno constituye una cota garantizada.
3. Los IC condicionan al desenlace clasificable; los límites por faltantes
   conservan otra identidad y no corrigen sesgo por no respuesta.

## CIERRE COMPARTIDO DIFERIDO

Después del trámite de Opus quedan sólo estas propagaciones potenciales:

1. insertar `lectura-TRA-WBES2023-precision-insercion.md` en el informe
   canónico si la mesa adopta el producto;
2. registrar la decisión humana de mostrar ambos escenarios condicionales;
3. actualizar estado/cola/registro global y contadores únicamente conforme a
   la gobernanza serial vigente.

No se reservaron ADR/NC/FP ni se editaron decisiones, firmas, hallazgos,
gobernanza, PARA, tableros, colas o vista de relevos. No se ejecutaron trámite,
despacho, derivación, cron ni registro con escritura.
