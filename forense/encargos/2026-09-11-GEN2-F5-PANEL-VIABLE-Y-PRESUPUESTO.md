# ACTO GEN2-F5-PANEL-VIABLE-Y-PRESUPUESTO

SHA de redacción: `70c64d9ead92384ece0eaf18cbfb53372bb88a74` (`origin/main`, verificado 11/sep/2026).
Entorno asignado: **NUBE**; CLI compatible sólo si el inventario documental requiere corpus local. No autoriza microdatos en nube.
Estado: **CONSUMIDO**.

## VERIFICACIÓN DE EXISTENCIA

- Estructura: `AGENTS.md`, `/acto`, las dos specs F5, snapshot GEN2 de #712, contratos de linaje/emisión, manifiesto, usos/resultados, FP-373/374, NC-0160/0161/0162 y benchmark #708 existen en `origin/main` al SHA de redacción.
- Contenido: #713 está fusionado y conserva `NO-ADJUDICABLE-POR-CONTROL`; #712 y #708 están fusionados. No había PR abiertos al arranque. El worktree paralelo del encargo 23 existía todavía sin cambios respecto de `origin/main`.
- Cobertura retroactiva: este encargo sucede a #713 y no sustituye sus specs ni el reanálisis histórico. Los valores R reservados, capturas L y emisiones M quedan expresamente fuera de lectura/ejecución para selección.

## Texto del encargo (verbatim)

ACTO: GEN2-F5-PANEL-VIABLE-Y-PRESUPUESTO
ENTORNO: NUBE
Compatible con CLI cuando el inventario documental requiera corpus local.
REPOSITORIO: Josanoforo/Modelado-Mexicano

OBJETIVO

Convertir las propuestas de #713 en una decisión ejecutable:
qué panel puede evaluarse, qué fuentes lo sostienen, qué puede cubrir M,
cuánto costaría y qué pregunta respondería.

Entregar candidatos nominales y protocolo concreto. No repetir el
diagnóstico del panel histórico ni entregar otra propuesta genérica.

AUTORIDAD Y OPERACIÓN

Autoriza investigación documental, análisis del inventario, preparación
de contratos/specs propuestas, documentación, commits, push y PR.
Jonás conserva la fusión y la decisión sobre llamadas y experimentos.

Lee AGENTS.md. Reporta worktree, rama, HEAD y estado inicial.
Comprueba main y PR abiertos para reutilizar cualquier avance posterior.
Archiva este encargo y usa los registros existentes.

No autoriza capturas L, emisiones experimentales M, nuevas estimaciones R,
apertura de R reservados ni uso de esos valores para seleccionar el panel.

ANTECEDENTES

#713 publicó NO-ADJUDICABLE-POR-CONTROL para el panel histórico:
0 celdas conjuntas puntuables bajo los controles nuevos.
Eso no evaluó el snapshot renovado de #712.

FP-373: recuperación documental de dos celdas, propuesta de 32 llamadas.
FP-374: transferencia reservada, piloto de 192 llamadas y confirmación
de 384–960; máximo total propuesto de 1,152.

La propuesta de transferencia todavía requiere familias concretas,
fuentes y un snapshot elegible. Las réplicas L no son familias nuevas.

ARCHIVOS INICIALES

- forense/prereg-duelo-v2/F5-documental-dirigida-spec-v1_0.md
- forense/prereg-duelo-v2/F5-transferencia-reservada-spec-v1_0.md
- Snapshot GEN2 explícito de #712
- Contratos de linaje, selección temporal y emisión
- Manifiesto, usos y resultados
- FP-373/374 y NC-0160/0161/0162
- Benchmark de cuatro decisiones fusionado en #708

FASE 1 — INVENTARIO NOMINAL Y EXPOSICIÓN

Construye una tabla de candidatos con:
familia, encuesta/fuente, ola, población, unidad, evento, códigos,
disponibilidad temporal, fuente de diseño, acceso, consumidor M posible
y evidencia de exposición previa.

Clasifica:
- conocido durante desarrollo;
- candidato potencialmente reservado;
- indeterminado;
- no comparable o no disponible.

Revisa si Gen1/Gen2 usaron la familia para escoger reglas, parámetros,
arquitectura, filtros o diseño. Renombrar o cambiar de ola no prueba reserva.

No abras valores R reservados para evaluar qué candidato conviene.
Si una fuente ya expone el objetivo, registra esa exposición.
No certifiques ausencia de exposición en el preentrenamiento del LLM.

FASE 2 — VIABILIDAD REAL DEL MOTOR Y LAS FUENTES

Para cada candidato, documenta el camino que permitiría producir M
y verificar R: contratos, datos anteriores al corte, unidades compatibles
y disponibilidad de diseño.

Usa inspección estática e inventario para preparar esta fase. No emitas
predicciones experimentales ni ajustes M con el objetivo reservado.

Coordina el formato con el encargo 23 y consume su contrato cuando esté
fusionado. No modifiques el emisor en este encargo.

Distingue origen numérico, validez de la medición, compatibilidad del
estimando e independencia de evaluación. Una firma o etiqueta no
sustituye evidencia; tampoco exijas conocer el acierto de la predicción
antes de poder evaluar una predicción retenida.

Entrega el número acreditado de familias disponibles y las indeterminadas.
No declares viable el mínimo de 6 familias piloto más 12 confirmatorias
disjuntas si no puedes enumerarlas y sostener su separación.

FASE 3 — PROTOCOLO Y COSTO COHERENTES

Para FP-373:
- identifica las fuentes concretas disponibles de DIN y TRA;
- determina qué información vería cada brazo;
- conserva la distinción entre recuperación documental y generalización;
- propone tratamiento de fuentes ausentes sin inventar sustitutos.

Para FP-374:
- explicita hipótesis primaria, margen de mejora y efecto esperado;
- alinea fórmula de tamaño con el criterio de éxito del IC;
- define la unidad familiar y la dependencia entre celdas;
- fija tratamiento de abstenciones, cobertura, faltantes y varianza R;
- separa piloto y confirmación;
- enumera modelo, cliente, ventana y demás identidades que deberán
  congelarse antes de ejecutar.

Distingue llamadas previstas, máximo de reintentos técnicos y costo total.
No presupongas precios: usa configuración/precios verificables o expresa
el costo en llamadas/tokens con los supuestos necesarios.

FASE 4 — DECISIÓN QUE PUEDA TOMAR LA MESA

Entrega una opción recomendada y alternativas concretas:
- ejecución documental si sus fuentes están listas;
- piloto de transferencia si existe panel viable;
- ampliación de fuentes o rediseño si la reserva no es defendible.

Si no existe panel suficiente, entrega el máximo acreditado, las faltas
exactas y el cambio de diseño que permitiría avanzar. No abras una
búsqueda indefinida ni infles familias a partir de réplicas o etiquetas.

El producto debe permitir a Jonás elegir sin reconstruir el repo.

FASE 5 — CIERRE

Entrega PR con:
- tabla nominal de candidatos y exclusiones;
- mapa de capacidad M y disponibilidad de fuentes;
- protocolo propuesto con costo, éxito y parada;
- ficha breve para FP-373 y FP-374;
- siguiente encargo de ejecución listo, marcado como pendiente de firma.

Actualizar preparación no equivale a cerrar NC-0160/0161/0162 ni a
autorizar F6. Mantén intactos TRIADA-0002 y el reanálisis histórico.

No firmes DIN, S6, complementos ni deduplicación ENCIG mediante este PR.

Puede arrancar junto con 23, 24 y 26. La versión final del protocolo
deberá referenciar la interfaz corregida antes de una futura ejecución.

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| Ejecutar las 32 llamadas documentales de FP-373 | `DECISIÓN-DE-MESA-PENDIENTE` | no hubo capturas L, gasto ni cierre de `NC-0160`; fuentes identificadas no equivalen a transporte validado | encargo `GEN2-F5-DOCUMENTAL-EJECUCION`, ya preparado en cola y pendiente de firma de Jonás |
| Ejecutar piloto/confirmación FP-374 o abrir R | `PANEL-RETENIDO-INSUFICIENTE` | 0 familias retenidas ejecutables; `NC-0161/0162` siguen abiertas y F6 no se habilita | ampliación sólo con lista nominal previa de 18 familias × 2 celdas, consumidores M, acceso/diseño, split y snapshot elegible |
| Anclar la ejecución a la interfaz final del encargo 23 | `COMPUERTA-CUMPLIDA-SIN-EJECUCIÓN` | PR #720 ya está fusionado en `main=6cda0282`; este acto consume el contrato y no modifica el emisor por cuenta propia | el acto de ejecución verifica ascendencia, fija snapshot v1.1 e identidad de interfaz |

## CONSUMIDO

Consumido el 11/sep/2026 por **[PR #722](https://github.com/Josanoforo/Modelado-Mexicano/pull/722)**,
rama `acto/gen2-f5-panel-viable-y-presupuesto`, HEAD al abrir el PR
`25ec8d380690d5ffe8c6d58abf6257dc63482eb4`, contra
`origin/main=70c64d9ead92384ece0eaf18cbfb53372bb88a74`. Entrega tabla nominal,
mapa M/fuentes, protocolo y presupuesto coherentes, fichas FP-373/374 y un
siguiente encargo pendiente de firma. Sincronizado después con
`origin/main=6cda0282079e9623425529f51c2bea171657b0cf`, que fusiona el contrato
del encargo 23. Cierre canónico: `ADR-480`, L0 y rótulo
`GEN2-F5-PANEL-VIABLE-Y-PRESUPUESTO`. Línea base verde sin entradas nuevas.
Este asiento registra el PR real; no afirma fusión, firma ni ejecución.
