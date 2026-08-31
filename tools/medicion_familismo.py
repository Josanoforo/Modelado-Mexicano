#!/usr/bin/env python3
"""ACTO MAESTRA32-E16 · MEDIDOR-FAMILISMO-APOYO.

Estima beta_hat (theta -> desenlace de G5) en eder2017 (primaria) y en
endireh2016 (robustez), con IC95 y lectura condicionada por eje.

Operacionalizaciones (COMMIT-1(c), congeladas antes de correr este script,
ver forense/notas/2026-08-31-familismo-spec.md):

  EDER 2017 (data/raw/eder2017/eder2017_bases_csv.zip):
    theta   = vivienda.financia_8 (dueño tuvo préstamo de un familiar,
              amigo o prestamista para pagar/construir la vivienda);
              1 si el código '8' está marcado, 0 si está en blanco.
              Universo: hogares con tipo_adqui no en blanco (el dueño
              pagó o construyó -- pregunta 33 apartado D no aplica a
              quien renta/le prestan la vivienda, tenencia in {1,2}).
    desenlace = corresidencia con familiar adulto: 1 si alguno de
              {padre_cor, madre_cor, hnos_cor, suegro_cor, suegra_cor}
              == '1' ("Inicio corresidencia") en cualquier fila del
              historial retrospectivo (historiavida.csv, panel
              persona-año, ~37 filas/persona en promedio) de esa
              persona; 0 si ninguna lo es. hij_cor_* EXCLUIDOS (corre-
              sidir con hijos menores no es "pooling", declarado en el
              encargo).
    join    = vivienda (por folioviv) -> historiavida (folioviv,
              foliohog, id_pobla), a nivel del respondiente del panel
              retrospectivo (23,831 personas únicas).
    peso    = vivienda.factor; diseño = vivienda.est_dis (estrato),
              vivienda.upm (UPM) -- citados de vivienda.csv, ambos
              presentes -> bootstrap por conglomerado (UPM dentro de
              estrato), no MAS simple.
    ejes    = sexo (historiavida.sexo), edad (historiavida.edad_act,
              cuartiles), urbano/rural (vivienda.tam_loc: 1-2=urbano
              >=15,000 hab., 3-4=rural).

  ENDIREH 2016 (data/raw/endireh2016/bd_mujeres_endireh2016_sitioinegi_csv.zip):
    theta   = P4_8_2==1 (recibe dinero de familiares/conocidos en EUA)
              O P4_8_3==1 (recibe dinero de familiares/conocidos
              dentro del país) -- TB_SEC_IV.csv. Sin códigos de no
              respuesta observados en el corpus (binario limpio 1/2).
    desenlace = P18_4 (TB_SEC_XVIII.csv, carga de cuidado de nietos/
              sobrinos): 1 si código in {1,2,3} (cuida con alguna
              frecuencia), 0 si código==4 ("No los cuida"). EXCLUIDOS:
              código 5 ("No tiene" nietos/sobrinos -- no aplica, no es
              "no respuesta" pero tampoco mide carga de cuidado),
              código 9 ("No especificado"), blanco (patrón de salto).
    join    = TB_SEC_IV, TB_SEC_XVIII, TSDem por ID_MUJ (llave única
              de la mujer elegida, 111,256 filas en las tres tablas).
    peso    = FAC_MUJ; diseño = EST_DIS (estrato), UPM_DIS (UPM),
              ambos presentes -> bootstrap por conglomerado.
    ejes    = edad (TSDem.EDAD, cuartiles), urbano/rural (TSDem.DOMINIO:
              U/C=urbano, R=rural). Sexo NO aplica (universo=mujeres).

Estimador (COMMIT-1(d)): diferencia de proporciones ponderada del
desenlace entre theta=1 y theta=0, misma escala que ADR-220. IC95 por
bootstrap de conglomerados (UPM dentro de estrato), B=10,000, seed=42
-- las dos bases traen estrato/UPM, así que el bootstrap resamplea UPMs
dentro de cada estrato (aproximación declarada al "IC95 por diseño":
no se dispone de librería de encuestas complejas en la caja; resamplear
la unidad de conglomeración es la aproximación estándar más cercana a
un diseño con linealización de Taylor, y se declara explícitamente en
vez de usar bootstrap i.i.d. plano). Condicionamiento: un eje a la vez,
celdas n>=30.

Escribe por código (no a mano): milpa/procedencia.yaml (sección A +
sellados + fila B de rutas_estimabilidad_coeficiente.detalle) y
forense/notas/2026-08-31-familismo-cierre.md.
"""
import csv
import io
import os
import random
import zipfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(RAIZ, "data", "raw")
PROCEDENCIA_PATH = os.path.join(RAIZ, "milpa", "procedencia.yaml")
CIERRE_PATH = os.path.join(
    RAIZ, "forense", "notas", "2026-08-31-familismo-cierre.md"
)

SEED = 42
B_BOOT = 10000
N_MIN = 30

COR_VARS = ["padre_cor", "madre_cor", "hnos_cor", "suegro_cor", "suegra_cor"]


# ─── lectura de payloads ────────────────────────────────────────────
def _leer_csv_de_zip(ruta_zip, nombre_interno, encoding="latin-1"):
    with zipfile.ZipFile(ruta_zip) as z:
        with z.open(nombre_interno) as f:
            r = csv.DictReader(io.TextIOWrapper(f, encoding=encoding))
            return list(r)


def cargar_eder():
    zpath = os.path.join(RAW, "eder2017", "eder2017_bases_csv.zip")
    vivienda = _leer_csv_de_zip(zpath, "vivienda.csv")
    historiavida = _leer_csv_de_zip(zpath, "historiavida.csv")

    # theta + peso + diseño + eje urbano/rural, universo tipo_adqui != blanco
    def _folioviv_key(row):
        for k in row:
            if k.endswith("folioviv"):
                return k
        raise KeyError("folioviv")

    hogares = {}
    n_universo_excluido_renta = 0
    fv_key_vivienda = _folioviv_key(vivienda[0])
    for row in vivienda:
        folioviv = row[fv_key_vivienda]
        if row["tipo_adqui"].strip() == "":
            n_universo_excluido_renta += 1
            continue
        theta = 1 if row["financia_8"].strip() == "8" else 0
        tam_loc = row["tam_loc"].strip()
        urbano = None
        if tam_loc in ("1", "2"):
            urbano = 1
        elif tam_loc in ("3", "4"):
            urbano = 0
        hogares[folioviv] = {
            "theta": theta,
            "peso": float(row["factor"]),
            "estrato": row["est_dis"].strip(),
            "upm": row["upm"].strip(),
            "urbano": urbano,
        }

    # desenlace: colapsar historiavida (panel persona-año) a nivel persona
    personas = {}
    fv_key_hv = _folioviv_key(historiavida[0])
    for row in historiavida:
        folioviv = row[fv_key_hv]
        key = (folioviv, row["foliohog"], row["id_pobla"])
        if key not in personas:
            personas[key] = {
                "folioviv": folioviv,
                "sexo": row["sexo"].strip(),
                "edad_act": row["edad_act"].strip(),
                "coreside": 0,
            }
        if any(row[c].strip() == "1" for c in COR_VARS):
            personas[key]["coreside"] = 1

    filas = []
    n_sin_theta = 0
    for key, p in personas.items():
        hog = hogares.get(p["folioviv"])
        if hog is None:
            n_sin_theta += 1
            continue
        edad = None
        try:
            edad = int(p["edad_act"])
        except ValueError:
            edad = None
        filas.append({
            "theta": hog["theta"],
            "desenlace": p["coreside"],
            "peso": hog["peso"],
            "estrato": hog["estrato"],
            "upm": hog["upm"],
            "sexo": p["sexo"],
            "edad": edad,
            "urbano": hog["urbano"],
        })

    meta = {
        "n_vivienda_total": len(vivienda),
        "n_universo_excluido_renta_o_prestada": n_universo_excluido_renta,
        "n_personas_historiavida": len(personas),
        "n_sin_theta_folioviv_no_en_universo": n_sin_theta,
    }
    return filas, meta


def cargar_endireh():
    zpath = os.path.join(
        RAW, "endireh2016", "bd_mujeres_endireh2016_sitioinegi_csv.zip"
    )
    pref = "bd_mujeres_endireh2016_sitioinegi_csv/"
    sec_iv = _leer_csv_de_zip(zpath, pref + "TB_SEC_IV.csv")
    sec_xviii = _leer_csv_de_zip(zpath, pref + "TB_SEC_XVIII.csv")
    tsdem = _leer_csv_de_zip(zpath, pref + "TSDem.csv")

    theta_de = {}
    for row in sec_iv:
        theta_de[row["ID_MUJ"]] = {
            "theta": 1 if (row["P4_8_2"] == "1" or row["P4_8_3"] == "1") else 0,
            "peso": float(row["FAC_MUJ"]),
            "estrato": row["EST_DIS"].strip(),
            "upm": row["UPM_DIS"].strip(),
        }

    desenlace_de = {}
    n_excluido_p18_4 = {"blanco": 0, "no_tiene(5)": 0, "no_especificado(9)": 0}
    for row in sec_xviii:
        v = row["P18_4"].strip()
        if v == "":
            n_excluido_p18_4["blanco"] += 1
            continue
        if v == "5":
            n_excluido_p18_4["no_tiene(5)"] += 1
            continue
        if v == "9":
            n_excluido_p18_4["no_especificado(9)"] += 1
            continue
        desenlace_de[row["ID_MUJ"]] = 1 if v in ("1", "2", "3") else 0

    dominio_de = {}
    for row in tsdem:
        dom = row["DOMINIO"].strip()
        urbano = 1 if dom in ("U", "C") else (0 if dom == "R" else None)
        edad = None
        try:
            edad = int(row["EDAD"])
        except ValueError:
            edad = None
        dominio_de[row["ID_MUJ"]] = {"urbano": urbano, "edad": edad}

    filas = []
    for id_muj, t in theta_de.items():
        if id_muj not in desenlace_de:
            continue
        dom = dominio_de.get(id_muj, {"urbano": None, "edad": None})
        filas.append({
            "theta": t["theta"],
            "desenlace": desenlace_de[id_muj],
            "peso": t["peso"],
            "estrato": t["estrato"],
            "upm": t["upm"],
            "sexo": None,
            "edad": dom["edad"],
            "urbano": dom["urbano"],
        })

    meta = {
        "n_sec_iv": len(sec_iv),
        "n_sec_xviii": len(sec_xviii),
        "n_excluido_p18_4": n_excluido_p18_4,
        "n_filas_finales": len(filas),
    }
    return filas, meta


# ─── estimador ──────────────────────────────────────────────────────
def diff_prop_ponderada(filas):
    """Diferencia de proporciones ponderada theta=1 - theta=0 del
    desenlace. Devuelve (diff, n1, n0) o (None, n1, n0) si alguna
    celda no alcanza n_min."""
    s1 = s1w = 0.0
    s0 = s0w = 0.0
    n1 = n0 = 0
    for f in filas:
        w = f["peso"]
        if f["theta"] == 1:
            n1 += 1
            s1w += w
            s1 += w * f["desenlace"]
        else:
            n0 += 1
            s0w += w
            s0 += w * f["desenlace"]
    if n1 < N_MIN or n0 < N_MIN:
        return None, n1, n0
    p1 = s1 / s1w
    p0 = s0 / s0w
    return p1 - p0, n1, n0


def bootstrap_ic95(filas, seed=SEED, b=B_BOOT):
    """Bootstrap por conglomerado: resamplea UPMs dentro de cada
    estrato (B repeticiones), recalcula la diferencia de proporciones
    ponderada en cada repetición, y toma el IC95 percentil."""
    por_estrato = {}
    for f in filas:
        por_estrato.setdefault(f["estrato"], {}).setdefault(f["upm"], []).append(f)

    estratos = list(por_estrato.keys())
    rng = random.Random(seed)
    estimaciones = []
    for _ in range(b):
        muestra = []
        for e in estratos:
            upms = list(por_estrato[e].keys())
            if not upms:
                continue
            elegidas = [rng.choice(upms) for _ in range(len(upms))]
            for u in elegidas:
                muestra.extend(por_estrato[e][u])
        diff, n1, n0 = diff_prop_ponderada(muestra)
        if diff is not None:
            estimaciones.append(diff)
    if len(estimaciones) < b * 0.5:
        return None
    estimaciones.sort()
    lo = estimaciones[int(0.025 * len(estimaciones))]
    hi = estimaciones[int(0.975 * len(estimaciones)) - 1]
    return lo, hi


def condicionar(filas, eje):
    """Un eje a la vez. Devuelve dict {valor_eje: (diff, ic, n1, n0)}
    solo para celdas con n>=N_MIN en ambos brazos de theta."""
    valores = set()
    for f in filas:
        v = f.get(eje)
        if v is None:
            continue
        if eje == "edad" and v is not None:
            if v < 30:
                v = "15-29"
            elif v < 45:
                v = "30-44"
            elif v < 60:
                v = "45-59"
            else:
                v = "60+"
        valores.add(v)

    resultado = {}
    for v in sorted(valores, key=str):
        if eje == "edad":
            sub = []
            for f in filas:
                e = f.get("edad")
                if e is None:
                    continue
                cat = ("15-29" if e < 30 else "30-44" if e < 45
                       else "45-59" if e < 60 else "60+")
                if cat == v:
                    sub.append(f)
        else:
            sub = [f for f in filas if f.get(eje) == v]
        diff, n1, n0 = diff_prop_ponderada(sub)
        if diff is None:
            continue
        ic = bootstrap_ic95(sub, seed=SEED, b=2000)  # sub-muestra: B reducido
        resultado[v] = (diff, ic, n1, n0)
    return resultado


# ─── escritura del ejecutable (por código, no a mano) ──────────────
def escribir_procedencia(res_eder, res_endireh, ic_eder, ic_endireh):
    with open(PROCEDENCIA_PATH, encoding="utf-8") as fh:
        texto = fh.read()

    signo_eder = "+" if res_eder["diff"] >= 0 else "-"
    signo_endireh = "+" if res_endireh["diff"] >= 0 else "-"
    signo_asignado_positivo = True  # G5.familismo_apoyo ASIGNADO 0.50 (modelo:459)

    no_distinguible_eder = ic_eder[0] <= 0 <= ic_eder[1]
    no_distinguible_endireh = ic_endireh[0] <= 0 <= ic_endireh[1]
    signo_discordante = (res_eder["diff"] >= 0) != (res_endireh["diff"] >= 0)

    sufijos = []
    if no_distinguible_eder:
        sufijos.append("·NO-DISTINGUIBLE-DE-CERO")
    if signo_discordante:
        sufijos.append("·DISCORDANTE-ENTRE-INSTRUMENTOS")
    rotulo = "ASOCIACION-MEDIDA·MARGINAL" + "".join(sufijos)

    # 1) sección A: coeficientes_generador_medidos -- nueva entrada
    #    G5_familismo_apoyo, insertada al final del bloque A (antes del
    #    marcador de coeficientes_generador_sellados).
    entrada_a = f'''  G5_familismo_apoyo:
    clase: "MEDIDO·β̂(diferencia de proporciones), un ítem, marginal, re-empareja ext (ADR-228/230)"
    antes: "ASIGNADO -- coeficiente de generador (G5 0.50), sin estimación empírica (modelo-decision-v4_0.md:459)"
    fuente: "ACTO MAESTRA32-E16, 31/ago/2026 -- eder2017 (data/raw/eder2017/eder2017_bases_csv.zip, sha256 {SHA_EDER_ZIP}) theta=vivienda.financia_8 (\\"préstamo familiar\\", universo tipo_adqui no blanco) x desenlace=historiavida.{{padre_cor,madre_cor,hnos_cor,suegro_cor,suegra_cor}}==1 en cualquier fila del panel retrospectivo, colapsado a nivel persona -- endireh2016 (data/raw/endireh2016/bd_mujeres_endireh2016_sitioinegi_csv.zip, sha256 {SHA_ENDIREH_ZIP}) theta=P4_8_2==1 ∨ P4_8_3==1 x desenlace=P18_4 en {{1,2,3}} -- forense/notas/2026-08-31-familismo-spec.md, forense/notas/2026-08-31-familismo-cierre.md"
    n_util: "EDER: theta=1 n={res_eder['n1']}, theta=0 n={res_eder['n0']} · ENDIREH: theta=1 n={res_endireh['n1']}, theta=0 n={res_endireh['n0']}"
    beta_hat: "EDER: {signo_eder}{abs(res_eder['diff']):.4f} [IC95% {ic_eder[0]:.4f},{ic_eder[1]:.4f}] · ENDIREH (robustez): {signo_endireh}{abs(res_endireh['diff']):.4f} [IC95% {ic_endireh[0]:.4f},{ic_endireh[1]:.4f}]"
    nota: >
      Escala de diferencia de proporciones ponderada del desenlace, NO la
      escala del índice del generador -- no comparable en magnitud contra
      el 0.50 ASIGNADO (canon/modelo-decision-v4_0.md:459). IC95 por
      bootstrap de conglomerados (UPM dentro de estrato), B=10000, seed=42
      (ambas bases traen estrato/UPM -- aproximación declarada al IC por
      diseño, ver docstring de tools/medicion_familismo.py). Ajuste de
      constructo (a): ambos reactivos declarados VÁLIDOS -- financia_8 y
      P4_8_2/P4_8_3 nombran "familiar" como fuente de dinero/préstamo
      recibido, aunque ambos son compuestos con no-familia (financia_8:
      "familiar, amigo o prestamista"; P4_8_2/3: "familiares o
      conocidos") -- contaminación de constructo declarada, no oculta.
      Circularidad (precedente ENIF p9_9_4): el desenlace NO es
      transformación del mismo reactivo -- corresidencia (EDER) y carga
      de cuidado (ENDIREH) son constructos distintos de "recibir dinero".
    eje_condicionante: >
      Un eje a la vez, celdas n>=30 (COMMIT-1(d)). EDER: sexo, edad
      (15-29/30-44/45-59/60+), urbano/rural (tam_loc). ENDIREH: edad
      (mismos cortes), urbano/rural (DOMINIO). Sexo no aplica en ENDIREH
      (universo=mujeres). Tabla completa condicionada en
      forense/notas/2026-08-31-familismo-cierre.md.
    adr57_a: >
      ADR-57 (a): concordancia o discordancia de signo entre estos β̂ y
      el ASIGNADO (G5 0.50) son ambas informativas y ninguna corrobora ni
      refuta -- asociar ≠ identificar. {"Signo DISCORDANTE entre EDER y ENDIREH." if signo_discordante else "Signo CONCORDANTE entre EDER y ENDIREH."}
'''
    marcador_a = "\ncoeficientes_generador_sellados:"
    idx = texto.index(marcador_a)
    # Insertar la nueva entrada A justo antes del bloque de comentario que
    # antecede a "coeficientes_generador_sellados:" (mismo patrón que las
    # entradas previas de la sección A, que terminan con línea en blanco).
    marcador_comentario = "\n# ══════════════════════════════════════════════════════════════════\n# COEFICIENTES DE GENERADOR SELLADOS"
    idx_comentario = texto.index(marcador_comentario)
    texto = texto[:idx_comentario] + "\n" + entrada_a + texto[idx_comentario:]

    # 2) coeficientes_generador_sellados: nueva entrada AL FINAL (verificar
    #    que sigue siendo la última clave raíz del YAML).
    import re as _re
    claves_raiz = [
        l.split(":")[0] for l in texto.splitlines()
        if _re.match(r"^[A-Za-z_][A-Za-z0-9_]*:", l)
    ]
    if claves_raiz[-1] != "coeficientes_generador_sellados":
        raise RuntimeError(
            "PARO: coeficientes_generador_sellados ya NO es la última clave "
            f"raíz del YAML (es {claves_raiz[-1]!r}) -- no se escribe la "
            "entrada sellada sin verificación manual."
        )

    valor_ejecutable = None
    reserva_endireh = (
        f"Robustez ENDIREH 2016: β̂={signo_endireh}{abs(res_endireh['diff']):.4f} "
        f"[IC95% {ic_endireh[0]:.4f},{ic_endireh[1]:.4f}], n_util theta=1 "
        f"{res_endireh['n1']}, theta=0 {res_endireh['n0']}. "
        f"{'Signo DISCORDANTE con EDER -- ambas van en reserva por regla de escritura (e).' if signo_discordante else 'Signo concordante con EDER.'} "
        "ADR-57(a): asociar ≠ identificar; concordancia/discordancia son "
        "ambas informativas, ninguna corrobora ni refuta."
    )

    if signo_discordante:
        rotulo_final = "ASOCIACION-MEDIDA·MARGINAL·DISCORDANTE-ENTRE-INSTRUMENTOS"
        if no_distinguible_eder:
            rotulo_final += "·NO-DISTINGUIBLE-DE-CERO"
        valor_ejecutable_eder = res_eder["diff"]
    else:
        rotulo_final = rotulo
        valor_ejecutable_eder = res_eder["diff"]

    entrada_sellada = f'''- gen: G5
  coef: familismo_apoyo
  clase: MEDIDO·β̂(diferencia de proporciones), un ítem, marginal, re-empareja ext (ADR-228/230)
  valor_origen: '{signo_eder}{abs(res_eder["diff"]):.4f} [IC95% {ic_eder[0]:.4f},{ic_eder[1]:.4f}]'
  unidad_origen: proporción (diferencia de proporciones, sin sufijo pp)
  valor_ejecutable: {valor_ejecutable_eder:.6f}
  ic: 'IC95% {ic_eder[0]:.6f},{ic_eder[1]:.6f}'
  escala: "proporción ponderada [0,1], enlace identidad (ADR-220)"
  rotulo: {rotulo_final}
  reserva: '{reserva_endireh}'
  fuente: coeficientes_generador_medidos.G5_familismo_apoyo, 31/ago/2026 (ACTO MAESTRA32-E16)
'''
    texto = texto.rstrip("\n") + "\n" + entrada_sellada

    # 3) rutas_estimabilidad_coeficiente.detalle: fila B de
    #    G5.familismo_apoyo, SIN-RUTA -> RUTA-A, escala_derivada APPEND-ONLY.
    marca_fila_b = (
        '- {gen: G5, coef: familismo_apoyo, ruta: SIN-RUTA, prioridad: BAJA, '
        'nota: "único candidato (ENIF p9_9_4) excluido por circularidad'
    )
    if marca_fila_b not in texto:
        raise RuntimeError(
            "PARO: no se encontró la fila B de G5.familismo_apoyo "
            "(SIN-RUTA) en rutas_estimabilidad_coeficiente.detalle -- no "
            "se puede re-sellar sin localizar la fila exacta."
        )
    idx_fila = texto.index(marca_fila_b)
    idx_fin_fila = texto.index("}\n", idx_fila) + 1
    fila_original = texto[idx_fila:idx_fin_fila]
    fila_nueva = fila_original.replace("ruta: SIN-RUTA", "ruta: RUTA-A", 1)
    append_texto = (
        ' Paso 3, 31/ago, ADR-<n provisional, corregir>: θ con fuente '
        'eder2017 financia_8 (ACTO MAESTRA32-E16, re-empareja ext '
        'ADR-228/230 -- eder2017/endireh2016 co-observación, ADR-230). '
        f'β̂ EDER {signo_eder}{abs(res_eder["diff"]):.4f}, β̂ ENDIREH (robustez, '
        f'reserva) {signo_endireh}{abs(res_endireh["diff"]):.4f}."'
    )
    # Insertar el append dentro del campo escala_derivada, antes de la
    # comilla de cierre final de esa cadena.
    marca_escala = 'escala_derivada: "SUBDETERMINADA'
    idx_ed = fila_nueva.index(marca_escala)
    idx_cierre = fila_nueva.index('."', idx_ed) + 2
    fila_nueva = fila_nueva[:idx_cierre - 2] + '.' + append_texto[1:] + fila_nueva[idx_cierre:]
    # (el reemplazo de arriba añade texto ANTES de la comilla de cierre,
    # append-only: el texto previo no se borra, solo se agrega al final)

    texto = texto[:idx_fila] + fila_nueva + texto[idx_fin_fila:]

    with open(PROCEDENCIA_PATH, "w", encoding="utf-8") as fh:
        fh.write(texto)

    return {
        "rotulo_sellado": rotulo_final,
        "signo_discordante": signo_discordante,
        "no_distinguible_eder": no_distinguible_eder,
        "no_distinguible_endireh": no_distinguible_endireh,
    }


SHA_EDER_ZIP = None
SHA_ENDIREH_ZIP = None


def _sha256(ruta):
    import hashlib
    h = hashlib.sha256()
    with open(ruta, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def escribir_cierre(res_eder, res_endireh, ic_eder, ic_endireh, cond_eder,
                     cond_endireh, meta_eder, meta_endireh, veredicto):
    lineas = []
    lineas.append("# ACTO MAESTRA32-E16 · MEDIDOR-FAMILISMO-APOYO -- cierre\n")
    lineas.append("31/ago/2026. Corrida única de `tools/medicion_familismo.py` "
                   "contra `data/raw/eder2017/eder2017_bases_csv.zip` "
                   f"(sha256 `{SHA_EDER_ZIP}`) y "
                   "`data/raw/endireh2016/bd_mujeres_endireh2016_sitioinegi_csv.zip` "
                   f"(sha256 `{SHA_ENDIREH_ZIP}`). "
                   '"el primer resultado que produzca este procedimiento es el que se reporta."\n')

    lineas.append("\n## 1 · n por universo\n")
    lineas.append(f"- EDER: `vivienda.csv` {meta_eder['n_vivienda_total']} filas -- "
                   f"{meta_eder['n_universo_excluido_renta_o_prestada']} excluidas "
                   "(tipo_adqui en blanco: renta/prestada, no aplica la pregunta "
                   "de financiamiento). `historiavida.csv` colapsado a "
                   f"{meta_eder['n_personas_historiavida']} personas (panel "
                   f"persona-año); {meta_eder['n_sin_theta_folioviv_no_en_universo']} "
                   "sin folioviv en el universo de theta (excluidas).")
    lineas.append(f"  - Universo final: theta=1 n={res_eder['n1']}, theta=0 "
                   f"n={res_eder['n0']} (total {res_eder['n1']+res_eder['n0']}).")
    lineas.append(f"- ENDIREH: `TB_SEC_IV.csv`/`TB_SEC_XVIII.csv` "
                   f"{meta_endireh['n_sec_iv']} filas cada una (universo bd_mujeres, "
                   "mujeres 15+). P18_4 excluidos: "
                   f"{meta_endireh['n_excluido_p18_4']}.")
    lineas.append(f"  - Universo final: theta=1 n={res_endireh['n1']}, theta=0 "
                   f"n={res_endireh['n0']} (total {res_endireh['n1']+res_endireh['n0']}).")

    lineas.append("\n## 2 · beta_hat e IC por instrumento\n")
    lineas.append(f"- **EDER (primaria):** {res_eder['diff']:+.4f} "
                   f"[IC95% {ic_eder[0]:.4f},{ic_eder[1]:.4f}]")
    lineas.append(f"- **ENDIREH (robustez):** {res_endireh['diff']:+.4f} "
                   f"[IC95% {ic_endireh[0]:.4f},{ic_endireh[1]:.4f}]")
    lineas.append("\nEscala: diferencia de proporciones ponderada del desenlace "
                   "(theta=1 - theta=0), proporción [0,1]. IC95 por bootstrap de "
                   "conglomerados (UPM dentro de estrato), B=10000 (EDER/ENDIREH "
                   "principal) / B=2000 (celdas condicionadas), seed=42.")

    lineas.append("\n## 3 · tabla condicionada (un eje a la vez, celdas n>=30)\n")
    lineas.append("### EDER")
    for eje, resultado in cond_eder.items():
        lineas.append(f"- **{eje}:**")
        for valor, (diff, ic, n1, n0) in resultado.items():
            ic_txt = f"[{ic[0]:.4f},{ic[1]:.4f}]" if ic else "SIN IC (submuestra insuficiente)"
            lineas.append(f"  - {valor}: {diff:+.4f} {ic_txt} (n1={n1}, n0={n0})")
    lineas.append("### ENDIREH")
    for eje, resultado in cond_endireh.items():
        lineas.append(f"- **{eje}:**")
        for valor, (diff, ic, n1, n0) in resultado.items():
            ic_txt = f"[{ic[0]:.4f},{ic[1]:.4f}]" if ic else "SIN IC (submuestra insuficiente)"
            lineas.append(f"  - {valor}: {diff:+.4f} {ic_txt} (n1={n1}, n0={n0})")

    lineas.append("\n## 4 · veredicto (a) -- ajuste de constructo\n")
    lineas.append(
        "financia_8 (EDER, ADR: texto_reactivo extraído de `eder2017_fd.pdf` "
        "#91): \"¿Para pagar o empezar a construir esta vivienda, el dueño "
        "tuvo préstamo de un familiar, amigo o prestamista?\" -- mide "
        "recepción de préstamo con fuente compuesta (familiar + amigo + "
        "prestamista comercial), específico al financiamiento de vivienda, "
        "no apoyo económico familiar genérico. p4_8_2/p4_8_3 (ENDIREH, "
        "texto extraído de `fd_endireh2016_dbf.pdf`): \"¿usted recibe "
        "dinero de familiares o conocidos que viven en Estados Unidos de "
        "América/dentro del país...?\" -- mide recepción de dinero con "
        "fuente compuesta (familiares + conocidos), sin restricción de "
        "propósito. **Veredicto: VÁLIDA en ambos instrumentos** -- "
        "\"familiar\" es nombrado explícitamente y en primer lugar en las "
        "dos fuentes, cumple la regla pre-registrada (apoyo económico "
        "familiar recibido/obtenido, préstamo/dinero de familiares); la "
        "contaminación con no-familia (amigo/prestamista/conocidos) es una "
        "reserva declarada, NO dispara PROXY bajo la regla tal como está "
        "escrita en el encargo. Circularidad: el desenlace NO es "
        "transformación del mismo reactivo en ninguno de los dos "
        "instrumentos -- corresidencia con familiar adulto (EDER) y carga "
        "de cuidado de nietos/sobrinos (ENDIREH) son constructos distintos "
        "de \"recibir dinero/préstamo\", mismo criterio que excluyó ENIF "
        "p9_9_4 por circularidad."
    )
    lineas.append(
        "\n**FALSADOR: NO DISPARADO** -- ningún instrumento marcó PROXY."
    )

    lineas.append("\n## 5 · veredicto (e) -- B-bis, ADR-57(a) y rótulo\n")
    lineas.append(
        f"Signo ASIGNADO de G5.familismo_apoyo (canon/modelo-decision-v4_0.md:459): "
        "**positivo (0.50)**."
    )
    lineas.append(
        f"- EDER: β̂ {res_eder['diff']:+.4f}, "
        f"{'NO distinguible de cero al 95%' if veredicto['no_distinguible_eder'] else 'distinguible de cero al 95%'}."
    )
    lineas.append(
        f"- ENDIREH: β̂ {res_endireh['diff']:+.4f}, "
        f"{'NO distinguible de cero al 95%' if veredicto['no_distinguible_endireh'] else 'distinguible de cero al 95%'}."
    )
    lineas.append(
        f"- Signos entre EDER y ENDIREH: "
        f"{'DISCORDANTES' if veredicto['signo_discordante'] else 'concordantes'} "
        "-- ADR-57(a): concordancia o discordancia son ambas informativas, "
        "ninguna corrobora ni refuta el ASIGNADO."
    )
    lineas.append(
        f"- Rótulo escrito en `coeficientes_generador_sellados`: "
        f"`{veredicto['rotulo_sellado']}`. Solo la primaria (EDER) lleva "
        "`valor_ejecutable`; ENDIREH queda en `reserva` como robustez, por "
        "regla de escritura del encargo."
    )

    with open(CIERRE_PATH, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lineas) + "\n")


def main():
    global SHA_EDER_ZIP, SHA_ENDIREH_ZIP
    SHA_EDER_ZIP = _sha256(os.path.join(RAW, "eder2017", "eder2017_bases_csv.zip"))
    SHA_ENDIREH_ZIP = _sha256(os.path.join(
        RAW, "endireh2016", "bd_mujeres_endireh2016_sitioinegi_csv.zip"
    ))
    print("sha256 eder2017_bases_csv.zip:", SHA_EDER_ZIP)
    print("sha256 bd_mujeres_endireh2016_sitioinegi_csv.zip:", SHA_ENDIREH_ZIP)

    filas_eder, meta_eder = cargar_eder()
    filas_endireh, meta_endireh = cargar_endireh()

    diff_eder, n1_e, n0_e = diff_prop_ponderada(filas_eder)
    diff_endireh, n1_h, n0_h = diff_prop_ponderada(filas_endireh)
    if diff_eder is None or diff_endireh is None:
        raise RuntimeError("PARO: alguna celda marginal no alcanza n>=30.")

    ic_eder = bootstrap_ic95(filas_eder)
    ic_endireh = bootstrap_ic95(filas_endireh)
    if ic_eder is None or ic_endireh is None:
        raise RuntimeError("PARO: bootstrap no produjo suficientes réplicas.")

    res_eder = {"diff": diff_eder, "n1": n1_e, "n0": n0_e}
    res_endireh = {"diff": diff_endireh, "n1": n1_h, "n0": n0_h}

    print("EDER beta_hat:", diff_eder, ic_eder)
    print("ENDIREH beta_hat:", diff_endireh, ic_endireh)

    cond_eder = {
        "sexo": condicionar(filas_eder, "sexo"),
        "edad": condicionar(filas_eder, "edad"),
        "urbano/rural": condicionar(filas_eder, "urbano"),
    }
    cond_endireh = {
        "edad": condicionar(filas_endireh, "edad"),
        "urbano/rural": condicionar(filas_endireh, "urbano"),
    }

    veredicto = escribir_procedencia(res_eder, res_endireh, ic_eder, ic_endireh)
    escribir_cierre(res_eder, res_endireh, ic_eder, ic_endireh, cond_eder,
                     cond_endireh, meta_eder, meta_endireh, veredicto)

    print("veredicto:", veredicto)


if __name__ == "__main__":
    main()
