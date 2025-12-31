from app.api.models import RegisterFileInfo, FileProcessLog, FileProcessStepLog
from app.api.db import database, file_process_log, file_process_step_log
from sqlalchemy import text


async def add_file_process_log(payload: FileProcessLog):
    """
    Insert a new file process log record.
    
    Args:
        payload: File process log data
        
    Returns:
        Last inserted record ID
    """
    query = file_process_log.insert().values(**payload)
    return await database.execute(query=query)


async def add_file_process_step_log(payload: FileProcessStepLog):
    """
    Insert a new file process step log record.
    
    Args:
        payload: File process step log data
        
    Returns:
        Last inserted record ID
    """
    query = file_process_step_log.insert().values(**payload)
    return await database.execute(query=query)


async def check_if_file_exists(file_hash: str):
    """
    Check if a file with the given hash already exists in the system.
    
    Args:
        file_hash: MD5 hash of the file identifier
        
    Returns:
        bool: True if file exists, False otherwise
    """
    query = text(
        "select exists(select 1 from file_process_log where file_hash = :file_hash)"
    )
    return await database.execute(query=query, values={"file_hash": file_hash})


async def get_file_process_data():
    """
    Retrieve all file process log records.
    
    Returns:
        List of all file process records
    """
    query = file_process_log.select()
    return await database.fetch_all(query=query)


async def get_file_process_step_data():
    """
    Retrieve all file process step log records.
    
    Returns:
        List of all file process step records
    """
    query = file_process_step_log.select()
    return await database.fetch_all(query=query)
