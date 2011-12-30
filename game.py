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
		fwords = lin.split();
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


# Other Player details:
#
# px_stat file
# ============================================================
# charac						plr_charac1	plr_charac2		plr_charac3		plr_charac4
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
		global SM_BLIND
		global BG_BLIND
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
			info_pre = LoadBet(NumStage['Pre_Flop'],self.pos);
			info_flop = LoadBet(NumStage['Flop'],self.pos);
			info_fourth = LoadBet(NumStage['Fourth_Street'],self.pos);
			info_fifth = LoadBet(NumStage['Fifth_Street'],self.pos);

			# pre:

			[best_hand, hand_comp, hand_odds, high_card, one_pair, two_pairs, sett, stright, flush, full_house, four_of_kind, stright_flush] = AnalyzCards(self.hole[0],self.hole[1], NumStage['Pre_Flop']);

			fcharac = 1;
			if(len(info_pre)):
				# if player not folded
				if(best_hand == NumRank['one_pair']):
					if(self.pos != SM_BLIND or self.pos != BG_BLIND):
						for i in range(len(info_pre)-1):
							if((info_pre[i][0] >= info_pre[i+1][0]) and (info_pre[i][1] >= info_pre[i+1][1])):
								pass
							else:
								fcharac = 0
								
						if(fcharac):
							self.plr_charac1 = NumCharac['agressive'];
					else:
						self.plr_charac1 = NumCharac['unknown'];
			else:
				self.plr_charac1 = NumCharac['unknown'];

			
			#flop:

			[best_hand, hand_comp, hand_odds, high_card, one_pair, two_pairs, sett, stright, flush, full_house, four_of_kind, stright_flush] = AnalyzCards(self.hole[0],self.hole[1], NumStage['Flop']);

			fcharac = 1;
			if(len(info_flop)):
				# if player not folded
				if(best_hand == NumRank['one_pair']):
					if(self.pos != SM_BLIND or self.pos != BG_BLIND):
						for i in range(len(info_flop)-1):
							if((info_flop[i][0] >= info_flop[i+1][0]) and (info_flop[i][1] >= info_flop[i+1][1])):
								pass
							else:
								fcharac = 0
								
						if(fcharac):
							self.plr_charac2 = NumCharac['agressive'];
					else:
						self.plr_charac2 = NumCharac['unknown'];
			else:
				self.plr_charac2 = NumCharac['unknown'];
			
			#fourth:

			[best_hand, hand_comp, hand_odds, high_card, one_pair, two_pairs, sett, stright, flush, full_house, four_of_kind, stright_flush] = AnalyzCards(self.hole[0],self.hole[1], NumStage['Fourth_Street']);

			fcharac = 1;
			if(len(info_fourth)):
				# if player not folded
				if(best_hand == NumRank['one_pair']):
					if(self.pos != SM_BLIND or self.pos != BG_BLIND):
						for i in range(len(info_fourth)-1):
							if((info_fourth[i][0] >= info_fourth[i+1][0]) and (info_fourth[i][1] >= info_fourth[i+1][1])):
								pass
							else:
								fcharac = 0
								
						if(fcharac):
							self.plr_charac3 = NumCharac['agressive'];
					else:
						self.plr_charac3 = NumCharac['unknown'];
			else:
				self.plr_charac3 = NumCharac['simple'];


			#fifth:

			[best_hand, hand_comp, hand_odds, high_card, one_pair, two_pairs, sett, stright, flush, full_house, four_of_kind, stright_flush] = AnalyzCards(self.hole[0],self.hole[1], NumStage['Fifth_Street']);

			fcharac = 1;
			if(len(info_fifth)):
				# if player not folded
				if(best_hand == NumRank['one_pair']):
					if(self.pos != SM_BLIND or self.pos != BG_BLIND):
						for i in range(len(info_fifth)-1):
							if((info_fifth[i][0] >= info_fifth[i+1][0]) and (info_fifth[i][1] >= info_fifth[i+1][1])):
								pass
							else:
								fcharac = 0
								
						if(fcharac):
							self.plr_charac4 = NumCharac['agressive'];
					else:
						self.plr_charac4 = NumCharac['unknown'];
			else:
				self.plr_charac4 = NumCharac['unknown'];


			# append charac:
			f = open(stat_fname, 'r')
			lins = f.readlines()
			for i in range(1,5):
				lins[i] = lins[i].strip()
			

			lins[1] = lins[1] + ' ' +str(self.plr_charac1) + '\n'
			lins[2] = lins[2] + ' ' +str(self.plr_charac2) + '\n'
			lins[3] = lins[3] + ' ' +str(self.plr_charac3) + '\n'
			lins[4] = lins[4] + ' ' +str(self.plr_charac4) + '\n'

			# update charac:

			f.close()

			f = open(stat_fname, 'w')
			f.writelines(lins)
			f.close();

			# recalculate carac :

			f = open(stat_fname, 'r')
			lins = f.readlines()
			for i in range(1,5):
				lins[i] = lins[i].strip()
				
			lpre = lins[1].split()
			lfold = lins[2].split()
			lfour = lins[3].split()
			lfive = lins[4].split()

			for i in range(len(lpre)):
				lpre[i] = int(lpre[i])
				lfold[i] = int(lfold[i])
				lfour[i] = int(lfour[i])
				lfive[i] = int(lfive[i])

			charc = [0,0,0,0,0,0]
			charc[1] = lpre.count(NumCharac['unknown']);
			charc[2] = lpre.count(NumCharac['bluff']);
			charc[3] = lpre.count(NumCharac['simple']);
			charc[4] = lpre.count(NumCharac['agressive']);
			charc[5] = lpre.count(NumCharac['smart']);
			
			self.plr_charac1 = charc.index(max(charc));


			charc = [0,0,0,0,0,0]
			charc[1] = lfold.count(NumCharac['unknown']);
			charc[2] = lfold.count(NumCharac['bluff']);
			charc[3] = lfold.count(NumCharac['simple']);
			charc[4] = lfold.count(NumCharac['agressive']);
			charc[5] = lfold.count(NumCharac['smart']);
			
			self.plr_charac2 = charc.index(max(charc));

			charc = [0,0,0,0,0,0]
			charc[1] = lfour.count(NumCharac['unknown']);
			charc[2] = lfour.count(NumCharac['bluff']);
			charc[3] = lfour.count(NumCharac['simple']);
			charc[4] = lfour.count(NumCharac['agressive']);
			charc[5] = lfour.count(NumCharac['smart']);
			
			self.plr_charac3 = charc.index(max(charc));


			charc = [0,0,0,0,0,0]
			charc[1] = lfive.count(NumCharac['unknown']);
			charc[2] = lfive.count(NumCharac['bluff']);
			charc[3] = lfive.count(NumCharac['simple']);
			charc[4] = lfive.count(NumCharac['agressive']);
			charc[5] = lfive.count(NumCharac['smart']);
			
			self.plr_charac4 = charc.index(max(charc));

			f = open(stat_fname,'r')
			lins = f.readlines()
			lins[0] = str(self.plr_charac1)+ ' '+ str(self.plr_charac2)+ ' ' +str(self.plr_charac3)+ ' '+str(self.plr_charac4) + '\n'
			f.close()

			f = open(stat_fname, 'w')
			f.writelines(lins)
			f.close()



		if(DEAL_NUM == 1):
			# stat file does not exists - New game
			self.plr_charac1 = NumCharac['unknown'];
			self.plr_charac2 = NumCharac['unknown'];
			self.plr_charac3 = NumCharac['unknown'];
			self.plr_charac4 = NumCharac['unknown'];
			f = open(stat_fname, 'w')
			s = str(self.plr_charac1)+ ' '+ str(self.plr_charac2)+ ' ' +str(self.plr_charac3)+ ' '+str(self.plr_charac4) + '\n'
			f.write(s);
			f.write('0')
			f.write('\n')
			f.write('0')
			f.write('\n')
			f.write('0')
			f.write('\n')
			f.write('0')
			f.write('\n')
			f.close();


		elif(DEAL_NUM > 1):
			# stat file already exists
			# load statistics
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


def LoadBet(stage,posn):
	# load bet 
	#[act , val]
	# returns empty list if has player folded before this stage
	ret = [];
	folded = 0;
	act = 0;
	val = 0;
	f = open(gv_deal, 'r');
	lin = f.readline();
	w = lin.strip();
	while(w != NameStage[stage]):
		lin = f.readline();
		if(not lin):
			# stage not reached:
			if(DEBUG):
				print "LoadBet: stage not reached"
			return ret
		
		w = lin.strip();
	if(NameStage[stage] != 'Pre_Flop'):
		lin = f.readline();	#dummy
	lin = f.readline();		#dummy2

	lin = f.readline();
	w = lin.strip();
	while(w != 'End'):
		plr = 1;
		fld = 1;
		ws = lin.split();
		for i in range(len(ws)):
			if(ws[i].strip() == '-'):
				if(posn == plr):
					return ret
				plr = plr + 1;
				fld = 1
			else:
				if(plr == posn):
					act = NumPlrAct[ws[i].strip()];
					val = int(ws[i+1].strip());
					break;
				if(fld ==1):
					fld = 2;
				elif(fld ==2):
					plr = plr + 1;
					fld = 1;
		ret.append([act,val]);
		lin = f.readline()
		w = lin.strip();
	return ret;



def EOF(name):
	if(not name):
		print "ERROR: File ended ... File not in correct format"
		exit(1)
	else:
		return 0;


# outs:
NumOuts = {'flush_draw' : 9, 'stright_draw' : 8, 'stright_or_flush_draw' : 12, 'stright_flush_draw' : 17};
NameOuts = {9 : 'flush_draw', 8 : 'stright_draw', 12 : 'stright_or_flush_draw',17 : 'stright_flush_draw'};



def AnalyzCards(hole1, hole2, stage):
	# what best can be formed by cards, return rank of corr hand
	# hand_comp = true if hand is already completed.
	# returns [best_hand, hand_comp, card_odds, high_card, one_pair, two_pairs, sett, stright, flush, full_house, four_of_kind, stright_flush]
	best_hand = 0;	# best hand that is already complete at this stage
	hand_comp = 0;
	hand_odds = 0; # 0 = invalid
	one_pair = 0;
	two_pairs = 0;
	sett = 0;
	stright = 0;
	flush = 0;
	full_house = 0;
	four_of_kind = 0;
	stright_flush = 0;
	high_card = 0;
	flush_draw = 0; # is it flush draw
	stright_draw = 0;
	stright_flush_draw = 0;

	if(stage == NumStage['Pre_Flop']):
		if(CardVal(hole1) >=10 or CardVal(hole2) >=10):
			# high cards?
			best_hand = NumRank['high_card'];
			high_card = 1
		if(SuitNum(hole1) == SuitNum(hole2)):
			#flush?
			flush = 1;
		if(abs(CardVal(hole1) - CardVal(hole2)) == 1):
			#stright?
			stright = 1
		if((abs(CardVal(hole1) - CardVal(hole2)) == 1) and (SuitNum(hole1) == SuitNum(hole2))):
			#stright + flush?
			stright_flush = 1;
		if(CardVal(hole1) == CardVal(hole2)):
			#pair?
			best_hand = NumRank['one_pair']
			one_pair = 1;
		if(DEBUG):
			print "AnalyzCards: Pre_Flop stage ..."

		ret = [best_hand, hand_comp, hand_odds, high_card, one_pair, two_pairs, sett, stright, flush, full_house, four_of_kind, stright_flush];
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

		# stright?
		for i in range(len(vcount) - 4):
			win = vcount[i:(i+5)]
			if(win.count(0) == 0):
				stright = 1;
				break
			else:
				stright = 0

			

			
		if(stright):
			if(max(scount)== 5):
				# stright flush
				stright_flush = 1;
				hand_comp = 1;
				best_hand = NumRank['stright_flush'];
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
			if(stright):
				#stright:
				hand_comp = 1;
				best_hand = NumRank['stright'];

		if( not hand_comp):
			if(max(vcount) == 2):
				#pair
				one_pair = 1;
				hand_comp = 0;	# nxt two cards can form two pairs or set or full house	
				best_hand = NumRank['one_pair'];
			if(vcount.count(2) == 2):
				#two_pairs
				two_pairs = 1;
				hand_comp = 0; # nxt two cards can form full house, calc odds
				best_hand = NumRank['two_pairs'];
			if(max(vcount) == 3):
				#set
				sett = 1;
				hand_comp == 0;	# next two cards may form full house, calc odds
				best_hand = NumRank['set'];
					
			if(max(scount)  == 4):
				# can be flush
				flush = 1;
				flush_draw = 1;

			# can be stright?
			for i in range(len(vcount) - 4):
				win = vcount[i:(i+5)]
				if(win.count(0)>1):
					stright = 0;
					stright_draw = 0;
				else:
					stright = 1
					stright_draw = 1
					stright_indx = i
					break

			# can be stright flush?
			if(stright and flush):
				for  i in range(4):
					if(sum(suit_flag[i]) == 4):
						sut = i
						break

				for i in range(stright_indx, stright_indx+5):
					if(vcount[i]):
						if(not suit_flag[sut][i]):
							stright_flush_draw = 0;
							break
						else:	
							stright_flush_draw = 1;
							stright_flush = 1

		# calc odds of possible	best hand				
				
		if(stright_flush_draw):
			hand_odds = TwoCardOdds[NumOuts['stright_flush_draw']];
		elif(flush_draw and stright_draw):
			hand_odds = TwoCardOdds[NumOuts['stright_or_flush_draw']];
		elif(flush_draw):
			hand_odds = TwoCardOdds[NumOuts['flush_draw']];
		elif(stright_draw):
			hand_odds = TwoCardOdds[NumOuts['stright_draw']];


		ret = [best_hand, hand_comp, hand_odds, high_card, one_pair, two_pairs, sett, stright, flush, full_house, four_of_kind, stright_flush];

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

		# stright?
		for i in range(len(vcount) - 4):
			win = vcount[i:(i+5)]
			if(win.count(0) == 0):
				stright = 1;
				break
			else:
				stright = 0

			
		if(stright):
			if(max(scount)== 5):
				# stright flush
				stright_flush = 1;
				hand_comp = 1;
				best_hand = NumRank['stright_flush'];
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
			if(stright):
				#stright:
				hand_comp = 1;
				best_hand = NumRank['stright'];

		if( not hand_comp):
			if(max(vcount) == 2):
				#pair
				one_pair = 1;
				hand_comp = 0;	# nxt two cards can form two pairs or set or full house	
				best_hand = NumRank['one_pair'];
			if(vcount.count(2) == 2):
				#two_pairs
				two_pairs = 1;
				hand_comp = 0; # nxt two cards can form full house, calc odds
				best_hand = NumRank['two_pairs'];
			if(max(vcount) == 3):
				#set
				sett = 1;
				hand_comp == 0;	# next two cards may form full house, calc odds
				best_hand = NumRank['set'];
					
			if(max(scount)  == 4):
				# can be flush
				flush = 1;
				flush_draw = 1;

			# can be stright?
			for i in range(len(vcount) - 4):
				win = vcount[i:(i+5)]
				if(win.count(0)>1):
					stright = 0;
					stright_draw = 0;
				else:
					stright = 1
					stright_draw = 1
					stright_indx = i
					break

			# can be stright flush?
			if(stright and flush):
				for  i in range(4):
					if(sum(suit_flag[i]) == 4):
						sut = i
						break

				for i in range(stright_indx, stright_indx+5):
					if(vcount[i]):
						if(not suit_flag[sut][i]):
							stright_flush_draw = 0;
							break
						else:	
							stright_flush_draw = 1;
							stright_flush = 1
				
		if(stright_flush_draw):
			hand_odds = TwoCardOdds[NumOuts['stright_flush_draw']];
		elif(flush_draw and stright_draw):
			hand_odds = TwoCardOdds[NumOuts['stright_or_flush_draw']];
		elif(flush_draw):
			hand_odds = TwoCardOdds[NumOuts['flush_draw']];
		elif(stright_draw):
			hand_odds = TwoCardOdds[NumOuts['stright_draw']];


		ret = [best_hand, hand_comp, hand_odds, high_card, one_pair, two_pairs, sett, stright, flush, full_house, four_of_kind, stright_flush];

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

		# stright?
		for i in range(len(vcount) - 4):
			win = vcount[i:(i+5)]
			if(win.count(0) == 0):
				stright = 1;
				break
			else:
				stright = 0

			

			
		if(stright):
			if(max(scount)== 5):
				# stright flush
				stright_flush = 1;
				hand_comp = 1;
				best_hand = NumRank['stright_flush'];
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
			if(stright):
				#stright:
				hand_comp = 1;
				best_hand = NumRank['stright'];

		if( not hand_comp):
			if(max(vcount) == 3):
				#set
				sett = 1;
				hand_comp == 1;	# next two cards may form full house, calc odds
				best_hand = NumRank['set'];
		if( not hand_comp):		
			if(vcount.count(2) == 2):
				#two_pairs
				two_pairs = 1;
				hand_comp = 1; # nxt two cards can form full house, calc odds
				best_hand = NumRank['two_pairs'];
		if( not hand_comp):
			if(max(vcount) == 2):
				#pair
				one_pair = 1;
				hand_comp = 1;	# nxt two cards can form two pairs or set or full house	
				best_hand = NumRank['one_pair'];
											

		ret = [best_hand, hand_comp, hand_odds, high_card, one_pair, two_pairs, sett, stright, flush, full_house, four_of_kind, stright_flush];

		if(DEBUG):
			print "AnalyzCards: return = %s\n" %ret
		return ret
	else:
		ret = [best_hand, hand_comp, hand_odds, high_card, one_pair, two_pairs, sett, stright, flush, full_house, four_of_kind, stright_flush];



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
	

# pot odds:
def CalcPotOdds():
	# calculate pot odds:
	pass
	

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


# min rise at this stage of game
def MinRise(stage, game):
	# minimum rise:
	if(game.curr_stage == NumStage['Pre_Flop']):
		#find
		pass


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
	f = open(gv_outputf)
	f.write(str(amt))
	f.close()
	

		


# START THE GAME ...


Game = PyGame();
MyPlayer = My_Player();
#Player1 = Other_Player(stat_fname = p1_stat, posn = (NxtPlayer(MyPlayer.mypos)));	# player to my left
#Player2 = Other_Player(stat_fname = p2_stat, posn = (NxtPlayer(Player1.pos)));	# 
#Player3 = Other_Player(stat_fname = p3_stat, posn = (NxtPlayer(Player2.pos)));	# 
#Player4 = Other_Player(stat_fname = p4_stat, posn = (NxtPlayer(Player3.pos)));	# 
#Player5 = Other_Player(stat_fname = p5_stat, posn = (NxtPlayer(Player4.pos)));	# player to my right


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
	stright = 0;
	full_house = 0;
	flush = 0;
	four_of_kind = 0;
	stright_flush = 0;



	# Play ...

	if(CURR_STAGE == NumStage['Pre_Flop']):

		
		[best_hand, hand_comp, hand_odds, high_card, one_pair, two_pairs, sett, stright, flush, full_house, four_of_kind, stright_flush] = AnalyzCards(MyPlayer.hole[0],MyPlayer.hole[1], NumStage['Pre_Flop']);

		if(flush or stright or one_pair or (best_hand >= NumRank['high_card'])):
			# CALL
			Call()
		else:
			#FOLD
			Fold()

	elif(CURR_STAGE == NumStage['Flop']):


		[best_hand, hand_comp, hand_odds, high_card, one_pair, two_pairs, sett, stright, flush, full_house, four_of_kind, stright_flush] = AnalyzCards(MyPlayer.hole[0],MyPlayer.hole[1], NumStage['Flop']);
		if(hand_comp and (best_hand >= NumRank['set'])):
			# BET ALL
			Call()
		elif(best_hand >= NumRank['one_pair']):
			# call
			Call()
		elif(sett or stright or flush or two_pairs or full_house or four_of_kind or stright_flush):
			# call - need to see outs
			# call 0 if possible
			Call()
		else:
			#fold
			Fold()
		
	elif(CURR_STAGE == NumStage['Fourth_Street']):
		

		[best_hand, hand_comp, hand_odds, high_card, one_pair, two_pairs, sett, stright, flush, full_house, four_of_kind, stright_flush] = AnalyzCards(MyPlayer.hole[0],MyPlayer.hole[1], NumStage['Fourth_Street']);
		if(hand_comp and (best_hand >= NumRank['set'])):
			#bet
			Call()
		elif(stright and flush):
			#call
			Call()
		else:
			#fold
			Fold()

	elif(CURR_STAGE == NumStage['Fifth_Street']):


		[best_hand, hand_comp, hand_odds, high_card, one_pair, two_pairs, sett, stright, flush, full_house, four_of_kind, stright_flush] = AnalyzCards(MyPlayer.hole[0],MyPlayer.hole[1], NumStage['Fifth_Street']);
		if(hand_comp and (best_hand >= NumRank['set'])):
			#call
			Call()
		else:
			#fold
			Fold()

elif(Game.state == NumState['analyz']):
	# END OF CURRENT DEAL:
	# remove gm_deal
	# remove gm_state
	if(DEBUG):
		print "GAME: Analyz state"
	if(os.path.isfile(gm_deal)):
		os.remove(gm_deal);
	if(os.path.isfile(gm_state)):
		os.remove(gm_state);
