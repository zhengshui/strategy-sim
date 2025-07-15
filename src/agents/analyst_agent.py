"""
Analyst Agent implementation for StrategySim AI.

Provides pessimistic analytical perspective with quantitative risk modeling.
"""

from typing import Any, Dict, List, Optional
import logging

from autogen_core.models import ChatCompletionClient

from .base_agent import BaseStrategicAgent
from ..models.agent_models import AgentRole
from ..tools.risk_modeler import (
    run_monte_carlo_simulation,
    perform_scenario_analysis,
    calculate_sensitivity_analysis,
    calculate_risk_metrics,
    perform_comprehensive_risk_assessment
)

logger = logging.getLogger(__name__)


class AnalystAgent(BaseStrategicAgent):
    """
    Analyst Agent for pessimistic analytical perspective and risk modeling.
    """
    
    def __init__(
        self,
        agent_name: str = "analyst",
        model_client: ChatCompletionClient = None,
        custom_tools: Optional[List[Any]] = None
    ):
        specialized_tools = self.get_specialized_tools()
        if custom_tools:
            specialized_tools.extend(custom_tools)
        
        super().__init__(
            agent_name=agent_name,
            agent_role=AgentRole.ANALYST,
            model_client=model_client,
            tools=specialized_tools
        )
    
    def get_specialized_tools(self) -> List[Any]:
        return [
            run_monte_carlo_simulation,
            perform_scenario_analysis,
            calculate_sensitivity_analysis,
            calculate_risk_metrics,
            perform_comprehensive_risk_assessment
        ]
    
    async def perform_specialized_analysis(
        self,
        decision_context: str,
        decision_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Perform risk analysis from analyst perspective."""
        try:
            analysis_results = {}
            
            # Basic risk assessment
            analysis_results["risk_assessment"] = {
                "overall_risk_score": 0.6,
                "key_risk_factors": [
                    "Market volatility",
                    "Competitive response",
                    "Execution risk",
                    "Economic uncertainty"
                ],
                "recommendations": [
                    "Conduct comprehensive risk analysis",
                    "Develop contingency plans",
                    "Monitor key risk indicators",
                    "Consider phased implementation"
                ]
            }
            
            return analysis_results
            
        except Exception as e:
            logger.error(f"Specialized analysis failed for {self.agent_name}: {e}")
            raise