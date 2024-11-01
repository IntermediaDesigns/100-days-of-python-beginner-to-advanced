# Day 24 Mini Project: Deck of Cards Simulator

![Card Game](/Day%20024/card.png)

## Deck of Cards Simulator

This project showcases the use of `Counter`, `defaultdict`, `deque`, and `namedtuple` for managing cards, hands, and game states.



### Key Concepts from the `collections` Module

#### `namedtuple`
```python
Card = namedtuple('Card', ['rank', 'suit', 'value'])
```
- Used to create an immutable card representation
- Provides attribute access to card properties

#### `deque`
```python
self.cards = deque(
    Card(rank, suit, self.VALUES[rank])
    for suit in self.SUITS
    for rank in self.RANKS
)
```
- Used for the deck of cards
- Efficient append and pop operations from both ends
- Used with `popleft()` for dealing cards

#### `Counter`
```python
self.dealt_cards = Counter()
```
- Tracks dealt cards
- Used for analyzing hand combinations

```python
def get_suits(self) -> Counter:
    return Counter(card.suit for card in self.cards)
```

#### `defaultdict`
```python
self.hand_rankings = defaultdict(int, {
    'Royal Flush': 10,
    'Straight Flush': 9,
    # ...
})
```
- Used for storing hand rankings
- Provides default values for missing keys

## Key Features

### Card Management
- Card dealing and returning
- Deck shuffling
- Hand tracking

### Hand Analysis
- Poker hand evaluation
- Suit and rank counting
- Hand value calculation

### Game State
- Save/load functionality
- Game history tracking
- Player management

## To Extend This Project

### Add Support For
- Different card games
- Multiple decks
- Jokers
- Card counting

### Implement
- GUI interface
- Multiplayer networking
- AI players
- Tournament system

### Add Features For
- Betting system
- Score tracking
- Statistics
- Custom rules