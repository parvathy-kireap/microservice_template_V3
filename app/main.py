from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
)

import app.shared.config.routers.router_list as routers
from app.app_setup import App
from app.core.database.connectivity.checker import check_db_connection
from app.core.database.connectivity.sync_connect import (
    db_base,
    sync_db_engine,
)
from app.shared.config.endpoints.details import APIEndpointDetail


db_base.metadata.create_all(bind=sync_db_engine)

# app
app = FastAPI(
    title=App.TITLE,
    description=App.DESCRIPTION,
    version=App.VERSION
)


# Root Route
@app.get(path=APIEndpointDetail.root.path,
         tags=APIEndpointDetail.root.tags,
         summary=APIEndpointDetail.root.summary,
         description=APIEndpointDetail.root.description,
         )
async def root(is_db_connected: bool = Depends(check_db_connection)):
    if is_db_connected:
        return {"message": "Database is connected"}

    raise HTTPException(status_code=500, detail="Database is not connected")

app.include_router(routers.sample_router_V0)
