from typing import List, Union, Optional
from .subscriber import Subscriber
from .newspaper import Newspaper
from .editors import Editor
from .issue import Issue

class Agency(object):
    singleton_instance = None

    def __init__(self):
        self.newspapers: List[Newspaper] = []
        self.editors: List[Editor] = []
        self.subscribers: List[Subscriber] = []


    @staticmethod
    def get_instance():
        if Agency.singleton_instance is None:
            Agency.singleton_instance = Agency()

        return Agency.singleton_instance

    def add_newspaper(self, new_paper: Newspaper):
        #TODO: assert that ID does not exist  yet (or create a new one)
        self.newspapers.append(new_paper)

    def get_newspaper(self, paper_id: Union[int,str]) -> Optional[Newspaper]:
        for paper in self.newspapers:
            if paper.paper_id == paper_id:
                return paper
        return None

    def all_newspapers(self) -> List[Newspaper]:
        return self.newspapers

    def remove_newspaper(self, paper: Newspaper):
        self.newspapers.remove(paper)

    def add_editor(self, new_editor: Editor):
        self.editors.append(new_editor)

    def get_editor(self, editor_id: Union[int,str]) -> Optional[Editor]:
        for editor in self.editors:
            if editor.editor_id == editor_id:
                return editor
        return None
    def del_editor(self, editor: Editor):
        self.editors.remove(editor)
    
    def all_editors(self):
        return self.editors
    

    def add_subscriber(self, new_subscriber: Subscriber):
        self.subscribers.append(new_subscriber)

    def get_subscriber(self, subscriber_id: Union[int,str]) -> Optional[Subscriber]:
        for subscriber in self.subscribers:
            if subscriber.subscriber_id == subscriber_id:
                return subscriber
        return None
    
    def del_subscriber(self, subscriber: Subscriber):
        self.subscribers.remove(subscriber)

    def all_subscribers(self):
        return self.subscribers
    

    def subscribe_subscriber(self, subscriber_id: Union[int,str], newspaper_id: Union[int,str]) -> Optional[Subscriber]:
        subscriber = self.get_subscriber(subscriber_id)
        if subscriber is None:
            return None
        paper = self.get_newspaper(newspaper_id)
        if paper is None:
            return None
        subscriber.subscribe(paper)
        return subscriber
    