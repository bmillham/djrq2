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
        committed_date = context.repo.head.commit.committed_date
        context.git_date = time.strftime(format_string, time.gmtime(committed_date))
        context.git_message = context.repo.head.commit.message
        context.git_name = context.repo.head.commit.committer.name
        context.git_total_commits = len(list(context.repo.iter_commits()))

        context.git_release = None
        context.git_tags = {}

        starttime = time.time()
        context.git_totals = {'files': 0,
                      'lines': 0,
                      'insertions': 0,
                      'deletions': 0,}
        for i, c in enumerate(context.repo.iter_commits('master')):
            for s in ('files', 'lines', 'insertions', 'deletions'):
                context.git_totals[s] += c.stats.total[s]

        print('end', time.time() - starttime)
        for t in context.repo.tags:
            context.git_tags[t.commit.hexsha] = t.name
            tagged_date = t.tag.tagged_date
            if context.git_hexsha == t.commit.hexsha or tagged_date < committed_date:
                context.git_release = t.name
                if tagged_date != committed_date and context.git_hexsha != t.commit.hexsha:
                    context.git_release += ' +' + context.git_hexsha[:7]
                context.git_release_date = time.strftime(format_string, time.gmtime(tagged_date))

