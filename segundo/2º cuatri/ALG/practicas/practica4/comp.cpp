#include <iostream>
#include <vector>

using namespace std;

const int N = 7; // Tamaño del tablero
const int MAX = 31; 

// Representación del tablero
vector<vector<int>> tablero = {
    {-1, -1,  0,  0,  0, -1, -1},
    {-1, -1,  0,  0,  0, -1, -1},
    { 0,  0,  0,  0,  0,  0,  0},
    { 0,  0,  0,  1,  0,  0,  0},
    { 0,  0,  0,  0,  0,  0,  0},
    {-1, -1,  0,  0,  0, -1, -1},
    {-1, -1,  0,  0,  0, -1}
};

vector<vector<int>> tabl_solucion = {
    {-1, -1,  0,  0,  0, -1, -1},
    {-1, -1,  0,  0,  0, -1, -1},
    { 0,  0,  0,  0,  0,  0,  0},
    { 0,  0,  0,  1,  0,  0,  0},
    { 0,  0,  0,  0,  0,  0,  0},
    {-1, -1,  0,  0,  0, -1, -1},
    {-1, -1,  0,  0,  0, -1, -1}
};

int main(){
	if(tablero == tabl_solucion)
		cout << "true";
	else
		cout << "false";
}
