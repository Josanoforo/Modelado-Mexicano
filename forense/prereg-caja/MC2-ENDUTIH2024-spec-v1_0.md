# MC2 · ENDUTIH 2024 (ola vista; 2025 RESERVADA) · uso de internet por edad, horas, uso diario y WhatsApp · spec v1.0

ACTO GEN2-MEDICION-CARRILES-2, hija ENDUTIH, CAJA, rama `acto/gen2-medicion-carriles-2--endutih`. CALC
`data/corrida0/CALC-MC2-ENDUTIH2024-0001` (prueba `tests/test_mc2_endutih2024.py`). Todo RETROSPECTIVA. No adopta.

## 0 · Premisas, reserva y lectura previa

- ENDUTIH 2025 **RESERVADA** (R05, ADENDA-1 de TRAMITE-FIRMAS-21): no es input (regla de mesa ADENDA-2: se miden olas
  vistas y se declara). ENDUTIH 2024 y 2023 son vistas (`CALC-ENDUTIH-PISOS-2024-0001`, `-2023-0001` sellados).
- Payload `endutih2024_bd_dbf_zip`, miembro `tic_2024_usuarios.DBF` (persona elegida de 6+; `FAC_PER`, `EST_DIS`, `UPM_DIS`),
  leído con `tests/dbfmini.py` como input de código con sha256 (el mismo lector que el CALC sellado).
- Lectura previa: FD `endutih2024_fd_xlsx` (hoja tic_2024_usuarios: 7.1–7.4, 7.15, 7.16) y nombres de campos del DBF; de
  `CALC-ENDUTIH-PISOS-2023/2024-0001` sólo las llaves (medida, dominio), no sus valores.
- E.5: los pisos sellados traen `internet`, `celular`, `actividad_mensajes`, motivos, por EDAD (06-11, 12-17, 18-29, 30-59,
  60+), TLOC, SEXO, ENT, escolaridad. No traen 18-24, 55-64, 65+, horas, uso diario ni WhatsApp: eso se mide aquí.

## 1 · Variables (A.15)

- `P7_1` «En los últimos tres meses, ¿ha utilizado internet…?» 1/2 → INTERNET.
- `P7_3` «¿con qué frecuencia ha utilizado internet?» 1 Diario … 5 → USO-DIARIO entre usuarios.
- `P7_4` «¿Cuántas horas al día usa internet? (cuando lo utiliza)» 01–24 → HORAS-DIA (media entre usuarios).
- `P7_15` «¿ha usado redes sociales?» 1/2; `P7_16_6` «¿Qué redes sociales utiliza? Whatsapp» 1/2 →
  WHATSAPP-USUARIOS-REDES (entre P7_15 = 1) y WHATSAPP-USUARIOS-INTERNET (entre usuarios; quien no usa redes = 0).
- Edad `EDAD`: 18-24, 25-54, 55-64, 65+. IC95: bootstrap de UPM dentro de estrato, 2 000 réplicas, `PCG64(42)`.

## 2 · Pre-registro B-bis (fijado antes del dato)

Nivel: `c` ∈ IC95 → CONFIRMA; |punto − c| ≤ 0.10 → MATIZA; si no ROMPE; horas en escala relativa (≤ 25 %). Celdas
selladas: su `punto` e `ic95`. Ola no nombrada u otra ola, o universo proxy → tope MATIZA.

| afirmación | estimando y regla |
|---|---|
| JUV-007 | INTERNET-EDAD-18-24 vs 0.97; HORAS-DIA-EDAD-18-24 vs 5.7 h (relativa); smartphone 97.2 % sin reactivo identificado: `PARCIAL` |
| TEC-008 | INTERNET-EDAD-55-64 vs 0.71 y INTERNET-EDAD-65-MAS vs 0.421 (nivel, el peor) |
| TEC-033 | «91 % de penetración de WhatsApp» (cifra de blogs): WHATSAPP-USUARIOS-INTERNET-NAC vs 0.91 (nivel) |
| TEC-031 | WhatsApp como capa transaccional: mecanismo no observable → **PISO-SIN-DICTAMEN** (se reportan los pisos de WhatsApp) |
| CONOC-008 | sellado 2023 `internet` TOTAL vs 0.812 (nivel) |
| CONOC-007 | sellado 2023 `actividad_mensajes` TOTAL vs 0.912 (universo usuarios de internet, no de smartphone: tope MATIZA); 91.5 % redes y 97.1 % smartphone no se miden: `PARCIAL` |
| CONS-038 | sellado 2024 `internet` TLOC_1 vs 0.712 y TLOC_4 vs 0.392 (ola no nombrada: tope MATIZA); ROMPE si TLOC_1 ≤ TLOC_4 |
| JUV-008 | sellado 2024 `internet` TLOC_1 vs 0.86 y TLOC_4 vs 0.67 (nivel, el peor) |
| SALMEN-025 | sellado 2024 `celular` EDAD_12_17 y EDAD_18_29 vs 0.90 (nivel, el peor); «35.3 millones» es total: `PARCIAL` |

## 3 · Módulo de auditoría v2.16

Unidad persona 6+; RETROSPECTIVA. La brecha de uso por edad y localidad es primero acceso y costo (los motivos sellados
lo muestran), no rechazo cultural. Sin variables de ascendencia.

El primer resultado que produzca este procedimiento es el que se reporta.
