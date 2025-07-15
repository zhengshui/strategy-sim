"""
Main Chainlit application for StrategySim AI.

Provides web interface for multi-agent strategic decision analysis.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, cast

import chainlit as cl
import yaml
from pydantic import ValidationError

from src.agents import create_decision_team, run_decision_analysis
from src.config.settings import settings, get_model_config
from src.models.decision_models import (
    DecisionInput, DecisionType, DecisionUrgency, DecisionOption, 
    DecisionConstraint, validate_decision_input
)
from src.models.agent_models import ConversationState
from src.models.report_models import DecisionReport

# Configure logging
logging.basicConfig(level=getattr(logging, settings.log_level))
logger = logging.getLogger(__name__)


@cl.set_starters
async def set_starters() -> List[cl.Starter]:
    """Set up conversation starters for different decision types."""
    return [
        cl.Starter(
            label="💰 Pricing Decision",
            message="I need help analyzing a pricing decision for my product/service.",
            icon="/public/pricing-icon.png"
        ),
        cl.Starter(
            label="🌍 Market Entry",
            message="I'm considering entering a new market and need strategic analysis.",
            icon="/public/market-icon.png"
        ),
        cl.Starter(
            label="🚀 Product Launch",
            message="I need to analyze a new product launch decision.",
            icon="/public/product-icon.png"
        ),
        cl.Starter(
            label="💼 Investment Decision",
            message="I need analysis for an investment opportunity.",
            icon="/public/investment-icon.png"
        ),
        cl.Starter(
            label="🤝 Strategic Partnership",
            message="I'm evaluating a strategic partnership opportunity.",
            icon="/public/partnership-icon.png"
        ),
    ]


@cl.on_chat_start
async def start_chat() -> None:
    """Initialize chat session with decision analysis team."""
    try:
        # Load model configuration
        model_config = get_model_config()
        
        # Create decision analysis team
        team = create_decision_team()
        
        # Store team in session
        cl.user_session.set("team", team)
        cl.user_session.set("conversation_state", "initializing")
        cl.user_session.set("decision_data", {})
        
        # Welcome message
        welcome_msg = cl.Message(
            content="""# 🧠 Welcome to StrategySim AI

I'm your strategic decision analysis assistant. I coordinate a team of expert AI agents to provide comprehensive analysis of your business decisions.

**My Expert Team:**
- 💰 **Investor Agent**: Aggressive financial analysis and growth opportunities
- ⚖️ **Legal Agent**: Conservative compliance and risk assessment
- 📊 **Analyst Agent**: Quantitative risk modeling and scenario analysis
- 👥 **Customer Agent**: Market research and customer impact analysis
- 🎯 **Strategic Agent**: Strategic synthesis and balanced recommendations

**How it works:**
1. Tell me about your decision
2. I'll gather the details through interactive questions
3. My expert team will analyze your decision from multiple perspectives
4. You'll receive a comprehensive report with recommendations

Ready to get started? Choose a decision type from the starters above or tell me about your decision!
""",
            author="StrategySim AI"
        )
        
        await welcome_msg.send()
        
        logger.info("Chat session initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize chat session: {e}")
        error_msg = cl.Message(
            content=f"❌ Sorry, I encountered an error during initialization: {str(e)}",
            author="StrategySim AI"
        )
        await error_msg.send()


@cl.on_message
async def handle_message(message: cl.Message) -> None:
    """Handle user messages and coordinate decision analysis."""
    try:
        # Get session data
        team = cl.user_session.get("team")
        conversation_state = cl.user_session.get("conversation_state", "initializing")
        decision_data = cl.user_session.get("decision_data", {})
        
        # Route based on conversation state
        if conversation_state == "initializing":
            await handle_initial_input(message, decision_data)
        elif conversation_state == "gathering_details":
            await handle_detail_gathering(message, decision_data)
        elif conversation_state == "analyzing":
            await handle_analysis_request(message, team, decision_data)
        elif conversation_state == "completed":
            await handle_follow_up(message, team)
        else:
            await handle_general_inquiry(message, team)
            
    except Exception as e:
        logger.error(f"Error handling message: {e}")
        error_msg = cl.Message(
            content=f"❌ I encountered an error: {str(e)}. Please try again.",
            author="StrategySim AI"
        )
        await error_msg.send()


async def handle_initial_input(message: cl.Message, decision_data: Dict[str, Any]) -> None:
    """Handle initial decision input and start gathering details."""
    try:
        # Determine decision type from message
        decision_type = detect_decision_type(message.content)
        
        # Store initial data
        decision_data["raw_input"] = message.content
        decision_data["decision_type"] = decision_type
        
        # Update session
        cl.user_session.set("decision_data", decision_data)
        cl.user_session.set("conversation_state", "gathering_details")
        
        # Send decision collection form
        await send_decision_form(decision_type)
        
    except Exception as e:
        logger.error(f"Error handling initial input: {e}")
        raise


async def handle_detail_gathering(message: cl.Message, decision_data: Dict[str, Any]) -> None:
    """Handle detailed decision information gathering."""
    try:
        # Parse the response (simplified - in production, you'd use structured forms)
        await parse_decision_details(message.content, decision_data)
        
        # Check if we have enough information
        if is_decision_complete(decision_data):
            # Show decision summary and ask for confirmation
            await show_decision_summary(decision_data)
            cl.user_session.set("conversation_state", "confirming")
        else:
            # Ask for missing information
            await ask_for_missing_info(decision_data)
            
    except Exception as e:
        logger.error(f"Error gathering details: {e}")
        raise


async def handle_analysis_request(message: cl.Message, team: Any, decision_data: Dict[str, Any]) -> None:
    """Handle decision analysis request."""
    try:
        # Check if user confirmed to proceed
        if "yes" in message.content.lower() or "proceed" in message.content.lower():
            await run_decision_analysis_flow(team, decision_data)
        else:
            # Go back to gathering details
            cl.user_session.set("conversation_state", "gathering_details")
            await cl.Message(
                content="Let's refine your decision details. What would you like to change?",
                author="StrategySim AI"
            ).send()
            
    except Exception as e:
        logger.error(f"Error handling analysis request: {e}")
        raise


async def handle_follow_up(message: cl.Message, team: Any) -> None:
    """Handle follow-up questions after analysis completion."""
    try:
        response_msg = cl.Message(
            content="I can help you with additional analysis or a new decision. What would you like to explore?",
            author="StrategySim AI"
        )
        await response_msg.send()
        
        # Reset for new decision
        cl.user_session.set("conversation_state", "initializing")
        cl.user_session.set("decision_data", {})
        
    except Exception as e:
        logger.error(f"Error handling follow-up: {e}")
        raise


async def handle_general_inquiry(message: cl.Message, team: Any) -> None:
    """Handle general inquiries and help requests."""
    try:
        if "help" in message.content.lower():
            await show_help_message()
        elif "status" in message.content.lower():
            await show_team_status(team)
        else:
            # General response
            response_msg = cl.Message(
                content="I can help you analyze strategic decisions. Please describe the decision you need help with.",
                author="StrategySim AI"
            )
            await response_msg.send()
            
    except Exception as e:
        logger.error(f"Error handling general inquiry: {e}")
        raise


def detect_decision_type(content: str) -> DecisionType:
    """Detect decision type from user input."""
    content_lower = content.lower()
    
    if any(word in content_lower for word in ["price", "pricing", "cost"]):
        return DecisionType.PRICING
    elif any(word in content_lower for word in ["market", "enter", "expansion"]):
        return DecisionType.MARKET_ENTRY
    elif any(word in content_lower for word in ["product", "launch", "release"]):
        return DecisionType.PRODUCT_LAUNCH
    elif any(word in content_lower for word in ["investment", "invest", "funding"]):
        return DecisionType.INVESTMENT
    elif any(word in content_lower for word in ["partnership", "partner", "alliance"]):
        return DecisionType.STRATEGIC_PARTNERSHIP
    else:
        return DecisionType.INVESTMENT  # Default


async def send_decision_form(decision_type: DecisionType) -> None:
    """Send interactive form for decision details."""
    try:
        form_msg = cl.Message(
            content=f"""## 📋 Decision Details for {decision_type.value.replace('_', ' ').title()}

Please provide the following information about your decision:

**Required Information:**
1. **Decision Title**: A clear, concise title for your decision
2. **Description**: Detailed description of the decision context
3. **Options**: What are the different options you're considering? (2-5 options)
4. **Timeline**: When do you need to make this decision?
5. **Urgency**: How urgent is this decision? (low/medium/high/critical)

**Additional Information (helpful but optional):**
- Budget range or financial constraints
- Key stakeholders involved
- Success metrics you'll use to measure outcomes
- Any specific constraints or limitations

You can provide this information in any format - I'll help organize it!
""",
            author="StrategySim AI"
        )
        await form_msg.send()
        
    except Exception as e:
        logger.error(f"Error sending decision form: {e}")
        raise


async def parse_decision_details(content: str, decision_data: Dict[str, Any]) -> None:
    """Parse decision details from user input."""
    try:
        # This is a simplified parser - in production, you'd use NLP or structured forms
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for key information
            if 'title:' in line.lower():
                decision_data['title'] = line.split(':', 1)[1].strip()
            elif 'description:' in line.lower():
                decision_data['description'] = line.split(':', 1)[1].strip()
            elif 'timeline:' in line.lower():
                decision_data['timeline'] = line.split(':', 1)[1].strip()
            elif 'urgency:' in line.lower():
                urgency_text = line.split(':', 1)[1].strip().lower()
                if urgency_text in ['low', 'medium', 'high', 'critical']:
                    decision_data['urgency'] = urgency_text
            elif 'option' in line.lower():
                if 'options' not in decision_data:
                    decision_data['options'] = []
                decision_data['options'].append(line.split(':', 1)[1].strip() if ':' in line else line)
        
        # If no structured format, treat as description
        if not any(key in decision_data for key in ['title', 'description']):
            decision_data['description'] = content
            
    except Exception as e:
        logger.error(f"Error parsing decision details: {e}")
        raise


def is_decision_complete(decision_data: Dict[str, Any]) -> bool:
    """Check if decision data is complete enough for analysis."""
    required_fields = ['title', 'description', 'timeline']
    
    # Check if at least title or description is provided
    if not (decision_data.get('title') or decision_data.get('description')):
        return False
    
    # Check if timeline is provided
    if not decision_data.get('timeline'):
        return False
    
    # Check if we have at least some options
    if not decision_data.get('options'):
        return False
    
    return True


async def show_decision_summary(decision_data: Dict[str, Any]) -> None:
    """Show decision summary and ask for confirmation."""
    try:
        summary = f"""## 📊 Decision Summary

**Title**: {decision_data.get('title', 'Not specified')}
**Type**: {decision_data.get('decision_type', 'Not specified')}
**Description**: {decision_data.get('description', 'Not specified')}
**Timeline**: {decision_data.get('timeline', 'Not specified')}
**Urgency**: {decision_data.get('urgency', 'medium')}

**Options being considered**:
{chr(10).join(f"• {option}" for option in decision_data.get('options', []))}

**Ready to proceed with analysis?** 
Type "yes" to start the multi-agent analysis or "no" to modify the details.
"""
        
        summary_msg = cl.Message(content=summary, author="StrategySim AI")
        await summary_msg.send()
        
        cl.user_session.set("conversation_state", "analyzing")
        
    except Exception as e:
        logger.error(f"Error showing decision summary: {e}")
        raise


async def ask_for_missing_info(decision_data: Dict[str, Any]) -> None:
    """Ask for missing decision information."""
    try:
        missing_info = []
        
        if not decision_data.get('title') and not decision_data.get('description'):
            missing_info.append("decision title or description")
        
        if not decision_data.get('timeline'):
            missing_info.append("timeline")
        
        if not decision_data.get('options'):
            missing_info.append("options you're considering")
        
        if missing_info:
            msg = cl.Message(
                content=f"I need a bit more information: {', '.join(missing_info)}. Can you provide these details?",
                author="StrategySim AI"
            )
            await msg.send()
            
    except Exception as e:
        logger.error(f"Error asking for missing info: {e}")
        raise


async def run_decision_analysis_flow(team: Any, decision_data: Dict[str, Any]) -> None:
    """Run the complete decision analysis flow."""
    try:
        # Show analysis starting message
        start_msg = cl.Message(
            content="🚀 **Starting Multi-Agent Analysis...**\n\nMy expert team is now analyzing your decision. You'll see their discussion in real-time.",
            author="StrategySim AI"
        )
        await start_msg.send()
        
        # Convert decision data to DecisionInput
        decision_input = create_decision_input(decision_data)
        
        # Validate decision input
        validation_result = validate_decision_input(decision_input)
        
        if not validation_result.is_valid:
            error_msg = cl.Message(
                content=f"❌ **Validation Error**: {validation_result.errors[0].message}",
                author="StrategySim AI"
            )
            await error_msg.send()
            return
        
        # Run analysis with streaming
        await run_analysis_with_streaming(team, decision_input)
        
        # Mark as completed
        cl.user_session.set("conversation_state", "completed")
        
    except Exception as e:
        logger.error(f"Error running decision analysis flow: {e}")
        raise


def create_decision_input(decision_data: Dict[str, Any]) -> DecisionInput:
    """Create DecisionInput from decision data."""
    try:
        # Create options
        options = []
        for i, option_text in enumerate(decision_data.get('options', [])):
            option = DecisionOption(
                name=f"Option {i+1}",
                description=option_text
            )
            options.append(option)
        
        # Create constraints
        constraints = []
        if decision_data.get('budget'):
            constraint = DecisionConstraint(
                name="Budget",
                description=f"Budget constraint: {decision_data['budget']}",
                constraint_type="budget",
                value=decision_data['budget']
            )
            constraints.append(constraint)
        
        # Create decision input
        decision_input = DecisionInput(
            title=decision_data.get('title', decision_data.get('description', 'Strategic Decision')[:50]),
            description=decision_data.get('description', 'Strategic decision analysis'),
            decision_type=DecisionType(decision_data.get('decision_type', 'investment')),
            urgency=DecisionUrgency(decision_data.get('urgency', 'medium')),
            options=options,
            constraints=constraints,
            timeline=decision_data.get('timeline', 'Not specified'),
            budget_range=decision_data.get('budget'),
            stakeholders=decision_data.get('stakeholders', [])
        )
        
        return decision_input
        
    except Exception as e:
        logger.error(f"Error creating decision input: {e}")
        raise


async def run_analysis_with_streaming(team: Any, decision_input: DecisionInput) -> None:
    """Run analysis with streaming updates."""
    try:
        # Start analysis
        analysis_msg = cl.Message(
            content="🔄 **Analysis in Progress...**\n\nThe team is discussing your decision...",
            author="StrategySim AI"
        )
        await analysis_msg.send()
        
        # Run the analysis (simplified - in production, you'd stream real agent messages)
        report = await run_decision_analysis(decision_input, team)
        
        # Show analysis results
        await show_analysis_results(report)
        
    except Exception as e:
        logger.error(f"Error running analysis with streaming: {e}")
        raise


async def show_analysis_results(report: DecisionReport) -> None:
    """Show comprehensive analysis results."""
    try:
        # Executive Summary
        summary_msg = cl.Message(
            content=f"""## 📋 Executive Summary

**Recommended Option**: {report.executive_summary.recommended_option}
**Recommendation**: {report.executive_summary.recommendation_category.value.replace('_', ' ').title()}
**Confidence Level**: {report.executive_summary.confidence_level:.1%}

### Key Findings:
{chr(10).join(f"• {finding}" for finding in report.executive_summary.key_findings)}

### Critical Risks:
{chr(10).join(f"• {risk}" for risk in report.executive_summary.critical_risks)}

### Success Factors:
{chr(10).join(f"• {factor}" for factor in report.executive_summary.success_factors)}
""",
            author="StrategySim AI"
        )
        await summary_msg.send()
        
        # Detailed Analysis
        detailed_msg = cl.Message(
            content=f"""## 🔍 Detailed Analysis

**Final Recommendation**: {report.final_recommendation}

### Agent Perspectives:
{chr(10).join(f"**{analysis.agent_role.value.title()}**: {analysis.analysis[:200]}..." for analysis in report.agent_analyses)}

### Next Steps:
{chr(10).join(f"{i+1}. {step}" for i, step in enumerate(report.executive_summary.next_steps))}

### Report Quality:
- **Completeness**: {report.report_metrics.completeness_score:.1%}
- **Analysis Depth**: {report.report_metrics.analysis_depth:.1%}
- **Overall Quality**: {report.report_metrics.overall_quality_score:.1%}

*Analysis completed in {report.analysis_duration:.1f} seconds*
""",
            author="StrategySim AI"
        )
        await detailed_msg.send()
        
        # Completion message
        completion_msg = cl.Message(
            content="""✅ **Analysis Complete!** 

Your comprehensive decision analysis is ready. Would you like to:
- Ask questions about the analysis
- Explore specific aspects in more detail
- Start a new decision analysis
- Get help with implementation planning

What would you like to do next?""",
            author="StrategySim AI"
        )
        await completion_msg.send()
        
    except Exception as e:
        logger.error(f"Error showing analysis results: {e}")
        raise


async def show_help_message() -> None:
    """Show help information."""
    help_msg = cl.Message(
        content="""## 🆘 Help & Support

**How to use StrategySim AI:**
1. Describe your strategic decision
2. Provide details when asked
3. Review the summary and confirm
4. Get comprehensive multi-agent analysis

**Decision Types Supported:**
- 💰 Pricing decisions
- 🌍 Market entry
- 🚀 Product launches
- 💼 Investment decisions
- 🤝 Strategic partnerships

**Commands:**
- Say "help" for this message
- Say "status" to check team status
- Say "new decision" to start over

**Need more help?** Visit our documentation or contact support.
""",
        author="StrategySim AI"
    )
    await help_msg.send()


async def show_team_status(team: Any) -> None:
    """Show team status information."""
    try:
        status = team.get_team_status()
        
        status_msg = cl.Message(
            content=f"""## 🏥 Team Status

**Team Size**: {status['team_size']} agents
**Status**: All agents operational

**Active Agents**:
{chr(10).join(f"• **{agent['name']}** ({agent['role']}) - {agent['tools_count']} tools" for agent in status['agents'])}

**Configuration**:
- Max turns: {status['configuration']['max_turns']}
- Termination: {status['configuration']['termination_condition']}

*Last updated: {status['last_updated']}*
""",
            author="StrategySim AI"
        )
        await status_msg.send()
        
    except Exception as e:
        logger.error(f"Error showing team status: {e}")
        error_msg = cl.Message(
            content="❌ Unable to retrieve team status at this time.",
            author="StrategySim AI"
        )
        await error_msg.send()


if __name__ == "__main__":
    # Run the Chainlit app
    import subprocess
    import sys
    
    # This would be run with: chainlit run app.py
    print("To run the app, use: chainlit run app.py")
    sys.exit(0)