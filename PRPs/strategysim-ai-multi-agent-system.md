name: "StrategySim AI Multi-Agent Decision System"
description: |

## Purpose
Build a comprehensive multi-agent decision simulation system using AutoGen that enables business decision makers to conduct thorough strategic analysis through specialized AI agents representing different professional perspectives.

## Core Principles
1. **Context is King**: Include ALL necessary documentation, examples, and caveats
2. **Validation Loops**: Provide executable tests/lints the AI can run and fix
3. **Information Dense**: Use keywords and patterns from the codebase
4. **Progressive Success**: Start simple, validate, then enhance
5. **Global rules**: Be sure to follow all rules in CLAUDE.md

---

## Goal
Create a production-ready multi-agent decision simulation platform where business professionals can input strategic decisions and receive comprehensive analysis from specialized AI agents (Investor, Legal Officer, Analyst, Customer Representative, Strategic Consultant) through an interactive web interface.

## Why
- **Business value**: Reduces decision-making risks and costs by providing multi-perspective analysis before implementation
- **Integration**: Demonstrates advanced AutoGen SelectorGroupChat patterns with professional role specialization
- **Problems solved**: Eliminates blind spots in strategic decision-making, quantifies risks, and provides structured decision reports

## What
A web-based application where:
- Users input strategic decisions through structured forms
- Multiple specialized AI agents analyze the decision from their professional perspectives
- Real-time collaborative discussion between agents using SelectorGroupChat
- Dynamic risk-reward visualization and comprehensive decision reports
- Support for various business scenarios (pricing, market entry, product launch, etc.)

### Success Criteria
- [ ] Five specialized agents with distinct professional personas and tools
- [ ] SelectorGroupChat enables natural agent interaction flow
- [ ] Chainlit interface provides real-time decision simulation visualization
- [ ] Risk-reward analysis with quantified metrics and probability assessments
- [ ] Structured decision reports with actionable recommendations
- [ ] Comprehensive test coverage for all agent interactions

## All Needed Context

### Documentation & References
```yaml
# MUST READ - Include these in your context window
- url: https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/selector-group-chat.html
  why: SelectorGroupChat implementation patterns for dynamic agent selection
  
- url: https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/index.html
  why: Core AgentChat patterns, agent creation, and tool integration
  
- url: https://docs.chainlit.io/get-started/overview
  why: Chainlit web interface patterns for multi-agent visualization
  
- url: https://docs.pydantic.dev/latest/concepts/models/
  why: Data validation patterns for business decision modeling
  
- file: examples/app_team.py
  why: RoundRobinGroupChat pattern to understand team structure
  
- file: examples/app_team_user_proxy.py
  why: User interaction patterns and termination conditions
  
- file: examples/app_agent.py
  why: Single agent implementation with tools and streaming
  
- file: examples/model_config.yaml
  why: Model configuration patterns for different providers
  
- file: CLAUDE.md
  why: Project-specific coding standards and architecture patterns
  
- file: INITIAL.md
  why: Core feature requirements and agent role specifications
```

### Current Codebase tree
```bash
.
├── examples/
│   ├── README.md
│   ├── app_agent.py                 # Single agent + tools pattern
│   ├── app_team.py                  # RoundRobinGroupChat pattern
│   ├── app_team_user_proxy.py       # User interaction pattern
│   ├── model_config.yaml            # LLM configuration
│   └── model_config_template.yaml
├── PRPs/
│   ├── EXAMPLE_multi_agent_prp.md
│   └── templates/
│       └── prp_base.md
├── CLAUDE.md                        # Project coding standards
├── INITIAL.md                       # Feature requirements
├── README.md
└── 产品需求.md                      # Business requirements
```

### Desired Codebase tree with files to be added
```bash
.
├── src/
│   ├── __init__.py                  # Package initialization
│   ├── agents/
│   │   ├── __init__.py              # Agent package init
│   │   ├── base_agent.py            # Base agent class with common functionality
│   │   ├── investor_agent.py        # Aggressive investor with financial tools
│   │   ├── legal_agent.py           # Conservative legal officer with compliance tools
│   │   ├── analyst_agent.py         # Pessimistic analyst with risk modeling tools
│   │   ├── customer_agent.py        # Customer representative with market research tools
│   │   └── strategist_agent.py      # Strategic consultant with decision frameworks
│   ├── tools/
│   │   ├── __init__.py              # Tools package init
│   │   ├── financial_calculator.py  # Financial analysis tools
│   │   ├── legal_compliance.py      # Legal and compliance checking tools
│   │   ├── risk_modeler.py          # Monte Carlo and risk analysis tools
│   │   ├── market_research.py       # Market and customer analysis tools
│   │   └── strategic_frameworks.py  # SWOT, decision trees, etc.
│   ├── models/
│   │   ├── __init__.py              # Models package init
│   │   ├── decision_models.py       # Pydantic models for decision inputs
│   │   ├── agent_models.py          # Agent response and communication models
│   │   └── report_models.py         # Decision report and analysis models
│   ├── config/
│   │   ├── __init__.py              # Config package init
│   │   ├── settings.py              # Environment configuration
│   │   └── prompts.py               # Agent system prompts and role definitions
│   └── utils/
│       ├── __init__.py              # Utils package init
│       ├── visualization.py         # Risk-reward visualization tools
│       └── report_generator.py      # Decision report generation
├── app.py                           # Main Chainlit application
├── requirements.txt                 # Updated dependencies
├── tests/
│   ├── __init__.py                  # Test package init
│   ├── conftest.py                  # Pytest configuration and fixtures
│   ├── test_agents/
│   │   ├── __init__.py              # Test agent package init
│   │   ├── test_investor_agent.py   # Investor agent tests
│   │   ├── test_legal_agent.py      # Legal agent tests
│   │   ├── test_analyst_agent.py    # Analyst agent tests
│   │   ├── test_customer_agent.py   # Customer agent tests
│   │   └── test_strategist_agent.py # Strategist agent tests
│   ├── test_tools/
│   │   ├── __init__.py              # Test tools package init
│   │   ├── test_financial_calculator.py
│   │   ├── test_legal_compliance.py
│   │   ├── test_risk_modeler.py
│   │   ├── test_market_research.py
│   │   └── test_strategic_frameworks.py
│   └── test_integration/
│       ├── __init__.py              # Integration tests package init
│       ├── test_selector_groupchat.py # SelectorGroupChat integration tests
│       └── test_chainlit_interface.py # Chainlit interface tests
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore patterns
└── pyproject.toml                   # Python project configuration
```

### Known Gotchas & Library Quirks
```python
# CRITICAL: AutoGen v0.4 uses async throughout - no sync functions in async context
# CRITICAL: SelectorGroupChat requires proper agent descriptions for selection logic
# CRITICAL: Chainlit requires specific async patterns for streaming agent responses
# CRITICAL: Agent tools must be properly registered with @agent.tool decorator
# CRITICAL: Model client streaming must be enabled for real-time updates
# CRITICAL: Termination conditions must be clearly defined to prevent infinite loops
# CRITICAL: Each agent needs distinct system prompts to avoid role confusion
# CRITICAL: Pydantic models require proper field validation for business logic
# CRITICAL: Use TextMentionTermination for proper conversation ending
# CRITICAL: Agent tools should return structured data, not just strings
# CRITICAL: Environment variables must be loaded with python-dotenv
# CRITICAL: File organization follows CLAUDE.md module size limits (500 lines max)
```

## Implementation Blueprint

### Data models and structure

```python
# src/models/decision_models.py - Core decision input structures
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class DecisionType(str, Enum):
    PRICING = "pricing"
    MARKET_ENTRY = "market_entry"
    PRODUCT_LAUNCH = "product_launch"
    INVESTMENT = "investment"
    MERGER_ACQUISITION = "merger_acquisition"

class DecisionInput(BaseModel):
    """Structured input for strategic decision analysis."""
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=20, max_length=2000)
    decision_type: DecisionType
    options: List[str] = Field(..., min_items=2, max_items=5)
    constraints: Dict[str, Any] = Field(default_factory=dict)
    timeline: str = Field(..., description="Decision timeline or deadline")
    budget_range: Optional[str] = None
    success_metrics: List[str] = Field(default_factory=list)
    
    @validator('options')
    def validate_options(cls, v):
        """Ensure options are meaningful and distinct."""
        if len(set(v)) != len(v):
            raise ValueError("Options must be unique")
        return v

class AgentAnalysis(BaseModel):
    """Individual agent analysis result."""
    agent_name: str
    agent_role: str
    analysis: str
    risk_level: float = Field(..., ge=0.0, le=1.0)
    confidence: float = Field(..., ge=0.0, le=1.0)
    recommendations: List[str]
    concerns: List[str]
    supporting_data: Dict[str, Any] = Field(default_factory=dict)

class DecisionReport(BaseModel):
    """Comprehensive decision analysis report."""
    decision_input: DecisionInput
    agent_analyses: List[AgentAnalysis]
    consensus_recommendation: str
    risk_assessment: Dict[str, float]
    probability_matrix: Dict[str, Dict[str, float]]
    action_items: List[str]
    generated_at: datetime = Field(default_factory=datetime.now)
```

### List of tasks to be completed

```yaml
Task 1: Project Structure and Configuration
CREATE src/config/settings.py:
  - PATTERN: Use pydantic-settings for environment management
  - Load OpenAI API key, model configurations
  - Support multiple LLM providers (OpenAI, Anthropic, etc.)
  - Validate required environment variables at startup

CREATE .env.example:
  - Document all required environment variables
  - Include API keys, model settings, debug flags

CREATE pyproject.toml:
  - Modern Python project configuration
  - Include all dependencies (autogen-agentchat, chainlit, pydantic, etc.)
  - Development dependencies (pytest, black, mypy, ruff)

Task 2: Core Data Models
CREATE src/models/decision_models.py:
  - PATTERN: Follow Pydantic v2 syntax with Field validation
  - Implement DecisionInput, AgentAnalysis, DecisionReport models
  - Add custom validators for business logic
  - Support multiple decision types (pricing, market entry, etc.)

CREATE src/models/agent_models.py:
  - Agent communication and response models
  - Tool output models with structured data
  - Conversation state management models

Task 3: Agent System Prompts and Configuration
CREATE src/config/prompts.py:
  - PATTERN: Each agent needs distinct professional persona
  - Investor: Aggressive financial focus, high-risk tolerance
  - Legal: Conservative compliance focus, risk aversion
  - Analyst: Pessimistic modeling, black swan events
  - Customer: Market sensitivity, user experience focus
  - Strategist: Balanced analysis, synthesis role

Task 4: Specialized Tools Implementation
CREATE src/tools/financial_calculator.py:
  - PATTERN: Async functions with proper error handling
  - NPV, IRR, payback period calculations
  - Cash flow modeling and sensitivity analysis
  - Return structured FinancialAnalysis models

CREATE src/tools/legal_compliance.py:
  - Regulatory compliance checking
  - Industry-specific legal considerations
  - Risk assessment for legal exposure
  - Integration with legal databases (simulated)

CREATE src/tools/risk_modeler.py:
  - Monte Carlo simulation for uncertainty analysis
  - Probability-impact matrix calculations
  - Scenario planning and stress testing
  - Quantitative risk scoring

CREATE src/tools/market_research.py:
  - Customer behavior simulation
  - Market acceptance probability modeling
  - Competitive analysis frameworks
  - Customer segmentation tools

CREATE src/tools/strategic_frameworks.py:
  - SWOT analysis generation
  - Decision tree creation and analysis
  - Porter's Five Forces evaluation
  - Strategic option evaluation

Task 5: Individual Agent Implementation
CREATE src/agents/base_agent.py:
  - PATTERN: Follow examples/app_agent.py structure
  - Common agent functionality and configuration
  - Tool registration patterns
  - Error handling and logging

CREATE src/agents/investor_agent.py:
  - PATTERN: AssistantAgent with financial tools
  - Aggressive questioning style in system prompt
  - Focus on profitability and growth potential
  - Challenge assumptions about revenue projections

CREATE src/agents/legal_agent.py:
  - Conservative legal perspective
  - Compliance and regulatory focus
  - Risk identification and mitigation
  - Contract and liability considerations

CREATE src/agents/analyst_agent.py:
  - Pessimistic analytical approach
  - Statistical modeling and data analysis
  - Black swan event consideration
  - Quantitative risk assessment

CREATE src/agents/customer_agent.py:
  - Customer-centric perspective
  - Market research and user behavior
  - Product-market fit evaluation
  - Customer satisfaction and retention

CREATE src/agents/strategist_agent.py:
  - Strategic synthesis and integration
  - Decision framework application
  - Balanced recommendation generation
  - Action plan development

Task 6: SelectorGroupChat Team Implementation
CREATE src/agents/__init__.py:
  - PATTERN: Follow examples/app_team.py but use SelectorGroupChat
  - Import and configure all specialized agents
  - Set up SelectorGroupChat with proper selection logic
  - Configure termination conditions based on consensus

MODIFY existing pattern:
  - Replace RoundRobinGroupChat with SelectorGroupChat
  - Add agent descriptions for selection algorithm
  - Implement approval_termination function
  - Handle dynamic agent selection based on context

Task 7: Chainlit Web Interface
CREATE app.py:
  - PATTERN: Follow examples/app_team_user_proxy.py structure
  - Implement structured decision input forms
  - Real-time streaming of agent discussions
  - Interactive visualization of analysis results
  - Decision report generation and download

IMPLEMENT features:
  - Decision input wizard with validation
  - Agent conversation visualization
  - Risk-reward matrix display
  - Progress tracking during analysis
  - Export functionality for reports

Task 8: Visualization and Reporting
CREATE src/utils/visualization.py:
  - Risk-reward matrix generation
  - Probability distribution charts
  - Agent consensus visualization
  - Decision tree rendering

CREATE src/utils/report_generator.py:
  - Structured decision report creation
  - PDF and markdown export
  - Executive summary generation
  - Action item extraction

Task 9: Comprehensive Testing
CREATE tests/conftest.py:
  - PATTERN: Follow pytest best practices
  - Mock external dependencies (OpenAI API)
  - Agent testing fixtures
  - Decision input factories

CREATE tests/test_agents/:
  - Individual agent testing
  - Tool integration testing
  - Response validation testing
  - Edge case handling

CREATE tests/test_integration/:
  - SelectorGroupChat flow testing
  - End-to-end decision simulation
  - Chainlit interface testing
  - Performance and stress testing

Task 10: Documentation and Deployment
UPDATE README.md:
  - Installation and setup instructions
  - Usage examples and tutorials
  - API documentation
  - Architecture overview

CREATE deployment configuration:
  - Docker containerization
  - Environment variable management
  - Production configuration
  - Monitoring and logging setup
```

### Per task pseudocode

```python
# Task 6: SelectorGroupChat Team Implementation
async def create_decision_team(model_client: ChatCompletionClient) -> SelectorGroupChat:
    """Create the specialized agent team with SelectorGroupChat."""
    
    # PATTERN: Each agent has distinct role and tools
    investor = InvestorAgent(
        name="investor", 
        model_client=model_client,
        tools=[financial_calculator, market_analyzer],
        system_message=INVESTOR_PROMPT  # Aggressive financial focus
    )
    
    legal = LegalAgent(
        name="legal_officer",
        model_client=model_client, 
        tools=[compliance_checker, risk_assessor],
        system_message=LEGAL_PROMPT  # Conservative compliance focus
    )
    
    analyst = AnalystAgent(
        name="analyst",
        model_client=model_client,
        tools=[monte_carlo_simulator, scenario_planner], 
        system_message=ANALYST_PROMPT  # Pessimistic modeling focus
    )
    
    customer = CustomerAgent(
        name="customer_representative",
        model_client=model_client,
        tools=[market_researcher, user_behavior_simulator],
        system_message=CUSTOMER_PROMPT  # Market sensitivity focus
    )
    
    strategist = StrategistAgent(
        name="strategic_consultant",
        model_client=model_client,
        tools=[swot_analyzer, decision_tree_generator],
        system_message=STRATEGIST_PROMPT  # Synthesis and integration
    )
    
    # CRITICAL: SelectorGroupChat requires agent descriptions for selection
    team = SelectorGroupChat(
        participants=[investor, legal, analyst, customer, strategist],
        model_client=model_client,  # For selection logic
        max_turns=20,  # Prevent infinite loops
        termination_condition=consensus_termination,  # Custom termination
        
        # PATTERN: Agent descriptions guide selection algorithm
        agent_descriptions={
            "investor": "Financial analysis, profitability assessment, growth potential",
            "legal_officer": "Compliance, regulatory issues, legal risks",
            "analyst": "Risk modeling, statistical analysis, scenario planning", 
            "customer_representative": "Market research, user experience, customer behavior",
            "strategic_consultant": "Strategic frameworks, synthesis, recommendations"
        }
    )
    
    return team

# Task 7: Chainlit Interface Implementation
@cl.on_chat_start
async def start_decision_session():
    """Initialize decision simulation session."""
    
    # PATTERN: Load model configuration
    with open("model_config.yaml", "r") as f:
        model_config = yaml.safe_load(f)
    model_client = ChatCompletionClient.load_component(model_config)
    
    # Create decision team
    team = await create_decision_team(model_client)
    
    # Store in session
    cl.user_session.set("team", team)
    cl.user_session.set("decision_context", {})
    
    # PATTERN: Interactive decision input
    await cl.Message(
        content="Welcome to StrategySim AI! Please provide your strategic decision details.",
        elements=[
            cl.Input(
                label="Decision Title",
                placeholder="e.g., Should we raise product prices by 15%?",
                required=True
            ),
            cl.Select(
                label="Decision Type", 
                options=["pricing", "market_entry", "product_launch", "investment"],
                required=True
            )
        ]
    ).send()

@cl.on_message
async def handle_decision_input(message: cl.Message):
    """Process decision input and start agent analysis."""
    
    # PATTERN: Validate input with Pydantic
    try:
        decision_input = DecisionInput.parse_obj(message.content)
    except ValidationError as e:
        await cl.Message(content=f"Invalid input: {e}").send()
        return
    
    # Get team from session
    team = cl.user_session.get("team")
    
    # PATTERN: Stream agent conversation
    streaming_response = cl.Message(content="")
    
    async for msg in team.run_stream(
        task=[TextMessage(content=decision_input.json(), source="user")],
        cancellation_token=CancellationToken()
    ):
        if isinstance(msg, ModelClientStreamingChunkEvent):
            # PATTERN: Show agent name and stream content
            if streaming_response.content == "":
                streaming_response.content = f"**{msg.source}**: "
            await streaming_response.stream_token(msg.content)
            
        elif isinstance(msg, TaskResult):
            # Analysis complete - generate report
            await streaming_response.send()
            await generate_decision_report(decision_input, msg.messages)
```

### Integration Points
```yaml
ENVIRONMENT:
  - add to: .env
  - vars: |
      # Model Configuration
      OPENAI_API_KEY=sk-...
      MODEL_PROVIDER=openai
      MODEL_NAME=gpt-4o
      
      # Application Settings
      DEBUG=true
      LOG_LEVEL=INFO
      
      # Chainlit Configuration
      CHAINLIT_AUTH_SECRET=your-secret-key
      CHAINLIT_HOST=0.0.0.0
      CHAINLIT_PORT=8000

DEPENDENCIES:
  - Update requirements.txt with:
    - autogen-agentchat>=0.4.0
    - autogen-ext[openai]>=0.4.0
    - chainlit>=1.0.0
    - pydantic>=2.0.0
    - pydantic-settings>=2.0.0
    - python-dotenv>=1.0.0
    - numpy>=1.24.0
    - matplotlib>=3.7.0
    - plotly>=5.15.0

DATABASE:
  - Optional: SQLite for session persistence
  - Decision history storage
  - Agent performance metrics

CONFIG:
  - Model configuration files in config/
  - Agent prompt templates
  - Tool parameter configurations
```

## Validation Loop

### Level 1: Syntax & Style
```bash
# Run these FIRST - fix any errors before proceeding
ruff check src/ --fix              # Auto-fix style issues
mypy src/                          # Type checking
black src/                         # Code formatting

# Expected: No errors. If errors, READ and fix.
```

### Level 2: Unit Tests
```python
# tests/test_agents/test_investor_agent.py
async def test_investor_agent_financial_analysis():
    """Test investor agent provides financial analysis."""
    agent = InvestorAgent(
        name="investor",
        model_client=mock_model_client,
        tools=[financial_calculator]
    )
    
    result = await agent.run("Analyze pricing increase from $100 to $115")
    
    assert result.data
    assert "revenue" in result.data.lower()
    assert "profit" in result.data.lower()

async def test_selector_groupchat_agent_selection():
    """Test SelectorGroupChat selects appropriate agents."""
    team = await create_decision_team(mock_model_client)
    
    # Financial question should select investor
    result = await team.run("What's the ROI of this investment?")
    
    # Verify investor was selected (implementation depends on AutoGen internals)
    assert "investor" in [msg.source for msg in result.messages]

# tests/test_tools/test_financial_calculator.py
def test_npv_calculation():
    """Test NPV calculation accuracy."""
    cash_flows = [-1000, 300, 400, 500, 600]
    discount_rate = 0.1
    
    npv = calculate_npv(cash_flows, discount_rate)
    
    # Expected NPV ≈ 338.65
    assert abs(npv - 338.65) < 0.01

def test_monte_carlo_simulation():
    """Test Monte Carlo risk simulation."""
    scenarios = generate_monte_carlo_scenarios(
        base_revenue=100000,
        volatility=0.2,
        iterations=1000
    )
    
    assert len(scenarios) == 1000
    assert all(s > 0 for s in scenarios)  # All scenarios positive
    assert 80000 < np.mean(scenarios) < 120000  # Reasonable range
```

```bash
# Run tests iteratively until passing:
pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html

# Target: 80%+ coverage, all tests passing
```

### Level 3: Integration Test
```bash
# Test Chainlit interface
chainlit run app.py --port 8000

# Expected interaction flow:
# 1. User sees decision input form
# 2. User enters: "Should we increase subscription price from $99 to $129?"
# 3. System validates input and starts agent analysis
# 4. Agents discuss in real-time (visible to user):
#    - Investor: "This 30% increase could boost revenue by..."
#    - Legal: "We need to check contract terms for price change clauses..."
#    - Analyst: "Risk of 15-25% customer churn based on price elasticity..."
#    - Customer: "User feedback indicates resistance above $120..."
#    - Strategist: "Recommend gradual increase with value justification..."
# 5. System generates comprehensive decision report
# 6. User can download report and see risk visualization

# Test decision scenarios:
curl -X POST http://localhost:8000/api/decision \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Market Entry Strategy",
    "description": "Should we enter the European market?",
    "decision_type": "market_entry",
    "options": ["Direct entry", "Partnership", "Acquisition", "Licensing"]
  }'
```

## Final Validation Checklist
- [ ] All tests pass: `pytest tests/ -v`
- [ ] No linting errors: `ruff check src/`
- [ ] No type errors: `mypy src/`
- [ ] SelectorGroupChat dynamically selects appropriate agents
- [ ] Each agent provides distinct professional perspective
- [ ] Chainlit interface streams agent conversations in real-time
- [ ] Decision reports generate with quantified risk assessments
- [ ] Agent tools return structured, actionable data
- [ ] Termination conditions prevent infinite loops
- [ ] Error handling gracefully manages API failures
- [ ] Documentation provides clear setup and usage instructions
- [ ] Environment configuration works across different deployments

---

## Anti-Patterns to Avoid
- ❌ Don't use RoundRobinGroupChat when dynamic selection is needed
- ❌ Don't create generic agents - each must have distinct expertise
- ❌ Don't skip agent descriptions for SelectorGroupChat
- ❌ Don't ignore business logic validation in Pydantic models
- ❌ Don't hardcode prompts - use configuration files
- ❌ Don't assume agent conversations will terminate naturally
- ❌ Don't return unstructured text from tools - use Pydantic models
- ❌ Don't skip error handling for external API failures
- ❌ Don't create files longer than 500 lines (CLAUDE.md requirement)
- ❌ Don't commit API keys or sensitive configuration

## Confidence Score: 8/10

High confidence due to:
- Clear examples in existing codebase to follow
- Well-documented AutoGen SelectorGroupChat patterns
- Established Chainlit interface patterns
- Comprehensive business logic validation approach
- Detailed task breakdown with specific implementation patterns

Minor uncertainty around:
- SelectorGroupChat selection algorithm fine-tuning
- Agent conversation flow optimization for business contexts
- Real-time visualization performance with complex decision analysis