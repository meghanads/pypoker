#include <iostream>
#include <fstream>
#include <cstring>

using namespace std;

class my_team
{
	public:
	
		int pos;
		int moneyleft;
		my_team()
		{
			ifstream myfile3;
			myfile3.open("inputf.txt");
			if (myfile3.is_open())
			{
				myfile3 >> pos;
				myfile3 >> pos;
				myfile3 >> pos;
				myfile3 >> moneyleft;
				moneyleft = 1500 - moneyleft;
				myfile3.close();
			}
			else
			{
				cout << "Unable to open inputf.txt" <<  endl;
			}
		}
};

class opp_team
{
	public:
	
		int pos;
		char charac;
		opp_team(int a)
		{
			pos = a;
			charac = 'u';		// characteristic is unknown
			ifstream myfile4;
			myfile4.open("help12222.txt");
			if (myfile4.is_open())
			{
				while (myfile4.eof())		// if help file contains something, it will be put in charac, it cab be 'b' => bluff or 's' => simple
				{
					myfile4 >> charac;
				}
				myfile4.close();
			}
		}
};
			
class game
{
	public:
	
		int smallblind;		// position of small blind
		int bigblind;
		int tocall;
		int minraise;
		game()
		{
			// initialse all the above parameters from the files
		}
		bool is_in_blinds()
		{}
};

// function to calculate probability given the stage

/* stage = 'p' => pre flop stage
   stage = 'f' => flop stage
   stage = 't' => turn stage
   stage = 'r' => river stage
   stage = 's' => show down stage
*/

double prob_cal (char stage)
{
       int card[7];
       int suits[4];
       int denom[13];
       int i;
       for(i=0;i<7;i++)card[i] = 0;
       for(i=0;i<4;i++)suits[i] = 0;
       for(i=0;i<13;i++)denom[i] = 0;
       
       // extract the two cards from inputf.txt file
       ifstream myfile;
       myfile.open("inputf.txt");
       if (myfile.is_open())
       {
          myfile >> card[0] >> card[1];
          myfile.close();
       }
       else
       {
           cout << "inputf.txt file not exists" << endl;
       }
       
       // extract the rest of the cards from deal.txt file
       string temp = "";
       if (stage != 'p')
       {
          myfile.open("deal.txt");
          if (myfile.is_open())
          {
             myfile >> temp;
             while (temp != "Flop") myfile >> temp;
             myfile >> card[2] >> card[3] >> card[4];
             if (stage != 'f')
             {
                myfile >> temp;
                while (temp != "Fourth_Street") myfile >> temp; 
                myfile >> card[5];
                if (stage != 't')
                {
                   myfile >> temp;
                   while (temp != "Fifth_Street") myfile >> temp;
                   myfile >> card[6];
                }
             }
             myfile.close();
          }
          else
          {
              cout << "Unable to open deal.txt" << endl;
          }
       }
       
       // filling the suits and denom array
       int  itemp = 0;  
       for (i=0;i<7;i++)
       {
           if (card[i] != 0)
           {
              itemp = card[i]%13;
              itemp--;
              if (itemp == -1) itemp = 12;
              denom[itemp]++;
           
              itemp = (card[i]-1)/13;
              suits[itemp]++;
           }
       }
       
       double prob = 0;
       // now you have to use some strategy to calculate probability given the cards, suits and denominations
       
       // i have assumed probability to be 0.8
       prob = 0.8
       return prob;
}

int main()
{
    my_team me = new my_team();			// to represent myself
    opp_team opp[5];					// to represent opponents
    game poker = new game();			// to represent the game
    
    int mypos = me.pos;
    int temp, i;
    
    // creating other players 
    // here temp is used for positions of other players
    for(i=1;i<6;i++)
    {
		temp = (mypos + i)%6;
		if (temp == 0) temp = 6;
		opp[i-1] = new opp_team(temp);
	}
	
	// check in which stage the program is called
	ifstream myfile;
	myfile.open("deal.txt");
	
	string str = "";
	char stage = 'p';			// initial stage is assumed as pre flop
    if(myfile.is_open())
    {
		while(myfile.eof())
		{
			myfile >> str;
			if (str == "Flop") stage = 'f';
			else if (str == "Fourth_Street") stage = 't';
			else if (str == "Fifth_Street") stage = 'r';
			else if (str == "Show_Down") stage = 's';
		}
		myfile.close();
	}
	else
	{
		cout << "Unable to open deal.txt" << endl;
	}
    
    // find probability corresponding to the stage
    double prob = prob_cal(stage);
    
    // now take decisions corresponding to the stage and probability of cards
    // these decisions can be very complex like checking other players moves, using help files and many more things
    // here to simplify i have used that if probability > 0.5 and the next player to move is a bluff, i will raise with the minimum otherwise i will call
     
    if (stage == 'p')
    {

			if (opp[0].charac == 'b' && prob > 0.5)
			{
				// print an output of minimum raise in output file if that much amount is there with me otherwise call otherwise fold
				if (me.moneyleft > game.minraise) {}// output min raise
				else if (me.moneyleft > game.tocall) {}// output 0
				else {} // fold 
			}
			else
			{
				if (me.moneyleft > game.tocall) {}// output 0
				else {} // fold 
			}
		}
	}			
	// do it for other stages as well, for showdown analyse the deal.txt and enter in help files
}
				
       

                     
        

