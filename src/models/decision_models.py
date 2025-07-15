"""
Core decision input structures for StrategySim AI.

Contains Pydantic models for decision analysis including:
- DecisionInput: Structured input for strategic decisions
- DecisionType: Enumeration of supported decision types
- DecisionOption: Individual decision option with metadata
- DecisionConstraint: Constraint definitions for decision analysis
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator


class DecisionType(str, Enum):
    """Enumeration of supported decision types."""
    
    PRICING = "pricing"
    MARKET_ENTRY = "market_entry"
    PRODUCT_LAUNCH = "product_launch"
    INVESTMENT = "investment"
    MERGER_ACQUISITION = "merger_acquisition"
    HIRING = "hiring"
    BUDGET_ALLOCATION = "budget_allocation"
    STRATEGIC_PARTNERSHIP = "strategic_partnership"


class DecisionUrgency(str, Enum):
    """Enumeration of decision urgency levels."""
    
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DecisionOption(BaseModel):
    """Individual decision option with metadata."""
    
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=10, max_length=500)
    estimated_cost: Optional[float] = Field(None, ge=0.0)
    estimated_timeline: Optional[str] = None
    confidence_level: Optional[float] = Field(None, ge=0.0, le=1.0)
    
    @validator('name')
    def validate_name(cls, v: str) -> str:
        """Ensure option name is meaningful."""
        if len(v.strip()) < 1:
            raise ValueError("Option name cannot be empty")
        return v.strip()


class DecisionConstraint(BaseModel):
    """Constraint definition for decision analysis."""
    
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=5, max_length=200)
    constraint_type: str = Field(..., description="Type of constraint (budget, time, regulatory, etc.)")
    value: Any = Field(..., description="Constraint value")
    is_hard_constraint: bool = Field(default=True, description="Whether this is a hard or soft constraint")


class DecisionInput(BaseModel):
    """Structured input for strategic decision analysis."""
    
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=20, max_length=2000)
    decision_type: DecisionType
    urgency: DecisionUrgency = Field(default=DecisionUrgency.MEDIUM)
    options: List[DecisionOption] = Field(..., min_items=2, max_items=5)
    constraints: List[DecisionConstraint] = Field(default_factory=list)
    timeline: str = Field(..., description="Decision timeline or deadline")
    budget_range: Optional[str] = None
    success_metrics: List[str] = Field(default_factory=list)
    stakeholders: List[str] = Field(default_factory=list)
    additional_context: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)
    
    @validator('options')
    def validate_options(cls, v: List[DecisionOption]) -> List[DecisionOption]:
        """Ensure options are unique and meaningful."""
        names = [option.name for option in v]
        if len(set(names)) != len(names):
            raise ValueError("Option names must be unique")
        return v
    
    @validator('title')
    def validate_title(cls, v: str) -> str:
        """Ensure title is meaningful."""
        if len(v.strip()) < 5:
            raise ValueError("Title must be at least 5 characters")
        return v.strip()
    
    @validator('timeline')
    def validate_timeline(cls, v: str) -> str:
        """Ensure timeline is provided."""
        if not v.strip():
            raise ValueError("Timeline cannot be empty")
        return v.strip()


class DecisionContext(BaseModel):
    """Context information for decision analysis."""
    
    industry: Optional[str] = None
    company_size: Optional[str] = None
    geographic_scope: Optional[str] = None
    competitive_landscape: Optional[str] = None
    regulatory_environment: Optional[str] = None
    market_conditions: Optional[str] = None
    internal_capabilities: Optional[str] = None
    risk_tolerance: Optional[str] = None
    strategic_priorities: List[str] = Field(default_factory=list)
    
    
class DecisionValidationError(BaseModel):
    """Validation error for decision inputs."""
    
    field: str
    message: str
    error_type: str
    suggested_fix: Optional[str] = None


class DecisionValidationResult(BaseModel):
    """Result of decision input validation."""
    
    is_valid: bool
    errors: List[DecisionValidationError] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)
    completeness_score: float = Field(default=0.0, ge=0.0, le=1.0)
    
    
def validate_decision_input(decision: DecisionInput) -> DecisionValidationResult:
    """Validate a decision input and provide feedback."""
    errors = []
    warnings = []
    suggestions = []
    
    # Check for completeness
    if not decision.budget_range:
        warnings.append("Budget range not specified - this may affect financial analysis")
    
    if not decision.success_metrics:
        warnings.append("Success metrics not defined - consider adding measurable outcomes")
    
    if not decision.stakeholders:
        warnings.append("Stakeholders not identified - consider adding key decision makers")
    
    # Check option completeness
    for i, option in enumerate(decision.options):
        if not option.estimated_cost:
            warnings.append(f"Option '{option.name}' has no cost estimate")
        if not option.estimated_timeline:
            warnings.append(f"Option '{option.name}' has no timeline estimate")
    
    # Calculate completeness score
    total_fields = 12  # Based on key fields in DecisionInput
    filled_fields = sum([
        1 if decision.title else 0,
        1 if decision.description else 0,
        1 if decision.decision_type else 0,
        1 if decision.options else 0,
        1 if decision.timeline else 0,
        1 if decision.budget_range else 0,
        1 if decision.success_metrics else 0,
        1 if decision.stakeholders else 0,
        1 if decision.constraints else 0,
        1 if decision.additional_context else 0,
        1 if decision.urgency else 0,
        1 if len(decision.options) >= 2 else 0,
    ])
    
    completeness_score = filled_fields / total_fields
    
    # Add suggestions based on completeness
    if completeness_score < 0.7:
        suggestions.append("Consider providing more details for better analysis")
    
    if not decision.constraints:
        suggestions.append("Adding constraints will help agents provide more realistic recommendations")
    
    return DecisionValidationResult(
        is_valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
        suggestions=suggestions,
        completeness_score=completeness_score
    )