"""
Agent communication and response models for StrategySim AI.

Contains Pydantic models for agent interactions including:
- AgentRole: Enumeration of agent roles
- AgentAnalysis: Individual agent analysis results
- AgentResponse: Structured agent response format
- AgentConversation: Conversation state management
- ToolResult: Tool execution results
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, field_validator


class AgentConfiguration(BaseModel):
    """Configuration settings for an agent."""
    
    name: str = Field(..., description="Agent name")
    role: str = Field(..., description="Agent role")
    personality: str = Field(default="balanced", description="Agent personality")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Temperature setting for responses")
    max_tokens: int = Field(default=1000, ge=100, le=4000, description="Maximum tokens for responses")
    tools_enabled: bool = Field(default=True, description="Whether tools are enabled")
    custom_instructions: Optional[str] = Field(None, description="Custom instructions for the agent")
    
    @field_validator('name')
    def validate_name(cls, v: str) -> str:
        """Ensure name is not empty."""
        if not v.strip():
            raise ValueError("Agent name cannot be empty")
        return v.strip()


class AgentRole(str, Enum):
    """Enumeration of agent roles in the system."""
    
    INVESTOR = "investor"
    LEGAL = "legal_officer"
    ANALYST = "analyst"
    CUSTOMER = "customer_representative"
    STRATEGIST = "strategic_consultant"
    MODERATOR = "moderator"


class AgentPersonality(str, Enum):
    """Enumeration of agent personality traits."""
    
    AGGRESSIVE = "aggressive"
    CONSERVATIVE = "conservative"
    ANALYTICAL = "analytical"
    EMPATHETIC = "empathetic"
    BALANCED = "balanced"
    SKEPTICAL = "skeptical"


class RiskLevel(str, Enum):
    """Enumeration of risk levels."""
    
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class ConfidenceLevel(str, Enum):
    """Enumeration of confidence levels."""
    
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class ToolResult(BaseModel):
    """Result from tool execution."""
    
    tool_name: str = Field(..., description="Name of the tool that was executed")
    success: bool = Field(..., description="Whether the tool execution was successful")
    result: Any = Field(..., description="Tool execution result")
    error_message: Optional[str] = Field(None, description="Error message if execution failed")
    execution_time: float = Field(..., description="Execution time in seconds")
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    @field_validator('execution_time')
    def validate_execution_time(cls, v: float) -> float:
        """Ensure execution time is non-negative."""
        if v < 0:
            raise ValueError("Execution time cannot be negative")
        return v


class AgentThought(BaseModel):
    """Individual agent thought or reasoning step."""
    
    content: str = Field(..., min_length=1, max_length=1000)
    thought_type: str = Field(..., description="Type of thought (analysis, concern, suggestion, etc.)")
    confidence: float = Field(..., ge=0.0, le=1.0)
    supporting_evidence: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)


class AgentRecommendation(BaseModel):
    """Agent recommendation with supporting rationale."""
    
    recommendation: str = Field(..., min_length=10, max_length=500)
    rationale: str = Field(..., min_length=20, max_length=1000)
    confidence: float = Field(..., ge=0.0, le=1.0)
    risk_assessment: RiskLevel
    priority: str = Field(..., description="Priority level (high, medium, low)")
    implementation_difficulty: str = Field(..., description="Implementation difficulty assessment")
    expected_impact: str = Field(..., description="Expected impact description")
    dependencies: List[str] = Field(default_factory=list)
    
    @field_validator('priority')
    def validate_priority(cls, v: str) -> str:
        """Ensure priority is valid."""
        if v.lower() not in ['high', 'medium', 'low']:
            raise ValueError("Priority must be high, medium, or low")
        return v.lower()


class AgentConcern(BaseModel):
    """Agent concern or risk identification."""
    
    concern: str = Field(..., min_length=10, max_length=500)
    severity: RiskLevel
    probability: float = Field(..., ge=0.0, le=1.0)
    impact: str = Field(..., description="Description of potential impact")
    mitigation_strategies: List[str] = Field(default_factory=list)
    category: str = Field(..., description="Category of concern (financial, legal, operational, etc.)")
    
    @field_validator('category')
    def validate_category(cls, v: str) -> str:
        """Ensure category is meaningful."""
        if len(v.strip()) < 1:
            raise ValueError("Category cannot be empty")
        return v.strip()


class AgentAnalysis(BaseModel):
    """Individual agent analysis result."""
    
    agent_name: str = Field(..., min_length=1, max_length=100)
    agent_role: AgentRole
    analysis: str = Field(..., min_length=50, max_length=3000)
    thoughts: List[AgentThought] = Field(default_factory=list)
    recommendations: List[AgentRecommendation] = Field(default_factory=list)
    concerns: List[AgentConcern] = Field(default_factory=list)
    risk_level: float = Field(..., ge=0.0, le=1.0, description="Overall risk assessment")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in analysis")
    supporting_data: Dict[str, Any] = Field(default_factory=dict)
    tool_results: List[ToolResult] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    
    @field_validator('agent_name')
    def validate_agent_name(cls, v: str) -> str:
        """Ensure agent name is meaningful."""
        if len(v.strip()) < 1:
            raise ValueError("Agent name cannot be empty")
        return v.strip()


class AgentResponse(BaseModel):
    """Structured agent response format."""
    
    agent_name: str = Field(..., min_length=1, max_length=100)
    agent_role: AgentRole
    message: str = Field(..., min_length=1, max_length=2000)
    response_type: str = Field(..., description="Type of response (analysis, question, recommendation, etc.)")
    target_agent: Optional[str] = Field(None, description="Target agent for directed messages")
    references: List[str] = Field(default_factory=list, description="References to previous messages or data")
    confidence: float = Field(..., ge=0.0, le=1.0)
    requires_response: bool = Field(default=False, description="Whether this message requires a response")
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.now)
    
    @field_validator('response_type')
    def validate_response_type(cls, v: str) -> str:
        """Ensure response type is valid."""
        valid_types = ['analysis', 'question', 'recommendation', 'concern', 'summary', 'clarification']
        if v.lower() not in valid_types:
            raise ValueError(f"Response type must be one of: {', '.join(valid_types)}")
        return v.lower()


class ConversationState(str, Enum):
    """Enumeration of conversation states."""
    
    INITIALIZING = "initializing"
    ANALYZING = "analyzing"
    DISCUSSING = "discussing"
    CONVERGING = "converging"
    CONCLUDED = "concluded"
    ERROR = "error"


class AgentConversation(BaseModel):
    """Conversation state management."""
    
    conversation_id: str = Field(..., min_length=1, max_length=100)
    participants: List[str] = Field(..., min_items=2)
    state: ConversationState = Field(default=ConversationState.INITIALIZING)
    messages: List[AgentResponse] = Field(default_factory=list)
    current_speaker: Optional[str] = Field(None)
    turn_count: int = Field(default=0, ge=0)
    max_turns: int = Field(default=20, ge=1)
    decision_input_id: Optional[str] = Field(None)
    context: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    @field_validator('participants')
    def validate_participants(cls, v: List[str]) -> List[str]:
        """Ensure participants are unique."""
        if len(set(v)) != len(v):
            raise ValueError("Participants must be unique")
        return v
    
    @field_validator('turn_count')
    def validate_turn_count(cls, v: int) -> int:
        """Ensure turn count is non-negative."""
        if v < 0:
            raise ValueError("Turn count cannot be negative")
        return v
    
    def add_message(self, message: AgentResponse) -> None:
        """Add a message to the conversation."""
        self.messages.append(message)
        self.current_speaker = message.agent_name
        self.turn_count += 1
        self.updated_at = datetime.now()
        
        # Update state based on turn count
        if self.turn_count >= self.max_turns:
            self.state = ConversationState.CONCLUDED
    
    def get_messages_by_agent(self, agent_name: str) -> List[AgentResponse]:
        """Get all messages from a specific agent."""
        return [msg for msg in self.messages if msg.agent_name == agent_name]
    
    def get_last_message(self) -> Optional[AgentResponse]:
        """Get the last message in the conversation."""
        return self.messages[-1] if self.messages else None
    
    def is_finished(self) -> bool:
        """Check if the conversation is finished."""
        return self.state in [ConversationState.CONCLUDED, ConversationState.ERROR]


class AgentMetrics(BaseModel):
    """Metrics for agent performance tracking."""
    
    agent_name: str = Field(..., min_length=1, max_length=100)
    agent_role: AgentRole
    total_messages: int = Field(default=0, ge=0)
    average_response_time: float = Field(default=0.0, ge=0.0)
    accuracy_score: float = Field(default=0.0, ge=0.0, le=1.0)
    user_satisfaction: float = Field(default=0.0, ge=0.0, le=1.0)
    tool_usage_count: int = Field(default=0, ge=0)
    successful_tool_usage: int = Field(default=0, ge=0)
    conversations_participated: int = Field(default=0, ge=0)
    last_active: datetime = Field(default_factory=datetime.now)
    
    @property
    def tool_success_rate(self) -> float:
        """Calculate tool success rate."""
        if self.tool_usage_count == 0:
            return 0.0
        return self.successful_tool_usage / self.tool_usage_count
    
    def update_metrics(self, response_time: float, tool_success: bool = False) -> None:
        """Update agent metrics."""
        self.total_messages += 1
        self.average_response_time = (
            (self.average_response_time * (self.total_messages - 1) + response_time) 
            / self.total_messages
        )
        
        if tool_success:
            self.successful_tool_usage += 1
            self.tool_usage_count += 1
        
        self.last_active = datetime.now()