#################################################
#			*POKER*
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
#		Four of Kind
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
#		shutdown- create best five-card hand possible
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
#	Ref: http://entertainment.howstuffworks.com/poker.htm

from math import *;


# cost of call
coc = 0;

# projected size of pot
proj_sop = 0;

# win-rate
win_rate = coc*sqrt(proj_sop);

# calling descision
call_dec = enum('showdown','next_bet_round');

# stages in game
stage= enum('Pre_Flop', 'Flop', 'Fourth_Street', 'Fifth_Street', 'Show_Down');


# Game info:
#	Holds games status

class PyGame:
	
	def _init_(self):
		self.smallblind = 0;
		self.bigblind = 0;
		




# Player details:
#	Holds Player specific info

class My_Player :

	def _init_(self) :
		self.money = 0;
		self.mypos = 0;		# my position in game
		self.hole = [0,0];	# hole cards

	def Action :






# Other Player details:

class Other_Player :

	def _init_(self):

