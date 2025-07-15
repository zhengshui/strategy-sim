"""
Market research and customer analysis tools for the Customer Agent.

Contains tools for customer behavior analysis, market segmentation,
competitive analysis, and user experience evaluation.
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
from pydantic import BaseModel, Field, field_validator
import numpy as np
import random


class CustomerSegment(str, Enum):
    """Customer segment types."""
    
    EARLY_ADOPTERS = "early_adopters"
    MAINSTREAM = "mainstream"
    LAGGARDS = "laggards"
    PRICE_SENSITIVE = "price_sensitive"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"
    SMB = "smb"
    CONSUMER = "consumer"


class MarketMaturity(str, Enum):
    """Market maturity levels."""
    
    EMERGING = "emerging"
    GROWTH = "growth"
    MATURE = "mature"
    DECLINING = "declining"


class CompetitivePosition(str, Enum):
    """Competitive position types."""
    
    LEADER = "leader"
    CHALLENGER = "challenger"
    FOLLOWER = "follower"
    NICHE = "niche"


class AdoptionStage(str, Enum):
    """Product adoption stages."""
    
    AWARENESS = "awareness"
    CONSIDERATION = "consideration"
    TRIAL = "trial"
    ADOPTION = "adoption"
    RETENTION = "retention"
    ADVOCACY = "advocacy"


class CustomerProfile(BaseModel):
    """Customer profile definition."""
    
    segment: CustomerSegment
    size: int = Field(..., description="Segment size")
    demographics: Dict[str, Any] = Field(..., description="Demographic characteristics")
    psychographics: Dict[str, Any] = Field(..., description="Psychographic characteristics")
    behavior_patterns: Dict[str, Any] = Field(..., description="Behavioral patterns")
    needs: List[str] = Field(..., description="Customer needs")
    pain_points: List[str] = Field(..., description="Customer pain points")
    decision_criteria: List[str] = Field(..., description="Decision-making criteria")
    price_sensitivity: float = Field(..., ge=0.0, le=1.0, description="Price sensitivity score")
    brand_loyalty: float = Field(..., ge=0.0, le=1.0, description="Brand loyalty score")
    adoption_likelihood: float = Field(..., ge=0.0, le=1.0, description="Adoption likelihood")
    
    @field_validator('size')
    def validate_size(cls, v: int) -> int:
        """Ensure segment size is positive."""
        if v <= 0:
            raise ValueError("Segment size must be positive")
        return v


class MarketAnalysis(BaseModel):
    """Market analysis result."""
    
    market_name: str = Field(..., description="Market name")
    market_size: float = Field(..., description="Total addressable market size")
    market_growth_rate: float = Field(..., description="Market growth rate")
    market_maturity: MarketMaturity
    key_trends: List[str] = Field(..., description="Key market trends")
    growth_drivers: List[str] = Field(..., description="Market growth drivers")
    barriers_to_entry: List[str] = Field(..., description="Barriers to market entry")
    market_segments: List[CustomerProfile] = Field(..., description="Customer segments")
    competitive_intensity: float = Field(..., ge=0.0, le=1.0, description="Competitive intensity")
    
    @field_validator('market_name')
    def validate_market_name(cls, v: str) -> str:
        """Ensure market name is meaningful."""
        if not v.strip():
            raise ValueError("Market name cannot be empty")
        return v.strip()


class CompetitorAnalysis(BaseModel):
    """Competitor analysis result."""
    
    competitor_name: str = Field(..., description="Competitor name")
    market_share: float = Field(..., ge=0.0, le=1.0, description="Market share")
    competitive_position: CompetitivePosition
    strengths: List[str] = Field(..., description="Competitor strengths")
    weaknesses: List[str] = Field(..., description="Competitor weaknesses")
    products_services: List[str] = Field(..., description="Products and services")
    pricing_strategy: str = Field(..., description="Pricing strategy")
    distribution_channels: List[str] = Field(..., description="Distribution channels")
    marketing_approach: str = Field(..., description="Marketing approach")
    financial_performance: Dict[str, float] = Field(default_factory=dict)
    strategic_focus: str = Field(..., description="Strategic focus")
    
    @field_validator('competitor_name')
    def validate_competitor_name(cls, v: str) -> str:
        """Ensure competitor name is meaningful."""
        if not v.strip():
            raise ValueError("Competitor name cannot be empty")
        return v.strip()


class CustomerJourney(BaseModel):
    """Customer journey mapping result."""
    
    stage: AdoptionStage
    touchpoints: List[str] = Field(..., description="Customer touchpoints")
    customer_actions: List[str] = Field(..., description="Customer actions")
    emotions: List[str] = Field(..., description="Customer emotions")
    pain_points: List[str] = Field(..., description="Pain points in this stage")
    opportunities: List[str] = Field(..., description="Improvement opportunities")
    success_metrics: List[str] = Field(..., description="Success metrics")
    conversion_rate: float = Field(..., ge=0.0, le=1.0, description="Conversion rate to next stage")
    
    @field_validator('touchpoints')
    def validate_touchpoints(cls, v: List[str]) -> List[str]:
        """Ensure touchpoints are provided."""
        if not v:
            raise ValueError("At least one touchpoint is required")
        return v


class CustomerFeedback(BaseModel):
    """Customer feedback analysis result."""
    
    feedback_source: str = Field(..., description="Source of feedback")
    feedback_type: str = Field(..., description="Type of feedback")
    sentiment_score: float = Field(..., ge=-1.0, le=1.0, description="Sentiment score")
    key_themes: List[str] = Field(..., description="Key themes identified")
    satisfaction_score: float = Field(..., ge=0.0, le=5.0, description="Satisfaction score")
    recommendation_score: float = Field(..., ge=0.0, le=10.0, description="Net Promoter Score")
    feature_requests: List[str] = Field(default_factory=list)
    complaints: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)
    
    @field_validator('feedback_source')
    def validate_feedback_source(cls, v: str) -> str:
        """Ensure feedback source is meaningful."""
        if not v.strip():
            raise ValueError("Feedback source cannot be empty")
        return v.strip()


class MarketResearchReport(BaseModel):
    """Comprehensive market research report."""
    
    report_id: str = Field(..., description="Unique report identifier")
    research_objective: str = Field(..., description="Research objective")
    market_analysis: MarketAnalysis
    competitor_analyses: List[CompetitorAnalysis] = Field(..., description="Competitor analyses")
    customer_profiles: List[CustomerProfile] = Field(..., description="Customer profiles")
    customer_journey: List[CustomerJourney] = Field(..., description="Customer journey stages")
    customer_feedback: List[CustomerFeedback] = Field(default_factory=list)
    market_opportunity: Dict[str, Any] = Field(..., description="Market opportunity assessment")
    recommendations: List[str] = Field(..., description="Strategic recommendations")
    research_limitations: List[str] = Field(default_factory=list)
    methodology: str = Field(..., description="Research methodology")
    research_date: datetime = Field(default_factory=datetime.now)
    
    @field_validator('report_id')
    def validate_report_id(cls, v: str) -> str:
        """Ensure report ID is meaningful."""
        if not v.strip():
            raise ValueError("Report ID cannot be empty")
        return v.strip()


# Market research databases and templates
MARKET_RESEARCH_DATABASE = {
    "technology": {
        "segments": [
            {"name": "Early Adopters", "size": 0.15, "price_sensitivity": 0.3, "adoption_speed": 0.9},
            {"name": "Mainstream", "size": 0.60, "price_sensitivity": 0.7, "adoption_speed": 0.5},
            {"name": "Laggards", "size": 0.25, "price_sensitivity": 0.9, "adoption_speed": 0.2}
        ],
        "trends": [
            "Digital transformation acceleration",
            "Cloud-first strategies",
            "AI/ML integration",
            "Cybersecurity focus",
            "Remote work technologies"
        ],
        "barriers": [
            "High switching costs",
            "Technical complexity",
            "Security concerns",
            "Integration challenges"
        ]
    },
    "healthcare": {
        "segments": [
            {"name": "Hospitals", "size": 0.40, "price_sensitivity": 0.8, "adoption_speed": 0.3},
            {"name": "Clinics", "size": 0.35, "price_sensitivity": 0.9, "adoption_speed": 0.4},
            {"name": "Consumers", "size": 0.25, "price_sensitivity": 0.7, "adoption_speed": 0.6}
        ],
        "trends": [
            "Telemedicine adoption",
            "Value-based care",
            "Patient engagement",
            "Regulatory compliance",
            "Cost containment"
        ],
        "barriers": [
            "Regulatory requirements",
            "Privacy concerns",
            "Reimbursement challenges",
            "Clinical workflow integration"
        ]
    },
    "financial": {
        "segments": [
            {"name": "Enterprise", "size": 0.30, "price_sensitivity": 0.6, "adoption_speed": 0.4},
            {"name": "SMB", "size": 0.45, "price_sensitivity": 0.8, "adoption_speed": 0.5},
            {"name": "Consumer", "size": 0.25, "price_sensitivity": 0.9, "adoption_speed": 0.7}
        ],
        "trends": [
            "Digital banking transformation",
            "Open banking initiatives",
            "Cryptocurrency adoption",
            "Robo-advisory services",
            "Regulatory technology"
        ],
        "barriers": [
            "Regulatory compliance",
            "Legacy system integration",
            "Security requirements",
            "Customer trust"
        ]
    }
}

COMPETITIVE_LANDSCAPE_TEMPLATES = {
    "fragmented": {
        "description": "Highly fragmented market with many small players",
        "competitive_intensity": 0.7,
        "typical_market_shares": [0.15, 0.12, 0.10, 0.08, 0.55],  # Top 4 + others
        "characteristics": [
            "Low barriers to entry",
            "Price competition",
            "Product differentiation opportunities",
            "Consolidation potential"
        ]
    },
    "concentrated": {
        "description": "Market dominated by few large players",
        "competitive_intensity": 0.9,
        "typical_market_shares": [0.40, 0.25, 0.20, 0.15],
        "characteristics": [
            "High barriers to entry",
            "Brand loyalty important",
            "Innovation focus",
            "Scale advantages"
        ]
    },
    "duopoly": {
        "description": "Market dominated by two major players",
        "competitive_intensity": 0.8,
        "typical_market_shares": [0.45, 0.35, 0.20],
        "characteristics": [
            "Head-to-head competition",
            "Feature parity pressure",
            "Marketing spend competition",
            "Customer switching costs"
        ]
    }
}


async def analyze_market_opportunity(
    market_name: str,
    industry: str,
    target_segments: List[str],
    product_category: str,
    geographic_scope: str = "domestic"
) -> MarketAnalysis:
    """
    Analyze market opportunity for a specific market.
    
    Args:
        market_name: Name of the market
        industry: Industry sector
        target_segments: Target customer segments
        product_category: Product category
        geographic_scope: Geographic scope
    
    Returns:
        MarketAnalysis object
    """
    # Get industry data
    industry_data = MARKET_RESEARCH_DATABASE.get(industry.lower(), {})
    
    # Calculate market size (simulated)
    base_market_size = 1000000000  # $1B base
    geographic_multiplier = 3.0 if geographic_scope == "global" else 1.0
    market_size = base_market_size * geographic_multiplier
    
    # Calculate growth rate
    growth_rates = {
        "technology": 0.15,
        "healthcare": 0.08,
        "financial": 0.10,
        "manufacturing": 0.05
    }
    growth_rate = growth_rates.get(industry.lower(), 0.07)
    
    # Determine market maturity
    maturity_mapping = {
        "emerging": MarketMaturity.EMERGING,
        "growth": MarketMaturity.GROWTH,
        "mature": MarketMaturity.MATURE,
        "declining": MarketMaturity.DECLINING
    }
    
    # Simple heuristic for maturity based on industry
    if industry.lower() in ["technology", "healthcare"]:
        maturity = MarketMaturity.GROWTH
    elif industry.lower() in ["financial", "manufacturing"]:
        maturity = MarketMaturity.MATURE
    else:
        maturity = MarketMaturity.GROWTH
    
    # Create customer profiles
    segments_data = industry_data.get("segments", [])
    customer_profiles = []
    
    for segment_data in segments_data:
        if segment_data["name"].lower() in [s.lower() for s in target_segments]:
            profile = CustomerProfile(
                segment=CustomerSegment.MAINSTREAM,  # Simplified
                size=int(market_size * segment_data["size"]),
                demographics={"age_range": "25-65", "income": "middle_to_high"},
                psychographics={"tech_savvy": True, "value_conscious": True},
                behavior_patterns={"online_research": True, "peer_recommendations": True},
                needs=[f"{product_category} functionality", "ease_of_use", "reliability"],
                pain_points=["high_cost", "complexity", "integration_challenges"],
                decision_criteria=["price", "features", "support", "reputation"],
                price_sensitivity=segment_data["price_sensitivity"],
                brand_loyalty=0.6,
                adoption_likelihood=segment_data["adoption_speed"]
            )
            customer_profiles.append(profile)
    
    # Generate market trends
    trends = industry_data.get("trends", [
        "Digital transformation",
        "Increased competition",
        "Customer experience focus",
        "Regulatory changes"
    ])
    
    # Generate barriers
    barriers = industry_data.get("barriers", [
        "High development costs",
        "Regulatory compliance",
        "Customer acquisition costs",
        "Technology complexity"
    ])
    
    return MarketAnalysis(
        market_name=market_name,
        market_size=market_size,
        market_growth_rate=growth_rate,
        market_maturity=maturity,
        key_trends=trends,
        growth_drivers=[
            "Technology advancement",
            "Changing customer needs",
            "Market expansion",
            "Regulatory support"
        ],
        barriers_to_entry=barriers,
        market_segments=customer_profiles,
        competitive_intensity=0.7
    )


async def analyze_competitors(
    industry: str,
    market_name: str,
    competitive_landscape: str = "fragmented"
) -> List[CompetitorAnalysis]:
    """
    Analyze competitors in the market.
    
    Args:
        industry: Industry sector
        market_name: Market name
        competitive_landscape: Type of competitive landscape
    
    Returns:
        List of CompetitorAnalysis objects
    """
    landscape_data = COMPETITIVE_LANDSCAPE_TEMPLATES.get(competitive_landscape, 
                                                        COMPETITIVE_LANDSCAPE_TEMPLATES["fragmented"])
    
    # Generate competitor profiles
    competitors = []
    competitor_names = [
        f"{industry.title()} Leader Corp",
        f"{industry.title()} Challenger Inc",
        f"{industry.title()} Innovator LLC",
        f"{industry.title()} Solutions Ltd"
    ]
    
    market_shares = landscape_data["typical_market_shares"]
    positions = [CompetitivePosition.LEADER, CompetitivePosition.CHALLENGER, 
                CompetitivePosition.FOLLOWER, CompetitivePosition.NICHE]
    
    for i, (name, share, position) in enumerate(zip(competitor_names, market_shares, positions)):
        competitor = CompetitorAnalysis(
            competitor_name=name,
            market_share=share,
            competitive_position=position,
            strengths=[
                "Strong brand recognition",
                "Extensive distribution network",
                "Technical expertise",
                "Customer relationships"
            ] if position == CompetitivePosition.LEADER else [
                "Innovative products",
                "Competitive pricing",
                "Agile operations",
                "Niche expertise"
            ],
            weaknesses=[
                "Legacy technology",
                "High cost structure",
                "Slow innovation",
                "Limited market reach"
            ] if position == CompetitivePosition.LEADER else [
                "Limited resources",
                "Brand recognition",
                "Market reach",
                "Technology gaps"
            ],
            products_services=[f"{industry.title()} Product {j+1}" for j in range(3)],
            pricing_strategy="Premium pricing" if position == CompetitivePosition.LEADER else "Competitive pricing",
            distribution_channels=["Direct sales", "Channel partners", "Online"],
            marketing_approach="Brand-focused" if position == CompetitivePosition.LEADER else "Product-focused",
            financial_performance={
                "revenue_growth": 0.1 if position == CompetitivePosition.LEADER else 0.15,
                "market_share_trend": 0.02 if position == CompetitivePosition.LEADER else -0.01,
                "profitability": 0.15 if position == CompetitivePosition.LEADER else 0.08
            },
            strategic_focus="Market expansion" if position == CompetitivePosition.LEADER else "Product innovation"
        )
        competitors.append(competitor)
    
    return competitors


async def map_customer_journey(
    product_type: str,
    customer_segment: str,
    sales_cycle_length: str = "medium"
) -> List[CustomerJourney]:
    """
    Map customer journey for a specific product and segment.
    
    Args:
        product_type: Type of product
        customer_segment: Customer segment
        sales_cycle_length: Length of sales cycle
    
    Returns:
        List of CustomerJourney objects
    """
    # Base conversion rates by sales cycle length
    conversion_rates = {
        "short": [0.8, 0.6, 0.4, 0.7, 0.9, 0.8],
        "medium": [0.6, 0.4, 0.3, 0.6, 0.8, 0.7],
        "long": [0.4, 0.3, 0.2, 0.5, 0.7, 0.6]
    }
    
    base_rates = conversion_rates.get(sales_cycle_length, conversion_rates["medium"])
    
    journey_stages = [
        {
            "stage": AdoptionStage.AWARENESS,
            "touchpoints": ["Website", "Social media", "Advertising", "Word of mouth"],
            "actions": ["Research problem", "Identify solutions", "Compare options"],
            "emotions": ["Curious", "Overwhelmed", "Hopeful"],
            "pain_points": ["Information overload", "Unclear differentiation", "Time constraints"],
            "opportunities": ["Educational content", "Clear value proposition", "Simplified messaging"],
            "metrics": ["Brand awareness", "Website traffic", "Content engagement"]
        },
        {
            "stage": AdoptionStage.CONSIDERATION,
            "touchpoints": ["Product demos", "Sales calls", "Documentation", "Reviews"],
            "actions": ["Evaluate features", "Compare pricing", "Check references"],
            "emotions": ["Analytical", "Skeptical", "Interested"],
            "pain_points": ["Feature complexity", "Pricing concerns", "Integration questions"],
            "opportunities": ["Product trials", "ROI calculators", "Customer testimonials"],
            "metrics": ["Demo requests", "Pricing inquiries", "Sales qualified leads"]
        },
        {
            "stage": AdoptionStage.TRIAL,
            "touchpoints": ["Free trial", "Pilot program", "Support team", "Documentation"],
            "actions": ["Test functionality", "Evaluate fit", "Assess implementation"],
            "emotions": ["Excited", "Cautious", "Evaluative"],
            "pain_points": ["Setup complexity", "Learning curve", "Integration issues"],
            "opportunities": ["Onboarding support", "Success metrics", "Quick wins"],
            "metrics": ["Trial signups", "Feature usage", "Time to value"]
        },
        {
            "stage": AdoptionStage.ADOPTION,
            "touchpoints": ["Purchase process", "Implementation team", "Training", "Support"],
            "actions": ["Make purchase", "Implement solution", "Train users"],
            "emotions": ["Committed", "Anxious", "Optimistic"],
            "pain_points": ["Implementation delays", "User resistance", "Technical issues"],
            "opportunities": ["Smooth onboarding", "Change management", "Success milestones"],
            "metrics": ["Conversion rate", "Time to implement", "User adoption"]
        },
        {
            "stage": AdoptionStage.RETENTION,
            "touchpoints": ["Customer success", "Support", "Product updates", "Community"],
            "actions": ["Use product", "Optimize usage", "Provide feedback"],
            "emotions": ["Satisfied", "Engaged", "Loyal"],
            "pain_points": ["Feature gaps", "Performance issues", "Support delays"],
            "opportunities": ["Feature development", "Usage optimization", "Community building"],
            "metrics": ["Usage metrics", "Customer satisfaction", "Retention rate"]
        },
        {
            "stage": AdoptionStage.ADVOCACY,
            "touchpoints": ["Referral program", "Case studies", "Events", "Reviews"],
            "actions": ["Recommend product", "Share experiences", "Provide references"],
            "emotions": ["Enthusiastic", "Proud", "Helpful"],
            "pain_points": ["Referral complexity", "Incentive clarity", "Time investment"],
            "opportunities": ["Referral programs", "Success stories", "Community leadership"],
            "metrics": ["Net Promoter Score", "Referrals", "Case studies"]
        }
    ]
    
    journey = []
    for i, stage_data in enumerate(journey_stages):
        stage = CustomerJourney(
            stage=stage_data["stage"],
            touchpoints=stage_data["touchpoints"],
            customer_actions=stage_data["actions"],
            emotions=stage_data["emotions"],
            pain_points=stage_data["pain_points"],
            opportunities=stage_data["opportunities"],
            success_metrics=stage_data["metrics"],
            conversion_rate=base_rates[i] if i < len(base_rates) else 0.5
        )
        journey.append(stage)
    
    return journey


async def analyze_customer_feedback(
    feedback_data: List[Dict[str, Any]],
    feedback_source: str = "survey"
) -> List[CustomerFeedback]:
    """
    Analyze customer feedback data.
    
    Args:
        feedback_data: List of feedback data dictionaries
        feedback_source: Source of feedback
    
    Returns:
        List of CustomerFeedback objects
    """
    feedback_analyses = []
    
    # Simulate feedback analysis
    feedback_types = ["product_feedback", "service_feedback", "feature_request", "complaint"]
    
    for i, data in enumerate(feedback_data):
        # Simulate sentiment analysis
        sentiment_score = random.uniform(-0.5, 0.8)  # Slightly positive bias
        
        # Simulate satisfaction scoring
        satisfaction_score = max(1.0, min(5.0, 3.0 + sentiment_score * 2))
        
        # Simulate NPS scoring
        nps_score = max(0.0, min(10.0, 6.0 + sentiment_score * 4))
        
        # Generate key themes
        themes = [
            "Product quality",
            "Customer service",
            "Pricing",
            "Features",
            "Usability"
        ]
        
        # Generate feedback items
        feature_requests = [
            "Mobile app improvement",
            "Integration capabilities",
            "Reporting features",
            "User interface updates"
        ]
        
        complaints = [
            "Slow response times",
            "Limited customization",
            "Integration issues",
            "Pricing concerns"
        ]
        
        suggestions = [
            "Improve onboarding process",
            "Add more tutorials",
            "Enhance customer support",
            "Expand feature set"
        ]
        
        feedback = CustomerFeedback(
            feedback_source=feedback_source,
            feedback_type=random.choice(feedback_types),
            sentiment_score=sentiment_score,
            key_themes=random.sample(themes, 3),
            satisfaction_score=satisfaction_score,
            recommendation_score=nps_score,
            feature_requests=random.sample(feature_requests, 2),
            complaints=random.sample(complaints, 2),
            suggestions=random.sample(suggestions, 2)
        )
        
        feedback_analyses.append(feedback)
    
    return feedback_analyses


# Alias for backward compatibility
analyze_customer_behavior = analyze_customer_feedback


async def perform_comprehensive_market_research(
    research_objective: str,
    market_name: str,
    industry: str,
    target_segments: List[str],
    product_category: str,
    geographic_scope: str = "domestic",
    competitive_landscape: str = "fragmented"
) -> MarketResearchReport:
    """
    Perform comprehensive market research analysis.
    
    Args:
        research_objective: Research objective
        market_name: Market name
        industry: Industry sector
        target_segments: Target customer segments
        product_category: Product category
        geographic_scope: Geographic scope
        competitive_landscape: Competitive landscape type
    
    Returns:
        MarketResearchReport object
    """
    # Conduct market analysis
    market_analysis = await analyze_market_opportunity(
        market_name, industry, target_segments, product_category, geographic_scope
    )
    
    # Analyze competitors
    competitor_analyses = await analyze_competitors(industry, market_name, competitive_landscape)
    
    # Map customer journey
    customer_journey = await map_customer_journey(product_category, target_segments[0] if target_segments else "mainstream")
    
    # Simulate customer feedback
    feedback_data = [{"rating": random.randint(1, 5)} for _ in range(10)]
    customer_feedback = await analyze_customer_feedback(feedback_data)
    
    # Assess market opportunity
    market_opportunity = {
        "total_addressable_market": market_analysis.market_size,
        "serviceable_addressable_market": market_analysis.market_size * 0.3,
        "serviceable_obtainable_market": market_analysis.market_size * 0.05,
        "market_penetration_potential": 0.15,
        "revenue_potential": market_analysis.market_size * 0.05 * 0.15,
        "time_to_market": "12-18 months",
        "investment_required": market_analysis.market_size * 0.001
    }
    
    # Generate recommendations
    recommendations = [
        "Focus on early adopter segment for initial market entry",
        "Develop competitive differentiation strategy",
        "Invest in customer education and onboarding",
        "Build strategic partnerships for market access",
        "Implement customer feedback collection system",
        "Monitor competitive landscape continuously"
    ]
    
    # Add industry-specific recommendations
    if industry.lower() == "technology":
        recommendations.append("Prioritize security and scalability features")
    elif industry.lower() == "healthcare":
        recommendations.append("Ensure regulatory compliance and clinical validation")
    elif industry.lower() == "financial":
        recommendations.append("Focus on trust-building and regulatory compliance")
    
    return MarketResearchReport(
        report_id=f"market_research_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        research_objective=research_objective,
        market_analysis=market_analysis,
        competitor_analyses=competitor_analyses,
        customer_profiles=market_analysis.market_segments,
        customer_journey=customer_journey,
        customer_feedback=customer_feedback,
        market_opportunity=market_opportunity,
        recommendations=recommendations,
        research_limitations=[
            "Limited primary research data",
            "Market dynamics may change rapidly",
            "Competitive landscape is dynamic",
            "Customer preferences may evolve"
        ],
        methodology="Secondary research analysis with market modeling"
    )