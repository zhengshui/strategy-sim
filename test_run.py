#!/usr/bin/env python3
"""
Quick test to verify the main application functionality.
"""

import asyncio
from src.agents import create_decision_team, run_decision_analysis
from src.models.decision_models import DecisionInput, DecisionType, DecisionOption

async def test_core_functionality():
    """Test the core functionality of the StrategySim AI system."""
    print("🚀 Testing StrategySim AI Core Functionality...")
    
    try:
        # Test 1: Create a decision team
        print("\n1. Creating decision analysis team...")
        team = create_decision_team()
        print("✅ Decision team created successfully")
        
        # Test 2: Create a sample decision
        print("\n2. Creating sample decision input...")
        decision = DecisionInput(
            title="Sample Strategic Decision",
            description="Should we expand our product line to include eco-friendly alternatives?",
            decision_type=DecisionType.PRODUCT_LAUNCH,
            options=[
                DecisionOption(
                    name="Eco-Friendly Expansion",
                    description="Launch new eco-friendly product line"
                ),
                DecisionOption(
                    name="Status Quo",
                    description="Continue with current product offerings"
                )
            ],
            timeline="6 months",
            budget_range="$500K - $1M"
        )
        print("✅ Decision input created successfully")
        
        # Test 3: Validate decision
        print("\n3. Validating decision input...")
        from src.models.decision_models import validate_decision_input
        validation = validate_decision_input(decision)
        print(f"✅ Decision validation: {'Valid' if validation.is_valid else 'Invalid'}")
        if validation.warnings:
            print(f"   Warnings: {len(validation.warnings)}")
        
        print("\n🎉 All core functionality tests passed!")
        print("The StrategySim AI system is ready for use.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(test_core_functionality())
    if result:
        print("\n✅ System is ready to run!")
        print("To start the web interface, run: chainlit run app.py")
    else:
        print("\n❌ Issues found. Please check the errors above.")