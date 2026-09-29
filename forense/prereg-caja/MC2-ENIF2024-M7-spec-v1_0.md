# MC2 · ENIF 2024 módulo 7 (cuatro columnas ABIERTA-PARCIAL) · forma de pago y CoDi · spec v1.0

ACTO GEN2-MEDICION-CARRILES-2, hija ENIF 2024 m7, CAJA, rama `acto/gen2-medicion-carriles-2--enif2024-m7`.
CALC `data/corrida0/CALC-MC2-ENIF2024-M7-0001` (prueba `tests/test_mc2_enif2024_m7.py`). Todo RETROSPECTIVA. No adopta.

## 0 · Premisas, reserva y lectura previa

- `[LEÍDO]` Firma de mesa (`forense/encargos/2026-09-28-GEN2-MEDICION-CARRILES-2-ADENDA-1.md`, sellada): «ENIF 2024
  módulo 7 queda ABIERTA-PARCIAL: columnas P7_1_1, P7_1_2, P7_2_1, P7_3_1». Sólo esas cuatro son input; el medidor
  revienta (`ReservaRota`) ante cualquier otra `P7_*`, con prueba por mutación (P7_4_1, P7_9_1_3) en el sintético.
- `[EJECUTADO]` Payload `enif_2024_enif_2024_bd_csv`, miembro `TMODULO.csv`, sha256 del manifiesto (preflight).
- Lectura previa: FD `enif2024_fd_xlsx` (filas de las cuatro columnas) y cuestionario §7 (7.1–7.3, pases). Ningún
  registro de módulo 7 leído antes del COMMIT-1.
- Diseño, ponderador, segmentos, estimador e IC: idénticos a `MC2-ENIF2024-spec-v1_0.md` §1–§2 (persona elegida 18+,
  `FAC_PER`, `EST_DIS`/`UPM_DIS`, 2 000 réplicas, `PCG64(42)`; sexo, edad FP-384, escolaridad, localidad, región).

## 1 · Variables por texto (A.15)

- `P7_1_1` «7.1 … ¿Qué forma de pago utiliza con más frecuencia cuando realiza compras de 500 pesos o menos?» 1
  Transferencia electrónica o aplicación de celular · 2 Uso físico de tarjeta de débito o crédito · 3 Efectivo;
  otro código fuera (contado). `P7_1_2` igual, «de 501 pesos o más». EFECTIVO/DIGITAL/TARJETA = 3/1/2 entre {1,2,3}.
- `P7_2_1` «7.2 ¿Conoce o ha escuchado de Cobro digital o CoDi?» 1 Sí 2 No → CODI-CONOCE.
- `P7_3_1` «7.3 ¿Ha utilizado Cobro Digital o CoDi para realizar sus pagos?» 1 Sí 2 No, sólo si 7.2 = 1 →
  CODI-USA-SI-CONOCE; CODI-USA-POBLACION = uso sobre toda la población (quien no conoce = 0).
- Diferencia EFECTIVO-500-O-MENOS localidad < 15 000 − ≥ 15 000 (misma réplica).

## 2 · Pre-registro B-bis (fijado antes del dato)

Regla de nivel (hijas MC2): `c` ∈ IC95 → CONFIRMA; |punto − c| ≤ 0.10 → MATIZA; si no, ROMPE.

- **CONS-010** («El 85.2 % lo usa [efectivo] para compras bajo 500 pesos (ENIF 2025)»): EFECTIVO-500-O-MENOS-NAC vs
  0.852. El report dice «ENIF 2025»; no hay ola 2025 en el manifiesto: se contrasta contra 2024 y se declara.
- **APUEST-030** («~85 % en 2024 (frente a ~90 % en 2021)»; ~62 % de NTT Data): EFECTIVO-500-O-MENOS-NAC vs 0.85
  (nivel). La ola 2021 y la cifra de NTT (transacciones, no personas) no se miden: `PARCIAL`.
- **APUEST-032** (hallazgo de instrumento, sin cifra): CODI-CONOCE y CODI-USA-* se reportan como pisos; **sin
  dictamen** (el falsador pide crecimiento 2021→2024 frente a otros medios digitales: fuera de esta pieza).

## 3 · Módulo de auditoría v2.16

Unidad persona elegida 18+; RETROSPECTIVA. Oferta antes que preferencia: el uso de efectivo en compras pequeñas se
lee junto a localidad (aceptación de pagos digitales en comercios: módulo 7 fuera de las cuatro columnas, sigue
reservado) — no como desconfianza. Sin variables de ascendencia.

El primer resultado que produzca este procedimiento es el que se reporta.
