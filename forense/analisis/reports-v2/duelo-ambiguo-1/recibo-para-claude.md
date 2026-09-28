# Solicitud de recibo · GEN2-RECIBO-ASTRA-PRODUCTO-N

**EJECUTADO.** PR propio de `codex/astra6-c3-duelo-ambiguo-1`, sin fusión ni adopción. Corte de main `eda5bb9f871a85613cfb4eda7d40dc741e55d0b5`. Objeto: report v2 de duelo y pérdida ambigua, tabla de 55 dictámenes, 16 fuentes, productor/verificador, nota y hoja de reglas propuestas. No se solicita considerar un recibo ya concedido.

| Objeto | SHA-256 |
|---|---|
| `corpus/reports-v2/Ausencia_sin_certeza__duelo_y_pérdida_ambigua_en_familias_de_personas_desaparecidas_en_México.md` | `0c4b7e99c701cddffc3759dc4db49b46f83312661bfd0cfdd646bc840397ce58` |
| `forense/analisis/reports-v2/duelo-ambiguo-1/decisiones.json` | `8fbc897467e3dac40ae0779fb6231f5a6de40a79a01b47e474a04601ff49b555` |
| `forense/analisis/reports-v2/duelo-ambiguo-1/tabla-afirmaciones.tsv` | `99c00accf545dfa4e5068f6489ca346a9a57303345da0fcbbe7b17eaaf94b9b7` |
| `forense/analisis/reports-v2/duelo-ambiguo-1/fuentes.md` | `916b3d825ad7f0c04548604bd4ba55518f96ec7cba31b1ab7b641a7a9d6b9e13` |
| `forense/analisis/reports-v2/duelo-ambiguo-1/tabla.py` | `b3b3cf3bd0fd2c7cbedb65ccc007f9b99a6ab3840f0a6c0db64f470cbb7bcd5b` |

**LEÍDO.** V1 blob `3158360ba0199af398a43f373ba48bccb40d6791`, mapa SHA-256 `1e3b06565ac399fccc81942ec33604f5994b2c4b6c91d132d2fbcb3499e4b1ec`; fuentes F01–F16 con alcance en fuentes.md. F10 y F12 solo ficha/resumen; F11 método editorial visible. Ninguna ola reservada.

**Comandos/resultados.** `python3 forense/analisis/reports-v2/duelo-ambiguo-1/tabla.py --check` → OK, 41/41 filas de mapa y 14 extras. `python3 tests/check.py --rapido` → 0 FAIL, 622 WARN heredados. `git diff --cached --check` detecta únicamente la línea vacía final del cuerpo recibido que se preserva byte por byte; excluido ese adjunto, sin avisos. Cobertura editorial y transporte no equivalen a validación científica.

**Revisión humana focal.** Verificar tres ROMPE clínicos, CED por etapas, stock CIDH/RNPDNO, 72 horas, selección del estudio colombiano, comparación institucional y toda cifra externa. Confirmar que las correcciones históricas del mapa permanecen: esperanza asociada sin causalidad y búsqueda legal inmediata. Regla por regla en [hoja](hoja-reglas-propuestas.md), sin adopción.

**NO-VERIFICADO.** Ningún RESULT propio ni prevalencia mexicana; no se verificó número vivo del RNPDNO; la decisión de Claude y la fusión corresponden al circuito de mesa. Este archivo solicita recibo, no lo acredita.
