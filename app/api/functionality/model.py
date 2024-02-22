from beanie import Document


class Deployment(Document):
    deploy_id: str
    user_id: str
    user_email: str
    enabled: bool

    def __repr__(self) -> str:
        return f"<DEPLOYMENTS  {self.deploy_id}>"

    class Settings:
        name = "deployments"
