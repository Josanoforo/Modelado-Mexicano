# GEN2-S6-DISENO-Y-ALCANCE-INFERENCIAL · contraste y tabla de impacto

Fecha de contraste: 10 de septiembre de 2026. Objeto: alcance inferencial de
`CALC-0003-v4` sobre ENNViH-1 (2002), sin recalcular ni reescribir la corrida.

| salida vigente | punto observado | IC95 publicado | supuesto que produce el IC y el veredicto histórico | conclusión bajo ese supuesto | conclusión que no depende de acreditarlo |
|---|---:|---:|---|---|---|
| C1/b3b, primaria: grave/serio → hospitalización pública | P(T=0)=84.2475%; P(T=1)=77.6514%; delta=-6.5961 pp | [-19.8439, +7.2787] pp | bootstrap de 118 `id_loc` dentro de las cuatro categorías `c_portad.estrato` | `NO-DISCRIMINA` | asociación puntual descriptiva negativa; no acredita la asociación positiva esperada, pero sin una varianza acreditada no permite concluir significancia ni ausencia de asociación poblacional |
| C3/b3b, secundaria: crónico → hospitalización pública | P(T=0)=66.6969%; P(T=1)=84.8835%; delta=+18.1865 pp | [+1.4702, +35.6366] pp | bootstrap de 111 `id_loc` dentro de las cuatro categorías `c_portad.estrato` | `CORROBORADA`, secundaria | asociación puntual descriptiva positiva de +18.19 pp; que su IC excluya cero no queda acreditado bajo el diseño oficial |
| C4/b3b, secundaria: crónico → consulta pública | P(T=0)=63.8801%; P(T=1)=70.5836%; delta=+6.7035 pp | [+1.2579, +12.0725] pp | bootstrap de 147 `id_loc` dentro de las cuatro categorías `c_portad.estrato` | `CORROBORADA`, secundaria | asociación puntual descriptiva positiva de +6.70 pp; que su IC excluya cero no queda acreditado bajo el diseño oficial |

Los puntos, universos, ponderadores, clasificaciones y joins no son objeto de
esta reserva. Los tres IC y las etiquetas que dependen de excluir o incluir
cero siguen siendo resultados históricos válidos **bajo el contrato que los
produjo**, pero hoy se usan sólo como sensibilidad por localidad, no como EE/IC
del diseño oficial.

## Contraste de diseño

La equivalencia no está acreditada:

- S6 v1.3 §3.5 llama a `id_loc` el conglomerado correcto, levanta la reserva de
  varianza y, en la misma sección, reconoce que la localidad es la mejor
  aproximación disponible porque el microdato no trae una UPM declarada. S6
  v1.4 corrige exclusivamente el join hogar (`folio`) y hereda esa afirmación;
  resolver la cobertura del join no identifica unidades de selección.
- `CALC-0003-v4` verifica una propiedad del archivo: 150 valores de `id_loc`,
  biyección con `(edo, mpio, loc)`, anidamiento dentro de cuatro valores de
  `c_portad.estrato` y cobertura analítica completa. No verifica que esas
  columnas sean UPM y estrato del diseño.
- La nota oficial de diseño de ENNViH-1, `ennvih1_muestra_diseno` (sha256
  `9f90df10338c7749cf46f86edc0664fc300c913e4fc4b1eee5e360d2970e91f0`),
  describe un diseño probabilístico, polietápico, estratificado y por
  conglomerados. Su §4.1.2 clasifica las UPM en tres estratos socioeconómicos
  (alto, medio y bajo); su cuadro 1 registra 180 UPM seleccionadas.
- La documentación de factores, `ennvih3_2009_factores_exp` (sha256
  `cc297561caa5e963fd5a7cd88a8ab0a45726b997015eafbcdac7bcf088fe214d`),
  selecciona UPM dentro de región y estrato y, en ciudades autorrepresentadas,
  selecciona además seis USM por UPM. No identifica `id_loc` como UPM ni las
  cuatro clases de tamaño como estratos de selección.
- La FAQ oficial declara que municipio, localidad y UPM no pueden hacerse
  públicos. El censo ya registrado examinó las cabeceras de 425 `.dta` de las
  tres olas: cero columnas de UPM/conglomerado y un único campo `estrato`, el de
  cuatro tamaños de localidad. No apareció una justificación oficial de la
  sustitución.

La diferencia 150 localidades frente a 180 UPM muestra que las unidades no
pueden darse por idénticas uno-a-uno; por sí sola no cuantifica el sesgo ni
determina si el IC publicado es más ancho o más estrecho que el verdadero. La
estratificación omitida y la conglomeración aproximada pueden actuar en
sentidos opuestos. Las comparaciones v2/v3/v4 son sensibilidades a recetas
distintas, no validaciones del IC real.

## Alcance de R4.4 y decisión para mesa

`R4.4` permanece `[MEDIA]` en `canon/modelo-decision-v4_0.md`; CALC-0003-v4
contó como corrida GEN2, pero no promovió el tier ni fue adoptado al motor. La
fila primaria C1 conserva un punto negativo y no produce evidencia descriptiva
positiva. C3/C4 conservan asociaciones descriptivas positivas, pero son filas
secundarias y su carácter `CORROBORADA` depende del IC aproximado. No se
atribuye a esta reserva un cambio de tier que nunca ocurrió.

Recomendación para la decisión `FP-372`: conservar puntos y asociaciones
descriptivas; mantener los IC por localidad como sensibilidades explícitas;
no promover conclusiones nuevas basadas exclusivamente en que esos IC excluyen
o incluyen cero. Alternativa: no usar ningún EE/IC de S6 inferencialmente hasta
recibir pesos replicados oficiales o un servicio oficial de varianza. Esta
decisión es distinta de `FP-371`: aquella trata constante+`folio` para
DIN-M-01; ninguna firma sobre DIN se extiende a S6.

## Vía oficial y continuidad

No hay hoy diseño público ejecutable. Se reutiliza, sin enviar ni duplicar
expediente, la solicitud preparada en la nota DIN: pedir al productor pesos
replicados con método/escala/grados de libertad o un servicio que devuelva el
EE bajo el diseño, sin solicitar geografía identificable. Si llega una vía
operativa, primero nace una spec sucesora en CAJA y sólo después se calcula un
resultado; no se construye un v5 con otra aproximación para obtener el mismo
veredicto. Falta de respuesta futura significaría `SIN-RESPUESTA`, no
inexistencia mundial.

## Avisos de consumo delimitados

**Ejecutor 12, GEN2-TANDAS-MEDICION-ACADEMICA.** Continúe con puntos
ponderados descriptivos por ola. No herede `c_portad.estrato` + `id_loc` como
diseño acreditado; si publica esa receta, sepárela como sensibilidad sin
dirección garantizada. La reserva de S6 no bloquea el primer punto de tandas ni
cierra la necesidad de datos grupales de turnos/pagos.

**Ejecutor 13, GEN2-F5-APRENDIZAJES-Y-SUCESOR.** Mantenga intactos el snapshot
M, los árbitros R y `CALC-TRIADA-0002`. Esta revisión no retira el punto DIN ni
cambia el veredicto `SIN-GANADOR-UNICO`; al separar incertidumbre del árbitro,
rotule el EE/IC aproximado de DIN según `FP-371` y no use una eventual decisión
de DIN para acreditar los IC de S6. Las abstenciones DIN-M-01/TRA-M-07 siguen
siendo cobertura documental, no evidencia contra los puntos de S6.

## Integración propuesta, no aplicada a vistas globales

Para la entrada `salud.atencion.grave_ennvih2002` de
`milpa/tramite-ola5-propuesta-v0.yaml`, el acto dueño de esa ruta debe añadir
una enmienda fechada que cite esta nota y `S6-L16-spec-v1_5.md`, preserve el
`veredicto_Bbis` histórico, y rotule C1/C3/C4 como
`IC-SENSIBILIDAD-LOCALIDAD-NO-DISENO-OFICIAL`. No se propone cargar un `p`,
cambiar el tier ni sustituir el texto histórico.

