from random import choice


class Player:
    name: str
    balance: int = 0

    def __init__(self, name: str) -> None:
        self.name = name

    def get_choice(self) -> str:
        player_choice: str = input(f'{self.name}, give you a card?(y/n) ')
        return player_choice

    def add_card(self, card_value: int) -> None:
        self.balance += card_value

    def print_balance(self) -> None:
        print(f'{self.name}`s balance is {self.balance} \n')


class Croupier:
    balance: int = 0
    hidden_card_value: int = 0

    def add_card(self, card_value: int) -> None:
        if self.hidden_card_value == 0:
            self.hidden_card_value = card_value
        else:
            self.balance += card_value

    def print_hidden_balance(self) -> None:
        print(f'Croupier`s balance is {self.balance} + ? \n')

    def add_hidden_card(self):
        self.balance += self.hidden_card_value

    def print_balance(self) -> None:
        print(f'Croupier`s balance is {self.balance} \n')


class Game:
    CARD_VALUES: list[int] = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
    num_players: int = 0
    deck: list[int] = []
    players: list[Player] = []
    croupier: Croupier

    def __init__(self) -> None:
        self.croupier = Croupier()
        self.start()

    def start(self):
        try:
            num_decks: int = self.starting_data()
            self.init_players()
        except ValueError:
            return
        self.deck = self.CARD_VALUES * num_decks
        self.starting_card()
        self.show_start_balance()
        self.loop()

    def starting_data(self) -> int:
        self.num_players = int(input('Number of players: '))
        if self.num_players > 5:
            print('Too much players \n')
            raise ValueError
        num_decks: int = int(input('Number of decks: '))
        print('')  # make indent
        return num_decks

    def init_players(self) -> None:
        for i in range(self.num_players):
            name: str = input(f'Name of {i + 1} player: ')
            if not name:
                raise ValueError
            self.players.append(Player(name))
        print('')  # make indent

    def starting_card(self) -> None:
        for _ in range(2):
            for player in self.players:
                card_value: int = choice(self.deck)
                player.add_card(card_value)
            card_value: int = choice(self.deck)
            self.croupier.add_card(card_value)

    def show_start_balance(self) -> None:
        for player in self.players:
            player.print_balance()
        self.croupier.print_hidden_balance()

    def end(self, winners: list[str]) -> None:
        if winners:
            print(f'Winners are {", ".join(winners)}')
        elif not winners and self.croupier.balance <= 21:
            print('Croupier win')
        else:
            print('No winners')

    def find_winners(self) -> list:
        winners: list[str] = []
        for player in self.players:
            if self.croupier.balance < player.balance <= 21:
                winners.append(player.name)
        return winners

    def loop(self) -> None:
        players_in_game: list[Player] = list(self.players)
        while not len(players_in_game) == 0:
            for player in players_in_game:
                if player.balance >= 21:
                    players_in_game.remove(player)
                    continue
                player_choice: str = player.get_choice()
                if player_choice == 'y':
                    card_value: int = choice(self.deck)
                    player.add_card(card_value)
                elif player_choice == 'n':
                    players_in_game.remove(player)
                player.print_balance()

        self.croupier.add_hidden_card()
        self.croupier.print_balance()

        while self.croupier.balance < 17:
            card_value: int = choice(self.deck)
            self.croupier.add_card(card_value)
            self.croupier.print_balance()

        winners: list[str] = self.find_winners()  # names of winners
        self.end(winners)


if __name__ == '__main__':
    Game()
