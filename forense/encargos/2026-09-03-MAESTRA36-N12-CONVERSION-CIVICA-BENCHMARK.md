3 · Conversión cívica con benchmark (firma 3)
ENCARGO · ACTO MAESTRA36-N12 · CONVERSION-CIVICA-BENCHMARK

SHA de redacción: 18fd2bd · v2.12 · Estado: LISTO PARA LANZAR — COMPUERTA: ninguna. ENTORNO: NUBE (solo lee data/l8-*, propuesta y web). NO en UBUNTU. MODELO: Opus. Invoca /acto; punto 4: toca red (web), no microdato — dilo.

FIRMA DE MESA (verbatim, arriba, #3). Lectura: mesa autoriza la conversión condicionada a un benchmark web que diga cómo se manejan efectos en puntos porcentuales al pasarlos a probabilidad individual, y a un contraste externo del tamaño del efecto. La carga al motor sigue gateada por FP-255: este acto propone la conversión con benchmark; la firma final es de mesa.

A.8, contra 18fd2bd: hallazgo L8: β_pres = +4.02 pp, IC wild cluster [+0.05, +7.89], IC municipio [+3.35, +4.68], β_int ≈ 0, ACOTADA, tier MEDIA (ADR e1, PR #493); entrada en la propuesta SELLADA-SIN-CARGA; FP-255 ABIERTA («dirección presenta, mesa traduce pp→p»). Conversión previa: grep -rn 'tipo_boleta_federal' milpa/tramite.yaml → 0. NO-ENCONTRADO.

P0 · Benchmark web, con fuente y sin decidir (antes de proponer nada). Dos preguntas, cada respuesta con URL, fecha de consulta y cita ≤ 15 palabras: (a) Tamaño del efecto en México. Punto de partida verificado por dirección el 3/sep: INE, Estudio muestral sobre la Participación Ciudadana 2015 (portalanterior.ine.mx/archivos2/DS/recopilacion/CG.ex201606-29in_01P11-00.pdf): distritos con elecciones locales concurrentes 53.3 % vs 50.2 % sin — +3 pp, misma dirección y orden que L8; TEPJF (2020), Elecciones concurrentes y participación electoral en México, 1991-2018 (te.gob.mx/editorial_service/media/pdf/250320241355301010.pdf); INE, Estudio muestral de participación ciudadana, elecciones concurrentes 2 de junio de 2024 (20 160 casillas). El acto abre los tres, extrae el efecto de concurrencia que cada uno reporte (o dice que no lo aísla), y añade lo que encuentre de la literatura comparada sobre elecciones on-cycle/off-cycle. Entregable: tabla fuente × efecto × unidad × diseño. (b) Cómo se convierte una diferencia en pp a probabilidad individual. Punto de partida verificado: diferencia de riesgo (aditiva: p₁ = p₀ + Δ) vs razón de momios (multiplicativa en logit: logit p₁ = logit p₀ + δ), y que la equivalencia entre ambas depende de la tasa base (effectsize, conversión OR↔RR con p0, Grant 2014). El acto documenta las dos convenciones, cuándo divergen (tasas base extremas) y cuál usa la literatura de turnout para efectos de contexto.

P1 · Propuesta de conversión, con sensibilidad. Regla propuesta: SI municipio con elección local concurrente con presidencial ENTONCES participa con p = p₀(municipio) + 0.040, p₀ = participación municipal base del propio panel de L8 (data/l8-*.json; se declara de dónde sale y su rango), acotada a [0,1]. Sensibilidad: la misma conversión en logit (δ tal que reproduce +4.0 pp en p₀ = 0.50) aplicada a los extremos del rango de p₀ observado; reportar cuánto difieren las dos convenciones en los municipios extremos. Escala declarada: probabilidad individual derivada de un efecto agregado municipal — es ecológica; se escribe así en la entrada. Tier propuesto MEDIA (heredado de L8). El benchmark de (a) se cita como corroboración externa del tamaño, no como dato del motor.

P2 · Presentación a mesa (RH), una página. Qué se carga, en qué escala, qué gana el modelo (primera regla cívica con dato causal), qué riesgo (inferencia ecológica; efecto de 2018/2024 con concurrencia casi universal), y las tres opciones que FP-255 ya nombra: cargar aditiva / cargar logit / dejar sellada. Entra a la propuesta como PROPUESTA-DE-CARGA, PENDIENTE-DE-MESA. No se toca tramite.yaml.

PERÍMETRO: forense/notas/…N12-* (benchmark + propuesta) · milpa/tramite-ola5-propuesta-v0.yaml (append) · forense/firmas-pendientes.tsv (FP-255: nota, sigue ABIERTA hasta la letra) · forense/hallazgos.md · cascada. NO toca milpa/tramite.yaml, milpa/procedencia.yaml, data/**, corpus/**. Frase del perímetro. CONTADOR: motor 16 → 16 (la carga es el sucesor); «propuestas de carga con benchmark externo: 0 → 1». Sucesor: letra de mesa sobre FP-255 → N13 · CARGA-CIVICA (motor 16 → 17).

## CONSUMIDO

Ejecutado por `ACTO MAESTRA36-N12 · CONVERSION-CIVICA-BENCHMARK`, 3/sep/2026,
entorno NUBE (`cloud_default`), rama `claude/conversion-civica-benchmark-8xvun4`,
contra `origin/main = 18fd2bd` (= SHA de redacción declarado, exacto).
`ADR-315` (renumerado DOS veces al fusionar tercero: `PR #506` `MAESTRA36-L12` se llevó el `313` y `PR #505` `MAESTRA36-A2` se llevó el `314`; re-derivado contra `origin/main = 035a07e`, máximo `314`, candidato `315`) · PR #507. `python3 tests/check.py --baseline` → **VERDE**
(19 FAIL, 175 WARN, nada nuevo contra `tests/baseline.json`).

**Punto 4 del ARRANQUE, como el encargo mandó decir:** el acto **toca red
(web)**, **no microdato**. `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` → `cloud_default`
(el ARRANQUE esperaba `sin_variable`; diferencia reportada, sin consecuencia
porque no se abre microdato) · `curl … https://www.inegi.org.mx/` → `000` ·
`ls data/raw/ 2>/dev/null | head -1` → vacío, `data/raw` **no existe**
(0 archivos examinados, `A.13`). Anti-PR#77 **no aplica**: este acto no
descarga nada.

**Desviación declarada respecto de lo que el encargo pidió:** `P0` ordenaba
«el acto abre los tres». **No abrió ninguno** — la política de egreso de este
entorno deniega `WebFetch` en general (control negativo con `en.wikipedia.org`
incluido). El benchmark se construyó con `WebSearch`, con la procedencia
marcada fila por fila y ninguna cita como `VERIFICADA-EN-DOCUMENTO`. La
reserva queda escrita en la entrada de la propuesta y en `forense/hallazgos.md`;
se cierra desde Ubuntu o desde una nube con egreso abierto.

**CONTADOR:** motor **16 → 16** · «propuestas de carga con benchmark externo:
**0 → 1**» · cargas al motor **0** · `FP-255` **ABIERTA** (anotada, no cerrada).
