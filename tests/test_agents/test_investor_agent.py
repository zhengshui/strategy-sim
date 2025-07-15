"""
Unit tests for investor agent in StrategySim AI.

Tests specialized investor agent functionality and financial analysis capabilities.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from typing import Any, Dict, List

from src.agents.investor_agent import InvestorAgent
from src.models.agent_models import AgentRole, AgentAnalysis
from src.tools.financial_calculator import (
    calculate_npv, calculate_irr, calculate_roi, calculate_payback_period
)


class TestInvestorAgent:
    """Test InvestorAgent functionality."""
    
    def test_investor_agent_initialization(self, mock_model_client):
        """Test investor agent initialization."""
        agent = InvestorAgent(
            agent_name="test_investor",
            model_client=mock_model_client
        )
        
        assert agent.agent_name == "test_investor"
        assert agent.agent_role == AgentRole.INVESTOR
        assert agent.model_client == mock_model_client
        assert len(agent.tools) > 0  # Should have financial tools
        
        # Check that financial tools are registered
        tool_names = agent.get_tool_names()
        assert "calculate_npv" in tool_names
        assert "calculate_irr" in tool_names
        assert "calculate_roi" in tool_names
        assert "calculate_payback_period" in tool_names
    
    def test_default_agent_name(self, mock_model_client):
        """Test default agent name."""
        agent = InvestorAgent(model_client=mock_model_client)
        assert agent.agent_name == "investor"
    
    def test_custom_tools_integration(self, mock_model_client):
        """Test integration with custom tools."""
        custom_tool = Mock()
        custom_tool.__name__ = "custom_financial_tool"
        
        agent = InvestorAgent(
            agent_name="test_investor",
            model_client=mock_model_client,
            custom_tools=[custom_tool]
        )
        
        # Should have both specialized and custom tools
        tool_names = agent.get_tool_names()
        assert "calculate_npv" in tool_names
        assert "custom_financial_tool" in tool_names
    
    def test_get_specialized_tools(self, mock_model_client):
        """Test getting specialized financial tools."""
        agent = InvestorAgent(model_client=mock_model_client)
        
        specialized_tools = agent.get_specialized_tools()
        
        assert len(specialized_tools) >= 4  # At least 4 financial tools
        assert calculate_npv in specialized_tools
        assert calculate_irr in specialized_tools
        assert calculate_roi in specialized_tools
        assert calculate_payback_period in specialized_tools
    
    def test_system_prompt_content(self, mock_model_client):
        """Test system prompt contains investor-specific content."""
        agent = InvestorAgent(model_client=mock_model_client)
        
        prompt = agent.system_prompt
        
        # Check for investor-specific keywords
        assert "investor" in prompt.lower()
        assert "financial" in prompt.lower()
        assert "roi" in prompt.lower() or "return" in prompt.lower()
        assert "aggressive" in prompt.lower()
        assert "growth" in prompt.lower()
        assert "profit" in prompt.lower()
    
    @pytest.mark.asyncio
    async def test_analyze_decision_basic(self, mock_model_client):
        """Test basic decision analysis."""
        agent = InvestorAgent(model_client=mock_model_client)
        
        # Mock the specialized analysis
        with patch.object(agent, 'perform_specialized_analysis') as mock_analysis:
            mock_analysis.return_value = {
                "financial_assessment": {
                    "projected_roi": 0.25,
                    "risk_level": "medium",
                    "investment_recommendation": "proceed"
                }
            }
            
            result = await agent.analyze_decision(
                "Market expansion decision",
                {"budget": 1000000, "timeline": "12 months"}
            )
            
            assert isinstance(result, AgentAnalysis)
            assert result.agent_role == AgentRole.INVESTOR
            assert result.confidence_level > 0
            assert len(result.analysis) > 0
            assert "financial" in result.analysis.lower()
            
            # Check that specialized analysis was called
            mock_analysis.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_analyze_decision_with_financial_data(self, mock_model_client):
        """Test decision analysis with financial data."""
        agent = InvestorAgent(model_client=mock_model_client)
        
        decision_data = {
            "budget": 1000000,
            "expected_revenue": 1500000,
            "timeline": "24 months",
            "risk_factors": ["market_volatility", "competition"],
            "cash_flows": [-1000000, 200000, 300000, 500000]
        }
        
        with patch.object(agent, 'perform_specialized_analysis') as mock_analysis:
            mock_analysis.return_value = {
                "financial_assessment": {
                    "npv": 250000,
                    "irr": 0.18,
                    "roi": 0.25,
                    "payback_period": 2.5,
                    "risk_adjusted_return": 0.20
                }
            }
            
            result = await agent.analyze_decision(
                "Product launch decision",
                decision_data
            )
            
            assert isinstance(result, AgentAnalysis)
            assert result.agent_role == AgentRole.INVESTOR
            assert len(result.recommendations) > 0
            assert len(result.key_insights) > 0
            
            # Should have financial metrics in analysis
            assert "npv" in result.analysis.lower() or "net present value" in result.analysis.lower()
            assert "roi" in result.analysis.lower() or "return" in result.analysis.lower()
    
    @pytest.mark.asyncio
    async def test_perform_specialized_analysis(self, mock_model_client):
        """Test specialized financial analysis."""
        agent = InvestorAgent(model_client=mock_model_client)
        
        decision_data = {
            "investment_amount": 500000,
            "expected_returns": [100000, 150000, 200000, 250000],
            "discount_rate": 0.10,
            "timeline": "4 years"
        }
        
        result = await agent.perform_specialized_analysis(
            "Investment opportunity analysis",
            decision_data
        )
        
        assert isinstance(result, dict)
        assert "financial_assessment" in result
        
        financial_assessment = result["financial_assessment"]
        assert "projected_roi" in financial_assessment
        assert "risk_level" in financial_assessment
        assert "investment_recommendation" in financial_assessment
        assert "key_metrics" in financial_assessment
        
        # Check that metrics are reasonable
        assert isinstance(financial_assessment["projected_roi"], (int, float))
        assert financial_assessment["risk_level"] in ["low", "medium", "high"]
        assert financial_assessment["investment_recommendation"] in ["proceed", "caution", "reject"]
    
    @pytest.mark.asyncio
    async def test_analyze_decision_error_handling(self, mock_model_client):
        """Test error handling in decision analysis."""
        agent = InvestorAgent(model_client=mock_model_client)
        
        # Mock specialized analysis to raise an exception
        with patch.object(agent, 'perform_specialized_analysis') as mock_analysis:
            mock_analysis.side_effect = Exception("Analysis failed")
            
            with pytest.raises(Exception) as exc_info:
                await agent.analyze_decision("Test decision", {})
            
            assert "Analysis failed" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_analyze_decision_with_missing_data(self, mock_model_client):
        """Test analysis with missing financial data."""
        agent = InvestorAgent(model_client=mock_model_client)
        
        # Decision data with missing financial information
        decision_data = {
            "description": "Market expansion",
            "timeline": "12 months"
            # Missing budget, revenue projections, etc.
        }
        
        with patch.object(agent, 'perform_specialized_analysis') as mock_analysis:
            mock_analysis.return_value = {
                "financial_assessment": {
                    "data_completeness": "insufficient",
                    "risk_level": "high",
                    "investment_recommendation": "seek_more_info"
                }
            }
            
            result = await agent.analyze_decision(
                "Incomplete decision",
                decision_data
            )
            
            assert isinstance(result, AgentAnalysis)
            assert result.confidence_level < 0.6  # Low confidence due to missing data
            assert len(result.concerns) > 0
            assert any("data" in concern.lower() for concern in result.concerns)
    
    @pytest.mark.asyncio
    async def test_analyze_high_risk_decision(self, mock_model_client):
        """Test analysis of high-risk decision."""
        agent = InvestorAgent(model_client=mock_model_client)
        
        decision_data = {
            "investment_amount": 10000000,
            "market_volatility": "high",
            "competition_level": "intense",
            "regulatory_risk": "high",
            "expected_roi": 0.50  # High return but high risk
        }
        
        with patch.object(agent, 'perform_specialized_analysis') as mock_analysis:
            mock_analysis.return_value = {
                "financial_assessment": {
                    "risk_level": "high",
                    "projected_roi": 0.50,
                    "risk_adjusted_return": 0.20,
                    "investment_recommendation": "caution"
                }
            }
            
            result = await agent.analyze_decision(
                "High-risk investment",
                decision_data
            )
            
            assert isinstance(result, AgentAnalysis)
            assert len(result.concerns) > 0
            assert any("risk" in concern.lower() for concern in result.concerns)
            assert any("caution" in rec.lower() for rec in result.recommendations)
    
    @pytest.mark.asyncio
    async def test_analyze_conservative_decision(self, mock_model_client):
        """Test analysis of conservative decision."""
        agent = InvestorAgent(model_client=mock_model_client)
        
        decision_data = {
            "investment_amount": 100000,
            "market_volatility": "low",
            "competition_level": "moderate",
            "regulatory_risk": "low",
            "expected_roi": 0.08  # Conservative return
        }
        
        with patch.object(agent, 'perform_specialized_analysis') as mock_analysis:
            mock_analysis.return_value = {
                "financial_assessment": {
                    "risk_level": "low",
                    "projected_roi": 0.08,
                    "risk_adjusted_return": 0.07,
                    "investment_recommendation": "proceed"
                }
            }
            
            result = await agent.analyze_decision(
                "Conservative investment",
                decision_data
            )
            
            assert isinstance(result, AgentAnalysis)
            assert result.confidence_level > 0.7  # High confidence for low-risk decision
            assert len(result.concerns) == 0 or len(result.concerns) == 1  # Few concerns
            assert any("proceed" in rec.lower() for rec in result.recommendations)
    
    def test_financial_tools_integration(self, mock_model_client):
        """Test integration with financial calculation tools."""
        agent = InvestorAgent(model_client=mock_model_client)
        
        # Test that all expected financial tools are available
        tool_names = agent.get_tool_names()
        
        expected_tools = [
            "calculate_npv",
            "calculate_irr", 
            "calculate_roi",
            "calculate_payback_period"
        ]
        
        for tool_name in expected_tools:
            assert tool_name in tool_names
            assert agent.has_tool(tool_name)
    
    def test_investor_specific_configuration(self, mock_model_client):
        """Test investor-specific configuration settings."""
        agent = InvestorAgent(model_client=mock_model_client)
        
        # Investor agents might have different thresholds
        assert agent.confidence_threshold >= 0.0
        assert agent.max_response_time > 0
        
        # Check that agent has financial analysis bias
        assert agent.agent_role == AgentRole.INVESTOR
        assert "financial" in agent.system_prompt.lower()
        assert "aggressive" in agent.system_prompt.lower()
    
    @pytest.mark.asyncio
    async def test_metrics_update_after_analysis(self, mock_model_client):
        """Test that metrics are updated after analysis."""
        agent = InvestorAgent(model_client=mock_model_client)
        
        # Get initial metrics
        initial_analyses = agent.metrics.total_analyses
        
        # Mock specialized analysis
        with patch.object(agent, 'perform_specialized_analysis') as mock_analysis:
            mock_analysis.return_value = {
                "financial_assessment": {
                    "projected_roi": 0.15,
                    "risk_level": "medium",
                    "investment_recommendation": "proceed"
                }
            }
            
            # Perform analysis
            await agent.analyze_decision("Test decision", {"budget": 100000})
            
            # Check that metrics were updated
            assert agent.metrics.total_analyses > initial_analyses
            assert agent.metrics.average_confidence > 0
    
    @pytest.mark.asyncio
    async def test_health_check_with_financial_tools(self, mock_model_client):
        """Test health check includes financial tools status."""
        agent = InvestorAgent(model_client=mock_model_client)
        
        health_status = await agent.health_check()
        
        assert health_status["status"] == "healthy"
        assert health_status["tools_count"] >= 4  # At least 4 financial tools
        assert health_status["agent_name"] == "investor"
        
        # Check that health check includes tool-specific information
        assert "model_client_status" in health_status
        assert "last_activity" in health_status
    
    @pytest.mark.asyncio
    async def test_concurrent_analyses(self, mock_model_client):
        """Test concurrent decision analyses."""
        agent = InvestorAgent(model_client=mock_model_client)
        
        # Mock specialized analysis
        with patch.object(agent, 'perform_specialized_analysis') as mock_analysis:
            mock_analysis.return_value = {
                "financial_assessment": {
                    "projected_roi": 0.20,
                    "risk_level": "medium",
                    "investment_recommendation": "proceed"
                }
            }
            
            # Run multiple analyses concurrently
            import asyncio
            tasks = [
                asyncio.create_task(agent.analyze_decision(f"Decision {i}", {"budget": 100000}))
                for i in range(3)
            ]
            
            results = await asyncio.gather(*tasks)
            
            # All analyses should complete successfully
            assert len(results) == 3
            for result in results:
                assert isinstance(result, AgentAnalysis)
                assert result.agent_role == AgentRole.INVESTOR
                assert result.confidence_level > 0
    
    def test_agent_equality_and_hash(self, mock_model_client):
        """Test agent equality and hash functionality."""
        agent1 = InvestorAgent(
            agent_name="investor1",
            model_client=mock_model_client
        )
        
        agent2 = InvestorAgent(
            agent_name="investor1",
            model_client=mock_model_client
        )
        
        agent3 = InvestorAgent(
            agent_name="investor2",
            model_client=mock_model_client
        )
        
        # Same name agents should be equal
        assert agent1 == agent2
        assert hash(agent1) == hash(agent2)
        
        # Different name agents should not be equal
        assert agent1 != agent3
        assert hash(agent1) != hash(agent3)
    
    def test_string_representation(self, mock_model_client):
        """Test string representation of investor agent."""
        agent = InvestorAgent(
            agent_name="test_investor",
            model_client=mock_model_client
        )
        
        str_repr = str(agent)
        assert "test_investor" in str_repr
        assert "investor" in str_repr.lower()
        
        repr_str = repr(agent)
        assert "InvestorAgent" in repr_str
        assert "test_investor" in repr_str