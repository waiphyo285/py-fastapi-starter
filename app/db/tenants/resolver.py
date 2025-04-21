from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Request, HTTPException
from contextvars import ContextVar

TENANT_DB_MAP = {
    "default": "mysql+pymysql://root:root@localhost:33060/fast_openai_db",
    "x_t0_db": "mysql+pymysql://root:root@localhost:33060/fast_openai_t0",
    "x_t1_db": "mysql+pymysql://root:root@localhost:33060/fast_openai_t1",
}

_session_ctx = ContextVar("session_ctx", default=None)

def get_tenant_id(request: Request) -> str:
    tenant_id = request.headers.get("X-Tenant-ID", "default")
    if not tenant_id:
        raise HTTPException(status_code=400, detail="Missing X-Tenant-ID header")
    if tenant_id not in TENANT_DB_MAP:
        raise HTTPException(status_code=404, detail="Invalid tenant")
    return tenant_id

def get_db(request: Request) -> Session:
    tenant_id = get_tenant_id(request)
    db_url = TENANT_DB_MAP[tenant_id]

    engine = create_engine(db_url)
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

    db = SessionLocal()
    _session_ctx.set(db)

    try:
        yield db
    finally:
        db.close()
        _session_ctx.set(None)
