"""
Agent package for StrategySim AI.

Contains specialized AI agents for different professional perspectives:
- InvestorAgent: Aggressive financial analysis
- LegalAgent: Conservative compliance focus
- AnalystAgent: Pessimistic risk modeling
- CustomerAgent: Market and user behavior analysis
- StrategistAgent: Strategic synthesis and integration
"""

from .base_agent import BaseStrategicAgent
from .investor_agent import InvestorAgent
from .legal_agent import LegalAgent
from .analyst_agent import AnalystAgent
from .customer_agent import CustomerAgent
from .strategist_agent import StrategistAgent
from .team import DecisionAnalysisTeam, create_decision_team, run_decision_analysis

__all__ = [
    "BaseStrategicAgent",
    "InvestorAgent",
    "LegalAgent",
    "AnalystAgent",
    "CustomerAgent",
    "StrategistAgent",
    "DecisionAnalysisTeam",
    "create_decision_team",
    "run_decision_analysis"
]