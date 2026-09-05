ENCARGO · ACTO MAESTRA38-N10 · COBERTURA-COMPLETA-OLA6 — invoca /acto

SHA de redacción: 25383f35 · COMPUERTA: N9 fusionado (usa tools/ya_medido.py en su A.8;
verificar por producto: test -f tools/ya_medido.py). ENTORNO: NUBE. NO en CAJA. MODELO:
Fable (diseño de dominio completo; Opus mínimo). CARRILES: ninguno sobre notas de Ola 6.

FIRMA DE MESA — verbatim (4/sep/2026): «Entiendo que hay un mínimo y ese mínimo para
lanzar una ola es una cosa. Pero hoy no tenemos lo mínimo y no quiero hacerlo al mínimo
no después de haber invertido tanto en la infraestructura que creamos.» Traducción
operativa: el producto es el mapa completo de cada dominio —toda regla, no la más
cercana— y el plan para cubrirlo entero; el criterio 2 de §3.a se reporta como
consecuencia, nunca se optimiza.

A.8 contra 25383f35. Universo derivado del canon (§3.2 trabajo, §3.4 salud, §3.6 tiempo,
§3.8 cooperación, §3.9 información, §3.10 comunicación): ~30 reglas — el acto deriva la
lista exacta por comando en COMMIT-1 y la congela. Insumos en repo: reevaluación
2026-09-03 (criterio 2 y razón verbatim por dominio), mapeo-ola6-N5 (veredicto A.4 por
regla), N5 §1.3 (criterio a/b/c) y §2.6/§2.8 (método de reformulación), N6 (carga como
«tercera formulación complementaria»), inventario v1_1 (42 548 filas) + busca_reactivos,
ya_medido.py por cada id ANTES de escribir su fila. Cinco reglas ya clasificadas por
N5/N6 no se reclasifican: se citan.

SPEC — dos commits, sello «el primer resultado que produzca este procedimiento es el que
se reporta».

COMMIT-1 · UNIVERSO Y CRITERIO, antes de mirar el inventario.
  (a) Tabla dominio × regla: id, tier, texto SI…ENTONCES…PORQUE verbatim, antecedente(s)
      y desenlace separados, salida de ya_medido.py.
  (b) Criterio de clasificación por regla, cerrado: MEDIBLE-COMO-ESTÁ (antecedente y
      desenlace en la misma persona en algún instrumento del corpus) · REFORMULABLE
      (existe reactivo para una consecuencia observable del antecedente O para otro
      desenlace del mismo driver; conserva driver y signo; cambia una sola cosa) ·
      CON-CANDIDATA (instrumento identificado fuera del corpus, con ficha) ·
      HIPÓTESIS-SIN-INSTRUMENTO (ningún instrumento nacional lo mide; se escribe el
      instrumento mínimo: una pregunta, una población).
  (c) Regla de honestidad: si conservar el driver exige un reactivo que no existe, no
      es REFORMULABLE aunque haya algo parecido. Ruido de substring no cuenta (N5 §2.0).

COMMIT-2 · CLASIFICACIÓN CON EVIDENCIA, regla por regla, las ~30.
  Por regla: clasificación, reactivos (id, instrumento, texto copiado del inventario,
  n aproximado), y para REFORMULABLE el objeto reformulado + se_mueve_si + qué
  sostiene/refuta; para CON-CANDIDATA la ficha; para HIPÓTESIS el instrumento mínimo.
  Por dominio, el PLAN DE COBERTURA COMPLETA: (i) reglas medibles hoy → specs a sellar
  en nube (S6…, patrón N7), (ii) adquisiciones necesarias → filas de cola candidatas,
  (iii) hipótesis declaradas → salen del denominador, (iv) el criterio 2 como
  consecuencia: «con (i) el dominio queda en k de n; con (i)+(ii) en k' de n». Un
  dominio se declara COMPLETABLE (toda regla en i, ii o iii con ruta escrita) o
  INCOMPLETABLE (alguna regla sin ruta ni instrumento mínimo formulable — se dice cuál).

CIERRE. Nota forense/notas/2026-09-0X-MAESTRA38-N10-cobertura-ola6.md con las seis
tablas y una tabla resumen dominio → n reglas → medibles / reformulables / candidatas /
hipótesis → COMPLETABLE. FP-303 · «mesa firma el plan de cobertura por dominio» (vence
7 días), con el costo por dominio a la vista: specs (nube), mediciones (caja),
adquisiciones (mesa). Cero cambios en canon ni propuesta: N-siguiente propaga lo firmado
y sella specs por dominio. Hallazgos: una línea por regla que N5/reevaluación clasificó
distinto de lo que ya_medido.py devuelve.

PERÍMETRO. Toca: la nota · tablero (FP-303 + recibo) · A.3 · cascada. NO toca: canon/**
(salvo ADR) · milpa/** · forense/prereg-caja/ · data/** · cola. Si te encuentras
escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo
vale más que el atajo.

FP/ADR: ADR-341 (340 es N9) · FP-303 (decisión) · FP-304 recibo. CONTADOR: reglas de
Ola 6 con clasificación y ruta 2 → ~30 (declara el real) · dominios con plan de
cobertura completa 0 → 6 · medición de modelo: cero — diseño, declarado.
