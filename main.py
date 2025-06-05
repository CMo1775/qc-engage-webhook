from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route("/enrich", methods=["POST"])
def enrich():
    try:
        data = request.get_json()
        account_owner = data.get("account_owner")
        account_id = data.get("account_id")
        company_name = data.get("company_name")
        website = data.get("website")

        enrichment_status = "Complete"
        enrich_date = datetime.today().strftime("%m/%d/%Y")
        dummy_excel_url = "https://yourdrive.com/path/to/enriched_file.xlsx"

        return jsonify({
            "status": enrichment_status,
            "date": enrich_date,
            "output_file": dummy_excel_url,
            "notes": f"Engaged {company_name} successfully."
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
