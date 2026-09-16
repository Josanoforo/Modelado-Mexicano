# ENIF 2024 · recibe dinero de familiares para la vejez — pre-registro congelado de `CALC-DINERO-FAMILIARES-VEJEZ-0001`

### `prereg-caja-ENIF-DINERO-FAMILIARES-VEJEZ` · **v1.0** · 15 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/ENIF-DINERO-FAMILIARES-VEJEZ-spec-v1_0.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-ENIF-DINERO-FAMILIARES-VEJEZ`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Registro `D-15` de una medición **ya corrida y sellada**: `recibe_dinero_familiares_para_vejez` / `no_recibe_dinero_familiares_para_vejez` (`familia.apoyo.recibe_dinero_familiares`, `milpa/tramite.yaml:833-834`), medida por `ACTO MAESTRA32-E18 · REGLAS-OLA5-FASE1` (`tools/tasas_base_fase1.py`, 31/ago/2026). Releva `CORR-0010` (`RES-0033`, `RES-0034`) resolviendo el bloqueador `IDENTIDAD-DE-PAYLOAD` **por hash de contenido (A.7)**, sin tocar `milpa/`. |
> | **QUÉ NO ES** | No corrige `milpa/tramite.yaml:845` (`payload_manifiesto_id: "NO-LOCALIZADO — ..."`) — esa corrección es `FUERA-DE-PERÍMETRO` de este acto (`NC-0195`, abierta por `ACTO GEN2-SPECS-DEMANDA-1`): la resuelve el acto que toque `milpa/`. No re-ejecuta el medidor. No adopta la cifra a ningún veredicto (la regla ya está `SELLADA`, tier `FUERTE`; este `CALC` solo le da cadena `E.2` en el registro GEN2). |
> | **VERIFICAS ASÍ** | `sha256sum data/raw/enif_2024_bd_csv.zip` (o el payload resuelto por manifiesto) da `00e4b0b42775276b2da236a5bba8c64dc5a92c289908a4727dec93dc7684f039` — **exactamente** el `sha256_payload` que la regla ya declara en `milpa/tramite.yaml:844`, y **exactamente** la entrada `enif_2024_enif_2024_bd_csv` de `data/manifiesto.yaml:5543-5550`. La identidad se resuelve por ese hash, nunca por el `id` textual que la regla escribió (`NO-LOCALIZADO`, buscando otro nombre). |

**Acto:** `ACTO GEN2-SPECS-DEMANDA-2`, 15/sep/2026, entorno **NUBE**, sobre `origin/main = da9b47a361143d408cd9fd9c20d17b101c4fe381`.

**Regla consumidora:** `familia.apoyo.recibe_dinero_familiares` (`milpa/tramite.yaml:827`), `situacion: SELLADA`, `tier: FUERTE`.

---

## 0 · A.7 — resolución de identidad por hash, no por nombre

### 0.1 · El bloqueador, verbatim

`data/corrida0/demanda-corridas.tsv:CORR-0010` cita `instrumento`:

```
ENIF2024	NO-LOCALIZADO -- se uso data/raw/enif_2024_bd_csv.zip (trae TMODULO.csv
con FILTRO_S9_1/P9_9_4/FAC_PER/EDAD_V); el id de manifiesto enif2024_csv
apunta a un ZIP distinto (data/raw/enif2024_csv.zip) sin estas columnas
confirmadas en este acto
```

`milpa/tramite.yaml:845` repite el mismo `NO-LOCALIZADO` en
`payload_manifiesto_id`. El bloqueo nace de **buscar por `id` de
manifiesto** (`enif2024_csv`, que resuelve a otro ZIP,
`data/raw/enif2024_csv.zip`) en vez de por el `sha256_payload` que la
propia regla ya trae.

### 0.2 · La resolución, con comando a la vista

```
$ grep -n "sha256_payload" milpa/tramite.yaml | grep -A0 -B0 "00e4b0b4"
    sha256_payload: "00e4b0b42775276b2da236a5bba8c64dc5a92c289908a4727dec93dc7684f039"   # familia.apoyo.recibe_dinero_familiares
$ grep -n "00e4b0b42775276b2da236a5bba8c64dc5a92c289908a4727dec93dc7684f039" data/manifiesto.yaml -B5
5543:- id: enif_2024_enif_2024_bd_csv
5544-  usado_para: sin uso asignado
...
5549-  archivo: enif_2024_bd_csv.zip
5550-  sha256: 00e4b0b42775276b2da236a5bba8c64dc5a92c289908a4727dec93dc7684f039
```

**Coincidencia exacta.** El `sha256_payload` que la regla declara **es** el
`sha256` de la entrada `enif_2024_enif_2024_bd_csv` del manifiesto —
`archivo: enif_2024_bd_csv.zip`, descargado el 5/ago/2026 vía `curl` desde
`inegi.org.mx`, `3 131 148` bytes. Es el **mismo payload** que
`data/raw/enif_2024_bd_csv.zip` (el ZIP que `demanda-corridas.tsv` dice que
"se usó"), identificado por contenido, no por el `id` textual que no
coincidía. Mismo patrón exacto que `NC-0188` (ENNViH) y que el hallazgo (4)
de `ACTO GEN2-SPECS-DEMANDA-1` sobre `CORR-0010` mismo (`enif_2024_bd_csv`
↔ `enif2024_csv` son ZIPs distintos; el correcto es el primero).

### 0.3 · Por qué esta spec no edita `milpa/`

`milpa/tramite.yaml:845` sigue diciendo `NO-LOCALIZADO` en la letra. Eso es
`FUERA-DE-PERÍMETRO` de este acto (`NC-0195`, `ACTO GEN2-SPECS-DEMANDA-1`,
`ABIERTA`): la corrección de esa línea la hace el acto que toque `milpa/`
(CAJA o mesa). Esta spec **no** espera esa corrección para congelar — la
identidad ya está resuelta por hash, con cita, y eso basta para dar a
`RES-0033`/`RES-0034` su capa `D-15` sin tocar el sellado.

---

## 1 · Payload y medición original

| campo | valor |
|---|---|
| payload | `enif_2024_enif_2024_bd_csv` (resuelto por hash, §0), `sha256=00e4b0b42775276b2da236a5bba8c64dc5a92c289908a4727dec93dc7684f039` |
| script original | `tools/tasas_base_fase1.py` (`ACTO MAESTRA32-E18 · REGLAS-OLA5-FASE1`, spec `forense/notas/2026-08-31-reglas-fase1-spec.md`) |
| unidad | PERSONA |
| universo | `FILTRO_S9_1=2` (aplica módulo vejez) y `EDAD_V<71` |
| ponderador | `FAC_PER` |
| diseño | **sin campo de diseño UPM/estrato reproducible** dentro del perímetro del acto original (declarado en su propia cabecera) — IC95 por bootstrap ponderado simple, `n_boot=10000`, `seed=42`, sin conglomerado |
| n | 11 895 |
| punto | `recibe_dinero_familiares_para_vejez = 0.457707`, IC95 `[0.444232, 0.470782]` |
| complemento | `no_recibe_dinero_familiares_para_vejez = 0.542293` — contado directamente |

---

## 2 · `resultados` que releva

`RES-0033`, `RES-0034`. `CORR-0010` queda **agotada** (2/2).

## 3 · Qué NO hace este acto

No re-corre `tools/tasas_base_fase1.py`. No edita `milpa/tramite.yaml`
(`E.3`, y además `FUERA-DE-PERÍMETRO`, `NC-0195`). No cierra `NC-0195` —
esa fila permanece `ABIERTA` hasta que el acto que toque `milpa/` corrija
la letra.

**El primer resultado que produjo este procedimiento —en `ACTO
MAESTRA32-E18`, no aquí— es el que se reporta.**
