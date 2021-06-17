from typing import List
from fastapi import APIRouter

from app.api.models import (
    RegisterFileInfo,
    FileProcessLog,
    FileProcessStepLog,
    BaseInfo,
)
from app.api import db_manager

import uuid
import random
import datetime

filesregister = APIRouter()


@filesregister.get("/files", response_model=List[FileProcessLog])
async def getFilesInfo():
    return await db_manager.get_file_process_data()


@filesregister.get("/steps", response_model=List[FileProcessStepLog])
async def getStepsInfo():
    return await db_manager.get_file_process_step_data()


@filesregister.post("/", status_code=201)
async def getData(payload: RegisterFileInfo):
    try:
        create_by = "FileRegisterMS"
        create_ts = datetime.datetime.now()
        data = payload.dict()
        data.update({"event_ts": payload.dict().get("event_ts").replace(tzinfo=None)})
        filepayload = {
            **data,
            **{
                "create_by": create_by,
                "create_ts": create_ts,
            },
        }
        file_process_id = await db_manager.add_file_process_log(filepayload)
        steppayload = {
            "file_process_id": file_process_id,
            "step_name": "Preprocessor",
            "step_status": "Initiated",
            "step_start_ts": datetime.datetime.now(),
            "step_end_ts": None,
            "create_by": create_by,
            "create_ts": create_ts,
        }
        step_id = await db_manager.add_file_process_step_log(steppayload)
        return {
            "Status": "Success",
            "id": {"file_process_id": file_process_id, "step_id": step_id},
        }
    except Exception as e:
        print(e)
