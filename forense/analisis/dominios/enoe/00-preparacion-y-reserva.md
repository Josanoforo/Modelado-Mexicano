# ENOE · preparación documental y reserva

Acto ASTRA5-U1-TRABAJO-ENOE · 23/sep/2026. Esta nota precede al COMMIT-1.
No es resultado ni congela la lista de conductas: la matriz reactivo↔ola se
cierra cuando las filas U0 estén selladas.

## Selección por paquete, sin abrir microdato

Se recorrieron las entradas de `data/manifiesto.yaml` por `id`, `archivo`,
descripción y URL. `data/enoe-olas-elegibles-preparacion-v1_0.tsv` recoge 43
paquetes únicos por edición/año/trimestre: 2005T1, 2008T1, 2012T1, 2014T1 y
2016T1–2025T4 con hueco real 2020T2. Para duplicados `/datosabiertos/` y
`/microdatos/` se prefirió el segundo, ruta canónica de ADR-152/FP-110.
SDEM, COE, documentación y formatos duplicados son componentes, no olas.
El hash de cada fila es **declarado en el manifiesto**, pendiente de cotejo
contra disco antes de cada apertura.

## Reserva vigente

El último trimestre en el manifiesto es **2026T1**, con los ids
`enoe_2026_1t_csv` y `enoe_2026_1t_microdatos`. El mandato específico recibido
lo reserva; ninguno de los dos payloads entra en el lote ni se abre. La página
[oficial de ENOE](https://www.inegi.org.mx/programas/enoe/) lista 2026T2 como
último trimestre publicado al 23/sep/2026. Esa ola no figura en el manifiesto;
no se descargó ni se consultaron sus tabulados, comunicado o cifras. La
publicación posterior no levanta la reserva de 2026T1.

## Saltos decididos por documentación

| Periodo | Edición | Decisión |
| --- | --- | --- |
| 2005T1–2020T1 | ENOE clásica | Persona 15+ como universo común; ampliar solo donde el instrumento lo acredita. |
| 2020T2 | ETOE telefónica, ENOE suspendida | No hay ola ENOE elegible; no interpolar. |
| 2020T3–2022T4 | ENOEN | Era separada; `FAC_TRI`/`EST_D_TRI`; no asumir enlace de panel con clásica. |
| 2023T1–2025T4 | Nueva edición con nombre de archivo `enoe` | Era separada hasta documentar equivalencia del estimando por reactivo. |
| 2026T1 | Paquete reservado | Excluido incluso de comprobación de miembros o lectura de valores. |

Fuentes internas: `forense/notas/2026-07-31-cal-enoe-fasea.md`,
`data/barrido-enoe-sonda-eras.tsv`, `data/barrido-enoe-puente-distribucion.tsv`,
ADR-144 y ADR-152. El panel rotatorio de cinco visitas está documentado, pero
el corpus no identifica un ponderador longitudinal de persona; ningún cambio
de formalidad se estimará como transición sin acreditar llave y peso.
