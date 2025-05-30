from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import logging
import datetime

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Created Tokens API",
    description="API for managing created tokens",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Supabase client
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "Created Tokens API",
        "version": "1.0.0",
        "endpoints": {
            "created_tokens": "/created-tokens",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    try:
        # Test Supabase connection
        supabase.table("created_tokens").select("count", count="exact").limit(1).execute()
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Service unhealthy")

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