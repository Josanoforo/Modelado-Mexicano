---
title: Consultar
---

# Consultar el Benchmark

[Portada]({{ '/' | relative_url }}) · [Contrato de consulta]({{ '/consulta.html' | relative_url }}) · [Ejemplos]({{ '/ejemplos.html' | relative_url }}) · [Verifica en 5 minutos]({{ '/verificar.html' | relative_url }}) · [Reto público]({{ '/reto.html' | relative_url }})

Escribe una conducta y, si quieres, un segmento. La página devuelve el **piso** adoptado del catálogo vigente con su intervalo, unidad, ola, origen y la cita `RESULT`/`CALC`/hash para verificarlo — exactamente lo que define el [contrato]({{ '/consulta.html' | relative_url }}). Todo corre en tu navegador sobre un archivo estático; no hay servidor. Toda cifra es retrospectiva y descriptiva de su ola: no es predicción ni efecto causal.

<div id="bm" data-base="{{ '/data/' | relative_url }}">
<form id="bm-f" onsubmit="return false">
<p><label>Conducta (palabras o id) <input id="bm-t" size="40" placeholder="ahorro · desocupacion · mensajes"></label></p>
<p><label>Eje <select id="bm-e"><option value="">(cualquiera)</option></select></label>
<label>Valor <input id="bm-v" size="14" placeholder="mujer · 18-29 · ENT_09"></label></p>
<p><label>Instrumento <input id="bm-i" size="10" placeholder="ENIF"></label>
<label>Ola <input id="bm-o" size="6" placeholder="2024"></label>
<button id="bm-b" type="submit">Consultar</button></p>
</form>
<p id="bm-s">Cargando catálogo…</p>
<div id="bm-r"></div>
</div>

<style>
#bm .card{border:1px solid #ccc;border-radius:6px;padding:.6em .8em;margin:.6em 0;font-size:.92em}
#bm .card b{font-size:1.05em}#bm .mut{color:#666}#bm .nc{border-color:#c90;background:#fff8e6}
#bm code{word-break:break-all}
</style>

<script>
(function(){
"use strict";
var root=document.getElementById("bm"),base=root.getAttribute("data-base"),D=null,F=null,IDX=null;
var $=function(i){return document.getElementById(i)};
function norm(s){return String(s).normalize("NFD").replace(/[̀-ͯ]/g,"").toLowerCase()}
function esc(s){return String(s==null?"":s).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;"}[c]})}
function fila(r){var o={},c=D.columnas,d=D.diccionarios;for(var j=0;j<c.length;j++){o[c[j]]=d[c[j]]?d[c[j]][r[j]]:r[j]}
 if(!o.llave){o.llave=/^\d+$/.test(o.celda)?o.result_id+"#"+o.celda:o.result_id}return o}
function tipoIC(n){n=n.toUpperCase();if(n.indexOf("SIN-IC")===0)return"sin-ic";
 if(n.indexOf("CALIBRADO")>=0&&n.indexOf("SIN-CALIBRACION")<0)return"calibrado";
 if(n.indexOf("SPEC")>=0||n.indexOf("T-1")>=0)return"ic-con-r";return"diseno"}
function hay(o){var h=norm([o.conducta,o.dominio,o.instrumento,o.llave].join(" "));return h.replace(/[_-]/g," ")+" "+h}
function carga(){
 fetch(base+"catalogo-vigente.json").then(function(r){return r.json()}).then(function(p){
  return fetch(base+p.archivo)}).then(function(r){return r.json()}).then(function(d){
  D=d;F=d.filas.map(fila);IDX=F.map(hay);
  Object.keys(d.ejes).forEach(function(e){var o=document.createElement("option");o.value=e;o.textContent=e;$("bm-e").appendChild(o)});
  $("bm-s").textContent="Catálogo "+d.catalogo+" · "+F.length+" pisos adoptados · contrato "+d.contrato;
 }).catch(function(e){$("bm-s").textContent="No se pudo cargar el catálogo ("+e+"). Si abriste esta página como archivo local, sírvela con: python3 -m http.server"})}
function consulta(){
 if(!D)return;var t=$("bm-t").value.trim(),e=$("bm-e").value,v=norm($("bm-v").value.trim()),
 ins=$("bm-i").value.trim().toUpperCase(),ola=$("bm-o").value.trim();
 var exacta=F.some(function(o){return o.conducta===t});
 var pal=exacta?[]:norm(t).replace(/_/g," ").split(/\s+/).filter(Boolean);
 var ejes=e?D.ejes[e]:null,out=[],nc=[];
 var exSeg=!!(ejes&&v&&F.some(function(o){return ejes.indexOf(o.eje)>=0&&norm(o.segmento)===v}));
 for(var i=0;i<F.length;i++){var o=F[i];
  if(exacta&&o.conducta!==t)continue;
  if(pal.length&&!pal.every(function(w){return IDX[i].indexOf(w)>=0}))continue;
  if(ins&&o.instrumento.toUpperCase()!==ins)continue;
  if(ola&&o.ola!==ola)continue;
  if(ejes&&(ejes.indexOf(o.eje)<0||(v&&(exSeg?norm(o.segmento)!==v:norm(o.segmento).indexOf(v)<0))))continue;
  out.push(o)}
 if(ins&&ola&&D.olas_reservadas.indexOf(ins+" "+ola)>=0)nc.push(["OLA-RESERVADA",ins+" "+ola+": reservada en data/manifiesto.yaml (E.6); no se abre ni se consulta"]);
 if(t){var calcs={};out.forEach(function(o){calcs[o.calc]=1});var g={};
  D.excluidos.forEach(function(x){if(ins&&x[1].toUpperCase().indexOf(ins)<0)return;var etq=calcs[x[1]]?x[3]:norm(x[0]),ok;
   if(exacta){ok=etq.split(/[\s#]+/).indexOf(norm(t))>=0||etq.indexOf("-"+norm(t)+"-")>=0}
   else{var tt=etq.replace(/[_-]/g," ")+" "+etq;ok=pal.every(function(w){return tt.indexOf(w)>=0})}
   if(!ok)return;var r=/^CELDA-(SUPRIMIDA|NO-ESTIMABLE)/.test(x[2])?"SEGMENTO-NO-ESTIMABLE":"FUERA-POR-REGLA";
   var k=r+"|"+x[2];(g[k]=g[k]||[]).push(x[0])});
  Object.keys(g).sort().forEach(function(k){var p=k.split("|");nc.push([p[0],p[1]+": "+g[k].length+" celda(s), p. ej. "+g[k][0]])});
  if(pal.length)D.cobertura.forEach(function(c){if(c.estado!=="MEDIDO"&&pal.every(function(w){return norm(c.dominio+" "+c.report).replace(/_/g," ").indexOf(w)>=0}))nc.push(["DOMINIO-NO-MEDIDO",c.dominio+": "+c.estado])})}
 if(!out.length&&!nc.length)nc.push(["SIN-COINCIDENCIA","ninguna fila del catálogo vigente casa; universo = catálogo completo"]);
 pinta(out,nc)}
function pinta(out,nc){
 var h=["<p><b>"+out.length+"</b> fila(s)"+(out.length>50?" · se muestran 50; afina con eje, instrumento u ola":"")+"</p>"];
 out.slice(0,50).forEach(function(o){
  var ic=o.ic95_inf&&o.ic95_sup?"["+(+o.ic95_inf).toPrecision(6)+", "+(+o.ic95_sup).toPrecision(6)+"]":"sin IC identificado (vacío no es cero)";
  var hs=D.hashes[o.calc]||["",""],rg=o.alcance==="PARAMETRO-DE-REGLA"?D.reglas[o.segmento]:null;
  h.push("<div class='card'><b>"+esc(o.conducta)+"</b> · "+esc(o.instrumento)+" "+esc(o.ola)+" · "+esc(o.eje)+"="+esc(o.segmento)+
  "<br>punto <b>"+esc(o.punto)+"</b> · IC95 "+esc(ic)+" <span class='mut'>("+tipoIC(o.naturaleza_ic)+": "+esc(o.naturaleza_ic)+")</span> · unidad "+esc(o.unidad)+
  "<br>"+esc(o.temporalidad)+" · origen "+esc(o.origen_piso)+" · "+esc(o.estado_adopcion)+" · "+esc(o.alcance)+" · firma <code>"+esc(o.firma_fp)+"</code>"+
  "<br>cita <code>"+esc(o.llave)+"</code> · <code>"+esc(o.calc)+"</code> · resultados <code>"+esc(hs[0].slice(0,12))+"</code> · sello <code>"+esc(hs[1].slice(0,12))+"</code>"+
  "<br>oferta: "+esc(o.oferta_exclusion)+
  (rg?"<br>regla "+esc(o.segmento)+" · tier "+esc(rg.tier)+" · falsable si: "+esc(rg.falsable_si):"")+
  (o.reserva?"<br><span class='mut'>reserva: "+esc(o.reserva)+"</span>":"")+
  "<br><span class='mut'>verifica: <code>python3 tools/benchmark.py verificar '"+esc(o.llave)+"'</code></span></div>")});
 nc.forEach(function(n){h.push("<div class='card nc'>NO CONTESTA · <b>"+esc(n[0])+"</b> · "+esc(n[1])+"</div>")});
 h.push("<p class='mut'>"+esc(D.terminos)+"</p>");
 $("bm-r").innerHTML=h.join("")}
$("bm-b").addEventListener("click",consulta);$("bm-f").addEventListener("submit",consulta);
carga();
})();
</script>

**Cómo verificar lo que ves.** Cada tarjeta trae la orden `python3 tools/benchmark.py verificar '<llave>'`, que desde un clon recorre `sello.sha256 → sello.json → resultados.json` y compara el valor sellado con el punto mostrado, sin abrir microdato. La receta completa está en [Verifica en 5 minutos]({{ '/verificar.html' | relative_url }}).

El archivo que carga esta página se deriva con `python3 tools/benchmark.py exporta` y un test comprueba que es idéntico al catálogo vigente, fila por fila. Lo que la página no puede contestar lo dice con su razón (segmento no estimable, dominio no medido, ola reservada, eje no disponible).
