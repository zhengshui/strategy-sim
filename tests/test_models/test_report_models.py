"""
Unit tests for report models in StrategySim AI.

Tests validation, metrics calculation, and business logic for report-related models.
"""

import pytest
from datetime import datetime
from typing import List, Dict

from pydantic import ValidationError

from src.models.report_models import (
    DecisionReport, ReportStatus, ActionPriority, RecommendationCategory,
    RiskCategory, RiskAssessment, ActionItem, OptionEvaluation,
    ConsensusAnalysis, ExecutiveSummary, ReportMetrics, ReportTemplate
)
from src.models.decision_models import DecisionType
from src.models.agent_models import AgentRole


class TestReportStatus:
    """Test ReportStatus enum."""
    
    def test_all_statuses_defined(self):
        """Test all report statuses are defined."""
        expected_statuses = ["draft", "completed", "reviewed", "approved", "rejected"]
        
        for status in expected_statuses:
            assert hasattr(ReportStatus, status.upper())
    
    def test_status_values(self):
        """Test report status enum values."""
        assert ReportStatus.DRAFT.value == "draft"
        assert ReportStatus.COMPLETED.value == "completed"
        assert ReportStatus.REVIEWED.value == "reviewed"
        assert ReportStatus.APPROVED.value == "approved"
        assert ReportStatus.REJECTED.value == "rejected"


class TestActionPriority:
    """Test ActionPriority enum."""
    
    def test_all_priorities_defined(self):
        """Test all action priorities are defined."""
        expected_priorities = ["critical", "high", "medium", "low", "nice_to_have"]
        
        for priority in expected_priorities:
            assert hasattr(ActionPriority, priority.upper())
    
    def test_priority_values(self):
        """Test action priority enum values."""
        assert ActionPriority.CRITICAL.value == "critical"
        assert ActionPriority.HIGH.value == "high"
        assert ActionPriority.MEDIUM.value == "medium"
        assert ActionPriority.LOW.value == "low"
        assert ActionPriority.NICE_TO_HAVE.value == "nice_to_have"


class TestRecommendationCategory:
    """Test RecommendationCategory enum."""
    
    def test_all_categories_defined(self):
        """Test all recommendation categories are defined."""
        expected_categories = ["proceed", "proceed_with_caution", "modify_approach", 
                             "delay", "reject", "seek_more_info"]
        
        for category in expected_categories:
            assert hasattr(RecommendationCategory, category.upper())
    
    def test_category_values(self):
        """Test recommendation category enum values."""
        assert RecommendationCategory.PROCEED.value == "proceed"
        assert RecommendationCategory.PROCEED_WITH_CAUTION.value == "proceed_with_caution"
        assert RecommendationCategory.MODIFY_APPROACH.value == "modify_approach"
        assert RecommendationCategory.DELAY.value == "delay"
        assert RecommendationCategory.REJECT.value == "reject"
        assert RecommendationCategory.SEEK_MORE_INFO.value == "seek_more_info"


class TestRiskCategory:
    """Test RiskCategory enum."""
    
    def test_all_categories_defined(self):
        """Test all risk categories are defined."""
        expected_categories = ["financial", "operational", "strategic", "legal", 
                             "regulatory", "reputational", "market", "technical"]
        
        for category in expected_categories:
            assert hasattr(RiskCategory, category.upper())
    
    def test_category_values(self):
        """Test risk category enum values."""
        assert RiskCategory.FINANCIAL.value == "financial"
        assert RiskCategory.OPERATIONAL.value == "operational"
        assert RiskCategory.STRATEGIC.value == "strategic"
        assert RiskCategory.LEGAL.value == "legal"
        assert RiskCategory.REGULATORY.value == "regulatory"
        assert RiskCategory.REPUTATIONAL.value == "reputational"
        assert RiskCategory.MARKET.value == "market"
        assert RiskCategory.TECHNICAL.value == "technical"


class TestRiskAssessment:
    """Test RiskAssessment model."""
    
    def test_valid_risk_assessment_creation(self, sample_risk_assessment):
        """Test creating valid risk assessment."""
        risk = sample_risk_assessment
        
        assert risk.category == RiskCategory.MARKET
        assert risk.probability == 0.3
        assert risk.impact == 0.7
        assert risk.risk_score == 0.21
        assert len(risk.mitigation_strategies) == 3
        assert len(risk.contingency_plans) == 3
        assert risk.responsible_party == "Marketing Team"
    
    def test_short_description_validation(self):
        """Test validation fails for short description."""
        with pytest.raises(ValidationError) as exc_info:
            RiskAssessment(
                category=RiskCategory.MARKET,
                description="Short",
                probability=0.5,
                impact=0.5,
                risk_score=0.25
            )
        
        assert "ensure this value has at least 10 characters" in str(exc_info.value)
    
    def test_invalid_probability_validation(self):
        """Test validation fails for invalid probability."""
        with pytest.raises(ValidationError) as exc_info:
            RiskAssessment(
                category=RiskCategory.MARKET,
                description="Valid description for testing",
                probability=1.5,
                impact=0.5,
                risk_score=0.25
            )
        
        assert "ensure this value is less than or equal to 1" in str(exc_info.value)
    
    def test_invalid_impact_validation(self):
        """Test validation fails for invalid impact."""
        with pytest.raises(ValidationError) as exc_info:
            RiskAssessment(
                category=RiskCategory.MARKET,
                description="Valid description for testing",
                probability=0.5,
                impact=-0.1,
                risk_score=0.25
            )
        
        assert "ensure this value is greater than or equal to 0" in str(exc_info.value)
    
    def test_risk_score_validation(self, sample_risk_assessment):
        """Test risk score validation logic."""
        risk = sample_risk_assessment
        
        # Test with calculated score
        risk.probability = 0.4
        risk.impact = 0.6
        risk.risk_score = 0.24  # 0.4 * 0.6 = 0.24
        
        # Should be valid
        assert risk.risk_score == 0.24
    
    def test_invalid_risk_score_validation(self):
        """Test validation fails for invalid risk score."""
        with pytest.raises(ValidationError) as exc_info:
            RiskAssessment(
                category=RiskCategory.MARKET,
                description="Valid description for testing",
                probability=0.5,
                impact=0.5,
                risk_score=1.5  # Invalid score > 1.0
            )
        
        assert "Risk score must be between 0.0 and 1.0" in str(exc_info.value)


class TestActionItem:
    """Test ActionItem model."""
    
    def test_valid_action_item_creation(self, sample_action_item):
        """Test creating valid action item."""
        item = sample_action_item
        
        assert item.title == "Conduct Market Research"
        assert item.priority == ActionPriority.HIGH
        assert item.category == "research"
        assert item.responsible_party == "Marketing Team"
        assert item.estimated_effort == "8 weeks"
        assert len(item.dependencies) == 2
        assert len(item.success_criteria) == 3
    
    def test_short_title_validation(self):
        """Test validation fails for short title."""
        with pytest.raises(ValidationError) as exc_info:
            ActionItem(
                title="Test",
                description="Valid description for testing purposes",
                priority=ActionPriority.HIGH,
                category="test"
            )
        
        assert "Action item title must be at least 5 characters" in str(exc_info.value)
    
    def test_short_description_validation(self):
        """Test validation fails for short description."""
        with pytest.raises(ValidationError) as exc_info:
            ActionItem(
                title="Valid Title",
                description="Short",
                priority=ActionPriority.HIGH,
                category="test"
            )
        
        assert "ensure this value has at least 20 characters" in str(exc_info.value)
    
    def test_title_validation_strips_whitespace(self):
        """Test title validation strips whitespace."""
        item = ActionItem(
            title="  Valid Title  ",
            description="Valid description for testing purposes",
            priority=ActionPriority.HIGH,
            category="test"
        )
        
        assert item.title == "Valid Title"  # Whitespace stripped


class TestOptionEvaluation:
    """Test OptionEvaluation model."""
    
    def test_valid_option_evaluation_creation(self, sample_option_evaluation):
        """Test creating valid option evaluation."""
        option = sample_option_evaluation
        
        assert option.option_name == "Option A"
        assert option.overall_score == 0.85
        assert option.success_probability == 0.7
        assert option.implementation_complexity == "High"
        assert len(option.pros) == 3
        assert len(option.cons) == 3
        assert option.financial_impact["roi"] == 0.25
    
    def test_empty_option_name_validation(self):
        """Test validation fails for empty option name."""
        with pytest.raises(ValidationError) as exc_info:
            OptionEvaluation(
                option_name="",
                overall_score=0.8,
                implementation_complexity="Medium",
                success_probability=0.7
            )
        
        assert "Option name cannot be empty" in str(exc_info.value)
    
    def test_invalid_overall_score_validation(self):
        """Test validation fails for invalid overall score."""
        with pytest.raises(ValidationError) as exc_info:
            OptionEvaluation(
                option_name="Valid Name",
                overall_score=1.5,
                implementation_complexity="Medium",
                success_probability=0.7
            )
        
        assert "ensure this value is less than or equal to 1" in str(exc_info.value)
    
    def test_invalid_success_probability_validation(self):
        """Test validation fails for invalid success probability."""
        with pytest.raises(ValidationError) as exc_info:
            OptionEvaluation(
                option_name="Valid Name",
                overall_score=0.8,
                implementation_complexity="Medium",
                success_probability=-0.1
            )
        
        assert "ensure this value is greater than or equal to 0" in str(exc_info.value)
    
    def test_overall_risk_score_property(self, sample_option_evaluation, sample_risk_assessment):
        """Test overall risk score property calculation."""
        option = sample_option_evaluation
        
        # No risk assessments
        assert option.overall_risk_score == 0.0
        
        # Add risk assessments
        option.risk_assessments = [sample_risk_assessment]
        assert option.overall_risk_score == 0.21  # Same as sample risk score
        
        # Add another risk assessment
        risk2 = RiskAssessment(
            category=RiskCategory.FINANCIAL,
            description="Financial risk description",
            probability=0.4,
            impact=0.8,
            risk_score=0.32
        )
        option.risk_assessments.append(risk2)
        
        expected_avg = (0.21 + 0.32) / 2
        assert option.overall_risk_score == expected_avg
    
    def test_option_name_validation_strips_whitespace(self):
        """Test option name validation strips whitespace."""
        option = OptionEvaluation(
            option_name="  Valid Name  ",
            overall_score=0.8,
            implementation_complexity="Medium",
            success_probability=0.7
        )
        
        assert option.option_name == "Valid Name"  # Whitespace stripped


class TestConsensusAnalysis:
    """Test ConsensusAnalysis model."""
    
    def test_valid_consensus_analysis_creation(self, sample_consensus_analysis):
        """Test creating valid consensus analysis."""
        consensus = sample_consensus_analysis
        
        assert consensus.consensus_level == 0.75
        assert len(consensus.agreement_by_option) == 3
        assert len(consensus.disagreement_areas) == 3
        assert len(consensus.unanimous_points) == 3
        assert "investor" in consensus.agent_alignment
    
    def test_invalid_consensus_level_validation(self):
        """Test validation fails for invalid consensus level."""
        with pytest.raises(ValidationError) as exc_info:
            ConsensusAnalysis(
                consensus_level=1.5,
                agreement_by_option={"Option A": 0.8},
                disagreement_areas=[],
                unanimous_points=[]
            )
        
        assert "Consensus level must be between 0.0 and 1.0" in str(exc_info.value)
    
    def test_negative_consensus_level_validation(self):
        """Test validation fails for negative consensus level."""
        with pytest.raises(ValidationError) as exc_info:
            ConsensusAnalysis(
                consensus_level=-0.1,
                agreement_by_option={"Option A": 0.8},
                disagreement_areas=[],
                unanimous_points=[]
            )
        
        assert "Consensus level must be between 0.0 and 1.0" in str(exc_info.value)
    
    def test_consensus_category_property(self, sample_consensus_analysis):
        """Test consensus category property."""
        consensus = sample_consensus_analysis
        
        # Strong consensus
        consensus.consensus_level = 0.85
        assert consensus.consensus_category == "strong_consensus"
        
        # Moderate consensus
        consensus.consensus_level = 0.65
        assert consensus.consensus_category == "moderate_consensus"
        
        # Weak consensus
        consensus.consensus_level = 0.45
        assert consensus.consensus_category == "weak_consensus"
        
        # No consensus
        consensus.consensus_level = 0.25
        assert consensus.consensus_category == "no_consensus"


class TestExecutiveSummary:
    """Test ExecutiveSummary model."""
    
    def test_valid_executive_summary_creation(self, sample_executive_summary):
        """Test creating valid executive summary."""
        summary = sample_executive_summary
        
        assert summary.decision_title == "Strategic Market Expansion Decision"
        assert summary.recommended_option == "Option A"
        assert summary.recommendation_category == RecommendationCategory.PROCEED_WITH_CAUTION
        assert summary.confidence_level == 0.75
        assert len(summary.key_findings) == 3
        assert len(summary.next_steps) == 4
    
    def test_short_decision_title_validation(self):
        """Test validation fails for short decision title."""
        with pytest.raises(ValidationError) as exc_info:
            ExecutiveSummary(
                decision_title="Test",
                recommended_option="Option A",
                recommendation_category=RecommendationCategory.PROCEED,
                confidence_level=0.8,
                key_findings=["Finding 1"],
                next_steps=["Step 1"],
                decision_urgency="high",
                estimated_impact="High impact"
            )
        
        assert "ensure this value has at least 5 characters" in str(exc_info.value)
    
    def test_empty_recommended_option_validation(self):
        """Test validation fails for empty recommended option."""
        with pytest.raises(ValidationError) as exc_info:
            ExecutiveSummary(
                decision_title="Valid Title",
                recommended_option="",
                recommendation_category=RecommendationCategory.PROCEED,
                confidence_level=0.8,
                key_findings=["Finding 1"],
                next_steps=["Step 1"],
                decision_urgency="high",
                estimated_impact="High impact"
            )
        
        assert "ensure this value has at least 1 characters" in str(exc_info.value)
    
    def test_invalid_confidence_level_validation(self):
        """Test validation fails for invalid confidence level."""
        with pytest.raises(ValidationError) as exc_info:
            ExecutiveSummary(
                decision_title="Valid Title",
                recommended_option="Option A",
                recommendation_category=RecommendationCategory.PROCEED,
                confidence_level=1.5,
                key_findings=["Finding 1"],
                next_steps=["Step 1"],
                decision_urgency="high",
                estimated_impact="High impact"
            )
        
        assert "ensure this value is less than or equal to 1" in str(exc_info.value)
    
    def test_empty_key_findings_validation(self):
        """Test validation fails for empty key findings."""
        with pytest.raises(ValidationError) as exc_info:
            ExecutiveSummary(
                decision_title="Valid Title",
                recommended_option="Option A",
                recommendation_category=RecommendationCategory.PROCEED,
                confidence_level=0.8,
                key_findings=[],
                next_steps=["Step 1"],
                decision_urgency="high",
                estimated_impact="High impact"
            )
        
        assert "At least one key finding is required" in str(exc_info.value)
    
    def test_short_key_findings_validation(self):
        """Test validation fails for short key findings."""
        with pytest.raises(ValidationError) as exc_info:
            ExecutiveSummary(
                decision_title="Valid Title",
                recommended_option="Option A",
                recommendation_category=RecommendationCategory.PROCEED,
                confidence_level=0.8,
                key_findings=["Short"],
                next_steps=["Step 1"],
                decision_urgency="high",
                estimated_impact="High impact"
            )
        
        assert "Each key finding must be at least 10 characters" in str(exc_info.value)
    
    def test_empty_next_steps_validation(self):
        """Test validation fails for empty next steps."""
        with pytest.raises(ValidationError) as exc_info:
            ExecutiveSummary(
                decision_title="Valid Title",
                recommended_option="Option A",
                recommendation_category=RecommendationCategory.PROCEED,
                confidence_level=0.8,
                key_findings=["Valid finding"],
                next_steps=[],
                decision_urgency="high",
                estimated_impact="High impact"
            )
        
        assert "ensure this value has at least 1 items" in str(exc_info.value)


class TestReportMetrics:
    """Test ReportMetrics model."""
    
    def test_valid_report_metrics_creation(self, sample_report_metrics):
        """Test creating valid report metrics."""
        metrics = sample_report_metrics
        
        assert metrics.completeness_score == 0.9
        assert metrics.consistency_score == 0.8
        assert metrics.analysis_depth == 0.85
        assert metrics.risk_coverage == 0.9
        assert metrics.recommendation_quality == 0.8
        assert metrics.evidence_support == 0.75
        assert len(metrics.agent_participation) == 5
    
    def test_invalid_completeness_score_validation(self):
        """Test validation fails for invalid completeness score."""
        with pytest.raises(ValidationError) as exc_info:
            ReportMetrics(
                completeness_score=1.5,
                consistency_score=0.8,
                analysis_depth=0.85,
                risk_coverage=0.9,
                recommendation_quality=0.8,
                evidence_support=0.75
            )
        
        assert "ensure this value is less than or equal to 1" in str(exc_info.value)
    
    def test_negative_score_validation(self):
        """Test validation fails for negative scores."""
        with pytest.raises(ValidationError) as exc_info:
            ReportMetrics(
                completeness_score=0.9,
                consistency_score=-0.1,
                analysis_depth=0.85,
                risk_coverage=0.9,
                recommendation_quality=0.8,
                evidence_support=0.75
            )
        
        assert "ensure this value is greater than or equal to 0" in str(exc_info.value)
    
    def test_overall_quality_score_property(self, sample_report_metrics):
        """Test overall quality score property calculation."""
        metrics = sample_report_metrics
        
        expected_score = (0.9 + 0.8 + 0.85 + 0.9 + 0.8 + 0.75) / 6
        assert abs(metrics.overall_quality_score - expected_score) < 0.001


class TestDecisionReport:
    """Test DecisionReport model."""
    
    def test_valid_decision_report_creation(self, sample_decision_report):
        """Test creating valid decision report."""
        report = sample_decision_report
        
        assert report.report_id == "test_report_001"
        assert report.status == ReportStatus.COMPLETED
        assert len(report.agent_analyses) == 1
        assert len(report.option_evaluations) == 1
        assert len(report.risk_assessments) == 1
        assert len(report.action_items) == 1
        assert len(report.participants) == 5
        assert report.analysis_duration == 45.5
        assert report.completed_at is not None
    
    def test_empty_report_id_validation(self, sample_decision_input):
        """Test validation fails for empty report ID."""
        with pytest.raises(ValidationError) as exc_info:
            DecisionReport(
                report_id="",
                decision_input=sample_decision_input,
                consensus_analysis=ConsensusAnalysis(
                    consensus_level=0.8,
                    agreement_by_option={},
                    disagreement_areas=[],
                    unanimous_points=[]
                ),
                executive_summary=ExecutiveSummary(
                    decision_title="Test",
                    recommended_option="Option A",
                    recommendation_category=RecommendationCategory.PROCEED,
                    confidence_level=0.8,
                    key_findings=["Finding 1"],
                    next_steps=["Step 1"],
                    decision_urgency="high",
                    estimated_impact="High impact"
                ),
                final_recommendation="Test recommendation",
                report_metrics=ReportMetrics(
                    completeness_score=0.9,
                    consistency_score=0.8,
                    analysis_depth=0.85,
                    risk_coverage=0.9,
                    recommendation_quality=0.8,
                    evidence_support=0.75
                ),
                participants=["investor"],
                analysis_duration=10.0
            )
        
        assert "Report ID cannot be empty" in str(exc_info.value)
    
    def test_short_final_recommendation_validation(self, sample_decision_input):
        """Test validation fails for short final recommendation."""
        with pytest.raises(ValidationError) as exc_info:
            DecisionReport(
                report_id="test_report",
                decision_input=sample_decision_input,
                consensus_analysis=ConsensusAnalysis(
                    consensus_level=0.8,
                    agreement_by_option={},
                    disagreement_areas=[],
                    unanimous_points=[]
                ),
                executive_summary=ExecutiveSummary(
                    decision_title="Test Title",
                    recommended_option="Option A",
                    recommendation_category=RecommendationCategory.PROCEED,
                    confidence_level=0.8,
                    key_findings=["Valid finding"],
                    next_steps=["Step 1"],
                    decision_urgency="high",
                    estimated_impact="High impact"
                ),
                final_recommendation="Short",
                report_metrics=ReportMetrics(
                    completeness_score=0.9,
                    consistency_score=0.8,
                    analysis_depth=0.85,
                    risk_coverage=0.9,
                    recommendation_quality=0.8,
                    evidence_support=0.75
                ),
                participants=["investor"],
                analysis_duration=10.0
            )
        
        assert "ensure this value has at least 50 characters" in str(exc_info.value)
    
    def test_empty_participants_validation(self, sample_decision_input):
        """Test validation fails for empty participants."""
        with pytest.raises(ValidationError) as exc_info:
            DecisionReport(
                report_id="test_report",
                decision_input=sample_decision_input,
                consensus_analysis=ConsensusAnalysis(
                    consensus_level=0.8,
                    agreement_by_option={},
                    disagreement_areas=[],
                    unanimous_points=[]
                ),
                executive_summary=ExecutiveSummary(
                    decision_title="Test Title",
                    recommended_option="Option A",
                    recommendation_category=RecommendationCategory.PROCEED,
                    confidence_level=0.8,
                    key_findings=["Valid finding"],
                    next_steps=["Step 1"],
                    decision_urgency="high",
                    estimated_impact="High impact"
                ),
                final_recommendation="This is a valid final recommendation that is long enough",
                report_metrics=ReportMetrics(
                    completeness_score=0.9,
                    consistency_score=0.8,
                    analysis_depth=0.85,
                    risk_coverage=0.9,
                    recommendation_quality=0.8,
                    evidence_support=0.75
                ),
                participants=[],
                analysis_duration=10.0
            )
        
        assert "ensure this value has at least 1 items" in str(exc_info.value)
    
    def test_duplicate_participants_validation(self, sample_decision_input):
        """Test validation fails for duplicate participants."""
        with pytest.raises(ValidationError) as exc_info:
            DecisionReport(
                report_id="test_report",
                decision_input=sample_decision_input,
                consensus_analysis=ConsensusAnalysis(
                    consensus_level=0.8,
                    agreement_by_option={},
                    disagreement_areas=[],
                    unanimous_points=[]
                ),
                executive_summary=ExecutiveSummary(
                    decision_title="Test Title",
                    recommended_option="Option A",
                    recommendation_category=RecommendationCategory.PROCEED,
                    confidence_level=0.8,
                    key_findings=["Valid finding"],
                    next_steps=["Step 1"],
                    decision_urgency="high",
                    estimated_impact="High impact"
                ),
                final_recommendation="This is a valid final recommendation that is long enough",
                report_metrics=ReportMetrics(
                    completeness_score=0.9,
                    consistency_score=0.8,
                    analysis_depth=0.85,
                    risk_coverage=0.9,
                    recommendation_quality=0.8,
                    evidence_support=0.75
                ),
                participants=["investor", "legal", "investor"],  # Duplicate
                analysis_duration=10.0
            )
        
        assert "Participants must be unique" in str(exc_info.value)
    
    def test_invalid_confidence_interval_validation(self, sample_decision_input):
        """Test validation fails for invalid confidence interval."""
        with pytest.raises(ValidationError) as exc_info:
            DecisionReport(
                report_id="test_report",
                decision_input=sample_decision_input,
                consensus_analysis=ConsensusAnalysis(
                    consensus_level=0.8,
                    agreement_by_option={},
                    disagreement_areas=[],
                    unanimous_points=[]
                ),
                executive_summary=ExecutiveSummary(
                    decision_title="Test Title",
                    recommended_option="Option A",
                    recommendation_category=RecommendationCategory.PROCEED,
                    confidence_level=0.8,
                    key_findings=["Valid finding"],
                    next_steps=["Step 1"],
                    decision_urgency="high",
                    estimated_impact="High impact"
                ),
                final_recommendation="This is a valid final recommendation that is long enough",
                report_metrics=ReportMetrics(
                    completeness_score=0.9,
                    consistency_score=0.8,
                    analysis_depth=0.85,
                    risk_coverage=0.9,
                    recommendation_quality=0.8,
                    evidence_support=0.75
                ),
                participants=["investor"],
                analysis_duration=10.0,
                confidence_interval=(0.8, 0.6)  # Invalid: lower > upper
            )
        
        assert "Confidence interval must be between 0.0 and 1.0 with lower <= upper" in str(exc_info.value)
    
    def test_get_recommended_option(self, sample_decision_report):
        """Test getting recommended option."""
        report = sample_decision_report
        
        recommended = report.get_recommended_option()
        assert recommended is not None
        assert recommended.option_name == "Option A"
        assert recommended.overall_score == 0.85
    
    def test_get_recommended_option_empty(self, sample_decision_report):
        """Test getting recommended option when no options exist."""
        report = sample_decision_report
        report.option_evaluations = []
        
        recommended = report.get_recommended_option()
        assert recommended is None
    
    def test_get_highest_risk_option(self, sample_decision_report):
        """Test getting highest risk option."""
        report = sample_decision_report
        
        highest_risk = report.get_highest_risk_option()
        assert highest_risk is not None
        assert highest_risk.option_name == "Option A"
    
    def test_get_risks_by_category(self, sample_decision_report):
        """Test getting risks by category."""
        report = sample_decision_report
        
        market_risks = report.get_risks_by_category(RiskCategory.MARKET)
        assert len(market_risks) == 1
        assert market_risks[0].category == RiskCategory.MARKET
        
        financial_risks = report.get_risks_by_category(RiskCategory.FINANCIAL)
        assert len(financial_risks) == 0
    
    def test_get_critical_action_items(self, sample_decision_report):
        """Test getting critical action items."""
        report = sample_decision_report
        
        # Add a critical action item
        critical_item = ActionItem(
            title="Critical Action",
            description="This is a critical action item that needs immediate attention",
            priority=ActionPriority.CRITICAL,
            category="urgent"
        )
        report.action_items.append(critical_item)
        
        critical_items = report.get_critical_action_items()
        assert len(critical_items) == 1
        assert critical_items[0].priority == ActionPriority.CRITICAL
    
    def test_mark_completed(self, sample_decision_report):
        """Test marking report as completed."""
        report = sample_decision_report
        report.status = ReportStatus.DRAFT
        report.completed_at = None
        
        report.mark_completed()
        assert report.status == ReportStatus.COMPLETED
        assert report.completed_at is not None
    
    def test_mark_reviewed(self, sample_decision_report):
        """Test marking report as reviewed."""
        report = sample_decision_report
        report.status = ReportStatus.COMPLETED
        report.reviewed_at = None
        
        report.mark_reviewed()
        assert report.status == ReportStatus.REVIEWED
        assert report.reviewed_at is not None
    
    def test_mark_approved(self, sample_decision_report):
        """Test marking report as approved."""
        report = sample_decision_report
        report.status = ReportStatus.REVIEWED
        report.approved_at = None
        
        report.mark_approved()
        assert report.status == ReportStatus.APPROVED
        assert report.approved_at is not None


class TestReportTemplate:
    """Test ReportTemplate model."""
    
    def test_valid_report_template_creation(self):
        """Test creating valid report template."""
        template = ReportTemplate(
            template_name="Standard Analysis Template",
            decision_types=[DecisionType.INVESTMENT, DecisionType.MARKET_ENTRY],
            sections=["Executive Summary", "Analysis", "Recommendations"],
            required_agents=[AgentRole.INVESTOR, AgentRole.ANALYST],
            format_options=["PDF", "HTML"],
            custom_fields={"priority": "high", "department": "strategy"}
        )
        
        assert template.template_name == "Standard Analysis Template"
        assert len(template.decision_types) == 2
        assert len(template.sections) == 3
        assert len(template.required_agents) == 2
        assert len(template.format_options) == 2
        assert template.custom_fields["priority"] == "high"
    
    def test_empty_template_name_validation(self):
        """Test validation fails for empty template name."""
        with pytest.raises(ValidationError) as exc_info:
            ReportTemplate(
                template_name="",
                decision_types=[DecisionType.INVESTMENT],
                sections=["Executive Summary"],
                required_agents=[AgentRole.INVESTOR]
            )
        
        assert "Template name cannot be empty" in str(exc_info.value)
    
    def test_empty_decision_types_validation(self):
        """Test validation fails for empty decision types."""
        with pytest.raises(ValidationError) as exc_info:
            ReportTemplate(
                template_name="Test Template",
                decision_types=[],
                sections=["Executive Summary"],
                required_agents=[AgentRole.INVESTOR]
            )
        
        assert "ensure this value has at least 1 items" in str(exc_info.value)
    
    def test_empty_sections_validation(self):
        """Test validation fails for empty sections."""
        with pytest.raises(ValidationError) as exc_info:
            ReportTemplate(
                template_name="Test Template",
                decision_types=[DecisionType.INVESTMENT],
                sections=[],
                required_agents=[AgentRole.INVESTOR]
            )
        
        assert "ensure this value has at least 1 items" in str(exc_info.value)
    
    def test_empty_required_agents_validation(self):
        """Test validation fails for empty required agents."""
        with pytest.raises(ValidationError) as exc_info:
            ReportTemplate(
                template_name="Test Template",
                decision_types=[DecisionType.INVESTMENT],
                sections=["Executive Summary"],
                required_agents=[]
            )
        
        assert "ensure this value has at least 1 items" in str(exc_info.value)
    
    def test_template_name_validation_strips_whitespace(self):
        """Test template name validation strips whitespace."""
        template = ReportTemplate(
            template_name="  Test Template  ",
            decision_types=[DecisionType.INVESTMENT],
            sections=["Executive Summary"],
            required_agents=[AgentRole.INVESTOR]
        )
        
        assert template.template_name == "Test Template"  # Whitespace stripped