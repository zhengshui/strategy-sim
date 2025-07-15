"""
Report generation utilities for StrategySim AI.

Contains tools for generating comprehensive decision reports in various formats,
managing report templates, and exporting analysis results.
"""

import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
import tempfile

from jinja2 import Environment, FileSystemLoader, Template
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import pandas as pd

from ..models.report_models import (
    DecisionReport, ReportTemplate, ReportStatus, 
    ActionPriority, RecommendationCategory, RiskCategory
)
from ..models.decision_models import DecisionType
from .visualization import generate_report_visualizations

logger = logging.getLogger(__name__)


class ReportGenerator:
    """
    Comprehensive report generator for StrategySim AI decision analysis.
    
    Supports multiple output formats and customizable templates.
    """
    
    def __init__(self, template_dir: Optional[str] = None):
        """
        Initialize the report generator.
        
        Args:
            template_dir: Directory containing Jinja2 templates
        """
        self.template_dir = template_dir or self._get_default_template_dir()
        self.jinja_env = self._setup_jinja_environment()
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
        logger.info(f"ReportGenerator initialized with template_dir: {self.template_dir}")
    
    def _get_default_template_dir(self) -> str:
        """Get default template directory."""
        return os.path.join(os.path.dirname(__file__), "templates")
    
    def _setup_jinja_environment(self) -> Environment:
        """Setup Jinja2 environment with custom filters."""
        try:
            # Ensure template directory exists
            os.makedirs(self.template_dir, exist_ok=True)
            
            env = Environment(
                loader=FileSystemLoader(self.template_dir),
                autoescape=True
            )
            
            # Add custom filters
            env.filters['datetime'] = self._format_datetime
            env.filters['percentage'] = self._format_percentage
            env.filters['currency'] = self._format_currency
            env.filters['priority_badge'] = self._format_priority_badge
            env.filters['risk_level'] = self._format_risk_level
            
            return env
            
        except Exception as e:
            logger.error(f"Failed to setup Jinja2 environment: {e}")
            raise
    
    def _setup_custom_styles(self) -> None:
        """Setup custom styles for PDF generation."""
        try:
            # Executive Summary style
            self.styles.add(ParagraphStyle(
                name='ExecutiveSummary',
                parent=self.styles['Normal'],
                fontSize=12,
                spaceAfter=12,
                leftIndent=20,
                rightIndent=20,
                backColor=colors.lightgrey
            ))
            
            # Risk indicator styles
            self.styles.add(ParagraphStyle(
                name='HighRisk',
                parent=self.styles['Normal'],
                fontSize=10,
                textColor=colors.red,
                fontName='Helvetica-Bold'
            ))
            
            self.styles.add(ParagraphStyle(
                name='MediumRisk',
                parent=self.styles['Normal'],
                fontSize=10,
                textColor=colors.orange,
                fontName='Helvetica-Bold'
            ))
            
            self.styles.add(ParagraphStyle(
                name='LowRisk',
                parent=self.styles['Normal'],
                fontSize=10,
                textColor=colors.green,
                fontName='Helvetica-Bold'
            ))
            
        except Exception as e:
            logger.error(f"Failed to setup custom styles: {e}")
    
    def generate_html_report(
        self, 
        report: DecisionReport, 
        template_name: str = "decision_report.html",
        include_visualizations: bool = True
    ) -> str:
        """
        Generate HTML report from decision analysis.
        
        Args:
            report: Decision report to generate
            template_name: Jinja2 template name
            include_visualizations: Whether to include charts and graphs
        
        Returns:
            HTML string
        """
        try:
            # Generate visualizations if requested
            visualizations = {}
            if include_visualizations:
                visualizations = generate_report_visualizations(report)
            
            # Prepare template context
            context = {
                'report': report,
                'visualizations': visualizations,
                'generated_at': datetime.now(),
                'report_summary': self._generate_report_summary(report),
                'critical_actions': report.get_critical_action_items(),
                'recommended_option': report.get_recommended_option(),
                'highest_risk_option': report.get_highest_risk_option(),
                'risks_by_category': self._group_risks_by_category(report),
                'agent_performance': self._calculate_agent_performance(report)
            }
            
            # Get template
            template = self._get_or_create_template(template_name)
            
            # Render HTML
            html_content = template.render(**context)
            
            logger.info(f"HTML report generated successfully for {report.report_id}")
            return html_content
            
        except Exception as e:
            logger.error(f"Failed to generate HTML report: {e}")
            raise
    
    def generate_pdf_report(
        self, 
        report: DecisionReport, 
        output_path: Optional[str] = None,
        include_visualizations: bool = True
    ) -> str:
        """
        Generate PDF report from decision analysis.
        
        Args:
            report: Decision report to generate
            output_path: Path to save PDF file
            include_visualizations: Whether to include charts and graphs
        
        Returns:
            Path to generated PDF file
        """
        try:
            # Generate output path if not provided
            if not output_path:
                output_path = f"decision_report_{report.report_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
            # Create PDF document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Build PDF content
            story = []
            
            # Title
            story.append(Paragraph(f"Decision Analysis Report: {report.decision_input.title}", 
                                 self.styles['Title']))
            story.append(Spacer(1, 12))
            
            # Executive Summary
            story.append(Paragraph("Executive Summary", self.styles['Heading1']))
            story.append(Paragraph(f"Recommendation: {report.executive_summary.recommendation_category.value.replace('_', ' ').title()}", 
                                 self.styles['ExecutiveSummary']))
            story.append(Paragraph(f"Recommended Option: {report.executive_summary.recommended_option}", 
                                 self.styles['ExecutiveSummary']))
            story.append(Paragraph(f"Confidence Level: {report.executive_summary.confidence_level:.1%}", 
                                 self.styles['ExecutiveSummary']))
            story.append(Spacer(1, 12))
            
            # Key Findings
            story.append(Paragraph("Key Findings", self.styles['Heading2']))
            for finding in report.executive_summary.key_findings:
                story.append(Paragraph(f"• {finding}", self.styles['Normal']))
            story.append(Spacer(1, 12))
            
            # Risk Analysis
            story.append(Paragraph("Risk Analysis", self.styles['Heading2']))
            if report.risk_assessments:
                risk_data = [["Risk Category", "Description", "Probability", "Impact", "Score"]]
                for risk in report.risk_assessments:
                    risk_data.append([
                        risk.category.value.title(),
                        risk.description[:50] + "..." if len(risk.description) > 50 else risk.description,
                        f"{risk.probability:.1%}",
                        f"{risk.impact:.1%}",
                        f"{risk.risk_score:.2f}"
                    ])
                
                risk_table = Table(risk_data)
                risk_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(risk_table)
                story.append(Spacer(1, 12))
            
            # Action Items
            story.append(Paragraph("Action Items", self.styles['Heading2']))
            if report.action_items:
                for item in report.action_items:
                    priority_style = self._get_priority_style(item.priority)
                    story.append(Paragraph(f"[{item.priority.value.upper()}] {item.title}", priority_style))
                    story.append(Paragraph(item.description, self.styles['Normal']))
                    story.append(Spacer(1, 6))
            
            # Visualizations
            if include_visualizations:
                story.append(Paragraph("Analysis Visualizations", self.styles['Heading2']))
                visualizations = generate_report_visualizations(report)
                
                for viz_name, viz_data in visualizations.items():
                    if viz_data:
                        # Save visualization as temporary image
                        temp_path = self._save_base64_image(viz_data, f"{viz_name}.png")
                        if temp_path:
                            story.append(Image(temp_path, width=6*inch, height=4*inch))
                            story.append(Spacer(1, 12))
            
            # Build PDF
            doc.build(story)
            
            logger.info(f"PDF report generated successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Failed to generate PDF report: {e}")
            raise
    
    def generate_excel_report(
        self, 
        report: DecisionReport, 
        output_path: Optional[str] = None
    ) -> str:
        """
        Generate Excel report from decision analysis.
        
        Args:
            report: Decision report to generate
            output_path: Path to save Excel file
        
        Returns:
            Path to generated Excel file
        """
        try:
            # Generate output path if not provided
            if not output_path:
                output_path = f"decision_report_{report.report_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            # Create Excel writer
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                
                # Summary sheet
                summary_data = {
                    'Metric': [
                        'Decision Title',
                        'Recommendation',
                        'Confidence Level',
                        'Analysis Duration',
                        'Participants',
                        'Status'
                    ],
                    'Value': [
                        report.decision_input.title,
                        report.executive_summary.recommendation_category.value.replace('_', ' ').title(),
                        f"{report.executive_summary.confidence_level:.1%}",
                        f"{report.analysis_duration:.1f} seconds",
                        ', '.join(report.participants),
                        report.status.value.title()
                    ]
                }
                pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)
                
                # Options evaluation sheet
                if report.option_evaluations:
                    options_data = []
                    for option in report.option_evaluations:
                        options_data.append({
                            'Option': option.option_name,
                            'Overall Score': option.overall_score,
                            'Risk Score': option.overall_risk_score,
                            'Success Probability': option.success_probability,
                            'Implementation Complexity': option.implementation_complexity,
                            'Pros': '; '.join(option.pros),
                            'Cons': '; '.join(option.cons)
                        })
                    pd.DataFrame(options_data).to_excel(writer, sheet_name='Options', index=False)
                
                # Risk analysis sheet
                if report.risk_assessments:
                    risk_data = []
                    for risk in report.risk_assessments:
                        risk_data.append({
                            'Category': risk.category.value.title(),
                            'Description': risk.description,
                            'Probability': risk.probability,
                            'Impact': risk.impact,
                            'Risk Score': risk.risk_score,
                            'Mitigation Strategies': '; '.join(risk.mitigation_strategies)
                        })
                    pd.DataFrame(risk_data).to_excel(writer, sheet_name='Risks', index=False)
                
                # Action items sheet
                if report.action_items:
                    action_data = []
                    for item in report.action_items:
                        action_data.append({
                            'Title': item.title,
                            'Priority': item.priority.value.title(),
                            'Category': item.category,
                            'Description': item.description,
                            'Responsible Party': item.responsible_party or 'Not assigned',
                            'Timeline': item.timeline or 'Not specified',
                            'Resources Required': '; '.join(item.resources_required)
                        })
                    pd.DataFrame(action_data).to_excel(writer, sheet_name='Actions', index=False)
                
                # Agent analyses sheet
                if report.agent_analyses:
                    agent_data = []
                    for analysis in report.agent_analyses:
                        agent_data.append({
                            'Agent': analysis.agent_role.value.title(),
                            'Analysis': analysis.analysis,
                            'Confidence': analysis.confidence_level,
                            'Recommendations': '; '.join(analysis.recommendations)
                        })
                    pd.DataFrame(agent_data).to_excel(writer, sheet_name='Agent Analyses', index=False)
            
            logger.info(f"Excel report generated successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Failed to generate Excel report: {e}")
            raise
    
    def generate_json_report(
        self, 
        report: DecisionReport, 
        output_path: Optional[str] = None,
        include_raw_data: bool = False
    ) -> str:
        """
        Generate JSON report from decision analysis.
        
        Args:
            report: Decision report to generate
            output_path: Path to save JSON file
            include_raw_data: Whether to include raw analysis data
        
        Returns:
            Path to generated JSON file
        """
        try:
            # Generate output path if not provided
            if not output_path:
                output_path = f"decision_report_{report.report_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            # Prepare report data
            report_data = report.dict()
            
            # Add computed fields
            report_data['computed_metrics'] = {
                'recommended_option': report.get_recommended_option().dict() if report.get_recommended_option() else None,
                'highest_risk_option': report.get_highest_risk_option().dict() if report.get_highest_risk_option() else None,
                'critical_actions': [item.dict() for item in report.get_critical_action_items()],
                'risks_by_category': self._group_risks_by_category(report),
                'agent_performance': self._calculate_agent_performance(report)
            }
            
            # Remove raw data if not requested
            if not include_raw_data:
                report_data.pop('probability_matrix', None)
                report_data.pop('sensitivity_analysis', None)
                report_data.pop('scenario_outcomes', None)
            
            # Write JSON file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False, default=str)
            
            logger.info(f"JSON report generated successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Failed to generate JSON report: {e}")
            raise
    
    def generate_text_summary(self, report: DecisionReport) -> str:
        """
        Generate concise text summary of decision analysis.
        
        Args:
            report: Decision report to summarize
        
        Returns:
            Text summary string
        """
        try:
            summary_parts = []
            
            # Header
            summary_parts.append(f"DECISION ANALYSIS SUMMARY")
            summary_parts.append(f"=" * 50)
            summary_parts.append(f"Title: {report.decision_input.title}")
            summary_parts.append(f"Type: {report.decision_input.decision_type.value.replace('_', ' ').title()}")
            summary_parts.append(f"Status: {report.status.value.title()}")
            summary_parts.append(f"Generated: {report.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            summary_parts.append("")
            
            # Executive Summary
            summary_parts.append("EXECUTIVE SUMMARY")
            summary_parts.append("-" * 20)
            summary_parts.append(f"Recommendation: {report.executive_summary.recommendation_category.value.replace('_', ' ').title()}")
            summary_parts.append(f"Recommended Option: {report.executive_summary.recommended_option}")
            summary_parts.append(f"Confidence Level: {report.executive_summary.confidence_level:.1%}")
            summary_parts.append("")
            
            # Key Findings
            summary_parts.append("KEY FINDINGS")
            summary_parts.append("-" * 15)
            for finding in report.executive_summary.key_findings:
                summary_parts.append(f"• {finding}")
            summary_parts.append("")
            
            # Critical Risks
            if report.executive_summary.critical_risks:
                summary_parts.append("CRITICAL RISKS")
                summary_parts.append("-" * 15)
                for risk in report.executive_summary.critical_risks:
                    summary_parts.append(f"• {risk}")
                summary_parts.append("")
            
            # Next Steps
            summary_parts.append("NEXT STEPS")
            summary_parts.append("-" * 12)
            for i, step in enumerate(report.executive_summary.next_steps, 1):
                summary_parts.append(f"{i}. {step}")
            summary_parts.append("")
            
            # Report Quality
            summary_parts.append("REPORT QUALITY METRICS")
            summary_parts.append("-" * 25)
            summary_parts.append(f"Overall Quality: {report.report_metrics.overall_quality_score:.1%}")
            summary_parts.append(f"Completeness: {report.report_metrics.completeness_score:.1%}")
            summary_parts.append(f"Analysis Depth: {report.report_metrics.analysis_depth:.1%}")
            summary_parts.append(f"Risk Coverage: {report.report_metrics.risk_coverage:.1%}")
            
            return "\n".join(summary_parts)
            
        except Exception as e:
            logger.error(f"Failed to generate text summary: {e}")
            raise
    
    def _get_or_create_template(self, template_name: str) -> Template:
        """Get existing template or create default one."""
        try:
            return self.jinja_env.get_template(template_name)
        except Exception:
            # Create default template
            return self._create_default_template(template_name)
    
    def _create_default_template(self, template_name: str) -> Template:
        """Create default HTML template."""
        default_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Decision Analysis Report: {{ report.decision_input.title }}</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .header { background-color: #f8f9fa; padding: 20px; border-left: 4px solid #007bff; }
                .section { margin: 20px 0; }
                .metric { background-color: #e9ecef; padding: 10px; margin: 5px 0; }
                .risk-high { color: #dc3545; font-weight: bold; }
                .risk-medium { color: #fd7e14; font-weight: bold; }
                .risk-low { color: #28a745; font-weight: bold; }
                .visualization { text-align: center; margin: 20px 0; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{{ report.decision_input.title }}</h1>
                <p>Generated: {{ generated_at.strftime('%Y-%m-%d %H:%M:%S') }}</p>
            </div>
            
            <div class="section">
                <h2>Executive Summary</h2>
                <div class="metric">Recommendation: {{ report.executive_summary.recommendation_category.value.replace('_', ' ').title() }}</div>
                <div class="metric">Recommended Option: {{ report.executive_summary.recommended_option }}</div>
                <div class="metric">Confidence Level: {{ report.executive_summary.confidence_level | percentage }}</div>
            </div>
            
            <div class="section">
                <h2>Key Findings</h2>
                <ul>
                {% for finding in report.executive_summary.key_findings %}
                    <li>{{ finding }}</li>
                {% endfor %}
                </ul>
            </div>
            
            {% if visualizations %}
            <div class="section">
                <h2>Analysis Visualizations</h2>
                {% for viz_name, viz_data in visualizations.items() %}
                    <div class="visualization">
                        <h3>{{ viz_name.replace('_', ' ').title() }}</h3>
                        <img src="{{ viz_data }}" alt="{{ viz_name }}" style="max-width: 100%;">
                    </div>
                {% endfor %}
            </div>
            {% endif %}
            
            <div class="section">
                <h2>Next Steps</h2>
                <ol>
                {% for step in report.executive_summary.next_steps %}
                    <li>{{ step }}</li>
                {% endfor %}
                </ol>
            </div>
        </body>
        </html>
        """
        
        # Save template
        template_path = os.path.join(self.template_dir, template_name)
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(default_template)
        
        return Template(default_template)
    
    def _generate_report_summary(self, report: DecisionReport) -> Dict[str, Any]:
        """Generate summary statistics for the report."""
        return {
            'total_options': len(report.option_evaluations),
            'total_risks': len(report.risk_assessments),
            'total_actions': len(report.action_items),
            'critical_actions': len(report.get_critical_action_items()),
            'consensus_level': report.consensus_analysis.consensus_level,
            'analysis_duration': report.analysis_duration,
            'participants_count': len(report.participants)
        }
    
    def _group_risks_by_category(self, report: DecisionReport) -> Dict[str, List[Dict[str, Any]]]:
        """Group risks by category for better organization."""
        risks_by_category = {}
        for risk in report.risk_assessments:
            category = risk.category.value
            if category not in risks_by_category:
                risks_by_category[category] = []
            risks_by_category[category].append(risk.dict())
        return risks_by_category
    
    def _calculate_agent_performance(self, report: DecisionReport) -> Dict[str, Any]:
        """Calculate agent performance metrics."""
        if not report.agent_analyses:
            return {}
        
        performance = {}
        for analysis in report.agent_analyses:
            performance[analysis.agent_role.value] = {
                'confidence_level': analysis.confidence_level,
                'recommendations_count': len(analysis.recommendations),
                'analysis_length': len(analysis.analysis),
                'participation_score': report.report_metrics.agent_participation.get(analysis.agent_role.value, 0)
            }
        return performance
    
    def _get_priority_style(self, priority: ActionPriority) -> str:
        """Get PDF style for action priority."""
        if priority == ActionPriority.CRITICAL:
            return 'HighRisk'
        elif priority == ActionPriority.HIGH:
            return 'MediumRisk'
        else:
            return 'LowRisk'
    
    def _save_base64_image(self, base64_data: str, filename: str) -> Optional[str]:
        """Save base64 image to temporary file."""
        try:
            import base64
            
            # Extract base64 data
            if base64_data.startswith('data:image'):
                base64_data = base64_data.split(',')[1]
            
            # Decode and save
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, filename)
            
            with open(temp_path, 'wb') as f:
                f.write(base64.b64decode(base64_data))
            
            return temp_path
            
        except Exception as e:
            logger.error(f"Failed to save base64 image: {e}")
            return None
    
    # Jinja2 filter functions
    def _format_datetime(self, value: datetime) -> str:
        """Format datetime for templates."""
        return value.strftime('%Y-%m-%d %H:%M:%S')
    
    def _format_percentage(self, value: float) -> str:
        """Format percentage for templates."""
        return f"{value:.1%}"
    
    def _format_currency(self, value: float) -> str:
        """Format currency for templates."""
        return f"${value:,.2f}"
    
    def _format_priority_badge(self, priority: ActionPriority) -> str:
        """Format priority badge for templates."""
        colors = {
            ActionPriority.CRITICAL: 'danger',
            ActionPriority.HIGH: 'warning',
            ActionPriority.MEDIUM: 'info',
            ActionPriority.LOW: 'secondary',
            ActionPriority.NICE_TO_HAVE: 'light'
        }
        color = colors.get(priority, 'secondary')
        return f'<span class="badge badge-{color}">{priority.value.upper()}</span>'
    
    def _format_risk_level(self, risk_score: float) -> str:
        """Format risk level for templates."""
        if risk_score >= 0.7:
            return '<span class="risk-high">HIGH</span>'
        elif risk_score >= 0.4:
            return '<span class="risk-medium">MEDIUM</span>'
        else:
            return '<span class="risk-low">LOW</span>'


# Utility functions
def generate_comprehensive_report(
    report: DecisionReport,
    output_dir: str = "reports",
    formats: List[str] = ["html", "pdf", "json"]
) -> Dict[str, str]:
    """
    Generate comprehensive report in multiple formats.
    
    Args:
        report: Decision report to generate
        output_dir: Directory to save reports
        formats: List of formats to generate
    
    Returns:
        Dictionary mapping format to file path
    """
    try:
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize generator
        generator = ReportGenerator()
        
        # Generate reports
        generated_files = {}
        
        for format_type in formats:
            if format_type == "html":
                html_content = generator.generate_html_report(report)
                html_path = os.path.join(output_dir, f"report_{report.report_id}.html")
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                generated_files['html'] = html_path
                
            elif format_type == "pdf":
                pdf_path = os.path.join(output_dir, f"report_{report.report_id}.pdf")
                generator.generate_pdf_report(report, pdf_path)
                generated_files['pdf'] = pdf_path
                
            elif format_type == "excel":
                excel_path = os.path.join(output_dir, f"report_{report.report_id}.xlsx")
                generator.generate_excel_report(report, excel_path)
                generated_files['excel'] = excel_path
                
            elif format_type == "json":
                json_path = os.path.join(output_dir, f"report_{report.report_id}.json")
                generator.generate_json_report(report, json_path)
                generated_files['json'] = json_path
        
        logger.info(f"Comprehensive report generated in {len(generated_files)} formats")
        return generated_files
        
    except Exception as e:
        logger.error(f"Failed to generate comprehensive report: {e}")
        raise


def validate_report_quality(report: DecisionReport) -> Dict[str, Any]:
    """
    Validate report quality and completeness.
    
    Args:
        report: Decision report to validate
    
    Returns:
        Validation results
    """
    try:
        validation_results = {
            'is_valid': True,
            'issues': [],
            'warnings': [],
            'quality_score': 0.0
        }
        
        # Check required fields
        if not report.decision_input.title:
            validation_results['issues'].append("Missing decision title")
            validation_results['is_valid'] = False
        
        if not report.agent_analyses:
            validation_results['issues'].append("No agent analyses found")
            validation_results['is_valid'] = False
        
        if not report.executive_summary.key_findings:
            validation_results['issues'].append("No key findings provided")
            validation_results['is_valid'] = False
        
        # Check data quality
        if report.executive_summary.confidence_level < 0.3:
            validation_results['warnings'].append("Low confidence level in recommendations")
        
        if not report.risk_assessments:
            validation_results['warnings'].append("No risk assessments provided")
        
        if not report.action_items:
            validation_results['warnings'].append("No action items provided")
        
        # Calculate quality score
        quality_factors = [
            len(report.agent_analyses) >= 3,  # Multiple agent perspectives
            len(report.option_evaluations) >= 2,  # Multiple options evaluated
            len(report.risk_assessments) >= 1,  # Risk assessment included
            len(report.action_items) >= 1,  # Action items provided
            report.executive_summary.confidence_level >= 0.6,  # Reasonable confidence
            report.report_metrics.overall_quality_score >= 0.7  # Good quality metrics
        ]
        
        validation_results['quality_score'] = sum(quality_factors) / len(quality_factors)
        
        return validation_results
        
    except Exception as e:
        logger.error(f"Report validation failed: {e}")
        return {
            'is_valid': False,
            'issues': [f"Validation error: {str(e)}"],
            'warnings': [],
            'quality_score': 0.0
        }