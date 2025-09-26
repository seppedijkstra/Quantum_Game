import random

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def value(self):
        try:
            if self.rank in ['J', 'Q', 'K']:
                return 10
            if self.rank == 'A':
                return 11  # or 1 based on game rules
            return int(self.rank)  # Assuming rank is a number string for 2-10
        except ValueError:
            raise ValueError("Invalid rank value")
        
class Deck:
    def __init__(self, n_decks=1):
        self.cards = []
        for _ in range(n_decks):
            for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades']:
                for rank in range(2, 11):
                    self.cards.append(Card(rank, suit))
                for rank in ['J', 'Q', 'K', 'A']:
                    self.cards.append(Card(rank, suit))
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop() if self.cards else None

class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def best_value(self):
        # Calculate the best total value of the hand, considering Aces as 1 or 11
        total = sum(card.value() for card in self.cards)
        aces = sum(1 for card in self.cards if card.rank == 'A')
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    def is_blackjack(self):
        return len(self.cards) == 2 and self.best_value() == 21

    def is_bust(self):
        return self.best_value() > 21


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Hand()

    def draw(self, deck):
        card = deck.draw()
        if card:
            self.hand.add_card(card)
        return card

    def decide(self):
        # Ask for input (hit/stand)
        action = input(f"{self.name}, do you want to hit or stand? ").strip().lower()
        while action not in ['hit', 'stand']:
            print("Invalid input. Please enter 'hit' or 'stand'.")
            action = input(f"{self.name}, do you want to hit or stand? ").strip().lower()
        return action

class Dealer(Player):
    def play(self, deck):
        # Dealer keeps hitting until 17 or higher
        while self.hand.best_value() < 17:
            self.draw(deck)
            print(f"{self.name} drew a card.")

class Game:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.player = Player("Player")
        self.dealer = Dealer("Dealer")

    def deal_initial(self):
        for _ in range(2):
            card = self.player.draw(self.deck)
            print(f"{self.player.name} drew {card.rank} of {card.suit}. Current value: {self.player.hand.best_value()}")
            self.dealer.draw(self.deck)
        print(f"{self.player.name}'s initial hand value: {self.player.hand.best_value()}")
        print(f"{self.dealer.name}'s visible card: {self.dealer.hand.cards[0].rank} of {self.dealer.hand.cards[0].suit}")
        if self.player.hand.is_blackjack():
            print(f"{self.player.name} has a blackjack! {self.player.name} wins!")

    def player_turn(self):
        action = self.player.decide()
        while action == 'hit':
            card = self.player.draw(self.deck)
            print(f"{self.player.name} drew {card.rank} of {card.suit}. Current value: {self.player.hand.best_value()}")
            if self.player.hand.is_bust():
                print(f"{self.player.name} busts with value {self.player.hand.best_value()}!")
                return
            action = self.player.decide()
        # Player stands
        print(f"{self.player.name} stands with value {self.player.hand.best_value()}.")

    def dealer_turn(self):
        self.dealer.play(self.deck)
        print(f"{self.dealer.name} stands with value {self.dealer.hand.best_value()}.")

    def determine_winner(self):
        player_value = self.player.hand.best_value()
        dealer_value = self.dealer.hand.best_value()

        if self.player.hand.is_bust():
            print("Dealer wins! Player busted.")
        elif self.dealer.hand.is_bust():
            print("Player wins! Dealer busted.")
        elif player_value > dealer_value:
            print("Player wins!")
        elif dealer_value > player_value:
            print("Dealer wins!")
        else:
            print("It's a tie!")

    def play_round(self):
        self.player_turn()
        if not self.player.hand.is_bust():
            self.dealer_turn()

    def start(self):
        self.deal_initial()
        if not self.player.hand.is_blackjack():
            self.play_round()
            self.determine_winner()

game = Game()
game.start()