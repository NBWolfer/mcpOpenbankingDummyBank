#!/usr/bin/env python3
"""
Test script demonstrating how MCP servers would interact with the Dummy Bank API using CustomerOID
"""
import requests
import json

BASE_URL = "http://localhost:3000"

def test_customer_oid_apis():
    """Test all CustomerOID-based endpoints"""
    
    print("🏦 Testing Dummy Bank API - CustomerOID Integration")
    print("=" * 60)
    
    # Test 1: Health check
    print("\n1. Health Check:")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("❌ Server not running on port 3000")
        print("   Please run: python run_server.py")
        return
    
    # Test 2: List all customers
    print("\n2. List All Customers:")
    response = requests.get(f"{BASE_URL}/customers")
    customers = response.json()
    print(f"✅ Found {len(customers)} customers:")
    for customer in customers:
        print(f"   - CustomerOID: {customer['customer_oid']} | Name: {customer['name']}")
    
    # Test 3: Check if customer exists
    test_customer_oid = "550e8400-e29b-41d4-a716-446655440001"
    print(f"\n3. Check CustomerOID '{test_customer_oid[:8]}...' exists:")
    response = requests.get(f"{BASE_URL}/customer/{test_customer_oid}/exists")
    if response.status_code == 200:
        exists_data = response.json()
        print(f"✅ CustomerOID '{test_customer_oid[:8]}...' exists: {exists_data['exists']}")
        if exists_data['exists']:
            print(f"   Name: {exists_data['name']}")
    else:
        print(f"❌ Error checking customer existence: {response.status_code}")
        print(f"   Response: {response.text}")
    
    # Test 4: Get full portfolio
    print(f"\n4. Get Full Portfolio for CustomerOID '{test_customer_oid[:8]}...':")
    response = requests.get(f"{BASE_URL}/user-portfolio/{test_customer_oid}")
    if response.status_code == 200:
        portfolio = response.json()
        print(f"✅ Portfolio retrieved successfully")
        print(f"   Customer: {portfolio['user']['name']}")
        print(f"   CustomerOID: {portfolio['user']['customer_oid'][:8]}...")
        print(f"   Summary:")
        summary = portfolio['portfolio_summary']
        print(f"     - Total Cash: ${summary['total_cash_balance']:,.2f}")
        print(f"     - Assets: {summary['total_assets']}")
        print(f"     - Bank Accounts: {summary['total_accounts']}")
        print(f"     - Transactions: {summary['total_transactions']}")
        print(f"     - Spending Categories: {summary['total_spending_categories']}")
        print(f"     - Derivative Positions: {summary['total_derivative_positions']}")
        
        # Show data availability
        has_data = summary['has_data']
        print(f"   Data Available:")
        for data_type, available in has_data.items():
            status = "✅" if available else "❌"
            print(f"     {status} {data_type.title()}")
            
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
    
    # Test 5: Test invalid CustomerOID
    print("\n5. Test Invalid CustomerOID:")
    invalid_oid = "invalid-oid"
    response = requests.get(f"{BASE_URL}/customer/{invalid_oid}/exists")
    if response.status_code == 400:
        print(f"✅ Correctly rejected invalid CustomerOID '{invalid_oid}'")
        print(f"   Error: {response.json()['detail']}")
    
    # Test 6: Test user registration
    print("\n6. Test User Registration:")
    user_data = {"name": "Test User"}
    response = requests.post(f"{BASE_URL}/register-customer", json=user_data)
    if response.status_code == 200:
        registration_data = response.json()
        print(f"✅ User registration successful")
        print(f"   New CustomerOID: {registration_data['customer_oid'][:8]}...")
        print(f"   Name: {registration_data['name']}")
        new_customer_oid = registration_data['customer_oid']
        
        # Clean up - delete the test user
        delete_response = requests.delete(f"{BASE_URL}/customer/{new_customer_oid}")
        if delete_response.status_code == 200:
            print("   ✅ Test user cleaned up successfully")
    else:
        print(f"❌ Registration failed: {response.status_code} - {response.text}")
    
    print("\n" + "=" * 60)
    print("🎯 All tests completed! Your API is ready for MCP server integration.")
    print(f"\n📋 Key endpoints for your MCP server:")
    print(f"   • Portfolio: GET {BASE_URL}/user-portfolio/{{customer_oid}}")
    print(f"   • Register: POST {BASE_URL}/register-customer")
    print(f"   • Delete: DELETE {BASE_URL}/customer/{{customer_oid}}")
    print(f"   • List customers: GET {BASE_URL}/customers")
    print(f"   • Check exists: GET {BASE_URL}/customer/{{customer_oid}}/exists")
    print(f"\n💡 Example CustomerOID: 550e8400-e29b-41d4-a716-446655440001")

if __name__ == "__main__":
    test_customer_oid_apis()
