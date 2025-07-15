"""
Test configuration and fixtures for StrategySim AI.

Contains shared fixtures and configuration for the entire test suite.
"""

import asyncio
import json
import os
import tempfile
from datetime import datetime
from typing import Any, Dict, List, Optional
from unittest.mock import Mock, MagicMock, patch

import pytest
from pydantic import BaseModel

# Test imports
from src.models.decision_models import (
    DecisionInput, DecisionType, DecisionUrgency, DecisionOption, DecisionConstraint
)
from src.models.agent_models import (
    AgentRole, AgentAnalysis, ConversationState, AgentConversation
)
from src.models.report_models import (
    DecisionReport, ExecutiveSummary, ConsensusAnalysis, ReportMetrics,
    ActionItem, ActionPriority, RiskAssessment, RiskCategory,
    OptionEvaluation, RecommendationCategory, ReportStatus
)
from src.agents.team import DecisionAnalysisTeam
from src.config.settings import settings


# Test configuration
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_model_client():
    """Mock AutoGen model client for testing."""
    mock_client = Mock()
    mock_client.model_info = Mock()
    mock_client.model_info.model_id = "test-model"
    return mock_client


@pytest.fixture
def sample_decision_input():
    """Create sample decision input for testing."""
    options = [
        DecisionOption(
            name="Option A",
            description="Expand into new market with aggressive pricing"
        ),
        DecisionOption(
            name="Option B", 
            description="Maintain current market position with quality focus"
        ),
        DecisionOption(
            name="Option C",
            description="Strategic acquisition of competitor"
        )
    ]
    
    constraints = [
        DecisionConstraint(
            name="Budget",
            description="Maximum budget of $10M",
            constraint_type="budget",
            value="10000000"
        ),
        DecisionConstraint(
            name="Timeline",
            description="Must complete within 12 months",
            constraint_type="timeline",
            value="12 months"
        )
    ]
    
    return DecisionInput(
        title="Strategic Market Expansion Decision",
        description="Deciding on the best approach for expanding our presence in the European market",
        decision_type=DecisionType.MARKET_ENTRY,
        urgency=DecisionUrgency.HIGH,
        options=options,
        constraints=constraints,
        timeline="12 months",
        budget_range="$5M - $10M",
        stakeholders=["CEO", "Marketing Director", "CFO"]
    )


@pytest.fixture
def sample_agent_analysis():
    """Create sample agent analysis for testing."""
    return AgentAnalysis(
        agent_role=AgentRole.INVESTOR,
        analysis="From a financial perspective, Option A shows the highest potential ROI with projected 25% growth in year one. However, it carries significant capital requirements and market risk.",
        confidence_level=0.8,
        recommendations=[
            "Secure additional funding before proceeding",
            "Conduct thorough market validation",
            "Develop risk mitigation strategies"
        ],
        key_insights=[
            "Market opportunity is substantial",
            "Competition is currently weak",
            "Customer demand is validated"
        ],
        concerns=[
            "High capital requirements",
            "Regulatory uncertainty",
            "Implementation complexity"
        ]
    )


@pytest.fixture
def sample_risk_assessment():
    """Create sample risk assessment for testing."""
    return RiskAssessment(
        category=RiskCategory.MARKET,
        description="Risk of market rejection due to cultural differences",
        probability=0.3,
        impact=0.7,
        risk_score=0.21,
        mitigation_strategies=[
            "Conduct extensive market research",
            "Partner with local companies",
            "Develop culturally adapted products"
        ],
        contingency_plans=[
            "Pivot to different market segment",
            "Adjust product offering",
            "Retreat and reassess"
        ],
        responsible_party="Marketing Team",
        timeline="3 months"
    )


@pytest.fixture
def sample_option_evaluation():
    """Create sample option evaluation for testing."""
    return OptionEvaluation(
        option_name="Option A",
        overall_score=0.85,
        pros=[
            "High growth potential",
            "Strong competitive position",
            "Market timing is optimal"
        ],
        cons=[
            "High capital requirements",
            "Regulatory uncertainty",
            "Implementation complexity"
        ],
        risk_assessments=[],
        financial_impact={"roi": 0.25, "npv": 2500000, "payback_period": 2.5},
        implementation_complexity="High",
        time_to_implement="12 months",
        resource_requirements=["Marketing team", "Legal support", "IT infrastructure"],
        success_probability=0.7,
        agent_votes={"investor": 0.9, "legal": 0.6, "analyst": 0.8}
    )


@pytest.fixture
def sample_executive_summary():
    """Create sample executive summary for testing."""
    return ExecutiveSummary(
        decision_title="Strategic Market Expansion Decision",
        recommended_option="Option A",
        recommendation_category=RecommendationCategory.PROCEED_WITH_CAUTION,
        confidence_level=0.75,
        key_findings=[
            "Market opportunity is substantial with 25% growth potential",
            "Option A offers the best risk-adjusted returns",
            "Implementation requires significant investment and careful planning"
        ],
        critical_risks=[
            "Market rejection due to cultural differences",
            "Regulatory compliance challenges"
        ],
        success_factors=[
            "Strong market research and validation",
            "Experienced local partnerships",
            "Adequate funding and resources"
        ],
        next_steps=[
            "Conduct detailed market research",
            "Secure regulatory approvals",
            "Develop implementation roadmap",
            "Establish local partnerships"
        ],
        decision_urgency="high",
        estimated_impact="High positive impact on revenue and market position"
    )


@pytest.fixture
def sample_consensus_analysis():
    """Create sample consensus analysis for testing."""
    return ConsensusAnalysis(
        consensus_level=0.75,
        agreement_by_option={
            "Option A": 0.8,
            "Option B": 0.6,
            "Option C": 0.4
        },
        disagreement_areas=[
            "Implementation timeline",
            "Resource allocation",
            "Risk tolerance"
        ],
        unanimous_points=[
            "Market opportunity exists",
            "Competitive advantage possible",
            "Strategic importance high"
        ],
        agent_alignment={
            "investor": {"Option A": 0.9, "Option B": 0.5, "Option C": 0.3},
            "legal": {"Option A": 0.6, "Option B": 0.8, "Option C": 0.4},
            "analyst": {"Option A": 0.8, "Option B": 0.6, "Option C": 0.5}
        },
        confidence_distribution={
            "high": 0.6,
            "medium": 0.3,
            "low": 0.1
        }
    )


@pytest.fixture
def sample_report_metrics():
    """Create sample report metrics for testing."""
    return ReportMetrics(
        completeness_score=0.9,
        consistency_score=0.8,
        agent_participation={"investor": 5, "legal": 3, "analyst": 4, "customer": 2, "strategist": 6},
        analysis_depth=0.85,
        risk_coverage=0.9,
        recommendation_quality=0.8,
        evidence_support=0.75
    )


@pytest.fixture
def sample_action_item():
    """Create sample action item for testing."""
    return ActionItem(
        title="Conduct Market Research",
        description="Comprehensive market research to validate demand and competitive landscape in target European markets",
        priority=ActionPriority.HIGH,
        category="research",
        responsible_party="Marketing Team",
        estimated_effort="8 weeks",
        timeline="Next 2 months",
        dependencies=["Budget approval", "Team allocation"],
        success_criteria=[
            "Market size validation",
            "Competitive analysis completed",
            "Customer segments identified"
        ],
        resources_required=["Market research firm", "Budget allocation", "Team time"],
        expected_outcome="Clear understanding of market opportunity and competitive landscape"
    )


@pytest.fixture
def sample_decision_report(
    sample_decision_input,
    sample_agent_analysis,
    sample_option_evaluation,
    sample_executive_summary,
    sample_consensus_analysis,
    sample_report_metrics,
    sample_action_item,
    sample_risk_assessment
):
    """Create comprehensive sample decision report for testing."""
    return DecisionReport(
        report_id="test_report_001",
        decision_input=sample_decision_input,
        status=ReportStatus.COMPLETED,
        agent_analyses=[sample_agent_analysis],
        option_evaluations=[sample_option_evaluation],
        risk_assessments=[sample_risk_assessment],
        consensus_analysis=sample_consensus_analysis,
        executive_summary=sample_executive_summary,
        final_recommendation="Based on comprehensive analysis, we recommend proceeding with Option A while implementing strong risk mitigation measures and securing adequate funding.",
        action_items=[sample_action_item],
        report_metrics=sample_report_metrics,
        participants=["investor", "legal", "analyst", "customer", "strategist"],
        analysis_duration=45.5,
        completed_at=datetime.now()
    )


@pytest.fixture
def mock_decision_team(mock_model_client):
    """Create mock decision analysis team for testing."""
    with patch('src.agents.team.DecisionAnalysisTeam') as mock_team:
        mock_instance = Mock()
        mock_instance.agents = []
        mock_instance.model_client = mock_model_client
        mock_instance.max_turns = 20
        mock_team.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def temp_directory():
    """Create temporary directory for testing file operations."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture
def mock_llm_response():
    """Mock LLM response for testing."""
    return {
        "choices": [
            {
                "message": {
                    "content": "This is a test response from the LLM model for decision analysis.",
                    "role": "assistant"
                }
            }
        ]
    }


@pytest.fixture
def sample_conversation_state():
    """Create sample conversation state for testing."""
    return AgentConversation(
        conversation_id="test_conv_001",
        participants=["investor", "legal", "analyst"],
        state=ConversationState.ANALYZING,
        max_turns=10,
        turn_count=5,
        context={"test_key": "test_value"}
    )


# Test utilities
class MockAsyncIterator:
    """Mock async iterator for testing streaming responses."""
    
    def __init__(self, items):
        self.items = items
        self.index = 0
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.index >= len(self.items):
            raise StopAsyncIteration
        item = self.items[self.index]
        self.index += 1
        return item


@pytest.fixture
def mock_stream_response():
    """Mock streaming response for testing."""
    return MockAsyncIterator([
        {"type": "message", "content": "Analyzing decision..."},
        {"type": "message", "content": "Generating recommendations..."},
        {"type": "message", "content": "Analysis complete."}
    ])


# Test data generators
def generate_test_decision_options(count: int = 3) -> List[DecisionOption]:
    """Generate test decision options."""
    options = []
    for i in range(count):
        options.append(DecisionOption(
            name=f"Option {chr(65 + i)}",
            description=f"Test option {i + 1} description"
        ))
    return options


def generate_test_constraints(count: int = 2) -> List[DecisionConstraint]:
    """Generate test decision constraints."""
    constraints = []
    types = ["budget", "timeline", "resource", "regulatory"]
    for i in range(count):
        constraints.append(DecisionConstraint(
            name=f"Constraint {i + 1}",
            description=f"Test constraint {i + 1} description",
            constraint_type=types[i % len(types)],
            value=f"test_value_{i}"
        ))
    return constraints


def generate_test_agent_analyses(count: int = 5) -> List[AgentAnalysis]:
    """Generate test agent analyses."""
    roles = [AgentRole.INVESTOR, AgentRole.LEGAL, AgentRole.ANALYST, AgentRole.CUSTOMER, AgentRole.STRATEGIST]
    analyses = []
    
    for i in range(count):
        analyses.append(AgentAnalysis(
            agent_role=roles[i % len(roles)],
            analysis=f"Test analysis {i + 1} content",
            confidence_level=0.7 + (i * 0.05),
            recommendations=[f"Recommendation {i + 1}"],
            key_insights=[f"Insight {i + 1}"],
            concerns=[f"Concern {i + 1}"]
        ))
    
    return analyses


# Test markers
pytest.mark.unit = pytest.mark.unit
pytest.mark.integration = pytest.mark.integration
pytest.mark.e2e = pytest.mark.e2e
pytest.mark.slow = pytest.mark.slow
pytest.mark.asyncio = pytest.mark.asyncio


# Test environment setup
@pytest.fixture(autouse=True)
def setup_test_environment():
    """Setup test environment variables."""
    os.environ['TESTING'] = 'true'
    os.environ['LOG_LEVEL'] = 'DEBUG'
    yield
    # Cleanup
    if 'TESTING' in os.environ:
        del os.environ['TESTING']