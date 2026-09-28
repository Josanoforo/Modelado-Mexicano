# Hoja para mesa · qué pide de verdad la demanda · GEN2-DEMANDA-DICTAMEN-1 (28/sep/2026)

**Contadores movidos: cero mediciones, no adopta.** La demanda baja sólo por dictamen citado; no se borró ninguna fila.

**En una línea.** La demanda decía 105 corridas y 236 resultados pendientes. Revisados uno por uno, **ninguna de las 105 corridas hace falta hoy**, y **173 de los 236 resultados ya no son deuda**: 88 ya se leen de un cálculo GEN2 y la demanda no se había enterado; 85 no se van a relevar por una regla o una firma que ya existe. Quedan **63**, y todos esperan una firma o un relevo de escritorio, no una corrida de caja.

| qué pasa con el resultado | cuántos | sale del pendiente |
|---|---:|---|
| Ya se lee de un GEN2 (`YA-RELEVADO-GEN2`) | 88 | sí |
| No se releva por regla 6 (retadores y duelos sobre olas vistas) | 43 | sí |
| No se releva porque mesa ya lo firmó (H1, H2, H3, B2, B3) | 22 | sí |
| θ y β̂ del generador: generan retadores, no emiten (§4) | 19 | sí |
| El GEN1 no dice qué midió (M03) | 1 | sí |
| Esperan firma HOLDOUT (M09–M23, letra A2 y A1) | 15 | no |
| Esperan otra firma (M05, evasión de norma ×2, ahorro ENNViH ×2) | 5 | no |
| Sin base GEN2: esperan el relevo de su medido | 17 | no |
| Celdas-D ya adjudicadas: falta el pin del champion | 17 | no |
| Celdas-D de evasión de norma sin champion | 4 | no |
| Hay un RESULT GEN2 que las releva: falta el pin | 5 | no |

Detalle fila por fila, con cita: `data/corrida0/demanda-dictamen-v1_0.tsv`.

**Qué significa para caja.** Los lotes de caja (RELEVO-TRAMITE-CAJA-2, CALC-ALTERNOS-LOTE-1) no tienen corridas de la demanda que correr hasta que mesa firme A1/A2 o B1. El trabajo que sigue es de firma y de relevo (RELEVO-CONSUMIDORES-4), no de medición.

---

## Ya en la mesa, no se repiten aquí

- **A1** (M05, M23) — `FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-01`, hoja `forense/analisis/mapa-instrumentos-alternos/hoja-para-mesa-mapa-instrumentos-alternos.md` §A1. De ella cuelgan M05, M23 y los dos asignados de evasión de norma (RES-0023/0024).
- **A2** (HOLDOUT M09–M22) — `FP-260927-GEN2-TRAMITE-NC-DECISIONES-1-f2e5-02`, misma hoja §A2.

Este acto no las decide ni las duplica: las cita como sucesor de 20 filas.

---

## B1 · Ahorro (ENNViH): el cálculo usa una ola que hoy está reservada

**Qué pasa.** `dinero.ahorro.tiene_ahorros` (RES-0029 y su complemento RES-0030) se midió en GEN1 con las olas 2 y 3 de ENNViH. Los tres archivos están en el corpus. Pero la ola 3 (2009) es la más reciente del programa, y la regla vigente la trata como reservada (`canon/MEMORIA-OPERATIVA.md` §1). Además, mesa ya dejó sin receta las celdas hermanas de esta conducta (D10 / FP-339, 7/sep).

**Opciones.**
- (a) HISTÓRICO-SIN-RELEVO: sale del pendiente, se conserva como GEN1 rotulado. Es lo mismo que ya se decidió para sus celdas.
- (b) Spec de caja sólo con la ola 2. Cambia el estimando (una ola en vez de dos) y así se declara.
- (c) Mesa abre la ola 3 de ENNViH para esta conducta.

**Recomendación: (a).** Es coherente con FP-339 y no gasta una reserva por un número que ningún consumidor vivo usa como calibración.

**Texto de firma listo:** «Firmo B1 (a): `dinero.ahorro.tiene_ahorros` (RES-0029/0030) queda HISTÓRICO-SIN-RELEVO, igual que sus celdas por FP-339; la ola 3 de ENNViH sigue reservada.»

## B2 · M03 (gobierno digital coercitivo): se dictaminó distinto de lo que pedía el encargo

**Qué pasa.** El encargo pedía que los momentos AJUSTE sin RESULT quedaran como DECIDIBLE para caja. M03 no se puede: su cálculo es «reproducir la proporción declarada de la regla», y esa proporción es un número asignado sin fuente (RES-0017/0018). Tampoco hay instrumento declarado ni un RESULT GEN2 de coercitivo en ninguna unidad (NC-…-72d9-02). Se dictaminó SIN-ESTIMANDO-RECONSTRUIBLE (INTERPRETACIÓN-DECLARADA).

**Opciones.**
- (a) Aceptar el dictamen: M03 sale del pendiente como histórico.
- (b) Mesa fija un instrumento (por ejemplo ENCIG 2025, trámite en línea obligatorio) y se encarga un CALC de caja descriptivo.

**Recomendación: (a).** Sin instrumento, una corrida de caja no tiene qué medir.

**Texto de firma listo:** «Firmo B2 (a): M03 queda HISTÓRICO-SIN-RELEVO por SIN-ESTIMANDO-RECONSTRUIBLE; si aparece instrumento, entra como momento nuevo.»

---

## Hallazgo que no pide firma

`corrida0 demanda` construía la demanda desde los consumidores, sin leer lo que ya estaba relevado: ni los `corrida0_resultado_id` GEN2 de `tramite.yaml`, ni `usos.tsv`, ni las firmas B2/B3/H1–H3. Por eso reportaba 105 corridas que ya no hacían falta. Desde este acto lee la vista de dictamen (8 líneas). El arreglo de raíz, que la demanda derive el estado por sí misma, queda como NC para el sucesor.
