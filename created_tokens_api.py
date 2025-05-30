from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os
from supabase import create_client
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

@app.get("/created-tokens")
async def get_created_tokens():
    try:
        result = supabase.table("created_tokens").select("*").order("created_at", desc=True).execute()
        return {"tokens": result.data}
    except Exception as e:
        logger.error(f"Failed to fetch created tokens: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch created tokens")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("API_PORT", 8000))) 