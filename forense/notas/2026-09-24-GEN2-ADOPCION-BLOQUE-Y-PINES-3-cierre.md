# Nota de cierre · ACTO GEN2-ADOPCION-BLOQUE-Y-PINES-3 · PARO-PREMISA (objetivo inalcanzable bajo la firma)

Cero contadores movidos. Cero mediciones. `milpa/tramite.yaml` no se tocó; el escritor no se extendió (no hay regla sobre la cual escribir).

## ARRANQUE
- Clon `/home/user/Modelado-Mexicano`, rama `claude/new-session-9bylha` (la fija la plataforma; no `acto/gen2-adopcion-bloque-y-pines-3`: logística, D-19). Mesa autorizó en sesión ejecutar en serie este encargo y GEN2-CATALOGO-CONTRATO-Y-TEST-1 («Ambos, en serie»).
- Base `3252aae` (origin/main; 0 detrás, 0 adelante). SHA de redacción `3d138c66` es ancestro; main se movió (#1111–#1113), re-derivado abajo.
- Entorno: hook `ENTORNO-DERIVADO = NUBE`, corpus montado=NO, archivos_examinados=0, red denegada por política. Cero microdato.
- Duplicados: `git ls-remote --heads origin | grep -i -E "adopcion|catalogo"` → 0; worktrees 1; PR abiertos con ADOPCION/CATALOGO → 0.

## Verificación de la premisa [SUPUESTO] de §3 — cae
Premisa: «cada uno de los diez RESULT tiene una regla en `tramite.yaml` cuyo `p` es exactamente el valor del RESULT».

EJECUTADO sobre `3252aae`, universo: `milpa/tramite.yaml` completo (22 reglas `^  - id:`):

| RESULT | regla/conducta en la propuesta ola 5 (l.) | conducta en tramite.yaml | p propuesta |
|---|---|---|---|
| RESULT-CTX-2019-P-ALTO | extorsión/contexto institucional · `contexto_institucional_alto_2019` (4004) | NO-ENCONTRADO | 0.7862745098039216 |
| RESULT-CTX-2023-P-ALTO | `contexto_institucional_alto_2023` (4007) | NO-ENCONTRADO | 0.7341176470588235 |
| RESULT-BANXICO-2024-HIP-ATRASO-P | `dinero.credito.atraso_y_dano_por_producto_banxico` · `atraso_credito_hipotecario_2024` (4046) | NO-ENCONTRADO | 0.18510485270103624 |
| RESULT-BANXICO-2024-TDC-ATRASO-P | `atraso_tarjeta_credito_2024` (4049) | NO-ENCONTRADO | 0.04235936236062071 |
| RESULT-BANXICO-2024-NOM-ATRASO-P | `atraso_credito_nomina_2024` (4052) | NO-ENCONTRADO | 0.1035233151033609 |
| RESULT-BANXICO-2024-PER-ATRASO-P | `atraso_credito_personal_2024` (4055) | NO-ENCONTRADO | 0.08031777453105593 |
| RESULT-BANXICO-2024-AUT-ATRASO-P | `atraso_credito_automotriz_2024` (4058) | NO-ENCONTRADO | 0.04309263821900375 |
| RESULT-MOTRAL15-P17-TOTAL-P | `trabajo.prestaciones.valoracion_seguridad_social_motral` · `valora_afirmativamente_seguridad_social_total` (4074) | NO-ENCONTRADO | 0.823626705331 |
| RESULT-MOTRAL15-ENOE-P17-CON-ACCESO-P | `…_con_acceso` (4077) | NO-ENCONTRADO | 0.832233738 |
| RESULT-MOTRAL15-ENOE-P17-SIN-ACCESO-P | `…_sin_acceso` (4080) | NO-ENCONTRADO | 0.790530962253 |

Comandos: `grep -c` en `milpa/tramite.yaml` de `contexto_institucional_alto`, `atraso_credito`, `atraso_tarjeta`, `valora_afirmativamente`, `dinero.credito.atraso_y_dano`, `trabajo.prestaciones` → 0 los seis. Búsqueda por valor (`p: 0.786`, `0.734`, `0.185`, `0.042`, `0.103`, `0.080`, `0.043`, `0.823`, `0.832`, `0.790`): 3 aciertos, los tres homónimos de otro constructo (l.926 ola ENIGH 2020 `0.043775`; l.992 denuncia con seguro `0.790900`; l.1482 `ahorra_solo_formal 0.080160`), descartados. `grep -c 'RESULT-BANXICO-2024\|RESULT-CTX-20\|RESULT-MOTRAL15' milpa/tramite.yaml` → 0 (paro f no aplica).

Las tres reglas viven solo en `milpa/tramite-ola5-propuesta-v0.yaml`, con `situacion/tier/porque/falsable_si: PENDIENTE-DE-MESA` y `rol_uso: proxy_descriptivo`; el propio bloque (l.3990-3993, l.4032-4035) dice «el OBJETO autoriza el consumidor descriptivo, no la carga al motor».

## Por qué es PARO y no replanteo
La firma (Decisión 2 de ADOPCION-2, verbatim en el encargo §2) dice «un RESULT por regla existente». No existe ninguna. Etiquetar exige primero **crear** tres reglas en el consumidor vivo del motor: eso es adoptar un consumidor nuevo (con tier y disparadores pendientes), no etiquetar; lo veda la firma y el paro (b)/(c) del encargo. La premisa toca una firma de mesa → PARA (§2 de las instrucciones). Objetivo (`pendientes_adopcion` 10 → 0) inalcanzable bajo esta firma → paro (f).

`corrida0.py status` en rama (sin cambios): `N_resultados_gen2_pendientes_adopcion=10` · `N_resultados_gen2_adoptados_activos=72` · `legacy_activas_por_consumidor__motor=34`.

## Pregunta a mesa (FP-260924-GEN2-ADOPCION-BLOQUE-Y-PINES-3-d164-01)
Opciones:
- **(a, recomendada)** Los diez quedan pendientes, a la vista, hasta que la propuesta ola 5 entre al motor con sus tiers; el contador 10 es verdadero y se deja así. Razón: los diez son `proxy_descriptivo` que su propio texto excluye de la carga al motor; meterlos al motor para bajar un contador contradice su `uso_motor`.
- **(b)** Firma nueva que autorice copiar las tres reglas de la propuesta a `milpa/tramite.yaml` vía escritor, con sus `p` = RESULT y `situacion/tier` pendientes. Costo: el motor carga reglas sin tier; hay que verificar que el cargador lo acepte.
- **(c)** Reconocer un consumidor descriptivo (no el motor) como consumidor válido para adopción: cambia la definición del contador; es acto de tubería.

Texto de firma para (a): «Los diez RESULT de 369b-01 no entran a milpa/tramite.yaml: son proxy descriptivo y el motor no los carga. Quedan como pendientes_adopcion hasta que la propuesta ola 5 entre con sus tiers; e0db-02 se cierra por esta decisión.»
