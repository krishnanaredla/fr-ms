from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Optional


class BaseInfo(BaseModel):
    filename: str
    source_ip: str
    file_size: int
    bucket_name: str
    event_name: str
    event_ts: datetime
    fp_id: int


class RegisterFileInfo(BaseInfo):
    pass


class FileProcessLog(BaseInfo):
    create_by: str
    create_ts: datetime


class FileProcessStepLog(BaseModel):
    file_process_id: int
    step_name: str
    step_status: str
    step_start_ts: datetime
    step_end_ts: Optional[datetime]
    create_by: str
    create_ts: datetime
