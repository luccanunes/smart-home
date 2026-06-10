# 💡 Smart Home API

## How to Run
Always run from the **project root** (~/projects/smart-home):

`uvicorn api.src.server:app --reload --host 0.0.0.0`

## Access & Testing
* **Swagger UI:** http://<RASPBERRY_PI_IP>:8000/docs

## ⚠️ Port Blocked?
If port 8000 is occupied by an old process, clear the memory with:

`ps aux | grep uvicorn`
`kill -9 ID`
`pkill -f uvicorn`