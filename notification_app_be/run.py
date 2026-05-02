import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

if __name__ == "__main__":
    print("Starting Notification System...")
    print("API Documentation: http://localhost:8000/docs")
    
    # Run the FastAPI app using uvicorn
    # host: 0.0.0.0 allows access from other devices in the network
    # port: 8000 is the default port for this app
    # reload: True enables auto-restart when code changes
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
