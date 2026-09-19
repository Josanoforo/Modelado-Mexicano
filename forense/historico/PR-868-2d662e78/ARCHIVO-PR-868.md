# Archivo histórico de los pisos de PR #868

Este directorio preserva, dentro del repositorio y fuera de la exploración de
`data/corrida0`, los tres artefactos de pisos que PR #868 tenía en el commit
`2d662e78b143f9b00a8e2b06fb7ff6cfe0ea15a1`. Una rama remota no se usa como
archivo permanente.

`artefactos-pisos.tar.gz` contiene los directorios completos de ENVIPE `0002`,
ENCIG `0002` y ENIF `0002`, el helper compartido `tools/pisos_ejes.py` que sus
wrappers invocaban y su evidencia de replay. SHA-256 del archivo:
`5640cb318c2f5b6d542a2796e2ab1914d80b984a43e2fdce39029827b1009c92`.

Verificación:

```sh
sha256sum forense/historico/PR-868-2d662e78/artefactos-pisos.tar.gz
tar -tzf forense/historico/PR-868-2d662e78/artefactos-pisos.tar.gz
```

El tar conserva los nombres que colisionan para auditoría; no los publica como
CALC activos. `mapa-colisiones.tsv` identifica cada homónimo por commit, ruta,
corrida y hashes de contenido. Ningún resultado del archivo es candidato de
integración de PR #871.
