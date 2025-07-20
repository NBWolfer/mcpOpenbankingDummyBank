from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_oid: str = Field(index=True, unique=True)
    name: str

class Asset(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_oid: str = Field(index=True)  # Add index for faster lookups
    asset_type: str
    symbol: str
    amount: float

class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_oid: str = Field(index=True)  # Add index for faster lookups
    date: str
    type: str
    asset: Optional[str]
    amount: float

class Spending(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_oid: str = Field(index=True)  # Add index for faster lookups
    category: str
    amount: float
    month: str

class Institution(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    type: str  # e.g. "bank", "broker", "exchange"
    contact_info: Optional[str] = None
    internal_code: str

class BankAccount(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_oid: str = Field(index=True)  # Add index for faster lookups
    institution_id: int
    balance: float
    currency: str
    iban: Optional[str] = None

class DerivativeTransaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_oid: str = Field(index=True)  # Add index for faster lookups
    type: str           # e.g. "option", "future"
    side: str           # "buy" or "sell"
    asset: str          # e.g. "EUR"
    strike_price: float
    premium: float
    expiration_date: str
    execution_date: str
    strategy: Optional[str] = None  # "covered_call", etc.
    status: str         # "open", "exercised", "expired"
    counterparty: Optional[str] = None  # "BANK" or another OID


def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)

def reset_database():
    """Reset the database by dropping and recreating all tables"""
    print("🗑️  Resetting database...")
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    print("✅ Database reset complete!")

def create_sample_data():
    """Create fresh sample data for testing the portfolio analysis"""
    session = Session(engine)
    
    try:
        print("📊 Creating fresh sample data...")
        
        # Create sample users
        users = [
            User(customer_oid="550e8400-e29b-41d4-a716-446655440001", name="John Doe"),
            User(customer_oid="550e8400-e29b-41d4-a716-446655440002", name="Jane Smith"),
            User(customer_oid="550e8400-e29b-41d4-a716-446655440003", name="Robert Johnson"),
            User(customer_oid="550e8400-e29b-41d4-a716-446655440004", name="ABC Corporation"),
            User(customer_oid="550e8400-e29b-41d4-a716-446655440005", name="Michael Chen")
        ]
        for user in users:
            session.add(user)
        
        # Create sample institutions
        institutions = [
            Institution(name="Global Bank", type="bank", contact_info="contact@globalbank.com", internal_code="GB001"),
            Institution(name="Investment Corp", type="broker", contact_info="support@investcorp.com", internal_code="IC001"),
            Institution(name="Crypto Exchange", type="exchange", contact_info="help@cryptoex.com", internal_code="CE001")
        ]
        for institution in institutions:
            session.add(institution)
        
        session.commit()
        
        # Create sample bank accounts
        bank_accounts = [
            # Customer 1 accounts
            BankAccount(customer_oid="550e8400-e29b-41d4-a716-446655440001", institution_id=1, balance=50000.0, currency="USD", iban="US1234567890123456"),
            BankAccount(customer_oid="550e8400-e29b-41d4-a716-446655440001", institution_id=1, balance=25000.0, currency="EUR", iban="DE9876543210987654"),
            # Customer 2 accounts  
            BankAccount(customer_oid="550e8400-e29b-41d4-a716-446655440002", institution_id=1, balance=75000.0, currency="USD", iban="US2345678901234567"),
            BankAccount(customer_oid="550e8400-e29b-41d4-a716-446655440002", institution_id=2, balance=100000.0, currency="USD", iban="US3456789012345678"),
            # Customer 3 accounts
            BankAccount(customer_oid="550e8400-e29b-41d4-a716-446655440003", institution_id=1, balance=30000.0, currency="USD", iban="US4567890123456789"),
            # Corporate customer account
            BankAccount(customer_oid="550e8400-e29b-41d4-a716-446655440004", institution_id=2, balance=500000.0, currency="USD", iban="US5678901234567890"),
            # Private customer account
            BankAccount(customer_oid="550e8400-e29b-41d4-a716-446655440005", institution_id=3, balance=85000.0, currency="USD", iban="US6789012345678901")
        ]
        for account in bank_accounts:
            session.add(account)
        
        # Create sample assets
        assets = [
            # Customer 1 portfolio
            Asset(customer_oid="550e8400-e29b-41d4-a716-446655440001", asset_type="stock", symbol="AAPL", amount=100),
            Asset(customer_oid="550e8400-e29b-41d4-a716-446655440001", asset_type="stock", symbol="GOOGL", amount=50),
            Asset(customer_oid="550e8400-e29b-41d4-a716-446655440001", asset_type="bond", symbol="US10Y", amount=10000),
            Asset(customer_oid="550e8400-e29b-41d4-a716-446655440001", asset_type="crypto", symbol="BTC", amount=2.5),
            Asset(customer_oid="550e8400-e29b-41d4-a716-446655440001", asset_type="etf", symbol="SPY", amount=200),
            
            # Customer 2 portfolio (more aggressive)
            Asset(customer_oid="550e8400-e29b-41d4-a716-446655440002", asset_type="stock", symbol="TSLA", amount=150),
            Asset(customer_oid="550e8400-e29b-41d4-a716-446655440002", asset_type="stock", symbol="NVDA", amount=75),
            Asset(customer_oid="550e8400-e29b-41d4-a716-446655440002", asset_type="crypto", symbol="BTC", amount=5.0),
            Asset(customer_oid="550e8400-e29b-41d4-a716-446655440002", asset_type="crypto", symbol="ETH", amount=20.0),
            Asset(customer_oid="550e8400-e29b-41d4-a716-446655440002", asset_type="stock", symbol="MSFT", amount=80),
            
            # Customer 3 portfolio (conservative)
            Asset(customer_oid="550e8400-e29b-41d4-a716-446655440003", asset_type="bond", symbol="US10Y", amount=20000),
            Asset(customer_oid="550e8400-e29b-41d4-a716-446655440003", asset_type="bond", symbol="CORP_BONDS", amount=15000),
            Asset(customer_oid="550e8400-e29b-41d4-a716-446655440003", asset_type="etf", symbol="SPY", amount=100),
            Asset(customer_oid="550e8400-e29b-41d4-a716-446655440003", asset_type="stock", symbol="JNJ", amount=60),
            
            # Corporate customer portfolio
            Asset(customer_oid="550e8400-e29b-41d4-a716-446655440004", asset_type="stock", symbol="AAPL", amount=1000),
            Asset(customer_oid="550e8400-e29b-41d4-a716-446655440004", asset_type="stock", symbol="MSFT", amount=800),
            Asset(customer_oid="550e8400-e29b-41d4-a716-446655440004", asset_type="bond", symbol="CORP_BONDS", amount=100000),
            Asset(customer_oid="550e8400-e29b-41d4-a716-446655440004", asset_type="etf", symbol="QQQ", amount=500),
            
            # Private customer portfolio
            Asset(customer_oid="550e8400-e29b-41d4-a716-446655440005", asset_type="stock", symbol="AMZN", amount=25),
            Asset(customer_oid="550e8400-e29b-41d4-a716-446655440005", asset_type="crypto", symbol="ETH", amount=10.0),
            Asset(customer_oid="550e8400-e29b-41d4-a716-446655440005", asset_type="etf", symbol="VTI", amount=300)
        ]
        for asset in assets:
            session.add(asset)
        
        # Create sample transactions
        transactions = [
            # Customer 1 transactions
            Transaction(customer_oid="550e8400-e29b-41d4-a716-446655440001", date="2025-01-15", type="buy", asset="AAPL", amount=-15000),
            Transaction(customer_oid="550e8400-e29b-41d4-a716-446655440001", date="2025-02-20", type="buy", asset="GOOGL", amount=-8500),
            Transaction(customer_oid="550e8400-e29b-41d4-a716-446655440001", date="2025-03-10", type="deposit", asset="USD", amount=25000),
            Transaction(customer_oid="550e8400-e29b-41d4-a716-446655440001", date="2025-04-05", type="buy", asset="BTC", amount=-12000),
            Transaction(customer_oid="550e8400-e29b-41d4-a716-446655440001", date="2025-05-15", type="sell", asset="AAPL", amount=3000),
            Transaction(customer_oid="550e8400-e29b-41d4-a716-446655440001", date="2025-06-01", type="dividend", asset="SPY", amount=250),
            
            # Customer 2 transactions
            Transaction(customer_oid="550e8400-e29b-41d4-a716-446655440002", date="2025-01-20", type="buy", asset="TSLA", amount=-25000),
            Transaction(customer_oid="550e8400-e29b-41d4-a716-446655440002", date="2025-02-15", type="buy", asset="NVDA", amount=-18000),
            Transaction(customer_oid="550e8400-e29b-41d4-a716-446655440002", date="2025-03-05", type="buy", asset="BTC", amount=-20000),
            Transaction(customer_oid="550e8400-e29b-41d4-a716-446655440002", date="2025-04-10", type="buy", asset="ETH", amount=-15000),
            Transaction(customer_oid="550e8400-e29b-41d4-a716-446655440002", date="2025-05-20", type="sell", asset="TSLA", amount=8000),
            
            # Customer 3 transactions
            Transaction(customer_oid="550e8400-e29b-41d4-a716-446655440003", date="2025-01-10", type="buy", asset="US10Y", amount=-20000),
            Transaction(customer_oid="550e8400-e29b-41d4-a716-446655440003", date="2025-02-25", type="buy", asset="CORP_BONDS", amount=-15000),
            Transaction(customer_oid="550e8400-e29b-41d4-a716-446655440003", date="2025-03-15", type="buy", asset="SPY", amount=-5000),
            Transaction(customer_oid="550e8400-e29b-41d4-a716-446655440003", date="2025-04-20", type="dividend", asset="JNJ", amount=180),
            
            # Corporate customer transactions
            Transaction(customer_oid="550e8400-e29b-41d4-a716-446655440004", date="2025-01-05", type="buy", asset="AAPL", amount=-150000),
            Transaction(customer_oid="550e8400-e29b-41d4-a716-446655440004", date="2025-02-10", type="buy", asset="MSFT", amount=-120000),
            Transaction(customer_oid="550e8400-e29b-41d4-a716-446655440004", date="2025-03-01", type="deposit", asset="USD", amount=200000),
            Transaction(customer_oid="550e8400-e29b-41d4-a716-446655440004", date="2025-04-15", type="dividend", asset="AAPL", amount=2500),
            
            # Private customer transactions
            Transaction(customer_oid="550e8400-e29b-41d4-a716-446655440005", date="2025-01-25", type="buy", asset="AMZN", amount=-35000),
            Transaction(customer_oid="550e8400-e29b-41d4-a716-446655440005", date="2025-03-20", type="buy", asset="ETH", amount=-25000),
            Transaction(customer_oid="550e8400-e29b-41d4-a716-446655440005", date="2025-05-10", type="buy", asset="VTI", amount=-15000),
        ]
        for transaction in transactions:
            session.add(transaction)
        
        # Create sample spending data
        spending_data = [
            # Customer 1 spending (moderate)
            Spending(customer_oid="550e8400-e29b-41d4-a716-446655440001", category="groceries", amount=800, month="2025-01"),
            Spending(customer_oid="550e8400-e29b-41d4-a716-446655440001", category="utilities", amount=300, month="2025-01"),
            Spending(customer_oid="550e8400-e29b-41d4-a716-446655440001", category="entertainment", amount=500, month="2025-01"),
            Spending(customer_oid="550e8400-e29b-41d4-a716-446655440001", category="transport", amount=400, month="2025-01"),
            Spending(customer_oid="550e8400-e29b-41d4-a716-446655440001", category="groceries", amount=750, month="2025-02"),
            Spending(customer_oid="550e8400-e29b-41d4-a716-446655440001", category="utilities", amount=280, month="2025-02"),
            Spending(customer_oid="550e8400-e29b-41d4-a716-446655440001", category="healthcare", amount=250, month="2025-02"),
            
            # Customer 2 spending (high earner, high spender)
            Spending(customer_oid="550e8400-e29b-41d4-a716-446655440002", category="groceries", amount=1200, month="2025-01"),
            Spending(customer_oid="550e8400-e29b-41d4-a716-446655440002", category="dining", amount=800, month="2025-01"),
            Spending(customer_oid="550e8400-e29b-41d4-a716-446655440002", category="travel", amount=2500, month="2025-01"),
            Spending(customer_oid="550e8400-e29b-41d4-a716-446655440002", category="entertainment", amount=1000, month="2025-01"),
            Spending(customer_oid="550e8400-e29b-41d4-a716-446655440002", category="shopping", amount=1500, month="2025-02"),
            Spending(customer_oid="550e8400-e29b-41d4-a716-446655440002", category="utilities", amount=400, month="2025-02"),
            
            # Customer 3 spending (conservative)
            Spending(customer_oid="550e8400-e29b-41d4-a716-446655440003", category="groceries", amount=600, month="2025-01"),
            Spending(customer_oid="550e8400-e29b-41d4-a716-446655440003", category="utilities", amount=250, month="2025-01"),
            Spending(customer_oid="550e8400-e29b-41d4-a716-446655440003", category="healthcare", amount=300, month="2025-01"),
            Spending(customer_oid="550e8400-e29b-41d4-a716-446655440003", category="groceries", amount=580, month="2025-02"),
            Spending(customer_oid="550e8400-e29b-41d4-a716-446655440003", category="utilities", amount=240, month="2025-02"),
            
            # Corporate customer spending
            Spending(customer_oid="550e8400-e29b-41d4-a716-446655440004", category="office_supplies", amount=5000, month="2025-01"),
            Spending(customer_oid="550e8400-e29b-41d4-a716-446655440004", category="utilities", amount=8000, month="2025-01"),
            Spending(customer_oid="550e8400-e29b-41d4-a716-446655440004", category="marketing", amount=15000, month="2025-01"),
            Spending(customer_oid="550e8400-e29b-41d4-a716-446655440004", category="office_supplies", amount=4500, month="2025-02"),
            Spending(customer_oid="550e8400-e29b-41d4-a716-446655440004", category="utilities", amount=7500, month="2025-02"),
            
            # Private customer spending
            Spending(customer_oid="550e8400-e29b-41d4-a716-446655440005", category="groceries", amount=900, month="2025-01"),
            Spending(customer_oid="550e8400-e29b-41d4-a716-446655440005", category="entertainment", amount=600, month="2025-01"),
            Spending(customer_oid="550e8400-e29b-41d4-a716-446655440005", category="travel", amount=1200, month="2025-01"),
            Spending(customer_oid="550e8400-e29b-41d4-a716-446655440005", category="groceries", amount=850, month="2025-02"),
            Spending(customer_oid="550e8400-e29b-41d4-a716-446655440005", category="utilities", amount=350, month="2025-02"),
        ]
        for spend in spending_data:
            session.add(spend)
        
        # Create sample derivative transactions
        derivatives = [
            # Customer 1 - moderate options trading
            DerivativeTransaction(
                customer_oid="550e8400-e29b-41d4-a716-446655440001", type="option", side="buy", asset="AAPL",
                strike_price=150.0, premium=500.0, expiration_date="2025-12-15",
                execution_date="2025-07-15", strategy="covered_call", status="open", counterparty="BANK"
            ),
            DerivativeTransaction(
                customer_oid="550e8400-e29b-41d4-a716-446655440001", type="option", side="sell", asset="SPY",
                strike_price=420.0, premium=300.0, expiration_date="2025-09-15",
                execution_date="2025-06-15", strategy="cash_secured_put", status="open", counterparty="BROKER"
            ),
            
            # Customer 2 - aggressive derivatives trading
            DerivativeTransaction(
                customer_oid="550e8400-e29b-41d4-a716-446655440002", type="option", side="buy", asset="TSLA",
                strike_price=200.0, premium=1500.0, expiration_date="2025-11-15",
                execution_date="2025-05-15", strategy="long_call", status="open", counterparty="EXCHANGE"
            ),
            DerivativeTransaction(
                customer_oid="550e8400-e29b-41d4-a716-446655440002", type="future", side="buy", asset="GOLD",
                strike_price=2100.0, premium=2000.0, expiration_date="2025-10-15",
                execution_date="2025-04-15", strategy="hedge", status="open", counterparty="EXCHANGE"
            ),
        ]
        for derivative in derivatives:
            session.add(derivative)
        
        session.commit()
        print("✅ Sample data created successfully!")
        print("📋 Created data for customers:")
        print("  • 550e8400-e29b-41d4-a716-446655440001 - John Doe")
        print("  • 550e8400-e29b-41d4-a716-446655440002 - Jane Smith") 
        print("  • 550e8400-e29b-41d4-a716-446655440003 - Robert Johnson")
        print("  • 550e8400-e29b-41d4-a716-446655440004 - ABC Corporation")
        print("  • 550e8400-e29b-41d4-a716-446655440005 - Michael Chen")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error creating sample data: {e}")
    finally:
        session.close()

def reset_and_seed_database():
    """Reset the database and create fresh sample data"""
    reset_database()
    create_sample_data()

sqlite_file = "bank.db"
engine = create_engine(f"sqlite:///{sqlite_file}", echo=True)