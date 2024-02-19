from pydantic import BaseModel
import typing
from uuid import uuid4 as uuid


class Deployment(BaseModel):
    id: typing.Optional[str]
    github_url: str
    repo_type: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": f"{uuid()}",
                    "github_url": "https://github.com/Vortexdude/static_site.git",
                    "repo_type": "static",
                }
            ]
        }
    }
