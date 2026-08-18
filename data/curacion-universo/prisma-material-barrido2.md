# PRISMA material BARRIDO-2

Fecha: 2026-08-17. Estado: CERRADO-E2. Red material: deshabilitada.

| Métrica | Cifra | Denominador | Comando de derivación |
|---|---:|---|---|
| declaraciones_totales | 631 | declaraciones del manifiesto | `CMD-MATERIAL` |
| declaraciones_con_archivo_sha | 627 | declaraciones del manifiesto | `CMD-MATERIAL` |
| declaraciones_sin_archivo_sha | 4 | declaraciones del manifiesto | `CMD-MATERIAL` |
| representaciones_fisicas | 672 | archivos de las dos raíces configuradas | `CMD-MATERIAL` |
| sha_unicos | 662 | representaciones físicas | `CMD-MATERIAL` |
| representaciones_declaradas | 626 | representaciones físicas | `CMD-MATERIAL` |
| representaciones_no_declaradas | 46 | representaciones físicas | `CMD-MATERIAL` |
| fuera_de_disco | 0 | declaraciones con archivo+sha | `CMD-MATERIAL` |
| divergentes_hash_o_tamano | 1 | declaraciones con archivo+sha | `CMD-MATERIAL` |
| corruptas_E0 | 0 | representaciones físicas | `CMD-MATERIAL` |
| cifradas_E0 | 0 | representaciones físicas | `CMD-MATERIAL` |
| no_soportadas_E0 | 0 | representaciones físicas | `CMD-MATERIAL` |
| reutilizadas | 0 | representaciones E2 | `CMD-MATERIAL` |
| abiertas_E1 | 672 | representaciones físicas | `CMD-MATERIAL` |
| caracterizadas_E2_o_excepcion | 672 | representaciones físicas | `CMD-MATERIAL` |
| representaciones_con_excepcion | 271 | representaciones E2 | `CMD-MATERIAL` |
| excepciones_por_objeto | 2817 | objetos E1 | `CMD-MATERIAL` |
| objetos_logicos_E1 | 1833802 | objetos enumerados | `CMD-MATERIAL` |
| objetos_caracterizados_E2 | 1830985 | objetos E1 | `CMD-MATERIAL` |
| reportes_durables_compactos | 2717 | grupos representación/tipo/estado/privacidad/frontera | `CMD-MATERIAL` |
| ola_W1 | 26 | representaciones físicas | `CMD-MATERIAL` |
| ola_W2 | 246 | representaciones físicas | `CMD-MATERIAL` |
| ola_W3 | 396 | representaciones físicas | `CMD-MATERIAL` |
| ola_W4 | 4 | representaciones físicas | `CMD-MATERIAL` |
| ola_W5_reintentos | 0 | referencias a representaciones ya asignadas | `CMD-MATERIAL` |

Comando `CMD-MATERIAL` (derivado de la invocación que produjo estas cifras):

```sh
unshare -Urn -- python3 tools/curador_registro/write_barrido2_material.py \
  --snapshot .barrido2/private/t0/snapshot-v4.json \
  --task-ledger .barrido2/private/t0/ledger-v7.tsv \
  --task-root .barrido2/tasks-v7 --staging-root .barrido2/staging-v7 \
  --contract data/curacion-universo/contrato-barrido2-v1_0.json \
  --contract-hashes data/curacion-universo/contratos-barrido2-hashes.json \
  --output-root . --private-index .barrido2/private/e2-neutral-index.jsonl --date 2026-08-17
```

Partición: W1∪W2∪W3∪W4=universo físico; intersecciones vacías; W5 sin reintentos.
