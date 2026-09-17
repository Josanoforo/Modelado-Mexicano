# GEN2-RELEVO-ENCUCI-F2-1 · nota de ejecución

## Metadatos de procedencia y consumo

- Encargo recibido como `ENCARGO-GEN2-RELEVO-ENCUCI-F2-1.md` y archivado
  verbatim en este directorio.
- SHA-256 del original y de la copia archivada:
  `0d24e50ef143694d8b1d5774a54af29a63ca174bb8640cfb88bd12432047a110`.
- Ejecución iniciada el 16/sep/2026 en
  `acto/gen2-relevo-encuci-f2-1`, desde `origin/main @ 4273a3a`.
- La autoridad consumida es la firma exacta F-1/F-2 de
  `forense/encargos/2026-09-15-GEN2-FIRMAS-MESA-2.md`; no se creó una firma,
  decisión ni corrida nueva.

## Producto y comprobación material

El escritor vuelve a leer en cada derivación el consumidor exacto
`RES-0005`: su valor vigente es `0.126006` y cita
`RESULT-ENCUCI-A-P-CUALQUIERA` como GEN2. El RESULT cubierto por el sello de
`CALC-ENCUCI-0001--18d21cdff449` vale `0.12600561008991654`; el verificador
existente devuelve `COINCIDE` para el sidecar y todos los artefactos cubiertos.
El RESULT de la vista de recibo concuerda exactamente con `resultados.json`.

La diferencia absoluta es `3.8991008347033507e-07`. F-1 no la decide por ser
menor que `1e-6`: `_compara_adopcion` redondea el RESULT al grano que el valor
vigente materializa, seis decimales, y obtiene `0.126006`. Por eso F-2 queda
efectiva como `SUPERADO-POR-F2`. La vista conserva por separado el veredicto
sellado histórico `NO-ADOPTABLE-POR-DISCREPANCIA` y su referencia original.
No cambian la cifra, la cita, milpa ni ningún artefacto sellado.

Si en una derivación futura el valor vigente deja de coincidir al grano, la
misma compuerta emite `CITA-PENDIENTE-DE-RETIRO-POR-F2`; si falta identidad,
firma, sello, valor o grano, emite `NO-ACREDITADO-POR-F2` con causa. Ninguno de
esos estados se promueve automáticamente a `YA-ADOPTADO`.

## Comparación estructurada de la vista

La base se guardó antes de editar en `/tmp/relevo-encuci-f2-base.json` y
`/tmp/relevo-usos-v1_0.antes.tsv`. Frente a esa misma base:

- permanecen 207 filas;
- el esquema pasa de 32 a 33 columnas por el campo estrecho
  `resolucion_vigente`;
- las otras 206 filas tienen valor neutral vacío en el campo nuevo;
- sólo `RES-0005` cambia contenido preexistente (`razon`) y recibe
  `resolucion_vigente=SUPERADO-POR-F2`;
- F-3/`RES-0035` conserva su salida y su campo nuevo queda neutral.

## Estados y cierre administrativo

- **PREPARADO:** el encargo archivado autoriza el perímetro.
- **EJECUTADO:** escritor, regresiones y vista canónica están actualizados.
- **SELLADO:** se comprobó el sello histórico de CALC-ENCUCI-0001; esta
  resolución derivada no se rotula como sellada.
- **INTEGRADO:** pendiente de revisión y fusión por Jonás.
- **ADOPTADO:** la cita GEN2 ya existía y permanece intacta; este acto no
  adopta una cifra nueva.

## CIERRE COMPARTIDO DIFERIDO

Después de la integración y del trámite serial de Opus, queda únicamente
consumir F-2/NC-0217 en los registros administrativos diferidos y reflejar su
cierre. No hay parche de retiro, cambio de cita ni cambio numérico que aplicar
en milpa para el estado vigente comprobado.
