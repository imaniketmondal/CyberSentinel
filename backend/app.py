from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psutil
import os
from twilio.rest import Client

app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# List of common vulnerable ports
VULNERABLE_PORTS = {21, 22, 23, 135, 139, 445, 3306, 3389, 8080, 9001}

class PortRequest(BaseModel):
    port: int  # Ensure the request contains a valid integer port

@app.get("/scan")
def scan():
    """Scans for open ports and determines if they are threats."""
    open_ports = [conn.laddr.port for conn in psutil.net_connections() if conn.status == "LISTEN"]
    
    port_data = []
    vulnerable_ports_detected = []
    
    for port in open_ports:
        if port in VULNERABLE_PORTS:
            port_data.append({"port": port, "status": "THREAT", "risk": "HIGH"})
            vulnerable_ports_detected.append(port)
        else:
            port_data.append({"port": port, "status": "SAFE", "risk": "LOW"})
    
    return {"ports": port_data, "vulnerable_ports": vulnerable_ports_detected}

@app.post("/close_port")
def close_port(request: PortRequest):
    """Closes a specified port by terminating its associated process."""
    port = request.port
    for conn in psutil.net_connections():
        if conn.laddr.port == port and conn.pid:
            try:
                os.system(f"taskkill /PID {conn.pid} /F")
                return {"message": f"Port {port} closed successfully."}
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error closing port: {str(e)}")
    
    raise HTTPException(status_code=404, detail=f"No process found using port {port}")

# Twilio Credentials
TWILIO_ACCOUNT_SID = ""
TWILIO_AUTH_TOKEN = ""
TWILIO_PHONE_NUMBER = "+"
RECEIVER_PHONE_NUMBER = "+"

@app.post("/send_report")
def send_report():
    """Sends a security report via SMS using Twilio."""
    try:
        scan_result = scan()
        vulnerable_ports = scan_result["vulnerable_ports"]

        if not vulnerable_ports:
            return {"message": "No vulnerable ports detected. No report sent."}

        # Create a detailed message
        message_body = "Security Alert: The following ports are open and vulnerable: " + ", ".join(map(str, vulnerable_ports))

        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=RECEIVER_PHONE_NUMBER
        )
        return {"message": "Report sent successfully via SMS", "sid": message.sid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
