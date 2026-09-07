# ACTO MAESTRA38-L2 · MPS-2012 — elección de rama (A.8)

Comando exacto que dicta el encargo (corregido: no `grep -c` sobre el manifiesto),
corrido contra las tres raíces declaradas en `data/raices.local.yaml`
(`data_raw`, `descargas_mx`, `downloads`):

```
f=$(find /home/pc0/mm-corpus/raw "/mnt/c/Users/PC0/Descargas MX" "/mnt/c/Users/PC0/Downloads" -name "35024-0001-Data.dta" 2>/dev/null | head -1); echo "f=[$f]"; [ -n "$f" ] && md5sum "$f"
```

Salida:

```
f=[]
```

`find` examinó 2051 archivos en las tres raíces (`find ... -type f | wc -l` = 2051)
y no encontró ningún `35024-0001-Data.dta`. `$f` vacío → **RAMA TEXTO** (rama B).

Lo que sí está en el corpus para ICPSR 35024 (ninguno es el `.dta` completo):
- `academico_icpsr35024/icpsr35024_ds1_subconjunto_dataverse.tab` (el parcial)
- `35024_dats_2.2.json`, `35024-0001-Codebook-spanish.pdf.zip`
- `academico_icpsr35024/icpsr35024_mexico_panel_study_2012_paquete_v1.zip` (14.6 MB, 0 datos, `unzip -l` de A4)
- en `descargas_mx`: los tabulados T5-T13 (`ICPSR35024-ds1-w2-tabulados-T5-T9-derivados-2026-09-02.csv`, 647 filas, once tablas pese al nombre del archivo), su LEEME de procedencia, y `ICPSR_35024/35024-Questionnaire-spanish.pdf`.

A.8 — `ya_medido.py` sobre R7.3, R7.6, P3 (salida completa pegada en el commit;
resumen): R7.3 (`civico.voto.agencia_con_secreto`) — ADR-329 (MEDIA,
`se_mueve_si`=medición 1ª mano en `.dta`), L9/L11 CONTRARIA-REPLICADA, L12 P2
REPLICA-DE-SEGUNDA-MANO-NO-SELLADA. R7.6 (`civico.voto.clientelar_si_observable`)
— tercera CONTRARIA en el otro brazo (ADR-349, LOTE-LAPOP): no se reabre, se
compara. P3 (lista `civico.clientelismo.prevalencia_lista_listcran_mps2012`) —
ADR-350: p=0.187 primera mano en subconjunto `list::mexico`, N=1004, sin
ponderar; S10 §6: el veredicto sobre el `.dta` completo reemplaza, no promedia.
Los 34 payloads de alta de A6 (ADR-353) — ninguno es MPS; no cambia la rama.

**RAMA ELEGIDA: TEXTO (rama B).**
