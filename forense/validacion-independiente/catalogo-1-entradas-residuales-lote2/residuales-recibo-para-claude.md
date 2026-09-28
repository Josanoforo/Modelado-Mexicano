# Solicitud de recepción · entradas residuales lote2

PENDIENTE por circuito de mesa en PR propio. Este archivo solicita revisión y no constituye recibo obtenido.

EJECUTADO: preparación sobre main `9536e5e2cff760a1866d7c3395395d9dbdd8bbd1`, dependencia #1202 HEAD `3316f9038954d3feab3c88a3d1e1affecc560621` recibida por merge, propuesta #1194 recibida por identidad. 0-bis `165308cc3a14d0246242f0491893aeecba0a97e3`. Originales intactos, preparación con valores previos conocidos y sin recálculo.

Objetos revisables: P1 tabla llave×componente y diferencias anteriores; P2 fuentes completas/hash/localizador y cláusulas humanas; P3 recetas históricas insuficientes frente a propuestas completas; P4 mapa exterior original→sucesor, manifestación de cambios, contenedores y verificación; P5 hoja de decisión por cohorte y firmas propuestas. Archivo de dirección y auditoría permanecen fuera de los contenedores.

Comandos desde la raíz del worktree:

```sh
python3 tools/validacion/astra6_entradas_residuales/p1.py
python3 tools/validacion/astra6_entradas_residuales/p4.py --verifica
python3 tests/check.py --rapido --baseline
git diff --check
git diff --name-only 9536e5e2cff760a1866d7c3395395d9dbdd8bbd1
```

LEÍDO: la firma Acordado vive en `forense/encargos/2026-09-26-ASTRA6-C1-PAQUETES-1.md` §2; no se crea otro asiento. PROPUESTO: adoptar cláusulas nuevas solo tras firma expresa por cohorte y hash, sin cambiar tolerancia ni dictámenes anteriores. NO-VERIFICADO: recibo de Claude, independencia cognitiva futura, reproducción científica y aceptación de mesa.

Revisión solicitada: comprobar separación de contenidos, precedencia de definiciones restauradas, compatibilidad de propuestas IC con #1194, correspondencia exacta de las 312 llaves, hashes y estados de uso. Dictaminar recepción y recomendar aceptación o devolución; este acto no fusiona ni autoaprueba.

EJECUTADO: `python3 tools/validacion/astra6_entradas_residuales/p1.py` PASS (368 pares, unión312); `python3 tools/validacion/astra6_entradas_residuales/p4.py --verifica` PASS (4 contenedores,312identidades,40miembros, bytes reproducibles); `git diff --cached --check` PASS; `python3 tests/check.py --rapido --baseline` VERDE, sin FAIL nuevos y 0 FAIL global. Gate documental, no evidencia científica. Detalle en `residuales-verificacion-final.json`.

PR propio publicado: https://github.com/Josanoforo/Modelado-Mexicano/pull/1229. Recibo técnico solicitado en el cuerpo del PR, aún no obtenido; merge y firma de contratos pendientes.

## Corrección de salida del PR #1229 · 27/sep/2026

EJECUTADO: los cuatro contenedores vigentes son `residuales-documentales-v2`; las copias v1 se preservan byte a byte en `p4/retirados/` y no se entregan. `esquema-identidades.tsv` ahora lleva la `llave` comparada explícita y `esquema-salida-v2.md` define exactamente `version/identidad/filas` de #1221. P2 y P3 remiten al mismo contrato; los diagnósticos auxiliares se separan del JSON comparado y se sellan antes de revelar referencias. La correspondencia exhaustiva y la limitación de estados están en `p4/residuales-p4-correspondencia-adaptador-v2.md`.

EJECUTADO: prueba sintética contra #1221 HEAD `d8ef9f56ef80ec1cd7867779489beb0ce7e4cfe9` con 12 circuitos paquete → congelación verificada → comparación (936 filas sintéticas: cuatro cohortes por punto sin IC, IC calculado y no recalculable por spec); los campos auxiliares antiguos se rechazan. Evidencia en `p4/residuales-p4-prueba-salida-v2.json`. Cero datos reales, cero recálculos, cero referencia histórica revelada; no se reinterpreta ninguna salida posterior. El adaptador #1221 sigue propuesto y una versión diferente exige nueva prueba antes de un intento real.

EJECUTADO tras sincronización: `origin/main` `140b716db8f381efb2916667ba1be6ec8fe3e3e4` ya integra #1221; `git merge origin/main` sin conflictos materiales. T02 detectó colisión nueva de `fuentes.json` con ENOE; el propio P2 se renombró `residuales-p2-fuentes.json` sin cambiar contenido. `tests/check.py --rapido --baseline`: VERDE, 0 FAIL, 620 WARN. `tools/ci_guardias.py --ejecuta-huerfanos`: 106 ejecutados, 111 saltados, 0 fallidos. P4 y 12 circuitos/936 filas sintéticas contra el adaptador fusionado: PASS. Ningún histórico ni dato real modificado.
