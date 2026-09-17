#!/usr/bin/env python3
"""`relevo-usos` -- ACTO GEN2-RELEVO-USOS-1 · cablea la ultima milla.

P1 del encargo, verbatim: «para cada uno de los 207 slots: ¿su corrida
natural ya tiene CALC sellada? Entregable: la tabla slot -> RESULT GEN2
candidato, o SIN-CANDIDATO con razon».

Este modulo NO MIDE, NO ADOPTA y NO ESCRIBE en `milpa/`. Deriva por LECTURA
el puente que hoy no existe en ninguna columna: el slot de demanda
(`RES-####`, un consumidor activo del aparato GEN1) frente al RESULT sellado
de oferta (`RESULT-…`, producto de un CALC GEN2) que podria relevarlo.

Por que se DERIVA y no se hereda por nombre
===========================================
`demanda-resultados.tsv:sucesor` esta vacio en las 207 filas y
`demanda-corridas.tsv` no trae columna CALC: su `medidor_o_spec_candidato`
declara un SCRIPT (`tools/emite_m.py`, `milpa/src/motor.py`, …), no un
`CALC-*`. El cruce CORR<->CALC no se resuelve por parecido de nombres --
`CALC-ENCIG-0001` no dice `CORR-0002` en su id -- y por eso el encargo lo
manda a derivar. La derivacion se hace por los TRES canales que las specs
DECLARAN, cada uno con su rotulo en la columna `canal`, sin elegir por
parecido y sin convertir una mencion negativa en candidatura:

  C1-MAPA      `parametros.adopcion*.consumidores`: mapa explicito
               `RES-#### -> "<consumidor> <- <destino>"`. Es el canal mas
               fuerte: fija consumidor Y RESULT, y esta dentro del bloque
               que el sello de la corrida cubre (`spec.yaml`).
  C1-SINGULAR  `parametros.adopcion*` con `{consumidor, result_id}` para un
               solo consumidor (patron de `CALC-B-0001` y `CALC-ENVIPE-0001`).
  C2-RESULTADO `resultados[].unidad` con una frase de enlace EXPLICITA
               (`releva RES-####`, `ADOPTABLE RES-####`, `candidato a
               RES-####`, `candidata de RES-####`). Fija RESULT por RESULT.
  C0-CONSUMIDOR El propio consumidor declara `corrida0_resultado_id` +
               `corrida0_generacion: GEN2` en `milpa/`. Se lee del ARCHIVO
               DEL CONSUMIDOR con el mismo resolvedor que usa `status`
               (`corrida0._ids_corrida0_declarados`) y NUNCA de `usos.tsv`:
               esa vista puede estar sin re-derivar -- hoy lo esta, porque
               el escritor canonico se NIEGA a reescribirla en esta sesion
               (ver la nota de cierre) -- y una tabla que se creyera la
               vista mentiria sobre adopciones que ya existen en el arbol.
               No es un canal para
               DESCUBRIR candidatos -- si el consumidor ya cita, el relevo
               esta hecho -- sino el CONTROL de los otros tres: la
               derivacion tiene que reproducir las 16 citas que hoy existen,
               o no merece credito sobre las que propone.
  C3-CORRIDA   `etiquetas.demanda_que_releva`, recortado ANTES de la primera
               negacion (`NO releva`, `NINGUNA`, `Residuo declarado`). Solo
               acredita COBERTURA de la corrida: dice que la corrida natural
               del slot ya tiene CALC, NO cual RESULT lo releva. Un slot que
               solo llega por C3 sale SIN-CANDIDATO con razon
               `CORR-CON-CALC-SIN-RESULT-FIJADO`, que es informacion, no un
               hueco: contesta la pregunta de P1 en su primera mitad.

El VEREDICTO SELLADO manda sobre los cuatro canales
====================================================
Varias specs pre-declararon, ANTES de medir, un RESULT de texto cuyo valor es
la rama de adopcion del slot (`RESULT-…-ADOPCION-P3-RES-0009`,
`…-ADOPCION-P3-COMPLEMENTOS`, `…-A-ADOPCION`). Ese veredicto ya esta MEDIDO y
SELLADO en `resultados.json`. Este modulo lo LEE y lo obedece: no vuelve a
decidir adoptabilidad ni la recalcula desde los valores. Un slot cuyo
veredicto sellado dice `NO-ADOPTABLE-POR-GRANO:-0.000032000` o
`COMPLEMENTO-CON-DENOMINADOR-RECORTADO` NO es candidato, aunque los canales
lo enlacen perfectamente -- y la razon que sale es el veredicto verbatim.
`LISTADO-PARA-MESA*` no es un no: es exactamente la lista que P4 sirve.

El veredicto se ata al slot por tres vias, en este orden y sin adivinar:
`RES-####` dentro del id del propio RESULT de veredicto; `RES-####` dentro de
su `unidad` declarada en la spec; o, solo cuando el CALC tiene UN veredicto y
UNA declaracion singular `adopcion*.{consumidor, result_id}`, esa pareja 1:1.

Dos resoluciones de mesa posteriores se aplican solo a sus identidades
cerradas: F-2 reevalua RES-0005 contra el valor vigente y el grano de su
consumidor, conservando `NO-ADOPTABLE-POR-DISCREPANCIA` como veredicto
historico; F-3 adjudica el conflicto sellado de RES-0035. No forman una regla
general de precedencia y dejan de aplicar si falla cualquiera de sus
compuertas de identidad, firma, sello, valor o grano.

Reglas que el codigo no negocia
===============================
  · Ningun canal INFIERE. Si `<destino>` no resuelve a un RESULT unico del
    mismo CALC, sale `RESULT-NO-RESUELTO:<destino>` y no se elige el mas
    parecido. El `<destino>` de C1 se resuelve en DOS pasos y ninguno admite
    empate: (a) sufijo exacto (`A-P-SOL1` -> `RESULT-ENCIG-MOR-A-P-SOL1`);
    (b) sufijo + `-P`, el punto de la familia (`A-P-CORTO-SIN` ->
    `RESULT-ENIF-AHO-A-P-CORTO-SIN-P`, que convive con veintiun hermanos
    `-IC-LO`, `-N-UPM`, `-S1-P`…). El paso (b) NO es una convencion
    inventada aqui: se acepta porque el control C0 lo verifica -- reproduce
    exactamente las citas que los consumidores YA declaran -- y se rechaza
    en cuanto no es unico.
  · Un candidato exige corrida de oferta SELLADA, `sello=COINCIDE` y
    `cuenta_gen2=SI`. Un CALC con spec fijada y sin sellar NO produce
    candidato: sale `CALC-DECLARADA-NO-SELLADA`.
  · Los canales se CRUZAN, no se colapsan: si dos fijan RESULT distintos
    para el mismo slot, sale `CONFLICTO-ENTRE-CANALES` con ambos, y la
    decision es de mesa.
  · La adopcion vigente (`usos.tsv`) no se toca ni se re-decide: un slot ya
    en GEN2 sale `YA-ADOPTADO`, y si lo derivado discrepa de lo adoptado se
    rotula `DISCREPANCIA-CON-ADOPTADO` en vez de pisar nada.
  · Un `SIN CITA` del mapa C1 es una decision de mesa ya firmada y VETA el
    slot: ningun otro canal lo resucita.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime
import json
import re
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "tools"))

import corrida0  # noqa: E402

C0 = RAIZ / "data" / "corrida0"
SALIDA_TSV = C0 / "relevo-usos-v1_0.tsv"

NO_DECLARADO = "NO-DECLARADO-EN-EL-REGISTRO"

COLUMNAS = [
    "resultado_id", "consumidor", "tipo_uso", "reglas_impacto",
    "corrida_natural", "generacion_hoy", "veredicto",
    "calc_candidato", "corrida_oferta", "estado_calc", "sello_calc",
    "result_gen2_candidato", "valor_gen2", "valor_legacy",
    "canal", "canales_observados", "control_c0", "veredicto_sellado",
    "veredicto_sellado_ref", "resolucion_vigente", "otras_candidaturas",
    "razon",
    # P3 · materialidad POR CONSUMIDOR (E.4). Vacias mientras no se pase
    # `--p3`: una columna vacia dice «no se corrio», que no es lo mismo que
    # «no hay diferencia».
    "delta_gen2_menos_legacy", "representacion_al_grano", "grano_consumidor",
    "cambia_signo", "cruza_grano_del_consumidor", "cruza_umbral_grano_milpa",
    "cambia_clasificacion", "es_coeficiente_central", "tier_consumidor",
    "materialidad_consumidor", "razon_materialidad",
]

P3_VACIAS = {c: "" for c in (
    "delta_gen2_menos_legacy", "representacion_al_grano", "grano_consumidor",
    "cambia_signo", "cruza_grano_del_consumidor", "cruza_umbral_grano_milpa",
    "cambia_clasificacion", "es_coeficiente_central", "tier_consumidor",
    "materialidad_consumidor", "razon_materialidad")}

# Frase de enlace EXPLICITA en `resultados[].unidad` (canal C2). El RES tiene
# que ir INMEDIATAMENTE despues del verbo: `(RES-0004/0010/0012)` dentro de
# una enumeracion sin verbo NO enlaza, y ese es el punto -- la lista de
# complementos de CALC-ENCIG-0001 no debe convertirse en seis candidaturas.
RE_ENLACE = re.compile(
    r"(?:releva|ADOPTABLE|candidato a|candidata a|candidato de|candidata de)"
    r"\s+(RES-\d{4})")
RE_RES = re.compile(r"RES-\d{4}")
RE_CORR = re.compile(r"CORR-\d{4}")
# Corte de la clausula positiva de `demanda_que_releva` (canal C3).
RE_NEGACION = re.compile(
    r"\bNO\s+(?:se\s+)?releva\b|\bNINGUNA\b|\bResiduo declarado\b|"
    r"\bno\s+forma\s+parte\b", re.IGNORECASE)

SELLADA = ("SELLADA", "SUPERADO")

# Ramas de veredicto sellado que SI habilitan candidatura. Es una lista
# CERRADA y copiada de las specs: no se acepta una rama nueva por parecerse.
ADOPTABLES = {"CANTIDAD-MEDIDA-ADOPTABLE", "ADOPTABLE-POR-REPLICA",
              "ADOPTABLE"}

# F-2 de `2026-09-15-GEN2-FIRMAS-MESA-2.md` resuelve UNA contradiccion
# historica, condicionada en cada derivacion por F-1. La resolucion no cambia
# ni el RESULT sellado ni el valor/cita del consumidor: solo acredita que el
# valor vigente sigue materializando el RESULT al grano que el consumidor
# escribe. Cualquier cambio de estas identidades vuelve a cerrar la compuerta.
F2_RES = "RES-0005"
F2_CONSUMIDOR = (
    "milpa/tramite.yaml:tramite.mordida.discrecional:"
    "solicitud_o_entrega_mordida_encuci2020")
F2_CALC = "CALC-ENCUCI-0001"
F2_CORRIDA = "CALC-ENCUCI-0001--18d21cdff449"
F2_RESULT = "RESULT-ENCUCI-A-P-CUALQUIERA"
F2_HISTORICO = (
    F2_CALC, "RESULT-ENCUCI-A-ADOPCION-P3",
    "NO-ADOPTABLE-POR-DISCREPANCIA")
F2_SPEC_SHA256 = (
    "f29561fbe59b550b398f05505e9891c5c512d6674eddf4924c904e0c406d678a")
F2_AUTORIDAD = RAIZ / "forense" / "encargos" / \
    "2026-09-15-GEN2-FIRMAS-MESA-2.md"
F2_FIRMA_FRAGMENTOS = (
    'FIRMA DE MESA, verbatim: "Si a todos."',
    "F-1 · NC-0214 — el árbol declara dos tolerancias que no coinciden",
    "F-2 · NC-0217 — RES-0005 cita GEN2 pero su corrida sellada dice "
    "NO-ADOPTABLE-POR-DISCREPANCIA",
)

# F-3 de `2026-09-15-GEN2-FIRMAS-MESA-2.md` adjudica UNA pareja para UN
# consumidor. No es una politica general de "el mas reciente gana": estas
# identidades selladas son parte de la compuerta y un re-sellado distinto
# vuelve a dejar el conflicto explicito para mesa.
F3_RES = "RES-0035"
F3_CONSUMIDOR = (
    "milpa/tramite.yaml:familia.seguro.volatilidad_ausencia_estado:"
    "recibe_remesas")
F3_ANTERIOR = (
    "CALC-B-0001", "RESULT-B-ADOPCION-P3", "NO-ADOPTABLE-POR-GRANO")
F3_VIGENTE = (
    "CALC-ENIGH-0001", "RESULT-ENIGH-A-ADOPCION",
    "LISTADO-PARA-MESA-REPRODUCE")
F3_CORRIDAS = {
    "CALC-B-0001": "CALC-B-0001--098298ca327f",
    "CALC-ENIGH-0001": "CALC-ENIGH-0001--d13529e2e3e9",
}
F3_SPEC_SHA256 = {
    "CALC-B-0001":
        "7feed075d55bf795f921bc7bd0d75ac8bffa60b205822cf1333364a2c67efe16",
    "CALC-ENIGH-0001":
        "1555d052cf0c9ebbf91d1080c6be976b64191fb932dfa04083d7804bc0ce4566",
}


def _instante_acreditable(texto: str):
    """Instante ISO-8601 con zona; nunca cae a mtime, commit ni nombre."""
    try:
        instante = datetime.fromisoformat(str(texto).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    return instante if instante.utcoffset() is not None else None


def _evidencia_ejecucion_f3(calc: str) -> dict:
    """Lee el recibo y verifica los bytes cubiertos por su sello."""
    ruta = C0 / calc / "ejecucion.json"
    if not ruta.is_file():
        return {}
    try:
        evidencia = json.loads(ruta.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    sello, detalle = corrida0._verifica_sello(C0 / calc)
    evidencia["__sello_archivos__"] = sello
    evidencia["__detalle_sello__"] = detalle
    return evidencia


def _firma_f2_acreditada() -> bool:
    """La decision F-1/F-2 debe seguir presente con su firma exacta."""
    try:
        texto = F2_AUTORIDAD.read_text(encoding="utf-8")
    except OSError:
        return False
    return all(fragmento in texto for fragmento in F2_FIRMA_FRAGMENTOS)


def _resultados_sellados(calc: str) -> dict:
    """RESULT del artefacto cubierto por sello; nunca de una vista historica."""
    ruta = C0 / calc / "resultados.json"
    try:
        crudo = json.loads(ruta.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    resultados = crudo.get("resultados", crudo)
    return resultados if isinstance(resultados, dict) else {}


def _resuelve_f2_encuci(res: str, consumidor: str, ramas: list[tuple],
                        oferta: dict[str, dict], ejecucion: dict,
                        punto: dict | None, resultados_sellados: dict,
                        uso: dict, spec: dict, firma_acreditada: bool):
    """Aplica F-2 a su pareja exacta o devuelve una causa no acreditada.

    `None` significa fuera del alcance. `aplica=True` solo significa que la
    resolucion F-2 es efectiva AHORA; se recalcula desde el valor vigente de
    `milpa/` en cada llamada a `deriva()`.
    """
    if res != F2_RES or consumidor != F2_CONSUMIDOR:
        return None

    def no(causa: str, resolucion: str = "F2-NO-ACREDITADA") -> dict:
        return {"aplica": False, "resolucion": resolucion, "causa": causa}

    if ramas != [F2_HISTORICO]:
        return no("CALC-RESULT-VEREDICTO-HISTORICO-DISTINTO")
    if not firma_acreditada:
        return no("FIRMA-F1-F2-AUSENTE-O-INVALIDA")

    corrida = oferta.get(F2_CALC)
    if not corrida:
        return no(f"CORRIDA-AUSENTE:{F2_CALC}")
    if (corrida.get("corrida_id") != F2_CORRIDA
            or corrida.get("spec_id") != F2_CALC
            or corrida.get("spec_yaml_sha256") != F2_SPEC_SHA256):
        return no(f"IDENTIDAD-SELLADA-DISTINTA:{F2_CALC}")
    if (not str(corrida.get("estado", "")).startswith(SELLADA)
            or corrida.get("sello") != "COINCIDE"
            or corrida.get("cuenta_gen2") != "SI"):
        return no(f"SELLO-NO-VALIDO:{F2_CALC}")

    campos = (
        ("corrida_id", "corrida_id"),
        ("spec_id", "spec_id"),
        ("fecha", "fecha"),
        ("git_commit", "codigo_commit"),
        ("script_path", "script_path"),
        ("script_blob_sha256", "script_blob_sha256"),
        ("spec_yaml_sha256", "spec_yaml_sha256"),
    )
    if not ejecucion:
        return no(f"EJECUCION-AUSENTE-O-ILEGIBLE:{F2_CALC}")
    if (ejecucion.get("__sello_archivos__") != "COINCIDE"
            or ejecucion.get("exit_code") != 0
            or ejecucion.get("error") is not None):
        return no(f"ARTEFACTOS-NO-SELLADOS:{F2_CALC}")
    for campo_ejecucion, campo_corrida in campos:
        if ejecucion.get(campo_ejecucion) != corrida.get(campo_corrida):
            return no(f"EJECUCION-NO-CORRESPONDE:{F2_CALC}:"
                      f"{campo_ejecucion}")

    if punto is None:
        return no(f"RESULT-AUSENTE-EN-LA-VISTA:{F2_RESULT}")
    if (punto.get("spec_id") != F2_CALC
            or punto.get("corrida_id") != F2_CORRIDA
            or punto.get("estado") != "SELLADA"
            or punto.get("sello") != "COINCIDE"):
        return no(f"RECIBO-RESULT-NO-CORRESPONDE:{F2_RESULT}")
    if resultados_sellados.get(F2_HISTORICO[1]) != F2_HISTORICO[2]:
        return no(f"VEREDICTO-SELLADO-DISTINTO:{F2_HISTORICO[1]}")
    try:
        valor_result = float(resultados_sellados[F2_RESULT])
        valor_recibo = float(punto["valor"])
    except (KeyError, TypeError, ValueError):
        return no(f"VALOR-RESULT-AUSENTE-O-ILEGIBLE:{F2_RESULT}")
    if valor_result != valor_recibo:
        return no(f"RESULT-NO-CONCUERDA-CON-RECIBO:{F2_RESULT}")

    if (uso.get("generacion") != "GEN2"
            or uso.get("resultado_id") != F2_RESULT):
        return no("CITA-VIGENTE-DISTINTA-O-AUSENTE")
    valor_consumidor = uso.get("valor", NO_DECLARADO)
    try:
        coincide, delta, modo = corrida0._compara_adopcion(
            valor_result, valor_consumidor,
            {"tipo": punto.get("tipo")}, spec.get("tolerancia") or {},
            corrida0._tol_adopcion_de(punto))
    except (TypeError, ValueError):
        return no("VALOR-VIGENTE-O-CONTRATO-DE-GRANO-ILEGIBLE")
    if not str(modo).startswith("grano del consumidor = "):
        return no(f"F1-GRANO-NO-ACREDITADO:{modo}")
    comun = {
        "valor_result": valor_result,
        "valor_consumidor": valor_consumidor,
        "delta": delta,
        "modo": modo,
    }
    if not coincide:
        return {
            "aplica": False,
            "resolucion": "CITA-PENDIENTE-DE-RETIRO-POR-F2",
            "causa": "VALOR-VIGENTE-DISTINTO-AL-GRANO",
            **comun,
        }
    return {
        "aplica": True,
        "resolucion": "SUPERADO-POR-F2",
        "causa": "COINCIDE-AL-GRANO",
        **comun,
    }


def _resuelve_f3_remesas(res: str, consumidor: str, ramas: list[tuple],
                         oferta: dict[str, dict], evidencias: dict[str, dict],
                         coincide_grano: bool, modo_grano: str):
    """Aplica la adjudicacion acotada F-3 o explica por que no aplica.

    `None` significa que el caso ni siquiera esta dentro del alcance de F-3.
    Un dict con `aplica=False` conserva el conflicto y deja su causa en la
    columna explicativa existente.
    """
    if res != F3_RES or consumidor != F3_CONSUMIDOR:
        return None

    esperadas = sorted((F3_ANTERIOR, F3_VIGENTE))
    if sorted(ramas) != esperadas:
        return {"aplica": False,
                "causa": "PAREJA-CALC-RESULT-VEREDICTO-DISTINTA"}
    if not coincide_grano or not modo_grano.startswith(
            "grano del consumidor = "):
        return {"aplica": False,
                "causa": f"F1-GRANO-NO-ACREDITADO:{modo_grano or 'AUSENTE'}"}

    instantes = {}
    campos = (
        ("corrida_id", "corrida_id"),
        ("spec_id", "spec_id"),
        ("fecha", "fecha"),
        ("git_commit", "codigo_commit"),
        ("script_path", "script_path"),
        ("script_blob_sha256", "script_blob_sha256"),
        ("spec_yaml_sha256", "spec_yaml_sha256"),
    )
    for calc in (F3_ANTERIOR[0], F3_VIGENTE[0]):
        corrida, ejecucion = oferta.get(calc), evidencias.get(calc)
        if not corrida:
            return {"aplica": False, "causa": f"CORRIDA-AUSENTE:{calc}"}
        if (corrida.get("corrida_id") != F3_CORRIDAS[calc]
                or corrida.get("spec_yaml_sha256") != F3_SPEC_SHA256[calc]):
            return {"aplica": False,
                    "causa": f"IDENTIDAD-SELLADA-DISTINTA:{calc}"}
        if (not str(corrida.get("estado", "")).startswith(SELLADA)
                or corrida.get("sello") != "COINCIDE"
                or corrida.get("cuenta_gen2") != "SI"):
            return {"aplica": False, "causa": f"SELLO-NO-VALIDO:{calc}"}
        if not ejecucion:
            return {"aplica": False,
                    "causa": f"EJECUCION-AUSENTE-O-ILEGIBLE:{calc}"}
        if (ejecucion.get("__sello_archivos__") != "COINCIDE"
                or ejecucion.get("exit_code") != 0
                or ejecucion.get("error") is not None):
            return {"aplica": False,
                    "causa": f"ARTEFACTOS-NO-SELLADOS:{calc}"}
        for campo_ejecucion, campo_corrida in campos:
            if ejecucion.get(campo_ejecucion) != corrida.get(campo_corrida):
                return {"aplica": False,
                        "causa": (f"EJECUCION-NO-CORRESPONDE:{calc}:"
                                  f"{campo_ejecucion}")}
        instante = _instante_acreditable(ejecucion.get("fecha"))
        if instante is None:
            return {"aplica": False,
                    "causa": f"FECHA-NO-ACREDITABLE:{calc}"}
        instantes[calc] = instante

    if instantes[F3_VIGENTE[0]] <= instantes[F3_ANTERIOR[0]]:
        return {"aplica": False,
                "causa": "ORDEN-SELLADO-NO-ACREDITADO"}
    return {
        "aplica": True,
        "valor": F3_VIGENTE[2],
        "referencia": (
            f"{F3_ANTERIOR[0]}/{F3_ANTERIOR[1]}=SUPERADO->"
            f"{F3_VIGENTE[0]}/{F3_VIGENTE[1]}"),
    }


def _res_ids(texto: str) -> set[str]:
    """`RES-####` de un texto, incluyendo las DOS abreviaturas que el arbol
    usa de verdad: la lista con barra (`RES-0004/0010/0012`) y el rango con
    puntos (`RES-0009..0016`). Leerlas importa: el veredicto conjunto de los
    seis complementos de `CALC-ENCIG-0001` vive escrito con barras, y un
    lector ingenuo se lleva solo el primero y deja cinco slots sin veredicto.
    El rango se acota a 64 para que un texto raro no explote la derivacion."""
    out: set[str] = set()
    for m in re.finditer(r"RES-(\d{4})((?:\s*(?:/|\.\.)\s*\d{4})*)", texto):
        base = int(m.group(1))
        out.add(f"RES-{base:04d}")
        cola, previo = m.group(2) or "", base
        for sep, num in re.findall(r"(/|\.\.)\s*(\d{4})", cola):
            num = int(num)
            if sep == "..":
                if 0 <= num - previo <= 64:
                    out |= {f"RES-{i:04d}" for i in range(previo, num + 1)}
            else:
                out.add(f"RES-{num:04d}")
            previo = num
    return out


def _lee_tsv(ruta: Path) -> list[dict]:
    with ruta.open(encoding="utf-8") as fh:
        lineas = [l for l in fh if not l.startswith("#")]
    return list(csv.DictReader(lineas, delimiter="\t"))


def _specs() -> dict[str, dict]:
    """`CALC-id -> spec.yaml` cargado. La ruta manda: el id es el directorio,
    no un campo que pudiera discrepar de donde vive el archivo."""
    out = {}
    for ruta in sorted(C0.glob("*/spec.yaml")):
        try:
            out[ruta.parent.name] = corrida0._yaml_safe_load(
                ruta.read_text(encoding="utf-8")) or {}
        except Exception as exc:                       # spec ilegible: se
            out[ruta.parent.name] = {"__error__": str(exc)}   # DECLARA
    return out


def _resuelve_destino(destino: str, ids_result: list[str]) -> tuple[str, str]:
    """`<destino>` del mapa C1 -> `(result_id, razon)`.

    `destino` viene en tres formas y ninguna se adivina: el RESULT completo,
    un SUFIJO de el (`A-P-SOL1` por `RESULT-ENCIG-MOR-A-P-SOL1`), o una
    declaracion de que NO hay cita. El sufijo se acepta solo si empareja con
    UN unico RESULT del mismo CALC."""
    destino = (destino or "").strip()
    if not destino:
        return "", "DESTINO-VACIO"
    if "SIN CITA" in destino.upper():
        return "", f"DESTINO-SIN-CITA:{destino}"
    if destino in ids_result:
        return destino, ""
    for sufijo in ("-" + destino, "-" + destino + "-P"):
        cand = [r for r in ids_result if r.endswith(sufijo)]
        if len(cand) == 1:
            return cand[0], ""
        if len(cand) > 1:
            return "", (f"DESTINO-AMBIGUO:{destino}->"
                        f"{'|'.join(sorted(cand))}")
    return "", f"RESULT-NO-RESUELTO:{destino}"


def _veredictos(calc: str, spec: dict, singulares: list,
                res_c3: set[str]) -> dict[str, tuple[str, str]]:
    """`RES -> (result_id_del_veredicto, valor_sellado)` para un CALC.

    Lee `resultados.json` -- el archivo que el sello cubre -- y NO el TSV
    derivado: el veredicto es un hecho de la corrida, no de la vista. Los
    `…-DELTA` quedan fuera a proposito: son la magnitud, no la rama."""
    ruta = C0 / calc / "resultados.json"
    if not ruta.is_file():
        return {}
    try:
        crudo = json.loads(ruta.read_text(encoding="utf-8"))
    except Exception:
        return {}
    crudo = crudo.get("resultados", crudo)
    if not isinstance(crudo, dict):
        return {}
    unidades = {str(r.get("id")): str(r.get("unidad", ""))
                for r in (spec.get("resultados") or []) if isinstance(r, dict)}
    ramas = {k: v for k, v in crudo.items()
             if "ADOPCION" in k.upper() and not k.upper().endswith("-DELTA")
             and isinstance(v, str)}
    out: dict[str, tuple[str, str]] = {}
    for rid, valor in ramas.items():
        for res in _res_ids(rid) | _res_ids(unidades.get(rid, "")):
            out[res] = (rid, valor)
    # 1:1 -- un solo veredicto y una sola declaracion singular en el CALC.
    sin_atar = [r for r in ramas if not (_res_ids(r) | _res_ids(unidades.get(r, "")))]
    if len(sin_atar) == 1 and len(singulares) == 1:
        out.setdefault("__singular__", (sin_atar[0], ramas[sin_atar[0]]))
    elif len(sin_atar) == 1 and res_c3:
        # UN solo veredicto en todo el CALC y una clausula positiva que
        # nombra los slots que el CALC releva: la rama es de esos slots y de
        # ningun otro. Es la forma de `CALC-ENFIH-0001`, `CALC-ENUT-0001`,
        # `CALC-L8-CONVERSION-0001` y hermanas -- specs de UNA familia, donde
        # el veredicto no repite el `RES-####` porque no hay con quien
        # confundirlo. Con DOS o mas veredictos sin atar no se reparte nada.
        for res in res_c3:
            out.setdefault(res, (sin_atar[0], ramas[sin_atar[0]]))
    return out


def _canal_c1(spec: dict) -> tuple[dict, list[tuple[str, str, str]]]:
    """`parametros.adopcion*` -> (`RES -> (destino, consumidor)`, singulares).

    Devuelve el mapa plural por RES y la lista de declaraciones singulares
    `(consumidor, result_id, clave)`, que se cruzan por consumidor y no por
    RES porque el bloque singular no nombra el slot."""
    mapa, singulares = {}, []
    par = spec.get("parametros")
    if not isinstance(par, dict):
        return mapa, singulares
    for clave, valor in par.items():
        if not str(clave).startswith("adopcion") or not isinstance(valor, dict):
            continue
        consumidores = valor.get("consumidores")
        if isinstance(consumidores, dict):
            for res, texto in consumidores.items():
                if not RE_RES.fullmatch(str(res)):
                    continue
                texto = str(texto)
                destino = texto.split("<-", 1)[1] if "<-" in texto else ""
                consumidor = texto.split("<-", 1)[0].strip()
                mapa[str(res)] = (destino.strip(), consumidor)
        elif valor.get("result_id"):
            singulares.append((str(valor.get("consumidor", "")),
                               str(valor["result_id"]), str(clave)))
    return mapa, singulares


def _canal_c2(spec: dict) -> dict[str, list[str]]:
    """`resultados[].unidad` con frase de enlace -> `RES -> [RESULT, …]`."""
    out: dict[str, list[str]] = {}
    for fila in spec.get("resultados") or []:
        if not isinstance(fila, dict):
            continue
        for res in RE_ENLACE.findall(str(fila.get("unidad", ""))):
            out.setdefault(res, []).append(str(fila.get("id", "")))
    return out


def _canal_c3(spec: dict) -> tuple[set[str], set[str]]:
    """`etiquetas.demanda_que_releva` -> (`{CORR}`, `{RES}`) de la clausula
    POSITIVA. Todo lo que sigue a la primera negacion se descarta entero: es
    justo donde viven los «NO releva RES-0031/RES-0032»."""
    etiquetas = spec.get("etiquetas")
    texto = str((etiquetas or {}).get("demanda_que_releva", "")) \
        if isinstance(etiquetas, dict) else ""
    if not texto:
        return set(), set()
    corte = RE_NEGACION.search(texto)
    positiva = texto[:corte.start()] if corte else texto
    return set(RE_CORR.findall(positiva)), set(RE_RES.findall(positiva))


def deriva() -> tuple[list[dict], dict]:
    slots = _lee_tsv(C0 / "demanda-resultados.tsv")
    corridas = _lee_tsv(C0 / "corridas.tsv")
    resultados = _lee_tsv(C0 / "resultados.tsv")
    declarado = corrida0._ids_corrida0_declarados()
    specs = _specs()

    # Corridas de OFERTA por CALC. Un CALC con varias corridas (re-sellados,
    # `-v2`) conserva la SELLADA mas reciente por fecha: el registro ya las
    # distingue por `corrida_id`, aqui no se inventa una regla nueva.
    oferta: dict[str, dict] = {}
    for fila in corridas:
        if fila["origen"] != "OFERTA":
            continue
        previa = oferta.get(fila["spec_id"])
        if previa is None or (fila["estado"].startswith(SELLADA)
                              and fila["fecha"] > previa["fecha"]):
            oferta[fila["spec_id"]] = fila
    valor_result = {(r["corrida_id"], r["resultado_id"]): r
                    for r in resultados if r["origen"] == "OFERTA"}
    evidencias_f3 = {calc: _evidencia_ejecucion_f3(calc)
                     for calc in F3_CORRIDAS}
    evidencia_f2 = _evidencia_ejecucion_f3(F2_CALC)
    resultados_f2 = _resultados_sellados(F2_CALC)
    firma_f2 = _firma_f2_acreditada()

    # Indices de los tres canales, construidos UNA vez sobre todas las specs.
    c1_por_res: dict[str, list[tuple[str, str, str]]] = {}
    c1_singular: list[tuple[str, str, str, str]] = []
    c2_por_res: dict[str, list[tuple[str, str]]] = {}
    c3_corr: dict[str, set[str]] = {}
    c3_res: dict[str, set[str]] = {}
    vered: dict[str, list[tuple[str, str, str]]] = {}   # RES -> [(calc, rid, valor)]
    vered_singular: dict[str, tuple[str, str]] = {}     # consumidor -> (rid, valor)
    veto: dict[str, list[tuple[str, str]]] = {}         # RES -> [(calc, texto)]
    for calc, spec in sorted(specs.items()):
        if "__error__" in spec:
            continue
        ids_result = [str(r.get("id")) for r in (spec.get("resultados") or [])
                      if isinstance(r, dict)]
        mapa, singulares = _canal_c1(spec)
        for res, (destino, consumidor) in mapa.items():
            rid, razon = _resuelve_destino(destino, ids_result)
            if razon.startswith("DESTINO-SIN-CITA"):
                veto.setdefault(res, []).append((calc, razon))
            c1_por_res.setdefault(res, []).append((calc, rid, razon))
        for consumidor, rid, _clave in singulares:
            c1_singular.append((consumidor, calc, rid, "C1-SINGULAR"))
        for res, rids in _canal_c2(spec).items():
            for rid in rids:
                c2_por_res.setdefault(res, []).append((calc, rid))
        corrs, ress = _canal_c3(spec)
        for res, (rid, valor) in _veredictos(
                calc, spec, singulares, ress).items():
            if res == "__singular__":
                vered_singular[singulares[0][0]] = (calc, rid, valor)
            else:
                vered.setdefault(res, []).append((calc, rid, valor))
        for corr in corrs:
            c3_corr.setdefault(corr, set()).add(calc)
        for res in ress:
            c3_res.setdefault(res, set()).add(calc)

    filas, contadores = [], {}
    for slot in slots:
        res = slot["resultado_id"]
        uso = declarado.get(slot["consumidor"], {})
        fila = {
            "resultado_id": res,
            "consumidor": slot["consumidor"],
            "tipo_uso": slot["tipo"],
            "reglas_impacto": corrida0._regla_de(slot["consumidor"]),
            "corrida_natural": slot["corrida_natural"] or NO_DECLARADO,
            "generacion_hoy": uso.get("generacion") or corrida0.GENERACION_LEGADO,
            "veredicto": "", "calc_candidato": "", "corrida_oferta": "",
            "estado_calc": "", "sello_calc": "",
            "result_gen2_candidato": "", "valor_gen2": "",
            "valor_legacy": slot["valor_legacy"] or NO_DECLARADO,
            "canal": "", "canales_observados": "", "control_c0": "",
            "veredicto_sellado": "", "veredicto_sellado_ref": "",
            "resolucion_vigente": "",
            "otras_candidaturas": "", "razon": "", **P3_VACIAS,
        }
        cita_c0 = (uso.get("resultado_id", "")
                   if uso.get("generacion") == "GEN2" else "")

        # ── veredicto SELLADO del slot (manda sobre los canales) ──────────
        ramas = list(vered.get(res, []))
        sing = vered_singular.get(slot["consumidor"])
        if sing:
            ramas.append(sing)
        if len({r[2] for r in ramas}) > 1:
            refs_conflicto = ";".join(
                f"{c}/{r}={v}" for c, r, v in sorted(ramas))
            coincide_grano, modo_grano = False, "RESULT-ENIGH-A-P-AUSENTE"
            corr_enigh = oferta.get(F3_VIGENTE[0])
            punto_enigh = (valor_result.get(
                (corr_enigh["corrida_id"], "RESULT-ENIGH-A-P"))
                if corr_enigh else None)
            if punto_enigh is not None:
                try:
                    coincide_grano, _delta, modo_grano = \
                        corrida0._compara_adopcion(
                            float(punto_enigh["valor"]),
                            float(slot["valor_legacy"]),
                            {"tipo": "proporcion"},
                            specs[F3_VIGENTE[0]].get("tolerancia") or {})
                except (KeyError, TypeError, ValueError):
                    modo_grano = "CONTRATO-DE-GRANO-ILEGIBLE"
            f3 = _resuelve_f3_remesas(
                res, slot["consumidor"], ramas, oferta, evidencias_f3,
                coincide_grano, modo_grano)
            if f3 and f3["aplica"]:
                fila["veredicto_sellado"] = f3["valor"]
                fila["veredicto_sellado_ref"] = f3["referencia"]
            else:
                fila["veredicto_sellado"] = "CONFLICTO-ENTRE-VEREDICTOS"
                fila["veredicto_sellado_ref"] = refs_conflicto
                if f3:
                    fila["veredicto_sellado_ref"] += (
                        f";F-3-NO-APLICA:{f3['causa']}")
        elif ramas:
            calc_v, rid_v, valor_v = ramas[0]
            fila["veredicto_sellado"] = valor_v
            fila["veredicto_sellado_ref"] = f"{calc_v}/{rid_v}"
        else:
            fila["veredicto_sellado"] = "SIN-VEREDICTO-SELLADO"
            fila["veredicto_sellado_ref"] = "NINGUNO"

        # ── candidaturas por canal, sin colapsar ──────────────────────────
        cands: list[tuple[str, str, str, str]] = []   # (canal, calc, rid, razon)
        for calc, rid, razon in c1_por_res.get(res, []):
            cands.append(("C1-MAPA", calc, rid, razon))
        for consumidor, calc, rid, canal in c1_singular:
            if consumidor and consumidor == slot["consumidor"]:
                cands.append((canal, calc, rid, ""))
        for calc, rid in c2_por_res.get(res, []):
            cands.append(("C2-RESULTADO", calc, rid, ""))
        cobertura = set(c3_corr.get(slot["corrida_natural"], set())) \
            | set(c3_res.get(res, set()))
        fila["canales_observados"] = ";".join(sorted(
            {c[0] for c in cands}
            | ({"C3-CORRIDA"} if cobertura else set())
            | ({"C0-CONSUMIDOR"} if cita_c0 else set()))) or "NINGUNO"

        # ── se exige oferta SELLADA con sello COINCIDE y cuenta_gen2 SI ───
        firmes, blandas = [], []
        for canal, calc, rid, razon in cands:
            corr = oferta.get(calc)
            if corr is None:
                blandas.append((canal, calc, rid, "CALC-SIN-CORRIDA-DE-OFERTA"))
            elif not corr["estado"].startswith(SELLADA):
                blandas.append((canal, calc, rid,
                                f"CALC-DECLARADA-NO-SELLADA:{corr['estado']}"))
            elif corr["sello"] != "COINCIDE":
                blandas.append((canal, calc, rid,
                                f"SELLO-NO-COINCIDE:{corr['sello']}"))
            elif corr["cuenta_gen2"] != "SI":
                blandas.append((canal, calc, rid,
                                f"NO-CUENTA-GEN2:{corr['motivo_cuenta_gen2']}"))
            elif razon:
                blandas.append((canal, calc, rid, razon))
            elif (corr["corrida_id"], rid) not in valor_result:
                blandas.append((canal, calc, rid,
                                f"RESULT-AUSENTE-EN-LA-VISTA:{rid}"))
            else:
                firmes.append((canal, calc, rid, corr))

        # Nada se descarta en silencio: toda candidatura que NO paso las
        # compuertas queda escrita con el motivo por el que no paso.
        fila["otras_candidaturas"] = ";".join(sorted(
            f"{canal}/{calc}/{rid or 'SIN-RESULT'}/{motivo}"
            for canal, calc, rid, motivo in blandas)) or "NINGUNA"

        distintos = {f[2] for f in firmes}
        if len(distintos) > 1:
            fila["veredicto"] = "CONFLICTO-ENTRE-CANALES"
            fila["canal"] = ";".join(sorted({f[0] for f in firmes}))
            fila["calc_candidato"] = ";".join(sorted({f[1] for f in firmes}))
            fila["result_gen2_candidato"] = ";".join(sorted(distintos))
            fila["razon"] = ("dos canales declarados fijan RESULT distintos "
                             "para el mismo slot; el registro no decide cual")
        elif firmes:
            canal, calc, rid, corr = firmes[0]
            r = valor_result[(corr["corrida_id"], rid)]
            fila.update(calc_candidato=calc, corrida_oferta=corr["corrida_id"],
                        estado_calc=corr["estado"], sello_calc=corr["sello"],
                        result_gen2_candidato=rid, valor_gen2=r["valor"],
                        canal=";".join(sorted({f[0] for f in firmes})))
            if cita_c0:
                fila["veredicto"] = ("YA-ADOPTADO" if cita_c0 == rid
                                     else "DISCREPANCIA-CON-ADOPTADO")
                fila["control_c0"] = ("COINCIDE" if cita_c0 == rid
                                      else f"DISCREPA:{cita_c0}")
                fila["razon"] = (
                    f"el consumidor ya cita {cita_c0} con corrida0_generacion"
                    f"=GEN2 y la derivacion lo reproduce" if cita_c0 == rid
                    else f"el consumidor cita {cita_c0}; lo derivado fija {rid}")
            elif res in veto:
                fila["veredicto"] = "VETADO-POR-DECISION"
                fila["razon"] = ";".join(
                    f"{c}: {t}" for c, t in sorted(veto[res]))
            elif fila["veredicto_sellado"] in ADOPTABLES:
                fila["veredicto"] = "CANDIDATO-GEN2"
                fila["razon"] = (
                    f"{calc} sellada ({corr['sello']}) declara este relevo por "
                    f"{canal}; veredicto sellado {fila['veredicto_sellado']}")
            elif fila["veredicto_sellado"] == "SIN-VEREDICTO-SELLADO":
                fila["veredicto"] = "CANDIDATO-GEN2"
                fila["razon"] = (
                    f"{calc} sellada ({corr['sello']}) declara este relevo por "
                    f"{canal}; la spec no pre-declaro rama de adopcion para "
                    f"este slot -- la comparacion la hace P2, no este canal")
            elif fila["veredicto_sellado"].startswith("LISTADO-PARA-MESA"):
                fila["veredicto"] = "LISTADO-PARA-MESA"
                fila["razon"] = (f"veredicto sellado "
                                 f"{fila['veredicto_sellado_ref']} = "
                                 f"{fila['veredicto_sellado']}")
            else:
                fila["veredicto"] = "NO-ADOPTABLE-POR-VEREDICTO-SELLADO"
                fila["razon"] = (f"veredicto sellado "
                                 f"{fila['veredicto_sellado_ref']} = "
                                 f"{fila['veredicto_sellado']}")
        elif cita_c0:
            # El consumidor cita y ningun canal de spec lo reproduce: el
            # relevo EXISTE (esta en el archivo del consumidor) y la spec no
            # lo declara. Se rotula, no se calla: es el hueco que impide
            # auditar esa adopcion desde la oferta.
            fila["veredicto"] = "YA-ADOPTADO"
            fila["result_gen2_candidato"] = cita_c0
            fila["canal"] = "C0-CONSUMIDOR"
            fila["control_c0"] = "NO-DERIVABLE-DESDE-LA-SPEC"
            fila["razon"] = (
                f"el consumidor cita {cita_c0}; ninguna spec sellada declara "
                f"ese relevo por C1/C2 -- adopcion no auditable desde la oferta")
        else:
            fila["veredicto"] = "SIN-CANDIDATO"
            if blandas:
                fila["calc_candidato"] = ";".join(sorted({b[1] for b in blandas}))
                fila["razon"] = ";".join(sorted({b[3] for b in blandas}))
            elif fila["veredicto_sellado"].startswith("LISTADO-PARA-MESA"):
                fila["veredicto"] = "LISTADO-PARA-MESA"
                fila["calc_candidato"] = ";".join(sorted(cobertura)) or \
                    fila["veredicto_sellado_ref"].split("/")[0]
                fila["razon"] = (
                    f"veredicto sellado {fila['veredicto_sellado_ref']} = "
                    f"{fila['veredicto_sellado']}; la spec no fija que RESULT "
                    f"releva este slot -- falta el pin, no la corrida")
            elif cobertura:
                sell = sorted(c for c in cobertura
                              if (oferta.get(c) or {}).get("estado", "")
                              .startswith(SELLADA))
                fila["calc_candidato"] = ";".join(sorted(cobertura))
                fila["razon"] = (
                    f"CORR-CON-CALC-SIN-RESULT-FIJADO:{';'.join(sell)}"
                    if sell else
                    f"CALC-DECLARADA-NO-SELLADA:{';'.join(sorted(cobertura))}")
            else:
                fila["razon"] = "CORR-SIN-CALC-DECLARADA"

        # F-2 no reescribe el veredicto sellado: lo conserva en sus columnas
        # historicas y publica aparte la resolucion efectiva, condicionada por
        # F-1 al valor que `milpa/` materializa AHORA.
        punto_f2 = valor_result.get((F2_CORRIDA, F2_RESULT))
        f2 = _resuelve_f2_encuci(
            res, slot["consumidor"], ramas, oferta, evidencia_f2, punto_f2,
            resultados_f2, uso, specs.get(F2_CALC) or {}, firma_f2)
        if f2:
            fila["resolucion_vigente"] = f2["resolucion"]
            detalle = (
                f"veredicto sellado historico {fila['veredicto_sellado_ref']}"
                f" = {fila['veredicto_sellado']}; resolucion vigente F-2 "
                f"({F2_AUTORIDAD.relative_to(RAIZ)} F-1/F-2): "
                f"{f2['resolucion']} ({f2['causa']})")
            if "modo" in f2:
                detalle += (
                    f"; RESULT={f2['valor_result']!r}; valor vigente del "
                    f"consumidor={f2['valor_consumidor']!r}; "
                    f"delta={f2['delta']!r}; {f2['modo']}")
            fila["razon"] = detalle
            if f2["aplica"]:
                fila["veredicto"] = "YA-ADOPTADO"
            elif f2["resolucion"] == "CITA-PENDIENTE-DE-RETIRO-POR-F2":
                fila["veredicto"] = f2["resolucion"]
            else:
                fila["veredicto"] = "NO-ACREDITADO-POR-F2"
        filas.append(fila)
        contadores[fila["veredicto"]] = contadores.get(fila["veredicto"], 0) + 1

    contadores["slots"] = len(filas)
    for clave in ("COINCIDE", "NO-DERIVABLE-DESDE-LA-SPEC"):
        contadores[f"control_c0[{clave}]"] = sum(
            1 for f in filas if f["control_c0"] == clave)
    contadores["control_c0[DISCREPA]"] = sum(
        1 for f in filas if f["control_c0"].startswith("DISCREPA"))
    # P1, primera mitad: corridas naturales cuya CALC YA esta sellada --
    # todo veredicto que no sea SIN-CANDIDATO se apoya en una corrida de
    # oferta sellada, mas los slots que solo llegan por cobertura C3.
    con_calc = {f["corrida_natural"] for f in filas
                if f["veredicto"] != "SIN-CANDIDATO"
                or f["razon"].startswith("CORR-CON-CALC-SIN-RESULT-FIJADO")}
    contadores["corridas_con_calc_sellada"] = len(con_calc)
    contadores["slots_con_corrida_con_calc_sellada"] = sum(
        1 for f in filas if f["corrida_natural"] in con_calc)
    return filas, contadores


# ═══════════════════════════════════════════════════════════════════════════
# P2 · el contrato GEN2-DELTA-1 de los pares cableados en P1.
#
# El encargo dice «por script, nunca a mano», y eso NO significa que la
# maquina invente las ocho dimensiones de comparabilidad: significa que la
# comparacion la ejecuta `corrida0 delta` sobre un contrato COMPLETO, y que
# ese contrato se GENERA de forma reproducible desde el registro en vez de
# teclearse par por par.
#
# Lo que la maquina pone: las identidades (CALC, corrida, RESULT, los tres
# sha256, el selector de la fuente legacy), los valores y las citas verbatim.
# Lo que este ACTO declara y firma: el estado de cada dimension, agrupado en
# CUATRO familias -- y cada familia queda ANCLADA a un texto que tiene que
# seguir existiendo, literal, en el `spec.yaml` sellado del CALC. Si el ancla
# desaparece, el generador PARA en vez de emitir un juicio que ya no sostiene
# el arbol. Esa es la diferencia entre una declaracion auditable y una
# suposicion: la de aqui se puede falsar con `grep`.
#
# Las familias se ASIGNAN por derivacion (veredicto sellado + canal), no a
# dedo slot por slot.
# ═══════════════════════════════════════════════════════════════════════════

COINCIDE = "COINCIDE"
DERIVA = "DERIVA-DOCUMENTADA"
INSUFICIENTE = "INFORMACION-INSUFICIENTE"

DIMENSIONES = ("unidad", "escala", "direccion", "poblacion", "evento",
               "codigos", "periodo", "transformacion")

FAMILIAS = {
    "F-MAPA-DIRECTO": {
        "ancla": "en esta spec se cuentan DIRECTAMENTE",
        "descripcion": (
            "el mapa `adopcion_p3.consumidores` fija el RESULT y la nota del "
            "mismo bloque declara que estas celdas se cuentan DIRECTAMENTE y "
            "SI son cantidad medida; no hay rama de adopcion sellada que "
            "contradiga eso"),
        "estados": {d: COINCIDE for d in DIMENSIONES},
    },
    "F-GRANO": {
        "ancla": ("La unica celda con la MISMA codificacion que el valor ya "
                  "materializado es la que se cita"),
        "descripcion": (
            "el mapa `adopcion_p3.consumidores` fija el RESULT y su nota "
            "declara que la celda citada es la de la MISMA codificacion que "
            "el valor materializado; el veredicto sellado no discute "
            "comparabilidad sino GRANO, que es justo lo que `delta` mide"),
        "estados": {d: COINCIDE for d in DIMENSIONES},
    },
    "F-COMPLEMENTO": {
        "ancla": "no 1 menos otra cosa",
        "descripcion": (
            "el veredicto sellado dice COMPLEMENTO-CON-DENOMINADOR-RECORTADO: "
            "el lado GEN1 es `1 - p` y el lado GEN2 cuenta la categoria "
            "DIRECTAMENTE sobre el mismo denominador declarado. Misma celda, "
            "misma poblacion, OTRA transformacion -- y la deriva esta "
            "documentada por el propio criterio pre-declarado de la spec"),
        "estados": {**{d: COINCIDE for d in DIMENSIONES},
                    "transformacion": DERIVA},
    },
    "F-ADOPTABLE-SELLADO": {
        "ancla": None,          # se ancla en el VALOR del veredicto sellado
        "descripcion": (
            "la rama de adopcion que la corrida sello para este slot es "
            "ADOPTABLE, y es una de las que la spec habia PRE-DECLARADO "
            "antes de medir. Mas fuerte que cualquier enlace por texto: la "
            "propia corrida certifico que el RESULT releva a este consumidor"),
        "estados": {d: COINCIDE for d in DIMENSIONES},
    },
    "F-CANDIDATO-SIN-VEREDICTO": {
        "ancla": None,          # se ancla en la `unidad` del propio RESULT
        "descripcion": (
            "la spec enlaza el RESULT al slot como CANDIDATO y nunca lo "
            "declaro ADOPTABLE ni le pre-declaro rama de adopcion. El "
            "registro no acredita que el denominador del candidato sea el de "
            "la celda legacy, y este acto NO lo supone: la poblacion queda "
            "INFORMACION-INSUFICIENTE y `delta` rechaza el delta sustantivo, "
            "que es exactamente lo que debe pasar"),
        "estados": {**{d: COINCIDE for d in DIMENSIONES},
                    "poblacion": INSUFICIENTE},
    },
}

# Anotacion por RESULT, no por familia: una advertencia que la propia spec
# escribio sobre ESE RESULT y que ninguna familia puede borrar.
ANOTACIONES = {
    "ADVERTENCIA DE ROTULO": ("evento", DERIVA),
}

# Criterio sustantivo de materialidad (P3). No se inventa un umbral: se cita
# el que el arbol YA declara como el grano con que un consumidor materializa
# una cifra y con que `T35` la compara contra el RESULT sellado.
CRITERIO_MATERIALIDAD = {
    "fuente": "data/corrida0/CALC-B-0001/spec.yaml",
    "cita": ("parametros.adopcion_p3.umbral_grano_milpa = 1e-06 -- «la "
             "tolerancia con que T35 (c) compara el valor materializado por "
             "el consumidor contra el RESULT»; es el grano del CONSUMIDOR, "
             "no de una spec, y por eso vale para los cuatro CALC de estos "
             "pares"),
    "metrica": "magnitud_absoluta",
    "umbral": 1e-06,
}

# Los DOS archivos de consumidor que `corrida0 demanda` recorre. El lado A
# de cada par apunta al archivo del CONSUMIDOR, no a la vista derivada: es
# «la fuente legacy anterior a adopcion» que NC-0048 exige, y ademas la vista
# derivada no es direccionable por el contrato (su cabecera `# DERIVADO` haria
# que un `csv.DictReader` tomara el comentario por encabezado).
ARCHIVOS_CONSUMIDOR = ("milpa/tramite.yaml", "milpa/procedencia.yaml")


def _ruta_del_consumidor(crudo, consumidor: str, rel: str):
    """Camino YAML exacto hasta el campo que MATERIALIZA la cifra de un
    consumidor, o `None`.

    Reproduce, paso por paso, el mismo recorrido con que
    `corrida0._ids_corrida0_declarados` construye el id del consumidor
    (`<archivo>:<regla>:<conducta>`, con el contexto acumulandose solo bajo
    `entonces`). Se reimplementa devolviendo el CAMINO en vez del valor
    porque el contrato GEN2-DELTA-1 no acepta un valor suelto: exige un
    selector con el que cualquiera pueda volver a sacarlo del archivo."""
    hallado = []

    def camina(nodo, contexto, camino):
        if hallado:
            return
        if isinstance(nodo, dict):
            nombre = (nodo.get("conducta") or nodo.get("id")
                      or nodo.get("clave") or "")
            partes = [c for c in contexto if c] + ([nombre] if nombre else [])
            if f"{rel}:{':'.join(partes)}" == consumidor:
                for campo in corrida0.CAMPOS_VALOR_MATERIALIZADO:
                    if campo in nodo:
                        hallado.append(camino + [campo])
                        return
            propio = nodo.get("id")
            for clave, valor in nodo.items():
                camina(valor, contexto + [str(propio or "")]
                       if clave == "entonces" else contexto, camino + [clave])
        elif isinstance(nodo, list):
            for i, elemento in enumerate(nodo):
                camina(elemento, contexto, camino + [i])

    camina(crudo, [], [])
    return hallado[0] if hallado else None


def _lado_legacy(fila: dict) -> tuple[dict | None, str]:
    """Lado A del par: el campo del archivo del consumidor, con su camino
    resuelto y VERIFICADO contra `valor_legacy` de la vista derivada.

    Si el camino no resuelve, o resuelve a otra cifra, el par NO se emite: un
    contrato que apunta a un campo equivocado es peor que un par de menos."""
    for rel in ARCHIVOS_CONSUMIDOR:
        ruta = RAIZ / rel
        if not ruta.is_file() or not fila["consumidor"].startswith(rel + ":"):
            continue
        crudo = corrida0._yaml_safe_load(ruta.read_text(encoding="utf-8"))
        camino = _ruta_del_consumidor(crudo, fila["consumidor"], rel)
        if camino is None:
            return None, (f"{fila['resultado_id']}: no se resolvio el camino "
                          f"YAML de {fila['consumidor']} en {rel}")
        nodo = crudo
        for paso in camino:
            nodo = nodo[paso]
        try:
            iguales = abs(float(nodo) - float(fila["valor_legacy"])) <= 0.0
        except (TypeError, ValueError):
            iguales = str(nodo) == fila["valor_legacy"]
        if not iguales:
            return None, (f"{fila['resultado_id']}: {rel}{camino} vale {nodo!r} "
                          f"y la vista derivada declara "
                          f"{fila['valor_legacy']!r} -- no se emite el par")
        return {
            "clase": "fuente",
            "fuente": rel,
            "sha256": corrida0._sha256_archivo(ruta),
            "version": (
                "archivo del consumidor en la base de este acto; el valor es "
                "la cifra GEN1 que el motor lee HOY, antes de toda adopcion"),
            "tipo": "proporcion",
            "unidad": "proporcion en escala [0,1]",
            "selector": {"formato": "yaml", "ruta": camino},
        }, ""
    return None, (f"{fila['resultado_id']}: {fila['consumidor']} no pertenece "
                  f"a ningun archivo de consumidor conocido")


def _texto_normalizado(nodo, salida: list[str] | None = None) -> str:
    """Todas las cadenas de una spec, con los saltos de linea del YAML
    colapsados. Las anclas se buscan AQUI y no en los bytes del archivo: un
    texto declarado es el mismo lo envuelva `yaml` a 80 columnas o a 100, y
    anclar en los bytes convertiria un re-formateo cosmetico en un PARO."""
    salida = [] if salida is None else salida
    if isinstance(nodo, str):
        salida.append(" ".join(nodo.split()))
    elif isinstance(nodo, dict):
        for clave, valor in nodo.items():
            salida.append(" ".join(str(clave).split()))
            _texto_normalizado(valor, salida)
    elif isinstance(nodo, (list, tuple)):
        for valor in nodo:
            _texto_normalizado(valor, salida)
    return "\n".join(salida)


def _familia(fila: dict) -> str:
    """Familia de comparabilidad de un par, DERIVADA del veredicto sellado y
    del canal que lo enlazo. Sin veredicto y sin mapa, no hay familia fuerte:
    cae en la que rechaza el delta."""
    vered = fila["veredicto_sellado"]
    if vered in ADOPTABLES:
        return "F-ADOPTABLE-SELLADO"
    if vered.startswith("COMPLEMENTO-CON-DENOMINADOR-RECORTADO"):
        return "F-COMPLEMENTO"
    if vered.startswith("NO-ADOPTABLE-POR-GRANO"):
        return "F-GRANO"
    if vered == "SIN-VEREDICTO-SELLADO" and "C1-MAPA" in fila["canal"]:
        return "F-MAPA-DIRECTO"
    return "F-CANDIDATO-SIN-VEREDICTO"


def contrato(filas: list[dict]) -> dict:
    """Contrato GEN2-DELTA-1 con un par por slot CABLEADO -- los que P1 dejo
    con RESULT fijado, ADOPTADOS O NO.

    Los ya adoptados NO se excluyen, y esa es una decision con motivo: para
    ellos el par es la correspondencia GEN1<->GEN2 declarada por identidad
    que `NC-0048` lleva abierta pidiendo, y ademas el control permanente de
    que la cita sigue apuntando a la cifra que el consumidor materializa. Un
    slot sin pin no entra: un par sin RESULT no es un par, y rellenarlo seria
    la inferencia que el contrato prohibe."""
    pares, saltados = [], []
    for fila in filas:
        rid = fila["result_gen2_candidato"]
        calc = fila["calc_candidato"]
        if not rid or ";" in rid or not calc or ";" in calc:
            continue
        directorio = C0 / calc
        spec = corrida0._yaml_safe_load(
            (directorio / "spec.yaml").read_text(encoding="utf-8")) or {}
        spec_txt = _texto_normalizado(spec)
        decl = [r for r in (spec.get("resultados") or [])
                if isinstance(r, dict) and r.get("id") == rid]
        if len(decl) != 1:
            saltados.append(f"{fila['resultado_id']}: {calc}/{rid} declarado "
                            f"{len(decl)} veces en la spec")
            continue
        unidad = str(decl[0].get("unidad", ""))

        lado_a, fallo = _lado_legacy(fila)
        if lado_a is None:
            saltados.append(fallo)
            continue

        nombre = _familia(fila)
        fam = FAMILIAS[nombre]
        if fam["ancla"] is not None:
            ancla = fam["ancla"]
        elif nombre == "F-ADOPTABLE-SELLADO":
            # El ancla es la rama sellada: tiene que constar, literal, entre
            # las que la spec enumero ANTES de medir. Una rama que la spec
            # nunca pre-declaro no acredita nada.
            ancla = fila["veredicto_sellado"]
        else:
            ancla = unidad
        ancla = " ".join(ancla.split())
        if ancla not in spec_txt:
            saltados.append(
                f"{fila['resultado_id']}: ancla de {nombre} ausente de "
                f"{calc}/spec.yaml -- no se emite juicio sin su texto")
            continue
        estados = dict(fam["estados"])
        anotado = []
        for marca, (dimension, estado) in ANOTACIONES.items():
            if marca in unidad:
                estados[dimension] = estado
                anotado.append(marca)

        sha = {campo: corrida0._sha256_archivo(directorio / archivo)
               for campo, archivo in (("spec_sha256", "spec.yaml"),
                                      ("resultados_sha256", "resultados.json"),
                                      ("sello_sha256", "sello.json"))}
        evidencia_spec = {
            "fuente": f"data/corrida0/{calc}/spec.yaml",
            "sha256": sha["spec_sha256"],
            "cita": (f"resultados[id={rid}].unidad = «{unidad}» · familia "
                     f"{nombre} anclada en «{ancla}»"),
        }
        razon_base = (
            f"{nombre}: {fam['descripcion']}. Declaracion verbatim del RESULT "
            f"en la spec sellada: «{unidad}». Veredicto sellado del slot: "
            f"{fila['veredicto_sellado']} ({fila['veredicto_sellado_ref']}).")
        if anotado:
            razon_base += (f" Anotacion propia del RESULT respetada sobre la "
                           f"familia: {', '.join(anotado)}.")

        pares.append({
            "id": f"RELEVO-{fila['resultado_id']}-VS-{rid}",
            "consumidor": fila["consumidor"],
            "uso": {
                "descripcion": (
                    f"relevo GEN1->GEN2 del slot {fila['resultado_id']} "
                    f"({fila['tipo_uso']}, reglas_impacto="
                    f"{fila['reglas_impacto']}): la cifra que el consumidor "
                    f"materializa hoy frente al RESULT sellado que la spec de "
                    f"{calc} declara que la releva. Adopcion NO ejecutada "
                    f"aqui: este par mide la distancia, no la autoriza."),
                "evidencias": [evidencia_spec],
            },
            "a": lado_a,
            "b": {
                "clase": "resultado",
                "calc_id": calc,
                "corrida_id": fila["corrida_oferta"],
                "resultado_id": rid,
                **sha,
            },
            "comparabilidad": {
                "dimensiones": {d: {"estado": estados[d], "razon": razon_base}
                                for d in DIMENSIONES},
                "evidencias": [evidencia_spec],
            },
            "diferencia": {
                "escala": "proporcion",
                "unidad": "proporcion en escala [0,1]",
                "relativo": {
                    "permitido": False,
                    "razon": ("el cero de una p de conducta no es una base "
                              "sustantiva para cambio relativo; el grano del "
                              "consumidor se mide en magnitud absoluta"),
                },
            },
            "representacion": {"aplica": True, "publicado": "a", "preciso": "b"},
            "materialidad": {
                "criterio": {
                    "metrica": CRITERIO_MATERIALIDAD["metrica"],
                    "umbral": CRITERIO_MATERIALIDAD["umbral"],
                    "evidencias": [{
                        "fuente": CRITERIO_MATERIALIDAD["fuente"],
                        "sha256": corrida0._sha256_archivo(
                            RAIZ / CRITERIO_MATERIALIDAD["fuente"]),
                        "cita": CRITERIO_MATERIALIDAD["cita"],
                    }],
                },
                "razon": (
                    "materialidad POR CONSUMIDOR (E.4): el umbral es el grano "
                    "con que el consumidor materializa la cifra, no una "
                    "tolerancia de spec. Por encima de el, el motor leeria un "
                    "numero distinto del que lee hoy."),
            },
        })
    return {
        "version": "GEN2-DELTA-1",
        "descripcion": (
            "ACTO GEN2-RELEVO-USOS-1 · P2. Un par por slot de demanda que P1 "
            "dejo CABLEADO a un RESULT sellado y que todavia no esta "
            "adoptado. Generado por `tools/relevo_usos.py --contrato`: ni los "
            "pares ni los hashes ni las citas se teclean. Las ocho "
            "dimensiones las declara este acto por familia, y cada familia "
            "esta anclada a texto verbatim de la spec sellada."),
        "pares": pares,
    }, saltados


# ═══════════════════════════════════════════════════════════════════════════
# P3 · materialidad POR CONSUMIDOR (E.4: `reglas_impacto`, no por spec).
#
# No se vuelve a calcular ningun delta aqui: se LEEN los que `corrida0 delta`
# produjo sobre el contrato de P2. Este paso solo traduce esos numeros al
# vocabulario con que mesa decide -- «cambia signo, tier, clasificacion o
# coeficiente central» -- y cada prueba dice de donde sale.
#
# Las cuatro pruebas del encargo, derivadas y no supuestas:
#
#   signo         Los dos lados son proporciones en [0,1]. El signo no puede
#                 cambiar, y se COMPRUEBA en vez de darse por hecho.
#   grano         DOS umbrales, porque el arbol declara dos y NO coinciden:
#                 (a) el grano con que el consumidor ESCRIBE la cifra, que es
#                 el que usa el comparador canonico de adopcion (`p: 0.116`
#                 son 3 decimales); (b) `umbral_grano_milpa = 1e-06`, fijo.
#                 Se reportan los dos por separado, sin promediarlos ni
#                 elegir uno: que discrepen es un HALLAZGO, no un detalle.
#   clasificacion Una adopcion es una CITA: el `p` no se mueve. La `clase`
#                 del consumidor solo tendria que cambiar si la cifra
#                 cambiara, asi que esta prueba se deriva del grano y no de
#                 una lectura de etiquetas.
#   coeficiente   Si el consumidor no es una `p` de conducta sino un
#   central       coeficiente del generador, entra a mesa aunque el delta sea
#                 cero: mueve el motor por otra via.
#
# El tier NO se deriva: subir o bajar un tier es firma de mesa. Se reporta el
# vigente y se declara `NO-DERIVABLE-SIN-FIRMA`.
# ═══════════════════════════════════════════════════════════════════════════

UMBRAL_GRANO_MILPA = CRITERIO_MATERIALIDAD["umbral"]
TIPOS_COEFICIENTE_CENTRAL = ("coeficiente", "theta", "corte_pi", "momento")


def _tiers() -> dict[str, str]:
    """`regla -> tier` leido del archivo del consumidor. Solo LECTURA: `milpa/`
    no se toca en este acto (P4 esta con la compuerta cerrada)."""
    out: dict[str, str] = {}
    for rel in ARCHIVOS_CONSUMIDOR:
        ruta = RAIZ / rel
        if not ruta.is_file():
            continue
        crudo = corrida0._yaml_safe_load(ruta.read_text(encoding="utf-8"))

        def camina(nodo):
            if isinstance(nodo, dict):
                if nodo.get("id") and nodo.get("tier"):
                    out.setdefault(str(nodo["id"]), str(nodo["tier"]))
                for valor in nodo.values():
                    camina(valor)
            elif isinstance(nodo, list):
                for valor in nodo:
                    camina(valor)

        camina(crudo)
    return out


def aplica_p3(filas: list[dict], delta_json: Path) -> dict:
    informe = json.loads(delta_json.read_text(encoding="utf-8"))
    por_slot = {}
    for par in informe.get("pares") or []:
        marca = str(par.get("id", ""))
        for res in _res_ids(marca.split("-VS-")[0]):
            por_slot[res] = par
    tiers = _tiers()
    contadores = {"MATERIAL": 0, "NO-MATERIAL": 0, "NO-DETERMINABLE": 0}

    for fila in filas:
        par = por_slot.get(fila["resultado_id"])
        if par is None:
            continue
        dif, rep = par["diferencia"], par["representacion"]
        delta = dif.get("delta")
        fila["delta_gen2_menos_legacy"] = (
            repr(delta) if delta is not None else "NO-CALCULADO")
        fila["representacion_al_grano"] = rep["estado"]
        fila["grano_consumidor"] = rep.get("modo") or "NO-APLICA"
        fila["tier_consumidor"] = (
            f"{tiers.get(fila['reglas_impacto'], NO_DECLARADO)}"
            f" · NO-DERIVABLE-SIN-FIRMA")
        coef = any(t in fila["tipo_uso"] for t in TIPOS_COEFICIENTE_CENTRAL)
        fila["es_coeficiente_central"] = "SI" if coef else "NO"

        if delta is None:
            fila.update(
                cambia_signo="NO-DETERMINABLE",
                cruza_grano_del_consumidor="NO-DETERMINABLE",
                cruza_umbral_grano_milpa="NO-DETERMINABLE",
                cambia_clasificacion="NO-DETERMINABLE",
                materialidad_consumidor="NO-DETERMINABLE",
                razon_materialidad=(
                    f"`corrida0 delta` no calculo delta: "
                    f"{par['comparabilidad']['estado']} -- "
                    f"{par['comparabilidad']['causa']}"))
            contadores["NO-DETERMINABLE"] += 1
            continue

        a = par["referencias"]["a"].get("valor")
        b = par["referencias"]["b"].get("valor")
        signo = "SI" if (a is not None and b is not None
                         and (a > 0) != (b > 0)) else "NO"
        grano = "SI" if rep["estado"] == "DISTINTO-AL-GRANO" else "NO"
        umbral = "SI" if abs(float(delta)) >= UMBRAL_GRANO_MILPA else "NO"
        clase = "SI" if (grano == "SI" or umbral == "SI") else "NO"
        material = "SI" in (signo, grano, umbral, fila["es_coeficiente_central"])
        fila.update(
            cambia_signo=signo, cruza_grano_del_consumidor=grano,
            cruza_umbral_grano_milpa=umbral, cambia_clasificacion=clase,
            materialidad_consumidor="MATERIAL" if material else "NO-MATERIAL",
            razon_materialidad=(
                f"|delta|={abs(float(delta)):.3e} · umbral_grano_milpa="
                f"{UMBRAL_GRANO_MILPA:g} -> {umbral} · comparador de adopcion "
                f"({rep.get('modo')}) -> {rep['estado']} · signo -> {signo} · "
                f"coeficiente central -> {fila['es_coeficiente_central']}"))
        contadores["MATERIAL" if material else "NO-MATERIAL"] += 1
    return contadores


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="relevo-usos", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--escribe", action="store_true",
                   help="escribe data/corrida0/relevo-usos-v1_0.tsv; sin la "
                        "bandera solo deriva e imprime los contadores")
    p.add_argument("--json", action="store_true", help="filas en JSON a stdout")
    p.add_argument("--p3", metavar="DELTA.json", default=None,
                   help="pliega el informe de `corrida0 delta` y clasifica "
                        "materialidad por consumidor antes de escribir")
    p.add_argument("--contrato", metavar="RUTA.yaml", default=None,
                   help="genera el contrato GEN2-DELTA-1 (P2) de los pares "
                        "cableados y lo escribe en RUTA")
    args = p.parse_args(argv)

    filas, contadores = deriva()
    if args.p3:
        for clave, valor in aplica_p3(filas, Path(args.p3)).items():
            contadores[f"materialidad[{clave}]"] = valor
    if args.json:
        print(json.dumps(filas, ensure_ascii=False, indent=1))
    else:
        for clave in sorted(contadores):
            print(f"{clave}={contadores[clave]}")
    if args.escribe:
        corrida0._escribe(SALIDA_TSV, COLUMNAS, filas)
        print(f"# escrito {SALIDA_TSV.relative_to(RAIZ)}", file=sys.stderr)
    if args.contrato:
        doc, saltados = contrato(filas)
        ruta = Path(args.contrato)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(
            yaml.safe_dump(doc, allow_unicode=True, sort_keys=False,
                           default_flow_style=False, width=100),
            encoding="utf-8")
        print(f"pares_en_el_contrato={len(doc['pares'])}")
        for linea in saltados:
            print(f"  SALTADO · {linea}", file=sys.stderr)
        print(f"# escrito {ruta}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
