#################################################
#	Name	:	Meghanad Shingate
#	email	:	meghanads@iitb.ac.in
#	RollNo	:	09307608
#	Mob.	:	+919960981078
#	IIT Bombay
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
from sys import exit
from random import *


# decision
NumPlrAct = {'Fold' : 1, 'Call' : 2, 'Rise' : 3};
NamePlrAct = {1 : 'Fold', 2 : 'Call',3 : 'Rise'};

# stages in game
NameStage = { 1 : 'Pre_Flop', 2 : 'Flop', 3 : 'Fourth_Street', 4 : 'Fifth_Street', 5 : 'Show_Down', 6 : 'NA'};
NumStage = { 'Pre_Flop' : 1, 'Flop' : 2, 'Fourth_Street' : 3, 'Fifth_Street' : 4 , 'Show_Down' : 5, 'NA' : 6};

# Rank of hand:
NumRank = {'high_card' : 1, 'one_pair' : 2, 'two_pairs' : 3, 'set' : 4, 'straight' : 5, 'flush' : 6, 'full_house' : 7, 'four_of_kind' : 8, 'straight_flush' : 9, 'royal_flush' : 10};

NameRank = {1 : 'high_card', 2 : 'one_pair',3 :  'two_pairs',4 : 'set',5 : 'straight',6 :  'flush',7 : 'full_house',8 :  'four_of_kind',9 : 'straight_flush',10 : 'royal_flush'};

# probability of hand in persentage:
ProbRank = [50.1, 42.3, 4.75, 2.11, 0.392, 0.197, 0.144, 0.024, 0.00139, 0.000154];

# hand odds: x:1
OddsRank = [649739, 72192, 4165, 694, 507, 253, 46, 20, 1.36, 0.995];

# Characteristics of opponents
NumCharac = {'bluff' : 2, 'simple' : 3, 'agressive' : 4, 'unknown' : 1, 'smart' : 5 };
NameCharac = {2 : 'bluff', 3 : 'simple', 4 : 'agressive',1 : 'unknown', 5 : 'smart',};

# Game States:
NameState = { 1 : 'play', 2 : 'analyz'};
NumState = {'play' : 1, 'analyz' : 2};

# Suit
NameSuit = { 0 : 'spade', 1 : 'club', 2 : 'heart', 3 : 'diamond'}
NumSuit = {'spade' : 0,'club' : 1,'heart' : 2,'diamond' : 3}

# CardOdds: x:1
# upto 17 outs
OneCardOdds = [0, 46, 22, 14, 10, 8, 6.7, 5.6, 4.7, 4.2, 3.6, 3.2, 2.8, 2.5, 2.3, 2.1, 1.9, 1.7];
TwoCardOdds = [0, 23, 12, 7, 5, 4, 3.2, 2.6, 2.2, 1.9, 1.6, 1.4, 1.2, 1.1, 0.95, 0.85, 0.75, 0.66];



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
SM_BLIND = 0;
BG_BLIND = 0;




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
gm_plrsin = 'megh_plrsin'


# given files:
gv_deals_money = 'deals_money.txt'
gv_deal = 'deal.txt'
gv_inputf = 'inputf.txt'
gv_outputf = 'outputf.txt'

# given
bg_bet = 10;
sm_bet =5

def CheckFiles():
	if(not(os.path.isfile(gv_deals_money))):
		print "ERR: deals_money.txt NOT FOUND"
		exit(1);
	if(not(os.path.isfile(gv_deal))):
		print "ERR: deal.txt NOT FOUND"
		exit(1);
	if(not(os.path.isfile(gv_inputf))):
		print "ERR: inputf.txt NOT FOUND"
		exit(1);


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
		global SM_BLIND
		global BG_BLIND
		if(DEBUG):
			print "PyGame: obj creted..."
		self.smallblind = 0;
		self.bigblind = 0;
		self.dealer = 0;
		self.main_pot = 0;		# pot of game
		self.curr_stage = 0;	#curr stage
		self.prev_stage = 0;	#prev stage
		self.min_rise = 0;	# min rise
		self.to_call = 0;	# money req to call
		self.new_deal = 0;	# is it new deal??
		self.deal_num = 0;	# deal number
		self.new_game = 0;
		self.state = 0;		# state of game
		self.plrs_left = 0;	# players still in game
		self.plr_posn = [0,0,0,0,0,0,0]	#player positions

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
			EOF(lin)
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
			EOF(lin)
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
		EOF(lin)
		fwords = lin.split();
		while(fwords[0].strip() != 'Dealer'):
			lin = f.readline()
			EOF(lin)
			fwords = lin.split()
		w = fwords[1];
		self.dealer = int(w.strip());
		self.smallblind = NxtPlayer(self.dealer);
		self.bigblind = NxtPlayer(self.smallblind);
		SM_BLIND = self.smallblind;
		BD_BLIND = self.bigblind;

		# player positions
		self.plr_posn[1] = self.smallblind
		self.plr_posn[2] = self.bigblind
		self.plr_posn[3] = NxtPlayer(self.plr_posn[2])
		self.plr_posn[4] = NxtPlayer(self.plr_posn[3])
		self.plr_posn[5] = NxtPlayer(self.plr_posn[4])
		self.plr_posn[6] = NxtPlayer(self.plr_posn[5])

		if(DEBUG):
			print "PyGame: plr_posn = %s" %self.plr_posn


		lin = f.readline();
		fwords = lin.split();
		while(fwords[0].strip() != 'Stage'):
			lin = f.readline()
			EOF(lin)
			fwords = lin.split()
		w = fwords[1];
		self.curr_stage = NumStage[w.strip()];
		CURR_STAGE = self.curr_stage;

		lin = f.readline();
		fwords = lin.split();
		while(fwords[0].strip() != 'Main_Pot'):
			lin = f.readline()
			EOF(lin)
			fwords = lin.split()
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


		if(NameStage[self.curr_stage] == 'Show_Down'):
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
				EOF(lin)
				w = lin.strip();
				while( w != 'Flop'):
					lin = f.readline();
					EOF(lin)
					w = lin.strip();
				lin = f.readline();
				EOF(lin)
				ws = lin.split();
				CARD1 = int(ws[0].strip());
				CARD2 = int(ws[1].strip());
				CARD3 = int(ws[2].strip());
			if(self.curr_stage >= NumStage['Fourth_Street']):
				# load 4th card
				lin = f.readline()
				EOF(lin)
				w = lin.strip()
				while(w != 'Fourth_Street'):
					lin = f.readline();
					EOF(lin)
					w = lin.strip();
				lin = f.readline();
				EOF(lin)
				w = lin.strip();
				CARD4 = int(w);
			
			if(self.curr_stage >= NumStage['Fifth_Street']):
				# load 5th card
				lin = f.readline()
				EOF(lin)
				w = lin.strip()
				while(w != 'Fifth_Street'):
					lin = f.readline()
					EOF(lin)
					w = lin.strip()
				lin = f.readline();
				EOF(lin)
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
		global SM_BLIND
		global BG_BLIND
		global CURR_STAGE
		if(DEBUG):
			print "My_Player: obj created ..."
		self.money = 0;
		self.mypos = 0;		# my position in game
		self.hole = [0,0];	# hole cards
		self.money_spent = 0;	# money spent in current deal
		self.coc = 0;		# cost of call
		self.money_left = 0;

		# load my info
		f = open(gv_inputf, 'r');
		lin = f.readline();
		EOF(lin)
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

		# load my money
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




def EOF(name):
	if(not name):
		print "ERROR: File ended ... File not in correct format"
		exit(1)
	else:
		return 0;


# outs:
NumOuts = {'flush_draw' : 9, 'straight_draw' : 8, 'straight_or_flush_draw' : 12, 'straight_flush_draw' : 17};
NameOuts = {9 : 'flush_draw', 8 : 'straight_draw', 12 : 'straight_or_flush_draw',17 : 'straight_flush_draw'};



def AnalyzCards(hole1, hole2, stage):
	# what best can be formed by cards, return rank of corr hand
	# hand_comp = true if hand is already completed.
	# returns [best_hand, hand_comp, card_odds, high_card, one_pair, two_pairs, sett, straight, flush, full_house, four_of_kind, straight_flush]
	best_hand = 0;	# best hand that is already complete at this stage
	hand_comp = 0;
	hand_odds = 0; # 0 = invalid
	one_pair = 0;
	two_pairs = 0;
	sett = 0;
	straight = 0;
	flush = 0;
	full_house = 0;
	four_of_kind = 0;
	straight_flush = 0;
	high_card = 0;
	flush_draw = 0; # is it flush draw
	straight_draw = 0;
	straight_flush_draw = 0;

	if(stage == NumStage['Pre_Flop']):
		if(CardVal(hole1) >=10 or CardVal(hole2) >=10):
			# high cards?
			best_hand = NumRank['high_card'];
			high_card = 1
		if(SuitNum(hole1) == SuitNum(hole2)):
			#flush?
			flush = 1;
		if(abs(CardVal(hole1) - CardVal(hole2)) == 1):
			#straight?
			straight = 1
		if((abs(CardVal(hole1) - CardVal(hole2)) == 1) and (SuitNum(hole1) == SuitNum(hole2))):
			#straight + flush?
			straight_flush = 1;
		if(CardVal(hole1) == CardVal(hole2)):
			#pair?
			best_hand = NumRank['one_pair']
			one_pair = 1;
		if(DEBUG):
			print "AnalyzCards: Pre_Flop stage ..."

		ret = [best_hand, hand_comp, hand_odds, high_card, one_pair, two_pairs, sett, staright, flush, full_house, four_of_kind, straight_flush];
		if(DEBUG):
			print "AnalyzCards: ret = %s" %ret
		return ret

	elif(stage == NumStage['Flop']):
		# i have 5 cards now, two cards to come

		# load card info:
		cards = [hole1, hole2, CARD1, CARD2, CARD3];	#cards
		vcards = [CardVal(hole1), CardVal(hole2), CardVal(CARD1), CardVal(CARD2), CardVal(CARD3)];	# card values
		scards = [SuitNum(hole1), SuitNum(hole2), SuitNum(CARD1), SuitNum(CARD2), SuitNum(CARD3)];	#card suits

		vcount = [vcards.count(0), vcards.count(1),	vcards.count(2),vcards.count(3),vcards.count(4),vcards.count(5),vcards.count(6),vcards.count(7),vcards.count(8),vcards.count(9),vcards.count(10),vcards.count(11),vcards.count(12)]	#cards count

		suit_flag =[[0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0]];

		# fill suit_flags:
		for i in range(len(vcount)):
			if(vcount[i]>0):
				n = vcount[i]
				while(n):
					for j in range(len(vcards)):
						if(vcards[j] == i):
							suit_flag[scards[j]][i] = 1;
							n = n - 1;
					

		scount = [scards.count(0), scards.count(1),scards.count(2),scards.count(3)];
	


		if(DEBUG):
			print "AnalyzCards: analyzing cards ...%s" %NameStage[stage]
			print "cards = %s" %cards
			print "vcards = %s" %vcards
			print "scards = %s" %scards
			print "vcount = %s" %vcount
			print "scount = %s" %scount
			print "suit_flag0 = %s" %suit_flag[0]
			print "suit_flag1 = %s" %suit_flag[1]
			print "suit_flag2 = %s" %suit_flag[2]
			print "suit_flag3 = %s" %suit_flag[3]


		#high card
		if(CardVal(hole1) >= 10 or CardVal(hole2) >=10):
			high_card = 1;

		# straight?
		for i in range(len(vcount) - 4):
			win = vcount[i:(i+5)]
			if(win.count(0) == 0):
				straight = 1;
				break
			else:
				straight = 0

			
		if(straight):
			if(max(scount)== 5):
				# straight flush
				straight_flush = 1;
				hand_comp = 1;
				best_hand = NumRank['straight_flush'];
		if( not hand_comp):
			if(max(vcount) == 4):
				#four of kind
				four_of_kind = 1;
				hand_comd = 1;
				best_hand = NumRank['four_of_kind'];
		if( not hand_comp):
			if(max(vcount) ==3):
				if(vcount.count(2) > 0):
					#full house
					full_house = 1;
					hand_comp = 1;
					best_hand = NumRank['full_house'];
		if( not hand_comp):
			if(max(scount) == 5):
				#flush
				flush = 1;
				hand_comp = 1;
				best_hand = NumRank['flush'];
		if( not hand_comp):
			if(straight):
				#straight:
				hand_comp = 1;
				best_hand = NumRank['straight'];

		if( not hand_comp):
			if(max(vcount) == 2):
				#pair
				one_pair = 1;
				hand_comp = 1;	# nxt two cards can form two pairs or set or full house	
				best_hand = NumRank['one_pair'];
			if(vcount.count(2) == 2):
				#two_pairs
				two_pairs = 1;
				hand_comp = 1; # nxt two cards can form full house, calc odds
				best_hand = NumRank['two_pairs'];
			if(max(vcount) == 3):
				#set
				sett = 1;
				hand_comp == 1;	# next two cards may form full house, calc odds
				best_hand = NumRank['set'];
					
			if(max(scount)  == 4):
				# can be flush
				flush = 1;
				flush_draw = 1;

			# can be straight?
			for i in range(len(vcount) - 4):
				win = vcount[i:(i+5)]
				if(win.count(0)>1):
					straight = 0;
					straight_draw = 0;
				else:
					straight = 1
					straight_draw = 1
					straight_indx = i
					break

			# can be straight flush?
			if(straight and flush):
				for  i in range(4):
					if(sum(suit_flag[i]) == 4):
						sut = i
						break

				for i in range(straight_indx, straight_indx+5):
					if(vcount[i]):
						if(not suit_flag[sut][i]):
							straight_flush_draw = 0;
							break
						else:	
							straight_flush_draw = 1;
							straight_flush = 1

		# calc odds of possible	best hand				
				
		if(straight_flush_draw):
			hand_odds = NumOuts['straight_flush_draw']*4;
		elif(flush_draw and straight_draw):
			hand_odds = NumOuts['straight_or_flush_draw']*4;
		elif(flush_draw):
			hand_odds = NumOuts['flush_draw']*4;
		elif(straight_draw):
			hand_odds = NumOuts['straight_draw']*4;


		ret = [best_hand, hand_comp, hand_odds, high_card, one_pair, two_pairs, sett, straight, flush, full_house, four_of_kind, straight_flush];

		if(DEBUG):
			print "return = %s\n" %ret
		return ret


	elif(stage == NumStage['Fourth_Street']):
		# i have 6 cards now, one card to come
		cards = [hole1, hole2, CARD1, CARD2, CARD3, CARD4];
		vcards = [CardVal(hole1), CardVal(hole2), CardVal(CARD1), CardVal(CARD2), CardVal(CARD3), CardVal(CARD4)];
		scards = [SuitNum(hole1), SuitNum(hole2), SuitNum(CARD1), SuitNum(CARD2), SuitNum(CARD3), SuitNum(CARD4)];

		vcount = [vcards.count(0), vcards.count(1),	vcards.count(2),vcards.count(3),vcards.count(4),vcards.count(5),vcards.count(6),vcards.count(7),vcards.count(8),vcards.count(9),vcards.count(10),vcards.count(11),vcards.count(12)]

		suit_flag =[[0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0]];

		# fill suit_flags:
		for i in range(len(vcount)):
			if(vcount[i]>0):
				n = vcount[i]
				while(n):
					for j in range(len(vcards)):
						if(vcards[j] == i):
							suit_flag[scards[j]][i] = 1;
							n = n - 1;
					

		scount = [scards.count(0), scards.count(1),scards.count(2),scards.count(3)];
	

		if(DEBUG):
			print "AnalyzCards: analyzing cards ...%s" %NameStage[stage]
			print "cards = %s" %cards
			print "vcards = %s" %vcards
			print "scards = %s" %scards
			print "vcount = %s" %vcount
			print "scount = %s" %scount
			print "suit_flag0 = %s" %suit_flag[0]
			print "suit_flag1 = %s" %suit_flag[1]
			print "suit_flag2 = %s" %suit_flag[2]
			print "suit_flag3 = %s" %suit_flag[3]

		#high card
		if(CardVal(hole1) >= 10 or CardVal(hole2) >=10):
			high_card = 1;
	

		# straight?
		for i in range(len(vcount) - 4):
			win = vcount[i:(i+5)]
			if(win.count(0) == 0):
				straight = 1;
				break
			else:
				straight = 0

			
		if(straight):
			if(max(scount)>= 5):
				# straight flush
				# do my cards in that? -> yes , 2+3+1
				straight_flush = 1;
				hand_comp = 1;
				best_hand = NumRank['straight_flush'];
		if( not hand_comp):
			if(max(vcount) == 4):
				#four of kind
				four_of_kind = 1;
				hand_comd = 1;
				best_hand = NumRank['four_of_kind'];
		if( not hand_comp):
			if(max(vcount) ==3):
				if(vcount.count(2) > 0):
					#full house
					full_house = 1;
					hand_comp = 1;
					best_hand = NumRank['full_house'];
		if( not hand_comp):
			if(max(scount) == 5):
				#flush
				flush = 1;
				hand_comp = 1;
				best_hand = NumRank['flush'];
		if( not hand_comp):
			if(straight):
				#straight:
				hand_comp = 1;
				best_hand = NumRank['straight'];

		if( not hand_comp):
			if(max(vcount) == 2):
				#pair
				one_pair = 1;
				hand_comp = 1;	# nxt two cards can form two pairs or set or full house	
				best_hand = NumRank['one_pair'];
			if(vcount.count(2) == 2):
				#two_pairs
				two_pairs = 1;
				hand_comp = 1; # nxt two cards can form full house, calc odds
				best_hand = NumRank['two_pairs'];
			if(max(vcount) == 3):
				#set
				sett = 1;
				hand_comp == 1;	# next two cards may form full house, calc odds
				best_hand = NumRank['set'];
					
			if(max(scount)  == 4):
				# can be flush
				flush = 1;
				flush_draw = 1;

			# can be straight?
			for i in range(len(vcount) - 4):
				win = vcount[i:(i+5)]
				if(win.count(0)>1):
					straight = 0;
					straight_draw = 0;
				else:
					straight = 1
					straight_draw = 1
					straight_indx = i
					break

			# can be straight flush?
			if(straight and flush):
				for  i in range(4):
					if(sum(suit_flag[i]) == 4):
						sut = i
						break

				for i in range(straight_indx, straight_indx+5):
					if(vcount[i]):
						if(not suit_flag[sut][i]):
							straight_flush_draw = 0;
							break
						else:	
							straight_flush_draw = 1;
							straight_flush = 1
				
		if(straight_flush_draw):
			hand_odds = 2*NumOuts['straight_flush_draw'];
		elif(flush_draw and straight_draw):
			hand_odds = 2*NumOuts['straight_or_flush_draw'];
		elif(flush_draw):
			hand_odds = 2*NumOuts['flush_draw'];
		elif(straight_draw):
			hand_odds = 2*NumOuts['straight_draw'];


		ret = [best_hand, hand_comp, hand_odds, high_card, one_pair, two_pairs, sett, straight, flush, full_house, four_of_kind, straight_flush];

		if(DEBUG):
			print "AnalyzCards: return = %s\n" %ret
		return ret
	elif(stage == NumStage['Fifth_Street']):
		# i have 7 cards now, NO cards to come
		cards = [hole1, hole2, CARD1, CARD2, CARD3, CARD4, CARD5];
		vcards = [CardVal(hole1), CardVal(hole2), CardVal(CARD1), CardVal(CARD2), CardVal(CARD3),CardVal(CARD4),CardVal(CARD5)];
		scards = [SuitNum(hole1), SuitNum(hole2), SuitNum(CARD1), SuitNum(CARD2), SuitNum(CARD3),SuitNum(CARD4),SuitNum(CARD5)];

		vcount = [vcards.count(0), vcards.count(1),	vcards.count(2),vcards.count(3),vcards.count(4),vcards.count(5),vcards.count(6),vcards.count(7),vcards.count(8),vcards.count(9),vcards.count(10),vcards.count(11),vcards.count(12)]

		suit_flag =[[0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0]];

		# fill suit_flags:
		for i in range(len(vcount)):
			if(vcount[i]>0):
				n = vcount[i]
				while(n):
					for j in range(len(vcards)):
						if(vcards[j] == i):
							suit_flag[scards[j]][i] = 1;
							n = n - 1;
					



		scount = [scards.count(0), scards.count(1),scards.count(2),scards.count(3)];
	

		if(DEBUG):
			print "AnalyzCards: analyzing cards ...%s" %NameStage[stage]
			print "cards = %s" %cards
			print "vcards = %s" %vcards
			print "scards = %s" %scards
			print "vcount = %s" %vcount
			print "scount = %s" %scount
			print "suit_flag0 = %s" %suit_flag[0]
			print "suit_flag1 = %s" %suit_flag[1]
			print "suit_flag2 = %s" %suit_flag[2]
			print "suit_flag3 = %s" %suit_flag[3]


		#high card
		if(CardVal(hole1) >= 10 or CardVal(hole2) >=10):
			high_card = 1;
	

		# straight?
		for i in range(len(vcount) - 4):
			win = vcount[i:(i+5)]
			if(win.count(0) == 0):
				straight = 1;
				break
			else:
				straight = 0

		if(straight):
			#do my cards are in that?
			if((vcards[0] >= i and vcards[0] < (i+5)) or (vcards[1] >= i  and vcards[1] < (i+5))):
				straight = 1;
			else:
				straight = 0;


			
		if(straight):
			if(max(scount)>= 5):
				# straight flush
				# do my cards are in that?
				m_suit = scount.index( max(scount));
				if(scards[0] == m_suit or scards[1] == m_suit):
					straight_flush = 1;
					hand_comp = 1;
					best_hand = NumRank['straight_flush'];
		if( not hand_comp):
			if(max(vcount) == 4):
				#four of kind
				c_val = vcount.index(max(vcount));
				if(vcards[0] == c_val or vcards[1] == c_val):
					four_of_kind = 1;
					hand_comd = 1;
					best_hand = NumRank['four_of_kind'];
		if( not hand_comp):
			if(max(vcount) >=3):
				if(vcount.count(2) > 0):
					#full house
					full_house = 1;
					hand_comp = 1;
					best_hand = NumRank['full_house'];
		if( not hand_comp):
			if(max(scount) >= 5):
				#flush
				# DO MY CARDS ARE IN THAT?
				m_suit = scount.index( max(scount));
				if(scards[0] == m_suit or scards[1] == m_suit):
					flush = 1;
					hand_comp = 1;
					best_hand = NumRank['flush'];
		if( not hand_comp):
			if(straight):
				#straight:
				hand_comp = 1;
				best_hand = NumRank['straight'];

		if( not hand_comp):
			if(max(vcount) >= 3):
				#set?
				c_val = vcount.index(max(vcount));
				if(vcards[0] == c_val or vcards[1] == c_val):
					sett = 1;
					hand_comp == 1;	# next two cards may form full house, calc odds
					best_hand = NumRank['set'];
		if( not hand_comp):		
			if(vcount.count(2) >= 2):
				#two_pairs
				two_pairs = 1;
				hand_comp = 1; # nxt two cards can form full house, calc odds
				best_hand = NumRank['two_pairs'];
		if( not hand_comp):
			if(max(vcount) >= 2):
				#pair
				one_pair = 1;
				hand_comp = 1;	# nxt two cards can form two pairs or set or full house	
				best_hand = NumRank['one_pair'];
											

		ret = [best_hand, hand_comp, hand_odds, high_card, one_pair, two_pairs, sett, straight, flush, full_house, four_of_kind, straight_flush];

		if(DEBUG):
			print "AnalyzCards: return = %s\n" %ret
		return ret
	else:
		ret = [best_hand, hand_comp, hand_odds, high_card, one_pair, two_pairs, sett, straight, flush, full_house, four_of_kind, straight_flush];



# Small Functions:

# get nxt player :
def NxtPlayer(prsnt):
	if(prsnt == 6):
		return 1;
	else:
		return (prsnt+1);

def PrevPlayer(prsnt):
	if(prsnt == 1):
		return 6;
	else:
		return (prsnt - 1);
	


# card value:
def CardVal(card):
	# returns card value
	return card%13;

# card suit:
def SuitNum(card):
	# returns suit number
	if(card == 13):
		return 0;
	elif(card == 26):
		return 1;
	elif(card == 39):
		return 2;
	elif( card == 52):
		return 3;
	else:
		return int(card/13);




def LoadStage(stage):
	# load stage
	ret = []
	f = open(gv_deal, 'r')
	lin = f.readline()
	EOF(lin)
	st = lin.strip()
	while(st != NameStage[stage]):
		lin = f.readline()
		EOF(lin)
		st = lin.strip()
	if(stage != NumStage['Pre_Flop']):
		lin = f.readline()
	lin = f.readline()
	lin = f.readline()
	lin = lin.strip()
	if(lin):
		w = lin.strip()
	else:
		w = 'End'
		
	while(w != 'End' and lin):
		ws = lin.split()
		if(len(ws) >= 2):
			if(ws[1].strip() =='Rise'):
				h = [int(ws[0].strip()), NumPlrAct['Rise'], int(ws[2].strip())]
				ret.append(h);
			elif(ws[1].strip() == 'Call'):
				h = [int(ws[0].strip()), NumPlrAct['Call'], int(ws[2].strip())]
				ret.append(h);
			elif(ws[1].strip() == 'Fold'):
				h = [int(ws[0].strip()), NumPlrAct['Fold'], int(ws[2].strip())]
				ret.append(h)
			elif(ws[1].strip() == '-'):
				h = [int(ws[0].strip()), NumPlrAct['Fold'], -1]
				ret.append(h)
		lin = f.readline()
		lin = lin.strip()
		if(lin):
			w = lin.strip()
		else:
			w = 'End'

	if(DEBUG):
		print "LoadStage: %s = %s" %(NameStage[stage], ret)
	return ret



# cost of call
def CoC(main_pot, spent):
	ret = 0;
	ret = main_pot - spent
	ret = max(ret, 0)
	if(DEBUG):
		print "CoC: main_pot = %d, spent = %d, ret = %d" %(main_pot, spent, ret)
	return ret
	


# min rise at this stage of game
def MinRise(stage):
	# minimum rise:
	st = LoadStage(stage);
	ret = -1;
	if(stage < NumStage['Show_Down']):

		#rise : bigblind + one additional bet
		#rerise : prev bet + one additional bet
		r=-1	# latest rise index
		c = -1 # call index just before rise index
		if( stage <= NumStage['Flop']):
			riseby = bg_bet;
		else:
			riseby = 2*bg_bet;
		riseby2 = 0;	
		if(st):
			re =range(len(st));
			re.reverse()
			for i in re:
				if(st[i][1] == NumPlrAct['Rise']):
					r = i
					break

			if(r > -1):
				re = range(r)
				re.reverse()
				for i in re:
					if(st[i][1] >= NumPlrAct['Call']):
						c = i
						break
	
			if(r>-1 and c > -1):
				riseby2 = st[r][2] - st[c][2];
		
			ret = max( riseby, riseby2);
		else:
			ret = riseby
	if(DEBUG):
		print "MinRise: stage_riseby = %d, ret = %d" %(riseby, ret)
	return ret
		



# Call
def Call():
	if(DEBUG):
		print "My_Player: Called ..."
	f = open(gv_outputf, 'w')
	f.write('0')
	f.close()


# fold
def Fold():
	if(DEBUG):
		print "My_Player: Folded ..."
	f = open(gv_outputf, 'w')
	f.write('-10')
	f.close()

# rise by amt
def Rise(amt):
	if(DEBUG):
		print "My_Player: Rised ..."
	f = open(gv_outputf, 'w')
	f.write(str(amt))
	f.close()
	

def PotOdds(main_pot, coc, plrsin):
	ret = int((coc/(main_pot*plrsin+coc+0.01))*100)
	if(DEBUG):
		print "PotOdds: Calcularing pot odds = %d" %ret;
	return ret 		

def Plrsin():
	#platers still in game:
	#megh_plrsin
	ret = 0;
	plrs = 0;
	if(DEAL_NUM == 1):
		f = open(gm_plrsin, 'w');
		f.write('6');
		f.close();
		plrs = 6;
	else:
		if(os.path.isfile(gm_plrsin)):
			f = open(gm_plrsin, 'r')
			w = f.readline();
			plrs = int(w.strip());
		else:
			plrs = 6;
				
	if(DEBUG):
		print "Plrsin: plrs = %d" %plrs
	return plrs;

				



# START THE GAME ...

CheckFiles();
Game = PyGame();
MyPlayer = My_Player();


if(Game.state == NumState['play']):
	# Play game
	if(DEBUG):
		print "GAME: Play state"

	best_hand = 0;
	hand_comp = 0;
	hand_odds = 0;
	high_card = 0;
	one_pair = 0;
	two_pairs = 0;
	sett = 0;
	straight = 0;
	full_house = 0;
	flush = 0;
	four_of_kind = 0;
	straight_flush = 0;

	call_cost = CoC(Game.main_pot, MyPlayer.money_spent);
	plrs_in = Plrsin();


	# Play ...
	if(DEBUG):
		MinRise(Game.curr_stage);
		Plrsin();


	if(CURR_STAGE == NumStage['Pre_Flop']):
		# always call in Pre_Flop
		Call()

	elif(CURR_STAGE == NumStage['Flop']):
		if(DEBUG):
			print "GAME: Entering Flop Stage ..."


		[best_hand, hand_comp, hand_odds, high_card, one_pair, two_pairs, sett, straight, flush, full_house, four_of_kind, straight_flush] = AnalyzCards(MyPlayer.hole[0],MyPlayer.hole[1], NumStage['Flop']);

		if(hand_comp and (best_hand >= NumRank['set'])):
			# BET ALL
			if(10*random() < 3):
				rise_amt = 0;
				r = MinRise(NumStage['Flop']);
				rise_amt = r + 1;
				if(MyPlayer.money_left > rise_amt):
					Rise(rise_amt);
				else:
					Call();
			else:
				Call();
		elif(call_cost == 0):
			if(DEBUG):
					print "GAME: Flop :call_cost = 0"
			Call();
		else:
			
			if(hand_comp and (best_hand >=  NumRank['two_pairs'])):
				# call
				Call();
				if(DEBUG):
					print "GAME: Flop :two_pairs"
			elif(hand_comp and best_hand == NumRank['one_pair'] and plrs_in <= 3):
				Call();
				if(DEBUG):
					print "GAME: Flop :one_pair"
			elif(hand_comp and (best_hand >= NumRank['one_pair']) and (straight or flush)):
				Call();
			elif(high_card  and plrs_in <=2):
				if(10*random() < 4):
					Fold();
				else:
					Call();
			elif(straight or flush):
				# call - need to see outs
				# call 0 if possible
				pot_odds = PotOdds(Game.main_pot, call_cost, plrs_in);
				if(DEBUG):
					print "GAME: pot_odds = %d, hand_odds = %d" %(pot_odds, hand_odds)
				if(pot_odds < hand_odds):
					Call();
				else:
					Fold();
			else:
				Fold()
		
	elif(CURR_STAGE == NumStage['Fourth_Street']):
		

		[best_hand, hand_comp, hand_odds, high_card, one_pair, two_pairs, sett, straight, flush, full_house, four_of_kind, straight_flush] = AnalyzCards(MyPlayer.hole[0],MyPlayer.hole[1], NumStage['Fourth_Street']);
		
		if(hand_comp and (best_hand >= NumRank['set'])):
			# BET ALL
			if(10*random() < 4):
				rise_amt = 0;
				r = MinRise(NumStage['Fourth_Street']);
				rise_amt = r + 1;
				if(MyPlayer.money_left > rise_amt):
					Rise(rise_amt);
				else:
					Call();
			else:
				Call();
		elif(call_cost == 0):
			Call();
		else:
			
			if(hand_comp and (best_hand >=  NumRank['two_pairs'])):
				# call
				Call();
			elif(hand_comp and best_hand == NumRank['one_pair'] and plrs_in <= 3):
				Call();
			elif(high_card and plrs_in <=2):
				Call();
			elif(straight or flush):
				# call - need to see outs
				# call 0 if possible
				pot_odds = PotOdds(Game.main_pot, call_cost, plrs_in);
				if(DEBUG):
					print "GAME: pot_odds = %d, hand_odds = %d" %(pot_odds, hand_odds)
				if(pot_odds < hand_odds):
					Call();
				else:
					Fold();
			else:
				Fold()
		

	elif(CURR_STAGE == NumStage['Fifth_Street']):


		[best_hand, hand_comp, hand_odds, high_card, one_pair, two_pairs, sett, straight, flush, full_house, four_of_kind, straight_flush] = AnalyzCards(MyPlayer.hole[0],MyPlayer.hole[1], NumStage['Fifth_Street']);

		if(hand_comp and (best_hand > NumRank['straight'])):
			#call
			if(10*random() < 7):
				Call();
			else:
				rise_amt = 0;
				r = MinRise(NumStage['Fifth_Street']);
				rise_amt = r + 1;
				if(MyPlayer.money_left > rise_amt):
					Rise(rise_amt);
				else:
					Call();
		elif(hand_comp and (best_hand >= NumRank['set'])):
			Call();
		elif(call_cost == 0):
			Call();
		elif(hand_comp and (best_hand > NumRank['one_pair'])):
			Call();
		elif(hand_comp and (best_hand >= NumRank['one_pair']) and plrs_in <=2):
			Call();
		elif(high_card and plrs_in <=2):
			Call()
		else:
			Fold();

elif(Game.state == NumState['analyz']):
	# END OF CURRENT DEAL:
	# remove gm_deal
	# remove gm_state
	
	# calculate plarsin
	if(os.path.isfile(gm_plrsin)):
		#file present
		f = open(gm_plrsin, 'w')
		st = LoadStage(NumStage['Pre_Flop']);
		plrsfold = 0;
		for i in range(6):
			if(st[i][2] == -1):
				#if folded befor preflop
				plrsfold = plrsfold + 1;
		plrsin = 6 - plrsfold;
		f.write(str(plrsin));
		f.close()
	else:
		f = open(gm_plrsin, 'w');
		f.write('6');
		f.close()
		
	

	if(DEBUG):
		print "GAME: Analyz state"
		print "GAME: Analyz ...plrsin = %d" %plrsin
	if(os.path.isfile(gm_deal)):
		os.remove(gm_deal);
	if(os.path.isfile(gm_state)):
		os.remove(gm_state);
