
from fastapi import APIRouter
import requests, time, hashlib, hmac, json

router = APIRouter(prefix="/plug")

CLIENT_ID = "g4gwgw7stxfr9agcvwnk"
CLIENT_SECRET = "6e4f8d492dde4c589c9d6b330969e922"
DEVICE_ID = "eb0d979bf17e2097aa75l1"
BASE_URL = "https://openapi.tuyaus.com"

def sha256_hex(body: str):
    return hashlib.sha256(body.encode()).hexdigest()
def get_token():
    t = str(int(time.time() * 1000))
    url_path = "/v1.0/token?grant_type=1"

    body = ""
    body_hash = sha256_hex(body)

    string_to_sign = f"GET\n{body_hash}\n\n{url_path}"
    sign_str = CLIENT_ID + t + string_to_sign

    sign = hmac.new(
        CLIENT_SECRET.encode(),
        sign_str.encode(),
        hashlib.sha256
    ).hexdigest().upper()

    headers = {
        "client_id": CLIENT_ID,
        "t": t,
        "sign": sign,
        "sign_method": "HMAC-SHA256"
    }

    res = requests.get(BASE_URL + url_path, headers=headers)
    data = res.json()

    print("TOKEN RESPONSE:", data)  # 👈 IMPORTANTE

    if not data.get("success"):
        raise Exception(data)  # 👈 ahora verás el error real

    return data["result"]["access_token"]
def send_command(commands):
    token = get_token()
    t = str(int(time.time() * 1000))
    url_path = f"/v1.0/devices/{DEVICE_ID}/commands"

    body = json.dumps({"commands": commands})
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

@router.get("/on/{num}")
def on(num: int):
    return send_command([{"code": f"switch_{num}", "value": True}])

@router.get("/off/{num}")
def off(num: int):
    return send_command([{"code": f"switch_{num}", "value": False}])

@router.get("/all/on")
def all_on():
    return send_command([
        {"code": "switch_1", "value": True},
        {"code": "switch_2", "value": True},
        {"code": "switch_3", "value": True},
        {"code": "switch_4", "value": True},
    ])

@router.get("/all/off")
def all_off():
    return send_command([
        {"code": "switch_1", "value": False},
        {"code": "switch_2", "value": False},
        {"code": "switch_3", "value": False},
        {"code": "switch_4", "value": False},
    ])
