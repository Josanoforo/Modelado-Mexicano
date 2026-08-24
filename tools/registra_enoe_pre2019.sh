#!/usr/bin/env bash
# ADQ-ENOE-PRE2019 · T1. Registra en data/manifiesto.yaml los payloads que este
# acto adquirio. sha256, tamano y entorno los deriva tests/manifiesto.py del
# archivo real -- aqui no se teclea ninguna cifra.
set -uo pipefail
cd "$(dirname "$0")/.."
M15="https://www.inegi.org.mx/contenidos/programas/enoe/15ymas"
USO="ADQ-ENOE-PRE2019 / llave (ii) ADR-57(c) -- antes/despues del decreto de la Zona Libre de la Frontera Norte (rige 1/ene/2019). Pendiente de pre-registro de diseno: adquirir no es disenar"
USOD="ADQ-ENOE-PRE2019 / T2 -- descriptor de instrumento por era, universo del barrido de los 9 constructos"
LIC="Terminos de Libre Uso de la Informacion del INEGI (https://www.inegi.org.mx/inegi/terminos.html)"
POR="ACTO ADQ-ENOE-PRE2019, 20/ago/2026, entorno UBUNTU, via tools/adq_enoe_pre2019.py (microdato) y tools/adq_enoe_docs.py / tools/adq_enoe_sonda_eras.py"
ok=0; ya=0; err=0

reg () {  # $1 id  $2 archivo  $3 url  $4 usado_para  $5 formato
  out=$(python3 tests/manifiesto.py --registra --id "$1" --archivo "$2" \
        --url-origen "$3" --usado-para "$4" --formato "$5" \
        --licencia "$LIC" --descargado-por "$POR" 2>&1)
  if [ $? -eq 0 ]; then echo "[ok] $1"; ok=$((ok+1))
  elif echo "$out" | grep -qi "ya existe\|ya está\|ya esta"; then echo "[ya] $1"; ya=$((ya+1))
  else echo "[XX] $1 :: $(echo "$out" | tail -2 | tr '\n' ' ')"; err=$((err+1)); fi
}

for y in 2016 2017 2018; do for t in 1 2 3 4; do
  reg "enoe_${y}_${t}t_csv_microdatos" "${y}trim${t}_csv.zip" \
      "$M15/microdatos/${y}trim${t}_csv.zip" "$USO" \
      "ZIP (microdatos ENOE ${y} trimestre ${t}, ruta /microdatos/) -- 5 tablas CSV: COE1T COE2T HOGT SDEMT VIVT"
done; done

for y in 2005 2008 2012 2014; do
  reg "enoe_${y}_1t_csv_microdatos" "${y}trim1_csv.zip" \
      "$M15/microdatos/${y}trim1_csv.zip" \
      "$USO -- sonda de era para el diferencial exhaustivo de variables pre-vs-post" \
      "ZIP (microdatos ENOE ${y} trimestre 1, ruta /microdatos/) -- 5 tablas CSV"
done

reg "enoe_2018_4t_csv_datosabiertos" "conjunto_de_datos_enoe_2018_4t_csv.zip" \
    "$M15/datosabiertos/2018/conjunto_de_datos_enoe_2018_4t_csv.zip" \
    "$USO -- puente de distribucion: la misma ola que enoe_2018_4t_csv_microdatos, por la otra ruta de INEGI" \
    "ZIP (datos abiertos ENOE 2018 trimestre 4, ruta /datosabiertos/) -- 5 tablas mas catalogos y diccionarios"

M14="https://www.inegi.org.mx/contenidos/programas/enoe/14ymas/doc"
for n in fd_c_amp_v1 fd_c_amp_v2 fd_c_amp_v3 fd_c_amp_v4 fd_c_bas_v1 fd_c_bas_v2 fd_c_bas_amp_conapo; do
  reg "enoe_${n}_pdf" "${n}.pdf" "$M14/${n}.pdf" "$USOD" \
      "PDF (INEGI, ENOE, Descripcion de archivos -- era 14ymas)"
done
for n in fd_c_bas_amp_15ymas enoe_123_fd_c_bas_amp enoe_325_fd_c_bas_amp; do
  reg "enoe_${n}_pdf" "${n}.pdf" "$M15/doc/${n}.pdf" "$USOD" \
      "PDF (INEGI, ENOE, Estructura de la base de datos -- era 15ymas)"
done
echo; echo "registradas=$ok  ya_estaban=$ya  errores=$err"
