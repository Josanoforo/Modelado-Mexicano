# Cobertura completa de Ola 6 — mapa de dominio y plan por regla

`ACTO MAESTRA38-N10 · COBERTURA-COMPLETA-OLA6`. Corrida 5/sep/2026, entorno
**NUBE**, contra `origin/main = 25383f35`. Encargo archivado en
`forense/encargos/2026-09-05-MAESTRA38-N10-COBERTURA-COMPLETA-OLA6.md`.
COMPUERTA `N9 fusionado` verificada por producto: `test -f tools/ya_medido.py`
contra `origin/main` → existe (`9e767a8`, `PR #538`).

**Mandato de mesa, verbatim (4/sep/2026):** «Entiendo que hay un mínimo y ese
mínimo para lanzar una ola es una cosa. Pero hoy no tenemos lo mínimo y no
quiero hacerlo al mínimo no después de haber invertido tanto en la
infraestructura que creamos.» Este acto no busca el mínimo que abre un
dominio: busca el mapa completo de las 25 reglas de los 6 dominios candidatos
y el plan para cubrirlas todas. El criterio 2 de `motor-nucleo-medible-v1_0.md`
§3.a se reporta abajo como consecuencia — no se relaja, no se reinterpreta, no
se optimiza para que pase.

---

## 1 · COMMIT-1 · Universo y criterio

### 1.1 · Universo, derivado por comando y congelado

```
$ sed -n '508,514p;524,531p;541,547p;562,569p;571,577p;579,588p' canon/modelo-decision-v4_0.md \
  | grep -c '^\- \*\*SI\*\*'
25
```

Verificado dos veces por mecanismos independientes: (1) conteo de bullets
`- **SI**` dentro del rango de línea de cada sección (`§3.2` 508-514, `§3.4`
524-531, `§3.6` 541-547, `§3.8` 562-569, `§3.9` 571-577, `§3.10` 579-588) →
**4+5+4+4+4+4 = 25**; (2) el `REGISTRO` congelado de
`tests/validador_registro_ids.py` (Hito D, 29/jul/2026) trae exactamente 4
`R2.*`, 5 `R4.*`, 4 `R6.*`, 4 `R8.*`, 4 `R9.*`, 4 `R10.*` — **25** filas para
estas seis secciones, cero huecos, cero duplicados. El encargo estimaba
«~30»; **el real es 25 — se declara, no se fuerza a 30.**

Una fila del universo (`salud.vacunacion.disponible`, `R9.2`) trae dominio
equivocado en su propio `id` (`salud.*` en una regla de `§3.9`, no `§3.4`) —
anomalía ya declarada por el propio canon y por `forense/hallazgos.md`, **no
se corrige aquí** (fuera de perímetro: `canon/modelo-decision-v4_0.md` no se
toca salvo ADR). Se cuenta en `§3.9` (su sección real), no en `§3.4`.

### 1.2 · Criterio de clasificación — cerrado, cita el precedente de la casa

Mismo vocabulario que `MAESTRA38-N5` §1.3 (`REFORMULABLE`/`SIN-INSTRUMENTO`/
`CON-CANDIDATA`), con una categoría más que ese acto no necesitaba porque sus
9 reglas ya venían todas sin `EXISTE-SATISFACE`: aquí `MAESTRA34-N5` ya había
encontrado 2 `EXISTE-SATISFACE`, así que el universo de N10 necesita nombrar
también ese caso.

- **MEDIBLE-COMO-ESTÁ** — antecedente y desenlace de la regla están medidos
  **en la misma persona, en el mismo instrumento** del corpus. Traducción al
  vocabulario `EXISTE-SATISFACE` de `MAESTRA34-N5`/`MAESTRA36-N6`, con un
  requisito más estricto (*misma persona, mismo instrumento*, no solo *ambos
  términos aparecen en el corpus*) — declarado así porque el encargo lo pide
  explícito y porque las dos filas que califican (ver `§2.2`, `§2.5`) lo
  cumplen de sobra.
- **REFORMULABLE** *(N5 §1.3.a)* — existe un reactivo que mide el mismo
  *driver* con otro desenlace observable, o el mismo desenlace con otro
  encuadre del *driver*: el objeto se reescribe para anclarse a lo que el
  reactivo realmente mide, **conservando driver y signo, cambiando una sola
  cosa** — sin inventar dato. Precedente de la casa, citado y no repetido:
  `civico.voto.clientelar_si_observable` → `..._lapop2019` y
  `civico.protesta.agravio_urbano` → `..._multiola` (`MAESTRA38-N5` §2.6/§2.8,
  cargadas por `MAESTRA38-N6`/`FP-298` como «tercera formulación
  complementaria» — ninguna de las dos pertenece al universo de Ola 6, se
  citan solo como método, **no se reclasifican aquí**).
- **CON-CANDIDATA** *(N5 §1.3.c)* — existe una fuente nombrada y conocida
  (encuesta o administrativa) que podría resolver el objeto, identificada
  **dentro** del corpus o el manifiesto pero pendiente de adquisición, de
  lectura completa, o de abrir bytes para confirmar alcance — el caso de
  referencia es `N34`/ENCRIGE (`MAESTRA38-N5` §2.3-2.4).
- **HIPÓTESIS-SIN-INSTRUMENTO** *(N5 §1.3.b)* — ningún instrumento nacional
  mide hoy la condición que la regla exige; se escribe el instrumento mínimo
  (una pregunta, una población).

**Regla de honestidad (c), verbatim del encargo, aplicada literalmente en las
25:** si conservar el *driver* exige un reactivo que no existe, no es
`REFORMULABLE` aunque haya algo parecido. Ruido de substring no cuenta (N5
§2.0) — un acierto de `busca_reactivos.py` que solo coincide por texto sin
relación conceptual con el mecanismo de la regla se declara ruido y el
veredicto cae a `HIPÓTESIS-SIN-INSTRUMENTO` o `CON-CANDIDATA` según
corresponda. Esta nota descarta explícitamente, regla por regla, cada acierto
que resultó ser ruido — no se omite el intento fallido (ver detalle por
dominio).

### 1.3 · `tools/ya_medido.py`, corrido para las 25 ANTES de clasificar

```
$ for id in trabajo.jerarquia.deferencia_iniciativa_suprimida trabajo.liderazgo.benevolencia_legitima \
    trabajo.prestaciones.formalidad_pesa_mas_que_salario trabajo.rotacion.joven_urbano_sin_culpa \
    salud.atencion.leve_sin_imss salud.atencion.grave salud.prevencion.hombre_sin_permiso \
    salud.adherencia.desabasto_vs_cuidadora salud.consumo.sellos_precio_similar \
    tiempo.puntualidad.formal_vs_social tiempo.compromiso.si_voy_incierto \
    tiempo.bomberazo.recursos_escasos_urgencias tiempo.cumplimiento.recordatorio_baja_barrera \
    cooperacion.comite.monitoreo_sancion_visible cooperacion.tanda.conoce_organizadora \
    cooperacion.confianza.puente_personal cooperacion.faena.sancion_social_pueblo_mestizo \
    informacion.credibilidad.allegado_confianza informacion.deferencia.costo_acceso_experto \
    salud.vacunacion.disponible informacion.escuela.miedo_a_caer_clase_media \
    comunicacion.rechazo.indirecto_face comunicacion.retroalimentacion.privada_publica_capital_social \
    comunicacion.inseguridad.ver_oir_callar comunicacion.directividad.regional_generacional; do
  python3 tools/ya_medido.py "$id" | tail -1
done
```

**Salida: `NUNCA-MEDIDA` en las 25, sin excepción.** Consistente con lo que
`MAESTRA34-N5`/`MAESTRA36-N6` ya habían dejado escrito (criterio 1 y criterio
2 evaluados, cero medición real corrida sobre Ola 6): las cinco fuentes que
`ya_medido.py` cruza (`milpa/tramite.yaml`, `milpa/tramite-ola5-propuesta-v0.
yaml`, `canon/modelo-decision-v4_0.md` §7, `forense/notas/*-L*-*.md`,
`forense/prereg-caja/S*-spec-*.md`) no traen ninguna falsación real sobre
ninguna de las 25 — ni siquiera las 2 que `MAESTRA34-N5` ya había encontrado
`EXISTE-SATISFACE` por reactivo. **No hay discrepancia que declarar contra
`ya_medido.py`** en esta pieza (ver `§5 · Hallazgos`): `MAESTRA34-N5`/
`MAESTRA36-N6` nunca afirmaron que hubiera medición corrida — afirmaron
existencia de reactivo, una pregunta distinta, y las dos lecturas coinciden.

### 1.4 · Tercer insumo que `MAESTRA34-N5`/`MAESTRA36-N6` no tenían asignado

`MAESTRA34-N5` buscó en `inventario-reactivos-v1_2.tsv` + `-ext-v1_0.tsv`
(241 591 filas, encuestas). `MAESTRA36-N6` cruzó `data/manifiesto.yaml`
(1 104 entradas, fuentes administrativas). **Ninguno de los dos acto corrió
`busca_reactivos.py --tablas descargas_mx_v1_1`** (42 548 filas, 42 536
examinadas — universo que el propio encargo de N10 nombra) — la tabla que
`MAESTRA38-N5` sí usó, en otro dominio, y que trae `LAPOP AmericasBarometer`
(2004/2006/2019/2021/2023), `World Values Survey` (ola 7), `ENSANUT 2024`
crudo, y paneles `AEJ`/Compartamos (`round2_mexico_anon.dta`,
`round5_mexiconew_anon.dta`) que **no están indexados** en `v1_2`/`ext`. Este
acto corre esa tercera pasada, regla por regla — **75 corridas** (3
formulaciones × 25 reglas, reusando literalmente las formulaciones ya
diseñadas por `MAESTRA34-N5` para cada regla, contra la tabla nueva, sin
inventar vocabulario de búsqueda nuevo). Comandos y salidas crudas:
`/tmp/claude-0/…/scratchpad/busca_v11/{trabajo,salud,tiempo,cooperacion,
informacion,comunicacion}.txt` (efímero de sesión, no versionado — cada
comando se reproduce con la línea citada en cada regla de abajo).

---
