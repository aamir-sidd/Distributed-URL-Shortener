# Distributed URL Shortener — Project Milestones

A staged roadmap for building a production-style distributed URL shortening service using FastAPI.

---

# Goal

Build a URL shortening platform that evolves from a simple CRUD backend into a distributed system with:

- caching
- background workers
- async processing
- analytics pipelines
- scalability concepts
- deployment infrastructure

Final architecture target:

```text
Frontend
   ↓
FastAPI Gateway
   ↓
Redis Cache
   ↓
PostgreSQL

Analytics Events
   ↓
Message Queue
   ↓
Background Workers
```

---

# Suggested Tech Stack

## Core Backend
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic

## Distributed Components
- Redis
- Celery or RQ
- Docker Compose

## Optional Frontend
- React
- TailwindCSS

## Deployment
- Render / Railway / Fly.io

---

# Milestone 0 — Project Setup

## Goal
Create a clean project structure and initialize the backend.

## Learn
- virtual environments
- FastAPI basics
- project organization
- environment variables

## Tasks
- [ ] Create GitHub repository
- [ ] Setup Python virtual environment
- [ ] Install FastAPI and Uvicorn
- [ ] Create requirements.txt
- [ ] Setup `.env`
- [ ] Create modular folder structure
- [ ] Run first FastAPI server

## Suggested Structure

```text
url-shortener/
│
├── app/
│   ├── main.py
│   ├── routes/
│   ├── models/
│   ├── services/
│   ├── database/
│   └── schemas/
│
├── requirements.txt
├── .env
└── README.md
```

---

# Milestone 1 — Basic URL Shortener MVP

## Goal
Users can shorten URLs and use short links.

## Learn
- REST APIs
- route parameters
- database CRUD
- redirects

## Features
- [ ] Create short URL
- [ ] Store original URL in database
- [ ] Redirect short URL to original URL
- [ ] Handle invalid short codes

## Endpoints

```text
POST /shorten
GET /{short_code}
```

## Example Flow

```text
User submits long URL
        ↓
Generate short code
        ↓
Store in DB
        ↓
Return short URL
```

## Bonus
- [ ] Validate URLs
- [ ] Prevent duplicate URLs

---

# Milestone 2 — PostgreSQL + ORM

## Goal
Move from temporary storage to production-style database.

## Learn
- PostgreSQL
- SQLAlchemy ORM
- migrations
- database sessions

## Tasks
- [ ] Install PostgreSQL
- [ ] Setup SQLAlchemy
- [ ] Create URL model
- [ ] Create migrations with Alembic
- [ ] Persist data permanently

## Suggested Table

| Column | Type |
|---|---|
| id | integer |
| original_url | text |
| short_code | varchar |
| created_at | timestamp |

---

# Milestone 3 — Better Short Code Generation

## Goal
Improve reliability and scalability.

## Learn
- collision handling
- hashing
- Base62 encoding
- distributed ID concepts

## Tasks
- [ ] Implement random short code generation
- [ ] Handle collisions
- [ ] Try Base62 encoding
- [ ] Benchmark code generation speed

## Bonus
- [ ] Custom aliases

Example:

```text
/fastapi
/openai
/github
```

---

# Milestone 4 — User Authentication

## Goal
Allow users to manage their own links.

## Learn
- JWT authentication
- password hashing
- protected routes
- user relationships

## Features
- [ ] User signup
- [ ] Login
- [ ] JWT tokens
- [ ] User-specific URLs
- [ ] Delete links
- [ ] View own links

## Endpoints

```text
POST /signup
POST /login
GET /my-links
DELETE /link/{id}
```

---

# Milestone 5 — Analytics Tracking

## Goal
Track URL usage.

## Learn
- event tracking
- analytics systems
- logging patterns

## Features
- [ ] Track click count
- [ ] Track timestamps
- [ ] Store browser/device info
- [ ] Store referrer data

## Important Concept

DO NOT block redirects for analytics writes.

Redirects must remain fast.

---

# Milestone 6 — Redis Caching

## Goal
Reduce database load.

## Learn
- caching strategies
- Redis basics
- cache-aside pattern

## Flow

```text
Request
   ↓
Check Redis
   ↓
If miss → PostgreSQL
   ↓
Store in Redis
```

## Tasks
- [ ] Setup Redis
- [ ] Cache URL mappings
- [ ] Add cache expiration
- [ ] Benchmark response times

## Metrics to Compare
- redirect latency with cache
- redirect latency without cache

---

# Milestone 7 — Async Analytics Workers

## Goal
Convert analytics into a distributed workflow.

## Learn
- message queues
- async workers
- event-driven systems
- task queues

## Architecture

```text
Redirect Request
      ↓
Push analytics event to queue
      ↓
Return redirect immediately
      ↓
Worker processes analytics later
```

## Stack Options
- Celery + Redis
- RQ + Redis

## Tasks
- [ ] Setup task queue
- [ ] Create analytics worker
- [ ] Send events asynchronously
- [ ] Retry failed jobs

## THIS is where the project becomes a real distributed system.

---

# Milestone 8 — Dockerization

## Goal
Containerize the application.

## Learn
- Docker
- Docker Compose
- service orchestration

## Services
- API
- PostgreSQL
- Redis
- Worker

## Tasks
- [ ] Create Dockerfile
- [ ] Create docker-compose.yml
- [ ] Run all services together
- [ ] Setup environment configs

## Final Compose Target

```text
api
postgres
redis
worker
frontend
```

---

# Milestone 9 — Rate Limiting

## Goal
Prevent abuse/spam.

## Learn
- Redis counters
- sliding window algorithms
- API protection

## Features
- [ ] Limit link creation requests
- [ ] Limit redirects per IP
- [ ] Temporary bans

## Example

```text
100 requests per minute
```

---

# Milestone 10 — Frontend Dashboard

## Goal
Create a usable UI.

## Learn
- React basics
- API integration
- authentication flows

## Features
- [ ] Login page
- [ ] Dashboard
- [ ] Create links
- [ ] View analytics
- [ ] Delete links

## Optional
- [ ] Dark mode
- [ ] QR code display
- [ ] Charts

---

# Milestone 11 — Real-Time Analytics

## Goal
Show live click updates.

## Learn
- WebSockets
- SSE
- real-time systems

## Features
- [ ] Live click counter
- [ ] Real-time dashboard updates
- [ ] Active visitors display

---

# Milestone 12 — Deployment

## Goal
Deploy production version.

## Learn
- cloud deployment
- environment management
- production configs

## Tasks
- [ ] Deploy backend
- [ ] Deploy PostgreSQL
- [ ] Deploy Redis
- [ ] Configure environment variables
- [ ] Setup HTTPS

## Recommended Platforms
- Render
- Railway
- Fly.io

---

# Milestone 13 — Advanced Features

Choose optional advanced additions.

---

## Option A — Expiring Links

Features:
- self-destruct links
- time-limited URLs

Learn:
- scheduled cleanup jobs
- TTL systems

---

## Option B — Geo Analytics

Features:
- country tracking
- click heatmaps

Learn:
- IP geolocation
- external APIs

---

## Option C — QR Code Generation

Features:
- QR download
- QR previews

Learn:
- image generation
- file handling

---

## Option D — URL Preview Metadata

Features:
- fetch page title
- thumbnail preview
- description preview

Learn:
- async scraping
- metadata extraction

---

## Option E — Kafka Event Streaming

Advanced distributed systems upgrade.

Architecture:

```text
URL_CLICKED event
        ↓
Kafka
        ↓
Analytics Consumer
Fraud Detection Consumer
Realtime Consumer
```

Learn:
- event streaming
- pub/sub systems
- scalable pipelines

---

# Final Resume Description Example

> Built a distributed URL shortening service using FastAPI, PostgreSQL, Redis, Docker, and asynchronous worker queues. Implemented caching, analytics pipelines, JWT authentication, and scalable event-driven architecture.

---

# Recommended Development Order

## Beginner Path

1. FastAPI basics
2. URL shortening MVP
3. PostgreSQL
4. Authentication
5. Analytics
6. Redis caching
7. Worker queues
8. Docker
9. Deployment

---

# Final Advice

Focus on:
- completing features fully
- writing clean code
- understanding WHY components exist
- documenting architecture

A smaller, well-finished distributed project is significantly stronger than a huge unfinished one.

