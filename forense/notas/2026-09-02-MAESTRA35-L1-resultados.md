# ACTO MAESTRA35-L1 · RESULTADOS por pieza

Este documento crece un bloque por commit de resultados. **No edita** la spec
congelada (`forense/notas/2026-09-02-MAESTRA35-L1-spec.md`, `e2dbd82`) ni el
censo (`…-P0-censo.md`, `0763c07`). Una sola corrida por celda, sin reintentos.

---

# `P1` · `tramite.mordida.con_registro` recorrida sin deduplicar

**Script:** `tools/recorre_mordida_con_registro_encig25.py` · **spec:** §2 ·
**firma:** mesa 2/sep/2026, `d1` = `FP-238`.
**Payload:** `encig25_base_datos_csv`,
sha256 `47daf2f732366ad842b7f60c784be9d61db68a00ae1a693980ec6a683e0d9e12`.

## §1 · Salida cruda de la única corrida

```
sec_7    : 124,314 filas · ID_TRA distintos 113,717 · (ID_TRA,NT_TIPO) grupos 124,314
sec_8    : 1,083,672 filas · ID_TRA llave unica (guardia 1 OK)
universo : P8_4 in {0,1} = 21,139 filas de sec_8; al grano de EVENTO -> 24,974 en 21,139 ID_TRA
           una deduplicacion por ID_TRA descartaria 3,835 eventos: no se deduplica.

MAPEO principal (MAESTRA34-L1: digital {3,4,5})
  DIGITAL/REGISTRADO · P7_3 in ['3', '4', '5']
    p̂ = 0.029868   IC95 = [0.021133, 0.040452]
    n = 7,219 EVENTOS de tramite (en 6,384 ID_TRA) · con mordida = 242
    estratos = 362 · UPM = 2,518 · poblacion expandida = 29,467,394
  PRESENCIAL · P7_3 in ['1']
    p̂ = 0.141041   IC95 = [0.116817, 0.169579]
    n = 11,167 EVENTOS de tramite (en 9,992 ID_TRA) · con mordida = 1,496
    estratos = 381 · UPM = 2,996 · poblacion expandida = 34,171,657
    RAZON presencial/digital = 4.7222x  (signo: presencial MAYOR)
    IC95 se traslapan: False

MAPEO sensibilidad A (MAESTRA34-L5: digital {4,5}, 3 fuera)
  DIGITAL/REGISTRADO · P7_3 in ['4', '5']
    p̂ = 0.025078   IC95 = [0.015990, 0.036467]
    n = 5,251 EVENTOS de tramite (en 5,040 ID_TRA) · con mordida = 158
    estratos = 357 · UPM = 2,308 · poblacion expandida = 25,821,039
  PRESENCIAL · P7_3 in ['1']
    p̂ = 0.141041   IC95 = [0.116817, 0.169579]
    n = 11,167 EVENTOS de tramite (en 9,992 ID_TRA) · con mordida = 1,496
    estratos = 381 · UPM = 2,996 · poblacion expandida = 34,171,657
    RAZON presencial/digital = 5.6241x  (signo: presencial MAYOR)
    IC95 se traslapan: False
```

## §2 · Antes y después, en la misma escala

| conducta cargada en `milpa/tramite.yaml` | sellada (1/sep) | recorrida (2/sep) | Δ | Δ relativo |
|---|---|---|---|---|
| `paga_mordida_encig2025_digital` | 0.027358 (n 6 337) | **0.029868** (n 7 219) | +0.002510 | +9.2 % |
| `paga_mordida_encig2025_presencial` | 0.116000 (n 9 937) | **0.141041** (n 11 167) | +0.025041 | +21.6 % |
| razón presencial/digital | 4.2401× | **4.7222×** | +0.4821 | +11.4 % |

Las `n` suben porque la deduplicación borraba eventos: 6 337 → 7 219 en el
canal digital y 9 937 → 11 167 en el presencial.

## §3 · Los dos veredictos — y el hueco de la spec

**Canal digital: `CORRECCIÓN SIN CAMBIO MATERIAL`.** La regla congelada en la
spec §2.1, escrita antes de ver el número, decía: si el IC95 nuevo del canal
digital contiene `0.027358`, se reporta así. **Lo contiene**:
`0.027358 ∈ [0.021133, 0.040452]`.

**Canal presencial: `VENCIDA EN ALCANCE — re-sello de mesa`, y se reclama
`FP-241`.** Aquí hay que decir dos cosas y no una:

1. **La spec congelada solo regló el canal digital.** Es un hueco de la spec,
   no un resultado: el `CONTADOR` del propio encargo pone los **dos** canales
   en alcance («cifra sellada corregida +1 (`con_registro`, **dos canales**)»),
   y `milpa/tramite.yaml:139-142` carga las cuatro conductas con `tier: FUERTE`.
   La spec no se edita (COMMIT-1 es intocable); el hueco se dice aquí.
2. **Aplicada al presencial la misma prueba, falla — por poco.**
   `0.116000 ∉ [0.116817, 0.169579]`: queda fuera **por 0.000817** del límite
   inferior. El criterio de pertenencia falla estrechamente; **el movimiento del
   punto no es estrecho**: +0.025041, +21.6 % relativo. Mesa tiene los dos
   números para decidir si el re-sello vale el trámite.

**Contra-hipótesis declarada: NO se cumple, y el hallazgo se refuerza.**
La spec decía que si la razón presencial/digital caía **por debajo de 2×** con
la llave correcta, el hallazgo de `MAESTRA34-L1` («el registro rompe la trampa
social») quedaba **ACOTADO**. Sube de 4.2401× a **4.7222×** (5.6241× en la
sensibilidad A), con IC95 sin traslape en los dos mapeos. **El hallazgo no
queda acotado: queda más grande.**

## §4 · Por qué el número se movió hacia arriba en los dos canales

No es ruido de remuestreo: el universo cambió. Los 3 835 eventos que la
deduplicación borraba no eran una muestra aleatoria del resto — eran **eventos
repetidos del mismo trámite por la misma persona**, y quien repite un trámite
tiene más ocasiones de encontrarse la mordida. Al devolverlos al universo, la
tasa por evento sube en los dos canales. Que suba **más** en el presencial
(+21.6 % vs +9.2 %) es consistente con el mismo mecanismo, pero **no** se
declara aquí como hallazgo: esta pieza recorre, no identifica. Es asociación
dentro de una corrida (A-bis 1), no un efecto (A-bis 2).

## §5 · Lo que este resultado escribió

- **Enmienda in situ** bajo `tramite.mordida.con_registro_encig2025` en
  `milpa/tramite-ola5-propuesta-v0.yaml`, clave `enmienda_maestra35_l1`.
  Verificado: **0 líneas del cuerpo viejo eliminadas o modificadas** (A.10
  corolario 1); el YAML parsea.
- **Filas nuevas** `TRA-M-13b` y `TRA-M-14b` en
  `forense/prereg-duelo-v2/codificacion-R-v1_0.tsv`, con
  `estado: SUSTITUYE-A TRA-M-13` / `SUSTITUYE-A TRA-M-14`. Verificado:
  **0 filas existentes editadas**; 37 filas, todas con 12 campos.
- **`milpa/tramite.yaml` NO se tocó.** El sello es de mesa, en RH.
