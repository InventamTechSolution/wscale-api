import socket
from fastapi import FastAPI, HTTPException
import uvicorn
from typing import Dict

app = FastAPI(
    title="Weight Scale API",
    description="API to fetch data from weight scale over socket connection",
    version="1.0.0"
)

# Configuration
HOST = "192.168.2.245"  # Static IP
PORT = 1702             # TCP Port

@app.get("/")
async def root():
    """Root endpoint that returns a welcome message."""
    return {"message": "Welcome to Weight Scale API. Use /get-data to fetch scale data."}

@app.get("/get-data")
async def get_scale_data() -> Dict:
    """Fetch data from the weight scale via socket connection."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)  # Set timeout to 5 seconds
            s.connect((HOST, PORT))
            s.sendall(b"GET_DATA")  # Send request command
            data = s.recv(1024)
            decoded_data = data.decode().strip()
            actual_data = decoded_data.split(" ")[1].replace("0","")
            print(type(actual_data), actual_data,int(actual_data))
            return {"status": "success", "data": int(actual_data)/100, "unit":"kg"}
    except socket.timeout:
        raise HTTPException(status_code=504, detail="Connection to scale timed out")
    except socket.error as e:
        raise HTTPException(status_code=500, detail=f"Socket error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("wscale:app", host="0.0.0.0", port=8000, reload=True)