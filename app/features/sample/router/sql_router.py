from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy import text
from sqlalchemy.engine import Connection
from app.core.database.connectivity.sync_connect import  get_conn_sync_db
from app.core.database.tables.sample_tables import SampleTable
from app.features.sample.data.services.sample_service import SqlSampleService
from app.features.sample.domain.req_models.sample_add_v0 import (
    SampleAddV0ReqModel,
    SampleFetchV0ReqModel,
    SampleUpdateV0ReqModel,
)
from app.features.sample.domain.res_models.sample_add_v0 import (
    SampleAddV0ResModel,
    SampleDeleteV0ResModel,
    SampleGetV0ResModel,
)
from app.shared.config.endpoints.details import APIEndpointDetail
from app.shared.config.routers.setup import RouterSetup, SqlRouterSetUp


sql_sample_router = APIRouter(
    prefix=SqlRouterSetUp.sql_sample_router.prefix,
    tags=SqlRouterSetUp.sql_sample_router.tag
    )


@sql_sample_router.post(path=APIEndpointDetail.sample_add_v0.path,
                       summary=APIEndpointDetail.sample_add_v0.summary,
                       description=APIEndpointDetail.sample_add_v0.description,
                       response_model=SampleAddV0ResModel,
                       )
async def sample_add_v0(req_body: SampleAddV0ReqModel,
                        connection: Connection = Depends(get_conn_sync_db)):
    sample_service = SqlSampleService(connection)
    try:
        data: SampleTable = sample_service.add_new(name=req_body.name)
        return SampleAddV0ResModel(id=data.id, name=data.name)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@sql_sample_router.put(path=APIEndpointDetail.sample_update.path,
                   summary=APIEndpointDetail.sample_update.summary,
                   description=APIEndpointDetail.sample_update.description,
                   response_model=SampleAddV0ResModel)
async def sample_update(req_body: SampleUpdateV0ReqModel, connection: Connection = Depends(get_conn_sync_db)):
    sample_service = SqlSampleService(connection)
    try:
        data : SampleTable = sample_service.update_sample(id=req_body.id,name=req_body.name)
        return SampleAddV0ResModel(id = data.id, name = data.name)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))
    
@sql_sample_router.get(path=APIEndpointDetail.get_sample.path,
                   summary=APIEndpointDetail.get_sample.summary,
                   description=APIEndpointDetail.get_sample.description,
                   response_model=SampleGetV0ResModel)
async def get_sample_data(id: int, connection: Connection = Depends(get_conn_sync_db)):
    sample_service = SqlSampleService(connection)
    try:
        # import pdb;pdb.set_trace()
        data : SampleTable = sample_service.get_sample(id=id)
        return SampleGetV0ResModel(id=data.id, name=data.name, address=data.address)
        # return SampleAddV0ResModel(id = data.id, name = data.name)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))
    
@sql_sample_router.delete(path=APIEndpointDetail.delete_sample.path,
                   summary=APIEndpointDetail.delete_sample.summary,
                   description=APIEndpointDetail.delete_sample.description,
                   response_model=SampleDeleteV0ResModel)
async def delete_sample_data(req_body: SampleFetchV0ReqModel, connection: Connection = Depends(get_conn_sync_db)):
    sample_service = SqlSampleService(connection)
    try:
        # sample_service.get_sample(id=req_body.id)
        sample_service.delete_sample(id=req_body.id)
        return SampleDeleteV0ResModel()
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))
