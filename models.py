from sqlalchemy import Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )


class UserModel(Base):
    __tablename__ = "user"
    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[String] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[String] = mapped_column(String)
    name: Mapped[String] = mapped_column(String)
