"""
Unit tests for base agent functionality in StrategySim AI.

Tests common agent functionality, tool registration, and error handling.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from typing import Any, Dict, List

from src.agents.base_agent import BaseStrategicAgent
from src.models.agent_models import AgentRole, AgentAnalysis, AgentMetrics
from src.config.settings import settings


class TestBaseStrategicAgent:
    """Test BaseStrategicAgent functionality."""
    
    def test_base_agent_initialization(self, mock_model_client):
        """Test basic agent initialization."""
        agent = BaseStrategicAgent(
            agent_name="test_agent",
            agent_role=AgentRole.INVESTOR,
            model_client=mock_model_client,
            tools=[]
        )
        
        assert agent.agent_name == "test_agent"
        assert agent.agent_role == AgentRole.INVESTOR
        assert agent.model_client == mock_model_client
        assert len(agent.tools) == 0
        assert agent.metrics is not None
        assert agent.system_prompt is not None
    
    def test_agent_initialization_with_tools(self, mock_model_client):
        """Test agent initialization with tools."""
        mock_tools = [Mock(), Mock(), Mock()]
        
        agent = BaseStrategicAgent(
            agent_name="test_agent",
            agent_role=AgentRole.INVESTOR,
            model_client=mock_model_client,
            tools=mock_tools
        )
        
        assert len(agent.tools) == 3
        assert agent.tools == mock_tools
    
    def test_agent_name_validation(self, mock_model_client):
        """Test agent name validation."""
        # Empty name should raise error
        with pytest.raises(ValueError) as exc_info:
            BaseStrategicAgent(
                agent_name="",
                agent_role=AgentRole.INVESTOR,
                model_client=mock_model_client,
                tools=[]
            )
        
        assert "Agent name cannot be empty" in str(exc_info.value)
        
        # None name should raise error
        with pytest.raises(ValueError) as exc_info:
            BaseStrategicAgent(
                agent_name=None,
                agent_role=AgentRole.INVESTOR,
                model_client=mock_model_client,
                tools=[]
            )
        
        assert "Agent name cannot be empty" in str(exc_info.value)
    
    def test_model_client_validation(self, mock_model_client):
        """Test model client validation."""
        # None client should raise error
        with pytest.raises(ValueError) as exc_info:
            BaseStrategicAgent(
                agent_name="test_agent",
                agent_role=AgentRole.INVESTOR,
                model_client=None,
                tools=[]
            )
        
        assert "Model client is required" in str(exc_info.value)
    
    def test_system_prompt_generation(self, mock_model_client):
        """Test system prompt generation."""
        agent = BaseStrategicAgent(
            agent_name="test_agent",
            agent_role=AgentRole.INVESTOR,
            model_client=mock_model_client,
            tools=[]
        )
        
        prompt = agent.system_prompt
        assert isinstance(prompt, str)
        assert len(prompt) > 0
        assert "investor" in prompt.lower()
        assert "financial" in prompt.lower()
    
    def test_register_tool(self, mock_model_client):
        """Test tool registration."""
        agent = BaseStrategicAgent(
            agent_name="test_agent",
            agent_role=AgentRole.INVESTOR,
            model_client=mock_model_client,
            tools=[]
        )
        
        mock_tool = Mock()
        mock_tool.__name__ = "test_tool"
        
        agent.register_tool(mock_tool)
        assert len(agent.tools) == 1
        assert agent.tools[0] == mock_tool
    
    def test_register_multiple_tools(self, mock_model_client):
        """Test registering multiple tools."""
        agent = BaseStrategicAgent(
            agent_name="test_agent",
            agent_role=AgentRole.INVESTOR,
            model_client=mock_model_client,
            tools=[]
        )
        
        mock_tools = [Mock(), Mock(), Mock()]
        for i, tool in enumerate(mock_tools):
            tool.__name__ = f"test_tool_{i}"
        
        agent.register_tools(mock_tools)
        assert len(agent.tools) == 3
        assert agent.tools == mock_tools
    
    def test_unregister_tool(self, mock_model_client):
        """Test tool unregistration."""
        mock_tool = Mock()
        mock_tool.__name__ = "test_tool"
        
        agent = BaseStrategicAgent(
            agent_name="test_agent",
            agent_role=AgentRole.INVESTOR,
            model_client=mock_model_client,
            tools=[mock_tool]
        )
        
        assert len(agent.tools) == 1
        
        agent.unregister_tool("test_tool")
        assert len(agent.tools) == 0
    
    def test_unregister_nonexistent_tool(self, mock_model_client):
        """Test unregistering non-existent tool."""
        agent = BaseStrategicAgent(
            agent_name="test_agent",
            agent_role=AgentRole.INVESTOR,
            model_client=mock_model_client,
            tools=[]
        )
        
        # Should not raise error
        agent.unregister_tool("nonexistent_tool")
        assert len(agent.tools) == 0
    
    def test_get_tool_names(self, mock_model_client):
        """Test getting tool names."""
        mock_tools = [Mock(), Mock(), Mock()]
        for i, tool in enumerate(mock_tools):
            tool.__name__ = f"test_tool_{i}"
        
        agent = BaseStrategicAgent(
            agent_name="test_agent",
            agent_role=AgentRole.INVESTOR,
            model_client=mock_model_client,
            tools=mock_tools
        )
        
        tool_names = agent.get_tool_names()
        assert len(tool_names) == 3
        assert "test_tool_0" in tool_names
        assert "test_tool_1" in tool_names
        assert "test_tool_2" in tool_names
    
    def test_has_tool(self, mock_model_client):
        """Test checking if agent has tool."""
        mock_tool = Mock()
        mock_tool.__name__ = "test_tool"
        
        agent = BaseStrategicAgent(
            agent_name="test_agent",
            agent_role=AgentRole.INVESTOR,
            model_client=mock_model_client,
            tools=[mock_tool]
        )
        
        assert agent.has_tool("test_tool") is True
        assert agent.has_tool("nonexistent_tool") is False
    
    @pytest.mark.asyncio
    async def test_analyze_decision_abstract_method(self, mock_model_client):
        """Test that analyze_decision is abstract and must be implemented."""
        agent = BaseStrategicAgent(
            agent_name="test_agent",
            agent_role=AgentRole.INVESTOR,
            model_client=mock_model_client,
            tools=[]
        )
        
        with pytest.raises(NotImplementedError):
            await agent.analyze_decision("test_decision", {})
    
    @pytest.mark.asyncio
    async def test_perform_specialized_analysis_abstract_method(self, mock_model_client):
        """Test that perform_specialized_analysis is abstract and must be implemented."""
        agent = BaseStrategicAgent(
            agent_name="test_agent",
            agent_role=AgentRole.INVESTOR,
            model_client=mock_model_client,
            tools=[]
        )
        
        with pytest.raises(NotImplementedError):
            await agent.perform_specialized_analysis("test_context", {})
    
    def test_update_metrics(self, mock_model_client):
        """Test updating agent metrics."""
        agent = BaseStrategicAgent(
            agent_name="test_agent",
            agent_role=AgentRole.INVESTOR,
            model_client=mock_model_client,
            tools=[]
        )
        
        # Initial metrics
        initial_analyses = agent.metrics.total_analyses
        initial_confidence = agent.metrics.average_confidence
        
        # Update metrics
        agent.update_metrics(
            analysis_count=5,
            confidence_score=0.85,
            response_time=2.5,
            quality_score=0.9
        )
        
        assert agent.metrics.total_analyses == initial_analyses + 5
        # Confidence should be updated (weighted average)
        assert agent.metrics.average_confidence != initial_confidence
        assert agent.metrics.response_time == 2.5
        assert agent.metrics.quality_score == 0.9
    
    def test_reset_metrics(self, mock_model_client):
        """Test resetting agent metrics."""
        agent = BaseStrategicAgent(
            agent_name="test_agent",
            agent_role=AgentRole.INVESTOR,
            model_client=mock_model_client,
            tools=[]
        )
        
        # Update metrics first
        agent.update_metrics(
            analysis_count=5,
            confidence_score=0.85,
            response_time=2.5,
            quality_score=0.9
        )
        
        # Reset metrics
        agent.reset_metrics()
        
        assert agent.metrics.total_analyses == 0
        assert agent.metrics.average_confidence == 0.0
        assert agent.metrics.response_time == 0.0
        assert agent.metrics.quality_score == 0.0
    
    def test_get_metrics_summary(self, mock_model_client):
        """Test getting metrics summary."""
        agent = BaseStrategicAgent(
            agent_name="test_agent",
            agent_role=AgentRole.INVESTOR,
            model_client=mock_model_client,
            tools=[]
        )
        
        # Update metrics
        agent.update_metrics(
            analysis_count=10,
            confidence_score=0.8,
            response_time=3.0,
            quality_score=0.85
        )
        
        summary = agent.get_metrics_summary()
        
        assert isinstance(summary, dict)
        assert "agent_name" in summary
        assert "agent_role" in summary
        assert "total_analyses" in summary
        assert "average_confidence" in summary
        assert "response_time" in summary
        assert "quality_score" in summary
        assert "performance_category" in summary
        
        assert summary["agent_name"] == "test_agent"
        assert summary["agent_role"] == AgentRole.INVESTOR.value
        assert summary["total_analyses"] == 10
        assert summary["quality_score"] == 0.85
    
    @pytest.mark.asyncio
    async def test_health_check(self, mock_model_client):
        """Test agent health check."""
        agent = BaseStrategicAgent(
            agent_name="test_agent",
            agent_role=AgentRole.INVESTOR,
            model_client=mock_model_client,
            tools=[]
        )
        
        health_status = await agent.health_check()
        
        assert isinstance(health_status, dict)
        assert "agent_name" in health_status
        assert "status" in health_status
        assert "tools_count" in health_status
        assert "model_client_status" in health_status
        assert "last_activity" in health_status
        
        assert health_status["agent_name"] == "test_agent"
        assert health_status["status"] == "healthy"
        assert health_status["tools_count"] == 0
        assert health_status["model_client_status"] == "available"
    
    @pytest.mark.asyncio
    async def test_health_check_with_tools(self, mock_model_client):
        """Test health check with tools."""
        mock_tools = [Mock(), Mock()]
        for i, tool in enumerate(mock_tools):
            tool.__name__ = f"test_tool_{i}"
        
        agent = BaseStrategicAgent(
            agent_name="test_agent",
            agent_role=AgentRole.INVESTOR,
            model_client=mock_model_client,
            tools=mock_tools
        )
        
        health_status = await agent.health_check()
        
        assert health_status["tools_count"] == 2
        assert health_status["status"] == "healthy"
    
    def test_agent_configuration_properties(self, mock_model_client):
        """Test agent configuration properties."""
        agent = BaseStrategicAgent(
            agent_name="test_agent",
            agent_role=AgentRole.INVESTOR,
            model_client=mock_model_client,
            tools=[]
        )
        
        # Test configuration properties
        assert hasattr(agent, 'max_response_time')
        assert hasattr(agent, 'confidence_threshold')
        assert hasattr(agent, 'enable_analysis_cache')
        
        # Test default values
        assert agent.max_response_time > 0
        assert 0 <= agent.confidence_threshold <= 1
        assert isinstance(agent.enable_analysis_cache, bool)
    
    def test_agent_string_representation(self, mock_model_client):
        """Test agent string representation."""
        agent = BaseStrategicAgent(
            agent_name="test_agent",
            agent_role=AgentRole.INVESTOR,
            model_client=mock_model_client,
            tools=[]
        )
        
        str_repr = str(agent)
        assert "test_agent" in str_repr
        assert "investor" in str_repr.lower()
        
        repr_str = repr(agent)
        assert "BaseStrategicAgent" in repr_str
        assert "test_agent" in repr_str
        assert "investor" in repr_str.lower()
    
    def test_agent_equality(self, mock_model_client):
        """Test agent equality comparison."""
        agent1 = BaseStrategicAgent(
            agent_name="test_agent",
            agent_role=AgentRole.INVESTOR,
            model_client=mock_model_client,
            tools=[]
        )
        
        agent2 = BaseStrategicAgent(
            agent_name="test_agent",
            agent_role=AgentRole.INVESTOR,
            model_client=mock_model_client,
            tools=[]
        )
        
        agent3 = BaseStrategicAgent(
            agent_name="different_agent",
            agent_role=AgentRole.INVESTOR,
            model_client=mock_model_client,
            tools=[]
        )
        
        # Same name and role should be equal
        assert agent1 == agent2
        
        # Different name should not be equal
        assert agent1 != agent3
        
        # Non-agent object should not be equal
        assert agent1 != "not_an_agent"
    
    def test_agent_hash(self, mock_model_client):
        """Test agent hash functionality."""
        agent1 = BaseStrategicAgent(
            agent_name="test_agent",
            agent_role=AgentRole.INVESTOR,
            model_client=mock_model_client,
            tools=[]
        )
        
        agent2 = BaseStrategicAgent(
            agent_name="test_agent",
            agent_role=AgentRole.INVESTOR,
            model_client=mock_model_client,
            tools=[]
        )
        
        # Same agents should have same hash
        assert hash(agent1) == hash(agent2)
        
        # Should be able to use in set
        agent_set = {agent1, agent2}
        assert len(agent_set) == 1  # Only one unique agent
    
    def test_error_handling_in_initialization(self, mock_model_client):
        """Test error handling during agent initialization."""
        # Test with invalid agent role
        with pytest.raises(ValueError):
            BaseStrategicAgent(
                agent_name="test_agent",
                agent_role="invalid_role",  # Should be AgentRole enum
                model_client=mock_model_client,
                tools=[]
            )
    
    def test_tool_validation(self, mock_model_client):
        """Test tool validation during registration."""
        agent = BaseStrategicAgent(
            agent_name="test_agent",
            agent_role=AgentRole.INVESTOR,
            model_client=mock_model_client,
            tools=[]
        )
        
        # Test registering None tool
        with pytest.raises(ValueError) as exc_info:
            agent.register_tool(None)
        
        assert "Tool cannot be None" in str(exc_info.value)
        
        # Test registering tool without name
        invalid_tool = Mock()
        del invalid_tool.__name__  # Remove name attribute
        
        with pytest.raises(ValueError) as exc_info:
            agent.register_tool(invalid_tool)
        
        assert "Tool must have a __name__ attribute" in str(exc_info.value)
    
    def test_metrics_initialization(self, mock_model_client):
        """Test metrics initialization."""
        agent = BaseStrategicAgent(
            agent_name="test_agent",
            agent_role=AgentRole.INVESTOR,
            model_client=mock_model_client,
            tools=[]
        )
        
        metrics = agent.metrics
        assert isinstance(metrics, AgentMetrics)
        assert metrics.agent_role == AgentRole.INVESTOR
        assert metrics.total_analyses == 0
        assert metrics.average_confidence == 0.0
        assert metrics.response_time == 0.0
        assert metrics.quality_score == 0.0
    
    def test_configuration_validation(self, mock_model_client):
        """Test configuration validation."""
        agent = BaseStrategicAgent(
            agent_name="test_agent",
            agent_role=AgentRole.INVESTOR,
            model_client=mock_model_client,
            tools=[]
        )
        
        # Test setting invalid max_response_time
        with pytest.raises(ValueError) as exc_info:
            agent.max_response_time = -1.0
        
        assert "Max response time must be positive" in str(exc_info.value)
        
        # Test setting invalid confidence_threshold
        with pytest.raises(ValueError) as exc_info:
            agent.confidence_threshold = 1.5
        
        assert "Confidence threshold must be between 0 and 1" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_concurrent_operations(self, mock_model_client):
        """Test agent behavior under concurrent operations."""
        agent = BaseStrategicAgent(
            agent_name="test_agent",
            agent_role=AgentRole.INVESTOR,
            model_client=mock_model_client,
            tools=[]
        )
        
        # Test concurrent tool registration
        mock_tools = [Mock() for _ in range(5)]
        for i, tool in enumerate(mock_tools):
            tool.__name__ = f"test_tool_{i}"
        
        # Register tools concurrently
        import asyncio
        tasks = [
            asyncio.create_task(asyncio.to_thread(agent.register_tool, tool))
            for tool in mock_tools
        ]
        
        await asyncio.gather(*tasks)
        
        # All tools should be registered
        assert len(agent.tools) == 5
        
        # Test concurrent health checks
        health_tasks = [
            asyncio.create_task(agent.health_check())
            for _ in range(3)
        ]
        
        health_results = await asyncio.gather(*health_tasks)
        
        # All health checks should succeed
        assert len(health_results) == 3
        for result in health_results:
            assert result["status"] == "healthy"