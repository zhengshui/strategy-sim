"""
Visualization utilities for StrategySim AI.

Contains tools for creating risk-reward matrices, decision trees,
and other visual representations of analysis results.
"""

import io
import base64
from typing import Dict, List, Optional, Tuple, Any
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from datetime import datetime

from ..models.report_models import DecisionReport, OptionEvaluation, RiskAssessment


def create_risk_reward_matrix(
    options: List[OptionEvaluation],
    title: str = "Risk-Reward Analysis"
) -> str:
    """
    Create risk-reward matrix visualization.
    
    Args:
        options: List of option evaluations
        title: Chart title
    
    Returns:
        Base64 encoded image string
    """
    try:
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Extract data
        risks = [opt.overall_risk_score for opt in options]
        rewards = [opt.overall_score for opt in options]
        names = [opt.option_name for opt in options]
        
        # Create scatter plot
        scatter = ax.scatter(risks, rewards, s=200, alpha=0.6, c=range(len(options)), cmap='viridis')
        
        # Add labels
        for i, name in enumerate(names):
            ax.annotate(name, (risks[i], rewards[i]), xytext=(5, 5), 
                       textcoords='offset points', fontsize=10, fontweight='bold')
        
        # Add quadrant lines
        ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5)
        ax.axvline(x=0.5, color='gray', linestyle='--', alpha=0.5)
        
        # Add quadrant labels
        ax.text(0.25, 0.75, 'Low Risk\nHigh Reward', ha='center', va='center', 
                bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.3))
        ax.text(0.75, 0.75, 'High Risk\nHigh Reward', ha='center', va='center',
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
        ax.text(0.25, 0.25, 'Low Risk\nLow Reward', ha='center', va='center',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))
        ax.text(0.75, 0.25, 'High Risk\nLow Reward', ha='center', va='center',
                bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.3))
        
        # Styling
        ax.set_xlabel('Risk Level', fontsize=12, fontweight='bold')
        ax.set_ylabel('Reward Potential', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        
        # Convert to base64
        return plot_to_base64(fig)
        
    except Exception as e:
        print(f"Error creating risk-reward matrix: {e}")
        return ""


def create_consensus_chart(
    consensus_data: Dict[str, float],
    title: str = "Agent Consensus Analysis"
) -> str:
    """
    Create consensus visualization chart.
    
    Args:
        consensus_data: Consensus data by option
        title: Chart title
    
    Returns:
        Base64 encoded image string
    """
    try:
        fig, ax = plt.subplots(figsize=(10, 6))
        
        options = list(consensus_data.keys())
        consensus_scores = list(consensus_data.values())
        
        # Create bar chart
        bars = ax.bar(options, consensus_scores, color='skyblue', alpha=0.7)
        
        # Add value labels on bars
        for bar, score in zip(bars, consensus_scores):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                   f'{score:.1%}', ha='center', va='bottom', fontweight='bold')
        
        # Add consensus threshold line
        ax.axhline(y=0.7, color='red', linestyle='--', alpha=0.7, label='Strong Consensus (70%)')
        ax.axhline(y=0.5, color='orange', linestyle='--', alpha=0.7, label='Moderate Consensus (50%)')
        
        # Styling
        ax.set_ylabel('Consensus Level', fontsize=12, fontweight='bold')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_ylim(0, 1)
        ax.grid(True, alpha=0.3, axis='y')
        ax.legend()
        
        # Rotate x-axis labels if needed
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
        plt.tight_layout()
        
        return plot_to_base64(fig)
        
    except Exception as e:
        print(f"Error creating consensus chart: {e}")
        return ""


def create_decision_timeline(
    milestones: List[Dict[str, Any]],
    title: str = "Implementation Timeline"
) -> str:
    """
    Create decision implementation timeline.
    
    Args:
        milestones: List of milestone dictionaries
        title: Chart title
    
    Returns:
        Base64 encoded image string
    """
    try:
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Create timeline
        y_pos = 0
        colors = ['red', 'orange', 'yellow', 'lightgreen', 'green']
        
        for i, milestone in enumerate(milestones):
            # Draw milestone
            ax.scatter(i, y_pos, s=200, c=colors[i % len(colors)], alpha=0.7, zorder=3)
            
            # Add milestone text
            ax.text(i, y_pos + 0.1, milestone.get('name', f'Milestone {i+1}'), 
                   ha='center', va='bottom', fontweight='bold', rotation=45)
            
            # Add timeline details
            ax.text(i, y_pos - 0.1, milestone.get('date', f'Month {i+1}'), 
                   ha='center', va='top', fontsize=10)
        
        # Draw timeline line
        ax.plot(range(len(milestones)), [y_pos] * len(milestones), 'k-', alpha=0.3, zorder=1)
        
        # Styling
        ax.set_ylim(-0.5, 0.5)
        ax.set_xlim(-0.5, len(milestones) - 0.5)
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_yticks([])
        ax.set_xlabel('Timeline', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')
        
        return plot_to_base64(fig)
        
    except Exception as e:
        print(f"Error creating decision timeline: {e}")
        return ""


def plot_to_base64(fig) -> str:
    """Convert matplotlib figure to base64 string."""
    try:
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight', dpi=300)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close(fig)
        return f"data:image/png;base64,{image_base64}"
    except Exception as e:
        print(f"Error converting plot to base64: {e}")
        return ""


def create_agent_participation_chart(
    participation_data: Dict[str, int],
    title: str = "Agent Participation"
) -> str:
    """
    Create agent participation pie chart.
    
    Args:
        participation_data: Agent participation counts
        title: Chart title
    
    Returns:
        Base64 encoded image string
    """
    try:
        fig, ax = plt.subplots(figsize=(8, 8))
        
        agents = list(participation_data.keys())
        counts = list(participation_data.values())
        
        # Create pie chart
        wedges, texts, autotexts = ax.pie(counts, labels=agents, autopct='%1.1f%%',
                                         startangle=90, colors=plt.cm.Set3.colors)
        
        # Styling
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        
        # Make percentage text bold
        for autotext in autotexts:
            autotext.set_fontweight('bold')
        
        return plot_to_base64(fig)
        
    except Exception as e:
        print(f"Error creating agent participation chart: {e}")
        return ""


def generate_report_visualizations(report: DecisionReport) -> Dict[str, str]:
    """
    Generate all visualizations for a decision report.
    
    Args:
        report: Decision report
    
    Returns:
        Dictionary of visualization names to base64 image strings
    """
    visualizations = {}
    
    try:
        # Risk-reward matrix
        if report.option_evaluations:
            visualizations['risk_reward_matrix'] = create_risk_reward_matrix(
                report.option_evaluations,
                f"Risk-Reward Analysis: {report.decision_input.title}"
            )
        
        # Consensus chart
        if report.consensus_analysis:
            visualizations['consensus_chart'] = create_consensus_chart(
                report.consensus_analysis.agreement_by_option,
                "Agent Consensus by Option"
            )
        
        # Agent participation
        if report.report_metrics:
            visualizations['agent_participation'] = create_agent_participation_chart(
                report.report_metrics.agent_participation,
                "Agent Participation in Analysis"
            )
        
        # Implementation timeline
        sample_milestones = [
            {"name": "Planning", "date": "Month 1"},
            {"name": "Approval", "date": "Month 2"},
            {"name": "Implementation", "date": "Month 3-6"},
            {"name": "Review", "date": "Month 7"},
            {"name": "Full Deployment", "date": "Month 8"}
        ]
        visualizations['timeline'] = create_decision_timeline(
            sample_milestones,
            "Implementation Timeline"
        )
        
    except Exception as e:
        print(f"Error generating report visualizations: {e}")
    
    return visualizations