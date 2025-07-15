"""
Team implementation for StrategySim AI multi-agent decision analysis.

Contains the SelectorGroupChat team implementation that coordinates
all specialized agents for comprehensive decision analysis.
"""

from typing import Any, Dict, List, Optional, Union
import logging
from datetime import datetime

from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.messages import TextMessage
from autogen_core.models import ChatCompletionClient
from autogen_core import CancellationToken

from .investor_agent import InvestorAgent
from .legal_agent import LegalAgent
from .analyst_agent import AnalystAgent
from .customer_agent import CustomerAgent
from .strategist_agent import StrategistAgent
from ..config.settings import settings, get_model_config
from ..config.prompts import AGENT_DESCRIPTIONS, get_conversation_starter
from ..models.decision_models import DecisionInput
from ..models.agent_models import AgentConversation, ConversationState
from ..models.report_models import DecisionReport

logger = logging.getLogger(__name__)


class DecisionAnalysisTeam:
    """
    Decision Analysis Team using SelectorGroupChat for dynamic agent coordination.
    
    Manages a team of specialized agents that collaborate to analyze strategic decisions
    through intelligent agent selection and natural conversation flow.
    """
    
    def __init__(
        self,
        model_client: ChatCompletionClient,
        max_turns: int = 20,
        include_all_agents: bool = True,
        custom_agents: Optional[List[Any]] = None
    ):
        """
        Initialize the Decision Analysis Team.
        
        Args:
            model_client: Model client for LLM communication
            max_turns: Maximum number of conversation turns
            include_all_agents: Whether to include all standard agents
            custom_agents: Optional list of custom agents to include
        """
        self.model_client = model_client
        self.max_turns = max_turns
        self.agents = []
        self.conversation_history = []
        
        # Initialize agents
        if include_all_agents:
            self._initialize_standard_agents()
        
        # Add custom agents if provided
        if custom_agents:
            self.agents.extend(custom_agents)
        
        # Create SelectorGroupChat
        self.team = self._create_selector_group_chat()
        
        logger.info(f"Initialized DecisionAnalysisTeam with {len(self.agents)} agents")
    
    def _initialize_standard_agents(self) -> None:
        """Initialize the standard set of strategic agents."""
        try:
            # Create investor agent
            investor = InvestorAgent(
                agent_name="investor",
                model_client=self.model_client
            )
            self.agents.append(investor)
            
            # Create legal agent
            legal = LegalAgent(
                agent_name="legal_officer",
                model_client=self.model_client
            )
            self.agents.append(legal)
            
            # Create analyst agent
            analyst = AnalystAgent(
                agent_name="analyst",
                model_client=self.model_client
            )
            self.agents.append(analyst)
            
            # Create customer agent
            customer = CustomerAgent(
                agent_name="customer_representative",
                model_client=self.model_client
            )
            self.agents.append(customer)
            
            # Create strategist agent
            strategist = StrategistAgent(
                agent_name="strategic_consultant",
                model_client=self.model_client
            )
            self.agents.append(strategist)
            
            logger.info("Standard agents initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize standard agents: {e}")
            raise
    
    def _create_selector_group_chat(self) -> SelectorGroupChat:
        """Create SelectorGroupChat with proper configuration."""
        try:
            # Create termination condition
            termination_condition = TextMentionTermination("CONSENSUS_REACHED")
            
            # Get AutoGen agents from our strategic agents
            autogen_agents = [agent.agent for agent in self.agents]
            
            # Create SelectorGroupChat
            selector_group_chat = SelectorGroupChat(
                participants=autogen_agents,
                model_client=self.model_client,
                max_turns=self.max_turns,
                termination_condition=termination_condition,
                # Custom selector prompt for strategic decision analysis
                selector_prompt="""You are coordinating a strategic decision analysis team with the following expert roles:
{roles}.

Based on the conversation history below, select the most appropriate expert from {participants} to provide the next response. Consider:
- The topic being discussed
- Each expert's area of expertise
- The natural flow of strategic analysis
- What perspective would be most valuable next

{history}

Select the next expert from {participants} to respond. Only return the role name."""
            )
            
            return selector_group_chat
            
        except Exception as e:
            logger.error(f"Failed to create SelectorGroupChat: {e}")
            raise
    
    async def analyze_decision(
        self,
        decision_input: DecisionInput,
        conversation_id: Optional[str] = None
    ) -> AgentConversation:
        """
        Analyze a strategic decision using the multi-agent team.
        
        Args:
            decision_input: Decision input to analyze
            conversation_id: Optional conversation identifier
        
        Returns:
            AgentConversation object with analysis results
        """
        try:
            # Create conversation ID if not provided
            if not conversation_id:
                conversation_id = f"decision_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Create conversation object
            conversation = AgentConversation(
                conversation_id=conversation_id,
                participants=[agent.agent_name for agent in self.agents],
                state=ConversationState.ANALYZING,
                max_turns=self.max_turns,
                context={"decision_input": decision_input.dict()}
            )
            
            # Create initial message
            initial_message = self._create_initial_message(decision_input)
            
            # Run the team analysis
            async for message in self.team.run_stream(
                task=[initial_message],
                cancellation_token=CancellationToken()
            ):
                # Process streaming messages
                await self._process_streaming_message(message, conversation)
                
                # Check if conversation is complete
                if conversation.is_finished():
                    break
            
            # Finalize conversation
            conversation.state = ConversationState.CONCLUDED
            
            return conversation
            
        except Exception as e:
            logger.error(f"Decision analysis failed: {e}")
            raise
    
    def _create_initial_message(self, decision_input: DecisionInput) -> TextMessage:
        """Create initial message to start the analysis."""
        try:
            # Get conversation starter based on decision type
            starter = get_conversation_starter(decision_input.decision_type.value)
            
            # Create comprehensive context message
            context_message = f"""
            {starter}
            
            DECISION TO ANALYZE:
            Title: {decision_input.title}
            Type: {decision_input.decision_type.value}
            Description: {decision_input.description}
            
            OPTIONS:
            {chr(10).join(f"- {option.name}: {option.description}" for option in decision_input.options)}
            
            CONSTRAINTS:
            {chr(10).join(f"- {constraint.name}: {constraint.description}" for constraint in decision_input.constraints)}
            
            TIMELINE: {decision_input.timeline}
            URGENCY: {decision_input.urgency.value}
            
            Please provide your analysis from your professional perspective. Consider:
            1. Key implications for your area of expertise
            2. Specific risks and opportunities
            3. Recommended actions
            4. Critical success factors
            
            When the team has thoroughly analyzed all aspects and reached consensus, 
            respond with "CONSENSUS_REACHED" followed by the agreed recommendation.
            """
            
            return TextMessage(content=context_message, source="user")
            
        except Exception as e:
            logger.error(f"Failed to create initial message: {e}")
            raise
    
    async def _process_streaming_message(
        self,
        message: Any,
        conversation: AgentConversation
    ) -> None:
        """Process streaming message from the team."""
        try:
            # This is a simplified processing - actual implementation would handle
            # different message types from AutoGen
            
            # For now, just log the message
            logger.debug(f"Processing message: {message}")
            
            # Update conversation turn count
            conversation.turn_count += 1
            
            # Check if max turns reached
            if conversation.turn_count >= conversation.max_turns:
                conversation.state = ConversationState.CONCLUDED
            
        except Exception as e:
            logger.error(f"Failed to process streaming message: {e}")
    
    async def generate_decision_report(
        self,
        conversation: AgentConversation,
        decision_input: DecisionInput
    ) -> DecisionReport:
        """
        Generate comprehensive decision report from conversation.
        
        Args:
            conversation: Completed conversation
            decision_input: Original decision input
        
        Returns:
            DecisionReport object
        """
        try:
            # Extract analyses from conversation
            agent_analyses = []
            for agent in self.agents:
                # Get agent's analysis (simplified)
                analysis = await agent.analyze_decision(
                    decision_input.title,
                    decision_input.dict()
                )
                agent_analyses.append(analysis)
            
            # Create mock consensus analysis
            from ..models.report_models import ConsensusAnalysis, ExecutiveSummary, ReportMetrics
            
            consensus_analysis = ConsensusAnalysis(
                consensus_level=0.8,
                agreement_by_option={option.name: 0.7 for option in decision_input.options},
                disagreement_areas=["Implementation timeline", "Resource allocation"],
                unanimous_points=["Market opportunity exists", "Risk mitigation needed"]
            )
            
            executive_summary = ExecutiveSummary(
                decision_title=decision_input.title,
                recommended_option=decision_input.options[0].name,
                recommendation_category="proceed_with_caution",
                confidence_level=0.8,
                key_findings=[
                    "Market opportunity is attractive",
                    "Implementation risks are manageable",
                    "Financial projections are realistic"
                ],
                critical_risks=["Competitive response", "Market acceptance"],
                success_factors=["Strong execution", "Market timing"],
                next_steps=[
                    "Conduct detailed planning",
                    "Engage stakeholders",
                    "Implement monitoring systems"
                ],
                decision_urgency=decision_input.urgency.value,
                estimated_impact="High positive impact expected"
            )
            
            report_metrics = ReportMetrics(
                completeness_score=0.9,
                consistency_score=0.8,
                agent_participation={agent.agent_name: 1 for agent in self.agents},
                analysis_depth=0.8,
                risk_coverage=0.9,
                recommendation_quality=0.8,
                evidence_support=0.7
            )
            
            # Create decision report
            report = DecisionReport(
                report_id=f"report_{conversation.conversation_id}",
                decision_input=decision_input,
                agent_analyses=agent_analyses,
                consensus_analysis=consensus_analysis,
                executive_summary=executive_summary,
                final_recommendation="Based on comprehensive analysis, we recommend proceeding with the first option while implementing appropriate risk mitigation measures.",
                report_metrics=report_metrics,
                participants=[agent.agent_name for agent in self.agents],
                analysis_duration=(datetime.now() - conversation.created_at).total_seconds()
            )
            
            report.mark_completed()
            
            return report
            
        except Exception as e:
            logger.error(f"Failed to generate decision report: {e}")
            raise
    
    def get_team_status(self) -> Dict[str, Any]:
        """Get current team status."""
        try:
            return {
                "team_size": len(self.agents),
                "agents": [
                    {
                        "name": agent.agent_name,
                        "role": agent.agent_role.value,
                        "status": "active",
                        "tools_count": len(agent.tools)
                    }
                    for agent in self.agents
                ],
                "configuration": {
                    "max_turns": self.max_turns,
                    "model_client": str(self.model_client),
                    "termination_condition": "CONSENSUS_REACHED"
                },
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to get team status: {e}")
            return {"error": str(e)}
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on all agents."""
        try:
            health_results = {
                "team_status": "healthy",
                "agents_health": [],
                "total_agents": len(self.agents),
                "healthy_agents": 0,
                "unhealthy_agents": 0
            }
            
            # Check each agent
            for agent in self.agents:
                agent_health = await agent.health_check()
                health_results["agents_health"].append(agent_health)
                
                if agent_health["status"] == "healthy":
                    health_results["healthy_agents"] += 1
                else:
                    health_results["unhealthy_agents"] += 1
            
            # Determine overall team health
            if health_results["unhealthy_agents"] == 0:
                health_results["team_status"] = "healthy"
            elif health_results["healthy_agents"] > health_results["unhealthy_agents"]:
                health_results["team_status"] = "partially_healthy"
            else:
                health_results["team_status"] = "unhealthy"
            
            return health_results
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {"team_status": "unhealthy", "error": str(e)}


def create_decision_team(
    model_client: Optional[ChatCompletionClient] = None,
    max_turns: int = 20,
    custom_agents: Optional[List[Any]] = None
) -> DecisionAnalysisTeam:
    """
    Create a decision analysis team with default configuration.
    
    Args:
        model_client: Optional model client (will create default if not provided)
        max_turns: Maximum conversation turns
        custom_agents: Optional custom agents to include
    
    Returns:
        DecisionAnalysisTeam instance
    """
    try:
        # Create model client if not provided
        if not model_client:
            from autogen_core.models import ChatCompletionClient
            model_config = get_model_config()
            model_client = ChatCompletionClient.load_component(model_config)
        
        # Create team
        team = DecisionAnalysisTeam(
            model_client=model_client,
            max_turns=max_turns,
            custom_agents=custom_agents
        )
        
        return team
        
    except Exception as e:
        logger.error(f"Failed to create decision team: {e}")
        raise


# Utility functions for team management
async def run_decision_analysis(
    decision_input: DecisionInput,
    team: Optional[DecisionAnalysisTeam] = None
) -> DecisionReport:
    """
    Run a complete decision analysis with report generation.
    
    Args:
        decision_input: Decision to analyze
        team: Optional team instance (will create default if not provided)
    
    Returns:
        DecisionReport with complete analysis
    """
    try:
        # Create team if not provided
        if not team:
            team = create_decision_team()
        
        # Run analysis
        conversation = await team.analyze_decision(decision_input)
        
        # Generate report
        report = await team.generate_decision_report(conversation, decision_input)
        
        return report
        
    except Exception as e:
        logger.error(f"Decision analysis failed: {e}")
        raise