# ENCUP — cadena TLS incompleta, resuelta por reparación honesta (no por certificado fijado)

**Contadores movidos: 0.** Sin módulo de auditoría. Este acto no lee, no mide, no adjudica ningún constructo — es logística de descarga y registro de procedencia.

Encargo L, mesa #18, emitido 4/ago/2026. Base declarada: `main` = `642be97`.

## 0 · Entorno

```
$ python3 tests/bitacora.py --abre
HEAD:         642be976c748f6e91a7888aceeb532e881fa100a
origin/main:  642be976c748f6e91a7888aceeb532e881fa100a
Divergencia:  ninguna — HEAD == origin/main
check.py --baseline:        exit=0 · LÍNEA BASE: VERDE
validador_registro_ids.py:  exit=0 · OK

$ echo "${CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE:-sin_variable}"
sin_variable

$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://fomentocivico.segob.gob.mx/
000
```

El `000` de la sonda **no es NO ALCANZABLE** — es exactamente el síntoma
que el encargo anticipa: `curl` sin `-k` rechaza la conexión porque la
cadena de certificado no verifica (ver §2 abajo). El `CONNECT` del proxy
de salida sí completa. Sonda corrida sin `-I`, tal como exige el
protocolo.

```
$ ls data/raw | wc -l
1   (existía vacío en este worktree nuevo, no es PARO)
```

Este acto corrió en un worktree nuevo (`git worktree add`, rama
`sesion/encup-certificado-fijado`) apuntando a `origin/main` en
`642be97`. El primer intento de crearlo falló con `error: could not lock
config file .git/config: File exists` — escritura concurrente de otra
sesión sobre el mismo `.git/config` del checkout compartido (mismo
patrón que `I-11`, ya visto dos veces en este corpus); reintentado tras
limpiar el lock stale, quedó creado. No se pegó la ruta real de
`data/raw` en esta nota ni se pegará en el PR.

## 1 · Premisas

| # | Premisa | Verificación |
|---|---|---|
| PL-1 | ENCUP responde pero con cadena TLS no verificable desde este entorno | **Sostiene.** `forense/notas/2026-08-04-barrido-alcanzabilidad-27fuentes.md` §4. Re-verificado abajo, causa nombrada con más detalle del que esa nota dio (no abrió `openssl s_client`, solo `curl -k`) |
| PL-2 | El barrido localizó `BaseDatos_ENCUP_2012_Final.xlsx` real, `Content-Range: bytes 0-0/4814178` (~4.8 MB), y cinco cuestionarios | **Sostiene, re-verificado.** Mismo `Content-Range` exacto obtenido en esta sesión, esta vez con verificación TLS activa (§2.4) |
| PL-3 | ENCUP está descontinuada; última edición 2012 | **Sostiene.** Portal (`/es/FomentoCivico/ENCUP`, HTML leído en esta sesión con verificación activa) no lista edición posterior a `Cuestionario-Quinta_2012_ENCUP.pdf` / `BaseDatos_ENCUP_2012_Final.xlsx` |
| PL-4 | No hay ninguna entrada `encup*` en el manifiesto | **Sostiene.** `grep -i encup data/manifiesto.yaml` antes de este acto: cero resultados (196 ids totales al abrir) |
| PL-5 | hitoE la nombra posición 9, candidata a `confianza_institucional[electoral]` | **Sostiene.** `forense/hitoE-campana-medicion-v2_0.md:292` |

Ninguna premisa (1) cayó. Se continúa.

## 2 · El acto

### 2.1 · Caracterización de la cadena

`openssl s_client` sin más no resuelve el DNS desde este entorno
(`Temporary failure in name resolution` — el entorno enruta HTTPS por un
proxy HTTP local que `curl` toma de `HTTPS_PROXY`/`https_proxy`, pero que
`s_client` no usa por defecto). Se repitió con `-proxy` (soportado por
OpenSSL 3.5, el proxy de salida configurado en el entorno) para llegar al
host real:

```
$ openssl s_client -connect fomentocivico.segob.gob.mx:443 \
    -servername fomentocivico.segob.gob.mx -proxy localhost:3128 \
    -proxy_user srt -proxy_pass pass:<redactado> -showcerts </dev/null
Certificate chain
 0 s:CN=*.segob.gob.mx
   i:C=US, ST=Arizona, L=Scottsdale, O=GoDaddy.com, Inc., CN=Go Daddy Secure Certificate Authority - G2
Verification error: unable to verify the first certificate
Verify return code: 21 (unable to verify the first certificate)
```

**Un solo certificado en la cadena enviada por el servidor** — el hoja,
sin el intermedio. Diagnóstico, con causa nombrada, no solo constatada:

- **No es autofirmado** — el emisor (`Go Daddy Secure Certificate
  Authority - G2`) es distinto del sujeto.
- **No es una CA no reconocida** — es una CA comercial ampliamente
  distribuida.
- **Es cadena incompleta del lado del servidor**: el servidor (Oracle
  GlassFish 3.1.2.19, el mismo motor viejo que sirve los documentos) no
  envía el certificado intermedio. `curl` sin `-k` falla con `SSL
  certificate OpenSSL verify result: unable to get local issuer
  certificate (20)` — mismo hecho, mismo diagnóstico, confirmado por dos
  herramientas independientes.

Certificado hoja:

- Sujeto: `CN=*.segob.gob.mx`
- Emisor: `CN=Go Daddy Secure Certificate Authority - G2` (GoDaddy.com, Inc.)
- Validez: `2026-03-05` a `2026-09-19`
- Huella SHA-256: `72:39:61:7A:02:C2:4F:13:4D:0D:36:06:19:C9:F1:55:C7:FC:CD:38:B7:C0:A2:1F:94:60:62:1F:86:93:6A:70`

### 2.2 · Reparación honesta — funcionó

El propio certificado hoja declara, en su extensión *Authority
Information Access*, la URL pública de su emisor:

```
Authority Information Access:
    CA Issuers - URI:http://certificates.godaddy.com/repository/gdig2.crt
```

Se descargó ese intermedio (HTTP simple, sin TLS que verificar en ese
paso — es la ruta que cualquier navegador usa quietamente para AIA
fetching) y se contrastó contra el almacén de CA del sistema:

```
$ openssl verify -untrusted gdig2.pem encup_leaf.pem
encup_leaf.pem: OK
```

**La verificación pasó, contra el almacén de CA del sistema, sin
desactivar ninguna comprobación.** El intermedio (`Go Daddy Secure
Certificate Authority - G2`, huella SHA-256
`97:3A:41:27:6F:FD:01:E0:27:A2:AA:D4:9E:34:C3:78:46:D3:E9:76:FF:6A:62:0B:67:12:E3:38:32:04:1A:A6`,
válido `2011-05-03`–`2031-05-03`) encadena a `Go Daddy Root Certificate
Authority - G2`, que el sistema ya reconoce. **Esto lo dice el propio
protocolo del encargo, §2.2, y ocurrió: no hay problema TLS que
resolver mediante anclaje a un certificado desconocido — era un servidor
mal configurado** (no sirve su intermedio), y con la cadena completada la
descarga es normal, verificada, contra la misma autoridad de siempre.
**No hizo falta fijar el certificado (§2.3 del encargo no se ejecutó
porque §2.2 ya resolvió el caso.)**

### 2.3 · Descarga, con verificación activa, sin `-k`

Con `--cacert` apuntando a un bundle que es el almacén de CA del sistema
más el intermedio recién obtenido (nunca `-k`/`--insecure`), se
re-verificó el payload principal:

```
$ curl -s --cacert system_plus_gdig2.pem -o /dev/null -D - -r 0-0 \
  https://fomentocivico.segob.gob.mx/work/models/FomentoCivico/Documentos/PDF/CultDemo/BaseDatos_ENCUP_2012_Final.xlsx
HTTP/1.1 206 Partial Content
Content-Range: bytes 0-0/4814178
```

Coincide exacto con `PL-2` (`4 814 178` bytes) — re-verificado, esta vez
con TLS activo, no con `-k` de diagnóstico como hizo el barrido del
4/ago. Se leyó también la página de portal (`/es/FomentoCivico/ENCUP`,
19 855 bytes, mismo tamaño que reportó el barrido) **con esta misma
verificación activa** para extraer los `href` reales de los cinco
cuestionarios — no adivinados, no reconstruidos por patrón:

```
Cuestionario_Primera_2001_ENCUP.pdf
Cuestionario_Segunda_2003_ENCUP.pdf
Cuestionario_Tercera_2005_ENCUP.pdf
Cuestionario_Cuarta_2008_ENCUP.pdf
Cuestionario-Quinta_2012_ENCUP.pdf
```

Cada uno de los seis (la base + los cinco cuestionarios) se verificó
antes de bajarlo con `curl -r 0-0` (rango de 1 byte, no `HEAD`) contra la
misma cadena reparada:

| Archivo | `Content-Range` | `Content-Type` |
|---|---|---|
| `BaseDatos_ENCUP_2012_Final.xlsx` | `0-0/4814178` | — (GlassFish no lo declara para `.xlsx`) |
| `Cuestionario_Primera_2001_ENCUP.pdf` | `0-0/147691` | `application/pdf` |
| `Cuestionario_Segunda_2003_ENCUP.pdf` | `0-0/233736` | `application/pdf` |
| `Cuestionario_Tercera_2005_ENCUP.pdf` | `0-0/116061` | `application/pdf` |
| `Cuestionario_Cuarta_2008_ENCUP.pdf` | `0-0/396678` | `application/pdf` |
| `Cuestionario-Quinta_2012_ENCUP.pdf` | `0-0/1026475` | `application/pdf` |

Ninguna dio la firma de soft-404 (2 263/13 370 bytes fijos). Los seis se
descargaron completos y el tamaño en disco coincidió exacto, byte a
byte, con el `Content-Range` verificado:

```
$ sha256sum data/raw/encup_*
bb33eedd… encup_2001_cuestionario_pdf.pdf   (147691 bytes)
acae1fe1… encup_2003_cuestionario_pdf.pdf   (233736 bytes)
c6f4a3c7… encup_2005_cuestionario_pdf.pdf   (116061 bytes)
df4337c8… encup_2008_cuestionario_pdf.pdf   (396678 bytes)
50341d97… encup_2012_base_datos_xlsx.xlsx   (4814178 bytes)
33be2b21… encup_2012_cuestionario_pdf.pdf   (1026475 bytes)
```

**Declaración explícita: en ningún paso de este acto se usó `-k` ni
`--insecure`.** La única vez que se leyó el sitio sin verificación fue en
la sesión previa del barrido (4/ago, con `-k`, declarado allí como "solo
para diagnóstico, no para tratar el contenido como confiable a ciegas");
esta sesión no repite ese paso — repara la cadena primero.

### 2.4 · No se abrió contenido

Los seis archivos se descargaron y se hashearon (`sha256sum`, y `file`
solo para confirmar la firma de tipo del `.xlsx` por cabecera de bytes,
no para leer una celda). **No se abrió ninguna hoja del `.xlsx` ni se
leyó texto de ningún PDF.** Este acto es logística de pre-registro
(§2.5 del encargo); abrir contenido lo habría contaminado (ADR-46(2)).

## 3 · Marca de procedencia que viaja

Cada una de las seis entradas nuevas en `data/manifiesto.yaml`
(`encup_2012_base_datos_xlsx`, `encup_2001_cuestionario_pdf`,
`encup_2003_cuestionario_pdf`, `encup_2005_cuestionario_pdf`,
`encup_2008_cuestionario_pdf`, `encup_2012_cuestionario_pdf`) lleva en su
campo `nota`:

- la causa exacta del fallo TLS (cadena incompleta, intermedio no
  servido) y que se resolvió por **reparación honesta**, no por
  certificado fijado;
- huella SHA-256 y validez del certificado hoja (`72:39:…:6A:70`,
  `2026-03-05`–`2026-09-19`) y del intermedio usado para completar la
  cadena (`97:3A:…:1A:A6`, `2011-05-03`–`2031-05-03`);
- que la verificación fue contra el almacén de CA del sistema con la
  cadena completa, sin desactivar ninguna comprobación, y que en ningún
  momento se usó `-k`/`--insecure`;
- que la fuente está **descontinuada, base 2012** — quien la use después
  ve esa fecha en la propia entrada, sin tener que buscarla.

`usado_para` en las seis declara, sin adjudicar nada, la candidatura de
hitoE §292 (posición 9, `confianza_institucional[electoral]`) y la
candidatura abierta a `deferencia` (hoy proxy vía Latinobarómetro,
`forense/notas/2026-08-03-cbis-deferencia-externas.md`) — ninguna leída
ni evaluada esta sesión.

## 4 · Suite

```
$ python3 tests/check.py --baseline
19 FAIL · 84 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json

$ python3 tests/validador_registro_ids.py
OK — 49 reglas · 27 en perímetro · 49 IDs verificados

$ python3 tests/manifiesto.py --verifica --id encup_2012_base_datos_xlsx
encup_2012_base_datos_xlsx [data_raw]: COINCIDE
$ python3 tests/manifiesto.py --verifica --id encup_2001_cuestionario_pdf
encup_2001_cuestionario_pdf [data_raw]: COINCIDE
$ python3 tests/manifiesto.py --verifica --id encup_2003_cuestionario_pdf
encup_2003_cuestionario_pdf [data_raw]: COINCIDE
$ python3 tests/manifiesto.py --verifica --id encup_2005_cuestionario_pdf
encup_2005_cuestionario_pdf [data_raw]: COINCIDE
$ python3 tests/manifiesto.py --verifica --id encup_2008_cuestionario_pdf
encup_2008_cuestionario_pdf [data_raw]: COINCIDE
$ python3 tests/manifiesto.py --verifica --id encup_2012_cuestionario_pdf
encup_2012_cuestionario_pdf [data_raw]: COINCIDE
```

Sin rojo nuevo, las seis COINCIDEN.

## 5 · HECHO

1. Causa del fallo TLS nombrada (cadena incompleta, intermedio GoDaddy G2
   no servido por el servidor) — no solo "no verificable".
2. Reparación intentada antes de fijar, y **funcionó**: intermedio
   obtenido de su URL pública AIA, verificación pasó contra el almacén
   de CA del sistema.
3. Descarga con verificación activa contra la cadena completada, en
   ningún momento `-k`/`--insecure`.
4. Huella y validez del certificado hoja y del intermedio, en el
   manifiesto (§3 arriba, campo `nota` de las seis entradas).
5. Marca de procedencia TLS y nota de fuente descontinuada (base 2012)
   en cada una de las seis entradas.
6. Contenido no abierto.
7. Suite VERDE (§4).
8. PR abierto, no fusionado (ver mensaje de cierre de este acto).

No hubo PARO: no hizo falta `-k`, la huella no cambió entre peticiones
(mismas huellas en las seis verificaciones de rango y en las seis
descargas completas), el host no redirigió a otro dominio, y ninguna
premisa (1) cayó.
