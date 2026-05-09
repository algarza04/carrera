#include <iostream>
#include <vector>
#include <climits> // para usar INT_MAX
using namespace std;

// Estructura para almacenar tanto el costo acumulado como la dirección previa
struct Cell {
    int cost;
    int prevCol;
};

// Función para encontrar el camino más corto
void findShortestPath(const vector<vector<int>>& mountain, vector<vector<Cell>>& cost) {
    int rows = mountain.size();
    int cols = mountain[0].size();

    // Inicializar la base de la montaña con los valores de la primera fila
    for (int j = 0; j < cols; ++j) {
        cost[0][j] = {mountain[0][j], -1};
    }

    // Rellenar la matriz de costos acumulados y almacenar la dirección previa
    for (int i = 1; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            int minCost = cost[i-1][j].cost;
            int prevCol = j;

            if (j > 0 && cost[i-1][j-1].cost < minCost) {
                minCost = cost[i-1][j-1].cost;
                prevCol = j - 1;
            }
            if (j < cols - 1 && cost[i-1][j+1].cost < minCost) {
                minCost = cost[i-1][j+1].cost;
                prevCol = j + 1;
            }

            cost[i][j] = {mountain[i][j] + minCost, prevCol};
        }
    }
}

// Función para recuperar el camino más corto
vector<int> retrieveShortestPath(const vector<vector<Cell>>& cost) {
    int rows = cost.size();
    int cols = cost[0].size();

    // Encontrar la columna con el menor costo en la última fila
    int minDifficulty = INT_MAX;
    int minIndex = -1;
    for (int j = 0; j < cols; ++j) {
        if (cost[rows-1][j].cost < minDifficulty) {
            minDifficulty = cost[rows-1][j].cost;
            minIndex = j;
        }
    }

    // Recuperar el camino de la cumbre a la base
    vector<int> path(rows);
    int col = minIndex;
    for (int i = rows - 1; i >= 0; --i) {
        path[i] = col;
        col = cost[i][col].prevCol;
    }

    return path;
}

void printMatrix(const vector<vector<int>> &mountain) {
    for (const auto &row : mountain) {
        for (int cell : row) {
            cout << cell << "\t";
        }
        cout << endl;
    }
}

void printPath(const vector<vector<int>> &mountain, const vector<int> &path) {
    int rows = mountain.size();
    int cols = mountain[0].size();

    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            if (j == path[i]) {
                cout << mountain[i][j] << "\t";
            } else {
                cout << "-\t";
            }
        }
        cout << endl;
    }
}

int main() {
    vector<vector<int>> mountain = {
        {2, 8, 9, 5, 8},
        {4, 4, 6, 2, 3},
        {5, 7, 5, 6, 1},
        {3, 2, 5, 4, 8}
    };

    cout << "Mountain Matrix:" << endl;
    printMatrix(mountain);
    cout << endl;

    int rows = mountain.size();
    int cols = mountain[0].size();

    // Inicializar la matriz de costos con valores iniciales grandes
    vector<vector<Cell>> cost(rows, vector<Cell>(cols, {INT_MAX, -1}));

    // Encontrar el camino más corto
    findShortestPath(mountain, cost);

    // Recuperar el camino más corto
    vector<int> path = retrieveShortestPath(cost);

    // Imprimir el camino más corto
    cout << "Shortest Path:" << endl;
    printPath(mountain, path);

    return 0;
}

