#include<iostream>
#include<queue>
using namespace std;

#define N 6

void printSolution(int sol[N][N]) {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++)
            cout << sol[i][j] << " ";
        cout << endl;
    }
}

bool isSafe(int Lab[N][N], int x, int y, bool visitado[N][N]) {
    return (x >= 0 && x < N && y >= 0 && y < N && Lab[x][y] == 1 && !visitado[x][y]);
}

bool ResolverLab(int Lab[N][N]) {
    int sol[N][N] = {0};
    bool visitado[N][N] = {false};

    int movX[] = {1, 0, -1, 0};
    int movY[] = {0, 1, 0, -1};

    visitado[0][0] = true;

    queue<pair<int, int> > posiciones;
    posiciones.push({0, 0});

    while (!posiciones.empty()) {
        pair<int, int> current = posiciones.front();
        posiciones.pop();

        int x = current.first;
        int y = current.second;

        for (int i = 0; i < 4; i++) {
            int newX = x + movX[i];
            int newY = y + movY[i];

            if (isSafe(Lab, newX, newY, visitado)) {
                visitado[newX][newY] = true;
                sol[newX][newY] = sol[x][y] + 1;
                posiciones.push({newX, newY});
            }
        }
    }

    if (!visitado[N - 1][N - 1]) {
        cout << "No hay solución\n";
        return false;
    }

    printSolution(sol);
    cout << "Longitud mínima del camino: " << sol[N - 1][N - 1] << endl;
    return true;
}

int main() {
    int Lab[N][N] = {{1, 1, 0, 1, 1, 1},
                      {0, 1, 0, 1, 0, 1},
                      {1, 1, 1, 1, 0, 1},
                      {1, 0, 0, 0, 0, 1},
                      {1, 0, 0, 0, 0, 1},
					  {1, 1, 1, 1, 1, 1}};
    ResolverLab(Lab);
    return 0;
}

