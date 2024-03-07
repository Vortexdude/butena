from pydantic import BaseModel
from pydantic.version import VERSION as PYDANTIC_VERSION

PYDANTIC_V2 = PYDANTIC_VERSION.startswith("2.")


class Deployment(BaseModel):
    github_url: str
    repo_type: str

    if PYDANTIC_V2:
        model_config = {
            "json_schema_extra": {
                "examples": [
                    {
                        "github_url": "https://github.com/Vortexdude/static_site.git",
                        "repo_type": "static",
                    }
                ]
            }
        }

    else:
        class Config:
            json_schema_extra = {
                "example": [
                    {
                        "github_url": "https://github.com/Vortexdude/static_site.git",
                        "repo_type": "static",
                    }
                ]
            }


class DeploySchema(BaseModel):
    bucket: str
    zone: str

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "bucket": "butena-public",
                "zone": "ap-south-1",
            }]
        }
    }
