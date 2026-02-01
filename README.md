# Advanced Store (Django + Next.js) — Docker Compose Dev Setup

A monorepo starter for an advanced store project:

- **Backend:** Django + Django REST Framework
- **Frontend:** Next.js (App Router, TypeScript)
- **Database:** PostgreSQL
- **Cache / Broker:** Redis
- **Orchestration:** Docker + Docker Compose

This repository is designed for a clean workflow where:

- **Next.js owns the website/UI** (root routes `/`)
- **Django owns the API** (recommended under `/api/`)

---

## Repository Structure

advanced-store-django-next/
backend/ # Django project lives here
frontend/ # Next.js project lives here
compose/
docker-compose.dev.yml
docker-compose.prod.yml # later
docker/
backend/Dockerfile.dev
frontend/Dockerfile.dev
nginx/ # later for production
envs/
.env.dev.example
.env.prod.example
docs/ # course deliverables: research/diagram/schema
README.md
.gitignore


---

## Requirements

- Docker Desktop (Windows/macOS/Linux)
- Docker Compose v2 (included in Docker Desktop)
- Git

---

## Environment Variables

Create a `.env.dev` file in:

envs/.env.dev


You can start from:

envs/.env.dev.example


Example `.env.dev` (adjust as needed):

```env
# Django
DEBUG=1
DJANGO_SECRET_KEY=dev-secret-key
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Postgres
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_PORT=5432

# Redis
REDIS_URL=redis://redis:6379/0

# Frontend
NEXT_PUBLIC_API_BASE=/api
Note: In development we usually keep database ports bound to 127.0.0.1 only for safety.

Development Setup (From Scratch)
1) Clone and enter the repository
git clone https://github.com/pooryafayazi/advanced-store-django-next.git
cd advanced-store-django-next
2) (First run only) Create external volumes (if your compose uses external volumes)
If your docker-compose.dev.yml declares postgres_data_dev as external, create it once:

docker volume create postgres_data_dev
You can list volumes with:

docker volume ls
First-Time Bootstrapping (Important)
When bootstrapping Next.js, create-next-app requires the target directory to be empty.
If your compose mounts a node_modules volume (frontend_node_modules) into /usr/src/app/node_modules,
it can create the node_modules/ folder before create-next-app runs, which makes the directory "not empty".

Recommended workflow:

Generate the Next.js project first.

Then enable the node_modules volume for faster dev reloads.

Backend Bootstrapping (Django)
3) Build images
docker compose -f compose/docker-compose.dev.yml build
4) Start only DB + Redis
docker compose -f compose/docker-compose.dev.yml up -d db redis
5) Create Django project (only if backend is empty)
Run this ONLY when backend/ does not already contain a Django project:

docker compose -f compose/docker-compose.dev.yml run --rm --no-deps backend django-admin startproject core .
Frontend Bootstrapping (Next.js)
6) Create Next.js project (only if frontend is empty)
If your frontend/ folder is empty, create the Next project:

docker compose -f compose/docker-compose.dev.yml run --rm --no-deps frontend sh -lc "npx create-next-app@16.1.6 . --ts --eslint --app --src-dir --no-tailwind --use-npm"
Confirm it created:

# On Windows PowerShell
Test-Path .\frontend\package.json
Should return:

True
Start the Full Stack
7) Bring everything up
docker compose -f compose/docker-compose.dev.yml up -d
8) Install frontend dependencies (first run only)
If the frontend container logs show next: not found, you need to install dependencies:

docker compose -f compose/docker-compose.dev.yml exec frontend npm install
Verify Next is available:

docker compose -f compose/docker-compose.dev.yml exec frontend npx next --version
Apply Django Migrations
If Django logs show unapplied migrations, run:

docker compose -f compose/docker-compose.dev.yml exec backend python manage.py migrate
URLs
Frontend (Next.js): http://localhost:3000

Backend (Django): http://localhost:8000

Database (Postgres): 127.0.0.1:${POSTGRES_PORT} (usually 5432)

In a typical production setup, Nginx will serve the website and proxy /api to the backend.

Useful Docker Commands
View container status
docker compose -f compose/docker-compose.dev.yml ps
View logs
docker compose -f compose/docker-compose.dev.yml logs -f
Frontend only:

docker compose -f compose/docker-compose.dev.yml logs -f frontend
Backend only:

docker compose -f compose/docker-compose.dev.yml logs -f backend
Restart a service
docker compose -f compose/docker-compose.dev.yml restart frontend
Stop everything
docker compose -f compose/docker-compose.dev.yml down
Stop and remove volumes (WARNING: deletes DB data in non-external volumes)
docker compose -f compose/docker-compose.dev.yml down -v
Common Issues & Fixes
1) Bind for 0.0.0.0:6379 failed: port is already allocated
Another Redis is already using port 6379 on your host.
Solution: Do not publish Redis ports in dev (recommended), or change the published port.

2) npm ERR! enoent ... /usr/src/app/package.json
The Next project hasn't been created yet, or the folder is not mounted correctly.
Fix: Ensure frontend/package.json exists, and volumes points to ../frontend:/usr/src/app in compose.

3) sh: next: not found
Dependencies were not installed in the container/volume.
Fix:

docker compose -f compose/docker-compose.dev.yml exec frontend npm install
4) create-next-app refuses to run because folder is not empty
If node_modules/ exists before running create-next-app, it stops.
Fix: Make sure the target directory is empty and temporarily disable node_modules volume until after creation.