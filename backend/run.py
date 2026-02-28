import uvicorn
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    # Run the FastAPI app, binding securely to the environment port (Railway)
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
