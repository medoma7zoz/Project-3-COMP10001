#Project 3, Whistful Hearts
#Knowledge of game play required to understand code assumptions

#-----------------------------------------------------------------------------#

#determine which card in a set is 'higher'
#Use ordered string of card values highest to lowest to determine higher
#valued cards
def hierarchy(possibles, cardset='AKQJ098765432'):
    #search for each value in cards of cardset
    #terminate as soon as value is found as orderd descending
    for division in cardset:
        for card in possibles:
            if card[0] == division:
                return(card)
            
#-----------------------------------------------------------------------------#
            
#determining winning card in trick
def winning_card(cardlist, prev_tricks, deck_top):
    possibles = []
    minilist = []
    #check for game phase, assign trump accordingly
    if len(prev_tricks) > 3:
        trump = cardlist[0][1]
    else:
        trump = deck_top[0][1]
    #determine trump cards, if any
    for card in cardlist:
        if trump in card:
            possibles += [card]
    #if trump cards are played determine winning trump
    if possibles != []:
        return(hierarchy(possibles))
    else:
    #given no trumps played, check for follow suit (phase differentiates
    # between trump and follow suit)
    #for cards that follow suit determine highest ranking, i.e winner
        for card in cardlist:
            if card[1] == cardlist[0][1]:
                minilist += [card]
        if minilist != []:
            return(hierarchy(minilist))
        else:
            return(None)

#-----------------------------------------------------------------------------#

#determine if hearts has been broken
def is_broken_hearts(prev_tricks, curr_trick = ()):
    #check for game phase, if phase 1, hearts can't have been broken yet
    if len(prev_tricks) <=3:
        return(False)
    #Check if hearts has been played yet in game
    #if hearts has been played then this constitutes a break
    for trick in prev_tricks[3:]:
        for card in trick:
            if card[1] == 'H':
                return(True)
    for card in curr_trick:
        if card[1] == 'H':
            return(True)
    return(False)

#-----------------------------------------------------------------------------#

#determine if move is allowed
def is_valid_play(play, curr_trick, hand, prev_tricks, broken=is_broken_hearts):
    suit = play[1]
    #determine follow suit for trick
    if len(curr_trick) >= 1:
        preferred = curr_trick[0][1] 
    else:
        preferred = suit
    #check for membership in hand
    if play not in hand:
        return(False)
    #checking validity for phase 1 plays
    if len(prev_tricks) <3:
    #if not following suit, check that no other cards in hand follow suit
        if suit != preferred:
            for card in hand:
                if preferred in card:
                    return(False)
    #checking validity for phase 2 plays
    else:
        #check for leading heart
        if curr_trick == ():
            if suit == 'H':
        #if leading heart, check that hearts is broken previously
        #Or that no other suit is held in hand
                if not broken(prev_tricks, curr_trick):
                    for card in hand:
                        if card[1] != 'H':
                            return(False)
        #Check for follow suit
        else:
            if suit != preferred:
                for card in hand:
                    if preferred in card:
                               return(False)
    return(True)

#-----------------------------------------------------------------------------#
#determine consecutive play order from previous player ID
def next_player(lead):
    if lead == 1:
        lead = 2
    elif lead == 2:
        lead = 3
    elif lead == 3:
        lead = 4
    elif lead == 4:
        lead = 1
    return(lead)
    
#-----------------------------------------------------------------------------#
                  
#To create tally of game scores to date
def score_game(tricks, deck_top):
    from collections import defaultdict
    points = defaultdict(int)
    p1list = [[]]
    p2list = [[]]
    if len(tricks) > 3:
        phase1 = tricks[:3]
        phase2 = tricks[3:]
    #points can only be earned in phase 2, if no phase 2, no points possible
    else:
       return( (0,0,0,0) )
    
    #keep track of who played what, phase 1
    #initial play order determined
    for play in range(len(phase1[0])):
        p1list[0] += [(phase1[0][play], play +1)]
    #Progressive play order determined based on trick wins
    #Assign player numbers to tuples based on clockwise gameplay and
    #previous trick winner
    for play in range(1,len(phase1)):
        winner = winning_card(phase1[play-1], tricks[:play-1], deck_top)
        for player in p1list[play-1]:
            if player[0] == winner:
                lead = player[1]
        p1list += [[]]
        for card in range(len(phase1[play])):
            p1list[play] += [(phase1[play][card], lead)]
            lead = next_player(lead)
            
    #keep track of who played what, phase 2, with respect to phase 1           
    winner = winning_card(phase1[-1], tricks[:3], deck_top)
    for player in p1list[-1]:
            if player[0] == winner:
                lead = player[1]
    #initial play order as for first trick of phase 2 with respect to phase 1              
    for play in range(len(phase2[0])):
        p2list[0] += [(phase2[0][play], lead)]
        lead = next_player(lead)
                
    #progressive play order recorded based on trick wins
     #Assign player numbers to tuples based on clockwise gameplay and
    #previous trick winner
    for play in range(1, len(phase2)):
        winner = winning_card(phase2[play-1], tricks[:4 + play], deck_top)
        for player in p2list[play - 1]:
            if player[0] == winner:
                lead = player[1]
                
        p2list += [[]]
              
        for card in range(len(phase2[play])):
            p2list[play] += [(phase2[play][card], lead)]
            lead = next_player(lead)
                    
    #point accumlation       
    for trick in range(len(p2list)-1):
        for play in p2list[trick]:
            if play[0] == 'QS':
    #Allocate points to winnder of round, i.e first player in next trick
                points[p2list[trick +1 ][0][1]] += 13
            elif 'H' in play[0]:
                points[p2list[trick + 1][0][1]] += 1
                
    #Determine value of points earned in final round
    finalwin = winning_card(phase2[-1], phase2[:len(phase2) -1], deck_top)
    
    for play in p2list[-1]:
    #Allocate points to winnder of final round
        if play[0] == finalwin:
            for card in phase2[-1]:
                if card == 'QS':
                    points[play[1]] += 13
                elif 'H' in card:
                    points[play[1]] += 1

    #Check for play of all point-bearing cards and determine shooting for moon
    heartcount = 0
    for trick in tricks:
        for card in trick:
            if 'H' in card or card == 'QS':
                heartcount += 1
    #Shooting for moon only occurs if one player holds all points
    zerocount = 0
    for player in (1,2,3,4):
        if points[player] == 0:
            zerocount += 1
    #if less than 3 players have 0, havent shot the moon        
    if zerocount == 3 and heartcount == 14:
        for player in points:
            if points[player] != 0:
                points[player] = points[player] - 2*points[player]
                
    return((points[1], points[2], points[3], points[4] ))

#-----------------------------------------------------------------------------#

#determine status of player_data and edit accordingly
def player_data_edit(player_data, curr_trick, hand, deck_top, prev_tricks):
    from collections import defaultdict
    #player_data will be used to card count by keeping track of cards not played
    #determine whether available or not and enact contingency to create
    #substitute record from available data.
    if player_data == None:
        player_data = defaultdict(list)
        #construct initial cards present for each suit
        for suit in 'HSDC':
            for division in 'AKQJ098765432':
                player_data[suit] += division
        #remove played cards from those listed
        for card in curr_trick + hand + deck_top:
            try:
                player_data[card[1]].remove(card[0])
            except ValueError:
                pass
        #remove cards currently in play from those listed
        for trick in prev_tricks:
            for card in trick:
                try:
                    player_data[card[1]].remove(card[0])
                except ValueError:
                    pass
                        
   #Update existing player_data for most recent trick
    else:
        for card in curr_trick + hand + deck_top + list(prev_tricks[-1]):
            try:
                player_data[card[1]].remove(card[0])
            except ValueError:
                pass
    return(player_data)

#-----------------------------------------------------------------------------#

#card to determine if valid plays are lower compared to other cards
#for comparison of commenced trick
def lowest_play(curr_trick, valid_cards, prev_tricks, deck_top, valid_copy):
    #compare valid plays to cards in play
    for card in valid_copy:
        if winning_card(curr_trick + [card,],prev_tricks,
                        deck_top) == card:
                     valid_copy.remove(card)
    #if list of losing cards determined, play from this list
    if valid_copy != []:
        play = valid_copy[0]
    #if no cards satisfy, play any
    else:
        play = valid_cards[0]
    return(play)

#-----------------------------------------------------------------------------#

#determine lead card that will ensure losing of trick by comparing to cards
#still in play
def lose_trick(valid_cards, prev_tricks, deck_top, player_data):
    from collections import defaultdict
    p = prev_tricks
    t = deck_top
    possible_suits = defaultdict(list) #cards still in play
    valid_copy = valid_cards + [] #create identical list to avoid altering
                                  #original list
    #create lists of card strings matching format of input
    for suit in 'HSDC':
        for division in player_data[suit]:
            cardleft = division + suit
            possible_suits[suit] += [cardleft]
    #remove cards that would win trick from consideration
    for card in valid_cards:
        cardlist = possible_suits[card[1]]+[card]
        if card == winning_card(cardlist, p, t):
                    valid_copy.remove(card)
    #if some cards deemed losers, select play from resultant list
    if valid_copy != []:
        play = valid_copy[0]
    #if no cards deemed losers, play any card
    else:
        play = valid_cards[0]
    return(play)

#-----------------------------------------------------------------------------#
        
#Determine next card to play
#Strategy split into to stages, phase 1 and 2. Phase 1 strategy is to eliminate
#as many point bearing cards as possible and be indiferent to winning trumps.
#This is to make points more dangerous in phase 2 and disadvantage other players
#Phase 2 strategy is to play hearts over all other valid cards with preference
#to low values in order to provide points to other players. Preference to lose
#tricks, to be achieved with play_data card counting.
def play(curr_trick, hand, prev_tricks, deck_top, is_valid= is_valid_play,
         score=score_game, player_data=None, suppress_player_data=False):

    hearts_list = [] #list to compare valid heart plays
    valid_cards = [] #list of vaild plays

    
    #find cards that would be valid plays held in hand
    for card in hand:
        if is_valid(card, curr_trick, hand, prev_tricks):
            valid_cards.append(card)

    #determine hearts present in valid_cards and record in hearts_list
    for card in valid_cards:
        if 'H' in card:
            hearts_list.append(card)
            
    #update or create player_data
    player_data = player_data_edit(player_data, list(curr_trick), hand,
                                   deck_top, prev_tricks)
                          
    #determine phase of gameplay
    #Determine if only one valid play available and terminate accordingly
    if len(valid_cards) == 1:
        nextmove = valid_cards[0]

    #play decisions for phase 2
    elif len(prev_tricks) >= 3: #condition of phase 2
        #if leading pick card likely to lose
        if len(curr_trick) < 1:
            nextmove = lose_trick(valid_cards, prev_tricks, deck_top,
                                  player_data)
        #Check if safe to dispose of QS
        elif 'QS' in valid_cards and 'QS' != winning_card(curr_trick + ['QS',],
                                                         prev_tricks,deck_top):
          nextmove = 'QS'
        #Given hearts are valid, determine if safe to dispose
        elif hearts_list != []:
        #if trump suit not hearts play highest as guaranteed loss
            if 'H' not in curr_trick[0]:
                nextmove = hierarchy(hearts_list)
        #if hearts already in playaim to lose so as not to gain points
            else:
                nextmove = lowest_play(curr_trick, hearts_list, prev_tricks,
                                   deck_top, hearts_list)
        #for all other plays, try to lose trick by playing 'low' card
        else:
             nextmove = lowest_play(curr_trick, valid_cards, prev_tricks,
                                   deck_top, valid_cards)     
    #play decisions for phase 1       
    else :
    #immediately dispose of QS if valid
     if 'QS' in valid_cards:
         nextmove = 'QS'
    #dispose of all high value hearts if posible
     elif hearts_list != []:
         nextmove = hierarchy(hearts_list)
    #do not win tricks with high value cards up for grabs
     elif 'AKQJ0' in deck_top[-1]:
         #if not leading trick compare to played cards
         if len(curr_trick) >= 1:
             nextmove = lowest_play(curr_trick, valid_cards, prev_trick,
                                    deck_top, valid_cards)
        #if leading, compare to possibles
        #determine which cards would ensure losing the trick
         else:
            nextmove = lose_trick(valid_cards, prev_tricks, deck_top,
                                  player_data)
     else:
         nextmove = valid_cards[0]                           
                 
    #determine return values based on suppression of player_data
    if suppress_player_data:
        return(nextmove)
    else:
        return((nextmove, player_data))
            
#-----------------------------------------------------------------------------#                      

def get_winner_score(trick, round_id, deck_top):
    prev_trick = []
    trick_score = 0
    for tricknum in range(round_id):
        prev_trick += [1]
    if round_id > 3:
        for card in trick:
            if 'H' in card:
                trick_score += 1
            if card == 'QS':
                trick_score += 13
    wincard = winning_card(trick, prev_trick, deck_top)
    ID = trick.index(wincard)
    return( ID, trick_score)

#-----------------------------------------------------------------------------#

def predict_score(hand):
    heart_count = []
    low_hearts = 0
    non_hearts = 0
    score = 0
    #if hearts in hand, score increases by relevant percentage
    #if low value hearts, score decreases by relevant percentage
    #for every non heart decrease score by relevant percentage
    for card in hand:
        if 'H' in card:
            heart_list += card[0]
            if card[0] not in 'AKQJ0':
                low_hearts += 1
        else:
            non_hearts += 1

    return(int(((len(heart_list)/13)-(low_hearts/13)-(non_hearts/13)
                )*26))
