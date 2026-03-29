# buildTHEshop
A full-stack virtual marketplace built for 42 students, where campus perks and privileges can be purchased using **MARVINS** — a virtual currency derived from your 42 Intra stats.

Your evaluation points, wallet, coalition score, and threshold from learning hub are automatically converted into MARVINS the first time you log in. Spend them wisely on perks like skipping the eval queue, reserving a desk, or getting your meme featured on campus screens.

![Vue.js](https://img.shields.io/badge/Vue.js-3-4FC08D?logo=vuedotjs&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3-06B6D4?logo=tailwindcss&logoColor=white)

## Setup

1. Clone the repo
2. Copy the  env sample and fill in your credentials:

3. .env sample
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_strong_password_here
POSTGRES_DB=hackathondb

FORTYTWO_CLIENT_ID=your_42_client_id
FORTYTWO_CLIENT_SECRET=your_42_client_secret
FORTYTWO_REDIRECT_URI=http://localhost:5000/auth/42/callback

LEARNINGHUB_CLIENT_ID=your_learninghub_client_id
LEARNINGHUB_CLIENT_SECRET=your_learninghub_client_secret
LEARNINGHUB_REDIRECT_URI=http://localhost:5000/auth/learninghub/callback

FRONTEND_URL=http://localhost:5173
APP_SECRET=your_random_secret_key_here

```

4. Start the app:
```bash
docker compose up --build
```

5. Open http://localhost:5173

## System Design

### Container Architecture

```mermaid
graph TB
    subgraph Docker Network
        subgraph frontend_container["🖥️ Frontend Container"]
            VUE["Vue 3 + Vite<br/>Port 5173"]
        end

        subgraph backend_container["⚙️ Backend Container"]
            FLASK["Flask API<br/>Port 5000"]
        end

        subgraph db_container["🗄️ Database Container"]
            PG["PostgreSQL 15<br/>Port 5432"]
            VOL[("📦 postgres_data<br/>Named Volume")]
        end

        FLASK -->|"SQL Queries<br/>psycopg2"| PG
        PG --- VOL
    end

    BROWSER["🌐 Browser"] -->|"http://localhost:5173"| VUE
    BROWSER -->|"http://localhost:5000<br/>REST API + JWT"| FLASK
    VUE -.->|"API Calls<br/>fetch()"| FLASK

    subgraph external["☁️ External APIs"]
        INTRA["42 Intra API<br/>api.intra.42.fr"]
        LH["Learning Hub<br/>intranet.42heilbronn.de"]
    end

    FLASK -->|"OAuth + User Data"| INTRA
    FLASK -->|"OAuth PKCE"| LH

    style frontend_container fill:#1e1b4b,stroke:#6366f1,color:#e0e7ff
    style backend_container fill:#0c4a6e,stroke:#22d3ee,color:#e0f2fe
    style db_container fill:#14532d,stroke:#4ade80,color:#dcfce7
    style external fill:#451a03,stroke:#f59e0b,color:#fef3c7
    style BROWSER fill:#020617,stroke:#94a3b8,color:#f8fafc
    style VOL fill:#14532d,stroke:#4ade80,color:#dcfce7
```

### Authentication Flow

```mermaid
sequenceDiagram
    actor User
    participant FE as 🖥️ Frontend<br/>localhost:5173
    participant BE as ⚙️ Backend<br/>localhost:5000
    participant API as ☁️ 42 Intra API
    participant DB as 🗄️ PostgreSQL

    User->>FE: Click "Login with 42"
    FE->>BE: GET /auth/42/login
    BE-->>User: Redirect to 42 OAuth

    User->>API: Authorize app
    API-->>BE: GET /auth/42/callback?code=xxx

    BE->>API: Exchange code for access_token
    API-->>BE: access_token

    BE->>API: GET /v2/me (profile)
    API-->>BE: user data (wallet, eval points)

    BE->>API: GET /v2/users/:id/coalitions_users
    API-->>BE: coalition score

    BE->>DB: User exists?

    alt New User
        DB-->>BE: No
        BE->>BE: Compute MARVINS from 42 stats
        BE->>DB: INSERT user with balance
    else Existing User
        DB-->>BE: Yes (with current balance)
        BE->>DB: UPDATE profile only (keep balance)
    end

    BE->>BE: Create JWT token
    BE-->>FE: Redirect with ?token=jwt

    FE->>FE: Store JWT in localStorage
    FE->>BE: GET /me (Bearer token)
    BE->>DB: SELECT fresh user data
    DB-->>BE: User row
    BE-->>FE: User JSON
    FE->>FE: Show marketplace
```

### Purchase Flow

```mermaid
sequenceDiagram
    actor User
    participant FE as 🖥️ Frontend
    participant BE as ⚙️ Backend
    participant DB as 🗄️ PostgreSQL

    User->>FE: Click "Buy" on product
    FE->>FE: Show confirmation modal

    User->>FE: Click "Confirm"
    FE->>BE: POST /api/purchase<br/>{"name", "price", "emoji"}

    BE->>DB: SELECT balance FOR UPDATE<br/>(row lock)
    DB-->>BE: current_balance

    alt Sufficient Balance
        BE->>DB: UPDATE balance = balance - price
        BE->>DB: INSERT INTO orders
        DB-->>BE: order_id, created_at
        BE-->>FE: ✅ {new_balance, order_id}
        FE->>FE: Update balance, show success
    else Insufficient Balance
        BE-->>FE: ❌ {error: "Insufficient MARVINS"}
        FE->>FE: Show failure modal
    end
```

### MARVINS Conversion

```mermaid
graph LR
    subgraph input["42 Intra Stats"]
        EP["Evaluation Points"]
        CS["Coalition Score"]
        WL["Wallet"]
        TH["Threshold"]
    end

    subgraph convert["Conversion"]
        EP -->|"× 1"| SUM
        CS -->|"÷ 100"| SUM
        WL -->|"÷ 100"| SUM
        TH -->|"× 1"| SUM
    end

    SUM["➕ Total"] -->|"First login only"| BAL["🪙 MARVINS Balance"]
    BAL -->|"Purchases deduct"| ORDERS["📦 Orders"]

    style input fill:#1e1b4b,stroke:#6366f1,color:#e0e7ff
    style convert fill:#0c4a6e,stroke:#22d3ee,color:#e0f2fe
    style BAL fill:#14532d,stroke:#4ade80,color:#dcfce7
    style ORDERS fill:#451a03,stroke:#f59e0b,color:#fef3c7
```

### Docker Compose Port Mapping

```mermaid
graph LR
    subgraph host["🖥️ Host Machine"]
        P1["localhost:5173"]
        P2["localhost:5000"]
        P3["localhost:5432"]
    end

    subgraph docker["🐳 Docker Network"]
        FE["vue_frontend<br/>:5173"]
        BE["flask_backend<br/>:5000"]
        DB["postgres_db<br/>:5432"]
    end

    P1 -->|"Published"| FE
    P2 -->|"Published"| BE
    P3 -->|"Published"| DB

    FE -.->|"API calls via<br/>browser (host)"| P2
    BE -->|"Connects via<br/>hostname 'db'"| DB

    style host fill:#020617,stroke:#94a3b8,color:#f8fafc
    style docker fill:#0f172a,stroke:#6366f1,color:#e0e7ff
```