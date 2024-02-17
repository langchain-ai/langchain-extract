import uuid
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import Column, DateTime, String, Text, create_engine
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql import func

from server.settings import get_postgres_url

ENGINE = create_engine(get_postgres_url())
SessionClass = sessionmaker(bind=ENGINE)

Base = declarative_base()


# TODO(Eugene): Convert to async code
def get_session() -> Generator[Session, None, None]:
    """Create a new session."""
    session = SessionClass()

    try:
        yield session
    except:
        session.rollback()
        raise
    finally:
        session.close()


class Extractor(Base):
    __tablename__ = "extractors"

    uuid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Unique identifier for this extractor.",
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Time when this extracted was originally created.",
    )
    modified_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        comment="Last time this was modified.",
    )
    schema = Column(
        JSONB,
        nullable=False,
        comment="JSON Schema that describes what content will be extracted from the document",
    )
    description = Column(
        String(100),
        nullable=False,
        server_default="",
        comment="Surfaced via UI to the users.",
    )
    instruction = Column(
        Text, nullable=False, comment="The prompt to the language model."
    )  # TODO: This will need to evolve

    def __repr__(self):
        return f"<Extractor(id={self.id}, description={self.description})>"
