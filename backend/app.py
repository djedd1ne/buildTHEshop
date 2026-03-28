from flask import Flask, jsonify, redirect, request
from flask_cors import CORS
import psycopg2
import os
import requests
import jwt
import datetime
from urllib.parse import urlencode

app = Flask(__name__)
CORS(app, supports_credentials=True)

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
            intra_id INTEGER UNIQUE NOT NULL,
            login VARCHAR(255) UNIQUE NOT NULL,
            email VARCHAR(255),
            display_name VARCHAR(255),
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.route("/")
def home():
    return jsonify({"message": "Flask backend is running!"})

@app.route("/db")
def test_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT NOW();")
        result = cur.fetchone()
        cur.close()
        conn.close()
        return jsonify({
            "message": "Database connected successfully",
            "time": str(result[0])
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/auth/42/login")
def auth_42_login():
    client_id = require_env("FORTYTWO_CLIENT_ID")
    redirect_uri = require_env("FORTYTWO_REDIRECT_URI")

    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
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

        intra_id = user_data["id"]
        login = user_data["login"]
        email = user_data.get("email")
        display_name = user_data.get("displayname")
        image_url = None

        image = user_data.get("image")
        if isinstance(image, dict):
            versions = image.get("versions") or {}
            image_url = versions.get("medium") or versions.get("small")
            if not image_url:
                image_url = image.get("link")

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (intra_id, login, email, display_name, image_url)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (intra_id)
            DO UPDATE SET
                login = EXCLUDED.login,
                email = EXCLUDED.email,
                display_name = EXCLUDED.display_name,
                image_url = EXCLUDED.image_url
            RETURNING id, intra_id, login, email, display_name, image_url;
        """, (intra_id, login, email, display_name, image_url))
        saved_user = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        payload = {
            "user": {
                "id": saved_user[0],
                "intra_id": saved_user[1],
                "login": saved_user[2],
                "email": saved_user[3],
                "display_name": saved_user[4],
                "image_url": saved_user[5]
            },
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }

        app_jwt = jwt.encode(payload, require_env("APP_SECRET"), algorithm="HS256")
        frontend_url = require_env("FRONTEND_URL")

        return redirect(f"{frontend_url}/auth-success?token={app_jwt}")

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