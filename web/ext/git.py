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
        grepo = git.Repo(os.path.join(os.path.dirname(__file__), '..', '..'))
        context.git_hexsha = grepo.head.commit.hexsha
        context.git_date = time.strftime("%Y-%m-%d %H:%M:%S %z", time.gmtime(grepo.head.commit.committed_date))
        context.git_message = grepo.head.commit.message
        context.git_name = grepo.head.commit.committer.name
