ENCARGO · ACTO MAESTRA38-V1 · CORROBORA-Y-RECONCILIA — invoca /acto

SHA de redacción: 68ce2a8d · COMPUERTA: ninguna. ENTORNO: UBUNTU con corpus y red (el disco es
el objeto). NO en NUBE. MODELO SUGERIDO: Opus o Codex — juicio de identidad de archivo y lectura
adversarial. Worktree propio; enlazar data/raw y data/raices.local.yaml desde el clon padre ANTES
de evaluar nada (defecto de PR #522). ESCRIBE SOLO: forense/notas/…V1-veredicto.md, hallazgos,
tablero (recibo). No corrige nada: encuentra.

FIRMA DE MESA — verbatim (4/sep/2026): «antes de que me digas que algo si o algo no etc, necesito
que lo corrobores a detalle o le pidamos a claude cloud o CLI que lo revise a detalle, además hay
descargas que no necesariamente entraron por el pipeline pues lo acabamos de ajustar. Entonces o
pedimos una revisión minuciosa o no avanzamos.»

P0 · RECONCILIACIÓN DISCO ↔ MANIFIESTO ↔ COLA (el censo que N6 aún no ha dado).
  python3 tests/manifiesto.py --escanea descargas_mx → salida cruda íntegra a la nota.
  Por cada «nuevo»: sha256, tamaño, mtime, y contra qué fila de la cola encaja (por nombre y por
  contenido, A.7). Tabla: DEPOSITADO-Y-REGISTRADO / DEPOSITADO-SIN-REGISTRO / REGISTRADO-SIN-BYTES.
  Verificación nominal, con comando y con sha, de lo que mesa dijo que bajaría: 35024-0001-Data.dta,
  WB 6667 microdato, PDN S1/S2/S6, y las 11 recetas de FP-286 (nombre por nombre de
  PAQUETE-RECETAS-3/-4). Cada una: PRESENTE (ruta, sha) / AUSENTE (comando que lo buscó,
  archivos examinados). Y `--verifica` por --id sobre una muestra de 20 entradas recientes.

P1 · CORROBORA DIEZ AFIRMACIONES DE DIRECCIÓN (REVISION-PR-521-528, §2 V1–V10), una por una,
  con comando, salida cruda y veredicto CONFIRMADA / REFUTADA / PARCIAL / NO-VERIFICABLE-AQUÍ.
  Incluye las dos que ya sé que están mal contadas: «4 ABIERTA» (son 6 por prefijo) y «7 entradas
  D2-a» (eran 6). V1: ¿existen filas FP-290/291 de MAESTRA38-A1? ¿T-FIRMAS las echa de menos?
  V2: ¿dos filas CSES? V4: ¿qué rechazó baseline.py exactamente? V5: ¿enfih2019_bd_csv_zip
  resuelve COINCIDE en disco para N3/N10/N13/N14? (es la comprobación barata que Frente D no hizo)
  V6: ls de tests de Frentes A/B. V7: estado real del .dta (P0). V10: los 19 FAIL del baseline,
  listados con su origen.

P2 · CORROBORA LAS PREMISAS DE LAS 28 LETRAS DE FP-286: por fila, ¿la receta de A2 sigue viva hoy
  (HEAD 200, tamaño, tipo)? ¿el objeto ya está en disco por P0? Veredicto por fila: RECETA-VIVA /
  YA-EN-DISCO / RECETA-MUERTA. Ninguna fila cambia de estado.

P3 · CORROBORA LA VERIFICACIÓN POST-HOC DE INFRA con una muestra adversarial propia, no releyendo
  la suya: correr los 5 tests de alta_relacion.py; provocar dos escritores simultáneos sobre un
  manifiesto de fixture (¿el lock falla claro?); un arbitra.py contra fixture (¿la vista queda
  intacta?); un git worktree add nuevo (¿nace sin data/raw? sí/no con ls).

CIERRE: nota con las cuatro tablas y un solo resumen: qué afirmaciones de dirección se sostienen,
cuáles no, y qué hay en disco que el repo no sabe. Hallazgos: una línea por refutación. Recibo
FP (deriva). CONTADOR: afirmaciones corroboradas 0 → N · archivos en disco sin registro 0 → M ·
medición: cero, declarado.

PERÍMETRO. Toca: forense/notas/2026-09-04-MAESTRA38-V1-veredicto.md · forense/hallazgos.md ·
tablero (recibo) · A.3 · cascada. NO toca: data/** · tests/** · tools/** · milpa/** · canon
(salvo ADR propio) · encargos existentes. Si te encuentras escribiendo fuera de esta lista, PARA —
el perímetro estaba mal calculado y saberlo vale más que el atajo.
