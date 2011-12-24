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
from os import *
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

# Rank of hand:
rank = Enum('one_pair', 'two_pairs', 'set', 'straight', 'flush', 'full_house', 'four_of_kind', 'straight_flush', 'royal_flush');

# Characteristics of opponents
opp_charc = Enum('bluff', 'simple', 'agressive');



# Game info:
#	Holds games status

# megh_game
# ===============
# new_game

# megh_deal
# =======================
# new_deal
#
class PyGame:
	
	def _init_(self):
		self.smallblind = 0;
		self.bigblind = 0;
		pot = 0;		# pot of game
		min_raise = 0;
		new_deal = 0;	# is it new deal??
		deal_num = 0;	# deal number
		new_game = 0;

		card = [0,0,0,0,0,0,0];	# cards can be seen by me

		
		# is it new deal??
		
		if(os.path.isfile('megh_deal')):
			# if file exists... old deal

		else:
			# new deal
			

		try:
			# megh_deal -> created at start of each deal and removed on show_down
			f = open('megh_deal');
			break;
		except IOError:
			# file does not exists...new deal just started.
			# cards are unknown
			new_deal = 1;	# new deal
			# find deal num
			f = open('deals_money.txt');
			lin = f.readline();
			fwords = lin.split(' ');
			deal_num = int(fword[1]);

			# in new deal cards are different but players are SAME
			



			just_strarted = 1;

		if(not just_started):
			# read file details and load...

		else:
			# read inputf.txt
			#

			


		self.load_status();


	def load_status(self) :	# load saved status



	


		




# Player details:
#	Holds Player specific info

class My_Player :

	def _init_(self) :
		self.money = 0;
		self.mypos = 0;		# my position in game
		self.hole = [0,0];	# hole cards
		self.coc = 0;		# cost of call
		self.load_status();

		
	def load_status(self) :	# load saved status

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



