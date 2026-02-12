"""
Audit Service - Comprehensive logging and tracking of all hiring decisions
Ensures transparency, compliance, and data-driven insights
"""
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, Optional, List
import json
from ..models.audit_log import AuditLog


class AuditService:
    """Service for tracking and logging all platform activities"""
    
    @staticmethod
    def log_application_evaluation(
        db: Session,
        application_id: int,
        job_id: int,
        candidate_id: int,
        scores: Dict,
        fraud_analysis: Dict,
        decision: str,
        decision_reason: str,
        explanation: Dict
    ) -> AuditLog:
        """
        Log a complete application evaluation
        
        Args:
            db: Database session
            application_id: ID of the application
            job_id: ID of the job
            candidate_id: ID of the candidate
            scores: All scoring metrics
            fraud_analysis: Fraud detection results
            decision: Final decision
            decision_reason: Reason for decision
            explanation: Detailed explanation
            
        Returns:
            Created audit log entry
        """
        audit_entry = AuditLog(
            event_type="application_evaluation",
            entity_type="application",
            entity_id=application_id,
            user_id=None,  # System-generated
            action="evaluate",
            details=json.dumps({
                "job_id": job_id,
                "candidate_id": candidate_id,
                "scores": scores,
                "fraud_analysis": fraud_analysis,
                "decision": decision,
                "decision_reason": decision_reason,
                "explanation": explanation
            }),
            ip_address=None,
            timestamp=datetime.utcnow()
        )
        
        db.add(audit_entry)
        db.commit()
        db.refresh(audit_entry)
        
        return audit_entry
    
    @staticmethod
    def log_job_creation(
        db: Session,
        job_id: int,
        company_id: int,
        role: str,
        user_id: Optional[int] = None
    ) -> AuditLog:
        """Log job posting creation"""
        audit_entry = AuditLog(
            event_type="job_creation",
            entity_type="job",
            entity_id=job_id,
            user_id=user_id,
            action="create",
            details=json.dumps({
                "company_id": company_id,
                "role": role,
                "created_at": datetime.utcnow().isoformat()
            }),
            timestamp=datetime.utcnow()
        )
        
        db.add(audit_entry)
        db.commit()
        db.refresh(audit_entry)
        
        return audit_entry
    
    @staticmethod
    def log_candidate_registration(
        db: Session,
        candidate_id: int,
        email: str
    ) -> AuditLog:
        """Log candidate registration"""
        audit_entry = AuditLog(
            event_type="candidate_registration",
            entity_type="candidate",
            entity_id=candidate_id,
            user_id=None,
            action="create",
            details=json.dumps({
                "email": email,
                "registered_at": datetime.utcnow().isoformat()
            }),
            timestamp=datetime.utcnow()
        )
        
        db.add(audit_entry)
        db.commit()
        db.refresh(audit_entry)
        
        return audit_entry
    
    @staticmethod
    def log_fraud_detection(
        db: Session,
        candidate_id: int,
        fraud_details: Dict
    ) -> AuditLog:
        """Log fraud detection event"""
        audit_entry = AuditLog(
            event_type="fraud_detection",
            entity_type="candidate",
            entity_id=candidate_id,
            user_id=None,
            action="flag",
            details=json.dumps({
                "fraud_analysis": fraud_details,
                "flagged_at": datetime.utcnow().isoformat()
            }),
            timestamp=datetime.utcnow()
        )
        
        db.add(audit_entry)
        db.commit()
        db.refresh(audit_entry)
        
        return audit_entry
    
    @staticmethod
    def get_application_history(
        db: Session,
        application_id: int
    ) -> List[AuditLog]:
        """Retrieve complete audit history for an application"""
        return db.query(AuditLog).filter(
            AuditLog.entity_type == "application",
            AuditLog.entity_id == application_id
        ).order_by(AuditLog.timestamp.desc()).all()
    
    @staticmethod
    def get_candidate_history(
        db: Session,
        candidate_id: int
    ) -> List[AuditLog]:
        """Retrieve complete audit history for a candidate"""
        return db.query(AuditLog).filter(
            AuditLog.entity_type == "candidate",
            AuditLog.entity_id == candidate_id
        ).order_by(AuditLog.timestamp.desc()).all()
    
    @staticmethod
    def get_job_applications_audit(
        db: Session,
        job_id: int
    ) -> List[AuditLog]:
        """Retrieve all application evaluations for a specific job"""
        logs = db.query(AuditLog).filter(
            AuditLog.event_type == "application_evaluation"
        ).all()
        
        # Filter by job_id in details
        job_logs = []
        for log in logs:
            try:
                details = json.loads(log.details)
                if details.get("job_id") == job_id:
                    job_logs.append(log)
            except:
                continue
        
        return sorted(job_logs, key=lambda x: x.timestamp, reverse=True)
    
    @staticmethod
    def get_fraud_flags(
        db: Session,
        limit: int = 100
    ) -> List[AuditLog]:
        """Retrieve recent fraud detection flags"""
        return db.query(AuditLog).filter(
            AuditLog.event_type == "fraud_detection"
        ).order_by(AuditLog.timestamp.desc()).limit(limit).all()
    
    @staticmethod
    def generate_audit_report(
        db: Session,
        start_date: datetime,
        end_date: datetime
    ) -> Dict:
        """Generate comprehensive audit report for a time period"""
        logs = db.query(AuditLog).filter(
            AuditLog.timestamp >= start_date,
            AuditLog.timestamp <= end_date
        ).all()
        
        # Aggregate statistics
        event_counts = {}
        for log in logs:
            event_type = log.event_type
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        # Decision distribution
        decisions = {}
        for log in logs:
            if log.event_type == "application_evaluation":
                try:
                    details = json.loads(log.details)
                    decision = details.get("decision", "unknown")
                    decisions[decision] = decisions.get(decision, 0) + 1
                except:
                    continue
        
        return {
            "period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat()
            },
            "total_events": len(logs),
            "event_breakdown": event_counts,
            "decision_distribution": decisions,
            "fraud_flags": event_counts.get("fraud_detection", 0),
            "applications_processed": event_counts.get("application_evaluation", 0),
            "jobs_created": event_counts.get("job_creation", 0),
            "candidates_registered": event_counts.get("candidate_registration", 0)
        }
    
    @staticmethod
    def log_decision_override(
        db: Session,
        application_id: int,
        original_decision: str,
        new_decision: str,
        user_id: int,
        reason: str
    ) -> AuditLog:
        """Log when a human overrides an AI decision"""
        audit_entry = AuditLog(
            event_type="decision_override",
            entity_type="application",
            entity_id=application_id,
            user_id=user_id,
            action="override",
            details=json.dumps({
                "original_decision": original_decision,
                "new_decision": new_decision,
                "reason": reason,
                "overridden_at": datetime.utcnow().isoformat()
            }),
            timestamp=datetime.utcnow()
        )
        
        db.add(audit_entry)
        db.commit()
        db.refresh(audit_entry)
        
        return audit_entry


# Easy access functions
def log_evaluation(db: Session, application_id: int, job_id: int, candidate_id: int,
                   scores: Dict, fraud_analysis: Dict, decision: str, 
                   decision_reason: str, explanation: Dict) -> AuditLog:
    """Log application evaluation"""
    return AuditService.log_application_evaluation(
        db, application_id, job_id, candidate_id, scores, 
        fraud_analysis, decision, decision_reason, explanation
    )


def log_fraud(db: Session, candidate_id: int, fraud_details: Dict) -> AuditLog:
    """Log fraud detection"""
    return AuditService.log_fraud_detection(db, candidate_id, fraud_details)
