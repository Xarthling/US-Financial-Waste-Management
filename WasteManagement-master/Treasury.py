from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import requests

# FastAPI instance
app = FastAPI()

# Jinja2 templates directory
templates = Jinja2Templates(directory="template")

# Treasury API Base URL
TREASURY_BASE_URL = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1"


@app.get("/treasury/rates_of_exchange", response_class=HTMLResponse)
def get_rates_of_exchange(
    request: Request,
    country_currency_desc: str = Query(None, description="Comma-separated currency descriptions (e.g., Canada-Dollar,Mexico-Peso)"),
    record_date_gte: str = Query(None, description="Record date greater than or equal to (format: YYYY-MM-DD)")
):
    """
    Fetch rates of exchange from the Treasury API and pass them to the frontend.
    """
    try:
        # Define API endpoint and parameters
        endpoint = f"{TREASURY_BASE_URL}/accounting/od/rates_of_exchange"
        fields = "country_currency_desc,exchange_rate,record_date"
        filters = []

        if country_currency_desc:
            filters.append(f"country_currency_desc:in:({country_currency_desc})")
        if record_date_gte:
            filters.append(f"record_date:gte:{record_date_gte}")

        params = {
            "fields": fields,
            "filter": ",".join(filters) if filters else None
        }

        # Make the API request
        response = requests.get(endpoint, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Extract rates of exchange
        rates = [
            {
                "country_currency_desc": rate.get("country_currency_desc"),
                "exchange_rate": float(rate.get("exchange_rate", 0)),
                "record_date": rate.get("record_date")
            }
            for rate in data.get("data", [])
        ]

        # Render the HTML template with data
        return templates.TemplateResponse("treasury.html", {"request": request, "rates": rates})

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="The request to the Treasury API timed out.")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data from Treasury API: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")



@app.get("/treasury/debt_to_penny", response_class=HTMLResponse)
def get_debt_to_penny(
    request: Request,
    page_size: int = Query(100, description="Number of records per page"),
    page_number: int = Query(1, description="Page number"),
):
    """
    Fetch debt data grouped by year and month from the Treasury API
    and render it in the frontend.
    """
    try:
        # Define API endpoint and parameters
        endpoint = f"{TREASURY_BASE_URL}/v2/accounting/od/debt_to_penny"
        params = {
            "fields": "record_calendar_year,record_calendar_month",
            "sort": "-record_calendar_year,-record_calendar_month",
            "page[size]": page_size,
            "page[number]": page_number,
        }

        # Make the API request
        response = requests.get(endpoint, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Extract relevant data
        debts = [
            {
                "record_calendar_year": record.get("record_calendar_year"),
                "record_calendar_month": record.get("record_calendar_month"),
            }
            for record in data.get("data", [])
        ]

        # Render the HTML template with data
        return templates.TemplateResponse(
            "debt_to_penny.html",
            {
                "request": request,
                "debts": debts,
                "meta": data.get("meta", {}),
                "page_size": page_size,
                "page_number": page_number,
            },
        )

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="The request to the Treasury API timed out.")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data from Treasury API: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
