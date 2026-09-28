# Contrato de salida v3 · PROPUESTO-POR-EJECUTOR

**Fuente:** encargo `ASTRA6-C1-EJECUTOR-AISLADO-3`, P4, sobre el contrato v2 de #1221 y los residuales documentales v2 de #1229. Este archivo fija la versión antes de cualquier recálculo real posterior. Su objeto es una salida comparable por paquete, sin números de referencia, diagnósticos ni código. La aprobación de contenido y el acceso a cada cohorte se deciden por separado.

## Documento único

JSON UTF-8 con exactamente `version`, `identidad` y `filas`. `version` es el entero `3`. `identidad` tiene exactamente `paquete`, `version_entrada` y `sha256_entrada`: strings no vacíos; SHA-256 hexadecimal minúsculo de 64 caracteres. `filas` es una lista no vacía con llaves únicas. La comparación debe exigir la misma identidad, llaves y unidades literales que su referencia; ni esta spec ni `contract.py` abren referencias.

Cada fila tiene `llave`, `unidad`, `estado`, opcionalmente `estado_ic`, `motivo`, `motivo_ic`, y como máximo un alias por campo numérico. Alias permitidos, idénticos a v2:

| Campo | Alias admitidos |
|---|---|
| `punto` | `punto`, `valor`, `p`, `estimacion`, `proporcion` |
| `ic95_inf` | `ic95_inf`, `ic_025`, `ic95_inferior`, `ic_inferior` |
| `ic95_sup` | `ic95_sup`, `ic_975`, `ic95_superior`, `ic_superior` |

Un número es un JSON number finito o un string decimal estricto; no booleano, NaN ni infinito. El lector estricto de JSON rechaza nombres duplicados. La normalización solo cambia nombres; conserva los valores, lexemas decimales y mapa de alias. No redondea, reescala, rellena ni altera tolerancias. Ausente, `null` y cero son distintos. Los archivos originales y la derivada se congelan antes de abrir referencia; `contract.py` valida el objeto y no sustituye el sello/exportación del ejecutor.

## Estados de fila e IC

| `estado` | Requisito | Interpretación |
|---|---|---|
| `RECONSTRUIDO` | `punto` numérico y `estado_ic` explícito | Hay estimación puntual útil. |
| `NO-EVALUADO` | Sin campos numéricos | No se intentó o completó esa fila. |
| `NO-RECALCULABLE-DESDE-SPEC` | Sin campos numéricos; `motivo` | La spec humana no basta. |
| `BLOQUEADO-POR-ACCESO` | Sin campos numéricos; `motivo` | Falta acceso autorizado. |
| `DENOMINADOR-CERO` | Sin campos numéricos; `motivo` | Spec suficiente; dominio observado con denominador cero. |
| `NO-ESTIMABLE` | Sin campos numéricos; `motivo` | Otra condición observada de no estimabilidad, descrita sin fingir insuficiencia de spec. |

Para `RECONSTRUIDO`, `estado_ic=CALCULADO` exige ambos extremos numéricos y ordenados; `SIN-IC` exige extremos ausentes y significa que no se declara un IC; `NO-IDENTIFICADA` exige extremos ausentes y `motivo_ic` no vacío, manteniendo el punto. Un bloqueo de inferencia se representa con `NO-IDENTIFICADA` y su causa concreta en `motivo_ic`. Para filas sin punto, `estado_ic` puede omitirse o ser `SIN-IC`; no se admiten `CALCULADO` ni `NO-IDENTIFICADA`. Ninguna fila sin punto admite `punto:null` ni extremos `null`: se omiten. No se deduce causa desde un `null`.

Ejemplos sintéticos, cada fila dentro del mismo documento:

```json
{
  "version": 3,
  "identidad": {"paquete": "SINTETICO", "version_entrada": "residuales-documentales-v2", "sha256_entrada": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"},
  "filas": [
    {"llave": "a", "unidad": "proporcion", "estado": "RECONSTRUIDO", "punto": "0.25", "estado_ic": "CALCULADO", "ic95_inf": "0.20", "ic95_sup": "0.30"},
    {"llave": "b", "unidad": "proporcion", "estado": "DENOMINADOR-CERO", "motivo": "dominio vacío observado bajo spec suficiente"},
    {"llave": "c", "unidad": "proporcion", "estado": "RECONSTRUIDO", "punto": "0.25", "estado_ic": "NO-IDENTIFICADA", "motivo_ic": "varianza no identificada"}
  ]
}
```

## Mapa conservador v2 → v3

`from_v2(document)` usa primero el adaptador v2 inalterado y solo después cambia `version:2` a `version:3`. Preserva identidad, orden de filas, estados v2, valores, unidades, motivos y el mapa de alias originales. `RECONSTRUIDO` con `CALCULADO` o `SIN-IC` explícitos conserva esos estados. `NO-EVALUADO`, `NO-RECALCULABLE-DESDE-SPEC` y `BLOQUEADO-POR-ACCESO` se conservan, con `motivo` requerido para los dos últimos. El mapa nunca convierte automáticamente `SIN-IC` en `NO-IDENTIFICADA`, ni un estado v2 en `DENOMINADOR-CERO` o `NO-ESTIMABLE`.

Se rechaza la conversión si un `RECONSTRUIDO` v2 no declaró `estado_ic`, si los extremos son `null`, si una fila sin estimación trae un campo numérico incluso `null`, si se declara IC en una fila sin punto o si falta motivo donde v3 lo exige. Son ambigüedades de interpretación; la sesión productora debe emitir v3 directamente con la causa observada. Una salida v2 que ya dice la verdad se reutiliza sin reclasificarla.

**Delta de integración:** el orquestador valida el JSON original con `read_json` estricto de v2 y `validate`, congela original, derivada, código, diagnóstico, contrato y tolerancias con hashes externos antes de revelar referencias. Solo los campos `punto`, `ic95_inf`, `ic95_sup` numéricos se comparan con las tolerancias v2 existentes; los estados de ausencia y de IC se comparan literalmente. Los diagnósticos extensos se exportan como artefactos propios, fuera de `filas`. Un `COINCIDE` responde coincidencia numérica, nunca validez del estimando, adopción ni autorización.

Prueba dirigida: `python3 -m unittest -q tools/validacion/astra6_ejecutor_v3/test_contract.py`. Usa cifras sintéticas y los cuatro formatos de alias de las cohortes ENBIARE, ENCODAT, ENCUCI y ENIGH. No abre microdatos ni resultados históricos.
