#!/usr/bin/env python3
"""
Script to run the dummy bank API server on port 3000
"""
import uvicorn
from db import create_sample_data

if __name__ == "__main__":
    print("Creating sample data...")
    create_sample_data()
    
    print("Starting Dummy Bank API on port 3000...")
    print("Portfolio endpoint: http://localhost:3000/user-portfolio/CUST001")
    print("Health check: http://localhost:3000/health")
    print("API docs: http://localhost:3000/docs")
    
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)
