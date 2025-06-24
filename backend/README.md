### **`backend/README.md`**

# Backend (Flask + OpenAI + LangChain)

Exposes **POST /run_agent**:

1. Receives a user prompt from the React app  
2. Passes it to `agent.generate_abaqus_script()` (GPT-4o via LangChain)  
3. Returns the generated Abaqus Python code  
4. Logs the interaction to **history.json**

`export_scripts.py` converts that history to human-readable `.py` files.

---

## 1  Prerequisites

| Tool   | Min version | macOS install (brew / native)            | Ubuntu / WSL |
|--------|-------------|------------------------------------------|--------------|
| Python | 3.10        | Pre-installed or `brew install python@3` | `sudo apt install python3 python3-venv` |

---

## 2  Install

```bash
cd backend
python3 -m venv .venv           # optional but recommended
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 3 Set your OpenAI API key
### macOS / Linux (bash / zsh)
```bash
export OPENAI_API_KEY="sk-********"
```
Add that line to ~/.bashrc or ~/.zshrc to persist.

### Windows (PowerShell)
```powershell
setx OPENAI_API_KEY "sk-********"
# then restart the shell
```

##  4 Run the server
```bash
python app.py
```
Expected log:

```csharp
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

## 5 API contract
```http
POST /run_agent
Content-Type: application/json

{
  "input": "Create a 25 × 25 × 25 mm solid cube named Cube1"
}
```

Success →
```json
{
  "response": "from abaqus import *\nfrom abaqusConstants import *\n…"
}
```

Each call appends:
```jsonc
{
  "timestamp": "2025-06-24T04:37:30Z",
  "input": "Create …",
  "output": "from abaqus import *\n…"
}
```
to history.json (auto-created in the backend folder).


## 6 Export previous scripts
```bash
python export_scripts.py history.json exported_scripts
```

Creates:
```css
exported_scripts/
 ├─ 0001_cube1.py
 ├─ 0002_cube1_steel_mesh.py
 └─ …
```
Each file has the prompt + timestamp header, followed by properly
line-broken code.


## 7 Folder layout
```pgsql
backend/
 ├─ app.py               ← Flask server
 ├─ agent.py             ← generate_abaqus_script()
 ├─ export_scripts.py    ← history → .py exporter
 ├─ history.json         ← grows with every call
 ├─ requirements.txt
 └─ README.md            ← you’re reading it
```

Notes & Tips
- Thread safety – history.json is fine for the single-process dev
server. Use SQLite or a lock file if you deploy with multiple workers.

- Abaqus execution – Generated scripts can be run via
abaqus cae noGUI=<script.py> on a licensed machine (Student Edition
VM, campus server, etc.). See root README for options on macOS.

---

**Copy/paste each block into its matching file and you’re done.**