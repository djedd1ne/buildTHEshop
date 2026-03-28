from flask import Flask, jsonify, redirect, request
from flask_cors import CORS
import psycopg2
import os
import requests
import jwt
import datetime
from urllib.parse import urlencode
import secrets
import hashlib
import base64

app = Flask(__name__)
CORS(app)

pkce_store = {}

def require_env(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=require_env("DB_NAME"),
        user=require_env("DB_USER"),
        password=require_env("DB_PASSWORD")
    )

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            provider VARCHAR(50) NOT NULL,
            provider_user_id VARCHAR(255) NOT NULL,
            login VARCHAR(255),
            email VARCHAR(255),
            display_name VARCHAR(255),
            image_url TEXT,
            balance_marvins INTEGER DEFAULT 1337,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(provider, provider_user_id)
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def create_app_token(user_row):
    payload = {
        "user": {
            "id": user_row[0],
            "provider": user_row[1],
            "provider_user_id": user_row[2],
            "login": user_row[3],
            "email": user_row[4],
            "display_name": user_row[5],
            "image_url": user_row[6],
            "balance_marvins": user_row[7]
        },
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, require_env("APP_SECRET"), algorithm="HS256")

def upsert_user(provider, provider_user_id, login, email, display_name, image_url):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (provider, provider_user_id, login, email, display_name, image_url)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (provider, provider_user_id)
        DO UPDATE SET
            login = EXCLUDED.login,
            email = EXCLUDED.email,
            display_name = EXCLUDED.display_name,
            image_url = EXCLUDED.image_url
        RETURNING id, provider, provider_user_id, login, email, display_name, image_url, balance_marvins;
    """, (provider, provider_user_id, login, email, display_name, image_url))
    user_row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return user_row

def generate_pkce_pair():
    code_verifier = secrets.token_urlsafe(64)
    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).decode().rstrip("=")
    return code_verifier, challenge

@app.route("/")
def home():
    return jsonify({"message": "Flask backend is running!"})

@app.route("/auth/42/login")
def auth_42_login():
    params = {
        "client_id": require_env("FORTYTWO_CLIENT_ID"),
        "redirect_uri": require_env("FORTYTWO_REDIRECT_URI"),
        "response_type": "code",
        "scope": "public"
    }
    auth_url = f"https://api.intra.42.fr/oauth/authorize?{urlencode(params)}"
    return redirect(auth_url)

@app.route("/auth/42/callback")
def auth_42_callback():
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "Missing authorization code"}), 400

    try:
        token_response = requests.post(
            "https://api.intra.42.fr/oauth/token",
            data={
                "grant_type": "authorization_code",
                "client_id": require_env("FORTYTWO_CLIENT_ID"),
                "client_secret": require_env("FORTYTWO_CLIENT_SECRET"),
                "code": code,
                "redirect_uri": require_env("FORTYTWO_REDIRECT_URI")
            },
            timeout=10
        )
        token_response.raise_for_status()
        token_data = token_response.json()
        access_token = token_data.get("access_token")

        user_response = requests.get(
            "https://api.intra.42.fr/v2/me",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10
        )
        user_response.raise_for_status()
        user_data = user_response.json()

        provider = "42"
        provider_user_id = str(user_data["id"])
        login = user_data.get("login")
        email = user_data.get("email")
        display_name = user_data.get("displayname")

        image_url = None
        image = user_data.get("image")
        if isinstance(image, dict):
            versions = image.get("versions") or {}
            image_url = versions.get("medium") or versions.get("small") or image.get("link")

        user_row = upsert_user(provider, provider_user_id, login, email, display_name, image_url)
        token = create_app_token(user_row)

        return redirect(f"{require_env('FRONTEND_URL')}?token={token}")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/auth/learninghub/login")
def auth_learninghub_login():
    code_verifier, code_challenge = generate_pkce_pair()
    state = secrets.token_urlsafe(32)

    pkce_store[state] = code_verifier

    params = {
        "client_id": require_env("LEARNINGHUB_CLIENT_ID"),
        "redirect_uri": require_env("LEARNINGHUB_REDIRECT_URI"),
        "response_type": "code",
        "scope": "openid profile email",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "state": state
    }

    auth_url = f"https://intranet.42heilbronn.de/oauth/authorize?{urlencode(params)}"
    return redirect(auth_url)

@app.route("/auth/learninghub/callback")
def auth_learninghub_callback():
    code = request.args.get("code")
    state = request.args.get("state")

    if not code or not state:
        return jsonify({"error": "Missing code or state"}), 400

    code_verifier = pkce_store.pop(state, None)
    if not code_verifier:
        return jsonify({"error": "Invalid or expired state"}), 400

    try:
        token_response = requests.post(
            "https://intranet.42heilbronn.de/oauth/token",
            data={
                "grant_type": "authorization_code",
                "client_id": require_env("LEARNINGHUB_CLIENT_ID"),
                "client_secret": require_env("LEARNINGHUB_CLIENT_SECRET"),
                "code": code,
                "redirect_uri": require_env("LEARNINGHUB_REDIRECT_URI"),
                "code_verifier": code_verifier
            },
            timeout=10
        )
        token_response.raise_for_status()
        token_data = token_response.json()
        access_token = token_data.get("access_token")

        user_response = requests.get(
            "https://intranet.42heilbronn.de/oauth/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10
        )
        user_response.raise_for_status()
        user_data = user_response.json()

        provider = "learninghub"
        provider_user_id = str(user_data.get("sub"))
        login = user_data.get("preferred_username") or user_data.get("username") or user_data.get("nickname")
        email = user_data.get("email")
        display_name = user_data.get("name") or login
        image_url = user_data.get("picture")

        user_row = upsert_user(provider, provider_user_id, login, email, display_name, image_url)
        token = create_app_token(user_row)

        return redirect(f"{require_env('FRONTEND_URL')}?token={token}")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/me")
def me():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing bearer token"}), 401

    token = auth_header.split(" ", 1)[1]

    try:
        payload = jwt.decode(token, require_env("APP_SECRET"), algorithms=["HS256"])
        return jsonify(payload["user"])
    except Exception as e:
        return jsonify({"error": str(e)}), 401

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)