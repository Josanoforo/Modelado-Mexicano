# Recibo para mesa · ASTRA-2 primer diseño

- Necesidad: `RES-0087`; consumidor exacto
  `milpa/procedencia.yaml:asignados_probabilidad:salud.atencion.leve_sin_imss`
  (`asignados_probabilidad[5]`). Regla R4.1, canon §3.4.
- Diseño congelado: `forense/prereg-caja/ASTRA-THETA-SALUD-OFERTA-spec-v1_0.md`,
  commit `c529cdf0`. Sorteo inicial de 74 pares de conglomerados; 50
  seguidos en 2005–06, selección de pares a auditar; ITT en pp del evento
  conjunto de consulta respiratoria en farmacia. Esto no es el vector
  condicional θ.
- Fuente adquirida: PR #1037, commit `37cfd059`, Harvard Dataverse
  DOI `10.7910/DVN/P6NC0M`; seis ids `astra_sp_rct_*` verificados por
  `tests/manifiesto.py`. Hash de `ALL.tab`:
  `79697720d54aa497156d49ad8f7ff86e10dc466abcbb4fc6866dfe41c3755788`.
- Diagnóstico reproducible: `diagnostico-salud-oferta.json`, script
  `tools/astra/theta/diagnostico_salud.py`; solo encabezados/hashes,
  647 columnas en `ALL.tab`, faltan cuatro preguntas del desenlace y
  dos códigos de seguro preregistrados. `estado=NO-ESTIMABLE`.
- `RESULT` y `CALC` numéricos: **no existen**. Sin estimación, IC,
  replay ni sello; `cuenta_gen2: NO`, `adopta: NO`. Estado del diseño:
  **NO-ESTIMABLE**; sin propuesta de `ARGUMENTO_EXPLICITO` ni cambio de E1.
- Decisión concreta: obtener tablas originales de visitas e individuo,
  llaves y términos de uso enumerados en `solicitud-adquisicion.tsv`; o
  autorizar nuevo estimando reducido de uso ambulatorio total, sin
  cargarlo en `RES-0087`. Mesa debe firmar cualquier nuevo enlace θ.

No se fusiona ni se instala un valor por este recibo.
