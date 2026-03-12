from pymongo import MongoClient
import requests
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime, timezone
import os
import re

from dotenv import load_dotenv

load_dotenv()



# MongoDB Connection
MONGO_URI = "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)
db = client.government_dashboard

# Base URLs
USASPENDING_BASE_URL = "https://api.usaspending.gov/api/v2"
TREASURY_BASE_URL = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1"

# Vector Space Directory
VECTOR_SPACE_PATH = "vector_db"

def usaspending_schedular():
    try:
        print('run usa')
        endpoint = f"{USASPENDING_BASE_URL}/references/toptier_agencies/"
        response = requests.get(endpoint, timeout=10)
        response.raise_for_status()
        data = response.json()

        agencies = [
            {
                "agency_id": agency.get("agency_id"),
                "toptier_code": agency.get("toptier_code"),
                "abbreviation": agency.get("abbreviation"),
                "agency_name": agency.get("agency_name"),
                "congressional_justification_url": agency.get("congressional_justification_url"),
                "active_fy": agency.get("active_fy"),
                "active_fq": agency.get("active_fq"),
                "outlay_amount": agency.get("outlay_amount"),
                "obligated_amount": agency.get("obligated_amount"),
                "budget_authority_amount": agency.get("budget_authority_amount"),
                "current_total_budget_authority_amount": agency.get("current_total_budget_authority_amount"),
                "percentage_of_total_budget_authority": agency.get("percentage_of_total_budget_authority"),
                "agency_slug": agency.get("agency_slug"),
                "fetched_at": datetime.now(timezone.utc)
            }
            for agency in data.get("results", [])
        ]

        if agencies:
            db.toptier_agencies.insert_many(agencies)  # Store data without deleting previous entries
        return agencies

    except Exception as e:
        print(f"Error fetching USAspending data: {e}")
        return None

def treasury_schedular():
    try:
        endpoint = f"{TREASURY_BASE_URL}/v2/accounting/od/debt_to_penny"
        params = {"fields": "record_calendar_year,record_calendar_month"}
        response = requests.get(endpoint, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        debts = [
            {
                "record_calendar_year": record.get("record_calendar_year"),
                "record_calendar_month": record.get("record_calendar_month"),
                "fetched_at": datetime.now(timezone.utc)
            }
            for record in data.get("data", [])
        ]

        if debts:
            db.debt_to_penny.insert_many(debts)  # Store data without deleting previous entries
        return debts

    except Exception as e:
        print(f"Error fetching Treasury data: {e}")
        return None






def fetch_latest_toptier_agencies(limit=10, search=None, start_date=None, end_date=None):
    try:
        query = {}
        
        # Filter by search term if provided
        if search:
            query["$or"] = [
                {"agency_name": {"$regex": search, "$options": "i"}},
                {"abbreviation": {"$regex": search, "$options": "i"}},
                {"toptier_code": {"$regex": search, "$options": "i"}},
            ]
        if start_date and end_date:
            query["fetched_at"] = {"$gte": start_date, "$lte": end_date}

        # Fetch and return the data
        latest_agencies = list(
            db.toptier_agencies.find(query, {"_id": 0}).sort("fetched_at", -1).limit(limit)
        )
        return latest_agencies
        latest_agencies = list(
            db.toptier_agencies.find({}, {"_id": 0}).sort("fetched_at", -1).limit(limit)
        )
        return latest_agencies
    except Exception as e:
        print(f"Error fetching latest toptier agencies: {e}")
        return []






OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def calculate_metrics_with_openai(data):

    llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    )
    prompt = ChatPromptTemplate.from_messages(
    [
        (
                "system",
                """You are a helpful assistant that is good with calculations. now calculate the follwoing mentioned below from the inputted data.We need the totalspending and the total waste, and total deficit from the provided data. What I need is the only three thing as output in dict form
            
                total_spending:$XX.XXT,
                total_waste:$XX.XXT,
                total_deficit:$X,XXX,XXX

                Ensure that none of the values default to zero unless explicitly provided in the data. Use the data to determine these values accurately.
                you are not calcu;ating waste please calculate that also

                output = {{
                "total_spending": $XX.XX,
                "total_waste": $XX.XX,
                "total_deficit": $X,XXX,XXX}}
                """
            ),
            ("human", "{input}"),
        ]
    )

    chain = prompt | llm
    X = chain.invoke(
        {
            "input": data,
        }
    )

    content = X.content  # Assuming `X` is your chain response object

    # Regex patterns to extract the three values
    total_spending_match = re.search(r'"total_spending":\s*"\$(.*?)T"', content)
    total_waste_match = re.search(r'"total_waste":\s*"\$(.*?)T"', content)
    total_deficit_match = re.search(r'"total_deficit":\s*"\$(.*?)"', content)

    # Extract values if matches are found
    total_spending = total_spending_match.group(1) if total_spending_match else None
    total_waste = total_waste_match.group(1) if total_waste_match else None
    total_deficit = total_deficit_match.group(1) if total_deficit_match else None

    # Create a dictionary for the results
    result = {
        "total_spending": f"${total_spending}" if total_spending else "Not Found",
        "total_waste": f"${total_waste}" if total_waste else "Not Found",
        "total_deficit": f"${total_deficit}" if total_deficit else "Not Found",
    }
    print(result)

    return result