from fastapi import FastAPI, HTTPException, Depends, Header, Query
from dotenv import load_dotenv
from pathlib import Path
import os
import pandas as pd
import json
from typing import Optional

# Load environment variables
load_dotenv()

# API key check supporting both header and query param
# Removed convert_underscores=False to allow x-api-key to work in browsers

def verify_api_key(
    x_api_key: Optional[str] = Header(default=None),
    api_key: Optional[str] = Query(default=None)
):
    key = x_api_key or api_key
    if key != os.getenv("UFC_API_KEY"):
        raise HTTPException(status_code=401, detail="Invalid API Key")

app = FastAPI(
    title="UFC Fighter Stats API 💪",
    description="Programmatic access to UFC fighter stats from a local dataset.",
    version="1.0.0"
)

# CSV path (assumes project root is ufc_stats_api/)
csv_path = Path(__file__).resolve().parent.parent / "data" / "ufc_fighters_stats.csv"

# Load data
try:
    df = pd.read_csv(csv_path)
    df = df.fillna("")  # Replace NaN with empty string
except FileNotFoundError:
    raise RuntimeError(f"CSV file not found at: {csv_path}")
except Exception as e:
    raise RuntimeError(f"Error reading CSV file: {e}")

@app.get("/", summary="Root Welcome Message")
def root():
    return {"message": "Welcome to the UFC Fighter Stats API 💪"}

@app.get("/fighters", summary="List all fighters", description="Returns a list of all fighters with their stats.")
def get_fighters(api_key: str = Depends(verify_api_key)):
    try:
        return json.loads(df.to_json(orient="records"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/fighters/{name}", summary="Get a fighter by name", description="Returns detailed stats for a specific fighter by name.")
def get_fighter_by_name(name: str, api_key: str = Depends(verify_api_key)):
    result = df[df['fighter_name'].str.lower() == name.lower()]
    if result.empty:
        raise HTTPException(status_code=404, detail="Fighter not found")
    return json.loads(result.to_json(orient="records"))[0]

@app.get("/summary/striking", summary="Striking summary", description="Get average striking stats across all fighters.")
def get_striking_summary(api_key: str = Depends(verify_api_key)):
    stats = df[['strikes_landed_per_min', 'strike_accuracy_pct', 'strikes_absorbed_per_min', 'strike_defense_pct']]
    summary = stats.astype(float).mean().to_dict()
    return {"average_striking_stats": summary}

@app.get("/summary/grappling", summary="Grappling summary", description="Get average grappling stats across all fighters.")
def get_grappling_summary(api_key: str = Depends(verify_api_key)):
    stats = df[['takedowns_per_15min', 'takedown_accuracy_pct', 'takedown_defense_pct', 'submission_attempts_per_15min']]
    summary = stats.astype(float).mean().to_dict()
    return {"average_grappling_stats": summary}

@app.get("/search", summary="Search fighters", description="Search fighters by partial name match.")
def search_fighters(query: str, api_key: str = Depends(verify_api_key)):
    result = df[df['fighter_name'].str.contains(query, case=False)]
    if result.empty:
        raise HTTPException(status_code=404, detail="No fighters matched your search")
    return json.loads(result.to_json(orient="records"))
