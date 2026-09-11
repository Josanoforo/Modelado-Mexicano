#!/usr/bin/env python3
"""Completa sólo los campos técnicos del formulario OECD Trust Survey PUM.

El original registrado queda fuera de Git. Este derivador exige su hash conocido,
preserva todos los miembros y metadatos del DOCX y deja intactos los campos de
identidad, afiliación, país, fecha de término, firma y fecha de firma.
"""

from __future__ import annotations

import argparse
import hashlib
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


SOURCE_SHA256 = "4a3ac6d704caa67e1a4dfc702b5a38747a56eb48e086d3aae4c14814601af915"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XML = "http://www.w3.org/XML/1998/namespace"

INTENDED_USE = (
    "Research question. For Mexico, how are interpersonal trust and trust in public "
    "institutions associated with perceived public-sector integrity, reliability, "
    "responsiveness, openness and fairness, and how do those relationships vary with "
    "social or organisational connection measures? This is a robustness study for an "
    "existing research need; it will not replace the existing WVS7 result unless the "
    "constructs and populations are shown to be comparable.",
    "Coverage. Use Mexico in each PUM wave in which Mexico is actually present among "
    "2021, 2023 and 2025. Cross-country analysis is limited to Chile, Colombia and Costa "
    "Rica, and only for questions harmonised with Mexico in the same collection. No "
    "country or wave will be treated as available before inspecting the delivered file.",
    "Variables. Request respondent identifier, country and wave/date; final survey "
    "weights and released design or replicate variables; Q1 interpersonal trust; Q2 "
    "institutional trust; Q5 or its harmonised integrity/bribery equivalent; Q8-Q22 or "
    "harmonised drivers of responsiveness, reliability, openness and fairness; Q33-Q34 "
    "or harmonised participation, volunteering, association and network measures; B14 "
    "or harmonised victimisation/bribery experience; survey mode; and the age, sex or "
    "gender, education, household composition, income or economic-well-being controls "
    "released in the PUM.",
    "Method. Begin with Mexico-specific weighted distributions and missingness. Then "
    "estimate pre-specified weighted regressions and interactions between trust, trust "
    "drivers and connection measures. Cross-country estimates will use only documented "
    "harmonised variables and will report wave, sample, weights, uncertainty and "
    "sensitivity to controls separately. Results are associational, not causal.",
    "Why microdata are necessary. Published indicators and StatLinks provide marginal "
    "aggregates, but not the respondent-level joint distributions, covariate adjustment, "
    "within-Mexico subgroup sample sizes, missing-data patterns or harmonisation checks "
    "required by the research question. Existing public OECD indicator extracts will "
    "not be downloaded again or presented as substitutes for those joint analyses.",
    "Data treatment. The PUM will be used only for non-commercial academic or policy "
    "research, accessed only by approved signatories in the access-controlled storage "
    "environment they truthfully declare outside this repository, and never redistributed "
    "or used to identify respondents. Only aggregate statistical outputs will leave that "
    "environment; small cells will be suppressed under the OECD terms. Retention and "
    "destruction will follow the executed agreement; no date is asserted in this draft.",
)

PLANNED_OUTPUTS = (
    "A reproducible technical report or working paper containing only aggregate tables, "
    "figures and model summaries; a methods appendix documenting variables, weights, "
    "harmonisation, missingness and sensitivity analyses; and, if warranted by the "
    "results, a non-commercial academic or policy paper. Outputs will cite the OECD "
    "Trust Survey and use the required disclaimer. No microdata, record-level examples "
    "or disclosure-risk outputs will be published."
)


def paragraph_text(paragraph: ET.Element) -> str:
    return "".join(node.text or "" for node in paragraph.iter(f"{{{W}}}t"))


def add_text(paragraph: ET.Element, value: str) -> None:
    if paragraph_text(paragraph).strip():
        raise ValueError("el párrafo técnico de destino no está vacío")
    run = ET.SubElement(paragraph, f"{{{W}}}r")
    text = ET.SubElement(run, f"{{{W}}}t")
    text.set(f"{{{XML}}}space", "preserve")
    text.text = value


def complete_document_xml(payload: bytes) -> bytes:
    ET.register_namespace("w", W)
    root = ET.fromstring(payload)
    paragraphs = list(root.iter(f"{{{W}}}p"))
    texts = [paragraph_text(p) for p in paragraphs]

    intended = next(
        i for i, value in enumerate(texts) if value.startswith("Intended use of the data")
    )
    outputs = next(
        i for i, value in enumerate(texts) if value.startswith("Planned outputs")
    )
    completion = next(
        i for i, value in enumerate(texts) if value.startswith("Expected completion date")
    )
    intended_targets = [
        i for i in range(intended + 1, outputs) if not texts[i].strip()
    ]
    if len(intended_targets) < len(INTENDED_USE):
        raise ValueError("el formulario no tiene suficientes párrafos técnicos vacíos")
    outputs_target = next(i for i in range(outputs + 1, completion) if not texts[i].strip())
    for target, value in zip(intended_targets, INTENDED_USE):
        add_text(paragraphs[target], value)
    add_text(paragraphs[outputs_target], PLANNED_OUTPUTS)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    digest = hashlib.sha256(args.source.read_bytes()).hexdigest()
    if digest != SOURCE_SHA256:
        raise SystemExit(f"hash de formulario inesperado: {digest}")
    args.output.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(args.source) as source:
        document_xml = complete_document_xml(source.read("word/document.xml"))
        with tempfile.NamedTemporaryFile(
            dir=args.output.parent, prefix=f".{args.output.name}.", delete=False
        ) as handle:
            temporary = Path(handle.name)
        try:
            with zipfile.ZipFile(temporary, "w") as target:
                for item in source.infolist():
                    payload = document_xml if item.filename == "word/document.xml" else source.read(item)
                    target.writestr(item, payload)
            temporary.replace(args.output)
        finally:
            temporary.unlink(missing_ok=True)

    with zipfile.ZipFile(args.output) as result:
        corrupt_member = result.testzip()
        if corrupt_member is not None:
            raise SystemExit(f"miembro DOCX corrupto: {corrupt_member}")
        text = paragraph_text(ET.fromstring(result.read("word/document.xml")))
    for required in ("Research question.", "Why microdata are necessary.", "A reproducible technical report"):
        if required not in text:
            raise SystemExit(f"texto técnico ausente: {required}")
    for field in (
        "Expected completion date of the research project:",
        "Name", "Affiliation", "Country", "Signature", "Date",
    ):
        if field not in text:
            raise SystemExit(f"campo personal perdido: {field}")
    print(f"OK: {args.output} · sha256={hashlib.sha256(args.output.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
