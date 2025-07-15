### 🔄 Project Awareness & Context
- **Always read `INITIAL.md`** at the start of a new conversation to understand the project's architecture, goals, style, and constraints.
- **Check `TASK.md`** before starting a new task. If the task isn't listed, add it with a brief description and today's date.
- **Use consistent naming conventions, file structure, and architecture patterns** as described in `INITIAL.md`.
- **Use venv_linux** (the virtual environment) whenever executing Python commands, including for unit tests.

### 🤖 StrategySim AI 专项指导
- **这是一个基于AutoGen的多代理决策推演系统**，重点关注Agent角色设计和团队协作。
- **每个Agent都有明确的专业背景**：投资人、法务官、分析师、客户代言人、战略顾问。
- **使用SelectorGroupChat而不是RoundRobinGroupChat**，实现更自然的对话流。
- **所有Agent都需要具备相应的专业工具和知识库**。
- **优先考虑决策推演的准确性和可信度**，避免幻觉和不切实际的建议。

### 🧱 Code Structure & Modularity
- **Never create a file longer than 500 lines of code.** If a file approaches this limit, refactor by splitting it into modules or helper files.
- **Organize code into clearly separated modules**, grouped by feature or responsibility.
  For agents this looks like:
    - `agent.py` - Main agent definition and execution logic 
    - `tools.py` - Tool functions used by the agent 
    - `prompts.py` - System prompts
- **Use clear, consistent imports** (prefer relative imports within packages).
- **Use python_dotenv and load_env()** for environment variables.

### 🎭 Agent Design Principles
- **每个Agent都有独特的系统提示**，体现其专业背景和思维模式。
- **Agent工具集要与其角色匹配**：
  - 投资人Agent → 财务计算、市场分析工具
  - 法务官Agent → 法规数据库、合规检查工具
  - 分析师Agent → 风险建模、蒙特卡洛模拟工具
  - 客户Agent → 市场调研、用户画像工具
  - 战略顾问Agent → 决策树、SWOT分析工具
- **避免Agent角色混淆**，每个Agent只专注于其专业领域。
- **设计合理的终止条件**，避免推演陷入无限循环。

### 🔒 Data Security & Privacy
- **敏感决策数据需要加密存储**，使用环境变量管理加密密钥。
- **支持本地化部署选项**，确保企业数据不出内网。
- **记录推演过程但保护隐私**，避免在日志中暴露敏感信息。
- **实现数据访问控制**，不同用户级别有不同的功能权限。

### 🧪 Testing & Reliability
- **Always create Pytest unit tests for new features** (functions, classes, routes, etc).
- **After updating any logic**, check whether existing unit tests need to be updated. If so, do it.
- **Tests should live in a `/tests` folder** mirroring the main app structure.
  - Include at least:
    - 1 test for expected use
    - 1 edge case
    - 1 failure case

### 🎯 Multi-Agent System Testing
- **单Agent测试**：测试每个Agent的独立功能和专业能力。
- **团队协作测试**：测试多Agent之间的交互和协作流程。
- **决策推演测试**：使用真实业务场景验证推演结果的合理性。
- **压力测试**：测试系统在高并发和复杂决策场景下的性能。
- **Mock外部依赖**：模拟法规数据库、市场数据等外部服务。

### ✅ Task Completion
- **Mark completed tasks in `TASK.md`** immediately after finishing them.
- Add new sub-tasks or TODOs discovered during development to `TASK.md` under a “Discovered During Work” section.

### 📎 Style & Conventions
- **Use Python** as the primary language.
- **Follow PEP8**, use type hints, and format with `black`.
- **Use `pydantic` for data validation**.
- Use `FastAPI` for APIs and `SQLAlchemy` or `SQLModel` for ORM if applicable.
- Write **docstrings for every function** using the Google style:
  ```python
  def example():
      """
      Brief summary.

      Args:
          param1 (type): Description.

      Returns:
          type: Description.
      """
  ```

### 📚 Documentation & Explainability
- **Update `README.md`** when new features are added, dependencies change, or setup steps are modified.
- **Comment non-obvious code** and ensure everything is understandable to a mid-level developer.
- When writing complex logic, **add an inline `# Reason:` comment** explaining the why, not just the what.

### 🔍 Decision Analysis Documentation
- **决策推演过程必须可追溯**，记录每个Agent的推理过程和依据。
- **为每个Agent的专业判断提供数据支撑**，避免基于假设的推理。
- **生成的决策报告要包含置信度评估**，让用户了解推演结果的可靠性。
- **提供推演过程的可视化展示**，帮助用户理解复杂的决策逻辑。

### 🧠 AI Behavior Rules
- **Never assume missing context. Ask questions if uncertain.**
- **Never hallucinate libraries or functions** – only use known, verified Python packages.
- **Always confirm file paths and module names** exist before referencing them in code or tests.
- **Never delete or overwrite existing code** unless explicitly instructed to or if part of a task from `TASK.md`.

### 🎪 Decision System Behavior Rules
- **每个Agent的输出都要基于其专业背景**，不要让投资人Agent谈论法律问题。
- **避免Agent给出过于绝对的判断**，决策推演应该展示不确定性和概率。
- **确保推演过程的逻辑连贯性**，每个结论都要有前提和推理链。
- **集成真实数据源**，避免使用虚假或过时的市场数据。
- **设计合理的Agent交互规则**，避免无效的重复对话。