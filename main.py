import os
import json
import openai
from flask import Flask, request, jsonify

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/enrich", methods=["POST"])
def enrich():
    try:
        data = request.json
        print("Incoming data:", data)

        account_owner = data.get("account_owner", "Unknown")
        account_id = data.get("account_id", "Unknown")
        company_name = data.get("company_name", "Unknown")
        website = data.get("website", "Unknown")

        response = openai.ChatCompletion.create(
            model="gpt-4o",
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
                        "required": [
                            "flex_fit_score",
                            "dayfit_score",
                            "current_hcm",
                            "gpt_summary_narrative"
                        ]
                    }
                }
            ],
            function_call={"name": "enrichEngageRow"}
        )

        output = response.choices[0].message.get("function_call", {}).get("arguments", "{}")
        result = json.loads(output)

        print("GPT function response:", result)
        return jsonify(result)

    except Exception as e:
        print("ENRICH ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
