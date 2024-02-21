from git import Repo
from os import path, remove


class CloudOperations:
    def __init__(self, user_id, github_url, repo_type):
        self.github_url = github_url
        self.repo_type = repo_type
        self.user_id = user_id
        self.clone_dir = f"/tmp/git/{self.user_id}"

    async def launch(self):
        self.clone()
        return {"Status": "Success"}

    def clone(self):
        if path.isdir(self.clone_dir):
            print("clone directory already exist.")
            print(f"Removing ... {self.clone_dir}")
            remove(self.clone_dir)
        try:
            local_dir = f"/tmp/git/{self.user_id}"
            Repo.clone_from(self.github_url, local_dir)
        except Exception:
            raise Exception(f"Cant able to clone the repo {self.github_url}")
