from typing import List

from flask_restx import Model

from .issue import Issue


class Editor:
    def __init__(self, editor_id, adress, name):
        self.editor_id = editor_id
        self.adress = adress
        self.name = name
        self.issues: List[Issue] = []

    def add_issue(self, issue: Issue):
        self.issues.append(issue)
        return issue

    def get_issue(self, issue_id: int):
        for issue in self.issues:
            if issue.issue_id == issue_id:
                return issue
        return None
    
    def remove_issue(self, issue: Issue):
        self.issues.remove(issue)
        return issue