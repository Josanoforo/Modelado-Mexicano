# FP-373 · ejecución documental v1.0

Este directorio conserva únicamente el contrato, manifiesto, plan, sobres de
captura y resultados públicos de `GEN2-F5-DOCUMENTAL-EJECUCION`. Los payloads
fuente y sus serializaciones viven fuera de Git.

Estado inicial: **PREPARADO; PENDIENTE DE FIRMA; CERO LLAMADAS**.

## Transporte congelable

- Proveedor/competidor observado en la última F5: Anthropic `firstParty`,
  `claude-opus-5`; el ejecutable pide ese identificador completo, no `opus`.
- Cliente observado e instalado al preparar: Claude Code `2.1.267`, sesión
  `claude.ai` Max. No se equipara `modelUsage.costUSD` con un cargo real.
- Cada brazo tiene un root físico distinto. El root control contiene únicamente
  `contextual.txt`; no contiene ni enlaza la tabla o documentos dirigidos.
- Entrada por `stdin`; documentos PDF convertidos mecánicamente a texto completo;
  tabla de campos declarados accesible sólo mediante
  `mcp__f5docs__weighted_distribution`.
- El CLI corre desde el directorio aislado de la celda con `--restricted`, sin
  web, sin persistencia, sin herramientas generales, sin sugerencias de prompt y
  con máximo dos turnos. El mismo conjunto de capacidades se ofrece a ambos
  brazos.
- La sonda posterior a la firma debe acreditar un único modelo reportado, el
  marcador al final del paquete mayor y lectura completa de la tabla. Cuenta
  contra el techo global.

La F5 anterior reportó exactamente dos entradas de `modelUsage` en sus 224
capturas: Opus y un Haiku auxiliar. Por eso no se hereda el contador por
invocación. Este ejecutable desactiva sugerencias y carga cada proceso con el
número de turnos reportado; ante un sobre ilegible carga conservadoramente dos.
Antes de cada proceso reserva dos solicitudes y para si el total podría superar
96.

## Secuencia

```bash
python3 tools/f5_documental.py --prepare
python3 tools/f5_documental.py --verify
```

Esos dos comandos son locales y no llaman al proveedor. Después de archivar la
firma explícita en el repositorio:

```bash
python3 tools/f5_documental.py --freeze-plan --authorization-file RUTA_FIRMA
python3 tools/f5_documental.py --transport-probe --authorization-file RUTA_FIRMA
python3 tools/f5_documental.py --run --authorization-file RUTA_FIRMA
python3 tools/f5_documental.py --summary
```

No se congela plan ni se llama sin un archivo vivo de autorización, fuera de
`forense/encargos/cola/`, con marcador explícito `FIRMA DE JONÁS` o `FIRMA DE
MESA`, cuyo texto fija
FP-373, 32 posiciones, máximo 96 solicitudes y la exclusión de FP-374/F6. Una
firma de alcance distinto exige ajustar explícitamente el verificador; nunca se
interpreta por aproximación.

## Materialización DIN

Se verifican los cinco IDs del manifiesto. Book 3B usa el cuestionario y
codebook completos, el diseño muestral completo y una serialización TSV que une
uno-a-uno `iiib_cr.dta` con `ehh02w_b3b.dta` por `folio+ls`, conservando todas
las filas CR y sólo `folio`, `ls`, `cr27`, `fac_3b`. No filtra, tabula ni calcula
el objetivo.

El codebook PDF imprime `NS=8`, mientras el `.dta` transportado contiene el
código 7 para esa categoría no válida. La diferencia no altera el estimando:
se aceptan exclusivamente `1=Sí` y `3=No`; tanto 7 como 8 quedan fuera.

El ZIP histórico del cuestionario usa Deflate64, no soportado por `zipfile` de
este entorno. El miembro oficial `ehh02q_b3b.pdf` se recuperó desde la URL
directa del mismo proveedor y se aceptó sólo después de igualar tamaño y CRC32
con el miembro del ZIP registrado.

## Materialización TRA

Se verifican los tres IDs del manifiesto. Se extrae texto completo del
cuestionario y estructura ENCIG 2021; del miembro
`encig2021_01_sec1_A_3_4_5_8_9_10.csv` se conservan todas las filas y sólo
`ID_PER`, `ID_VIV`, `P8_3_1`, `FAC_P18`, `EST_DIS`, `UPM_DIS`. No se filtra,
tabula ni calcula el objetivo.

Las 32 derivaciones deben revisarse contra esos documentos antes del veredicto.
Un `PUNTO` automático sin sustitución es sólo candidato trazable, no éxito ya
adjudicado.
