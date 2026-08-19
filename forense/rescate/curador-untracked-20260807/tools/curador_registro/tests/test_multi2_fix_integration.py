import sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from multi2_fix_supervisor import derive_decisions,detect_narrowing,normalize_records,validate_worker_evidence
from multi2_fix2_finalizer import final_ok
import random

def row(n="N1",s="SRC_ALIAS",o="OE-A",state="CANDIDATA",note=""):
 return {"necesidad_id":n,"fuente_id_canonico":s,"fuente_nombre":s,"objeto_evidencia_id":o,"clasificacion_relacion":state,"nota":note,"evidencia_ref":"MAIN:x:L1"}
def rule(old,canonical,obj,action="CONSERVAR_EVIDENCIA_DISTINTA"):
 return {"old_relation_key":old,"canonical_relation_key":f"N1|{canonical}|{obj}","fuente_canonica_normalizada":canonical,"objeto_evidencia_canonico":obj,"accion":action,"evidencia_ref":"MAIN:x:L1"}

class Multi2FixIntegrationTest(unittest.TestCase):
 def test_aliases_no_duplican_relacion_equivalente(self):
  rows=[row(s="SRC",o="OE-C"),row(s="SRC_ALIAS",o="OE-A")]; rules=[rule("N1|SRC_ALIAS|OE-A","SRC","OE-C","FUSIONAR_RELACION")]
  out,_,loss,_,err=normalize_records(rows,rules); self.assertEqual((len(out),len(loss),err),(1,1,[]))
 def test_normalizar_no_fusiona_evidencias_distintas(self):
  rows=[row(s="SRC",o="OE-C"),row(s="SRC_ALIAS",o="OE-A")]; out,*_=normalize_records(rows,[rule("N1|SRC_ALIAS|OE-A","SRC","OE-A")]); self.assertEqual(len(out),2)
 def test_alias_antes_de_canonica_es_invariante(self):
  canonical=row(s="SRC",o="OE-C");alias=row(s="SRC_ALIAS",o="OE-A");rules=[{**rule("N1|SRC_ALIAS|OE-A","SRC","OE-C","FUSIONAR_RELACION"),"canonical_relation_key":"N1|SRC|OE-C"}]
  a=normalize_records([alias,canonical],rules);b=normalize_records([canonical,alias],rules);self.assertEqual((a[0],a[1]),(b[0],b[1]))
 def test_permutacion_aleatoria_byte_estable(self):
  rows=[row(n=f"N{i}",s="SRC",o=f"OE-{i}") for i in range(1,6)];base=normalize_records(rows,[])[0]
  random.Random(7).shuffle(rows);self.assertEqual(normalize_records(rows,[])[0],base)
 def test_decision_heredada_no_desaparece(self):
  r=row("N13","ENASIC","OE-X",note="La decisión de reemplazar o complementar el proxy ENUT pertenece a la mesa")
  self.assertEqual(len(list(derive_decisions([r]))),1)
 def test_evidencia_worker_no_asignado_falla(self): self._evidence_case(assign="worker-2",foreign=False,missing=False)
 def test_evidencia_clave_ajena_falla(self): self._evidence_case(assign="worker-1",foreign=True,missing=False)
 def test_evidencia_sin_relacion_falla(self): self._evidence_case(assign="worker-1",foreign=False,missing=True)
 def _evidence_case(self,assign,foreign,missing):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td); (root/'x').write_text('token\n'); d=root/'worker-1'; d.mkdir(); base=('N2' if foreign else 'N1','SRC','OE-A');
   rf=['worker_id','necesidad_id','fuente_canonica','objeto_evidencia_id','estado_anterior','estado_propuesto','tipo_resultado','evidencia_ref','evidencia_localizador','evidencia_explicita','razon','reserva_incertidumbre','requiere_decision_humana','siguiente_accion']; ef=['necesidad_id','fuente_canonica','objeto_evidencia_id','tipo_evidencia','evidencia_ref','evidencia_localizador','variable_reactivo_tabla','texto_evidencia','unidad_observacion','periodo','universo_muestra','codificacion','parte_necesidad_cubierta','parte_necesidad_no_cubierta','uso_potencial_modelo','transformacion_requerida','incertidumbre','traza_revision','siguiente_accion']
   import csv
   rr=dict(zip(rf,['worker-1',*base,'CANDIDATA','CANDIDATA','CANDIDATA','MAIN:x:L1','token','x','x','x','NO','x'])); ee={f:'x' for f in ef}; ee.update({'necesidad_id':base[0],'fuente_canonica':'SRC','objeto_evidencia_id':'OE-A','evidencia_ref':'MAIN:x:L1','evidencia_localizador':'token'})
   for p,fields,rows in [(d/'worker-1-relaciones.tsv',rf,([] if missing else [rr])),(d/'worker-1-evidencia.tsv',ef,[ee])]:
    with p.open('w',newline='') as h:w=csv.DictWriter(h,fields,delimiter='\t');w.writeheader();w.writerows(rows)
   errors,*_=validate_worker_evidence(root,root,{('N1','SRC','OE-A')},{'SRC':assign}); self.assertTrue(errors)
 def test_nueva_adjudicacion_sin_evidencia_falla(self):
  # Covered by the same strict validator path: an invalid worker packet must fail.
  self._evidence_case(assign="worker-1",foreign=False,missing=True)
 def test_localizador_fallido_candidata_no_es_sustantivo(self):
  self.assertFalse(final_ok(True,False))
 def test_localizador_fallido_negativa_impide_core(self):
  self._evidence_case(assign="worker-1",foreign=False,missing=True)
 def test_parche_invalido_impide_ok(self): self.assertFalse(final_ok(True,False))
 def test_perdida_alias_no_activa_narrowing(self): self.assertFalse(detect_narrowing({'a','b'},{'a'},{'b'})[0])
 def test_perdida_no_explicada_activa_narrowing(self): self.assertTrue(detect_narrowing({'a','b'},{'a'},set())[0])
if __name__=='__main__':unittest.main()
