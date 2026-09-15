# ACTO GEN2-F5-DOCUMENTAL-RUN · PARO de transporte, cero llamadas experimentales

Fecha: 14 de septiembre de 2026.

Entorno: CAJA (Ubuntu/WSL2), `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable`,
red 200, corpus montado (412 archivos examinados), `claude 2.1.270`.

Base: `11c8783be2a9362cb5710013abf34a2be31701f7` (`origin/main` al arranque,
merge de PR #754). Encargo: `forense/encargos/2026-09-14-GEN2-F5-DOCUMENTAL-RUN.md`.

## Veredicto de la secundaria: NO HAY VEREDICTO — PARO DE TRANSPORTE

La pregunta secundaria del duelo (uso documental, **acotada al panel y al
paquete**: `DIN-M-01` y `TRA-M-07`, brazos `CONTEXTUAL-v2` y
`FUENTE-DIRIGIDA-v1`, 8 réplicas) **no recibe veredicto en este acto**. Su
fila del criterio, textual de
`forense/prereg-duelo-v2/F5-panel-viabilidad-presupuesto-spec-v1_0.md` §4.3:
«Éxito por celda: dirigido con >=6/8 puntos válidos y trazables, cero
sustituciones y mejora de cobertura >=4/8 contra su control contemporáneo.»
Ninguna de las 32 posiciones se ejecutó: la sonda de transporte que el propio
contrato antepone a la corrida devolvió `TRANSPORTE-NO-VALIDADO`, y la regla
sellada dice «si falla, TRANSPORTE-NO-VALIDADO, cero llamadas experimentales».
Ni `≥6/8` ni `<6/8`: no hay dato. Este párrafo no toca la primaria
(`CALC-TRIADA-0002`, `SIN-GANADOR-UNICO`) ni la re-adjudica, y no se lee junto
con ella — esa lectura es de mesa y dirección.

**Contador: no se mueve. No hay CALC, no hay cadena E.2, `cuenta_gen2` no
cambia.** Se dice en una línea, como pide el encargo.

## Embudo, contado en vivo

| paso del contrato | resultado | solicitudes (ledger / techo 96) |
|---|---|---|
| `--verify` | FALLA por `sha256_manifiesto_fuentes` únicamente (ver §3) | 0 (local) |
| `--freeze-plan` | plan congelado: 32 posiciones, cliente `2.1.270`, modelo `claude-opus-5`, HEAD `eea3cb44` | 0 (local) |
| `--transport-probe` | cuota RESPONDE; contrato dictamina `TRANSPORTE-NO-VALIDADO` | **2** (1 invocación; `num_turns=3`; cargo conservador) |
| `--run` | **NO EJECUTADO** por regla del contrato | 0 |
| éxitos / reintentos / abstenciones | 0 / 0 / 0 (ninguna posición corrida) | — |

Total gastado contra el techo: **2 / 96**.

## 1 · La firma (P1 previa) — dos huecos del contrato sellado, resueltos con mesa

El verificador sellado (`tools/f5_documental.py::verificar_autorizacion`)
exige un archivo vivo fuera de `forense/encargos/cola/` con marcador
`FIRMA DE MESA` y cuatro frases literales tomadas del texto propuesto en
`cola/2026-09-11-GEN2-POST-723/31-GEN2-F5-DOCUMENTAL-EJECUCION-PARA-FIRMA.md`.
Corrido contra el encargo archivado de este acto:

```
RECHAZADA: firma no coincide con alcance esperado; faltan:
['Autorizo el encargo 31 y FP-373', 'máximo 96 solicitudes', 'No autorizo FP-374 ni F6']
```

Mesa, preguntada explícitamente, contestó «Firmo el texto de 31 tal cual».
Se archivó `forense/prereg-duelo-v2/F5-documental-v1_0/F5-documental-firma-v1_0.md`
con las palabras de mesa verbatim («si, ya hay cuota de opus, dame ese
encargo f5»), la cita al encargo RUN y el texto de autorización del encargo 31
verbatim. El verificador lo acepta sin cambio:
`sha256 aa7135c8ad53053592798141d1ea91f4c37d467cd10f640522578e5298583f60`,
1496 bytes. **FP-373 → FIRMADA** (token en `forense/firmas-pendientes.tsv`,
A.16); el merge de mesa del PR de este acto perfecciona la firma.

## 2 · La sonda (P1) — salida cruda y las tres causas

Registro completo: `forense/prereg-duelo-v2/F5-documental-v1_0/sonda-transporte-v1_0.json`
(sobre CLI original íntegro). Extracto:

```
estado=TRANSPORTE-NO-VALIDADO  timestamp=2026-09-14T18:34:24Z  returncode=0  is_error=false
modelos_reportados=['claude-haiku-4-5', 'claude-opus-5']  num_turns=3  stop_reason=tool_use
modelUsage: claude-opus-5 {cacheCreation 118212, cacheRead 117745, in 4, out 867}
            claude-haiku-4-5-20251001 {in 91703, out 22}
permission_denials: [{tool_name: mcp__f5docs__weighted_distribution,
                      tool_input: {path: analysis.tsv, value_column: P8_3_1, weight_column: FAC_P18}}]
structured_output.estado=ABSTENCION  punto_porcentaje=null  sustitucion_semantica=false
structured_output.nota empieza con el marcador 63ae53fa…  (marcador: OK)
```

Las tres condiciones de la sonda, una por una: marcador en `nota` = OK ·
`modelos == {claude-opus-5}` = **FALLA** · `cargo ≤ 2` = OK (por regla
conservadora: `num_turns=3` se carga como 2).

1. **Herramienta MCP denegada.** El comando sellado (`comando_mcp`) pasa
   `--permission-prompts none` («anything that would prompt is denied
   automatically», `claude -p --help`) y `--tools mcp__f5docs__weighted_distribution`,
   pero **no** `--allowedTools`. `--tools` limita el catálogo; no concede
   permiso. El modelo lo escribió en su derivación: «la llamada a
   weighted_distribution … fue bloqueada: la herramienta requiere aprobación y
   esta sesión no tiene superficie de aprobación … se responde ABSTENCION».
   Consecuencia estructural: con el contrato tal como está, el brazo
   `FUENTE-DIRIGIDA-v1` no puede leer `analysis.tsv` en ninguna de sus 16
   posiciones — un `≥6/8` sería imposible por diseño, no por el dato.
2. **Modelo auxiliar.** El contrato registra que la F5 anterior reportó «Opus y
   un Haiku auxiliar» y apuesta a que `--prompt-suggestions false` lo elimina;
   no lo elimina (Haiku leyó 91 703 tokens y emitió 22). La sonda exige un solo
   modelo. No se identificó la causa sin más llamadas contadas, y no se gastaron.
3. **Turnos.** `num_turns=3` con `--max-turns 2`: la premisa contable «≤2
   solicitudes por invocación» no la sostiene el cliente `2.1.270`; el ledger
   carga 2 por regla conservadora del contrato, que por eso no queda subcontado
   pero sí incierto.

Ninguna de las tres es de cuota (P1 pedía PARO honesto si la cuota no
respondía; respondió). Las tres son del contrato tal como se selló, y el
encargo dice «lo EJECUTA, no lo enmienda … PARA y repórtalo». Mesa,
preguntada, eligió «PARO como manda el encargo».

## 3 · `--verify` — reserva declarada

`RuntimeError: materializacion no reproduce manifiesto`. Diferencia única,
por diff campo a campo del manifiesto esperado contra el archivado:
`sha256_manifiesto_fuentes` (esperado `07f19433…`, archivado `9eb91ebe…`).
`data/manifiesto.yaml` cambió en 6 commits ajenos desde el sello `c9f714e`
(1599 → 1608 filas); las 8 filas del contrato (`ennvih1_2002_hogar_q`,
`_cb`, `_dta`, `ennvih1_2002_ponderador`, `ennvih1_muestra_diseno`,
`encig2021_cuestionario_pdf`, `encig2021_estructura_base_datos_pdf`,
`encig_2021_encig21_base_datos_csv`) son IDÉNTICAS campo a campo, y
`validar_fuente` (tamaño + sha256 de cada payload), `verificar_paquete`
(bytes + sha256 de los 10 archivos del paquete) y `comprobar_ancestros`
(#720, #722) pasan. El verificador compara contra un archivo que crece con
cada acto de adquisición: defecto del verificador, no del transporte. Mesa
autorizó seguir con reserva; el runner no se tocó. Va como fila NC.

## 4 · Lo que sí queda en el árbol

- `F5-documental-firma-v1_0.md` (firma archivada, aceptada por el verificador).
- `F5-documental-plan-v1_0.json` (plan congelado v1.0; un contrato v1.1 lo
  sucede, no lo edita).
- `sonda-transporte-v1_0.json` y `solicitudes-ledger-v1_0.json` (2/96).
- Enmienda fechada de REANUDACIÓN Y PARO en `F5-documental-ejecucion-v1_0.md`
  (original intacto; el asiento de la PAUSA sigue en `NC-0173`, no llegó).
- `FP-373 → FIRMADA` (no ejecutada). `NC-0160` sigue ABIERTA con enmienda:
  la decisión de mesa ya no está pendiente, las 32 posiciones siguen sin
  correr; su sucesor pasa a la fila NC nueva de este acto.

## 5 · Sucesor que este acto no ejecuta

Un contrato `F5-documental-ejecucion-v1_1` (sucesora fechada, v1.0 intacta)
que: (a) conceda la herramienta (`--allowedTools mcp__f5docs__weighted_distribution`
o el mecanismo equivalente del cliente vigente); (b) decida qué hace la sonda
con el modelo auxiliar — o lo suprime con causa identificada, o lo admite como
auxiliar con tope de tokens de salida, nunca lo ignora; (c) reconcilie la
contabilidad de turnos con lo que el cliente reporta; (d) re-congele el plan
y corra su propia sonda (contada). La firma de FP-373 ya existe y su alcance
(32 posiciones, techo 96, sin FP-374/F6) no cambia; las 2 solicitudes de este
acto se cuentan contra el mismo techo. Los 32 estados, si se corren, se
reportan separados de la primaria.
