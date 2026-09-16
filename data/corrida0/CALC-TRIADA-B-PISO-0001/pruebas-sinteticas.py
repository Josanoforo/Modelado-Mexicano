"""Pruebas SINTETICAS del medidor de CALC-TRIADA-B-PISO-0001, antes del COMMIT-1.
Cuatro casos pre-declarados: control exacto, control al centesimo, control roto,
y guardia de identidad."""
import importlib.util, json, sys

spec = importlib.util.spec_from_file_location(
    "med", "data/corrida0/CALC-TRIADA-B-PISO-0001/medidor.py")
med = importlib.util.module_from_spec(spec); spec.loader.exec_module(med)

CONTRATO = {"parametros": {
    "input_marco": "IN-MARCO", "input_celdas": "IN-CELDAS",
    "input_b_mae": "IN-B-MAE", "input_triada_0002": "IN-0002",
    "n_celdas_marco": 4, "brazo_b": "PERSISTENCIA",
    "patron_b": "RESULT-BM-MAE-{celda}-{brazo}-ERR-PP",
    "corredores": ["B", "L_CORPUS", "L_SOLO", "M"],
    "columnas_err": {"L_SOLO": "error_abs_l_solo_pp",
                     "L_CORPUS": "error_abs_l_corpus_pp",
                     "M": "error_abs_m_pp"},
    "rid_veredicto_0002": "RESULT-F5C-VEREDICTO-GLOBAL",
    "control": {"umbral_exacto": 1e-9, "umbral_centesimo": 0.005,
                "sellado": {"L_SOLO": "RESULT-F5C-MAE-L-SOLO-PP",
                            "L_CORPUS": "RESULT-F5C-MAE-L-CORPUS-PP",
                            "M": "RESULT-F5C-MAE-M-PP"}}}}

MARCO = "id\n" + "\n".join(["C-1", "C-2", "C-3", "C-4"]) + "\n"
# C-1,C-2,C-3 en U3; C-4 fuera. B cubre C-1,C-2,C-4 -> U_COMUN = {C-1,C-2}
CELDAS = ("id_celda\terror_abs_l_solo_pp\terror_abs_l_corpus_pp\terror_abs_m_pp\ten_u3\n"
          "C-1\t1.0\t2.0\t4.0\tSI\n"
          "C-2\t3.0\t4.0\t8.0\tSI\n"
          "C-3\t5.0\t6.0\t12.0\tSI\n"
          "C-4\t9.0\t9.0\t9.0\tNO\n")
B = {"spec_id": "X", "resultados": {
    "RESULT-BM-MAE-C-1-PERSISTENCIA-ERR-PP": -0.5,
    "RESULT-BM-MAE-C-2-PERSISTENCIA-ERR-PP": 1.5,
    "RESULT-BM-MAE-C-3-PERSISTENCIA-ERR-PP": None,
    "RESULT-BM-MAE-C-4-PERSISTENCIA-ERR-PP": 7.0}}

def corre(mae_sellado, celdas=CELDAS, marco=MARCO):
    d = {"spec_id": "Y", "resultados": dict(mae_sellado,
         **{"RESULT-F5C-VEREDICTO-GLOBAL": "SIN-GANADOR-UNICO"})}
    inputs = {"IN-MARCO": {"bytes": marco.encode()},
              "IN-CELDAS": {"bytes": celdas.encode()},
              "IN-B-MAE": {"bytes": json.dumps(B).encode()},
              "IN-0002": {"bytes": json.dumps(d).encode()}}
    return med.medir(inputs, CONTRATO)

fallos = []
def ok(nombre, cond, extra=""):
    print(("PASA  " if cond else "FALLA ") + nombre + ("" if cond else f"  -- {extra}"))
    if not cond: fallos.append(nombre)

# U3 = {C-1,C-2,C-3}: MAE L_SOLO=3, L_CORPUS=4, M=8
EXACTO = {"RESULT-F5C-MAE-L-SOLO-PP": 3.0, "RESULT-F5C-MAE-L-CORPUS-PP": 4.0,
          "RESULT-F5C-MAE-M-PP": 8.0}
r = corre(EXACTO)
ok("1 control exacto -> DERIVA", r["RESULT-TBP-U3-CONTROL-VEREDICTO"] == "DERIVA")
ok("1 las tres ramas son REPRODUCE-EXACTO",
   all(r[f"RESULT-TBP-U3-CONTROL-{c}-RAMA"] == "REPRODUCE-EXACTO"
       for c in ("L_SOLO", "L_CORPUS", "M")))
ok("1 U_COMUN = C-1,C-2", r["RESULT-TBP-UCOMUN-IDS"] == "C-1,C-2" and r["RESULT-TBP-UCOMUN-N"] == 2)
ok("1 MAE B = 1.0 (|-0.5|,|1.5|)", abs(r["RESULT-TBP-UCOMUN-MAE-B-PP"] - 1.0) < 1e-12,
   r["RESULT-TBP-UCOMUN-MAE-B-PP"])
ok("1 MAE M = 6.0 sobre U_COMUN, no 8.0 de U3", abs(r["RESULT-TBP-UCOMUN-MAE-M-PP"] - 6.0) < 1e-12)
ok("1 orden descriptiva B < L_SOLO < L_CORPUS < M",
   r["RESULT-TBP-UCOMUN-ORDEN-DESCRIPTIVA"] == "B < L_SOLO < L_CORPUS < M",
   r["RESULT-TBP-UCOMUN-ORDEN-DESCRIPTIVA"])
ok("1 veredicto NO-ADJUDICA-POR-DISENO", r["RESULT-TBP-VEREDICTO"] == "NO-ADJUDICA-POR-DISENO")
ok("1 B menor que M en 2 de 2", r["RESULT-TBP-UCOMUN-N-CELDAS-B-MENOR-QUE-M"] == 2)
ok("1 C-3 excluida por SIN-B", r["RESULT-TBP-C-3-RAZON-EXCLUSION"] == "SIN-B-PERSISTENCIA")
ok("1 la razon se emite para LAS 4, incluidas las de U_COMUN",
   all(f"RESULT-TBP-C-{i}-RAZON-EXCLUSION" in r for i in (1,2,3,4))
   and r["RESULT-TBP-C-1-RAZON-EXCLUSION"] == "EN-UCOMUN")
ok("1 C-4 excluida por FUERA-DE-U3", r["RESULT-TBP-C-4-RAZON-EXCLUSION"] == "FUERA-DE-U3")
ok("1 veredicto de la triada se cita intacto",
   r["RESULT-TBP-TRIADA-VEREDICTO-VIGENTE"] == "SIN-GANADOR-UNICO")
ok("1 cero pareadas / IC / adopciones / llamadas",
   (r["RESULT-TBP-PAREADAS-NUEVAS"], r["RESULT-TBP-IC-NUEVOS"],
    r["RESULT-TBP-ADOPCIONES"], r["RESULT-TBP-LLAMADAS-A-MODELO"]) == (0, 0, 0, 0))
ok("1 cobertura B = 3 sobre el marco", r["RESULT-TBP-COBERTURA-B-PERSISTENCIA"] == 3)

# borde: delta justo por dentro del centesimo
r = corre(dict(EXACTO, **{"RESULT-F5C-MAE-M-PP": 8.0 - 0.004}))
ok("2 delta 0.004 -> REPRODUCE-AL-CENTESIMO y DERIVA",
   r["RESULT-TBP-U3-CONTROL-M-RAMA"] == "REPRODUCE-AL-CENTESIMO"
   and r["RESULT-TBP-U3-CONTROL-VEREDICTO"] == "DERIVA")

# delta claramente por encima del centesimo -> NO-REPRODUCE y tabla NO emitida.
# (El umbral se compara con `<` ESTRICTO; no se prueba el borde exacto porque
#  `8.0 - 0.005` no cae sobre el umbral en binario: eso probaria la aritmetica
#  flotante, no la regla.)
r = corre(dict(EXACTO, **{"RESULT-F5C-MAE-M-PP": 8.0 - 0.05}))
ok("3 delta 0.05 -> NO-REPRODUCE, tabla NO emitida",
   r["RESULT-TBP-U3-CONTROL-M-RAMA"] == "NO-REPRODUCE"
   and r["RESULT-TBP-U3-CONTROL-VEREDICTO"] == "NO-DERIVA"
   and r["RESULT-TBP-VEREDICTO"] == "NO-DERIVA-CONTROL-FALLA"
   and r["RESULT-TBP-UCOMUN-MAE-B-PP"] is None
   and r["RESULT-TBP-UCOMUN-ORDEN-DESCRIPTIVA"] == "NO-EMITIDA")
ok("3 aun asi reporta U_COMUN y los errores por celda",
   r["RESULT-TBP-UCOMUN-IDS"] == "C-1,C-2" and r["RESULT-TBP-C-1-ERR-ABS-B-PP"] == 0.5)

# U_COMUN vacio: ninguna celda de U3 tiene B. No es un MAE de cero celdas.
B_VACIO = {"spec_id": "X", "resultados": {
    f"RESULT-BM-MAE-C-{i}-PERSISTENCIA-ERR-PP": (7.0 if i == 4 else None)
    for i in (1, 2, 3, 4)}}
_B = B
globals()["B"] = B_VACIO
r = corre(EXACTO)
globals()["B"] = _B
ok("5 U_COMUN vacio -> NO-EMITE-UCOMUN-VACIO, sin division por cero",
   r["RESULT-TBP-UCOMUN-N"] == 0
   and r["RESULT-TBP-VEREDICTO"] == "NO-EMITE-UCOMUN-VACIO"
   and r["RESULT-TBP-UCOMUN-MAE-M-PP"] is None
   and r["RESULT-TBP-U3-CONTROL-VEREDICTO"] == "DERIVA")

# guardia de identidad
try:
    corre(EXACTO, marco="id\nC-1\nC-2\nC-3\nC-9\n")
    ok("4 guardia de identidad levanta", False, "no levanto")
except RuntimeError as e:
    ok("4 guardia de identidad levanta", "!=" in str(e))

print("\nRESUMEN:", "TODAS PASAN" if not fallos else f"FALLAN {fallos}")
sys.exit(1 if fallos else 0)
