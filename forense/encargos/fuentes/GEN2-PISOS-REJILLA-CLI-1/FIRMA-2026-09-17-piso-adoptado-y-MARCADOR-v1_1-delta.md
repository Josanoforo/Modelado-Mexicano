# FIRMA DE MESA · 17/sep/2026 · el piso no vencido es el estimador de la celda — y delta v1.1 del diseño del marcador

## 1 · Firma, verbatim (conversación de dirección, 17/sep/2026; se archiva en `forense/encargos/` con el primer acto de la tanda 2 que la propague)

> "Un piso no vencido en su celda-D es el estimador adjudicado de esa celda y se adopta salvo veto de mesa. Se adoptan las 20 celdas de ADR-538 y ADR-542 (piso C2) como estimadores por celda de sus reglas consumidoras. El vocabulario celda-D v0.6 lo escribe. Los retadores son credencial para emitir donde no hay piso, no sustitutos del piso donde lo hay."

Lo que la firma **no** cambia: emitir ≠ decidir; el intervalo viaja con la `p`; H5 sigue (adoptar el piso dice qué número usar, no nada de la población); adoptar es por merge de mesa (E.2) — el acto que la propague la ejecuta, no la decide.

## 2 · Delta v1.1 sobre `MARCADOR-SEGMENTO-diseno-direccion-v1_0` (`dc66b3b73fba0346…`); el v1.0 no se edita

- **§3, una frase nueva al inicio:** *"El piso no es solo lo que hay que vencer: es el **estimador por defecto adoptado** de la celda cuando nadie lo vence (firma de mesa 17/sep). 'Valor añadido' mide cuánto mejora un retador sobre lo ya adoptado."*
- **§4, tabla:** la columna `adjudicado_id` admite el id del piso; el estado `SOLO-PISO` pasa a leerse *"R + piso adoptado, ningún retador"*, y el tercer número derivado del programa se completa con un cuarto: `celdas_con_estimador_adoptado / celdas_del_arbitro` — hoy 20 de 117 (las de cruce de los pilotos), 0 de 74 marginales hasta `PISOS-PERSISTENCIA-1`.
- **§5, con caja:** `PISOS-PERSISTENCIA-1` deja de ser "medir pisos para poder evaluar" y pasa a ser **"medir el estimador por defecto de ≈40 celdas marginales"** — alimenta al motor directamente.
- **§9, firma:** se añade la firma del §1 de este documento como punto (6).
- **§10, sucesores:** se antepone `GEN2-VOCABULARIO-v0.6` (nube): sin él, `champion_actual` no admite un piso y la adopción no se puede escribir en el registro de la celda.

## 3 · Universo (A.10)
Derivado contra `9eff694`; fuentes: notas de cierre `ADR-538`/`ADR-542`, `propuesta-motor-adaptativo-celda-v0_5.md` §3(a) (roles), `data/corrida0/decisiones.tsv` objeto `regla-adopcion-en-bloque`, `tools/corrida0.py:4256` (`ADOPTADO_ACTIVO` = sellado citado por consumidor activo). Contadores movidos: cero.
