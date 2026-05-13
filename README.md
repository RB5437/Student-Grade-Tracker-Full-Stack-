# 🐳 Docker Day 31 — Student Grade Tracker
### Complete Hands-on Project | AWS Free Tier | All Docker Concepts Covered

---

## 📁 Project Structure

```
student-grade-tracker/
├── app/
│   ├── index.js            ← Node.js Express API
│   ├── package.json
│   ├── Dockerfile          ← Multi-stage build
│   ├── .dockerignore
│   └── public/
│       └── index.html      ← Frontend UI
├── nginx/
│   └── default.conf        ← Reverse proxy config
├── docker-compose.yml      ← Full stack orchestration
└── README.md
```

---

## 🏗️ Architecture

```
Internet
   │
   ▼  Port 80
┌──────────┐
│  NGINX   │  ← Reverse Proxy (frontend-network)
│ (alpine) │
└────┬─────┘
     │ proxy_pass
     ▼
┌──────────┐
│ Node.js  │  ← Express API (frontend + backend network)
│  App     │     Port 3000 (NOT exposed to internet)
└────┬─────┘
     │ mongoose
     ▼
┌──────────┐
│ MongoDB  │  ← Database (backend-network only)
│          │     Port 27017 (NOT exposed to internet)
└──────────┘
     │
     ▼
Named Volume: mongo-data (data persists forever)
```

---

## 🎯 Docker Concepts Covered

| Concept | Where Used |
|---------|-----------|
| Dockerfile | `app/Dockerfile` |
| Multi-stage Build | Stage 1 (builder) → Stage 2 (production) |
| Docker Images | Node.js app image built from Dockerfile |
| Docker Containers | 3 containers: nginx, app, mongo |
| Docker Networks | frontend-network + backend-network |
| Docker Volumes | mongo-data (named volume) |
| Docker Compose | `docker-compose.yml` |
| Health Checks | All 3 services have healthchecks |
| Non-root User | app container runs as `appuser` |
| .dockerignore | Excludes node_modules, .git |

---

## 🚀 STEP BY STEP PRACTICE ON AWS EC2

### Step 1 — Launch EC2 (AWS Free Tier)
```bash
# Use: Ubuntu 22.04 LTS, t2.micro, 20GB storage
# Security Group: open port 22 (SSH) and port 80 (HTTP)
```

### Step 2 — Install Docker & Docker Compose
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker

# Add your user to docker group (no sudo needed)
sudo usermod -aG docker ubuntu
newgrp docker

# Install Docker Compose
sudo apt install docker-compose -y

# Verify
docker --version
docker-compose --version
```

### Step 3 — Clone / Create Project
```bash
mkdir student-grade-tracker
cd student-grade-tracker

# Create folder structure
mkdir -p app/public nginx
```

### Step 4 — Create all files (copy from this repo)
```bash
# Create each file as shown in project structure above
# app/index.js, app/package.json, app/Dockerfile
# app/public/index.html, nginx/default.conf, docker-compose.yml
```

---

## 🔬 PRACTICE COMMANDS — One by One

### PART 1 — Docker Images Practice

```bash
# Build image manually (without compose)
docker build -t grade-app:v1 ./app

# See image size — notice multi-stage result
docker images grade-app

# Build with specific stage (builder stage — larger)
docker build --target builder -t grade-app:builder ./app

# Compare sizes
docker images | grep grade-app
# grade-app:v1       → ~150MB  (production stage)
# grade-app:builder  → ~300MB  (all build tools included)

# Inspect image layers
docker history grade-app:v1

# Docker Scout — scan for vulnerabilities
docker scout cves grade-app:v1

# Docker Init — auto-generate Dockerfile (bonus!)
mkdir test-init && cd test-init
docker init
cd ..
```

### PART 2 — Docker Containers Practice

```bash
# Run MongoDB container manually
docker run -d \
  --name test-mongo \
  -e MONGO_INITDB_DATABASE=gradesdb \
  -p 27017:27017 \
  mongo:6.0

# Check container running
docker ps
docker ps -a   # shows stopped containers too

# Container logs
docker logs test-mongo
docker logs -f test-mongo   # follow logs

# Execute commands inside container
docker exec -it test-mongo mongosh
# Inside mongo shell:
show dbs
use gradesdb
db.students.find()
exit

# Container stats (CPU, Memory)
docker stats test-mongo

# Inspect container details
docker inspect test-mongo

# Stop and remove
docker stop test-mongo
docker rm test-mongo
```

### PART 3 — Docker Networks Practice

```bash
# See default networks
docker network ls

# Create custom networks
docker network create frontend-network
docker network create backend-network

# Inspect network
docker network inspect frontend-network

# Run mongo on backend-network
docker run -d \
  --name mongo-net-test \
  --network backend-network \
  mongo:6.0

# Run app on both networks
docker run -d \
  --name app-net-test \
  --network backend-network \
  -e MONGO_URL=mongodb://mongo-net-test:27017/gradesdb \
  -e PORT=3000 \
  grade-app:v1

# Connect app to frontend-network too
docker network connect frontend-network app-net-test

# Test: can app reach mongo?
docker exec -it app-net-test ping mongo-net-test
# YES — same network

# Test: can nginx reach mongo directly?
docker run --rm --network frontend-network alpine ping mongo-net-test
# NO — different network = ISOLATED

# Cleanup
docker stop mongo-net-test app-net-test
docker rm mongo-net-test app-net-test
docker network rm frontend-network backend-network
```

### PART 4 — Docker Volumes Practice

```bash
# Create named volume
docker volume create mongo-data

# List volumes
docker volume ls

# Inspect volume (see where data is stored)
docker volume inspect mongo-data

# Run mongo WITH named volume
docker run -d \
  --name mongo-vol-test \
  --network bridge \
  -v mongo-data:/data/db \
  mongo:6.0

# Add some data
docker exec -it mongo-vol-test mongosh
use gradesdb
db.students.insertOne({name:"Ritik", subject:"Docker", marks:95, grade:"A+"})
db.students.find()
exit

# KILL the container (data should survive!)
docker rm -f mongo-vol-test

# Restart with SAME volume — data still there?
docker run -d \
  --name mongo-vol-test2 \
  -v mongo-data:/data/db \
  mongo:6.0

docker exec -it mongo-vol-test2 mongosh gradesdb --eval "db.students.find()"
# YOUR DATA IS STILL THERE! ✅ That's volume persistence!

# Cleanup
docker rm -f mongo-vol-test2
docker volume rm mongo-data
```

### PART 5 — Docker Compose Practice (FULL STACK!)

```bash
# Start entire stack with one command
docker-compose up -d

# Watch all containers start (in order due to depends_on)
docker-compose ps

# Watch logs of all services
docker-compose logs -f

# Watch specific service logs
docker-compose logs -f app
docker-compose logs -f mongo

# Check health status
docker inspect grade-mongo | grep -A 5 "Health"
docker inspect grade-app | grep -A 5 "Health"

# Scale app (run 2 instances)
docker-compose up -d --scale app=2
docker-compose ps  # see 2 app containers!

# Test the app
curl http://localhost/health
curl http://localhost/api/students

# Add a student via API
curl -X POST http://localhost/api/students \
  -H "Content-Type: application/json" \
  -d '{"name":"Ritik","subject":"Docker","marks":98}'

# Open in browser
# http://<your-ec2-public-ip>
```

### PART 6 — Docker Compose Advanced Commands

```bash
# Stop all containers (data preserved in volumes)
docker-compose stop

# Start again
docker-compose start

# Restart specific service
docker-compose restart app

# Rebuild image and restart
docker-compose up -d --build

# Remove containers (but keep volumes)
docker-compose down

# Remove containers AND volumes (DANGER! data lost)
docker-compose down -v

# View resource usage
docker-compose top
```

---

## 🔬 Multi-Stage Build Comparison

```bash
# Build production stage
docker build --target production -t grade-app:prod ./app
docker images grade-app:prod
# Expected: ~150-180MB

# Build builder stage (includes all build tools)
docker build --target builder -t grade-app:builder ./app
docker images grade-app:builder
# Expected: ~300-400MB

# Difference = what multi-stage removes!
echo "Multi-stage saved you ~200MB per image!"
echo "At 100 pulls/day = 20GB bandwidth saved daily"
```

---

## 🔒 Docker Scout & Security

```bash
# Scan your image for CVEs
docker scout cves grade-app:prod

# Quick summary
docker scout quickview grade-app:prod

# Recommendations for base image
docker scout recommendations grade-app:prod

# Compare two images
docker scout compare grade-app:prod grade-app:builder
```

---

## 🪄 Docker Init (Bonus!)

```bash
# In a new folder with any app
mkdir my-python-app && cd my-python-app
echo "print('hello')" > app.py

# Docker Init auto-generates Dockerfile + compose!
docker init

# It asks: what language? Python/Node/Go/etc
# Then generates everything automatically!
ls -la
# Dockerfile, docker-compose.yml, .dockerignore — all created!
```

---

## ✅ What You Practiced Today (Day 31)

| # | Concept | Practice Done |
|---|---------|--------------|
| 1 | Dockerfile | Multi-stage build for Node.js |
| 2 | Multi-stage Build | Builder → Production (size comparison) |
| 3 | Docker Images | Build, tag, inspect, compare sizes |
| 4 | Docker Containers | Run, exec, logs, stats, inspect |
| 5 | Docker Networks | Custom bridge, network isolation |
| 6 | Docker Volumes | Named volume, data persistence test |
| 7 | Docker Compose | Full 3-tier stack |
| 8 | Health Checks | All services monitored |
| 9 | Docker Scout | Vulnerability scanning |
| 10 | Docker Init | Auto-generate Dockerfile |

---

## 🐛 Common Errors & Fixes

| Error | Reason | Fix |
|-------|--------|-----|
| `cannot connect to mongo` | depends_on not waiting | Use `condition: service_healthy` |
| `permission denied` | Running as root | Add `USER appuser` in Dockerfile |
| `port already in use` | Port 80 taken | `sudo lsof -i :80` then kill |
| `network not found` | Compose network issue | `docker-compose down` then `up` |
| `volume not persisting` | Using bind mount not named volume | Use `volume-name:/path` format |

---

## 📊 Architecture Summary

```
What's isolated:
├── MongoDB → backend-network ONLY (not reachable from internet)
├── Node App → both networks (bridge between nginx and mongo)
└── Nginx → frontend-network + port 80 exposed

What persists:
├── mongo-data volume → survives container restarts/removal
└── mongo-logs volume → log persistence

What's secure:
├── Non-root user in Node container
├── .dockerignore prevents node_modules in image
├── MongoDB NOT exposed on host ports
└── Health checks ensure traffic only to healthy containers
```

---

## 🚀 GitHub Upload

```bash
git init
git add .
git commit -m "Day 31 - Docker complete project: multi-stage, compose, volumes, networks"
git remote add origin https://github.com/YOUR_USERNAME/docker-day31
git push -u origin main
```

---

**Day 31 Complete! 🎉 Tomorrow Day 32 — Docker project revision + Jenkins prep!**

> Resources: [Shubham Londhe Docker One Shot](https://www.youtube.com/watch?v=docker-one-shot) | [Docker Docs](https://docs.docker.com)
