# Lanzamiento · cinco encargos adicionales 33–37

Corte: 12 de septiembre de 2026 UTC, main `e37367581d5186ce4d4cf497377c83ebcd61cf93`. Consultados contenido de main, notas/cierres pertinentes y PR abiertos. Es preparación de ejecución; no se han corrido estos cinco encargos desde ChatGPT.

## Lo que ya está en marcha

- #721, #722, #723 y #724 están fusionados. #723 desbloqueó los insumos de 27/28; #724 archivó 27–31, pero archivar no es ejecutar ni firmar.
- #725 sigue abierto y entrega IMOR temporal: corresponde al 28; no se repite.
- #726 sigue abierto y desarrolla demanda→residual→cron: corresponde al 32. Su descripción todavía anuncia despliegue/corrida real posterior; no dar producción por terminada desde ese texto.
- Por la indicación de Jonás, tratar 27, 29, 30 y las continuaciones vigentes como ocupadas aunque no tengan aún PR. GitHub no permite ver procesos locales no publicados.
- #727 acaba de abrir otro censo; su cuerpo no demuestra por sí solo una adquisición efectiva. No añade un encargo nuevo.
- #728 prepara el 31: sus 5 IDs DIN y 3 TRA ya están materializados según el PR, cero llamadas y estado PENDIENTE DE FIRMA. No duplicar esa materialización ni alterar sus paquetes desde 33/34.
- 31 exige su autorización explícita de FP-373. «Todo corre en CLI» no cambia la identidad del competidor ni firma por sí solo una nueva captura. Esta tanda no añade llamadas F5 ni habilita FP-374/F6.

## Tanda adicional

| Encargo | Resultado tangible | Puede empezar | Frontera principal |
|---|---|---|---|
| 33 · Corpus compartido | Datos adquiridos accesibles desde todas las sesiones; resolución del lote NC-0059 | Ahora | No tocar cron ni worktrees activos |
| 34 · Reactivos con texto | Índices actualizados, búsquedas reales y extracción incremental sin LLM | Ahora, con archivos ya disponibles | Índices/buscador; preservar citas históricas |
| 35 · Tandas longitudinal | Matrices de entrada/salida y pérdida de seguimiento ENNViH | Ahora, con crosswalk y corpus | CALC sucesor; no confundir salida con impago |
| 36 · Datos N34 | Descargas y lectura de fuentes sobre producto/costo/daño del consumidor | Ahora | Integración de residuales coordinada con #726 |
| 37 · Delta | Comando operativo y comparaciones reales con alcance explícito | Ahora | Adaptador en corrida0 coordinado con 30 |

**Son cinco encargos distintos de 27–32.** Adjunta un MD por sesión. Cada uno contiene fases, autoridad al despacho, límites, pruebas útiles y cierre; puede seguir hasta PR sin pedir el encargo de la fase siguiente.

## Paralelo de trabajo y orden de integración

No existe una cadena global de cinco merges. 33, 34 y 35 entregan resultados independientes; 34/35 consumen archivos de 33 sólo cuando realmente les falten. 36 descarga en staging propio mientras #726 trabaja y después integra sus objetos con el mecanismo consolidado. 37 desarrolla módulo/ejemplos aparte y concilia su pequeño adaptador con 30.

Los registros comunes se integran por identidad. No copiar completos `manifiesto`, `no-corrido`, `corridas`, `resultados`, `usos` ni índices desde una rama atrasada. El cron conserva un solo dueño: 32/#726. Ningún otro encargo cambia scheduler, ejecutor o selección.

Se pueden abrir las cinco sesiones. Con 27/30 y el cron también activos, iniciar 33 y 36 mientras 34/35 preparan documentación/spec y 37 implementa. Escalonar las fases que descomprimen o leen grandes archivos: como pauta inicial, máximo dos de esas lecturas pesadas a la vez; ajustar a la carga observada. No instalar un orquestador nuevo para administrar esta tanda. No es una restricción de firmas ni una obligación de secuenciar los PR.

## Decisiones

El despacho autoriza el panel descriptivo del 35 y la comparación explícita del 37, dentro de sus contratos. No hace falta definir una materialidad científica para calcular un delta rotulado como no determinable. 33/34 son ejecución técnica; 36 es adquisición pública dirigida ya alineada con la búsqueda autorizada de datos.

Siguen fuera: adopción causal de N34/R8.2, inferencia DIN/S6 no acreditada, compras/accesos de terceros, envío de solicitudes personales, nueva evaluación F5. No convertir esos pendientes en freno de los cinco resultados autorizados.

## Prompt único de despacho

> Ejecuta íntegramente el MD adjunto en un worktree propio de CLI. Autorizo su alcance explícito, commits, push y PR; el merge queda conmigo. Los encargos anteriores siguen ocupados: contrasta main y PR pertinentes y no dupliques trabajo. Reutiliza herramientas y decisiones, resuelve el acceso al corpus y continúa hasta el resultado operativo, sin cerrar sólo con inventarios, pruebas o planes. Coordina únicamente los archivos compartidos indicados; no cambies el cron de #726 desde otra tarea.

## Fuentes de la selección

- [#700 · Tandas](https://github.com/Josanoforo/Modelado-Mexicano/pull/700): panel entrada/salida explícitamente residual.
- [#723 · Fuentes financieras](https://github.com/Josanoforo/Modelado-Mexicano/pull/723): adquisición IMOR/ENSAFI y residual NC-0164.
- [#724 · Encargos 27–31](https://github.com/Josanoforo/Modelado-Mexicano/pull/724): cartera anterior y firma separada de 31.
- [#725 · IMOR](https://github.com/Josanoforo/Modelado-Mexicano/pull/725) y [#726 · Adquisición](https://github.com/Josanoforo/Modelado-Mexicano/pull/726): frentes abiertos que esta tanda respeta. [#728 · Preparación F5](https://github.com/Josanoforo/Modelado-Mexicano/pull/728) sigue pendiente de firma; [#727](https://github.com/Josanoforo/Modelado-Mexicano/pull/727) es otro censo.
- `forense/no-corrido.tsv`: NC-0059, NC-0100, NC-0136, NC-0037, NC-0091/0048 y NC-0164.
- `tools/corrida0.py`: stub actual de delta; `tests/manifiesto.py`: verificación repetible por ID; extractores y buscador existentes de reactivos.
