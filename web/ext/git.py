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
        format_string = "%Y-%m-%d %H:%M:%S %z"
        context.repo = git.Repo(os.path.join(os.path.dirname(__file__), '..', '..'))
        context.git_hexsha = context.repo.head.commit.hexsha
        context.git_date = time.strftime(format_string, time.gmtime(context.repo.head.commit.committed_date))
        context.git_message = context.repo.head.commit.message
        context.git_name = context.repo.head.commit.committer.name
        context.git_total_commits = len(list(context.repo.iter_commits()))
        context.git_release = None

        for t in context.repo.tags:
            print(t.commit, t.name, time.strftime(format_string, time.gmtime(t.tag.tagged_date)))
            if context.git_hexsha == t.commit.hexsha:
                context.git_release = t.name
                context.git_release_date = time.strftime(format_string, time.gmtime(t.tag.tagged_date))

