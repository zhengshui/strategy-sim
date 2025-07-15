"""
Legal Agent implementation for StrategySim AI.

Provides conservative legal analysis, regulatory compliance assessment,
and risk mitigation recommendations.
"""

from typing import Any, Dict, List, Optional
import logging

from autogen_core.models import ChatCompletionClient

from .base_agent import BaseStrategicAgent
from ..models.agent_models import AgentRole
from ..tools.legal_compliance import (
    assess_regulatory_compliance,
    identify_legal_risks,
    assess_contract_risks,
    calculate_legal_risk_score,
    generate_legal_recommendations,
    perform_comprehensive_legal_assessment
)

logger = logging.getLogger(__name__)


class LegalAgent(BaseStrategicAgent):
    """
    Legal Agent for conservative legal analysis and compliance assessment.
    
    Focuses on:
    - Regulatory compliance and legal risks
    - Contract analysis and risk mitigation
    - Legal implications of strategic decisions
    - Conservative risk assessment and prevention
    """
    
    def __init__(
        self,
        agent_name: str = "legal_officer",
        model_client: ChatCompletionClient = None,
        custom_tools: Optional[List[Any]] = None
    ):
        """
        Initialize the Legal Agent.
        
        Args:
            agent_name: Name of the agent
            model_client: Model client for LLM communication
            custom_tools: Additional custom tools
        """
        # Get specialized tools
        specialized_tools = self.get_specialized_tools()
        
        # Add custom tools if provided
        if custom_tools:
            specialized_tools.extend(custom_tools)
        
        super().__init__(
            agent_name=agent_name,
            agent_role=AgentRole.LEGAL,
            model_client=model_client,
            tools=specialized_tools
        )
        
        logger.info(f"Initialized LegalAgent: {agent_name}")
    
    def get_specialized_tools(self) -> List[Any]:
        """
        Get tools specific to legal analysis.
        
        Returns:
            List of legal analysis tools
        """
        return [
            assess_regulatory_compliance,
            identify_legal_risks,
            assess_contract_risks,
            calculate_legal_risk_score,
            generate_legal_recommendations,
            perform_comprehensive_legal_assessment
        ]
    
    async def perform_specialized_analysis(
        self,
        decision_context: str,
        decision_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Perform legal analysis specific to legal officer perspective.
        
        Args:
            decision_context: Context of the decision
            decision_data: Decision data including legal considerations
        
        Returns:
            Dictionary with legal analysis results
        """
        try:
            analysis_results = {}
            
            # Extract legal-relevant data
            legal_data = decision_data.get("legal_data", {})
            business_data = decision_data.get("business_data", {})
            
            # Perform comprehensive legal assessment
            legal_assessment = await self._execute_tool(
                "perform_comprehensive_legal_assessment",
                decision_context=decision_context,
                decision_type=decision_data.get("decision_type", "general"),
                industry=business_data.get("industry", "technology"),
                jurisdiction=legal_data.get("jurisdiction", "United States"),
                business_activities=business_data.get("activities", ["product_development", "sales"]),
                contract_details=legal_data.get("contract_details")
            )
            
            analysis_results["legal_assessment"] = legal_assessment
            
            # Assess regulatory compliance
            compliance_assessment = await self._execute_tool(
                "assess_regulatory_compliance",
                decision_context=decision_context,
                industry=business_data.get("industry", "technology"),
                jurisdiction=legal_data.get("jurisdiction", "United States"),
                business_activities=business_data.get("activities", ["product_development", "sales"])
            )
            
            analysis_results["compliance_assessment"] = compliance_assessment
            
            # Identify legal risks
            legal_risks = await self._execute_tool(
                "identify_legal_risks",
                decision_type=decision_data.get("decision_type", "general"),
                business_model=business_data.get("business_model", "technology product"),
                stakeholders=decision_data.get("stakeholders", ["customers", "employees", "partners"]),
                geographic_scope=legal_data.get("geographic_scope", "domestic")
            )
            
            analysis_results["legal_risks"] = legal_risks
            
            # Assess contract risks if applicable
            if "contract_details" in legal_data:
                contract_risks = await self._execute_tool(
                    "assess_contract_risks",
                    contract_type=legal_data["contract_details"].get("type", "service_agreement"),
                    contract_terms=legal_data["contract_details"].get("terms", {}),
                    counterparty_profile=legal_data["contract_details"].get("counterparty", "unknown")
                )
                analysis_results["contract_risks"] = contract_risks
            
            # Calculate overall legal risk score
            if legal_risks.success and legal_risks.result:
                risk_score = await self._execute_tool(
                    "calculate_legal_risk_score",
                    risks=legal_risks.result
                )
                analysis_results["legal_risk_score"] = risk_score
            
            # Generate legal recommendations
            legal_recommendations = await self._generate_legal_recommendations(
                decision_context, analysis_results
            )
            analysis_results["legal_recommendations"] = legal_recommendations
            
            return analysis_results
            
        except Exception as e:
            logger.error(f"Specialized analysis failed for {self.agent_name}: {e}")
            raise
    
    async def _generate_legal_recommendations(
        self,
        decision_context: str,
        analysis_results: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generate legal recommendations based on analysis results.
        
        Args:
            decision_context: Context of the decision
            analysis_results: Results from legal analysis
        
        Returns:
            List of legal recommendations
        """
        recommendations = []
        
        # Legal assessment recommendations
        if "legal_assessment" in analysis_results:
            assessment_result = analysis_results["legal_assessment"]
            if assessment_result.success:
                assessment_data = assessment_result.result
                
                # High-level legal recommendations
                if hasattr(assessment_data, 'overall_risk_score') and assessment_data.overall_risk_score > 0.7:
                    recommendations.append({
                        "type": "high_legal_risk_warning",
                        "reasoning": f"High legal risk score of {assessment_data.overall_risk_score:.2f} requires immediate attention",
                        "confidence": 0.9,
                        "priority": "critical",
                        "actions": [
                            "Engage external legal counsel immediately",
                            "Conduct comprehensive legal risk assessment",
                            "Develop risk mitigation strategies"
                        ]
                    })
                
                if hasattr(assessment_data, 'legal_risks'):
                    for risk in assessment_data.legal_risks:
                        if hasattr(risk, 'severity') and risk.severity in ["high", "critical"]:
                            recommendations.append({
                                "type": "specific_legal_risk",
                                "reasoning": f"Critical legal risk identified: {risk.description}",
                                "confidence": 0.8,
                                "priority": "high",
                                "actions": risk.mitigation_strategies if hasattr(risk, 'mitigation_strategies') else []
                            })
        
        # Compliance recommendations
        if "compliance_assessment" in analysis_results:
            compliance_result = analysis_results["compliance_assessment"]
            if compliance_result.success:
                compliance_data = compliance_result.result
                
                # Check for non-compliant requirements
                if isinstance(compliance_data, list):
                    for requirement in compliance_data:
                        if hasattr(requirement, 'compliance_status') and requirement.compliance_status == "non_compliant":
                            recommendations.append({
                                "type": "compliance_violation",
                                "reasoning": f"Non-compliant with {requirement.regulation}",
                                "confidence": 0.9,
                                "priority": "critical",
                                "actions": [
                                    "Immediate compliance remediation required",
                                    "Review regulatory requirements",
                                    "Implement compliance measures"
                                ]
                            })
                        elif hasattr(requirement, 'compliance_status') and requirement.compliance_status == "requires_review":
                            recommendations.append({
                                "type": "compliance_review_needed",
                                "reasoning": f"Compliance review needed for {requirement.regulation}",
                                "confidence": 0.7,
                                "priority": "medium",
                                "actions": [
                                    "Conduct compliance assessment",
                                    "Engage regulatory experts",
                                    "Document compliance status"
                                ]
                            })
        
        # Risk-based recommendations
        if "legal_risks" in analysis_results:
            risks_result = analysis_results["legal_risks"]
            if risks_result.success and risks_result.result:
                risks = risks_result.result
                
                # Count critical risks
                critical_risks = [r for r in risks if hasattr(r, 'severity') and r.severity == "critical"]
                if critical_risks:
                    recommendations.append({
                        "type": "multiple_critical_risks",
                        "reasoning": f"Multiple critical legal risks identified ({len(critical_risks)} risks)",
                        "confidence": 0.8,
                        "priority": "critical",
                        "actions": [
                            "Pause decision until risks are mitigated",
                            "Engage specialized legal counsel",
                            "Develop comprehensive risk management plan"
                        ]
                    })
                
                # High probability risks
                high_prob_risks = [r for r in risks if hasattr(r, 'probability') and r.probability > 0.7]
                if high_prob_risks:
                    recommendations.append({
                        "type": "high_probability_risks",
                        "reasoning": f"High probability legal risks identified ({len(high_prob_risks)} risks)",
                        "confidence": 0.7,
                        "priority": "high",
                        "actions": [
                            "Implement preventive measures",
                            "Monitor risk factors closely",
                            "Prepare contingency plans"
                        ]
                    })
        
        # Contract risk recommendations
        if "contract_risks" in analysis_results:
            contract_result = analysis_results["contract_risks"]
            if contract_result.success and contract_result.result:
                contract_risks = contract_result.result
                
                # High severity contract risks
                high_severity_risks = [r for r in contract_risks if hasattr(r, 'severity') and r.severity in ["high", "critical"]]
                if high_severity_risks:
                    recommendations.append({
                        "type": "contract_risk_mitigation",
                        "reasoning": f"High severity contract risks identified ({len(high_severity_risks)} risks)",
                        "confidence": 0.8,
                        "priority": "high",
                        "actions": [
                            "Revise contract terms",
                            "Negotiate protective provisions",
                            "Add risk mitigation clauses"
                        ]
                    })
        
        # Overall risk score recommendations
        if "legal_risk_score" in analysis_results:
            score_result = analysis_results["legal_risk_score"]
            if score_result.success:
                risk_score = score_result.result
                
                if risk_score > 0.8:
                    recommendations.append({
                        "type": "extreme_risk_warning",
                        "reasoning": f"Extreme legal risk score of {risk_score:.2f} - recommend against proceeding",
                        "confidence": 0.9,
                        "priority": "critical",
                        "actions": [
                            "Do not proceed with current approach",
                            "Redesign decision to mitigate risks",
                            "Seek alternative approaches"
                        ]
                    })
                elif risk_score > 0.6:
                    recommendations.append({
                        "type": "significant_risk_warning",
                        "reasoning": f"Significant legal risk score of {risk_score:.2f} - proceed with caution",
                        "confidence": 0.8,
                        "priority": "high",
                        "actions": [
                            "Implement comprehensive risk mitigation",
                            "Increase legal oversight",
                            "Regular risk monitoring"
                        ]
                    })
                elif risk_score > 0.4:
                    recommendations.append({
                        "type": "moderate_risk_management",
                        "reasoning": f"Moderate legal risk score of {risk_score:.2f} - standard risk management needed",
                        "confidence": 0.7,
                        "priority": "medium",
                        "actions": [
                            "Implement standard risk controls",
                            "Regular legal review",
                            "Document risk management procedures"
                        ]
                    })
        
        # Default recommendations if no specific issues identified
        if not recommendations:
            recommendations.append({
                "type": "standard_legal_diligence",
                "reasoning": "Standard legal due diligence recommended for all strategic decisions",
                "confidence": 0.6,
                "priority": "medium",
                "actions": [
                    "Conduct legal review of decision",
                    "Document legal considerations",
                    "Ensure compliance with applicable laws"
                ]
            })
        
        return recommendations
    
    async def assess_regulatory_environment(
        self,
        industry: str,
        jurisdiction: str,
        business_activities: List[str]
    ) -> Dict[str, Any]:
        """
        Assess regulatory environment for decision.
        
        Args:
            industry: Industry sector
            jurisdiction: Legal jurisdiction
            business_activities: List of business activities
        
        Returns:
            Dictionary with regulatory assessment
        """
        try:
            assessment = {
                "regulatory_complexity": "high" if industry in ["healthcare", "financial", "energy"] else "moderate",
                "compliance_burden": "heavy" if len(business_activities) > 5 else "moderate",
                "regulatory_changes": "frequent" if industry in ["technology", "healthcare"] else "infrequent",
                "key_regulations": [],
                "compliance_priorities": []
            }
            
            # Industry-specific regulations
            if industry == "healthcare":
                assessment["key_regulations"] = ["HIPAA", "FDA", "Clinical Trial Regulations"]
            elif industry == "financial":
                assessment["key_regulations"] = ["SOX", "Dodd-Frank", "Basel III"]
            elif industry == "technology":
                assessment["key_regulations"] = ["GDPR", "CCPA", "Cybersecurity Regulations"]
            
            # Jurisdiction-specific considerations
            if "international" in jurisdiction.lower():
                assessment["compliance_priorities"].append("Multi-jurisdictional compliance coordination")
            
            if "european" in jurisdiction.lower():
                assessment["compliance_priorities"].append("GDPR compliance")
            
            if "california" in jurisdiction.lower():
                assessment["compliance_priorities"].append("CCPA compliance")
            
            return assessment
            
        except Exception as e:
            logger.error(f"Regulatory environment assessment failed: {e}")
            raise
    
    async def evaluate_contract_structure(
        self,
        contract_type: str,
        key_terms: Dict[str, Any],
        counterparty_profile: str
    ) -> Dict[str, Any]:
        """
        Evaluate contract structure and terms.
        
        Args:
            contract_type: Type of contract
            key_terms: Key contract terms
            counterparty_profile: Counterparty profile
        
        Returns:
            Dictionary with contract evaluation
        """
        try:
            evaluation = {
                "contract_risk_level": "moderate",
                "key_concerns": [],
                "recommended_changes": [],
                "negotiation_priorities": []
            }
            
            # Contract type specific evaluation
            if contract_type in ["service_agreement", "technology_license"]:
                evaluation["key_concerns"].append("Liability limitations")
                evaluation["recommended_changes"].append("Add mutual liability caps")
            
            # Counterparty risk assessment
            if "startup" in counterparty_profile.lower():
                evaluation["key_concerns"].append("Counterparty financial stability")
                evaluation["recommended_changes"].append("Require parent company guarantee")
            
            # Terms evaluation
            if "unlimited_liability" in str(key_terms).lower():
                evaluation["contract_risk_level"] = "high"
                evaluation["key_concerns"].append("Unlimited liability exposure")
                evaluation["recommended_changes"].append("Negotiate liability limitations")
            
            return evaluation
            
        except Exception as e:
            logger.error(f"Contract structure evaluation failed: {e}")
            raise
    
    async def generate_legal_summary(
        self,
        decision_context: str,
        analysis_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate comprehensive legal summary.
        
        Args:
            decision_context: Decision context
            analysis_results: All analysis results
        
        Returns:
            Dictionary with legal summary
        """
        try:
            summary = {
                "legal_recommendation": "proceed_with_caution",
                "confidence_level": 0.7,
                "key_legal_issues": [],
                "critical_risks": [],
                "compliance_status": "requires_review",
                "action_items": []
            }
            
            # Determine overall recommendation
            high_risk_count = 0
            critical_risk_count = 0
            
            # Count risks from analysis
            if "legal_recommendations" in analysis_results:
                for rec in analysis_results["legal_recommendations"]:
                    if rec["priority"] == "critical":
                        critical_risk_count += 1
                    elif rec["priority"] == "high":
                        high_risk_count += 1
            
            # Set recommendation based on risk levels
            if critical_risk_count > 0:
                summary["legal_recommendation"] = "do_not_proceed"
                summary["confidence_level"] = 0.9
            elif high_risk_count > 2:
                summary["legal_recommendation"] = "proceed_with_significant_caution"
                summary["confidence_level"] = 0.8
            elif high_risk_count > 0:
                summary["legal_recommendation"] = "proceed_with_caution"
                summary["confidence_level"] = 0.7
            else:
                summary["legal_recommendation"] = "proceed_with_standard_controls"
                summary["confidence_level"] = 0.6
            
            # Extract key issues
            if "legal_risks" in analysis_results and analysis_results["legal_risks"].success:
                risks = analysis_results["legal_risks"].result
                summary["key_legal_issues"] = [risk.description for risk in risks[:3]]  # Top 3
                summary["critical_risks"] = [risk.description for risk in risks if hasattr(risk, 'severity') and risk.severity == "critical"]
            
            # Determine compliance status
            if "compliance_assessment" in analysis_results:
                compliance_result = analysis_results["compliance_assessment"]
                if compliance_result.success:
                    compliance_data = compliance_result.result
                    non_compliant = any(req.compliance_status == "non_compliant" for req in compliance_data if hasattr(req, 'compliance_status'))
                    
                    if non_compliant:
                        summary["compliance_status"] = "non_compliant"
                    else:
                        summary["compliance_status"] = "compliant_with_monitoring"
            
            # Generate action items
            summary["action_items"] = [
                "Engage qualified legal counsel",
                "Conduct detailed legal risk assessment",
                "Develop compliance monitoring procedures",
                "Implement legal risk mitigation strategies",
                "Establish legal review processes"
            ]
            
            return summary
            
        except Exception as e:
            logger.error(f"Legal summary generation failed: {e}")
            raise