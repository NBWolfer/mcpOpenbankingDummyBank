from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import select
from db import (
    init_db, get_session, User, Asset, Transaction, Spending, 
    BankAccount, Institution, DerivativeTransaction
)
import uvicorn
from typing import Dict, Any, List, Optional
import re
import uuid
from pydantic import BaseModel

app = FastAPI(
    title="Dummy Bank API",
    description="API for portfolio analysis and customer data - CustomerOID based",
    version="1.0.0"
)

# Pydantic models for API requests
class UserRegistrationRequest(BaseModel):
    name: str
    customer_oid: Optional[str] = None  # If not provided, will generate UUID
    
class UserRegistrationResponse(BaseModel):
    customer_oid: str
    name: str
    message: str

@app.on_event("startup")
def on_startup():
    init_db()

def validate_customer_oid(customer_oid: str) -> str:
    """Validate CustomerOID format"""
    if not customer_oid:
        raise HTTPException(status_code=400, detail="CustomerOID cannot be empty")
    
    # UUID format validation (36 characters with hyphens) or alphanumeric format
    import uuid
    try:
        # Try to parse as UUID first
        parsed_uuid = uuid.UUID(customer_oid)
        return customer_oid
    except ValueError:
        # Fall back to alphanumeric validation for backward compatibility
        if not re.match(r'^[A-Z0-9-]{8,36}$', customer_oid):
            raise HTTPException(
                status_code=400, 
                detail="Invalid CustomerOID format. Expected UUID format (e.g., 550e8400-e29b-41d4-a716-446655440000) or alphanumeric string"
            )
        return customer_oid

def get_db_session():
    """Dependency to get database session"""
    session = get_session()
    try:
        yield session
    finally:
        session.close()

@app.get("/user-portfolio/{customer_oid}")
def get_user_portfolio(customer_oid: str, session = Depends(get_db_session)) -> Dict[str, Any]:
    """
    Get comprehensive portfolio data for a customer by CustomerOID including:
    - User information
    - Assets holdings
    - Bank accounts
    - Transaction history
    - Spending patterns
    - Derivative transactions
    """
    # Validate CustomerOID format
    customer_oid = validate_customer_oid(customer_oid)
    
    # Get user
    user = session.exec(select(User).where(User.customer_oid == customer_oid)).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with CustomerOID '{customer_oid}' not found")

    # Get all portfolio data efficiently using indexed customer_oid
    assets = session.exec(select(Asset).where(Asset.customer_oid == customer_oid)).all()
    transactions = session.exec(select(Transaction).where(Transaction.customer_oid == customer_oid)).all()
    spending = session.exec(select(Spending).where(Spending.customer_oid == customer_oid)).all()
    bank_accounts = session.exec(select(BankAccount).where(BankAccount.customer_oid == customer_oid)).all()
    derivative_transactions = session.exec(select(DerivativeTransaction).where(DerivativeTransaction.customer_oid == customer_oid)).all()
    
    # Get institutions for bank accounts
    institution_ids = {acc.institution_id for acc in bank_accounts}
    institutions = {}
    if institution_ids:
        inst_results = session.exec(select(Institution).where(Institution.id.in_(institution_ids))).all()
        institutions = {inst.id: inst for inst in inst_results}

    # Calculate total portfolio value for analysis
    total_cash = sum(acc.balance for acc in bank_accounts)
    total_spending = sum(s.amount for s in spending)
    
    # Build comprehensive response optimized for MCP server analysis
    return {
        "customer_oid": customer_oid,
        "user": {
            "name": user.name,
            "customer_oid": user.customer_oid
        },
        "assets": [asset.dict() for asset in assets],
        "bank_accounts": [
            {
                **account.dict(),
                "institution": institutions.get(account.institution_id, {}).dict() if account.institution_id in institutions else None
            }
            for account in bank_accounts
        ],
        "transactions": [transaction.dict() for transaction in transactions],
        "spending": [spend.dict() for spend in spending],
        "derivative_transactions": [deriv.dict() for deriv in derivative_transactions],
        "portfolio_summary": {
            "customer_oid": customer_oid,
            "total_cash_balance": total_cash,
            "total_spending": total_spending,
            "total_assets": len(assets),
            "total_accounts": len(bank_accounts),
            "total_transactions": len(transactions),
            "total_spending_categories": len(set(s.category for s in spending)),
            "total_derivative_positions": len(derivative_transactions),
            "has_data": {
                "assets": len(assets) > 0,
                "accounts": len(bank_accounts) > 0,
                "transactions": len(transactions) > 0,
                "spending": len(spending) > 0,
                "derivatives": len(derivative_transactions) > 0
            }
        }
    }

@app.get("/customers")
def list_customers(session = Depends(get_db_session)) -> List[Dict[str, str]]:
    """
    List all customers with their CustomerOIDs - useful for MCP server discovery
    """
    users = session.exec(select(User)).all()
    return [
        {
            "customer_oid": user.customer_oid,
            "name": user.name
        }
        for user in users
    ]

@app.get("/customer/{customer_oid}/exists")
def check_customer_exists(customer_oid: str, session = Depends(get_db_session)) -> Dict[str, Any]:
    """
    Quick check if a CustomerOID exists in the system
    """
    customer_oid = validate_customer_oid(customer_oid)
    
    user = session.exec(select(User).where(User.customer_oid == customer_oid)).first()
    return {
        "customer_oid": customer_oid,
        "exists": user is not None,
        "name": user.name if user else None
    }

@app.post("/register-customer", response_model=UserRegistrationResponse)
def register_customer(user_data: UserRegistrationRequest, session = Depends(get_db_session)) -> UserRegistrationResponse:
    """
    Register a new customer in the system
    - If customer_oid is provided, it will be validated and used
    - If customer_oid is not provided, a new UUID will be generated
    - Returns the registered customer information
    """
    try:
        # Generate CustomerOID if not provided
        if user_data.customer_oid:
            customer_oid = validate_customer_oid(user_data.customer_oid)
        else:
            customer_oid = str(uuid.uuid4())
        
        # Check if customer already exists
        existing_user = session.exec(select(User).where(User.customer_oid == customer_oid)).first()
        if existing_user:
            raise HTTPException(
                status_code=409, 
                detail=f"Customer with CustomerOID '{customer_oid}' already exists"
            )
        
        # Validate name
        if not user_data.name or len(user_data.name.strip()) < 2:
            raise HTTPException(
                status_code=400,
                detail="Name must be at least 2 characters long"
            )
        
        # Create new user
        new_user = User(
            customer_oid=customer_oid,
            name=user_data.name.strip()
        )
        
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        
        return UserRegistrationResponse(
            customer_oid=customer_oid,
            name=new_user.name,
            message="Customer registered successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to register customer: {str(e)}"
        )

@app.delete("/customer/{customer_oid}")
def delete_customer(customer_oid: str, session = Depends(get_db_session)) -> Dict[str, str]:
    """
    Delete a customer and all associated data from the system
    WARNING: This will permanently delete all portfolio data for the customer
    """
    customer_oid = validate_customer_oid(customer_oid)
    
    try:
        # Check if customer exists
        user = session.exec(select(User).where(User.customer_oid == customer_oid)).first()
        if not user:
            raise HTTPException(
                status_code=404,
                detail=f"Customer with CustomerOID '{customer_oid}' not found"
            )
        
        # Delete all associated data
        # Delete assets
        assets = session.exec(select(Asset).where(Asset.customer_oid == customer_oid)).all()
        for asset in assets:
            session.delete(asset)
        
        # Delete transactions
        transactions = session.exec(select(Transaction).where(Transaction.customer_oid == customer_oid)).all()
        for transaction in transactions:
            session.delete(transaction)
        
        # Delete spending
        spending = session.exec(select(Spending).where(Spending.customer_oid == customer_oid)).all()
        for spend in spending:
            session.delete(spend)
        
        # Delete bank accounts
        bank_accounts = session.exec(select(BankAccount).where(BankAccount.customer_oid == customer_oid)).all()
        for account in bank_accounts:
            session.delete(account)
        
        # Delete derivative transactions
        derivatives = session.exec(select(DerivativeTransaction).where(DerivativeTransaction.customer_oid == customer_oid)).all()
        for derivative in derivatives:
            session.delete(derivative)
        
        # Delete user
        session.delete(user)
        session.commit()
        
        return {
            "customer_oid": customer_oid,
            "message": "Customer and all associated data deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete customer: {str(e)}"
        )

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "dummy-bank-api"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
