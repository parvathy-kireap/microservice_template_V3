from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)


class SampleAddV0ReqModel(BaseModel):
    name: str = Field(..., description="Name of the sample")

    # sample request
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "sample name",
            }
        }
    )

    @field_validator("name")
    def validate_name(cls, value):
        if not value:
            raise ValueError("Name cannot be empty")
        # if contains special characters
        if not value.isalnum():
            raise ValueError("Name must be alphanumeric")
        return value

class SampleUpdateV0ReqModel(BaseModel):
    id: int = Field(..., description="Id of the sample")
    name: str = Field(..., description="Name of the sample")

    # sample request
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "sample name",
            }
        }
    )

    @field_validator("name")
    def validate_name(cls, value):
        if not value:
            raise ValueError("Name cannot be empty")
        # if contains special characters
        if not value.isalnum():
            raise ValueError("Name must be alphanumeric")
        return value
    
    @field_validator("id")
    def validate_id(cls, value):
        if not value:
            raise ValueError("Id cannot be empty")
        # if contains special characters
        if not isinstance(value, int):
            raise ValueError("Id must be integer")
        return value
    
class SampleFetchV0ReqModel(BaseModel):
    id: int = Field(..., description="Id of the sample")

    # sample request
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
            }
        }
    )
    
    @field_validator("id")
    def validate_id(cls, value):
        if not value:
            raise ValueError("Id cannot be empty")
        # if contains special characters
        if not isinstance(value, int):
            raise ValueError("Id must be integer")
        return value