from typing import List
from fastapi import APIRouter, HTTPException

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
import logging
from app.api.settings import getConfig

# Configure logging
logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(level=logging.INFO)

cnf = getConfig()
filesregister = APIRouter()


@filesregister.get("/files", response_model=List[FileProcessLog])
async def getFilesInfo():
    """
    Retrieve all file process logs.
    
    Returns:
        List[FileProcessLog]: List of all file process records
    """
    return await db_manager.get_file_process_data()


@filesregister.get("/steps", response_model=List[FileProcessStepLog])
async def getStepsInfo():
    """
    Retrieve all file process step logs.
    
    Returns:
        List[FileProcessStepLog]: List of all step process records
    """
    return await db_manager.get_file_process_step_data()


def getSNSClient():
    """
    Creates and returns an SNS client with configured endpoint and region.
    
    Returns:
        boto3.client: Configured SNS client
    """
    client = boto3.client(
        "sns",
        endpoint_url=cnf.SNS_ENDPOINT_URL,
        region_name=cnf.SNS_REGION_NAME
    )
    return client


@filesregister.post("/", status_code=201)
async def postData(payload: RegisterFileInfo):
    """
    Register a new file in the system.
    
    Args:
        payload: File registration information
        
    Returns:
        dict: Status, message, and IDs of created records
        
    Raises:
        HTTPException: If processing fails
    """
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
                logger.info(f"SNS notification sent for duplicate file: {data.get('filename')}")
            except Exception as e:
                logger.error(f"Failed to send SNS notification: {e}")
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
        logger.info(f"File registered successfully: {data.get('filename')}, file_process_id: {file_process_id}")
        return {
            "Status": returnStatus,
            "Message": returnReason,
            "id": {"file_process_id": file_process_id, "step_id": step_id},
        }
    except Exception as e:
        logger.error(f"File registration failed: {e}")
        message = {"message": "Processing failed with error : {0}".format(e)}
        try:
            client = getSNSClient()
            response = client.publish(
                TargetArn=cnf.SNS_TARGET_ARN,
                Message=json.dumps({"default": json.dumps(message)}),
                Subject="File Registration: Error",
                MessageStructure="json",
            )
            logger.info("SNS error notification sent")
        except Exception as sns_error:
            logger.error(f"Failed to send SNS error notification: {sns_error}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {e}")
