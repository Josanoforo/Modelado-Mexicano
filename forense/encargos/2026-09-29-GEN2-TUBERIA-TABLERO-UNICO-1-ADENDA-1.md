# ADENDA-1 · ENCARGO GEN2-TUBERIA-TABLERO-UNICO-1 · sustituye los tres adjuntos

**De:** dirección, con el material del puesto de tablero.
**Fecha:** 29/sep/2026.
**Para:** la sesión que archivó el encargo en su 0-bis. Es la rama `claude/new-session-dpju77`, commit `22eeeedc`; su sello de cuerpo es `7654e498…a160`.

Esta adenda no toca el cuerpo sellado del encargo. Se archiva como archivo propio y se sella al recibirse (A.3).

## Qué cambia

Los tres adjuntos del §3 del encargo se sustituyen por las versiones que viajan con esta adenda. Pasaron dos cosas:

- **El tablero del puesto se reorganizó** después de que se redactó el encargo.
- **Los carriles van ahora primero, antes del programa, y completos.**
  - Antes eran §11 y §12, al final del archivo, y §11 era solo un resumen.
  - Ahora son **§C Carriles**: el tablero de carriles entero, con «cómo leer», la tabla de los 31, lo que más frena, `SIN-UNION`, la simulación, la adquisición global, el frente 2027, **las 31 tarjetas** y la cadena de procedencia. Sale tal cual de `python3 tools/tablero_carriles.py`, con los niveles de encabezado bajados dos.
  - Le sigue **§P Pendientes**.
  - Los marcadores no cambian de nombre: `TABLERO-UNICO:CARRILES` y `TABLERO-UNICO:PENDIENTES`.

Lo que el encargo dice de §11 y §12 del adjunto se lee como §C y §P. P1 y la opción (b) de 5-bis se refieren a esta versión.

## Adjuntos que sustituyen a los recibidos

| archivo | sha256 |
|---|---|
| `TABLERO-PROGRAMA.md` (tablero único v2.24, corte `5c8b42d3`) | `9d976c05fda3266a9414a57e7d8c09c3b2d40355d38cbd12a0d98872faaab0e7` |
| `tablero_unico.py` (genera §C y §P; `carriles` ahora recibe también el markdown completo de la herramienta) | `991771c2eb6afc110845886c943c69b882f45d9fa9f8c530e2611953b9ce9935` |
| `tablero_vista.py` (la vista abre con carriles y pendientes; el pliegue técnico trae §C completa) | `f0865da914c6af3c6d76917c4d7b280d41e00bec038ef5cd6db48622f791a53e` |

El acto recalcula cada sha al recibirlos y lo asienta en el 0-bis. Si un sha no coincide, el adjunto no se usa y se pide de nuevo.

## Lo que no cambia

Objetivo, «hecho», piezas P1 a P5, opciones de 5-bis, latitud, paros, compuertas y perímetro. Todo sigue como está en el encargo archivado.
