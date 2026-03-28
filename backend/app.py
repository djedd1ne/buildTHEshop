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

def compute_marvins(wallet=0, correction_points=0, coalition_score=0, threshold=0):
    return (
        int(correction_points or 0)
        + int(threshold or 0)
        + int((float(coalition_score or 0)) / 250)
        + int((int(wallet or 0)) / 100)
    )

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            provider VARCHAR(50),
            provider_user_id VARCHAR(255),
            login VARCHAR(255),
            email VARCHAR(255),
            display_name VARCHAR(255),
            image_url TEXT,
            balance_marvins INTEGER DEFAULT 0,
            wallet INTEGER DEFAULT 0,
            correction_points INTEGER DEFAULT 0,
            coalition_score NUMERIC(10,2) DEFAULT 0,
            threshold INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS provider VARCHAR(50);")
    cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS provider_user_id VARCHAR(255);")
    cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS login VARCHAR(255);")
    cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS email VARCHAR(255);")
    cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS display_name VARCHAR(255);")
    cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS image_url TEXT;")
    cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS balance_marvins INTEGER DEFAULT 0;")
    cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS wallet INTEGER DEFAULT 0;")
    cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS correction_points INTEGER DEFAULT 0;")
    cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS coalition_score NUMERIC(10,2) DEFAULT 0;")
    cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS threshold INTEGER DEFAULT 0;")

    cur.execute("""
        DO 
$$
BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM pg_constraint
                WHERE conname = 'users_provider_provider_user_id_key'
            ) THEN
                ALTER TABLE users
                ADD CONSTRAINT users_provider_provider_user_id_key
                UNIQUE (provider, provider_user_id);
            END IF;
        END
$$
;
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
            "balance_marvins": int(user_row[7] or 0),
            "wallet": int(user_row[8] or 0),
            "correction_points": int(user_row[9] or 0),
            "coalition_score": float(user_row[10] or 0),
            "threshold": int(user_row[11] or 0)
        },
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, require_env("APP_SECRET"), algorithm="HS256")

def upsert_user(
    provider,
    provider_user_id,
    login,
    email,
    display_name,
    image_url,
    wallet=0,
    correction_points=0,
    coalition_score=0,
    threshold=0
):
    balance_marvins = compute_marvins(wallet, correction_points, coalition_score, threshold)

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (
            provider,
            provider_user_id,
            login,
            email,
            display_name,
            image_url,
            balance_marvins,
            wallet,
            correction_points,
            coalition_score,
            threshold
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (provider, provider_user_id)
        DO UPDATE SET
            login = EXCLUDED.login,
            email = EXCLUDED.email,
            display_name = EXCLUDED.display_name,
            image_url = EXCLUDED.image_url,
            balance_marvins = EXCLUDED.balance_marvins,
            wallet = EXCLUDED.wallet,
            correction_points = EXCLUDED.correction_points,
            coalition_score = EXCLUDED.coalition_score,
            threshold = EXCLUDED.threshold
        RETURNING
            id,
            provider,
            provider_user_id,
            login,
            email,
            display_name,
            image_url,
            balance_marvins,
            wallet,
            correction_points,
            coalition_score,
            threshold;
    """, (
        provider,
        provider_user_id,
        login,
        email,
        display_name,
        image_url,
        balance_marvins,
        int(wallet or 0),
        int(correction_points or 0),
        float(coalition_score or 0),
        int(threshold or 0)
    ))
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

def extract_personal_coalition_score(access_token, user_id):
    try:
        response = requests.get(
            f"https://api.intra.42.fr/v2/users/{user_id}/coalitions_users",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        if not isinstance(data, list) or len(data) == 0:
            return 0

        scores = []
        for item in data:
            if isinstance(item, dict) and item.get("score") is not None:
                try:
                    scores.append(float(item.get("score")))
                except Exception:
                    pass

        if not scores:
            return 0

        return max(scores)
    except Exception:
        return 0

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

        wallet = user_data.get("wallet", 0) or 0
        correction_points = user_data.get("correction_point", 0) or 0
        coalition_score = extract_personal_coalition_score(access_token, provider_user_id)
        threshold = 0

        user_row = upsert_user(
            provider,
            provider_user_id,
            login,
            email,
            display_name,
            image_url,
            wallet,
            correction_points,
            coalition_score,
            threshold
        )

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

        user_row = upsert_user(
            provider,
            provider_user_id,
            login,
            email,
            display_name,
            image_url,
            0,
            0,
            0,
            0
        )

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