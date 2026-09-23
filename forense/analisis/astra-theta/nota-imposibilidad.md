# ASTRA-2 · dictamen del primer diseño

**Veredicto:** `CALC-ASTRA-THETA-SALUD-OFERTA-0001` no estimable con la
réplica pública adquirida. No hay estimación puntual, IC ni RESULT numérico:
el desenlace preregistrado no está en `ALL.tab`. No se atribuye `GEN2`
medido ni `ARGUMENTO_EXPLICITO` a `RES-0087`.

## Secuencia verificable

1. Mapa de 40 consumidores exactos y contraste de trámite, G3 y salud.
   El recibo ENCIG #1034 `1d99b5f0` resolvió acceso, pero `P7_3` es
   elección de canal y el código `05` mezcla trámites. Una ventanilla
   digital se asignaría por **lugar del trámite** `P7_1/P7_2`, no por
   domicilio. Falta calendario de servicio y cobertura para ese DiD.
2. Se eligió la asignación aleatoria de Seguro Popular por 50 pares de
   conglomerados de salud. El consumidor exacto investigado es
   `RES-0087` / `salud.atencion.leve_sin_imss` /
   `asignados_probabilidad[5]`. El mecanismo del canon es costo, tiempo
   y trato en la elección de farmacia o automedicación. La intervención
   junta seguro, mejora de instalación y medicamentos. Se congeló en
   `c529cdf0` un ITT del **evento conjunto** de consulta respiratoria en
   farmacia entre adultos sin IMSS al inicio, en pp, basal 2005 y
   seguimiento 2006. No es la probabilidad condicional del motor.
3. PR de adquisición #1037, commit `37cfd059`: seis archivos del DOI
   `10.7910/DVN/P6NC0M`, id/hash/tamaño por `tests/manifiesto.py`, todos
   `COINCIDE`. El depósito advierte que no informa condiciones de uso y
   recomienda contactar al responsable. Corpus compartido:
   `/home/pc0/mm-corpus/raw/seguro_popular_rct/`.
4. Tras el freeze, el comando de abajo leyó **solo encabezados** y SHA256.
   `ALL.tab` tiene 647 columnas; faltan los cuatro reactivos de razón y
   lugar de consulta preregistrados y dos códigos de seguro basal. El
   script original `Eval/utilization.formerge.R` señala la tabla fuente
   `tbl_seccion11_vis.dta` y `P11D0501`, ausente del depósito. El README
   llama a `ALL.tab` tabla de resultados de la publicación, no encuesta
   exhaustiva. La coincidencia de una variable `P10D04` sería falsa:
   el codebook basal la define como última mamografía. No se abrió ninguna
   fila de desenlace ni se seleccionó otro resultado por disponibilidad.

```
python3 tools/astra/theta/diagnostico_salud.py \
  --root data/raw/seguro_popular_rct \
  --out forense/analisis/astra-theta/diagnostico-salud-oferta.json \
  --selftest
```

Salida decisiva: `hashes_validos=true`, `estado=NO-ESTIMABLE`, faltan
`P11D0401`, `P11D0501`, `P10E0401_T2`, `P10E0501_T2` además de los dos
códigos de seguro inicial. El ensayo sintético confirma que una columna
obligatoria ausente activa el bloqueo. Las reglas del preregistro ordenan
NO-ESTIMABLE ante columna requerida ausente. Preflight/run/verify del
contrato numérico no pueden ejecutarse honestamente: no hay variable Y.

## Insumo y decisión exactos para mesa

Adquirir del equipo de evaluación/DGED-INSP las tablas **originales** de
visitas basal y seguimiento (el código nombra
`tbl_seccion11_vis.dta` para basal), tabla de personas/seguro por
individuo, diccionario de cambio `P11D*` ↔ `P10E*`, y llaves
`id_hogar`, `id_pers`, `conglome`, `matchnum` con términos de uso claros.
Registrar cada objeto en `codex/adq-*` con id/hash/tamaño antes de
reabrir el medidor. Criterio de éxito: las preguntas de motivo y lugar
aparecen en ambas olas, la elegibilidad sin IMSS corresponde al individuo,
y enlazan sin duplicados a los pares sorteados. La petición está en
`solicitud-adquisicion.tsv`.

Si esos microdatos no pueden obtenerse, la alternativa concreta es que
Jonás autorice cambiar el producto a un ITT de **uso ambulatorio total**
en `ALL.tab` mediante preregistro nuevo. Se reportaría solo como efecto
reducido del programa; no cuantifica la elección de farmacia ni el vector
de `RES-0087`. Cambiar el significado o enlace de θ requiere firma de
mesa. No se inventa un coeficiente sustituto.

## Alcance del argumento

El sorteo habría controlado pobreza e informalidad como confusores
basales para un ITT de la oferta, si el desenlace estuviera disponible.
La intervención compuesta no separaría costo, tiempo y trato; una caída
en farmacia no probaría preferencia psicológica. Las seis entidades y
conglomerados participantes no transportan automáticamente a México
rural fuera del ensayo ni al ecosistema de consultorios anexos de 2022.
No se infiere ausencia de efecto de la ausencia de columnas.
