from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from data.database import Base

class User(Base):
    __tablename__ = "users"

    # id = Column(Integer, primary_key=True, index=True)
    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)