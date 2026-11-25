from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import String
from app.database.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    websites: Mapped[list["Website"]] = relationship(back_populates="user", cascade="all, delete-orphan")
