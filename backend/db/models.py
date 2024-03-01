import uuid
from datetime import datetime
from typing import Generator

from sqlalchemy import Column, DateTime, ForeignKey, String, Text, create_engine
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship, sessionmaker
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


class TimestampedModel(Base):
    """An abstract base model that includes the timestamp fields."""

    __abstract__ = True

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        comment="The time the record was created (UTC).",
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        doc="The time the record was last updated (UTC).",
    )

    # This is our own uuid assigned to the artifact.
    # By construction guaranteed to be unique no matter what.
    uuid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        doc="Unique identifier for this model.",
    )


class Extractor(TimestampedModel):
    __tablename__ = "extractors"

    name = Column(
        String(100),
        nullable=False,
        server_default="",
        comment="The name of the extractor.",
    )
    schema = Column(
        JSONB,
        nullable=False,
        comment="JSON Schema that describes what content will be "
        "extracted from the document",
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

    examples = relationship("Example", backref="extractor")

    def __repr__(self) -> str:
        return f"<Extractor(id={self.uuid}, description={self.description})>"


class Example(TimestampedModel):
    """A representation of an example.

    Examples consist of content together with the expected output.

    The output is a JSON object that is expected to be extracted from the content.

    The JSON object should be valid according to the schema of the associated extractor.

    The JSON object is defined by the schema of the associated extractor, so
    it's perfectly fine for a given example to represent the extraction
    of multiple instances of some object from the content since
    the JSON schema can represent a list of objects.
    """

    __tablename__ = "examples"

    content = Column(
        Text,
        nullable=False,
        comment="The input portion of the example.",
    )
    output = Column(
        JSONB,
        comment="The output associated with the example.",
    )
    extractor_id = Column(
        UUID(as_uuid=True),
        ForeignKey("extractors.uuid", ondelete="CASCADE"),
        nullable=False,
        comment="Foreign key referencing the associated extractor.",
    )

    def __repr__(self) -> str:
        return f"<Example(uuid={self.uuid}, content={self.content[:20]}>"
