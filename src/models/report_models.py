"""
Decision report and analysis models for StrategySim AI.

Contains Pydantic models for decision reporting including:
- DecisionReport: Comprehensive decision analysis report
- RiskAssessment: Risk analysis and scoring
- ConsensusAnalysis: Agent consensus measurement
- ActionItem: Actionable recommendations
- ReportMetrics: Report quality metrics
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel, Field, validator

from .agent_models import AgentAnalysis, AgentRole, RiskLevel
from .decision_models import DecisionInput, DecisionType


class ReportStatus(str, Enum):
    """Enumeration of report statuses."""
    
    DRAFT = "draft"
    COMPLETED = "completed"
    REVIEWED = "reviewed"
    APPROVED = "approved"
    REJECTED = "rejected"


class ActionPriority(str, Enum):
    """Enumeration of action item priorities."""
    
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NICE_TO_HAVE = "nice_to_have"


class RecommendationCategory(str, Enum):
    """Enumeration of recommendation categories."""
    
    PROCEED = "proceed"
    PROCEED_WITH_CAUTION = "proceed_with_caution"
    MODIFY_APPROACH = "modify_approach"
    DELAY = "delay"
    REJECT = "reject"
    SEEK_MORE_INFO = "seek_more_info"


class RiskCategory(str, Enum):
    """Enumeration of risk categories."""
    
    FINANCIAL = "financial"
    OPERATIONAL = "operational"
    STRATEGIC = "strategic"
    LEGAL = "legal"
    REGULATORY = "regulatory"
    REPUTATIONAL = "reputational"
    MARKET = "market"
    TECHNICAL = "technical"


class RiskAssessment(BaseModel):
    """Risk analysis and scoring for decision options."""
    
    category: RiskCategory
    description: str = Field(..., min_length=10, max_length=500)
    probability: float = Field(..., ge=0.0, le=1.0, description="Probability of risk occurring")
    impact: float = Field(..., ge=0.0, le=1.0, description="Impact severity if risk occurs")
    risk_score: float = Field(..., ge=0.0, le=1.0, description="Combined risk score")
    mitigation_strategies: List[str] = Field(default_factory=list)
    contingency_plans: List[str] = Field(default_factory=list)
    responsible_party: Optional[str] = Field(None)
    timeline: Optional[str] = Field(None)
    
    @validator('risk_score')
    def validate_risk_score(cls, v: float, values: Dict[str, Any]) -> float:
        """Validate risk score calculation."""
        probability = values.get('probability', 0.0)
        impact = values.get('impact', 0.0)
        expected_score = probability * impact
        
        # Allow some tolerance for different risk calculation methods
        if abs(v - expected_score) > 0.1:
            # If custom scoring is used, ensure it's reasonable
            if not (0.0 <= v <= 1.0):
                raise ValueError("Risk score must be between 0.0 and 1.0")
        return v


class ActionItem(BaseModel):
    """Actionable recommendation with implementation details."""
    
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=20, max_length=1000)
    priority: ActionPriority
    category: str = Field(..., description="Category of action (implementation, research, etc.)")
    responsible_party: Optional[str] = Field(None)
    estimated_effort: Optional[str] = Field(None, description="Estimated effort required")
    timeline: Optional[str] = Field(None)
    dependencies: List[str] = Field(default_factory=list)
    success_criteria: List[str] = Field(default_factory=list)
    resources_required: List[str] = Field(default_factory=list)
    expected_outcome: Optional[str] = Field(None)
    
    @validator('title')
    def validate_title(cls, v: str) -> str:
        """Ensure title is meaningful."""
        if len(v.strip()) < 5:
            raise ValueError("Action item title must be at least 5 characters")
        return v.strip()


class OptionEvaluation(BaseModel):
    """Evaluation of a specific decision option."""
    
    option_name: str = Field(..., min_length=1, max_length=100)
    overall_score: float = Field(..., ge=0.0, le=1.0)
    pros: List[str] = Field(default_factory=list)
    cons: List[str] = Field(default_factory=list)
    risk_assessments: List[RiskAssessment] = Field(default_factory=list)
    financial_impact: Optional[Dict[str, float]] = Field(None)
    implementation_complexity: str = Field(..., description="Complexity assessment")
    time_to_implement: Optional[str] = Field(None)
    resource_requirements: List[str] = Field(default_factory=list)
    success_probability: float = Field(..., ge=0.0, le=1.0)
    agent_votes: Dict[str, float] = Field(default_factory=dict)
    
    @validator('option_name')
    def validate_option_name(cls, v: str) -> str:
        """Ensure option name is meaningful."""
        if len(v.strip()) < 1:
            raise ValueError("Option name cannot be empty")
        return v.strip()
    
    @property
    def overall_risk_score(self) -> float:
        """Calculate overall risk score for the option."""
        if not self.risk_assessments:
            return 0.0
        return sum(risk.risk_score for risk in self.risk_assessments) / len(self.risk_assessments)


class ConsensusAnalysis(BaseModel):
    """Analysis of agent consensus on decision options."""
    
    consensus_level: float = Field(..., ge=0.0, le=1.0, description="Overall consensus level")
    agreement_by_option: Dict[str, float] = Field(default_factory=dict)
    disagreement_areas: List[str] = Field(default_factory=list)
    unanimous_points: List[str] = Field(default_factory=list)
    agent_alignment: Dict[str, Dict[str, float]] = Field(default_factory=dict)
    confidence_distribution: Dict[str, float] = Field(default_factory=dict)
    
    @validator('consensus_level')
    def validate_consensus_level(cls, v: float) -> float:
        """Ensure consensus level is valid."""
        if not (0.0 <= v <= 1.0):
            raise ValueError("Consensus level must be between 0.0 and 1.0")
        return v
    
    @property
    def consensus_category(self) -> str:
        """Categorize consensus level."""
        if self.consensus_level >= 0.8:
            return "strong_consensus"
        elif self.consensus_level >= 0.6:
            return "moderate_consensus"
        elif self.consensus_level >= 0.4:
            return "weak_consensus"
        else:
            return "no_consensus"


class ExecutiveSummary(BaseModel):
    """Executive summary of decision analysis."""
    
    decision_title: str = Field(..., min_length=5, max_length=200)
    recommended_option: str = Field(..., min_length=1, max_length=100)
    recommendation_category: RecommendationCategory
    confidence_level: float = Field(..., ge=0.0, le=1.0)
    key_findings: List[str] = Field(..., min_items=1, max_items=5)
    critical_risks: List[str] = Field(default_factory=list)
    success_factors: List[str] = Field(default_factory=list)
    next_steps: List[str] = Field(..., min_items=1, max_items=10)
    decision_urgency: str = Field(..., description="Urgency level")
    estimated_impact: str = Field(..., description="Expected impact description")
    
    @validator('key_findings')
    def validate_key_findings(cls, v: List[str]) -> List[str]:
        """Ensure key findings are meaningful."""
        if not v:
            raise ValueError("At least one key finding is required")
        for finding in v:
            if len(finding.strip()) < 10:
                raise ValueError("Each key finding must be at least 10 characters")
        return v


class ReportMetrics(BaseModel):
    """Metrics for report quality and completeness."""
    
    completeness_score: float = Field(..., ge=0.0, le=1.0)
    consistency_score: float = Field(..., ge=0.0, le=1.0)
    agent_participation: Dict[str, int] = Field(default_factory=dict)
    analysis_depth: float = Field(..., ge=0.0, le=1.0)
    risk_coverage: float = Field(..., ge=0.0, le=1.0)
    recommendation_quality: float = Field(..., ge=0.0, le=1.0)
    evidence_support: float = Field(..., ge=0.0, le=1.0)
    
    @property
    def overall_quality_score(self) -> float:
        """Calculate overall report quality score."""
        scores = [
            self.completeness_score,
            self.consistency_score,
            self.analysis_depth,
            self.risk_coverage,
            self.recommendation_quality,
            self.evidence_support
        ]
        return sum(scores) / len(scores)


class DecisionReport(BaseModel):
    """Comprehensive decision analysis report."""
    
    report_id: str = Field(..., min_length=1, max_length=100)
    decision_input: DecisionInput
    status: ReportStatus = Field(default=ReportStatus.DRAFT)
    
    # Core analysis components
    agent_analyses: List[AgentAnalysis] = Field(default_factory=list)
    option_evaluations: List[OptionEvaluation] = Field(default_factory=list)
    risk_assessments: List[RiskAssessment] = Field(default_factory=list)
    consensus_analysis: ConsensusAnalysis
    executive_summary: ExecutiveSummary
    
    # Recommendations and actions
    final_recommendation: str = Field(..., min_length=50, max_length=1000)
    action_items: List[ActionItem] = Field(default_factory=list)
    
    # Analysis metrics
    probability_matrix: Dict[str, Dict[str, float]] = Field(default_factory=dict)
    sensitivity_analysis: Dict[str, Any] = Field(default_factory=dict)
    scenario_outcomes: Dict[str, Any] = Field(default_factory=dict)
    
    # Report metadata
    report_metrics: ReportMetrics
    participants: List[str] = Field(..., min_items=1)
    analysis_duration: float = Field(..., ge=0.0, description="Analysis duration in seconds")
    confidence_interval: Tuple[float, float] = Field(default=(0.0, 1.0))
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = Field(None)
    reviewed_at: Optional[datetime] = Field(None)
    approved_at: Optional[datetime] = Field(None)
    
    @validator('report_id')
    def validate_report_id(cls, v: str) -> str:
        """Ensure report ID is meaningful."""
        if len(v.strip()) < 1:
            raise ValueError("Report ID cannot be empty")
        return v.strip()
    
    @validator('participants')
    def validate_participants(cls, v: List[str]) -> List[str]:
        """Ensure participants are unique."""
        if len(set(v)) != len(v):
            raise ValueError("Participants must be unique")
        return v
    
    @validator('confidence_interval')
    def validate_confidence_interval(cls, v: Tuple[float, float]) -> Tuple[float, float]:
        """Ensure confidence interval is valid."""
        lower, upper = v
        if not (0.0 <= lower <= upper <= 1.0):
            raise ValueError("Confidence interval must be between 0.0 and 1.0 with lower <= upper")
        return v
    
    def get_recommended_option(self) -> Optional[OptionEvaluation]:
        """Get the recommended option evaluation."""
        if not self.option_evaluations:
            return None
        return max(self.option_evaluations, key=lambda x: x.overall_score)
    
    def get_highest_risk_option(self) -> Optional[OptionEvaluation]:
        """Get the option with highest risk."""
        if not self.option_evaluations:
            return None
        return max(self.option_evaluations, key=lambda x: x.overall_risk_score)
    
    def get_risks_by_category(self, category: RiskCategory) -> List[RiskAssessment]:
        """Get all risks for a specific category."""
        return [risk for risk in self.risk_assessments if risk.category == category]
    
    def get_critical_action_items(self) -> List[ActionItem]:
        """Get action items with critical priority."""
        return [item for item in self.action_items if item.priority == ActionPriority.CRITICAL]
    
    def mark_completed(self) -> None:
        """Mark the report as completed."""
        self.status = ReportStatus.COMPLETED
        self.completed_at = datetime.now()
    
    def mark_reviewed(self) -> None:
        """Mark the report as reviewed."""
        self.status = ReportStatus.REVIEWED
        self.reviewed_at = datetime.now()
    
    def mark_approved(self) -> None:
        """Mark the report as approved."""
        self.status = ReportStatus.APPROVED
        self.approved_at = datetime.now()


class ReportTemplate(BaseModel):
    """Template for generating decision reports."""
    
    template_name: str = Field(..., min_length=1, max_length=100)
    decision_types: List[DecisionType] = Field(..., min_items=1)
    sections: List[str] = Field(..., min_items=1)
    required_agents: List[AgentRole] = Field(..., min_items=1)
    format_options: List[str] = Field(default_factory=list)
    custom_fields: Dict[str, Any] = Field(default_factory=dict)
    
    @validator('template_name')
    def validate_template_name(cls, v: str) -> str:
        """Ensure template name is meaningful."""
        if len(v.strip()) < 1:
            raise ValueError("Template name cannot be empty")
        return v.strip()