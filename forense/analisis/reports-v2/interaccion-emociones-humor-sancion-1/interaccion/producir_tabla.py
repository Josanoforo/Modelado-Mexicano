"""Produce the two editorial claim tables from explicit judgments and the current map.

Run from the repository root: python3 forense/analisis/reports-v2/
interaccion-emociones-humor-sancion-1/interaccion/producir_tabla.py
Only the two assigned table files are written.
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
BASE = Path(__file__).resolve().parents[1]
MAP = ROOT / "canon/mapa-dominios-v1_1.tsv"

# An explicit editorial decision for every mapped claim; map labels are not
# semantic decisions. Evidence IDs and scope are expanded in the v2 reports.
JUDGMENTS = {
"INTER": {
1:("SIN-CIFRA","Castillo 2019 is not securely identified; reputation-sensitive forgiveness is a bounded hypothesis, not national honor.","Map INTER-001; ADR-29.a; source acquisition pending"),
2:("MATIZA","Smith measured students' perceptions of what most compatriots endorse; r is within the Mexican student sample, not a population behavioral correlation.","Smith 2017 DOI 10.1016/j.aipprr.2017.03.001, Tables 1–3"),
3:("SIN-CIFRA","Goffman/Ting-Toomey offer an analogy, without a Mexican facework prevalence measure.","Map INTER-003; imported framework (c)"),
4:("SIN-CIFRA","The sympathy script is a definition, not a count of Mexicans who follow it.","Triandis 1984 as delimited in map INTER-004"),
5:("MATIZA","Scale factor structure in studied participants does not establish prevalence in Mexico residents.","Acevedo 2020; map INTER-005; diaspora (b)"),
6:("MATIZA","Observed conversation time in a bounded study cannot establish a national contrast.","Ramírez-Esparza 2009; map INTER-006"),
7:("MATIZA","Latino positive expression is not a Mexican population rate or unique motive.","Holloway 2009; map INTER-007"),
8:("SIN-CIFRA","Historical premise adherence has no verified current denominator and cannot explain all present interaction.","Díaz-Guerrero; map INTER-008"),
9:("MATIZA","Refusal strategies were recorded for male speakers in one community and prompted situations; quoted rate is not a national interaction share.","Félix-Brasdefer 2006 DOI 10.1016/j.pragma.2006.05.004, methods/results"),
10:("SIN-CIFRA","Albur functions are plausible but no frequency or causal dominance is estimated.","Map INTER-010; no comparable behavioral instrument"),
11:("SIN-CIFRA","Gossip may communicate or sanction; a main national conflict-resolution channel is unmeasured.","Map INTER-011; function versus prevalence"),
12:("MATIZA","Association with distress is from US Hispanic cohort; cannot be stated for all women in Mexico.","Nuñez 2016 HCHS/SOL; map INTER-012; diaspora (b)"),
13:("MATIZA","Clinical statements of selected patients are not a population script.","Gil and Vázquez 1996; map INTER-013; diaspora (b)"),
14:("MATIZA","Compared conflict preferences are study-specific and do not support uniform avoidance.","Gabrielidis 1997; map INTER-014"),
15:("MATIZA","Different responses to coworkers and contenders weaken a single national conflict style.","Posthuma 2006; map INTER-015"),
16:("MATIZA","Worker associations do not identify hierarchy as cause or silence as beneficial generally.","Madlock 2012; map INTER-016"),
17:("SIN-CIFRA","Meyer's typology is an imported descriptive model, not a representative behavioral measure.","Meyer Culture Map; map INTER-017; framework (c)"),
18:("MATIZA","Negotiation case descriptions are contextual; universal sequence and motive do not follow.","Ogliastri and Davis 2017; map INTER-018"),
19:("SIN-CIFRA","Permanent failure after threats is an untested universal intervention prediction.","Map INTER-019; requires negotiation outcome design"),
20:("ROMPE","The phrase six border states lists seven states and includes Sinaloa; INEGI's six-state border list excludes it. Only that geographic subclause breaks; directness remains unmeasured.","INEGI https://cuentame.inegi.org.mx/descubre/geografia/fronteras/ ; original v1 geography paragraph; map INTER-020"),
21:("MATIZA","Regional variation in scale answers does not identify region-specific directness in conversation.","Díaz-Loving 2018; map INTER-021"),
22:("MATIZA","Multi-country Generation Z statements cannot establish Mexican cohort change over time.","Madrigal-Moreno; map INTER-022"),
23:("SIN-CIFRA","The four-i slogan is a category, not a Mexican behavioral estimate.","Vilanova and Ortega 2017; map INTER-023"),
24:("SIN-CIFRA","Media exposure causing directness requires exposure, behavior and time measured together.","Map INTER-024; no identification"),
25:("MATIZA","Machismo/caballerismo factors were developed in diaspora; transfer to Mexico is unverified.","Arciniega 2008; map INTER-025; diaspora (b)"),
26:("MATIZA","Marianismo and couple findings come from selected US Mexican-origin samples; do not assign roles nationally.","Castillo 2010; Wheeler 2010; map INTER-026; diaspora (b)"),
27:("MATIZA","Convivial versus harmony labels suggest an affective contrast without paired Mexican/Asian behavioral measure.","Acevedo 2020; map INTER-027; mixed (b/c)"),
28:("SIN-CIFRA","One company case cannot rank national communication norms.","Amsterdam UAS case cited v1; map INTER-028"),
29:("SIN-CIFRA","Meyer contrast is an expert framework, not a matched Mexico–Spain frequency measure.","Meyer; map INTER-029; framework (c)"),
30:("MATIZA","Hofstede country scores are descriptive aggregates; causal and individual claims removed.","ADR-06; map INTER-030; Hofstede (c)"),
31:("MATIZA","GLOBE practice/aspiration contrast is managerial/cluster-level; downward assertion is a hypothesis.","House et al. 2004; map INTER-031"),
32:("MATIZA","Original WVS/ENCUCI trust trajectory combines waves and instruments; no verified comparable communication trend.","Map INTER-032; trust v2 Q57 correction"),
33:("SIN-CIFRA","Israeli dugri offers a contrast of discourse norms, not maximum polar distance.","Katriel 1986; map INTER-033"),
34:("MATIZA","Urban safety perception is measurable, but cannot be a national interpersonal speech rate or mechanism.","ENSU 2024; map INTER-034; no GEN2 interaction RESULT"),
35:("SIN-CIFRA","Homicide and disappearance cumulative figures have different registers and denominators and no direct speech link.","Map INTER-035; acquisition and reconciliation pending"),
36:("MATIZA","Institutional trust survey responses do not identify a causal cycle of indirect speech.","LAPOP/ENCUCI; map INTER-036; trust v2"),
37:("SIN-CIFRA","The saying is a local survival account, not a measured national mechanism.","Parra Rosales 2019; map INTER-037"),
38:("MATIZA","Somatic symptom association in Mexican adults does not identify suppressed speech as its cause.","Brambila-Tapia 2023; map INTER-038"),
39:("MATIZA","Hispanic/migrant symptom studies have a different target population; national transfer unwarranted.","Koss 1990; Escobar 2000; map INTER-039; diaspora (b)"),
40:("SIN-CIFRA","Controlarse/aguantarse/sobreponerse are proposed constructs without a frequency or causal effect here.","Map INTER-040"),
41:("MATIZA","Association of suppression type and anhedonia in US Mexican-origin adolescents is not a Mexican therapy rule.","Study PMC9644291; map INTER-041; diaspora (b)"),
42:("MATIZA","Multisource feedback findings do not prove universal failure or optimal feedback design in Mexico.","Varela and Premeaux 2008; map INTER-042"),
43:("MATIZA","US Latino clinical samples cannot set a Mexico-resident disclosure schedule.","Kim, Lau and Chorpita 2016; map INTER-043; diaspora (b)"),
44:("SIN-CIFRA","Never/always negotiation and management advice lacks evaluated outcome and segment conditions.","Map INTER-044; proposed intervention only"),
45:("SIN-CIFRA","No comparable hemisphere-wide study ranks national indirectness; superlative withdrawn.","Map INTER-045; no common instrument"),
},
"EMOC": {
1:("MATIZA","Students rated perceived compatriot norms, not their own identity; rankings are sample comparisons with invariance limits.","Smith 2017 DOI 10.1016/j.aipprr.2017.03.001, Tables 1–2"),
2:("MATIZA","Correlations are within-sample associations among perceived national norms, not Mexican behavior or country-level correlation.","Smith 2017 Table 3"),
3:("MATIZA","Regional self-construal contrast challenges a binary but does not identify Mexican moral emotion.","Krys 2022 as mapped EMOC-003; Salvador 2025 update"),
4:("MATIZA","Relational-mobility ranking is a study/sample score, not a mechanism causing Mexican face behavior.","Thomson 2018; map EMOC-004"),
5:("MATIZA","Hofstede indulgence is an aggregate descriptive index, not individual emotion or causal variable.","Hofstede (c); ADR-06; map EMOC-005"),
6:("SIN-CIFRA","Perceived/desirable control from other samples is not an estimate of moral emotion in Mexico.","Hornsey 2019; map EMOC-006"),
7:("SIN-CIFRA","Public shame versus private guilt is a proposed contrast without paired Mexican measurement.","Benedict (c); map EMOC-007"),
9:("MATIZA","Census supports affiliation change, not guilt decline; historical and current denominators require separation.","INEGI Census 2020 religion table; map EMOC-009"),
10:("SIN-CIFRA","Warm rather than hierarchical motive is not separated by observed matched interaction data.","Triandis (c/b); map EMOC-010"),
11:("MATIZA","Historical premises are documented but do not describe current modal morality or prove mechanism.","Díaz-Guerrero; map EMOC-011"),
12:("MATIZA","Shame/guilt–distress associations are scale- and sample-specific and often imported.","TOSCA/GASP literature; map EMOC-012; framework (c)"),
13:("MATIZA","Marianismo and self-silencing evidence is largely US Latina; Mexico transport unverified.","HCHS/SOL; map EMOC-013; diaspora (b)"),
14:("MATIZA","Two-factor machismo/caballerismo construct comes from US Mexican-origin populations.","Arciniega 2008; map EMOC-014; diaspora (b)"),
15:("MATIZA","Smith challenges a fixed honor assignment for its student sample; it does not refute honor in every Mexican context.","Smith 2017; ADR-29.a; map EMOC-015"),
16:("SIN-CIFRA","Institutional weakness causing face behavior has no identified causal pathway here.","Map EMOC-016; trust v2 distinguishes referents"),
17:("MATIZA","Original generic trust attribution is unstable across WVS/ENAFI; no shared trend or emotion mechanism.","Map EMOC-017; trust v2 Q57 correction"),
18:("MATIZA","Latinobarómetro generalized trust is a distinct question and wave; cannot corroborate a WVS number by equal rounding.","Map EMOC-018; trust v2"),
19:("MATIZA","Government trust across waves/instruments cannot be read as a proven causal rebound in moral emotion.","Map EMOC-019; trust v2"),
20:("SIN-CIFRA","Cross-sectional age/religion differences cannot show within-cohort change toward dignity.","Map EMOC-020; no repeated emotion measure"),
21:("SIN-CIFRA","Segmentation is a methodological recommendation, not its own prevalence statistic.","Map EMOC-021"),
22:("SIN-CIFRA","Composite dignity+face+guilt+shame architecture is a testable synthesis, not jointly observed.","Map EMOC-022; no common respondent design"),
23:("MATIZA","Within-country variation cannot be asserted always larger without matched variable and sample.","Fischer and Schwartz 2011; map EMOC-023"),
24:("MATIZA","2025 self-enhancement study concerns self-construal and interdependence, not Mexican face or guilt frequency.","Salvador et al. 2025 primary study; map EMOC-024"),
25:("MATIZA","Adolescent shame-management scale establishes factors in its validation sample, not national shame prevalence.","MOSS-SAST; map EMOC-025"),
26:("SIN-CIFRA","No representative emotion-specific item in this report separates shame from face by community type.","Map EMOC-026; instrument inadequate"),
27:("SIN-CIFRA","Local guilt scales do not identify a national Catholic-guilt mechanism or trend.","Reidl/Jurado and local scale; map EMOC-027"),
28:("MATIZA","Life satisfaction and depression in Smith are distinct outcomes in students; cannot infer protective dignity for all Mexico.","Smith 2017; map EMOC-028"),
29:("MATIZA","Census affiliation shares are primary external figures; affiliation cannot stand in for felt guilt.","INEGI 2020 Census religion table; map EMOC-029"),
30:("SIN-CIFRA","Chiapas highest proportion does not prove highest absolute evangelical population or stated ranking.","INEGI Panorama de las religiones 2020; map EMOC-030"),
31:("SIN-CIFRA","Gap in indigenous moral-cosmology measures is real for this corpus, not a claim that measurement is impossible.","Map EMOC-031; project scope"),
32:("SIN-CIFRA","Message and leadership effectiveness requires outcome experiments; proposed use is not established.","Map EMOC-032; no intervention test"),
},
}

EXTRA = {
"INTER": [
 ("INTER-EXTRA-01","Mexico is the hemisphere's most consistently indirect communication profile", "SIN-CIFRA","No common, representative hemisphere-wide act measure or denominator.","V1 closing paragraph; map INTER-045 adjacent"),
 ("INTER-EXTRA-02","A Mexican yes frequently means probably and predicts later nonperformance", "SIN-CIFRA","Speech interpretation and subsequent action were not jointly observed.","V1 refusal paragraph; Félix-Brasdefer 2006 limited scenarios"),
 ("INTER-EXTRA-03","Precolonial protocol caused contemporary indirect speech", "SIN-CIFRA","Historical analogy has no identified transmission design.","V1 structural paragraph"),
 ("INTER-EXTRA-04","Catholic gossip taboo creates paradox in Mexican conflict resolution", "SIN-CIFRA","Requires measured practice and moral judgment in the same communities.","V1 gossip paragraph"),
],
"EMOC": [
 ("EMOC-EXTRA-01","Catholic guilt is declining as a moral feeling", "SIN-CIFRA","Census affiliation trend contains no guilt measure.","V1 executive claim; INEGI Census 2020"),
 ("EMOC-EXTRA-02","Dignity is declared while warm face is practiced by the same people", "SIN-CIFRA","Smith elicits perceived norms and no paired conduct.","V1 central synthesis; Smith 2017"),
 ("EMOC-EXTRA-03","Honor is peripheral particularly in men and violent regions", "SIN-CIFRA","Neither distribution nor region-by-sex honor response established.","V1 Pattern E"),
],
}

def main() -> None:
    with MAP.open(encoding="utf-8", newline="") as fh:
        mapped = list(csv.DictReader(fh, delimiter="\t"))
    for prefix, directory in (("INTER", "interaccion"), ("EMOC", "moral")):
        selected = [r for r in mapped if r["id_afirmacion"].startswith(f"ASTRA5-U0-{prefix}-")]
        ids = {int(r["id_afirmacion"].rsplit("-",1)[1]) for r in selected}
        assert ids == set(JUDGMENTS[prefix]), (prefix, ids ^ set(JUDGMENTS[prefix]))
        out = BASE / directory / "tabla-afirmaciones.tsv"
        with out.open("w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=["id", "id_mapa", "localizador_v1", "afirmacion_original", "dictamen", "razon", "evidencia"], delimiter="\t", lineterminator="\n")
            w.writeheader()
            for r in selected:
                n = int(r["id_afirmacion"].rsplit("-",1)[1])
                status, reason, evidence = JUDGMENTS[prefix][n]
                w.writerow(dict(id=r["id_afirmacion"],id_mapa=r["id_afirmacion"],localizador_v1=r["localizador"],afirmacion_original=r["texto_vigente"],dictamen=status,razon=reason,evidencia=evidence))
            for identifier, claim, status, reason, evidence in EXTRA[prefix]:
                w.writerow(dict(id=identifier,id_mapa="",localizador_v1="fuera del mapa",afirmacion_original=claim,dictamen=status,razon=reason,evidencia=evidence))
        print(f"{out.relative_to(ROOT)}: {len(selected)} map rows + {len(EXTRA[prefix])} extra")

if __name__ == "__main__":
    main()
