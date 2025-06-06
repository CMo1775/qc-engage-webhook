import openai
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/enrich", methods=["POST"])
def enrich():
    data = request.json

    # Send to OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=[{
            "role": "user",
            "content": f"Run quota_crusher_engage for {data['company_name']} at {data['website']}."
        }],
        functions=[YOUR_FUNCTION_SCHEMA_HERE],
        function_call={"name": "quota_crusher_engage"}
    )

    # Parse the flat JSON from function call
    function_args_str = response['choices'][0]['message']['function_call']['arguments']
    parsed_output = json.loads(function_args_str)

    # ✅ Return the parsed object directly so Zapier can read all fields
    return jsonify(parsed_output)
