from typing import List, Optional
from .newspaper import Newspaper
from .issue import Issue
from .agency import Agency

class Subscriber:
    def __init__(self, subscriber_id: str, name: str, address: str, subscription: List[Newspaper] = [], special_issues: List[Issue] = []):
        self.name = name
        self.address = address
        self.subscriber_id = subscriber_id
        self.subscription: List[Newspaper] = subscription
        self.special_issues: List[Issue] = special_issues
        

    def subscribe(self, newspaper: Newspaper):
        if newspaper not in self.subscription:
            self.subscription.append(newspaper)
            return newspaper
        
    def unsubscribe(self, newspaper: Newspaper):
        if newspaper in self.subscription:
            self.subscription.remove(newspaper)
            return newspaper
        
    def subscribe_special_issue(self, issue: Issue):
        if issue not in self.special_issues:
            self.special_issues.append(issue)
            return issue
        
    def unsubscribe_special_issue(self, issue: Issue):
        if issue in self.special_issues:
            self.special_issues.remove(issue)
            return issue
        
    def mark_issue_delivered(self, issue: Issue):
        issue.delivered = True
        return issue
        
    def calculate_subscription_cost(self) -> float:
        monthly_cost = sum(newspaper.price for newspaper in self.subscription)
        return monthly_cost
    
    def calculate_annual_cost(self) -> float:
        monthly_cost = self.calculate_subscription_cost()
        annual_cost = monthly_cost * 12
        return annual_cost
    
    def get_num_subscription(self) -> int:
        return len(self.subscription)
