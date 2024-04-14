
class Issue(object):

    def __init__(self, releasedate, num_pages,issue_id, released: bool = False):
        self.releasedate = releasedate
        self.issue_id = issue_id
        self.released: bool = released
        self.num_pages = num_pages
        self.editor = None
        

    def set_editor(self, editor):
        self.editor = editor

    def release_issue(self):
        self.released = True
        return self.released


