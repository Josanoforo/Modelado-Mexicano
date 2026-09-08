ENCARGO · GEN2-TRAMITE-TABLERO-1
Alinear el tablero del repo con Gen 2 · siete piezas de trámite
Redactado el 8/sep/2026 contra origin/main = d48014ed. Validado por dirección (Tablero 004) con cuatro ajustes, los cuatro incorporados abajo.

0 · Arranque
Ejecuta /acto. La skill corre el ARRANQUE completo, la verificación de compuerta y el 0-bis de A.3. No transcribo esos bloques aquí: viven versionados en .claude/commands/acto.md.
Compuerta: ninguna. El PR #631 ya fusionó, así que el orden de fusión que dirección pidió ya se cumplió.
Si al arrancar el terreno no coincide con lo que este encargo declara, PARA y repórtalo: encontrar que el terreno no es el que el encargo supone es entregable, no interrupción.

1 · Cabecera
campo	valor
SHA de redacción	d48014ed (8/sep 13:52 −06:00)
ENTORNO ASIGNADO	NUBE. No lanzar en caja. Este acto no toca microdato, ni data/raw, ni red a fuentes; lanzarlo en caja desperdicia la capacidad escasa
MODELO SUGERIDO	Sonnet. Receta congelada: un reemplazo de archivo, un reemplazo de script y cuatro correcciones de una o dos líneas. Quien lanza puede subir de modelo, nunca bajar
Candidatos	Máximos en main al redactar: ADR-410 · FP-357 · NC-0047. Candidatos ADR-411 · FP-358 · NC-0048. Derívalos con tools/cierre_acto.py; no los heredes de esta tabla
Ramas vivas al redactar	origin/acto/gen2-e5-calc-0001-0003 y origin/acto/gen2-e5-1-verificador-calc0003v2, ambas de caja. Perímetro disjunto del tuyo

2 · ⚠️ Adjuntos — léelo antes de tocar nada
Este encargo necesita dos archivos que no están en el repo y que deben venir adjuntos a esta sesión:
TABLERO-PROGRAMA.md — el cuerpo curado nuevo (pieza A1)
tablero_vista.py — el generador de la vista, 555 líneas (pieza A2)
si falta	qué haces
TABLERO-PROGRAMA.md	PARO sobre A1 y solo A1. No inventes el cuerpo, no reconstruyas los snapshots intermedios, no uses el -v1_1 como si fuera el nuevo. Fila en ## NO-CORRIDO, razón PARO-PREMISA, sucesor SIN-ASIGNAR. A2 a A7 corren igual
tablero_vista.py	PARO sobre A2 y solo A2. No reescribas el generador desde cero para «salvar» la pieza: eso es inventar el adjunto por otra vía. Fila en ## NO-CORRIDO, razón PARO-PREMISA. A1, A3, A4, A6 y A7 corren igual
Precedente: MAESTRA38-TRAMITE-3 y MAESTRA38-TRAMITE-4 pararon por esta misma causa y las dos veces hicieron lo correcto al no inventar. Que pare una tercera es aceptable; que se invente el contenido, no.

3 · Verificación de existencia (A.8) — contestada por quien escribe
(1) Estructura. grep -c "forense/tablero" data/INFRAESTRUCTURA-v1_0.md → 0. El índice no cubre este dominio. Por A.8 ese hueco es entregable y lo cierra la pieza A7; el encargo no se detiene porque el hueco es del índice, no del trabajo.
(2) Contenido. Prueba por SHA, la única concluyente:
$ for s in 9cbd8d8 9af8407 2a2af31 a5350e5 1b469b7 baca702d 03bcd6f6 fbce146d e36c66dc d48014ed; do
      echo "$s -> $(grep -rl "$s" forense/tablero/ | wc -l) de 3"; done
  9cbd8d8  -> 2 de 3      <- control positivo: es el cuerpo v1.1 que SÍ está (9 menciones)
  todos los demás -> 0 de 3
Vocabulario A.4: NO-ENCONTRADO. El cuerpo curado del tablero canónico sigue siendo v1.1, snapshot 9cbd8d8, del 2/sep.
Aviso de método, porque casi nos engaña a los dos lados: un grep -rlE "Gen 2|v2_1|Snapshot v1\.7" da positivo en los tres archivos y es falso — v2_1 casa como subcadena con v2_13. La prueba buena es por SHA.
(3) Cobertura retroactiva. forense/tablero/ nace el 7/sep (PR #489 lo crea, PR #571 lo consolida). El trabajo del tablero anterior a esa fecha vivió fuera del repo y su ausencia no prueba que no existiera.

4 · Piezas
A1 · Reemplazar el cuerpo curado del tablero canónico
Sustituye el contenido de forense/tablero/TABLERO-PROGRAMA.md por el adjunto, íntegro.
Verificación de cierre — usa el patrón de línea completa, no la subcadena:
grep -cx '<!-- TABLERO-DERIVADO:BEGIN -->' forense/tablero/TABLERO-PROGRAMA.md    # esperado 1
grep -cx '<!-- TABLERO-DERIVADO:END -->'   forense/tablero/TABLERO-PROGRAMA.md    # esperado 1
python3 tools/tablero_programa.py --actualiza                                     # sin error
Por qué el patrón exacto y no grep -c: el cuerpo nuevo menciona el marcador en prosa dentro de una tabla, así que la subcadena puede dar 2 sin que haya dos marcadores. tablero_programa.py:66-67 casa por constantes exactas y rebana entre las primeras apariciones, así que una mención en prosa después del END es inocua. (En el adjunto de este encargo la mención ya se reescribió y los dos patrones dan 1; el check exacto queda igual, para que no dependa de eso.)

A2 · Reemplazar el generador de la vista
Sustituye tools/tablero_vista.py por el adjunto (555 líneas contra 201 del repo).
Diferencias que lo motivan: localiza secciones por título y no por número; tolera tablas que cambian de forma; suprime secciones vacías en vez de dibujarlas; y en modo Gen 2 el héroe es la cadena de procedencia — una casilla por resultado activo — en vez de las 49 reglas del motor.
Dependencia verificada: markdown ya está en requirements.txt (2 menciones). No la añadas otra vez.

A3 · Retirar dominios_activos
tools/tablero_programa.py:224 fija la constante 4 con la nota «Ola 6 NO abierta» incrustada en el texto del comando. Hoy acierta por coincidencia: si la Ola 6 abriera, el tablero seguiría diciendo 4 · NO abierta sin avisar.
Retíralo del derivador. Es un indicador de capa legacy y Gen 2 no lo consume. Dirección avaló esta salida.

A4 · Normalizar el estado de la cola antes de contarlo
tools/tablero_programa.py:231 cuenta la columna 2 de data/cola-adquisicion-v1_0.tsv.
PROHIBIDO cortar por el primer espacio. Corta por ' REL-'.
Derivado hoy: 14 estados distintos, 7 con espacio interno, y solo 3 son el defecto.
CERRADA NO-BAJAR-PORQUE                                    (2)  legítimo
CERRADA NO-GASTAR                                          (2)  legítimo
DIFERIDO-A: spec GEN2 dinero.credito.scoring_alternativo   (1)  legítimo
NO-OBTENIDO-POR-ESTE-AGENTE(4 rutas)                       (2)  legítimo
SUPERADA-POR REL-2fa1c0ddb0bd7c2776e43ea8                  (1)  DEFECTO
SUPERADA-POR REL-fbda9054154ac31de9be4eff                  (1)  DEFECTO
SUPERADA-POR REL-ec408a0b6399f198bcdb5776                  (1)  DEFECTO
Los cuatro primeros son estados legítimos con espacio: déjalos en paz. Cortar por el primer espacio los rompería a todos.
Verificación de cierre: tras el cambio, SUPERADA-POR debe sumar 1 + 3 = 4 y los cuatro estados legítimos deben conservar su texto completo.

A5 · Contar tiers por entrada, no por línea
Archivo: milpa/tramite-ola5-propuesta-v0.yaml — el acumulador, que es lo que cuentan las recetas propuesta_tier_*. No es milpa/tramite.yaml.
Derivado hoy contra d48014ed:
$ grep -cE '^  - id: '  milpa/tramite-ola5-propuesta-v0.yaml     → 50   entradas
$ grep -cE '^\s+tier: ' milpa/tramite-ola5-propuesta-v0.yaml     → 51   líneas
$ indentaciones de 'tier:'                                        → {4: 50, 6: 1}
$ entrada con dos líneas 'tier:'  →  tramite.mordida.con_registro_encig2025
El derivador cuenta líneas y sobrecuenta 1. Cuenta por entrada: una sola tier: por bloque - id:, la de indentación 4.
Verificación de cierre: la suma de las cuatro recetas propuesta_tier_* debe dar 50, igual que el número de entradas.
Nota: una validación previa dio esta pieza por retirada tras medir milpa/tramite.yaml (el motor, 21 entradas). Es otro archivo. La pieza se ejecuta.

A6 · Anotar el archivo superado
forense/tablero/TABLERO-PROGRAMA-v1_1.md tiene el mismo cuerpo que el canónico tenía antes de A1. Añade una línea al inicio diciendo que su contenido ya vive en TABLERO-PROGRAMA.md y que este archivo es historia. No lo borres — append-only.

A7 · Cerrar el hueco del índice
Añade a data/INFRAESTRUCTURA-v1_0.md la fila que gobierna forense/tablero/: qué archivo es el vigente, qué lo escribe — tools/tablero_programa.py --actualiza para el bloque derivado, la conversación del tablero para la capa curada — y que los -superado son historia. Es el entregable de A.8(1).

5 · Perímetro y concurrencia
Archivos que este acto toca: forense/tablero/TABLERO-PROGRAMA.md · forense/tablero/TABLERO-PROGRAMA-v1_1.md · tools/tablero_vista.py · tools/tablero_programa.py · data/INFRAESTRUCTURA-v1_0.md · más la cascada de cierre (canon/gobernanza-v1_15.md, canon/registro-rotulos.tsv, forense/no-corrido.tsv, forense/hallazgos.md).
Actos en paralelo: dos ramas de caja, gen2-e5-calc-0001-0003 y gen2-e5-1-verificador-calc0003v2, con perímetro data/corrida0/CALC-* y los tres TSV del registro. Disjunto, salvo la cascada compartida, que se renumera al fusionar.
Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.

6 · Contador
Este acto no mueve ningún contador de la señal de Gen 2, y se declara. N_resultados_sellados seguirá en 0 de 205 al cerrar. Es instrumentación: hace que el tablero describa Gen 2 en vez de describir el 2 de septiembre.

7 · Lo que este encargo NO hace
No traza el origen de ningún dato de Gen 1. Firma de mesa del 8/sep: «no haremos una revisión para trazar el origen de los datos de Gen1, empezamos de 0». Los valores legacy quedan íntegros y sin auditar.
No toca milpa/**, data/corrida0/**, ni ninguna corrida sellada. Incluye el hallazgo de milpa/tramite.yaml (21 entradas, 24 líneas tier:), que queda como sucesor fuera de perímetro.
No corre ninguna medición. Sin corpus en nube no sería ejecutable de todos modos.
No cambia el vocabulario del bloque derivado: ya lee corrida0 status y está bien hecho.
No cierra los bloqueadores G1 (el GO de E.5 no derivable) ni G2 (vigencia y delta sin implementar).

8 · Cierre
Cascada completa por tools/cierre_acto.py: ADR re-derivado, cabecera de gobernanza, registro-rotulos, tests/check.py --baseline en VERDE o PARO-reporta.
Sección ## NO-CORRIDO / RESERVAS obligatoria, inmediatamente antes de ## CONSUMIDO, con una fila por cada pieza no ejecutada, ejecutada a medias, hecha distinto o con reserva — y Ninguno. si no hay, que es respuesta obligatoria y no omisión. Cada fila con qué, por qué (vocabulario de A.14), impacto y sucesor. Las mismas filas van al cuerpo del PR y como NC- en forense/no-corrido.tsv con estado ABIERTA.
Filas esperables, si aplican: A1 o A2 por adjunto faltante (PARO-PREMISA); A5 si decides no hacerla (FUERA-DE-PERÍMETRO, con sucesor nombrado).
Política de cero ramas (A.14): el acto termina con su rama fusionada o borrada.

9 · Sucesores nombrados
corrida0.py go — reportar los seis checks de E.5 juntos, para que «podemos lanzar» sea derivación y no juicio (bloqueador G1).
corrida0.py vigencia y delta — hoy [NO-IMPLEMENTADO] (B-6/B-7). Sin delta no hay comparación por script contra GEN1, que E.1 exige (bloqueador G2).
milpa/tramite.yaml: 21 entradas y 24 líneas tier: — el mismo defecto de conteo de A5, en el motor. Fuera de perímetro aquí.

## NO-CORRIDO / RESERVAS

**Ninguno.** Los dos adjuntos (`TABLERO-PROGRAMA.md` nuevo, `tools/tablero_vista.py` nuevo) llegaron pegados a la sesión después del 0-bis A.3 y antes de tocar cualquier pieza sustantiva — ningún PARO-PREMISA sobre A1/A2. Las siete piezas (A1-A7) corrieron íntegras, con su verificación de cierre declarada en el encargo cumplida en cada caso: A1 (marcadores `grep -cx` → 1/1, `--actualiza` sin error), A2 (555 líneas, dependencia `markdown` ya declarada, corrida de extremo a extremo produjo HTML válido), A3 (constante retirada), A4 (`SUPERADA-POR` = 1+3 = 4, los cuatro estados legítimos con espacio íntegros), A5 (ejecutada pese a la nota de una validación previa que la daba por retirada — es otro archivo, el encargo lo aclara explícitamente; suma de las cuatro recetas = 50 = entradas), A6 (anotación append-only), A7 (hueco del índice cerrado). Nota de mecanismo, fuera del vocabulario de A.14 porque no es una pieza del encargo sino del ARRANQUE: este acto corrió sobre la rama que el arnés de ejecución ya tenía asignada (`claude/happy-davinci-i61zay`, coincide con `origin/main = d48014ed` al arrancar) en vez de crear una rama nueva con el rótulo del encargo (`acto/gen2-tramite-tablero-1`), por restricción externa del entorno ("nunca push a una rama distinta de la asignada sin permiso explícito") — `tools/cierre_acto.py` lo reporta como rótulo best-effort `HAPPY-DAVINCI-I61ZAY` ausente de `registro-rotulos.tsv`; el rótulo real del acto (`GEN2-TRAMITE-TABLERO-1`) sí quedó censado, a mano, en la fila que este mismo commit añade.
