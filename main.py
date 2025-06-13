import os
import openai
from flask import Flask, request, jsonify

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/enrich", methods=["POST"])
def enrich():
    try:
        data = request.json
        print("Incoming data:", data)

        # Required fields from Google Sheet
        account_owner = data.get("account_owner", "Unknown")
        account_id = data.get("account_id", "Unknown")
        company_name = data.get("company_name", "Unknown")
        website = data.get("website", "Unknown")

        # Call GPT with a function call structure
        response = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=[
                {"role": "system", "content": "You are Quota Crusher Engage. Return all metadata fields required for enrichment."},
                {"role": "user", "content": f"Enrich the following company: {company_name} ({website}) for account owner {account_owner} with SFDC ID {account_id}."}
            ],
            functions=[
                {
                    "name": "enrichEngageRow",
                    "description": "Returns company metadata for Engage enrichment",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "flex_fit_score": {"type": "string"},
                            "dayfit_score": {"type": "string"},
                            "current_hcm": {"type": "string"},
                            "gpt_summary_narrative": {"type": "string"}
                        },
                        "required": ["flex_fit_score", "dayfit_scor_]()
