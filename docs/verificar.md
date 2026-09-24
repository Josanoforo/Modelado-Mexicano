---
title: Verificar
---

# Verificar

[Portada]({{ '/' | relative_url }}) · [Informe]({{ '/guia-lectura-publica.html' | relative_url }}) · [Reto público]({{ '/reto.html' | relative_url }})

## Lectura rápida, sin microdatos

Requisitos: Git, Python 3 y acceso a los archivos versionados del repo. Clona `https://github.com/Josanoforo/Modelado-Mexicano.git`, entra al directorio y ejecuta `python3 tools/corrida0.py status`. Compara las claves de salida con la [tabla del README](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/README.md#estado-derivado). Abre la [nota del piloto de ahorro](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/forense/notas/2026-09-16-GEN2-CELDA-D-PILOTO-1-cierre.md) y localiza sus CALC en [corrida0](https://github.com/Josanoforo/Modelado-Mexicano/tree/main/data/corrida0).

El control de identidad sobre un CALC versionado puede hacerse con `sha256sum data/corrida0/<CALC-ID>/spec.yaml data/corrida0/<CALC-ID>/resultados.json data/corrida0/<CALC-ID>/sello.json` y cotejando los hashes declarados en la spec y el sello. `sha256sum` sólo abre esos tres artefactos nombrados; no accede a `data/raw`. El `sello.json` registra el contexto y los hashes. Esta inspección no equivale a volver a calcular el estimando.

`python3 tests/check.py --baseline` compara la línea base del repositorio y excluye `data/raw` del barrido general; no se garantiza una duración fija. La [receta del sello externo](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/docs/sello-externo.md) explica cómo comprobar el testigo de tiempo y qué demuestra.

## Reproducción numérica

`python3 tools/corrida0.py verify <CALC-ID>` vuelve a comprobar la corrida. Puede necesitar los payloads del corpus montados bajo `data/raw`, dependencias y más tiempo. Consulta el `spec.yaml` del CALC para sus requisitos. Un error de corpus ausente no invalida por sí solo la inspección documental anterior.

**Corregido tras una verificación de punta a punta (24/sep/2026, sesión GEN2-FRONT-2), desde un clon limpio y sin contexto previo:** los pasos de "Lectura rápida" (`status`, `sha256sum` de un CALC) reprodujeron exactamente lo declarado arriba y en el README, sin instalar nada. `verify` sobre un `CALC` de ejemplo sin `data/raw` montado sí llegó honestamente a `[3/5 INPUT AUSENTE]` para cada input del manifiesto — pero el paso `[5/5 RESULT]` puede fallar antes con `ModuleNotFoundError: No module named 'numpy'` (o `pandas`) si tu entorno de Python no los trae, un `NO-EJECUTABLE` por falta de dependencia, distinto del `NO-EJECUTABLE` por falta de corpus. `pip install --break-system-packages numpy pandas` resuelve el import; ninguno de los dos cambia el resultado si además falta `data/raw`, porque el `medidor.py` de ese `CALC` no puede recalcular sin el microdato de todos modos. El detalle completo de la sesión está en [la nota de verificación](https://github.com/Josanoforo/Modelado-Mexicano/blob/main/forense/notas/2026-09-24-GEN2-FRONT-2-verificacion-tercero.md).
