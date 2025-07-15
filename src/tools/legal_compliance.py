"""
Legal compliance and risk assessment tools for the Legal Agent.

Contains tools for regulatory compliance checking, legal risk assessment,
and contract analysis.
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
from pydantic import BaseModel, Field, validator


class RiskSeverity(str, Enum):
    """Legal risk severity levels."""
    
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ComplianceStatus(str, Enum):
    """Compliance status levels."""
    
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    REQUIRES_REVIEW = "requires_review"
    UNKNOWN = "unknown"


class LegalRisk(BaseModel):
    """Legal risk assessment result."""
    
    risk_id: str = Field(..., description="Unique risk identifier")
    category: str = Field(..., description="Risk category")
    description: str = Field(..., min_length=10, max_length=500)
    severity: RiskSeverity
    probability: float = Field(..., ge=0.0, le=1.0)
    potential_impact: str = Field(..., description="Description of potential impact")
    regulatory_basis: List[str] = Field(default_factory=list)
    mitigation_strategies: List[str] = Field(default_factory=list)
    estimated_cost: Optional[float] = Field(None, description="Estimated cost of risk")
    timeline: Optional[str] = Field(None, description="Risk timeline")
    responsible_party: Optional[str] = Field(None)
    
    @validator('risk_id')
    def validate_risk_id(cls, v: str) -> str:
        """Ensure risk ID is meaningful."""
        if not v.strip():
            raise ValueError("Risk ID cannot be empty")
        return v.strip()


class ComplianceRequirement(BaseModel):
    """Compliance requirement definition."""
    
    requirement_id: str = Field(..., description="Unique requirement identifier")
    regulation: str = Field(..., description="Relevant regulation or law")
    description: str = Field(..., min_length=10, max_length=1000)
    jurisdiction: str = Field(..., description="Legal jurisdiction")
    compliance_status: ComplianceStatus
    deadline: Optional[datetime] = Field(None, description="Compliance deadline")
    penalties: List[str] = Field(default_factory=list)
    implementation_steps: List[str] = Field(default_factory=list)
    estimated_cost: Optional[float] = Field(None)
    responsible_party: Optional[str] = Field(None)
    
    @validator('requirement_id')
    def validate_requirement_id(cls, v: str) -> str:
        """Ensure requirement ID is meaningful."""
        if not v.strip():
            raise ValueError("Requirement ID cannot be empty")
        return v.strip()


class ContractRisk(BaseModel):
    """Contract-related risk assessment."""
    
    contract_type: str = Field(..., description="Type of contract")
    risk_description: str = Field(..., min_length=10, max_length=500)
    severity: RiskSeverity
    affected_clauses: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    alternative_approaches: List[str] = Field(default_factory=list)
    negotiation_points: List[str] = Field(default_factory=list)
    
    @validator('contract_type')
    def validate_contract_type(cls, v: str) -> str:
        """Ensure contract type is meaningful."""
        if not v.strip():
            raise ValueError("Contract type cannot be empty")
        return v.strip()


class LegalAssessment(BaseModel):
    """Comprehensive legal assessment result."""
    
    assessment_id: str = Field(..., description="Unique assessment identifier")
    decision_context: str = Field(..., description="Decision being assessed")
    legal_risks: List[LegalRisk] = Field(default_factory=list)
    compliance_requirements: List[ComplianceRequirement] = Field(default_factory=list)
    contract_risks: List[ContractRisk] = Field(default_factory=list)
    overall_risk_score: float = Field(..., ge=0.0, le=1.0)
    recommendations: List[str] = Field(default_factory=list)
    next_actions: List[str] = Field(default_factory=list)
    estimated_total_cost: Optional[float] = Field(None)
    assessment_date: datetime = Field(default_factory=datetime.now)
    
    @validator('assessment_id')
    def validate_assessment_id(cls, v: str) -> str:
        """Ensure assessment ID is meaningful."""
        if not v.strip():
            raise ValueError("Assessment ID cannot be empty")
        return v.strip()


# Simulated regulatory databases and compliance frameworks
REGULATORY_FRAMEWORKS = {
    "gdpr": {
        "name": "General Data Protection Regulation",
        "jurisdiction": "European Union",
        "scope": "Data protection and privacy",
        "key_requirements": [
            "Data protection by design and default",
            "Lawful basis for processing",
            "Data subject rights",
            "Data breach notification",
            "Privacy impact assessments"
        ],
        "penalties": ["Up to €20 million or 4% of annual global turnover"],
        "compliance_deadline": "2018-05-25"
    },
    "ccpa": {
        "name": "California Consumer Privacy Act",
        "jurisdiction": "California, USA",
        "scope": "Consumer privacy rights",
        "key_requirements": [
            "Consumer right to know",
            "Consumer right to delete",
            "Consumer right to opt-out",
            "Non-discrimination provisions"
        ],
        "penalties": ["Up to $7,500 per violation"],
        "compliance_deadline": "2020-01-01"
    },
    "sox": {
        "name": "Sarbanes-Oxley Act",
        "jurisdiction": "United States",
        "scope": "Corporate governance and financial reporting",
        "key_requirements": [
            "Internal controls over financial reporting",
            "CEO/CFO certifications",
            "Independent auditor oversight",
            "Corporate responsibility"
        ],
        "penalties": ["Up to $5 million fine and 20 years imprisonment"],
        "compliance_deadline": "2002-07-30"
    },
    "hipaa": {
        "name": "Health Insurance Portability and Accountability Act",
        "jurisdiction": "United States",
        "scope": "Healthcare information protection",
        "key_requirements": [
            "Administrative safeguards",
            "Physical safeguards",
            "Technical safeguards",
            "Breach notification"
        ],
        "penalties": ["Up to $1.5 million per violation"],
        "compliance_deadline": "2003-04-14"
    }
}

INDUSTRY_SPECIFIC_REGULATIONS = {
    "financial_services": [
        "Basel III capital requirements",
        "Dodd-Frank Act compliance",
        "MiFID II regulations",
        "PCI DSS standards",
        "Anti-money laundering (AML) requirements"
    ],
    "healthcare": [
        "HIPAA compliance",
        "FDA regulations",
        "Clinical trial regulations",
        "Medical device regulations",
        "Pharmaceutical regulations"
    ],
    "technology": [
        "GDPR compliance",
        "CCPA compliance",
        "Cybersecurity regulations",
        "Intellectual property laws",
        "Software licensing requirements"
    ],
    "manufacturing": [
        "Environmental regulations",
        "Safety standards (OSHA)",
        "Product liability laws",
        "Import/export regulations",
        "Quality standards (ISO)"
    ]
}

CONTRACT_RISK_PATTERNS = {
    "liability_caps": {
        "description": "Inadequate liability limitation clauses",
        "severity": RiskSeverity.HIGH,
        "recommendations": [
            "Include mutual liability caps",
            "Exclude gross negligence and willful misconduct",
            "Consider insurance requirements"
        ]
    },
    "indemnification": {
        "description": "Broad indemnification obligations",
        "severity": RiskSeverity.HIGH,
        "recommendations": [
            "Limit indemnification scope",
            "Include knowledge qualifiers",
            "Add reciprocal indemnification"
        ]
    },
    "termination_rights": {
        "description": "Unfavorable termination provisions",
        "severity": RiskSeverity.MEDIUM,
        "recommendations": [
            "Include termination for convenience",
            "Define material breach clearly",
            "Add appropriate cure periods"
        ]
    },
    "ip_ownership": {
        "description": "Unclear intellectual property ownership",
        "severity": RiskSeverity.CRITICAL,
        "recommendations": [
            "Clearly define IP ownership",
            "Include work-for-hire provisions",
            "Address derivative works"
        ]
    }
}


async def assess_regulatory_compliance(
    decision_context: str,
    industry: str,
    jurisdiction: str,
    business_activities: List[str]
) -> List[ComplianceRequirement]:
    """
    Assess regulatory compliance requirements for a business decision.
    
    Args:
        decision_context: Description of the decision being made
        industry: Industry sector
        jurisdiction: Legal jurisdiction
        business_activities: List of business activities involved
    
    Returns:
        List of ComplianceRequirement objects
    """
    requirements = []
    
    # Check general regulations
    for reg_code, reg_info in REGULATORY_FRAMEWORKS.items():
        if (jurisdiction.lower() in reg_info["jurisdiction"].lower() or
            reg_info["jurisdiction"].lower() in jurisdiction.lower()):
            
            for req_desc in reg_info["key_requirements"]:
                requirement = ComplianceRequirement(
                    requirement_id=f"{reg_code}_{len(requirements)+1}",
                    regulation=reg_info["name"],
                    description=req_desc,
                    jurisdiction=reg_info["jurisdiction"],
                    compliance_status=ComplianceStatus.REQUIRES_REVIEW,
                    penalties=reg_info["penalties"],
                    implementation_steps=[
                        "Conduct compliance gap analysis",
                        "Develop implementation plan",
                        "Train relevant personnel",
                        "Implement monitoring procedures"
                    ]
                )
                requirements.append(requirement)
    
    # Check industry-specific regulations
    if industry.lower() in INDUSTRY_SPECIFIC_REGULATIONS:
        for reg_name in INDUSTRY_SPECIFIC_REGULATIONS[industry.lower()]:
            requirement = ComplianceRequirement(
                requirement_id=f"{industry}_{len(requirements)+1}",
                regulation=reg_name,
                description=f"Compliance with {reg_name} requirements",
                jurisdiction=jurisdiction,
                compliance_status=ComplianceStatus.REQUIRES_REVIEW,
                implementation_steps=[
                    "Review specific regulatory requirements",
                    "Assess current compliance status",
                    "Develop remediation plan if needed"
                ]
            )
            requirements.append(requirement)
    
    return requirements


async def identify_legal_risks(
    decision_type: str,
    business_model: str,
    stakeholders: List[str],
    geographic_scope: str
) -> List[LegalRisk]:
    """
    Identify potential legal risks for a business decision.
    
    Args:
        decision_type: Type of decision (e.g., "pricing", "market_entry")
        business_model: Description of business model
        stakeholders: List of stakeholders affected
        geographic_scope: Geographic scope of the decision
    
    Returns:
        List of LegalRisk objects
    """
    risks = []
    
    # Common legal risks by decision type
    risk_templates = {
        "pricing": [
            {
                "category": "Antitrust",
                "description": "Price fixing or anti-competitive pricing practices",
                "severity": RiskSeverity.HIGH,
                "probability": 0.3,
                "regulatory_basis": ["Sherman Act", "Clayton Act", "Competition law"],
                "mitigation_strategies": [
                    "Conduct antitrust compliance review",
                    "Document independent pricing decisions",
                    "Avoid coordination with competitors"
                ]
            },
            {
                "category": "Consumer Protection",
                "description": "Deceptive pricing practices or hidden fees",
                "severity": RiskSeverity.MEDIUM,
                "probability": 0.4,
                "regulatory_basis": ["Consumer protection laws", "Truth in advertising"],
                "mitigation_strategies": [
                    "Ensure transparent pricing disclosure",
                    "Review marketing materials for accuracy",
                    "Implement clear terms and conditions"
                ]
            }
        ],
        "market_entry": [
            {
                "category": "Regulatory Compliance",
                "description": "Non-compliance with local market regulations",
                "severity": RiskSeverity.CRITICAL,
                "probability": 0.6,
                "regulatory_basis": ["Local business laws", "Industry regulations"],
                "mitigation_strategies": [
                    "Conduct thorough regulatory review",
                    "Engage local legal counsel",
                    "Obtain necessary licenses and permits"
                ]
            },
            {
                "category": "Intellectual Property",
                "description": "IP infringement in new market",
                "severity": RiskSeverity.HIGH,
                "probability": 0.4,
                "regulatory_basis": ["Patent law", "Trademark law", "Copyright law"],
                "mitigation_strategies": [
                    "Conduct IP clearance search",
                    "File defensive IP applications",
                    "Monitor for potential infringement"
                ]
            }
        ]
    }
    
    # Generate risks based on decision type
    if decision_type.lower() in risk_templates:
        for i, risk_template in enumerate(risk_templates[decision_type.lower()]):
            risk = LegalRisk(
                risk_id=f"{decision_type}_{i+1}",
                category=risk_template["category"],
                description=risk_template["description"],
                severity=risk_template["severity"],
                probability=risk_template["probability"],
                potential_impact=f"Legal liability, regulatory penalties, business disruption",
                regulatory_basis=risk_template["regulatory_basis"],
                mitigation_strategies=risk_template["mitigation_strategies"],
                timeline="Immediate to 12 months"
            )
            risks.append(risk)
    
    # Add geographic-specific risks
    if "international" in geographic_scope.lower() or "global" in geographic_scope.lower():
        international_risk = LegalRisk(
            risk_id="international_1",
            category="International Compliance",
            description="Cross-border regulatory compliance challenges",
            severity=RiskSeverity.HIGH,
            probability=0.7,
            potential_impact="Regulatory violations, market access restrictions",
            regulatory_basis=["International trade laws", "Local regulations"],
            mitigation_strategies=[
                "Engage local legal counsel in each jurisdiction",
                "Develop compliance monitoring systems",
                "Establish local legal entities if required"
            ],
            timeline="3-6 months"
        )
        risks.append(international_risk)
    
    return risks


async def assess_contract_risks(
    contract_type: str,
    contract_terms: Dict[str, Any],
    counterparty_profile: str
) -> List[ContractRisk]:
    """
    Assess risks in contract terms and structure.
    
    Args:
        contract_type: Type of contract (e.g., "service_agreement", "license")
        contract_terms: Dictionary of contract terms
        counterparty_profile: Description of counterparty
    
    Returns:
        List of ContractRisk objects
    """
    risks = []
    
    # Check for common contract risk patterns
    for pattern_name, pattern_info in CONTRACT_RISK_PATTERNS.items():
        # Simulate risk detection based on contract type and terms
        if (pattern_name in str(contract_terms).lower() or
            pattern_name.replace("_", " ") in contract_type.lower()):
            
            risk = ContractRisk(
                contract_type=contract_type,
                risk_description=pattern_info["description"],
                severity=pattern_info["severity"],
                affected_clauses=[pattern_name.replace("_", " ").title()],
                recommendations=pattern_info["recommendations"],
                alternative_approaches=[
                    "Consider alternative contract structure",
                    "Negotiate more balanced terms",
                    "Include protective provisions"
                ],
                negotiation_points=[
                    f"Negotiate {pattern_name.replace('_', ' ')} terms",
                    "Request reciprocal provisions",
                    "Include carve-out exceptions"
                ]
            )
            risks.append(risk)
    
    # Add counterparty-specific risks
    if "startup" in counterparty_profile.lower() or "early stage" in counterparty_profile.lower():
        counterparty_risk = ContractRisk(
            contract_type=contract_type,
            risk_description="Counterparty financial stability and performance risk",
            severity=RiskSeverity.MEDIUM,
            affected_clauses=["Performance obligations", "Payment terms"],
            recommendations=[
                "Require parent company guarantee",
                "Include financial reporting requirements",
                "Consider shorter contract terms"
            ],
            alternative_approaches=[
                "Staged performance milestones",
                "Escrow arrangements",
                "Performance bonds"
            ],
            negotiation_points=[
                "Financial guarantees",
                "Performance security",
                "Termination rights"
            ]
        )
        risks.append(counterparty_risk)
    
    return risks


async def calculate_legal_risk_score(risks: List[LegalRisk]) -> float:
    """
    Calculate overall legal risk score.
    
    Args:
        risks: List of LegalRisk objects
    
    Returns:
        Risk score between 0.0 and 1.0
    """
    if not risks:
        return 0.0
    
    severity_weights = {
        RiskSeverity.LOW: 0.25,
        RiskSeverity.MEDIUM: 0.5,
        RiskSeverity.HIGH: 0.75,
        RiskSeverity.CRITICAL: 1.0
    }
    
    weighted_score = 0.0
    for risk in risks:
        risk_score = severity_weights[risk.severity] * risk.probability
        weighted_score += risk_score
    
    # Normalize to 0-1 scale
    return min(weighted_score / len(risks), 1.0)


async def generate_legal_recommendations(
    risks: List[LegalRisk],
    compliance_requirements: List[ComplianceRequirement],
    contract_risks: List[ContractRisk]
) -> List[str]:
    """
    Generate comprehensive legal recommendations.
    
    Args:
        risks: List of legal risks
        compliance_requirements: List of compliance requirements
        contract_risks: List of contract risks
    
    Returns:
        List of recommendation strings
    """
    recommendations = []
    
    # Risk-based recommendations
    critical_risks = [r for r in risks if r.severity == RiskSeverity.CRITICAL]
    if critical_risks:
        recommendations.append("Immediate action required for critical legal risks")
        for risk in critical_risks:
            recommendations.extend(risk.mitigation_strategies)
    
    # Compliance recommendations
    non_compliant = [r for r in compliance_requirements if r.compliance_status == ComplianceStatus.NON_COMPLIANT]
    if non_compliant:
        recommendations.append("Address non-compliant regulatory requirements immediately")
    
    requires_review = [r for r in compliance_requirements if r.compliance_status == ComplianceStatus.REQUIRES_REVIEW]
    if requires_review:
        recommendations.append("Conduct compliance review for uncertain requirements")
    
    # Contract recommendations
    high_severity_contract_risks = [r for r in contract_risks if r.severity in [RiskSeverity.HIGH, RiskSeverity.CRITICAL]]
    if high_severity_contract_risks:
        recommendations.append("Review and revise contract terms to address high-severity risks")
    
    # General recommendations
    recommendations.extend([
        "Engage qualified legal counsel for decision implementation",
        "Establish ongoing compliance monitoring procedures",
        "Document legal analysis and decision rationale",
        "Consider insurance coverage for identified risks"
    ])
    
    return list(set(recommendations))  # Remove duplicates


async def perform_comprehensive_legal_assessment(
    decision_context: str,
    decision_type: str,
    industry: str,
    jurisdiction: str,
    business_activities: List[str],
    contract_details: Optional[Dict[str, Any]] = None
) -> LegalAssessment:
    """
    Perform comprehensive legal assessment for a business decision.
    
    Args:
        decision_context: Description of the decision
        decision_type: Type of decision
        industry: Industry sector
        jurisdiction: Legal jurisdiction
        business_activities: List of business activities
        contract_details: Optional contract details
    
    Returns:
        LegalAssessment object
    """
    # Assess compliance requirements
    compliance_requirements = await assess_regulatory_compliance(
        decision_context, industry, jurisdiction, business_activities
    )
    
    # Identify legal risks
    legal_risks = await identify_legal_risks(
        decision_type, industry, business_activities, jurisdiction
    )
    
    # Assess contract risks if applicable
    contract_risks = []
    if contract_details:
        contract_risks = await assess_contract_risks(
            contract_details.get("type", "general"),
            contract_details.get("terms", {}),
            contract_details.get("counterparty", "unknown")
        )
    
    # Calculate overall risk score
    overall_risk_score = await calculate_legal_risk_score(legal_risks)
    
    # Generate recommendations
    recommendations = await generate_legal_recommendations(
        legal_risks, compliance_requirements, contract_risks
    )
    
    # Generate next actions
    next_actions = [
        "Engage legal counsel for detailed review",
        "Conduct regulatory compliance audit",
        "Develop risk mitigation implementation plan",
        "Establish legal monitoring and reporting procedures"
    ]
    
    return LegalAssessment(
        assessment_id=f"legal_assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        decision_context=decision_context,
        legal_risks=legal_risks,
        compliance_requirements=compliance_requirements,
        contract_risks=contract_risks,
        overall_risk_score=overall_risk_score,
        recommendations=recommendations,
        next_actions=next_actions
    )