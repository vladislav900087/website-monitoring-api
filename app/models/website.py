from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import String, ForeignKey, UniqueConstraint
from app.database.base import Base


class Website(Base):

    __tablename__ = "websites"
    __table_args__ = (UniqueConstraint("user_id", "url", name="uq_websites_user_id_url"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    url: Mapped[str] = mapped_column(String(2048), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    user: Mapped["User"] = relationship(back_populates="websites")
    checks: Mapped[list["CheckResult"]] = relationship(back_populates="website", cascade='all, delete-orphan', passive_deletes=True)