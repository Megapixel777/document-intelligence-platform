from app.core.database import engine
from app.models.document import Base


def init_db() -> None:
    Base.metadata.create_all(bind=engine)