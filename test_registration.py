#!/usr/bin/env python3
"""
Test script for the new user registration endpoint
"""
import requests
import json
import uuid

BASE_URL = "http://localhost:3000"

def test_user_registration():
    """Test the user registration endpoint"""
    
    print("🆕 Testing User Registration Endpoint")
    print("=" * 50)
    
    # Test 1: Register user with auto-generated CustomerOID
    print("\n1. Register user with auto-generated CustomerOID:")
    user_data = {
        "name": "Alice Johnson"
    }
    response = requests.post(f"{BASE_URL}/register-customer", json=user_data)
    if response.status_code == 200:
        registration_data = response.json()
        print(f"✅ User registered successfully!")
        print(f"   CustomerOID: {registration_data['customer_oid']}")
        print(f"   Name: {registration_data['name']}")
        print(f"   Message: {registration_data['message']}")
        alice_oid = registration_data['customer_oid']
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
        return
    
    # Test 2: Register user with custom CustomerOID
    print("\n2. Register user with custom CustomerOID:")
    custom_oid = str(uuid.uuid4())
    user_data = {
        "name": "Bob Wilson",
        "customer_oid": custom_oid
    }
    response = requests.post(f"{BASE_URL}/register-customer", json=user_data)
    if response.status_code == 200:
        registration_data = response.json()
        print(f"✅ User registered successfully!")
        print(f"   CustomerOID: {registration_data['customer_oid']}")
        print(f"   Name: {registration_data['name']}")
        print(f"   Custom OID matches: {registration_data['customer_oid'] == custom_oid}")
        bob_oid = registration_data['customer_oid']
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
        return
    
    # Test 3: Try to register duplicate CustomerOID
    print("\n3. Try to register duplicate CustomerOID:")
    user_data = {
        "name": "Charlie Brown",
        "customer_oid": custom_oid  # Same as Bob's
    }
    response = requests.post(f"{BASE_URL}/register-customer", json=user_data)
    if response.status_code == 409:
        print("✅ Correctly rejected duplicate CustomerOID")
        print(f"   Error: {response.json()['detail']}")
    else:
        print(f"❌ Unexpected response: {response.status_code} - {response.text}")
    
    # Test 4: Try to register with invalid name
    print("\n4. Try to register with invalid name:")
    user_data = {
        "name": "A"  # Too short
    }
    response = requests.post(f"{BASE_URL}/register-customer", json=user_data)
    if response.status_code == 400:
        print("✅ Correctly rejected invalid name")
        print(f"   Error: {response.json()['detail']}")
    else:
        print(f"❌ Unexpected response: {response.status_code} - {response.text}")
    
    # Test 5: Verify new users appear in customer list
    print("\n5. Verify new users appear in customer list:")
    response = requests.get(f"{BASE_URL}/customers")
    if response.status_code == 200:
        customers = response.json()
        alice_found = any(c['customer_oid'] == alice_oid for c in customers)
        bob_found = any(c['customer_oid'] == bob_oid for c in customers)
        print(f"✅ Total customers: {len(customers)}")
        print(f"   Alice found: {alice_found}")
        print(f"   Bob found: {bob_found}")
    else:
        print(f"❌ Error getting customer list: {response.status_code}")
    
    # Test 6: Check if new users exist
    print("\n6. Check if new users exist:")
    for name, oid in [("Alice", alice_oid), ("Bob", bob_oid)]:
        response = requests.get(f"{BASE_URL}/customer/{oid}/exists")
        if response.status_code == 200:
            exists_data = response.json()
            print(f"✅ {name} exists: {exists_data['exists']} - {exists_data['name']}")
        else:
            print(f"❌ Error checking {name}: {response.status_code}")
    
    # Test 7: Get portfolio for new user (should be empty)
    print("\n7. Get portfolio for Alice (should be empty):")
    response = requests.get(f"{BASE_URL}/user-portfolio/{alice_oid}")
    if response.status_code == 200:
        portfolio = response.json()
        summary = portfolio['portfolio_summary']
        print(f"✅ Portfolio retrieved for Alice")
        print(f"   Total Assets: {summary['total_assets']}")
        print(f"   Total Accounts: {summary['total_accounts']}")
        print(f"   Has any data: {any(summary['has_data'].values())}")
    else:
        print(f"❌ Error getting portfolio: {response.status_code}")
    
    print("\n" + "=" * 50)
    print("🎯 User registration endpoint tests completed!")
    print(f"\n📋 API endpoints for MCP client backend:")
    print(f"   • Register user: POST {BASE_URL}/register-customer")
    print(f"   • Delete user: DELETE {BASE_URL}/customer/{{customer_oid}}")
    print(f"   • Check exists: GET {BASE_URL}/customer/{{customer_oid}}/exists")
    print(f"   • Get portfolio: GET {BASE_URL}/user-portfolio/{{customer_oid}}")
    print(f"   • List all: GET {BASE_URL}/customers")
    
    print(f"\n💡 Example registration payload:")
    print(f"   {{\"name\": \"Customer Name\", \"customer_oid\": \"optional-uuid\"}}")

if __name__ == "__main__":
    try:
        test_user_registration()
    except requests.exceptions.ConnectionError:
        print("❌ Server not running on port 3000")
        print("   Please start the server first: python run_server.py")
