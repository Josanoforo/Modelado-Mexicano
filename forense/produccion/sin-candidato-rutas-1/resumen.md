# GEN2-SIN-CANDIDATO-RUTAS-1 · decisión de producción

**Corte:** `origin/main = 9dffd6455c67e2ca99740e79f90be59a13f250e1`, 16/sep/2026.  
**Derivación:** `python3 tools/relevo_usos.py --json`, sin `--escribe`.  
**Universo:** 153 slots `SIN-CANDIDATO`, sin duplicados ni omisiones.

## Qué puede producirse ahora

No hay un paquete `LANZABLE-SIN-DECISION-NUEVA` que no invada un trabajo vivo o contradiga una firma vigente. Eso no significa que los 153 sean 153 mediciones:

| salida operativa | slots | lectura |
|---|---:|---|
| **Ya decididos; no medir** | 16 | 9 ASIGNADOS retirados por precedencia del MEDIDO y 7 coeficientes cuya formalización F-11 difiere expresamente hasta demanda material. La vista sigue diciendo `SIN-CANDIDATO`, pero abrir una corrida sería repetir o contradecir la decisión. |
| **Espera a Opus/piloto** | 79 | 50 componentes del marcador fuera de las cuatro celdas reservadas, 6 cortes, 3 celdas-D, 8 momentos de ajuste y 12 condicionales θ. El gate no es “cargar θ entera”: es adjudicar estimador/ruta/dato por celda y consumir crosswalk/corte de edad firmados. |
| **Espera a MEDICION-DEMANDA-3** | 22 | 2 slots de `CORR-0004` y 20 componentes de `DIN-M-01`, `FAM-M-01`, `TRA-M-02`, `TRA-M-03`. No se renombran ni se re-especifican aquí. |
| **Necesita decisión de estimando** | 34 | 4 ENCIG 2023, 16 priors todavía sin MEDIDO de la misma regla y 14 momentos HOLDOUT cuyo instrumento/universo sigue `POR DECLARAR`. |
| **Necesita documento/dato exacto** | 2 | `RES-0029/0030`: payload ENNViH existe; faltan pesos replicados o servicio oficial de varianza. |

La suma es 153. Las causas principales del TSV son, por diseño, la acción que gobierna hoy: `RESERVADO-O-YA-ENCARGADO=117`, `DECISION-O-ESTIMANDO-PENDIENTE=34`, `DATO-O-DOCUMENTACION-FALTANTE=2`.

## Corrección material del corte

El encargo enumera correctamente los tipos, pero su frase “84 M/R/L/agregado” no concilia con esos mismos conteos. El universo vivo contiene **70**, no 84: `R=14 + M=14 + L=28 + AGREGADO=14`. El total 153 sí reproduce. La diferencia cambia la lectura de prioridad: son 70 salidas computadas del marcador, no 84 encuestas ni 84 fuentes faltantes.

De esos 70, 20 pertenecen a las cuatro celdas sin B reservadas a MEDICION-DEMANDA-3 y 50 esperan el piloto/crosswalk. En seis slots el derivador observa un `CALC-R-*`, pero la declaración cae sobre la corrida/celda contigua y no fija `RESULT`; se conserva como hueco de correspondencia, no como oferta adoptable. El caso de control es `RES-0100`: consumidor `CIV-M-02:R`, pero el canal C3 observa `CALC-R-CIV-M-01` y ningún RESULT.

## Paquetes siguientes

Sólo dos paquetes son suficientemente concretos y distintos de los trabajos vivos:

1. **P01 · ENCIG 2023, correspondencia de consumidor — `DECISION-REQUERIDA`.** Separa `RES-0007/0008`, para los que existe medición por canal, de `RES-0001/0002`, que la propia spec declara fuera de cobertura. La decisión es si el consumidor único se parte por canal o recibe un nuevo estimando agregado; no se elige un canal por parecido.
2. **P02 · ENNViH, diseño oficial — `DECISION-REQUERIDA`.** Amplía el expediente ya listo para pedir, en el mismo contacto, pesos replicados o servicio oficial de varianza para `RES-0029/0030` y `G3.horizonte_temporal`; después congela y ejecuta la spec en CAJA.

No se fabrica un tercer paquete “post-piloto”: el resultado del piloto decide qué celda y qué estimador siguen. Nombrar ahora una interfaz general, un ensamble E o 50 adopciones anticiparía precisamente la decisión que Opus conserva.

## Cómo leer el TSV

`rutas.tsv` conserva el identificador y consumidor exactos, la razón viva de `relevo_usos`, el CALC/RESULT observado, una causa principal, subcausa, dependencia compartida, disponibilidad, siguiente acción, compuerta y paquete. `reconciliacion.json` vuelve mecánicos los conteos. Ningún `RESULT` se infiere por nombre y ningún valor legacy se presenta como GEN2.

## Reservas

- No se abrió microdato, no se adquirió documentación, no se llamó a modelos y no se inspeccionaron resultados nuevos del piloto/F6.
- Los 12 `CANDIDATO-GEN2` no pertenecen a este universo ni se tocaron.
- Las fichas son propuestas: no lanzan, firman, adoptan ni modifican cola/canon/registro.
