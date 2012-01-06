#include<fstream>
#include<iostream>
#include<cstdlib>
using namespace std;

int main() {
	
	srand (time(NULL));
	int out = 0;
	//cout << "Program!!!"<<endl;
	int k = rand() % 3;
	cout << "-------------------- " << k << "\n";
	if (k == 0) {
		out = -10;
	}
	else if (k == 1) {
		out = 0;
	}
	else out = 10;
	ofstream myfile;
	myfile.open ("outputf.txt");
	myfile << out;
	myfile.close();
	return 0;
	
}
