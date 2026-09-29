# Lanzamiento · validación ciega continua 1 · ACTO GEN2-VALIDACION-Y-2027-1 (P1)

Lo escribe la sesión receptora **antes** de entregar ningún paquete. El commit de este archivo y de `<paq>/entrada/` es el «paquete con sha antes de entregar» (E.2). No contiene valores sellados.

## Gates (14 paquetes, 20 518 llaves)
- **APTO-TECNICAMENTE.** Paquetes armados por `prepara.py` desde `paquetes/<paq>.json`. La spec humana casa con `spec_md_sha256`, los datos casan con el sha del input DATO y el esquema lleva solo llave, unidad y descriptores. Sonda de aislamiento con control positivo en `/home/pc0/vyc27-rec/sonda-transcript.jsonl`: repo, corpus, `/tmp` ajeno, red y memoria bloqueados; numpy 2.3.5 / pandas 2.3.3.
- **CONTEXTO-NUEVO-ACREDITADO.** Opción A (R32): cada paquete corre en una sesión nueva `claude -p` (`lanza-vc1.sh`). El transcript se audita antes de abrir sellados.
- **CONTRATO-FIRMADO.** CONTRATO-v3 `821a5ecb…94eb` (R31).
- **ACCESO-AUTORIZADO.** Firma de mesa en el chat del acto (28/sep), verbatim en la nota de cierre y en `FIRMAS-Y-ACCESO.md` de cada paquete (FP `f926-01`).

## Receta (igual a LANZAMIENTO-LOTE3 §3, con estas diferencias)
- Directorio de trabajo: `/home/pc0/vyc27-rec/<paq>/`, fuera del repo.
- `paquete/lib/`: copia de `pyreadstat`, `dbfread` y `narwhals`. Son lectores de terceros que el sandbox no ve en `~/.local`; no contienen método del programa.
- Tolerancia: la sellada en el `spec.yaml` de cada CALC (`flotante abs 1e-10`). Su traducción v2 es `catalogo-1-lote3/endireh-pisos-2016-pareja-fisica-0002/entrada/tolerancia-v2.json` (mismos bytes, `{"abs": "1e-10", "rel": "0"}`). Queda fijada aquí, antes de revelar.
- IC: diagnóstico (R23); no adjudica.
- Orden E.2: la reconstructora termina; la receptora archiva su `salida/` y el transcript, y commitea y empuja. Solo después vienen la auditoría del transcript, `compare_v3 freeze`, la referencia desde el sellado y `compare_v3 compare`.

## Regla de dictamen (fijada antes de revelar; la misma de C1-LOTE-3)
- Punto dentro de la tolerancia → SOSTENER. Asiento: PASA si el comparador dice COINCIDE; si no, CONCUERDA-NO-APROBADA.
- Punto fuera → ACOTAR (NO-PASA).
- Sin punto de la reconstructora → SOSTENER-SIN-CORROBORACION. Si la causa es la spec, va a `specs-insuficientes-v1_3.tsv` (D-15).
- Rótulo del asiento: `CIEGA-POR-CONTEXTO-NUEVO`, con la reserva de red declarada (el proceso `claude` sale a la API; el aislamiento es de sandbox y namespace, no de broker).

## Declaraciones de la receptora
- En esta sesión, antes de construir los paquetes, la receptora imprimió una fila del catálogo v1.3 (`RESULT-CCPV-FAM-PISOS-AM-HOG-NUCLEAR-O-AMPLIADO-2010-EDAD-JEFE-30-44-P`, con punto e IC) al inspeccionar su esquema. No toca la ceguera de las reconstructoras, que no comparten sesión, y se declara.
- Un subagente de configuración vio por accidente la primera fila de `tsdem` de ENVIPE 2024 (llaves y códigos demográficos, sin conductas) al leer el encabezado. Está declarado en `paquetes/envipe-percepcion-2024-0001.json`.
