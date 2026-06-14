"""
Ted-AI Database Layer

Sophisticated database management with connection pooling,
query optimization, and comprehensive state management.
"""

import logging
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any, Generator
import json

from sqlalchemy import create_engine, event, func, desc
from sqlalchemy.orm import sessionmaker, Session, scoped_session
from sqlalchemy.pool import StaticPool, QueuePool

from ted_ai.models import (
    Base, Engagement, Objective, Evidence, Finding, Hypothesis,
    SessionLog, EngagementSummary, EngagementStatus, SeverityLevel,
    EvidenceType
)

logger = logging.getLogger(__name__)


class DatabaseConfig:
    """Configuration for database connections"""
    def __init__(
        self,
        db_path: str = "ted_ai.db",
        echo_sql: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
        timeout: int = 30,
    ):
        self.db_path = db_path
        self.echo_sql = echo_sql
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self.timeout = timeout

    @property
    def connection_string(self) -> str:
        return f"sqlite:///{self.db_path}"


class DatabaseManager:
    """
    Sophisticated database manager with connection pooling,
    transaction management, and query optimization.
    """

    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.engine = self._create_engine()
        self.SessionLocal = scoped_session(sessionmaker(
            bind=self.engine,
            expire_on_commit=False
        ))
        self._init_database()

    def _create_engine(self):
        """Create SQLAlchemy engine with optimized pool settings"""
        if self.config.db_path == ":memory:":
            return create_engine(
                "sqlite:///:memory:",
                echo=self.config.echo_sql,
                connect_args={"timeout": self.config.timeout},
                poolclass=StaticPool,
            )
        else:
            return create_engine(
                self.config.connection_string,
                echo=self.config.echo_sql,
                connect_args={"timeout": self.config.timeout},
                pool_size=self.config.pool_size,
                max_overflow=self.config.max_overflow,
                pool_pre_ping=True,
            )

    def _init_database(self):
        """Initialize database schema"""
        # Enable foreign keys for SQLite
        def enable_fk(dbapi_conn, connection_record):
            cursor = dbapi_conn.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

        event.listen(self.engine, "connect", enable_fk)
        
        # Create all tables
        Base.metadata.create_all(self.engine)
        logger.info(f"Database initialized at {self.config.db_path}")

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """Context manager for database sessions with automatic cleanup"""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database error: {str(e)}")
            raise
        finally:
            session.close()

    # ==================== Engagement Operations ====================

    def create_engagement(
        self,
        target_name: str,
        target_type: str,
        target_url: Optional[str] = None,
        scope: Optional[str] = None,
        technology_stack: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Engagement:
        """Create a new engagement"""
        with self.get_session() as session:
            engagement = Engagement(
                target_name=target_name,
                target_type=target_type,
                target_url=target_url,
                scope=scope,
                technology_stack=technology_stack or {},
                **kwargs
            )
            session.add(engagement)
            session.flush()
            engagement_id = engagement.id
            logger.info(f"Created engagement: {target_name} (ID: {engagement_id})")
            return engagement

    def get_engagement(self, engagement_id: int) -> Optional[Engagement]:
        """Retrieve engagement by ID"""
        with self.get_session() as session:
            return session.query(Engagement).filter(
                Engagement.id == engagement_id
            ).first()

    def get_engagement_by_target(self, target_name: str) -> Optional[Engagement]:
        """Retrieve engagement by target name"""
        with self.get_session() as session:
            return session.query(Engagement).filter(
                Engagement.target_name == target_name
            ).first()

    def get_all_engagements(self, status: Optional[EngagementStatus] = None) -> List[Engagement]:
        """Get all engagements, optionally filtered by status"""
        with self.get_session() as session:
            query = session.query(Engagement)
            if status:
                query = query.filter(Engagement.status == status)
            return query.order_by(desc(Engagement.created_at)).all()

    def get_engagement_summary(self, engagement_id: int) -> Optional[EngagementSummary]:
        """Get aggregated engagement metrics"""
        with self.get_session() as session:
            engagement = session.query(Engagement).filter(
                Engagement.id == engagement_id
            ).first()
            
            if not engagement:
                return None

            total_objectives = len(engagement.objectives)
            completed_objectives = sum(
                1 for obj in engagement.objectives if obj.status == "completed"
            )
            
            critical_findings = sum(
                1 for f in engagement.findings if f.severity == SeverityLevel.CRITICAL
            )
            high_findings = sum(
                1 for f in engagement.findings if f.severity == SeverityLevel.HIGH
            )
            
            pending_hypotheses = sum(
                1 for h in engagement.hypotheses if h.status == "pending"
            )

            return EngagementSummary(
                engagement_id=engagement.id,
                target_name=engagement.target_name,
                status=engagement.status.value,
                total_objectives=total_objectives,
                completed_objectives=completed_objectives,
                total_evidence=len(engagement.evidence),
                total_findings=len(engagement.findings),
                critical_findings=critical_findings,
                high_findings=high_findings,
                pending_hypotheses=pending_hypotheses,
                last_updated=engagement.updated_at,
            )

    # ==================== Objective Operations ====================

    def create_objective(
        self,
        engagement_id: int,
        title: str,
        description: str,
        objective_type: str,
        priority: int = 1,
        **kwargs
    ) -> Objective:
        """Create a new testing objective"""
        with self.get_session() as session:
            objective = Objective(
                engagement_id=engagement_id,
                title=title,
                description=description,
                objective_type=objective_type,
                priority=priority,
                **kwargs
            )
            session.add(objective)
            session.flush()
            logger.info(f"Created objective: {title} in engagement {engagement_id}")
            return objective

    def get_objective(self, objective_id: int) -> Optional[Objective]:
        """Retrieve objective by ID"""
        with self.get_session() as session:
            return session.query(Objective).filter(
                Objective.id == objective_id
            ).first()

    def get_engagement_objectives(
        self,
        engagement_id: int,
        status: Optional[str] = None
    ) -> List[Objective]:
        """Get all objectives for an engagement"""
        with self.get_session() as session:
            query = session.query(Objective).filter(
                Objective.engagement_id == engagement_id
            )
            if status:
                query = query.filter(Objective.status == status)
            return query.order_by(Objective.priority).all()

    # ==================== Evidence Operations ====================

    def add_evidence(
        self,
        engagement_id: int,
        evidence_type: EvidenceType,
        title: str,
        description: str,
        objective_id: Optional[int] = None,
        raw_data: Optional[Dict[str, Any]] = None,
        confidence_level: float = 0.5,
        **kwargs
    ) -> Evidence:
        """Add evidence to engagement"""
        with self.get_session() as session:
            evidence = Evidence(
                engagement_id=engagement_id,
                objective_id=objective_id,
                evidence_type=evidence_type,
                title=title,
                description=description,
                raw_data=raw_data or {},
                confidence_level=confidence_level,
                **kwargs
            )
            session.add(evidence)
            session.flush()
            logger.info(
                f"Added evidence: {title} "
                f"(confidence: {confidence_level}) to engagement {engagement_id}"
            )
            return evidence

    def get_evidence(self, evidence_id: int) -> Optional[Evidence]:
        """Retrieve evidence by ID"""
        with self.get_session() as session:
            return session.query(Evidence).filter(
                Evidence.id == evidence_id
            ).first()

    def get_engagement_evidence(
        self,
        engagement_id: int,
        evidence_type: Optional[EvidenceType] = None,
        min_confidence: float = 0.0
    ) -> List[Evidence]:
        """Get evidence for engagement with optional filtering"""
        with self.get_session() as session:
            query = session.query(Evidence).filter(
                Evidence.engagement_id == engagement_id,
                Evidence.confidence_level >= min_confidence
            )
            if evidence_type:
                query = query.filter(Evidence.evidence_type == evidence_type)
            return query.order_by(desc(Evidence.confidence_level)).all()

    def get_endpoint_evidence(
        self,
        engagement_id: int,
        endpoint: str
    ) -> List[Evidence]:
        """Get all evidence related to a specific endpoint"""
        with self.get_session() as session:
            return session.query(Evidence).filter(
                Evidence.engagement_id == engagement_id,
                Evidence.affected_endpoint == endpoint
            ).all()

    # ==================== Hypothesis Operations ====================

    def create_hypothesis(
        self,
        engagement_id: int,
        title: str,
        description: str,
        hypothesis_type: str,
        affected_component: Optional[str] = None,
        attack_vector: Optional[str] = None,
        **kwargs
    ) -> Hypothesis:
        """Create a testable hypothesis"""
        with self.get_session() as session:
            hypothesis = Hypothesis(
                engagement_id=engagement_id,
                title=title,
                description=description,
                hypothesis_type=hypothesis_type,
                affected_component=affected_component,
                attack_vector=attack_vector,
                **kwargs
            )
            session.add(hypothesis)
            session.flush()
            logger.info(f"Created hypothesis: {title} in engagement {engagement_id}")
            return hypothesis

    def get_hypothesis(self, hypothesis_id: int) -> Optional[Hypothesis]:
        """Retrieve hypothesis by ID"""
        with self.get_session() as session:
            return session.query(Hypothesis).filter(
                Hypothesis.id == hypothesis_id
            ).first()

    def get_engagement_hypotheses(
        self,
        engagement_id: int,
        status: Optional[str] = None
    ) -> List[Hypothesis]:
        """Get hypotheses for engagement"""
        with self.get_session() as session:
            query = session.query(Hypothesis).filter(
                Hypothesis.engagement_id == engagement_id
            )
            if status:
                query = query.filter(Hypothesis.status == status)
            return query.order_by(
                desc(Hypothesis.confidence_score),
                Hypothesis.created_at
            ).all()

    def update_hypothesis_status(
        self,
        hypothesis_id: int,
        status: str,
        confidence_score: Optional[float] = None,
        validation_notes: Optional[str] = None
    ):
        """Update hypothesis validation status"""
        with self.get_session() as session:
            hypothesis = session.query(Hypothesis).filter(
                Hypothesis.id == hypothesis_id
            ).first()
            if hypothesis:
                hypothesis.status = status
                if confidence_score is not None:
                    hypothesis.confidence_score = confidence_score
                if validation_notes:
                    hypothesis.validation_notes = validation_notes
                hypothesis.updated_at = datetime.utcnow()
                logger.info(f"Updated hypothesis {hypothesis_id} status to {status}")

    # ==================== Finding Operations ====================

    def create_finding(
        self,
        engagement_id: int,
        title: str,
        description: str,
        finding_type: str,
        severity: SeverityLevel,
        impact_description: str,
        objective_id: Optional[int] = None,
        **kwargs
    ) -> Finding:
        """Create a confirmed finding"""
        with self.get_session() as session:
            finding = Finding(
                engagement_id=engagement_id,
                title=title,
                description=description,
                finding_type=finding_type,
                severity=severity,
                impact_description=impact_description,
                primary_objective_id=objective_id,
                **kwargs
            )
            finding.mark_confirmed()
            session.add(finding)
            session.flush()
            logger.info(
                f"Created finding: {title} "
                f"(severity: {severity.value}) in engagement {engagement_id}"
            )
            return finding

    def get_finding(self, finding_id: int) -> Optional[Finding]:
        """Retrieve finding by ID"""
        with self.get_session() as session:
            return session.query(Finding).filter(
                Finding.id == finding_id
            ).first()

    def get_engagement_findings(
        self,
        engagement_id: int,
        severity: Optional[SeverityLevel] = None,
        status: Optional[str] = None,
        report_ready_only: bool = False
    ) -> List[Finding]:
        """Get findings for engagement with filtering"""
        with self.get_session() as session:
            query = session.query(Finding).filter(
                Finding.engagement_id == engagement_id
            )
            if severity:
                query = query.filter(Finding.severity == severity)
            if status:
                query = query.filter(Finding.status == status)
            if report_ready_only:
                query = query.filter(Finding.report_ready == True)
            
            return query.order_by(
                Finding.severity,
                desc(Finding.confirmed_at)
            ).all()

    def get_critical_findings(self, engagement_id: int) -> List[Finding]:
        """Get all critical severity findings"""
        return self.get_engagement_findings(
            engagement_id,
            severity=SeverityLevel.CRITICAL
        )

    def get_high_findings(self, engagement_id: int) -> List[Finding]:
        """Get all high severity findings"""
        return self.get_engagement_findings(
            engagement_id,
            severity=SeverityLevel.HIGH
        )

    # ==================== Session Operations ====================

    def log_session(
        self,
        engagement_id: int,
        session_id: str,
        session_type: str,
        ai_model_used: Optional[str] = None,
        recommended_actions: Optional[List[str]] = None,
        **kwargs
    ) -> SessionLog:
        """Log an AI reasoning session"""
        with self.get_session() as session:
            log = SessionLog(
                engagement_id=engagement_id,
                session_id=session_id,
                session_type=session_type,
                ai_model_used=ai_model_used,
                recommended_actions=recommended_actions or [],
                **kwargs
            )
            session.add(log)
            session.flush()
            return log

    def get_session_logs(
        self,
        engagement_id: int,
        session_type: Optional[str] = None,
        limit: int = 10
    ) -> List[SessionLog]:
        """Get recent session logs"""
        with self.get_session() as session:
            query = session.query(SessionLog).filter(
                SessionLog.engagement_id == engagement_id
            )
            if session_type:
                query = query.filter(SessionLog.session_type == session_type)
            
            return query.order_by(
                desc(SessionLog.session_date)
            ).limit(limit).all()

    # ==================== Statistics ====================

    def get_engagement_statistics(self, engagement_id: int) -> Dict[str, Any]:
        """Get comprehensive engagement statistics"""
        summary = self.get_engagement_summary(engagement_id)
        if not summary:
            return {}

        with self.get_session() as session:
            engagement = session.query(Engagement).filter(
                Engagement.id == engagement_id
            ).first()

            if not engagement:
                return {}

            # Calculate severity distribution
            severity_dist = {}
            for severity in SeverityLevel:
                count = session.query(func.count(Finding.id)).filter(
                    Finding.engagement_id == engagement_id,
                    Finding.severity == severity
                ).scalar()
                severity_dist[severity.value] = count

            return {
                "target": engagement.target_name,
                "status": summary.status,
                "progress": summary.progress_percentage(),
                "objectives": {
                    "total": summary.total_objectives,
                    "completed": summary.completed_objectives,
                },
                "findings": {
                    "total": summary.total_findings,
                    "critical": summary.critical_findings,
                    "high": summary.high_findings,
                    "by_severity": severity_dist,
                },
                "evidence": {
                    "total": summary.total_evidence,
                },
                "hypotheses": {
                    "pending": summary.pending_hypotheses,
                },
            }

    def close(self):
        """Close database connections"""
        self.SessionLocal.remove()
        self.engine.dispose()
        logger.info("Database connections closed")