'''
the deck class
'''

from typing import List, Dict, Any
from time import mktime, time, asctime, localtime
from card import Card


class Deck:
    '''
    a deck is a collection of cards

    Args:
        name: the name of the deck, e.g. "U.S. State Capitals"
        card_prefix: an optional prefix that can be put in front of each card's front text,
                     e.g. "What is the captial of this state?"
    '''
    def __init__(self, name: str, card_prefix: str = ''):
        self.name = name
        self.cards: List[Card] = []
        self.card_prefix = card_prefix

    def __iter__(self) -> Card:
        for card in self.cards:
            yield card

    def __str__(self) -> str:
        return f'{self.name}: {len(self.cards)} cards'

    def to_dict(self) -> Dict[str, Any]:
        '''
        construct a dictionary that represents this deck
        '''
        return {
            'name': self.name,
            'card_prefix': self.card_prefix,
            'cards': [card.to_dict() for card in self.cards]
        }

    def __repr__(self) -> str:
        return repr(self.to_dict())

    def next_card_due(self) -> Card:
        '''
        card that is due for review next
        '''
        return min(self.cards, key = lambda card: mktime(card.recall_data.next_due))

    def any_due_now(self) -> bool:
        '''
        return true iff some card is do for practice now
        '''
        return self.next_card_due().due() == 'now'

    def cards_due_now(self):
        '''
        return an iterator over cards due now
        '''
        return filter(
            lambda card: mktime(card.recall_data.next_due) <= time(),
            self.cards)

    def number_cards_due_now(self) -> int:
        '''
        how many cards are due for review right now
        '''
        return len(list(self.cards_due_now()))

    def due_now(self) -> Card:
        '''
        generate a sequence of cards that are due for review right now
        '''
        for card in sorted(
                self.cards_due_now(),
                key = lambda card: card.recall_data.next_due):
            yield card

    def add(self, card: Card) -> None:
        '''
        add a card to the deck

        Args:
            card: card to add
        '''
        self.cards.append(card)

    def remove(self, id: int) -> None:
        '''
        remove a card from the deck

        Args:
            id: unique id of card to remove
        '''
        i = -1
        index = None
        for card in self:
            i += 1
            if card.id == id:
                index = i
                break
        if index:
            del self.cards[index]

    @classmethod
    def from_dict(cls, deck_dict: Dict[str, Any]):
        '''
        recover a deck from a dictionary (inverse of to_dict)
        '''
        deck = Deck(deck_dict['name'], deck_dict['card_prefix'])
        deck.cards = [Card.from_dict(card) for card in deck_dict['cards']]
        return deck