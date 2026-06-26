import random

def DrawCards(place: list, amount: int):
    for x in range(amount):
        place.append(pile.pop(0))

# Creates and shuffles pile.
pile = []
for i in ["D", "H", "C", "S"]:
    for x in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]:
        pile.append(i+x)
random.shuffle(pile)

print(pile)

visible_table = []
hidden_table = []

DrawCards(visible_table, 3)
DrawCards(hidden_table, 2)

print(f"Table: {visible_table}")
players = int(input("How many players?\n"))
match players:
    case 1:
        player_list = [player1]

# Establishes player1's deck.
player1 = []

# Draws a card from the pile for player1.
DrawCards(player1, 5)

# Player chooses a card and it goes on the bottom of the pile.
card = input("Card: ")
player1.remove(card)
pile.append(card)

print(pile)