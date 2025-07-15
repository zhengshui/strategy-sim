"""
Base agent class with common functionality for StrategySim AI agents.

Contains shared functionality for all specialized agents including
tool registration, error handling, and response formatting.
"""

from typing import Any, Dict, List, Optional, Union
from abc import ABC, abstractmethod
import asyncio
import logging
from datetime import datetime

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core.models import ChatCompletionClient

from ..config.settings import settings
from ..config.prompts import get_agent_prompt, get_agent_description
from ..models.agent_models import (
    AgentRole, AgentResponse, AgentAnalysis, AgentMetrics, 
    ToolResult, AgentRecommendation, AgentConcern
)

# Set up logging
logging.basicConfig(level=getattr(logging, settings.log_level))
logger = logging.getLogger(__name__)


class BaseStrategicAgent(ABC):
    """
    Base class for all strategic agents in StrategySim AI.
    
    Provides common functionality including:
    - Tool registration and management
    - Error handling and logging
    - Response formatting
    - Metrics tracking
    - Communication patterns
    """
    
    def __init__(
        self,
        agent_name: str,
        agent_role: AgentRole,
        model_client: ChatCompletionClient,
        tools: Optional[List[Any]] = None,
        system_message: Optional[str] = None
    ):
        """
        Initialize the base strategic agent.
        
        Args:
            agent_name: Name of the agent
            agent_role: Role of the agent
            model_client: Model client for LLM communication
            tools: List of tools available to the agent
            system_message: Custom system message (optional)
        """
        self.agent_name = agent_name
        self.agent_role = agent_role
        self.model_client = model_client
        self.tools = tools or []
        
        # Get system message from configuration
        self.system_message = system_message or get_agent_prompt(agent_role.value)
        
        # Initialize metrics
        self.metrics = AgentMetrics(
            agent_name=agent_name,
            agent_role=agent_role
        )
        
        # Create AutoGen agent
        self.agent = AssistantAgent(
            name=agent_name,
            model_client=model_client,
            tools=self.tools,
            system_message=self.system_message,
            model_client_stream=True,
            reflect_on_tool_use=True
        )
        
        # Register tools
        self._register_tools()
        
        logger.info(f"Initialized {agent_name} agent with role {agent_role.value}")
    
    def _register_tools(self) -> None:
        """Register tools with the agent."""
        for tool in self.tools:
            try:
                # AutoGen tool registration happens automatically when tools are passed
                # to AssistantAgent constructor
                logger.debug(f"Tool {tool.__name__} registered with {self.agent_name}")
            except Exception as e:
                logger.error(f"Failed to register tool {tool}: {e}")
    
    async def _execute_tool(self, tool_name: str, **kwargs) -> ToolResult:
        """
        Execute a tool safely with error handling.
        
        Args:
            tool_name: Name of the tool to execute
            **kwargs: Tool arguments
        
        Returns:
            ToolResult object
        """
        start_time = datetime.now()
        
        try:
            # Find the tool function
            tool_func = None
            for tool in self.tools:
                if tool.__name__ == tool_name:
                    tool_func = tool
                    break
            
            if not tool_func:
                raise ValueError(f"Tool {tool_name} not found")
            
            # Execute the tool
            result = await tool_func(**kwargs)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Update metrics
            self.metrics.update_metrics(execution_time, True)
            
            return ToolResult(
                tool_name=tool_name,
                success=True,
                result=result,
                execution_time=execution_time
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Update metrics
            self.metrics.update_metrics(execution_time, False)
            
            logger.error(f"Tool {tool_name} execution failed: {e}")
            
            return ToolResult(
                tool_name=tool_name,
                success=False,
                result=None,
                error_message=str(e),
                execution_time=execution_time
            )
    
    async def analyze_decision(
        self,
        decision_context: str,
        decision_data: Dict[str, Any]
    ) -> AgentAnalysis:
        """
        Analyze a decision from the agent's perspective.
        
        Args:
            decision_context: Context of the decision
            decision_data: Decision data
        
        Returns:
            AgentAnalysis object
        """
        try:
            # Create analysis prompt
            analysis_prompt = f"""
            Please analyze the following decision from your perspective as a {self.agent_role.value}:
            
            Decision Context: {decision_context}
            Decision Data: {decision_data}
            
            Provide a comprehensive analysis including:
            1. Your professional assessment
            2. Key considerations from your perspective
            3. Specific recommendations
            4. Potential risks and concerns
            5. Success factors and opportunities
            
            Be specific and actionable in your analysis.
            """
            
            # Get analysis from the agent
            messages = [TextMessage(content=analysis_prompt, source="user")]
            
            # This is a simplified approach - in a real implementation,
            # you'd use the actual AutoGen agent.run() method
            response = await self._get_agent_response(messages)
            
            # Extract structured analysis (simplified)
            analysis = AgentAnalysis(
                agent_name=self.agent_name,
                agent_role=self.agent_role,
                analysis=response,
                risk_level=0.5,  # This would be calculated based on analysis
                confidence=0.8,  # This would be calculated based on analysis
                recommendations=self._extract_recommendations(response),
                concerns=self._extract_concerns(response),
                supporting_data=decision_data
            )
            
            return analysis
            
        except Exception as e:
            logger.error(f"Analysis failed for {self.agent_name}: {e}")
            raise
    
    async def _get_agent_response(self, messages: List[TextMessage]) -> str:
        """
        Get response from the agent.
        
        Args:
            messages: List of messages
        
        Returns:
            Agent response string
        """
        try:
            # This is a simplified implementation
            # In a real implementation, you'd use the AutoGen agent's run method
            response = f"Analysis from {self.agent_name} ({self.agent_role.value}): "
            response += "Based on my expertise, I recommend a thorough evaluation of the decision. "
            response += "Key considerations include risk assessment, stakeholder impact, and strategic alignment. "
            response += "I suggest developing a detailed implementation plan with proper risk mitigation strategies."
            
            return response
            
        except Exception as e:
            logger.error(f"Failed to get response from {self.agent_name}: {e}")
            raise
    
    def _extract_recommendations(self, analysis_text: str) -> List[AgentRecommendation]:
        """
        Extract recommendations from analysis text.
        
        Args:
            analysis_text: Analysis text from agent
        
        Returns:
            List of AgentRecommendation objects
        """
        # This is a simplified extraction - in a real implementation,
        # you'd use NLP or structured prompts to extract recommendations
        recommendations = [
            AgentRecommendation(
                recommendation="Conduct thorough risk assessment",
                rationale="Risk assessment is crucial for informed decision-making",
                confidence=0.9,
                risk_assessment="medium",
                priority="high",
                implementation_difficulty="medium",
                expected_impact="high"
            ),
            AgentRecommendation(
                recommendation="Develop comprehensive implementation plan",
                rationale="Detailed planning ensures successful execution",
                confidence=0.8,
                risk_assessment="low",
                priority="high",
                implementation_difficulty="high",
                expected_impact="high"
            )
        ]
        
        return recommendations
    
    def _extract_concerns(self, analysis_text: str) -> List[AgentConcern]:
        """
        Extract concerns from analysis text.
        
        Args:
            analysis_text: Analysis text from agent
        
        Returns:
            List of AgentConcern objects
        """
        # This is a simplified extraction - in a real implementation,
        # you'd use NLP or structured prompts to extract concerns
        concerns = [
            AgentConcern(
                concern="Potential implementation challenges",
                severity="medium",
                probability=0.6,
                impact="Implementation delays and cost overruns possible",
                mitigation_strategies=["Detailed planning", "Risk monitoring", "Contingency planning"],
                category="operational"
            ),
            AgentConcern(
                concern="Market acceptance uncertainty",
                severity="medium",
                probability=0.4,
                impact="Lower than expected market response",
                mitigation_strategies=["Market research", "Pilot testing", "Phased rollout"],
                category="market"
            )
        ]
        
        return concerns
    
    async def create_response(
        self,
        message: str,
        response_type: str = "analysis",
        target_agent: Optional[str] = None,
        requires_response: bool = False
    ) -> AgentResponse:
        """
        Create a structured agent response.
        
        Args:
            message: Response message
            response_type: Type of response
            target_agent: Target agent (optional)
            requires_response: Whether response is required
        
        Returns:
            AgentResponse object
        """
        try:
            return AgentResponse(
                agent_name=self.agent_name,
                agent_role=self.agent_role,
                message=message,
                response_type=response_type,
                target_agent=target_agent,
                confidence=0.8,  # This would be calculated based on response
                requires_response=requires_response
            )
            
        except Exception as e:
            logger.error(f"Failed to create response for {self.agent_name}: {e}")
            raise
    
    @abstractmethod
    def get_specialized_tools(self) -> List[Any]:
        """
        Get tools specific to this agent type.
        
        Returns:
            List of specialized tools
        """
        pass
    
    @abstractmethod
    async def perform_specialized_analysis(
        self,
        decision_context: str,
        decision_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Perform analysis specific to this agent type.
        
        Args:
            decision_context: Context of the decision
            decision_data: Decision data
        
        Returns:
            Dictionary with specialized analysis results
        """
        pass
    
    def get_agent_description(self) -> str:
        """
        Get description of the agent's role and capabilities.
        
        Returns:
            Agent description string
        """
        return get_agent_description(self.agent_role.value)
    
    def get_metrics(self) -> AgentMetrics:
        """
        Get current agent metrics.
        
        Returns:
            AgentMetrics object
        """
        return self.metrics
    
    def reset_metrics(self) -> None:
        """Reset agent metrics."""
        self.metrics = AgentMetrics(
            agent_name=self.agent_name,
            agent_role=self.agent_role
        )
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Perform health check on the agent.
        
        Returns:
            Dictionary with health check results
        """
        try:
            # Test basic functionality
            test_message = "Health check test"
            response = await self.create_response(test_message)
            
            return {
                "agent_name": self.agent_name,
                "agent_role": self.agent_role.value,
                "status": "healthy",
                "tools_count": len(self.tools),
                "metrics": self.metrics.dict(),
                "last_check": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Health check failed for {self.agent_name}: {e}")
            return {
                "agent_name": self.agent_name,
                "agent_role": self.agent_role.value,
                "status": "unhealthy",
                "error": str(e),
                "last_check": datetime.now().isoformat()
            }
    
    def __str__(self) -> str:
        """String representation of the agent."""
        return f"{self.agent_name} ({self.agent_role.value})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the agent."""
        return f"BaseStrategicAgent(name='{self.agent_name}', role='{self.agent_role.value}', tools={len(self.tools)})"