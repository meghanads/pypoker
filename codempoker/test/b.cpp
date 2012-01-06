#include<fstream>
#include<iostream>
#include<cstdlib>
using namespace std;

int main() {
	
	ofstream myfile;
	myfile.open ("outputf.txt");
	myfile << "0";
	myfile.close();
	return 0;
	
}
