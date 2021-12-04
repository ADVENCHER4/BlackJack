from random import choice


class Player():
    def __init__(self, name):
        self.name = name
        self.balance = 0

    def get_choice(self):
        choice = input(f'{self.name}, give you a card?(y/n) ')
        return choice

    def add_card(self, card_value):
        self.balance += card_value

    def print_balance(self):
        print(f'{self.name}`s balance is {self.balance} \n')


class Croupier():
    def __init__(self):
        self.balance = 0
        self.hidden_card_value = 0

    def add_card(self, card_value):
        if self.hidden_card_value == 0:
            self.hidden_card_value = card_value
        else:
            self.balance += card_value

    def print_hidden_balance(self):
        print(f'Croupier`s balance is {self.balance} + ? \n')

    def ad_hidden_card(self):
        self.balance += self.hidden_card_value

    def print_balance(self):
        print(f'Croupier`s balance is {self.balance} \n')


class Game():
    CARD_VALUES = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
    num_players = 0
    deck = []
    players = []

    def __init__(self):
        self.croupier = Croupier()
        self.start()

    def start(self):
        try:
            num_decks = self.starting_data()
            self.init_players()
        except(ValueError):
            return
        self.deck = self.CARD_VALUES * num_decks
        self.starting_card()
        self.show_start_balance()
        self.loop()

    def starting_data(self):
        self.num_players = int(input('Number of players: '))
        if(self.num_players > 5):
            print('Too much players \n')
            raise ValueError
        num_decks = int(input('Number of decks: '))
        print('')   # make indent
        return num_decks

    def init_players(self):
        for i in range(self.num_players):
            name = input(f'Name of {i + 1} player: ')
            if not name:
                raise ValueError
            self.players.append(Player(name))
        print('')   # make indent

    def starting_card(self):
        for _ in range(2):
            for player in self.players:
                card_value = choice(self.deck)
                player.add_card(card_value)
            card_value = choice(self.deck)
            self.croupier.add_card(card_value)

    def show_start_balance(self):
        for player in self.players:
            player.print_balance()
        self.croupier.print_hidden_balance()

    def end(self, winners):
        if winners:
            print(f'Winners are {", ".join(winners.name)}')
        else:
            print('Croupier win')

    def find_winners(self):
        winners = []
        for player in self.players:
            if player.balance > self.croupier.balance and player.balance <= 21:
                winners.append(player.name)
        return winners
        
    def loop(self):
        players_in_game = list(self.players)
        while not len(players_in_game) == 0:
            for player in players_in_game:
                if player.balance >= 21:
                    players_in_game.remove(player)
                    continue
                player_choice = player.get_choice()
                if player_choice == 'y':
                    card_value = choice(self.deck)
                    player.add_card(card_value)
                elif player_choice == 'n':
                    players_in_game.remove(player)
                player.print_balance()

        self.croupier.add_hidden_card()
        self.croupier.print_balance()

        while self.croupier.balance < 17:
            card_value = choice(self.deck)
            self.croupier.add_card(card_value)
            self.croupier.print_balance()

        winners = self.find_winners()    # names of winners
        self.end(winners)


if __name__ == '__main__':
    Game()
