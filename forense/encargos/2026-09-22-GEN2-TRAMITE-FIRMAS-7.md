# ENCARGO · ACTO GEN2-TRAMITE-FIRMAS-7 · Cuatro firmas del 22/sep con fila, y el bloque de adopción de doce RESULT — adoptado por tu merge, no por el acto

> ENTORNO: **NUBE**. Hook; si no coincide, PARA.

CABECERA · SHA `3f48be30` · una sola sesión · MODELO: Sonnet (propagación con textos dados) · MODO: **ABIERTO** · CONTADOR: cero mediciones; `cuenta_gen2` de `K2-…-0002` SI → NO (−1 en `N_corridas_selladas`, reportado); `adoptados_activos` sube por el bloque de P2 **solo si mesa deja la hoja firmada**; `adoptados_activos` 72 → 87 si P3 acredita `origen_numerico` · ids raíz de acto.

## 1 · OBJETIVO
Que las cuatro decisiones de mesa del 22/sep queden con fila, y que el bloque de 12 RESULT de `FP-260922-GEN2-TRAMITE-PENDIENTES-1-18fa-01` entre como PR de adopción (E.2: el merge de mesa del PR que trae el bloque **es** la adopción). «Hecho» = `decisiones.tsv` con fila por firma de §2 que sobreviva; FP `…18fa-01`, `…2868-01`, `…02e6-01` FIRMADAS con cita; NC `…MARGINALES-ADOPCION-1-c45c-01` CERRADA con las filas 3D; `status` → `pendientes_adopcion` 12 → N y `adoptados_activos` reportados.

## 2 · FIRMAS DE MESA — propuestas; mesa borra la línea que no firme
- **F1 · K2 réplica:** «`CALC-DIN-CREDITO-K2-BANCARIA-HISTORIA-0002` es RÉPLICA de la `-0001` (`repite_de`; 68/68 RESULT idénticos, delta 0): evidencia de replay, no medición nueva. `cuenta_gen2 = NO` para la `-0002`; la `-0001` es la que cuenta; su asiento cita la réplica.»
- **F2 · ENIF-IC 2868-01:** «ADOPTAR-CON-RESERVA-DE-ANCHO: las 32 marginales de ENIF 2024 adoptan el piso t−1 (mismo punto); el IC viaja rotulado «conservador: calibrado con un solo choque 2018→2021, 35 pp de ancho mediano»; ninguna frase de producto lo llama cobertura. Sucesor: recalibrar τ con un segundo choque comparable.»
- **F3 · MARCO-M 02e6-01:** «HISTÓRICO-SIN-RETIRO: el marco M deja de admitir lecturas nuevas; las 7 herramientas siguen leyéndolo hasta que el relevo sustituya las 43 lecturas sin candidato; se retira cuando el mapa dé 0 SIN-SUSTITUTO.»
- **F4 · origen_numerico (NC c45c-01):** «Se acredita `origen_numerico` de los `CALC-PISOS-*-EJES-000x` citados por las 15 celdas ENVIPE adoptadas, por fila de decisión 3D caso por caso tras leer la spec de cada uno, sin editar ningún CALC (precedente ed7d-01).»
- **F5 · Hoja de adopción 18fa-01:** «Se adopta en bloque la hoja tal como la escribió TRÁMITE-PENDIENTES-1, **excepto** los RESULT que ahí llevan recomendación VETAR o `verify ≠ REPRODUCE`, que se vetan con esa cita.» *(mesa edita la lista si quiere otra cosa; sin esta línea, P2 no corre y la FP sigue ABIERTA).*

## 3 · LO QUE DIRECCIÓN SABE
- `[EJECUTADO]` `decisiones.tsv` al redactar: 0 filas con `K2-BANCARIA-HISTORIA-0002`, `RESERVA-DE-ANCHO`, `HISTÓRICO-SIN-RETIRO`; 15 con `origen_numerico` (el acto lee cuáles son y qué falta). FP abiertas: 4 (las tres de arriba + respaldo del corpus, que no va aquí).
- `[EJECUTADO]` `-0002` de K2: `repite_de = -0001`, 68/68 RESULT con delta 0, `cuenta_gen2 = SI` en las dos etiquetas. `[LEÍDO]` FP `…2868-01`: 32/32 cobertura, 35 pp de ancho, opciones ADOPTAR-CON-IC-CALIBRADO / CON-RESERVA-DE-ANCHO / SEGUIR-DIFERIDA. `[LEÍDO]` FP `…02e6-01`: 65 SIN-SUSTITUTO, 7 herramientas, recomendación del ejecutor HISTÓRICO-SIN-RETIRO. `[LEÍDO]` FP `…18fa-01`: hoja de 12 RESULT con consumidor, GEN1, GEN2, delta, verify y recomendación.
- `[SUPUESTO]` El mecanismo de adopción por bloque (`corrida0` + `usos.tsv`) admite marcar los 12 como ADOPTADO en un solo commit a partir de la hoja. Si resulta falso, P2 abre NC con lo que el instrumento no admite y el bloque queda en la FP FIRMADA, sin ejecutar.
- ADJUNTOS: ninguno (las firmas van en §2, el sello del cuerpo las cubre).

## 4 · YA HECHO / YA DECIDIDO
Por id de FP y de RESULT en `decisiones.tsv` y `usos.tsv` antes de asentar; si algo entró vía #1011 o #1002, se cita. Ramas vivas al abrir: E11 (canal) puede estar en vuelo — **fusionar después de E11** para que las filas de la vista se publiquen solas.

## 5 · PIEZAS
- **P1** una fila en `decisiones.tsv` por firma que sobreviva (F1–F4); FP → FIRMADA; `cuenta_gen2` de `-0002` proyectado a NO por el mecanismo (precedencia: fila de mesa); NC c45c-01 → CERRADA con las filas 3D (una por CALC-PISOS, con la spec citada).
- **P2** el bloque: los RESULT de F5 marcados ADOPTADO por el mecanismo de la casa, en **un** commit rotulado `[ADOPCION-BLOQUE 18fa-01]`; los vetados con fila propia; FP `…18fa-01` → FIRMADA. `status` antes/después.
- **P3** nota con la tabla firma · fila · qué desbloquea.

## 6 · LATITUD
DECIDES TÚ: orden y formato. PREGUNTAS A MESA: si un RESULT de la hoja cambió de `verify` desde #1011 (p. ej. por E11), ¿se adopta con el veredicto nuevo (recomendado, citado) o se saca del bloque? NO DECIDES: §7.

## 7 · PAROS
a) no aplica · b) editar sellos o firmas dadas · **c) adoptar fuera de F5, o `cuenta_gen2 = SI` a la `-0002`** · d) no aplica · e) caja · f) inalcanzable.

## 8 · COMPUERTAS
«F5 presente en el lanzamiento — protege: adoptar (P2).» Sin F5, P1 y P3 corren igual.

## 9 · PERÍMETRO
Propio: `data/corrida0/decisiones.tsv` · `forense/firmas-pendientes.tsv` · `forense/no-corrido.tsv` · derivados por comando (`usos.tsv` vía mecanismo de adopción) · nota · `canon/L0/<raíz>.md`. Ajeno: CALC, `milpa/`, el yaml de estimadores (lo escribe el marcador; si F2 exige re-derivarlo, es sucesor `MARGINALES-ADOPCION-2`). Otro acto en vuelo: E11 (`.gitattributes`, `verify.yml`) — sin archivo común. «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · NO HACE · SUCESORES · CIERRE
No mide, no re-deriva el marcador, no edita CALC. Sucesor: `MARGINALES-ADOPCION-2` (ENIF con reserva de ancho, por el marcador). Auditoría: no aplica. Cierre por /acto.


