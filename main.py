
from flask import Flask, request, jsonify
import openai
import json
import os

app = Flask(__name__)

# Set your OpenAI API key (in Render environment settings)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the function schema
function_schema = [
    {
        "name": "quota_crusher_engage",
        "description": "Full company enrichment for Dayforce HCM using Quota Crusher Engage pipeline.",
        "parameters": {
            "type": "object",
            "required": ["Account Owner", "Account ID (18 Char)", "SFDC Account Name", "Website", "QC Engage Status", "Last QC Engage Date", "GPT Summary Narrative"],
            "properties": {
                "Account Owner": {"type": "string"},
                "Account ID (18 Char)": {"type": "string"},
                "SFDC Account Name": {"type": "string"},
                "Website": {"type": "string"},
                "QC Engage Status": {"type": "string"},
                "Last QC Engage Date": {"type": "string"},
                "GPT Summary Narrative": {"type": "string"}
            },
            "additionalProperties": True
        }
    }
]

@app.route("/enrich", methods=["POST"])
def enrich():
    data = request.get_json()

    # Map Zapier input to schema keys
    mapped_input = {
        "Account Owner": data.get("account_owner", "Unknown"),
        "Account ID (18 Char)": data.get("account_id", "Unknown"),
        "SFDC Account Name": data.get("company_name", "Unknown"),
        "Website": data.get("website", "Unknown"),
        "QC Engage Status": "Active",
        "Last QC Engage Date": "2025-06-06",
        "GPT Summary Narrative": ""  # Will be filled by OpenAI
    }

    messages = [
        {
            "role": "user",
            "content": f"Run quota_crusher_engage for {mapped_input['SFDC Account Name']} at {mapped_input['Website']}"
        }
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=messages,
            functions=function_schema,
            function_call={"name": "quota_crusher_engage"}
        )

        function_args_str = response['choices'][0]['message']['function_call']['arguments']
        parsed_args = json.loads(function_args_str)

        # Merge mapped input into parsed_args to complete required fields
        parsed_args.update(mapped_input)

        return jsonify(parsed_args)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

