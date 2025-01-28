from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.core.database.connectivity.sync_connect import get_sync_db
from app.core.database.tables.sample_tables import SampleTable
from app.features.sample.data.services.sample_service import SampleService
from app.features.sample.domain.req_models.sample_add_v0 import (
    SampleAddV0ReqModel,
    SampleFetchV0ReqModel,
    SampleUpdateV0ReqModel,
)
from app.features.sample.domain.res_models.sample_add_v0 import (
    SampleAddV0ResModel,
    SampleDeleteV0ResModel,
)
from app.shared.config.endpoints.details import APIEndpointDetail
from app.shared.config.routers.setup import RouterSetup


sample_router_V0 = APIRouter(
    prefix=RouterSetup.sample_router_v0.prefix,
    tags=RouterSetup.sample_router_v0.tag
    )


@sample_router_V0.post(path=APIEndpointDetail.sample_add_v0.path,
                       summary=APIEndpointDetail.sample_add_v0.summary,
                       description=APIEndpointDetail.sample_add_v0.description,
                       response_model=SampleAddV0ResModel,
                       )
async def sample_add_v0(req_body: SampleAddV0ReqModel,
                        db: Session = Depends(get_sync_db)):
    sample_service = SampleService(db)
    try:
        data: SampleTable = sample_service.add_new(name=req_body.name)
        return SampleAddV0ResModel(id=data.id, name=data.name)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@sample_router_V0.put(path=APIEndpointDetail.sample_update.path,
                   summary=APIEndpointDetail.sample_update.summary,
                   description=APIEndpointDetail.sample_update.description,
                   response_model=SampleAddV0ResModel)
async def sample_update(req_body: SampleUpdateV0ReqModel, db: Session = Depends(get_sync_db)):
    sample_service = SampleService(db)
    try:
        data : SampleTable = sample_service.update_sample(id=req_body.id,name=req_body.name)
        return SampleAddV0ResModel(id = data.id, name = data.name)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))
    
@sample_router_V0.get(path=APIEndpointDetail.get_sample.path,
                   summary=APIEndpointDetail.get_sample.summary,
                   description=APIEndpointDetail.get_sample.description,
                   response_model=SampleAddV0ResModel)
async def get_sample_data(id: int, db: Session = Depends(get_sync_db)):
    sample_service = SampleService(db)
    try:
        data : SampleTable = sample_service.get_sample(id=id)
        return SampleAddV0ResModel(id = data.id, name = data.name)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))
    
@sample_router_V0.delete(path=APIEndpointDetail.delete_sample.path,
                   summary=APIEndpointDetail.delete_sample.summary,
                   description=APIEndpointDetail.delete_sample.description,
                   response_model=SampleDeleteV0ResModel)
async def delete_sample_data(req_body: SampleFetchV0ReqModel, db: Session = Depends(get_sync_db)):
    sample_service = SampleService(db)
    try:
        # sample_service.get_sample(id=req_body.id)
        sample_service.delete_sample(id=req_body.id)
        return SampleDeleteV0ResModel()
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))