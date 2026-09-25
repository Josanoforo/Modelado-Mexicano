---
title: "Sellado y verificación"
---

# 7/10 · Sellado y verificación

[Deck]({{ '/deck.html' | relative_url }}) · [Portada]({{ '/' | relative_url }})

- Cada RESULT tiene su CALC: `spec.yaml`, `resultados.json`, `sello.json` con hash — verificable con `sha256sum` sin abrir microdato.
- 344 sellos en el manifiesto externo, con testigo de tiempo: OpenTimestamps o TSA cuando hay egress; firma GPG del merge y tag de mesa cuando la sesión no tuvo salida a red — demuestra existencia-antes-de, no autoría.
- La validación independiente recalcula desde la spec humana, el cuestionario y el descriptor, sin leer el código que produjo la cifra, y commitea sus números antes de abrir los sellados.

[← anterior]({{ '/deck/06-donde-ganan-los-otros.html' | relative_url }}) · [siguiente →]({{ '/deck/08-reto-publico.html' | relative_url }})
