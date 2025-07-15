# Contributing to StrategySim AI

Thank you for your interest in contributing to StrategySim AI! This guide will help you get started with contributing to our multi-agent decision analysis system.

## 🚀 Getting Started

### Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/strategy-sim.git
   cd strategy-sim
   ```

3. **Set up development environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

4. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

### Development Dependencies

The development environment includes:

- **Testing**: pytest, pytest-asyncio, pytest-cov
- **Code Quality**: black, ruff, mypy
- **Pre-commit**: pre-commit hooks for code quality

## 📋 Contribution Guidelines

### Code Style

We follow strict code quality standards:

- **Black**: Code formatting (line length: 88)
- **Ruff**: Fast Python linter
- **MyPy**: Static type checking
- **Docstrings**: Google style docstrings for all functions

### Testing Requirements

All contributions must include comprehensive tests:

- **Unit Tests**: Test individual components
- **Integration Tests**: Test multi-agent interactions
- **Coverage**: Maintain 80%+ test coverage
- **Async Tests**: Use pytest-asyncio for async code

### Documentation

- **Docstrings**: All functions must have Google-style docstrings
- **Type Hints**: All functions must have complete type hints
- **README Updates**: Update README.md for new features
- **Examples**: Include usage examples for new functionality

## 🔧 Types of Contributions

### 1. Bug Fixes

- **Issue**: Create or reference an existing issue
- **Tests**: Add tests that reproduce the bug
- **Fix**: Implement the minimal fix
- **Verification**: Ensure all tests pass

### 2. New Features

- **Discussion**: Open an issue to discuss the feature first
- **Design**: Follow existing architecture patterns
- **Implementation**: Include comprehensive tests
- **Documentation**: Update all relevant documentation

### 3. Agent Development

Adding new agents to the system:

```python
from src.agents.base_agent import BaseStrategicAgent
from src.models.agent_models import AgentRole

class MyCustomAgent(BaseStrategicAgent):
    def __init__(self, model_client):
        super().__init__(
            agent_name="my_custom_agent",
            agent_role=AgentRole.CUSTOM,
            model_client=model_client,
            tools=self.get_specialized_tools()
        )
    
    def get_specialized_tools(self):
        return [tool1, tool2, tool3]
    
    async def perform_specialized_analysis(self, context, data):
        # Implementation
        return analysis_results
```

### 4. Tool Development

Adding new analysis tools:

```python
def my_analysis_tool(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform custom analysis on input data.
    
    Args:
        input_data: Input data for analysis
        
    Returns:
        Analysis results
        
    Raises:
        ValueError: If input data is invalid
    """
    # Validation
    if not input_data:
        raise ValueError("Input data cannot be empty")
    
    # Analysis logic
    results = perform_analysis(input_data)
    
    return results
```

## 🧪 Testing Guidelines

### Test Structure

```
tests/
├── conftest.py              # Shared fixtures
├── test_models/             # Model tests
│   ├── test_decision_models.py
│   ├── test_agent_models.py
│   └── test_report_models.py
├── test_agents/             # Agent tests
│   ├── test_base_agent.py
│   └── test_investor_agent.py
├── test_tools/              # Tool tests
│   └── test_financial_calculator.py
├── test_integration/        # Integration tests
│   └── test_team_integration.py
└── test_utils/              # Utility tests
    └── test_report_generator.py
```

### Test Examples

**Unit Test:**
```python
def test_npv_calculation():
    """Test NPV calculation with positive cash flows."""
    cash_flows = [-100000, 30000, 35000, 40000, 45000]
    discount_rate = 0.10
    
    npv = calculate_npv(cash_flows, discount_rate)
    
    assert npv > 0
    assert isinstance(npv, float)
```

**Integration Test:**
```python
@pytest.mark.asyncio
async def test_team_decision_analysis(mock_model_client, sample_decision_input):
    """Test complete team decision analysis workflow."""
    team = DecisionAnalysisTeam(mock_model_client)
    
    conversation = await team.analyze_decision(sample_decision_input)
    
    assert conversation.state == ConversationState.CONCLUDED
    assert len(conversation.participants) == 5
```

### Running Tests

```bash
# Run all tests
python run_tests.py

# Run with coverage
python run_tests.py --coverage

# Run specific test suite
python run_tests.py --unit
python run_tests.py --integration

# Run specific test file
python -m pytest tests/test_models/test_decision_models.py -v
```

## 📚 Documentation Standards

### Docstring Format

Use Google-style docstrings:

```python
def calculate_roi(initial_investment: float, final_value: float, years: Optional[int] = None) -> float:
    """
    Calculate Return on Investment (ROI).
    
    Args:
        initial_investment: Initial investment amount
        final_value: Final value of investment
        years: Number of years for annualized calculation
        
    Returns:
        ROI as a decimal (e.g., 0.15 for 15%)
        
    Raises:
        ValueError: If initial_investment is zero or negative
        
    Example:
        >>> calculate_roi(100000, 150000)
        0.5
        >>> calculate_roi(100000, 150000, 3)
        0.144
    """
```

### Type Hints

All functions must have complete type hints:

```python
from typing import Dict, List, Optional, Any, Union

async def analyze_decision(
    self,
    decision_input: DecisionInput,
    conversation_id: Optional[str] = None
) -> AgentConversation:
    """Analysis implementation..."""
```

## 🔍 Code Review Process

### Before Submitting

1. **Run Tests**: Ensure all tests pass
   ```bash
   python run_tests.py
   ```

2. **Check Code Quality**:
   ```bash
   black .
   ruff check .
   mypy src/
   ```

3. **Update Documentation**: Ensure all changes are documented

### Pull Request Guidelines

1. **Title**: Use clear, descriptive titles
2. **Description**: Explain what changes were made and why
3. **Tests**: Include test coverage for new functionality
4. **Documentation**: Update relevant documentation
5. **Breaking Changes**: Clearly mark any breaking changes

### Review Criteria

- **Functionality**: Does the code work as intended?
- **Tests**: Are there comprehensive tests?
- **Code Quality**: Does it follow our style guidelines?
- **Documentation**: Is it well documented?
- **Architecture**: Does it fit the existing architecture?

## 🎯 Architecture Guidelines

### Project Structure

Follow the established project structure:

```
src/
├── agents/          # Agent implementations
├── models/          # Pydantic data models
├── tools/           # Analysis tools
├── utils/           # Utility functions
└── config/          # Configuration
```

### Design Principles

1. **Single Responsibility**: Each component has one clear purpose
2. **Open/Closed**: Open for extension, closed for modification
3. **Dependency Inversion**: Depend on abstractions, not concretions
4. **Composition over Inheritance**: Prefer composition patterns
5. **Fail Fast**: Validate inputs early and provide clear error messages

### Error Handling

```python
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def process_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process input data with proper error handling.
    
    Args:
        data: Input data to process
        
    Returns:
        Processed data
        
    Raises:
        ValueError: If data is invalid
    """
    try:
        # Validate input
        if not data:
            raise ValueError("Data cannot be empty")
        
        # Process data
        result = perform_processing(data)
        
        logger.info(f"Successfully processed data: {len(result)} items")
        return result
        
    except Exception as e:
        logger.error(f"Error processing data: {e}")
        raise
```

## 🐛 Bug Reports

### Before Reporting

1. **Search**: Check if the issue already exists
2. **Reproduce**: Ensure you can reproduce the bug
3. **Minimal Example**: Create a minimal reproduction case

### Bug Report Template

```markdown
## Bug Description
A clear description of the bug.

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen.

## Actual Behavior
What actually happens.

## Environment
- Python version:
- StrategySim AI version:
- OS:
- Other relevant details:

## Code Example
```python
# Minimal code to reproduce the issue
```

## Error Message
```
Full error traceback if available
```
```

## ✨ Feature Requests

### Feature Request Template

```markdown
## Feature Description
Clear description of the proposed feature.

## Use Case
Why is this feature needed? What problem does it solve?

## Proposed Implementation
How might this feature be implemented?

## Alternatives Considered
What other approaches were considered?

## Additional Context
Any other relevant information.
```

## 📊 Performance Guidelines

### Performance Considerations

1. **Async/Await**: Use async patterns for I/O operations
2. **Caching**: Implement caching for expensive operations
3. **Lazy Loading**: Load data only when needed
4. **Memory Management**: Be mindful of memory usage
5. **Parallel Processing**: Use concurrent execution where appropriate

### Performance Testing

```python
import time
import asyncio
from typing import List

async def benchmark_agent_analysis(agents: List[BaseAgent], iterations: int = 100):
    """Benchmark agent analysis performance."""
    start_time = time.time()
    
    tasks = [
        agent.analyze_decision("test", {})
        for agent in agents
        for _ in range(iterations)
    ]
    
    await asyncio.gather(*tasks)
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"Completed {len(tasks)} analyses in {total_time:.2f} seconds")
    print(f"Average time per analysis: {total_time / len(tasks):.3f} seconds")
```

## 🔒 Security Guidelines

### Security Considerations

1. **Input Validation**: Always validate and sanitize inputs
2. **API Keys**: Never commit API keys or secrets
3. **Error Messages**: Don't expose sensitive information in errors
4. **Dependencies**: Keep dependencies updated
5. **Logging**: Don't log sensitive information

### Security Checklist

- [ ] Input validation implemented
- [ ] No hardcoded secrets
- [ ] Error handling doesn't expose sensitive data
- [ ] Dependencies are up to date
- [ ] Logging is secure

## 🎉 Recognition

Contributors are recognized in:

- **README**: Major contributors listed
- **Release Notes**: Contributions acknowledged
- **GitHub**: Contributor graphs and statistics

## 📞 Getting Help

- **Issues**: Open an issue for questions
- **Discussions**: Use GitHub discussions
- **Code Review**: Ask questions during review

Thank you for contributing to StrategySim AI! 🚀