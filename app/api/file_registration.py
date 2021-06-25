from typing import List
from fastapi import APIRouter

from app.api.models import (
    RegisterFileInfo,
    FileProcessLog,
    FileProcessStepLog,
    BaseInfo,
)
from app.api import db_manager

import hashlib
import uuid
import datetime
import boto3
import json
from app.api.settings import getConfig

cnf = getConfig()
filesregister = APIRouter()


@filesregister.get("/files", response_model=List[FileProcessLog])
async def getFilesInfo():
    return await db_manager.get_file_process_data()


@filesregister.get("/steps", response_model=List[FileProcessStepLog])
async def getStepsInfo():
    return await db_manager.get_file_process_step_data()


def getSNSClient():
    client = boto3.client("sns",endpoint_url='http://localhost:4566',region_name='us-east-1')
    return client


@filesregister.post("/", status_code=201)
async def postData(payload: RegisterFileInfo):
    try:
        returnStatus = "Success"
        returnReason = "Inserted into DB"
        step_status = "DONE"
        step_status_detail = "Completed Successfully"
        file_process_id = str(uuid.uuid4())
        create_by = "FileRegisterMS"
        create_ts = datetime.datetime.now()
        data = payload.dict()
        # Check if the file is already processed
        file_hash = hashlib.md5(
            "".join(
                [
                    str(data.get("source_ip")),
                    "|",
                    data.get("filename"),
                    "|",
                    str(data.get("event_ts")),
                ]
            ).encode()
        ).hexdigest()
        getStatus = await db_manager.check_if_file_exists(file_hash)
        if getStatus:
            # File already exists
            returnStatus = "Failure"
            returnReason = "File already exists"
            step_status = "FAILED"
            step_status_detail = "File already exists"
            client = getSNSClient()
            message = {
                "message": "File ({0}) was already processed once before. If the same file needs to be reprocessed, please send event with force_process='true' option set".format(
                    data.get("filename")
                )
            }
            try:
                response = client.publish(
                    TargetArn=cnf.SNS_TARGET_ARN,
                    Message=json.dumps({"default": json.dumps(message)}),
                    Subject="File Registration: Error",
                    MessageStructure="json",
                )
            except Exception as e:
                print(e)
        data.update({"event_ts": payload.dict().get("event_ts").replace(tzinfo=None)})
        filepayload = {
            **data,
            **{
                "file_process_id": file_process_id,
                "create_by": create_by,
                "create_ts": create_ts,
                "file_hash": file_hash,
            },
        }
        file_status = await db_manager.add_file_process_log(filepayload)
        steppayload = {
            "file_process_id": file_process_id,
            "step_name": "File Registration",
            "step_status": step_status,
            "step_start_ts": create_ts,
            "step_end_ts": datetime.datetime.now(),
            "step_status_detail": step_status_detail,
            "create_by": create_by,
            "create_ts": create_ts,
        }
        step_id = await db_manager.add_file_process_step_log(steppayload)
        return {
            "Status": returnStatus,
            "Message": returnReason,
            "id": {"file_process_id": file_process_id, "step_id": step_id},
        }
    except Exception as e:
        print(e)
        message = {"message": "Processing failed with error : {0}".format(e)}
        try:
            client = getSNSClient()
            response = client.publish(
                TargetArn=cnf.SNS_TARGET_ARN,
                Message=json.dumps({"default": json.dumps(message)}),
                Subject="File Registration: Error",
                MessageStructure="json",
            )
        except Exception as e:
            print(e)
