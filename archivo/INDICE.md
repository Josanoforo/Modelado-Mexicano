# Archivo histórico

Índice de redirección (ACTO GEN2-FRONT-3-PORTADA-1, 26/sep/2026). Firma de mesa
del 26/sep: «Los archivos históricos y normativos salen de la raíz con git mv;
una cita por nombre en texto sellado no se edita: la resuelve archivo/INDICE.md
y tools/resuelve_cita.py. La raíz queda con ≤ 12 archivos de primer nivel.»

Un texto sellado (`canon/`, `forense/notas`, ADR, encargos) que cite uno de
estos nombres —o un enlace relativo a la raíz— se lee con esta tabla:

    python3 tools/resuelve_cita.py <nombre>

La tabla se deriva por comando, no se teclea:
`python3 tools/resuelve_cita.py --genera 1734006a` y `--genera 40a1829a`
(`requirements-dev.txt`, sustituido por el grupo `dev` de `pyproject.toml`;
su `-r requirements.txt` interno ya no resuelve desde `archivo/`: usa `uv sync --group dev`). La guarda es
`tests/test_portada.py`. Lo normativo vigente vive en [gobierno/](../gobierno/).

FRONT-1 (23/sep) había aplazado este movimiento por las citas selladas; su
inventario sigue en la [nota de cierre](../forense/notas/2026-09-23-GEN2-FRONT-1-cierre.md).

| nombre citado | ruta actual | commit del movimiento |
|---|---|---|
| `instrucciones-proyecto-v2.md` | `archivo/instrucciones/instrucciones-proyecto-v2.md` | `1734006a` |
| `instrucciones-proyecto-v2_10.md` | `archivo/instrucciones/instrucciones-proyecto-v2_10.md` | `1734006a` |
| `instrucciones-proyecto-v2_11.md` | `archivo/instrucciones/instrucciones-proyecto-v2_11.md` | `1734006a` |
| `instrucciones-proyecto-v2_12.md` | `archivo/instrucciones/instrucciones-proyecto-v2_12.md` | `1734006a` |
| `instrucciones-proyecto-v2_13-DELTA-2026-09-08.md.sha256` | `archivo/instrucciones/instrucciones-proyecto-v2_13-DELTA-2026-09-08.md.sha256` | `1734006a` |
| `instrucciones-proyecto-v2_13-DELTA-2026-09-08.md` | `archivo/instrucciones/instrucciones-proyecto-v2_13-DELTA-2026-09-08.md` | `1734006a` |
| `instrucciones-proyecto-v2_13.md.sha256` | `archivo/instrucciones/instrucciones-proyecto-v2_13.md.sha256` | `1734006a` |
| `instrucciones-proyecto-v2_14-HISTORIA.md` | `archivo/instrucciones/instrucciones-proyecto-v2_14-HISTORIA.md` | `1734006a` |
| `instrucciones-proyecto-v2_15-HISTORIA.md.sha256` | `archivo/instrucciones/instrucciones-proyecto-v2_15-HISTORIA.md.sha256` | `1734006a` |
| `instrucciones-proyecto-v2_15-HISTORIA.md` | `archivo/instrucciones/instrucciones-proyecto-v2_15-HISTORIA.md` | `1734006a` |
| `instrucciones-proyecto-v2_15.md.sha256` | `archivo/instrucciones/instrucciones-proyecto-v2_15.md.sha256` | `1734006a` |
| `instrucciones-proyecto-v2_15.md` | `archivo/instrucciones/instrucciones-proyecto-v2_15.md` | `1734006a` |
| `instrucciones-proyecto-v2_16-HISTORIA.md.sha256` | `gobierno/instrucciones-proyecto-v2_16-HISTORIA.md.sha256` | `1734006a` |
| `instrucciones-proyecto-v2_16-HISTORIA.md` | `gobierno/instrucciones-proyecto-v2_16-HISTORIA.md` | `1734006a` |
| `instrucciones-proyecto-v2_16.md.sha256` | `gobierno/instrucciones-proyecto-v2_16.md.sha256` | `1734006a` |
| `instrucciones-proyecto-v2_16.md` | `gobierno/instrucciones-proyecto-v2_16.md` | `1734006a` |
| `instrucciones-proyecto-v2_4.md` | `archivo/instrucciones/instrucciones-proyecto-v2_4.md` | `1734006a` |
| `instrucciones-proyecto-v2_5.md` | `archivo/instrucciones/instrucciones-proyecto-v2_5.md` | `1734006a` |
| `instrucciones-proyecto-v2_6.md` | `archivo/instrucciones/instrucciones-proyecto-v2_6.md` | `1734006a` |
| `instrucciones-proyecto-v2_7.md` | `archivo/instrucciones/instrucciones-proyecto-v2_7.md` | `1734006a` |
| `instrucciones-proyecto-v2_8.md` | `archivo/instrucciones/instrucciones-proyecto-v2_8.md` | `1734006a` |
| `instrucciones-proyecto-v2_9.md` | `archivo/instrucciones/instrucciones-proyecto-v2_9.md` | `1734006a` |
| `PROPUESTA-cola-sondeo27-2026-08-14.md` | `archivo/propuestas/PROPUESTA-cola-sondeo27-2026-08-14.md` | `1734006a` |
| `propuesta-motor-adaptativo-celda-v0_1.md` | `archivo/propuestas/propuesta-motor-adaptativo-celda-v0_1.md` | `1734006a` |
| `propuesta-motor-adaptativo-celda-v0_2.md` | `archivo/propuestas/propuesta-motor-adaptativo-celda-v0_2.md` | `1734006a` |
| `propuesta-motor-adaptativo-celda-v0_3.md` | `archivo/propuestas/propuesta-motor-adaptativo-celda-v0_3.md` | `1734006a` |
| `propuesta-motor-adaptativo-celda-v0_4.md` | `archivo/propuestas/propuesta-motor-adaptativo-celda-v0_4.md` | `1734006a` |
| `propuesta-motor-adaptativo-celda-v0_5.md` | `archivo/propuestas/propuesta-motor-adaptativo-celda-v0_5.md` | `1734006a` |
| `propuesta-motor-adaptativo-celda-v0_6.md` | `archivo/propuestas/propuesta-motor-adaptativo-celda-v0_6.md` | `1734006a` |
| `propuesta-motor-como-contexto-2026-07-30.md` | `archivo/propuestas/propuesta-motor-como-contexto-2026-07-30.md` | `1734006a` |
| `propuesta-motor-matriz-v0_1.md` | `archivo/propuestas/propuesta-motor-matriz-v0_1.md` | `1734006a` |
| `PROPUESTA-reconciliacion-universo-puertas.md` | `archivo/propuestas/PROPUESTA-reconciliacion-universo-puertas.md` | `1734006a` |
| `PROPUESTA-remediacion-brecha-documental.md` | `archivo/propuestas/PROPUESTA-remediacion-brecha-documental.md` | `1734006a` |
| `revision-programa-2026-07-31.md` | `archivo/propuestas/revision-programa-2026-07-31.md` | `1734006a` |
| `revision-publicacion-2026-07-30.md` | `archivo/propuestas/revision-publicacion-2026-07-30.md` | `1734006a` |
| `requirements-dev.txt` | `archivo/requirements-dev.txt` | `40a1829a` |
