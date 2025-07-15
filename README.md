# 🧠 StrategySim AI - Multi-Agent Decision Analysis System

A comprehensive multi-agent decision analysis system built with AutoGen that provides strategic business decision support through specialized AI agents. Each agent represents a different professional perspective: Investor, Legal Officer, Analyst, Customer Representative, and Strategic Consultant.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 🚀 Features

### Multi-Agent Decision Analysis
- **5 Specialized Agents**: Investor, Legal, Analyst, Customer, and Strategic perspectives
- **SelectorGroupChat**: Dynamic agent selection for natural conversation flow
- **Real-time Collaboration**: Agents discuss and reach consensus on decisions
- **Comprehensive Analysis**: Financial, legal, market, and strategic evaluation

### Advanced Decision Support
- **Financial Analysis**: NPV, IRR, ROI, payback period calculations
- **Risk Assessment**: Multi-dimensional risk modeling and mitigation strategies
- **Market Research**: Customer behavior analysis and market opportunity evaluation
- **Legal Compliance**: Regulatory risk assessment and compliance frameworks
- **Strategic Planning**: SWOT analysis, Porter's Five Forces, decision trees

### Interactive Web Interface
- **Chainlit Integration**: Modern web interface for real-time interaction
- **Decision Workflows**: Guided decision input and analysis processes
- **Visualization**: Charts, graphs, and interactive dashboards
- **Report Generation**: HTML, PDF, Excel, and JSON export formats

### Robust Architecture
- **Pydantic Models**: Type-safe data validation and serialization
- **Comprehensive Testing**: 80%+ test coverage with unit and integration tests
- **Scalable Design**: Modular architecture supporting custom agents and tools
- **Production Ready**: Environment configuration, logging, and error handling

## 🏗️ Architecture

```
strategysim-ai/
├── src/
│   ├── agents/           # AI agent implementations
│   │   ├── base_agent.py     # Abstract base agent
│   │   ├── investor_agent.py  # Financial analysis agent
│   │   ├── legal_agent.py     # Legal compliance agent
│   │   ├── analyst_agent.py   # Risk analysis agent
│   │   ├── customer_agent.py  # Market research agent
│   │   ├── strategist_agent.py # Strategic planning agent
│   │   └── team.py           # SelectorGroupChat coordination
│   ├── models/           # Pydantic data models
│   │   ├── decision_models.py # Decision input/output models
│   │   ├── agent_models.py    # Agent conversation models
│   │   └── report_models.py   # Report and analysis models
│   ├── tools/            # Specialized agent tools
│   │   ├── financial_calculator.py # Financial analysis tools
│   │   ├── legal_compliance.py     # Legal assessment tools
│   │   ├── market_research.py      # Market analysis tools
│   │   ├── risk_modeler.py         # Risk modeling tools
│   │   └── strategic_frameworks.py # Strategic planning tools
│   ├── utils/            # Utility functions
│   │   ├── visualization.py    # Chart and graph generation
│   │   └── report_generator.py # Multi-format report generation
│   └── config/           # Configuration management
│       ├── settings.py       # Application settings
│       └── prompts.py        # Agent system prompts
├── tests/                # Comprehensive test suite
├── app.py               # Main Chainlit application
├── run_tests.py         # Test runner with coverage
└── pyproject.toml       # Modern Python packaging
```

## 🛠️ Installation

### Prerequisites
- Python 3.10+
- OpenAI API key (or other LLM provider)

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/zhengshui/strategy-sim.git
cd strategy-sim
```

2. **Set up virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -e .
# Or for development:
pip install -e ".[dev]"
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

5. **Run the application**
```bash
chainlit run app.py
```

The application will be available at `http://localhost:8000`

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following configuration:

```env
# Model Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here
MODEL_PROVIDER=openai
MODEL_NAME=gpt-4o

# Application Settings
DEBUG=true
LOG_LEVEL=INFO

# Chainlit Configuration
CHAINLIT_AUTH_SECRET=your-secret-key-here
CHAINLIT_HOST=0.0.0.0
CHAINLIT_PORT=8000
```

### Model Configuration

Create a `model_config.yaml` file for AutoGen model configuration:

```yaml
model_type: "openai"
model: "gpt-4o"
api_key: "${OPENAI_API_KEY}"
base_url: "https://api.openai.com/v1"
temperature: 0.7
max_tokens: 4000
```

## 🎯 Usage

### Decision Analysis Workflow

1. **Start a Session**: Launch the web interface and select a decision type
2. **Provide Decision Details**: Enter decision context, options, and constraints
3. **Multi-Agent Analysis**: Watch as specialized agents analyze your decision
4. **Receive Comprehensive Report**: Get detailed analysis with recommendations

### Supported Decision Types

- **💰 Pricing Decisions**: Product/service pricing optimization
- **🌍 Market Entry**: New market expansion analysis
- **🚀 Product Launch**: New product introduction planning
- **💼 Investment Decisions**: Investment opportunity evaluation
- **🤝 Strategic Partnerships**: Partnership opportunity assessment

### API Usage

```python
from src.agents import create_decision_team, run_decision_analysis
from src.models.decision_models import DecisionInput, DecisionType

# Create decision input
decision = DecisionInput(
    title="Market Expansion Decision",
    description="Evaluating expansion into European markets",
    decision_type=DecisionType.MARKET_ENTRY,
    options=[
        DecisionOption(name="UK Market", description="Enter UK market first"),
        DecisionOption(name="Germany Market", description="Enter German market first"),
    ],
    timeline="6 months",
    budget_range="$1M - $5M"
)

# Run analysis
team = create_decision_team()
report = await run_decision_analysis(decision, team)

# Access results
print(f"Recommendation: {report.executive_summary.recommended_option}")
print(f"Confidence: {report.executive_summary.confidence_level:.1%}")
```

## 🧪 Testing

### Run Tests

```bash
# Run all tests with coverage
python run_tests.py

# Run specific test suites
python run_tests.py --unit        # Unit tests only
python run_tests.py --integration # Integration tests only
python run_tests.py --tools       # Tool tests only

# Generate test report
python run_tests.py --report
```

### Test Coverage

The system includes comprehensive tests with 80%+ coverage:

- **Unit Tests**: Individual component functionality
- **Integration Tests**: Multi-agent team coordination
- **Tool Tests**: Financial calculations and analysis tools
- **Model Tests**: Data validation and business logic

## 📊 Agent Capabilities

### 💰 Investor Agent
- **Financial Analysis**: NPV, IRR, ROI calculations
- **Growth Projections**: Revenue and market growth modeling
- **Risk Assessment**: Investment risk evaluation
- **Market Opportunities**: Growth potential analysis

### ⚖️ Legal Agent
- **Compliance Assessment**: Regulatory requirement analysis
- **Risk Mitigation**: Legal risk identification and mitigation
- **Contract Analysis**: Agreement and partnership evaluation
- **Regulatory Monitoring**: Compliance framework assessment

### 📊 Analyst Agent
- **Risk Modeling**: Monte Carlo simulations and scenario analysis
- **Data Analysis**: Statistical analysis and trend identification
- **Performance Metrics**: KPI tracking and benchmarking
- **Market Research**: Competitive analysis and market sizing

### 👥 Customer Agent
- **Market Research**: Customer behavior and preference analysis
- **Segmentation**: Customer segment identification and targeting
- **User Experience**: Customer journey and satisfaction analysis
- **Demand Forecasting**: Market demand prediction and validation

### 🎯 Strategic Agent
- **Strategic Planning**: SWOT analysis and strategic frameworks
- **Decision Integration**: Cross-functional analysis synthesis
- **Implementation Planning**: Execution roadmap development
- **Performance Monitoring**: Success metrics and tracking

## 📈 Report Generation

### Multiple Export Formats

- **HTML**: Interactive web reports with visualizations
- **PDF**: Professional documents with charts and tables
- **Excel**: Detailed spreadsheets with multiple worksheets
- **JSON**: Structured data for API integration

### Visualization Features

- **Risk-Reward Matrices**: Option comparison and evaluation
- **Consensus Charts**: Agent agreement visualization
- **Implementation Timelines**: Project planning and milestones
- **Performance Dashboards**: Key metrics and indicators

## 🔧 Development

### Project Structure

The project follows modern Python best practices:

- **Modular Design**: Clear separation of concerns
- **Type Safety**: Comprehensive type hints and validation
- **Testing**: Extensive test coverage with pytest
- **Documentation**: Detailed docstrings and examples
- **Code Quality**: Black formatting, Ruff linting, MyPy checking

### Adding Custom Agents

1. **Create Agent Class**: Extend `BaseStrategicAgent`
2. **Implement Tools**: Add specialized analysis tools
3. **Define Prompts**: Create agent-specific system prompts
4. **Write Tests**: Add comprehensive test coverage

```python
from src.agents.base_agent import BaseStrategicAgent
from src.models.agent_models import AgentRole

class CustomAgent(BaseStrategicAgent):
    def __init__(self, model_client):
        super().__init__(
            agent_name="custom_agent",
            agent_role=AgentRole.CUSTOM,
            model_client=model_client,
            tools=self.get_specialized_tools()
        )
    
    def get_specialized_tools(self):
        return [custom_tool_1, custom_tool_2]
    
    async def perform_specialized_analysis(self, context, data):
        # Custom analysis logic
        return analysis_results
```

### Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Write tests**: Ensure comprehensive test coverage
4. **Run tests**: `python run_tests.py`
5. **Commit changes**: `git commit -m 'Add amazing feature'`
6. **Push to branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

## 📚 Documentation

### API Reference

For detailed API documentation, see the docstrings in the source code. Key modules:

- `src.agents`: Agent implementations and team coordination
- `src.models`: Data models and validation schemas
- `src.tools`: Specialized analysis tools and utilities
- `src.utils`: Report generation and visualization utilities

### Architecture Deep Dive

The system uses a sophisticated multi-agent architecture:

1. **SelectorGroupChat**: Dynamically selects the most appropriate agent for each conversation turn
2. **Specialized Agents**: Each agent has distinct tools and expertise areas
3. **Consensus Building**: Agents collaborate to reach informed decisions
4. **Comprehensive Reporting**: Analysis results are synthesized into actionable reports

## 🚀 Deployment

### Production Deployment

1. **Environment Setup**: Configure production environment variables
2. **Database Setup**: Set up database for session persistence (optional)
3. **Model Configuration**: Configure LLM provider and model settings
4. **Security**: Set up authentication and authorization
5. **Monitoring**: Configure logging and performance monitoring

### Docker Deployment

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install -e .

EXPOSE 8000
CMD ["chainlit", "run", "app.py", "--host", "0.0.0.0", "--port", "8000"]
```

## 🔒 Security

- **API Key Management**: Secure storage of API keys and secrets
- **Input Validation**: Comprehensive input sanitization and validation
- **Authentication**: Optional user authentication and authorization
- **Audit Logging**: Detailed logging for security and compliance

## 📞 Support

### Getting Help

- **Documentation**: Check the in-code documentation and examples
- **Issues**: Open an issue on GitHub for bug reports and feature requests
- **Discussions**: Join the community discussions for questions and ideas

### Common Issues

1. **API Key Errors**: Ensure your OpenAI API key is correctly configured
2. **Memory Issues**: Adjust model parameters for available system memory
3. **Network Issues**: Check internet connectivity for API calls
4. **Dependencies**: Ensure all required packages are installed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **AutoGen**: Microsoft's multi-agent conversation framework
- **Chainlit**: Modern web framework for AI applications
- **Pydantic**: Data validation and settings management
- **OpenAI**: GPT models for agent intelligence

---

Built with ❤️ by the StrategySim Team

For more information, visit our [GitHub repository](https://github.com/zhengshui/strategy-sim) or contact us at team@strategysim.ai.