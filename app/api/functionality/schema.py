from pydantic import BaseModel
import typing


class Deployment(BaseModel):
    github_url: str
    repo_type: str

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
