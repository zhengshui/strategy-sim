"""
Unit tests for decision models in StrategySim AI.

Tests validation, serialization, and business logic for decision-related models.
"""

import pytest
from datetime import datetime
from typing import List

from pydantic import ValidationError

from src.models.decision_models import (
    DecisionInput, DecisionType, DecisionUrgency, DecisionOption, DecisionConstraint,
    validate_decision_input, ValidationResult
)


class TestDecisionOption:
    """Test DecisionOption model."""
    
    def test_valid_option_creation(self):
        """Test creating valid decision option."""
        option = DecisionOption(
            name="Test Option",
            description="A test option for validation",
            estimated_cost=50000,
            estimated_timeline="6 months",
            success_probability=0.8
        )
        
        assert option.name == "Test Option"
        assert option.description == "A test option for validation"
        assert option.estimated_cost == 50000
        assert option.estimated_timeline == "6 months"
        assert option.success_probability == 0.8
        assert len(option.option_id) > 0
        assert isinstance(option.created_at, datetime)
    
    def test_empty_name_validation(self):
        """Test validation fails for empty name."""
        with pytest.raises(ValidationError) as exc_info:
            DecisionOption(name="", description="Valid description")
        
        assert "ensure this value has at least 1 characters" in str(exc_info.value)
    
    def test_empty_description_validation(self):
        """Test validation fails for empty description."""
        with pytest.raises(ValidationError) as exc_info:
            DecisionOption(name="Valid Name", description="")
        
        assert "ensure this value has at least 10 characters" in str(exc_info.value)
    
    def test_invalid_success_probability(self):
        """Test validation fails for invalid success probability."""
        with pytest.raises(ValidationError) as exc_info:
            DecisionOption(
                name="Test Option",
                description="Valid description",
                success_probability=1.5
            )
        
        assert "ensure this value is less than or equal to 1" in str(exc_info.value)
    
    def test_negative_cost_validation(self):
        """Test validation fails for negative cost."""
        with pytest.raises(ValidationError) as exc_info:
            DecisionOption(
                name="Test Option",
                description="Valid description",
                estimated_cost=-1000
            )
        
        assert "ensure this value is greater than or equal to 0" in str(exc_info.value)


class TestDecisionConstraint:
    """Test DecisionConstraint model."""
    
    def test_valid_constraint_creation(self):
        """Test creating valid decision constraint."""
        constraint = DecisionConstraint(
            name="Budget Constraint",
            description="Maximum budget limit",
            constraint_type="budget",
            value="1000000",
            priority="high"
        )
        
        assert constraint.name == "Budget Constraint"
        assert constraint.description == "Maximum budget limit"
        assert constraint.constraint_type == "budget"
        assert constraint.value == "1000000"
        assert constraint.priority == "high"
        assert constraint.is_mandatory is True  # Default value
    
    def test_empty_name_validation(self):
        """Test validation fails for empty name."""
        with pytest.raises(ValidationError) as exc_info:
            DecisionConstraint(
                name="",
                description="Valid description",
                constraint_type="budget",
                value="1000000"
            )
        
        assert "ensure this value has at least 1 characters" in str(exc_info.value)
    
    def test_short_description_validation(self):
        """Test validation fails for short description."""
        with pytest.raises(ValidationError) as exc_info:
            DecisionConstraint(
                name="Valid Name",
                description="Short",
                constraint_type="budget",
                value="1000000"
            )
        
        assert "ensure this value has at least 10 characters" in str(exc_info.value)
    
    def test_invalid_priority_validation(self):
        """Test validation fails for invalid priority."""
        with pytest.raises(ValidationError) as exc_info:
            DecisionConstraint(
                name="Valid Name",
                description="Valid description",
                constraint_type="budget",
                value="1000000",
                priority="invalid"
            )
        
        assert "value is not a valid enumeration member" in str(exc_info.value)


class TestDecisionInput:
    """Test DecisionInput model."""
    
    def test_valid_decision_input_creation(self, sample_decision_input):
        """Test creating valid decision input."""
        decision = sample_decision_input
        
        assert decision.title == "Strategic Market Expansion Decision"
        assert decision.decision_type == DecisionType.MARKET_ENTRY
        assert decision.urgency == DecisionUrgency.HIGH
        assert len(decision.options) == 3
        assert len(decision.constraints) == 2
        assert decision.timeline == "12 months"
        assert decision.budget_range == "$5M - $10M"
        assert len(decision.stakeholders) == 3
        assert len(decision.decision_id) > 0
        assert isinstance(decision.created_at, datetime)
    
    def test_empty_title_validation(self):
        """Test validation fails for empty title."""
        with pytest.raises(ValidationError) as exc_info:
            DecisionInput(
                title="",
                description="Valid description",
                decision_type=DecisionType.INVESTMENT,
                urgency=DecisionUrgency.MEDIUM,
                options=[],
                constraints=[]
            )
        
        assert "ensure this value has at least 5 characters" in str(exc_info.value)
    
    def test_short_description_validation(self):
        """Test validation fails for short description."""
        with pytest.raises(ValidationError) as exc_info:
            DecisionInput(
                title="Valid Title",
                description="Short",
                decision_type=DecisionType.INVESTMENT,
                urgency=DecisionUrgency.MEDIUM,
                options=[],
                constraints=[]
            )
        
        assert "ensure this value has at least 20 characters" in str(exc_info.value)
    
    def test_too_many_options_validation(self):
        """Test validation fails for too many options."""
        options = [
            DecisionOption(name=f"Option {i}", description=f"Description {i}")
            for i in range(11)  # More than 10 options
        ]
        
        with pytest.raises(ValidationError) as exc_info:
            DecisionInput(
                title="Valid Title",
                description="Valid description that is long enough",
                decision_type=DecisionType.INVESTMENT,
                urgency=DecisionUrgency.MEDIUM,
                options=options,
                constraints=[]
            )
        
        assert "ensure this value has at most 10 items" in str(exc_info.value)
    
    def test_unique_stakeholders_validation(self):
        """Test validation ensures unique stakeholders."""
        stakeholders = ["CEO", "CFO", "CEO"]  # Duplicate CEO
        
        with pytest.raises(ValidationError) as exc_info:
            DecisionInput(
                title="Valid Title",
                description="Valid description that is long enough",
                decision_type=DecisionType.INVESTMENT,
                urgency=DecisionUrgency.MEDIUM,
                options=[],
                constraints=[],
                stakeholders=stakeholders
            )
        
        assert "Stakeholders must be unique" in str(exc_info.value)
    
    def test_get_option_by_name(self, sample_decision_input):
        """Test getting option by name."""
        decision = sample_decision_input
        
        option = decision.get_option_by_name("Option A")
        assert option is not None
        assert option.name == "Option A"
        
        option = decision.get_option_by_name("Nonexistent")
        assert option is None
    
    def test_get_constraints_by_type(self, sample_decision_input):
        """Test getting constraints by type."""
        decision = sample_decision_input
        
        budget_constraints = decision.get_constraints_by_type("budget")
        assert len(budget_constraints) == 1
        assert budget_constraints[0].name == "Budget"
        
        timeline_constraints = decision.get_constraints_by_type("timeline")
        assert len(timeline_constraints) == 1
        assert timeline_constraints[0].name == "Timeline"
        
        nonexistent_constraints = decision.get_constraints_by_type("nonexistent")
        assert len(nonexistent_constraints) == 0
    
    def test_add_stakeholder(self, sample_decision_input):
        """Test adding stakeholder."""
        decision = sample_decision_input
        initial_count = len(decision.stakeholders)
        
        decision.add_stakeholder("CTO")
        assert len(decision.stakeholders) == initial_count + 1
        assert "CTO" in decision.stakeholders
        
        # Adding duplicate should not increase count
        decision.add_stakeholder("CTO")
        assert len(decision.stakeholders) == initial_count + 1
    
    def test_remove_stakeholder(self, sample_decision_input):
        """Test removing stakeholder."""
        decision = sample_decision_input
        initial_count = len(decision.stakeholders)
        
        decision.remove_stakeholder("CEO")
        assert len(decision.stakeholders) == initial_count - 1
        assert "CEO" not in decision.stakeholders
        
        # Removing non-existent stakeholder should not change count
        decision.remove_stakeholder("NonExistent")
        assert len(decision.stakeholders) == initial_count - 1
    
    def test_is_urgent_property(self, sample_decision_input):
        """Test is_urgent property."""
        decision = sample_decision_input
        assert decision.is_urgent is True  # HIGH urgency
        
        decision.urgency = DecisionUrgency.LOW
        assert decision.is_urgent is False
        
        decision.urgency = DecisionUrgency.CRITICAL
        assert decision.is_urgent is True
    
    def test_estimated_total_cost_property(self, sample_decision_input):
        """Test estimated_total_cost property."""
        decision = sample_decision_input
        
        # Add costs to options
        decision.options[0].estimated_cost = 100000
        decision.options[1].estimated_cost = 200000
        decision.options[2].estimated_cost = 300000
        
        assert decision.estimated_total_cost == 600000
    
    def test_decision_complexity_property(self, sample_decision_input):
        """Test decision_complexity property."""
        decision = sample_decision_input
        
        # Should be "medium" with 3 options and 2 constraints
        assert decision.decision_complexity == "medium"
        
        # Add more options and constraints to make it complex
        for i in range(5):
            decision.options.append(DecisionOption(
                name=f"Extra Option {i}",
                description=f"Extra description {i}"
            ))
            decision.constraints.append(DecisionConstraint(
                name=f"Extra Constraint {i}",
                description=f"Extra constraint description {i}",
                constraint_type="other",
                value=f"value_{i}"
            ))
        
        assert decision.decision_complexity == "complex"


class TestValidateDecisionInput:
    """Test decision input validation function."""
    
    def test_valid_decision_validation(self, sample_decision_input):
        """Test validation passes for valid decision input."""
        result = validate_decision_input(sample_decision_input)
        
        assert result.is_valid is True
        assert len(result.errors) == 0
        assert len(result.warnings) == 0
    
    def test_no_options_validation(self, sample_decision_input):
        """Test validation fails when no options provided."""
        decision = sample_decision_input
        decision.options = []
        
        result = validate_decision_input(decision)
        
        assert result.is_valid is False
        assert len(result.errors) == 1
        assert "At least 2 options are required" in result.errors[0].message
    
    def test_single_option_validation(self, sample_decision_input):
        """Test validation fails with single option."""
        decision = sample_decision_input
        decision.options = [decision.options[0]]
        
        result = validate_decision_input(decision)
        
        assert result.is_valid is False
        assert len(result.errors) == 1
        assert "At least 2 options are required" in result.errors[0].message
    
    def test_duplicate_option_names_validation(self, sample_decision_input):
        """Test validation fails with duplicate option names."""
        decision = sample_decision_input
        decision.options[1].name = decision.options[0].name
        
        result = validate_decision_input(decision)
        
        assert result.is_valid is False
        assert len(result.errors) == 1
        assert "Duplicate option names found" in result.errors[0].message
    
    def test_missing_timeline_warning(self, sample_decision_input):
        """Test warning for missing timeline."""
        decision = sample_decision_input
        decision.timeline = ""
        
        result = validate_decision_input(decision)
        
        assert result.is_valid is True
        assert len(result.warnings) == 1
        assert "Timeline not specified" in result.warnings[0].message
    
    def test_missing_budget_warning(self, sample_decision_input):
        """Test warning for missing budget."""
        decision = sample_decision_input
        decision.budget_range = ""
        
        result = validate_decision_input(decision)
        
        assert result.is_valid is True
        assert len(result.warnings) == 1
        assert "Budget range not specified" in result.warnings[0].message
    
    def test_no_stakeholders_warning(self, sample_decision_input):
        """Test warning for no stakeholders."""
        decision = sample_decision_input
        decision.stakeholders = []
        
        result = validate_decision_input(decision)
        
        assert result.is_valid is True
        assert len(result.warnings) == 1
        assert "No stakeholders specified" in result.warnings[0].message
    
    def test_multiple_validation_errors(self, sample_decision_input):
        """Test multiple validation errors."""
        decision = sample_decision_input
        decision.options = []  # No options
        decision.options.append(DecisionOption(name="Test", description="Test desc"))
        decision.options.append(DecisionOption(name="Test", description="Test desc"))  # Duplicate
        
        result = validate_decision_input(decision)
        
        assert result.is_valid is False
        assert len(result.errors) >= 1
    
    def test_validation_result_properties(self, sample_decision_input):
        """Test ValidationResult properties."""
        decision = sample_decision_input
        decision.timeline = ""  # Create warning
        
        result = validate_decision_input(decision)
        
        # Test summary property
        summary = result.summary
        assert "Valid: True" in summary
        assert "Errors: 0" in summary
        assert "Warnings: 1" in summary
    
    def test_critical_urgency_validation(self, sample_decision_input):
        """Test validation behavior with critical urgency."""
        decision = sample_decision_input
        decision.urgency = DecisionUrgency.CRITICAL
        decision.timeline = ""  # Missing timeline
        
        result = validate_decision_input(decision)
        
        # Should have warning about missing timeline for critical decision
        assert result.is_valid is True
        assert len(result.warnings) >= 1
    
    def test_long_option_names_validation(self, sample_decision_input):
        """Test validation with very long option names."""
        decision = sample_decision_input
        decision.options[0].name = "x" * 101  # Exceeds 100 character limit
        
        result = validate_decision_input(decision)
        
        assert result.is_valid is False
        assert len(result.errors) == 1
        assert "Option name too long" in result.errors[0].message
    
    def test_validation_with_constraints(self, sample_decision_input):
        """Test validation considers constraints."""
        decision = sample_decision_input
        
        # Add conflicting constraints
        decision.constraints.append(DecisionConstraint(
            name="Conflicting Budget",
            description="Budget must be less than $1M",
            constraint_type="budget",
            value="1000000"
        ))
        
        result = validate_decision_input(decision)
        
        # Should still be valid but might have warnings
        assert result.is_valid is True