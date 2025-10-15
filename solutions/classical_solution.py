from model.model import Deck, Hand, Card, Player, Dealer

class Game:
    def __init__(self, money = 100):
        self.deck = Deck()
        self.deck.shuffle()
        self.money = money
        self.player = Player("Player")
        self.dealer = Dealer("Dealer")

    def deal_initial(self):
        self.dealer.hand.clear_hand() # Clear hand to play multiple rounds
        self.player.hand.clear_hand() # Clear hand to play multiple rounds
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
            elif self.player.hand.best_value() == 21:
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
            return "dealer"
        elif self.dealer.hand.is_bust():
            print("Player wins! Dealer busted.")
            return "player"
        elif player_value > dealer_value:
            print("Player wins!")
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

    def initialize_game(self):
        print("Hello to Blackjack!")
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

    def start_round(self, bet = 0):
        self.deal_initial()
        if not self.player.hand.is_blackjack():
            self.play_round()
            winner = self.determine_winner()
            self.calculate_money(winner, bet)

game = Game()  # create a new game
game.initialize_game()

while True:
    if game.money > 0:
        bet = int(input("How much money do you want to bet?"))
        while not game.money >= bet:
            bet = int(input("You dont have that amount of money, how much do you want to bet?"))
        game.start_round(bet)
        answer = input("You have $" + str(game.money) + " left, do you want to play again? (yes/no)").lower()
        if answer != 'yes':
            print("Thank you for playing! The total amount of money you have is: $" + str(game.money))
            break
        print("\n--- New Round ---")