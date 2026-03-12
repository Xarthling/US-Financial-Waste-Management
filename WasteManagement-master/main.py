from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.responses import JSONResponse
from apscheduler.schedulers.background import BackgroundScheduler
from utils import usaspending_schedular, treasury_schedular, calculate_metrics_with_openai, fetch_latest_toptier_agencies
from fastapi.middleware.cors import CORSMiddleware
import json
from datetime import datetime, timedelta,timezone

app = FastAPI()
cache = {
    "data": None,
    "expires_at": None
}
# Initialize Scheduler
def initialize_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.start()

    # Adding scheduled jobs
    def schedule_jobs():
        scheduler.add_job(usaspending_schedular, "interval", days=1, id="usaspending_schedular")
        scheduler.add_job(treasury_schedular, "interval", days=1, id="treasury_schedular")

    schedule_jobs()
    return scheduler

scheduler = initialize_scheduler()

# Mock Data
def get_mock_data():
    return {
        "expenses": [
            {
                "project": "Education Reform",
                "tags": ["education", "reform"],
                "timestamp": "2024-12-28",
                "amount": 1200000,
            }
        ],
        "deficit": {"total_deficit": "$3251656515"},
        "metrics": {"total_spent": "$3.2T", "total_waste": "$284B"},
    }

mock_data = get_mock_data()

# CORS Configuration
def setup_cors():
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Replace with specific origins in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

setup_cors()


# Helper Functions
def safely_parse_dates(start_date: str, end_date: str):
    try:
        parsed_start_date = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
        parsed_end_date = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None
        return parsed_start_date, parsed_end_date
    except ValueError as ve:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.") from ve


def process_filtered_expenses(expenses):
    for expense in expenses:
        if "fetched_at" in expense and isinstance(expense["fetched_at"], datetime):
            expense["fetched_at"] = expense["fetched_at"].isoformat()
    return expenses


# Core Logic
def get_grok_response():
    try:
        # Check if cache is valid
        if cache["data"] and cache["expires_at"] > datetime.now(timezone.utc):
            print("Returning cached response.")
            return cache["data"]

        # Fetch data from external sources
        print("Fetching new data...")
        data = fetch_latest_toptier_agencies()

        # Calculate metrics using OpenAI
        response = calculate_metrics_with_openai(data)
        print("Raw LLM response:", response)

        # Store response in cache with expiry
        cache["data"] = response
        cache["expires_at"] = datetime.now(timezone.utc) + timedelta(minutes=5)

        return response

    except json.JSONDecodeError as jde:
        raise HTTPException(status_code=500, detail=f"JSON parsing failed: {jde}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoints
@app.post("/api/expenses", response_class=JSONResponse)
def get_expenses(payload: dict = Body(...)):
    try:
        search = payload.get("search", "")
        start_date = payload.get("startDate", "")
        end_date = payload.get("endDate", "")

        # Parse dates
        parsed_start_date, parsed_end_date = safely_parse_dates(start_date, end_date)

        # Fetch and filter expenses
        filtered_expenses = fetch_latest_toptier_agencies(
            limit=10, search=search, start_date=parsed_start_date, end_date=parsed_end_date
        )

        # Process expenses for consistent formatting
        formatted_expenses = process_filtered_expenses(filtered_expenses)

        return JSONResponse(content=formatted_expenses)

    except Exception as e:
        print("Error occurred:", e)
        raise HTTPException(status_code=500, detail="An error occurred while processing expenses.")


@app.get("/api/metrics", response_class=JSONResponse)
def get_metrics():
    try:
        metrics = get_grok_response()

        # Construct response with mock metrics fallback
        formatted_metrics = {
            "total_spent": metrics.get("total_spending", mock_data["metrics"]["total_spent"]),
            "total_waste": metrics.get("total_waste", mock_data["metrics"]["total_waste"]),
        }
        return JSONResponse(content=formatted_metrics)
    except Exception as e:
        print("Error in /api/metrics:", e)
        raise HTTPException(status_code=500, detail=f"Metrics retrieval failed: {e}")


@app.get("/api/deficit", response_class=JSONResponse)
def get_deficit():
    try:
        print("Getting Deficit")
        metrics = get_grok_response()

        # Construct response with mock deficit fallback
        formatted_deficit = {"total_deficit": metrics.get("total_deficit", mock_data["deficit"]["total_deficit"])}
        return JSONResponse(content=formatted_deficit)
    except Exception as e:
        print("Error in /api/deficit:", e)
        raise HTTPException(status_code=500, detail=f"Deficit retrieval failed: {e}")
