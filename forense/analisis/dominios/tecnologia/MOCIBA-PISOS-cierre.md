# MOCIBA-PISOS · cierre descriptivo

Fuente primaria mexicana: MOCIBA 2015–2017, tres contratos de instrumento
distintos documentados en `forense/prereg-caja/MOCIBA-PISOS-spec-v1_0.md`.
Los `RESULT-MOCIBA-PISOS-YYYY-TABLA` están sellados en los CALC homónimos.
`tabla-principal.tsv` enlaza llave de RESULT, CALC y SHA256. Este uso
descriptivo no abre ni convierte a elegible el candidato predictivo F6.

| Ola | Población elegida | Afectados, % [IC95] | Bloqueó entre víctimas, % [IC95] | Denuncia/informe entre víctimas, % [IC95] |
| --- | --- | ---: | ---: | ---: |
| 2015 | 12+ usuario de internet o celular | no estimable: falta estrato publicado | no estimable | no estimable |
| 2016 | 12+ usuario de internet o celular | 16.10 [15.59, 16.54] | 47.56 [46.20, 49.03] | 7.57 [6.76, 8.37], policía u otra autoridad |
| 2017 | 12–59 usuario de internet | 16.91 [16.17, 17.59] | 60.08 [57.52, 62.21] | 5.35 [4.34, 6.36], ministerio/policía/**proveedor** |

Las ventanas son últimos 12 meses en 2015/2016 y junio de 2016 a la
entrevista de 2017. El cambio de 12+ internet **o celular** a 12–59 internet
excluye la comparación directa 2016–2017 como cambio conductual. Además, la
respuesta de denuncia de 2017 incorpora proveedor del servicio: no se llama
denuncia ante autoridad sin ese matiz. 2015 usa 10 situaciones `P3_i`, 2016
`P1_i`, 2017 `P4_01..10`; ninguna de estas tasas tiene denominador de toda
la población mexicana. La acción «bloquear» puede coexistir con denunciar.

2015 conserva el primer RESULT no estimable: `n_tabla=59,800`,
`n_universo=59,582`; `n=59,151` respuestas válidas a la batería,
15,431 con al menos una exposición, 431 NS y 43,720 no, **conteos sin
ponderar**. No se inventó un estrato con UPM. 2016 tiene `n_tabla=91,675`,
410 estratos y 18,521 UPM; 2017, `n_tabla=33,566`, 586 estratos y 17,122
UPM. Los dos años con diseño publicable conservan 399 réplicas agregadas
por total, sin identificadores. Los tres CALC devuelven `verify REPRODUCE`
con `CONTEXTO=IDENTICO`, asentados en `forense/replay-evidencia.tsv`.

Cobertura: **279 celdas** en 3 medidas y 3 olas: 249 `ESTIMABLE`, 30
`NO-ESTIMABLE-SIN-EST_DIS`. El rubro de 2015 se conserva íntegro sin punto
ni IC. Localidad no consta como campo del módulo temprano; no se infiere de
UPM. Entidad está disponible en 2016/2017. Estado temporal:
`SIN-HISTORIA-PARA-CALIBRAR`; no se construyó IC predictivo ni un contraste
de cambio entre olas.

**Auditoría de rigor extremo.** El ciberacoso observado no identifica
motivos, jerarquía social, chisme, envidia, «funa» ni aceptación cultural.
Se mide exposición y respuesta, no una psicología nacional ni causalidad.
La menor cifra de informe a autoridad/proveedor en 2017 no se interpreta
como caída de denuncia respecto de 2016 por las diferencias de universo y
texto. El módulo ENDUTIH anfitrión implica dependencia de muestra donde
coincidan ola y población, no dos muestras independientes.
