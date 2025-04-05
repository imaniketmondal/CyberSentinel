# CyberSentinel

CyberSentinel is a real-time cybersecurity threat detection and prevention tool built with FastAPI. It monitors open ports on your system, identifies commonly known vulnerable ports, allows remote port closure, and sends security alerts via SMS using the Twilio API.

## Features

- Scan and list open ports on your system
- Identify high-risk (vulnerable) ports from a predefined list
- Close specific ports by terminating associated processes
- Send real-time alerts via SMS using Twilio
- CORS-enabled FastAPI backend for frontend integration

---

## Tech Stack

- FastAPI
- Python 3.x
- psutil (for system and network monitoring)
- Twilio API (for SMS alerts)


## Installation

1. Clone the repository:

git clone https://github.com/your-username/CyberSentinel.git
cd CyberSentinel


2. (Optional) Create a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


3. Install dependencies:

pip install -r requirements.txt


## Running the App

Start the development server:

uvicorn main:app --reload


Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)  
API Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## API Endpoints

### GET /scan

Scans for open ports and returns their status.

Response:
```json
{
  "ports": [
    {"port": 80, "status": "SAFE", "risk": "LOW"},
    {"port": 445, "status": "THREAT", "risk": "HIGH"}
  ],
  "vulnerable_ports": [445]
}
```

### POST /close_port

Closes a port by killing the process using it.

Request Body:

{
  "port": 445
}


Response:

{"message": "Port 445 closed successfully."}

### POST /send_report

Sends a security report via SMS with a list of detected vulnerable ports.

Response:

{
  "message": "Report sent successfully via SMS",
  "sid": "SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}



## Twilio Setup

1. Sign up at [Twilio](https://www.twilio.com/)
2. Get your Account SID, Auth Token, and phone number
3. Update the following in `main.py`:


TWILIO_ACCOUNT_SID = "your_sid"
TWILIO_AUTH_TOKEN = "your_token"
TWILIO_PHONE_NUMBER = "+1234567890"
RECEIVER_PHONE_NUMBER = "+0987654321"


## Project Structure

```
CyberSentinel/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```
