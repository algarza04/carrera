//c++ -std=c++11 -pthread -o fumadores_p2 fumadores_p2.cpp scd.cpp scd.h
#include <iostream>
#include <iomanip>
#include <cassert>
#include <thread>
#include <mutex>
#include <random> // dispositivos, generadores y distribuciones aleatorias
#include <chrono> // duraciones (duration), unidades de tiempo
#include "scd.h"

using namespace std ;
using namespace scd ;

// numero de fumadores 

constexpr int num_fumadores = 3,
				  a_dormir = 3;
				  				 
int contador[num_fumadores] = {0,0,0};


mutex
   mtx ;                 // mutex de escritura en pantalla
//-------------------------------------------------------------------------
// Función que simula la acción de producir un ingrediente, como un retardo
// aleatorio de la hebra (devuelve número de ingrediente producido)

int producir_ingrediente()
{
   // calcular milisegundos aleatorios de duración de la acción de fumar)
   chrono::milliseconds duracion_produ( aleatorio<10,100>() );

   // informa de que comienza a producir
   mtx.lock();
   cout << "Estanquero : empieza a producir ingrediente (" << duracion_produ.count() << " milisegundos)" << endl;
   mtx.unlock();
   // espera bloqueada un tiempo igual a ''duracion_produ' milisegundos
   this_thread::sleep_for( duracion_produ );

   const int num_ingrediente = aleatorio<0,num_fumadores-1>() ;

   // informa de que ha terminado de producir
   mtx.lock();
   cout << "Estanquero : termina de producir ingrediente " << endl;
   mtx.unlock();
   
   return num_ingrediente ;
}

//-------------------------------------------------------------------------
// Función que simula la acción de fumar, como un retardo aleatoria de la hebra

void fumar( int num_fumador )
{

   // calcular milisegundos aleatorios de duración de la acción de fumar)
   chrono::milliseconds duracion_fumar( aleatorio<20,200>() );

   // informa de que comienza a fumar
   mtx.lock();
    cout << "Fumador " << num_fumador << "  :"
          << " empieza a fumar (" << duracion_fumar.count() << " milisegundos)" << endl;
   mtx.unlock();
   
   // espera bloqueada un tiempo igual a ''duracion_fumar' milisegundos
   this_thread::sleep_for( duracion_fumar );

   // informa de que ha terminado de fumar
   mtx.lock();
    cout << "Fumador " << num_fumador << "  : termina de fumar, comienza espera de ingrediente." << endl;
   mtx.unlock();
}

//----------------------------------------------------------------------
// clase para monitor
class Estanco : public HoareMonitor
{
	private:
	int ingre_mostrador;	//variable que nos dice si ya se ha puesto algún ingrediente
	CondVar
		ingr_disp[num_fumadores],
		most_vacio,
		esta_durmiendo[num_fumadores];
	public:
	Estanco();
	void obtenerIngrediente( int ingre );
	void ponerIngrediente( int ingre );
	void esperarRecogidaIngrediente();
	void dormir(int ingre);
};

//----------------------------------------------------------
	
Estanco::Estanco(){
	ingre_mostrador = -1;
	most_vacio = newCondVar();
	for(int i = 0; i < num_fumadores; i++)
		ingr_disp[i] = newCondVar();
	for(int i = 0; i < num_fumadores; i++)
		esta_durmiendo[i] = newCondVar();
}

void Estanco::obtenerIngrediente( int ingre ){
	if ( ingre_mostrador != ingre )
		ingr_disp[ingre].wait();
		
	ingre_mostrador = -1;
	
	cout << "Fumador " << ingre << " retira su ingrediente del mostrador" <<endl;
	most_vacio.signal();
}

void Estanco::ponerIngrediente( int ingre ){
	if ( ingre_mostrador != -1 )
		most_vacio.wait();
		
	ingre_mostrador = ingre;
	if (contador[ingre] == 3){
		cout << "El estanquero despierta al fumador " << ingre << endl;
		esta_durmiendo[ingre].signal();
	}
	cout << "Estanquero pone ingrediente " << ingre << " en el mostrador" << endl;
	ingr_disp[ingre].signal();
}

void Estanco::esperarRecogidaIngrediente(){
	if ( ingre_mostrador != -1 )
		most_vacio.wait();
}

void Estanco::dormir(int ingre) {
	if (contador[ingre] == a_dormir){
		cout << "El fumador " << ingre << " se va a dormir" << endl;
		esta_durmiendo[ingre].wait();
		contador[ingre] = 0;
	}
}

void funcion_hebra_estanquero( MRef<Estanco> monitor ){
	while ( true ){
		int ingre = producir_ingrediente();
		monitor->ponerIngrediente( ingre );
		monitor->esperarRecogidaIngrediente();
	}
}

void funcion_hebra_fumador( int num_fum, MRef<Estanco> monitor){
	while ( true ){
		monitor->obtenerIngrediente( num_fum );
		contador[num_fum]++;
		monitor->dormir(num_fum);
		fumar( num_fum );
	}
}
int main()
{
	// crear monitor  ('monitor' es una referencia al mismo, de tipo MRef<...>)
   MRef<Estanco> monitor = Create<Estanco>() ;
   
   thread hebras_fumadores[num_fumadores], hebra_estanquero(funcion_hebra_estanquero, monitor);
   
   for (int i = 0; i < num_fumadores; i++)
   	hebras_fumadores[i] = thread(funcion_hebra_fumador, i, monitor);
   	
   hebra_estanquero.join();
   
   for (int i = 0; i < num_fumadores; i++)
   	hebras_fumadores[i].join();
   
}
