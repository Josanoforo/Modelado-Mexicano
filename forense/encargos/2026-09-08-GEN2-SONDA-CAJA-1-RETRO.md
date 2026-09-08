ENCARGO-ORIGINAL-NO-RECUPERADO — conversación externa (ChatGPT), procedencia tipo (3): reportado, no verificado; este expediente ficha el ACTO, no reconstruye el encargo.

# ACTO GEN2-RETRO-SELLO-SONDA-CAJA-1 · FICHA-PR635-HACIA-ATRAS

**ESTADO:** CONSUMIDO — este mismo acto
**FECHA:** 2026-09-08
**ENTORNO DE EJECUCIÓN:** NUBE
**COMPUERTA:** ninguna — trámite registral puro

## Objetivo

`PR #635` (`ACTO GEN2-SONDA-CAJA-1 · CIERRA-RESERVAS-PR632`) corrió bien y nunca fichó: fusionó con el mismo defecto que `PR #632` demostró el mismo día — sin ADR propio, sin fila en `canon/registro-rotulos.tsv`, sin fila en `forense/no-corrido.tsv`. Mesa reconoce el trabajo como propio del programa y ordena ficharlo retroactivamente, sin reescribir nada de lo que #635 ya escribió.

## Registro de qué corrió

- **PR:** #635
- **Rama:** `acto/gen2-sonda-caja-1-cierra-reservas-pr632`
- **Commit de fusión:** `51fec0539406f486eff4480f727640b5d1c33dcb` (merge de `4f26fb92149175efd47f48d9e84f29ce6e84c690` con `a7d38ff6e9feef43c54647b0244516ded914cc1f`)
- **Archivos tocados (5, verificado por comando):**
  - `data/cola-adquisicion-v1_0.tsv` (+1/-1)
  - `data/curacion-registro/cola-adquisicion-registro.tsv` (+1/-1)
  - `data/manifiesto.yaml` (+29, payloads reales)
  - `forense/hallazgos.md` (+5)
  - `forense/notas/2026-09-08-GEN2-SONDA-CAJA-1.md` (nuevo, 524 líneas)
- **Contenido revisado por dirección: bueno** — incluye la recuperación del snapshot histórico del RUPC vía republicador y la corrección de un negativo prematuro re-leyendo el JavaScript de Bienestar (`forense/notas/2026-09-08-GEN2-SONDA-CAJA-1.md`, citada, no copiada).

Verificación mecánica de conteo de manifiesto:

```text
git show 51fec053^:data/manifiesto.yaml > /tmp/mani_before.yaml
git show 51fec053:data/manifiesto.yaml > /tmp/mani_after.yaml
diff /tmp/mani_before.yaml /tmp/mani_after.yaml | grep -c '^>'   -> 29
```

Huella registral verificada contra `51fec053` (y contra `origin/main` vigente al redactar este expediente):

```text
git show 51fec053:forense/no-corrido.tsv       | grep -c "SONDA-CAJA"  -> 0
git show 51fec053:canon/registro-rotulos.tsv   | grep -c "SONDA-CAJA"  -> 0
git show 51fec053:canon/gobernanza-v1_15.md    | grep -c "SONDA-CAJA"  -> 0
git show 51fec053:canon/gobernanza-v1_15.md    | grep -c "#635"        -> 0
find forense/encargos -iname "*635*"                                   -> (vacío)
find forense/encargos -iname "*SONDA-CAJA*"                            -> (vacío, antes de este expediente)
```

Sin 0-bis, sin ADR, sin rótulo, sin fila NO-CORRIDO. `PR #635` es real (verificado por commit y contenido, no supuesto) y quedó sin sello — el mismo defecto que `PR #632`, el mismo día.

## NO-CORRIDO / RESERVAS

| qué no se corrió | razón | sucesor |
|---|---|---|
| el texto del encargo original que ordenó #635 | PARO-PREMISA (no recuperado) | SIN-ASIGNAR — si mesa lo pega algún día, se apendiza aquí con fecha, nunca se inventa |
| verificación de que los 29 payloads del manifiesto viven en el corpus compartido, no solo en el worktree de caja donde se adquirieron | NO-VERIFICABLE-AQUÍ desde NUBE — este expediente solo cuenta las 29 entradas en `data/manifiesto.yaml` versionado, no confirma que cada payload referenciado exista físicamente fuera del worktree `/home/pc0/mm-gen2-sonda-caja-1`; es exactamente el defecto que `PR #77` ya dejó documentado (manifiesto declarando payloads que el corpus compartido no tenía) | un `--verifica` por id en el próximo acto de caja |

## CONSUMIDO por PR #635

FIRMA DE MESA, verbatim del 8/sep/2026: «dame retro-sello-2» — mesa reconoce el trabajo del PR #635 como propio del programa y ordena ficharlo hacia atrás.
