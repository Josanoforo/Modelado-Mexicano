"""Inspección de cabeceras (solo nombres/tipos de columna, sin filas)."""
import sys
import csv
sys.path.insert(0, "paquete/lib")
from dbfread import DBF

OLAS_DBF = ["2013t3", "2013t4", "2014t1", "2014t2", "2014t3", "2014t4", "2015t1", "2015t2",
            "2015t3", "2015t4", "2016t1", "2016t2", "2016t3", "2016t4", "2017t1", "2017t2",
            "2017t3", "2017t4", "2018t1", "2018t2", "2018t3", "2018t4", "2019t1", "2019t2",
            "2019t3", "2019t4", "2020t1", "2020t3", "2020t4"]
OLAS_CSV = ["2021t2", "2021t3", "2021t4", "2022t1", "2022t2", "2022t3", "2022t4", "2023t1",
            "2023t2", "2023t3", "2023t4", "2024t1", "2024t2", "2024t3", "2024t4", "2025t1",
            "2025t2", "2025t3", "2025t4"]
INTERES = {"CD", "EST_DIS", "EDIS", "UPM_DIS", "FAC_SEL", "FACTOR", "BP1_1", "P1", "SEX", "EDA",
           "EDAD", "SEXO", "R_SEL", "N_REN", "UPM", "VIV_SEL", "ENT"}

for o in OLAS_DBF:
    for t in ("cb", "cs"):
        f = "paquete/datos/ensu_%s_%s.dbf" % (o, t)
        d = DBF(f, load=False)
        print(o, t, d.encoding, len(d.field_names),
              [(x.name, x.type, x.length) for x in d.fields if x.name in INTERES])
for o in OLAS_CSV:
    f = "paquete/datos/ensu_%s_cb.csv" % o
    with open(f, "rb") as fh:
        raw = fh.readline()
    h = next(csv.reader([raw.decode("latin-1")]))
    print(o, "cb", len(h), repr(raw[:3]), [x for x in h if x.strip().strip("﻿ï»¿") in INTERES or "UPM" in x], repr(raw[-4:]))
