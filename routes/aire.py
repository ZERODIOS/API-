from fastapi import APIRouter
import requests, time, hashlib, hmac, json

router = APIRouter(prefix="/ac")
CLIENT_ID = "g4gwgw7stxfr9agcvwnk"
CLIENT_SECRET = "6e4f8d492dde4c589c9d6b330969e922"
DEVICE_ID = "eb99917de38cf624edfqev"
BASE_URL = "https://openapi.tuyaus.com"

def sha256_hex(body: str):
    return hashlib.sha256(body.encode()).hexdigest()

def get_token():
    t = str(int(time.time() * 1000))
    url_path = "/v1.0/token?grant_type=1"

    string_to_sign = f"GET\n{sha256_hex('')}\n\n{url_path}"
    sign_str = CLIENT_ID + t + string_to_sign

    sign = hmac.new(CLIENT_SECRET.encode(), sign_str.encode(), hashlib.sha256).hexdigest().upper()

    headers = {
        "client_id": CLIENT_ID,
        "t": t,
        "sign": sign,
        "sign_method": "HMAC-SHA256"
    }

    res = requests.get(BASE_URL + url_path, headers=headers)
    return res.json()["result"]["access_token"]

def send_command(code, value):
    token = get_token()
    t = str(int(time.time() * 1000))
    url_path = f"/v1.0/devices/{DEVICE_ID}/commands"

    body = json.dumps({"commands": [{"code": code, "value": value}]})
    body_hash = sha256_hex(body)

    string_to_sign = f"POST\n{body_hash}\n\n{url_path}"
    sign_str = CLIENT_ID + token + t + string_to_sign

    sign = hmac.new(CLIENT_SECRET.encode(), sign_str.encode(), hashlib.sha256).hexdigest().upper()

    headers = {
        "client_id": CLIENT_ID,
        "access_token": token,
        "t": t,
        "sign": sign,
        "sign_method": "HMAC-SHA256",
        "Content-Type": "application/json"
    }

    return requests.post(BASE_URL + url_path, data=body, headers=headers).json()

# 🔥 endpoints

@router.get("/on")
def on():
    return send_command("switch", True)

@router.get("/off")
def off():
    return send_command("switch", False)

@router.get("/temp/{temp}")
def temp(temp: int):
    return send_command("temp_set", temp)

@router.get("/mode/{mode}")
def mode(mode: str):
    return send_command("mode", mode)
