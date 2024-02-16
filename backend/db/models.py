import uuid
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import Column, DateTime, String, create_engine
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

from server.settings import get_postgres_url

ENGINE = create_engine(get_postgres_url())
Session = sessionmaker(bind=ENGINE)

Base = declarative_base()


# TODO(Eugene): Convert to async code
def get_session() -> Generator[Session, None, None]:
    """Create a new session."""
    session = Session()

    try:
        yield session
    except:
        session.rollback()
        raise
    finally:
        session.close()


class Extractor(Base):
    __tablename__ = "extractors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), onupdate=func.now())
    schema = Column(JSONB)
    description = Column(String(100))

    def __repr__(self):
        return f"<Extractor(id={self.id}, description={self.description})>"
