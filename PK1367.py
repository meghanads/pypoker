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
from enum import *
import os
import os.path



# cost of call
coc = 0;

# projected size of pot
proj_sop = 0;

# win-rate
win_rate = coc*sqrt(proj_sop);

# calling decision
call_dec = Enum('showdown','next_bet_round');

# decision
decision = Enum('fold', 'call', 'raise');

# stages in game
stage= Enum('Pre_Flop', 'Flop', 'Fourth_Street', 'Fifth_Street', 'Show_Down');

NameStage = { 1 : 'Pre_Flop', 2 : 'Flop', 3 : 'Fourth_Street', 4 : 'Fifth_Street', 5 : 'Show_Down'};
NumStage = { 'Pre_Flop' : 1, 'Flop' : 2, 'Fourth_Street' : 3, 'Fifth_Street' : 4 , 'Show_Down' : 5};

# Rank of hand:
rank = Enum('one_pair', 'two_pairs', 'set', 'straight', 'flush', 'full_house', 'four_of_kind', 'straight_flush', 'royal_flush');

# Characteristics of opponents
opp_charc = Enum('bluff', 'simple', 'agressive');



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
NW_GAME = 0;

class PyGame:
	
	def _init_(self):
		self.smallblind = 0;
		self.bigblind = 0;
		self.dealer = 0;
		self.main_pot = 0;		# pot of game
		self.stage = 0;
		self.min_raise = 0;
		self.new_deal = 0;	# is it new deal??
		self.deal_num = 0;	# deal number
		self.new_game = 0;

		self.card = [0,0,0,0,0,0,0];	# cards can be seen by me

		# is new game?
		if(os.path.isfile('megh_game')):
			# game already started...
			self.new_game = 0;

		else:
			# game just started
			# remove player_stat files if exists
			if(os.path.isfile('megh_player1_stat'):
					os.remove('megh_player1_stat');

			if(os.path.isfile('megh_player2_stat'):
					os.remove('megh_player2_stat');

			if(os.path.isfile('megh_player3_stat'):
					os.remove('megh_player3_stat');

			if(os.path.isfile('megh_player4_stat'):
					os.remove('megh_player4_stat');

			if(os.path.isfile('megh_player5_stat'):
					os.remove('megh_player5_stat');

			f = open('megh_game','w');
			f.write(str(0));
			f.write('\n');
			f.close();

			self.new_game = 1;

								
	



		# is it new deal??
		if(os.path.isfile('megh_deal')):
			# if file exists... old deal
			self.new_deal = 0;	# old deal
			f = open('megh_deal','r');
			lin = f.readline();
			self.deal_num = int(lin.strip());

			

		else:
			# new deal
			# find deal num
			self.new_deal = 1;
			f = open('deals_money.txt');
			lin = f.readline();
			fwords = lin.split(' ');
			w = fwords[1];
			self.deal_num = int(w.strip());
			f.close();

			f = open('megh_deal', 'w');
			f.write(str(self.deal_num));
			f.write('\n');
			f.close();

		
		f = open('deal.txt', 'r');
		lin = f.readline();
		fwords = lin.split(' ');
		w = fwords[1];
		self.dealer = int(w.strip());
		self.smallblind = (self.delear+1)%7;
		self.bigblind = (self.delear+2)%7;

		lin = f.readline();
		fwords = lin.split(' ');
		w = fwords[1];
		self.stage = NumStage[w.strip()];

		lin = f.readline();
		fwords = lin.split(' ');
		w = fwords[1];
		self.main_pot = int(w.strip());

		NW_DEAL = self.new_deal;
		NW_GAME = self.new_game;

		




# Player details:
#	Holds Player specific info

class My_Player :

	def _init_(self) :
		self.money = 0;
		self.mypos = 0;		# my position in game
		self.hole = [0,0];	# hole cards
		self.money_spent = 0;	# money spent in current deal
		self.coc = 0;		# cost of call
		self.load_status();

		
	def load_status(self) :	# load saved status
		if(not NW_DEAL):
			# old deal : load details of player from -> megh_deal

		else:
			# new deal : load details from -> inputf.txt, deals_money.txt
			f = open('inputf.txt', 'r');
			lin = f.readline();
			fwords = lin.split(' ');
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

			f = open('deals_money.txt', 'r');
			for i in range(self.mypos):
				lin = f.readline();
			lin = f.readline();
			fwords = lin.split(' ');
			w =fwords[1];
			self.money = int(w.strip());









			

	def outs(self) :	# evaluating self's hand
		# 1. Counting outs - cards still in deck that can give potentially winning hand
		# http://www.youtube.com/watch?v=D96gUcTNlxs

	
	def odds(self) :







	def Action :






# Other Player details:

class Other_Player :

	def _init_(self):
		self.charac = 0;
		self.load_status();

	def load_status(self) :	# load saved status








# START THE GAME ...


Game = PyGame();
MyPlayer = MY_Player();
Player1 = Other_Player('megh_opp1');	# player to my left
Player2 = Other_Player('megh_opp2');
Player3 = Other_Player('megh_opp3');
Player4 = Other_Player('megh_opp4');
Player5 = Other_Player('megh_opp5');	# player to my right



