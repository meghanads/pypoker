#################################################
#			*POKER*
#	(No Limit Texas Hold'em Poker)
#
#	1.	People (code :))
#	2.	Probability
#	3.	Money
#
#
#	Positions:
#
#			1	2
#		6			3
#			5	4
#
#
#
#	Rank of hand:
#
#		One pair (low)
#		Two Pair
#		Three of Kind - set/trips
#		Straight - of any kinds
#		Flush	-	five cards of same suit
#		Full house	-	three of kind + pair
#		Four of Kind - 4 with same val
#		straight flush	-	
#		royal flush	(high)-	10-j-q-k-a
#
#
#	Terms:
#		dealer
#		small blind
#		big blind
#		hole cards	-	pair cards given to us(player)
#		flop - three cards face-up, can be used by any player at shutdown.
#		turn - forth card face-up
#		river - fifth card face-up
#		showdown- create best five-card hand possible
#
#
#
#
#	Actions:
#		1. Call	- match amount bet
#
#
#
#	decisions:
#	==========
#
#
#	Files:
#	======
#	inputf.txt	-	
#
#	deals_money.txt	-	
#
#	deal.txt	-	
#
#	outputf.txt	-	
#
#
#	Ref:	http://entertainment.howstuffworks.com/poker.htm
#			http://en.wikipedia.org/wiki/Texas_hold_'em

from math import *
import os
import os.path



# cost of call
coc = 0;

# projected size of pot
proj_sop = 0;

# win-rate
win_rate = coc*sqrt(proj_sop);

# calling decision
#call_dec = Enum('showdown','next_bet_round');

# decision
#decision = Enum('fold', 'call', 'raise');

# stages in game
NameStage = { 1 : 'Pre_Flop', 2 : 'Flop', 3 : 'Fourth_Street', 4 : 'Fifth_Street', 5 : 'Show_Down', 6 : 'NA'};
NumStage = { 'Pre_Flop' : 1, 'Flop' : 2, 'Fourth_Street' : 3, 'Fifth_Street' : 4 , 'Show_Down' : 5, 'NA' : 6};

# Rank of hand:
NumRank = {'high_card' : 1, 'one_pair' : 2, 'two_pairs' : 3, 'set' : 4, 'straight' : 5, 'flush' : 6, 'full_house' : 7, 'four_of_kind' : 8, 'straight_flush' : 9, 'royal_flush' : 10};

NameRank = {1 : 'high_card', 2 : 'one_pair',3 :  'two_pairs',4 : 'set',5 : 'straight',6 :  'flush',7 : 'full_house',8 :  'four_of_kind',9 : 'straight_flush',10 : 'royal_flush'};

# Characteristics of opponents
NumCharac = {'bluff' : 1, 'simple' : 2, 'agressive' : 3, 'passive' : 4, 'unknown' : 5, 'smart' : 6 };
NameCharac = {1 : 'bluff', 2 : 'simple', 3 : 'agressive', 4 : 'passive', 5 : 'unknown', 6 : 'smart'};

# Game States:
NameState = { 1 : 'play', 2 : 'analyz'};
NumState = {'play' : 1, 'analyz' : 2};

# Suit
NameSuit = { 0 : 'spade', 1 : 'club', 2 : 'heart', 3 : 'diamond'}
NumSuit = {'spade' : 0,'club' : 1,'heart' : 2,'diamond' : 3}

#


# Game info:
#	Holds games status


# megh_game
# =======================
# new_game



# megh_deal
# =======================
# deal_num
#

NW_DEAL = 0;	# new_deal?
DEAL_NUM = 0;
NW_GAME = 0;
DEBUG = 1;	# debug option
CURR_STAGE = 0;	#current stage
GM_STATE = 0;


# cards on board:

# Flop:
CARD1 = 0;
CARD2 = 0;
CARD3 = 0;
# Fourth_Street:
CARD4 = 0;
# Fifth_Street:
CARD5 = 0;



# stat files:
p1_stat = 'megh_player1_stat'
p2_stat = 'megh_player2_stat'
p3_stat = 'megh_player3_stat'
p4_stat = 'megh_player4_stat'
p5_stat = 'megh_player5_stat'

# files :
gm_state = 'megh_game_state'
gm_game = 'megh_game'
gm_deal = 'megh_deal'


# given files:
gv_deals_money = 'deals_money.txt'
gv_deal = 'deal.txt'
gv_inputf = 'inputf.txt'
gv_outputf = 'outputf.txt'



class PyGame:
	def __init__(self):
		global NW_DEAL
		global NW_GAME
		global DEAL_NUM
		global CURR_STAGE
		global CARD1
		global CARD2
		global CARD3
		global CARD4
		global CARD5
		global GM_STATE
		if(DEBUG):
			print "PyGame: obj creted..."
		self.smallblind = 0;
		self.bigblind = 0;
		self.dealer = 0;
		self.main_pot = 0;		# pot of game
		self.curr_stage = 0;	#curr stage
		self.prev_stage = 0;	#prev stage
		self.min_raise = 0;
		self.new_deal = 0;	# is it new deal??
		self.deal_num = 0;	# deal number
		self.new_game = 0;
		self.state = 0;		# state of game
		self.plrs_in = 0;	# players still in game

		self.card = [0,0,0,0,0,0,0];	# cards can be seen by me

		# is new game?
		if(os.path.isfile(gm_game)):
			# game already started...
			f = open(gm_game,'r')
			lin = f.readline();
			w = lin.strip()
			self.new_game = int(w);
			NW_GAME = self.new_game;
			if(DEBUG):
				print "PyGame: Old game..."

		else:
			# game just started
			# remove player_stat files if exists
			if(DEBUG):
				print "PyGame: New_Game..."
			if(os.path.isfile(p1_stat)):
					os.remove(p1_stat);

			if(os.path.isfile(p2_stat)):
					os.remove(p2_stat);

			if(os.path.isfile(p3_stat)):
					os.remove(p3_stat);

			if(os.path.isfile(p4_stat)):
					os.remove(p4_stat);

			if(os.path.isfile(p5_stat)):
					os.remove(p5_stat);

			f = open(gm_game,'w');
			f.write("0\n");
			f.close();

			self.new_game = 1;
			NW_GAME = 1;

								


		# is it new deal??
		if(os.path.isfile(gm_deal)):
			# if file exists... old deal
			self.new_deal = 0;	# old deal
			NW_DEAL = 0;
			if(DEBUG):
				print "PyGame: old deal ..."
			f = open(gm_deal,'r');
			lin = f.readline();
			self.deal_num = int(lin.strip());
			DEAL_NUM = self.deal_num;
			f.close()

		else:
			# new deal
			# find deal num
			self.new_deal = 1;
			NW_DEAL = 1

			if(DEBUG):
				print "PyGame: new deal ..."
			f = open(gv_deals_money);
			lin = f.readline();
			fwords = lin.split();
			w = fwords[1];
			self.deal_num = int(w.strip());
			DEAL_NUM = self.deal_num;
			f.close();
			f = open(gm_deal, 'w');
			f.write(str(self.deal_num));
			f.write('\n');
			f.close();
		
		if(DEBUG):
			print"PyGame: deal_num= %d" %self.deal_num


		
		f = open(gv_deal, 'r');
		lin = f.readline();
		fwords = lin.split();
		w = fwords[1];
		self.dealer = int(w.strip());
		self.smallblind = NxtPlayer(self.dealer);
		self.bigblind = NxtPlayer(self.smallblind);

		lin = f.readline();
		fwords = lin.split();
		w = fwords[1];
		self.curr_stage = NumStage[w.strip()];
		CURR_STAGE = self.curr_stage;

		lin = f.readline();
		fwords = lin.split();
		w = fwords[1];
		self.main_pot = int(w.strip());

		if(os.path.isfile(gm_state)):
			f = open(gm_state, 'r')
			lin = f.readline();
			w = lin.strip();
			self.prev_stage = int(w)
			f.close()
		else:
			self.prev_stage = NumStage['NA'];

		f = open(gm_state, 'w')
		f.write(str(self.curr_stage))
		f.close()


		if(NameStage[self.prev_stage] == 'Show_Down'):
			self.state = NumState['analyz']
		else:
			self.state = NumState['play']
		GM_STATE = self.state;	

		# Load cards on board:
		if(self.curr_stage > NumStage['Pre_Flop']):
			
			if(self.curr_stage >= NumStage['Flop']):
				# load 3 cards on board
				f = open(gv_deal, 'r')
				lin = f.readline()
				w = lin.strip();
				while( w != 'Flop'):
					lin = f.readline();
					w = lin.strip();
				lin = f.readline();
				ws = lin.split();
				CARD1 = int(ws[0].strip());
				CARD2 = int(ws[1].strip());
				CARD3 = int(ws[2].strip());
			if(self.curr_stage >= NumStage['Fourth_Street']):
				# load 4th card
				lin = f.readline()
				w = lin.strip()
				while(w != 'Fourth_Street'):
					lin = f.readline();
					w = lin.strip();
				lin = f.readline();
				w = lin.strip();
				CARD4 = int(w);
			
			if(self.curr_stage >= NumStage['Fifth_Street']):
				# load 5th card
				lin = f.readline()
				w = lin.strip()
				while(w != 'Fifth_Street'):
					lin = f.readline()
					w = lin.strip()
				lin = f.readline();
				w = lin.strip();
				CARD5 = int(w);
			f.close();	
			


		if(DEBUG):
			print "PyGame: dealer = %d" %(self.dealer)
			print "PyGame: samllblind = %d" %(self.smallblind)
			print "PyGame: bigblind = %d" %(self.bigblind)
			print "PyGame: curr_stage = %s" %(NameStage[self.curr_stage])
			print "PyGame: prev_stage = %s" %(NameStage[self.prev_stage])
			print "PyGame: state = %s" %(NameState[self.state])
			print "PyGame: main_pot = %d" %(self.main_pot)
			print "PyGame: CARD1 = %d" %(CARD1)
			print "PyGame: CARD2 = %d" %(CARD2)
			print "PyGame: CARD3 = %d" %(CARD3)
			print "PyGame: CARD4 = %d" %(CARD4)
			print "PyGame: CARD5 = %d\n" %(CARD5)



# Player details:
#	Holds Player specific info

class My_Player :
	def __init__(self) :
		global NW_DEAL
		global NW_GAME
		global DEAL_NUM
		global CARD1
		global CARD2
		global CARD3
		global CARD4
		global CARD5
		global CURR_STAGE
		if(DEBUG):
			print "My_Player: obj created ..."
		self.money = 0;
		self.mypos = 0;		# my position in game
		self.hole = [0,0];	# hole cards
		self.money_spent = 0;	# money spent in current deal
		self.coc = 0;		# cost of call
		self.money_left = 0;

		if(not NW_DEAL):
			# old deal : load details of player from -> megh_deal
			if(DEBUG):
				print "My_Player: Old deal ..."

		else:
			# new deal : load details from -> inputf.txt, deals_money.txt
			if(DEBUG):
				print "My_Player: New deal ..."
		f = open(gv_inputf, 'r');
		lin = f.readline();
		fwords = lin.split();
		w = fwords[0];
		self.hole[0] = int(w.strip());
		w = fwords[1];
		self.hole[1] = int(w.strip());
		w = fwords[2];
		self.mypos = int(w.strip());
		w = fwords[3];
		self.money_spent = int(w.strip());
		f.close();

		assert(self.mypos and self.mypos < 7);	# assert

		f = open(gv_deals_money, 'r');
		for i in range(self.mypos):
			lin = f.readline();
		lin = f.readline();
		fwords = lin.split();
		w =fwords[1];
		self.money = int(w.strip());
		self.money_left = self.money - self.money_spent;
		
		if(DEBUG):
			print "My_Player: hole cards = %d %d" %(self.hole[0], self.hole[1])
			print "My_Player: mypos = %d" %(self.mypos)
			print "My_Player: money_spent = %d " %(self.money_spent)
			print "My_Player: money = %d" %(self.money)
			print "My_Player: money_left = %d \n" %(self.money_left)
	

	def Action(self) :
		pass



# Other Player details:
#
# px_stat file
# ============================================================
# plr_charac1	plr_charac2		plr_charac3		plr_charac4
# Pre_Flop charac list			deal1	deal2	.	.	.
# Flop charac list				deal1	deal2	.	.	.
# Fourth_Street charac list		deal1	deal2	.	.	.
# Fifth_Street charac list		deal1	deal2	.	.	.
# ============================================================



class Other_Player :
	def __init__(self, stat_fname, posn):
		global NW_GAME
		global NW_DEAL
		global DEAL_NUM
		global CARD1
		global CARD2
		global CARD3
		global CARD4
		global CARD5
		global CURR_STAGE
		self.plr_charac1 = NumCharac['unknown'];	# Pre_Flop charac
		self.plr_charac2 = NumCharac['unknown'];	# Flop charac
		self.plr_charac3 = NumCharac['unknown'];	# Fourth_street charac
		self.plr_charac4 = NumCharac['unknown'];	# Fifth_street charac
		self.pos = posn;	# position
		self.hole = [0,0];	# hole cards used for analyz
		self.money = 0; # money at start of current deal

		if(DEBUG):
			print "Other_Player %d: obj created ..." %(self.pos)

		f = open(gv_deals_money, 'r')
		lins = f.readlines();
		lin = lins[self.pos];
		ws = lin.split();
		w = ws[1];
		self.money = int(w.strip());
		f.close()

		if(GM_STATE == NumState['analyz']):
			# load hole cards:
			if(DEBUG):
				print "Other_Player %d: Analyzing ..." %self.pos
			f = open(gv_deal, 'r')
			lin = f.readline();
			w = lin.strip();
			while(w != 'Show_Down'):
				lin = f.readline()
				w = lin.strip()
			lin = f.readline();
			ws = lin.split()
			w = ws[0]
			i = int(w.strip())
			while(i != self.pos):
				lin = f.readline()
				ws = lin.split()
				w = ws[0]
				i = int(w.strip())
			w = ws[1];
			i =int(w.strip())
			self.hole[0] = i	
			w = ws[2];
			i =int(w.strip())
			self.hole[1] = i
			f.close()

			# Analyz...
			f = open(gv_deal, 'r')
			lin = f.readline();
			w = lin.strip();
			while(w != 'Pre_Flop'):
				lin = f.readline();
				w = lin.strip();
			lin = f.readline();
			w = lin.strip();
			while(w != 'End'):
				# analyz pre_flop
				ws = lin.split();





		if(DEAL_NUM == 1):
			# stat file does not exists - New game
			self.plr_charac1 = NumCharac['unknown'];
			self.plr_charac2 = NumCharac['unknown'];
			self.plr_charac3 = NumCharac['unknown'];
			self.plr_charac4 = NumCharac['unknown'];
			f = open(stat_fname, 'w')
			s = str(self.plr_charac1)+ ' '+ str(self.plr_charac2)+ ' ' +str(self.plr_charac3)+ ' '+str(self.plr_charac4)
			f.write(s);
			f.close();


		elif(DEAL_NUM > 1):
			# stat file already exists
			# load statistics
			if(NW_DEAL and DEAL_NUM > 1):
				# at start of new deal analyz player
				f = open(stat_fname, 'r')
				lin = f.readline()
				ws = lin.split()
				self.plr_charac1 = int(ws[0].strip())
				self.plr_charac2 = int(ws[1].strip())
				self.plr_charac3 = int(ws[2].strip())
				self.plr_charac4 = int(ws[3].strip())
				f.close()



		if(DEBUG):
			print "Other_Player %d: money = %d" %(self.pos, self.money)
			print "Other_Player %d: hole[0] = %d" %(self.pos, self.hole[0])
			print "Other_Player %d: hole[1] = %d" %(self.pos, self.hole[1])


#	def Analyz(self):
		# Analyz deal.txt and old stat file 
		# read hole cards:
#		pass


def AnalyzCards(hole1, hole2, stage):
	# what best can be formed by cards, return rank of corr hand
	# returns [val, best_hand]
	# val = number of possible 'GOOD' hands
	val =0;
	best_hand = 0;
	if(stage == NumStage['Pre_Flop']):
		if(CardVal(hole1) == CardVal(hole2)):
			#pair?
			val = val + 1;
			best_hand = NumRank['one_pair']
		if(SuitNum(hole1) == SuitNum(hole2)):
			#flush?
			val = val + 1;
		if((CardVal(hole1) - CardVal(hole2)) == 1):
			#stright?
			val = val + 1;
		if(((CardVal(hole1) - CardVal(hole2)) == 1) and (SuitNum(hole1) == SuitNum(hole2))):
			#stright + flush?
			val = val + 1;
		if(CardVal(hole1) >=10 or CardVal(hole2) >=10):
			# high cards?
			val = val + 1;
		ret = [val, best_hand];	

		return ret
	elif(stage == NumStage['Flop']):




# get nxt player :
def NxtPlayer(prsnt):
	if(prsnt == 6):
		return 1;
	else:
		return (prsnt+1);



def CalcOdds(hole1, hole2):
	# calculate odds
	if(DEBUG):
		print "CalcOdds: calculatig odds ..."


def CalcOuts(hole1, hole2):
	# 1. Counting outs - cards still in deck that can give potentially winning hand
	# http://www.youtube.com/watch?v=D96gUcTNlxs
	if(DEBUG):
		print "CalcOdds: calculating outs ..."


def CardVal(card):
	# returns card value
	return card%13;

def SuitNum(card):
	# returns suit number
	return int(card/13);


		


# START THE GAME ...


Game = PyGame();
MyPlayer = My_Player();
Player1 = Other_Player(stat_fname = p1_stat, posn = (NxtPlayer(MyPlayer.mypos)));	# player to my left
Player2 = Other_Player(stat_fname = p2_stat, posn = (NxtPlayer(Player1.pos)));	# 
Player3 = Other_Player(stat_fname = p3_stat, posn = (NxtPlayer(Player2.pos)));	# 
Player4 = Other_Player(stat_fname = p4_stat, posn = (NxtPlayer(Player3.pos)));	# 
Player5 = Other_Player(stat_fname = p5_stat, posn = (NxtPlayer(Player4.pos)));	# player to my right








if(Game.state == NumState['play']):
	# Play game
	if(DEBUG):
		print "GAME: Play state"

	if(NW_GAME):
		# if game just started
		if(DEBUG):
			print "GAME: new game started ..."

	else:
		# if game already started 
		if(DEBUG):
			print "GAME: old game playing ..."




elif(Game.state == NumState['analyz']):
	# END OF CURRENT DEAL:
	# analyz all players using deal.txt
	# remove gm_deal
	# remove gm_state
	if(DEBUG):
		print "GAME: Analyz state"

	# Analyz players
	


	# remove files specific to "deal"
	if(os.path.isfile(gm_deal)):
		os.remove(gm_deal);
	if(os.path.isfile(gm_state)):
		os.remove(gm_state);
