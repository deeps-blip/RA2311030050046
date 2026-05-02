from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import List, Optional

class NotificationBase(BaseModel):
    type: str
    message: str

class NotificationCreate(NotificationBase):
    student_id: int

class NotificationResponse(NotificationBase):
    id: UUID
    is_read: bool
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class NotificationListResponse(BaseModel):
    notifications: List[NotificationResponse]

class UnreadCountResponse(BaseModel):
    unread_count: int

class MarkReadResponse(BaseModel):
    id: UUID
    is_read: bool

class MessageResponse(BaseModel):
    message: str
    updated_count: Optional[int] = None
