from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from datetime import datetime, timezone
import requests

app = FastAPI()

# MongoDB connection
MONGO_URI = "mongodb://localhost:27017"  # Replace with your MongoDB URI
client = MongoClient(MONGO_URI)
db = client.government_database

# Base URL for USAspending.gov APIs
USASPENDING_BASE_URL = "https://api.usaspending.gov/api/v2"

templates = Jinja2Templates(directory="template")

@app.get("/usaspending/agencies", response_class=HTMLResponse)
def get_agencies_list(request: Request):
    try:
        endpoint = f"{USASPENDING_BASE_URL}/references/toptier_agencies/"
        response = requests.get(endpoint)
        response.raise_for_status()
        data = response.json()

        # Prepare filtered data for MongoDB
        agencies = []
        for agency in data.get("results", []):
            agencies.append({
                "agency_name": agency.get("agency_name"),
                "abbreviation": agency.get("abbreviation"),
                "outlay_amount": agency.get("outlay_amount"),
                "obligated_amount": agency.get("obligated_amount"),
                "congressional_justification_url": agency.get("congressional_justification_url"),
                "toptier_code": agency.get("toptier_code"),  
                "fetched_at": datetime.now(timezone.utc)  
            })

        # Insert data into MongoDB
        if agencies:
            db.toptier_agencies.delete_many({})  # Clear old data (optional)
            db.toptier_agencies.insert_many(agencies)

        # Retrieve stored data for display
        stored_agencies = list(db.toptier_agencies.find({}, {
            "_id": 0,
            "agency_name": 1,
            "abbreviation": 1,
            "outlay_amount": 1,
            "obligated_amount": 1,
            "congressional_justification_url": 1,
            "toptier_code": 1  # Ensure to retrieve this field
        }))

        # Render the HTML template with the agencies data
        return templates.TemplateResponse("usa.html", {"request": request, "agencies": stored_agencies})

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data from API: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")



# Function to get agency overview information
@app.get("/usaspending/agency/{toptier_agency_code}")
def get_agency_overview(toptier_agency_code: str):
    try:
        endpoint = f"{USASPENDING_BASE_URL}/agency/{toptier_agency_code}/"
        response = requests.get(endpoint)
        response.raise_for_status()

        data = response.json()
        return {"agency_overview": data}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


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
