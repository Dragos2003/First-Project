from typing import List

from flask_restx import Model

from .issue import Issue

from .subscriber import Subscriber

class Newspaper(object):

    def __init__(self, paper_id: int, name: str, frequency: int, price: float):
        self.paper_id: int = paper_id
        self.name: str = name
        self.frequency: int = frequency  # the issue frequency (in days)
        self.price: float = price  # the monthly price
        self.issues: List[Issue] = []

    def add_issue(self, issue: Issue):
        self.issues.append(issue)
        return issue
    
    def get_issue(self, issue_id: int):
        for issue in self.issues:
            if issue.issue_id == issue_id:
                return issue
        return None
    
    def add_special_issue(self, issue: Issue):
        self.issues.append(issue)
        return issue
    
    def get_special_issue(self, issue_id: int):
        for issue in self.issues:
            if issue.issue_id == issue_id:
                return issue
        return None
    
    def remove_issue(self, issue: Issue):
        self.issues.remove(issue)
        return issue
    
    def remove_special_issue(self, issue: Issue):
        self.issues.remove(issue)
        return issue
    
    def all_issues(self):
        return self.issues
    
    def all_special_issues(self):
        return self.issues
    
    def add_subscriber(self, subscriber: Subscriber):
        subscriber.subscribe(self)
        self.subscribers.append(subscriber)
        return subscriber
    
    def remove_subscriber(self, subscriber: Subscriber):
        subscriber.unsubscribe(self)
        self.subscribers.remove(subscriber)
        return subscriber
    
    def all_subscribers(self):
        return self.subscriber
    
