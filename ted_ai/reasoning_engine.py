"""
Ted-AI Reasoning Engine

Sophisticated multi-agent reasoning system for contextual analysis,
hypothesis generation, and intelligent recommendations.
"""

import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import List, Dict, Any, Optional, Tuple
from uuid import uuid4

logger = logging.getLogger(__name__)


class RecommendationType(str, Enum):
    """Types of recommendations the system can generate"""
    NEXT_TEST = "next_test"
    EVIDENCE_ANALYSIS = "evidence_analysis"
    HYPOTHESIS_VALIDATION = "hypothesis_validation"
    PRIORITY_SHIFT = "priority_shift"
    FINDING_CONFIRMATION = "finding_confirmation"
    REPORT_GUIDANCE = "report_guidance"


@dataclass
class RecommendedAction:
    """An actionable recommendation based on analysis"""
    action_type: RecommendationType
    title: str
    description: str
    priority: int  # 1 = highest
    effort_estimate: str  # low, medium, high, critical_path
    success_probability: float  # 0.0 to 1.0
    reasoning: str
    related_objective_id: Optional[int] = None
    related_evidence_ids: List[int] = None
    related_hypothesis_ids: List[int] = None
    estimated_impact: Optional[str] = None

    def __post_init__(self):
        if self.related_evidence_ids is None:
            self.related_evidence_ids = []
        if self.related_hypothesis_ids is None:
            self.related_hypothesis_ids = []


class ReasoningAgent(ABC):
    """
    Base class for specialized reasoning agents.
    Each agent has domain expertise in a specific area.
    """

    def __init__(self, agent_id: str, expertise: str):
        self.agent_id = agent_id
        self.expertise = expertise
        self.session_id = str(uuid4())

    @abstractmethod
    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Perform specialized analysis"""
        pass

    @abstractmethod
    def generate_recommendations(self, analysis: Dict[str, Any]) -> List[RecommendedAction]:
        """Generate actionable recommendations from analysis"""
        pass


class EvidenceAnalysisAgent(ReasoningAgent):
    """
    Analyzes collected evidence to identify patterns,
    confidence levels, and knowledge gaps.
    """

    def __init__(self):
        super().__init__("evidence_analyzer", "Evidence Pattern Recognition")

    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze evidence patterns in engagement context
        
        Args:
            context: Contains engagement, objectives, evidence, hypotheses
        
        Returns:
            Analysis results with patterns and insights
        """
        evidence_list = context.get("evidence", [])
        
        # Convert dict evidence to objects for analysis
        evidence_items = []
        for ev in evidence_list:
            if isinstance(ev, dict):
                # Map 'type' to 'evidence_type' if needed
                if 'type' in ev and 'evidence_type' not in ev:
                    ev['evidence_type'] = ev.pop('type')
                # Create proper fields, use defaults if missing ones
                evidence_items.append(EvidenceItem(
                    id=ev.get("id", 0),
                    evidence_type=ev.get("evidence_type", "notes"),
                    confidence_level=ev.get("confidence_level", 0.5),
                    title=ev.get("title"),
                    description=ev.get("description"),
                    affected_endpoint=ev.get("affected_endpoint"),
                    related_hypotheses=ev.get("related_hypotheses", [])
                ))
            else:
                evidence_items.append(ev)

        analysis = {
            "total_evidence": len(evidence_items),
            "confidence_distribution": self._analyze_confidence(evidence_items),
            "evidence_gaps": self._identify_gaps(evidence_items),
            "endpoint_coverage": self._analyze_endpoint_coverage(evidence_items),
            "evidence_clustering": self._cluster_evidence(evidence_items),
            "high_confidence_evidence": self._get_high_confidence(evidence_items),
            "contradictions": self._find_contradictions(evidence_items),
        }

        return analysis

    def _analyze_confidence(self, evidence: List["EvidenceItem"]) -> Dict[str, int]:
        """Analyze confidence level distribution"""
        distribution = {"high": 0, "medium": 0, "low": 0}
        for ev in evidence:
            confidence = getattr(ev, "confidence_level", 0.5)
            if confidence >= 0.7:
                distribution["high"] += 1
            elif confidence >= 0.4:
                distribution["medium"] += 1
            else:
                distribution["low"] += 1
        return distribution

    def _identify_gaps(self, evidence: List["EvidenceItem"]) -> List[str]:
        """Identify missing evidence types"""
        gaps = []
        evidence_types = set(
            getattr(ev, "evidence_type", None) for ev in evidence
        )
        
        needed_types = {
            "http_request", "http_response", "endpoint_discovery",
            "code_analysis", "database_query"
        }
        
        missing = needed_types - evidence_types
        if missing:
            gaps = [f"No {ev_type} evidence collected" for ev_type in missing]
        
        return gaps

    def _analyze_endpoint_coverage(self, evidence: List["EvidenceItem"]) -> Dict[str, int]:
        """Analyze how many endpoints have been tested"""
        endpoints = {}
        for ev in evidence:
            endpoint = getattr(ev, "affected_endpoint", None)
            if endpoint:
                endpoints[endpoint] = endpoints.get(endpoint, 0) + 1
        return endpoints

    def _cluster_evidence(self, evidence: List["EvidenceItem"]) -> Dict[str, List[int]]:
        """Cluster evidence by type"""
        clusters = {}
        for ev in evidence:
            ev_type = getattr(ev, "evidence_type", "unknown")
            if ev_type not in clusters:
                clusters[ev_type] = []
            ev_id = getattr(ev, "id", None)
            if ev_id:
                clusters[ev_type].append(ev_id)
        return clusters

    def _get_high_confidence(self, evidence: List["EvidenceItem"]) -> List[int]:
        """Get IDs of high-confidence evidence"""
        high_conf = []
        for ev in evidence:
            confidence = getattr(ev, "confidence_level", 0)
            ev_id = getattr(ev, "id", None)
            if confidence >= 0.8 and ev_id:
                high_conf.append(ev_id)
        return high_conf

    def _find_contradictions(self, evidence: List["EvidenceItem"]) -> List[str]:
        """Identify contradictory evidence"""
        contradictions = []
        # Simple contradiction detection based on notes/descriptions
        # More sophisticated analysis would compare endpoint responses
        return contradictions

    def generate_recommendations(self, analysis: Dict[str, Any]) -> List[RecommendedAction]:
        """Generate evidence-focused recommendations"""
        recommendations = []

        # If there are evidence gaps, recommend collection
        if analysis.get("evidence_gaps"):
            recommendations.append(RecommendedAction(
                action_type=RecommendationType.EVIDENCE_ANALYSIS,
                title="Collect Missing Evidence Types",
                description="The following evidence types are missing: " + 
                            ", ".join(analysis["evidence_gaps"]),
                priority=2,
                effort_estimate="medium",
                success_probability=0.8,
                reasoning="Evidence collection gaps may limit hypothesis validation"
            ))

        # If endpoint coverage is low, recommend more testing
        endpoints = analysis.get("endpoint_coverage", {})
        if len(endpoints) < 5:
            recommendations.append(RecommendedAction(
                action_type=RecommendationType.NEXT_TEST,
                title="Expand Endpoint Coverage",
                description=f"Currently testing {len(endpoints)} endpoints. "
                            "Consider testing additional endpoints.",
                priority=3,
                effort_estimate="medium",
                success_probability=0.7,
                reasoning="Wider endpoint coverage increases vulnerability discovery"
            ))

        return recommendations


class HypothesisValidationAgent(ReasoningAgent):
    """
    Evaluates hypotheses based on supporting evidence
    and determines next validation steps.
    """

    def __init__(self):
        super().__init__("hypothesis_validator", "Hypothesis Validation")

    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze hypothesis validity based on evidence"""
        hypotheses = context.get("hypotheses", [])
        evidence = context.get("evidence", [])

        analysis = {
            "hypothesis_scores": self._score_hypotheses(hypotheses, evidence),
            "top_candidates": self._rank_hypotheses(hypotheses, evidence),
            "validation_readiness": self._assess_readiness(hypotheses, evidence),
            "contradicted_hypotheses": self._find_contradictions(hypotheses, evidence),
        }

        return analysis

    def _score_hypotheses(
        self,
        hypotheses: List[Dict[str, Any]],
        evidence: List[Dict[str, Any]]
    ) -> Dict[int, float]:
        """Score each hypothesis based on supporting evidence"""
        scores = {}
        for hyp in hypotheses:
            hyp_id = hyp.get("id")
            if not hyp_id:
                continue
            
            # Count supporting evidence
            supporting_count = 0
            for ev in evidence:
                related_hyp = ev.get("related_hypotheses", [])
                if hyp_id in related_hyp:
                    confidence = ev.get("confidence_level", 0)
                    supporting_count += confidence
            
            scores[hyp_id] = min(supporting_count, 1.0)
        
        return scores

    def _rank_hypotheses(
        self,
        hypotheses: List[Dict[str, Any]],
        evidence: List[Dict[str, Any]]
    ) -> List[Tuple[int, float]]:
        """Rank hypotheses by validation likelihood"""
        scores = self._score_hypotheses(hypotheses, evidence)
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]

    def _assess_readiness(
        self,
        hypotheses: List[Dict[str, Any]],
        evidence: List[Dict[str, Any]]
    ) -> Dict[int, bool]:
        """Determine if hypotheses are ready for validation"""
        readiness = {}
        for hyp in hypotheses:
            hyp_id = hyp.get("id")
            if hyp_id:
                # A hypothesis is ready if it has supporting evidence and testing approach
                has_evidence = any(
                    hyp_id in ev.get("related_hypotheses", [])
                    for ev in evidence
                )
                has_approach = bool(hyp.get("testing_approach"))
                readiness[hyp_id] = has_evidence and has_approach
        
        return readiness

    def _find_contradictions(
        self,
        hypotheses: List[Dict[str, Any]],
        evidence: List[Dict[str, Any]]
    ) -> List[int]:
        """Find hypotheses contradicted by evidence"""
        contradicted = []
        # More sophisticated analysis would look for evidence disproving hypotheses
        return contradicted

    def generate_recommendations(self, analysis: Dict[str, Any]) -> List[RecommendedAction]:
        """Generate hypothesis validation recommendations"""
        recommendations = []

        top_candidates = analysis.get("top_candidates", [])
        if top_candidates:
            top_id, score = top_candidates[0]
            recommendations.append(RecommendedAction(
                action_type=RecommendationType.HYPOTHESIS_VALIDATION,
                title=f"Validate Top Hypothesis (Score: {score:.2f})",
                description="The highest-scoring hypothesis has sufficient "
                            "supporting evidence for validation testing.",
                priority=1,
                effort_estimate="high",
                success_probability=score,
                reasoning="Evidence-based hypothesis scoring indicates high validation potential",
                related_hypothesis_ids=[top_id]
            ))

        return recommendations


class PriorityAgent(ReasoningAgent):
    """
    Determines testing priorities based on engagement state,
    severity, and efficiency metrics.
    """

    def __init__(self):
        super().__init__("priority_manager", "Priority Management")

    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze engagement state to determine priorities"""
        objectives = context.get("objectives", [])
        findings = context.get("findings", [])
        time_spent = context.get("time_spent_hours", 0)

        analysis = {
            "objective_priorities": self._prioritize_objectives(objectives),
            "critical_findings": len([f for f in findings if f.get("severity") == "critical"]),
            "effort_efficiency": self._calculate_efficiency(objectives, time_spent),
            "recommended_focus": self._determine_focus(objectives, findings),
        }

        return analysis

    def _prioritize_objectives(self, objectives: List[Dict[str, Any]]) -> List[int]:
        """Rank objectives by priority and completion status"""
        prioritized = sorted(
            objectives,
            key=lambda x: (x.get("status") != "completed", -x.get("priority", 999))
        )
        return [obj.get("id") for obj in prioritized[:5]]

    def _calculate_efficiency(self, objectives: List[Dict[str, Any]], hours: float) -> float:
        """Calculate testing efficiency (objectives per hour)"""
        if hours == 0:
            return 0
        completed = sum(1 for obj in objectives if obj.get("status") == "completed")
        return completed / hours if hours > 0 else 0

    def _determine_focus(
        self,
        objectives: List[Dict[str, Any]],
        findings: List[Dict[str, Any]]
    ) -> str:
        """Determine recommended testing focus area"""
        # If many critical findings, focus on remediation tracking
        critical = sum(1 for f in findings if f.get("severity") == "critical")
        if critical > 2:
            return "remediation_validation"
        
        # If objectives not started, focus on initial testing
        started = sum(1 for obj in objectives if obj.get("progress") > 0)
        if started < len(objectives) * 0.5:
            return "objective_coverage"
        
        # Otherwise, deep dive into existing findings
        return "finding_depth"

    def generate_recommendations(self, analysis: Dict[str, Any]) -> List[RecommendedAction]:
        """Generate priority-based recommendations"""
        recommendations = []

        focus = analysis.get("recommended_focus")
        if focus == "remediation_validation":
            recommendations.append(RecommendedAction(
                action_type=RecommendationType.PRIORITY_SHIFT,
                title="Shift Focus to Remediation Validation",
                description="Multiple critical findings discovered. Recommend "
                            "validating remediation efforts.",
                priority=1,
                effort_estimate="high",
                success_probability=0.9,
                reasoning="High critical finding count requires remediation tracking"
            ))

        return recommendations


class ReasoningEngine:
    """
    Orchestrates multiple reasoning agents to provide comprehensive
    analysis and intelligent recommendations.
    """

    def __init__(self, ai_model: Optional[str] = None):
        self.ai_model = ai_model or "local/qwen"
        self.agents: Dict[str, ReasoningAgent] = {
            "evidence": EvidenceAnalysisAgent(),
            "hypothesis": HypothesisValidationAgent(),
            "priority": PriorityAgent(),
        }
        self.session_history: List[Dict[str, Any]] = []

    def analyze_engagement(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive analysis of engagement using all agents
        
        Args:
            context: Current engagement state including objectives, evidence, etc.
        
        Returns:
            Comprehensive analysis from all agents
        """
        session_id = str(uuid4())
        analyses = {}

        # Run each agent
        for agent_name, agent in self.agents.items():
            try:
                analysis = agent.analyze(context)
                analyses[agent_name] = analysis
                logger.info(f"Agent {agent_name} completed analysis")
            except Exception as e:
                logger.error(f"Agent {agent_name} analysis failed: {str(e)}")
                analyses[agent_name] = {"error": str(e)}

        return {
            "session_id": session_id,
            "timestamp": datetime.utcnow().isoformat(),
            "analyses": analyses,
        }

    def generate_recommendations(
        self,
        context: Dict[str, Any],
        analysis: Optional[Dict[str, Any]] = None
    ) -> List[RecommendedAction]:
        """
        Generate actionable recommendations based on analysis
        
        Args:
            context: Current engagement state
            analysis: Optional pre-computed analysis (runs new if not provided)
        
        Returns:
            Prioritized list of recommended actions
        """
        if not analysis:
            analysis = self.analyze_engagement(context)

        all_recommendations: List[RecommendedAction] = []

        # Get recommendations from each agent
        for agent_name, agent in self.agents.items():
            agent_analysis = analysis.get("analyses", {}).get(agent_name, {})
            try:
                recommendations = agent.generate_recommendations(agent_analysis)
                all_recommendations.extend(recommendations)
            except Exception as e:
                logger.error(
                    f"Failed to get recommendations from {agent_name}: {str(e)}"
                )

        # Sort by priority
        all_recommendations.sort(key=lambda x: x.priority)

        return all_recommendations

    def evaluate_hypothesis(
        self,
        hypothesis: Dict[str, Any],
        supporting_evidence: List[Dict[str, Any]]
    ) -> float:
        """
        Evaluate hypothesis validity based on evidence
        
        Returns:
            Confidence score (0.0 to 1.0)
        """
        if not supporting_evidence:
            return 0.0

        # Aggregate confidence from evidence
        total_confidence = sum(
            ev.get("confidence_level", 0) for ev in supporting_evidence
        )
        avg_confidence = total_confidence / len(supporting_evidence)

        # Weight by evidence quality
        high_quality = sum(
            1 for ev in supporting_evidence
            if ev.get("confidence_level", 0) >= 0.7
        )
        quality_boost = min(0.2, high_quality * 0.1)

        return min(1.0, avg_confidence + quality_boost)


@dataclass
class EvidenceItem:
    """Helper dataclass for evidence"""
    id: int
    evidence_type: str
    confidence_level: float
    title: Optional[str] = None
    description: Optional[str] = None
    affected_endpoint: Optional[str] = None
    related_hypotheses: List[int] = None

    def __post_init__(self):
        if self.related_hypotheses is None:
            self.related_hypotheses = []