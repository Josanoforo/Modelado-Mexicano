"""Generate the four frozen CALC contracts before historical fitting."""
from pathlib import Path
import hashlib
import yaml
from tools.astra.envipe.model import PAIRS, ORDER

ROOT = Path(__file__).resolve().parents[3]
MODEL_SHA = "47ded83d3e8a9283a2972289240d8fa6b90c440cefb238bca04255e044a11212"
PUBLIC_SHA = "93dfa3f9aab250dabf9cbe8c93ccef2012cb763c5367d023f24dbfbd867fbc8f"

for pair, (a, b) in PAIRS.items():
    calc = f"CALC-ASTRA-ENVIPE-{pair}-0001"
    directory = ROOT / "data/corrida0" / calc
    directory.mkdir(parents=True, exist_ok=True)
    cells = [(x, y) for x in ORDER[a] for y in ORDER[b]]
    grid = ", ".join(f"({x}, {y})" for x, y in cells)
    md = f"""# C-ASTRA ENVIPE 2025 · {a} × {b} · v1.0

Estado: procedimiento congelado antes del ajuste histórico y de cualquier lectura del cruce de evaluación.
El primer resultado que produzca este procedimiento es el que se reporta.

## Estimando y fuentes
Unidad DELITO; universo BP1_20 ∈ {{1,2}}; Y=1 si BP1_20=2 y BP1_23 ∈ {{04,05,06,08}}. Es la probabilidad conjunta en el universo, no la condicional a no denuncia. FAC_DEL pondera; EST_DIS estratifica; UPM_DIS es conglomerado. 2023 y 2024 son las únicas olas de ajuste. `envipe2023_csv` SHA 0dcc00a7fc37b79806f1bf1b85b12cd090b5ecc8e76983a3a1a861f2ef3fb404; `envipe2024_csv` SHA 90776b2fab6e3666dad1cb5f5f3eb7d6a7699dbfefd4f8f04f07fb01e61a6fb2; licencia INEGI Términos de Libre Uso. Los reactivos, códigos y filtros son los de `prereg-caja-ENVIPE-EVASION-NORMA` y del lector histórico con hash fijado; 2023/24 usan tmod_vic, y NIV se une desde tsdem por ID_PER única. Sexo y edad vienen de tmod_vic. Edad válida 18..96; otros códigos de eje quedan fuera solo de ese eje. Se cuentan vacíos de BP1_23 entre no denunciados y huérfanos del enlace, sin imputarlos. Ponderador positivo y estrato/UPM completos o PARO.

El único dato de 2025 es el segmento público sellado `tramite.evasion_norma_ejes_envipe2025` de `milpa/tramite-ola5-propuesta-v0.yaml` (SHA {PUBLIC_SHA}) y el nacional sellado 0.562774. Se extrae solamente ese segmento; el cruce 2025 no se abre. Sus marginales son puntos condicionados, sin réplicas inventadas.

## Rejilla y procedimiento
{len(cells)} celdas: {grid}. Edad × dominio (NC-0328), escolaridad × dominio y resultados de pilotos anteriores se excluyen del ajuste.

`C2_2025(c)=expit(logit p25(a)+logit p25(b)-logit p25(nacional))`. Para t=2023,2024: `I_t(c)=logit p_t(a,b)-logit p_t(a)-logit p_t(b)+logit p_t(nacional)`. Cada p histórica es suma(FAC_DEL·Y)/suma(FAC_DEL). Una p en frontera se recorta a [1e-6,1-1e-6] antes de logit. Celda vacía en punto o réplica es NO-ESTIMABLE con causa; no elimina las otras celdas.

Modelo normal empírico: `theta24~N(0,tau²)`, `I23|theta24~N(theta24,v23+q)`, `I24|theta24~N(theta24,v24)`, `theta25|theta24~N(theta24,q)`. `v23/v24` son varianzas de 256 réplicas de UPM dentro de EST_DIS, comunes a todas las celdas y marginales de una ola, PCG64(20260922+t). Hiperparámetros por pooling entre celdas: `tau²=max(0,median_c(I23·I24))`; `q=max(0.0004,median_c((I24-I23)^2-v23-v24)/2)`. El mínimo de q regulariza la deriva no identificable por celda con solo dos olas. No hay búsqueda de variantes contra 2025. Media posterior normal por precisión; punto `expit(logit C2 + media posterior de theta24)`. Este ruido por celda y persistencia anual aporta algo distinto del λ fijo de C-ENCOGIDA. No garantiza preservar los marginales.

Intervalo predictivo 95%: 2048 sorteos PCG64(20260922), con índices de réplicas históricas compartidos entre celdas de la misma ola; tau² y q se recalculan en cada sorteo; posterior y evolución anual se simulan. Percentiles 2.5 y 97.5 de la probabilidad predicha. Incorpora ruido histórico, hiperparámetros y deriva temporal; condiciona los marginales 2025. No es IC de R y sus sorteos no se emparejan con las réplicas de R. El piloto conserva su criterio congelado.

Tolerancia replay absoluta 1e-10. Fallo de hash, ruta 2025 de evaluación, llave duplicada, diseño inválido o dependencia mutable detiene la corrida. Toda corrección sustantiva requiere versión nueva y declaración de exposición.
"""
    human = ROOT / "forense/prereg-caja" / f"ASTRA-ENVIPE-{pair}-spec-v1_0.md"
    human.write_text(md)
    (directory / "spec.md").write_text(md)
    md_sha = hashlib.sha256(md.encode()).hexdigest()
    adapter = '''"""Frozen C-ASTRA CALC adapter."""
import hashlib
import importlib.util
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
MODEL = ROOT / "tools/astra/envipe/model.py"
MODEL_SHA = "__MODEL_SHA__"
PAIR = "__PAIR__"
def medir(inputs, contrato):
    if hashlib.sha256(MODEL.read_bytes()).hexdigest() != MODEL_SHA:
        raise ValueError("C-ASTRA code changed since freeze")
    spec = importlib.util.spec_from_file_location("astra_envipe_model", MODEL)
    model = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model)
    history = [inputs[f"envipe{y}_csv"]["ruta_absoluta"] for y in (2023, 2024)]
    public = inputs["MARGINALES-PUBLICOS"]["bytes"]
    (pred, hyper), meta = model.run(PAIR, history, public)
    result = {}
    a, b = model.PAIRS[PAIR]
    for i, cell in enumerate((x, y) for x in model.ORDER[a] for y in model.ORDER[b]):
        key = f"RESULT-ASTRA-{PAIR}-{i+1:02d}"
        value = pred[cell]
        result[key+"-P"] = None if value is None else value[0]
        result[key+"-LO"] = None if value is None else value[1]
        result[key+"-HI"] = None if value is None else value[2]
        result[key+"-ESTADO"] = "NO-ESTIMABLE: denominador histórico o réplica vacía" if value is None else "ESTIMABLE: INTERVALO-PREDICTIVO-95"
    result[f"RESULT-ASTRA-{PAIR}-TAU2"] = hyper["tau2"]
    result[f"RESULT-ASTRA-{PAIR}-Q"] = hyper["q"]
    return result
'''.replace("__MODEL_SHA__", MODEL_SHA).replace("__PAIR__", pair)
    (directory / "medidor.py").write_text(adapter)
    outputs = []
    for i, (x, y) in enumerate(cells, 1):
        base = f"RESULT-ASTRA-{pair}-{i:02d}"
        for suffix in ("P", "LO", "HI"):
            outputs.append(dict(id=f"{base}-{suffix}", tipo="proporcion", unidad=f"{x} × {y}: predicción", permite_no_estimable=True))
        outputs.append(dict(id=f"{base}-ESTADO", tipo="texto", unidad=f"{x} × {y}: estado y causa"))
    for suffix in ("TAU2", "Q"):
        outputs.append(dict(id=f"RESULT-ASTRA-{pair}-{suffix}", tipo="flotante", unidad="varianza logit", permite_no_estimable=True))
    variables = []
    for year in (2023, 2024):
        for var in ("BP1_20", "BP1_23", "FAC_DEL", "EST_DIS", "UPM_DIS", "ID_PER", "SEXO", "EDAD", "DOMINIO"):
            variables.append(dict(archivo=f"conjunto_de_datos_tmod_vic_envipe{year}.csv", variable=var, rol="historico"))
        for var in ("ID_PER", "NIV"):
            variables.append(dict(archivo=f"conjunto_de_datos_tsdem_envipe{year}.csv", variable=var, rol="historico"))
    contract = dict(calc_id=calc, spec_md="spec.md", spec_md_sha256=md_sha,
        script=f"data/corrida0/{calc}/medidor.py",
        etiquetas=dict(generacion="GEN2", cuenta_gen2="SI", adopta="NO", origen_numerico="MICRODATO", exposicion_historica="CIEGO-A-ENVIPE2025-CRUCE-NO-ABIERTO", tipo_incertidumbre="PREDICTIVA-CONDICIONAL-MARGINALES-2025"),
        inputs=[dict(id=f"envipe{y}_csv", origen="manifiesto") for y in (2023, 2024)] + [dict(id="MARGINALES-PUBLICOS", origen="repo", ruta="milpa/tramite-ola5-propuesta-v0.yaml", sha256=PUBLIC_SHA)],
        variables=variables, universo="DELITO BP1_20 in {1,2}; conjunta BP1_20=2 y BP1_23 in {04,05,06,08}",
        filtros="FAC_DEL>0; EST_DIS/UPM_DIS completos; ID_PER único en tsdem; códigos fuera excluidos solo del eje",
        ponderador="FAC_DEL", transformacion="C2 + interacción normal EB dinámica v1.0; ver spec.md",
        estimando=f"Probabilidad predicha ENVIPE 2025 por celda {a} × {b}",
        parametros=dict(pair=pair, modelo_sha256=MODEL_SHA, replicas_upm=256, sorteos_predictivos=2048, seed=20260922,
            celdas=[dict(a=x, b=y) for x, y in cells]),
        seed=dict(aplica=True, valor=20260922, rng="numpy.PCG64"),
        dependencias_materiales=["numpy", "pandas", "PyYAML"], resultados=outputs,
        tolerancia=dict(tipo="flotante", abs=1e-10))
    (directory / "spec.yaml").write_text(yaml.safe_dump(contract, allow_unicode=True, sort_keys=False, width=120))
print("Generated four frozen CALC contracts")
