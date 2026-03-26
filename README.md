<div align="center">

<a href="https://github.com/Sumit0ubey/Pinggo">
  <img src="https://readme-typing-svg.demolab.com?font=Inter&weight=700&size=28&duration=3500&pause=700&color=22C55E&center=true&vCenter=true&width=750&lines=Pinggo+%E2%9A%A1+Real-Time+Chat+Platform;Django+%2B+Channels+%2B+Redis+%2B+PostgreSQL;Global+%7C+Group+%7C+Private+Messaging;Production-ready+ASGI+Architecture" alt="Typing SVG" />
</a>

<br/>

<p>
  <a href="https://github.com/Sumit0ubey/Pinggo/repo-size">
    <img src="https://img.shields.io/github/repo-size/Sumit0ubey/Pinggo?style=for-the-badge" />
  </a>
  <a href="https://github.com/Sumit0ubey/Pinggo/stargazers">
    <img src="https://img.shields.io/github/stars/Sumit0ubey/Pinggo?style=for-the-badge&logo=github&label=Stars" alt="GitHub Stars"/>
  </a>
  <a href="https://github.com/Sumit0ubey/Pinggo/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-informational?style=for-the-badge&logo=open-source-initiative&logoColor=white" alt="License"/>
  </a>
</p>

<p>
  <a href="http://143.244.132.69/">
    <img src="https://img.shields.io/badge/Live%20Demo-Online-22c55e?style=for-the-badge&logo=vercel&logoColor=white" alt="Live Demo"/>
  </a>
  <a href="https://github.com/Sumit0ubey/Pinggo">
    <img src="https://img.shields.io/badge/Repo-GitHub-111827?style=for-the-badge&logo=github&logoColor=white" alt="Repo"/>
  </a>
  <img src="https://img.shields.io/badge/Real--time-WebSockets-3b82f6?style=for-the-badge&logo=socketdotio&logoColor=white" alt="WebSockets"/>
</p>


<p>
  <img src="https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white" alt="Django"/>
  <img src="https://img.shields.io/badge/Django%20Channels-1f2937?style=flat-square&logo=python&logoColor=white" alt="Django Channels"/>
  <img src="https://img.shields.io/badge/ASGI-0ea5e9?style=flat-square&logo=fastapi&logoColor=white" alt="ASGI"/>
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL"/>
  <img src="https://img.shields.io/badge/Redis-DC382D?style=flat-square&logo=redis&logoColor=white" alt="Redis"/>
  <img src="https://img.shields.io/badge/Cloudinary-3448C5?style=flat-square&logo=cloudinary&logoColor=white" alt="Cloudinary"/>
  <img src="https://img.shields.io/badge/TailwindCSS-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white" alt="TailwindCSS"/>
  <img src="https://img.shields.io/badge/HTMX-0f172a?style=flat-square&logo=html5&logoColor=white" alt="HTMX"/>
  <img src="https://img.shields.io/badge/Alpine.js-8BC0D0?style=flat-square&logo=alpinedotjs&logoColor=white" alt="Alpine.js"/>
</p>


<h3>⚡ Real-Time Conversations. Engineered for Scale.</h3>
<p>Global • Group • Private messaging — built on Django + WebSockets with a production-ready ASGI architecture.</p>

</div>

---

## 📌 Table of Contents

- [✨ Overview](#-overview)
- [🚀 Why Pinggo?](#-why-pinggo)
- [🧩 Features](#-features)
- [🏗 System Design](#-system-design)
  - [1) High-Level](#1-high-level)
  - [2) Low-Level](#2-low-level)
  - [3) Data Flow](#3-data-flow)
  - [4) Deployment & Scaling](#4-deployment--scaling)
  - [5) Database ER](#5-database-er)
- [🛠 Tech Stack](#-tech-stack)
- [📦 Project Structure](#-project-structure)
- [⚙️ Getting Started](#️-getting-started)
- [🌩 Environment Variables](#-environment-variables)
- [🚢 Production Deployment](#-production-deployment)
- [🧪 Security & Best Practices](#-security--best-practices)
- [🗺 Roadmap](#-roadmap)
- [🤝 Contributing](#-contributing)
- [👨‍💻 Author](#-author)
- [📄 License](#-license)

---

## ✨ Overview

**Pinggo** is a real-time chat platform designed to deliver smooth, instant messaging across:

- 🌍 **Global chat**
- 👥 **Group rooms**
- 🔐 **Private 1:1 DMs**
- 🖼 **Media sharing** (Cloudinary)

It’s built like a deployable product: **ASGI-first**, **Redis channel layer**, **PostgreSQL storage**, and a modern UI stack for responsive interactions.

**Live:** http://143.244.132.69/  

---

## 🚀 Why Pinggo?

- **Realtime-first**: WebSocket messaging using Django Channels
- **Scales horizontally**: Redis/Upstash for the channel layer fan-out
- **Production-ready**: ASGI + Daphne/Uvicorn compatible deployment
- **Cloud media**: Cloudinary for avatars and attachments
- **Modern UI**: Tailwind + HTMX + Alpine.js for app-like experience

---

## 🧩 Features

### Messaging
- ✅ Real-time messaging via WebSockets  
- ✅ Global / Group / Private rooms  
- ✅ Room-based broadcast delivery  
- ✅ Persistent history in PostgreSQL  

### Media
- ✅ User avatars  
- ✅ Group avatars  
- ✅ File uploads / attachments  
- ✅ Cloudinary integration  

### Infrastructure-ready
- ✅ ASGI deployment support  
- ✅ Redis channel layer for scale  
- ✅ Clear separation of routes/consumers/services  

---

# 🏗 System Design

## 1) High-Level

```mermaid
flowchart TB
  U[Users / Browsers] -->|HTTPS| LB[Load Balancer / Reverse Proxy<br/>Nginx / Cloud LB]
  U -->|WSS WebSocket Secure| LB

  LB --> APP[ASGI App<br/>Django + Channels<br/>Daphne/Uvicorn Workers]

  APP --> DB[(PostgreSQL<br/>Users, Rooms, Messages, Memberships)]
  APP --> REDIS[(Redis / Upstash<br/>Channel Layer + PubSub)]
  APP --> CLOUD[(Cloudinary<br/>Avatars + Files)]
  APP --> EMAIL[Email Provider / API<br/>Verification / system emails]
```

---

## 2) Low-Level

```mermaid
flowchart LR
  subgraph Client["Client (Browser)"]
    UI[Chat UI<br/>Tailwind/HTMX/Alpine]
    WS[WebSocket Client]
    HTTP[HTTP Client]
    UI --> WS
    UI --> HTTP
  end

  subgraph Server["Server (Django ASGI)"]
    ROUTES[HTTP Routes<br/>Auth, Rooms, Profiles]
    CONSUMERS[Channels Consumers<br/>WebSocket handlers]
    AUTH[Auth Layer<br/>Sessions/JWT/Allauth]
    SVC[Service Layer<br/>RoomService, MessageService]
    POL[Permissions / Policy]
    SERIAL[Serialization / Validation]
  end

  subgraph Storage[Storage & Infra]
    PG[(PostgreSQL)]
    REDIS[(Redis Channel Layer)]
    CLOUD[(Cloudinary)]
  end

  HTTP --> ROUTES
  WS --> CONSUMERS

  ROUTES --> AUTH
  CONSUMERS --> AUTH

  AUTH --> POL
  ROUTES --> SERIAL
  CONSUMERS --> SERIAL

  SERIAL --> SVC
  POL --> SVC

  SVC --> PG
  CONSUMERS --> REDIS
  SVC --> CLOUD
```

---

## 3) Data Flow

### 3A) WebSocket Message Send (Room/Group/Global)

```mermaid
sequenceDiagram
  autonumber
  participant C as Client (Browser)
  participant LB as LB / Nginx
  participant A as ASGI App (Django+Channels)
  participant R as Redis (Channel Layer)
  participant P as PostgreSQL

  C->>LB: WSS connect /ws/chat/{room}/
  LB->>A: Upgrade to WebSocket
  A->>R: Join group (room channel group)

  C->>A: Send message payload (WS frame)
  A->>A: Validate + authorize (membership/permissions)
  A->>P: Persist message (insert)
  A->>R: Publish to room group
  R-->>A: Fan-out event to all subscribers
  A-->>C: Broadcast message event (WS)
```

### 3B) File Upload / Media Share (Cloudinary)

```mermaid
sequenceDiagram
  autonumber
  participant C as Client
  participant A as ASGI App
  participant CL as Cloudinary
  participant P as PostgreSQL

  C->>A: Request upload (HTTP) / get upload signature
  A->>A: Check auth + size/type rules
  A-->>C: Return signed upload params (or upload endpoint)
  C->>CL: Upload file (direct to Cloudinary)
  CL-->>C: Return asset URL + public_id
  C->>A: Send message referencing asset URL (WS/HTTP)
  A->>P: Save message with attachment metadata
  A-->>C: Broadcast message with attachment URL
```

### 3C) Private Chat Initiation (1:1)

```mermaid
sequenceDiagram
  autonumber
  participant C as Client
  participant A as ASGI App
  participant P as PostgreSQL
  participant R as Redis

  C->>A: Create/find DM room (HTTP)
  A->>P: Upsert DM room + membership (two users)
  A-->>C: Return room_id
  C->>A: WSS connect /ws/chat/{room_id}/
  A->>R: Join DM group
  C->>A: Send message (WS)
  A->>P: Persist message
  A->>R: Publish to DM group
  A-->>C: Broadcast to both users
```

---

## 4) Deployment & Scaling

```mermaid
flowchart TB
  U[Users] --> LB[Cloud LB / Nginx]

  LB --> A1[ASGI Instance #1<br/>Daphne/Uvicorn + Django]
  LB --> A2[ASGI Instance #2<br/>Daphne/Uvicorn + Django]
  LB --> A3[ASGI Instance #3<br/>Daphne/Uvicorn + Django]

  A1 --> REDIS[(Redis / Upstash<br/>Channel Layer)]
  A2 --> REDIS
  A3 --> REDIS

  A1 --> PG[(PostgreSQL)]
  A2 --> PG
  A3 --> PG

  A1 --> CLOUD[(Cloudinary)]
  A2 --> CLOUD
  A3 --> CLOUD
```

---

## 5) Database ER

```mermaid
erDiagram
  %% USERS
  USER ||--|| PROFILE : has_profile

  %% CHAT GROUPS
  USER ||--o{ CHATGROUP : creates
  USER }o--o{ CHATGROUP : member_of

  %% MESSAGES
  CHATGROUP ||--o{ GROUPMESSAGE : has
  USER ||--o{ GROUPMESSAGE : writes

  PROFILE {
    int id
    int user_id
    string image_url
    string displayname
    string info
  }

  CHATGROUP {
    int id
    string group_name
    string chat_type "global|group|private"
    string description
    string image_url
    int creator_id
    datetime created_at
  }

  GROUPMESSAGE {
    int id
    int group_id
    int author_id
    string message
    string file_url
    string file_type "image|video|audio|pdf|other"
    string file_name
    datetime created_at
  }
```

---

## 🛠 Tech Stack

### Backend
- Django
- Django Channels (WebSockets)
- ASGI + Daphne/Uvicorn
- PostgreSQL
- Redis / Upstash Redis

### Frontend
- HTML5
- Tailwind CSS
- HTMX
- Alpine.js
- JavaScript

### Media
- Cloudinary

---

## 📦 Project Structure

```
Pinggo/
│
├── chats/                # Chat related files and configuration
├── home/                 # Simple app for redirection
├── MailApix/             # app for configuring MailAPIX API as an email backed
├── Pinggo/               # Django project core
├── static/               # Static files folder
├── templates/            # Html files folder
├── users/                # app for user authentication and authorization
├── __init__.py
├── manage.py
├── .env
└──  requirements.txt                 
```

---

## ⚙️ Getting Started

### 1) Clone & install

```bash
git clone https://github.com/Sumit0ubey/Pinggo.git
cd Pinggo

python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 2) Migrate DB

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3) Run locally

```bash
python manage.py runserver
```

---

## 🌩 Environment Variables

Create `.env` based on `.env.example`.

```env
DEBUG=True
SECRET_KEY=your_secret_key
APP_NAME=Pinggo

# Database
DATABASE_HOST=
DATABASE_PORT=
DATABASE_NAME=
DATABASE_USER=

# Redis / Upstash
UPSTASH_REDIS_URL=

# Cloudinary
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=

# Optional folders
CLOUDINARY_USER_AVATAR=
CLOUDINARY_GROUP_AVATAR=
CLOUDINARY_CHAT_FILES=
```

---

## 🚢 Production Deployment

### Run ASGI with Daphne

```bash
daphne -b 0.0.0.0 -p 8000 Pinggo.asgi:application
```

### Recommended production setup
- Nginx reverse proxy (TLS termination)
- PostgreSQL managed DB
- Upstash Redis (channel layer)
- Cloudinary for media
- `DEBUG=False` and restricted `ALLOWED_HOSTS`

---

## 🧪 Security & Best Practices

- ✅ Keep secrets in environment variables
- ✅ Use `DEBUG=False` in production
- ✅ Validate message payloads server-side
- ✅ Add rate limiting (WS + HTTP) for abuse prevention
- ✅ Restrict allowed file types/sizes before upload
- ✅ Use HTTPS/WSS everywhere

---

## 🗺 Roadmap

- Read receipts ✅/👀  
- Typing indicators ✍️  
- Reactions ❤️🔥  
- Push notifications 🔔  
- Search 🔎  
- Moderation tools 🛡  
- Optional E2E encryption 🔐  

---

## 🤝 Contributing

1. Fork the repo  
2. Create a branch: `git checkout -b feature/amazing-feature`  
3. Commit changes: `git commit -m "Add amazing feature"`  
4. Push: `git push origin feature/amazing-feature`  
5. Open a PR 🎉  

---

## 👨‍💻 Author

**Sumit Dubey**  
GitHub: https://github.com/Sumit0ubey

---

## 📄 License

This project is licensed under the MIT License.

See the [LICENSE](./LICENSE) file for details.

---

<div align="center">

### 💬 Pinggo — Built for Conversations that Matter

</div>
