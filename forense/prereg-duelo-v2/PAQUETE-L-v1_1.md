# Paquete de la corrida `L` — marco-M v1_1, 11 celdas

**Acto que lo produce:** `MAESTRA33-E9 · L-SPEC-v1_1` (NUBE, `cloud_default`, repo-only). Redactado contra SHA `a71c9ea`, 1/sep/2026. CONTADOR: cero — este acto no corre ninguna `L`; produce el paquete que mesa pega y ejecuta en una sesión limpia fuera de este proyecto.

**Qué es este documento.** El paquete autocontenido para correr el corredor `L` sobre las 11 celdas de `marco-M-sorteado-v1_1.tsv` (`elegible_v1_1 = SI`), análogo a `lanzamiento-L-v1_0.md` (marco piloto), sin reabrir ese documento ni reinventar sus decisiones donde no cambian. Todo lo citado abajo viene del árbol congelado — nada se redefine aquí.

**Orden sagrado, repetido porque gobierna todo lo que sigue:** hashes → L → R → scoring. Las sesiones `L` jamás ven `R`. Este acto ya declara que 4 de las 11 celdas (`CIV-M-01/06/08/09`) tienen `R` en el repo — la sesión que corre `L` no las abre.

---

## 0 · Prohibición explícita — léela antes de arrancar

**Durante esta corrida, NO se abre:**
- `forense/prereg-duelo-v2/corridas-R/` (ni sus 4 archivos existentes)
- `forense/prereg-duelo-v2/scoreboard-v1_1.md`

Ninguna cifra de esos dos sitios entra en ningún prompt ni en ningún archivo de `corridas-L/`. `L-spec-v1_1.json` (§1) fue generado sin abrir ninguno de los dos — su cabecera lo declara.

---

## 1 · Compuerta de hashes — CORRE ESTO PRIMERO

Antes de cualquier llamada al modelo, la sesión ejecutora corre estos comandos desde `forense/prereg-duelo-v2/` y compara contra la tabla. Cualquier discordancia → PARO, con el campo que cambió declarado (A.7).

```bash
sha256sum pipeline-L-adv1-m2.py
sha256sum carga_l_v1_1.py
sha256sum L-spec-v1_1.json    # debe coincidir además con L-spec-v1_1.sha256
```

| Archivo | `sha256` esperado (al sellar este paquete) |
|---|---|
| `pipeline-L-adv1-m2.py` | ver `sha256sum` real en el repo — sellado por `E2-PREP-L-RUN`, tabla completa en `lanzamiento-L-v1_0.md` §0; este acto NO lo modificó, verificable con `git log -p -- forense/prereg-duelo-v2/pipeline-L-adv1-m2.py` desde `MAESTRA33-E9` |
| `carga_l_v1_1.py` | ver `L-spec-v1_1.sha256`-sibling `sha256sum forense/prereg-duelo-v2/carga_l_v1_1.py` al momento de correr — cargador nuevo de este acto, no del piloto |
| `L-spec-v1_1.json` | valor en `forense/prereg-duelo-v2/L-spec-v1_1.sha256` |

Si algo no coincide: no se sobreescribe la tabla — se aplica la regla de enmienda de `prereg-corrida-v1_0.md:110` (fila fechada, hash viejo, hash nuevo, razón) y se PARA hasta que mesa lo resuelva.

---

## 2 · Invariantes de la corrida (idénticos al piloto, F2 de `prereg-corrida-v1_0.md`, no re-declarados con otro valor)

| Parámetro | Valor | Fuente |
|---|---|---|
| `modelo_id` | `claude-opus-4-6` (o el que mesa fije en la RANURA de mesa de este mismo paquete antes de arrancar, sin editar este documento archivado — anotarlo en la sesión ejecutora) | `prereg-corrida-v1_0.md` F2(a) |
| `temperatura` | `1.0` | `prereg-corrida-v1_0.md` F2(a) |
| `k_corridas` | `8` | `prereg-corrida-v1_0.md` F2(b), `ParametrosCorredorL.__post_init__` exige `[5,10]` |
| Variantes | `L-solo`, `L+corpus` | `ADV1-M2`, `pipeline-L-adv1-m2.py:65` |
| Agregado | mediana + q10/q90/IQR (continuas); moda + self_consistency + distribución (categóricas) | `pipeline-L-adv1-m2.py` §5, `agregar_continua`/`agregar_categorica` — NO reinventado aquí |
| Descartes | CERO — todas las corridas registradas, rechazo de contenido cuenta como corrida válida | `pipeline-L-adv1-m2.py:189-206` |
| `version_declarada` | la cadena real que el proveedor devuelva en la primera llamada (`r.model`), congelada para el resto de la corrida — nunca inventada aquí | `prereg-corrida-v1_0.md:73`, `lanzamiento-L-v1_0.md` §3 |

**Total: 11 celdas × 2 variantes × 8 corridas = 176 llamadas al modelo.**

Las 11 celdas, con `id · conducta · encuesta · ola`, verbatim de `marco-M-sorteado-v1_1.tsv` (`elegible_v1_1 = SI`), copiadas de `L-spec-v1_1.json`:

```
CIV-M-01 · denuncia_con_miedo_o_desconfianza · ENVIPE · 2012
CIV-M-06 · denuncia_con_miedo_o_desconfianza · ENVIPE · 2017
CIV-M-08 · denuncia_con_miedo_o_desconfianza · ENVIPE · 2019
CIV-M-09 · denuncia_con_miedo_o_desconfianza · ENVIPE · 2020
CIV-M-11 · denuncia_con_miedo_o_desconfianza · ENVIPE · 2022
CIV-M-12 · denuncia_con_miedo_o_desconfianza · ENVIPE · 2023
CIV-M-13 · denuncia_con_miedo_o_desconfianza · ENVIPE · 2024
FAM-M-01 · recibe_dinero_familiares_para_vejez · ENIF · 2018
TRA-M-03 · paga_mordida · ENCIG · 2013
TRA-M-05 · paga_mordida · ENCIG · 2017
TRA-M-07 · paga_mordida · ENCIG · 2021
```

De estas, `CIV-M-01/06/08/09` ya tienen `R` en el repo (`corridas-R/`) — **no consultado por este paquete ni por `L-spec-v1_1.json`**; se listan aquí solo para que la sesión ejecutora sepa qué NO abrir (§0).

---

## 3 · Ceguera del modelo

Igual que `lanzamiento-L-v1_0.md` §2: cada llamada individual a la API es la "sesión limpia". El modelo solo ve el prompt que `construir_prompt` (`pipeline-L-adv1-m2.py:145-155`) arma a partir de `SpecCelda` — nunca este paquete, `L-spec-v1_1.json`, el marco, `corridas-R/` ni `scoreboard-v1_1.md`.

`carga_l_v1_1.py` (§5) adapta cada fila de `L-spec-v1_1.json` a `SpecCelda` (`celda_a_spec`, ver script) antes de llamar `construir_prompt` — la adaptación es mecánica y está documentada en el propio script.

---

## 4 · Comando exacto que mesa corre en sesión limpia fuera del proyecto

```bash
# 0) verificar hashes (§1) antes de nada
cd forense/prereg-duelo-v2 && sha256sum pipeline-L-adv1-m2.py carga_l_v1_1.py L-spec-v1_1.json

# 1) en ESTA sesión (nube, repo-only) el smoke-test ya se corrió y no se repite:
#    python3 forense/prereg-duelo-v2/carga_l_v1_1.py --dry-run
#    (verifica rutas + esquema; no llama a ningún modelo; no se ejecuta fuera de este acto salvo para reverificar)

# 2) en la SESIÓN EJECUTORA REAL (fuera de este proyecto, D-iii), con
#    ANTHROPIC_API_KEY presente y red saliente solo a api.anthropic.com:
#    - copiar carga_l_v1_1.py y pipeline-L-adv1-m2.py (sin editar ninguno)
#    - implementar llamar_modelo() exactamente como lanzamiento-L-v1_0.md §3
#      (mismo patrón: anthropic.Anthropic().messages.create(model=..., temperature=1.0, ...))
#    - invocar correr_celda(spec, params, contexto_corpus) por cada
#      (celda, variante) de L-spec-v1_1.json -- k=8 corridas cada una
#    - escribir cada RespuestaCorrida en la ruta de §5
```

**Modelo/versión/fecha/temperatura/k**: los de §2 — `claude-opus-4-6`, `version_declarada` = `r.model` real, fecha de la corrida real, `temperatura=1.0`, `k=8`. Ninguno se re-declara distinto de lo sellado en `prereg-corrida-v1_0.md`.

---

## 5 · Archivos que produce

Un JSON por `(id_celda, variante, índice)`:

```
forense/prereg-duelo-v2/corridas-L/L-<id_celda>-M__<variante>__<indice:02d>.json
```

Ejemplo real (verificado por `carga_l_v1_1.py --dry-run` en este acto): `forense/prereg-duelo-v2/corridas-L/L-CIV-M-01-M__L-solo__01.json`.

Esquema — igual que las 120 capturas del marco piloto (`id_celda`, `variante`, `indice`, `texto_crudo`, `valor_extraido`, `fuente_citada`, `timestamp`, `params`, `sha256_prompt`), verificado byte-a-byte de esquema (no de contenido) contra `corridas-L/CIV-08__L-solo__01.json` por `carga_l_v1_1.py --dry-run` en este mismo acto.

**Total esperado: 176 archivos** (11 celdas × 2 variantes × 8 corridas), todos commiteados.

`valor_extraido` queda `null` en la captura — el parseo real lo hace un extractor aparte, congelado antes de aplicarse (mismo patrón que `ACTO MAESTRA30-E6 · L-RUN` documentó para el piloto, `lanzamiento-L-v1_0.md` §5, enmienda 2026-08-26). Este paquete no construye ese extractor — queda para el acto que procese las 176 capturas.

---

## 6 · Cómo trae los archivos de vuelta al repo

1. La sesión ejecutora produce los 176 archivos localmente, fuera de este proyecto.
2. Abre rama nueva contra `main` y hace commit(s) con únicamente los 176 archivos de `corridas-L/` (perímetro estricto — ningún otro archivo del repo se toca desde la sesión ejecutora).
3. Abre **un** PR titulado **`[L] corridas v1_1`** contra `main`.
4. El revisor (`/revisa`, o mesa) **comenta** el PR — verifica compuerta de hashes (§1), conteo (176), esquema, y que ninguna celda con `R` existente (`CIV-M-01/06/08/09`) muestra evidencia de haber sido ajustada post-hoc. El revisor **no fusiona** — el merge es autorización de mesa, no trámite del ejecutor ni del revisor.
5. Una vez fusionado, el acto sucesor de scoring (`tools/score_marco_m.py`, `MAESTRA33-E8`) puede puntuar las celdas que ya tengan `R` + `L`.

---

## 7 · Dónde corre esto

**Fuera de NUBE** — `cloud_default` no tiene salida de red (verificado en este acto: `curl … https://www.inegi.org.mx/` → `000`; A.13: 0 archivos de `data/raw/` examinados porque ese directorio no existe en este clon, consistente con nube sin corpus montado). `api.anthropic.com` es el único destino de red que este paquete autoriza — ninguna descarga de microdato, ninguna consulta a INEGI ni a ninguna otra fuente.

**Firma de entorno (A.2, tres partes)** que la sesión ejecutora reporta al arrancar, mismo patrón que `lanzamiento-L-v1_0.md` §4:
1. `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` — valor crudo del entorno donde corre.
2. `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://api.anthropic.com/` (nunca `curl -I`).
3. `ANTHROPIC_API_KEY` presente — solo presencia/ausencia, nunca el valor.

---

## 8 · Prohibición explícita (repetida, D-13 la exige clara y no solo al inicio)

Durante esta corrida:
- **NO** se abre `corridas-R/` ni `scoreboard-v1_1.md`.
- **NO** se edita `pipeline-L-adv1-m2.py`.
- **NO** se ejecuta ninguna celda desde esta caja (NUBE, repo-only) — solo desde la sesión ejecutora externa.
- **NO** se activa el corredor `E` ni se corre `corredor-B-tasa-base.py`/`scoring-adv1-m3.py` — eso es un acto posterior, con microdato, en UBUNTU.

---

## Checklist de mesa antes de lanzar

- [ ] Caja elegida (con red saliente a `api.anthropic.com`).
- [ ] `ANTHROPIC_API_KEY` presente en esa caja.
- [ ] `modelo_id` confirmado (`claude-opus-4-6` por defecto) o sustituido explícitamente antes de arrancar.
- [ ] Compuerta de hashes (§1) corrida y verde.
- [ ] Confirmado que la sesión ejecutora no tiene abierto `corridas-R/` ni `scoreboard-v1_1.md`.
