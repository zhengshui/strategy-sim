"""
Financial analysis tools for the Investor Agent.

Contains tools for financial calculations including NPV, IRR, payback period,
cash flow analysis, and sensitivity analysis.
"""

import math
from typing import Dict, List, Optional, Tuple, Any
from pydantic import BaseModel, Field, validator
import numpy as np


class CashFlowAnalysis(BaseModel):
    """Cash flow analysis result."""
    
    periods: List[int] = Field(..., description="Time periods")
    cash_flows: List[float] = Field(..., description="Cash flows for each period")
    discount_rate: float = Field(..., description="Discount rate used")
    npv: float = Field(..., description="Net Present Value")
    irr: Optional[float] = Field(None, description="Internal Rate of Return")
    payback_period: Optional[float] = Field(None, description="Payback period in years")
    discounted_payback: Optional[float] = Field(None, description="Discounted payback period")
    profitability_index: float = Field(..., description="Profitability index")
    
    @validator('cash_flows')
    def validate_cash_flows(cls, v: List[float]) -> List[float]:
        """Ensure cash flows are provided."""
        if not v:
            raise ValueError("Cash flows cannot be empty")
        return v


class SensitivityAnalysis(BaseModel):
    """Sensitivity analysis result."""
    
    variable_name: str = Field(..., description="Variable being analyzed")
    base_value: float = Field(..., description="Base value of the variable")
    sensitivity_range: List[float] = Field(..., description="Range of values tested")
    npv_impacts: List[float] = Field(..., description="NPV impacts for each value")
    elasticity: float = Field(..., description="Elasticity of NPV to variable change")
    
    @validator('sensitivity_range')
    def validate_range(cls, v: List[float], values: Dict[str, Any]) -> List[float]:
        """Ensure sensitivity range is valid."""
        if len(v) != len(values.get('npv_impacts', [])):
            raise ValueError("Sensitivity range and NPV impacts must have same length")
        return v


class FinancialRatios(BaseModel):
    """Financial ratios analysis."""
    
    revenue: float = Field(..., description="Revenue")
    costs: float = Field(..., description="Total costs")
    gross_margin: float = Field(..., description="Gross margin percentage")
    operating_margin: float = Field(..., description="Operating margin percentage")
    net_margin: float = Field(..., description="Net margin percentage")
    roe: Optional[float] = Field(None, description="Return on Equity")
    roa: Optional[float] = Field(None, description="Return on Assets")
    debt_to_equity: Optional[float] = Field(None, description="Debt to Equity ratio")
    current_ratio: Optional[float] = Field(None, description="Current ratio")
    
    @validator('gross_margin', 'operating_margin', 'net_margin')
    def validate_margins(cls, v: float) -> float:
        """Ensure margins are reasonable."""
        if v < -100 or v > 100:
            raise ValueError("Margins should be between -100% and 100%")
        return v


class InvestmentMetrics(BaseModel):
    """Investment performance metrics."""
    
    initial_investment: float = Field(..., description="Initial investment amount")
    total_returns: float = Field(..., description="Total returns generated")
    annualized_return: float = Field(..., description="Annualized return rate")
    volatility: float = Field(..., description="Return volatility")
    sharpe_ratio: float = Field(..., description="Sharpe ratio")
    max_drawdown: float = Field(..., description="Maximum drawdown")
    var_95: float = Field(..., description="95% Value at Risk")
    
    @validator('initial_investment')
    def validate_investment(cls, v: float) -> float:
        """Ensure investment is positive."""
        if v <= 0:
            raise ValueError("Initial investment must be positive")
        return v


async def calculate_npv(cash_flows: List[float], discount_rate: float) -> float:
    """
    Calculate Net Present Value.
    
    Args:
        cash_flows: List of cash flows (first element is initial investment, typically negative)
        discount_rate: Discount rate as decimal (e.g., 0.10 for 10%)
    
    Returns:
        Net Present Value
    """
    if not cash_flows:
        raise ValueError("Cash flows cannot be empty")
    
    npv = 0.0
    for i, cf in enumerate(cash_flows):
        npv += cf / ((1 + discount_rate) ** i)
    
    return npv


async def calculate_irr(cash_flows: List[float], max_iterations: int = 100) -> Optional[float]:
    """
    Calculate Internal Rate of Return using Newton-Raphson method.
    
    Args:
        cash_flows: List of cash flows
        max_iterations: Maximum iterations for convergence
    
    Returns:
        Internal Rate of Return as decimal, or None if no solution found
    """
    if not cash_flows or len(cash_flows) < 2:
        return None
    
    # Initial guess
    rate = 0.1
    tolerance = 1e-6
    
    for _ in range(max_iterations):
        npv = sum(cf / ((1 + rate) ** i) for i, cf in enumerate(cash_flows))
        
        if abs(npv) < tolerance:
            return rate
        
        # Calculate derivative
        derivative = sum(-i * cf / ((1 + rate) ** (i + 1)) for i, cf in enumerate(cash_flows))
        
        if abs(derivative) < tolerance:
            break
        
        rate = rate - npv / derivative
        
        # Prevent negative rates
        if rate < -0.99:
            rate = -0.99
    
    return rate if abs(npv) < tolerance else None


async def calculate_payback_period(cash_flows: List[float]) -> Optional[float]:
    """
    Calculate payback period.
    
    Args:
        cash_flows: List of cash flows
    
    Returns:
        Payback period in years, or None if not recovered
    """
    if not cash_flows:
        return None
    
    cumulative = 0.0
    for i, cf in enumerate(cash_flows):
        cumulative += cf
        if cumulative >= 0:
            if i == 0:
                return 0.0
            # Linear interpolation for more accurate payback
            if cash_flows[i] != 0:
                return i - 1 + (cumulative - cf) / (-cf)
            return float(i)
    
    return None


async def calculate_discounted_payback(cash_flows: List[float], discount_rate: float) -> Optional[float]:
    """
    Calculate discounted payback period.
    
    Args:
        cash_flows: List of cash flows
        discount_rate: Discount rate as decimal
    
    Returns:
        Discounted payback period in years, or None if not recovered
    """
    if not cash_flows:
        return None
    
    cumulative = 0.0
    for i, cf in enumerate(cash_flows):
        discounted_cf = cf / ((1 + discount_rate) ** i)
        cumulative += discounted_cf
        if cumulative >= 0:
            if i == 0:
                return 0.0
            # Linear interpolation
            prev_discounted = cash_flows[i-1] / ((1 + discount_rate) ** (i-1))
            if discounted_cf != 0:
                return i - 1 + (cumulative - discounted_cf) / (-discounted_cf)
            return float(i)
    
    return None


async def calculate_profitability_index(cash_flows: List[float], discount_rate: float) -> float:
    """
    Calculate Profitability Index.
    
    Args:
        cash_flows: List of cash flows
        discount_rate: Discount rate as decimal
    
    Returns:
        Profitability Index
    """
    if not cash_flows:
        return 0.0
    
    initial_investment = abs(cash_flows[0])
    if initial_investment == 0:
        return float('inf')
    
    pv_future_flows = sum(cf / ((1 + discount_rate) ** i) for i, cf in enumerate(cash_flows[1:], 1))
    
    return pv_future_flows / initial_investment


async def perform_cash_flow_analysis(
    cash_flows: List[float], 
    discount_rate: float,
    periods: Optional[List[int]] = None
) -> CashFlowAnalysis:
    """
    Perform comprehensive cash flow analysis.
    
    Args:
        cash_flows: List of cash flows
        discount_rate: Discount rate as decimal
        periods: Time periods (defaults to 0, 1, 2, ...)
    
    Returns:
        CashFlowAnalysis object with all metrics
    """
    if periods is None:
        periods = list(range(len(cash_flows)))
    
    npv = await calculate_npv(cash_flows, discount_rate)
    irr = await calculate_irr(cash_flows)
    payback = await calculate_payback_period(cash_flows)
    discounted_payback = await calculate_discounted_payback(cash_flows, discount_rate)
    pi = await calculate_profitability_index(cash_flows, discount_rate)
    
    return CashFlowAnalysis(
        periods=periods,
        cash_flows=cash_flows,
        discount_rate=discount_rate,
        npv=npv,
        irr=irr,
        payback_period=payback,
        discounted_payback=discounted_payback,
        profitability_index=pi
    )


async def sensitivity_analysis(
    base_cash_flows: List[float],
    base_discount_rate: float,
    variable_name: str,
    variable_impacts: List[Tuple[float, List[float]]],
    base_value: float
) -> SensitivityAnalysis:
    """
    Perform sensitivity analysis on a variable.
    
    Args:
        base_cash_flows: Base case cash flows
        base_discount_rate: Base discount rate
        variable_name: Name of the variable being analyzed
        variable_impacts: List of (value, modified_cash_flows) tuples
        base_value: Base value of the variable
    
    Returns:
        SensitivityAnalysis object
    """
    base_npv = await calculate_npv(base_cash_flows, base_discount_rate)
    
    values = []
    npv_impacts = []
    
    for value, cash_flows in variable_impacts:
        values.append(value)
        npv = await calculate_npv(cash_flows, base_discount_rate)
        npv_impacts.append(npv - base_npv)
    
    # Calculate elasticity (% change in NPV / % change in variable)
    if len(values) >= 2 and base_value != 0:
        value_change = (values[-1] - values[0]) / base_value
        npv_change = (npv_impacts[-1] - npv_impacts[0]) / base_npv if base_npv != 0 else 0
        elasticity = npv_change / value_change if value_change != 0 else 0
    else:
        elasticity = 0
    
    return SensitivityAnalysis(
        variable_name=variable_name,
        base_value=base_value,
        sensitivity_range=values,
        npv_impacts=npv_impacts,
        elasticity=elasticity
    )


async def calculate_financial_ratios(
    revenue: float,
    cost_of_goods_sold: float,
    operating_expenses: float,
    interest_expense: float = 0.0,
    tax_rate: float = 0.0,
    equity: Optional[float] = None,
    assets: Optional[float] = None,
    debt: Optional[float] = None,
    current_assets: Optional[float] = None,
    current_liabilities: Optional[float] = None
) -> FinancialRatios:
    """
    Calculate key financial ratios.
    
    Args:
        revenue: Total revenue
        cost_of_goods_sold: Cost of goods sold
        operating_expenses: Operating expenses
        interest_expense: Interest expense
        tax_rate: Tax rate as decimal
        equity: Shareholders' equity
        assets: Total assets
        debt: Total debt
        current_assets: Current assets
        current_liabilities: Current liabilities
    
    Returns:
        FinancialRatios object
    """
    gross_profit = revenue - cost_of_goods_sold
    operating_income = gross_profit - operating_expenses
    net_income = operating_income - interest_expense - (operating_income * tax_rate)
    
    gross_margin = (gross_profit / revenue * 100) if revenue > 0 else 0
    operating_margin = (operating_income / revenue * 100) if revenue > 0 else 0
    net_margin = (net_income / revenue * 100) if revenue > 0 else 0
    
    roe = (net_income / equity * 100) if equity and equity > 0 else None
    roa = (net_income / assets * 100) if assets and assets > 0 else None
    debt_to_equity = (debt / equity) if equity and equity > 0 and debt is not None else None
    current_ratio = (current_assets / current_liabilities) if current_liabilities and current_liabilities > 0 and current_assets is not None else None
    
    return FinancialRatios(
        revenue=revenue,
        costs=cost_of_goods_sold + operating_expenses,
        gross_margin=gross_margin,
        operating_margin=operating_margin,
        net_margin=net_margin,
        roe=roe,
        roa=roa,
        debt_to_equity=debt_to_equity,
        current_ratio=current_ratio
    )


async def calculate_investment_metrics(
    returns: List[float],
    initial_investment: float,
    risk_free_rate: float = 0.02
) -> InvestmentMetrics:
    """
    Calculate investment performance metrics.
    
    Args:
        returns: List of periodic returns
        initial_investment: Initial investment amount
        risk_free_rate: Risk-free rate for Sharpe ratio calculation
    
    Returns:
        InvestmentMetrics object
    """
    if not returns:
        raise ValueError("Returns cannot be empty")
    
    returns_array = np.array(returns)
    
    # Calculate total returns
    total_returns = np.sum(returns_array)
    
    # Calculate annualized return
    periods = len(returns)
    annualized_return = (1 + total_returns / initial_investment) ** (1 / periods) - 1
    
    # Calculate volatility (standard deviation of returns)
    volatility = np.std(returns_array)
    
    # Calculate Sharpe ratio
    excess_return = annualized_return - risk_free_rate
    sharpe_ratio = excess_return / volatility if volatility > 0 else 0
    
    # Calculate maximum drawdown
    cumulative_returns = np.cumsum(returns_array)
    peak = np.maximum.accumulate(cumulative_returns)
    drawdown = (cumulative_returns - peak) / peak
    max_drawdown = np.min(drawdown)
    
    # Calculate 95% Value at Risk
    var_95 = np.percentile(returns_array, 5)
    
    return InvestmentMetrics(
        initial_investment=initial_investment,
        total_returns=total_returns,
        annualized_return=annualized_return,
        volatility=volatility,
        sharpe_ratio=sharpe_ratio,
        max_drawdown=max_drawdown,
        var_95=var_95
    )


async def break_even_analysis(
    fixed_costs: float,
    variable_cost_per_unit: float,
    price_per_unit: float
) -> Dict[str, float]:
    """
    Calculate break-even analysis metrics.
    
    Args:
        fixed_costs: Fixed costs
        variable_cost_per_unit: Variable cost per unit
        price_per_unit: Price per unit
    
    Returns:
        Dictionary with break-even metrics
    """
    if price_per_unit <= variable_cost_per_unit:
        raise ValueError("Price per unit must be greater than variable cost per unit")
    
    contribution_margin = price_per_unit - variable_cost_per_unit
    break_even_units = fixed_costs / contribution_margin
    break_even_revenue = break_even_units * price_per_unit
    margin_of_safety_units = lambda target_units: target_units - break_even_units
    
    return {
        "break_even_units": break_even_units,
        "break_even_revenue": break_even_revenue,
        "contribution_margin": contribution_margin,
        "contribution_margin_ratio": contribution_margin / price_per_unit,
        "operating_leverage": contribution_margin / (contribution_margin - fixed_costs) if contribution_margin > fixed_costs else float('inf')
    }