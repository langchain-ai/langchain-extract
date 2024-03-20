import uuid
from datetime import datetime
from typing import Generator

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
    create_engine,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship, sessionmaker

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


class SharedExtractors(TimestampedModel):
    """A table for managing sharing of extractors."""

    __tablename__ = "shared_extractors"

    extractor_id = Column(
        UUID(as_uuid=True),
        ForeignKey("extractors.uuid", ondelete="CASCADE"),
        index=True,
        nullable=False,
        comment="The extractor that is being shared.",
    )

    share_token = Column(
        UUID(as_uuid=True),
        index=True,
        nullable=False,
        unique=True,
        comment="The token that is used to access the shared extractor.",
    )

    # Add unique constraint for (extractor_id, share_token)
    __table_args__ = (
        UniqueConstraint("extractor_id", "share_token", name="unique_share_token"),
    )

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"<SharedExtractor(id={self.id}, run_id={self.run_id})>"


class Extractor(TimestampedModel):
    __tablename__ = "extractors"

    name = Column(
        String(100),
        nullable=False,
        server_default="",
        comment="The name of the extractor.",
    )
    owner_id = Column(
        UUID(as_uuid=True),
        nullable=False,
        comment="Owner uuid.",
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

    # Used for sharing the extractor with others.
    share_uuid = Column(
        UUID(as_uuid=True),
        nullable=True,
        comment="The uuid of the shareable link.",
    )

    def __repr__(self) -> str:
        return f"<Extractor(id={self.uuid}, description={self.description})>"


def validate_extractor_owner(
    session: Session, extractor_id: UUID, user_id: UUID
) -> Extractor:
    """Validate the extractor id."""
    extractor = (
        session.query(Extractor).filter_by(uuid=extractor_id, owner_id=user_id).first()
    )
    if extractor is None:
        return False
    else:
        return True
