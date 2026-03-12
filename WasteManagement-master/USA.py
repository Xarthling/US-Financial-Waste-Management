from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from datetime import datetime, timezone
import requests

app = FastAPI()

# MongoDB Connection
MONGO_URI = "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)
db = client.government_dashboard

# Jinja2 Templates Directory
templates = Jinja2Templates(directory="template")

# Base URL for USAspending API
USASPENDING_BASE_URL = "https://api.usaspending.gov/api/v2"


@app.get("/usaspending/agencies", response_class=HTMLResponse)
def get_agencies_list(request: Request):
    try:
        # endpoint = f"{USASPENDING_BASE_URL}/references/toptier_agencies/"
        
        # response = requests.get(endpoint, timeout=10)
        # response.raise_for_status()
        # data = response.json()

        # agencies = [
        #     {
        #         "agency_id": agency.get("agency_id"),
        #         "toptier_code": agency.get("toptier_code"),
        #         "abbreviation": agency.get("abbreviation"),
        #         "agency_name": agency.get("agency_name"),
        #         "congressional_justification_url": agency.get("congressional_justification_url"),
        #         "active_fy": agency.get("active_fy"),
        #         "active_fq": agency.get("active_fq"),
        #         "outlay_amount": agency.get("outlay_amount"),
        #         "obligated_amount": agency.get("obligated_amount"),
        #         "budget_authority_amount": agency.get("budget_authority_amount"),
        #         "current_total_budget_authority_amount": agency.get("current_total_budget_authority_amount"),
        #         "percentage_of_total_budget_authority": agency.get("percentage_of_total_budget_authority"),
        #         "agency_slug": agency.get("agency_slug"),
        #         "fetched_at": datetime.now(timezone.utc)
        #     }
        #     for agency in data.get("results", [])
        # ]

        # if agencies:
        #     db.toptier_agencies.delete_many({})  
        #     db.toptier_agencies.insert_many(agencies)  
        stored_agencies = list(db.toptier_agencies.find({}, {"_id": 0}))

        return templates.TemplateResponse("usa.html", {"request": request, "agencies": stored_agencies})

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="API request timed out")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data from API: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")




@app.get("/usaspending/agency/{toptier_agency_code}")
def get_agency_overview(toptier_agency_code: str):
    try:
        agency = db.toptier_agencies.find_one({"toptier_code": toptier_agency_code}, {"_id": 0})
        
        if not agency:
            raise HTTPException(status_code=404, detail="Agency not found")

        return {"agency": agency}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")



# Function to get agency summary information for sub-agencies
@app.get("/usaspending/agency/{toptier_agency_code}/awards")
def get_agency_awards_summary(toptier_agency_code: str):
    try:
        endpoint = f"{USASPENDING_BASE_URL}/agency/{toptier_agency_code}/awards/"
        response = requests.get(endpoint)
        response.raise_for_status()

        data = response.json()
        return {"agency_awards_summary": data}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

# Function to get count of new awards for an agency
@app.get("/usaspending/agency/{toptier_agency_code}/awards/new/count")
def get_new_awards_count(toptier_agency_code: str):
    try:
        endpoint = f"{USASPENDING_BASE_URL}/agency/{toptier_agency_code}/awards/new/count/"
        response = requests.get(endpoint)
        response.raise_for_status()

        data = response.json()
        return {"new_awards_count": data}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

# Function to get budgetary resources for an agency
@app.get("/usaspending/agency/{toptier_agency_code}/budgetary-resources")
def get_budgetary_resources(toptier_agency_code: str):
    try:
        endpoint = f"{USASPENDING_BASE_URL}/agency/{toptier_agency_code}/budgetary_resources/"
        response = requests.get(endpoint)
        response.raise_for_status()

        data = response.json()
        return {"budgetary_resources": data}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

# Function to get obligations by award category
@app.get("/usaspending/agency/{toptier_agency_code}/obligations-by-award-category")
def get_obligations_by_award_category(toptier_agency_code: str):
    try:
        endpoint = f"{USASPENDING_BASE_URL}/agency/{toptier_agency_code}/obligations_by_award_category/"
        response = requests.get(endpoint)
        response.raise_for_status()

        data = response.json()
        return {"obligations_by_award_category": data}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

# Function to get spending by category
@app.get("/usaspending/category-breakdown")
def get_spending_by_category():
    try:
        endpoint = f"{USASPENDING_BASE_URL}/search/spending_by_category/"
        response = requests.get(endpoint)
        response.raise_for_status()

        data = response.json()
        spending_data = data.get("results", [])
        return {"spending_by_category": spending_data}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
