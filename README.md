# Distributed URL Shortener

A high-performance, production-grade URL shortening platform built with **FastAPI** and designed to evolve step-by-step into a highly scalable distributed system. 

This project is structured in stages to demonstrate key system design principles: transition from local in-memory storage to relational databases, implementation of caching layers, decoupled background processing queues, rate limiting, and containerization.

---

## 🚀 Current Status: Phase 1 — Project Setup & In-Memory MVP

We have established the core backend skeleton and built an in-memory, thread-safe URL shortening MVP. This serves as the system's architectural foundation before introducing external database or caching infrastructures.

### Key Features Implemented:
* **Modular Codebase**: A clean, scalable directory structure separating routes, schemas, services, and storage repositories.
* **FastAPI Entrypoint**: Clean routing with automatic documentation generation (Swagger UI at `/docs`).
* **Thread-Safe Mock DB**: A thread-safe `InMemoryStorage` mock utilizing a Python dictionary protected by a `threading.Lock()` to handle concurrent concurrent requests safely.
* **Cryptographically Secure Short Codes**: A generator utilizing Python's `secrets` module and a 62-character alphanumeric alphabet (Base62 character set).
* **HTTP 307 Temporary Redirection**: Intentionally chose `307 Temporary Redirect` over `301 Permanent Redirect` to prevent client-side browser caching. This ensures every link access routes through our backend, laying the groundwork for accurate analytics tracking in future phases.
* **CORS Middleware Integration**: Prepared for front-end dashboard consumption.

---

## 📐 Architecture (Phase 1)

```text
User Request (POST /shorten)  ──► [ FastAPI Gateway ] ──► [ Schema Validation ]
                                         │
                                         ▼
                               [ Code Generator ] (Secrets, Base62 set)
                                         │
                                         ▼
                               [ InMemoryStorage ] (Thread-Safe Dictionary Lock)
                                         │
                                         ▼
User Request (GET /{code})   ──► [ FastAPI Redirect ] ──► HTTP 307 Temporary Redirect
```

---

## 🛠️ Getting Started & Running Locally

### 1. Prerequisites
* Python 3.12+ installed.

### 2. Installation
Clone the repository and navigate to the project directory:
```bash
git clone https://github.com/aamir-sidd/Distributed-URL-Shortener.git
cd Distributed-URL-Shortener
```

Create a virtual environment and activate it:
* **Windows**:
  ```bash
  python -m venv .venv
  .\.venv\Scripts\activate
  ```
* **macOS/Linux**:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Running the Server
Start the development server using Uvicorn:
```bash
uvicorn app.main:app --reload
```
The API will be available locally at `http://127.0.0.1:8000`. You can explore and test the interactive API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

---

## 🧪 Testing the API

We maintain a self-contained, standard-library-only test suite in `test_api.py` that validates all core features without requiring any external testing tools:

Run the tests using the virtual environment python interpreter:
```bash
python test_api.py
```

### Expected Output:
```text
[INFO] Starting URL Shortener API Tests...
[SUCCESS] Health Check Passed: {'status': 'healthy', 'service': 'Distributed URL Shortener'}
[SUCCESS] Shorten URL Passed: {'original_url': 'https://github.com/fastapi/fastapi', 'short_code': 'dGPx7H', 'short_url': 'http://127.0.0.1:8000/dGPx7H'}
[SUCCESS] Validation Passed: Correctly rejected invalid URL (HTTP 422)
[SUCCESS] Redirection Passed: Redirected to https://github.com/fastapi/fastapi (HTTP 307)
[SUCCESS] Missing Code Passed: Returned HTTP 404

[INFO] API verification complete!
```

---

## 🔮 Roadmap & Evolving System Design

* **Phase 2 (Next)**: Integrate **PostgreSQL** with **SQLAlchemy ORM** and **Alembic** migrations to transition to persistent storage.
* **Phase 3**: Implement mathematical **Base62 ID encoding** and sophisticated collision-handling strategies.
* **Phase 4**: Add user authentication (JWT-based) for secure account and short-link management.
* **Phase 5**: Introduce click analytics gathering.
* **Phase 6**: Incorporate a **Redis Caching layer** using the cache-aside pattern to reduce database query load.
* **Phase 7**: Add asynchronous processing with **Celery/RQ** and **Redis** to offload analytics writes from the main thread.
* **Phase 8**: Containerize the entire application using **Docker** and orchestrate multi-container services with **Docker Compose**.
