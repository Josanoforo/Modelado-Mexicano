# Cierre · autoridad, civismo y comunalidad

**EJECUTADO.** Tres homónimos v2 completos con Bloque B, auditoría final, matriz por afirmación y fuente primaria localizada. El [índice local](indice-local.md) deriva 179 registros editoriales: Autoridad 59 (30 del mapa), Civismo 60 (43), Comunalidad 60 (49). Estos registros pueden solaparse; no son 179 tesis independientes ni representan población encuestada. Las tres tablas nacen de juicios explícitos, no del dictamen heredado del mapa ni de una regla de texto.

| Report | Fuente principal de conclusión | Qué se sostiene | Qué cambia | Falta |
|---|---|---|---|---|
| Autoridad | OCDE México urbano, ENCUCI, GLOBE con unidades separadas | Confianza y referentes varían por institución y situación | El supuesto sistema psicológico nacional dual queda como hipótesis; se retira la exclusividad de confianza personal | Coobservar costo de disentir, preferencia, conducta y consecuencias |
| Civismo | INE, ENVIPE 2025, ENCIG/ENCUCI, Langston 2025 | Participación y denuncia varían por proceso, población y canal | El contraste de elecciones no identifica los mismos electores ni motivos; «sin broker» se rompe sólo como universalidad | Panel de motivos, cargo/corte judicial, identificación de mecanismos |
| Comunalidad | IEEPCO, TEPJF, ENUT 2019 como instrumento, textos situados | SNI es estatus municipal; la comunalidad aporta una teoría institucional situada | Reconocimiento formal no equivale a voz efectiva ni reciprocidad a seguro; 418 municipios del portal vigente no refutan el conteo de otro periodo | Denominadores de participación, costos y beneficios por género/edad, comparadores longitudinales |

**LEÍDO.** Originales completos, mapa vigente y fuentes primarias por report. La cifra IEEPCO es externa y se atribuye al portal realmente leído. Autoridad y Comunalidad no publican RESULT propios; Civismo cita dos RESULT ENVIPE 2025 provisionales con identidad, fila, sello, unidad y decisión, sin convertirlos en regla adoptada. Coincidencia puntual, incertidumbre, validez del estimando y adopción quedan separadas.

**PROPUESTO-POR-EJECUTOR.** La [hoja de firma](hoja-firma.md) propone recibir los reports y considerar después reglas con consumidor, condición y falsador. Ninguna regla fue adoptada en motor o catálogo. C1 incompleto no impide esta entrega editorial; una decisión posterior corrige solo la tesis afectada mediante sucesor.

**Reservas.** No se abrieron ENVIPE 2026, ENASEM 2024, ENADID 2023 ni ENIGH 2024. El entorno documental CLI mostró `INDETERMINADO` por variable ausente, red permitida y corpus de microdatos no montado; se trabajó con documentos permitidos y productos sellados ya presentes. Recibo técnico independiente y firma de contenido siguen pendientes. No hay medición nueva ni incremento manual del contador.

**Gate.** Los controles locales y el gate del repositorio terminaron como consta en [verificaciones](verificaciones.md): `tests/check.py --baseline --parallel` exit 0, línea base VERDE sin FAIL nuevos. Los FAIL heredados y WARN de estado se distinguen de los controles propios; T25 quedó VERDE tras corregir tres referencias al momento 08 en las notas de este lote.

**Trazabilidad.** Corte de entrada `7748208614570a50a97c1ba830aee72a972185f9`; encargo recibido SHA-256 `8d84587787d00ba3fbeb479dcc749c6e83e47386f6afffa47ed3bb3bbe100124`, copiado en 0-bis `3a1f0be1` y archivado de forma canónica por #1237 en tanda5; producto `375d671d`. `origin/main` posterior `eda5bb9f871a85613cfb4eda7d40dc741e55d0b5` se incorporó por merge sin conflicto de producto. Los hashes por objeto están en [hashes-producto.json](hashes-producto.json).

**Interpretación declarada ante main posterior.** El 0-bis propio incluyó una copia y un sidecar local; #1237 archivó después los mismos bytes en `forense/encargos/fuentes/ASTRA6-tanda5-20260927/` con manifiesto de lote. Para cumplir «archivar una sola vez», la copia y sidecar propios salen del árbol final; permanecen en el historial del 0-bis como testigo. `verifica_lote.py` compara byte por byte ese 0-bis con el archivo canónico y su SHA de manifiesto; `## CONSUMIDO` se añade sólo al pie canónico. El sidecar inicial había usado SHA crudo donde `tools/sella_sha256.py --cuerpo` esperaba normalización; el defecto se resolvió al usar el archivo canónico y su manifiesto, sin resellar ni modificar ningún cuerpo inicial.

## NO-CORRIDO / RESERVAS

| Pendiente | Razón | Efecto | Sucesor |
|---|---|---|---|
| Recibo técnico independiente y recepción de las reglas | DECISIÓN-DE-MESA-PENDIENTE | El autor no acredita revisión externa ni adopción | Circuito `GEN2-RECIBO-ASTRA-PRODUCTO-N` y hoja de firma de este lote |

## CONSUMIDO

El encargo se ejecuta en este worktree y en el [PR #1240](https://github.com/Josanoforo/Modelado-Mexicano/pull/1240), sin fusión propia. El asiento `CONSUMIDO` está al pie del archivo recibido. La firma de misión de Jonás se cita desde el lanzamiento social existente, sin duplicarla.
