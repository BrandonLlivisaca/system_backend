from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class BaseModel(Base):
    """Base Model with audit fields for all models"""

    __abstract__ = True #Don't create the table, it's only used for inheritance

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(),
                                                 onupdate=func.now())
    is_active: Mapped[bool] = mapped_column(default=True)
