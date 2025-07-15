"""
Unit tests for report generator utilities in StrategySim AI.

Tests report generation, formatting, and export functionality.
"""

import pytest
import os
import tempfile
from unittest.mock import Mock, patch, mock_open
from typing import Dict, Any

from src.utils.report_generator import (
    ReportGenerator, generate_comprehensive_report, validate_report_quality
)
from src.models.report_models import DecisionReport, ReportStatus


class TestReportGenerator:
    """Test ReportGenerator functionality."""
    
    def test_report_generator_initialization(self):
        """Test report generator initialization."""
        generator = ReportGenerator()
        
        assert generator.template_dir is not None
        assert generator.jinja_env is not None
        assert generator.styles is not None
        assert hasattr(generator, '_format_datetime')
        assert hasattr(generator, '_format_percentage')
        assert hasattr(generator, '_format_currency')
    
    def test_report_generator_with_custom_template_dir(self):
        """Test report generator with custom template directory."""
        custom_dir = "/custom/template/dir"
        
        with patch('os.makedirs') as mock_makedirs:
            generator = ReportGenerator(template_dir=custom_dir)
            
            assert generator.template_dir == custom_dir
            mock_makedirs.assert_called_with(custom_dir, exist_ok=True)
    
    def test_generate_html_report(self, sample_decision_report):
        """Test HTML report generation."""
        generator = ReportGenerator()
        
        with patch.object(generator, '_get_or_create_template') as mock_template:
            mock_template_instance = Mock()
            mock_template_instance.render.return_value = "<html><body>Test Report</body></html>"
            mock_template.return_value = mock_template_instance
            
            html_content = generator.generate_html_report(sample_decision_report)
            
            assert isinstance(html_content, str)
            assert "<html>" in html_content
            assert "Test Report" in html_content
            mock_template.assert_called_once_with("decision_report.html")
    
    def test_generate_html_report_with_visualizations(self, sample_decision_report):
        """Test HTML report generation with visualizations."""
        generator = ReportGenerator()
        
        with patch.object(generator, '_get_or_create_template') as mock_template, \
             patch('src.utils.report_generator.generate_report_visualizations') as mock_viz:
            
            mock_template_instance = Mock()
            mock_template_instance.render.return_value = "<html><body>Test Report with Charts</body></html>"
            mock_template.return_value = mock_template_instance
            
            mock_viz.return_value = {
                "risk_reward_matrix": "data:image/png;base64,test_image_data",
                "consensus_chart": "data:image/png;base64,test_chart_data"
            }
            
            html_content = generator.generate_html_report(
                sample_decision_report,
                include_visualizations=True
            )
            
            assert isinstance(html_content, str)
            assert "Test Report with Charts" in html_content
            mock_viz.assert_called_once_with(sample_decision_report)
    
    def test_generate_html_report_custom_template(self, sample_decision_report):
        """Test HTML report generation with custom template."""
        generator = ReportGenerator()
        
        with patch.object(generator, '_get_or_create_template') as mock_template:
            mock_template_instance = Mock()
            mock_template_instance.render.return_value = "<html><body>Custom Template</body></html>"
            mock_template.return_value = mock_template_instance
            
            html_content = generator.generate_html_report(
                sample_decision_report,
                template_name="custom_template.html"
            )
            
            assert "Custom Template" in html_content
            mock_template.assert_called_once_with("custom_template.html")
    
    def test_generate_pdf_report(self, sample_decision_report, temp_directory):
        """Test PDF report generation."""
        generator = ReportGenerator()
        output_path = os.path.join(temp_directory, "test_report.pdf")
        
        with patch('src.utils.report_generator.SimpleDocTemplate') as mock_doc:
            mock_doc_instance = Mock()
            mock_doc.return_value = mock_doc_instance
            
            result_path = generator.generate_pdf_report(
                sample_decision_report,
                output_path=output_path
            )
            
            assert result_path == output_path
            mock_doc.assert_called_once()
            mock_doc_instance.build.assert_called_once()
    
    def test_generate_pdf_report_with_visualizations(self, sample_decision_report, temp_directory):
        """Test PDF report generation with visualizations."""
        generator = ReportGenerator()
        output_path = os.path.join(temp_directory, "test_report_viz.pdf")
        
        with patch('src.utils.report_generator.SimpleDocTemplate') as mock_doc, \
             patch('src.utils.report_generator.generate_report_visualizations') as mock_viz, \
             patch.object(generator, '_save_base64_image') as mock_save:
            
            mock_doc_instance = Mock()
            mock_doc.return_value = mock_doc_instance
            
            mock_viz.return_value = {
                "risk_reward_matrix": "data:image/png;base64,test_image_data"
            }
            
            mock_save.return_value = "/tmp/test_image.png"
            
            result_path = generator.generate_pdf_report(
                sample_decision_report,
                output_path=output_path,
                include_visualizations=True
            )
            
            assert result_path == output_path
            mock_viz.assert_called_once_with(sample_decision_report)
            mock_save.assert_called_once()
    
    def test_generate_excel_report(self, sample_decision_report, temp_directory):
        """Test Excel report generation."""
        generator = ReportGenerator()
        output_path = os.path.join(temp_directory, "test_report.xlsx")
        
        with patch('src.utils.report_generator.pd.ExcelWriter') as mock_writer:
            mock_writer_instance = Mock()
            mock_writer.return_value.__enter__.return_value = mock_writer_instance
            
            result_path = generator.generate_excel_report(
                sample_decision_report,
                output_path=output_path
            )
            
            assert result_path == output_path
            mock_writer.assert_called_once_with(output_path, engine='openpyxl')
    
    def test_generate_json_report(self, sample_decision_report, temp_directory):
        """Test JSON report generation."""
        generator = ReportGenerator()
        output_path = os.path.join(temp_directory, "test_report.json")
        
        with patch('builtins.open', mock_open()) as mock_file:
            result_path = generator.generate_json_report(
                sample_decision_report,
                output_path=output_path
            )
            
            assert result_path == output_path
            mock_file.assert_called_once_with(output_path, 'w', encoding='utf-8')
    
    def test_generate_json_report_with_raw_data(self, sample_decision_report, temp_directory):
        """Test JSON report generation with raw data."""
        generator = ReportGenerator()
        output_path = os.path.join(temp_directory, "test_report_raw.json")
        
        with patch('builtins.open', mock_open()) as mock_file:
            result_path = generator.generate_json_report(
                sample_decision_report,
                output_path=output_path,
                include_raw_data=True
            )
            
            assert result_path == output_path
            mock_file.assert_called_once_with(output_path, 'w', encoding='utf-8')
    
    def test_generate_text_summary(self, sample_decision_report):
        """Test text summary generation."""
        generator = ReportGenerator()
        
        summary = generator.generate_text_summary(sample_decision_report)
        
        assert isinstance(summary, str)
        assert "DECISION ANALYSIS SUMMARY" in summary
        assert "EXECUTIVE SUMMARY" in summary
        assert "KEY FINDINGS" in summary
        assert "NEXT STEPS" in summary
        assert "REPORT QUALITY METRICS" in summary
        assert sample_decision_report.decision_input.title in summary
    
    def test_create_default_template(self):
        """Test default template creation."""
        generator = ReportGenerator()
        
        with patch('builtins.open', mock_open()) as mock_file:
            template = generator._create_default_template("test_template.html")
            
            assert template is not None
            mock_file.assert_called_once()
    
    def test_generate_report_summary(self, sample_decision_report):
        """Test report summary generation."""
        generator = ReportGenerator()
        
        summary = generator._generate_report_summary(sample_decision_report)
        
        assert isinstance(summary, dict)
        assert "total_options" in summary
        assert "total_risks" in summary
        assert "total_actions" in summary
        assert "critical_actions" in summary
        assert "consensus_level" in summary
        assert "analysis_duration" in summary
        assert "participants_count" in summary
        
        assert summary["total_options"] == len(sample_decision_report.option_evaluations)
        assert summary["total_risks"] == len(sample_decision_report.risk_assessments)
        assert summary["total_actions"] == len(sample_decision_report.action_items)
    
    def test_group_risks_by_category(self, sample_decision_report):
        """Test grouping risks by category."""
        generator = ReportGenerator()
        
        risks_by_category = generator._group_risks_by_category(sample_decision_report)
        
        assert isinstance(risks_by_category, dict)
        assert "market" in risks_by_category
        assert len(risks_by_category["market"]) == 1
    
    def test_calculate_agent_performance(self, sample_decision_report):
        """Test agent performance calculation."""
        generator = ReportGenerator()
        
        performance = generator._calculate_agent_performance(sample_decision_report)
        
        assert isinstance(performance, dict)
        assert "investor" in performance
        
        investor_performance = performance["investor"]
        assert "confidence_level" in investor_performance
        assert "recommendations_count" in investor_performance
        assert "analysis_length" in investor_performance
        assert "participation_score" in investor_performance
    
    def test_save_base64_image(self, temp_directory):
        """Test saving base64 image."""
        generator = ReportGenerator()
        
        # Mock base64 image data
        base64_data = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChAI9jU8lKQAAAABJRU5ErkJggg=="
        
        with patch('tempfile.gettempdir') as mock_temp_dir:
            mock_temp_dir.return_value = temp_directory
            
            with patch('builtins.open', mock_open()) as mock_file:
                result_path = generator._save_base64_image(base64_data, "test_image.png")
                
                expected_path = os.path.join(temp_directory, "test_image.png")
                assert result_path == expected_path
                mock_file.assert_called_once_with(expected_path, 'wb')
    
    def test_jinja_filters(self):
        """Test Jinja2 custom filters."""
        generator = ReportGenerator()
        
        # Test datetime filter
        from datetime import datetime
        test_date = datetime(2023, 1, 1, 12, 0, 0)
        formatted_date = generator._format_datetime(test_date)
        assert formatted_date == "2023-01-01 12:00:00"
        
        # Test percentage filter
        formatted_percentage = generator._format_percentage(0.8)
        assert formatted_percentage == "80.0%"
        
        # Test currency filter
        formatted_currency = generator._format_currency(1234.56)
        assert formatted_currency == "$1,234.56"
    
    def test_error_handling_html_generation(self, sample_decision_report):
        """Test error handling in HTML generation."""
        generator = ReportGenerator()
        
        with patch.object(generator, '_get_or_create_template') as mock_template:
            mock_template.side_effect = Exception("Template error")
            
            with pytest.raises(Exception) as exc_info:
                generator.generate_html_report(sample_decision_report)
            
            assert "Template error" in str(exc_info.value)
    
    def test_error_handling_pdf_generation(self, sample_decision_report):
        """Test error handling in PDF generation."""
        generator = ReportGenerator()
        
        with patch('src.utils.report_generator.SimpleDocTemplate') as mock_doc:
            mock_doc.side_effect = Exception("PDF error")
            
            with pytest.raises(Exception) as exc_info:
                generator.generate_pdf_report(sample_decision_report)
            
            assert "PDF error" in str(exc_info.value)
    
    def test_error_handling_excel_generation(self, sample_decision_report):
        """Test error handling in Excel generation."""
        generator = ReportGenerator()
        
        with patch('src.utils.report_generator.pd.ExcelWriter') as mock_writer:
            mock_writer.side_effect = Exception("Excel error")
            
            with pytest.raises(Exception) as exc_info:
                generator.generate_excel_report(sample_decision_report)
            
            assert "Excel error" in str(exc_info.value)


class TestGenerateComprehensiveReport:
    """Test comprehensive report generation utility."""
    
    def test_generate_comprehensive_report(self, sample_decision_report, temp_directory):
        """Test generating comprehensive report in multiple formats."""
        with patch('src.utils.report_generator.ReportGenerator') as mock_generator_class:
            mock_generator = Mock()
            mock_generator_class.return_value = mock_generator
            
            # Mock report generation methods
            mock_generator.generate_html_report.return_value = "<html>Test</html>"
            mock_generator.generate_pdf_report.return_value = "test_report.pdf"
            mock_generator.generate_json_report.return_value = "test_report.json"
            
            with patch('builtins.open', mock_open()) as mock_file:
                result = generate_comprehensive_report(
                    sample_decision_report,
                    output_dir=temp_directory,
                    formats=["html", "pdf", "json"]
                )
                
                assert isinstance(result, dict)
                assert "html" in result
                assert "pdf" in result
                assert "json" in result
                
                # Check that all generation methods were called
                mock_generator.generate_html_report.assert_called_once()
                mock_generator.generate_pdf_report.assert_called_once()
                mock_generator.generate_json_report.assert_called_once()
    
    def test_generate_comprehensive_report_excel(self, sample_decision_report, temp_directory):
        """Test generating comprehensive report with Excel format."""
        with patch('src.utils.report_generator.ReportGenerator') as mock_generator_class:
            mock_generator = Mock()
            mock_generator_class.return_value = mock_generator
            
            mock_generator.generate_excel_report.return_value = "test_report.xlsx"
            
            result = generate_comprehensive_report(
                sample_decision_report,
                output_dir=temp_directory,
                formats=["excel"]
            )
            
            assert "excel" in result
            mock_generator.generate_excel_report.assert_called_once()
    
    def test_generate_comprehensive_report_error_handling(self, sample_decision_report, temp_directory):
        """Test error handling in comprehensive report generation."""
        with patch('src.utils.report_generator.ReportGenerator') as mock_generator_class:
            mock_generator = Mock()
            mock_generator_class.return_value = mock_generator
            
            mock_generator.generate_html_report.side_effect = Exception("Generation failed")
            
            with pytest.raises(Exception) as exc_info:
                generate_comprehensive_report(
                    sample_decision_report,
                    output_dir=temp_directory,
                    formats=["html"]
                )
            
            assert "Generation failed" in str(exc_info.value)
    
    def test_generate_comprehensive_report_directory_creation(self, sample_decision_report):
        """Test directory creation in comprehensive report generation."""
        output_dir = "/non/existent/directory"
        
        with patch('os.makedirs') as mock_makedirs, \
             patch('src.utils.report_generator.ReportGenerator') as mock_generator_class:
            
            mock_generator = Mock()
            mock_generator_class.return_value = mock_generator
            mock_generator.generate_html_report.return_value = "<html>Test</html>"
            
            with patch('builtins.open', mock_open()):
                generate_comprehensive_report(
                    sample_decision_report,
                    output_dir=output_dir,
                    formats=["html"]
                )
                
                mock_makedirs.assert_called_once_with(output_dir, exist_ok=True)


class TestValidateReportQuality:
    """Test report quality validation."""
    
    def test_validate_report_quality_valid(self, sample_decision_report):
        """Test validating a valid report."""
        result = validate_report_quality(sample_decision_report)
        
        assert isinstance(result, dict)
        assert "is_valid" in result
        assert "issues" in result
        assert "warnings" in result
        assert "quality_score" in result
        
        assert result["is_valid"] is True
        assert len(result["issues"]) == 0
        assert isinstance(result["quality_score"], float)
        assert 0 <= result["quality_score"] <= 1
    
    def test_validate_report_quality_missing_title(self, sample_decision_report):
        """Test validating report with missing title."""
        # Remove title
        sample_decision_report.decision_input.title = ""
        
        result = validate_report_quality(sample_decision_report)
        
        assert result["is_valid"] is False
        assert len(result["issues"]) > 0
        assert any("title" in issue.lower() for issue in result["issues"])
    
    def test_validate_report_quality_no_analyses(self, sample_decision_report):
        """Test validating report with no agent analyses."""
        # Remove agent analyses
        sample_decision_report.agent_analyses = []
        
        result = validate_report_quality(sample_decision_report)
        
        assert result["is_valid"] is False
        assert len(result["issues"]) > 0
        assert any("agent analyses" in issue.lower() for issue in result["issues"])
    
    def test_validate_report_quality_no_key_findings(self, sample_decision_report):
        """Test validating report with no key findings."""
        # Remove key findings
        sample_decision_report.executive_summary.key_findings = []
        
        result = validate_report_quality(sample_decision_report)
        
        assert result["is_valid"] is False
        assert len(result["issues"]) > 0
        assert any("key findings" in issue.lower() for issue in result["issues"])
    
    def test_validate_report_quality_low_confidence(self, sample_decision_report):
        """Test validating report with low confidence."""
        # Set low confidence
        sample_decision_report.executive_summary.confidence_level = 0.2
        
        result = validate_report_quality(sample_decision_report)
        
        assert result["is_valid"] is True  # Still valid but with warnings
        assert len(result["warnings"]) > 0
        assert any("confidence" in warning.lower() for warning in result["warnings"])
    
    def test_validate_report_quality_no_risks(self, sample_decision_report):
        """Test validating report with no risk assessments."""
        # Remove risk assessments
        sample_decision_report.risk_assessments = []
        
        result = validate_report_quality(sample_decision_report)
        
        assert result["is_valid"] is True  # Still valid but with warnings
        assert len(result["warnings"]) > 0
        assert any("risk" in warning.lower() for warning in result["warnings"])
    
    def test_validate_report_quality_no_actions(self, sample_decision_report):
        """Test validating report with no action items."""
        # Remove action items
        sample_decision_report.action_items = []
        
        result = validate_report_quality(sample_decision_report)
        
        assert result["is_valid"] is True  # Still valid but with warnings
        assert len(result["warnings"]) > 0
        assert any("action" in warning.lower() for warning in result["warnings"])
    
    def test_validate_report_quality_score_calculation(self, sample_decision_report):
        """Test quality score calculation."""
        result = validate_report_quality(sample_decision_report)
        
        # With a complete report, quality score should be high
        assert result["quality_score"] > 0.8
        
        # Remove some components and check score decreases
        sample_decision_report.risk_assessments = []
        sample_decision_report.action_items = []
        
        result2 = validate_report_quality(sample_decision_report)
        assert result2["quality_score"] < result["quality_score"]
    
    def test_validate_report_quality_error_handling(self, sample_decision_report):
        """Test error handling in report validation."""
        # Mock to cause an error
        with patch.object(sample_decision_report, 'decision_input', None):
            result = validate_report_quality(sample_decision_report)
            
            assert result["is_valid"] is False
            assert len(result["issues"]) > 0
            assert "Validation error" in result["issues"][0]
            assert result["quality_score"] == 0.0