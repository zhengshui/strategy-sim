"""
Risk modeling and analysis tools for the Analyst Agent.

Contains tools for Monte Carlo simulation, probability analysis,
scenario planning, and quantitative risk assessment.
"""

import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any, Callable
from pydantic import BaseModel, Field, validator
import numpy as np
from enum import Enum


class RiskType(str, Enum):
    """Types of risk categories."""
    
    MARKET = "market"
    FINANCIAL = "financial"
    OPERATIONAL = "operational"
    STRATEGIC = "strategic"
    REGULATORY = "regulatory"
    TECHNOLOGY = "technology"
    REPUTATION = "reputation"
    ENVIRONMENTAL = "environmental"


class ProbabilityDistribution(str, Enum):
    """Probability distribution types."""
    
    NORMAL = "normal"
    UNIFORM = "uniform"
    TRIANGULAR = "triangular"
    BETA = "beta"
    EXPONENTIAL = "exponential"
    LOGNORMAL = "lognormal"


class ScenarioType(str, Enum):
    """Scenario analysis types."""
    
    BEST_CASE = "best_case"
    BASE_CASE = "base_case"
    WORST_CASE = "worst_case"
    STRESS_TEST = "stress_test"
    BLACK_SWAN = "black_swan"


class RiskVariable(BaseModel):
    """Risk variable definition for Monte Carlo simulation."""
    
    name: str = Field(..., description="Variable name")
    description: str = Field(..., description="Variable description")
    distribution: ProbabilityDistribution
    parameters: Dict[str, float] = Field(..., description="Distribution parameters")
    unit: Optional[str] = Field(None, description="Unit of measurement")
    correlation_matrix: Optional[Dict[str, float]] = Field(None, description="Correlations with other variables")
    
    @validator('parameters')
    def validate_parameters(cls, v: Dict[str, float], values: Dict[str, Any]) -> Dict[str, float]:
        """Validate distribution parameters."""
        distribution = values.get('distribution')
        
        if distribution == ProbabilityDistribution.NORMAL:
            if 'mean' not in v or 'std' not in v:
                raise ValueError("Normal distribution requires 'mean' and 'std' parameters")
        elif distribution == ProbabilityDistribution.UNIFORM:
            if 'min' not in v or 'max' not in v:
                raise ValueError("Uniform distribution requires 'min' and 'max' parameters")
        elif distribution == ProbabilityDistribution.TRIANGULAR:
            if 'min' not in v or 'max' not in v or 'mode' not in v:
                raise ValueError("Triangular distribution requires 'min', 'max', and 'mode' parameters")
        
        return v


class MonteCarloResult(BaseModel):
    """Monte Carlo simulation result."""
    
    variable_name: str = Field(..., description="Name of the output variable")
    iterations: int = Field(..., description="Number of simulation iterations")
    mean: float = Field(..., description="Mean value")
    std_dev: float = Field(..., description="Standard deviation")
    percentiles: Dict[str, float] = Field(..., description="Percentile values")
    var_95: float = Field(..., description="95% Value at Risk")
    cvar_95: float = Field(..., description="95% Conditional Value at Risk")
    probability_negative: float = Field(..., description="Probability of negative outcomes")
    confidence_intervals: Dict[str, Tuple[float, float]] = Field(..., description="Confidence intervals")
    
    @validator('iterations')
    def validate_iterations(cls, v: int) -> int:
        """Ensure sufficient iterations."""
        if v < 1000:
            raise ValueError("Monte Carlo simulation requires at least 1000 iterations")
        return v


class ScenarioAnalysis(BaseModel):
    """Scenario analysis result."""
    
    scenario_name: str = Field(..., description="Scenario name")
    scenario_type: ScenarioType
    assumptions: Dict[str, Any] = Field(..., description="Key assumptions")
    outcomes: Dict[str, float] = Field(..., description="Outcome metrics")
    probability: float = Field(..., ge=0.0, le=1.0, description="Scenario probability")
    impact_assessment: str = Field(..., description="Impact assessment")
    risk_factors: List[str] = Field(..., description="Key risk factors")
    mitigation_strategies: List[str] = Field(default_factory=list)
    
    @validator('scenario_name')
    def validate_scenario_name(cls, v: str) -> str:
        """Ensure scenario name is meaningful."""
        if not v.strip():
            raise ValueError("Scenario name cannot be empty")
        return v.strip()


class RiskMetric(BaseModel):
    """Risk metric calculation result."""
    
    metric_name: str = Field(..., description="Risk metric name")
    value: float = Field(..., description="Metric value")
    confidence_level: float = Field(..., ge=0.0, le=1.0, description="Confidence level")
    methodology: str = Field(..., description="Calculation methodology")
    assumptions: List[str] = Field(..., description="Key assumptions")
    limitations: List[str] = Field(default_factory=list)
    
    @validator('metric_name')
    def validate_metric_name(cls, v: str) -> str:
        """Ensure metric name is meaningful."""
        if not v.strip():
            raise ValueError("Metric name cannot be empty")
        return v.strip()


class SensitivityAnalysis(BaseModel):
    """Sensitivity analysis result."""
    
    base_case_value: float = Field(..., description="Base case output value")
    sensitivity_results: Dict[str, Dict[str, float]] = Field(..., description="Sensitivity results by variable")
    tornado_chart_data: List[Tuple[str, float]] = Field(..., description="Tornado chart data")
    most_sensitive_variables: List[str] = Field(..., description="Most sensitive variables")
    elasticity_measures: Dict[str, float] = Field(..., description="Elasticity measures")
    
    @property
    def highest_sensitivity_variable(self) -> str:
        """Get the variable with highest sensitivity."""
        if not self.tornado_chart_data:
            return ""
        return max(self.tornado_chart_data, key=lambda x: abs(x[1]))[0]


class RiskAssessment(BaseModel):
    """Comprehensive risk assessment result."""
    
    assessment_id: str = Field(..., description="Unique assessment identifier")
    decision_context: str = Field(..., description="Decision being assessed")
    risk_variables: List[RiskVariable] = Field(..., description="Risk variables analyzed")
    monte_carlo_results: List[MonteCarloResult] = Field(..., description="Monte Carlo simulation results")
    scenario_analyses: List[ScenarioAnalysis] = Field(..., description="Scenario analysis results")
    sensitivity_analysis: SensitivityAnalysis
    risk_metrics: List[RiskMetric] = Field(..., description="Calculated risk metrics")
    overall_risk_score: float = Field(..., ge=0.0, le=1.0, description="Overall risk score")
    confidence_level: float = Field(..., ge=0.0, le=1.0, description="Analysis confidence level")
    recommendations: List[str] = Field(..., description="Risk management recommendations")
    assessment_date: datetime = Field(default_factory=datetime.now)
    
    @validator('assessment_id')
    def validate_assessment_id(cls, v: str) -> str:
        """Ensure assessment ID is meaningful."""
        if not v.strip():
            raise ValueError("Assessment ID cannot be empty")
        return v.strip()


def generate_random_sample(distribution: ProbabilityDistribution, parameters: Dict[str, float], size: int = 1) -> np.ndarray:
    """
    Generate random samples from specified distribution.
    
    Args:
        distribution: Type of probability distribution
        parameters: Distribution parameters
        size: Number of samples to generate
    
    Returns:
        Array of random samples
    """
    if distribution == ProbabilityDistribution.NORMAL:
        return np.random.normal(parameters['mean'], parameters['std'], size)
    elif distribution == ProbabilityDistribution.UNIFORM:
        return np.random.uniform(parameters['min'], parameters['max'], size)
    elif distribution == ProbabilityDistribution.TRIANGULAR:
        return np.random.triangular(parameters['min'], parameters['mode'], parameters['max'], size)
    elif distribution == ProbabilityDistribution.BETA:
        return np.random.beta(parameters['alpha'], parameters['beta'], size)
    elif distribution == ProbabilityDistribution.EXPONENTIAL:
        return np.random.exponential(parameters['scale'], size)
    elif distribution == ProbabilityDistribution.LOGNORMAL:
        return np.random.lognormal(parameters['mean'], parameters['sigma'], size)
    else:
        raise ValueError(f"Unsupported distribution: {distribution}")


async def run_monte_carlo_simulation(
    risk_variables: List[RiskVariable],
    objective_function: Callable[[Dict[str, float]], float],
    iterations: int = 10000,
    random_seed: Optional[int] = None
) -> MonteCarloResult:
    """
    Run Monte Carlo simulation for risk analysis.
    
    Args:
        risk_variables: List of risk variables
        objective_function: Function to calculate objective value
        iterations: Number of simulation iterations
        random_seed: Random seed for reproducibility
    
    Returns:
        MonteCarloResult object
    """
    if random_seed is not None:
        np.random.seed(random_seed)
    
    results = []
    
    for _ in range(iterations):
        # Generate random values for each variable
        variable_values = {}
        for var in risk_variables:
            value = generate_random_sample(var.distribution, var.parameters, 1)[0]
            variable_values[var.name] = value
        
        # Calculate objective value
        objective_value = objective_function(variable_values)
        results.append(objective_value)
    
    results_array = np.array(results)
    
    # Calculate statistics
    mean = np.mean(results_array)
    std_dev = np.std(results_array)
    
    # Calculate percentiles
    percentiles = {
        'p5': np.percentile(results_array, 5),
        'p10': np.percentile(results_array, 10),
        'p25': np.percentile(results_array, 25),
        'p50': np.percentile(results_array, 50),
        'p75': np.percentile(results_array, 75),
        'p90': np.percentile(results_array, 90),
        'p95': np.percentile(results_array, 95)
    }
    
    # Calculate risk metrics
    var_95 = np.percentile(results_array, 5)  # 95% VaR
    cvar_95 = np.mean(results_array[results_array <= var_95])  # 95% CVaR
    probability_negative = np.mean(results_array < 0)
    
    # Calculate confidence intervals
    confidence_intervals = {
        '90%': (np.percentile(results_array, 5), np.percentile(results_array, 95)),
        '95%': (np.percentile(results_array, 2.5), np.percentile(results_array, 97.5)),
        '99%': (np.percentile(results_array, 0.5), np.percentile(results_array, 99.5))
    }
    
    return MonteCarloResult(
        variable_name="objective_value",
        iterations=iterations,
        mean=mean,
        std_dev=std_dev,
        percentiles=percentiles,
        var_95=var_95,
        cvar_95=cvar_95,
        probability_negative=probability_negative,
        confidence_intervals=confidence_intervals
    )


async def perform_scenario_analysis(
    base_case_assumptions: Dict[str, Any],
    scenario_definitions: Dict[str, Dict[str, Any]],
    outcome_calculator: Callable[[Dict[str, Any]], Dict[str, float]]
) -> List[ScenarioAnalysis]:
    """
    Perform scenario analysis for different risk scenarios.
    
    Args:
        base_case_assumptions: Base case assumptions
        scenario_definitions: Dictionary of scenario definitions
        outcome_calculator: Function to calculate outcomes
    
    Returns:
        List of ScenarioAnalysis objects
    """
    scenarios = []
    
    for scenario_name, scenario_def in scenario_definitions.items():
        # Merge base case with scenario-specific assumptions
        scenario_assumptions = {**base_case_assumptions, **scenario_def.get('assumptions', {})}
        
        # Calculate outcomes
        outcomes = outcome_calculator(scenario_assumptions)
        
        # Create scenario analysis
        scenario = ScenarioAnalysis(
            scenario_name=scenario_name,
            scenario_type=scenario_def.get('type', ScenarioType.BASE_CASE),
            assumptions=scenario_assumptions,
            outcomes=outcomes,
            probability=scenario_def.get('probability', 0.5),
            impact_assessment=scenario_def.get('impact_assessment', 'Impact assessment not provided'),
            risk_factors=scenario_def.get('risk_factors', []),
            mitigation_strategies=scenario_def.get('mitigation_strategies', [])
        )
        scenarios.append(scenario)
    
    return scenarios


async def calculate_sensitivity_analysis(
    base_case_inputs: Dict[str, float],
    variable_ranges: Dict[str, Tuple[float, float]],
    objective_function: Callable[[Dict[str, float]], float],
    num_points: int = 10
) -> SensitivityAnalysis:
    """
    Calculate sensitivity analysis for key variables.
    
    Args:
        base_case_inputs: Base case input values
        variable_ranges: Range of values for each variable
        objective_function: Function to calculate objective value
        num_points: Number of points to test for each variable
    
    Returns:
        SensitivityAnalysis object
    """
    base_case_value = objective_function(base_case_inputs)
    sensitivity_results = {}
    tornado_chart_data = []
    elasticity_measures = {}
    
    for var_name, (min_val, max_val) in variable_ranges.items():
        # Create test values
        test_values = np.linspace(min_val, max_val, num_points)
        outcomes = []
        
        for test_val in test_values:
            # Create modified inputs
            modified_inputs = base_case_inputs.copy()
            modified_inputs[var_name] = test_val
            
            # Calculate outcome
            outcome = objective_function(modified_inputs)
            outcomes.append(outcome)
        
        # Store results
        sensitivity_results[var_name] = {
            'input_values': test_values.tolist(),
            'output_values': outcomes,
            'range': max(outcomes) - min(outcomes)
        }
        
        # Calculate tornado chart data (impact of +/- 10% change)
        base_input_value = base_case_inputs[var_name]
        if base_input_value != 0:
            # Test +10% change
            modified_inputs_high = base_case_inputs.copy()
            modified_inputs_high[var_name] = base_input_value * 1.1
            outcome_high = objective_function(modified_inputs_high)
            
            # Test -10% change
            modified_inputs_low = base_case_inputs.copy()
            modified_inputs_low[var_name] = base_input_value * 0.9
            outcome_low = objective_function(modified_inputs_low)
            
            # Calculate impact
            impact = (outcome_high - outcome_low) / 2
            tornado_chart_data.append((var_name, impact))
            
            # Calculate elasticity
            if base_case_value != 0:
                elasticity = ((outcome_high - outcome_low) / base_case_value) / 0.2  # 20% change
                elasticity_measures[var_name] = elasticity
    
    # Sort tornado chart data by absolute impact
    tornado_chart_data.sort(key=lambda x: abs(x[1]), reverse=True)
    
    # Get most sensitive variables
    most_sensitive_variables = [var for var, _ in tornado_chart_data[:5]]
    
    return SensitivityAnalysis(
        base_case_value=base_case_value,
        sensitivity_results=sensitivity_results,
        tornado_chart_data=tornado_chart_data,
        most_sensitive_variables=most_sensitive_variables,
        elasticity_measures=elasticity_measures
    )


async def calculate_risk_metrics(
    historical_data: List[float],
    confidence_level: float = 0.95
) -> List[RiskMetric]:
    """
    Calculate various risk metrics from historical data.
    
    Args:
        historical_data: Historical performance data
        confidence_level: Confidence level for metrics
    
    Returns:
        List of RiskMetric objects
    """
    if not historical_data:
        raise ValueError("Historical data cannot be empty")
    
    data_array = np.array(historical_data)
    metrics = []
    
    # Value at Risk (VaR)
    var_percentile = (1 - confidence_level) * 100
    var_value = np.percentile(data_array, var_percentile)
    
    var_metric = RiskMetric(
        metric_name="Value at Risk (VaR)",
        value=var_value,
        confidence_level=confidence_level,
        methodology="Historical simulation",
        assumptions=["Past performance is representative of future risk"],
        limitations=["Does not capture tail risks beyond confidence level"]
    )
    metrics.append(var_metric)
    
    # Conditional Value at Risk (CVaR)
    cvar_value = np.mean(data_array[data_array <= var_value])
    
    cvar_metric = RiskMetric(
        metric_name="Conditional Value at Risk (CVaR)",
        value=cvar_value,
        confidence_level=confidence_level,
        methodology="Expected shortfall calculation",
        assumptions=["Linear relationship between historical and future losses"],
        limitations=["Assumes stable distribution of returns"]
    )
    metrics.append(cvar_metric)
    
    # Maximum Drawdown
    cumulative_returns = np.cumsum(data_array)
    peak = np.maximum.accumulate(cumulative_returns)
    drawdown = (cumulative_returns - peak) / peak
    max_drawdown = np.min(drawdown)
    
    drawdown_metric = RiskMetric(
        metric_name="Maximum Drawdown",
        value=max_drawdown,
        confidence_level=1.0,
        methodology="Peak-to-trough decline calculation",
        assumptions=["Drawdown pattern is representative"],
        limitations=["Historical measure may not predict future drawdowns"]
    )
    metrics.append(drawdown_metric)
    
    # Volatility
    volatility = np.std(data_array)
    
    volatility_metric = RiskMetric(
        metric_name="Volatility",
        value=volatility,
        confidence_level=confidence_level,
        methodology="Standard deviation calculation",
        assumptions=["Returns are normally distributed"],
        limitations=["May underestimate risk for non-normal distributions"]
    )
    metrics.append(volatility_metric)
    
    # Skewness
    skewness = float(np.mean(((data_array - np.mean(data_array)) / np.std(data_array)) ** 3))
    
    skewness_metric = RiskMetric(
        metric_name="Skewness",
        value=skewness,
        confidence_level=confidence_level,
        methodology="Third moment calculation",
        assumptions=["Sample skewness represents population skewness"],
        limitations=["Sensitive to outliers"]
    )
    metrics.append(skewness_metric)
    
    # Kurtosis
    kurtosis = float(np.mean(((data_array - np.mean(data_array)) / np.std(data_array)) ** 4) - 3)
    
    kurtosis_metric = RiskMetric(
        metric_name="Kurtosis",
        value=kurtosis,
        confidence_level=confidence_level,
        methodology="Fourth moment calculation (excess kurtosis)",
        assumptions=["Sample kurtosis represents population kurtosis"],
        limitations=["Sensitive to outliers"]
    )
    metrics.append(kurtosis_metric)
    
    return metrics


async def identify_black_swan_scenarios(
    decision_context: str,
    industry: str,
    time_horizon: str
) -> List[ScenarioAnalysis]:
    """
    Identify potential black swan scenarios for risk assessment.
    
    Args:
        decision_context: Description of the decision
        industry: Industry sector
        time_horizon: Time horizon for analysis
    
    Returns:
        List of black swan ScenarioAnalysis objects
    """
    # Common black swan event templates
    black_swan_templates = {
        "pandemic": {
            "description": "Global pandemic disrupting business operations",
            "probability": 0.05,
            "impact_factors": ["supply_chain_disruption", "demand_shock", "workforce_disruption"],
            "assumptions": {
                "revenue_impact": -0.4,
                "cost_increase": 0.2,
                "recovery_time": 18
            }
        },
        "financial_crisis": {
            "description": "Major financial crisis affecting capital markets",
            "probability": 0.1,
            "impact_factors": ["credit_crunch", "market_volatility", "currency_fluctuation"],
            "assumptions": {
                "revenue_impact": -0.3,
                "financing_cost_increase": 0.5,
                "recovery_time": 24
            }
        },
        "cyber_attack": {
            "description": "Major cyber security breach or attack",
            "probability": 0.15,
            "impact_factors": ["data_breach", "system_downtime", "reputation_damage"],
            "assumptions": {
                "revenue_impact": -0.2,
                "recovery_cost": 1000000,
                "recovery_time": 6
            }
        },
        "regulatory_shock": {
            "description": "Sudden major regulatory change",
            "probability": 0.2,
            "impact_factors": ["compliance_costs", "business_model_disruption", "market_access"],
            "assumptions": {
                "compliance_cost_increase": 0.3,
                "revenue_impact": -0.15,
                "adaptation_time": 12
            }
        }
    }
    
    scenarios = []
    
    for event_name, template in black_swan_templates.items():
        # Adjust probability based on industry and time horizon
        adjusted_probability = template["probability"]
        
        # Industry-specific adjustments
        if industry.lower() == "technology" and event_name == "cyber_attack":
            adjusted_probability *= 2
        elif industry.lower() == "healthcare" and event_name == "pandemic":
            adjusted_probability *= 1.5
        elif industry.lower() == "financial" and event_name == "financial_crisis":
            adjusted_probability *= 1.5
        
        # Time horizon adjustments
        if "long" in time_horizon.lower():
            adjusted_probability *= 1.5
        elif "short" in time_horizon.lower():
            adjusted_probability *= 0.5
        
        # Create scenario
        scenario = ScenarioAnalysis(
            scenario_name=f"Black Swan: {event_name.replace('_', ' ').title()}",
            scenario_type=ScenarioType.BLACK_SWAN,
            assumptions=template["assumptions"],
            outcomes={
                "probability": adjusted_probability,
                "severity": 0.8,
                "impact_score": 0.9
            },
            probability=adjusted_probability,
            impact_assessment=template["description"],
            risk_factors=template["impact_factors"],
            mitigation_strategies=[
                "Develop contingency plans",
                "Diversify risk exposure",
                "Build financial reserves",
                "Implement early warning systems",
                "Create crisis management protocols"
            ]
        )
        scenarios.append(scenario)
    
    return scenarios


async def perform_comprehensive_risk_assessment(
    decision_context: str,
    risk_variables: List[RiskVariable],
    objective_function: Callable[[Dict[str, float]], float],
    base_case_inputs: Dict[str, float],
    scenario_definitions: Dict[str, Dict[str, Any]],
    historical_data: Optional[List[float]] = None,
    monte_carlo_iterations: int = 10000
) -> RiskAssessment:
    """
    Perform comprehensive risk assessment combining multiple analysis methods.
    
    Args:
        decision_context: Description of the decision
        risk_variables: List of risk variables
        objective_function: Function to calculate objective value
        base_case_inputs: Base case input values
        scenario_definitions: Scenario definitions
        historical_data: Historical performance data
        monte_carlo_iterations: Number of Monte Carlo iterations
    
    Returns:
        RiskAssessment object
    """
    # Run Monte Carlo simulation
    monte_carlo_result = await run_monte_carlo_simulation(
        risk_variables, objective_function, monte_carlo_iterations
    )
    
    # Perform scenario analysis
    scenario_analyses = await perform_scenario_analysis(
        base_case_inputs, scenario_definitions, 
        lambda x: {"outcome": objective_function(x)}
    )
    
    # Calculate sensitivity analysis
    variable_ranges = {
        var.name: (var.parameters.get('min', base_case_inputs[var.name] * 0.5),
                   var.parameters.get('max', base_case_inputs[var.name] * 1.5))
        for var in risk_variables
        if var.name in base_case_inputs
    }
    
    sensitivity_analysis = await calculate_sensitivity_analysis(
        base_case_inputs, variable_ranges, objective_function
    )
    
    # Calculate risk metrics
    risk_metrics = []
    if historical_data:
        risk_metrics = await calculate_risk_metrics(historical_data)
    
    # Calculate overall risk score
    risk_factors = [
        monte_carlo_result.probability_negative,
        abs(monte_carlo_result.var_95) / abs(monte_carlo_result.mean) if monte_carlo_result.mean != 0 else 0,
        len([s for s in scenario_analyses if s.scenario_type == ScenarioType.WORST_CASE]) / len(scenario_analyses) if scenario_analyses else 0
    ]
    overall_risk_score = min(sum(risk_factors) / len(risk_factors), 1.0)
    
    # Generate recommendations
    recommendations = [
        "Monitor key risk variables closely",
        "Develop contingency plans for worst-case scenarios",
        "Consider risk mitigation strategies",
        "Implement early warning systems",
        "Regular risk assessment updates"
    ]
    
    if monte_carlo_result.probability_negative > 0.2:
        recommendations.append("High probability of negative outcomes - consider risk reduction measures")
    
    if overall_risk_score > 0.7:
        recommendations.append("High overall risk score - recommend conservative approach")
    
    return RiskAssessment(
        assessment_id=f"risk_assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        decision_context=decision_context,
        risk_variables=risk_variables,
        monte_carlo_results=[monte_carlo_result],
        scenario_analyses=scenario_analyses,
        sensitivity_analysis=sensitivity_analysis,
        risk_metrics=risk_metrics,
        overall_risk_score=overall_risk_score,
        confidence_level=0.95,
        recommendations=recommendations
    )