#!/usr/bin/env python3
"""
Script to reset and seed the database with fresh sample data
"""

from db import reset_and_seed_database

if __name__ == "__main__":
    print("🏦 Dummy Bank Database Reset & Seed")
    print("=" * 40)
    
    try:
        reset_and_seed_database()
        print("\n🎉 Database reset and seeded successfully!")
        print("\n📋 Available customers for testing:")
        print("  • 550e8400-e29b-41d4-a716-446655440001 - John Doe (moderate portfolio)")
        print("  • 550e8400-e29b-41d4-a716-446655440002 - Jane Smith (aggressive portfolio)")  
        print("  • 550e8400-e29b-41d4-a716-446655440003 - Robert Johnson (conservative portfolio)")
        print("  • 550e8400-e29b-41d4-a716-446655440004 - ABC Corporation (corporate portfolio)")
        print("  • 550e8400-e29b-41d4-a716-446655440005 - Michael Chen (private banking)")
        print("\n🔗 Test URLs:")
        print("  • Portfolio: http://localhost:3000/user-portfolio/550e8400-e29b-41d4-a716-446655440001")
        print("  • Portfolio: http://localhost:3000/user-portfolio/550e8400-e29b-41d4-a716-446655440002")
        print("  • Portfolio: http://localhost:3000/user-portfolio/550e8400-e29b-41d4-a716-446655440003")
        print("  • Portfolio: http://localhost:3000/user-portfolio/550e8400-e29b-41d4-a716-446655440004")
        print("  • Portfolio: http://localhost:3000/user-portfolio/550e8400-e29b-41d4-a716-446655440005")
        print("  • All customers: http://localhost:3000/customers")
        
    except Exception as e:
        print(f"❌ Error: {e}")
