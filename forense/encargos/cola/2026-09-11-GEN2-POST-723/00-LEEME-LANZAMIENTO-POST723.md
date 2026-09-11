# Lanzamiento · GEN2 · encargos 27–31

Fecha de preparación: 11 de septiembre de 2026. Corte actualizado: `main=6cda0282079e9623425529f51c2bea171657b0cf`, que contiene #720. #719 también está fusionado. #721, #722 y #723 seguían abiertos al último contraste.

**Paquete de ejecución:** cuatro encargos pueden avanzar con las dependencias indicadas y uno queda listo para firma de llamadas. Cada MD contiene el contrato completo; adjunta un archivo por tarea.

## Qué cambió y por qué sigue esta tanda

- [#719](https://github.com/Josanoforo/Modelado-Mexicano/pull/719) reporta el correctivo de adquisición desplegado y una ejecución programada con cola vacía sin invocar un LLM. [#721](https://github.com/Josanoforo/Modelado-Mexicano/pull/721) conserva el recibo. No se vuelve a encargar el cron.
- [#720](https://github.com/Josanoforo/Modelado-Mexicano/pull/720) quedó fusionado: selección autenticada y snapshot sucesor, con 16 salidas directas conservadas. Ahora se puede ofrecer una consulta operativa y acreditar sus números por implementación independiente.
- [#723](https://github.com/Josanoforo/Modelado-Mexicano/pull/723) propone 123 meses de IMOR por cinco productos y resultados ENSAFI sobre atraso/afrontamiento. Al fusionarse, dejan de ser búsquedas pendientes y permiten análisis registrados.
- [#722](https://github.com/Josanoforo/Modelado-Mexicano/pull/722) entrega el inventario: 0 familias retenidas ejecutables para la confirmación grande. Deja preparado el estudio documental de 32 posiciones; no corresponde volver a encargar ese inventario ni lanzar 1,152 llamadas.

## Encargos y orden

| Archivo | Entrega | Entorno | Cuándo iniciar la ejecución dependiente |
|---|---|---|---|
| [27 · ENSAFI](27-GEN2-ENSAFI-MEDICION-DESCRIPTIVA-CON-DISENO.md) | 13 estimandos nominales registrados; denominadores, diseño e incertidumbre cuando se acredite | CLI/CAJA | Tras merge #723 |
| [28 · IMOR](28-GEN2-IMOR-CONTEXTO-TEMPORAL-POR-REGIMEN.md) | Tablas y gráficos temporales por régimen; ficha contextual para R1.6 | Cloud o CLI | Tras merge #723 |
| [29 · Consulta GEN2](29-GEN2-CONSULTA-OPERATIVA-CON-CONTRATO.md) | Comando de consulta con salida legible/JSON, origen, alcance y no cobertura | Cloud o CLI | **Ya**, desde #720 fusionado |
| [30 · Parámetros activos](30-GEN2-VALIDACION-INDEPENDIENTE-PARAMETROS-ACTIVOS.md) | Validación numérica independiente y overlay consumido por el motor | CLI/CAJA | **Ya**, desde #720 fusionado y con corpus |
| [31 · F5 documental](31-GEN2-F5-DOCUMENTAL-EJECUCION-PARA-FIRMA.md) | 32 posiciones, análisis y cierre del experimento documental | CLI/CAJA | Tras merge #722 y firma explícita incluida en el MD |

27/28 pueden prepararse mientras se fusiona #723. No conviene ejecutar su cálculo definitivo contra una cabeza abierta que luego cambie. 29 y 30 pueden trabajar simultáneamente: 29 implementa consulta; 30 produce evidencia de validación. Ninguno espera que el otro termine para desarrollar su parte.

El recibo #721 puede integrarse independientemente. #722 y #723 no imponen entre sí un orden científico; cada sucesor consume su propio antecedente fusionado.

## Autorización y decisiones

Al despachar 27 se aceptan las clases amplias ENSAFI para los estimandos descriptivos explícitos del documento. Al despachar 28 se autoriza el análisis contextual de IMOR por régimen. Sus resultados no se adoptan automáticamente como parámetros de N34/R1.6.

29 y 30 usan parámetros ya adoptados. La validación independiente de cálculo no crea independencia de muestra ni un holdout.

**31 permanece pendiente de firma.** Texto listo en su MD: 32 posiciones y techo de 96 solicitudes al proveedor, con el modelo competidor efectivo ya registrado en F5 y sin sustitución silenciosa. El techo incluye reintentos y solicitudes adicionales del cliente. Codex puede ejecutar el encargo sin que eso cambie al competidor. Si la identidad no está disponible, el ejecutor presenta una alternativa concreta antes de llamar.

FP-374 y F6 siguen sin habilitarse. DIN/FP-371, S6/FP-372, NC-0085 y NC-0107 no se firman con esta tanda. No se agregan al final como obligaciones implícitas que impidan cerrar los nuevos resultados.

## Prompt de lanzamiento para 27–30

> Ejecuta íntegramente el MD adjunto en este repositorio. Queda autorizado su alcance técnico y científico explícito, los commits, push y PR; la fusión queda conmigo. Comprueba las dependencias en main, consume lo ya resuelto y continúa entre fases sin pedirme otro encargo. Si falta corpus, resuelve la configuración y el acceso antes del cálculo. Termina con el resultado utilizable y su cadena de cierre; no entregues sólo un plan o tests. Respeta las decisiones expresamente reservadas.

Para 31, usar además el texto de autorización de su propio archivo cuando Jonás decida ejecutarlo. Adjuntar el MD sin esa decisión no autoriza llamadas.

## Integración y evidencia compartida

Una tarea por worktree/rama/PR. Mantener el corpus compartido como fuente; salidas específicas por tarea. Los registros comunes se actualizan por identidad con el escritor canónico. Quien integra después concilia sus filas y vuelve a derivar vistas; no reemplaza el registro del otro.

29 consume el overlay existente aunque todavía diga NO-HECHA. Al fusionar 30 se comprueba la lectura de la evidencia nueva, sin repetir el cálculo independiente. 27/28 no entran automáticamente al perímetro congelado de validación de 30.

Los MD son autónomos y no dependen de esta guía para su contrato. Este paquete no ejecutó cálculos, llamadas ni modificaciones en el repositorio: prepara el despacho a partir de los resultados y estados consultados.
