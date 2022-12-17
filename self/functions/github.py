from github import Github
from self import config
import base64
import os
import glob

class Git:
    def __init__(self, token=config.GIT_TOKEN, repo="imAboli/SmartSelf"):
        self.token = base64.b64decode(token).decode('utf-8')
        self.git = Github(self.token)
        self.repo = self.git.get_repo(repo)

    def create(self, oldfile, newfile):
        try:
            content = open(oldfile, "r").read()
        except:
            content = open(oldfile, "rb").read()
        try:
            self.repo.create_file(newfile, f"Create {newfile.split('/')[-1]}", content, branch="master")
            return True
        except:
            return False

    def update(self, file, oldfile):
        try:
            content = open(oldfile, "r").read()
        except:
            content = open(oldfile, "rb").read()
        try:
            contents = self.repo.get_contents(file, ref="master")
            self.repo.update_file(contents.path,  f"Update {file.split('/')[-1]}", content, contents.sha, branch="master")
            return True
        except:
            return False

    def delete(self, file):
        try:
            contents = self.repo.get_contents(file, ref="master")
            self.repo.delete_file(contents.path,  f"Remove {file.split('/')[-1]}", contents.sha, branch="master")
            return True
        except:
            return False
