"""
Ted-AI Database Models and Schemas

Enhanced data models using SQLAlchemy ORM with comprehensive 
relationship management and validation.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from sqlalchemy import (
    Column, String, Integer, Text, DateTime, Float, Boolean, 
    ForeignKey, JSON, Enum as SQLEnum, Table, Index, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from dataclasses import dataclass, asdict, field
import json

Base = declarative_base()


class SeverityLevel(str, Enum):
    """Finding severity classification"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class EngagementStatus(str, Enum):
    """Engagement lifecycle status"""
    PLANNING = "planning"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CLOSED = "closed"


class EvidenceType(str, Enum):
    """Classification of evidence collected"""
    HTTP_REQUEST = "http_request"
    HTTP_RESPONSE = "http_response"
    ENDPOINT_DISCOVERY = "endpoint_discovery"
    RECONNAISSANCE = "reconnaissance"
    CODE_ANALYSIS = "code_analysis"
    DATABASE_QUERY = "database_query"
    SCREENSHOT = "screenshot"
    NETWORK_TRACE = "network_trace"
    LOG_ENTRY = "log_entry"
    NOTES = "notes"


class Engagement(Base):
    """
    Represents a complete bug bounty or penetration testing engagement.
    Central entity that tracks the overall assessment scope and status.
    """
    __tablename__ = "engagements"
    __table_args__ = ()

    id = Column(Integer, primary_key=True)
    target_name = Column(String(255), nullable=False, unique=True)
    target_url = Column(String(512), nullable=True)
    target_type = Column(String(50), nullable=False)  # web_app, api, mobile, network, etc.
    
    # Status tracking
    status = Column(SQLEnum(EngagementStatus), default=EngagementStatus.PLANNING)
    scope = Column(Text, nullable=True)  # Detailed scope definition
    out_of_scope = Column(Text, nullable=True)  # Out-of-scope items
    
    # Metadata
    client_name = Column(String(255), nullable=True)
    penetration_tester = Column(String(255), nullable=True)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    
    # Environment details
    technology_stack = Column(JSON, default=dict)  # {framework, language, database, etc.}
    known_vulnerabilities = Column(JSON, default=list)
    remediation_notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    objectives = relationship("Objective", back_populates="engagement", cascade="all, delete-orphan")
    evidence = relationship("Evidence", back_populates="engagement", cascade="all, delete-orphan")
    findings = relationship("Finding", back_populates="engagement", cascade="all, delete-orphan")
    hypotheses = relationship("Hypothesis", back_populates="engagement", cascade="all, delete-orphan")
    session_logs = relationship("SessionLog", back_populates="engagement", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Engagement(id={self.id}, target={self.target_name}, status={self.status})>"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "target_name": self.target_name,
            "target_url": self.target_url,
            "target_type": self.target_type,
            "status": self.status.value,
            "scope": self.scope,
            "client": self.client_name,
            "tester": self.penetration_tester,
            "technology_stack": self.technology_stack,
            "objectives_count": len(self.objectives),
            "evidence_count": len(self.evidence),
            "findings_count": len(self.findings),
        }


class Objective(Base):
    """
    Represents a testing objective within an engagement.
    Objectives help focus and track progress toward specific goals.
    """
    __tablename__ = "objectives"
    __table_args__ = (
        Index('idx_objective_engagement_id', 'engagement_id'),
        Index('idx_priority', 'priority'),
    )

    id = Column(Integer, primary_key=True)
    engagement_id = Column(Integer, ForeignKey("engagements.id"), nullable=False)
    
    # Objective definition
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    objective_type = Column(String(50), nullable=False)  # vulnerability, reconnaissance, auth_bypass, etc.
    
    # Progress tracking
    priority = Column(Integer, default=1)  # 1 = highest
    status = Column(String(20), default="active")  # active, completed, rejected, deprioritized
    progress_percentage = Column(Float, default=0.0)
    
    # Context
    testing_strategy = Column(Text, nullable=True)
    attack_vectors = Column(JSON, default=list)
    rejected_hypotheses = Column(JSON, default=list)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    engagement = relationship("Engagement", back_populates="objectives")
    evidence_items = relationship("Evidence", back_populates="objective")
    related_findings = relationship("Finding", back_populates="primary_objective")

    def mark_completed(self):
        self.status = "completed"
        self.completed_at = datetime.utcnow()
        self.progress_percentage = 100.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "type": self.objective_type,
            "status": self.status,
            "priority": self.priority,
            "progress": self.progress_percentage,
            "evidence_count": len(self.evidence_items),
        }


class Evidence(Base):
    """
    Represents factual observations and data collected during testing.
    Evidence is raw data that supports or refutes hypotheses.
    """
    __tablename__ = "evidence"
    __table_args__ = (
        Index('idx_engagement_objective', 'engagement_id', 'objective_id'),
        Index('idx_evidence_type', 'evidence_type'),
        Index('idx_confidence', 'confidence_level'),
    )

    id = Column(Integer, primary_key=True)
    engagement_id = Column(Integer, ForeignKey("engagements.id"), nullable=False)
    objective_id = Column(Integer, ForeignKey("objectives.id"), nullable=True)
    
    # Evidence classification
    evidence_type = Column(SQLEnum(EvidenceType), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    
    # Data and context
    raw_data = Column(JSON, nullable=True)
    source = Column(String(255), nullable=True)  # endpoint, tool, manual observation
    artifacts = Column(JSON, default=list)  # file references, screenshots
    
    # Analysis metadata
    confidence_level = Column(Float, default=0.5)  # 0.0 to 1.0
    affected_endpoint = Column(String(512), nullable=True)
    affected_parameters = Column(JSON, default=list)
    impact_description = Column(Text, nullable=True)
    
    # Relationships to findings and hypotheses
    related_finding_id = Column(Integer, ForeignKey("findings.id"), nullable=True)
    related_hypotheses = relationship("Hypothesis", secondary="evidence_hypothesis")
    
    # Timestamps
    collected_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    engagement = relationship("Engagement", back_populates="evidence")
    objective = relationship("Objective", back_populates="evidence_items")
    related_finding = relationship("Finding", back_populates="supporting_evidence")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.evidence_type.value,
            "title": self.title,
            "source": self.source,
            "confidence": self.confidence_level,
            "endpoint": self.affected_endpoint,
            "collected_at": self.collected_at.isoformat() if self.collected_at else None,
        }


# Association table for Evidence-Hypothesis relationship
evidence_hypothesis = Table(
    'evidence_hypothesis',
    Base.metadata,
    Column('evidence_id', Integer, ForeignKey('evidence.id'), primary_key=True),
    Column('hypothesis_id', Integer, ForeignKey('hypotheses.id'), primary_key=True)
)


class Hypothesis(Base):
    """
    Represents a testable theory about potential vulnerabilities.
    Hypotheses guide testing activities and get validated or rejected.
    """
    __tablename__ = "hypotheses"
    __table_args__ = (
        Index('idx_hypothesis_engagement_id', 'engagement_id'),
        Index('idx_status', 'status'),
    )

    id = Column(Integer, primary_key=True)
    engagement_id = Column(Integer, ForeignKey("engagements.id"), nullable=False)
    
    # Hypothesis definition
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    hypothesis_type = Column(String(100), nullable=False)  # vulnerability_type, attack_chain, privilege_escalation
    
    # Vulnerability classification
    affected_component = Column(String(255), nullable=True)
    attack_vector = Column(String(255), nullable=True)
    required_privileges = Column(String(100), nullable=True)
    estimated_impact = Column(String(255), nullable=True)
    
    # Status and validation
    status = Column(String(20), default="pending")  # pending, in_progress, validated, rejected
    confidence_score = Column(Float, default=0.0)  # Based on supporting evidence
    validation_notes = Column(Text, nullable=True)
    
    # Testing guidance
    testing_approach = Column(Text, nullable=True)
    tools_recommended = Column(JSON, default=list)
    estimated_effort = Column(String(20), nullable=True)  # low, medium, high, critical_path
    
    # Relationships
    supporting_evidence = relationship("Evidence", secondary=evidence_hypothesis, overlaps="related_hypotheses", back_populates="related_hypotheses")
    related_finding = relationship("Finding", back_populates="validated_hypothesis")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    engagement = relationship("Engagement", back_populates="hypotheses")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "type": self.hypothesis_type,
            "status": self.status,
            "confidence": self.confidence_score,
            "affected_component": self.affected_component,
            "evidence_count": len(self.supporting_evidence),
        }


class Finding(Base):
    """
    Represents confirmed vulnerabilities and security issues.
    Findings are derived from evidence and hypotheses validation.
    """
    __tablename__ = "findings"
    __table_args__ = (
        Index('idx_findings_engagement_severity', 'engagement_id', 'severity'),
        Index('idx_findings_status', 'status'),
    )

    id = Column(Integer, primary_key=True)
    engagement_id = Column(Integer, ForeignKey("engagements.id"), nullable=False)
    primary_objective_id = Column(Integer, ForeignKey("objectives.id"), nullable=True)
    validated_hypothesis_id = Column(Integer, ForeignKey("hypotheses.id"), nullable=True)
    
    # Finding classification
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    finding_type = Column(String(100), nullable=False)  # vulnerability_type
    cwe_id = Column(String(20), nullable=True)
    cve_id = Column(String(20), nullable=True)
    
    # Severity and impact
    severity = Column(SQLEnum(SeverityLevel), default=SeverityLevel.MEDIUM)
    cvss_score = Column(Float, nullable=True)
    impact_description = Column(Text, nullable=False)
    affected_endpoints = Column(JSON, default=list)
    
    # Remediation
    remediation_guidance = Column(Text, nullable=True)
    remediation_effort = Column(String(20), nullable=True)  # low, medium, high
    prevention_techniques = Column(JSON, default=list)
    
    # Status and reporting
    status = Column(String(20), default="confirmed")  # confirmed, false_positive, duplicate, in_remediation
    report_ready = Column(Boolean, default=False)
    report_notes = Column(Text, nullable=True)
    
    # Proof of concept
    proof_of_concept = Column(Text, nullable=True)
    reproduction_steps = Column(JSON, default=list)
    
    # Relationships
    engagement = relationship("Engagement", back_populates="findings")
    primary_objective = relationship("Objective", back_populates="related_findings")
    validated_hypothesis = relationship("Hypothesis", back_populates="related_finding")
    supporting_evidence = relationship("Evidence", back_populates="related_finding")
    
    # Timestamps
    discovered_at = Column(DateTime, default=datetime.utcnow)
    confirmed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def mark_confirmed(self):
        self.status = "confirmed"
        self.confirmed_at = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "type": self.finding_type,
            "severity": self.severity.value,
            "cvss": self.cvss_score,
            "status": self.status,
            "cwe": self.cwe_id,
            "cve": self.cve_id,
            "endpoints": self.affected_endpoints,
        }


class SessionLog(Base):
    """
    Tracks AI reasoning sessions and important decisions.
    Provides audit trail and learning from previous analyses.
    """
    __tablename__ = "session_logs"
    __table_args__ = (
        Index('idx_session_logs_engagement_session', 'engagement_id', 'session_date'),
    )

    id = Column(Integer, primary_key=True)
    engagement_id = Column(Integer, ForeignKey("engagements.id"), nullable=False)
    
    # Session metadata
    session_id = Column(String(100), unique=True)
    session_type = Column(String(50), nullable=False)  # analysis, recommendation, research, report
    
    # Context
    context_summary = Column(Text, nullable=True)
    objectives_considered = Column(JSON, default=list)
    evidence_analyzed = Column(JSON, default=list)
    findings_reviewed = Column(JSON, default=list)
    
    # AI reasoning
    ai_model_used = Column(String(50), nullable=True)
    reasoning_tokens_used = Column(Integer, default=0)
    reasoning_output = Column(Text, nullable=True)
    
    # Recommendations
    recommended_actions = Column(JSON, default=list)
    recommended_priority = Column(Integer, nullable=True)
    
    # Evaluation
    user_feedback = Column(String(20), nullable=True)  # useful, partially_useful, not_useful
    feedback_notes = Column(Text, nullable=True)
    
    # Timestamps
    session_date = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    engagement = relationship("Engagement", back_populates="session_logs")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "session_id": self.session_id,
            "type": self.session_type,
            "model": self.ai_model_used,
            "actions_recommended": len(self.recommended_actions),
            "feedback": self.user_feedback,
            "session_date": self.session_date.isoformat(),
        }


@dataclass
class EngagementSummary:
    """Aggregated engagement state for quick reference"""
    engagement_id: int
    target_name: str
    status: str
    total_objectives: int
    completed_objectives: int
    total_evidence: int
    total_findings: int
    critical_findings: int
    high_findings: int
    pending_hypotheses: int
    last_updated: datetime

    def progress_percentage(self) -> float:
        if self.total_objectives == 0:
            return 0.0
        return (self.completed_objectives / self.total_objectives) * 100