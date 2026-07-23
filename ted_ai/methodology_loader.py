"""
Methodology Loader - Loads raw methodology documents from knowledge base.
No structural parsing — files are passed to the LLM as-is so their
actual internal structure (phases, tables, examples) isn't lost.
"""

import logging
from pathlib import Path
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# Files that are reference lookups, not domain methodologies to select from
# during general analysis (e.g. used only when writing up a confirmed finding).
REFERENCE_ONLY = {"mitre_attack_methodology"}

# Short descriptions used during domain-selection — helps the LLM pick
# without needing to read full file content just to choose.
DOMAIN_DESCRIPTIONS = {
    "authentication_testing": "Login, registration, credentials, password reset, MFA, OAuth/SSO, session-at-login, API auth abuse.",
    "jwt_testing": "JWT-specific attack techniques: algorithm confusion, signature bypass, claim manipulation.",
    "session_testing": "Session management: token generation, rotation, expiration, fixation, hijacking.",
    "api_testing_methodology": "API-specific testing: endpoints, rate limiting, object-level authorization, API-specific input handling.",
    "web_testing_methodology": "Overall engagement lifecycle framework (objective -> recon -> discovery -> hypothesis -> validation -> evidence -> finding -> reporting). Always relevant as lifecycle context, not a selectable domain.",
}


class MethodologyKnowledgeBase:
    def __init__(self, knowledge_dir: str = "knowledge"):
        self.knowledge_dir = Path(knowledge_dir)
        self.documents: Dict[str, str] = {}  # filename stem -> raw content
        self._load_all()

    def _load_all(self):
        path = self.knowledge_dir / "methodologies"
        if not path.exists():
            logger.warning(f"Knowledge base not found at {path}")
            return

        for md_file in path.glob("*.md"):
            try:
                self.documents[md_file.stem] = md_file.read_text(encoding="utf-8")
                logger.info(f"Loaded methodology document: {md_file.stem}")
            except Exception as e:
                logger.error(f"Error loading {md_file}: {str(e)}")

    def get_lifecycle_document(self) -> str:
        """The overarching engagement lifecycle framework."""
        return self.documents.get("web_testing_methodology", "")

    def get_selectable_domains(self) -> Dict[str, str]:
        """Domain files eligible for selection, excluding lifecycle doc and reference-only files."""
        return {
            name: DOMAIN_DESCRIPTIONS.get(name, "")
            for name in self.documents
            if name != "web_testing_methodology" and name not in REFERENCE_ONLY
        }

    def get_domain_content(self, domain_name: str) -> str:
        return self.documents.get(domain_name, "")

    def get_reference_document(self, name: str) -> str:
        """For finding write-up: e.g. mitre_attack_methodology"""
        return self.documents.get(name, "")


_kb_instance: Optional[MethodologyKnowledgeBase] = None


def get_knowledge_base() -> MethodologyKnowledgeBase:
    global _kb_instance
    if _kb_instance is None:
        _kb_instance = MethodologyKnowledgeBase()
    return _kb_instance