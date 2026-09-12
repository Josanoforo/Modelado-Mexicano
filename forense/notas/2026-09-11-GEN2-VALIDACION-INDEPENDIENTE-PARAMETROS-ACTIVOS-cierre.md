# Cierre · GEN2 · validación independiente de parámetros activos

## Veredicto

El acto termina **16/16 PASA**. Los 16 `RESULT` directos del snapshot efectivo
posterior a #720 fueron recalculados desde cinco payloads originales mediante
una implementación separada. Los puntos, n y cantidades declaradas concuerdan;
no hay discrepancias que proteger ni correctivos sucesores que abrir.

La concordancia es numérica y de contrato del estimando. La inferencia de
diseño permanece `NO-COMPROBADA`; no se compararon EE/IC, no existe una muestra
nueva y el contador científico no aumenta.

## Cadena cerrada

| eslabón | evidencia |
|---|---|
| encargo | `forense/encargos/2026-09-11-GEN2-VALIDACION-INDEPENDIENTE-PARAMETROS-ACTIVOS.md`, SHA de redacción `93658acb3a58bc02ed2834c7ef1b7ff8686a5b6e1f92bf1b19542a0c49248321` |
| protocolo e implementación | `forense/validaciones/GEN2-VALIDACION-INDEPENDIENTE-PARAMETROS-ACTIVOS-v1_0/{protocolo-parametros-activos.md,valida_parametros_activos.py}`, protocolo fijado en commit `323b403` |
| evidencia | `evidencia-parametros-activos.json` SHA-256 `2c9669f134db034f54c422a114bb8368f55bba7e44e19c0c482ffa172f3e491f`; `resumen-parametros-activos.tsv` SHA-256 `a90512df3dd209adcaf3990bc3b601c6e0d127b00707ce42f67f46d280f4a8da` |
| informe | `forense/validaciones/GEN2-VALIDACION-INDEPENDIENTE-PARAMETROS-ACTIVOS-v1_0/informe-parametros-activos.md` |
| registro | 16 filas nuevas en `data/corrida0/validaciones-independientes.tsv`; 16 proyecciones `PASA` en `data/corrida0/resultados.tsv` |
| consumo | `forense/prereg-duelo-v2/snapshot-M-gen2-explicito-v1_2.json`, SHA-256 `2279aaafb4c98b7643780d6a362b5e1802f5c77922781973a9a06eb86cb31c7c`; verificación exacta: 16 directas, 16 `EMITE`, 16 `PASA`, 16 identidades únicas |
| gobierno | `ADR-483`, anotación L0 y rótulo GEN2; ninguna obligación `NC` o firma existente correspondía a este objeto |

## Comprobaciones ejecutadas

```text
python3 forense/validaciones/GEN2-VALIDACION-INDEPENDIENTE-PARAMETROS-ACTIVOS-v1_0/valida_parametros_activos.py --write
  -> 16/16 PASA; max_abs_delta=4.789432163088136e-07
  -> segunda ejecución: hashes idénticos

python3 -m tools.snapshot_motor_gen2 --verifica \
  forense/prereg-duelo-v2/snapshot-M-gen2-explicito-v1_2.json
  -> OK snapshot reproducible
  -> directas=16; EMITE=16; PASA=16; resultado_unico=16
```

Las pruebas dirigidas y el gate general se registran en el PR. Los snapshots
históricos permanecen intactos: v1.0 conserva
`05350667baa245c79c3ed487aeb1403d74b4612fcae69e16845b8d42f1a5eaa8` y v1.1
conserva `95d36cef4735f85a22f0346bc04dabdab2f13724c96e9a19179996cb93bca3bb`.
La deriva viva queda representada en v1.2, no neutralizada ni retroescrita.

## Residuales y límites

- Diseño muestral, EE e IC no fueron objeto de esta validación.
- El `PASA` no cambia roles retenidos, comparabilidad temporal, aptitud causal o
  decisiones de adopción.
- La rederivación integral revela una publicación F5 pendiente en las vistas,
  originada por trabajo ya fusionado y fuera de este perímetro. Este acto no la
  incorpora ni oculta: proyecta sólo sus 16 asientos con el mecanismo canónico.
- No se enviaron mensajes, formularios ni compromisos externos; no hubo compra,
  descarga nueva ni llamada a modelos.

**Contador científico: cero.** Los 16 son `RESULT` validados, no 16 muestras ni
16 mediciones nuevas.
