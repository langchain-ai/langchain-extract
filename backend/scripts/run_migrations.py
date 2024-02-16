#!/usr/bin/env python
"""Run migrations."""
from db.models import Base, ENGINE


def main() -> None:
    """Create all tables."""
    Base.metadata.create_all(ENGINE)


if __name__ == "__main__":
    print("Running migrations...")
    print("For now this is a simple script that creates all tables.")
    main()
