import random
# a tuple for the suits and ranks for a Card
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
# a dictionary for the value of a Card
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

#Defining Card class
class Card:
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return self.rank + ' of ' + self.suit

#Defining Deck class with functions for shuffling and dealing the deck
class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list#
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))
            
    def shuffle(self):
        random.shuffle(self.deck) # random.shuffle will change the position of each element in the list
        
    def deal(self):
        single_card = self.deck.pop() # this will remove the index item from the list and also return it.
        return single_card

#Defining Hand class with functions for adding card, 
# making visible dealer value and adjusting for ace

class Hand:
    def __init__(self):
        self.cards = []  # List of cards retrieved from the deck. Starts empty.
        self.value = 0  
        self.value_visible = 0
        # Attribute tracking amount of aces so we can change value of hand if over 21 and has an ace
        self.aces = 0
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1
    
    def visible_dealer(self):
        self.value_visible = self.value        

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1
            
#Defining Chips class with functions for winning, losing bet and if a natural occured in starting hand
class Chips:
    
    def __init__(self):
        self.total = 100  # This is how much chips the player will start with
        self.bet = 0 #
        
    def win_bet(self):
        self.total += self.bet # operator for adding bet to total
        
    def lose_bet(self):
        self.total -= self.bet # operator for subtracting bet from total

    def natural(self):
        #A natural win will give 150% of the initial bet but is rounded to nearest full number
        natural_win = round(self.bet+(self.bet/2))
        self.total += natural_win

        
# Function for taking bets. Makes sure that the input is an integer and that the bet is not more than total
def take_bet(chips):
    while True:
        try:
            chips.bet = int(input('How many chips would you like to bet?\n'))
        except ValueError:
            print("Sorry, a bet must be an integer!\n")
        else:
            if chips.bet > chips.total:
                print('Sorry, your bet cannot exceed {} \n'.format(chips.total))
            else:
                break      

# Function for adding a card to hand from top of deck, and will adjust for ace
def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

# Function for hitting the dealer of standing
def hit_or_stand(deck,hand):

    while True:
        try:
            x = input("Would you like to Hit or Stand? Enter 'h' or 's'\n")
        
            if x[0].lower() == 'h':
                hit(deck,hand)  # hit() function defined above
                return True # Will return True which keeps the player in playing loop

            elif x[0].lower() == 's':
                print("Player stands. Dealer is playing.")
                return False # Will end the playing loop proceeding to dealer hand check
            else:
                print("Must input 'h' or 's'\n")
                continue
            break
        except IndexError: # Makes sure that if pressed Enter without an input that program won't crash
            # because the if statement is saying x[0].lower()
            print("Must input 'h' or 's'\n")
    
# Function for checking if dealer and player total, after first cards are given to see if anyone has 21
def natural(chips, bet, dealer_value, player_value):
    if dealer_value == 21:
        if player_value == 21:
            print('Both dealer and player has 21!')
            return 'draw'
        else:
            print('Dealer has a natural and takes the players bet!')
            chips.lose_bet()
            return 'lose'
    elif player_value == 21:
        print("Player has a natural and wins 150% of the bet")        
        chips.natural()
        return 'win'

#Functions to display either some of dealers card or all
def show_some(player,dealer):
    # Will only show the value of the first card in dealer's hand
    print("\nDealer's hand value is approximately", dealer.value_visible)
    print("<Hidden Card>,",dealer.cards[0])
    print("\nPlayer's hand value is",player.value)
    print(*player.cards, sep= ', ', end='\n\n')
        
def show_all(player,dealer):
    print("\nDealer's hand value is", dealer.value)
    print(*dealer.cards, sep=", ")
    print("\nPlayer's hand value is",player.value)
    print(*player.cards, sep= ', ', end='\n\n')


# Main function for running the game recieves the player chips and boolean
def main(player_chips, playing):
    
    while True: 
        #Make a deck and shuffles it 
        deck = Deck()
        deck.shuffle()

        #Makes player hand and adds two cards and adjusts for aces in case player gets two aces.
        player_hand = Hand()
        player_hand.add_card(deck.deal())
        player_hand.add_card(deck.deal())
        player_hand.adjust_for_ace()

        #Makes dealer hand ands a card then adds the value to visible value and then adds another card.
        #Last also checks for aces in case dealer has two aces
        dealer_hand = Hand()
        dealer_hand.add_card(deck.deal())
        dealer_hand.visible_dealer()
        dealer_hand.add_card(deck.deal())
        dealer_hand.adjust_for_ace()

        # Prompt the Player for their bet
        take_bet(player_chips)

        # Show cards
        show_some(player_hand, dealer_hand) 

        #Checks for natural which will end this match if anyone or both has a natural. (21 value)
        check_natural = natural(player_chips, player_chips.bet, dealer_hand.value,player_hand.value)
        if check_natural == 'win':
            print('')
        elif check_natural == 'lose':
            print('')
        elif check_natural == 'draw':
            print('')
        else:
            #If no naturals the player will proceed with the game
            while playing: 
                
                # Will go to hit or stand function and return true or false to either stay in loop or end
                playing = hit_or_stand(deck, player_hand)
                
                # Show cards (but keep one dealer card hidden)
                show_some(player_hand,dealer_hand) 

                
                # If player's hand value exceeds 21, run player_busts() and break out of loop
                if player_hand.value >21:
                    print("Player busts!")
                    player_chips.lose_bet()
                    #player_busts(player_hand,dealer_hand,player_chips)

                    break
                # If player's hand value is equal to 21 the game proceeds to dealer
                if player_hand.value == 21:
                    playing = False

            # If Player hasn't busted, play Dealer's hand until Dealer reaches atleast 17
            if player_hand.value <= 21:
                
                while dealer_hand.value <17:
                    hit(deck, dealer_hand)
            
                # Show all cards
                show_all(player_hand,dealer_hand)
                
                # Run different winning scenarios
                if dealer_hand.value > 21:
                    print("Dealer busts!")
                    player_chips.win_bet()

                elif dealer_hand.value > player_hand.value:
                    print("Dealer wins!")
                    player_chips.lose_bet()

                elif dealer_hand.value < player_hand.value:
                    print("Player wins!")
                    player_chips.win_bet()

                else:
                    print("Dealer and Player tie! It's a push.")

        # If the player busted and has no more chips the program will shut down             
        if player_chips.total <= 0:
            print('...You lost...Thanks for playing!')
            break
        # Will show how much chips the player has left
        print("\nPlayers winnings stand at", player_chips.total)

        # Checking for IndexError if they user presses enter without an input
        # This will either continue the While loop or end the program
        try:
            new_game = input("would you like to play again? Enter 'y' or 'n'\n")
        except IndexError:
            new_game = " "
        if new_game[0].lower() == 'y':
            playing = True
            continue
        else:
            print('Thanks for playing!')
            break

# Will run this code is run from same .py file
if __name__ == '__main__':
    print("\nPython 2 Mandatory BlackJack Game.\n")

    # Making a new instance of the class Chips
    player_chips = Chips()
    # Starting the main game with two parameters
    main(player_chips, True)
