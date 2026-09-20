# Cierre del sucesor 0002

## Resultados

Las tablas selladas de `tablas/` contienen perfiles con EE/IC para libre,
directo y residual, ocho intersecciones y los contrastes. El sucesor corrige
el marco: las 23,831 personas ponderables definen el sorteo; las 5,142 sin
primera unión y cualquier fuera de dominio aportan cero, no se eliminan antes
de formar UPM/estrato.

## Control independiente

`control_independiente.py` no importa el medidor. Reconstruye ZIP, terna,
primer evento, dominio, peso y el bootstrap de UPM desde el marco completo.
Frente a las tablas: p libre total = 0.4809714298527631, p libre mujer =
0.47592585577368585, contraste 1991+ = -0.07971659625959726 y EE =
0.020982248937062832. Las diferencias absolutas observadas son 5.6e-17 para
el contraste y 3.2e-17 para EE; tolerancia declarada 1e-10 por float64.

## Replay y cobertura

`replay_oficial.txt` registra `VERIFY: REPRODUCE`, contexto idéntico e inputs
coincidentes. El RESULT sellado incluye hashes de las tres tablas regeneradas.

| Requisito del brief | Archivo | Evidencia |
|---|---|---|
| enlaces, dominio y marco | `tablas/resultados.json` | 23,831 marco; 18,689 primera unión |
| perfiles y residual | `tablas/perfiles.csv` | n, masa, punto, EE e IC |
| contrastes y estándar | `tablas/contrastes.csv`, `pesos_estandarizacion.csv` | 2,000 réplicas PCG64 |
| control separado | `control_independiente.json` | punto y EE coinciden |
| replay | `replay_oficial.txt`, `sello.json` | REPRODUCE |

## Límites

No interpreta causalidad, riesgo de unión ni situación conyugal actual. Los
singleton se conservan; los IC no son garantía matemática de incertidumbre.
