'''
the card class
'''

from dataclasses import dataclass, field
from time import localtime, struct_time, mktime, asctime, time
from typing import List, Dict, Any

@dataclass
class RecallHistoryElement:
    '''
    stores data about the history of recall
    '''
    timestamp: struct_time
    result: bool

    def to_dict(self) -> Dict[str, Any]:
        '''
        construct a dictionary that represents this element
        '''
        return {
            'timestamp': mktime(self.timestamp),
            'result': self.result
        }

    def __repr__(self) -> str:
        return repr(self.to_dict())

    @classmethod
    def from_dict(cls, element_dict: Dict[str, Any]):
        '''
        recover recall history element from a dictionary (inverse of to_dict)
        '''
        element = RecallHistoryElement(
            localtime(element_dict['timestamp']),
            element_dict['result'])
        return element

@dataclass
class RecallHistory:
    '''
    stores data about the history of recall
    '''
    data: List[RecallHistoryElement] = field(default_factory=list)
    accuracy: float = 0

    def to_dict(self) -> Dict[str, Any]:
        '''
        construct a dictionary that represents this recall history
        '''
        return {
            'data': [element.to_dict() for element in self.data],
            'accuracy': self.accuracy
        }

    def __repr__(self) -> str:
        return repr(self.to_dict())

    def append(self, result: bool) -> None:
        '''
        append a recall result to the history
        '''
        x = 1 if result else 0
        a, n = self.accuracy, len(self.data)
        self.accuracy = (a * n + x) / (n + 1)
        self.data.append(
            RecallHistoryElement(
                localtime(),
                result
            ))

    @classmethod
    def from_dict(cls, history_dict: Dict[str, Any]):
        '''
        recover recall history from a dictionary (inverse of to_dict)
        '''
        history = RecallHistory(
            [RecallHistoryElement.from_dict(element) for element in history_dict['data']],
            history_dict['accuracy'])
        return history

@dataclass
class RecallData:
    '''
    stores data about the user's recall of a card
    '''
    next_due: struct_time = localtime()
    current_streak: int = 0
    history: RecallHistory = field(default_factory=RecallHistory)

    def to_dict(self) -> Dict[str, Any]:
        '''
        construct a dictionary that represents this recall data
        '''
        return {
            'next_due': mktime(self.next_due),
            'current_streak': self.current_streak,
            'history': self.history.to_dict()
        }

    def __repr__(self) -> str:
        return repr(self.to_dict())

    def record_success(self) -> None:
        '''
        recompute next_due, increment streak, log event for a successful recall
        '''
        if self.current_streak < 0:
            self.current_streak = 0
        self.current_streak += 1
        streak = self.current_streak
        period = 4 * streak * 3600  # seconds
        now = mktime(localtime())
        self.next_due = localtime(now + period)
        self.history.append(True)

    def record_failure(self) -> None:
        '''
        recompute next_due, increment streak, log event for a failed recall
        '''
        if self.current_streak > 0:
            period = 4 * 3600  # 4 hours in seconds
            self.current_streak = -1
        else:
            period = 4 * 3600 * 2 ** (self.current_streak) # seconds
            self.current_streak -= 1
        now = mktime(localtime())
        self.next_due = localtime(now + period)
        self.history.append(False)

    @classmethod
    def from_dict(cls, recall_data_dict: Dict[str, Any]):
        '''
        recover recall data from a dictionary (inverse of to_dict)
        '''
        recall_data = RecallData(
            localtime(recall_data_dict['next_due']),
            recall_data_dict['current_streak'],
            RecallHistory.from_dict(recall_data_dict['history']))
        return recall_data

class Card:
    '''
    represents a card
    '''
    _next_id: int = 1

    def __init__(self, front: str, back: str):
        self.id = Card._next_id
        self.front = front
        self.back = back
        self.recall_data: RecallData = RecallData()
        Card._next_id += 1

    def __str__(self) -> str:
        return self.front

    def to_dict(self) -> Dict[str, Any]:
        '''
        construct a dictionary that represents this card
        '''
        return {
            'id': self.id,
            'front': self.front,
            'back': self.back,
            'recall_data': self.recall_data.to_dict()
        }

    def __repr__(self) -> str:
        return repr(self.to_dict())

    def recall_success(self) -> None:
        '''
        handle a successful recall
        '''
        self.recall_data.record_success()

    def recall_failure(self) -> None:
        '''
        handle an unsuccessful recall
        '''
        self.recall_data.record_failure()

    def due(self) -> str:
        '''
        ascii time until card is due for review
        '''
        t = mktime(self.recall_data.next_due)
        diff = t - time()
        if diff <= 0:
            return "now"
        if diff < 60:
            return "in less than 1 minute"
        if diff < 3600:
            return f'in {int(diff/60)} minutes'
        if diff < 86400:
            return f'in {int(diff/3600)} hours'
        return f'in {int(diff/86400)} days'

    @classmethod
    def from_dict(cls, card_dict: Dict[str, Any]):
        '''
        recover a card from a dictionary (inverse of to_dict)
        '''
        card = Card(
            card_dict['front'],
            card_dict['back'])
        card.id = card_dict['id']
        card.recall_data = RecallData.from_dict(card_dict['recall_data'])
        return card