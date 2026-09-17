# Nota de cierre — ACTO GEN2-REGISTRO-CAJA-1

Redactada contra `67fa97e` (merge de #850, base del encargo). CAJA (Ubuntu,
corpus montado, `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable`,
`acceso_corpus.montado=SI`, `archivos_examinados=419`). COMPUERTA: ninguna.

## P1 — verificación por CALC, una invocación aislada cada una

Catorce `python3 tools/corrida0.py verify <CALC>` en procesos separados
(nunca `registro --verifica` en lote — ver la razón en P2). Los dos
veredictos no triviales se corrieron dos veces cada uno, aislados, antes de
declararlos estables (feedback establecido tras `GEN2-B-MARCO`/`NC-0182`:
`registro --verifica` puede dar un veredicto inestable dentro del mismo
proceso; `verify` invocado como proceso propio por CALC no comparte ese
riesgo, y aun así se dobló donde el resultado no era REPRODUCE limpio).

| CALC | RESULTADO | CONTEXTO | cuenta_gen2 (derivado por `registro`, PENDIENTE-DE-MESA salvo decisión) |
|---|---|---|---|
| CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0001 | REPRODUCE | IDENTICO | PENDIENTE-DE-MESA |
| CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001 | **NO-REPRODUCE** (causa abajo) | IDENTICO | PENDIENTE-DE-MESA |
| CALC-ENCIG2023-AGREGADO-CONDICIONAL-0001 | REPRODUCE | IDENTICO | PENDIENTE-DE-MESA |
| CALC-ENCIG2023-FLUJO-0001 | REPRODUCE | IDENTICO | PENDIENTE-DE-MESA |
| CALC-ENCRIGE-CARGA-INTENSIDAD-0001 | REPRODUCE | IDENTICO | PENDIENTE-DE-MESA |
| CALC-ENCRIGE-CORRUPCION-DESCRIPTIVA-0001 | REPRODUCE (ver nota sandbox) | IDENTICO | PENDIENTE-DE-MESA |
| CALC-ENIGH2022-INTENSIDAD-REMESAS-0001 | REPRODUCE | IDENTICO | PENDIENTE-DE-MESA |
| CALC-ENVIPE-RES0028-U4-DERIVADO-0001 | REPRODUCE | IDENTICO | PENDIENTE-DE-MESA |
| CALC-ENVIPE-U4-2013-0001 | REPRODUCE | IDENTICO | PENDIENTE-DE-MESA |
| CALC-ENVIPE-U4-2015-0001 | REPRODUCE | IDENTICO | PENDIENTE-DE-MESA |
| CALC-WBES2023-CORRUPCION-DESCRIPTIVA-0001 | REPRODUCE | IDENTICO | PENDIENTE-DE-MESA |
| CALC-WBES2023-PRECISION-0001 | REPRODUCE | IDENTICO | PENDIENTE-DE-MESA |
| CALC-AGG-marco-M-sorteado-v1_3-ola-v3 | REPRODUCE | IDENTICO | PENDIENTE-DE-MESA |
| CALC-C0D-ALCANCE-CORPUS-CAPTURA-SUCESOR | REPRODUCE | IDENTICO | PENDIENTE-DE-MESA |

13/14 REPRODUCE limpio con CONTEXTO IDENTICO. Ninguno cae en NO-EJECUTABLE
sobre corpus real. La salida cruda completa de las catorce corridas
(1600 líneas) vive en el log de esta sesión; no se transcribe aquí por
extensión — el veredicto de esta tabla es re-derivable en un comando por
fila con `python3 tools/corrida0.py verify <CALC>`.

**Corrección sobre la premisa del encargo (A.8, verificado contra el
árbol):** el CALC que el encargo llama `CALC-ARBITRO-CRUCE-0001` (piloto,
#849) no existe con ese nombre — el directorio real es
`CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0001` (el encargo usaba una
elipsis que comprime el prefijo compartido con la entrada anterior). Censo
independiente de los 118 `CALC-*/` contra el campo `spec_id` (columna 3) de
`corridas.tsv` — no contra `corrida_id` (columna 1, que lleva sufijo de
hash) — reproduce exactamente los 14 ids que el encargo nombra, ni uno más
ni uno menos.

**Sandbox falso negativo, corregido (A.13).**
`CALC-ENCRIGE-CORRUPCION-DESCRIPTIVA-0001` dio primero
`NO-EJECUTABLE -- FileNotFoundError` sobre
`/mnt/c/Users/PC0/Descargas MX/UNIVERSO-2026-09/ENCRIGE/conjunto_de_datos_encrige_2020_csv.zip`.
Es el defecto ya documentado (`/mnt` está en la lista de denegación de
lectura del sandbox de esta sesión, sin importar si el archivo existe):
confirmado con `dangerouslyDisableSandbox: true` que el archivo SÍ existe
(1 630 532 B, 3/sep/2026) en esa ruta exacta. Re-corrido `verify` fuera del
sandbox (dos veces, aislado): `REPRODUCE`, `CONTEXTO=IDENTICO`, 15/15
RESULT con delta 0. No es un defecto del CALC ni de su spec.

**Causa del único NO-REPRODUCE, ya acreditada por `NC-0313` (no se
re-deriva, se cita).** `RESULT-DIN-LXE8-G-R-EXISTE-AL-CERRAR`: sellado=`NO`,
hoy=`SI`. `CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001` selló a las
`2026-09-17T03:25:55Z`; `CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0001`
("R") selló 4m10s después, a las `03:30:05Z`. El RESULT es un snapshot del
estado del árbol al momento del sello (si R ya existía), no una función de
los inputs sellados — no puede volver a reproducir una vez que R existe,
por diseño del medidor, y `NC-0313` ya lo declaró `PARO-PREMISA` de diseño,
no una rotura. Confirmado aquí de forma independiente (misma causa,
mismos timestamps) antes de leer `NC-0313`: converge.

## P2 — registro: PARA, con causa

`status` antes: `N_corridas_selladas=80` (igual al que el encargo declara).

`python3 tools/corrida0.py registro --escribe` (sin `--verifica`, por la
razón de abajo) termina:

```
PARO · REPLAY-PISADO (NC-0094): escribir borraria o cambiaria evidencia de
replay de 25 corrida(s) AJENA(s) al lote autorizado (50 campo(s)). No se
escribio ninguna vista.
    CALC-B-MARCO-ENCIG-0001--3be11ba6cd7e · contexto_replay: IDENTICO -> NO-VERIFICADO
    CALC-B-MARCO-ENCIG-0001--3be11ba6cd7e · resultado_replay: REPRODUCE -> NO-VERIFICADO
    [... 23 corridas más, mismo patrón ...]
  Si el cambio es intencional, nombra las corridas en `--lote …`
no se escribio ninguna vista
```

`git status --porcelain` tras el PARO: vacío. Confirmado que no se escribió
nada, ni siquiera parcialmente.

**Las 25 corridas del PARO no tienen relación con las 14 de este lote.**
Ninguna de las 14 aparece en la lista (son inserciones nuevas, no
transiciones — el guardia `NC-0094` sólo protege verdicos YA PUBLICADOS).
Las 25 son corridas ajenas (`CALC-EDER-*`, `CALC-B-MARCO-*`,
`CALC-ENVIPE-U4-2012`, etc.) cuyo `resultado_replay`/`contexto_replay`
publicado hoy es `REPRODUCE`/`IDENTICO`, pero que **no tienen asiento
vigente en `forense/replay-evidencia.tsv`** (confirmado: `grep -F
"CALC-EDER-0001" forense/replay-evidencia.tsv` → 0 filas). Sin
`--verifica` (que llamaría `verify()` fresco para las 118 CALC selladas,
no sólo las 14), `_proyecta_replay` no tiene de dónde sostener su valor
publicado y cae a `SIN-FUENTE → NO-VERIFICADO` — el guardia `NC-0094`
existe exactamente para impedir que esa caída se escriba en silencio.

**Se intentó `registro --verifica` (sin `--escribe`, sólo para medir el
alcance) fuera del sandbox: no terminó en 280s** y se abortó por
`timeout`. Sí re-verifica las 118 CALC selladas en un solo proceso — el
mismo mecanismo de inestabilidad in-process ya medido en `GEN2-B-MARCO`
(`NC-0182`: un veredicto puede voltear entre pasadas del mismo proceso
porque los medidores comparten `sys.modules`). Someter las ~104 corridas
ajenas a esa reverificación en bloque, sólo para poder escribir 14 filas
nuevas, es desproporcionado al perímetro de este encargo (catorce
corridas, cero mediciones nuevas, "no adopta nada") y no se intentó de
nuevo: `--force` no existe, y `--lote` nombrando 25 corridas que esta
sesión no verificó sería exactamente el `--force` de facto que el encargo
prohíbe ("no se fuerza").

**Conclusión de P2, per el propio contingente del encargo: PARA. No se
escribió ninguna vista. `corridas.tsv` sigue en 187 filas
(201 tras cabecera − 14 filas fantasma no escritas), `N_corridas_selladas`
sigue en 80.**

## P3 — el contador, explicado una vez

`N_corridas_selladas` (`status`, `tools/corrida0.py:4282`) se deriva
**del disco** — cuenta directorios `CALC-*/` con `sello.json` y
`estado=SELLADA`, `origen=OFERTA` — no de `corridas.tsv`. `corridas.tsv`
es la **vista publicada** (`# DERIVADO — NO EDITAR`), una proyección
separada que sólo se actualiza cuando alguien corre `registro --escribe`
con éxito.

Por eso el piloto (`#849`) pudo cerrar declarando "+2 corridas selladas"
sin que el contador se moviera: selló los CALC en disco (eso sí sube
`N_corridas_selladas`, automáticamente, al derivarse de disco) pero nunca
llegó a `registro --escribe` — y aunque hubiera llegado, este acto mide
que el intento habría PAROado por la misma razón que el de arriba.

**Regla para `hallazgos.md` (`PARA-v2.14`):** *toda corrida sellada entra
a la vista publicada (`corridas.tsv`) en el mismo acto que la sella, o el
CONTADOR del acto dice explícitamente "sellada en disco, no registrada" —
nunca se reporta un delta de `N_corridas_selladas` como si fuera un
delta de filas publicadas; son dos cifras distintas que se mueven en
momentos distintos.* Corolario medido aquí, más ancho que el original: el
instrumento de registro es todo-o-nada no sólo porque agrupe las
adiciones pendientes en una sola escritura (`NC-0286`), sino porque
**cualquier** `--escribe` — con o sin filas nuevas — recalcula el replay
de las 118 corridas selladas y aborta si alguna corrida YA PUBLICADA,
ajena al lote, perdería evidencia. Un acto puede tener sus 14 corridas
limpias y aun así no poder escribir una sola fila.

### NC-0284 / NC-0285 / NC-0286 / NC-0288

Ninguna se cierra — el registro no ocurrió. Lo que sí cambia:

- **NC-0284** (`CALC-ENCRIGE-CORRUPCION-DESCRIPTIVA-0001`): el diferido "a
  CAJA con corpus montado" está cumplido — `verify` en CAJA da REPRODUCE,
  CONTEXTO IDENTICO (una vez corregido el falso negativo de sandbox). El
  registro sigue bloqueado, ahora por la causa de `NC-0315` (abajo), no
  por falta de corpus.
- **NC-0285** (`CALC-ENCIG2023-AGREGADO-CONDICIONAL-0001`): mismo patrón —
  REPRODUCE en CAJA, registro bloqueado por `NC-0315`.
- **NC-0286** (`CALC-ENVIPE-RES0028-U4-DERIVADO-0001`): su propio
  diagnóstico ("todo-o-nada, no hay bandera de exclusión") se confirma y
  se amplía: no es sólo que las adiciones pendientes se agrupen — es que
  el guardia de reproyección de replay bloquea con o sin adiciones
  nuevas, contra corridas que no tienen nada que ver con el lote.
- **NC-0288** (contador "80→83"): reconfirmado con el lote más grande de
  este acto (14, no 3): `status` antes = 80, `status` después = 80 (no se
  escribió nada). El contador nunca fue el problema; la vista sigue sin
  reflejar 14 CALC sellados (antes eran 6 los nombrados por `NC-0288`: 3
  de su propia tanda + `AGG-marco-M-sorteado-v1_3-ola-v3`,
  `C0D-ALCANCE-CORPUS-CAPTURA-SUCESOR`, `WBES2023-CORRUPCION-DESCRIPTIVA`
  — los tres últimos están en este lote de 14 también).

Las cuatro quedan **ABIERTA**, sin editar su fila histórica (el análisis
que registraron en su momento sigue siendo válido; lo que cambia es que
CAJA cerró la incertidumbre de "¿verifica o no?" para las que la
señalaban, y lo que falta ahora es exclusivamente mecánico: el instrumento
necesita el sucesor de abajo). Se abre `NC-0315` con el diagnóstico
preciso y más amplio, para que la próxima sesión no repita la medición del
`timeout` de 280s.
