# ACTO GEN2-SIN-CANDIDATO-RUTAS-1 · cierre

**Resultado:** NC-0256 queda convertido en un mapa accionable de 153 slots y dos paquetes siguientes concretos. No se lanzó ninguno, no se tocó la cola y no se redefinió MEDICION-DEMANDA-3.

**Base:** `origin/main = 9dffd6455c67e2ca99740e79f90be59a13f250e1`.

**Rama:** `acto/gen2-sin-candidato-rutas-1`.

**Worktree:** `/home/pc0/mm-gen2-sin-candidato-rutas-1`.
**Entorno:** repo-only; no corpus, microdato, adquisición, correo ni llamada experimental.

## 1 · Decisión de producción

No existe hoy un paquete `LANZABLE-SIN-DECISION-NUEVA` que sea independiente de los encargos vivos:

- **101 `ESPERA-MERGE`:** 79 dependen de las piezas que conserva Opus (piloto/celda-D, crosswalk, corte de edad y D-θ por celda) y 22 del remanente reservado de MEDICION-DEMANDA-3.
- **16 `YA-DECIDIDO`:** 9 ASIGNADOS retirados por precedencia del MEDIDO; 7 coeficientes con fuentes localizadas cuya formalización F-11 difiere expresamente. No son corridas pendientes.
- **36 `DECISION-REQUERIDA`:** 34 slots requieren fijar estimando/consumidor y 2 requieren decidir la solicitud del diseño oficial ENNViH.

Los dos paquetes propuestos son:

1. `P01-ENCIG2023-CORRESPONDENCIA`: separar familia A sin oferta de familia B medida por canal y decidir si el consumidor B se parte o recibe un RESULT agregado nuevo.
2. `P02-ENNVIH-DISENO`: ampliar el expediente oficial ya listo para obtener pesos replicados/servicio de varianza para `RES-0029/0030` y `G3.horizonte_temporal`, y después congelar/ejecutar la spec en CAJA.

No hay tercera ficha: cualquier paquete de marcador antes del resultado del piloto decidiría por adelantado el estimador o fabricaría una interfaz general prohibida por el encargo.

## 2 · Derivación y reconciliación

Comando de entrada, una sola vez por ejecución del productor:

```text
python3 tools/relevo_usos.py --json
```

Resultado vivo: `207` filas, `153 SIN-CANDIDATO`. Por tipo reproduce exactamente `28 L; 14 R; 14 M; 14 AGREGADO; 22 momento; 13 asignado_probabilidad; 12 condicional_theta; 10 conducta_p_asignado; 8 coeficiente_asignado; 7 coeficiente_ejecutable; 6 corte_pi; 3 celda_D; 2 conducta_p_medido`.

**Corrección material:** esos mismos conteos suman **70 M/R/L/AGREGADO**, no 84. El `153` total no cambia. El resumen usa 70 y separa 20 componentes de las cuatro celdas reservadas a MEDICION-DEMANDA-3 de los 50 que esperan piloto/crosswalk.

Clasificación principal:

```text
RESERVADO-O-YA-ENCARGADO       117
DECISION-O-ESTIMANDO-PENDIENTE  34
DATO-O-DOCUMENTACION-FALTANTE     2
TOTAL                           153
```

Control de correspondencia: `RES-0100` consume `CIV-M-02:R`, pero el canal C3 observa `CALC-R-CIV-M-01` y no fija RESULT. Se conserva como correspondencia no acreditada; no se adopta por nombre. La misma regla protege los seis casos desplazados del marcador.

## 3 · Producto

- `forense/produccion/sin-candidato-rutas-1/rutas.tsv`: 153 filas, consumidor exacto, razón viva, causa, dependencia, siguiente acción y compuerta.
- `forense/produccion/sin-candidato-rutas-1/reconciliacion.json`: conteos mecánicos.
- `forense/produccion/sin-candidato-rutas-1/resumen.md`: decisión de producción, máximo tres páginas.
- Dos fichas ejecutables en el mismo directorio.
- `tools/rutas_sin_candidato.py`: productor con `--output-dir` obligatorio; nunca escribe vistas canónicas.
- `tests/test_rutas_sin_candidato.py`: totalidad/unicidad y guarda contra el RESULT homónimo/desplazado.

El encargo externo quedó archivado verbatim con cabeceras de procedencia/consumo fuera del bloque original; la comparación del bloque da `MATCH True` contra SHA-256 `5d538aea9669b7ce02a3ac327a86d657800df76174e68a6d9b59763d3ab8a8d4`.

## 4 · Comprobaciones

```text
python3 tools/rutas_sin_candidato.py --output-dir forense/produccion/sin-candidato-rutas-1
→ {"filas": 153, ...}

python3 -m pytest -q tests/test_rutas_sin_candidato.py
→ 2 passed

git diff --check
→ sin salida

python3 tests/check.py --baseline
→ 3 FAIL · 4351 WARN; LÍNEA BASE VERDE, nada nuevo frente a tests/baseline.json
```

Los tres FAIL heredados son `T06×2` y `T08`; ninguno toca este perímetro. La incorporación final de `origin/main` se registra en `## CONSUMIDO`.

## 5 · Reservas

- No se inspeccionaron capturas/resultados nuevos del piloto ni desenlaces de F6.
- No se leyó/derivó ENIF 2024 localidad × edad.
- No se ejecutó `--escribe`, emisión, medición, cron, `/tramite`, `/despacha`, `/deriva` ni escritor de registro.
- No se editaron `milpa/`, theta, motor, contratos, medidores ajenos, fuentes leídas, decisiones, NC, firmas, canon, índices, tableros, colas, manifiesto, rutinas, contadores o baseline.
- Un PR listo será propuesta; no equivale a integración, adopción o despliegue. La fusión queda con Jonás.

## CONSUMIDO

PR [#828](https://github.com/Josanoforo/Modelado-Mexicano/pull/828), abierto contra `main` el 16/sep/2026 y **no fusionado por el ejecutor**. El merge queda con Jonás.

Antes del push final se ejecutó `git fetch origin --prune`: `origin/main` permaneció en `9dffd6455c67e2ca99740e79f90be59a13f250e1` (`HEAD...origin/main = 1 0` después del primer commit), por lo que no había commit remoto que incorporar. Rama publicada sin force.

El PR lleva la leyenda requerida `CIERRE COMPARTIDO DIFERIDO — integrar después de CAREO/TRÁMITE-4`. Propagaciones compartidas necesarias: ninguna desde este PR; las dos fichas requieren decisión/acto propios y no reservan números ni modifican registros.
