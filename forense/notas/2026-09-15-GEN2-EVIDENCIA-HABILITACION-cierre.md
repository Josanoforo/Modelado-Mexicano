# GEN2-EVIDENCIA-HABILITACION · cierre

**Fecha:** 15/sep/2026. **Base recibida:** `582d4e936654cf0b5cac9574a60a9aafb0a2f5a4`.
**Base final revalidada:** `5973f121134e2962bfeba70a5d38f7500385b6cf`.
**Entorno:** CAJA/WSL2 con corpus montado. **Contador:** cero mediciones nuevas;
se reutilizan tres RESULT ya sellados. La adopción se perfecciona sólo con el
merge de mesa.

## Habilitación científica acotada

La decisión de Jonás autoriza el uso `DESCRIPTIVO` de tres RESULT existentes
como categoría `sin_colchon_un_mes`. El evento es `P4_10 en {1,2}`: no disponer
de ahorro suficiente para cubrir al menos un mes de gastos, incluidas personas
sin ahorros. No es duración condicionada a tener ahorro.

| RESULT | dominio | punto | IC95 sellado | n |
|---|---|---:|---|---:|
| `RESULT-ENIF-AHO-A-P-CORTO-SIN-P` | trabaja; `P3_13=7` | 0.541343 | [0.521597, 0.561928] | 4,973 |
| `RESULT-ENIF-AHO-A-P-CORTO-CON-P` | trabaja; `P3_13∈{1,2,3,4}` | 0.373130 | [0.349888, 0.393834] | 3,969 |
| `RESULT-ENIF-POB-P-CORTO-NO-TRABAJA-P` | `P3_8=8` o `P3_9=7` | 0.632782 | [0.608904, 0.656366] | 3,462 |

Unidad: persona elegida de 18+; denominador `P4_10∈{1,2,3,4,5}`;
8/9 excluidos; ponderador `FAC_PER`. La transformación es
`1 - p(P4_10∈{3,4,5})` dentro de cada dominio sellado. Los IC conservan
`IC-CON-ESTRATOS-DE-UPM-UNICA`: no se recalcularon ni se presentan como
validación independiente.

Cada identidad tiene vínculo y decisión propios. `tools/consulta_gen2.py`
expone categoría, evento, transformación, dominio y límites. Una petición
`MEDICION-GEN2` sigue en `NO_COVERAGE`; la suficiencia original de NC-0126 y
`DEM-AHORRO-STOCK-DURACION-01` no se reinterpretan como resueltas. No inferir
preferencia temporal, causalidad, probabilidad individual ni duración entre
quienes sí tienen ahorro.

## Documentación ENNViH adquirida

La ruta general antigua y RAND devolvieron 404. Se usaron las rutas oficiales
por ola y se incorporaron dos documentos complementarios al corpus:

| id | URL oficial | bytes | sha256 | verificación |
|---|---|---:|---|---|
| `ennvih2_2005_guia_usuario_ingles` | `https://www.ennvih-mxfls.org/english/assets/usersguidev2.pdf` | 385,292 | `63e98081cfb4c0556909be2890d73b7d0000784e880cb9118bf2c21fd4e42fcc` | PDF legible, 37 páginas |
| `ennvih3_2009_guia_usuario_ingles` | `https://www.ennvih-mxfls.org/english/assets/usersguidemxfls-3.pdf` | 708,423 | `747a9a0f33ec73166a62ebfc0ddca752dcc48ec14976100c124e4d204d6d10a8` | PDF legible, 45 páginas |

Total: **2 PDF / 1,093,715 bytes**. Son documentación, no microdatos ni
encuestas nuevas. Ambas distinguen usos longitudinales/transversales y remiten
a Berumen (2007), *Sample Design*, pero no publican réplicas ni identificadores
de UPM/estrato que habiliten los IC pendientes. `NC-0202` queda con contrato
explícito `FUENTE_O_VARIABLE/LISTA_SONDA`: comprobar ICPSR 118971 y Berumen sin
repetir estas guías. `NC-0156` conserva por separado el envío humano.

El paquete de transferencia
`ENNVIH-DOCUMENTACION-2026-09-15.zip` quedó en Descargas MX con rutas internas
portables `data/raw/ennvih/...`: 951,278 bytes, SHA-256
`1ba92400a2d3b044d60adffe2cf31eb5afdbdca88f3f6459196906964263eddd`.
La prueba integral del ZIP (`testzip`) no reportó miembro corrupto y los hashes
de ambos miembros coinciden con el manifiesto.

## Revisión end-to-end del cableado

Se recorrió la cadena completa: contrato científico → estado/versionado →
vínculo y decisión exactos → guardia de suficiencia → emisor GEN2 → consulta
pública → proyección de demanda → ejemplos y snapshot reproducibles →
manifiesto/corpus. La revisión encontró y corrigió una omisión adicional: la
proyección mostraba correctamente `MEDICION-GEN2` bloqueada, pero no exponía el
canal descriptivo habilitado. Ahora cada uno de los tres elementos conserva
`uso_disponible_hoy=false` para el uso original y añade exactamente un
`usos_alcance_menor[]` con `DESCRIPTIVO`, categoría, evento, transformación,
límites, guardia y `disponible_hoy=true`; el resumen cuenta exactamente tres.

La revalidación sobre la base vigente #785 encontró otro corte defectuoso:
una referencia histórica de conciliación (`NC-0088`, ya cerrada) provocaba un
`KeyError` porque el proyector la trataba como contrato activo. La conciliación
ahora retiene esa historia como evidencia pero sólo pasa contratos vigentes a
`necesidades_nc_abiertas`, faltantes y ruteo. Una regresión general comprueba
que ninguna referencia cerrada reaparezca en ese campo.

El selector del 15/sep enruta `NC-0202` por su contrato explícito y mantiene
`DEM-AHORRO-STOCK-DURACION-01` en espera hasta el 16/sep. La proyección no
reabre NC-0126 ni convierte el alcance menor en disponibilidad del uso
original. Los ejemplos originales `MEDICION-GEN2` continúan en `NO_COVERAGE`;
los tres ejemplos nuevos emiten únicamente `DESCRIPTIVO`. Decisiones ausentes,
no aplicables o múltiples fallan cerrado. Se regeneraron con sus escritores
canónicos la proyección, las respuestas de consulta y el snapshot del motor.

Verificación dirigida final: consulta (18), cableado ADQ (27), configuración
ADQ (7), contrato (20), cierre verificable (12), doctor (9), continuidad (3),
residuales (3), descubrimiento (9 grupos), motor/emisor (45), más las pruebas
directas de determinismo, clases, procedencia, matriz, umbrales y ejecutable.
El manifiesto verificó ambos IDs contra los bytes montados y el snapshot se
reprodujo exactamente. El verificador integral deja verdes `T02` (sin
colisiones), `T23` (cableado) y el resto del perímetro; conserva sólo tres
fallos de baseline, reproducidos también sobre `origin/main` #785: dos `T06`
(Gini/confianza interpersonal heterogéneos en reports) y un `T08` (siete
reports sin mapa de evidencia). La prueba histórica de orden holdout conserva
además su fallo de baseline (catálogo y motor entraron en el mismo commit).
Ninguno de esos cuatro hechos fue alterado ni ocultado por este acto.

## NO-CORRIDO / RESERVAS

- No se despliega esta rama aislada mientras #782 y sus evidencias #783/#784
  sigan sin fusionarse.
- No se envía el expediente de NC-0156 ni se contacta a terceros.
- La lectura directa de ICPSR 118971 permanece no verificada (HTTP 403).

## Resultado

La consulta descriptiva queda implementada y protegida por pruebas por dominio,
identidad de decisión y fallo cerrado ante ambigüedad. Cero RESULT, CALC,
reestimaciones o cambios a sellos. El cambio de `milpa/tramite.yaml` añade
evento y límite de uso; la autorización DESCRIPTIVA la impone el vínculo de
suficiencia exacto. No cambia ningún punto, IC, `n` ni tier.
