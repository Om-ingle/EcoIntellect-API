import uvicorn
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    # Railway's Edge Proxy requires allowing forwarded IPs and proxy headers to connect smoothly
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=port, 
        proxy_headers=True, 
        forwarded_allow_ips="*"
    )
