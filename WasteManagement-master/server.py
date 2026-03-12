from flask import Flask, jsonify, request
from flask_cors import CORS
import time
import threading

app = Flask(__name__)
CORS(app)  # Enable CORS

mock_deficit = {
    "currentDeficit": 1781394527149,  # Starting deficit in dollars
}

def increment_deficit():
    while True:
        time.sleep(1)
        mock_deficit["currentDeficit"] += 156464000  # Increase per second

# Start the incrementing thread
threading.Thread(target=increment_deficit, daemon=True).start()

mock_expenses = [
    {
        "id": "DOD-2024-1234",
        "department": "Department of Defense",
        "project": "Maintaining existing aircraft is crucial until replacement systems are operational. This maintenance package is necessary to prevent catastrophic failures and protect pilot safety.",
        "timestamp": "2023-03-14T15:23:00Z",
        "score": 85,
        "spent": 47200000,  # $47.2M
        "waste": 9000000,   # $9.0M
        "tags": ["Defense", "Maintenance", "F-35 Program"],
        "items": [
            {
            "item": "N95 Respirators (2.5M units)",
            "itemCost": 18400000,  # $18.4M
            "marketPrice": 15200000,  # $15.2M
            "waste": 3200000,  # $3.2M
            "source": "GSA Schedule"
            },
            {
            "item": "Medical Gowns (1M units)",
            "itemCost": 12600000,  # $12.6M
            "marketPrice": 10800000,  # $10.8M
            "waste": 1800000,  # $1.8M
            "source": "Medicare Rate"
            },
            {
            "item": "Emergency Medical Kits",
            "itemCost": 16200000,  # $16.2M
            "marketPrice": 12200000,  # $12.2M
            "waste": 4000000,  # $4.0M
            "source": "VA Contract"
            }
        ],
        "total": {
            "itemCost": 47200000,  # $47.2M
            "marketPrice": 38200000,  # $38.2M
            "waste": 9000000  # $9.0M
        }
    },
    {
        "id": "HHS-2024-5678",
        "department": "Health & Human Services",
        "project": "Procurement of N95 Respirators to ensure adequate supply for healthcare workers.",
        "timestamp": "2024-03-14T15:23:00Z",
        "score": 65,
        "spent": 47200000,  # $47.2M
        "waste": 9000000,   # $9.0M
        "tags": ["Health", "Budget", "Waste"],
        "items": [
            {
            "item": "N95 Respirators (2.5M units)",
            "itemCost": 18400000,  # $18.4M
            "marketPrice": 15200000,  # $15.2M
            "waste": 3200000,  # $3.2M
            "source": "GSA Schedule"
            },
            {
            "item": "Medical Gowns (1M units)",
            "itemCost": 12600000,  # $12.6M
            "marketPrice": 10800000,  # $10.8M
            "waste": 1800000,  # $1.8M
            "source": "Medicare Rate"
            },
            {
            "item": "Emergency Medical Kits",
            "itemCost": 16200000,  # $16.2M
            "marketPrice": 12200000,  # $12.2M
            "waste": 4000000,  # $4.0M
            "source": "VA Contract"
            }
        ],
        "total": {
            "itemCost": 47200000,  # $47.2M
            "marketPrice": 38200000,  # $38.2M
            "waste": 9000000  # $9.0M
        }
    },
    {
        "id": "DOE-2024-9101",
        "department": "Department of Energy",
        "project": "Development of renewable energy sources to reduce dependency on fossil fuels.",
        "timestamp": "2024-03-14T15:23:00Z",
        "score": 90,
        "spent": 60000000,  # $60.0M
        "waste": 5000000,   # $5.0M
        "tags": ["Energy", "Renewable", "Research"],
        "items": [
            {
            "item": "N95 Respirators (2.5M units)",
            "itemCost": 18400000,  # $18.4M
            "marketPrice": 15200000,  # $15.2M
            "waste": 3200000,  # $3.2M
            "source": "GSA Schedule"
            },
            {
            "item": "Medical Gowns (1M units)",
            "itemCost": 12600000,  # $12.6M
            "marketPrice": 10800000,  # $10.8M
            "waste": 1800000,  # $1.8M
            "source": "Medicare Rate"
            },
            {
            "item": "Emergency Medical Kits",
            "itemCost": 16200000,  # $16.2M
            "marketPrice": 12200000,  # $12.2M
            "waste": 4000000,  # $4.0M
            "source": "VA Contract"
            }
        ],
        "total": {
            "itemCost": 47200000,  # $47.2M
            "marketPrice": 38200000,  # $38.2M
            "waste": 9000000  # $9.0M
        }
    },
    {
        "id": "DOT-2024-1121",
        "department": "Department of Transportation",
        "project": "Infrastructure improvements for interstate highways to reduce traffic congestion.",
        "timestamp": "2024-03-14T15:23:00Z",
        "score": 75,
        "spent": 80000000,  # $80.0M
        "waste": 10000000,  # $10.0M
        "tags": ["Transportation", "Infrastructure", "Highways"],
        "items": [
            {
            "item": "N95 Respirators (2.5M units)",
            "itemCost": 18400000,  # $18.4M
            "marketPrice": 15200000,  # $15.2M
            "waste": 3200000,  # $3.2M
            "source": "GSA Schedule"
            },
            {
            "item": "Medical Gowns (1M units)",
            "itemCost": 12600000,  # $12.6M
            "marketPrice": 10800000,  # $10.8M
            "waste": 1800000,  # $1.8M
            "source": "Medicare Rate"
            },
            {
            "item": "Emergency Medical Kits",
            "itemCost": 16200000,  # $16.2M
            "marketPrice": 12200000,  # $12.2M
            "waste": 4000000,  # $4.0M
            "source": "VA Contract"
            }
        ],
        "total": {
            "itemCost": 47200000,  # $47.2M
            "marketPrice": 38200000,  # $38.2M
            "waste": 9000000  # $9.0M
        }
    },
    {
        "id": "DOD-2022-1234",
        "department": "Department of Defense",
        "project": "Upgrading communication systems for enhanced security.",
        "timestamp": "2022-05-10T10:15:00Z",
        "score": 80,
        "spent": 35000000,  # $35.0M
        "waste": 7000000,   # $7.0M
        "tags": ["Defense", "Communication", "Upgrade"],
        "items": [
            {
            "item": "N95 Respirators (2.5M units)",
            "itemCost": 18400000,  # $18.4M
            "marketPrice": 15200000,  # $15.2M
            "waste": 3200000,  # $3.2M
            "source": "GSA Schedule"
            },
            {
            "item": "Medical Gowns (1M units)",
            "itemCost": 12600000,  # $12.6M
            "marketPrice": 10800000,  # $10.8M
            "waste": 1800000,  # $1.8M
            "source": "Medicare Rate"
            },
            {
            "item": "Emergency Medical Kits",
            "itemCost": 16200000,  # $16.2M
            "marketPrice": 12200000,  # $12.2M
            "waste": 4000000,  # $4.0M
            "source": "VA Contract"
            }
        ],
        "total": {
            "itemCost": 47200000,  # $47.2M
            "marketPrice": 38200000,  # $38.2M
            "waste": 9000000  # $9.0M
        }
    },
    {
        "id": "HHS-2022-5678",
        "department": "Health & Human Services",
        "project": "Expansion of telehealth services.",
        "timestamp": "2022-07-22T09:30:00Z",
        "score": 70,
        "spent": 25000000,  # $25.0M
        "waste": 5000000,   # $5.0M
        "tags": ["Health", "Telehealth", "Expansion"],
        "items": [
            {
            "item": "N95 Respirators (2.5M units)",
            "itemCost": 18400000,  # $18.4M
            "marketPrice": 15200000,  # $15.2M
            "waste": 3200000,  # $3.2M
            "source": "GSA Schedule"
            },
            {
            "item": "Medical Gowns (1M units)",
            "itemCost": 12600000,  # $12.6M
            "marketPrice": 10800000,  # $10.8M
            "waste": 1800000,  # $1.8M
            "source": "Medicare Rate"
            },
            {
            "item": "Emergency Medical Kits",
            "itemCost": 16200000,  # $16.2M
            "marketPrice": 12200000,  # $12.2M
            "waste": 4000000,  # $4.0M
            "source": "VA Contract"
            }
        ],
        "total": {
            "itemCost": 47200000,  # $47.2M
            "marketPrice": 38200000,  # $38.2M
            "waste": 9000000  # $9.0M
        }
    },
    {
        "id": "DOE-2022-9101",
        "department": "Department of Energy",
        "project": "Research on battery storage technologies.",
        "timestamp": "2022-11-15T14:45:00Z",
        "score": 88,
        "spent": 40000000,  # $40.0M
        "waste": 6000000,   # $6.0M
        "tags": ["Energy", "Battery", "Research"],
        "items": [
            {
            "item": "N95 Respirators (2.5M units)",
            "itemCost": 18400000,  # $18.4M
            "marketPrice": 15200000,  # $15.2M
            "waste": 3200000,  # $3.2M
            "source": "GSA Schedule"
            },
            {
            "item": "Medical Gowns (1M units)",
            "itemCost": 12600000,  # $12.6M
            "marketPrice": 10800000,  # $10.8M
            "waste": 1800000,  # $1.8M
            "source": "Medicare Rate"
            },
            {
            "item": "Emergency Medical Kits",
            "itemCost": 16200000,  # $16.2M
            "marketPrice": 12200000,  # $12.2M
            "waste": 4000000,  # $4.0M
            "source": "VA Contract"
            }
        ],
        "total": {
            "itemCost": 47200000,  # $47.2M
            "marketPrice": 38200000,  # $38.2M
            "waste": 9000000  # $9.0M
        }
    },
    {
        "id": "DOT-2022-1121",
        "department": "Department of Transportation",
        "project": "Development of smart traffic management systems.",
        "timestamp": "2022-03-18T08:20:00Z",
        "score": 78,
        "spent": 45000000,  # $45.0M
        "waste": 8000000,   # $8.0M
        "tags": ["Transportation", "Smart Systems", "Traffic"],
        "items": [
            {
            "item": "N95 Respirators (2.5M units)",
            "itemCost": 18400000,  # $18.4M
            "marketPrice": 15200000,  # $15.2M
            "waste": 3200000,  # $3.2M
            "source": "GSA Schedule"
            },
            {
            "item": "Medical Gowns (1M units)",
            "itemCost": 12600000,  # $12.6M
            "marketPrice": 10800000,  # $10.8M
            "waste": 1800000,  # $1.8M
            "source": "Medicare Rate"
            },
            {
            "item": "Emergency Medical Kits",
            "itemCost": 16200000,  # $16.2M
            "marketPrice": 12200000,  # $12.2M
            "waste": 4000000,  # $4.0M
            "source": "VA Contract"
            }
        ],
        "total": {
            "itemCost": 47200000,  # $47.2M
            "marketPrice": 38200000,  # $38.2M
            "waste": 9000000  # $9.0M
        }
    }
]

mock_metrics = {
    "amountSpent": "$3.2T",
    "totalWaste": "$284B",
}

@app.route('/api/deficit', methods=['GET'])
def get_deficit():
    return jsonify(mock_deficit)

@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    search_query = request.args.get('search', '')
    start_date = request.args.get('startDate', '')
    end_date = request.args.get('endDate', '')

    filtered_expenses = mock_expenses

    if search_query:
        filtered_expenses = [
            expense for expense in filtered_expenses 
            if search_query.lower() in expense['project'].lower() or search_query.lower() in [tag.lower() for tag in expense['tags']]
        ]

    if start_date and end_date:
        filtered_expenses = [expense for expense in filtered_expenses if start_date <= expense['timestamp'] <= end_date]

    return jsonify(filtered_expenses)

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    return jsonify(mock_metrics)

if __name__ == '__main__':
    app.run(debug=True)





from flask import Flask, request, jsonify
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from pymongo import MongoClient
import requests

# Flask app initialization
app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client['your_database']
collection = db['your_collection']

# x.ai API key
XAI_API_KEY = "API KEY"

# Fetch data from MongoDB
def fetch_data_from_mongo(query):
    result = collection.find_one(query)  # Adjust query to match your data schema
    if not result:
        return "No relevant data found in MongoDB."
    return result

# Fetch data from Chroma
def fetch_data_from_chroma(query):
    path = 'vector_db'
    vector_store = Chroma(
        embedding_function=OpenAIEmbeddings(),
        persist_directory=path
    )
    documents = vector_store.search(query, n_results=3)  # Adjust n_results as needed
    if not documents:
        return "No relevant data found in the vector database."
    return "\n".join([doc.page_content for doc in documents])

# Query Grok API
def query_grok_api(system_prompt, user_query):
    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {XAI_API_KEY}"
    }
    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ],
        "model": "grok-beta",
        "stream": False,
        "temperature": 0
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# API endpoint for Grok interaction
@app.route('/api/grok', methods=['POST'])
def interact_with_grok():
    # Extract query from the user
    user_query = request.json.get("query", "")
    source = request.json.get("source", "mongo")  # Either 'mongo' or 'chroma'

    # Define the system prompt for Grok
    system_prompt = "You are an assistant who retrieves information from a database and answers user queries based on that information."

    # Fetch data from MongoDB or Chroma
    if source == "mongo":
        db_query = {}  # Customize this query to filter MongoDB documents as needed
        data = fetch_data_from_mongo(db_query)
    elif source == "chroma":
        data = fetch_data_from_chroma(user_query)
    else:
        return jsonify({"error": "Invalid source specified. Use 'mongo' or 'chroma'."}), 400

    # Pass the retrieved data and user query to Grok
    full_prompt = f"{system_prompt}\n\nData:\n{data}\n\nUser Query: {user_query}"
    grok_response = query_grok_api(system_prompt, full_prompt)

    # Extract Grok's answer
    answer = grok_response.get("choices", [{}])[0].get("message", {}).get("content", "No answer available.")

    return jsonify({"answer": answer})

# Main entry point
if __name__ == '__main__':
    app.run(debug=True)
