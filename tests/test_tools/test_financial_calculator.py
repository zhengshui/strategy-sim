"""
Unit tests for financial calculator tools in StrategySim AI.

Tests financial calculation functions used by the Investor Agent.
"""

import pytest
import math
from typing import List

from src.tools.financial_calculator import (
    calculate_npv, calculate_irr, calculate_roi, calculate_payback_period,
    calculate_break_even_point, analyze_cash_flow, calculate_wacc,
    perform_sensitivity_analysis, calculate_profitability_index
)


class TestCalculateNPV:
    """Test Net Present Value calculation."""
    
    def test_npv_positive_investment(self):
        """Test NPV calculation for positive investment."""
        cash_flows = [-100000, 30000, 35000, 40000, 45000]
        discount_rate = 0.10
        
        npv = calculate_npv(cash_flows, discount_rate)
        
        # NPV should be positive for this investment
        assert npv > 0
        assert isinstance(npv, float)
    
    def test_npv_negative_investment(self):
        """Test NPV calculation for negative investment."""
        cash_flows = [-100000, 10000, 15000, 20000, 25000]
        discount_rate = 0.15
        
        npv = calculate_npv(cash_flows, discount_rate)
        
        # NPV should be negative for this investment
        assert npv < 0
        assert isinstance(npv, float)
    
    def test_npv_zero_discount_rate(self):
        """Test NPV calculation with zero discount rate."""
        cash_flows = [-100000, 30000, 35000, 40000, 45000]
        discount_rate = 0.0
        
        npv = calculate_npv(cash_flows, discount_rate)
        
        # With zero discount rate, NPV should equal sum of cash flows
        expected_npv = sum(cash_flows)
        assert abs(npv - expected_npv) < 0.01
    
    def test_npv_single_cash_flow(self):
        """Test NPV calculation with single cash flow."""
        cash_flows = [-100000, 150000]
        discount_rate = 0.10
        
        npv = calculate_npv(cash_flows, discount_rate)
        
        # NPV = -100000 + 150000 / (1 + 0.10)^1 = 36363.64
        expected_npv = -100000 + 150000 / (1 + 0.10)
        assert abs(npv - expected_npv) < 0.01
    
    def test_npv_empty_cash_flows(self):
        """Test NPV calculation with empty cash flows."""
        cash_flows = []
        discount_rate = 0.10
        
        with pytest.raises(ValueError) as exc_info:
            calculate_npv(cash_flows, discount_rate)
        
        assert "Cash flows cannot be empty" in str(exc_info.value)
    
    def test_npv_negative_discount_rate(self):
        """Test NPV calculation with negative discount rate."""
        cash_flows = [-100000, 30000, 35000, 40000]
        discount_rate = -0.05
        
        with pytest.raises(ValueError) as exc_info:
            calculate_npv(cash_flows, discount_rate)
        
        assert "Discount rate cannot be negative" in str(exc_info.value)
    
    def test_npv_high_discount_rate(self):
        """Test NPV calculation with high discount rate."""
        cash_flows = [-100000, 30000, 35000, 40000, 45000]
        discount_rate = 0.50
        
        npv = calculate_npv(cash_flows, discount_rate)
        
        # With high discount rate, NPV should be negative
        assert npv < 0
        assert isinstance(npv, float)


class TestCalculateIRR:
    """Test Internal Rate of Return calculation."""
    
    def test_irr_positive_investment(self):
        """Test IRR calculation for positive investment."""
        cash_flows = [-100000, 30000, 35000, 40000, 45000]
        
        irr = calculate_irr(cash_flows)
        
        # IRR should be positive and reasonable
        assert irr > 0
        assert irr < 1.0  # Less than 100%
        assert isinstance(irr, float)
    
    def test_irr_negative_investment(self):
        """Test IRR calculation for negative investment."""
        cash_flows = [-100000, 10000, 15000, 20000, 25000]
        
        irr = calculate_irr(cash_flows)
        
        # IRR should be low or negative
        assert irr < 0.20  # Less than 20%
        assert isinstance(irr, float)
    
    def test_irr_no_positive_cash_flows(self):
        """Test IRR calculation with no positive cash flows."""
        cash_flows = [-100000, -10000, -15000, -20000]
        
        irr = calculate_irr(cash_flows)
        
        # IRR should be None or negative
        assert irr is None or irr < 0
    
    def test_irr_single_cash_flow(self):
        """Test IRR calculation with single cash flow."""
        cash_flows = [-100000, 150000]
        
        irr = calculate_irr(cash_flows)
        
        # IRR = (150000 / 100000) - 1 = 0.5 = 50%
        expected_irr = 0.5
        assert abs(irr - expected_irr) < 0.01
    
    def test_irr_empty_cash_flows(self):
        """Test IRR calculation with empty cash flows."""
        cash_flows = []
        
        with pytest.raises(ValueError) as exc_info:
            calculate_irr(cash_flows)
        
        assert "Cash flows cannot be empty" in str(exc_info.value)
    
    def test_irr_all_positive_cash_flows(self):
        """Test IRR calculation with all positive cash flows."""
        cash_flows = [100000, 30000, 35000, 40000]
        
        irr = calculate_irr(cash_flows)
        
        # IRR should be very high or infinite
        assert irr is None or irr > 1.0
    
    def test_irr_convergence_issue(self):
        """Test IRR calculation with convergence issues."""
        # Cash flows that might cause convergence issues
        cash_flows = [-100000, 200000, -150000, 100000]
        
        irr = calculate_irr(cash_flows)
        
        # Should handle convergence issues gracefully
        assert irr is None or isinstance(irr, float)


class TestCalculateROI:
    """Test Return on Investment calculation."""
    
    def test_roi_positive_return(self):
        """Test ROI calculation for positive return."""
        initial_investment = 100000
        final_value = 150000
        
        roi = calculate_roi(initial_investment, final_value)
        
        # ROI = (150000 - 100000) / 100000 = 0.5 = 50%
        expected_roi = 0.5
        assert abs(roi - expected_roi) < 0.01
    
    def test_roi_negative_return(self):
        """Test ROI calculation for negative return."""
        initial_investment = 100000
        final_value = 80000
        
        roi = calculate_roi(initial_investment, final_value)
        
        # ROI = (80000 - 100000) / 100000 = -0.2 = -20%
        expected_roi = -0.2
        assert abs(roi - expected_roi) < 0.01
    
    def test_roi_zero_return(self):
        """Test ROI calculation for zero return."""
        initial_investment = 100000
        final_value = 100000
        
        roi = calculate_roi(initial_investment, final_value)
        
        # ROI = (100000 - 100000) / 100000 = 0 = 0%
        assert roi == 0.0
    
    def test_roi_zero_investment(self):
        """Test ROI calculation with zero investment."""
        initial_investment = 0
        final_value = 50000
        
        with pytest.raises(ValueError) as exc_info:
            calculate_roi(initial_investment, final_value)
        
        assert "Initial investment cannot be zero" in str(exc_info.value)
    
    def test_roi_negative_investment(self):
        """Test ROI calculation with negative investment."""
        initial_investment = -100000
        final_value = 50000
        
        with pytest.raises(ValueError) as exc_info:
            calculate_roi(initial_investment, final_value)
        
        assert "Initial investment cannot be negative" in str(exc_info.value)
    
    def test_roi_with_time_period(self):
        """Test ROI calculation with time period."""
        initial_investment = 100000
        final_value = 150000
        years = 3
        
        annualized_roi = calculate_roi(initial_investment, final_value, years)
        
        # Annualized ROI = (150000 / 100000)^(1/3) - 1 ≈ 0.144 = 14.4%
        expected_roi = (final_value / initial_investment) ** (1/years) - 1
        assert abs(annualized_roi - expected_roi) < 0.01
    
    def test_roi_zero_time_period(self):
        """Test ROI calculation with zero time period."""
        initial_investment = 100000
        final_value = 150000
        years = 0
        
        with pytest.raises(ValueError) as exc_info:
            calculate_roi(initial_investment, final_value, years)
        
        assert "Time period cannot be zero or negative" in str(exc_info.value)


class TestCalculatePaybackPeriod:
    """Test Payback Period calculation."""
    
    def test_payback_period_even_cash_flows(self):
        """Test payback period with even cash flows."""
        initial_investment = 100000
        annual_cash_flows = [25000, 25000, 25000, 25000, 25000]
        
        payback_period = calculate_payback_period(initial_investment, annual_cash_flows)
        
        # Payback period = 100000 / 25000 = 4 years
        expected_payback = 4.0
        assert abs(payback_period - expected_payback) < 0.01
    
    def test_payback_period_uneven_cash_flows(self):
        """Test payback period with uneven cash flows."""
        initial_investment = 100000
        annual_cash_flows = [20000, 30000, 40000, 50000, 60000]
        
        payback_period = calculate_payback_period(initial_investment, annual_cash_flows)
        
        # Cumulative: 20000, 50000, 90000, 140000
        # Payback occurs between year 3 and 4
        # Payback = 3 + (100000 - 90000) / 50000 = 3.2 years
        expected_payback = 3.2
        assert abs(payback_period - expected_payback) < 0.01
    
    def test_payback_period_insufficient_cash_flows(self):
        """Test payback period with insufficient cash flows."""
        initial_investment = 100000
        annual_cash_flows = [10000, 15000, 20000, 25000]
        
        payback_period = calculate_payback_period(initial_investment, annual_cash_flows)
        
        # Total cash flows = 70000 < 100000, so payback never occurs
        assert payback_period is None
    
    def test_payback_period_immediate_return(self):
        """Test payback period with immediate return."""
        initial_investment = 100000
        annual_cash_flows = [150000, 50000, 30000]
        
        payback_period = calculate_payback_period(initial_investment, annual_cash_flows)
        
        # Payback occurs in first year
        expected_payback = 100000 / 150000  # ≈ 0.67 years
        assert abs(payback_period - expected_payback) < 0.01
    
    def test_payback_period_zero_investment(self):
        """Test payback period with zero investment."""
        initial_investment = 0
        annual_cash_flows = [10000, 20000, 30000]
        
        payback_period = calculate_payback_period(initial_investment, annual_cash_flows)
        
        # Zero investment means immediate payback
        assert payback_period == 0.0
    
    def test_payback_period_negative_investment(self):
        """Test payback period with negative investment."""
        initial_investment = -100000
        annual_cash_flows = [10000, 20000, 30000]
        
        with pytest.raises(ValueError) as exc_info:
            calculate_payback_period(initial_investment, annual_cash_flows)
        
        assert "Initial investment cannot be negative" in str(exc_info.value)
    
    def test_payback_period_empty_cash_flows(self):
        """Test payback period with empty cash flows."""
        initial_investment = 100000
        annual_cash_flows = []
        
        with pytest.raises(ValueError) as exc_info:
            calculate_payback_period(initial_investment, annual_cash_flows)
        
        assert "Cash flows cannot be empty" in str(exc_info.value)
    
    def test_payback_period_negative_cash_flows(self):
        """Test payback period with negative cash flows."""
        initial_investment = 100000
        annual_cash_flows = [-10000, -20000, -30000]
        
        payback_period = calculate_payback_period(initial_investment, annual_cash_flows)
        
        # Negative cash flows mean no payback
        assert payback_period is None


class TestCalculateBreakEvenPoint:
    """Test Break-Even Point calculation."""
    
    def test_break_even_basic(self):
        """Test basic break-even calculation."""
        fixed_costs = 50000
        variable_cost_per_unit = 10
        price_per_unit = 25
        
        break_even = calculate_break_even_point(fixed_costs, variable_cost_per_unit, price_per_unit)
        
        # Break-even = 50000 / (25 - 10) = 3333.33 units
        expected_break_even = 50000 / (25 - 10)
        assert abs(break_even - expected_break_even) < 0.01
    
    def test_break_even_zero_margin(self):
        """Test break-even with zero margin."""
        fixed_costs = 50000
        variable_cost_per_unit = 25
        price_per_unit = 25
        
        with pytest.raises(ValueError) as exc_info:
            calculate_break_even_point(fixed_costs, variable_cost_per_unit, price_per_unit)
        
        assert "Price per unit must be greater than variable cost per unit" in str(exc_info.value)
    
    def test_break_even_negative_margin(self):
        """Test break-even with negative margin."""
        fixed_costs = 50000
        variable_cost_per_unit = 30
        price_per_unit = 25
        
        with pytest.raises(ValueError) as exc_info:
            calculate_break_even_point(fixed_costs, variable_cost_per_unit, price_per_unit)
        
        assert "Price per unit must be greater than variable cost per unit" in str(exc_info.value)
    
    def test_break_even_negative_fixed_costs(self):
        """Test break-even with negative fixed costs."""
        fixed_costs = -50000
        variable_cost_per_unit = 10
        price_per_unit = 25
        
        with pytest.raises(ValueError) as exc_info:
            calculate_break_even_point(fixed_costs, variable_cost_per_unit, price_per_unit)
        
        assert "Fixed costs cannot be negative" in str(exc_info.value)
    
    def test_break_even_zero_fixed_costs(self):
        """Test break-even with zero fixed costs."""
        fixed_costs = 0
        variable_cost_per_unit = 10
        price_per_unit = 25
        
        break_even = calculate_break_even_point(fixed_costs, variable_cost_per_unit, price_per_unit)
        
        # With zero fixed costs, break-even should be zero
        assert break_even == 0.0


class TestAnalyzeCashFlow:
    """Test Cash Flow Analysis."""
    
    def test_cash_flow_analysis_basic(self):
        """Test basic cash flow analysis."""
        cash_flows = [-100000, 30000, 35000, 40000, 45000]
        
        analysis = analyze_cash_flow(cash_flows)
        
        assert isinstance(analysis, dict)
        assert "total_inflows" in analysis
        assert "total_outflows" in analysis
        assert "net_cash_flow" in analysis
        assert "cumulative_cash_flows" in analysis
        assert "payback_period" in analysis
        
        # Check calculations
        assert analysis["total_inflows"] == 150000  # 30000 + 35000 + 40000 + 45000
        assert analysis["total_outflows"] == 100000
        assert analysis["net_cash_flow"] == 50000
        assert len(analysis["cumulative_cash_flows"]) == 5
    
    def test_cash_flow_analysis_all_positive(self):
        """Test cash flow analysis with all positive flows."""
        cash_flows = [10000, 20000, 30000, 40000]
        
        analysis = analyze_cash_flow(cash_flows)
        
        assert analysis["total_inflows"] == 100000
        assert analysis["total_outflows"] == 0
        assert analysis["net_cash_flow"] == 100000
        assert analysis["payback_period"] == 0  # Immediate payback
    
    def test_cash_flow_analysis_all_negative(self):
        """Test cash flow analysis with all negative flows."""
        cash_flows = [-10000, -20000, -30000, -40000]
        
        analysis = analyze_cash_flow(cash_flows)
        
        assert analysis["total_inflows"] == 0
        assert analysis["total_outflows"] == 100000
        assert analysis["net_cash_flow"] == -100000
        assert analysis["payback_period"] is None
    
    def test_cash_flow_analysis_empty(self):
        """Test cash flow analysis with empty flows."""
        cash_flows = []
        
        with pytest.raises(ValueError) as exc_info:
            analyze_cash_flow(cash_flows)
        
        assert "Cash flows cannot be empty" in str(exc_info.value)


class TestCalculateWACC:
    """Test Weighted Average Cost of Capital calculation."""
    
    def test_wacc_basic(self):
        """Test basic WACC calculation."""
        cost_of_equity = 0.12
        cost_of_debt = 0.08
        tax_rate = 0.30
        market_value_equity = 600000
        market_value_debt = 400000
        
        wacc = calculate_wacc(
            cost_of_equity, cost_of_debt, tax_rate,
            market_value_equity, market_value_debt
        )
        
        # WACC = (E/V * Re) + (D/V * Rd * (1-T))
        # E/V = 600000/1000000 = 0.6
        # D/V = 400000/1000000 = 0.4
        # WACC = (0.6 * 0.12) + (0.4 * 0.08 * 0.7) = 0.072 + 0.0224 = 0.0944
        expected_wacc = 0.0944
        assert abs(wacc - expected_wacc) < 0.001
    
    def test_wacc_no_debt(self):
        """Test WACC calculation with no debt."""
        cost_of_equity = 0.12
        cost_of_debt = 0.08
        tax_rate = 0.30
        market_value_equity = 1000000
        market_value_debt = 0
        
        wacc = calculate_wacc(
            cost_of_equity, cost_of_debt, tax_rate,
            market_value_equity, market_value_debt
        )
        
        # With no debt, WACC should equal cost of equity
        assert abs(wacc - cost_of_equity) < 0.001
    
    def test_wacc_no_equity(self):
        """Test WACC calculation with no equity."""
        cost_of_equity = 0.12
        cost_of_debt = 0.08
        tax_rate = 0.30
        market_value_equity = 0
        market_value_debt = 1000000
        
        wacc = calculate_wacc(
            cost_of_equity, cost_of_debt, tax_rate,
            market_value_equity, market_value_debt
        )
        
        # With no equity, WACC should equal after-tax cost of debt
        expected_wacc = cost_of_debt * (1 - tax_rate)
        assert abs(wacc - expected_wacc) < 0.001
    
    def test_wacc_zero_values(self):
        """Test WACC calculation with zero values."""
        cost_of_equity = 0.12
        cost_of_debt = 0.08
        tax_rate = 0.30
        market_value_equity = 0
        market_value_debt = 0
        
        with pytest.raises(ValueError) as exc_info:
            calculate_wacc(
                cost_of_equity, cost_of_debt, tax_rate,
                market_value_equity, market_value_debt
            )
        
        assert "Total market value cannot be zero" in str(exc_info.value)
    
    def test_wacc_negative_values(self):
        """Test WACC calculation with negative values."""
        cost_of_equity = -0.12
        cost_of_debt = 0.08
        tax_rate = 0.30
        market_value_equity = 600000
        market_value_debt = 400000
        
        with pytest.raises(ValueError) as exc_info:
            calculate_wacc(
                cost_of_equity, cost_of_debt, tax_rate,
                market_value_equity, market_value_debt
            )
        
        assert "Costs cannot be negative" in str(exc_info.value)
    
    def test_wacc_invalid_tax_rate(self):
        """Test WACC calculation with invalid tax rate."""
        cost_of_equity = 0.12
        cost_of_debt = 0.08
        tax_rate = 1.5  # Invalid tax rate > 1
        market_value_equity = 600000
        market_value_debt = 400000
        
        with pytest.raises(ValueError) as exc_info:
            calculate_wacc(
                cost_of_equity, cost_of_debt, tax_rate,
                market_value_equity, market_value_debt
            )
        
        assert "Tax rate must be between 0 and 1" in str(exc_info.value)


class TestPerformSensitivityAnalysis:
    """Test Sensitivity Analysis."""
    
    def test_sensitivity_analysis_basic(self):
        """Test basic sensitivity analysis."""
        base_case = {
            "revenue": 1000000,
            "costs": 600000,
            "discount_rate": 0.10
        }
        
        variables = {
            "revenue": [0.8, 0.9, 1.0, 1.1, 1.2],
            "costs": [0.8, 0.9, 1.0, 1.1, 1.2]
        }
        
        analysis = perform_sensitivity_analysis(base_case, variables)
        
        assert isinstance(analysis, dict)
        assert "results" in analysis
        assert "tornado_chart_data" in analysis
        assert len(analysis["results"]) == 2  # Two variables
        
        # Check that revenue and costs are analyzed
        assert "revenue" in analysis["results"]
        assert "costs" in analysis["results"]
    
    def test_sensitivity_analysis_empty_variables(self):
        """Test sensitivity analysis with empty variables."""
        base_case = {"revenue": 1000000, "costs": 600000}
        variables = {}
        
        analysis = perform_sensitivity_analysis(base_case, variables)
        
        assert analysis["results"] == {}
        assert analysis["tornado_chart_data"] == []
    
    def test_sensitivity_analysis_single_variable(self):
        """Test sensitivity analysis with single variable."""
        base_case = {"revenue": 1000000, "costs": 600000}
        variables = {"revenue": [0.8, 0.9, 1.0, 1.1, 1.2]}
        
        analysis = perform_sensitivity_analysis(base_case, variables)
        
        assert len(analysis["results"]) == 1
        assert "revenue" in analysis["results"]
        assert len(analysis["results"]["revenue"]) == 5


class TestCalculateProfitabilityIndex:
    """Test Profitability Index calculation."""
    
    def test_profitability_index_positive(self):
        """Test profitability index for positive investment."""
        cash_flows = [-100000, 30000, 35000, 40000, 45000]
        discount_rate = 0.10
        
        pi = calculate_profitability_index(cash_flows, discount_rate)
        
        # PI should be greater than 1 for positive NPV investments
        assert pi > 1.0
        assert isinstance(pi, float)
    
    def test_profitability_index_negative(self):
        """Test profitability index for negative investment."""
        cash_flows = [-100000, 10000, 15000, 20000, 25000]
        discount_rate = 0.15
        
        pi = calculate_profitability_index(cash_flows, discount_rate)
        
        # PI should be less than 1 for negative NPV investments
        assert pi < 1.0
        assert isinstance(pi, float)
    
    def test_profitability_index_zero_investment(self):
        """Test profitability index with zero initial investment."""
        cash_flows = [0, 30000, 35000, 40000]
        discount_rate = 0.10
        
        with pytest.raises(ValueError) as exc_info:
            calculate_profitability_index(cash_flows, discount_rate)
        
        assert "Initial investment cannot be zero" in str(exc_info.value)
    
    def test_profitability_index_positive_initial_investment(self):
        """Test profitability index with positive initial investment."""
        cash_flows = [100000, 30000, 35000, 40000]  # Positive initial
        discount_rate = 0.10
        
        with pytest.raises(ValueError) as exc_info:
            calculate_profitability_index(cash_flows, discount_rate)
        
        assert "Initial investment should be negative" in str(exc_info.value)