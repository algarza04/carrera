#include <iostream>
#include <vector>
using namespace std;

struct recorrido {
	int cost;
	int col_origen;
};

const int MAXIM = 1000000;

int min(const int a, const int b){
	if (a < b)
	return a;
	else return b;
}

//función que calcula el camino de menor dificultad
int calcularOpt(const vector<vector<int>> &mountain, vector<vector<recorrido>> &cost){
	int fil = mountain.size();
	int col = mountain[0].size();

	//inicializamos la montaña con los valores de la primera fila
	for (int i = 0; i < col; i++)
		cost[0][i] = {mountain[0][i], -1};

	//rellenamos la matriz de costos y almacenamos la dirección origen
	for (int i = 1; i < fil; i++){
		for (int j = 0; j < col; j++){
			int cost_min = cost[i-1][j].cost;
			int col_origen = j;

			if (j > 0 && cost[i-1][j-1].cost < cost_min) {
				cost_min = cost[i-1][j-1].cost;
				col_origen = j - 1;
			}

			if (j < col - 1 && cost[i-1][j+1].cost < cost_min) {
				cost_min = cost[i-1][j+1].cost;
				col_origen = j + 1;
			}

			cost[i][j] = {mountain[i][j] + cost_min, col_origen};
		}
	}	

	// Encontrar el menor costo en la última fila y su posición
	int dif_min = MAXIM;
	int col_min_cost = -1;

	for (int j = 0; j < col; j++){
		if (cost[fil-1][j].cost < dif_min){
			dif_min = cost[fil-1][j].cost;
			col_min_cost = j;
		}
	}

	return dif_min;
}

//función que recupera el camino más corto
vector<int> recuperaCamino(const vector<vector<recorrido>> &cost){
	int fil = cost.size();
	int col = cost[0].size();

	// Encontrar el menor costo en la última fila y su posición
	int dificultad_minima = MAXIM;
	int col_min_cost = -1;
			
	for (int j = 0; j < col; ++j){
		if (cost[fil-1][j].cost < dificultad_minima){
			dificultad_minima = cost[fil-1][j].cost;
			col_min_cost = j;
		}
	}

	// Recuperar el camino desde la base hasta la cumbre
	vector<int> camino(fil);
	int c = col_min_cost;

	for (int i = fil-1; i>= 0; i--){
		camino[i] = c;
		c = cost[i][c].col_origen;
	}

	return camino;
}



void imprimeMatriz(const vector<vector<int>> &mountain){
	for (int i = 0; i < mountain.size(); i++){
		cout << "|";

		for (int j = 0; j < mountain[i].size(); j++){
			cout << " " << mountain[i][j] << " |";
		}

		cout << endl;
	}
}

void imprimeCamino(const vector<vector<int>> &mountain, const vector<int> &camino){
	for (int i = 0; i < mountain.size(); i++){
		cout << "|";

		for (int j = 0; j < mountain[i].size(); j++){
			if (camino[i] == j)
				cout << " " << mountain[i][j] << " |";
			else
				cout << " - |";
		}

		cout << endl;
	}
}

int main(){
	vector<vector<int>> mountain = {
		{2, 8, 9, 5, 8},
		{4, 4, 6, 2, 3},
		{5, 7, 5, 6, 1},
		{3, 2, 5, 4, 8}
	};

	imprimeMatriz(mountain);

	int fil = mountain.size();
	int col = mountain[0].size();

	vector<vector<recorrido>> cost(fil, vector<recorrido>(col, {MAXIM, -1}));

	int dificultad_minima = calcularOpt(mountain, cost);
	cout << "La menor dificultad del recorrido es: " << dificultad_minima << endl;

	vector<int> camino = recuperaCamino(cost);

	cout << "El camino de menor dificultad es: ";
	
	for (int i = camino.size()-1; i >= 0; i--) {
		cout << camino[i];

		if(i != 0)
		cout << "-";
	}

	cout << endl;

	imprimeCamino(mountain, camino);   

	cout << endl;
	return 0;
}
