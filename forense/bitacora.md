# Bitácora de sesión

*(Generado por `tests/bitacora.py --cierra`, protocolo §2. No se edita a mano salvo las dos líneas declaradas en cada bloque.)*

## 2026-07-30

**Fecha:** 2026-07-30 · **Rama:** `canon/verde-y-t17` · **HEAD inicial (origin/main):** `24df4b31434d70db0122a7ddb41ada0579a462cb` · **HEAD final:** `7dd1c5a77b4a911a992d09788c1a8e79f463cd31`

**Commits de la sesión:**
  - `7dd1c5a` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · Parte 2: aterriza protocolo-sesion, cola.yaml y tests/bitacora.py
  - `c42abc9` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · Parte 1: cierre del gate T17 -- estado sincronizado, deuda congelada, .gitignore
  - `97b9f2b` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · tests: T17 ve su propio objeto -- escanea hitoD-preregistro, no solo estado
  - `d123f49` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · gobernanza: v1.10 -> v1.11 -- ADR-42 (qué significa el verde) y ADR-43 (esquema de co-autoría)

**Archivos tocados:**
```
.gitignore                                         |  15 ++
 canon/cola.yaml                                    |  75 ++++++
 canon/estado-programa-v1_9.md                      |   6 +-
 canon/{gobernanza-v1_10.md => gobernanza-v1_11.md} |  22 +-
 canon/protocolo-sesion-v1_0.md                     | 107 ++++++++
 forense/historico/TRANSFER-maestra-9.md            | 188 ++++++++++++++
 tests/baseline.json                                |   9 +-
 tests/bitacora.py                                  | 270 +++++++++++++++++++++
 tests/check.py                                     | 106 +++++---
 9 files changed, 750 insertions(+), 48 deletions(-)
```

**ADRs añadidos:** ADR-42, ADR-43
**Líneas de versión modificadas en canon/:** 2
  - ### `gobernanza` · **v1.11** · 29 de julio de 2026 · **43 ADR**
  - ### `protocolo` · **v1.0** · 29 de julio de 2026

**Delta de suite:**
  - Antes: 18 FAIL · 81 WARN (congelados en origin/main)
  - Después: 19 FAIL · 82 WARN (corrida real, sin --baseline)

**Cola — IDs afectados en la sesión:**
  - Abiertos: D-01, D-02, D-03, D-04, E-01, I-01, I-02, I-03
  - Cerrados: (ninguno)

**Qué se decidió:** Se cerró el gate de T17 (deuda congelada en tests/baseline.json, hitoD-preregistro:8 NO se edita) y se aterrizó protocolo-sesion-v1_0, canon/cola.yaml y tests/bitacora.py -- primera vez que el protocolo de apertura/cierre existe en archivo, no solo en dos documentos tipo (3).
**Qué quedó bloqueado:** R3.1 y R3.4 siguen sin ficha -- bloqueadas por D-04 (qué modelo genera el baseline LLM) hasta que se decida. P3 de TRANSFER-9 (4 de 5 'decisiones que requieren firma') sigue sin poder derivarse: el documento nombra la #1 y dice 'las otras cuatro' sin listarlas.

---

