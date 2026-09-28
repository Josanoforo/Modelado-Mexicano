"""Errores materiales: conservar cero dominios; no confundir m=1 con certeza."""
import json
from enoe_diagnostico import original,varianza_clusters

def main():
    base={k:'1' for k in original.CAMPOS}
    base.update(R_DEF='0',C_RES='1',EDA='30',FAC_TRI='1',EST_D_TRI='a',ENT='01',EMP_PPAL='1',CLASE2='1')
    rows=[]
    for upm,sex,clase,y in [('1','1','1','1'),('2','1','2','2'),('1','2','1','2')]:
        r=dict(base,UPM=upm,SEX=sex,CLASE2=clase,EMP_PPAL=y,N_REN=str(len(rows)+1));rows.append(r)
    g=original.medir(rows,original.CAMPOS)
    assert all(x['upm']==2 and x['singleton']==[] for x in g.values())
    assert varianza_clusters({'h':{'a':1.,'b':0.}})==1.
    assert varianza_clusters({'h':{'a':1.}}) is None
    assert varianza_clusters({'h':{'a':0.}}) is None
    assert varianza_clusters({'h':{'a':1.}},certeza={'h'})==0.
    print(json.dumps({'estado':'PASS','casos':['UPM sin miembros del dominio preservada por lector histórico','contribución cero incluida','singleton no identificable','singleton cero tampoco prueba certeza','certeza explícita sólo en sintético']}))

if __name__=='__main__': main()
