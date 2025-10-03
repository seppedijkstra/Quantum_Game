from model.model import Deck, Hand, Card, Player, Dealer

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