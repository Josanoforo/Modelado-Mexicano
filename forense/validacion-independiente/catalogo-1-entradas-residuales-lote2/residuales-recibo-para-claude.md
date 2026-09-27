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
