# ENCARGO · GEN2-RELEVO-ENCUCI-F2-1

**Entorno:** Codex CLI o Claude Cloud, sin microdatos. **Producto:** escritor y vista de relevos que apliquen F-2 a RES-0005 con su condición F-1, preservando veredicto histórico y resolución efectiva. No mide ni cambia cifras.

## 1. Problema observado y autoridad existente

Al corte consultado, `data/corrida0/relevo-usos-v1_0.tsv` presenta simultáneamente para RES-0005:

- consumidor `milpa/tramite.yaml:tramite.mordida.discrecional:solicitud_o_entrega_mordida_encuci2020`;
- estado YA-ADOPTADO con cita `RESULT-ENCUCI-A-P-CUALQUIERA`;
- valor GEN2 `0.12600561008991654` y valor vigente `0.126006`;
- veredicto sellado `NO-ADOPTABLE-POR-DISCREPANCIA`, de `CALC-ENCUCI-0001/RESULT-ENCUCI-A-ADOPCION-P3`.

La contradicción operativa tiene resolución firmada, todavía no materializada por F-3: F-2 declara superado el veredicto si el valor vigente coincide al grano del consumidor; de lo contrario se retira la cita. F-1 separa ese criterio de adopción de la tolerancia de reproducción 1e-06. #835 aplica únicamente F-3 a RES-0035; **no extenderlo por semejanza**.

Leer `forense/encargos/2026-09-15-GEN2-FIRMAS-MESA-2.md`, F-1/F-2 y tabla de residuales; fila NC-0217; `tools/relevo_usos.py`; `tests/test_relevo_remesas_f3.py`; `tests/test_relevo_candidatos_delta.py`; CALC-ENCUCI-0001 y fila vigente en milpa, sólo lectura. Localizar la implementación vigente de `_compara_adopcion` y su contrato sin editarla por comodidad.

## 2. Cambio preciso

1. Revalidar identidad de RES-0005, consumidor, CALC/RESULT y referencia de la firma; comprobar sello real y concordancia del resultado con el recibo. Reutilizar verificadores existentes. Un rótulo SELLADA en una tabla no sustituye comprobar los artefactos necesarios.
2. Leer **el valor actual del consumidor**, no sólo una copia histórica de demanda ni una constante incrustada en el test. Si las vistas están desfasadas, comparar contra milpa en memoria e identificar la diferencia sin lanzar cascada general.
3. Aplicar F-1 con la regla de representación/acreditación del grano del consumidor. No comparar únicamente `abs(delta)<1e-6`; usar la semántica vigente y mostrar el grano aplicado. No alterar valor, redondeo o tolerancia para que pase.
4. Si coincide y todas las identidades están acreditadas, la resolución F-2 queda efectiva: el veredicto histórico sigue legible como SUPERADO por decisión F-2 condicionada a esa comparación. La cifra y cita actuales permanecen iguales.
5. Diferenciar **veredicto sellado histórico** de **resolución de mesa vigente**. No inventar un RESULT sellado nuevo, ni llamar sellada a una resolución calculada, ni borrar el valor original. Usar las columnas/explicaciones existentes si pueden expresar ambos sin ambigüedad; sólo añadir un campo estrecho de resolución efectiva si es estrictamente necesario. No construir un sistema general de precedencias.
6. Fuera de RES-0005/consumidor exacto, F-2 no aplica. Si falta sello, firma, identidad, grano o valor, conservar estado no acreditado con causa y no promover automáticamente a YA-ADOPTADO.

La condición de F-2 se verifica en cada derivación; no debe quedar un “superado para siempre” que sobreviva a un cambio futuro del valor. Una misma firma no legitima otros pares ni otros consumidores.

## 3. Rama negativa y concurrencia con milpa

Hoy los valores conocidos coinciden al grano de seis decimales; verificarlo de nuevo. Este acto no escribe en milpa porque el piloto/Opus mantiene ese archivo.

Si el valor vigente real ya NO coincide, no cambiarlo para lograr coincidencia. El derivador debe exponer `CITA-PENDIENTE-DE-RETIRO-POR-F2` o equivalente no acreditado y preservar el motivo. Preparar un parche mínimo separado de retiro de **la cita exacta**, sin aplicarlo a milpa ni modificar números: la ejecución de ese retiro pasa al trámite serial de Opus. Marcar el PR como cumplimiento parcial de F-2 en ese caso. No afirmar que una cita se retiró cuando sólo se redactó el parche.

Este camino negativo es una contingencia, no una excusa para dejar sin ejecutar el caso acreditado. Si coincide, entregar escritor y vista corregidos completos sin pedir otra firma.

## 4. Pruebas y reproducción

Guardar la derivación base en salida temporal antes de editar. Añadir regresiones focales:

- pareja real, valor vigente y firma exacta permiten la resolución;
- discrepancia al grano no se aprueba aunque otra tolerancia numérica parezca pequeña;
- sello/identidad/firma ausente o inválida no pasa;
- cambio del valor vigente después de una resolución anterior vuelve a evaluar;
- otro consumidor/RESULT no hereda F-2;
- F-3 de RES-0035 conserva su salida y sus pruebas pasan.

Regenerar `data/corrida0/relevo-usos-v1_0.tsv` con su escritor canónico, nunca a mano. Comparar estructuradamente antes/después con la misma base: sólo RES-0005 cambia sustantivamente. Si se añade un campo de esquema, documentar la diferencia estructural y exigir valores neutrales en las demás filas; no declarar “una sola línea cambió” cuando no sea verdad. Separar cambios concurrentes provenientes de main de efectos de esta implementación.

No ejecutar mediciones, microdatos, cron o registro global. Verificar que padre/sellos y los números/citas de milpa permanecen intactos. No refactorizar F-3: reutilizar helpers sólo cuando ahorre código sin alterar su política.

## 5. Entregables y criterio de cierre

Perímetro: `tools/relevo_usos.py`, `tests/test_relevo_encuci_f2.py`, vista canónica mencionada y `forense/analisis/relevo-encuci-f2-1/`. Fuera: `tools/corrida0.py`, milpa, demanda-resultados.tsv, CALC/sellos, otros conflictos (NC-0244, RES-0047/0049), registros de mesa y manifiesto.

Entregar explicación antes/después con valor leído, resultado de comparación, evidencia de sello y autoridad F-2; script/pruebas/vista funcionales; nota de qué cierre administrativo queda. No abrir un expediente de auditoría nuevo ni duplicar el acto de remesas.

Terminado cuando el usuario de la vista puede distinguir el veredicto histórico de su resolución vigente, el caso negativo no pasa en silencio y F-3 sigue funcionando. Si sólo se modifica prosa sin conectar el derivador, el encargo no está cumplido.

## Ejecución, autoridad y concurrencia comunes

Preparado el 17/sep/2026 UTC contra `main @ 402d1a3d0e96f6d159e5c4763bbd93c01f234295` de `Josanoforo/Modelado-Mexicano`. Al ejecutar manda origin/main vigente. Este archivo autoriza su perímetro cuando Jonás lo lanza; no constituye una firma ya registrada ni una adopción científica.

1. Leer el encargo completo, AGENTS.md e instrucciones del perímetro. Reportar worktree absoluto, rama, HEAD y git status --short. Hacer fetch y comprobar si este mismo encargo ya corre o ya está integrado; continuar el trabajo existente si corresponde, sin duplicarlo. Revalidar sólo premisas materiales.
2. Una tarea/worktree/rama/PR. Se puede continuar en la misma conversación CLI. Si la rama anterior fue fusionada, abrir sucesora desde origin/main; preservar cualquier trabajo posterior mediante commits/parches explícitos. No reset/clean/force ni stash de árboles ajenos. No confundir squash merge con falta de integración: comparar contenido pertinente.
3. Resolver corpus mediante tools/entorno.py, raíces locales y las opciones reales de tools/prepara_corpus.py. Ausencia de data/raw en un worktree no demuestra ausencia del corpus. No incorporar microdatos, identificadores individuales, rutas privadas o secretos a Git.
4. Autorizados al lanzar: cambios delimitados, pruebas focales, commits, push sin force y un PR. **Fusiones con Jonás.** Cero comunicaciones externas, cuentas, compras o llamadas experimentales a modelos. CLI para desarrollar no equivale a emitir L.
5. Sincronizar antes del push final, revisar diff/perímetro y ejecutar sólo las verificaciones afectadas. No debilitar checks, no recongelar baseline ni ampliar la tarea a reparar fallos heredados sin efecto material. Si una compuerta exige escribir fuera del perímetro, entregar el producto probado y el impedimento preciso para integración serial. Resolver defectos propios de nomenclatura sin alterar el contenido del encargo archivado.

### Perímetros vivos y reserva

CAREO #827, ENCO #834, remesas/F-3 #835 y ENCRIGE-carga #836 están fusionados al corte. Precisión WBES #837 está abierto: su contenido no se trata como consolidado. ENVIPE-U4-2013-2015, ENCIG2023-FLUJO-Y-ESTIMANDO-1 y MOCIBA-FLUJO-DOCUMENTAL-1 se consideran en curso aunque todavía no aparezca un PR. MEDICION-DEMANDA-3 conserva su dueño.

Opus conserva PILOTO-1/TRÁMITE-4, firmas, corte de edad, crosswalk, θ y adopciones del piloto. **No abrir ni derivar ENIF 2024 localidad × edad**, ni leer sus capturas/resultados reservados. No abrir respuestas MOCIBA/ISSP/ENCO ni olas retenidas de F6. El merge de CAREO no levanta reservas. No ampliar corpus L ni ejecutar herramientas generales que consuman reservas incidentalmente.

Excepción temporal de cascada autorizada por el lanzamiento: archivar este encargo verbatim en el directorio propio, con metadatos de procedencia/consumo fuera del bloque, y entregar producto; diferir decisiones.tsv, no-corrido.tsv, firmas-pendientes.tsv, hallazgos, PARA, gobernanza, estado, rótulos, tableros, contadores, colas y registro global. No reservar números ADR/NC/FP. No correr /tramite, /despacha, /deriva, cron ni registro --escribe. Sólo F-2 autoriza regenerar su vista específica mediante el escritor canónico; eso no autoriza una cascada global.

Manifiesto: ENIGH admite hasta dos documentos metodológicos nuevos y ENAPROCE hasta seis documentos instrumentales. Son adiciones por identidad, no regeneración completa. Preservar las adiciones concurrentes de ENCIG/MOCIBA/WBES y no duplicar un documento ya registrado. F-2 no toca manifiesto. Cada encargo tiene salidas propias.

### Cierre

Devuelve primero producto, por qué importa y decisión que habilita; después PR y rutas, SHA base/final, comandos realmente ejecutados, pruebas/CI, reservas materiales y máximo tres decisiones pendientes precisas. Distinguir PREPARADO, EJECUTADO, SELLADO, INTEGRADO y ADOPTADO. Un PR no adopta una cifra; un nuevo CALC no crea una fuente independiente.

Incluir **CIERRE COMPARTIDO DIFERIDO** con únicamente las propagaciones necesarias después del trámite de Opus. No convertirlo en otro inventario general. Aproximadamente 20% máximo del esfuerzo en control, salvo riesgo material de datos. Dos intentos razonables, una alternativa directa y receta concreta por bloqueo; continuar piezas independientes. Terminar con producto usable y siguiente acción clara, sin refinamiento por inercia.

## Prompt de lanzamiento

> Ejecuta íntegramente GEN2-RELEVO-ENCUCI-F2-1 desde main vigente posterior a #835. Materializa F-2/F-1 únicamente para RES-0005, leyendo valor vigente, grano y evidencia sellada reales; conserva veredicto histórico y distingue resolución vigente. Entrega escritor, regresiones y vista regenerada. No cambies cifras, sellos, milpa ni F-3; si la comparación actual exige retiro, prepara el parche de cita para integración serial y declara ese residual. Autorizo pruebas, commits, push y PR; fusión conmigo. Cero microdatos y cascada compartida diferida.
