#include<fstream>
#include<iostream>
#include<cstdlib>
using namespace std;

int main() {
	
	srand (getpid());
	int out = 0;
	//cout << "Program!!!"<<endl;
	if (rand() / RAND_MAX < 0.5) {
		out = 10;
	}
	ofstream myfile;
	myfile.open ("outputf.txt");
	myfile << out;
	myfile.close();
	return 0;
	
}
