import os
from app.config.settings import load_root_env_if_present, API_HOST, API_PORT
from app import create_app

# Load environment variables
load_root_env_if_present()

# Create FastAPI application
app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT, reload=False)