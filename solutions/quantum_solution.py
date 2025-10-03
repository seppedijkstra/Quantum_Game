import random
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from math import sqrt

from model.model import Card, Deck

class QCard:
    def __init__(self, c1: Card, a1: float, c2: Card, a2: float):
        self.c1 = c1
        self.a1 = a1
        self.c2 = c2
        self.a2 = a2

    def measure(self):
        qc = QuantumCircuit(1)
        qc.initialize([self.a1, self.a2], 0)
        qc.measure_all()
        sim = AerSimulator()
        tqc = transpile(qc, sim)
        res = sim.run(tqc, shots=1).result().get_counts()
        if '0' in res:
            self.a1 = 1
            self.a2 = 0
            return self.c1
        self.a1 = 0
        self.a2 = 1
        return self.c2

        # Alternative probabilistic approach without quantum simulation
        '''
        if random.random() < self.a1 ** 2:
            self.a1 = 1
            self.a2 = 0
            return self.c1
        self.a1 = 0
        self.a2 = 1
        return self.c2
        '''
    
#TEST FOR THE PROBABILISTIC APPROACH
""" 
counter = 0
n_tests = 10000
for _ in range(n_tests):
    qcard = QCard(Card('A', 'Hearts'), 1/2, Card('K', 'Spades'), sqrt(3)/2)
    if qcard.measure().rank == 'A':
        counter += 1
print(counter*100/n_tests, "% A Hearts, ", (n_tests-counter)*100/n_tests, "% K Spades") 
"""
# TEST FOR THE QUANTUM MEASUREMENT
'''
qcard = QCard(Card('A', 'Hearts'), 1/2, Card('K', 'Spades'), sqrt(3)/2)
card = qcard.measure()
print(f"Measured card: {card.rank} of {card.suit}") 

counter = 0
n_tests = 100
for _ in range(n_tests):
    qcard = QCard(Card('A', 'Hearts'), 1/2, Card('K', 'Spades'), sqrt(3)/2)
    if qcard.measure().rank == 'A':
        counter += 1
print(counter*100/n_tests, "% A Hearts, ", (n_tests-counter)*100/n_tests, "% K Spades") 
'''



class QDeck:
    def draw(self) -> QCard:
        rank1 = random.choice(['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'])
        suit1 = random.choice(['Hearts', 'Diamonds', 'Clubs', 'Spades'])
        rank2 = random.choice(['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'])
        suit2 = random.choice(['Hearts', 'Diamonds', 'Clubs', 'Spades'])
        a1 = random.random()
        a2 = sqrt(1 - a1**2)
        qcard = QCard(Card(rank1, suit1), a1, Card(rank2, suit2), a2)
        return qcard


#TEST FOR QDECK
'''
qdeck = QDeck()
qcard = qdeck.draw()
print(f"Card 1: {qcard.c1.rank} of {qcard.c1.suit} with amplitude {qcard.a1}")
print(f"Card 2: {qcard.c2.rank} of {qcard.c2.suit} with amplitude {qcard.a2}")
measured_card = qcard.measure()
print(f"Measured card: {measured_card.rank} of {measured_card.suit}")
'''


class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def best_value(self):
        if any(isinstance(card, QCard) for card in self.cards):
            raise ValueError("Cannot compute best value with unmeasured quantum cards.")
        # Calculate the best total value of the hand, considering Aces as 1 or 11
        total = sum(card.value() for card in self.cards)
        aces = sum(1 for card in self.cards if card.rank == 'A')
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    def is_blackjack(self):
        if any(isinstance(card, QCard) for card in self.cards):
            raise ValueError("Cannot compute blackjack with unmeasured quantum cards.")
        return len(self.cards) == 2 and self.best_value() == 21

    def is_bust(self):
        if any(isinstance(card, QCard) for card in self.cards):
            raise ValueError("Cannot compute bust with unmeasured quantum cards.")
        return self.best_value() > 21

    def measure_all(self):
        measured_cards = []
        for qcard in self.cards:
            measured_cards.append(qcard.measure())
        self.cards = measured_cards
        return measured_cards
    
#TEST FOR HAND
'''
qdeck = QDeck()
hand = Hand()
hand.add_card(qdeck.draw())
hand.add_card(qdeck.draw())
print("Cards in hand (before measurement):")
for qcard in hand.cards:
    print(f"Card 1: {qcard.c1.rank} of {qcard.c1.suit} with amplitude {qcard.a1}")
    print(f"Card 2: {qcard.c2.rank} of {qcard.c2.suit} with amplitude {qcard.a2}\n")
measured_cards = hand.measure_all()
for card in measured_cards:
    print(f"Measured card: {card.rank} of {card.suit}")
'''


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
        self.qdeck = QDeck()
        self.deck = Deck()
        self.deck.shuffle()
        self.player = Player("Player")
        self.dealer = Dealer("Dealer")

    def deal_initial(self):
        for _ in range(2):
            card = self.player.draw(self.qdeck)
            print(f"{self.player.name} drew {card.c1.rank} of {card.c1.suit} with amplitude {card.a1} and {card.c2.rank} of {card.c2.suit} with amplitude {card.a2}.")
            self.dealer.draw(self.deck)
        print(f"{self.dealer.name}'s visible card: {self.dealer.hand.cards[0].rank} of {self.dealer.hand.cards[0].suit}")

    def player_turn(self):
        action = self.player.decide()
        while action == 'hit':
            card = self.player.draw(self.qdeck)
            print(f"{self.player.name} drew {card.c1.rank} of {card.c1.suit} with amplitude {card.a1} and {card.c2.rank} of {card.c2.suit} with amplitude {card.a2}.")
            action = self.player.decide()
        # Player stands
        print(f"{self.player.name} stands. Now measuring hand...")
        measured_cards = self.player.hand.measure_all()
        for card in measured_cards:
            print(f"Measured card: {card.rank} of {card.suit}")
        print(f"{self.player.name}'s hand value: {self.player.hand.best_value()}")
        if self.player.hand.is_bust():
            print(f"{self.player.name} busts with value {self.player.hand.best_value()}!")

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
        self.play_round()
        self.determine_winner()

game = Game()
game.start()