import git
import os
import time

class GitExtension:
    """ Get git into on the site for display on the about page """
    first = True
    needs = {'request'}
    provides = {'git'}

    def __init__(self):
        pass

    def start(self, context):
        context.repo = git.Repo(os.path.join(os.path.dirname(__file__), '..', '..'))
        context.git_hexsha = context.repo.head.commit.hexsha
        context.git_date = time.strftime("%Y-%m-%d %H:%M:%S %z", time.gmtime(context.repo.head.commit.committed_date))
        context.git_message = context.repo.head.commit.message
        context.git_name = context.repo.head.commit.committer.name
        context.git_total_commits = len(list(context.repo.iter_commits()))

