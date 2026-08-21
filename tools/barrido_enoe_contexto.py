import os,re,subprocess,sys,unicodedata
CORPUS="/home/pc0/mm-corpus/raw"
def plegar(s):
    s=unicodedata.normalize("NFD",s.lower())
    return "".join(c for c in s if unicodedata.category(c)!="Mn")
def texto(p):
    r=subprocess.run(["pdftotext","-layout",p,"-"],capture_output=True,text=True,errors="replace")
    t=r.stdout
    try:
        import pypdf; t+="\n"+"\n".join((x.extract_text() or "") for x in pypdf.PdfReader(p).pages)
    except Exception: pass
    return plegar(t)
term=sys.argv[1]; ancho=int(sys.argv[2]) if len(sys.argv)>2 else 90
files=sys.argv[3:] if len(sys.argv)>3 else sorted(f for f in os.listdir(CORPUS) if re.match(r"(c_(amp|bas|sdem)_v|fd_c_|enoe_(123|325)_fd)",f) and f.endswith(".pdf"))
vistos=set()
for f in files:
    t=texto(os.path.join(CORPUS,f))
    for m in re.finditer(re.escape(plegar(term)),t):
        i=m.start()
        c=re.sub(r"\s+"," ",t[max(0,i-ancho):i+len(term)+ancho]).strip()
        k=c[:110]
        if k in vistos: continue
        vistos.add(k)
        print(f"[{f[:22]:22s}] …{c}…")
print(f"\n({len(vistos)} contextos distintos para «{term}» en {len(files)} PDF)")
