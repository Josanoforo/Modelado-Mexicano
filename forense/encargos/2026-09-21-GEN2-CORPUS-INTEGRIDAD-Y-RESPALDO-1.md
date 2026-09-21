# ENCARGO · ACTO GEN2-CORPUS-INTEGRIDAD-Y-RESPALDO-1 · SE SABE, ARCHIVO POR ARCHIVO, QUÉ DEL CORPUS ESTÁ FÍSICAMENTE EN LA CAJA Y COINCIDE CON SU HASH — Y EL CORPUS DEJA DE VIVIR EN UNA SOLA MÁQUINA

> ENTORNO: **CAJA** (es el único lugar donde el corpus existe). Si el hook no dice CAJA, PARA en una línea. NO es NUBE.

CABECERA · SHA de redacción `fc13cdcc`; re-deriva al abrir · una sola sesión, rama `acto/gen2-corpus-integridad-y-respaldo-1` · MODELO: Sonnet (receta; se puede subir) · MODO: **ABIERTO** · CONTADOR: ninguno · FP/ADR/NC: raíz de acto.
**Si al fusionar `main` choca la línea L0 de `canon/estado-programa-v1_14.md`: NO conserves los dos lados; toma la de `main` y re-inserta solo tu anotación.** Si `canon/L0/` ya existe al cerrar, tu anotación va ahí.
**NO CHOCAR CON TUBERÍA (acto en vuelo):** no edites `.github/workflows/verify.yml`, `tests/check.py`, `.gitattributes`, `.claude/commands/*.md`, `tools/cierre_acto.py`, `tools/tablero_programa.py`, `tools/estado_comun.py` ni `tools/digesto_tramite.py`. Tu test nuevo **no** se cablea a mano: el job de guardias lo ejecuta como huérfano (`tools/ci_guardias.py --ejecuta-huerfanos`) `[EJECUTADO por dirección: 56 ejecutados]`. Si tu cierre exige tocar uno de esos archivos, déjalo en NC con sucesor y dilo.

## 1 · OBJETIVO
Todo lo que el programa ha sellado depende de payloads que viven en un solo disco: 18.4 GB declarados en el manifiesto `[EJECUTADO]`. Si ese disco falla, ningún sello se puede volver a verificar y varias fuentes ya no se consiguen igual (INEGI reorganiza, otras requieren licencia). Hoy hay ocho sesiones abriendo ese corpus y dos payloads grandes por entrar. Y hay un hueco previo: de 1 632 entradas del manifiesto, **1 016 no declaran raíz** `[EJECUTADO]`, así que de la mayoría no se sabe, por comando, si el archivo está en la caja.
«Hecho» significa: censo de integridad, entrada por entrada, con los estados de A.1 sin colapsar · lo ausente que se pueda traer por id, traído · un juego de respaldo verificable en el destino que mesa indique, con prueba de restauración · una nota: cuánto del corpus está, cuánto no, y qué no se puede volver a conseguir.

## 2 · FIRMAS DE MESA — verbatim
Mandato (21/sep): «Todo lo que sea descargas se baja, tenemos una infraestructura COMPLETA diseñada por CODEX y una ruta de manejo de descargas completa […] Capacidad de descarga tenemos casi 100gb libres.» Reservas vivas: ENVIPE 2026 («Bajar el payload está permitido; abrirlo, derivar de él o leer sus tabulados, no»), ENIGH 2024 (si su reserva ya está asentada, igual; si no, trátala igual).
**Bifurcación que SÍ se pregunta a mesa, al empezar, y sigues con P1 mientras contesta:** ¿a dónde va el respaldo? Opciones: (i) disco externo que mesa conecte — recomendada: barata, inmediata, fuera de la máquina; (ii) almacenamiento en nube de mesa, cifrado — mejor contra robo o incendio, exige credenciales que solo mesa tiene; (iii) las dos. Si mesa no contesta antes de P3: deja el juego armado y verificado en un directorio de la caja, **y dilo así: eso todavía no es un respaldo.**

## 3 · LO QUE DIRECCIÓN SABE (contra `fc13cdcc`, sin corpus)
- `[EJECUTADO sobre data/manifiesto.yaml]` 1 632 entradas; por raíz: sin raíz 1 016 · `descargas_mx` 335 · `data_raw` 277 · `reserva_respondentes` 4; 18.4 GB declarados.
- `[LEÍDO: tests/manifiesto.py:20-27,682-687]` la verificación tabula por raíz sin colapsar: `AUSENTE` · raíz no configurada · `COINCIDE` / `NO_COINCIDE`. `[LEÍDO: nota de cierre del piloto 3]` en la caja: «corpus montado 420 archivos». **420 contra 1 632: la diferencia es lo que este acto explica.**
- `[LEÍDO: data/INFRAESTRUCTURA-v1_0.md, Dominio 1]` adquisición: `/adquiere` camina la cola; `python3 tests/manifiesto.py --descarga --id <id>` baja por id y verifica sha. El launcher del agente usa un candado: **no corras descargas a la vez que el agente; si el candado está tomado, espera o sáltate P2 y dilo.**
- `[LEÍDO: nota de #960]` dos PDF (`enif_2012_cuestionario_pdf`, `enif_2015_cuestionario_pdf`) se registraron desde nube y aún no están físicamente en la caja.

## 4 · YA HECHO
Por objeto («respaldo», «backup», «integridad», «censo de corpus») en encargos, notas y ramas: hay censos parciales de raíz (uno en la nota del piloto de nube: 1 013 sin raíz) y ningún respaldo. **Repítela tú.**

## 5 · PIEZAS
**P1 · Censo.** Por entrada: estado de A.1, raíz, tamaño real contra declarado. Salida cruda pegada; conteo de archivos examinados (A.13). Para las entradas sin raíz: ¿el archivo está en alguna raíz configurada bajo su nombre? Clasifica: `ESTÁ-Y-COINCIDE` · `ESTÁ-Y-NO-COINCIDE` · `NO-ESTÁ` · `NO-ES-ARCHIVO` (entradas que son referencia, licencia o nota). No edites el manifiesto para que cuadre: propón el cambio en una tabla.
**P2 · Traer lo que falta y se puede.** Por id, con verificación de sha, lo `NO-ESTÁ` que tenga `url_origen`; empieza por lo que usan los actos en vuelo (ENIF, ENVIPE, ENCIG, ENUT, ENIGH, ENSAFI, ENFIH). Lo que no baje: «NO OBTENIDO POR ESTE AGENTE EN N INTENTOS» + receta de un minuto (A.5). **Los payloads reservados se bajan y se hashean; no se abren ni se listan.**
**P3 · Respaldo.** Juego con índice (ruta, tamaño, sha256) generado **desde los archivos**, no desde el manifiesto; copia al destino de mesa; verificación por hash en destino; **prueba de restauración** de una muestra (al menos un payload por encuesta) a un directorio temporal, con su hash. Instrucción de una página para repetirlo (cada cuándo, qué comando).
**P4 · Lo irrecuperable.** Lista de payloads que no tienen `url_origen` viva o que requirieron licencia o gestión manual: son los que más duele perder y los primeros que se respaldan.

## 6 · LATITUD
Decides tú: herramienta de copia, formato del juego, orden. Obstáculo reversible y barato se resuelve y se declara.

## 7 · PAROS — lista cerrada
a) abrir, listar o descomprimir un payload reservado · b) borrar, mover o renombrar cualquier archivo del corpus · c) editar `data/manifiesto.yaml` fuera de registrar lo que P2 baje por la vía de la casa · d) subir el corpus a un destino que mesa no nombró · e) entorno equivocado.

## 8 · COMPUERTAS
«Mesa nombró el destino» protege: nada de las cuatro — es orden sugerido; sin destino, P3 queda a medias y se dice.

## 9 · PERÍMETRO
Propio: `forense/analisis/corpus-integridad-1/` (censo, tabla de propuestas, índice del juego, instrucción) · entradas de manifiesto de lo que P2 baje · nota · cascada · fuera del repo: el directorio de respaldo. Ajeno: todo código · la cola de adquisición · la lista de TUBERÍA. Si te encuentras escribiendo fuera de esta lista, PARA.

## 10 · NO HACE · SUCESORES · CIERRE
No reorganiza raíces · no corrige el manifiesto · no automatiza el respaldo (D-14: primero se ve si se repite a mano). Sucesor: decisión de mesa sobre la tabla de propuestas de raíz. Auditoría §5: no aplica. Falsador a tres meses: si nadie repitió el respaldo, la instrucción no sirve y se anota. `## NO-CORRIDO / RESERVAS` · `## CONSUMIDO`.
