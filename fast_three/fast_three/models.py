from datetime import datetime

from sqlalchemy import func, create_engine
from sqlalchemy.orm import Mapped, mapped_column, registry, Session

table_registry = registry()

engine = create_engine("sqlite:///:memory:")

@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

with Session as session:
    ...