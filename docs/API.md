# StrategySim AI API Documentation

This document provides comprehensive API documentation for the StrategySim AI multi-agent decision analysis system.

## Table of Contents

- [Overview](#overview)
- [Core APIs](#core-apis)
- [Agent APIs](#agent-apis)
- [Model APIs](#model-apis)
- [Utility APIs](#utility-apis)
- [Configuration APIs](#configuration-apis)
- [Examples](#examples)

## Overview

StrategySim AI provides both programmatic APIs and a web interface for multi-agent decision analysis. The system is built with modern Python practices using Pydantic for data validation and async/await patterns for performance.

### Key Features

- **Type-safe APIs**: All APIs use Pydantic models for validation
- **Async/Await**: Full async support for concurrent operations
- **Comprehensive Testing**: Extensive test coverage for all APIs
- **Error Handling**: Robust error handling with meaningful messages

## Core APIs

### Decision Analysis

#### `run_decision_analysis`

Run a complete decision analysis with multi-agent collaboration.

```python
from src.agents import run_decision_analysis, create_decision_team
from src.models.decision_models import DecisionInput, DecisionType

async def run_decision_analysis(
    decision_input: DecisionInput,
    team: Optional[DecisionAnalysisTeam] = None
) -> DecisionReport:
    """
    Run a complete decision analysis with report generation.
    
    Args:
        decision_input: Decision to analyze
        team: Optional team instance (creates default if not provided)
    
    Returns:
        DecisionReport with complete analysis
    
    Raises:
        ValidationError: If decision_input is invalid
        RuntimeError: If analysis fails
    """
```

**Example:**
```python
# Create decision input
decision = DecisionInput(
    title="Market Expansion Strategy",
    description="Evaluating expansion into European markets",
    decision_type=DecisionType.MARKET_ENTRY,
    options=[
        DecisionOption(name="UK First", description="Enter UK market first"),
        DecisionOption(name="Germany First", description="Enter German market first"),
    ],
    timeline="12 months",
    budget_range="$2M - $5M"
)

# Run analysis
report = await run_decision_analysis(decision)
print(f"Recommendation: {report.executive_summary.recommended_option}")
```

#### `create_decision_team`

Create a decision analysis team with specialized agents.

```python
def create_decision_team(
    model_client: Optional[ChatCompletionClient] = None,
    max_turns: int = 20,
    custom_agents: Optional[List[Any]] = None
) -> DecisionAnalysisTeam:
    """
    Create a decision analysis team with default configuration.
    
    Args:
        model_client: Optional model client (creates default if not provided)
        max_turns: Maximum conversation turns
        custom_agents: Optional custom agents to include
    
    Returns:
        DecisionAnalysisTeam instance
    """
```

**Example:**
```python
# Create team with default configuration
team = create_decision_team()

# Create team with custom configuration
team = create_decision_team(
    max_turns=30,
    custom_agents=[my_custom_agent]
)
```

### Decision Validation

#### `validate_decision_input`

Validate decision input for completeness and correctness.

```python
from src.models.decision_models import validate_decision_input

def validate_decision_input(decision_input: DecisionInput) -> ValidationResult:
    """
    Validate decision input for analysis readiness.
    
    Args:
        decision_input: Decision input to validate
    
    Returns:
        ValidationResult with validation status and messages
    """
```

**Example:**
```python
# Validate decision input
validation_result = validate_decision_input(decision)

if validation_result.is_valid:
    print("Decision input is valid!")
else:
    print(f"Validation errors: {validation_result.errors}")
    print(f"Warnings: {validation_result.warnings}")
```

## Agent APIs

### Base Agent

#### `BaseStrategicAgent`

Abstract base class for all strategic agents.

```python
from src.agents.base_agent import BaseStrategicAgent
from src.models.agent_models import AgentRole

class BaseStrategicAgent(ABC):
    """
    Abstract base class for strategic decision analysis agents.
    
    Provides common functionality for all agents including:
    - Tool registration and management
    - Performance metrics tracking
    - Error handling and logging
    - Health monitoring
    """
    
    def __init__(
        self,
        agent_name: str,
        agent_role: AgentRole,
        model_client: ChatCompletionClient,
        tools: List[Any]
    ):
        """Initialize base agent with configuration."""
    
    @abstractmethod
    async def analyze_decision(
        self,
        decision_context: str,
        decision_data: Dict[str, Any]
    ) -> AgentAnalysis:
        """Analyze decision from agent's perspective."""
    
    @abstractmethod
    async def perform_specialized_analysis(
        self,
        decision_context: str,
        decision_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Perform specialized analysis based on agent's expertise."""
```

### Specialized Agents

#### `InvestorAgent`

Financial analysis and investment evaluation agent.

```python
from src.agents.investor_agent import InvestorAgent

class InvestorAgent(BaseStrategicAgent):
    """
    Investor Agent for aggressive financial analysis and growth opportunities.
    
    Specializes in:
    - Financial calculations (NPV, IRR, ROI)
    - Investment risk assessment
    - Growth opportunity evaluation
    - Market timing analysis
    """
    
    def __init__(
        self,
        agent_name: str = "investor",
        model_client: ChatCompletionClient = None,
        custom_tools: Optional[List[Any]] = None
    ):
        """Initialize investor agent with financial tools."""
    
    def get_specialized_tools(self) -> List[Any]:
        """Get financial analysis tools."""
        return [
            calculate_npv,
            calculate_irr,
            calculate_roi,
            calculate_payback_period,
            calculate_break_even_point
        ]
```

#### `LegalAgent`

Legal compliance and risk assessment agent.

```python
from src.agents.legal_agent import LegalAgent

class LegalAgent(BaseStrategicAgent):
    """
    Legal Agent for conservative compliance and risk assessment.
    
    Specializes in:
    - Regulatory compliance analysis
    - Legal risk identification
    - Contract and partnership evaluation
    - Compliance framework assessment
    """
```

#### `AnalystAgent`

Risk modeling and quantitative analysis agent.

```python
from src.agents.analyst_agent import AnalystAgent

class AnalystAgent(BaseStrategicAgent):
    """
    Analyst Agent for pessimistic risk modeling and scenario analysis.
    
    Specializes in:
    - Monte Carlo simulations
    - Risk assessment and modeling
    - Scenario analysis
    - Statistical analysis
    """
```

#### `CustomerAgent`

Market research and customer behavior analysis agent.

```python
from src.agents.customer_agent import CustomerAgent

class CustomerAgent(BaseStrategicAgent):
    """
    Customer Agent for market research and customer impact analysis.
    
    Specializes in:
    - Customer behavior analysis
    - Market segmentation
    - User experience evaluation
    - Demand forecasting
    """
```

#### `StrategistAgent`

Strategic planning and synthesis agent.

```python
from src.agents.strategist_agent import StrategistAgent

class StrategistAgent(BaseStrategicAgent):
    """
    Strategist Agent for strategic synthesis and balanced recommendations.
    
    Specializes in:
    - SWOT analysis
    - Porter's Five Forces
    - Decision tree construction
    - Strategic option evaluation
    """
```

### Team Management

#### `DecisionAnalysisTeam`

Multi-agent team coordination and management.

```python
from src.agents.team import DecisionAnalysisTeam

class DecisionAnalysisTeam:
    """
    Decision Analysis Team using SelectorGroupChat for dynamic agent coordination.
    
    Manages a team of specialized agents that collaborate to analyze strategic 
    decisions through intelligent agent selection and natural conversation flow.
    """
    
    def __init__(
        self,
        model_client: ChatCompletionClient,
        max_turns: int = 20,
        include_all_agents: bool = True,
        custom_agents: Optional[List[Any]] = None
    ):
        """Initialize decision analysis team."""
    
    async def analyze_decision(
        self,
        decision_input: DecisionInput,
        conversation_id: Optional[str] = None
    ) -> AgentConversation:
        """Analyze a strategic decision using the multi-agent team."""
    
    async def generate_decision_report(
        self,
        conversation: AgentConversation,
        decision_input: DecisionInput
    ) -> DecisionReport:
        """Generate comprehensive decision report from conversation."""
    
    def get_team_status(self) -> Dict[str, Any]:
        """Get current team status."""
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on all agents."""
```

## Model APIs

### Decision Models

#### `DecisionInput`

Core decision input model with validation.

```python
from src.models.decision_models import DecisionInput, DecisionType, DecisionUrgency

class DecisionInput(BaseModel):
    """
    Input model for strategic decision analysis.
    
    Contains all necessary information for multi-agent analysis including
    decision context, options, constraints, and requirements.
    """
    
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=20, max_length=2000)
    decision_type: DecisionType
    urgency: DecisionUrgency
    options: List[DecisionOption] = Field(..., min_items=2, max_items=10)
    constraints: List[DecisionConstraint] = Field(default_factory=list)
    timeline: str = Field(..., min_length=1, max_length=100)
    budget_range: Optional[str] = Field(None)
    stakeholders: List[str] = Field(default_factory=list)
    
    # Computed properties
    @property
    def is_urgent(self) -> bool:
        """Check if decision is urgent."""
        return self.urgency in [DecisionUrgency.HIGH, DecisionUrgency.CRITICAL]
    
    @property
    def decision_complexity(self) -> str:
        """Calculate decision complexity."""
        # Implementation details...
```

#### `DecisionOption`

Individual decision option model.

```python
from src.models.decision_models import DecisionOption

class DecisionOption(BaseModel):
    """
    Individual option within a strategic decision.
    
    Represents a single choice available to the decision maker
    with associated metadata and constraints.
    """
    
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=10, max_length=1000)
    estimated_cost: Optional[float] = Field(None, ge=0)
    estimated_timeline: Optional[str] = Field(None)
    success_probability: Optional[float] = Field(None, ge=0, le=1)
    
    # Metadata
    option_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.now)
```

#### `DecisionConstraint`

Decision constraint and limitation model.

```python
from src.models.decision_models import DecisionConstraint

class DecisionConstraint(BaseModel):
    """
    Constraint or limitation for decision analysis.
    
    Represents boundaries and requirements that must be considered
    during the decision-making process.
    """
    
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=10, max_length=500)
    constraint_type: str = Field(..., min_length=1, max_length=50)
    value: str = Field(..., min_length=1, max_length=200)
    is_mandatory: bool = Field(default=True)
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")
```

### Agent Models

#### `AgentAnalysis`

Agent analysis result model.

```python
from src.models.agent_models import AgentAnalysis, AgentRole

class AgentAnalysis(BaseModel):
    """
    Analysis result from a strategic agent.
    
    Contains the agent's professional assessment, recommendations,
    and insights for the strategic decision.
    """
    
    agent_role: AgentRole
    analysis: str = Field(..., min_length=50, max_length=5000)
    confidence_level: float = Field(..., ge=0, le=1)
    recommendations: List[str] = Field(default_factory=list)
    key_insights: List[str] = Field(default_factory=list)
    concerns: List[str] = Field(default_factory=list)
    
    # Computed properties
    @property
    def analysis_summary(self) -> str:
        """Get truncated analysis summary."""
        return self.analysis[:200] + "..." if len(self.analysis) > 200 else self.analysis
    
    @property
    def risk_level(self) -> RiskLevel:
        """Calculate risk level based on confidence."""
        if self.confidence_level >= 0.8:
            return RiskLevel.LOW
        elif self.confidence_level >= 0.6:
            return RiskLevel.MEDIUM
        elif self.confidence_level >= 0.4:
            return RiskLevel.HIGH
        else:
            return RiskLevel.CRITICAL
```

#### `AgentConversation`

Multi-agent conversation state model.

```python
from src.models.agent_models import AgentConversation, ConversationState

class AgentConversation(BaseModel):
    """
    Multi-agent conversation tracking and state management.
    
    Tracks the progress and state of agent collaboration
    during decision analysis.
    """
    
    conversation_id: str = Field(..., min_length=1, max_length=100)
    participants: List[str] = Field(..., min_items=1, max_items=20)
    state: ConversationState = Field(default=ConversationState.INITIALIZING)
    max_turns: int = Field(..., gt=0)
    turn_count: int = Field(default=0, ge=0)
    context: Dict[str, Any] = Field(default_factory=dict)
    
    # Computed properties
    def is_finished(self) -> bool:
        """Check if conversation is finished."""
        return (
            self.state == ConversationState.CONCLUDED or
            self.turn_count >= self.max_turns
        )
    
    @property
    def progress_percentage(self) -> float:
        """Calculate conversation progress percentage."""
        return min(self.turn_count / self.max_turns, 1.0)
```

### Report Models

#### `DecisionReport`

Comprehensive decision analysis report.

```python
from src.models.report_models import DecisionReport, ReportStatus

class DecisionReport(BaseModel):
    """
    Comprehensive decision analysis report.
    
    Contains complete analysis results, recommendations,
    and supporting data from multi-agent collaboration.
    """
    
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
    
    # Report metadata
    report_metrics: ReportMetrics
    participants: List[str] = Field(..., min_items=1)
    analysis_duration: float = Field(..., ge=0.0)
    
    # Helper methods
    def get_recommended_option(self) -> Optional[OptionEvaluation]:
        """Get the recommended option evaluation."""
        if not self.option_evaluations:
            return None
        return max(self.option_evaluations, key=lambda x: x.overall_score)
    
    def get_critical_action_items(self) -> List[ActionItem]:
        """Get action items with critical priority."""
        return [item for item in self.action_items if item.priority == ActionPriority.CRITICAL]
```

## Utility APIs

### Financial Calculator

Financial analysis tools for investment evaluation.

```python
from src.tools.financial_calculator import (
    calculate_npv, calculate_irr, calculate_roi, 
    calculate_payback_period, calculate_break_even_point
)

def calculate_npv(cash_flows: List[float], discount_rate: float) -> float:
    """
    Calculate Net Present Value (NPV).
    
    Args:
        cash_flows: List of cash flows (negative for outflows)
        discount_rate: Discount rate as decimal (e.g., 0.10 for 10%)
    
    Returns:
        NPV value
    
    Raises:
        ValueError: If cash flows are empty or discount rate is negative
    """

def calculate_irr(cash_flows: List[float], max_iterations: int = 100) -> Optional[float]:
    """
    Calculate Internal Rate of Return (IRR).
    
    Args:
        cash_flows: List of cash flows
        max_iterations: Maximum iterations for convergence
    
    Returns:
        IRR as decimal or None if no solution found
    """

def calculate_roi(
    initial_investment: float, 
    final_value: float, 
    years: Optional[int] = None
) -> float:
    """
    Calculate Return on Investment (ROI).
    
    Args:
        initial_investment: Initial investment amount
        final_value: Final value of investment
        years: Number of years for annualized ROI
    
    Returns:
        ROI as decimal
    """
```

### Report Generator

Multi-format report generation utilities.

```python
from src.utils.report_generator import ReportGenerator, generate_comprehensive_report

class ReportGenerator:
    """
    Comprehensive report generator for StrategySim AI decision analysis.
    
    Supports multiple output formats and customizable templates.
    """
    
    def __init__(self, template_dir: Optional[str] = None):
        """Initialize report generator with template directory."""
    
    def generate_html_report(
        self, 
        report: DecisionReport, 
        template_name: str = "decision_report.html",
        include_visualizations: bool = True
    ) -> str:
        """Generate HTML report from decision analysis."""
    
    def generate_pdf_report(
        self, 
        report: DecisionReport, 
        output_path: Optional[str] = None,
        include_visualizations: bool = True
    ) -> str:
        """Generate PDF report from decision analysis."""
    
    def generate_excel_report(
        self, 
        report: DecisionReport, 
        output_path: Optional[str] = None
    ) -> str:
        """Generate Excel report from decision analysis."""

# Utility function for comprehensive report generation
def generate_comprehensive_report(
    report: DecisionReport,
    output_dir: str = "reports",
    formats: List[str] = ["html", "pdf", "json"]
) -> Dict[str, str]:
    """
    Generate comprehensive report in multiple formats.
    
    Args:
        report: Decision report to generate
        output_dir: Directory to save reports
        formats: List of formats to generate
    
    Returns:
        Dictionary mapping format to file path
    """
```

### Visualization

Chart and graph generation utilities.

```python
from src.utils.visualization import (
    create_risk_reward_matrix, create_consensus_chart,
    create_decision_timeline, generate_report_visualizations
)

def create_risk_reward_matrix(
    options: List[OptionEvaluation],
    title: str = "Risk-Reward Analysis"
) -> str:
    """
    Create risk-reward matrix visualization.
    
    Args:
        options: List of option evaluations
        title: Chart title
    
    Returns:
        Base64 encoded image string
    """

def generate_report_visualizations(report: DecisionReport) -> Dict[str, str]:
    """
    Generate all visualizations for a decision report.
    
    Args:
        report: Decision report
    
    Returns:
        Dictionary of visualization names to base64 image strings
    """
```

## Configuration APIs

### Settings Management

Application configuration and settings.

```python
from src.config.settings import settings, get_model_config

class Settings(BaseSettings):
    """
    Application settings with environment variable support.
    
    Provides configuration for model providers, API keys,
    and application parameters.
    """
    
    # Model configuration
    model_provider: str = Field(default="openai")
    model_name: str = Field(default="gpt-4")
    openai_api_key: Optional[str] = Field(None)
    
    # Application settings
    debug: bool = Field(default=False)
    log_level: str = Field(default="INFO")
    
    # Chainlit settings
    chainlit_host: str = Field(default="0.0.0.0")
    chainlit_port: int = Field(default=8000)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Global settings instance
settings = Settings()

def get_model_config() -> Dict[str, Any]:
    """
    Get model configuration for AutoGen agents.
    
    Returns:
        Model configuration dictionary
    """
```

## Examples

### Complete Analysis Example

```python
import asyncio
from src.agents import create_decision_team, run_decision_analysis
from src.models.decision_models import DecisionInput, DecisionType, DecisionOption
from src.utils.report_generator import generate_comprehensive_report

async def main():
    # Create decision input
    decision = DecisionInput(
        title="Cloud Migration Strategy",
        description="Evaluating cloud migration options for enterprise application",
        decision_type=DecisionType.STRATEGIC_PARTNERSHIP,
        options=[
            DecisionOption(
                name="AWS Migration",
                description="Migrate to Amazon Web Services",
                estimated_cost=500000,
                estimated_timeline="6 months"
            ),
            DecisionOption(
                name="Azure Migration", 
                description="Migrate to Microsoft Azure",
                estimated_cost=450000,
                estimated_timeline="8 months"
            ),
            DecisionOption(
                name="Multi-Cloud",
                description="Implement multi-cloud strategy",
                estimated_cost=750000,
                estimated_timeline="12 months"
            )
        ],
        timeline="Must decide within 3 months",
        budget_range="$400K - $800K",
        stakeholders=["CTO", "IT Director", "CFO"]
    )
    
    # Create team and run analysis
    team = create_decision_team(max_turns=25)
    report = await run_decision_analysis(decision, team)
    
    # Generate comprehensive reports
    file_paths = generate_comprehensive_report(
        report,
        output_dir="cloud_migration_reports",
        formats=["html", "pdf", "excel", "json"]
    )
    
    # Print results
    print(f"Analysis Complete!")
    print(f"Recommendation: {report.executive_summary.recommended_option}")
    print(f"Confidence: {report.executive_summary.confidence_level:.1%}")
    print(f"Reports generated: {list(file_paths.keys())}")
    
    # Show key insights
    for analysis in report.agent_analyses:
        print(f"\n{analysis.agent_role.value.title()} Agent:")
        print(f"  Confidence: {analysis.confidence_level:.1%}")
        print(f"  Key Insights: {analysis.key_insights[:2]}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Custom Agent Example

```python
from src.agents.base_agent import BaseStrategicAgent
from src.models.agent_models import AgentRole, AgentAnalysis

class SecurityAgent(BaseStrategicAgent):
    """Custom security analysis agent."""
    
    def __init__(self, model_client):
        super().__init__(
            agent_name="security_analyst",
            agent_role=AgentRole.ANALYST,  # Reuse existing role
            model_client=model_client,
            tools=self.get_specialized_tools()
        )
    
    def get_specialized_tools(self):
        return [
            security_risk_assessment,
            compliance_check,
            threat_modeling
        ]
    
    async def perform_specialized_analysis(self, context, data):
        """Perform security-focused analysis."""
        security_assessment = {
            "vulnerability_scan": await self.scan_vulnerabilities(data),
            "compliance_status": await self.check_compliance(data),
            "threat_analysis": await self.analyze_threats(data),
            "recommendations": await self.generate_security_recommendations(data)
        }
        
        return {"security_assessment": security_assessment}

# Use custom agent in team
team = create_decision_team(custom_agents=[SecurityAgent(model_client)])
```

### Error Handling Example

```python
from src.models.decision_models import ValidationError
from src.agents import run_decision_analysis

async def safe_analysis(decision_input):
    """Run analysis with comprehensive error handling."""
    try:
        # Validate input
        validation_result = validate_decision_input(decision_input)
        if not validation_result.is_valid:
            print(f"Validation errors: {validation_result.errors}")
            return None
        
        # Run analysis
        report = await run_decision_analysis(decision_input)
        
        # Validate report quality
        quality_check = validate_report_quality(report)
        if quality_check["quality_score"] < 0.7:
            print(f"Warning: Low quality report (score: {quality_check['quality_score']:.1%})")
        
        return report
        
    except ValidationError as e:
        print(f"Validation error: {e}")
        return None
    except Exception as e:
        print(f"Analysis error: {e}")
        return None
```

## Error Handling

### Common Error Types

- **ValidationError**: Input validation failures
- **RuntimeError**: Analysis execution failures
- **ValueError**: Invalid parameter values
- **TimeoutError**: Analysis timeout
- **ConnectionError**: Model API connection issues

### Error Response Format

```python
{
    "error": "ValidationError",
    "message": "Decision input validation failed",
    "details": {
        "field": "options",
        "error": "At least 2 options are required"
    },
    "timestamp": "2024-01-15T10:30:00Z"
}
```

## Rate Limits

- **Model API**: Depends on provider (OpenAI, Azure, etc.)
- **Analysis**: No built-in limits, depends on system resources
- **Report Generation**: No limits, but large reports may take time

## Authentication

Currently, StrategySim AI uses environment-based authentication:

- **API Keys**: Stored in environment variables
- **Model Access**: Configured per provider
- **Web Interface**: Optional authentication via Chainlit

## Versioning

API versioning follows semantic versioning:
- **Major**: Breaking changes
- **Minor**: New features, backward compatible
- **Patch**: Bug fixes, backward compatible

Current version: `0.1.0`

For more information, see the [CHANGELOG](../CHANGELOG.md).