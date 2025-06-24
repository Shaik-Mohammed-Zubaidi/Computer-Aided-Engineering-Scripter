from flask import Flask, request, jsonify
from flask_cors import CORS
import json, pathlib, datetime

from agent import generate_abaqus_script   # your code-gen helper

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

HISTORY_FILE = pathlib.Path("history.json")

def append_to_history(user_input: str, reply: str) -> None:
    """Add one entry to history.json (creates file if absent)."""
    if HISTORY_FILE.exists():
        with HISTORY_FILE.open("r", encoding="utf-8") as fp:
            history = json.load(fp)
    else:
        history = []

    history.append(
        {
            "input": user_input,
            "output": reply,
        }
    )

    with HISTORY_FILE.open("w", encoding="utf-8") as fp:
        json.dump(history, fp, ensure_ascii=False, indent=2)

@app.route("/run_agent", methods=["POST"])
def run_agent():
    try:
        data = request.get_json(force=True)
        user_input = data.get("input", "").strip()

        if not user_input:
            return jsonify({"error": "User input is required"}), 400

        response = generate_abaqus_script(user_input)

        # -------------  NEW: persist interaction -------------
        append_to_history(user_input, response)
        # ------------------------------------------------------

        return jsonify({"response": response})

    except Exception as e:
        # print to server log
        app.logger.exception("Agent failure")
        # send minimal info to client
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # history file bootstrap: create empty list if file missing
    if not HISTORY_FILE.exists():
        HISTORY_FILE.write_text("[]", encoding="utf-8")

    app.run(debug=True)
