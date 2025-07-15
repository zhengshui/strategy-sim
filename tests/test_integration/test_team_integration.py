"""
Integration tests for multi-agent team functionality in StrategySim AI.

Tests team coordination, decision analysis workflows, and agent interactions.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from typing import Any, Dict, List

from src.agents.team import DecisionAnalysisTeam, create_decision_team, run_decision_analysis
from src.agents.investor_agent import InvestorAgent
from src.agents.legal_agent import LegalAgent
from src.agents.analyst_agent import AnalystAgent
from src.agents.customer_agent import CustomerAgent
from src.agents.strategist_agent import StrategistAgent
from src.models.agent_models import AgentRole, AgentAnalysis, ConversationState
from src.models.decision_models import DecisionInput, DecisionType, DecisionUrgency
from src.models.report_models import DecisionReport


class TestDecisionAnalysisTeam:
    """Test DecisionAnalysisTeam functionality."""
    
    def test_team_initialization(self, mock_model_client):
        """Test team initialization with default configuration."""
        team = DecisionAnalysisTeam(
            model_client=mock_model_client,
            max_turns=10,
            include_all_agents=True
        )
        
        assert team.model_client == mock_model_client
        assert team.max_turns == 10
        assert len(team.agents) == 5  # All 5 standard agents
        assert team.team is not None
        
        # Check that all agent types are present
        agent_roles = [agent.agent_role for agent in team.agents]
        assert AgentRole.INVESTOR in agent_roles
        assert AgentRole.LEGAL in agent_roles
        assert AgentRole.ANALYST in agent_roles
        assert AgentRole.CUSTOMER in agent_roles
        assert AgentRole.STRATEGIST in agent_roles
    
    def test_team_initialization_with_custom_agents(self, mock_model_client):
        """Test team initialization with custom agents."""
        custom_agent = Mock()
        custom_agent.agent_name = "custom_agent"
        custom_agent.agent_role = AgentRole.STRATEGIST
        custom_agent.agent = Mock()  # Mock AutoGen agent
        
        team = DecisionAnalysisTeam(
            model_client=mock_model_client,
            max_turns=10,
            include_all_agents=False,
            custom_agents=[custom_agent]
        )
        
        assert len(team.agents) == 1
        assert team.agents[0] == custom_agent
    
    def test_team_initialization_standard_plus_custom(self, mock_model_client):
        """Test team initialization with standard and custom agents."""
        custom_agent = Mock()
        custom_agent.agent_name = "custom_agent"
        custom_agent.agent_role = AgentRole.STRATEGIST
        custom_agent.agent = Mock()
        
        team = DecisionAnalysisTeam(
            model_client=mock_model_client,
            max_turns=10,
            include_all_agents=True,
            custom_agents=[custom_agent]
        )
        
        assert len(team.agents) == 6  # 5 standard + 1 custom
        assert custom_agent in team.agents
    
    def test_initialize_standard_agents(self, mock_model_client):
        """Test initialization of standard agents."""
        with patch('src.agents.team.InvestorAgent') as mock_investor, \
             patch('src.agents.team.LegalAgent') as mock_legal, \
             patch('src.agents.team.AnalystAgent') as mock_analyst, \
             patch('src.agents.team.CustomerAgent') as mock_customer, \
             patch('src.agents.team.StrategistAgent') as mock_strategist:
            
            # Configure mocks
            mock_investor.return_value.agent_name = "investor"
            mock_legal.return_value.agent_name = "legal_officer"
            mock_analyst.return_value.agent_name = "analyst"
            mock_customer.return_value.agent_name = "customer_representative"
            mock_strategist.return_value.agent_name = "strategic_consultant"
            
            team = DecisionAnalysisTeam(
                model_client=mock_model_client,
                max_turns=10,
                include_all_agents=True
            )
            
            # Check that all agent constructors were called
            mock_investor.assert_called_once()
            mock_legal.assert_called_once()
            mock_analyst.assert_called_once()
            mock_customer.assert_called_once()
            mock_strategist.assert_called_once()
    
    def test_create_selector_group_chat(self, mock_model_client):
        """Test SelectorGroupChat creation."""
        with patch('src.agents.team.SelectorGroupChat') as mock_selector:
            mock_selector.return_value = Mock()
            
            team = DecisionAnalysisTeam(
                model_client=mock_model_client,
                max_turns=10,
                include_all_agents=True
            )
            
            # SelectorGroupChat should be created
            mock_selector.assert_called_once()
            
            # Check call arguments
            call_args = mock_selector.call_args
            assert call_args[1]['model_client'] == mock_model_client
            assert call_args[1]['max_turns'] == 10
            assert 'termination_condition' in call_args[1]
    
    @pytest.mark.asyncio
    async def test_analyze_decision_basic(self, mock_model_client, sample_decision_input):
        """Test basic decision analysis workflow."""
        team = DecisionAnalysisTeam(
            model_client=mock_model_client,
            max_turns=5,
            include_all_agents=True
        )
        
        # Mock the team's run_stream method
        with patch.object(team.team, 'run_stream') as mock_run_stream:
            # Mock streaming messages
            mock_messages = [
                Mock(content="Starting analysis..."),
                Mock(content="Analyzing financial aspects..."),
                Mock(content="Considering legal implications..."),
                Mock(content="CONSENSUS_REACHED: Proceed with Option A")
            ]
            
            async def mock_stream():
                for msg in mock_messages:
                    yield msg
            
            mock_run_stream.return_value = mock_stream()
            
            # Run analysis
            conversation = await team.analyze_decision(sample_decision_input)
            
            # Check results
            assert conversation.conversation_id.startswith("decision_")
            assert conversation.state == ConversationState.CONCLUDED
            assert len(conversation.participants) == 5
            assert conversation.turn_count > 0
    
    @pytest.mark.asyncio
    async def test_analyze_decision_with_conversation_id(self, mock_model_client, sample_decision_input):
        """Test decision analysis with custom conversation ID."""
        team = DecisionAnalysisTeam(
            model_client=mock_model_client,
            max_turns=5,
            include_all_agents=True
        )
        
        custom_id = "custom_conv_123"
        
        with patch.object(team.team, 'run_stream') as mock_run_stream:
            mock_run_stream.return_value = AsyncMock()
            mock_run_stream.return_value.__aiter__.return_value = []
            
            conversation = await team.analyze_decision(
                sample_decision_input,
                conversation_id=custom_id
            )
            
            assert conversation.conversation_id == custom_id
    
    def test_create_initial_message(self, mock_model_client, sample_decision_input):
        """Test creation of initial analysis message."""
        team = DecisionAnalysisTeam(
            model_client=mock_model_client,
            max_turns=5,
            include_all_agents=True
        )
        
        with patch('src.agents.team.get_conversation_starter') as mock_starter:
            mock_starter.return_value = "Starting strategic analysis..."
            
            message = team._create_initial_message(sample_decision_input)
            
            assert message.content is not None
            assert sample_decision_input.title in message.content
            assert sample_decision_input.description in message.content
            assert "CONSENSUS_REACHED" in message.content
            assert message.source == "user"
    
    @pytest.mark.asyncio
    async def test_process_streaming_message(self, mock_model_client, sample_conversation_state):
        """Test processing of streaming messages."""
        team = DecisionAnalysisTeam(
            model_client=mock_model_client,
            max_turns=5,
            include_all_agents=True
        )
        
        mock_message = Mock()
        mock_message.content = "Test message from agent"
        
        initial_turn_count = sample_conversation_state.turn_count
        
        await team._process_streaming_message(mock_message, sample_conversation_state)
        
        # Turn count should be incremented
        assert sample_conversation_state.turn_count == initial_turn_count + 1
    
    @pytest.mark.asyncio
    async def test_process_streaming_message_max_turns(self, mock_model_client, sample_conversation_state):
        """Test processing message when max turns reached."""
        team = DecisionAnalysisTeam(
            model_client=mock_model_client,
            max_turns=5,
            include_all_agents=True
        )
        
        # Set turn count to max
        sample_conversation_state.turn_count = sample_conversation_state.max_turns - 1
        
        mock_message = Mock()
        await team._process_streaming_message(mock_message, sample_conversation_state)
        
        # Should be concluded
        assert sample_conversation_state.state == ConversationState.CONCLUDED
    
    @pytest.mark.asyncio
    async def test_generate_decision_report(self, mock_model_client, sample_decision_input, sample_conversation_state):
        """Test decision report generation."""
        team = DecisionAnalysisTeam(
            model_client=mock_model_client,
            max_turns=5,
            include_all_agents=True
        )
        
        # Mock agent analyses
        with patch.object(team.agents[0], 'analyze_decision') as mock_analyze:
            mock_analyze.return_value = AgentAnalysis(
                agent_role=AgentRole.INVESTOR,
                analysis="Financial analysis shows positive outlook",
                confidence_level=0.8,
                recommendations=["Proceed with investment"],
                key_insights=["Strong ROI potential"],
                concerns=["Market volatility"]
            )
            
            # Generate report
            report = await team.generate_decision_report(
                sample_conversation_state,
                sample_decision_input
            )
            
            # Check report structure
            assert isinstance(report, DecisionReport)
            assert report.report_id.startswith("report_")
            assert report.decision_input == sample_decision_input
            assert len(report.agent_analyses) > 0
            assert report.consensus_analysis is not None
            assert report.executive_summary is not None
            assert report.final_recommendation is not None
            assert report.completed_at is not None
    
    def test_get_team_status(self, mock_model_client):
        """Test getting team status."""
        team = DecisionAnalysisTeam(
            model_client=mock_model_client,
            max_turns=10,
            include_all_agents=True
        )
        
        status = team.get_team_status()
        
        assert isinstance(status, dict)
        assert "team_size" in status
        assert "agents" in status
        assert "configuration" in status
        assert "last_updated" in status
        
        assert status["team_size"] == 5
        assert len(status["agents"]) == 5
        assert status["configuration"]["max_turns"] == 10
        assert status["configuration"]["termination_condition"] == "CONSENSUS_REACHED"
    
    @pytest.mark.asyncio
    async def test_health_check(self, mock_model_client):
        """Test team health check."""
        team = DecisionAnalysisTeam(
            model_client=mock_model_client,
            max_turns=10,
            include_all_agents=True
        )
        
        # Mock agent health checks
        mock_health = {
            "agent_name": "test_agent",
            "status": "healthy",
            "tools_count": 3,
            "model_client_status": "available"
        }
        
        with patch.object(team.agents[0], 'health_check') as mock_agent_health:
            mock_agent_health.return_value = mock_health
            
            # Mock all agents to return healthy
            for agent in team.agents:
                agent.health_check = AsyncMock(return_value=mock_health)
            
            health_results = await team.health_check()
            
            assert health_results["team_status"] == "healthy"
            assert health_results["total_agents"] == 5
            assert health_results["healthy_agents"] == 5
            assert health_results["unhealthy_agents"] == 0
    
    @pytest.mark.asyncio
    async def test_health_check_with_unhealthy_agents(self, mock_model_client):
        """Test health check with some unhealthy agents."""
        team = DecisionAnalysisTeam(
            model_client=mock_model_client,
            max_turns=10,
            include_all_agents=True
        )
        
        # Mock mixed health statuses
        healthy_status = {"status": "healthy"}
        unhealthy_status = {"status": "unhealthy"}
        
        # First 3 agents healthy, last 2 unhealthy
        for i, agent in enumerate(team.agents):
            if i < 3:
                agent.health_check = AsyncMock(return_value=healthy_status)
            else:
                agent.health_check = AsyncMock(return_value=unhealthy_status)
        
        health_results = await team.health_check()
        
        assert health_results["team_status"] == "partially_healthy"
        assert health_results["healthy_agents"] == 3
        assert health_results["unhealthy_agents"] == 2
    
    @pytest.mark.asyncio
    async def test_analyze_decision_error_handling(self, mock_model_client, sample_decision_input):
        """Test error handling in decision analysis."""
        team = DecisionAnalysisTeam(
            model_client=mock_model_client,
            max_turns=5,
            include_all_agents=True
        )
        
        # Mock team to raise exception
        with patch.object(team.team, 'run_stream') as mock_run_stream:
            mock_run_stream.side_effect = Exception("Analysis failed")
            
            with pytest.raises(Exception) as exc_info:
                await team.analyze_decision(sample_decision_input)
            
            assert "Analysis failed" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_generate_report_error_handling(self, mock_model_client, sample_decision_input, sample_conversation_state):
        """Test error handling in report generation."""
        team = DecisionAnalysisTeam(
            model_client=mock_model_client,
            max_turns=5,
            include_all_agents=True
        )
        
        # Mock agent to raise exception
        with patch.object(team.agents[0], 'analyze_decision') as mock_analyze:
            mock_analyze.side_effect = Exception("Agent analysis failed")
            
            with pytest.raises(Exception) as exc_info:
                await team.generate_decision_report(
                    sample_conversation_state,
                    sample_decision_input
                )
            
            assert "Agent analysis failed" in str(exc_info.value)


class TestCreateDecisionTeam:
    """Test create_decision_team utility function."""
    
    def test_create_team_with_defaults(self):
        """Test creating team with default configuration."""
        with patch('src.agents.team.get_model_config') as mock_config, \
             patch('src.agents.team.ChatCompletionClient') as mock_client:
            
            mock_config.return_value = {"model": "test-model"}
            mock_client_instance = Mock()
            mock_client.load_component.return_value = mock_client_instance
            
            team = create_decision_team()
            
            assert isinstance(team, DecisionAnalysisTeam)
            assert team.max_turns == 20  # Default value
            assert len(team.agents) == 5  # All standard agents
    
    def test_create_team_with_custom_client(self, mock_model_client):
        """Test creating team with custom model client."""
        team = create_decision_team(
            model_client=mock_model_client,
            max_turns=15
        )
        
        assert isinstance(team, DecisionAnalysisTeam)
        assert team.model_client == mock_model_client
        assert team.max_turns == 15
    
    def test_create_team_with_custom_agents(self, mock_model_client):
        """Test creating team with custom agents."""
        custom_agent = Mock()
        custom_agent.agent_name = "custom_agent"
        custom_agent.agent_role = AgentRole.STRATEGIST
        custom_agent.agent = Mock()
        
        team = create_decision_team(
            model_client=mock_model_client,
            custom_agents=[custom_agent]
        )
        
        assert isinstance(team, DecisionAnalysisTeam)
        assert len(team.agents) == 6  # 5 standard + 1 custom
        assert custom_agent in team.agents
    
    def test_create_team_error_handling(self):
        """Test error handling in team creation."""
        with patch('src.agents.team.get_model_config') as mock_config:
            mock_config.side_effect = Exception("Config error")
            
            with pytest.raises(Exception) as exc_info:
                create_decision_team()
            
            assert "Config error" in str(exc_info.value)


class TestRunDecisionAnalysis:
    """Test run_decision_analysis utility function."""
    
    @pytest.mark.asyncio
    async def test_run_analysis_with_default_team(self, sample_decision_input):
        """Test running analysis with default team."""
        with patch('src.agents.team.create_decision_team') as mock_create_team:
            mock_team = Mock()
            mock_conversation = Mock()
            mock_conversation.conversation_id = "test_conv"
            mock_report = Mock()
            mock_report.report_id = "test_report"
            
            mock_team.analyze_decision = AsyncMock(return_value=mock_conversation)
            mock_team.generate_decision_report = AsyncMock(return_value=mock_report)
            mock_create_team.return_value = mock_team
            
            result = await run_decision_analysis(sample_decision_input)
            
            assert result == mock_report
            mock_team.analyze_decision.assert_called_once_with(sample_decision_input)
            mock_team.generate_decision_report.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_run_analysis_with_custom_team(self, sample_decision_input, mock_model_client):
        """Test running analysis with custom team."""
        custom_team = DecisionAnalysisTeam(
            model_client=mock_model_client,
            max_turns=5,
            include_all_agents=True
        )
        
        with patch.object(custom_team, 'analyze_decision') as mock_analyze, \
             patch.object(custom_team, 'generate_decision_report') as mock_generate:
            
            mock_conversation = Mock()
            mock_report = Mock()
            mock_analyze.return_value = mock_conversation
            mock_generate.return_value = mock_report
            
            result = await run_decision_analysis(sample_decision_input, custom_team)
            
            assert result == mock_report
            mock_analyze.assert_called_once_with(sample_decision_input)
            mock_generate.assert_called_once_with(mock_conversation, sample_decision_input)
    
    @pytest.mark.asyncio
    async def test_run_analysis_error_handling(self, sample_decision_input):
        """Test error handling in analysis execution."""
        with patch('src.agents.team.create_decision_team') as mock_create_team:
            mock_team = Mock()
            mock_team.analyze_decision = AsyncMock(side_effect=Exception("Analysis failed"))
            mock_create_team.return_value = mock_team
            
            with pytest.raises(Exception) as exc_info:
                await run_decision_analysis(sample_decision_input)
            
            assert "Analysis failed" in str(exc_info.value)


class TestTeamIntegrationScenarios:
    """Test real-world integration scenarios."""
    
    @pytest.mark.asyncio
    async def test_complete_decision_analysis_workflow(self, mock_model_client, sample_decision_input):
        """Test complete decision analysis workflow from start to finish."""
        team = DecisionAnalysisTeam(
            model_client=mock_model_client,
            max_turns=10,
            include_all_agents=True
        )
        
        # Mock all agent analyses
        mock_analyses = []
        for i, agent in enumerate(team.agents):
            mock_analysis = AgentAnalysis(
                agent_role=agent.agent_role,
                analysis=f"Analysis from {agent.agent_name}",
                confidence_level=0.8,
                recommendations=[f"Recommendation from {agent.agent_name}"],
                key_insights=[f"Insight from {agent.agent_name}"],
                concerns=[f"Concern from {agent.agent_name}"]
            )
            agent.analyze_decision = AsyncMock(return_value=mock_analysis)
            mock_analyses.append(mock_analysis)
        
        # Mock team streaming
        with patch.object(team.team, 'run_stream') as mock_run_stream:
            mock_run_stream.return_value = AsyncMock()
            mock_run_stream.return_value.__aiter__.return_value = []
            
            # Run complete workflow
            conversation = await team.analyze_decision(sample_decision_input)
            report = await team.generate_decision_report(conversation, sample_decision_input)
            
            # Verify results
            assert isinstance(conversation, AgentConversation)
            assert isinstance(report, DecisionReport)
            assert report.decision_input == sample_decision_input
            assert len(report.agent_analyses) == 5
            assert report.consensus_analysis is not None
            assert report.executive_summary is not None
    
    @pytest.mark.asyncio
    async def test_team_scalability(self, mock_model_client):
        """Test team performance with multiple concurrent analyses."""
        team = DecisionAnalysisTeam(
            model_client=mock_model_client,
            max_turns=5,
            include_all_agents=True
        )
        
        # Create multiple decision inputs
        decision_inputs = []
        for i in range(3):
            decision_inputs.append(DecisionInput(
                title=f"Decision {i+1}",
                description=f"Test decision {i+1} for scalability testing",
                decision_type=DecisionType.INVESTMENT,
                urgency=DecisionUrgency.MEDIUM,
                options=[],
                constraints=[]
            ))
        
        # Mock team operations
        with patch.object(team.team, 'run_stream') as mock_run_stream:
            mock_run_stream.return_value = AsyncMock()
            mock_run_stream.return_value.__aiter__.return_value = []
            
            # Run multiple analyses concurrently
            tasks = [
                asyncio.create_task(team.analyze_decision(decision_input))
                for decision_input in decision_inputs
            ]
            
            results = await asyncio.gather(*tasks)
            
            # All analyses should complete successfully
            assert len(results) == 3
            for result in results:
                assert isinstance(result, AgentConversation)
                assert result.state == ConversationState.CONCLUDED
    
    @pytest.mark.asyncio
    async def test_team_resilience_with_agent_failures(self, mock_model_client, sample_decision_input):
        """Test team resilience when some agents fail."""
        team = DecisionAnalysisTeam(
            model_client=mock_model_client,
            max_turns=5,
            include_all_agents=True
        )
        
        # Mock some agents to fail
        for i, agent in enumerate(team.agents):
            if i < 3:
                # First 3 agents succeed
                agent.analyze_decision = AsyncMock(return_value=AgentAnalysis(
                    agent_role=agent.agent_role,
                    analysis="Successful analysis",
                    confidence_level=0.8,
                    recommendations=["Test recommendation"],
                    key_insights=["Test insight"],
                    concerns=["Test concern"]
                ))
            else:
                # Last 2 agents fail
                agent.analyze_decision = AsyncMock(side_effect=Exception("Agent failed"))
        
        # Mock team streaming
        with patch.object(team.team, 'run_stream') as mock_run_stream:
            mock_run_stream.return_value = AsyncMock()
            mock_run_stream.return_value.__aiter__.return_value = []
            
            # Analysis should still work with partial failures
            conversation = await team.analyze_decision(sample_decision_input)
            
            # Should handle partial failures gracefully
            assert isinstance(conversation, AgentConversation)
            assert conversation.state == ConversationState.CONCLUDED