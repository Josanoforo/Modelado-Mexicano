ENCARGO · ACTO MAESTRA32-E18 · REGLAS-OLA5-FASE1 (desde los pares medidos)

SHA de redacción: 899113c (main, merge PR #404 / ADR-232) · Redactado: 31/ago/2026, dirección maestra-32 · Instrucciones vigentes: v2.11 · Estado: GATED a que MAESTRA32-E16 · MEDIDOR-FAMILISMO fusione (mismo carril CAJA; su β̂ y su desenlace entran a esta fase si existen). Sin ranuras. El motor no se toca: las reglas nacen en un archivo PROPUESTA que el motor no carga, y mesa las sella o las devuelve al recibirlas.

ENTORNO ASIGNADO: UBUNTU (caja con corpus). Calcula las tasas base p de cada desenlace en su encuesta de calibración. NO se lanza en NUBE.

CARRILES EN PARALELO (declarado): carril CAJA = E16 → E18 (este); carril NUBE = E15 → E17. Compartidos: solo la cascada. Renumera quien fusiona segundo.

FIRMA DE MESA — verbatim, 31/ago/2026

D-C · "Ampliar." El programa (i′) (FP-190) pasa de "5 celdas + 3 θ" a dos fases: fase 1 (este acto) — reglas del motor con desenlace sellado a partir de los 6 pares ya medidos, donde el dato existe y solo falta la regla; fase 2 (sucesor) — las 5 celdas sin regla (CIV-08, DIN-11, SFT-04, SFT-06, TIC-06) y las 3 sin θ (DIN-07, TIC-01, EMP-05). Se propaga en FP-190 como enmienda fechada (texto original intacto). El congelamiento del motor (ADR-68(a)) sigue vigente: la propuesta no entra a tramite.yaml hasta sello de mesa.

0-bis · A.3

Primer commit: este encargo verbatim en forense/encargos/2026-08-31-MAESTRA32-E18-REGLAS-OLA5-FASE1.md. Al cerrar, ## CONSUMIDO con el PR.

Objeto

milpa/tramite-ola5-propuesta-v0.yaml — archivo nuevo que el motor no carga — con una regla por desenlace medido, clonando la forma exacta de tramite.mordida.discrecional (mismos campos, misma sintaxis de si:/entonces:/conducta/p/clase), y p medida en caja como tasa base ponderada del desenlace en su universo de calibración, con IC95 y ola_calibracion.

COMMIT-1 — congelado ANTES de abrir un solo archivo de datos

forense/notas/2026-08-31-reglas-fase1-spec.md: (a) plantilla: copia verbatim de tramite.mordida.discrecional (archivo:líneas) y la lista de sus campos; toda regla nueva llena exactamente esos campos — si un campo no se puede llenar desde el dato (p.ej. condiciones si: en términos de θ), se llena con el texto PENDIENTE-DE-MESA y se declara, no se inventa; (b) lista cerrada de reglas fase 1, con id propuesto en el formato de la casa (dominio.tema.conducta): civico.denuncia.miedo_desconfianza (ENVIPE 2025, BP1_23, θ G4), dinero.ahorro.tiene_ahorros (ENNViH olas 2-3, cr27, θ G3.horizonte), familia.apoyo.<desenlace ENIF 2024 de G3.familismo> (leer fuente), familia.corresidencia.adulto_familiar (EDER 2017, si E16 fusionó — si no, se lista como PENDIENTE-E16), y el sello ENCUCI de tramite.mordida.discrecional (desenlace AP5_17|AP5_18, FAC_SEL) como enmienda propuesta a la regla existente; (c) por regla: encuesta, ola, base/payload (id del manifiesto), universo, ponderador (todos copiados de sección A / E8 spec / notas del 4/ago, archivo:línea), estimador de p = proporción ponderada del desenlace=1 en el universo, IC95 por diseño o bootstrap 10k/seed 42 declarado; (d) ola_calibracion = la ola de la que sale p; clase: MEDIDO·p(tasa base ponderada); (e) B-bis: cada regla propuesta con p medida es un candidato nuevo de marco-M (P0 en su ola de calibración; P1 en otras olas por el criterio D-D) — se cuenta cuántas celdas de transferencia habilitaría cada una con los inventarios, sin sellar nada. Cierra con: "el primer resultado que produzca este procedimiento es el que se reporta."

COMMIT-2 — corrida única

tools/tasas_base_fase1.py (nuevo) → los p con IC por regla, pegados en milpa/tramite-ola5-propuesta-v0.yaml y en forense/notas/2026-08-31-reglas-fase1-cierre.md (n por universo, p, IC, ponderador, A.13). Intocables (git diff --stat vacío): milpa/tramite.yaml, milpa/procedencia.yaml, milpa/src/**, todo el duelo. tests/check.py --baseline VERDE (el archivo nuevo no debe romper ningún test de carga: verifica que milpa/src/procedencia.py no lo lea; si lo leyera, PARO — el motor seguiría congelado solo de nombre). Tablero: FP-190 enmienda fechada (fase 1/fase 2); fila nueva "mesa sella las N reglas de fase 1 o las devuelve; hasta entonces el motor no las carga" — es el recibo que trae la decisión siguiente, no una ranura de este acto.

PERÍMETRO Y CONCURRENCIA

Archivos: forense/encargos/2026-08-31-MAESTRA32-E18-REGLAS-OLA5-FASE1.md · forense/notas/2026-08-31-reglas-fase1-spec.md · forense/notas/2026-08-31-reglas-fase1-cierre.md · tools/tasas_base_fase1.py · milpa/tramite-ola5-propuesta-v0.yaml (nuevo, no cargado) · forense/firmas-pendientes.tsv · cascada. No toca tramite.yaml, procedencia.yaml, milpa/src/**. "Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo."

FP pre-asignadas

FP-200–FP-201 (re-deriva).

ADR y cascada

Candidato re-derivado (deriva, no heredes; renumera quien fusiona segundo). El ADR trae la firma D-C, la lista de reglas con p e IC y escala declarada, los campos PENDIENTE-DE-MESA, y el conteo de celdas de transferencia que habilitarían. registro-rotulos: MAESTRA32-E18. T25.

CONTADOR

Reglas propuestas con p medida: N (esperado 4-5) · dominios del motor que dejarían de estar vacíos si mesa sella: hasta 3 (cívico, dinero, familia).

Lo que este acto NO hace

No carga nada al motor. No toca tramite.yaml. No escribe condiciones si: que el dato no dicte. No hace fase 2. No congela marco-M.

Sucesores declarados, no lanzados

Propagación de las reglas selladas a tramite.yaml (tras firma de mesa, con descongelamiento acotado en el ADR) · MARCO-M-CONGELA-v1_1 (A″) con las celdas nuevas · REGLAS-OLA5-FASE2 (las 5+3).

---

## CONSUMIDO

PR pendiente.

Gate verificado SATISFECHO (MAESTRA32-E16 fusionó como PR #406 antes de arrancar este acto). 5 de 5 reglas candidatas con `p` medida real: `civico.denuncia.miedo_desconfianza` (ENVIPE2025 p=0.294313), `dinero.ahorro.tiene_ahorros` (ENNViH ola2 p=0.174804), `familia.apoyo.recibe_dinero_familiares` (ENIF2024 p=0.457707), `familia.corresidencia.adulto_familiar` (EDER2017 p=0.996086), enmienda ENCUCI a `tramite.mordida.discrecional` (p=0.125822). Ninguna cayó en `PENDIENTE-E16` (gate satisfecho) ni en `NO-ENCONTRADO` (los 5 payloads existen en `data/raw/`).

Detalle: `forense/notas/2026-08-31-reglas-fase1-spec.md` (COMMIT-1), `forense/notas/2026-08-31-reglas-fase1-cierre.md` (COMMIT-2), `milpa/tramite-ola5-propuesta-v0.yaml` (objeto, motor NO lo carga), `tools/tasas_base_fase1.py` (script). Tablero: `forense/firmas-pendientes.tsv` FP-190 enmendada, FP-200/FP-201 nuevas. Cascada: `canon/gobernanza-v1_15.md` ADR-236 (candidato), `canon/estado-programa-v1_10.md`, `canon/registro-rotulos.tsv` (MAESTRA32-E18), `tests/check.py` (T25).

Intocables verificados vacíos: `milpa/tramite.yaml`, `milpa/procedencia.yaml`, `milpa/src/**`. `tests/check.py --baseline`: VERDE.
