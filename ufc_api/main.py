from fastapi import FastAPI, HTTPException, Depends, Header, Query, Request
from dotenv import load_dotenv
from pathlib import Path
import os
import pandas as pd
import json
from typing import Optional
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import logging

# Load environment variables
load_dotenv()

# Set up logging
log_dir = Path(__file__).resolve().parent.parent / "logs"
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    filename=log_dir / "api.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(
    title="UFC Fighter Stats API 💪",
    description="Programmatic access to UFC fighter stats from a local dataset.",
    version="1.0.0"
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# API key verification
def verify_api_key(
    x_api_key: Optional[str] = Header(default=None, convert_underscores=False),
    api_key: Optional[str] = Query(default=None)
):
    key = x_api_key or api_key
    if key != os.getenv("UFC_API_KEY"):
        raise HTTPException(status_code=401, detail="Invalid API Key")

# Load CSV
csv_path = Path(__file__).resolve().parent.parent / "data" / "ufc_fighters_stats.csv"
try:
    df = pd.read_csv(csv_path).fillna("")
except Exception as e:
    raise RuntimeError(f"CSV load error: {e}")

# Logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.info(f"{request.method} {request.url}")
    response = await call_next(request)
    logging.info(f"Completed with status {response.status_code}")
    return response

@app.get("/", summary="Root Welcome Message")
@limiter.limit("10/minute")
def root(request: Request):  # <- this is REQUIRED
    return {"message": "Welcome to the UFC Fighter Stats API 💪"}

@app.get("/fighters", summary="List all fighters")
@limiter.limit("5/minute")
def get_fighters(request: Request, api_key: str = Depends(verify_api_key)):  # ✅
    return json.loads(df.to_json(orient="records"))

@app.get("/fighters/{name}", summary="Get a fighter by name")
@limiter.limit("5/minute")
def get_fighter_by_name(request: Request, name: str, api_key: str = Depends(verify_api_key)):  # ✅
    result = df[df['fighter_name'].str.lower() == name.lower()]
    if result.empty:
        raise HTTPException(status_code=404, detail="Fighter not found")
    return json.loads(result.to_json(orient="records"))[0]

@app.get("/summary/striking", summary="Striking summary")
@limiter.limit("3/minute")
def get_striking_summary(request: Request, api_key: str = Depends(verify_api_key)):  # ✅
    stats = df[['strikes_landed_per_min', 'strike_accuracy_pct', 'strikes_absorbed_per_min', 'strike_defense_pct']]
    return {"average_striking_stats": stats.astype(float).mean().to_dict()}

@app.get("/summary/grappling", summary="Grappling summary")
@limiter.limit("3/minute")
def get_grappling_summary(request: Request, api_key: str = Depends(verify_api_key)):  # ✅
    stats = df[['takedowns_per_15min', 'takedown_accuracy_pct', 'takedown_defense_pct', 'submission_attempts_per_15min']]
    return {"average_grappling_stats": stats.astype(float).mean().to_dict()}

@app.get("/search", summary="Search fighters")
@limiter.limit("5/minute")
def search_fighters(request: Request, query: str, api_key: str = Depends(verify_api_key)):  # ✅
    result = df[df['fighter_name'].str.contains(query, case=False)]
    if result.empty:
        raise HTTPException(status_code=404, detail="No fighters matched your search")
    return json.loads(result.to_json(orient="records"))

@app.get("/stats/summary", summary="Get summary statistics")
@limiter.limit("5/minute")
def get_stats_summary(api_key: str = Depends(verify_api_key)):
    try:
        summary = {
            "total_fighters": len(df),
            "average_height": pd.to_numeric(df["Height_cms"], errors="coerce").mean(skipna=True),
            "average_weight": pd.to_numeric(df["Weight_lbs"], errors="coerce").mean(skipna=True),
            "average_reach": pd.to_numeric(df["Reach_in"], errors="coerce").mean(skipna=True)
        }
        return summary
    except Exception as e:
        logging.exception("Error generating summary stats")
        raise HTTPException(status_code=500, detail=f"Error generating summary: {e}")

