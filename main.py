from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from supabase_client import get_supabase_client
from cashflow_logic import (
    validate_transactions,
    sort_transactions_chronologically,
    apply_constraints,
    minimize_transactions
)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
supabase = get_supabase_client()

class TransactionInput(BaseModel):
    sender: str
    receiver: str
    amount: float = Field(..., gt=0)
    timestamp: Optional[str] = None
    due_date: Optional[str] = None
    interest_rate: Optional[float] = None
    penalty: Optional[float] = None

@app.post("/transactions/", response_model=dict)
def add_transactions(transactions: List[TransactionInput]):
    data = [t.dict() for t in transactions]
    try:
        for tx in data:
            if not tx.get("timestamp"):
                tx["timestamp"] = datetime.utcnow().isoformat()
        result = supabase.table("transactions").insert(data).execute()
        return {"status": "success", "data": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/transactions/", response_model=List[dict])
def get_transactions():
    try:
        result = supabase.table("transactions").select("*").execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/settle/", response_model=List[dict])
def settle(transactions: List[TransactionInput]):
    txs = [t.dict() for t in transactions]
    valid_txs = validate_transactions(txs)
    if not valid_txs:
        raise HTTPException(status_code=400, detail="No valid transactions provided.")
    # Optional: sort and apply constraints before minimizing
    valid_txs = sort_transactions_chronologically(valid_txs)
    valid_txs = apply_constraints(valid_txs)
    result = minimize_transactions(valid_txs)
    return result

@app.get("/")
def root():
    return {"message": "Cash Flow Minimizer API is running!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
