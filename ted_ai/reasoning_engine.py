"""
Ted-AI Grounded Reasoning Engine

Two-call design for accuracy:
  Call 1: LLM selects which domain methodology file(s) are relevant + engagement stage
  Call 2: LLM analyzes evidence grounded in the full content of the selected domain(s)
"""

import logging
from typing import Dict, Any, Optional

from ted_ai.llm_client import OllamaClient
from ted_ai.methodology_loader import get_knowledge_base
from ted_ai.prompt_engine import (
    build_selection_prompt, parse_selection_response,
    build_analysis_prompt, parse_response, AnalysisResult
)

logger = logging.getLogger(__name__)


class ReasoningEngine:
    def __init__(self, api_endpoint: str = "http://localhost:11434", ai_model: Optional[str] = None):
        self.model = ai_model or "qwen3.5:9b"
        self.llm = OllamaClient(endpoint=api_endpoint, model=self.model)
        self.kb = get_knowledge_base()

    def analyze_engagement(self, context: Dict[str, Any]) -> AnalysisResult:
        evidence = context.get("evidence", [])

        # --- Call 1: select relevant domain(s) + lifecycle stage ---
        domains = self.kb.get_selectable_domains()
        if not domains:
            raise RuntimeError("No domain methodology files loaded — check knowledge/methodologies/")

        selection_prompt = build_selection_prompt(evidence, domains)
        logger.info("Sending domain-selection prompt")
        selection_raw = self.llm.generate(selection_prompt, temperature=0.1)
        selection = parse_selection_response(selection_raw, valid_domains=list(domains.keys()))

        logger.info(f"Selected domains: {selection.domains} | stage: {selection.stage} | reasoning: {selection.reasoning}")

        # --- Build methodology content from selected domain(s) ---
        if selection.domains:
            content_parts = [self.kb.get_domain_content(d) for d in selection.domains]
            methodology_content = "\n\n---\n\n".join(content_parts)
        else:
            methodology_content = ""

        # --- Call 2: grounded analysis ---
        analysis_prompt = build_analysis_prompt(selection.stage, evidence, methodology_content)
        logger.info(f"Sending analysis prompt | domains={selection.domains} | evidence_count={len(evidence)}")
        analysis_raw = self.llm.generate(analysis_prompt, temperature=0.3)

        result = parse_response(analysis_raw)
        result.selected_domains = selection.domains
        result.phase_name = selection.stage
        return result

    def ask(self, question: str, context: Dict[str, Any]) -> str:
        """Ad-hoc direct question — reuses domain selection for grounding."""
        evidence = context.get("evidence", [])
        domains = self.kb.get_selectable_domains()

        selection_prompt = build_selection_prompt(evidence, domains)
        selection_raw = self.llm.generate(selection_prompt, temperature=0.1)
        selection = parse_selection_response(selection_raw, valid_domains=list(domains.keys()))

        methodology_content = "\n\n---\n\n".join(
            self.kb.get_domain_content(d) for d in selection.domains
        ) if selection.domains else "(no specific domain matched)"

        evidence_lines = "\n".join(
            f"- [{ev.get('evidence_type')}] {ev.get('title')}: {ev.get('description')}"
            for ev in evidence
        ) or "(no evidence collected yet)"

        prompt = f"""You are a penetration testing mentor. The user asked a direct question about their engagement.

EVIDENCE SO FAR:
{evidence_lines}

RELEVANT METHODOLOGY:
{methodology_content}

USER QUESTION: {question}

Answer specifically using the evidence and methodology above. If there isn't enough to answer, say exactly what's missing. Do not give generic advice."""

        return self.llm.generate(prompt)