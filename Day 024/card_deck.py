from collections import namedtuple, deque, Counter, defaultdict
from typing import List, Dict, Set
import random
import json
from datetime import datetime

# Define card structure using namedtuple
Card = namedtuple("Card", ["rank", "suit", "value"])


class Deck:
    # Define card ranks, suits, and values
    RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    SUITS = ["♠", "♣", "♥", "♦"]
    VALUES = {
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
        "A": 14,
    }

    def __init__(self, shuffle_deck: bool = True):
        # Create a deque of cards
        self.cards = deque(
            Card(rank, suit, self.VALUES[rank])
            for suit in self.SUITS
            for rank in self.RANKS
        )
        if shuffle_deck:
            self.shuffle()

        # Track dealt cards using Counter
        self.dealt_cards = Counter()

    def shuffle(self) -> None:
        """Shuffle the deck."""
        temp_list = list(self.cards)
        random.shuffle(temp_list)
        self.cards = deque(temp_list)

    def deal(self, num_cards: int = 1) -> List[Card]:
        """Deal specified number of cards."""
        if len(self.cards) < num_cards:
            raise ValueError("Not enough cards in deck")

        dealt = []
        for _ in range(num_cards):
            card = self.cards.popleft()
            self.dealt_cards[card] += 1
            dealt.append(card)
        return dealt

    def return_cards(self, cards: List[Card]) -> None:
        """Return cards to the deck."""
        for card in cards:
            if self.dealt_cards[card] > 0:
                self.dealt_cards[card] -= 1
                self.cards.append(card)
            else:
                raise ValueError(f"Card {card} was not dealt from this deck")

    def cards_remaining(self) -> int:
        """Get number of remaining cards."""
        return len(self.cards)


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0

    def add_card(self, card: Card) -> None:
        """Add a card to the hand."""
        self.cards.append(card)
        self.value += card.value

    def remove_card(self, card: Card) -> None:
        """Remove a card from the hand."""
        self.cards.remove(card)
        self.value -= card.value

    def get_suits(self) -> Counter:
        """Get count of each suit in hand."""
        return Counter(card.suit for card in self.cards)

    def get_ranks(self) -> Counter:
        """Get count of each rank in hand."""
        return Counter(card.rank for card in self.cards)


class PokerHandAnalyzer:
    def __init__(self):
        self.hand_rankings = defaultdict(
            int,
            {
                "Royal Flush": 10,
                "Straight Flush": 9,
                "Four of a Kind": 8,
                "Full House": 7,
                "Flush": 6,
                "Straight": 5,
                "Three of a Kind": 4,
                "Two Pair": 3,
                "One Pair": 2,
                "High Card": 1,
            },
        )

    def analyze_hand(self, hand: Hand) -> str:
        """Analyze poker hand and return the hand ranking."""
        suits = hand.get_suits()
        ranks = hand.get_ranks()
        values = sorted([card.value for card in hand.cards])

        # Check for flush
        is_flush = any(count >= 5 for count in suits.values())

        # Check for straight
        is_straight = False
        if len(values) >= 5:
            for i in range(len(values) - 4):
                if values[i + 4] - values[i] == 4:
                    is_straight = True
                    break

        # Check for royal flush
        if is_flush and set(ranks.keys()) & {"10", "J", "Q", "K", "A"}:
            return "Royal Flush"

        # Check for straight flush
        if is_flush and is_straight:
            return "Straight Flush"

        # Check for four of a kind
        if any(count >= 4 for count in ranks.values()):
            return "Four of a Kind"

        # Check for full house
        if any(count >= 3 for count in ranks.values()) and len(ranks) <= 3:
            return "Full House"

        if is_flush:
            return "Flush"

        if is_straight:
            return "Straight"

        if any(count >= 3 for count in ranks.values()):
            return "Three of a Kind"

        if len([count for count in ranks.values() if count >= 2]) >= 2:
            return "Two Pair"

        if any(count >= 2 for count in ranks.values()):
            return "One Pair"

        return "High Card"


class CardGame:
    def __init__(self):
        self.deck = Deck()
        self.players = defaultdict(Hand)
        self.analyzer = PokerHandAnalyzer()
        self.game_history = []

    def deal_hands(self, num_players: int, cards_per_hand: int) -> None:
        """Deal cards to specified number of players."""
        self.players.clear()
        for i in range(num_players):
            cards = self.deck.deal(cards_per_hand)
            for card in cards:
                self.players[f"Player {i+1}"].add_card(card)

    def show_hands(self) -> None:
        """Display all players' hands."""
        for player, hand in self.players.items():
            print(f"\n{player}'s Hand:")
            for card in hand.cards:
                print(f"{card.rank}{card.suit}", end=" ")
            print(f"\nHand Type: {self.analyzer.analyze_hand(hand)}")

    def save_game_state(self, filename: str) -> None:
        """Save the current game state to a file."""
        state = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "players": {
                player: [
                    {"rank": c.rank, "suit": c.suit, "value": c.value}
                    for c in hand.cards
                ]
                for player, hand in self.players.items()
            },
            "deck_remaining": self.deck.cards_remaining(),
        }

        self.game_history.append(state)

        with open(filename, "w") as f:
            json.dump(state, f, indent=4)


def main():
    game = CardGame()

    while True:
        print("\nCard Game Simulator")
        print("1. Deal New Hands")
        print("2. Show Current Hands")
        print("3. Shuffle Deck")
        print("4. Save Game State")
        print("5. Draw Additional Cards")
        print("6. Return Cards")
        print("7. Exit")

        choice = input("\nEnter your choice (1-7): ")

        try:
            if choice == "1":
                num_players = int(input("Enter number of players: "))
                cards_per_hand = int(input("Enter cards per hand: "))
                game.deal_hands(num_players, cards_per_hand)
                print("Hands dealt successfully!")

            elif choice == "2":
                game.show_hands()

            elif choice == "3":
                game.deck.shuffle()
                print("Deck shuffled!")

            elif choice == "4":
                filename = input("Enter filename to save game state: ")
                game.save_game_state(filename)
                print(f"Game state saved to {filename}")

            elif choice == "5":
                player = input("Enter player number: ")
                player_key = f"Player {player}"
                if player_key in game.players:
                    num_cards = int(input("Enter number of cards to draw: "))
                    new_cards = game.deck.deal(num_cards)
                    for card in new_cards:
                        game.players[player_key].add_card(card)
                    print(f"Drew {num_cards} cards for {player_key}")
                else:
                    print("Invalid player number")

            elif choice == "6":
                player = input("Enter player number: ")
                player_key = f"Player {player}"
                if player_key in game.players:
                    hand = game.players[player_key]
                    print("\nCurrent hand:")
                    for i, card in enumerate(hand.cards):
                        print(f"{i+1}. {card.rank}{card.suit}")
                    card_index = int(input("Enter card number to return: ")) - 1
                    if 0 <= card_index < len(hand.cards):
                        card = hand.cards[card_index]
                        hand.remove_card(card)
                        game.deck.return_cards([card])
                        print(f"Returned {card.rank}{card.suit} to deck")
                    else:
                        print("Invalid card number")
                else:
                    print("Invalid player number")

            elif choice == "7":
                print("Thanks for playing!")
                break

            else:
                print("Invalid choice. Please try again.")

        except Exception as e:
            print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
