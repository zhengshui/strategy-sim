"""
Unit tests for agent models in StrategySim AI.

Tests validation, state management, and business logic for agent-related models.
"""

import pytest
from datetime import datetime, timedelta
from typing import List

from pydantic import ValidationError

from src.models.agent_models import (
    AgentRole, AgentAnalysis, ConversationState, AgentConversation,
    RiskLevel, AgentMetrics, AgentConfiguration
)


class TestAgentRole:
    """Test AgentRole enum."""
    
    def test_all_roles_defined(self):
        """Test all required agent roles are defined."""
        expected_roles = ["investor", "legal", "analyst", "customer", "strategist"]
        
        for role in expected_roles:
            assert hasattr(AgentRole, role.upper())
    
    def test_role_values(self):
        """Test role enum values."""
        assert AgentRole.INVESTOR.value == "investor"
        assert AgentRole.LEGAL.value == "legal"
        assert AgentRole.ANALYST.value == "analyst"
        assert AgentRole.CUSTOMER.value == "customer"
        assert AgentRole.STRATEGIST.value == "strategist"
    
    def test_role_string_representation(self):
        """Test string representation of roles."""
        assert str(AgentRole.INVESTOR) == "AgentRole.INVESTOR"


class TestRiskLevel:
    """Test RiskLevel enum."""
    
    def test_all_risk_levels_defined(self):
        """Test all risk levels are defined."""
        expected_levels = ["low", "medium", "high", "critical"]
        
        for level in expected_levels:
            assert hasattr(RiskLevel, level.upper())
    
    def test_risk_level_values(self):
        """Test risk level enum values."""
        assert RiskLevel.LOW.value == "low"
        assert RiskLevel.MEDIUM.value == "medium"
        assert RiskLevel.HIGH.value == "high"
        assert RiskLevel.CRITICAL.value == "critical"


class TestConversationState:
    """Test ConversationState enum."""
    
    def test_all_states_defined(self):
        """Test all conversation states are defined."""
        expected_states = ["initializing", "analyzing", "discussing", "synthesizing", "concluded"]
        
        for state in expected_states:
            assert hasattr(ConversationState, state.upper())
    
    def test_state_values(self):
        """Test conversation state enum values."""
        assert ConversationState.INITIALIZING.value == "initializing"
        assert ConversationState.ANALYZING.value == "analyzing"
        assert ConversationState.DISCUSSING.value == "discussing"
        assert ConversationState.SYNTHESIZING.value == "synthesizing"
        assert ConversationState.CONCLUDED.value == "concluded"


class TestAgentAnalysis:
    """Test AgentAnalysis model."""
    
    def test_valid_analysis_creation(self, sample_agent_analysis):
        """Test creating valid agent analysis."""
        analysis = sample_agent_analysis
        
        assert analysis.agent_role == AgentRole.INVESTOR
        assert analysis.confidence_level == 0.8
        assert len(analysis.recommendations) == 3
        assert len(analysis.key_insights) == 3
        assert len(analysis.concerns) == 3
        assert len(analysis.analysis_id) > 0
        assert isinstance(analysis.created_at, datetime)
    
    def test_empty_analysis_validation(self):
        """Test validation fails for empty analysis."""
        with pytest.raises(ValidationError) as exc_info:
            AgentAnalysis(
                agent_role=AgentRole.INVESTOR,
                analysis="",
                confidence_level=0.8
            )
        
        assert "ensure this value has at least 50 characters" in str(exc_info.value)
    
    def test_invalid_confidence_level(self):
        """Test validation fails for invalid confidence level."""
        with pytest.raises(ValidationError) as exc_info:
            AgentAnalysis(
                agent_role=AgentRole.INVESTOR,
                analysis="This is a valid analysis that is long enough for testing purposes",
                confidence_level=1.5
            )
        
        assert "ensure this value is less than or equal to 1" in str(exc_info.value)
    
    def test_negative_confidence_level(self):
        """Test validation fails for negative confidence level."""
        with pytest.raises(ValidationError) as exc_info:
            AgentAnalysis(
                agent_role=AgentRole.INVESTOR,
                analysis="This is a valid analysis that is long enough for testing purposes",
                confidence_level=-0.1
            )
        
        assert "ensure this value is greater than or equal to 0" in str(exc_info.value)
    
    def test_analysis_summary_property(self, sample_agent_analysis):
        """Test analysis summary property."""
        analysis = sample_agent_analysis
        summary = analysis.analysis_summary
        
        assert isinstance(summary, str)
        assert len(summary) <= 200  # Should be truncated
        assert "..." in summary or len(analysis.analysis) <= 200
    
    def test_risk_level_property(self, sample_agent_analysis):
        """Test risk level property calculation."""
        analysis = sample_agent_analysis
        
        # Test different confidence levels
        analysis.confidence_level = 0.9
        assert analysis.risk_level == RiskLevel.LOW
        
        analysis.confidence_level = 0.7
        assert analysis.risk_level == RiskLevel.MEDIUM
        
        analysis.confidence_level = 0.5
        assert analysis.risk_level == RiskLevel.HIGH
        
        analysis.confidence_level = 0.3
        assert analysis.risk_level == RiskLevel.CRITICAL
    
    def test_has_concerns_property(self, sample_agent_analysis):
        """Test has_concerns property."""
        analysis = sample_agent_analysis
        assert analysis.has_concerns is True
        
        analysis.concerns = []
        assert analysis.has_concerns is False
    
    def test_add_recommendation(self, sample_agent_analysis):
        """Test adding recommendation."""
        analysis = sample_agent_analysis
        initial_count = len(analysis.recommendations)
        
        analysis.add_recommendation("New recommendation")
        assert len(analysis.recommendations) == initial_count + 1
        assert "New recommendation" in analysis.recommendations
    
    def test_add_insight(self, sample_agent_analysis):
        """Test adding insight."""
        analysis = sample_agent_analysis
        initial_count = len(analysis.key_insights)
        
        analysis.add_insight("New insight")
        assert len(analysis.key_insights) == initial_count + 1
        assert "New insight" in analysis.key_insights
    
    def test_add_concern(self, sample_agent_analysis):
        """Test adding concern."""
        analysis = sample_agent_analysis
        initial_count = len(analysis.concerns)
        
        analysis.add_concern("New concern")
        assert len(analysis.concerns) == initial_count + 1
        assert "New concern" in analysis.concerns
    
    def test_analysis_validation_with_empty_lists(self):
        """Test analysis creation with empty lists."""
        analysis = AgentAnalysis(
            agent_role=AgentRole.INVESTOR,
            analysis="This is a valid analysis that is long enough for testing purposes",
            confidence_level=0.8,
            recommendations=[],
            key_insights=[],
            concerns=[]
        )
        
        assert len(analysis.recommendations) == 0
        assert len(analysis.key_insights) == 0
        assert len(analysis.concerns) == 0
        assert analysis.has_concerns is False


class TestAgentMetrics:
    """Test AgentMetrics model."""
    
    def test_valid_metrics_creation(self):
        """Test creating valid agent metrics."""
        metrics = AgentMetrics(
            agent_role=AgentRole.INVESTOR,
            total_analyses=50,
            average_confidence=0.8,
            response_time=2.5,
            quality_score=0.9
        )
        
        assert metrics.agent_role == AgentRole.INVESTOR
        assert metrics.total_analyses == 50
        assert metrics.average_confidence == 0.8
        assert metrics.response_time == 2.5
        assert metrics.quality_score == 0.9
    
    def test_negative_analyses_validation(self):
        """Test validation fails for negative analyses count."""
        with pytest.raises(ValidationError) as exc_info:
            AgentMetrics(
                agent_role=AgentRole.INVESTOR,
                total_analyses=-1,
                average_confidence=0.8,
                response_time=2.5,
                quality_score=0.9
            )
        
        assert "ensure this value is greater than or equal to 0" in str(exc_info.value)
    
    def test_invalid_confidence_range(self):
        """Test validation fails for invalid confidence range."""
        with pytest.raises(ValidationError) as exc_info:
            AgentMetrics(
                agent_role=AgentRole.INVESTOR,
                total_analyses=50,
                average_confidence=1.5,
                response_time=2.5,
                quality_score=0.9
            )
        
        assert "ensure this value is less than or equal to 1" in str(exc_info.value)
    
    def test_negative_response_time(self):
        """Test validation fails for negative response time."""
        with pytest.raises(ValidationError) as exc_info:
            AgentMetrics(
                agent_role=AgentRole.INVESTOR,
                total_analyses=50,
                average_confidence=0.8,
                response_time=-1.0,
                quality_score=0.9
            )
        
        assert "ensure this value is greater than or equal to 0" in str(exc_info.value)
    
    def test_performance_category_property(self):
        """Test performance category property."""
        metrics = AgentMetrics(
            agent_role=AgentRole.INVESTOR,
            total_analyses=50,
            average_confidence=0.8,
            response_time=2.5,
            quality_score=0.9
        )
        
        # Test excellent performance
        metrics.quality_score = 0.9
        assert metrics.performance_category == "excellent"
        
        # Test good performance
        metrics.quality_score = 0.8
        assert metrics.performance_category == "good"
        
        # Test average performance
        metrics.quality_score = 0.6
        assert metrics.performance_category == "average"
        
        # Test poor performance
        metrics.quality_score = 0.4
        assert metrics.performance_category == "poor"


class TestAgentConfiguration:
    """Test AgentConfiguration model."""
    
    def test_valid_configuration_creation(self):
        """Test creating valid agent configuration."""
        config = AgentConfiguration(
            agent_role=AgentRole.INVESTOR,
            max_response_time=30.0,
            confidence_threshold=0.7,
            enable_analysis_cache=True
        )
        
        assert config.agent_role == AgentRole.INVESTOR
        assert config.max_response_time == 30.0
        assert config.confidence_threshold == 0.7
        assert config.enable_analysis_cache is True
    
    def test_negative_response_time_validation(self):
        """Test validation fails for negative response time."""
        with pytest.raises(ValidationError) as exc_info:
            AgentConfiguration(
                agent_role=AgentRole.INVESTOR,
                max_response_time=-1.0,
                confidence_threshold=0.7
            )
        
        assert "ensure this value is greater than 0" in str(exc_info.value)
    
    def test_invalid_confidence_threshold(self):
        """Test validation fails for invalid confidence threshold."""
        with pytest.raises(ValidationError) as exc_info:
            AgentConfiguration(
                agent_role=AgentRole.INVESTOR,
                max_response_time=30.0,
                confidence_threshold=1.5
            )
        
        assert "ensure this value is less than or equal to 1" in str(exc_info.value)
    
    def test_is_high_confidence_threshold_property(self):
        """Test is_high_confidence_threshold property."""
        config = AgentConfiguration(
            agent_role=AgentRole.INVESTOR,
            max_response_time=30.0,
            confidence_threshold=0.8
        )
        
        assert config.is_high_confidence_threshold is True
        
        config.confidence_threshold = 0.6
        assert config.is_high_confidence_threshold is False


class TestAgentConversation:
    """Test AgentConversation model."""
    
    def test_valid_conversation_creation(self, sample_conversation_state):
        """Test creating valid agent conversation."""
        conversation = sample_conversation_state
        
        assert conversation.conversation_id == "test_conv_001"
        assert len(conversation.participants) == 3
        assert conversation.state == ConversationState.ANALYZING
        assert conversation.max_turns == 10
        assert conversation.turn_count == 5
        assert conversation.context == {"test_key": "test_value"}
        assert isinstance(conversation.created_at, datetime)
    
    def test_empty_conversation_id_validation(self):
        """Test validation fails for empty conversation ID."""
        with pytest.raises(ValidationError) as exc_info:
            AgentConversation(
                conversation_id="",
                participants=["investor", "legal"],
                state=ConversationState.ANALYZING,
                max_turns=10
            )
        
        assert "ensure this value has at least 1 characters" in str(exc_info.value)
    
    def test_empty_participants_validation(self):
        """Test validation fails for empty participants."""
        with pytest.raises(ValidationError) as exc_info:
            AgentConversation(
                conversation_id="test_conv",
                participants=[],
                state=ConversationState.ANALYZING,
                max_turns=10
            )
        
        assert "ensure this value has at least 1 items" in str(exc_info.value)
    
    def test_zero_max_turns_validation(self):
        """Test validation fails for zero max turns."""
        with pytest.raises(ValidationError) as exc_info:
            AgentConversation(
                conversation_id="test_conv",
                participants=["investor", "legal"],
                state=ConversationState.ANALYZING,
                max_turns=0
            )
        
        assert "ensure this value is greater than 0" in str(exc_info.value)
    
    def test_negative_turn_count_validation(self):
        """Test validation fails for negative turn count."""
        with pytest.raises(ValidationError) as exc_info:
            AgentConversation(
                conversation_id="test_conv",
                participants=["investor", "legal"],
                state=ConversationState.ANALYZING,
                max_turns=10,
                turn_count=-1
            )
        
        assert "ensure this value is greater than or equal to 0" in str(exc_info.value)
    
    def test_unique_participants_validation(self):
        """Test validation ensures unique participants."""
        participants = ["investor", "legal", "investor"]  # Duplicate
        
        with pytest.raises(ValidationError) as exc_info:
            AgentConversation(
                conversation_id="test_conv",
                participants=participants,
                state=ConversationState.ANALYZING,
                max_turns=10
            )
        
        assert "Participants must be unique" in str(exc_info.value)
    
    def test_is_finished_property(self, sample_conversation_state):
        """Test is_finished property."""
        conversation = sample_conversation_state
        
        # Not finished - analyzing state
        assert conversation.is_finished() is False
        
        # Finished - concluded state
        conversation.state = ConversationState.CONCLUDED
        assert conversation.is_finished() is True
        
        # Finished - max turns reached
        conversation.state = ConversationState.ANALYZING
        conversation.turn_count = conversation.max_turns
        assert conversation.is_finished() is True
    
    def test_is_active_property(self, sample_conversation_state):
        """Test is_active property."""
        conversation = sample_conversation_state
        
        # Active - analyzing state
        assert conversation.is_active() is True
        
        # Not active - concluded state
        conversation.state = ConversationState.CONCLUDED
        assert conversation.is_active() is False
        
        # Not active - initializing state
        conversation.state = ConversationState.INITIALIZING
        assert conversation.is_active() is False
    
    def test_progress_percentage_property(self, sample_conversation_state):
        """Test progress_percentage property."""
        conversation = sample_conversation_state
        
        # 5 out of 10 turns = 50%
        assert conversation.progress_percentage == 0.5
        
        # Test completed conversation
        conversation.turn_count = conversation.max_turns
        assert conversation.progress_percentage == 1.0
    
    def test_add_participant(self, sample_conversation_state):
        """Test adding participant."""
        conversation = sample_conversation_state
        initial_count = len(conversation.participants)
        
        conversation.add_participant("strategist")
        assert len(conversation.participants) == initial_count + 1
        assert "strategist" in conversation.participants
        
        # Adding duplicate should not increase count
        conversation.add_participant("strategist")
        assert len(conversation.participants) == initial_count + 1
    
    def test_remove_participant(self, sample_conversation_state):
        """Test removing participant."""
        conversation = sample_conversation_state
        initial_count = len(conversation.participants)
        
        conversation.remove_participant("investor")
        assert len(conversation.participants) == initial_count - 1
        assert "investor" not in conversation.participants
        
        # Removing non-existent participant should not change count
        conversation.remove_participant("nonexistent")
        assert len(conversation.participants) == initial_count - 1
    
    def test_increment_turn(self, sample_conversation_state):
        """Test incrementing turn count."""
        conversation = sample_conversation_state
        initial_count = conversation.turn_count
        
        conversation.increment_turn()
        assert conversation.turn_count == initial_count + 1
    
    def test_update_context(self, sample_conversation_state):
        """Test updating conversation context."""
        conversation = sample_conversation_state
        
        conversation.update_context("new_key", "new_value")
        assert conversation.context["new_key"] == "new_value"
        assert conversation.context["test_key"] == "test_value"  # Original should remain
    
    def test_get_context_value(self, sample_conversation_state):
        """Test getting context value."""
        conversation = sample_conversation_state
        
        assert conversation.get_context_value("test_key") == "test_value"
        assert conversation.get_context_value("nonexistent") is None
        assert conversation.get_context_value("nonexistent", "default") == "default"
    
    def test_conversation_duration_property(self, sample_conversation_state):
        """Test conversation duration property."""
        conversation = sample_conversation_state
        
        # Mock completion time
        conversation.completed_at = conversation.created_at + timedelta(minutes=5)
        
        duration = conversation.conversation_duration
        assert duration == 300.0  # 5 minutes in seconds
    
    def test_conclude_conversation(self, sample_conversation_state):
        """Test concluding conversation."""
        conversation = sample_conversation_state
        
        conversation.conclude_conversation()
        assert conversation.state == ConversationState.CONCLUDED
        assert conversation.completed_at is not None
        assert conversation.is_finished() is True
    
    def test_conversation_summary_property(self, sample_conversation_state):
        """Test conversation summary property."""
        conversation = sample_conversation_state
        
        summary = conversation.conversation_summary
        assert isinstance(summary, dict)
        assert "conversation_id" in summary
        assert "participants" in summary
        assert "state" in summary
        assert "progress" in summary
        assert "duration" in summary