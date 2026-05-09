#include <iostream>
#include <vector>
using namespace std;

const int N = 7;

vector<vector<int>> tablero = {
	{-1, -1,  1,  1,  1, -1, -1},
	{-1, -1,  1,  1,  1, -1, -1},
	{ 1,  1,  1,  1,  1,  1,  1},
	{ 1,  1,  1,  0,  1,  1,  1},
	{ 1,  1,  1,  1,  1,  1,  1},
	{-1, -1,  1,  1,  1, -1, -1},
	{-1, -1,  1,  1,  1, -1, -1}
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

const vector<pair<int, int>> direcciones = {{-2, 0}, {2, 0}, {0, -2}, {0, 2}};

bool esValido(const vector<vector<int>> &tabl, int f_origen, int c_origen, int f_destino, int c_destino){
	if (f_destino < 0 || f_destino >= N || c_destino < 0 || c_destino >= N)
		return false;

	if (tabl[f_destino][c_destino] == 0){
		//si el mov es horizontal
		if (abs(c_origen - c_destino) == 2 && tabl[f_origen][(c_origen + c_destino) / 2] == 1)
			return true;
		
		//si el mov es vertical
		if (abs(f_origen - f_destino) == 2 && tabl[(f_origen + f_destino) / 2][c_origen] == 1)
			return true;
	}

	return false;
}


void hacerMovimiento(vector<vector<int>> &tabl, int f_origen, int c_origen, int f_destino, int c_destino){
	tabl[f_origen][c_origen] = 0;
	tabl[(f_origen + f_destino) / 2][(c_origen + c_destino) / 2] = 0;
	tabl[f_destino][c_destino] = 1;
}

void deshacerMovimiento(vector<vector<int>> &tabl, int f_origen, int c_origen, int f_destino, int c_destino){
	tabl[f_origen][c_origen] = 1;
	tabl[(f_origen + f_destino) / 2][(c_origen + c_destino) / 2] = 1;
	tabl[f_destino][c_destino] = 0;
}

bool esSolucion(vector<vector<int>> &tabl){
	if (tabl == tabl_solucion)
		return true;
	else
		return false;
}

void imprimirTablero(const vector<vector<int>>& tabl) {
	for (int fil = 0; fil < N; fil++){
		for (int col = 0; col < N; col++)
			cout << tabl[fil][col] << " ";
		
		cout << "\n";
	}
}

vector<vector<int>> backtracking(vector<vector<int>> &tabl){
	if (esSolucion(tabl))	
		return tabl;
		
	for (int i = 0; i < N; i++){
		for (int j = 0; j < N; j++){
			if (tabl[i][j] == 1){
			
				for (auto dir : direcciones){
					int f_destino = i + dir.first;
					int c_destino = j + dir.second;

					if (esValido(tabl, i, j, f_destino, c_destino)){
						hacerMovimiento(tabl, i, j, f_destino, c_destino);
                  
						vector<vector<int>> solucion = backtracking(tabl);
						
						if (!solucion.empty())
							return solucion;
						
						deshacerMovimiento(tablero, i, j, f_destino, c_destino);
					}
				}
			}
		}	
	}

	return {};
}

int main() {
	cout << "Tablero inicial:" << "\n";
	imprimirTablero(tablero);
	
	vector<vector<int>> solucion = backtracking(tablero);
	if (!solucion.empty()){
		cout << "\nSe encontró una solución:" << "\n";
		imprimirTablero(solucion);
	} 
	else 
		cout << "\nNo se encontró ninguna solución." << "\n";
	
	return 0;
}
