# ACTO GEN2-CIERRES-GRUPO-A · cierre

Nota del acto, contra `origin/main = fbce146d`. Encargo archivado en
`forense/encargos/2026-09-08-GEN2-CIERRES-GRUPO-A-cierra-folders-costo.md`.

## §0 · Qué hace

Propaga las firmas de mesa del 8/sep/2026 (Grupo A: «cerrar folders que
ahorita tienen costo») sobre 6 de las 10 filas VIVAS que el cruce D-4 de
`ACTO GEN2-TRAMITE-FIRMAS-1` había devuelto a mesa, más una séptima
(`PI`) diferida a un sucesor nombrado. Ningún cierre es «nunca más»: cada
uno lleva estampa de universo (A.10) — si un consumidor futuro cita la
fuente, el cierre queda VENCIDO EN ALCANCE y se reabre por re-sello, sin
tocar el texto original.

## §1 · P1/P2 — HOMESCAN / PANEL_DE_COMPRA_DE_HOGARES → CERRADA NO-GASTAR

```
$ grep -n "HOMESCAN_CONSUMER_PANEL_SERVICES\|PANEL_DE_COMPRA_DE_HOGARES" data/curacion-registro/relaciones.tsv
45:REL-2dcacf02f67355e96eac10d7  N21  HOMESCAN_CONSUMER_PANEL_SERVICES ... NO-ACCESIBLE ... NO_REFERENCIADO ...
126:REL-94e18be48f89c37e4d7164e8 N21  PANEL_DE_COMPRA_DE_HOGARES ... NO-ACCESIBLE ... NO_REFERENCIADO ...
$ grep -c "HOMESCAN\|PANEL_DE_COMPRA" data/corrida0/demanda-resultados.tsv
0
```

Cero consumidores activos hoy; ambas ya archivadas con veredicto D
firmado (`ADR-187`). `estado_A4A5` → `CERRADA NO-GASTAR` en
`data/curacion-registro/cola-adquisicion-registro.tsv`, vista
regenerada con `python3 tools/vista_cola_adquisicion.py`.

## §2 · P3 — EXT_OF_07_CATALOGO_PROVEEDORES_S1_S3_S6 → CERRADA NO-BAJAR-PORQUE

```
$ grep -rc "EXT_OF_07" data/curacion-registro/relaciones.tsv
0
```

El hueco decisivo (persona-con-id + sanción) lo cierra
`PDN_SESNA_S1_S2_S3_S6` (ya `OBTENIDO`), no el catálogo histórico de
~951MB. Contratos/expedientes 2019-2023 ya en corpus. `estado_A4A5` →
`CERRADA NO-BAJAR-PORQUE`.

## §3 · P4 — INEGI_CNGF → CERRADA NO-BAJAR-PORQUE

```
$ grep -rn "INEGI_CNGF" data/curacion-registro/relaciones.tsv
(0 líneas)
```

Documentación/cuestionarios/marco conceptual ya `OBTENIDOS`; el CSV tras
JS queda candidata registrada (receta en `PAQUETE-RECETAS-5`), no
perseguida. `estado_A4A5` → `CERRADA NO-BAJAR-PORQUE`, con la reserva de
mesa verbatim («no sabemos en un futuro») como razón de no borrar la
receta.

## §4 · P5 — SSRN hermanos → ALTA DE HERMANA

Registradas en `data/curacion-registro/aliases-fuentes.tsv`:

| alias | fuente_canonica_normalizada | sha256 | accion |
|---|---|---|---|
| `SSRN_BAUCHET_2589578_PDF` | `BAUCHET_SSRN_2474620` | `cbb6a2d43acb2657d7d54c8791aae5edb4b515bad11faef50082e50775faf029` | `NO_FUSIONAR` |
| `SSRN_BAUCHET_2689238_PDF` | `BAUCHET_SSRN_2474620` | `d0ef4d86e07b18ce52e0d4b16a1a07c644d0e829e2a58aba7104ca988c5a3a60` | `NO_FUSIONAR` |

El objeto exacto pedido por la fila (SSRN abstract_id=2474620) sigue
`EXIGE-SESION-NAVEGADOR` (5 rutas agotadas, ya documentadas en la fila
`PRICE_AND_INFORMATION_TYPE_IN_LIFE_MICROINSURANCE_DEMAND`); queda
CANDIDATA-SIN-FETCH con receta manual ≤1 min (A.5: abrir
`https://cenfri.org/research-paper/price-and-information-type-in-life-microinsurance-demand-experimental-evidence-from-mexico/`
con sesión de navegador y usar el enlace de descarga directa del PDF que
el HTML sin sesión no expone).

## §5 · P6 — OECD Trust Survey PUM → SOLICITUD-PREPARADA

El formulario ya vive en el corpus (`data/manifiesto.yaml:21239`,
id `tc_oecd_trust_survey_pum_2021_2023_2025`, archivo
`Descargas Manuales/TC-OECD-Trust-Survey-PUM-2021-2023-2025.docx`).
Receta de envío, para que mesa la ejecute (el agente no manda correos):

- **Destinatario:** `govtrustinfo@oecd.org`
- **Adjunto:** `Descargas Manuales/TC-OECD-Trust-Survey-PUM-2021-2023-2025.docx` (id de manifiesto `tc_oecd_trust_survey_pum_2021_2023_2025`)
- **Texto sugerido (inglés, ≤10 líneas):**

  > Dear OECD Trust Survey team,
  >
  > I am requesting access to the OECD Trust Survey Public Use Microdata
  > File (PUM) for Mexico (waves 2021/2023/2025), collected in Mexico by
  > INEGI. I have completed and attached the required Terms of Use form.
  > This data will be used for academic/policy research on institutional
  > trust in Mexico. Please let me know if any further information or
  > signature is needed to process this request.
  >
  > Thank you,
  > [nombre de mesa]

`estado_A4A5` de la fuente `OECD` no cambia globalmente (agrupa 3
objetos, 2 ya `OBTENIDO`); la nota de la fila registra el sub-objeto PUM
como `SOLICITUD-PREPARADA`. `## NO-CORRIDO / RESERVAS` del encargo cubre
el envío físico como `DECISIÓN-DE-MESA-PENDIENTE`.

## §6 · P7 — PI / tablero CNBV → DIFERIDO-A

Grupo B resuelto de paso: la calificación aludida por mesa es GEN1
(`RES-0083`, `LEGACY-GEN1`, `data/corrida0/usos.tsv:85`), datos
indistintos a la generación. La regla de scoring vive en la demanda GEN2
(`milpa/procedencia.yaml:755`, `milpa/catalogo-momentos-v0_1.md:67`
`M07`); la reserva del eje 3 que `RES-0083` cita, no:

```
$ grep -c "eje 3\|eje_3" data/corrida0/usos.tsv
0
```

`estado_A4A5` → `DIFERIDO-A: spec GEN2 dinero.credito.scoring_alternativo`.
No se exporta nada de `portafolioinfo.cnbv.gob.mx` hoy — 4 rutas ya
agotadas (dashboard Power-BI/ASP.NET, sin URL fija de exportación,
receta en `PAQUETE-RECETAS-11`). El acto que escriba esa spec hereda la
instrucción de export manual con destino concreto.

## §7 · Cruce con FP-286/FP-343

De las 10 filas VIVAS de §3.c (`2026-09-08-GEN2-TRAMITE-FIRMAS-1-propaga-firmas.md`):
6 cierran/avanzan aquí (P1-P6), 1 queda diferida con sucesor (P7), y 3
permanecen VIVAS sin tocar por ser Grupo C, encargo propio:
`REGISTRO_DE_TANDAS_Y_REPUTACION`, `REGISTRO_OPERATIVO_DE_TANDAS_DIGITALES`,
`ENAFIN`. `forense/firmas-pendientes.tsv` (`FP-286`/`FP-343`) actualizado
con este desglose, sin borrar el texto previo.

## §8 · Verificación

```
$ python3 tests/check.py --baseline
```

(salida pegada en el commit / PR)

## CONTADOR

Cero GEN2 — trámite declarado, mismo criterio que
`ACTO GEN2-TRAMITE-FIRMAS-1`.
