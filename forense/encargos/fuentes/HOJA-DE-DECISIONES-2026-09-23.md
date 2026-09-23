# HOJA DE DECISIONES DE MESA · 23/sep/2026
**Dirección (Claude Fable) · derivada de `origin/main = 523f3c6d` y de las ramas vivas al corte · FP ABIERTAS en el TSV: 2 · NC con razón `DECISIÓN-DE-MESA-PENDIENTE`: 36 según inventario v3, re-verificadas aquí una por una contra lo que ya cerró. Cada decisión trae qué es, por qué ahora, recomendación con razón y texto de firma listo. Lo que mesa firme aquí entra al repo por `GEN2-TRAMITE-FIRMAS-11` (por escribir con esta hoja como adjunto) o viaja verbatim en el encargo que lo ejecute — nunca las dos cosas sobre la misma fila (A.12).**

## Hecho verificado que cambia la estrategia
- Piloto 3 (ENCIG, gobierno digital): encogida ΔMAE −1.47 pp, IC [0.44, 2.12] → `FALSADOR DÉBIL`. Piloto 4 (ENVIPE, evasión de norma, 4 cruces, 38 celdas): ΔMAE de C7 y C-ENCOGIDA con IC que incluye 0 en los cuatro → `FALSADOR DÉBIL` (`forense/notas/2026-09-22-GEN2-CELDA-D-PILOTO-4-ENCOGIDA-1-cierre.md:40-45`, rama). Duelos ENIGH 2024 y ENVIPE 2026: `C-PISO-ADOPTADO` / `NADIE-VENCE`. **Cinco evaluaciones, cuatro dominios: el piso nunca pierde y ningún retador de la casa lo vence con IC que despeje.** Eso es un resultado del programa, no un fracaso: hay que publicarlo así (informe v1.3, tesis D1) y dejar de lanzar pilotos de la misma familia sin un retador nuevo.
- Al fusionar el piloto 4, `celdas_validadas` sube de 92 a ~130 (38 prospectivas nuevas); al fusionar #1030 entra el primer asiento nuevo y el canal publica los 25 sellados sin fila.

## Decisiones vivas (8)

**D1 · PR de Astra: #1030 sí, #1031 no — y qué hacer con las cuatro emisiones ENVIPE de Astra.** FP `…RECIBO-ASTRA-1-4e74-01`. El recibo verificó (a)–(c) para ENCIG y encontró que ENVIPE llegó tarde para el piloto 4. Pero el piloto 4 ya abrió y selló la R de esos mismos cuatro cruces, y las emisiones de Astra se sellaron antes (20:15 vs 20:58, orden de sellos verificable por diff): pueden adjudicarse **PROSPECTIVA por orden de sello, secundaria, sin adopción**, en un acto chico de nube que lea solo RESULT sellados. Es la primera prueba real de si Astra vence al piso, sin pilotos nuevos.
Recomendación: fusionar #1030; devolver #1031 con la instrucción de re-abrirlo contra `main` cuando el piloto 4 fusione, para que un acto `GEN2-ASTRA-ENVIPE-ADJUDICACION-1` lo puntúe contra la R del piloto 4.
Firma: «Mesa fusiona #1030 con las NC del recibo. #1031 se devuelve sin fusionar; sus cuatro CALC se adjudican contra la R sellada por GEN2-CELDA-D-PILOTO-4-ENCOGIDA-1 en un acto de nube, rotulados PROSPECTIVA-POR-ORDEN-DE-SELLO, secundarios, sin adopción, con el mismo umbral primario del piloto.»

**D2 · Fusionar el piloto 4 y qué sigue: piloto 5 solo con retador externo.** Rama `acto/gen2-celda-d-piloto-4-encogida-1`, 10 commits, dictamen sellado. Con dos pilotos negativos, el piloto 5 (ENCIG) solo vale si trae un retador que no sea de la casa: C-ASTRA ENCIG (#1030) cumple (a)–(c) y entra por id.
Recomendación: fusionar el piloto 4 hoy; lanzar el piloto 5 con C-ASTRA como retador principal y C-ENCOGIDA como secundario, no al revés; si Astra tampoco vence, cerrar la serie de pilotos de encogida y escribirlo.
Firma: «Mesa fusiona el piloto 4. Autoriza el piloto 5 con C-ASTRA ENCIG (#1030) como retador principal y C-ENCOGIDA como secundario; comparación primaria = diferencia de error medio con IC por réplica, umbral fijado antes de abrir 2025. Si nadie vence, la serie de pilotos de encogida se cierra con ese dictamen.»

**D3 · ¿Las adjudicaciones de crédito cuentan en `celdas_validadas`?** NC `…ESCOLARIDAD-2-0af9-02`: 4 celdas × 9 conductas con veredicto sellado (ADJ16) no entran porque `_celdas_validadas` solo lee marcador y celdas-D. Es la definición de la métrica rectora: predicha antes, comparada después.
Recomendación: entran, vía celda-D registrada por el acto que las selló (no fila de marcador a mano). Si quedan fuera, la métrica subcuenta el producto de dinero por diseño y habrá que decirlo en el informe.
Firma: «Las adjudicaciones selladas de CALC-DIN-CREDITO-PREDICCION-2024-ADJUDICACION-0001 entran a celdas_validadas mediante celda-D registrada por un acto sucesor de PRODUCTO-DINERO; ninguna fila del marcador se escribe a mano.»

**D4 · Gobierno de fusiones (las tres líneas de 8e53-04).** NC `…CIERRE-SIN-CHOQUE-2-8e53-04`, `…AUTOMERGE-1-e889-01/02/03`, `…FIRMAS-8-aa3f-04`. Sin respuesta, el auto-merge de rutinas (#1022) queda instalado y apagado, y todo PR de papeleo sigue pasando por tu botón.
Recomendación: (i) `main` protegida con CI verde obligatorio; (ii) merge queue sí; (iii) el token de Actions fusiona solo PR rotulados de rutina (`/encola`, trámites, `[deriva]`); todo lo que mide lo fusiona mesa.
Firma: «main exige check.py VERDE antes de fusionar; se activa merge queue; el token de Actions puede fusionar únicamente PR cuya rama empiece por claude/encola-, acto/gen2-tramite- o [deriva]; los actos que sellan corridas los fusiona mesa.»

**D5 · Respaldo físico del corpus.** FP `…CORPUS-INTEGRIDAD-Y-RESPALDO-1-3d56-01` (ABIERTA desde el 21/sep) y NC `3d56-02` (cuatro propuestas de manifiesto). 19.8 GB verificados siguen en el mismo disco que el corpus: no es respaldo. Es la única FP humana pendiente y la que peor sale si falla.
Recomendación: disco externo esta semana; las cuatro propuestas de manifiesto se aceptan (raíz explícita en 1 009 entradas y los dos PDF de MOCIBA), las ejecuta el acto que traiga el disco.
Firma: «Destino del respaldo: disco externo conectado a caja; repetir los cuatro comandos de INSTRUCCION-RESPALDO.md con --destino. Se aceptan las cuatro propuestas de propuestas-manifiesto-2026-09-21.tsv.»

**D6 · Eje del replay en la vía (i).** NC `…RELEVO-TANDA-4-dedd-02`: ocho corridas selladas con `cuenta_gen2 = SI` dan `REPLICA-RESULTADO · CONTEXTO-DISTINTO`; E.3 dice que la vía (i) exige REPRODUCE «mientras mesa no firme otra cosa». Sin firma, esos ocho pines no relevan a nada.
Recomendación: la vía (i) lee el eje RESULTADO igual que (ii) y (iii), con el CONTEXTO declarado en la nota del pin — es lo que ya se firmó para las otras dos vías (7bf5-01) y no hay razón distinta aquí.
Firma: «La vía (i) de relevo lee el eje RESULTADO; CONTEXTO se declara en la nota del pin. Aplica a las ocho corridas de NC-260921-GEN2-RELEVO-TANDA-4-dedd-02.»

**D7 · Motor: quién puede tocar `motor.py`.** NC `…MOTOR-THETA-CONGELADA-1-e8fa-01/02`, NC-0445/0446 (tests que fallan por el ValueError del cargador). Nadie tiene permiso de editar `milpa/src/motor.py` porque mueve el contexto de replay de dos sellos. Es un bloqueo real para MOTOR y para ASTRA-2 (θ).
Recomendación: autorizar un acto sucesor de MOTOR con permiso explícito y perímetro cerrado (las líneas que la NC cita), que re-selle los dos CALC afectados como CALC nuevos (E.3: reejecutar es un CALC nuevo) y arregle el cargador.
Firma: «Se autoriza un acto de MOTOR a editar milpa/src/motor.py en las líneas citadas por NC-260921-MOTOR-THETA-CONGELADA-1-e8fa-01; los dos sellos cuyo contexto cambie se suceden por CALC nuevos, no se reescriben.»

**D8 · `INDETERMINADO` en `envuelto_legacy` / `origen_numerico`.** NC `…C2-RESTRINGIDO-1-4e12-03`, `…IC-CALIBRADO-1-2868-03`, `…DUELO-ENVIPE2026-COMMIT-1-8796-05`: el registro no sabe clasificar inputs que son TSV sin campo `funcion` o METADATO que cita CALC por id. Hoy cinco corridas GEN2 llevan ese rótulo.
Recomendación: aceptar `INDETERMINADO` como valor válido de registro (no bloquea contar ni adoptar) y encargar a TUBERÍA, sin prisa, que `_funcion_de_dependencia` lea el `funcion` cuando exista.
Firma: «INDETERMINADO es un valor válido de origen_numerico/envuelto_legacy para inputs METADATO o dictamen; no impide cuenta_gen2 ni adopción. TUBERÍA lo refina cuando toque tools/corrida0.py.»

## Ya superadas — no decidir, cerrar por trámite (verificado por objeto)
- `…PENDIENTES-CAJA-1-c09b-01` (vista re-derivada en caja), `…DUELO-ENVIPE2026-EJECUCION-1-c2b4-02` (quién corre `registro --lote`), `…CANAL-PUBLICACION-1-7d98-01/02` (bandera de lote estricto): las resuelve el canal + lote estricto (#1028, `verify.yml:464-491`). Cierre `SUSTITUIDO-POR: GEN2-TUBERIA-LOTE-ESTRICTO-1`.
- `…DIN-CREDITO-HISTORIA-1-ff56-01/03` (correr K2 -0001; lectura conjunta 2012–2021): K2 -0002 sellado (#1012) y la lectura está en cola (`GEN2-DIN-CREDITO-SERIE-LECTURA-1`). Cierre `SUSTITUIDO-POR`.
- `…ENIGH2024-SERIE-Y-COMMIT-1-7492-01` (run nunca invocado): el duelo ENIGH 2024 corrió COMMIT-2/3 (`CALC-ENIGH-DUELO-*` sellados). Cierre `SUSTITUIDO-POR`.
- `NC-0394` (cuenta_gen2 de RES0028 derivado): vía recibo; ya hay recibos 4/5/6 — si ninguno la firmó, va como fila en FIRMAS-11, no como decisión nueva.

## Lo que sigue siendo de dirección, no de mesa (lo tomo yo)
FP-374 re-sello (`958c-02`) · las 62 filas DE-MESA (`38c3-02`) · las tres FP de regla del cuaderno (`b6dc-02`) · informe v1.3 · estado v1.16 · encargo `GEN2-TRAMITE-PENDIENTES-2-ADOPCION-BLOQUE` (10 RESULT esperando adopción, exige `milpa/`).
