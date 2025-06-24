# Cosmon

# Natural-Language → Abaqus Script Generator

This project lets you describe a CAE task in plain English and instantly
receive a ready-to-run Python script that uses the Abaqus Scripting
Interface (ASI).

* **Frontend (React)** – single-page UI for entering prompts and viewing
  generated code.  
* **Backend (Flask + LangChain + OpenAI)** – calls GPT-4o (or any chat
  model), produces the script, logs every interaction, and offers an
  exporter that converts the log to standalone `.py` files.

> See the individual READMEs for installation and usage:
>
> * [`frontend/README.md`](frontend/README.md)  
> * [`backend/README.md`](backend/README.md)

## Tech Stack
| Layer      | Key Libraries / Tools               |
|------------|-------------------------------------|
| **UI**     | React 18, fetch API, CORS           |
| **API**    | Flask 3.0, Flask-CORS, Pydantic     |
| **AI**     | LangChain / LangGraph, OpenAI GPT-4o |
| **Storage**| `history.json` (simple JSON log)    |
| **Export** | `export_scripts.py` → readable `.py`

Clone the repo, follow the two sub-project guides, and you’ll be running
end-to-end in minutes.
