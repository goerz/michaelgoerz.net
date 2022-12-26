"""Get the history of files from git."""

import datetime
from pathlib import Path

from dulwich.repo import Repo

REPO = Repo(Path(__file__).parent.parent)


class Commit:
    """Git commit object.

    Attributes:

    * `id`: The commit ID as a string
    * `date`: The date when the commit was made as a `datetime`.
    """

    def __init__(self, commit_id, date):
        self.id = commit_id
        self.date = date


def get_history(path):
    """Get a list of commits for the given `path`.

    The `path` must a relative to the root of the `REPO`.
    """
    w = REPO.get_walker(paths=[str(path).encode("utf-8")])
    history = []
    for entry in w:
        commit_id = entry.commit.id.decode("utf-8")
        date = datetime.datetime.fromtimestamp(entry.commit.commit_time)
        history.append(Commit(commit_id, date))
    return history
