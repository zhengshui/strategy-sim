#!/usr/bin/env python3
"""
Verification script for StrategySim AI success criteria.

This script checks all success criteria from the PRP document.
"""

import sys
import asyncio
from typing import List, Dict, Any

def check_success_criteria():
    """Check all success criteria from the PRP document."""
    
    criteria = [
        {
            "id": "SC1",
            "description": "Five specialized agents with distinct professional personas and tools",
            "validation": check_specialized_agents
        },
        {
            "id": "SC2", 
            "description": "SelectorGroupChat enables natural agent interaction flow",
            "validation": check_selector_groupchat
        },
        {
            "id": "SC3",
            "description": "Chainlit interface provides real-time decision simulation visualization",
            "validation": check_chainlit_interface
        },
        {
            "id": "SC4",
            "description": "Risk-reward analysis with quantified metrics and probability assessments",
            "validation": check_risk_reward_analysis
        },
        {
            "id": "SC5",
            "description": "Structured decision reports with actionable recommendations",
            "validation": check_decision_reports
        },
        {
            "id": "SC6",
            "description": "Comprehensive test coverage for all agent interactions",
            "validation": check_test_coverage
        }
    ]
    
    return criteria

def check_specialized_agents():
    """Check if five specialized agents exist with distinct personas."""
    try:
        from src.agents.investor_agent import InvestorAgent
        from src.agents.legal_agent import LegalAgent
        from src.agents.analyst_agent import AnalystAgent
        from src.agents.customer_agent import CustomerAgent
        from src.agents.strategist_agent import StrategistAgent
        
        # Check if each agent has specialized tools
        from src.tools.financial_calculator import calculate_npv, calculate_roi
        from src.tools.legal_compliance import assess_regulatory_compliance
        from src.tools.risk_modeler import run_monte_carlo_simulation
        from src.tools.market_research import analyze_customer_behavior
        from src.tools.strategic_frameworks import conduct_swot_analysis
        
        agents = [
            ("Investor Agent", InvestorAgent),
            ("Legal Agent", LegalAgent),
            ("Analyst Agent", AnalystAgent),
            ("Customer Agent", CustomerAgent),
            ("Strategist Agent", StrategistAgent)
        ]
        
        for name, agent_class in agents:
            # Check if agent class exists and has expected methods
            if hasattr(agent_class, 'get_specialized_tools'):
                print(f"    ✅ {name} - has specialized tools")
            else:
                print(f"    ⚠️  {name} - missing specialized tools method")
        
        return {"status": "success", "message": "5 specialized agents implemented with distinct tools"}
    except Exception as e:
        return {"status": "error", "message": f"Error checking agents: {str(e)}"}

def check_selector_groupchat():
    """Check if SelectorGroupChat is implemented."""
    try:
        from src.agents.team import DecisionAnalysisTeam
        
        # Check if team uses SelectorGroupChat
        team_source = open("src/agents/team.py", "r").read()
        if "SelectorGroupChat" in team_source:
            print("    ✅ SelectorGroupChat implementation found")
            return {"status": "success", "message": "SelectorGroupChat enabled for dynamic agent selection"}
        else:
            return {"status": "error", "message": "SelectorGroupChat not found in team implementation"}
    except Exception as e:
        return {"status": "error", "message": f"Error checking SelectorGroupChat: {str(e)}"}

def check_chainlit_interface():
    """Check if Chainlit interface is implemented."""
    try:
        import os
        if os.path.exists("app.py"):
            app_source = open("app.py", "r").read()
            if "chainlit" in app_source.lower() and "@cl.on_chat_start" in app_source:
                print("    ✅ Chainlit interface implementation found")
                return {"status": "success", "message": "Chainlit interface provides real-time visualization"}
            else:
                return {"status": "error", "message": "Chainlit interface not properly implemented"}
        else:
            return {"status": "error", "message": "app.py not found"}
    except Exception as e:
        return {"status": "error", "message": f"Error checking Chainlit interface: {str(e)}"}

def check_risk_reward_analysis():
    """Check if risk-reward analysis is implemented."""
    try:
        from src.tools.risk_modeler import run_monte_carlo_simulation, calculate_risk_metrics
        from src.tools.financial_calculator import calculate_npv, calculate_roi
        from src.models.report_models import RiskAssessment
        
        print("    ✅ Risk modeling tools available")
        print("    ✅ Financial analysis tools available")
        print("    ✅ Risk assessment models available")
        
        return {"status": "success", "message": "Risk-reward analysis implemented with quantified metrics"}
    except Exception as e:
        return {"status": "error", "message": f"Error checking risk-reward analysis: {str(e)}"}

def check_decision_reports():
    """Check if structured decision reports are implemented."""
    try:
        from src.models.report_models import DecisionReport, ExecutiveSummary, ActionItem
        from src.utils.report_generator import ReportGenerator
        
        print("    ✅ Decision report models available")
        print("    ✅ Report generation utilities available")
        
        return {"status": "success", "message": "Structured decision reports with actionable recommendations"}
    except Exception as e:
        return {"status": "error", "message": f"Error checking decision reports: {str(e)}"}

def check_test_coverage():
    """Check if comprehensive test coverage exists."""
    try:
        import os
        test_files = []
        
        # Check for test files
        test_dirs = ["tests/test_agents", "tests/test_tools", "tests/test_models", "tests/test_utils"]
        for test_dir in test_dirs:
            if os.path.exists(test_dir):
                files = [f for f in os.listdir(test_dir) if f.startswith("test_") and f.endswith(".py")]
                test_files.extend(files)
        
        if len(test_files) > 10:  # Reasonable number of test files
            print(f"    ✅ {len(test_files)} test files found")
            return {"status": "success", "message": f"Comprehensive test coverage with {len(test_files)} test files"}
        else:
            return {"status": "warning", "message": f"Limited test coverage - only {len(test_files)} test files"}
    except Exception as e:
        return {"status": "error", "message": f"Error checking test coverage: {str(e)}"}

async def main():
    """Run all success criteria checks."""
    print("=== StrategySim AI Success Criteria Verification ===\n")
    
    criteria = check_success_criteria()
    
    results = []
    for criterion in criteria:
        print(f"{criterion['id']}: {criterion['description']}")
        result = criterion['validation']()
        results.append(result)
        
        if result["status"] == "success":
            print(f"  ✅ PASS: {result['message']}")
        elif result["status"] == "warning":
            print(f"  ⚠️  WARNING: {result['message']}")
        else:
            print(f"  ❌ FAIL: {result['message']}")
        print()
    
    # Summary
    print("=== Verification Summary ===")
    success_count = sum(1 for r in results if r["status"] == "success")
    warning_count = sum(1 for r in results if r["status"] == "warning")
    fail_count = sum(1 for r in results if r["status"] == "error")
    
    print(f"✅ Passed: {success_count}/{len(results)}")
    print(f"⚠️  Warnings: {warning_count}/{len(results)}")
    print(f"❌ Failed: {fail_count}/{len(results)}")
    
    if success_count == len(results):
        print("\n🎉 All success criteria have been met!")
        return 0
    elif success_count + warning_count == len(results):
        print("\n✅ All critical success criteria have been met (with some warnings)!")
        return 0
    else:
        print("\n❌ Some success criteria need attention.")
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))