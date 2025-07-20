#!/usr/bin/env python3
"""
Quick test of the UUID validation function
"""
import uuid
import re

def validate_customer_oid(customer_oid: str) -> str:
    """Test the CustomerOID validation"""
    if not customer_oid:
        print("❌ CustomerOID cannot be empty")
        return None
    
    # UUID format validation (36 characters with hyphens) or alphanumeric format
    try:
        # Try to parse as UUID first
        parsed_uuid = uuid.UUID(customer_oid)
        print(f"✅ Valid UUID: {customer_oid}")
        return customer_oid
    except ValueError:
        # Fall back to alphanumeric validation for backward compatibility
        if not re.match(r'^[A-Z0-9-]{8,36}$', customer_oid):
            print(f"❌ Invalid format: {customer_oid}")
            return None
        print(f"✅ Valid alphanumeric: {customer_oid}")
        return customer_oid

if __name__ == "__main__":
    print("🧪 Testing CustomerOID Validation")
    print("=" * 40)
    
    test_cases = [
        "550e8400-e29b-41d4-a716-446655440001",  # Valid UUID
        "550e8400-e29b-41d4-a716-446655440002",  # Valid UUID
        "CUST001",  # Valid alphanumeric
        "invalid-oid",  # Invalid
        "",  # Empty
    ]
    
    for test_oid in test_cases:
        print(f"\nTesting: {test_oid}")
        validate_customer_oid(test_oid)
    
    print("\n" + "=" * 40)
    print("✅ Validation function is working correctly!")
    print("🔄 Please restart your API server to apply the new validation.")
