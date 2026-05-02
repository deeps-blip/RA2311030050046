from fastapi import FastAPI, Depends, HTTPException, Header, BackgroundTasks, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
import uuid
import json
import redis.asyncio as redis
import os
from datetime import datetime, timezone

from database import get_db, engine, Base
from models import Notification
from schemas import (
    NotificationResponse, NotificationListResponse, UnreadCountResponse,
    MarkReadResponse, MessageResponse, NotificationCreate
)
import crud
from socket_manager import socket_app, emit_new_notification

app = FastAPI(title="Notification System")

# Mount Socket.IO
app.mount("/socket", socket_app)

# Redis client for Stage 4
redis_client = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"), decode_responses=True)

# Helper for Auth (Mock)
async def get_current_student_id(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")
    # Mock validation: token is just the student_id
    token = authorization.split(" ")[1]
    try:
        return int(token)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid student ID in token")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# STAGE 1 & 4: GET /api/notifications
@app.get("/api/notifications", response_model=NotificationListResponse)
async def list_notifications(
    db: AsyncSession = Depends(get_db),
    student_id: int = Depends(get_current_student_id),
    limit: int = Query(20, ge=1),
    offset: int = Query(0, ge=0)
):
    # Stage 4: Redis Cache lookup
    cache_key = f"notifications:{student_id}:{limit}:{offset}"
    cached_data = await redis_client.get(cache_key)
    if cached_data:
        return {"notifications": json.loads(cached_data)}

    notifications = await crud.get_notifications(db, student_id, limit, offset)
    
    # Store in Redis for 60s (Stage 4)
    resp_data = [NotificationResponse.model_validate(n).model_dump() for n in notifications]
    # Serializing UUID and datetime for JSON
    serializable_data = json.loads(json.dumps(resp_data, default=str))
    await redis_client.setex(cache_key, 60, json.dumps(serializable_data))

    return {"notifications": notifications}

# STAGE 1: GET /api/notifications/unread-count
@app.get("/api/notifications/unread-count", response_model=UnreadCountResponse)
async def unread_count(
    db: AsyncSession = Depends(get_db),
    student_id: int = Depends(get_current_student_id)
):
    count = await crud.get_unread_count(db, student_id)
    return {"unread_count": count}

# STAGE 6: Priority Scoring
@app.get("/api/notifications/priority", response_model=NotificationListResponse)
async def list_priority_notifications(
    db: AsyncSession = Depends(get_db),
    student_id: int = Depends(get_current_student_id),
    top_n: int = Query(10, ge=1)
):
    # This would ideally be a complex SQL query with score calculation
    # For now, let's fetch unread and score them in Python
    result = await db.execute(
        select(Notification)
        .where(Notification.student_id == student_id, Notification.is_read == False)
    )
    unread = result.scalars().all()
    
    def calculate_score(n):
        weights = {"Placement": 3, "Result": 2, "Event": 1}
        type_weight = weights.get(n.type, 0)
        
        now = datetime.now(timezone.utc)
        created_at = n.created_at
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)
            
        age_hours = (now - created_at).total_seconds() / 3600
        # priorityScore = typeWeight + 0.5^(ageInHours / 24)
        return type_weight + (0.5 ** (age_hours / 24))

    sorted_notifications = sorted(unread, key=calculate_score, reverse=True)
    return {"notifications": sorted_notifications[:top_n]}

# STAGE 1: GET /api/notifications/:id
@app.get("/api/notifications/{notification_id}", response_model=NotificationResponse)
async def get_notification(
    notification_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    student_id: int = Depends(get_current_student_id)
):
    notification = await crud.get_notification(db, notification_id, student_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

# STAGE 1: PATCH /api/notifications/:id/read
@app.patch("/api/notifications/{notification_id}/read", response_model=MarkReadResponse)
async def mark_read(
    notification_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    student_id: int = Depends(get_current_student_id)
):
    notification = await crud.mark_as_read(db, notification_id, student_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    # Clear cache
    await redis_client.delete(f"notifications:{student_id}:*") 
    return notification

# STAGE 1: PATCH /api/notifications/read-all
@app.patch("/api/notifications/read-all", response_model=MessageResponse)
async def mark_all_read(
    db: AsyncSession = Depends(get_db),
    student_id: int = Depends(get_current_student_id)
):
    count = await crud.mark_all_as_read(db, student_id)
    # Clear cache
    await redis_client.delete(f"notifications:{student_id}:*")
    return {"message": "All marked as read", "updated_count": count}

# STAGE 1: DELETE /api/notifications/:id
@app.delete("/api/notifications/{notification_id}", response_model=MessageResponse)
async def delete_notification(
    notification_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    student_id: int = Depends(get_current_student_id)
):
    await crud.delete_notification(db, notification_id, student_id)
    return {"message": "Deleted"}

# STAGE 5: Asynchronous Processing (Email/Push)
def send_external_notification(student_id: int, message: str):
    # Mocking external API call
    print(f"Sending email to student {student_id}: {message}")

# Internal trigger for new notification (e.g. from an admin panel)
@app.post("/api/internal/notify", response_model=NotificationResponse)
async def notify_student(
    notification: NotificationCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    # 1. Save to DB first (Stage 5)
    db_notification = await crud.create_notification(db, notification)
    
    # 2. Emit WebSocket event (Stage 1)
    await emit_new_notification(NotificationResponse.model_validate(db_notification).model_dump())
    
    # 3. Enqueue background tasks (Stage 5)
    background_tasks.add_task(send_external_notification, notification.student_id, notification.message)
    
    return db_notification
