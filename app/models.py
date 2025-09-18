import uuid
from sqlalchemy import Column, String, Date, DateTime, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import enum
from .database import Base

class PlatformEnum(str, enum.Enum):
    youtube = "youtube"
    x = "x"
    reddit = "reddit"
    insta = "insta"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    dob = Column(Date, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # bcrypt hash
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Creator(Base):
    __tablename__ = "creators"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    platform = Column(Enum(PlatformEnum), nullable=False)
    platform_id = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("id", "platform_id", name="uq_creator_platform"),
    )

class Flag(Base):
    __tablename__ = "flags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    creator_id = Column(UUID(as_uuid=True), ForeignKey("creators.id"), nullable=False)
    flagged_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("creator_id", "flagged_by", name="uq_flag_creator_user"),
    )