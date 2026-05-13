# Student Grade Tracker Full Stack Application

## Project Overview

This project is a Dockerized Full Stack Application with:

* Frontend: Nginx Static Website
* Backend: Python Flask API with Gunicorn
* Database: MySQL 8.0
* Docker Compose Orchestration
* Health Checks
* Persistent Volumes
* Custom Docker Network

---

# Project Structure

```bash
Student-Grade-Tracker-Full-Stack-
│
├── backend/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
│
├── frontend/
│   ├── Dockerfile
│   ├── index.html
│   └── nginx.conf
│
├── docker-compose.yml
└── README.md
```

---

# Prerequisites

Install the following:

* Docker
* Docker Compose
* AWS EC2 Ubuntu Instance (Optional)

Check versions:

```bash
docker --version
docker compose version
```

---

# Clone Repository

```bash
git clone <repository-url>
cd Student-Grade-Tracker-Full-Stack-
```

---

# Build Docker Images Manually

## Build Backend Image

```bash
docker build -t grade-backend:v1 ./backend
```

## Build Frontend Image

```bash
docker build -t grade-frontend:v1 ./frontend
```

## Verify Images

```bash
docker images
```

---

# Run Complete Application

## Start Containers

```bash
docker compose up --build
```

## Run in Background

```bash
docker compose up -d --build
```

---

# Verify Running Containers

```bash
docker ps
```

Expected Containers:

* grade-tracker-mysql
* grade-tracker-backend
* grade-tracker-frontend

---

# Access Application

## Local Machine

Open browser:

```bash
http://localhost
```

## AWS EC2 Instance

Get Public IP:

```bash
curl ifconfig.me
```

Open browser:

```bash
http://<EC2-PUBLIC-IP>
```

Example:

```bash
http://13.xx.xx.xx
```

---

# AWS Security Group Configuration

Allow the following inbound rules:

| Type | Port |
| ---- | ---- |
| HTTP | 80   |
| SSH  | 22   |

Source:

```bash
0.0.0.0/0
```

---

# Useful Docker Commands

## View Logs

```bash
docker logs grade-tracker-backend
docker logs grade-tracker-frontend
docker logs grade-tracker-mysql
```

## Stop Containers

```bash
docker compose down
```

## Remove Containers + Volumes

```bash
docker compose down -v
```

## Restart Services

```bash
docker compose restart
```

---

# Docker Compose Services

## MySQL

* MySQL 8.0 Database
* Persistent Storage Volume
* Health Check Enabled

## Backend

* Flask Application
* Gunicorn Server
* Health Check Enabled
* Connected to MySQL

## Frontend

* Nginx Server
* Static Frontend
* Reverse Proxy Support

---

# Health Check Commands

## Backend Health

```bash
curl http://localhost:5000/health
```

## Frontend Health

```bash
curl http://localhost/health
```

---

# Troubleshooting

## Port Already in Use

Check running process:

```bash
sudo lsof -i :80
```

Stop containers:

```bash
docker compose down
```

---

## Permission Denied Error

Example:

```bash
permission denied
```

Fix:

```bash
sudo chown -R ubuntu:ubuntu .
```

---

## Container Not Starting

Check logs:

```bash
docker logs <container-name>
```

---

# Resource Check Commands

## Check Memory

```bash
free -h
```

## Check Disk

```bash
df -h
```

## Check Running Containers Resource Usage

```bash
docker stats
```

---

# Cleanup Docker Resources

## Remove Unused Images

```bash
docker image prune -a
```

## Remove Unused Volumes

```bash
docker volume prune
```

## Remove Everything Unused

```bash
docker system prune -a
```

---

# Important Notes

* The old README command using `./app` is incorrect for this project.
* Correct directories are:

  * `./backend`
  * `./frontend`
* Docker Compose automatically builds and starts all services.
* `version:` field in docker-compose.yml is deprecated warning only and does not break the application.

---

# Final Working Command

```bash
docker compose up -d --build
```

Then open:

```bash
http://<EC2-PUBLIC-IP>
```
