from github import Github
from FidoSelf import config
import base64
import os
import glob

class Git:
    def __init__(self, token=config.GIT_TOKEN, repo="iMaBoLi/FidoSelf"):
        self.token = base64.b64decode(token).decode('utf-8')
        self.git = Github(self.token)
        self.repo = self.git.get_repo(repo)

    def create(self, content, newfile):
        try:
            self.repo.create_file(newfile, f"Create {newfile.split('/')[-1]}", content, branch="main")
            return True
        except Exception as error:
            return error

    def update(self, file, content):
        try:
            contents = self.repo.get_contents(file, ref="main")
            self.repo.update_file(contents.path,  f"Update {file.split('/')[-1]}", content, contents.sha, branch="main")
            return True
        except Exception as error:
            return error

    def delete(self, file):
        try:
            contents = self.repo.get_contents(file, ref="main")
            self.repo.delete_file(contents.path,  f"Remove {file.split('/')[-1]}", contents.sha, branch="main")
            return True
        except Exception as error:
            return error
