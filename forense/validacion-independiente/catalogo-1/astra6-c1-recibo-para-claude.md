# Solicitud de recibo técnico · ASTRA6 C1

PENDIENTE: este archivo no es un recibo obtenido. Revisión por circuito de mesa, sin mensajes externos de esta sesión.

Revisar corte `4f125e709d3b3830078fe749c82068b3d55e6e70`, cobertura exacta de universo.tsv, identidad de los 68 paquetes, separación de preparación/ respecto de paquetes/ y primera prueba de lanzamiento. 9 paquetes disponibles (3371 estimadores); 59 incompletos con faltantes explícitos. Preparación no ciega; cero validaciones adjudicadas. No hay tasa global.

Comandos: `python3 tools/validacion/astra6_paquetes.py --verifica`; `python3 -m pytest -q tests/test_astra6_paquetes.py`. Primer lote ENDIREH 2021 comunitaria, 100 estimadores, materializado en caja; `lanza.sh --prueba` pasa y `--ejecuta` no se corrió.

Adopciones: las referencias del catálogo se verificaron al corte, sin duplicar la firma Acordado del encargo ni modificar decisiones. El preparador lee valores esperados exclusivamente fuera de entradas. Comparador preparado pero no ejecutado. Falta recibo real; mesa decide aceptación y merge.

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| P2 · Partición completa y entradas separadas | DIFERIDO-A:SIN-ASIGNAR: 59 paquetes con faltantes documentales, método mixto, tolerancia ausente o proyección autorizada pendiente; lista exacta en lotes.json y faltantes.json. | 32772 estimadores sin paquete completo; no cambia validación ni adopción. | SIN-ASIGNAR; continuación de preparación descrita en lanzamientos.md |
| Perímetro de cierre · recibo técnico de Claude | DIFERIDO-A:SIN-ASIGNAR: el recibo requiere revisión real por el circuito de mesa. | PR sin recibo; no se declara aceptado ni se fusiona. | SIN-ASIGNAR; GEN2-RECIBO-ASTRA-PRODUCTO-N por asignar en mesa |
