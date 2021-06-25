from app.api.models import RegisterFileInfo, FileProcessLog, FileProcessStepLog
from app.api.db import database, file_process_log, file_process_step_log


async def add_file_process_log(payload: FileProcessLog):
    query = file_process_log.insert().values(**payload)
    return await database.execute(query=query)


async def add_file_process_step_log(payload: FileProcessStepLog):
    query = file_process_step_log.insert().values(**payload)
    return await database.execute(query=query)


async def check_if_file_exists(file_hash: str):
    query = (
        "select exists(select 1 from file_process_log where file_hash = '{0}')".format(
            file_hash
        )
    )
    return await database.execute(query=query)


async def get_file_process_data():
    query = file_process_log.select()
    return await database.fetch_all(query=query)


async def get_file_process_step_data():
    query = file_process_step_log.select()
    return await database.fetch_all(query=query)
