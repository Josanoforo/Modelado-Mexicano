ENCARGO-ORIGINAL-NO-RECUPERADO — redactado en conversación externa (ChatGPT), procedencia tipo (3) de v2.1: reportado, no verificado. Este expediente ficha el ACTO, no reconstruye el encargo.

# ACTO GEN2-RETRO-SELLO-SONDA-2 · FICHA-PR632-HACIA-ATRAS

**ESTADO:** CONSUMIDO — este mismo acto
**FECHA:** 2026-09-08
**ENTORNO DE EJECUCIÓN:** NUBE
**COMPUERTA:** ninguna — trámite registral puro

## Objetivo

`PR #632` (`ACTO GEN2-SONDA-2 · OPERACIONALIZA-SONDA-LATERAL`) corrió bien y nunca fichó: fusionó con un solo commit (`8cbbc9f9`), sin ADR propio, sin fila en `canon/registro-rotulos.tsv`, sin fila en `forense/no-corrido.tsv`. Mesa reconoce el trabajo como propio del programa y ordena ficharlo retroactivamente, sin reescribir nada de lo que #632 ya escribió.

## Registro de qué corrió

- **PR:** #632
- **Commit único de fusión:** `8cbbc9f9b0f378655587b91f2cedd31948c4cf14` (merge `a800f29999028f25ed830215e5ed2180f04a57a7`)
- **Archivos creados:** `.claude/commands/sonda.md`, `.claude/commands/mapea.md` (puente mínimo `SONDA-RECOMENDADA`, cambio no destructivo)
- **Colas apendizadas:** dos filas con rutas laterales `SIN-FETCH` (RUPC — verificado contra `data/curacion-registro/cola-adquisicion-registro.tsv`)
- **Nota de referencia (289 líneas, citada, no copiada):** `forense/notas/2026-09-08-GEN2-SONDA-2-operacionaliza-sonda-lateral.md`

Huella registral verificada contra `d1a97cd6` (y contra `main` vigente al redactar este expediente):

```text
grep -c "SONDA-2" forense/no-corrido.tsv        -> 0
grep -c "SONDA-2" canon/registro-rotulos.tsv    -> 0
grep -c "SONDA-2" canon/gobernanza-v1_15.md     -> 0
```

Sin 0-bis, sin ADR, sin rótulo, sin fila NO-CORRIDO. `PR #632` es real (verificado por commit y contenido, no supuesto) y quedó sin sello.

## NO-CORRIDO / RESERVAS

| qué no se corrió | razón | sucesor |
|---|---|---|
| el texto del encargo original que ordenó #632 | PARO-PREMISA (no recuperado) | SIN-ASIGNAR — si mesa lo pega algún día, se apendiza aquí con fecha, nunca se inventa |

## CONSUMIDO por PR #632

FIRMA DE MESA, verbatim del 8/sep/2026: «ármame el sello, el encargo ya corrió» — mesa reconoce el trabajo de #632 como propio del programa y ordena ficharlo retroactivamente.
