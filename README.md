# Dummy Bank API Documentation

A comprehensive FastAPI-based banking API designed for portfolio analysis and customer data management, optimized for CustomerOID-based operations and MCP (Model Context Protocol) server integration.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Conda environment (recommended)

### Installation & Setup

1. **Set up environment**:

   ```bash
   conda create -n openbanking-backend python=3.11
   conda activate openbanking-backend
   ```

2. **Install dependencies**:

   ```bash
   pip install fastapi uvicorn sqlmodel sqlite3
   ```

3. **Start the API server**:

   ```bash
   conda run -n openbanking-backend uvicorn main:app --host 127.0.0.1 --port 3000 --reload
   ```

4. **Access API documentation**:

   - Swagger UI: <http://127.0.0.1:3000/docs>
   - ReDoc: <http://127.0.0.1:3000/redoc>

## 📋 API Overview

### Base URL

```text
http://127.0.0.1:3000
```

### Core Features

- **CustomerOID-centric design**: All operations are based on unique Customer IDs (UUID format)
- **Comprehensive portfolio data**: Assets, transactions, bank accounts, spending patterns, derivatives
- **Customer lifecycle management**: Registration, deletion, and data retrieval
- **MCP server integration ready**: Optimized responses for analysis agents
- **SQLite database**: Local file-based storage with indexed CustomerOID fields

## 🔑 CustomerOID Format

The API uses UUID format for CustomerOIDs:

- **Format**: `550e8400-e29b-41d4-a716-446655440000`
- **Generation**: Automatic UUID generation for new customers
- **Validation**: Strict UUID format validation with backward compatibility

## 📊 Data Models

### User

- `customer_oid` (UUID): Unique customer identifier
- `name` (string): Customer name

### Asset Holdings

- Asset type, symbol, quantity, current value
- Market data and performance metrics

### Bank Accounts

- Account details, balances, institution information
- Multiple accounts per customer supported

### Transactions

- Transaction history with amounts, dates, descriptions
- Categorized for analysis

### Spending Patterns

- Spending categories and amounts
- Useful for financial behavior analysis

### Derivative Transactions

- Options, futures, and other derivative instruments
- Advanced portfolio components

## 🛠 API Endpoints

### Customer Management

#### `GET /customers`
List all registered customers.

**Response:**
```json
[
  {
    "customer_oid": "550e8400-e29b-41d4-a716-446655440000",
    "name": "John Doe"
  }
]
```

#### `POST /register-customer`
Register a new customer in the system.

**Request Body:**
```json
{
  "name": "John Doe",
  "customer_oid": "550e8400-e29b-41d4-a716-446655440000"  // Optional
}
```

**Response:**
```json
{
  "customer_oid": "550e8400-e29b-41d4-a716-446655440000",
  "name": "John Doe",
  "message": "Customer registered successfully"
}
```

**Features:**
- Auto-generates UUID if `customer_oid` not provided
- Validates name (minimum 2 characters)
- Prevents duplicate registrations
- Returns comprehensive error messages

#### `DELETE /customer/{customer_oid}`
Delete a customer and all associated data.

**⚠️ WARNING**: This permanently deletes all portfolio data for the customer.

**Response:**
```json
{
  "customer_oid": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Customer and all associated data deleted successfully"
}
```

#### `GET /customer/{customer_oid}/exists`
Quick check if a CustomerOID exists in the system.

**Response:**
```json
{
  "customer_oid": "550e8400-e29b-41d4-a716-446655440000",
  "exists": true,
  "name": "John Doe"
}
```

### Portfolio Data

#### `GET /user-portfolio/{customer_oid}`
Get comprehensive portfolio data for a customer.

**Response Structure:**
```json
{
  "customer_oid": "550e8400-e29b-41d4-a716-446655440000",
  "user": {
    "name": "John Doe",
    "customer_oid": "550e8400-e29b-41d4-a716-446655440000"
  },
  "assets": [
    {
      "id": 1,
      "customer_oid": "550e8400-e29b-41d4-a716-446655440000",
      "asset_type": "stock",
      "symbol": "AAPL",
      "quantity": 100.0,
      "current_value": 15000.0
    }
  ],
  "bank_accounts": [
    {
      "id": 1,
      "customer_oid": "550e8400-e29b-41d4-a716-446655440000",
      "account_number": "ACC-001",
      "account_type": "checking",
      "balance": 25000.0,
      "institution": {
        "id": 1,
        "name": "First National Bank",
        "routing_number": "123456789"
      }
    }
  ],
  "transactions": [...],
  "spending": [...],
  "derivative_transactions": [...],
  "portfolio_summary": {
    "customer_oid": "550e8400-e29b-41d4-a716-446655440000",
    "total_cash_balance": 25000.0,
    "total_spending": 2500.0,
    "total_assets": 3,
    "total_accounts": 2,
    "total_transactions": 10,
    "total_spending_categories": 5,
    "total_derivative_positions": 2,
    "has_data": {
      "assets": true,
      "accounts": true,
      "transactions": true,
      "spending": true,
      "derivatives": true
    }
  }
}
```

### System Health

#### `GET /health`
Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "healthy",
  "service": "dummy-bank-api"
}
```

## 🗄 Database Schema

### Tables
- **users**: Customer information with UUID CustomerOID (indexed)
- **assets**: Investment holdings per customer
- **bank_accounts**: Banking account details
- **institutions**: Bank and financial institution data
- **transactions**: Transaction history
- **spending**: Spending pattern data
- **derivative_transactions**: Derivative instrument trades

### Key Features
- **Indexed CustomerOID**: All tables indexed on `customer_oid` for fast queries
- **Referential integrity**: Proper foreign key relationships
- **SQLModel ORM**: Type-safe database operations
- **Automatic seeding**: Sample data for testing and development

## 🧪 Testing

### Test Files Included

1. **`test_api.py`**: Comprehensive API testing
2. **`test_registration.py`**: User registration workflow testing
3. **`reset_database.py`**: Database reset and reseeding

### Running Tests

```bash
# Test API endpoints
conda run -n openbanking-backend python test_api.py

# Test registration functionality
conda run -n openbanking-backend python test_registration.py

# Reset database with sample data
conda run -n openbanking-backend python reset_database.py
```

## 🔧 Configuration

### Environment Variables
- **Port**: Default 3000 (configurable)
- **Host**: Default 127.0.0.1
- **Database**: SQLite file `banking.db`

### Sample Data
The API includes comprehensive sample data for 5 customers:
- Complete portfolio data
- Multiple asset types
- Various transaction patterns
- Diverse spending categories
- Derivative instruments

## 🎯 MCP Server Integration

This API is optimized for MCP (Model Context Protocol) server integration:

### Key Features for MCP
- **CustomerOID-centric design**: Easy customer identification
- **Comprehensive data structure**: All portfolio data in single endpoint
- **Analysis-ready format**: Pre-calculated summaries and metrics
- **Efficient queries**: Indexed database operations
- **Standardized responses**: Consistent JSON structure

### Recommended MCP Usage
1. **Customer Discovery**: Use `/customers` to list available customers
2. **Portfolio Analysis**: Use `/user-portfolio/{customer_oid}` for complete data
3. **Customer Management**: Use registration/deletion endpoints for lifecycle management
4. **Health Monitoring**: Use `/health` for system status

## 🚨 Error Handling

### Common Error Codes
- **400**: Invalid CustomerOID format or validation errors
- **404**: Customer not found
- **409**: Duplicate customer registration
- **500**: Internal server errors

### Error Response Format
```json
{
  "detail": "Customer with CustomerOID '550e8400-e29b-41d4-a716-446655440000' not found"
}
```

## 🔄 Development Workflow

### Making Changes
1. **Edit code**: Modify `main.py` or `db.py`
2. **Restart server**: Server restart required for validation changes
3. **Test changes**: Run test scripts to verify functionality
4. **Reset data**: Use reset script if database schema changes

### Adding New Customers
```bash
# Method 1: Use registration endpoint
curl -X POST "http://127.0.0.1:3000/register-customer" \
     -H "Content-Type: application/json" \
     -d '{"name": "New Customer"}'

# Method 2: Specify custom UUID
curl -X POST "http://127.0.0.1:3000/register-customer" \
     -H "Content-Type: application/json" \
     -d '{"name": "New Customer", "customer_oid": "550e8400-e29b-41d4-a716-446655440001"}'
```

## 📝 Best Practices

### CustomerOID Management
- Always use UUID format for new customers
- Validate CustomerOID before database operations
- Use the provided validation function consistently

### Database Operations
- Use dependency injection for database sessions
- Implement proper error handling and rollbacks
- Close sessions properly to prevent leaks

### API Design
- Follow RESTful conventions
- Provide comprehensive error messages
- Include validation for all inputs
- Document all endpoints clearly

## 🤝 Contributing

1. Follow the existing code structure
2. Add tests for new functionality
3. Update documentation for API changes
4. Ensure CustomerOID validation is maintained
5. Test with sample data before deployment

## 📄 License

This is a dummy/example implementation for development and testing purposes.

---

**Need help?** Check the Swagger documentation at http://127.0.0.1:3000/docs when the server is running.
