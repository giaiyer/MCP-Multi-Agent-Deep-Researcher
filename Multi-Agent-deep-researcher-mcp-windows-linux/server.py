from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents import run_research
import os
from dotenv import load_dotenv
import sys
import pathlib

# Add the current directory to sys.path for import
sys.path.append(str(pathlib.Path(__file__).parent.resolve()))
from linkup_only import linkup_search

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

class ResearchRequest(BaseModel):
    query: str

@app.post("/research")
def research(request: ResearchRequest):
    try:
        result = run_research(request.query)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080) 