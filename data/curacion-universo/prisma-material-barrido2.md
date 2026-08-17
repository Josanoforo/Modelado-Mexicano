# PRISMA material BARRIDO-2 · W0

Fecha: 2026-08-17. Estado: PRELIMINAR-W0. Red material: deshabilitada.

| Métrica | Cifra | Denominador | Comando de derivación |
|---|---:|---|---|
| declaraciones_totales | 631 | declaraciones del manifiesto | `CMD-W0` |
| declaraciones_con_archivo_sha | 627 | declaraciones del manifiesto | `CMD-W0` |
| declaraciones_sin_archivo_sha | 4 | declaraciones del manifiesto | `CMD-W0` |
| representaciones_fisicas | 672 | archivos de las dos raíces configuradas | `CMD-W0` |
| sha_unicos | 662 | representaciones físicas | `CMD-W0` |
| representaciones_declaradas | 577 | representaciones físicas | `CMD-W0` |
| representaciones_no_declaradas | 95 | representaciones físicas | `CMD-W0` |
| fuera_de_disco | 49 | declaraciones con archivo+sha | `CMD-W0` |
| divergentes_hash_o_tamano | 1 | declaraciones con archivo+sha | `CMD-W0` |
| corruptas_E0 | 0 | representaciones físicas | `CMD-W0` |
| cifradas_E0 | 0 | representaciones físicas | `CMD-W0` |
| no_soportadas_E0 | 0 | representaciones físicas | `CMD-W0` |
| reutilizadas | 0 | representaciones físicas; W0 no abre | `CMD-W0` |
| abiertas_E1 | 0 | representaciones físicas; W0 no abre | `CMD-W0` |
| caracterizadas_E2 | 0 | representaciones físicas; W0 no abre | `CMD-W0` |
| excepciones_de_apertura | 0 | representaciones físicas; W0 no abre | `CMD-W0` |
| objetos_logicos | 0 | objetos enumerados; W0 no abre | `CMD-W0` |
| reportes | 0 | registros E2; W0 no abre | `CMD-W0` |
| ola_W1 | 26 | representaciones físicas | `CMD-W0` |
| ola_W2 | 246 | representaciones físicas | `CMD-W0` |
| ola_W3 | 399 | representaciones físicas | `CMD-W0` |
| ola_W4 | 1 | representaciones físicas | `CMD-W0` |
| ola_W5_reintentos | 0 | referencias a representaciones ya asignadas | `CMD-W0` |

Comando `CMD-W0`:

```sh
unshare -Urn -- python3 tools/curador_registro/snapshot_universe.py \
  --barrido2 --manifest data/manifiesto.yaml \
  --roots-config data/raices.local.yaml \
  --snapshot-output .barrido2/private/t0/snapshot.json
```

La partición inicial es disjunta y exhaustiva:
W1∪W2∪W3∪W4=universo físico; W5 permanece vacío en W0.
