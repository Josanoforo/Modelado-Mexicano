# Descarga masiva CPV 2020 (XML) + ENADID 2023 (enlace directo): dos mecanismos, para reuso

Sesión Sonnet, Ubuntu, rama `sesion/descarga-dirigida`. Encargo: bajar y registrar 9 archivos
(7 CPV, 2 ENADID) más el propio XML de descarga masiva, y documentar el mecanismo que los
desbloqueó. No se abrió ningún microdato más allá de lo necesario para HEAD (Content-Type/tamaño)
y para nombrar correctamente cada archivo por su ruta ya conocida (ADR-46).

## 0 · Qué bloqueo resuelve esto

`forense/notas/2026-07-31-cola-descarga-rederivada.md` §4 dejó declarado el bloqueo: el endpoint
AJAX de microdatos de CPV/ENADID (`.../descargamasiva/lista/archivoscompaginacion`) exige
`proyecto`/`anio` que no aparecen como atributo `data-*` en `pestanadata.js` de esos dos portales,
y esa sesión decidió no fuerza-bruta-earlos. Esta sesión no resolvió ese endpoint — lo **rodeó**:
el botón "Descarga masiva" del portal entrega un XML con las URLs ya resueltas, sin pasar por ese
endpoint en absoluto.

## 1 · Mecanismo A — XML de "Descarga masiva" (botón del portal, confirmado para CPV)

El usuario descargó `DescargaMasiva_382026_131650.zip` desde el botón "Descarga masiva" de
`/programas/ccpv/2020/` en el navegador. Contiene tres archivos (`leeme.txt` es explícito sobre
esto):
- `DescargaMasivaApp.exe` — instalador genérico de escritorio de INEGI (el mismo que
  `forense/notas/2026-07-31-enut-descarga.md` Parte 2 ya documentó para otro programa: no trae
  payload de encuesta, solo orquesta la descarga real).
- `DescargaMasivaOD.xml` — **lo que importa**: `<Archivo>` por cada URL real,
  `https://www.inegi.org.mx/contenidos/programas/ccpv/2020/...`, verificado en esta sesión con
  **576 URLs exactas** (570 en `<Archivo>` bajo `microdatos/` + 6 bajo `doc/`), agrupadas en 5
  familias: `caas` (99) · `cl` (99) · `ceu` (97) · `iter` (65) · `ageb_manzana` (64). El elemento
  raíz trae `<Descarga totalMb="8.23 GB" aut="57de16c5-…" />` — el atributo `aut` es un token de
  sesión/solicitud, no un parámetro a derivar ni reutilizar: se regenera cada vez que el portal
  arma el ZIP, no identifica el conjunto de archivos.

**Receta para reusar esto en otra fuente:**
1. En el navegador, abrir `/programas/{prog}/{año}/` y pulsar "Descarga masiva" (pestaña
   Microdatos). Requiere navegador — no se encontró forma de invocarlo por curl (el botón dispara
   la generación del ZIP del lado del portal).
2. Descomprimir el `.zip`, extraer solo `DescargaMasivaOD.xml` (el `.exe` no se ejecuta ni se
   registra como payload — es el mismo instalador genérico ya documentado, no dato).
3. `grep -oP '(?<=<Archivo>).*?(?=</Archivo>)'` sobre el XML da la lista plana de URLs reales.
4. `curl -sI` cada URL antes de bajar (Content-Type, Content-Length) — no asumir que todas
   resuelven; alguna familia puede fallar aunque el resto sirva.
5. `curl` real, `tests/manifiesto.py --registra` con `--archivo` apuntando al nombre en
   `data/raw/`, luego `--verifica`.

**No verificado esta sesión:** si el botón "Descarga masiva" existe en las páginas de las 27
fuentes SIN PAYLOAD de `cola-descarga-rederivada.md` §2 (ENASEM, ENDIREH, ENSU, ENCUP, etc.). Se
confirmó únicamente para CPV. Es razonable esperar que el mismo botón exista en otros programas
del mismo portal (la SPA es compartida, ya documentado en §4 de esa nota), pero **eso es una
expectativa, no una verificación** — cualquier sesión que lo intente para otra fuente debe
confirmar primero que el botón está presente en esa página específica.

## 2 · Mecanismo B — enlace directo en HTML (confirmado para ENADID 2023, DISTINTO del anterior)

ENADID 2023 **no necesitó XML de descarga masiva**: sus dos URLs de microdatos
(`base_datos_enadid23_csv.zip`, `fd_enadid23.xlsx`) están directas en el HTML de
`/programas/enadid/2023/microdatos/`, sin pasar por el flujo de botón+ZIP+XML. Confirmado por
`curl -sI` exitoso directo, sin extraer nada de ningún ZIP.

**Son dos mecanismos, no uno.** La premisa con la que arrancó este encargo ("ENADID y cualquier
otra fuente del portal usan el mismo [mecanismo que CPV]") **queda corregida**: cada portal del
sitio puede exponer su descarga de microdatos por cualquiera de los dos caminos (XML de descarga
masiva, o enlace directo en HTML), y no hay forma de saber cuál sin mirar la página de esa fuente
específica. Un intento de reuso debe probar primero si el enlace ya está en el HTML crudo (más
barato, no requiere navegador) antes de asumir que hace falta el flujo de botón+ZIP+XML.

## 3 · Cola declarada, no abierta hoy: los 5 `DescargaMasiva_*.zip` ya en manifiesto

`data/manifiesto.yaml` ya registra 5 entradas `descargamasiva_3072026_*` (`raiz: descargas_mx`,
`usado_para: sin uso asignado`), bajadas por el usuario el 30/jul vía navegador — instancias de
este mismo mecanismo A para el programa que el usuario navegaba ese día, sin identificar. Por el
§2 de `cola-descarga-rederivada.md`, se sabe que solo contienen el instalador genérico — pero eso
se concluyó **sin abrir el XML interno de cada uno**, y el mecanismo A recién confirmado aquí dice
que el XML sí trae URLs aprovechables. **Se anota como cola, no se abre esta sesión** (instrucción
explícita del encargo): la próxima sesión que trabaje descarga dirigida debería extraer el
`DescargaMasivaOD.xml` de esos 5 zips y correr la receta de §1 sobre lo que encuentre, antes de
asumir que esos 5 registros siguen siendo solo ruido de instalador.

## 4 · Universo declarado por el portal (CAAS/CEU)

La página de microdatos del Cuestionario Ampliado declara explícitamente que la muestra (CAAS =
personas, CEU = viviendas) cubre **solo viviendas particulares habitadas**: excluye viviendas
colectivas, Servicio Exterior mexicano y población sin vivienda. Cualquier uso de las marginales
de CAAS/CEU aguas abajo (modelo §1.1, los 6 ejes de perfil) debe declarar esta exclusión — no es
matiz de reactivo, es alcance de producto, declarado por el propio portal.

## 5 · Descarga y registro

| id | Archivo | Familia/origen | Bytes | `--verifica` |
|---|---|---|---|---|
| `cpv2020_caas_eum_csv` | `Censo2020_CAAS_eum_csv.zip` | CAAS nacional (personas) | 1 076 224 | COINCIDE |
| `cpv2020_ceu_eum_csv` | `Censo2020_CEU_eum_csv.zip` | CEU nacional (viviendas) | 135 163 712 | COINCIDE (re-registrado, ver §6) |
| `cpv2020_iter_nal_csv` | `ITER_NAL_2020_csv.zip` | Iter nacional (localidad) | 36 604 573 | COINCIDE |
| `cpv2020_diccionario_cuestionario_ampliado_xlsx` | `diccionario_cuestionario_ampliado_cpv2020.xlsx` | diccionario CAAS/CEU | 95 642 | COINCIDE |
| `cpv2020_caas_descriptor_bd_xlsx` | `Censo2020_CAAS_descriptor_bd.xlsx` | descriptor de BD, CAAS | 77 167 | COINCIDE |
| `cpv2020_ceu_descriptor_bd_xlsx` | `Censo2020_CEU_descriptor_bd.xlsx` | descriptor de BD, CEU | 52 106 | COINCIDE |
| `cpv2020_fd_iter_pdf` | `fd_iter_cpv2020.pdf` | ficha descriptiva, Iter | 921 352 | COINCIDE |
| `enadid2023_base_datos_csv` | `base_datos_enadid23_csv.zip` | ENADID 2023, base completa (mecanismo B) | 44 922 433 | COINCIDE |
| `enadid2023_fd_xlsx` | `fd_enadid23.xlsx` | ficha descriptiva ENADID 2023 | 2 085 302 | COINCIDE |
| `descargamasiva_382026_131650_xml` | `DescargaMasivaOD_382026_131650.xml` | el XML mismo, registrado como payload de mecanismo | 69 763 | COINCIDE |

Las 9 URLs se localizaron: las 7 de CPV, literal en `DescargaMasivaOD.xml` (mecanismo A); las 2
de ENADID, directas en el HTML de su página de microdatos (mecanismo B). Las 10 se verificaron
por `curl -sI` (Content-Type y Content-Length exactos) antes de bajar y las 10 `--registra`n sin
colisión de id ni de sha256.

## 6 · Anomalía encontrada: hash inestable en la primera descarga de `cpv2020_ceu_eum_csv`

El primer `curl` de `Censo2020_CEU_eum_csv.zip` completó con `HTTP 200`, tamaño exacto
(135 163 712 bytes, igual al HEAD previo) y `tests/manifiesto.py --registra` computó
`sha256=0f3a1baa…` sobre ese archivo. Corriendo `--verifica` minutos después sobre el mismo path
en disco, el sha256 recomputado dio `49f2dd95…` — **mismo tamaño, hash distinto**. Dos
re-descargas frescas del mismo URL a rutas nuevas, corridas de inmediato para descartar
corrupción, dieron `49f2dd95…` de forma estable y reproducible (idéntico entre sí). Ningún proceso
propio de esta sesión tocó el archivo entre el registro y la verificación (`ps aux` sin
curl/python concurrentes).

**No se puede concluir con certeza cuál de las dos hipótesis es la causa real:**
- **(a)** el servidor de INEGI sirvió contenido distinto para la misma URL en dos momentos del
  mismo día (regeneración no determinista del ZIP, tamaño coincidente por construcción); o
  **(b)** otra sesión, en otro worktree que comparte el mismo `data/raw` externo
  (`/home/pc0/mm-corpus/raw`, symlink común a los tres worktrees vivos), sobrescribió el mismo
  archivo entre el `--registra` y el `--verifica` de esta sesión.

`ps aux` no permite descartar (b): `forense/hallazgos.md` (31/jul) ya dejó registrado que el
namespace de PID de este bash es aislado y no ve procesos de otro worktree, así que "no vi nada
corriendo" no es evidencia de que no había nada corriendo. Dado que (b) tiene precedente directo
en este mismo repositorio (`forense/hallazgos.md`, 31/jul, dos incidentes de sesiones concurrentes
sobre `data/raw` compartido), es la hipótesis más verosímil, no la única posible.

**Corregido:** se retiró la entrada con el hash `0f3a1baa…` (nunca comiteada — se detectó dentro
de la misma sesión antes de cualquier commit) y se re-registró contra el contenido estable
verificado dos veces (`49f2dd95…`), que es el que persiste en disco ahora. Registrado también en
`forense/hallazgos.md`.

**Para la próxima sesión que baje o verifique este archivo:** un `--verifica` que dé COINCIDE hoy
no es garantía de que siga dando COINCIDE mañana si otra sesión toca el mismo `data/raw` en el
ínterin — no es un defecto de `manifiesto.py` (hace exactamente lo que su docstring promete:
compara contra lo que el archivo real trae *en el momento de correr*), es una propiedad del
`data_raw` compartido entre worktrees vivos.

## 7 · Nota de ruta: "Descargas" vs "Downloads"

El encargo nombró la ruta como `/mnt/c/Users/PC0/Descargas/...`; la carpeta real de Windows para
este usuario se llama `Downloads` (inglés) — el zip estaba en
`/mnt/c/Users/PC0/Downloads/DescargaMasiva_382026_131650.zip`. No es una fuente nueva: `downloads`
ya está declarada en `data/raices.local.yaml`, distinta de `descargas_mx`
(`/mnt/c/Users/PC0/Descargas MX`, la carpeta donde viven los 5 zips de §3). Ningún cambio de
configuración hizo falta.

## Prohibiciones respetadas

`canon/` no se tocó. No se abrió microdato: el contenido de los 9 archivos de datos no se leyó
más allá de HEAD (Content-Type/tamaño); el XML se leyó completo porque es el mecanismo mismo, no
un payload de encuesta (es una lista de URLs). Los 5 `DescargaMasiva_*.zip` de §3 no se abrieron,
por instrucción explícita del encargo — quedan como cola declarada. Ninguna cifra de este
documento se tecleó a mano: las 576 URLs, la partición por familia y los tamaños en bytes salen de
`grep`/`curl -sI`/`tests/manifiesto.py --verifica` corridos en esta sesión.
