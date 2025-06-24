from flask import Flask, request, jsonify
from flask_cors import CORS

from langchain_community.tools.tavily_search import TavilySearchResults
from agent import generate_abaqus_script

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

@app.route("/run_agent", methods=["POST"])
def run_agent():
    try:
        data = request.json
        user_input = data.get("input", "")

        if not user_input:
            return jsonify({"error": "User input is required"}), 400

        response = generate_abaqus_script(user_input)
        print(f"Generated script: {response}")
        return jsonify({"response": response})

    except Exception as e:
        console.log(e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
