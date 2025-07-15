"""
Investor Agent implementation for StrategySim AI.

Provides aggressive financial analysis, investment evaluation,
and growth-oriented strategic recommendations.
"""

from typing import Any, Dict, List, Optional
import logging

from autogen_core.models import ChatCompletionClient

from .base_agent import BaseStrategicAgent
from ..models.agent_models import AgentRole
from ..tools.financial_calculator import (
    calculate_npv, calculate_irr, perform_cash_flow_analysis,
    calculate_financial_ratios, calculate_investment_metrics,
    break_even_analysis, sensitivity_analysis
)

logger = logging.getLogger(__name__)


class InvestorAgent(BaseStrategicAgent):
    """
    Investor Agent for aggressive financial analysis and investment evaluation.
    
    Focuses on:
    - Financial returns and profitability
    - Growth potential and scalability
    - Market opportunities and competitive advantages
    - Risk-adjusted returns and investment metrics
    """
    
    def __init__(
        self,
        agent_name: str = "investor",
        model_client: ChatCompletionClient = None,
        custom_tools: Optional[List[Any]] = None
    ):
        """
        Initialize the Investor Agent.
        
        Args:
            agent_name: Name of the agent
            model_client: Model client for LLM communication
            custom_tools: Additional custom tools
        """
        # Get specialized tools
        specialized_tools = self.get_specialized_tools()
        
        # Add custom tools if provided
        if custom_tools:
            specialized_tools.extend(custom_tools)
        
        super().__init__(
            agent_name=agent_name,
            agent_role=AgentRole.INVESTOR,
            model_client=model_client,
            tools=specialized_tools
        )
        
        logger.info(f"Initialized InvestorAgent: {agent_name}")
    
    def get_specialized_tools(self) -> List[Any]:
        """
        Get tools specific to investor analysis.
        
        Returns:
            List of financial analysis tools
        """
        return [
            calculate_npv,
            calculate_irr,
            perform_cash_flow_analysis,
            calculate_financial_ratios,
            calculate_investment_metrics,
            break_even_analysis,
            sensitivity_analysis
        ]
    
    async def perform_specialized_analysis(
        self,
        decision_context: str,
        decision_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Perform financial analysis specific to investor perspective.
        
        Args:
            decision_context: Context of the decision
            decision_data: Decision data including financial projections
        
        Returns:
            Dictionary with financial analysis results
        """
        try:
            analysis_results = {}
            
            # Extract financial data
            financial_data = decision_data.get("financial_data", {})
            
            # Perform NPV analysis if cash flows are available
            if "cash_flows" in financial_data and "discount_rate" in financial_data:
                cash_flows = financial_data["cash_flows"]
                discount_rate = financial_data["discount_rate"]
                
                npv_result = await self._execute_tool(
                    "calculate_npv",
                    cash_flows=cash_flows,
                    discount_rate=discount_rate
                )
                analysis_results["npv_analysis"] = npv_result
                
                # Calculate IRR
                irr_result = await self._execute_tool(
                    "calculate_irr",
                    cash_flows=cash_flows
                )
                analysis_results["irr_analysis"] = irr_result
                
                # Perform comprehensive cash flow analysis
                cash_flow_analysis = await self._execute_tool(
                    "perform_cash_flow_analysis",
                    cash_flows=cash_flows,
                    discount_rate=discount_rate
                )
                analysis_results["cash_flow_analysis"] = cash_flow_analysis
            
            # Calculate financial ratios if P&L data is available
            if "revenue" in financial_data and "costs" in financial_data:
                revenue = financial_data["revenue"]
                cogs = financial_data.get("cost_of_goods_sold", financial_data["costs"] * 0.6)
                opex = financial_data.get("operating_expenses", financial_data["costs"] * 0.4)
                
                ratios_result = await self._execute_tool(
                    "calculate_financial_ratios",
                    revenue=revenue,
                    cost_of_goods_sold=cogs,
                    operating_expenses=opex
                )
                analysis_results["financial_ratios"] = ratios_result
            
            # Perform break-even analysis
            if "fixed_costs" in financial_data and "variable_cost_per_unit" in financial_data and "price_per_unit" in financial_data:
                breakeven_result = await self._execute_tool(
                    "break_even_analysis",
                    fixed_costs=financial_data["fixed_costs"],
                    variable_cost_per_unit=financial_data["variable_cost_per_unit"],
                    price_per_unit=financial_data["price_per_unit"]
                )
                analysis_results["breakeven_analysis"] = breakeven_result
            
            # Calculate investment metrics if returns data is available
            if "historical_returns" in financial_data and "initial_investment" in financial_data:
                investment_metrics = await self._execute_tool(
                    "calculate_investment_metrics",
                    returns=financial_data["historical_returns"],
                    initial_investment=financial_data["initial_investment"]
                )
                analysis_results["investment_metrics"] = investment_metrics
            
            # Generate investment recommendations
            analysis_results["investment_recommendations"] = await self._generate_investment_recommendations(
                decision_context, analysis_results
            )
            
            return analysis_results
            
        except Exception as e:
            logger.error(f"Specialized analysis failed for {self.agent_name}: {e}")
            raise
    
    async def _generate_investment_recommendations(
        self,
        decision_context: str,
        analysis_results: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generate investment recommendations based on analysis results.
        
        Args:
            decision_context: Context of the decision
            analysis_results: Results from financial analysis
        
        Returns:
            List of investment recommendations
        """
        recommendations = []
        
        # NPV-based recommendations
        if "npv_analysis" in analysis_results:
            npv_result = analysis_results["npv_analysis"]
            if npv_result.success and npv_result.result > 0:
                recommendations.append({
                    "type": "investment_approval",
                    "reasoning": f"Positive NPV of ${npv_result.result:,.2f} indicates value creation",
                    "confidence": 0.9,
                    "priority": "high"
                })
            elif npv_result.success and npv_result.result < 0:
                recommendations.append({
                    "type": "investment_rejection",
                    "reasoning": f"Negative NPV of ${npv_result.result:,.2f} indicates value destruction",
                    "confidence": 0.9,
                    "priority": "high"
                })
        
        # IRR-based recommendations
        if "irr_analysis" in analysis_results:
            irr_result = analysis_results["irr_analysis"]
            if irr_result.success and irr_result.result:
                irr_value = irr_result.result
                if irr_value > 0.15:  # 15% threshold
                    recommendations.append({
                        "type": "high_return_opportunity",
                        "reasoning": f"High IRR of {irr_value:.2%} exceeds investment threshold",
                        "confidence": 0.8,
                        "priority": "high"
                    })
                elif irr_value < 0.08:  # 8% threshold
                    recommendations.append({
                        "type": "low_return_warning",
                        "reasoning": f"Low IRR of {irr_value:.2%} below acceptable returns",
                        "confidence": 0.8,
                        "priority": "medium"
                    })
        
        # Cash flow analysis recommendations
        if "cash_flow_analysis" in analysis_results:
            cf_result = analysis_results["cash_flow_analysis"]
            if cf_result.success:
                cf_data = cf_result.result
                if hasattr(cf_data, 'payback_period') and cf_data.payback_period:
                    if cf_data.payback_period <= 3:  # 3 years
                        recommendations.append({
                            "type": "quick_payback",
                            "reasoning": f"Quick payback period of {cf_data.payback_period:.1f} years",
                            "confidence": 0.7,
                            "priority": "medium"
                        })
                    elif cf_data.payback_period > 7:  # 7 years
                        recommendations.append({
                            "type": "long_payback_warning",
                            "reasoning": f"Long payback period of {cf_data.payback_period:.1f} years",
                            "confidence": 0.7,
                            "priority": "medium"
                        })
        
        # Financial ratios recommendations
        if "financial_ratios" in analysis_results:
            ratios_result = analysis_results["financial_ratios"]
            if ratios_result.success:
                ratios_data = ratios_result.result
                if hasattr(ratios_data, 'gross_margin') and ratios_data.gross_margin > 60:
                    recommendations.append({
                        "type": "strong_margins",
                        "reasoning": f"Strong gross margin of {ratios_data.gross_margin:.1f}%",
                        "confidence": 0.8,
                        "priority": "medium"
                    })
                elif hasattr(ratios_data, 'gross_margin') and ratios_data.gross_margin < 20:
                    recommendations.append({
                        "type": "margin_concern",
                        "reasoning": f"Low gross margin of {ratios_data.gross_margin:.1f}%",
                        "confidence": 0.8,
                        "priority": "high"
                    })
        
        # Break-even analysis recommendations
        if "breakeven_analysis" in analysis_results:
            breakeven_result = analysis_results["breakeven_analysis"]
            if breakeven_result.success:
                breakeven_data = breakeven_result.result
                if "break_even_units" in breakeven_data:
                    units = breakeven_data["break_even_units"]
                    recommendations.append({
                        "type": "breakeven_assessment",
                        "reasoning": f"Break-even at {units:,.0f} units - assess market feasibility",
                        "confidence": 0.7,
                        "priority": "medium"
                    })
        
        # Investment metrics recommendations
        if "investment_metrics" in analysis_results:
            metrics_result = analysis_results["investment_metrics"]
            if metrics_result.success:
                metrics_data = metrics_result.result
                if hasattr(metrics_data, 'sharpe_ratio') and metrics_data.sharpe_ratio > 1.5:
                    recommendations.append({
                        "type": "excellent_risk_adjusted_return",
                        "reasoning": f"Excellent Sharpe ratio of {metrics_data.sharpe_ratio:.2f}",
                        "confidence": 0.8,
                        "priority": "high"
                    })
                elif hasattr(metrics_data, 'max_drawdown') and metrics_data.max_drawdown < -0.3:
                    recommendations.append({
                        "type": "high_volatility_warning",
                        "reasoning": f"High maximum drawdown of {metrics_data.max_drawdown:.1%}",
                        "confidence": 0.8,
                        "priority": "high"
                    })
        
        # Add general investment recommendations
        if not recommendations:
            recommendations.append({
                "type": "comprehensive_analysis_needed",
                "reasoning": "Insufficient financial data for detailed analysis - recommend gathering more information",
                "confidence": 0.6,
                "priority": "medium"
            })
        
        return recommendations
    
    async def evaluate_market_opportunity(
        self,
        market_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Evaluate market opportunity from investment perspective.
        
        Args:
            market_data: Market opportunity data
        
        Returns:
            Dictionary with market evaluation results
        """
        try:
            evaluation = {
                "market_size_assessment": "attractive" if market_data.get("market_size", 0) > 1000000000 else "limited",
                "growth_potential": "high" if market_data.get("growth_rate", 0) > 0.1 else "moderate",
                "competitive_dynamics": "favorable" if market_data.get("competitive_intensity", 0.5) < 0.6 else "challenging",
                "investment_thesis": []
            }
            
            # Build investment thesis
            if market_data.get("market_size", 0) > 1000000000:
                evaluation["investment_thesis"].append("Large addressable market supports scalable growth")
            
            if market_data.get("growth_rate", 0) > 0.15:
                evaluation["investment_thesis"].append("High growth rate indicates strong market dynamics")
            
            if market_data.get("competitive_intensity", 0.5) < 0.5:
                evaluation["investment_thesis"].append("Moderate competition allows for market share capture")
            
            return evaluation
            
        except Exception as e:
            logger.error(f"Market opportunity evaluation failed: {e}")
            raise
    
    async def assess_competitive_position(
        self,
        competitive_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Assess competitive position from investment perspective.
        
        Args:
            competitive_data: Competitive positioning data
        
        Returns:
            Dictionary with competitive assessment results
        """
        try:
            assessment = {
                "competitive_strength": "strong" if competitive_data.get("market_share", 0) > 0.2 else "moderate",
                "differentiation": "high" if competitive_data.get("unique_value_props", 0) > 2 else "moderate",
                "barriers_to_entry": "high" if competitive_data.get("moat_strength", 0) > 0.7 else "moderate",
                "investment_implications": []
            }
            
            # Generate investment implications
            if competitive_data.get("market_share", 0) > 0.2:
                assessment["investment_implications"].append("Strong market position supports pricing power")
            
            if competitive_data.get("moat_strength", 0) > 0.7:
                assessment["investment_implications"].append("Strong competitive moat protects market position")
            
            if competitive_data.get("growth_trajectory", 0) > 0.2:
                assessment["investment_implications"].append("Strong growth trajectory indicates market leadership")
            
            return assessment
            
        except Exception as e:
            logger.error(f"Competitive position assessment failed: {e}")
            raise
    
    async def generate_investment_summary(
        self,
        decision_context: str,
        analysis_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate comprehensive investment summary.
        
        Args:
            decision_context: Decision context
            analysis_results: All analysis results
        
        Returns:
            Dictionary with investment summary
        """
        try:
            summary = {
                "investment_recommendation": "neutral",
                "confidence_level": 0.7,
                "key_metrics": {},
                "risk_factors": [],
                "value_drivers": [],
                "action_items": []
            }
            
            # Determine overall recommendation
            positive_signals = 0
            negative_signals = 0
            
            # Count positive and negative signals from analysis
            if "investment_recommendations" in analysis_results:
                for rec in analysis_results["investment_recommendations"]:
                    if rec["type"] in ["investment_approval", "high_return_opportunity", "strong_margins"]:
                        positive_signals += 1
                    elif rec["type"] in ["investment_rejection", "low_return_warning", "margin_concern"]:
                        negative_signals += 1
            
            # Set recommendation based on signals
            if positive_signals > negative_signals:
                summary["investment_recommendation"] = "positive"
                summary["confidence_level"] = 0.8
            elif negative_signals > positive_signals:
                summary["investment_recommendation"] = "negative"
                summary["confidence_level"] = 0.8
            else:
                summary["investment_recommendation"] = "neutral"
                summary["confidence_level"] = 0.6
            
            # Add key metrics
            if "npv_analysis" in analysis_results and analysis_results["npv_analysis"].success:
                summary["key_metrics"]["npv"] = analysis_results["npv_analysis"].result
            
            if "irr_analysis" in analysis_results and analysis_results["irr_analysis"].success:
                summary["key_metrics"]["irr"] = analysis_results["irr_analysis"].result
            
            # Add risk factors
            summary["risk_factors"] = [
                "Market volatility impact on projections",
                "Competitive response to market entry",
                "Execution risk in implementation",
                "Economic downturn impact on demand"
            ]
            
            # Add value drivers
            summary["value_drivers"] = [
                "Market growth and expansion opportunities",
                "Operational efficiency improvements",
                "Competitive differentiation and pricing power",
                "Technology and innovation advantages"
            ]
            
            # Add action items
            summary["action_items"] = [
                "Conduct detailed financial modeling",
                "Validate market assumptions with research",
                "Assess competitive response scenarios",
                "Develop implementation timeline and milestones"
            ]
            
            return summary
            
        except Exception as e:
            logger.error(f"Investment summary generation failed: {e}")
            raise