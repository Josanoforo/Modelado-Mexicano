#!/usr/bin/env python3
"""Integración determinista Multi2→Multi2-fix con aliases y evidencia frozen."""
from __future__ import annotations

import argparse, csv, hashlib, json, re, shutil, subprocess
from collections import Counter, defaultdict
from pathlib import Path

from curador import FIELDS, read_tsv
from multi_supervisor import EVIDENCE_FIELDS, WORKER_FIELDS, write_tsv

LOCATOR_FIELDS = EVIDENCE_FIELDS + ["worker_id", "localizador_tipo", "referencia_estado", "referencia_detalle", "hash_archivo_worker"]
DECISION_FIELDS = ["decision_id", "necesidad_id", "fuente_canonica_normalizada", "objeto_evidencia_id", "pregunta_decision", "alternativas", "efecto_sobre_modelo", "evidencia_ref", "estado_decision", "procedencia"]
USO_FIELDS = ["necesidad_id", "fuente_canonica_normalizada", "objeto_evidencia_id", "clasificacion_relacion", "estado_uso_modelo", "evidencia_disponible", "reserva_material", "verificacion_requerida", "uso_permitido_actual", "evidencia_ref"]

def key(r, source_field="fuente_id_canonico", object_field="objeto_evidencia_id"):
    return r["necesidad_id"], r[source_field], r[object_field]

def split_main_refs(value):
    return [x[5:] for x in (value or "").split(";") if x.startswith("MAIN:")]

def materials(repo: Path, reference: str):
    result=[]
    for raw in split_main_refs(reference):
        m=re.fullmatch(r"(.+?)(?::L(\d+))?",raw); path=repo/m.group(1) if m else None
        if not path or not path.is_file(): continue
        lines=path.read_text(encoding="utf-8",errors="replace").splitlines(); n=int(m.group(2)) if m and m.group(2) else None
        if n and 1<=n<=len(lines): result.append((path,lines,n,lines[n-1]))
        elif not n: result.append((path,lines,None,"\n".join(lines)))
    return result

def classify_locator(row, repo: Path):
    loc=(row.get("evidencia_localizador") or "").strip(); relation="|".join(key(row,"fuente_canonica"))
    mats=materials(repo,row.get("evidencia_ref",""))
    if re.fullmatch(r"L\d+",loc):
        n=int(loc[1:]); ok=any(n<=len(lines) for _,lines,_,_ in mats); return "LINEA",ok,f"línea {n} {'válida' if ok else 'inválida'}"
    m=re.fullmatch(r"L(\d+)-L?(\d+)",loc)
    if m:
        a,b=map(int,m.groups()); ok=a<=b and any(b<=len(lines) for _,lines,_,_ in mats); return "RANGO_LINEAS",ok,f"rango {a}-{b} {'válido' if ok else 'inválido'}"
    if loc==relation:
        return "CLAVE_RELACION",True,"clave coincide exactamente; no es prueba sustantiva"
    if loc.startswith("NO_APLICA"):
        ok=bool(row.get("incertidumbre","").strip() or row.get("traza_revision","").strip()); return "NO_APLICA_JUSTIFICADO",ok,"justificación presente" if ok else "sin justificación"
    state_tokens={"APERTURA_INDETERMINADA","INDEXADO-NO-DESCARGADO","MAPEADO-NO-SATISFACE","ABIERTO-SIN-MAPEO","CANDIDATA_ESTRUCTURAL_SIN_APERTURA"}
    found=any(loc in text for *_,text in mats)
    if loc in state_tokens:
        return "ESTADO_INDICE",found,"estado encontrado" if found else "estado no encontrado"
    return "TOKEN",found,"token encontrado" if found else "token no encontrado"

def validate_worker_evidence(input_dir: Path, repo: Path, baseline_keys: set, assignments: dict):
    errors=[]; consolidated=[]; relation_keys=set(); evidence_keys=set(); worker_hashes={}
    for i in range(1,5):
        wid=f"worker-{i}"; rp=input_dir/f"{wid}-relaciones.tsv"; ep=input_dir/f"{wid}-evidencia.tsv"; sp=input_dir/f"{wid}-resumen.json"
        if not rp.is_file() or not ep.is_file(): errors.append(f"faltan outputs {wid}"); continue
        worker_hashes[rp.name]=hashlib.sha256(rp.read_bytes()).hexdigest(); worker_hashes[ep.name]=hashlib.sha256(ep.read_bytes()).hexdigest()
        if sp.is_file(): worker_hashes[sp.name]=hashlib.sha256(sp.read_bytes()).hexdigest()
        rr,ee=read_tsv(rp),read_tsv(ep); rkeys={key(r,"fuente_canonica") for r in rr}; ekeys={key(r,"fuente_canonica") for r in ee}
        if len(rkeys)!=len(rr): errors.append(f"relaciones duplicadas {wid}")
        if len(ekeys)!=len(ee): errors.append(f"evidencias duplicadas {wid}")
        if rkeys!=ekeys: errors.append(f"evidencia sin correspondencia {wid}")
        for k in rkeys|ekeys:
            if k not in baseline_keys: errors.append(f"clave ajena al baseline {wid}: {k}")
            if assignments.get(k[1])!=wid: errors.append(f"evidencia de worker no asignado {wid}: {k}")
        rel_by={key(r,"fuente_canonica"):r for r in rr}
        for e in ee:
            k=key(e,"fuente_canonica"); typ,ok,detail=classify_locator(e,repo); relation=rel_by.get(k,{})
            if any(not e.get(f,"").strip() for f in EVIDENCE_FIELDS): errors.append(f"campo evidencia vacío {wid}: {k}")
            if relation.get("estado_propuesto") in {"CONFIRMADA","NEGATIVA"}:
                substantive=typ not in {"CLAVE_RELACION","NO_APLICA_JUSTIFICADO","ESTADO_INDICE"}
                if not ok or not substantive or not relation.get("evidencia_explicita","").strip() or not relation.get("razon","").strip(): errors.append(f"adjudicación sin evidencia verificable {wid}: {k}")
            material=relation.get("estado_propuesto") in {"CONFIRMADA","NEGATIVA"}
            if ok and typ in {"LINEA","RANGO_LINEAS","TOKEN"}: ref_state="CONTENIDO_VERIFICADO"
            elif ok and typ in {"CLAVE_RELACION","ESTADO_INDICE","NO_APLICA_JUSTIFICADO"}: ref_state="ANCLA_ESTRUCTURAL_VERIFICADA"
            elif not ok and not material and materials(repo,e.get("evidencia_ref","")): ref_state="NO_VERIFICADO_NO_MATERIAL"
            else: ref_state="INVALIDO_MATERIAL"
            if ref_state=="INVALIDO_MATERIAL": errors.append(f"referencia inválida material {wid}: {k}: {detail}")
            consolidated.append({**e,"worker_id":wid,"localizador_tipo":typ,"referencia_estado":ref_state,"referencia_detalle":detail,"hash_archivo_worker":worker_hashes[ep.name]})
        relation_keys|=rkeys; evidence_keys|=ekeys
    return errors,consolidated,relation_keys,evidence_keys,worker_hashes

def normalize_records(rows, rules):
    by_old={r["old_relation_key"]:r for r in rules}; groups=defaultdict(list); provenance=[]; expected_losses=set(); errors=[]
    for row in rows:
        old="|".join(key(row)); rule=by_old.get(old); new=dict(row)
        if rule:
            new["fuente_id_canonico"]=rule["fuente_canonica_normalizada"]; new["fuente_nombre"]=rule["fuente_canonica_normalizada"]
            new["objeto_evidencia_id"]=rule["objeto_evidencia_canonico"]
        nk="|".join(key(new)); action=rule["accion"] if rule else "SIN_CAMBIO"
        provenance.append({"old_relation_key":old,"normalized_relation_key":nk,"accion":action,"evidencia_ref":(rule or {}).get("evidencia_ref",row.get("evidencia_ref",""))})
        groups[nk].append((old,new,rule))
    result={}
    for nk,members in sorted(groups.items()):
        if len(members)==1: result[nk]=members[0][1]; continue
        fusion_rules=[rule for _,_,rule in members if rule and rule["accion"]=="FUSIONAR_RELACION"]
        canonical_key=fusion_rules[0]["canonical_relation_key"] if fusion_rules else ""
        canonical=[new for old,new,_ in members if old==canonical_key]
        if not fusion_rules or len({r["canonical_relation_key"] for r in fusion_rules})!=1 or len(canonical)!=1:
            errors.append(f"colisión no autorizada o canónica ambigua: {nk}"); continue
        result[nk]=canonical[0]
        expected_losses.update(old for old,_,_ in members if old!=canonical_key)
    provenance.sort(key=lambda r:(r["normalized_relation_key"],r["old_relation_key"]))
    return [result[k] for k in sorted(result)],provenance,expected_losses,set(),errors

def derive_decisions(rows):
    decisions=[]
    for r in rows:
        note=r.get("nota","")
        if "reemplazar o complementar el proxy ENUT" in note:
            q="¿ENASIC P7_12_7 debe reemplazar o complementar el proxy previo de ENUT para el uso posterior en el modelo?"
            decisions.append({"decision_id":"DH-"+hashlib.sha256(("N13|ENASIC|P7_12_7").encode()).hexdigest()[:16],"necesidad_id":"N13","fuente_canonica_normalizada":"ENASIC","objeto_evidencia_id":r["objeto_evidencia_id"],"pregunta_decision":q,"alternativas":"REEMPLAZAR_PROXY_ENUT|COMPLEMENTAR_PROXY_ENUT|NO_USAR_EN_MODELO","efecto_sobre_modelo":"Cambia la operacionalización de familismo_obligacion.","evidencia_ref":"MAIN:data/abrir4-variables-2026-08-08.tsv:L20","estado_decision":"PENDIENTE","procedencia":"nota heredada Multi1/Multi2"})
        if r["necesidad_id"]=="N14" and r["fuente_id_canonico"]=="ENBIARE" and "NO VERIFICADO" in note:
            q="¿PB1_01/PB1_02 de ENBIARE son equivalentes al constructo vigente de radio_confianza para uso paramétrico?"
            decisions.append({"decision_id":"DH-"+hashlib.sha256(("N14|ENBIARE|PB1").encode()).hexdigest()[:16],"necesidad_id":"N14","fuente_canonica_normalizada":"ENBIARE","objeto_evidencia_id":r["objeto_evidencia_id"],"pregunta_decision":q,"alternativas":"EQUIVALENTE|PROXY_PARCIAL|NO_EQUIVALENTE","efecto_sobre_modelo":"Determina si la medición provisional puede convertirse en parámetro.","evidencia_ref":r["evidencia_ref"],"estado_decision":"PENDIENTE","procedencia":"reserva material heredada de apertura L28"})
    return {d["decision_id"]:d for d in decisions}.values()

def detect_narrowing(original_keys,new_keys,expected_losses):
    lost=set(original_keys)-set(new_keys); unexpected=lost-set(expected_losses); return bool(unexpected),lost,unexpected

def usage_rows(rows):
    out=[]
    for r in rows:
        state=r["clasificacion_relacion"]
        use={"CONFIRMADA":"MEDICION_DISPONIBLE_NO_PARAMETRO","NEGATIVA":"NO_USAR_PARA_RELACION","CANDIDATA":"PENDIENTE_EVIDENCIA","NO_ACCESIBLE":"BLOQUEADA_ACCESO"}.get(state,"REVISION_REQUERIDA")
        available=r.get("evidencia_textual_breve","") or "NO_DETERMINADO"; reserve=r.get("nota","") or "NO_DETERMINADO"; verify="Revisión de equivalencia y codificación antes de parametrizar."
        allowed="Exploración/medición descriptiva según reserva; no parámetro definitivo."
        if r["necesidad_id"]=="N14" and r["fuente_id_canonico"]=="ENBIARE" and state=="CONFIRMADA":
            use="MEDICION_PROVISIONAL"; available="PB1_01/PB1_02 y PF1_1..6; coobservación en la misma muestra."; reserve="Equivalencia PB1↔radio_confianza vigente no verificada."; verify="Resolver equivalencia conceptual y codificación."; allowed="Medición provisional; prohibido parámetro definitivo."
        out.append({"necesidad_id":r["necesidad_id"],"fuente_canonica_normalizada":r["fuente_id_canonico"],"objeto_evidencia_id":r["objeto_evidencia_id"],"clasificacion_relacion":state,"estado_uso_modelo":use,"evidencia_disponible":available,"reserva_material":reserve,"verificacion_requerida":verify,"uso_permitido_actual":allowed,"evidencia_ref":r["evidencia_ref"]})
    return out

def normalize_auxiliary(rows, rules):
    by_old={r["old_relation_key"]:r for r in rules}; out=[]
    for row in rows:
        source_field="fuente_canonica" if "fuente_canonica" in row else "fuente_id_canonico"
        obj_field="objeto_evidencia_id" if "objeto_evidencia_id" in row else "evidencia_id"
        old="|".join((row["necesidad_id"],row[source_field],row[obj_field])); rule=by_old.get(old); new=dict(row)
        if rule: new[source_field]=rule["fuente_canonica_normalizada"]; new[obj_field]=rule["objeto_evidencia_canonico"]
        out.append(new)
    return sorted(out,key=lambda r:(r["necesidad_id"],r.get("fuente_canonica",r.get("fuente_id_canonico","")),r.get("objeto_evidencia_id",r.get("evidencia_id",""))))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--repo",type=Path,required=True); ap.add_argument("--input",type=Path,required=True); ap.add_argument("--output",type=Path,required=True); ap.add_argument("--normalization",type=Path,required=True); args=ap.parse_args()
    args.output.mkdir(parents=True,exist_ok=True); baseline=read_tsv(args.input/"registro-demanda-universo-curado.tsv"); rejected_count=json.loads((args.input/"validacion.json").read_text())["resultado"]["artefactos_rechazados"]
    assignment_rows=read_tsv(args.input/"asignacion-workers.tsv"); assignments={r["fuente_id_canonico"]:r["worker_id"] for r in assignment_rows}; baseline_keys={key(r) for r in baseline}
    errors,evidence,rkeys,ekeys,worker_hashes=validate_worker_evidence(args.input,args.repo,baseline_keys,assignments)
    rules=read_tsv(args.normalization); integrated,provenance,expected,unexpected,norm_errors=normalize_records(baseline,rules); errors+=norm_errors
    original_string={"|".join(key(r)) for r in baseline}; result_string={"|".join(key(r)) for r in integrated}; expected_normalized={p["normalized_relation_key"] for p in provenance}; unexplained=expected_normalized-result_string; narrowing=bool(unexplained); errors += [f"pérdida inesperada {x}" for x in sorted(unexplained)]
    old_neg=sum(r["clasificacion_relacion"]=="NEGATIVA" for r in baseline); new_neg=sum(r["clasificacion_relacion"]=="NEGATIVA" for r in integrated); decisions=list(derive_decisions(baseline));
    for d in decisions:
        if d["necesidad_id"]=="N13" and d["fuente_canonica_normalizada"]=="ENASIC": d["objeto_evidencia_id"]="OE-59dce3f81e2e7722d336b538"
    counts=Counter(r["clasificacion_relacion"] for r in integrated)
    write_tsv(args.output/"registro-demanda-universo-curado.tsv",integrated,FIELDS); write_tsv(args.output/"evidencia-relaciones.tsv",evidence,LOCATOR_FIELDS); write_tsv(args.output/"normalizacion-fuentes.tsv",rules,list(rules[0])); write_tsv(args.output/"procedencias-relaciones.tsv",provenance,["old_relation_key","normalized_relation_key","accion","evidencia_ref"]); write_tsv(args.output/"decisiones-humanas.tsv",decisions,DECISION_FIELDS); write_tsv(args.output/"uso-modelo-relaciones.tsv",usage_rows(integrated),USO_FIELDS)
    for name in ("cambios-clasificacion.tsv","pendientes-siguiente-accion.tsv"):
        source_rows=read_tsv(args.input/name); normalized=normalize_auxiliary(source_rows,rules); write_tsv(args.output/name,normalized,list(source_rows[0]))
    input_sums=json.loads((args.input/"SHA256SUMS.json").read_text()); hashes_workers_intactos=all(input_sums.get(name)==digest for name,digest in worker_hashes.items()) and len(worker_hashes)==12
    source_counts=Counter(r["fuente_id_canonico"] for r in assignment_rows); workers_repetidos=sum(n>1 for n in source_counts.values())
    final_by={"|".join(key(r)):r for r in integrated}; states_changed=0; provenance_by_old={p["old_relation_key"]:p for p in provenance}
    for old in baseline:
        prov=provenance_by_old["|".join(key(old))]; target=final_by.get(prov["normalized_relation_key"])
        if target and target["clasificacion_relacion"]!=old["clasificacion_relacion"]: states_changed+=1
    ref_counts=Counter(r["referencia_estado"] for r in evidence)
    worker_relations=[r for i in range(1,5) for r in read_tsv(args.input/f"worker-{i}-relaciones.tsv")]
    new_negative_keys={key(r,"fuente_canonica") for r in worker_relations if r["estado_anterior"]=="CANDIDATA" and r["estado_propuesto"]=="NEGATIVA"}
    supported_keys={key(r,"fuente_canonica") for r in evidence if r["referencia_estado"]=="CONTENIDO_VERIFICADO"}
    supported_negatives=len(new_negative_keys & supported_keys); unsupported_negatives=sorted(new_negative_keys-supported_keys)
    errors += [f"negativa nueva sin soporte sustantivo: {k}" for k in unsupported_negatives]
    structural_ok=len(rkeys)==len(ekeys)==len(evidence)==157
    core_ok=not errors and structural_ok and not narrowing and old_neg==new_neg and states_changed==0 and workers_repetidos==0 and hashes_workers_intactos and supported_negatives==len(new_negative_keys)
    validation={"relaciones_semanticas_activas_multi2":len(baseline),"relaciones_semanticas_activas_multi2_fix":len(integrated),"artefactos_rechazados":rejected_count,"universo_contable_multi2":len(baseline)+rejected_count,"universo_contable_multi2_fix":len(integrated)+rejected_count,"alias_fuente_normalizados":len({r['alias_fuente'] for r in rules}),"relaciones_fusionadas_por_alias":len(expected),"evidencias_procedencia_conservadas":len(provenance),"claves_perdidas_esperadas_por_fusion":len(expected),"claves_perdidas_inesperadas":len(unexplained),"confirmadas":counts['CONFIRMADA'],"negativas":counts['NEGATIVA'],"candidatas":counts['CANDIDATA'],"no_accesibles":counts['NO_ACCESIBLE'],"conflictos_materiales":counts['CONFLICTO_MATERIAL'],"decisiones_humanas":len(decisions),"evidencias_esperadas":len(rkeys),"evidencias_recibidas":len(ekeys),"evidencias_correspondencia_estructural_valida":len(evidence) if structural_ok else 0,"localizadores_contenido_verificados":ref_counts['CONTENIDO_VERIFICADO'],"anclas_estructurales_o_indice_verificadas":ref_counts['ANCLA_ESTRUCTURAL_VERIFICADA'],"localizadores_no_verificados_no_materiales":ref_counts['NO_VERIFICADO_NO_MATERIAL'],"adjudicaciones_nuevas_con_soporte_sustantivo":supported_negatives,"localizadores_invalidos_materiales":ref_counts['INVALIDO_MATERIAL'],"referencias_invalidas":ref_counts['INVALIDO_MATERIAL'],"negativos_nuevos_esperados":len(new_negative_keys),"negativos_nuevos_con_soporte_por_clave":supported_negatives,"negativos_perdidos":max(0,old_neg-new_neg),"estados_protegidos_modificados":states_changed,"narrowing_detectado":narrowing,"workers_repetidos":workers_repetidos,"hashes_workers_intactos":hashes_workers_intactos,"core_ok":core_ok,"patch_ok":False,"parche_aplicable":False,"errores_integracion":errors,"ok":False}
    (args.output/"validacion.json").write_text(json.dumps(validation,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); print(json.dumps(validation,ensure_ascii=False,indent=2)); return 0 if validation['core_ok'] else 2
if __name__=="__main__": raise SystemExit(main())
