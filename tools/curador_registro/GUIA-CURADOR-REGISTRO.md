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
