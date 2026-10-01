# PAQUETE-RECETAS-2026-10-01 · ADQ ENEM/EQD

Mandato: GEN2-38. Corte: 2026-10-01. Entorno: CAJA.

## ENEM_2024

- A.8: no hubo coincidencia por objeto/ola en `data/manifiesto.yaml`.
- Búsqueda web real: `"Encuesta Nacional Electoral de México" 2024 microdatos ENEM` y `"ENEM 2024" encuesta electoral México datos CIDE`.
- Resultado verificable: `https://tinyurl.com/MexicanElectionStudy2024` respondió `HTTP/2 301` y `location: https://drive.google.com/drive/folders/1lz_4A-fmWrxwwqO01cJsxNX7APpRI6V2?usp=drive_link`.
- Resultado de contenido: la convocatoria pública localizada dice literalmente que el cuestionario y reporte están en esa carpeta y que «La información para acceder a la base de datos se proporcionará una vez aceptada la propuesta». La carpeta pública respondió y contiene documentación, pero no se acreditó un microdato público descargable.
- Estado: `NO-OBTENIDO-POR-ESTE-AGENTE(5 intentos)`; intento efectivo 2026-10-01.
- Reactivación: publicación abierta del microdato ENEM 2024, incorporación de México a una entrega CSES que contenga esa ola, o autorización humana para presentar propuesta/contactar al custodio.
- Receta ≤1 minuto: abrir `https://tinyurl.com/MexicanElectionStudy2024`; revisar la carpeta; si se necesita el microdato, presentar una propuesta conforme a la convocatoria y aportar el acuse o enlace de acceso. Archivo esperado: base ENEM 2024 (no confundir con cuestionario/reporte).

## EQD-PANEL_2018

- A.8: no hubo coincidencia por objeto/ola en `data/manifiesto.yaml`.
- Búsqueda web real: `Greene Simpser Mexico 2018 panel survey data` y `"Mexico 2018" election panel Greene Simpser dataset`.
- Resultado verificable: la página pública de Kenneth Greene identificó “Mexico 2018 Panel Study” y enlazó la réplica DOI `10.7910/DVN/ESRIBE`; el API público de Harvard Dataverse enumeró `mx_2018_eqd_codebook.pdf` (file 6354285) y `mx_2018_eqd_stata12.tab` (file 6300448).
- Resultado de descarga: `API pública enumeró y descargó mx_2018_eqd_codebook.pdf (file 6354285) y mx_2018_eqd_stata12.tab (file 6300448); dos descargas por archivo fueron byte-idénticas; PDF termina en %%EOF.`
- Manifiesto: `eqd_panel_2018_codebook`; `eqd_panel_2018_microdato_tab`.
- Cobertura permitida: análisis del panel EQD México 2018 con su codebook y extracto tabular publicado en la réplica.
- Brecha: el nombre `_partial` aparece en otros archivos de la réplica, pero no en `mx_2018_eqd_stata12.tab`; aun así, adquisición no adjudica suficiencia científica, no acredita por sí sola selección/no respuesta, diseño causal ni equivalencia con otro panel.
