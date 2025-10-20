import random
import itertools
from terminal_playing_cards import Card as ViewCard, View
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from math import sqrt, acos

from model.model import Card, Deck

class QCard:
    def __init__(self, c1: Card, a1: float, c2: Card, a2: float):
        self.c1 = c1
        self.a1 = a1
        self.c2 = c2
        self.a2 = a2

    def measure(self):
        qc = QuantumCircuit(1)
        # qc.initialize([self.a1, self.a2], 0)
        qc.ry(2*acos(self.a1), 0)
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
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        cards = list(itertools.product(ranks, suits))
        random.shuffle(cards)
        rank1, suit1 = cards.pop()
        rank2, suit2 = cards.pop()
        p1 = random.random()
        p2 = 1 - p1
        a1 = sqrt(p1)
        a2 = sqrt(p2)
        qcard = QCard(Card(rank1, suit1), a1, Card(rank2, suit2), a2)
        return qcard


#TEST FOR QDECK
'''
qdeck = QDeck()
qcard = qdeck.draw()
print(f"Card 1: {qcard.c1.rank} of {qcard.c1.suit} with probability {qcard.a1**2}")
print(f"Card 2: {qcard.c2.rank} of {qcard.c2.suit} with probability {qcard.a2**2}")
measured_card = qcard.measure()
print(f"Measured card: {measured_card.rank} of {measured_card.suit}")
'''


class Hand:
    def __init__(self):
        self.cards = []

    def clear_hand(self):
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

    def is_quantum_bust(self):
        min = 0
        for card in self.cards:
            if isinstance(card, QCard):
                r1 = int(card.c1.rank) if card.c1.rank not in ['A', 'J', 'Q', 'K'] else 1 if card.c1.rank == 'A' else 10
                r2 = int(card.c2.rank) if card.c2.rank not in ['A', 'J', 'Q', 'K'] else 1 if card.c2.rank == 'A' else 10
                if r1 <= r2:
                    min += r1
                else:
                    min += r2
            else:
                min += card.value()
        return min > 21

    def measure_all(self):
        measured_cards = []
        for qcard in self.cards:
            if isinstance(qcard, QCard):
                measured_cards.append(qcard.measure())
            else:
                measured_cards.append(qcard)
        self.cards = measured_cards
        return measured_cards
    
    def entangle_and_measure(self, card1: int, card2: int):
        if card1 < 0 or card1 >= len(self.cards) or card2 < 0 or card2 >= len(self.cards):
            raise IndexError("Card index out of range.")
        if not isinstance(self.cards[card1], QCard) or not isinstance(self.cards[card2], QCard):
            raise ValueError("Both cards must be quantum cards to entangle.")
        qc = QuantumCircuit(2)
        # qc.initialize([self.cards[card1].a1, self.cards[card1].a2], 0)
        # qc.initialize([self.cards[card2].a1, self.cards[card2].a2], 1)
        qc.ry(2*acos(self.cards[card1].a1), 0)
        qc.ry(2*acos(self.cards[card2].a1), 1)
        qc.cx(0, 1)  # Entangling operation
        qc.measure_all()
        sim = AerSimulator()
        tqc = transpile(qc, sim)
        res = sim.run(tqc, shots=1).result().get_counts()
        if list(res.keys())[0].startswith('0'):
            self.cards[card1] = self.cards[card1].c1
        else:
            self.cards[card1] = self.cards[card1].c2
        if list(res.keys())[0].endswith('0'):
            self.cards[card2] = self.cards[card2].c1
        else:
            self.cards[card2] = self.cards[card2].c2
        return self.measure_all()

#TEST FOR HAND
'''
qdeck = QDeck()
hand = Hand()
hand.add_card(qdeck.draw())
hand.add_card(qdeck.draw())
print("Cards in hand (before measurement):")
for qcard in hand.cards:
    print(f"Card 1: {qcard.c1.rank} of {qcard.c1.suit} with probability {qcard.a1**2}")
    print(f"Card 2: {qcard.c2.rank} of {qcard.c2.suit} with probability {qcard.a2**2}\n")
measured_cards = hand.entangle_and_measure(0,1)
for card in measured_cards:
    print(f"Measured card: {card.rank} of {card.suit}")
'''


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Hand()
        self.entanglement_tokens = 1  # Number of entanglement tokens available

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
    
    def decide_entangle(self):
        if self.entanglement_tokens <= 0:
            print("No entanglement tokens left.")
            return 'no'
        print(f"You have {self.entanglement_tokens} entanglement token(s) left.")
        action = input(f"{self.name}, do you want to entangle two quantum cards? (yes/no) ").strip().lower()
        while action not in ['yes', 'no']:
            print("Invalid input. Please enter 'yes' or 'no'.")
            action = input(f"{self.name}, do you want to entangle two quantum cards? (yes/no) ").strip().lower()
        if action == 'yes':
            self.entanglement_tokens -= 1
        return action

class Dealer(Player):
    def play(self, deck):
        # Dealer keeps hitting until 17 or higher
        while self.hand.best_value() < 17:
            self.draw(deck)
            print(f"{self.name} drew a card.")





class QGame:
    def __init__(self, money = 10):
        self.qdeck = QDeck()
        self.deck = Deck()
        self.deck.shuffle()
        self.money = money
        self.player = Player("Player")
        self.dealer = Dealer("Dealer")

    def deal_initial(self):
        print(f"\n=== PLAYER ===\n")
        for _ in range(2):
            card = self.player.draw(self.qdeck)
            viewCard1 = ViewCard(str(card.c1.rank), card.c1.suit)
            viewCard2 = ViewCard(str(card.c2.rank), card.c2.suit)
            print(f"{self.player.name} drew: {View([viewCard1, viewCard2])} with probability {card.a1**2} and {card.a2**2} respectively")
            self.dealer.draw(self.deck)
        print(f"\n=== DEALER ===\n")
        print(self.dealer.hand.cards[0].rank, self.dealer.hand.cards[0].suit)
        viewCardDealer = ViewCard(str(self.dealer.hand.cards[0].rank), self.dealer.hand.cards[0].suit)
        print(f"{self.dealer.name}'s visible card: {View([viewCardDealer])}")

    def player_turn(self):
        action = self.player.decide()
        while action == 'hit':
            card = self.player.draw(self.qdeck)
            viewCard1 = ViewCard(str(card.c1.rank), card.c1.suit)
            viewCard2 = ViewCard(str(card.c2.rank), card.c2.suit)
            print(f"{self.player.name} drew: {View([viewCard1, viewCard2])} with probability {card.a1**2} and {card.a2**2} respectively")
            if self.player.hand.is_quantum_bust():
                print(f"{self.player.name} is in a quantum bust state! Must stand and measure now.")
                action = 'stand'
                break
            action = self.player.decide()
        # Player stands
        action_entangle = self.player.decide_entangle()
        if action_entangle == 'yes':
            if len(self.player.hand.cards) < 2:
                print("Not enough cards to entangle.")
            else:
                try:
                    idx1 = int(input(f"Enter the index of the first quantum card to entangle (1 to {len(self.player.hand.cards)}): "))
                    idx2 = int(input(f"Enter the index of the second quantum card to entangle (1 to {len(self.player.hand.cards)}): "))
                    print(f"{self.player.name} stands and entangles the cards. Now measuring hand...")
                    measured_cards = self.player.hand.entangle_and_measure(idx1-1, idx2-1)
                except (IndexError, ValueError) as e:
                    print(f"Error during entanglement: {e}")
        else:
            print(f"{self.player.name} stands. Now measuring hand...")
            measured_cards = self.player.hand.measure_all()
        measured_viewCards = []
        for card in measured_cards:
            measured_viewCards.append(ViewCard(str(card.rank), card.suit))
        print(f"{self.player.name}'s {View(measured_viewCards)} with hand value: {self.player.hand.best_value()}")
        if self.player.hand.is_bust():
            print(f"{self.player.name} busts with value {self.player.hand.best_value()}!")

    def dealer_turn(self):
        self.dealer.play(self.deck)
        dealer_cards = []
        for card in self.dealer.hand.cards:
            dealer_cards.append(ViewCard(str(card.rank), card.suit))
        print(f"{self.dealer.name} stands: {View(dealer_cards)} with value {self.dealer.hand.best_value()}.")
    
    def determine_winner(self):
        player_value = self.player.hand.best_value()
        dealer_value = self.dealer.hand.best_value()

        if self.player.hand.is_bust():
            return self.tunneling(player_value)

        elif self.dealer.hand.is_bust():
            self.player.entanglement_tokens += 1
            print("Player wins! Dealer busted.")
            print(f"{self.player.name} now has {self.player.entanglement_tokens} entanglement token(s).")
            return "player"
        elif player_value > dealer_value:
            self.player.entanglement_tokens += 1
            print("Player wins!")
            print(f"{self.player.name} now has {self.player.entanglement_tokens} entanglement token(s).")
            return "player"
        elif dealer_value > player_value:
            print("Dealer wins!")
            return "dealer"
        else:
            print("It's a tie!")
            return "tie"

    def play_round(self):
        self.player_turn()
        if not self.player.hand.is_bust():
            self.dealer_turn()

    def reset(self):
        self.qdeck = QDeck()
        self.deck.shuffle()
        self.player.hand = Hand()
        self.dealer.hand = Hand()

    def start(self):
        bet = int(input("How much money do you want to bet: "))
        while not game.money >= bet:
            bet = int(input("You dont have that amount of money, how much do you want to be: "))
        self.deal_initial()
        self.play_round()
        winner = self.determine_winner()
        self.calculate_money(winner, bet)
        # Optionally, ask to play again
        again = input("Do you want to play again? (yes/no) ").strip().lower()
        if again == 'yes':
            self.reset()
            self.start()
        else:
            print("Thanks for playing!")

    def initialize_game(self):
        print("Welcome to Quantum Blackjack!")
        money = int(input("Enter the amount of money that you will play with: "))
        if money >= 0:
            self.money = money
            print(f"You have {self.money} to play with.")
        else:
            print("Invalid amount. Starting with $10.")
            self.money = 10
            print(f"You have {self.money} to play with.")

    def calculate_money(self, winner, bet):
        if winner == "player":
            self.money += bet
            print(f"You won this round! You now have {self.money}.")
        elif winner == "dealer":
            self.money -= bet
            print(f"You lost this round! You now have {self.money}.")
        else:
            print(f"It's a tie! You still have {self.money}.")
        if self.money <= 0:
            print("You are out of money! Game over.")
            exit()

    def tunneling(self, hand: int, p : float = 0.2 ):
        print("You busted! You are at", hand, "tunneling is activated.")
        n_of_walls = hand - 21
        current_hand = hand

        for i in range(n_of_walls):
            if random.random() <= p:
                print(f"Tunneled through wall {i+1}: {current_hand} → {current_hand - 1}")
                current_hand -= 1
            else:
                print(f"Stopped at wall {i+1}. Tunneling failed!.")
                break
        if current_hand == 21:
            print("You tunneled exactly to 21! Congrats. You win!")
            return "player"
        else:
            print("You busted! Dealer wins.")
            return "dealer"

game = QGame()
game.initialize_game()
game.start()
