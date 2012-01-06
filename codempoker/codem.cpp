#include <iostream>
#include <fstream>
#include <cstring>
#include <sys/wait.h>
#include <malloc.h>
#include <algorithm>
#include <vector>


#include "lib/pokerlib.cpp"

#define DEBUG 0
#define MAXLINE 1000
#define LOOPS 1

using namespace std;

fstream myfile;


void change_header_stage (string stage, int potmoney, int dealer) {
	
	ofstream dealfile;
	dealfile.open("deal_header.txt");
	if (dealfile.is_open())
	{
		dealfile << "Dealer   " << dealer << endl;
		dealfile << "Stage    " << "Show_Down" << endl;
		dealfile << "Main_Pot " << potmoney << endl;
		dealfile.close();
	}
}

void prepare_deal_file () {
	
	myfile.close();
	
	string stage = "";
	ofstream dealfile2;
	dealfile2.open ("deal.txt");
	
	ifstream f;

	f.open("deal_header.txt");
	while (!f.eof()) {
		getline (f,stage);
		dealfile2 << stage << endl;
	}
	f.close();

	f.open("deal_help.txt");
	while (!f.eof()) {
		getline (f,stage);
		dealfile2 << stage << endl;
	}
	f.close();	
	dealfile2.close();

	myfile.open("deal_help.txt", ios::out | ios::app);

}


class player {
	public:
	int curstage;
	int curmoney;
	char status;
	int money;
	int card1;
	int card2;
	char** command;

	player () {
		command = NULL;
		curstage = 0;
		curmoney = 0;
		status = 'a';
		money = 1500;
		card1 = 0;
		card2 = 0;
	}

};

// defining players of the game
player p[6];

int deck[52];
int table[5];
int deck_start = 0;


/************************/

bool run_program (int p_num) {

	prepare_deal_file();

	int seconds = 2;

	pid_t child;
	child = fork();

	if (child == -1) {
		printf("Failed to create child \n");
		return -1;
	}

	if (child == 0) {
		//cout << "Child process! "<<endl;
		execv(p[p_num].command[0],p[p_num].command);

	}

	else {
		bool done = false;
		clock_t endwait;
		endwait = clock () + seconds * CLOCKS_PER_SEC ;
		while (clock() < endwait) {
			int st;
			int status = waitpid(child,&st,WNOHANG);
			if (status == child) {
				//cout << "status = " << status <<endl;
				int ret = WIFEXITED (st);
				if (ret != 0) {
					return false;
				}
				done = true;
				break;
			}
		}
		if (!done) {
		
			//TIMEOUT!!!
			//terminate player
			kill (child, SIGKILL);
			return false;
		}
		else {
			return true;
		}
	}
}

char ** tokenize(char* input);

void input_run_commands () {
	char str[1000];
	for (int i=0; i<6; i++) {
		cout << "Command to run code " << (i+1) << " : ";
		cin.getline(str,1000);
		p[i].command = tokenize (str);
	}
}


/*the tokenizer function takes a string of chars and forms tokens out of it*/
char ** tokenize(char* input) {
	int i;

	const char *delim = " \t\n";//the delimiters to separate tokens
	char *token, **tokens;

	tokens = (char **) malloc(MAXLINE*sizeof(char*));

	i = 0;
	if(DEBUG) printf("-- Tokens\n");
	while((token = strtok(input, delim)) !=NULL){
		tokens[i] = (char*)malloc(sizeof(char));
		if(tokens[i] == NULL) {fprintf(stderr, "tokens[%d].",i); perror("Cannot malloc");}
		strcpy(tokens[i], token);
		if(DEBUG) printf("   %d:%s \n",i,tokens[i]);//for debugging
		if(i==0) input = NULL;//input to strtok should be NULL after first call
		i++;
	}
	tokens[i] = NULL;

	return tokens; 
}





/*********************/

int orig_deck[52];

int evaluate_hand (int c1, int c2) {
	int hand[7];
	hand[0] = orig_deck[c1-1];
	hand[1] = orig_deck[c2-1];
	for (int i=2; i<7; i++) hand[i] = orig_deck[table[i-2]-1];
	return eval_7hand(hand);
}


int get_card () {
	//cout<<"Card ";
	deck_start++;
	int card_selected = deck [deck_start-1];
	for (int i=0; i<52; i++) {
		if (orig_deck[i] == card_selected) {
			//cout << i << endl;
			return (i+1);
		}
	}
	cout<<"Error in get_card() "<<endl;
	return -1;
}

void prepare_deck () {
	deck_start = 0;
	init_deck (deck);		
	init_deck (orig_deck);		
	shuffle_deck (deck);
}

void deal_cards (int dealer) {
	dealer = (dealer-1)>=0?(dealer-1):5;
	int end = (dealer-1)>=0?(dealer-1):5;
	int i = dealer;
	//cout << "Dealer " <<dealer << " End " << end<<endl;
	for (int j=0; j<6; j++) {
		if (p[i].money == 0) {
			i = (i+1)%6;
			continue;
		}
		//cout << i << " ";
		p[i].card1 = get_card();
		i = (i+1)%6;
	}
	i = dealer;
	for (int j=0; j<6; j++) {
		if (p[i].money == 0) {
			i = (i+1)%6;
			continue;
		}
		//cout << i << " ";
		p[i].card2 = get_card();
		i = (i+1)%6;
	}
	cout<<endl;
	int burn_card = get_card();
	table[0] = get_card();
	table[1] = get_card();
	table[2] = get_card();
	burn_card = get_card();
	table[3] = get_card();
	burn_card = get_card();
	table[4] = get_card();
}

// function to find the last person to call to end the stage
int find_tc (int pl)
{
    int tc = pl-1;
    tc = (tc<1)?6:tc;         
    int k=0;
    while (1)
    {
        if (p[tc-1].money <= 0 || p[tc-1].status == 'f')
        {
            tc--;
            tc = (tc<1)?6:tc;
        }
        else break;
        k++;
        if (k>6)
        {
            tc = 7;
            break;
        }
    }
    return tc;
}

int find_count ()
{
    int j, count=6;
    for(j=0;j<6;j++)
    if (p[j].curmoney <= 0 || p[j].status == 'f') count--;
    return count;
}

int main()
{
	input_run_commands();
	
	for(int i=0;i<6;i++) {
			p[i].money = 1500;
			p[i].status = 'a';
	}
	
    for(int i=0;i<LOOPS;i++)
    {

		cout<<"Round " << i <<endl;
		int pl, tc, te, tr;
		int potmoney, minraise, stagemoney;

		prepare_deck();

		for (int I=0; I<5; I++) table[I] = 0;

        // find the number of active players and if there is single active player, declare him to win
        int count = 6;
        int j;
        for (j=0;j<6;j++)
        {
            if (p[j].money <=0) count--;
        }
        if (count <= 1) break;


        //chose a dealer
        int dealer = i%6;
        dealer = (dealer==0)?6:dealer;
        while (1)
        {
            if (p[dealer-1].money <= 0)
            {
                dealer++;
                dealer = (dealer==7)?1:dealer;
            }
            else break;
        }
        
		cout << "Dealer chosen : " << dealer <<endl;
    
        // defining file input output streams
        fstream myf;
        ofstream dealfile;
        
        myfile.open("deal_help.txt", ios::out | ios::trunc);
        myfile.close();
        
        // prepare deal.txt file
		change_header_stage ("Pre_Flop", dealer, 0);
        
        // prepare deals_money.txt file
        myfile.open("deals_money.txt", ios::out | ios::trunc);
        if (myfile.is_open())
        {
            myfile << "Deal      " << (i+1) << endl;
            for (j=0;j<5;j++)
            {
                myfile << (j+1) << " " << p[j].money << endl;
            }

            myfile << (j+1) << " " << p[j].money;
            myfile.close();
        }
        
        // initialising potmoney and curmoney of players
        potmoney = 0;
        for (j=0;j<6;j++) 
        {
            p[j].curmoney = 0;
            p[j].status = 'a';
        }
        
        // Pre_Flop stage
        Pre_Flop:
        
        minraise = 10;
        stagemoney = 0;
        for(j=0;j<6;j++) p[j].curstage = 0;
        myfile.open("deal_help.txt", ios::out | ios::app);
        if (myfile.is_open())
        {    
			
			deal_cards (dealer);
			
			myfile << "Pre_Flop" << endl << endl;
			
            // players before small blind
            pl = dealer + 1;
            pl = (pl > 6)?1:pl;
            
            while(1)
            {
                if (p[pl-1].money <= 0)
                {
                    myfile << pl << "    -" << endl;
                    pl++;
                    pl = (pl==7)?1:pl;
                }
                else break;
            }
            
            
            for (int i=0; i<6; i++) {
				cout << p[i].money << " " << p[i].card1 << " " << p[i].card2 << endl;
			}
            
            // small blind
            tr = 5;
            int small_blind_pl = pl;
            if (p[pl-1].money < 5) tr = p[pl-1].money;
            
            p[pl-1].money -= tr;
            stagemoney = tr;
            p[pl-1].curstage = tr;
            potmoney = tr;
            p[pl-1].curmoney = tr;
            
            change_header_stage ("Pre_Flop", potmoney, dealer );
            
            myfile << pl << "    " << "Rise " << tr << endl;
            
            
            // players before big blind
            pl = pl + 1;
            pl = (pl > 6)?1:pl;
            
            while(1)
            {
                if (p[pl-1].money <= 0)
                {
                    myfile << pl << "    -" << endl;
                    pl++;
                    pl = (pl==7)?1:pl;
                }
                else break;
            }
            
            // big blind
            tr = 10;
            int big_blind_pl = pl;
            if (p[pl-1].money < 10) tr = p[pl-1].money;
            
            p[pl-1].money -= tr;
            stagemoney = max (tr, stagemoney);
            p[pl-1].curstage += tr;
            potmoney = max (tr, potmoney);
            p[pl-1].curmoney += tr;
            
			change_header_stage ("Pre_Flop", dealer, 0);            
            
            myfile << pl << "    " << "Rise " << tr;
            
            // finding tc
            tc = find_tc (pl); 
            cout << "Pre_Flop tc = " << tc << endl;
            if (tc == pl || tc == 7) goto Flop;
            
            cout << "Stage Money " << stagemoney << " Pot Money " << potmoney << endl;
            
            bool raised_after_big_blind = false;
            
            while(1)
            {
                pl = pl+1;
                pl = (pl > 6)?1:pl;
                
                // if the player is already fold or has no money, just insert a '-' in deal.txt file
                if (p[pl-1].status == 'f' || p[pl-1].money <= 0)
                {
                    myfile << endl << pl << "    -";
                    continue;
                }
                
                // prepare inputf.txt file
                myf.open ("inputf.txt", ios::out | ios::trunc);
                if (myf.is_open())
                {
                    myf << p[pl-1].card1 << "        " << p[pl-1].card2 << "    " << pl << "    " << p[pl-1].curmoney;
                    myf.close();
                }
                    
                // clear outputf.txt
                myf.open ("outputf.txt", ios::out | ios::trunc);
                if (myf.is_open())
                {
                    myf << "";
                    myf.close();
                }
                
                // call code of player pl if his money is greater than 0 and if he is not fold or if there are atleast two players
                run_program (pl-1);
                
                // read outputf.txt file
                myf.open ("outputf.txt", ios::in);
                if (myf.is_open())
                {
                    myf >> te;
                    myf.close();
                }
             
				cout << "Player " << pl << " : " << te <<endl;
                
                // fold
                if (te == -10)
                {
                    p[pl-1].status = 'f';
                    myfile << endl << pl << "    " << "Fold " << p[pl-1].curstage;
                    myfile.flush();
                    if (find_count() <= 1) goto Flop;
                }
                
                // call
                else if (te == 0)
                {
                    tr = stagemoney;
                    if (p[pl-1].money < (stagemoney - p[pl-1].curstage)) tr = p[pl-1].money + p[pl-1].curstage;
                    myfile << endl << pl << "    " << "Call " << tr;
					myfile.flush();

                    p[pl-1].money -= (tr - p[pl-1].curstage);
                    //potmoney += (tr - p[pl-1].curstage);
                    p[pl-1].curmoney += (tr - p[pl-1].curstage);
                    p[pl-1].curstage = tr;
                    
                }
                
                // rise
                else 
                {
                    if (p[pl-1].money < (te+stagemoney-p[pl-1].curstage)) {
						p[pl-1].status = 'f';
						myfile << endl << pl << "     " << "Fold " << p[pl-1].curstage;
						myfile.flush();
						if (find_count() <= 1) goto Flop;
					}
                    else if(te < minraise && p[pl-1].money > (te+stagemoney-p[pl-1].curstage)) {
						p[pl-1].status = 'f';
						myfile << endl << pl << "     " << "Fold " << p[pl-1].curstage;
						myfile.flush();
						if (find_count() <= 1) goto Flop;
					}
                    else
                    {
						raised_after_big_blind = true;    
                        p[pl-1].money -= (te + stagemoney - p[pl-1].curstage);
                        p[pl-1].curmoney += (te + stagemoney - p[pl-1].curstage);
                        p[pl-1].curstage = stagemoney + te;
                        potmoney = p[pl-1].curmoney;
                        stagemoney += te;
                        minraise = (te>minraise)?te:minraise;
                        
                        change_header_stage ("Pre_Flop", potmoney, dealer);
					
                        myfile << endl << pl << "    " << "Rise " << p[pl-1].curstage;
                        
                        tc = find_tc (pl);
                    }
                }
                
                cout << "PLAYER : money " << p[pl-1].money << " curmoney " << p[pl-1].curmoney << " curstage " << p[pl-1].curstage << " status " << p[pl-1].status <<endl;
                cout << "Stage Money " << stagemoney << " Pot Money " << potmoney << endl;
                
                if (pl == small_blind_pl && !raised_after_big_blind) {
					tc++;
					//cout << "---------" <<endl;
					continue;
				}
                if (tc == pl || tc == 7) goto Flop;
            }
            myfile.close();
        }
        
        // Flop stage
        Flop:
		
		char c;
		cin >> c;
		
		cout << "Stage Money " << stagemoney << " Pot Money " << potmoney << endl;

		for (int y=0; y<6; y++) {
			cout << "PLAYER " << y << " : money " << p[y].money << " curmoney " << p[y].curmoney << " curstage " << p[y].curstage << " status " << p[y].status <<endl;
		}

        
        minraise = 10;
        stagemoney = 0;
        for(j=0;j<6;j++) p[j].curstage = 0;
        
        // prepare deal.txt file
        change_header_stage ("Flop", 0, dealer);
        
        // SHUFFLE cards to get three cards in c1, c2, c3
        int c1 = table[0];
        int c2 = table[1];
        int c3 = table[2];
       
        
        dealfile.open("deal_help.txt", ios::out | ios::app);
        if (dealfile.is_open())
        {
            dealfile << endl<<"End" << endl << endl;
            cout << " !!! End" << endl << endl;
            dealfile << "Flop" << endl;
            dealfile << c1 << "	" << c2 << "	" << c3 << endl << endl;
            dealfile.close();
        }
        
        // if there is a single player or no players with money, then no entry to be done
        if (find_count() <= 1) goto Fourth_Street;
        
        myfile.open("deal_help.txt", ios::out | ios::app);
        if (myfile.is_open())
        {    
            pl = dealer;
            
            tc = find_tc (dealer+1);
            
            cout << "Flop tc = " << tc << endl;
				
            while(1)
            {
				
				cout << "Stage Money " << stagemoney << " Pot Money " << potmoney << endl;
				
                pl = pl+1;
                pl = (pl > 6)?1:pl;
                
                // if the player is already fold or has no money, just insert a '-' in deal.txt file
                if (p[pl-1].status == 'f' || p[pl-1].money <= 0)
                {
                    myfile << endl << pl << "    -";
                    continue;
                }
                
                // prepare inputf.txt file
                myf.open ("inputf.txt", ios::out | ios::trunc);
                if (myf.is_open())
                {
                    myf << p[pl-1].card1 << "        " << p[pl-1].card2 << "    " << pl << "    " << p[pl-1].curmoney;
                    myf.close();
                }
                    
                // clear outputf.txt
                myf.open ("outputf.txt", ios::out | ios::trunc);
                if (myf.is_open())
                {
                    myf << "";
                    myf.close();
                }
                
                // call code of player pl if his money is greater than 0 and if he is not fold or if there are atleast two players
                run_program (pl-1);
                
                // read outputf.txt file
                myf.open ("outputf.txt", ios::in);
                if (myf.is_open())
                {
                    myf >> te;
                    myf.close();
                }
                
                cout << "Player " << pl << " : " << te <<endl;
                
                // fold
                if (te == -10)
                {
                    p[pl-1].status = 'f';
                    myfile << endl << pl << "    " << "Fold " << p[pl-1].curstage;
                    myfile.flush();
					if (find_count() <= 1) goto Fourth_Street;
                }
                
                // call
                
                else if (te == 0)
                {
                    tr = stagemoney;
                    if (p[pl-1].money < (stagemoney - p[pl-1].curstage)) tr = p[pl-1].money + p[pl-1].curstage;
                    myfile << endl << pl << "    " << "Call " << tr;
					myfile.flush();

                    p[pl-1].money -= (tr - p[pl-1].curstage);
                    //potmoney += (tr - p[pl-1].curstage);
                    p[pl-1].curmoney += (tr - p[pl-1].curstage);
                    p[pl-1].curstage = tr;
                    
                }
                
                // rise
                else 
                {
                    if (p[pl-1].money < (te+stagemoney-p[pl-1].curstage)) {
						p[pl-1].status = 'f';
						myfile << endl << pl << "     " << "Fold " << p[pl-1].curstage;
						myfile.flush();
						if (find_count() <= 1) goto Flop;
					}
                    else if(te < minraise && p[pl-1].money > (te+stagemoney-p[pl-1].curstage)) {
						p[pl-1].status = 'f';
						myfile << endl << pl << "     " << "Fold " << p[pl-1].curstage;
						myfile.flush();
						if (find_count() <= 1) goto Flop;
					}
                    else
                    {
						    
                        p[pl-1].money -= (te + stagemoney - p[pl-1].curstage);
                        p[pl-1].curmoney += (te + stagemoney - p[pl-1].curstage);
                        p[pl-1].curstage = stagemoney + te;
                        potmoney = p[pl-1].curmoney;
                        stagemoney += te;
                        minraise = (te>minraise)?te:minraise;
                        
                        change_header_stage ("Flop", potmoney, dealer);
					
                        myfile << endl << pl << "    " << "Rise " << p[pl-1].curstage;
                        
                        tc = find_tc (pl);
                    }
                }
                
                
                

				cout << "money " << p[pl-1].money << " curmoney " << p[pl-1].curmoney << " curstage " << p[pl-1].curstage << " status " << p[pl-1].status <<endl;
                
                if (tc == pl || tc == 7) goto Fourth_Street;
            }
            myfile.close();
        }
        
        
        // Forth_Street stage
        Fourth_Street:

		cout << "Stage Money " << stagemoney << " Pot Money " << potmoney << endl;

		for (int y=0; y<6; y++) {
			cout << "PLAYER " << y << " : money " << p[y].money << " curmoney " << p[y].curmoney << " curstage " << p[y].curstage << " status " << p[y].status <<endl;
		}

        
        cout << "FOURTH STREET" <<endl;
        
        minraise = 20;
        stagemoney = 0;
        for(j=0;j<6;j++) p[j].curstage = 0;
        
        // prepare deal.txt file
		change_header_stage ("Fourth_Street", dealer, potmoney);        
        
        // SHUFFLE cards to get a card in c1
        c1 = table[4];
        
        dealfile.open("deal_help.txt", ios::out | ios::app);
        if (dealfile.is_open())
        {
            dealfile << endl << "End" << endl << endl;
            dealfile << "Fourth_Street" << endl;
            dealfile << c1 << endl << endl;
            dealfile.close();
        }
        
        // if there is a single player or no players with money, then no entry to be done
        if (find_count() <= 1) goto Fifth_Street;
        
        myfile.open("deal_help.txt", ios::out | ios::app);
        if (myfile.is_open())
        {    
            pl = dealer;
            tc = find_tc (dealer+1);
            while(1)
            {
                pl = pl+1;
                pl = (pl > 6)?1:pl;
                
                // if the player is already fold or has no money, just insert a '-' in deal.txt file
                if (p[pl-1].status == 'f' || p[pl-1].money <= 0)
                {
                    myfile << endl << pl << "    -";
                    continue;
                }
                
                // prepare inputf.txt file
                myf.open ("inputf.txt", ios::out | ios::trunc);
                if (myf.is_open())
                {
                    myf << p[pl-1].card1 << "        " << p[pl-1].card2 << "    " << pl << "    " << p[pl-1].curmoney;
                    myf.close();
                }
                    
                // clear outputf.txt
                myf.open ("outputf.txt", ios::out | ios::trunc);
                if (myf.is_open())
                {
                    myf << "";
                    myf.close();
                }
                
                // call code of player pl if his money is greater than 0 and if he is not fold or if there are atleast two players
                run_program (pl-1);
                
                // read outputf.txt file
                myf.open ("outputf.txt", ios::in);
                if (myf.is_open())
                {
                    myf >> te;
                    myf.close();
                }
                
                // fold
                if (te == -10)
                {
                    p[pl-1].status = 'f';
                    myfile << endl << pl << "    " << "Fold " << p[pl-1].curstage;
                    myfile.flush();
					if (find_count() <= 1) goto Fifth_Street;
                }
                                
                // call
                
                else if (te == 0)
                {
                    tr = stagemoney;
                    if (p[pl-1].money < (stagemoney - p[pl-1].curstage)) tr = p[pl-1].money + p[pl-1].curstage;
                    myfile << endl << pl << "    " << "Call " << tr;
					myfile.flush();

                    p[pl-1].money -= (tr - p[pl-1].curstage);
                    //potmoney += (tr - p[pl-1].curstage);
                    p[pl-1].curmoney += (tr - p[pl-1].curstage);
                    p[pl-1].curstage = tr;
                    
                }
                
                // rise
                else 
                {
                    if (p[pl-1].money < (te+stagemoney-p[pl-1].curstage)) {
						p[pl-1].status = 'f';
						myfile << endl << pl << "     " << "Fold " << p[pl-1].curstage;
						myfile.flush();
						if (find_count() <= 1) goto Flop;
					}
                    else if(te < minraise && p[pl-1].money > (te+stagemoney-p[pl-1].curstage)) {
						p[pl-1].status = 'f';
						myfile << endl << pl << "     " << "Fold " << p[pl-1].curstage;
						myfile.flush();
						if (find_count() <= 1) goto Flop;
					}
                    else
                    {
						
                        p[pl-1].money -= (te + stagemoney - p[pl-1].curstage);
                        p[pl-1].curmoney += (te + stagemoney - p[pl-1].curstage);
                        p[pl-1].curstage = stagemoney + te;
                        potmoney = p[pl-1].curmoney;
                        stagemoney += te;
                        minraise = (te>minraise)?te:minraise;
                        
                        change_header_stage ("Fourth_Street", potmoney, dealer);
					
                        myfile << endl << pl << "    " << "Rise " << p[pl-1].curstage;
                        
                        tc = find_tc (pl);
                    }
                }
                cout << "money " << p[pl-1].money << " curmoney " << p[pl-1].curmoney << " curstage " << p[pl-1].curstage << " status " << p[pl-1].status <<endl;
                
                if (tc == pl || tc == 7) goto Fifth_Street;
            }
            myfile.close();
        }
                                                         
                                                         
        // Fifth_Street stage
        Fifth_Street:
                
        minraise = 20;
        stagemoney = 0;
        for(j=0;j<6;j++) p[j].curstage = 0;
        
        // prepare deal.txt file
        change_header_stage ("Fifth_Street" , potmoney, dealer);
        
        // SHUFFLE cards to get a card in c1
        c1 = table[5];
        
        dealfile.open("deal_help.txt", ios::out | ios::app);
        if (dealfile.is_open())
        {
            dealfile << endl<<"End" << endl << endl;
            dealfile << "Fifth_Street" << endl;
            dealfile << c1 << endl << endl;
            dealfile.close();
        }
        
        // if there is a single player or no players with money, then no entry to be done
        if (find_count() <= 1) goto Show_Down;
        
        myfile.open("deal_help.txt", ios::out | ios::app);
        if (myfile.is_open())
        {    
            pl = dealer;
            tc = find_tc (dealer+1);
            while(1)
            {
                pl = pl+1;
                pl = (pl > 6)?1:pl;
                
                // if the player is already fold or has no money, just insert a '-' in deal.txt file
                if (p[pl-1].status == 'f' || p[pl-1].money <= 0)
                {
                    myfile << endl << pl << "    -";
                    continue;
                }
                
                // prepare inputf.txt file
                myf.open ("inputf.txt", ios::out | ios::trunc);
                if (myf.is_open())
                {
                    myf << p[pl-1].card1 << "        " << p[pl-1].card2 << "    " << pl << "    " << p[pl-1].curmoney;
                    myf.close();
                }
                    
                // clear outputf.txt
                myf.open ("outputf.txt", ios::out | ios::trunc);
                if (myf.is_open())
                {
                    myf << "";
                    myf.close();
                }
                
                // call code of player pl if his money is greater than 0 and if he is not fold or if there are atleast two players
                run_program (pl-1);
                
                // read outputf.txt file
                myf.open ("outputf.txt", ios::in);
                if (myf.is_open())
                {
                    myf >> te;
                    myf.close();
                }
                
                // fold
                if (te == -10)
                {
                    p[pl-1].status = 'f';
                    myfile << endl << pl << "    " << "Fold " << p[pl-1].curstage;
					myfile.flush();
                }
                
                // call
                else if (te == 0)
                {
                    tr = stagemoney;
                    if (p[pl-1].money < (stagemoney - p[pl-1].curstage)) tr = p[pl-1].money + p[pl-1].curstage;
                    
                    myfile << endl << pl << "    " << "Call " << tr;
					myfile.flush();        
                    
                    p[pl-1].money -= (tr - p[pl-1].curstage);
                    potmoney += (tr - p[pl-1].curstage);
                    p[pl-1].curmoney += (tr - p[pl-1].curstage);
                    p[pl-1].curstage = tr;
                    
                }
                
                else if (te == 0)
                {
                    tr = stagemoney;
                    if (p[pl-1].money < (stagemoney - p[pl-1].curstage)) tr = p[pl-1].money + p[pl-1].curstage;
                    myfile << endl << pl << "    " << "Call " << tr;
					myfile.flush();

                    p[pl-1].money -= (tr - p[pl-1].curstage);
                    //potmoney += (tr - p[pl-1].curstage);
                    p[pl-1].curmoney += (tr - p[pl-1].curstage);
                    p[pl-1].curstage = tr;
                    
                }
                
                // rise
                else 
                {
                    if (p[pl-1].money < (te+stagemoney-p[pl-1].curstage)) {
						p[pl-1].status = 'f';
						myfile << endl << pl << "     " << "Fold " << p[pl-1].curstage;
						myfile.flush();
						if (find_count() <= 1) goto Flop;
					}
                    else if(te < minraise && p[pl-1].money > (te+stagemoney-p[pl-1].curstage)) {
						p[pl-1].status = 'f';
						myfile << endl << pl << "     " << "Fold " << p[pl-1].curstage;
						myfile.flush();
						if (find_count() <= 1) goto Flop;
					}
                    else
                    {
						
                        p[pl-1].money -= (te + stagemoney - p[pl-1].curstage);
                        p[pl-1].curmoney += (te + stagemoney - p[pl-1].curstage);
                        p[pl-1].curstage = stagemoney + te;
                        potmoney = p[pl-1].curmoney;
                        stagemoney += te;
                        minraise = (te>minraise)?te:minraise;
                        
                        change_header_stage ("Fifth_Street", potmoney, dealer);
					
                        myfile << endl << pl << "    " << "Rise " << p[pl-1].curstage;
                        
                        tc = find_tc (pl);
                    }
                }
                cout << "money " << p[pl-1].money << " curmoney " << p[pl-1].curmoney << " curstage " << p[pl-1].curstage << " status " << p[pl-1].status <<endl;
                
                if (tc == pl || tc == 7) goto Show_Down;
            }
            myfile.close();
        }
                
         
        
        Show_Down:
        
        cout << "SHOW DOWN" <<endl;
        
		cout << "Stage Money " << stagemoney << " Pot Money " << potmoney << endl;
        
        //Decide who won.
        //Add money to respective players
        
        // prepare deal.txt file
        change_header_stage ("Show_Down", potmoney, dealer);
        
                
        dealfile.open("deal_help.txt", ios::out | ios::app);
        if (dealfile.is_open())
        {
            dealfile << endl << "End" << endl << endl;
            dealfile << "Show_Down" << endl;
            for (int i=0; i<6; i++) {
				if (p[i].curmoney > 0)
				dealfile << (i+1) << "	" << p[i].card1 << "	" << p[i].card2 << endl;
				else
				dealfile << (i+1) << "	" << "-" << endl; 
			}
            
            dealfile.close();
        }
        
        int player_rank[6];
        int player_hand[6];
        
        for (int I=0; I<6; I++) {
			player_rank[I] = 0;
			player_hand[I] = 0;
        }
        
        
        //consider card representations
        
		for (int y=0; y<6; y++) {
			cout << "PLAYER " << y << " : money " << p[y].money << " curmoney " << p[y].curmoney << " curstage " << p[y].curstage << " status " << p[y].status <<endl;
		}

        
        int count2 = 0;
        
        vector<pair<int,int> > rankss (6);
        
        for (int I=0; I<6; I++) {
			player_hand[I] = evaluate_hand (p[I].card1, p[I].card2);
			rankss[I] = make_pair (player_hand[I], I);
		}
        
        sort (rankss.begin(), rankss.end());
        
        for (int I=0; I<6; I++) {
			player_rank[rankss[I].second] = I + 1;
			player_hand[rankss[I].second] = rankss[I].first;
		}
		
		cout << "RANKS"<<endl;
		for (int g=0; g<6; g++) {
			cout << player_rank[g] << " " << player_hand[g] << endl;
		}
		
		//split pot ?
		
		//we now have an array of player_ranks
		int players_gone = 0;
		for (int I=0; I<6; I++) {
			int sum = 0;
			
			//cout << I << " " << p[player_rank[I]-1].curmoney << endl;
			
			int money_that_he_can_win = p[player_rank[I]-1].curmoney ;
			
			if (money_that_he_can_win != 0) {
			
				for (int c=I; c<6; c++) {
					int m2 = p[player_rank[c]-1].curmoney;
					//cout << c << " " << p[player_rank[c]-1].curmoney << endl;
					if (m2 >= money_that_he_can_win) {
						sum += money_that_he_can_win;
						p[player_rank[c]-1].curmoney -= money_that_he_can_win;
					}
					else {
						sum += m2;
						p[player_rank[c]-1].curmoney = 0;
					}
				}
			}
			
			p[player_rank[I]-1].money += sum;
			cout << "Player " << player_rank[I] << " won " << sum << "  |  Money : " << p[player_rank[I]-1].money << endl;
		}
		
		int winner = -1;
		for (int h=0; h<6; h++) {
			if (player_rank[h] == 1) {
				winner = h + 1;
				break;
			}
		}
		
        dealfile.open("deal_help.txt", ios::out | ios::app);
        if (dealfile.is_open())
        {
			dealfile << "Win	" << winner << endl;
			dealfile.close();
		}
		
		for (int I=0; I<6; I++) {
			run_program (i);
		}
		
	}
}
