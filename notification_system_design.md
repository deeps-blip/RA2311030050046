# Notification System Backend

A high-performance, real-time notification system built with FastAPI, PostgreSQL, Redis, and Socket.IO.

## Features

- **Real-time Notifications:** Instant delivery of notifications using Socket.IO.
- **Priority Scoring:** Intelligent sorting of notifications based on type (Placement, Result, Event) and age.
- **Caching:** Redis-based caching for frequent notification queries to reduce database load.
- **Asynchronous Processing:** Background tasks for external notification delivery (e.g., Email/Push mocks).
- **CRUD Operations:** Complete set of APIs to list, read, mark as read, and delete notifications.
- **Mock Authentication:** Simple Bearer token authentication (token = student ID).
- **Dockerized:** Easy deployment using Docker and Docker Compose.

## Tech Stack

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **Database:** [PostgreSQL](https://www.postgresql.org/) with [SQLAlchemy](https://www.sqlalchemy.org/) (Async)
- **Cache:** [Redis](https://redis.io/)
- **Real-time:** [python-socketio](https://python-socketio.readthedocs.io/)
- **Task Queue:** FastAPI BackgroundTasks
- **Containerization:** [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)

## Getting Started

### Prerequisites

- Python 3.9+
- Docker & Docker Compose (optional, for containerized setup)
- Redis and PostgreSQL (if running locally without Docker)

### Installation (Local)

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd notification_app_be
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory and configure the following:
   ```env
   DATABASE_URL=postgresql+asyncpg://user:password@localhost/notification_db
   REDIS_URL=redis://localhost:6379
   ```

5. **Run the application:**
   ```bash
   python run.py
   ```

### Running with Docker

1. **Build and start the services:**
   ```bash
   docker-compose up --build
   ```
   This will start the FastAPI app, PostgreSQL, and Redis.

## API Documentation

Once the server is running, you can access the interactive API documentation at:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/notifications` | List notifications for the current student (paginated, cached). |
| `GET` | `/api/notifications/unread-count` | Get total count of unread notifications. |
| `GET` | `/api/notifications/priority` | Get top-N notifications sorted by priority score. |
| `PATCH`| `/api/notifications/{id}/read` | Mark a specific notification as read. |
| `PATCH`| `/api/notifications/read-all` | Mark all notifications as read for the student. |
| `POST` | `/api/internal/notify` | Trigger a new notification (Internal use). |

## WebSocket Connection

Connect to the WebSocket server at `ws://localhost:8000/socket`.
The server emits `new_notification` events when a new notification is created.

## Project Structure

```text
notification_app_be/
├── main.py            # FastAPI application and route handlers
├── models.py          # SQLAlchemy database models
├── schemas.py         # Pydantic models for request/response validation
├── crud.py            # Database CRUD operations
├── database.py        # Database connection and session management
├── socket_manager.py  # Socket.IO configuration and event emitters
├── run.py             # Script to run the application
├── Dockerfile         # Docker configuration
└── docker-compose.yml # Docker Compose configuration
```
