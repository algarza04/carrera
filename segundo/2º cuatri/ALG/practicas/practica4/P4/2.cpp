#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int nivel_conveniencia_total(const vector<int>& asignacion, const vector<vector<int>>& conveniencia) {
    int total = 0;
    int n = asignacion.size();
    for (int i = 0; i < n; ++i) {
        total += conveniencia[asignacion[i]][asignacion[(i + 1) % n]]; // Suma la conveniencia con el invitado de la izquierda
        total += conveniencia[asignacion[i]][asignacion[(i - 1 + n) % n]]; // Suma la conveniencia con el invitado de la derecha
    }
    return total;
}

void asignar_invitados(int n, const vector<vector<int>>& conveniencia, vector<int>& asignacion_actual, vector<int>& mejor_asignacion, int& mejor_conveniencia) {
    if (asignacion_actual.size() == n) {
        int nivel_actual = nivel_conveniencia_total(asignacion_actual, conveniencia);
        if (nivel_actual > mejor_conveniencia) {
            mejor_asignacion = asignacion_actual;
            mejor_conveniencia = nivel_actual;
        }
    } else {
        for (int i = 0; i < n; ++i) {
            if (find(asignacion_actual.begin(), asignacion_actual.end(), i) == asignacion_actual.end()) {
                asignacion_actual.push_back(i);
                asignar_invitados(n, conveniencia, asignacion_actual, mejor_asignacion, mejor_conveniencia);
                asignacion_actual.pop_back();
            }
        }
    }
}

int main() {
    int n = 4; // Número de invitados
    vector<vector<int>> conveniencia = {
        {0, 5, 80, 30},  // Nivel de conveniencia del invitado 0 con los demás
        {5, 0, 40, 10},  // Nivel de conveniencia del invitado 1 con los demás
        {80, 40, 0, 60},  // Nivel de conveniencia del invitado 2 con los demás
        {30, 10, 60, 0}   // Nivel de conveniencia del invitado 3 con los demás
    };

    vector<int> mejor_asignacion;
    int mejor_conveniencia = 0;

    vector<int> asignacion_actual;
    asignar_invitados(n, conveniencia, asignacion_actual, mejor_asignacion, mejor_conveniencia);

    cout << "Mejor asignación de invitados: ";
    for (int i = 0; i < n; ++i) {
        cout << mejor_asignacion[i] << " ";
    }
    cout << endl;

    cout << "Nivel de conveniencia total: " << mejor_conveniencia << endl;

    return 0;
}
