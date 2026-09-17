# Cierre · GEN2-ENCO-DOS-OLAS-RESERVADAS-1

Estado del producto: **EJECUTADO Y PREPARADO; NO SELLADO, INTEGRADO NI
ADOPTADO**. Se adquirieron y reservaron las dos olas fijadas antes de ver
respuestas. No se abrió ninguna fila, no se calculó una tasa y no se ejecutó F6.

| Fecha | Bytes e identidad | Reserva | Definición | Falta para medir | Falta para comparar con M |
|---|---|---|---|---|---|
| junio 2025 | Sí; 159 172 B; SHA-256 `fd283a1a…`; ZIP/CRC y tres miembros DBF validados | `RESERVADA-NO-ABIERTA-NO-INDEXAR-L` en raíz lógica no escaneable | Completa para punto descriptivo P10: persona elegida 18+, Sí=1, No=2, No sabe=3, sin ingresos=4, FACTOR | autorización de lectura acotada; gate de códigos; contrato de varianza/covarianza por panel | puente científico pre-R entre posibilidad percibida y stock de ahorro; hoy `M-NO-ELEGIBLE` |
| junio 2026 | Sí; 164 273 B; SHA-256 `f1c10fb4…`; ZIP/CRC y tres miembros DBF validados | respuestas de junio no abiertas; cegamiento de familia parcial por exposición incidental a tabulado del mes anterior | Misma P10/FACTOR; cambio geográfico estructural registrado; definición completa para punto descriptivo | los mismos tres gates; no asumir independencia respecto de 2025 | el mismo puente; adquirir/definir no vuelve elegible a M |

## Producto utilizable

- reserva prospectiva y encargo verbatim;
- recibos con URL final, tipo, tamaño, SHA, miembros y ruta lógica;
- cuatro entradas aditivas únicas de manifiesto (dos olas y dos documentos);
- contrato documental/spec y tarjetas legibles;
- `tools/enco_reserva_prepara.py`, que sólo inspecciona cabeceras DBF,
  valida tarjetas, publica sin reemplazo y ejecuta fixtures sintéticos;
- pruebas de códigos especiales, “No tiene ingresos”, denominador vacío,
  pesos inválidos, escalas y barrera contra lectura accidental de filas.

La comprobación requerida de reutilización se ejecutó como `python3
tools/ya_medido.py dinero.ahorro.tiene_ahorros` y devolvió `MEDIDA-EN:
tramite-ola5-propuesta-v0.yaml, tramite.yaml`. Es evidencia de que la tasa de
stock M ya existe, no de equivalencia con la posibilidad percibida de P10.

La adquisición está completa. La definición está completa para un punto
descriptivo, no para inferencia de diseño: faltan llaves/receta operativa de
estrato, covarianza por panel y política firmada ante estratos singulares. La
elegibilidad experimental está incompleta por constructo, no por bytes.

## CIERRE COMPARTIDO DIFERIDO

Este PR no toca `decisiones.tsv`, `no-corrido.tsv`, firmas, hallazgos, PARA,
gobernanza, estado, rótulos, tableros, contadores, colas, registro global ni el
panel F6. Después del trámite de Opus, la integración serial deberá: (1)
reconciliar las cuatro adiciones de manifiesto conservando cambios concurrentes;
(2) propagar que R10 ya tiene dos olas adquiridas pero sigue sin enlace M; y (3)
mantener los ZIP fuera del índice/corpus L.

## Decisiones siguientes (máximo tres)

1. Autorizar o no una medición **descriptiva** de P10, fijando qué ola se abre
   primero y si esa apertura consume la reserva para B/F6.
2. Aprobar un puente científico pre-R con `dinero.ahorro.tiene_ahorros` o
   ratificar `M-NO-ELEGIBLE-PARA-ESTE-ESTIMANDO`.
3. Fijar el contrato de varianza interanual que represente panel compartido,
   estrato/UPM y estratos singulares; sin él sólo procede el punto ponderado.

Base de trabajo: `origin/main@e4f5f771b7fd9bccc88d3b6c30d0e5362b0e52a5`.
COMMIT 1 de reserva: `d171066`. El SHA final y el PR se registran en la entrega
de Git; una publicación no constituye adopción científica.

Este acto deja más cerca una **medición descriptiva bien definida**, sin fingir
que también resolvió la comparación con M.
