Phase 5 — React Frontend

Scaffold React app — From project root:
bash   
```cd frontend
npm create vite@latest . -- --template react-ts
npm install
```
Create a simple chat UI — Just need:
Text input for questions
Submit button
Area to display the answer
Area to display sources
Add API call — Fetch to http://localhost:8000/query with the question
Handle loading state — Show "Thinking..." while waiting for response
Display sources — Show which chunks were used below the answer
Handle CORS — You'll need to add CORS middleware to your FastAPI app:
python   
```from fastapi.middleware.cors import CORSMiddleware
   
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_methods=["*"],
    allow_headers=["*"],
)```

Test end-to-end — Run both servers, ask a question, see the answer
Commit — feat: React chat frontend

Start with steps 1-3. Get a basic form submitting to your API first, then we'll add polish.