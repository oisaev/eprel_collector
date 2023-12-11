from sqlalchemy import Column, DateTime

from core.db import Base


class PDFCommit(Base):
    '''Модель PDF Commit.'''

    pdf_commit_datetime = Column(DateTime, nullable=False)
