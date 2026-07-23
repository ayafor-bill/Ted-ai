"""
Prompt Engine - Builds prompts for domain selection and grounded analysis.
"""

import re
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class AnalysisResult:
    analysis: str
    questions: List[str]
    next_steps: List[str]
    raw_response: str
    selected_domains: List[str] = None
    phase_name: Optional[str] = None


def _format_evidence(evidence: List[Dict[str, Any]]) -> str:
    if not evidence:
        return "(none collected yet)"
    lines = []
    for i, ev in enumerate(evidence, 1):
        title = ev.get("title", "Untitled")
        ev_type = ev.get("evidence_type", "unknown")
        desc = ev.get("description", "")
        endpoint = ev.get("affected_endpoint", "")
        confidence = ev.get("confidence_level", "")
        endpoint_str = f" | Endpoint: {endpoint}" if endpoint else ""
        conf_str = f" | Confidence: {confidence}" if confidence != "" else ""
        lines.append(f"{i}. [{ev_type}] {title}{endpoint_str}{conf_str}\n   {desc}")
    return "\n".join(lines)


SELECTION_PROMPT_TEMPLATE = """You are a penetration testing mentor selecting which security testing methodology documents are relevant to review, based on the evidence collected so far in a real engagement.

EVIDENCE COLLECTED SO FAR:
{evidence_block}

AVAILABLE METHODOLOGY DOMAINS:
{domain_list}

Based ONLY on the evidence above, respond in EXACTLY this format:

DOMAINS: <comma-separated list of domain names from the list above that are relevant to this evidence, e.g. authentication_testing, jwt_testing>
STAGE: <one of: reconnaissance, discovery, hypothesis_generation, validation, evidence_collection, finding_confirmation, reporting>
REASONING: <one sentence explaining why these domains and this stage fit the evidence>

Select only domains that are actually relevant to specific evidence above — do not select a domain "just in case." If evidence is too sparse to justify any domain, return DOMAINS: none and explain what's missing in REASONING.
"""


def build_selection_prompt(evidence: List[Dict[str, Any]], domains: Dict[str, str]) -> str:
    domain_list = "\n".join(f"- {name}: {desc}" for name, desc in domains.items())
    return SELECTION_PROMPT_TEMPLATE.format(
        evidence_block=_format_evidence(evidence),
        domain_list=domain_list,
    )


@dataclass
class SelectionResult:
    domains: List[str]
    stage: str
    reasoning: str


def parse_selection_response(raw: str, valid_domains: List[str]) -> SelectionResult:
    domains_match = re.search(r"DOMAINS:\s*(.+)", raw)
    stage_match = re.search(r"STAGE:\s*(\w+)", raw)
    reasoning_match = re.search(r"REASONING:\s*(.+)", raw)

    domains = []
    if domains_match:
        raw_domains = domains_match.group(1).split("\n")[0]  # only first line
        candidates = [d.strip() for d in raw_domains.split(",")]
        domains = [d for d in candidates if d in valid_domains]

    stage = stage_match.group(1).strip() if stage_match else "reconnaissance"
    reasoning = reasoning_match.group(1).strip() if reasoning_match else ""

    return SelectionResult(domains=domains, stage=stage, reasoning=reasoning)


ANALYSIS_PROMPT_TEMPLATE = """You are a penetration testing mentor following established security testing methodology. You are reviewing a real bug bounty engagement's findings so far.

ENGAGEMENT LIFECYCLE STAGE: {stage}

EVIDENCE COLLECTED SO FAR:
{evidence_block}

RELEVANT METHODOLOGY GUIDANCE:
{methodology_content}

Based ONLY on the specific evidence listed above, respond in EXACTLY this format:

ANALYSIS:
<2-4 sentences describing what this specific evidence reveals about the target, and what it implies is worth testing next>

QUESTIONS:
1. <a question that references a SPECIFIC piece of evidence above by name/endpoint>
2. <another specific question>
3. <another specific question>

NEXT_STEPS:
1. <a concrete action tied directly to one of the findings above, naming the exact endpoint/evidence, and referencing the specific test/phase from the methodology guidance above>
2. <another concrete action>

RULES:
- Do not give generic security advice ("test for injection", "check authentication").
- Every question and step must name a specific endpoint, finding, or detail from the evidence above.
- Ground your next steps in the methodology guidance provided — reference the specific phase or test case it describes.
- If there is not enough evidence to say something specific, say so explicitly and ask what evidence is missing to proceed on THIS target.
"""


def build_analysis_prompt(stage: str, evidence: List[Dict[str, Any]], methodology_content: str) -> str:
    return ANALYSIS_PROMPT_TEMPLATE.format(
        stage=stage,
        evidence_block=_format_evidence(evidence),
        methodology_content=methodology_content or "(no specific domain methodology matched — reason generally from the evidence)",
    )


def parse_response(raw_response: str) -> AnalysisResult:
    analysis_match = re.search(r"ANALYSIS:\s*(.+?)(?=QUESTIONS:|$)", raw_response, re.DOTALL)
    questions_match = re.search(r"QUESTIONS:\s*(.+?)(?=NEXT_STEPS:|$)", raw_response, re.DOTALL)
    next_steps_match = re.search(r"NEXT_STEPS:\s*(.+)", raw_response, re.DOTALL)

    analysis = analysis_match.group(1).strip() if analysis_match else raw_response.strip()

    def extract_numbered_items(text: Optional[str]) -> List[str]:
        if not text:
            return []
        items = re.findall(r"^\s*\d+\.\s*(.+)$", text, re.MULTILINE)
        return [item.strip() for item in items if item.strip()]

    questions = extract_numbered_items(questions_match.group(1) if questions_match else None)
    next_steps = extract_numbered_items(next_steps_match.group(1) if next_steps_match else None)

    return AnalysisResult(
        analysis=analysis,
        questions=questions,
        next_steps=next_steps,
        raw_response=raw_response,
    )