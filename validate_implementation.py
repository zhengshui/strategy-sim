#!/usr/bin/env python3
"""
Validation script for StrategySim AI implementation.

This script validates the core functionality and identifies any issues.
"""

import sys
import traceback
import asyncio
from typing import List, Dict, Any

def check_import(module_name: str) -> Dict[str, Any]:
    """Check if a module can be imported successfully."""
    try:
        exec(f"import {module_name}")
        return {"status": "success", "module": module_name}
    except Exception as e:
        return {"status": "error", "module": module_name, "error": str(e)}

def check_basic_functionality():
    """Check basic functionality of key components."""
    results = []
    
    # Test basic imports
    modules = [
        "src.config.settings",
        "src.models.decision_models",
        "src.models.agent_models",
        "src.models.report_models",
        "src.tools.financial_calculator",
        "src.tools.risk_modeler",
        "src.tools.market_research",
        "src.tools.legal_compliance",
        "src.tools.strategic_frameworks",
        "src.agents.base_agent",
        "src.agents.investor_agent",
        "src.agents.legal_agent",
        "src.agents.analyst_agent",
        "src.agents.customer_agent",
        "src.agents.strategist_agent",
        "src.agents.team",
        "src.utils.report_generator",
        "src.utils.visualization",
    ]
    
    for module in modules:
        result = check_import(module)
        results.append(result)
    
    return results

async def test_basic_calculations():
    """Test basic financial calculations."""
    try:
        from src.tools.financial_calculator import calculate_npv, calculate_roi, calculate_irr
        
        # Test NPV
        cash_flows = [-100000, 30000, 35000, 40000, 45000]
        npv = await calculate_npv(cash_flows, 0.10)
        print(f"NPV calculation: {npv}")
        
        # Test ROI
        roi = await calculate_roi(100000, 150000, 2)
        print(f"ROI calculation: {roi}")
        
        # Test IRR
        irr = await calculate_irr(cash_flows)
        print(f"IRR calculation: {irr}")
        
        return {"status": "success", "message": "Basic calculations work"}
    except Exception as e:
        return {"status": "error", "message": f"Error in calculations: {str(e)}"}

async def test_decision_models():
    """Test decision models."""
    try:
        from src.models.decision_models import DecisionInput, DecisionType, DecisionOption
        
        # Create a test decision
        decision = DecisionInput(
            title="Test Decision",
            description="This is a test decision for validation purposes",
            decision_type=DecisionType.INVESTMENT,
            options=[
                DecisionOption(name="Option A", description="First option"),
                DecisionOption(name="Option B", description="Second option")
            ],
            timeline="30 days"
        )
        
        print(f"Decision created: {decision.title}")
        return {"status": "success", "message": "Decision models work"}
    except Exception as e:
        return {"status": "error", "message": f"Error in decision models: {str(e)}"}

async def main():
    """Run all validation tests."""
    print("=== StrategySim AI Validation ===\n")
    
    # Check imports
    print("1. Checking imports...")
    import_results = check_basic_functionality()
    
    success_count = sum(1 for r in import_results if r["status"] == "success")
    total_count = len(import_results)
    
    print(f"   Imports: {success_count}/{total_count} successful")
    
    # Show failed imports
    failed_imports = [r for r in import_results if r["status"] == "error"]
    if failed_imports:
        print("   Failed imports:")
        for failed in failed_imports:
            print(f"     - {failed['module']}: {failed['error']}")
    
    # Test basic calculations
    print("\n2. Testing basic calculations...")
    calc_result = await test_basic_calculations()
    print(f"   {calc_result['message']}")
    
    # Test decision models
    print("\n3. Testing decision models...")
    model_result = await test_decision_models()
    print(f"   {model_result['message']}")
    
    # Summary
    print("\n=== Validation Summary ===")
    if success_count == total_count and calc_result["status"] == "success" and model_result["status"] == "success":
        print("✅ All core components are working correctly!")
        return 0
    else:
        print("❌ Some components have issues that need to be addressed.")
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))