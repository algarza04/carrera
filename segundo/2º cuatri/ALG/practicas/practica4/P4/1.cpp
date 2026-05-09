#include <iostream>
#include <vector>
#include <cstdlib>

using namespace std;


int CalculaUnion( const vector<int> &almacen, vector<vector<int>> &preferencia);
bool esta(const vector<int> almacen, int esta);
void imprime(const vector<int> &almacen);
void imprimeMatriz(const vector<vector<int>> &preferencia);
void Backtracking(vector<vector<int>> &preferencia, vector<int>& almacen, int est, int& mejor_valor, vector<int>& asignaciones);


int main(int argc, char *argv[]) {
    int n = 0;
    if (argc != 2 || atoi(argv[1]) <= 0 || atoi(argv[1]) % 2 == 1) {
        cerr << "No has introducido un número válido de argumentos, introduce un argumento con la cantidad de alumnos, tiene que ser par";
        exit(1);
    }
    n = atoi(argv[1]);
    const int semilla = 99;
    vector<vector<int>> preferencia;
    vector<int> almacen;
    int valor = 0;
    vector<int> asignaciones;
    srand(semilla);
 
 
    almacen.resize(n,-1);
    asignaciones.resize(n);
    preferencia.resize(n, vector<int>(n)); // Inicialización de las filas de preferencia

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++)
            preferencia[i][j] = rand()%99 + 1; // Inicializamos el array con randoms del 1 al 99
    }
    
    imprimeMatriz(preferencia);

    Backtracking(preferencia, almacen, 0 , valor, asignaciones);
    
    
    imprime(asignaciones);
    cout << "La suma de la preferencia total es " << valor << endl;   
}

bool esta(const vector<int> almacen, int esta) {
    for (int i = 0; i < almacen.size(); ++i)
        if (almacen[i] == esta)
            return true;
    return false;
}


void imprimeMatriz(const vector<vector<int>> &preferencia){
	for (int i = 0; i < preferencia.size(); i++){
		cout << "|";
		for(int j=0; j < preferencia.size(); j ++){
			if(j==i)
				cout << " -- |";	
			else if (preferencia[i][j] < 10 )
				cout << " 0" << preferencia[i][j] << " |";
			else
				cout << " " << preferencia[i][j] << " |";
		}
	cout << endl;
	}
}

void imprime(const vector<int> &asignaciones){
	for (int i = 0; i < asignaciones.size(); i+=2){
		if(asignaciones[i] < 10)
			cout << "0"<<asignaciones[i] << "  ";
		else
			cout << asignaciones[i] << "  ";
			
		if(asignaciones[i+1] < 10)
			cout << "0" << asignaciones[i+1] << endl;
		else
			cout << asignaciones[i+1] << endl;
	}		
}

int CalculaUnion(const vector<int> &almacen, vector<vector<int>> &preferencia) {
    int valor = 0;
    for (int i = 0; i < almacen.size(); i+=2) {
        int estudiante_i = almacen[i];
        int estudiante_j = almacen[i+1];
        valor += preferencia[estudiante_i][estudiante_j] * preferencia[estudiante_j][estudiante_i];
    }
    return valor;
}

void Backtracking(vector<vector<int>> &preferencia, vector<int>& almacen, int est, int& mejor, vector<int>& asignaciones) {
    int n = preferencia.size();
    int valor;
    if (est == n) {
        valor= CalculaUnion(almacen, preferencia);

        if (valor > mejor){
            mejor = valor;
            asignaciones = almacen;
        }
        return;
    }
    
    for (int estudiante = 0; estudiante < n; estudiante++) {
	if (!esta(almacen, estudiante)) {
	    almacen[est] = estudiante;
	    Backtracking(preferencia, almacen, est + 1, mejor, asignaciones);
	    almacen[est] = -1;
	}
    }
}

