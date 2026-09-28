# Nota principal · ACTO GEN2-RECIBO-ASTRA6-2 · recibo post-merge de trece PR de Codex

Recibo POST-MERGE: los trece PR se fusionaron sin recibo de Claude (R(a) de FIRMAS-15 / FIRMAS-20 D); este recibo llega después del merge.

- Encargo: `forense/encargos/2026-09-27-GEN2-RECIBO-ASTRA6-2.md` (0-bis `627e8a46`, sello de cuerpo `5d6aa419…`). SHA de redacción `5f708a47`; base al abrir `9536e5e2` (main avanzó con #1213 y #1217, trámite; no es PARO). Entorno NUBE, cero microdato.
- ADR: `ADR-260927-GEN2-RECIBO-ASTRA6-2-627e-01`. Modo AUTÓNOMO-AMPLIO. Lotes D-11, uno por subagente: C1-a (#1166, #1194, #1199, #1200) · C1-b (#1202, #1203, #1205) · C2+archivo (#1195, #1214) · C3 (#1171, #1180, #1196, #1197). Todo va en un solo PR de recibo, porque los lotes no se tocan entre sí (declarado).

## P1 · Veredictos (EJECUTADO: `grep -h '^VEREDICTO' pr-*.md | sort | uniq -c` → 4 RECIBIDO-POST-MERGE, 9 RECIBIDO-POST-MERGE-CON-NC)

| PR | carril | rutas sensibles | veredicto | NC |
|---|---|---|---|---|
| #1166 | C1 (y archivo de otros cinco encargos, recibidos por carril) | 0 | RECIBIDO-POST-MERGE | 0 |
| #1194 | C1 | 0 | RECIBIDO-POST-MERGE | 0 |
| #1199 | C1 | 0 | RECIBIDO-POST-MERGE-CON-NC | 04–06 |
| #1200 | C1 | 1 (tabla propia del lote, no `data/corrida0/decisiones.tsv`) | RECIBIDO-POST-MERGE | 0 |
| #1202 | C1 | 0 | RECIBIDO-POST-MERGE-CON-NC | 07–08 |
| #1203 | C1 | 0 | RECIBIDO-POST-MERGE-CON-NC | 09 |
| #1205 | C1 | 0 | RECIBIDO-POST-MERGE | 0 |
| #1195 | C2 | 0 | RECIBIDO-POST-MERGE-CON-NC | 01–02 |
| #1214 | archivo | 0 (solo cambia la tupla de T02; no cambia qué se verifica) | RECIBIDO-POST-MERGE-CON-NC | 03 |
| #1171 | C3 | 0 | RECIBIDO-POST-MERGE-CON-NC | 10–12 |
| #1180 | C3 | 0 | RECIBIDO-POST-MERGE-CON-NC | 13–14 |
| #1196 | C3 | 0 | RECIBIDO-POST-MERGE-CON-NC | 15 |
| #1197 | C3 | 0 | RECIBIDO-POST-MERGE-CON-NC | 16–17 |

**PROPONER-REVERTIR: 0.** Ningún PR escribió en sellos, catálogo, `decisiones.tsv`, `milpa/`, tabla de piso ni vistas, y ninguno borra líneas.

Los números NC son sufijos de `NC-260927-GEN2-RECIBO-ASTRA6-2-627e-NN`, en `forense/no-corrido.tsv`.

## Hallazgos que pesan
- **#1203, ventana (criterio C1 principal):** 859 = 767 + 92 se reproduce abriendo los tar. Los 5 sucesores traen la columna `ventana` sin vacíos, y las filas conservadas son idénticas por `llave`. En cambio, el paquete no transporta *solo* la ventana: añade `esquema.json` y semántica, y NF pasa de 590 a 471 filas (NC-09).
- **#1202:** se re-deriva 275 / 2 / 56 / 92 desde `lote2-tabla-estimadores.tsv`, con tolerancias preexistentes de cada spec.yaml. Hay dos reservas:
  - 130 COINCIDE dependen de un alias de columnas añadido después de revelar; con los dictámenes v1 serían 145 (NC-07).
  - Los 2 DISCREPA de ENIGH2020 remesas caen bajo la tolerancia 0.0 de la spec. Se asientan como **NO-PASA** en `data/corrida0/validaciones-independientes.tsv` (2 filas), lo que mueve `resultados_con_validacion_independiente`, declarado (NC-08 lleva a mesa la enmienda de tolerancia).
- **#1199:** es contraste no ciego y queda rotulado como REIMPLEMENTACIÓN-INDEPENDIENTE-NO-CIEGA (rama prevista del encargo §5).
- **#1195:** los oros ENSU/ENOE son cifras propias sin CALC (NC-01). Ninguna ola reservada: ENOE 2024T4 no es la más reciente, y ENSU 2025 ya está vista por los CALC de pisos y serie.

## P2 · Hoja para mesa
`forense/analisis/recibo-astra6-2/hoja-para-mesa-recibo-astra6-2.md`: 15 dictámenes, uno por id (6 TAL-CUAL · 8 CON-CAMBIO · 1 YA-CUBIERTA-POR). Hay dos correcciones a lo que el encargo daba por supuesto:
- **39de-01 no es YA-CUBIERTA-POR beee-02.** beee-02 solo cubre el trato en el catálogo; no cubre el denominador del sucesor, la regla 98/99 ni la autorización de sucesores. Por eso va CON-CAMBIO, con el texto de firma listo.
- **ee49-01/02 piden autorizar una sesión ciega nueva, no una apertura de reserva.** Las 12 entradas de ENDIREH 2021 y las 20 de 2016 no traen campo de reserva.

FIRMAS-21 asienta la hoja.

**157c-04:** su producto (el recibo de #1194) queda entregado en `pr-1194.md`. El cambio de estado de la fila en `firmas-pendientes.tsv` **no se escribió en esta sesión**: el clasificador de permisos denegó la edición en sitio. Queda para FIRMAS-21 o para mesa: marcarla `CERRADA-RECIBO` citando este ADR.

## P3 · Advertencia hacia adelante
`p3-advertencia-tanda4.md`: el lote 2 repitió el defecto de ventana. Los 11 paquetes lanzados no traen la columna `ventana` (11/11). Tanda 4 debe lanzar desde `-ventana-v1` y congelar los alias antes de revelar. El encargo 02 de tanda 4 (CAJA) es el que hay que vigilar en RECIBO-ASTRA6-3.

## Módulo de auditoría
No aplica: el acto no afirma nada sobre México. Contadores movidos: cero mediciones y cero adopciones; `resultados_con_validacion_independiente` suma 2 filas NO-PASA.
