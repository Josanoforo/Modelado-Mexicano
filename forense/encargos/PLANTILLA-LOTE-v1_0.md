PLANTILLA-LOTE · v1.0

Esqueleto D-12 (`instrucciones-proyecto-v2_12.md`, Bloque D-quater). Formato
corto de encargo: sellada la skill `/acto` (D-10), el encargo trae solo lo
sustantivo — el ARRANQUE, la compuerta y el cierre en cascada ya no se
transcriben aquí, los ejecuta la skill. Objetivo medible: tamaño mediano
≤40% del formato largo anterior. Copia este archivo, llena cada sección y
borra la línea de guía; una sección vacía sin su guía borrada es un
encargo a medio escribir, no uno corto.

---

ENCARGO · ACTO <PROGRAMA>-<Nn> · <NOMBRE>
<!-- Cabecera: SHA de redacción · fecha y quién redacta · instrucciones
     vigentes contra las que se redactó · Estado (LISTO PARA LANZAR / GATED
     a X) · si este es el último encargo en su forma, dilo. -->

ENTORNO ASIGNADO: <NUBE (`cloud_default`) | UBUNTU> — y decir explícitamente
en qué entorno NO se lanza. MODELO SUGERIDO: <Sonnet | Opus | Fable> (D-13:
Sonnet para recetas congeladas sin juicio; Opus para medidores de dos
commits y lotes; Fable para dirección/diseño/auditoría).
<!-- Una línea. Las dos veces que faltó, el encargo salió duplicado. -->

CARRILES: <qué corre en paralelo, y qué no, hasta el merge de este acto>.
<!-- Una línea. -->

FIRMAS DE MESA — verbatim, <fecha>. El ejecutor propaga, no decide (SELLA-3)
<!-- Cada firma citada exactamente como mesa la dio, con su fecha. Sin
     firma, no hay decisión que propagar — el ejecutor no la inventa. -->

═══ VERIFICACIÓN DE EXISTENCIA (A.8) — contestada por quien escribe ═══
<!-- (1) ESTRUCTURA: qué tablas gobiernan este dominio (data/INFRAESTRUCTURA-v1_0.md,
     no de memoria) y cuáles toca este encargo. (2) CONTENIDO: comando +
     salida cruda que demuestra que lo que se manda producir no existe ya,
     vocabulario A.4 (EXISTE-SATISFACE / EXISTE-NO-SATISFACE / NO-ENCONTRADO
     / NO-ACCESIBLE). (3) COBERTURA RETROACTIVA: fecha de nacimiento de cada
     tabla gobernante contra la fecha del trabajo que se va a tocar. -->

SPEC CONGELABLE POR PIEZA
<!-- Hasta cuatro piezas afines del mismo entorno = un encargo, un PR, un
     ADR, un recibo de tablero (D-11). Por pieza: variables, universo,
     ponderadores, ejes, dicotomizaciones — lo que el COMMIT-1 de esa pieza
     congela antes de abrir ningún dato, cerrando con "el primer resultado
     que produzca este procedimiento es el que se reporta". Una pieza que
     PARA no tumba el lote, salvo PARO de entorno (A.2). -->

PERÍMETRO Y CONCURRENCIA
<!-- Qué archivos toca, qué actos corren en paralelo y sus archivos, con la
     frase exacta: "Si te encuentras escribiendo fuera de esta lista, PARA
     — el perímetro estaba mal calculado y saberlo vale más que el atajo." -->

FP/ADR CANDIDATOS
<!-- Deriva, no heredes: máximo FP hoy (`forense/firmas-pendientes.tsv`) y
     rango pre-asignado para este lote; candidato de ADR por el comando de
     la casa contra `canon/gobernanza-v1_15.md`. Nunca el número que "hoy
     daría" de memoria o de un acto anterior. -->

CONTADOR
<!-- Qué contador mueve este acto y cuánto, o "cero directo, declarado" si
     no mide — nunca ausente sin decirlo (regla de señal, v2.3). -->

Lo que este acto NO hace
<!-- Declarado, no implícito: qué queda fuera del perímetro a propósito. -->

Sucesores declarados, no lanzados
<!-- Qué actos habilita este, sin lanzarlos aquí. -->
