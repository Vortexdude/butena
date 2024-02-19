from git import Repo


class CloudOperations:
    def __init__(self, github_url, repo_type, id=None):
        self.github_url = github_url
        self.repo_type = repo_type
        self.user_id = id

    async def launch(self):
        self.clone()
        return {"Status": "Success"}

    def clone(self):
        try:
            local_dir = f"/tmp/git/{self.user_id}"
            Repo.clone_from(self.github_url, local_dir)
        except Exception:
            raise Exception(f"Cant able to clone the repo {self.github_url}")
