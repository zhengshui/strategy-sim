"""
Customer Agent implementation for StrategySim AI.

Provides customer-centric perspective with market research capabilities.
"""

from typing import Any, Dict, List, Optional
import logging

from autogen_core.models import ChatCompletionClient

from .base_agent import BaseStrategicAgent
from ..models.agent_models import AgentRole
from ..tools.market_research import (
    analyze_market_opportunity,
    analyze_competitors,
    map_customer_journey,
    perform_comprehensive_market_research
)

logger = logging.getLogger(__name__)


class CustomerAgent(BaseStrategicAgent):
    """
    Customer Agent for customer-centric perspective and market research.
    """
    
    def __init__(
        self,
        agent_name: str = "customer_representative",
        model_client: ChatCompletionClient = None,
        custom_tools: Optional[List[Any]] = None
    ):
        specialized_tools = self.get_specialized_tools()
        if custom_tools:
            specialized_tools.extend(custom_tools)
        
        super().__init__(
            agent_name=agent_name,
            agent_role=AgentRole.CUSTOMER,
            model_client=model_client,
            tools=specialized_tools
        )
    
    def get_specialized_tools(self) -> List[Any]:
        return [
            analyze_market_opportunity,
            analyze_competitors,
            map_customer_journey,
            perform_comprehensive_market_research
        ]
    
    async def perform_specialized_analysis(
        self,
        decision_context: str,
        decision_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Perform customer analysis from customer perspective."""
        try:
            analysis_results = {}
            
            # Basic customer impact assessment
            analysis_results["customer_impact"] = {
                "customer_satisfaction_impact": "moderate",
                "market_acceptance_likelihood": 0.7,
                "key_customer_concerns": [
                    "Price sensitivity",
                    "Product quality",
                    "Service availability",
                    "Brand trust"
                ],
                "recommendations": [
                    "Conduct customer research",
                    "Develop customer communication plan",
                    "Monitor customer feedback",
                    "Implement customer support measures"
                ]
            }
            
            return analysis_results
            
        except Exception as e:
            logger.error(f"Specialized analysis failed for {self.agent_name}: {e}")
            raise