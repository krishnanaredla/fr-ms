from sqlalchemy import Column, MetaData, Table, create_engine, Sequence
from sqlalchemy.dialects import postgresql
from databases import Database
from app.api.settings import getConfig

cnf = getConfig()

DATABASE_URL = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
    cnf.DB_USER, cnf.DB_PASS, cnf.DB_HOST, cnf.DB_PORT, cnf.DB_DATABASE
)

engine = create_engine(DATABASE_URL)
metadata = MetaData()

file_process_log = Table(
    "file_process_log",
    metadata,
    Column(
        "file_process_id",
        postgresql.VARCHAR(100),
        primary_key=True,
    ),
    Column("fp_id", postgresql.BIGINT),
    Column("filename", postgresql.VARCHAR(100)),
    Column("source_ip", postgresql.VARCHAR(15)),
    Column("file_size", postgresql.BIGINT),
    Column("bucket_name", postgresql.VARCHAR(100)),
    Column("event_name", postgresql.VARCHAR(100)),
    Column("event_ts", postgresql.TIMESTAMP),
    Column("file_hash", postgresql.VARCHAR(100)),
    Column("create_by", postgresql.VARCHAR(20)),
    Column("create_ts", postgresql.TIMESTAMP),
)

file_process_step_log = Table(
    "file_process_step_log",
    metadata,
    Column("step_id", postgresql.BIGINT, Sequence("step_seq"), primary_key=True),
    Column("file_process_id", postgresql.VARCHAR(100)),
    Column("step_name", postgresql.VARCHAR(100)),
    Column("step_status", postgresql.VARCHAR(50)),
    Column("step_status_detail", postgresql.TEXT),
    Column("step_start_ts", postgresql.TIMESTAMP),
    Column("step_end_ts", postgresql.TIMESTAMP),
    Column("create_by", postgresql.VARCHAR(20)),
    Column("create_ts", postgresql.TIMESTAMP),
)

database = Database(DATABASE_URL)
