# ENCARGO M-4 (etiqueta repetida) · ENCUP + LAPOP + Latinobarómetro — bloqueado por entorno antes de abrir un solo PDF

Contadores movidos: 0

*5 de agosto de 2026.*

**Resultado de este acto, dicho antes que nada: NINGUNA de las dos
tareas del encargo (§5 del mensaje recibido) se ejecutó. No es "las
fuentes no tienen el dato" ni "el reactivo no califica" — es que esta
sesión no pudo abrir ningún PDF de ninguna de las tres encuestas. El
entorno es `cloud_default`, `data/raw` no existe en este worktree, el
corpus compartido (`/home/pc0/mm-corpus`) no está montado en ningún
punto del disco, y el propio encargo prohíbe tocar red "más allá de
git" — así que tampoco cabe bajar una copia nueva por HTTP. Impidió
medir las dos partes.**

---

## 0 · Colisión de etiqueta — verificada antes de escribir nada más

El mensaje recibido llama a esta tarea **"§5 · Encargo M-4"** y a la
siguiente **"§6 · Encargo M-5"**. Verificado contra el propio repositorio
antes de proceder: **ambas etiquetas ya están consumidas hoy mismo**,
para contenido sin relación alguna con ENCUP/LAPOP/Latinobarómetro ni con
inventarios/catálogo:

```
$ git log --format="%h %ad %s" --date=short | grep -i "ADR-63\|ADR-64"
7d590df 2026-08-05 ENCARGO M-5: sella conf.06 con ADR-64 — no era un conflicto sin nombrar...
a1ba9a4 2026-08-05 ENCARGO M-4: adjudica R1.3 → veredicto E (ADR-63, MESA-M4)
```

- **"ENCARGO M-4"** ya designó, hoy, la adjudicación de `R1.3` → veredicto
  `E` (`ADR-63`, `canon/gobernanza-v1_15.md:13`, entrada de
  `forense/hallazgos.md:130`).
- **"ENCARGO M-5"** ya designó, hoy, el cierre de `conf.06` (`ADR-64`,
  commit `7d590df`).
- Antes de esos dos, la misma serie de etiquetas ya se había usado el
  4/ago para **M-1** (`ADR-60`) y **M-2** (`ADR-61`,
  `forense/notas/2026-08-04-m2-adjudicacion-adr-61.md`).

Esto **no** se interpreta aquí como que la compuerta de `§6`
("requiere M-1 a M-4 fusionados") se refiera a esos ADR ya sellados —
su contenido no tiene relación con inventarios/catálogo/cruce, y leerlo
así sería inventar una premisa que el encargo no escribe. Se declara la
colisión para que mesa la vea: la serie `M-1..M-5` se está reutilizando
para un segundo lote de encargos, sin desambiguar. Este acto trata
"§5/M-4" y "§6/M-5" como un lote **nuevo y distinto**, y dos de sus
archivos (abajo) quedan nombrados sin la sigla `M-4`/`M-5` sola, para no
sumar una tercera colisión al grep de quien audite después.

---

## 1 · Verificación de entorno (bloque de arranque, antes de tocar nada)

```
$ echo "${CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE:-sin_variable}"
cloud_default
$ ls -la /home/pc0 2>&1
ls: cannot access '/home/pc0': No such file or directory
$ find / -maxdepth 3 -iname "*mm-corpus*" 2>/dev/null
(sin salida)
$ find data -maxdepth 3
data
data/catalogo-fuentes-v2_0.md
data/diseno-muestral.yaml
data/inventarios
data/manifiesto-staging.yaml
data/manifiesto.yaml
(sin data/raw, ni como directorio ni como symlink)
$ find / -iname "raices.local.yaml" 2>/dev/null
(sin salida)
$ git ls-files | grep -i "\.pdf$"
(sin salida — ningún PDF vive en git, por diseño: .gitignore:5 declara data/raw/)
```

Firma idéntica, verificada de forma independiente en el mismo día, por
otro acto: `forense/hallazgos.md:131` (Acto E-ENCIG) — *"este entorno es
`cloud_default` verificado, sin `data/raw` poblado y sin corpus
compartido montado en ningún punto del disco (barrido completo del
contenedor, cero resultados)"*. Y por el propio Acto P-LAPOP de hoy
(`forense/notas/2026-08-05-p-lapop-microdato.md` §3), que corrió en un
entorno *distinto* (Ubuntu con red, `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE`
vacío) y por eso sí pudo enlazar `data/raw -> /home/pc0/mm-corpus/raw`.
Este acto no tiene esa opción: no hay `/home/pc0` que enlazar.

**El encargo, para esta tarea, autoriza expresamente "nube o pc0,
cualquiera" pero prohíbe "tocar red más allá de git".** No se probó
ningún host externo (INEGI, `fomentocivico.segob.gob.mx`,
`vanderbilt.edu`, `latinobarometro.org`) porque hacerlo, aunque
respondiera, violaría esa cláusula — a diferencia de actos previos como
`cbis-deferencia-externas` (3/ago) o `P-LAPOP` (hoy), que corrieron bajo
encargos que sí permitían red y confirmaron alcanzabilidad. Aquí no se
intenta: la regla del encargo cierra esa puerta de entrada,
independientemente de si estaría abierta.

---

## 2 · Qué pedía el encargo (§5, dos partes)

**Parte 1 — ENCUP.** Leer los cinco cuestionarios (2001, 2003, 2005,
2008, 2012) y reportar, con redacción textual, qué reactivos de
participación política y colectiva traen — motivado por
`forense/cruce-catalogo-fichas-v2_0.md:90`, que marca:

> `R7.4/R7.5` | ≥25% de casos documentados de respuesta colectiva ante
> agravio cruzan la predicción ambiental | Ninguna | — | — | — |
> **NO EXISTE** — registro de eventos (protesta/autodefensa) codificado
> por entorno. Ninguna de las 6 clases nuevas lo trae (transparencia/
> sociedad civil se buscó vía MCCI/Cero Desabasto, ninguna de las dos es
> un registro de eventos de conflicto).

**Parte 2 — LAPOP AmericasBarometer 2023 México y Latinobarómetro 2024.**
Verificar contra el cuestionario (sin bajar microdato) qué reactivos de
deferencia, confianza institucional y confianza interpersonal traen, y
con qué escala.

---

## 3 · Parte 1 — ENCUP: qué hay registrado, qué no se pudo abrir

Los cinco cuestionarios (más la base de datos xlsx) están, en efecto, en
el manifiesto — "sin uso asignado", tal como afirma el encargo:

```
$ grep -n "^- id: encup" data/manifiesto.yaml
3277:- id: encup_2012_base_datos_xlsx
3310:- id: encup_2001_cuestionario_pdf
3343:- id: encup_2003_cuestionario_pdf
3376:- id: encup_2005_cuestionario_pdf
3409:- id: encup_2008_cuestionario_pdf
3442:- id: encup_2012_cuestionario_pdf
```

| Edición | id de manifiesto | archivo | sha256 (prefijo) | tamaño |
|---|---|---|---|---|
| 2001 | `encup_2001_cuestionario_pdf` | `encup_2001_cuestionario_pdf.pdf` | `bb33eedd…` | 147 691 B |
| 2003 | `encup_2003_cuestionario_pdf` | `encup_2003_cuestionario_pdf.pdf` | `acae1fe1…` | 233 736 B |
| 2005 | `encup_2005_cuestionario_pdf` | `encup_2005_cuestionario_pdf.pdf` | `c6f4a3c7…` | 116 061 B |
| 2008 | `encup_2008_cuestionario_pdf` | `encup_2008_cuestionario_pdf.pdf` | `df4337c8…` | 396 678 B |
| 2012 | `encup_2012_cuestionario_pdf` | `encup_2012_cuestionario_pdf.pdf` | `33be2b21…` | 1 026 475 B |

Los cinco están anotados en el manifiesto con el mismo `usado_para`
("sin uso asignado -- registro de inventario... No leída ni evaluada
esta sesión") y la misma nota de descarga (bajados 2026-08-04,
verificación TLS activa contra `fomentocivico.segob.gob.mx`, cadena
reparada con el intermedio Go Daddy vía su propia extensión AIA — sin
`-k`/`--insecure`). **Ninguno de los cinco vive en git** (confirmado,
§1) — todos están solo en `data/raw`, gitignorado, dentro del corpus
compartido de `pc0`, inalcanzable desde este contenedor.

Único antecedente de lectura: `forense/hallazgos.md:96` (Encargo M,
4/ago) abrió **solo el de 2012** (`Cuestionario-Quinta_2012_ENCUP.pdf`,
84 preguntas), buscando el reactivo de `deferencia` de `R2.1` — dos
candidatas examinadas (`P44A`, `P68`), ambas descartadas por objeto de
actitud. Ese acto **no** reporta nada sobre participación política o
colectiva (verificado: `grep -n "participaci\|protesta\|manifestaci\|
marcha\|colectiv"` sobre las dos notas de ese acto,
`2026-08-04-encup-paso1-deferencia.md` y
`2026-08-04-encup-paso2-deferencia.md`, cero coincidencias) — buscaba
otra cosa. **Los cuestionarios de 2001, 2003,
2005 y 2008 no han sido abiertos por ningún acto de este corpus**, para
ningún propósito (mismo grep, `-r` sobre `forense/`, sin resultado que
los nombre por contenido).

**Esta sesión no puede cerrar esa brecha.** No hay un solo PDF de ENCUP
alcanzable desde este contenedor, y aunque lo hubiera, el encargo mismo
prohíbe recuperarlo por red. No se fabrica una lista de reactivos de
memoria o por inferencia del nombre de la encuesta — sería exactamente
el tipo de "fingir un dato que el instrumento no documenta" que este
programa rechaza en cada acto anterior (p. ej. `forense/ficha-id-g3-v1_0.md:145`,
"no se finge una corrección que el instrumento no documenta").

---

## 4 · Parte 2 — LAPOP / Latinobarómetro: lo ya verificado por otro acto, y lo que sigue sin cubrir

Los tres payloads correspondientes también están en el manifiesto, todos
descargados el 3/ago/2026 por `sesion/cbis-deferencia-externas` desde un
entorno con red (WSL2, host `FF-5563`) — ninguno vive en este contenedor:

```
$ grep -n "^- id: lapop\|^- id: latinobarometro" data/manifiesto.yaml
3173:- id: lapop_abmex2023_cuestionario_mexico
3187:- id: latinobarometro2024_cuestionario_esp
3201:- id: latinobarometro2024_fichas_tecnicas
```

**Lo que ya está verificado — leído completo por ese acto (77 páginas /
3543 líneas para LAPOP, cuestionario + fichas técnicas completos para
Latinobarómetro, vía `pdftotext -layout` —
`forense/notas/2026-08-03-cbis-deferencia-externas.md` §2, §4):**

- **LAPOP AmericasBarometer México 2023 — deferencia (`R2.1`): SIN
  REACTIVO.** Barrido completo por `autoridad`, `obedien`, `jerarqu`,
  `superior`, `jefe`, `patrón`, `empleador`, `iniciativa`, `mand(a/ar/ó)`,
  `orden(a/es)`, `sumis`, `acatar`, `cuestionar`, `desafi`, `crianza`,
  `hijos` (§2.2). Cero coincidencias sobre jerarquía interpersonal
  concreta con efecto conductual. Los candidatos por vocabulario
  (`CHM1BN`/`CHM2BN`, apoyo a golpe de Estado, `FORMAL`/AFORE) miden
  legitimidad de régimen o formalidad laboral, no conducta ante
  jerarquía — mismo criterio que ya descartó `AP5_11` de ENCUCI.
- **Latinobarómetro 2024 — deferencia (`R2.1`): PROXY CON SUPUESTO
  DECLARADO.** Ítem `P4NOIJ` (§4.3): *"Pensando en las cualidades que se
  pueden alentar en los niños en el hogar... ¿cuáles considera usted que
  es especialmente importante de enseñar a un niño?"* — 15 opciones,
  escoger hasta 5, incluida **"Obediencia"**. Escala: selección múltiple
  no ordenada (binario por opción: escogida / no escogida), no una
  escala Likert. Objeto de actitud: crianza, no conducta del propio
  entrevistado ante una jerarquía — proxy, no reactivo directo (§4.4).
  País-año-n verificado contra la ficha técnica: México, n=1200,
  27 ago–8 sep 2024, muestra probabilística de 3 etapas + cuota en la
  última (§4.2).

**Lo que ese acto NO cubrió, y esta sesión no pudo cubrir tampoco.** El
encargo de hoy pide algo más amplio que `R2.1`: **confianza
institucional** y **confianza interpersonal**, con su escala — ninguna
de las dos aparece en `2026-08-03-cbis-deferencia-externas.md` (ese acto barrió
términos de jerarquía/obediencia, no de confianza; verificado: `grep -n
"confianza\|IT1\|B1\b\|B2\b\|B3\b\|B21"` sobre ese archivo, cero
coincidencias relevantes a batería de confianza). Se sabe, por
conocimiento externo al corpus (no verificado aquí, no se usa como
dato): LAPOP trae históricamente una batería de confianza institucional
(serie `B`, escala 1-7) y un ítem de confianza interpersonal (`IT1`,
escala 1-4); Latinobarómetro trae su propia batería de confianza en
instituciones y el ítem clásico "¿diría que se puede confiar en la
mayoría de las personas...?". **Ninguna de estas afirmaciones se
verifica contra el PDF real en este acto** — es exactamente la clase de
afirmación por fama que `forense/notas/2026-08-03-cbis-deferencia-externas.md:136`
ya señaló no usar como veredicto ("es conocimiento externo al corpus, no
una lectura de diccionario"). Se declara aquí como lo que falta, no como
hallazgo.

**Ninguna descarga nueva, ninguna lectura nueva.** No se tocó
`data/manifiesto.yaml`, no corrió `tests/manifiesto.py`, no se abrió
ningún PDF (ninguno es alcanzable desde este contenedor de todas
formas). Declaración ADR-46: esta sesión no leyó contenido de ningún
instrumento — la cita de §3-4 arriba es cita de un documento ya
publicado en este mismo repositorio (`2026-08-03-cbis-deferencia-externas.md`),
no una lectura nueva del PDF. Queda **habilitada** para pre-registrar
contra LAPOP 2023 y Latinobarómetro 2024 (a diferencia de la sesión que
sí los leyó, que quedó inhabilitada — `2026-08-03-cbis-deferencia-externas.md`
línea 35).

---

## 5 · §6 · Encargo "M-5" (cierre de inventarios/catálogo/cruce) — no se ejecuta

Compuerta explícita del propio encargo: *"requiere M-1 a M-4
fusionados."* Este acto es, él mismo, el intento de "M-4" del lote
nuevo (§4 de este documento) — **no está fusionado** (vive en la rama de
este PR, sin abrir siquiera). No hay forma de que la compuerta esté
satisfecha en el momento de escribir esto, bajo ninguna lectura: ni la
lectura "M-1..M-4 de este lote nuevo" (M-4 = este acto, sin fusionar por
definición, y M-1/M-2/M-3 del mismo lote nunca llegaron a esta sesión —
no hay encargo ni PR visible con ese contenido), ni la lectura errónea
"los ADR-60/61/?/63 ya sellados" (que además no tienen relación de
contenido con inventarios/catálogo, §0).

**Por disciplina de compuerta — el mismo criterio que
`forense/notas/2026-08-04-m1-adjudicacion-r3-1-paro.md`
(`forense/hallazgos.md:117`, primer intento de "ENCARGO M-1") ya aplicó
cuando verificó que dos PR requeridos seguían `open` y paró antes del
Commit 1 — este acto no toca ningún archivo del perímetro de §6:** `data/inventarios/*.md`,
`data/catalogo-fuentes-v2_0.md`, `forense/cruce-catalogo-fichas-v3_0.md`,
`tests/dedup.py`. Se deja constancia aquí de las cinco tareas que
`§6` pedía, para que una sesión futura con la compuerta satisfecha no
tenga que reconstruir el encargo desde cero (texto completo archivado en
`forense/encargos/`, §6 abajo).

---

## 6 · Qué no se tocó

`data/raw` no existe en este worktree (confirmado, §1). No se creó
symlink hacia ningún corpus — no hay `/home/pc0` que enlazar desde este
contenedor (a diferencia de `P-LAPOP`, hoy, que sí pudo). No se llamó a
ninguna herramienta de red hacia `fomentocivico.segob.gob.mx`,
`inegi.org.mx`, `vanderbilt.edu` ni `latinobarometro.org` — prohibido
por el propio encargo, independientemente de alcanzabilidad. No se tocó
`milpa/`, `canon/`, `data/manifiesto.yaml`, `data/inventarios/*.md`,
`data/catalogo-fuentes-v2_0.md`, `forense/cruce-catalogo-fichas-v2_0.md`
(solo leído), `tests/dedup.py`. No se selló ningún ADR.

---

## 7 · Ruta de recuperación anotada

Para que Parte 1 y Parte 2 de `§5` se completen de verdad, la próxima
sesión necesita **uno** de:

1. Correr en un entorno con `/home/pc0/mm-corpus` accesible (el patrón
   de `P-LAPOP`, hoy: `ln -s /home/pc0/mm-corpus/raw data/raw`) —
   entorno "Ubuntu con red" o `pc0` directo, no `cloud_default`.
2. Correr en `cloud_default` con la restricción de red del encargo
   **relajada** explícitamente por mesa para permitir `git clone`/`pull`
   de un espejo del corpus, o con el corpus wireado de otra forma al
   contenedor (no existe hoy ningún mecanismo así).

Con cualquiera de las dos, la Parte 1 exige abrir los cinco PDF de ENCUP
(`data/raw/encup_*cuestionario_pdf.pdf`, verificar sha256 contra la
tabla de §3 antes de leer) y transcribir, con página/línea, cada
reactivo de participación política/colectiva — no solo protesta:
también denuncia, contacto con autoridad, afiliación, voto, etc.,
declarando cuáles son individuales (participación) y cuáles, si los
hay, registran evento (para adjudicar `R7.4/R7.5` con evidencia, no
inferencia). La Parte 2 exige releer LAPOP y Latinobarómetro con
barrido de términos de **confianza** (`confianza`, `IT1`, serie `B`,
"puede confiarse en") con la misma disciplina de `cbis-deferencia-
externas.md` §2 — reactivo textual + escala + página.

---

## 8 · Suite

```
$ python3 tests/check.py --baseline
18 FAIL · 95 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado 837d5fe56d523615259efb77c17c84fee86ac684)
```

Idéntico antes y después de este acto (no se tocó ningún archivo medido).
