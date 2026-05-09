#include<iostream>
using namespace std;

#define N 5

bool RecorreLab(int Lab[N][N], int x, int y, int sol[N][N]);

void printSolution(int sol[N][N]) {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++)
            cout << sol[i][j] << " ";
        cout << endl;
    }
}

bool isSafe(int Lab[N][N], int x, int y) {
    if(x >= 0 && x < N && y >= 0 && y < N && Lab[x][y] == 1)
        return true;
    return false;
}

bool ResolverLab(int Lab[N][N]) {
    //Se crea el laberinto vacio
    int sol[N][N];
    for(int i = 0; i < N; i++)
        for(int j = 0; j < N; j++)
            sol[i][j] = 0;


    if(!RecorreLab(Lab, 0, 0, sol)) {
        cout << "No hay solucion\n";
        return false;
    }
    printSolution(sol);
    return true;
}

bool RecorreLab(int Lab[N][N], int x, int y, int sol[N][N]) {
    if(x == N-1 && y == N-1 && Lab[x][y] == 1) {
        sol[x][y] = 1;
        return true;
    }
    if(isSafe(Lab, x, y) ) {
        sol[x][y] = 1;
        //se compara con 0 para comprobar que no se haya pasado por ahí
        if (x+1 < N && sol[x+1][y] == 0 && RecorreLab(Lab, x+1, y, sol) )
            return true;
        if (y+1 < N && sol[x][y+1] == 0 && RecorreLab(Lab, x, y+1, sol) )
            return true;
        if (x-1 >= 0 && sol[x-1][y] == 0 && RecorreLab(Lab, x-1, y, sol) )
            return true;
        if (y-1 >= 0 && sol[x][y-1] == 0 && RecorreLab(Lab, x, y-1, sol) )
            return true;
        sol[x][y] = 0;
    }   
    return false;
}


int main() {
    int Lab[N][N] = {{1, 1, 1, 0, 1},
                      {0, 0, 1, 1, 0},
                      {1, 1, 1, 1, 1},
                      {1, 0, 0, 0, 0},
                      {1, 1, 1, 1, 1}};
    ResolverLab(Lab);
    return 0;
}