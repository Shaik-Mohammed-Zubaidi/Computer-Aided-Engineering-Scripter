# Frontend (React)

A single-page React app that lets you:

1. type a natural-language Abaqus request  
2. press **Run**  
3. read the generated Python script below the input box

---

## 1  Prerequisites

| Tool | Min version | macOS install                     | Windows / Linux |
|------|-------------|-----------------------------------|-----------------|
| **Node.js + npm** | 18 LTS | `brew install node` | <https://nodejs.org/en/download> |

---

## 2  Setup

```bash
cd frontend
npm install
```

## 3 Run

```bash
npm start
```

The dev server opens http://localhost:3000.
Make sure the Flask backend is running on http://localhost:5000.

## 4 Project structure
```css
frontend/
 ├─ src/
 │   ├─ App.jsx   ← main page (input + results)
 │   └─ …
 └─ package.json
```

![alt text](<Screenshot 2025-06-24 at 01.30.32.png>)

No routing, no global state—just React hooks and fetch.

