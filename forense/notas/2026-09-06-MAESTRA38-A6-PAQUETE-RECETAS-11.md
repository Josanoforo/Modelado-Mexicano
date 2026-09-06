# PAQUETE-RECETAS-11 · ACTO MAESTRA38-A6

Producido por `ACTO MAESTRA38-A6 · RE-SONDEO-DE-NEGATIVOS-CON-CAPACIDAD-COMPLETA`,
6/sep/2026, contra `ef9ba36`.

**Criterio de inclusión, y es estrecho a propósito.** Aquí entra **sólo** lo
que exige **cuenta, sesión o solicitud escrita**. La caja baja todo lo
público, y en esta corrida bajó 34 payloads que actos anteriores habían
rotulado como imposibles — así que una fila en este paquete significa
«barrera humana real», no «no lo intentamos».

Cada receta es ejecutable por una persona o por Claude in Chrome en ≤ 1 minuto.

---

## 1 · `RUPC` — Registro Único de Proveedores y Contratistas

**Razón: `EXIGE-SESION-NAVEGADOR`.** Medido: el host responde y sirve esta
familia de backends (control positivo
`/adele/interoperabilidad/tp/reloj` → `200 application/json`, 104 B), pero
las rutas del RUPC devuelven `403 {"error":"Acceso no permitido."}`.

1. Abrir `https://comprasmx.buengobierno.gob.mx/sitiopublico/`
2. Entrar a **Proveedores y contratistas** → **Consulta del RUPC**.
3. Con la sesión ya abierta (cookie puesta por el SPA), el backend
   `https://upcp-cnetservicios.buengobierno.gob.mx/backends/rose` deja de
   responder 403.
4. Exportar el listado. Archivo esperado: un `.xlsx` o `.csv` de proveedores
   con `Folio en el RUPC` — la llave que la fila `EXT_OF_07` necesita para
   cerrar «persona + sanción».

**Ojo, dato nuevo de este acto:** el host histórico
`upcp-cnetservicios.funcionpublica.gob.mx` **ya no resuelve** (`curl 6`). El
servicio migró a `…buengobierno.gob.mx`. Toda receta anterior que apunte al
dominio viejo está muerta por dominio, no por permiso.

## 2 · `DD_COMPRANET_DICCIONARIOS_DE_DATOS` — los tres diccionarios

**Razón: `EXIGE-SESION-NAVEGADOR`** (SPA Angular sin enlace estático; el
bundle de 2 647 141 B no contiene ni una cadena `DD_`).

1. Abrir `https://comprasmx.buengobierno.gob.mx/datos-abiertos`
2. Esperar a que el Angular pinte la lista (con JS; `curl` sólo ve 7 000 B de shell).
3. Descargar los tres `DD_*.xlsx` del bloque «Diccionarios de datos».
4. Archivos esperados: tres `.xlsx`, uno por cada tabla de la serie de contratos.

## 3 · `CNBV_PORTAFOLIO_INFORMACION_IMOR_CONSUMO` y la fila `PI`

**Razón: postback ASP.NET** (no es cuenta — es que el reporte se arma con
`__VIEWSTATE`, y `curl` no lo reproduce en ≤ 1 min).

**Prerrequisito técnico que este acto resolvió y hay que conservar:** el
servidor de CNBV **no manda el intermedio** `GlobalSign RSA OV SSL CA 2018`.
Cualquier cliente estricto aborta con `curl 60` **antes de hablar HTTP**. Los
navegadores lo salvan solo (AIA fetching); `curl` necesita:

```
curl -sS http://secure.globalsign.com/cacert/gsrsaovsslca2018.crt -o gs.crt
openssl x509 -inform DER -in gs.crt -out gs.pem
cat /etc/ssl/certs/ca-certificates.crt gs.pem > ca_cnbv.pem
curl --cacert ca_cnbv.pem https://portafolioinfo.cnbv.gob.mx/
```

Receta de navegador:

1. Abrir `https://portafolioinfo.cnbv.gob.mx/Paginas/InicioModoExcel.aspx`
2. **Banca Múltiple** → **Cartera** (o directo:
   `…/Paginas/Reporte.aspx?s=40&t=26&st=0&ti=0&sti=0&n=0&tp=0`).
3. Elegir **IMOR** y desagregar por **tipo de cartera de consumo**
   (no garantizada / tarjeta vs. garantizada), periodicidad mensual.
4. Botón de exportar a Excel. Archivo esperado: un `.xlsx` de serie mensual.

## 4 · `ENCRIGE_2020_FD_COMPLETO_MAS_CONDUSEF` — la mitad ENCRIGE

**Razón: `URL-NO-LOCALIZADA`** — no hay barrera de permiso; es que la página
de programa es shell JS y las URL por convención dan soft-404.

**Control que este acto dejó medido, y que evita el falso positivo:**
`www.inegi.org.mx/contenidos/…` sirve **`200` con 2 263 B** para cualquier
ruta inexistente, y `www.inegi.org.mx/programas/<inexistente>/2020/` sirve
**`200` con 13 370 B**. Un `200` de INEGI no es éxito: hay que comparar el
tamaño contra estos dos controles antes de aceptarlo.

1. Abrir `https://www.inegi.org.mx/programas/encrige/2020/` **con JS activo**.
2. Pestaña **Microdatos** (o **Documentación** para el FD).
3. Copiar el enlace real que el JS inyecta — ése es el que ninguna
   convención de URL adivina.
4. Archivo esperado: FD en `.pdf` y/o microdato en `.zip`.

## 5 · `OECD` — sólo el PUM (microdato), no los indicadores

**Razón: `EXIGE-SOLICITUD-ESCRITA`.** Los **indicadores** ya NO necesitan
receta: este acto los bajó por API pública (ver `a6_oecd_tdg_2025_csv`,
`a6_oecd_public_integrity_csv`). Lo único que sigue tras muro es el
**public use microdata** del Trust Survey.

1. Abrir `https://www.oecd.org/en/about/programmes/trust-survey.html`
2. Formulario de acceso al PUM → enviar a `govtrustinfo@oecd.org`.
3. Revisión discrecional, sin plazo publicado. **No hay archivo esperado
   hoy**: es una solicitud, y decir eso es el entregable.

---

## Cierre del paquete

- Filas que este acto cerró en `NO-OBTENIDO-POR-ESTE-AGENTE`: **3**
  (`PI`, `RUPC`, `DD_COMPRANET_DICCIONARIOS_DE_DATOS`), todas con ≥ 4 rutas
  y salida cruda pegada en la nota de su fila.
- Filas que este acto **sacó** de un rótulo negativo: **2**
  (`SICEE`, `BASE_DE_EVENTOS_DE_PROTESTA_EN_MEXICO` → `OBTENIDO`).
- Filas que subieron a `OBTENIDO-PARCIAL` desde `NO-ACCESIBLE` o
  `PENDIENTE-DE-MESA`: **3** (`OECD`, `DENUNCIA_VINCULADA_CON_TENENCIA_DE_SEGURO`,
  `ENCRIGE_2020_FD_COMPLETO_MAS_CONDUSEF`).
- Recetas en este paquete: **5**.
