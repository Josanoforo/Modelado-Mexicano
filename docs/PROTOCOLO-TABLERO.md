---
title: Protocolo del tablero
---

# Protocolo del tablero

ACTO GEN2-TUBERIA-TABLERO-EN-CANAL-1 (24/sep/2026): el tablero del
programa deja de tener dos productores. El único que escribe el bloque
`<!-- TABLERO-DERIVADO:BEGIN … END -->` es el job `guardias` de CI
(`.github/workflows/verify.yml`), corriendo `tools/tablero_programa.py
--actualiza` sobre `origin/main`, en el mismo commit `[deriva]` que abre su
PR automático. `/tramite` T0 puede seguir intentando el mismo comando,
pero corre **sin** `--permitir-rama`: si su rama administrativa no
coincide con `origin/main` (el caso normal, con la huella del ciclo ya
commiteada), el comando se niega con código != 0 y eso es lo esperado —
no escribe nada y no bloquea el ciclo de trámite.

**Para una conversación que interpreta el tablero:** léelo de
[`forense/tablero/TABLERO-PROGRAMA.md`](https://raw.githubusercontent.com/Josanoforo/Modelado-Mexicano/main/forense/tablero/TABLERO-PROGRAMA.md)
en `main`, o de [esta página en Pages]({{ '/tablero.html' | relative_url }})
una vez activada (FP-260923-GEN2-FRONT-1-4296-01). Cítalo e interprétalo;
**nunca lo regeneres ni subas una versión nueva** — eso es trabajo del job
de CI, no de una sesión de chat. Un bloque cuya línea de Procedencia dice
`¿árbol == origin/main? False` es inválido: viene de una corrida con
`--permitir-rama` (rotulada `NO-ES-ORIGIN-MAIN`) o de un productor viejo, y
se ignora — no se cita como estado vigente del programa.

**Para mesa:** lo mismo aplica a cualquier archivo que alguien te entregue
a mano con este bloque adentro. El estado vigente es el que está en
`origin/main` ahora mismo, con `¿árbol == origin/main? True`; cualquier
otra copia es, a lo sumo, una fotografía de un momento pasado o de una
rama que nunca se fusionó.

**Un solo tablero** (ACTO GEN2-TUBERIA-TABLERO-UNICO-1, 29/sep/2026; firma de mesa 5-bis (b)). El programa tiene un
solo tablero, `forense/tablero/TABLERO-PROGRAMA.md`, y una sola página, `docs/tablero.md`. CI reescribe únicamente lo
que está entre tres pares de marcadores: `TABLERO-DERIVADO` (estado vivo), `TABLERO-UNICO:CARRILES` (los 31 carriles,
de `tools/tablero_carriles.py`) y `TABLERO-UNICO:PENDIENTES` (firmas abiertas y deuda por dueño, de
`tools/tablero_unico.py`). Todo lo que queda fuera de los marcadores es el cuerpo curado del puesto de tablero: entra al
repo por `/tramite` como adjunto, nunca por CI ni por una conversación. `TABLERO-CARRILES.md`, su página HTML y el
inventario `PENDIENTES-PROGRAMA` dejaron de publicarse; las versiones del catálogo, las reglas y las familias que leen
los carriles se resuelven del puntero `docs/data/catalogo-vigente.json` o de la serie más alta del árbol.
