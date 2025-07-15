"""
Strategist Agent implementation for StrategySim AI.

Provides strategic synthesis and balanced recommendations.
"""

from typing import Any, Dict, List, Optional
import logging

from autogen_core.models import ChatCompletionClient

from .base_agent import BaseStrategicAgent
from ..models.agent_models import AgentRole
from ..tools.strategic_frameworks import (
    perform_swot_analysis,
    perform_porter_five_forces,
    build_decision_tree,
    evaluate_strategic_options,
    synthesize_strategic_analysis
)

logger = logging.getLogger(__name__)


class StrategistAgent(BaseStrategicAgent):
    """
    Strategist Agent for strategic synthesis and balanced recommendations.
    """
    
    def __init__(
        self,
        agent_name: str = "strategic_consultant",
        model_client: ChatCompletionClient = None,
        custom_tools: Optional[List[Any]] = None
    ):
        specialized_tools = self.get_specialized_tools()
        if custom_tools:
            specialized_tools.extend(custom_tools)
        
        super().__init__(
            agent_name=agent_name,
            agent_role=AgentRole.STRATEGIST,
            model_client=model_client,
            tools=specialized_tools
        )
    
    def get_specialized_tools(self) -> List[Any]:
        return [
            perform_swot_analysis,
            perform_porter_five_forces,
            build_decision_tree,
            evaluate_strategic_options,
            synthesize_strategic_analysis
        ]
    
    async def perform_specialized_analysis(
        self,
        decision_context: str,
        decision_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Perform strategic analysis from strategist perspective."""
        try:
            analysis_results = {}
            
            # Basic strategic assessment
            analysis_results["strategic_assessment"] = {
                "strategic_alignment": "high",
                "implementation_complexity": "medium",
                "strategic_priorities": [
                    "Market positioning",
                    "Competitive advantage",
                    "Resource allocation",
                    "Risk management"
                ],
                "recommendations": [
                    "Develop comprehensive strategic plan",
                    "Align with organizational objectives",
                    "Ensure resource availability",
                    "Monitor strategic progress"
                ]
            }
            
            return analysis_results
            
        except Exception as e:
            logger.error(f"Specialized analysis failed for {self.agent_name}: {e}")
            raise