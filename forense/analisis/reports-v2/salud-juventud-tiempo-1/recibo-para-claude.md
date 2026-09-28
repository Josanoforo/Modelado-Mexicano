# Recibo para Claude · C3 salud, juventud y tiempo

**EJECUTADO:** rama `codex/astra6-c3-salud-juventud-tiempo-1`, worktree `/home/pc0/mm-astra6-c3-salud-juventud-tiempo-1`, corte de redacción original `7748208614570a50a97c1ba830aee72a972185f9`; corrección desde `15a581898bcec9e04914e253b466d2c3afc86860`. Encargo inicial: `forense/encargos/2026-09-27-ASTRA6-C3-SALUD-JUVENTUD-TIEMPO-1.md`, SHA-256 de cuerpo normalizado `7fe46fac74cc177dce09dcb68994731e1552f3e80269f02426a26be73cb764d9`. Encargo correctivo: `forense/encargos/2026-09-27-ASTRA6-C3-CORRECCION-1242-1.md`, SHA-256 de cuerpo normalizado `a88a905ba76306e15edd64572e0e4f04d8aed50ac3b816c727b3d001e1b01a0e`. Los tres adjuntos de cada cuerpo pasaron sus hashes. Firma «Acordado» citada del asiento previo, sin duplicación.

**Objetos para revisar:** [índice y conteos](indice-local.md), [SHA-256 por ruta](identidades-producto.tsv), [salud](../../../../corpus/reports-v2/Health__Body__Food_and_Substance_Use_in_Mexico__The_Behavioral_Layer_of_Decisions__Environment_and_Structure.md), [juventud](../../../../corpus/reports-v2/Psicología_de_la_Juventud_Mexicana_Contemporánea__Gen_Z_y_Millennials_Jóvenes_como_Cohorte_Divergente.md), [tiempo](../../../../corpus/reports-v2/El_Mexicano_y_el_Tiempo__Estructura__no_Cultura__en_la_Planeación_y_el_Compromiso_Temporal.md). Cada pieza incluye tabla de afirmaciones, productor y verificador en su subdirectorio. El manifiesto de hashes lista ambos cuerpos recibidos, tres reports y tres tablas; no se presenta como sello de RESULT.

**LEÍDO:** originales completos por bloques, 39/32/38 identidades de mapa y 13/8/7 cláusulas adicionales, total 137 decisiones editoriales: 3 CONFIRMA, 35 MATIZA, 9 ROMPE, 90 SIN-CIFRA. Salud queda sin modificación sustantiva en esta corrección; sus trazas están en `salud/cifras.json`. Tiempo conserva cuatro RESULT ENIF en `tiempo/trazas-result.tsv`; juventud cita celdas ENDUTIH con índice, denominador, hashes y firma. La cifra externa ENOE histórica conserva denominador de ocupados; las publicaciones ENUT 2024, ENIF 2024 y ENSU dic/2025 dejaron de sostener el report de Tiempo. Las 9 ROMPE y los mecanismos centrales requieren revisión humana dirigida.

**Comandos EJECUTADOS desde la raíz:**

```bash
python3 forense/analisis/reports-v2/salud-juventud-tiempo-1/producir_lote.py --check
python3 forense/analisis/reports-v2/salud-juventud-tiempo-1/verificar_lote.py
python3 tools/sella_sha256.py --cuerpo --verifica forense/encargos/2026-09-27-ASTRA6-C3-SALUD-JUVENTUD-TIEMPO-1.md
python3 tools/sella_sha256.py --cuerpo --verifica forense/encargos/2026-09-27-ASTRA6-C3-CORRECCION-1242-1.md
python3 tests/check.py --rapido
python3 tools/corrida0.py status
```

**Resultados EJECUTADOS:** verificador local VERDE; gate rápido 0 FAIL y 624 WARN. No se corrió microdato ni se creó CALC/RESULT. El contador de adopciones no aumenta por este lote. `tools/entorno.py --arranque` devolvió INDETERMINADO, con `data/raw` ausente en el worktree.

**PROPUESTO:** diez reglas editoriales en [hoja para mesa](hoja-para-mesa.md), sin adopción. Dos FP propias siguen ABIERTAS: recepción de reglas y adjudicación expresa de exposición documental en juventud, salud y tiempo. Opción recomendada: recibir el producto editorial saneado para revisión independiente, mantener excluidas las fuentes reservadas y no otorgar permiso retroactivo.

**NO-VERIFICADO:** recepción independiente de Claude, fusión, validez inferencial por C1 y eficacia predictiva. En la revisión del PR, comprobar manualmente correspondencia prosa–tabla para las 9 ROMPE y mecanismos centrales; comprobar que las citas Berkeley/Mitofsky del v1 no se presentan como errores que el original no cometió y que el colchón corto ENIF se lee en la dirección correcta. Confirmar exclusión de EDER 2025, ENADID 2023, ENCODAT 2025 y las publicaciones ENUT 2024, ENIF 2024 y ENSU dic/2025. Los tres expedientes de exposición delimitan superficie y efecto; una publicación pública no levanta la reserva.

**EJECUTADO:** [PR #1242](https://github.com/Josanoforo/Modelado-Mexicano/pull/1242) abierto tras integrar `origin/main` hasta `3facfa9f3b39b36ac6585baf23aaecedb424d948`. El encabezado `CONSUMIDO` se añadió al pie del encargo sin reescribir el cuerpo; el SHA-256 completo del archivo actualizado se regenera en `identidades-producto.tsv`. El PR solicita recibo independiente y queda sin fusión propia.

**Corrección EJECUTADA:** desde `15a581898bcec9e04914e253b466d2c3afc86860`, commit correctivo `8a594361` e integración `origin/main` en `f003edc670ccdb98972dff2a1db2f7efca871f19` (base integrada `3ac3ab7d32c640d0f0081339f77b4287c9f7bd10`). El cuerpo correctivo `a88a905ba76306e15edd64572e0e4f04d8aed50ac3b816c727b3d001e1b01a0e` quedó inalterado al añadir el cierre al pie. `identidades-producto.tsv` contiene los SHA-256 completos de ambos archivos de encargo, tres reports y tres tablas. Verificador conjunto y `tests/check.py --rapido` pasaron después del merge: 0 FAIL, 624 WARN; la ejecución CI del nuevo HEAD se consulta por separado. El cuerpo del PR se actualizó para solicitar recibo de la versión saneada. Ninguna aprobación, recepción ni fusión se infiere de esa actualización.
