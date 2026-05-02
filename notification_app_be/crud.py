from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from models import Notification
from schemas import NotificationCreate
import uuid

async def get_notifications(db: AsyncSession, student_id: int, limit: int = 20, offset: int = 0):
    result = await db.execute(
        select(Notification)
        .where(Notification.student_id == student_id)
        .order_by(Notification.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    return result.scalars().all()

async def get_notification(db: AsyncSession, notification_id: uuid.UUID, student_id: int):
    result = await db.execute(
        select(Notification).where(Notification.id == notification_id, Notification.student_id == student_id)
    )
    return result.scalar_one_or_none()

async def mark_as_read(db: AsyncSession, notification_id: uuid.UUID, student_id: int):
    await db.execute(
        update(Notification)
        .where(Notification.id == notification_id, Notification.student_id == student_id)
        .values(is_read=True)
    )
    await db.commit()
    return await get_notification(db, notification_id, student_id)

async def mark_all_as_read(db: AsyncSession, student_id: int):
    result = await db.execute(
        update(Notification)
        .where(Notification.student_id == student_id, Notification.is_read == False)
        .values(is_read=True)
    )
    await db.commit()
    return result.rowcount

async def get_unread_count(db: AsyncSession, student_id: int):
    result = await db.execute(
        select(func.count(Notification.id))
        .where(Notification.student_id == student_id, Notification.is_read == False)
    )
    return result.scalar()

async def delete_notification(db: AsyncSession, notification_id: uuid.UUID, student_id: int):
    await db.execute(
        delete(Notification).where(Notification.id == notification_id, Notification.student_id == student_id)
    )
    await db.commit()
    return True

async def create_notification(db: AsyncSession, notification: NotificationCreate):
    db_notification = Notification(**notification.model_dump())
    db.add(db_notification)
    await db.commit()
    await db.refresh(db_notification)
    return db_notification
