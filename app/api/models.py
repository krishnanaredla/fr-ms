from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Optional


class BaseInfo(BaseModel):
    """Base model for file information."""
    filename: str
    source_ip: str
    file_size: int
    bucket_name: str
    event_name: str
    event_ts: datetime
    fp_id: int


class RegisterFileInfo(BaseInfo):
    """Model for file registration request."""
    pass


class FileProcessLog(BaseInfo):
    """Model for file process log record."""
    create_by: str
    create_ts: datetime


class FileProcessStepLog(BaseModel):
    """Model for file process step log record."""
    file_process_id: str
    step_name: str
    step_status: str
    step_status_detail: str
    step_start_ts: datetime
    step_end_ts: Optional[datetime]
    create_by: str
    create_ts: datetime
