#include <iostream>
#include <vector>
#include <limits>
#include <time.h>
#include <string>
using namespace std;

const int PESOS = 10;

struct Nodo{
    int id;                     //Identificador de cada nodo
    int dist;                   //coste del nodo al Sink
    vector<int> adyacentes;     //nodos adyacentes (con los que puede unirse)
    vector<int> costeUnion;     //costes con sus uniones
};

struct solucion{
    vector<int> camino;         //todos los nodos por los que tiene que pasar
};

int MenorCoste(vector<Nodo> c){
	if (c.empty())
        return -1;

	int menorCoste = c[0].dist;
	int nodoMenorCoste = c[0].id;
	
	for (int i = 1; i < c.size(); i++){
		if (c[i].dist < menorCoste){
			menorCoste = c[i].dist;
			nodoMenorCoste = c[i].id;
		}
	} 
	
	return nodoMenorCoste;
}

bool Encontrar(vector<Nodo> nodos, int id){
	for (int i = 0; i < nodos.size(); i++){
		if (nodos[i].id == id)
			return true;
	}
	
	return false;
}

void Greedy(vector<Nodo>& grafo, int sink, vector<solucion>& sol) {
    if (grafo.empty()) {
        return;
    }

    int nodos_seleccionados = 1;
    int idpadre = sink;

    vector<Nodo> seleccionados;
    seleccionados.push_back(grafo[sink]);

    while (nodos_seleccionados < grafo.size()) {
        int costemenor = 1000;
        vector<Nodo> candidatos;

        for (int i = 0; i < seleccionados.size(); i++) {
            for (int j = 0; j < seleccionados[i].adyacentes.size(); j++) {
                if (!Encontrar(seleccionados, seleccionados[i].adyacentes[j])) {
                    int costesSinkPadre = seleccionados[i].dist;
                    Nodo n = grafo[seleccionados[i].adyacentes[j]];
                    n.dist += (costesSinkPadre + seleccionados[i].costeUnion[j]);

                    if (n.dist < costemenor) {
                        idpadre = seleccionados[i].id;
                        costemenor = n.dist;
                    }

                    candidatos.push_back(n);
                }
            }
        }

        int seleccion = MenorCoste(candidatos);

        nodos_seleccionados++;
        grafo[candidatos[seleccion].id].dist = candidatos[seleccion].dist;

        seleccionados.push_back(grafo[candidatos[seleccion].id]);

        sol[candidatos[seleccion].id] = sol[idpadre];

        (sol[candidatos[seleccion].id]).camino.push_back(candidatos[seleccion].id);
    }
}

int main(){
    int n_nodos = 5;

    vector<solucion> salida;

    srand(time(NULL)); 
 
    int num = 0;

    int matriz[n_nodos][n_nodos] = {0};
 
    for(int i = 0; i < n_nodos; i++){ 
        for(int j = i; j < n_nodos; j++){ 
            num = rand()%(PESOS);

            if(i==j){
                matriz[i][j] = 0; 
            }
            else{ 
                matriz[i][j] = num; 
                matriz[j][i] = num; 
            }  
        } 
    } 

    for(int i = 0; i < n_nodos; i++){ 
        
        for(int j = 0; j < n_nodos; j++){ 
            cout << matriz[i][j] << " "; 
        } 
        
        cout << endl; 
    }

    vector<Nodo> red;

    for(int i = 0; i < n_nodos; i++){
        Nodo n;

        n.id = i;
        n.dist = 0;

        for(int j = 0; j < n_nodos; j++){

            if(matriz[i][j] != 0){
                n.adyacentes.push_back(j);
                n.costeUnion.push_back(matriz[i][j]);
            }
        }

        red.push_back(n);
    }


    for(int i = 0; i < n_nodos; i++){
        cout << "Nodo sensor " << red[i].id << " :[";

        for(int j = 0; j < red[i].adyacentes.size(); j++){
            cout << "(" << ((red.at(i)).adyacentes).at(j) << "," << ((red.at(i)).costeUnion).at(j) << "),";
        }

        cout << "]" << endl;
    }

    int servidor = rand()%(n_nodos);

    for(int i = 0; i < n_nodos; i++){
        solucion resultado;

        vector<int> camino;

        camino.push_back(i);

        resultado.camino = camino;

        salida.push_back(resultado);
    }

    Greedy(red, servidor, salida);

    cout << endl;
    cout << "MOSTRANDO RESULTADOS:" << endl;

    for(int i = 0; i < n_nodos; i++){
        cout << "Nodo sensor " << i << ", recorre: [";

        for(int j = salida.at(i).camino.size() - 1; j >= 0; j--){
            cout << (salida.at(i)).camino.at(j) << " ";
        }

        cout << "]" << endl;
    }

    cout << endl;
}
