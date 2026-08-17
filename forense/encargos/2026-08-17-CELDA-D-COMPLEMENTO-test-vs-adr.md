- **SHA de redacción:** `b653bb4` (`origin/main`, confirmado sin drift al ejecutar — `git fetch origin main` deja `origin/main` = `b653bb4`)
- **Entorno asignado:** CAJA (repo-only, no necesita corpus) o nube — ejecutado en nube, repo-only, sin `data/raw`
- **Estado:** CONSUMIDO — ejecutado en este mismo acto, rama `claude/celda-d-complemento-conflict-jursjw`. Encargo y ejecución llegan en el mismo commit; no hay PR que citar todavía (el encargo no pide abrir uno). Ver `forense/notas/2026-08-17-celda-d-complemento.md` para la ejecución completa, comando por comando.

---

ENCARGO 2 · `CELDA-D-COMPLEMENTO` — el test y el ADR se contradicen

* Entorno: CAJA (repo-only, no necesita corpus) o nube. · Modelo: Sonnet 4.6.
* Por qué Sonnet: perímetro de un archivo, decisión acotada con condición de paro explícita, cero derivación de cantidades.
* SHA de redacción: `b653bb4` · Estado: `VIVO`.

§0 · El defecto, medido hoy

```
$ python3 tests/test_celdas_d.py
1 error(es) contra el contrato v0.3 §3:
  G5.obligacion_medida.conducta.yaml: falta campo obligatorio 'relacion_complemento' (v0.3 §3)
```

Y no es una omisión. El propio archivo lo declara en su línea 13: "NO LLEVA `relacion_complemento`. Es exigencia explícita del rector, no una omisión: ADR-75(b) dice que [...] dos análisis, sin fusión ni jerarquía."
O sea: `tests/test_celdas_d.py:71` y `ADR-75(b)` se contradicen. Nadie lo ha visto porque ese test no está en CI — `.github/workflows/verify.yml` corre `tests/check.py --baseline` y `tests/test_svystat.py`, y nada más.
§1 · Verificación de existencia — contestada
1 · ESTRUCTURA. Dominio 5 de `data/INFRAESTRUCTURA-v1_0.md` ("Registrar una celda-D del piloto"). Escribe `data/curacion-registro/celdas-d/G5.obligacion_medida.conducta.yaml` y nada más de `data/`.
2 · CONTENIDO. Tres celdas-D en el árbol; dos pasan, una falla. Y existe vocabulario sancionado para este caso, ya en uso:

```
$ grep -n relacion_complemento data/curacion-registro/celdas-d/*.yaml
G5.familismo_obligacion.actitud.yaml:138:  relacion_complemento: G5.familismo_obligacion.conducta
G5.radio_confianza.encuci_vs_enbiare.yaml:204:  relacion_complemento: NO-APLICA
```

`NO-APLICA` EXISTE-SATISFACE como forma de declarar que el campo no aplica.
3 · COBERTURA RETROACTIVA. La celda nació el 13/ago (`1224c37`, ACTO PROC-11 COMMIT 2); el contrato v0.3 es anterior. Sin brecha: la celda nació ya incumpliendo.
§2 · Qué hace — y dónde para
Paso 1, y es el que decide. Lee el contrato v0.3 §3.1 y el comentario de `G5.radio_confianza...:204`, que acota el rol: "rol COMPLEMENTO/relacion_complemento (H2, v0.3 §3.1) es para el caso…". Responde con cita: ¿`NO-APLICA` cubre el caso de ADR-75(b) —dos análisis sin fusión ni jerarquía— o está reservado a otro supuesto?

* Si lo cubre: escribe `relacion_complemento: NO-APLICA` con un comentario que cite `ADR-75(b)` como razón. La omisión deliberada pasa a ser explícita en el vocabulario del propio esquema. No es cambio semántico y no necesita ADR.
* Si NO lo cubre: PARA. Entonces la contradicción es real y la resuelve mesa: o el contrato gana una exención, o `ADR-75(b)` se enmienda. Redacta las dos opciones con su precio y deja la fila del tablero escrita en tu nota, sin escribirla — `firmas-pendientes.tsv` es perímetro de E-DEC.

Paso 2, en los dos casos. Declara en la nota que `test_celdas_d.py` no está en CI, con el `grep` del workflow. No lo añadas: tocar `.github/workflows/` durante dos actos en vuelo no vale el riesgo, y es decisión propia. Deja el contenido de la fila redactado en la nota.
§3 · Perímetro
Escribe: el YAML de la celda · `forense/notas/2026-08-17-celda-d-complemento.md` · `forense/hallazgos.md` (una línea) · este encargo en `forense/encargos/` (A.3). NO escribe: `canon/**` · `tests/**` · `.github/**` · `forense/firmas-pendientes.tsv` · `data/curacion-universo/**` · `tools/**`.
`python3 tests/test_celdas_d.py` y `python3 tests/check.py --baseline` antes y después, las cuatro salidas pegadas. Merge local. Contadores del programa: 0 — dilo así.

---

**Nota de ejecución (no parte del encargo original, añadida al archivar):** Paso 1 se contestó "sí lo cubre" — ver `forense/notas/2026-08-17-celda-d-complemento.md` §2 para la cita completa y el razonamiento. La rama de PARO (segunda viñeta de §2) no se ejecutó porque no aplicó: `ADR-75(b)` (`canon/gobernanza-v1_15.md:896`) contesta directamente la pregunta de si hay celda hermana ligada ("no dos facetas de lo mismo"), así que no quedó tablero que redactar para esa rama. La fila para `firmas-pendientes.tsv` que sí se redactó y no se escribió es la de Paso 2 (CI), no la de Paso 1 — ver la nota, §3.
