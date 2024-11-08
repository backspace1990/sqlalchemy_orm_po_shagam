from sqlalchemy import Table, Column, String, Integer, MetaData, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column
from database import Base, str_256
from typing import Optional, Annotated
import enum
from datetime import datetime, timezone


intpk = Annotated[int, mapped_column(primary_key=True)]
an_created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
an_uptated_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"),onupdate=datetime.now(timezone.utc))]


class WorkersOrm(Base):
    __tablename__ = "workers"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]

class Workload(enum.Enum):
    parttime = "parttime"
    fulltime = "fulltime"


class ResumesOrm(Base):
    __tablename__ = "resumes"

    id: Mapped[intpk]
    title: Mapped[str_256]
    compensation: Mapped[Optional[int]]
    workload: Mapped[Workload]
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"))
    created_at: Mapped[an_created_at]
    updated_at: Mapped[an_uptated_at]























metadata_obj = MetaData()


workers_table = Table(
    "workers",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String),
)


