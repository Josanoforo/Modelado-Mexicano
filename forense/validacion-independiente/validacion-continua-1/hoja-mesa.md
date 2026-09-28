# Hoja para mesa · ACTO GEN2-VALIDACION-Y-2027-1 · lo irreversible

28/sep/2026 · dirección resuelve, mesa sella · base `9d2550b9`, 0-bis `f926d95c`. Solo hay tres decisiones, más una premisa que cayó. Ninguna adopta cifras.

## 1 · Aperturas de acceso para la validación ciega (P1 y lote 4)

**Situación.** El aparato de C1 está listo: CONTRATO-v3 firmado (R31), reconstructor de opción A (R32) y receta aislada de LANZAMIENTO-LOTE3. Lo único que falta es el gate **ACCESO-AUTORIZADO**, que se firma por paquete (`26a2-01`: «cualquier C1 real exige además … ACCESO-AUTORIZADO por paquete»). En `forense/firmas-pendientes.tsv` hay 647 filas. Solo `0c1f-02` concede «Acceso C1», y cubre ENBIARE, ENCODAT, ENCUCI y ENIGH 2022. Ninguna de esas filas nombra los instrumentos de abajo; lo derivan `gates.py` y su control positivo.

- **P1 · 20 518 RESULT nuevos del catálogo v1.3** (14 CALC; tabla `gates-v1_3.tsv`): ENSU 12 634 · EMAT 3 304 · EDR 2 578 · CCPV 640 · ENDISEG 424 · ENPECYT 280 · MMSI 158 · ENVIPE 138 · ENOE 136 · ENADID 100 · LATINOBARÓMETRO 68 · PEW 44 · ENASEM 14. Las 14 specs humanas existen y su sha casa con el `spec.yaml`. Hoy tienen 0 filas en el libro.
- **P2 · lote 4** (tabla `lote4-gates.tsv`): ENIF 2024 99 RESULT en 7 CALC (7 ya en el libro) · ENUT 2024 1 · ENSANUT 2024 169. Mantienen su reserva: ENIF m7 (R06), ENSANUT 2024 como ola que entró reservada, y `9c9e-01`, que difiere los permisos «por textos separados».

**Opciones** (`FP-260928-GEN2-VALIDACION-Y-2027-1-f926-01` y `-02`):
- (1) **Firmar el acceso por paquete** con el texto de la columna `firma_que_lo_abre` de cada tabla. Costo: una sesión receptora y una reconstructora por paquete. ENSU y EMAT son grandes.
- (2) Firmar solo P1 (olas abiertas) y dejar el lote 4 hasta que haya texto por módulo. Costo: ENIF, ENUT y ENSANUT 2024 siguen sin validación ciega.
- (3) No firmar. Las 20 518 quedan SOSTENER-SIN-CORROBORACION con la razón ya asentada.

**Recomendación: (2).** Las olas de P1 no están reservadas; abrirlas para la reconstructora no gasta ninguna R. El lote 4 toca olas reservadas o módulos cerrados y merece un texto por módulo.

## 2 · Atestación externa (`.ots`)

**Situación.** Quedó escrito `forense/sellos/manifiesto-sellos-2026-09-28.tsv` (578 filas = 365 `sello.json` + 213 sidecars; sha256 `ff020b949040334957d47527252373a08a3896eac915ea8652f1cd5c3ff2a6e0`), que incluye las seis emisiones 2027 selladas. El manifiesto del 23/sep tenía 343 filas.

**Receta de un minuto (SELLO-EXTERNO-2):**
```
pip install opentimestamps-client
ots stamp forense/sellos/manifiesto-sellos-2026-09-28.tsv    # crea el .ots junto al TSV
ots upgrade forense/sellos/manifiesto-sellos-2026-09-28.tsv.ots   # horas después, al anclar en Bitcoin
ots verify  forense/sellos/manifiesto-sellos-2026-09-28.tsv.ots
```
**Opciones** (`-03`): (1) mesa corre `ots stamp` y commitea el `.ots` · (2) autorizar a una sesión de caja a correrlo (la caja tiene red) · (3) quedarse con el sello interno más la firma GPG del merge. **Recomendación: (1)**, que es lo que el encargo reserva a mesa.

## 3 · Premisa que cayó: ENOE-INFORMALIDAD y ENSU-CAMPECHE no tienen contrato firmado

El encargo (§1 P3) dice «con contrato firmado (R27 (2))». R27 (2) dice, verbatim: «ENOE-INFORMALIDAD 2027T4 queda NO-LANZAR-TODAVIA; autorizo enviar a INEGI la solicitud de regla de varianza para los 39 estratos singleton de ENOE 2024T4. No adopto la receta sucesora, ningún tratamiento alternativo de singleton, cifra de diagnóstico ni COMMIT-3; cualquier regla nueva requiere firma propia antes del dato.» ENSU-Campeche solo tiene `71cf-01`, firmada como «recibir sin adoptar». No se hizo COMMIT-1 ni se selló ninguna emisión: hacerlo habría fijado un contrato que mesa no firmó (paro d). **Opciones** (`-04`): (1) esperar la regla de varianza de INEGI y firmar entonces el contrato ENOE · (2) firmar ya un contrato ENSU-Campeche con la banda de potencia que la hoja C2 declaró insuficiente (5 pp) · (3) retirar las dos del frente 2027. **Recomendación: (1) para ENOE y (1) también para ENSU**, es decir, esperar el contrato. Ninguna de las dos pierde nada mientras no llegue la ola 2027T4.
