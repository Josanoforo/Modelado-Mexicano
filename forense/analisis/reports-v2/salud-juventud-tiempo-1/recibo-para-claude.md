# Recibo para Claude · C3 salud, juventud y tiempo

**EJECUTADO:** rama `codex/astra6-c3-salud-juventud-tiempo-1`, worktree `/home/pc0/mm-astra6-c3-salud-juventud-tiempo-1`, corte de redacción `7748208614570a50a97c1ba830aee72a972185f9`. El encargo recibido está en `forense/encargos/2026-09-27-ASTRA6-C3-SALUD-JUVENTUD-TIEMPO-1.md`; SHA-256 del cuerpo normalizado `7fe46fac74cc177dce09dcb68994731e1552f3e80269f02426a26be73cb764d9`. Los adjuntos embebidos pasaron sus tres hashes. Firma «Acordado» citada del asiento previo, sin duplicación.

**Objetos para revisar:** [índice y conteos](indice-local.md), [SHA-256 por ruta](identidades-producto.tsv), [salud](../../../../corpus/reports-v2/Health__Body__Food_and_Substance_Use_in_Mexico__The_Behavioral_Layer_of_Decisions__Environment_and_Structure.md), [juventud](../../../../corpus/reports-v2/Psicología_de_la_Juventud_Mexicana_Contemporánea__Gen_Z_y_Millennials_Jóvenes_como_Cohorte_Divergente.md), [tiempo](../../../../corpus/reports-v2/El_Mexicano_y_el_Tiempo__Estructura__no_Cultura__en_la_Planeación_y_el_Compromiso_Temporal.md). Cada pieza incluye tabla de afirmaciones, productor y verificador en su subdirectorio. El manifiesto de hashes lista archivo recibido, tres reports y tres tablas; no se presenta como sello de RESULT.

**LEÍDO:** originales completos por bloques, 39/32/38 identidades de mapa y 13/5/7 afirmaciones materiales adicionales. Las trazas cuantitativas de salud están en `salud/cifras.json`; las cuatro de tiempo en `tiempo/trazas-result.tsv`; juventud cita celdas ENDUTIH con índice, denominador, hashes y firma en el propio report. Las cifras externas llevan fuente primaria, población/método y límite; no se atribuyen a RESULT. Las inferencias causales, edad–periodo–cohorte, denominadores y las 12 ROMPE requieren revisión humana dirigida.

**Comandos EJECUTADOS desde la raíz:**

```bash
python3 forense/analisis/reports-v2/salud-juventud-tiempo-1/producir_lote.py --check
python3 forense/analisis/reports-v2/salud-juventud-tiempo-1/verificar_lote.py
python3 tools/sella_sha256.py --cuerpo --verifica forense/encargos/2026-09-27-ASTRA6-C3-SALUD-JUVENTUD-TIEMPO-1.md
python3 tests/check.py --rapido
python3 tools/corrida0.py status
```

**Resultados EJECUTADOS:** verificador local VERDE; gate rápido 0 FAIL y 624 WARN. No se corrió microdato ni se creó CALC/RESULT. El contador de adopciones no aumenta por este lote. `tools/entorno.py --arranque` devolvió INDETERMINADO, con `data/raw` ausente en el worktree.

**PROPUESTO:** diez reglas editoriales en [hoja para mesa](hoja-para-mesa.md), sin adopción. La recepción de las reglas y la adjudicación de extractos públicos reservados constan en dos FP propias, ABIERTAS. Opción recomendada: conservar propuestas para revisión futura y mantener excluidos los extractos, sin permiso retroactivo.

**NO-VERIFICADO:** recepción independiente de Claude, fusión, validez inferencial por C1 y eficacia predictiva. En la revisión del PR, comprobar manualmente correspondencia prosa–tabla para las 12 ROMPE, tres comparaciones centrales y los mecanismos propuestos; confirmar que EDER 2025, ENADID 2023 y ENCODAT 2025 no aportan cifras o inferencias al producto final. Los incidentes están delimitados en los expedientes de juventud y salud; una publicación pública no levanta la reserva.
