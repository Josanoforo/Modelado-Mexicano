# Curador reusable del registro demanda-universo

Este directorio contiene utilidades generales para validar un baseline semántico
y derivar su cola de candidatas. El baseline es la fuente de verdad; la cola es
una vista reproducible y no debe versionarse.

```bash
python3 tools/curador_registro/baseline.py RUTA_AL_BASELINE
python3 tools/curador_registro/derive_queue.py RUTA_AL_BASELINE --output /tmp/cola.tsv
```

La identidad estable de una relación se construye con la terna
`(necesidad_id, fuente_canonica_normalizada, objeto_evidencia_id_canonico)`.
El validador comprueba hashes, conteos declarados, procedencias, fusiones,
decisiones y la proyección de utilidad sin depender de nombres o cantidades
particulares de una corrida.

## `via_capa2.py` — la vía de `capa2_manifiesto`

```bash
python3 tools/curador_registro/via_capa2.py --root .              # solo lectura (por defecto)
python3 tools/curador_registro/via_capa2.py --root . --escribe    # aplica los diffs propuestos
```

Deriva `capa2_manifiesto` por fila de `relaciones.tsv` contra `data/manifiesto.yaml`
real y reporta el diff propuesto. Solo promueve a `SI` cuando `id_manifiesto`
resuelve a una entrada con payload verificado — nunca por coincidencia de
nombre de fuente. Ver `forense/notas/2026-08-13-v2-via-capa2.md` para la
especificación completa (qué distingue `SI`/`SI_O_REFERENCIADO`/`NO_REFERENCIADO`,
y por qué esta vía no promueve las filas `SI_O_REFERENCIADO` automáticamente).
