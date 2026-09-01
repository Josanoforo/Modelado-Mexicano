# `sorteo_v3.py` — regresión contra B′ (v1_0) y reporte informativo sobre v1_1

`ACTO MAESTRA33-S1 · SORTEO-v3-Y-PROPAGA`, P1, 1/sep/2026. Corridas reales
sobre los archivos ya en el árbol (`sorteo_marco_m.cargar_marco_m()`,
`sorteo_marco_m_v1_1.cargar_marco_m_v1_1()`, ambos con verificación de
sha256 contra su sidecar, sin editar ninguno de los dos), no supuestas —
comando y salida cruda declarados abajo (A.13). Cero archivos `*sorteado*`
escritos por esta nota ni por `tests_sorteo_v3.py` (verificado: `git diff
--stat` vacío contra los tres marcos/sorteados citados, es la propia
`TestReporteInformativoV1_1.test_este_archivo_no_toca_ningun_sorteado`).

## 1 · Regresión contra B′ (v1_0)

B′ (`ACTO MAESTRA32-E14 · MARCO-M-SORTEA`) sorteó con la rama **identidad**
de `sorteo_marco_m.sortear_marco_m` (`N_elegibles=2 < 15`, regla de tamaño
§e): no invoca `asignar_asientos_proporcional` en absoluto, sólo ordena por
`id`. Esa rama vive en `sorteo_marco_m.py` (no tocado) y su salida no
depende de qué función de reparto de asientos esté detrás — por
construcción, un `sortear_marco_m_v3` hipotético (mismo despacho por `N`,
sólo cambiando qué `sortear` usa cuando `N>=15`) reproduciría B′ byte a
byte, para cualquier versión del reparto de asientos. Eso no es la
afirmación interesante — es cierta independientemente de si el piso liga.

La afirmación que sí depende del piso: **¿el reparto de asientos de v3
habría dado algo distinto al de v2 sobre el marco real de B′, si se
forzara a correr?** Verificado por cómputo directo (`estratos` real, no un
marco sintético):

```
$ python3 -c "
import sys; sys.path.insert(0,'forense/prereg-duelo-v2')
import importlib.util
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s)
    sys.modules[n]=m; s.loader.exec_module(m); return m
marco_m=load('sorteo_marco_m','forense/prereg-duelo-v2/sorteo_marco_m.py')
v3=load('sorteo_v3','forense/prereg-duelo-v2/sorteo_v3.py')
v2=marco_m._SORTEO_V2
marco=marco_m.cargar_marco_m()
estratos=v2._agrupar_por_estrato(marco)
print('estratos:', {e: len(fs) for e,fs in estratos.items()})
print('asientos v2:', v2.asignar_asientos_proporcional(estratos, 2))
print('asientos v3:', v3.asignar_asientos_proporcional_v3(estratos, 2))
"
estratos: {'tramite|P1|MEDIA': 2}
asientos v2: {'tramite|P1|MEDIA': 2}
asientos v3: {'tramite|P1|MEDIA': 2}
```

**El piso no ligaba ahí**: mono-estrato (`tramite|P1|MEDIA`, `TRA-M-01`,
`TRA-M-02`), `n_sorteo=2`. Con un solo estrato no vacío, "piso 1 + Hamilton
sobre el resto" da trivialmente el 100% del resto a ese mismo estrato — no
hay otro estrato con el que competir por fracción, así que v3 coincide con
v2 (`{'tramite|P1|MEDIA': 2}` en ambos casos). Confirma lo que
`sorteo-marco-M-resultados-v1_0.md` ya declaraba ("único estrato presente…
No aplica un segundo estrato — el universo entero es monoestrato").

**Conclusión de la regresión**: dado que el piso no liga (verificado
arriba, no supuesto) y que la rama que B′ realmente ejecutó no depende de
la versión del reparto (verificado también, `TestRegresionBPrime` en
`tests_sorteo_v3.py`), B′ se reproduce byte a byte — `TRA-M-01`, `TRA-M-02`
— bajo cualquier reparto de asientos, v2 o v3. La condición que el encargo
puso ("si el piso no ligaba ahí") se cumple, declarada con la aritmética a
la vista, no afirmada sin verificar.

## 2 · Reporte informativo sobre la semilla de v1_1 (B″) — qué habría cambiado

**Sin escribir ningún sorteado nuevo.** `marco-M-sorteado-v1_1.tsv` sigue
siendo el sellado de `FP-213`/`ADR-248` (opción A: se acepta tal cual — ver
`forense/firmas-pendientes.tsv` FP-213). Esta sección es sólo lectura: qué
habría producido `sortear_v3` con la MISMA semilla y el MISMO marco, para
que mesa vea el costo concreto de cada opción antes de decidir si alguna
vez se re-sortea.

```
$ python3 -c "
... (misma carga que arriba, sorteo_marco_m_v1_1 + sorteo_v3) ...
marco = cargar_marco_m_v1_1()   # 22 filas elegible_v1_1=='SI', sha256 verificado
semilla = semilla_desde_sha_merge('af41796f50baad1737987b7e9a1e737c38ab85f2', 'MARCO-M-v1_1')
# semilla = 34354141898495593251517379743390345279 (misma que selló B'')
estratos = {'PENDIENTE': 21, 'tramite|P1|MEDIA': 1}
asientos v2 (real, sellado):   {'PENDIENTE': 11, 'tramite|P1|MEDIA': 0}
asientos v3 (hipotético):      {'PENDIENTE': 10, 'tramite|P1|MEDIA': 1}
"
```

`sortear_v3(marco, n_sorteo=11, cuota_max=2, semilla=34354141898495593251517379743390345279)`,
verificado ids contra el `.tsv` sellado en disco (control: recomputar con
`sorteo_v2.sortear` sin editar coincide exacto con
`marco-M-sorteado-v1_1.tsv`, como conjunto — `TestReporteInformativoV1_1.
test_v2_recomputado_coincide_con_el_sellado`):

| | v2 (real, sellado) | v3 (hipotético, no escrito) |
|---|---|---|
| `PENDIENTE` | 11 asientos | 10 asientos |
| `tramite\|P1\|MEDIA` | 0 asientos — `TRA-M-02` sin asiento (el hallazgo de `FP-213`) | 1 asiento — `TRA-M-02` entra |

**Diff exacto de las 11 filas** (mismo PRNG, misma semilla — el `rng.sample`
de 10 elementos sobre `PENDIENTE` no es un subconjunto trivial del de 11,
se recorrió el algoritmo completo, no se truncó a mano):

- **Entraría bajo v3, no está en el sellado:** `TRA-M-02`.
- **Saldría bajo v3, sí está en el sellado:** `CIV-M-01`.
- Las otras 10 filas (`CIV-M-06/08/09/11/12/13`, `FAM-M-01`,
  `TRA-M-03/05/07`) no cambian.
- `skips` y `estratos_excluidos` de v3: ambos vacíos — el cambio es
  únicamente de reparto de asientos, no dispara ninguna infactibilidad
  nueva (`tramite|P1|MEDIA` tiene a `TRA-M-02` como `publicada=NO`, sí
  factible).

Verificación mecánica de las dos afirmaciones anteriores:
`TestReporteInformativoV1_1.test_v3_hipotetico_agrega_tra_m_02_quita_civ_m_01`
(`tests_sorteo_v3.py`).

## 3 · Lo que esta nota NO hace

No re-sortea v1_1 (opción A, `FP-213`, se acepta tal cual — declarado en el
encargo). No toca `marco-M-sorteado-v1_1.tsv`, `marco-M-sorteado-v1_0.tsv`
ni `marco-congelado-piloto-v1_0.tsv` (verificado, `git diff --stat` vacío
contra los tres). No edita `sorteo_v2.py`, `sorteo_marco_m.py` ni
`sorteo_marco_m_v1_1.py` (verificado, `git diff --stat` vacío contra los
tres). No decide si mesa debe re-sortear alguna vez — presenta el costo
exacto (1 fila entra, 1 fila sale) para que esa decisión, si llega, no sea
a ciegas.
