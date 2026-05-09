//c++ -std=c++11 -pthread -o fumadores3 fumadores3.cpp scd.cpp scd.h
#include <iostream>
#include <cassert>
#include <thread>
#include <mutex>
#include <random> // dispositivos, generadores y distribuciones aleatorias
#include <chrono> // duraciones (duration), unidades de tiempo
#include "scd.h"

using namespace std ;
using namespace scd ;

// numero de fumadores 

const int num_fumadores = 3 ,
			 max_vec = 3, 
			 num_suministradoras = 2;

int vec[max_vec],
	 prim_vacia = 0,
	 prim_ocupada = 0,
	 pos = max_vec;

Semaphore mostr_vacio(1),
			 ingr_disp[num_fumadores] = {0, 0, 0},
			 vector_con_espacios(max_vec);


//-------------------------------------------------------------------------
// Función que simula la acción de producir un ingrediente, como un retardo
// aleatorio de la hebra (devuelve número de ingrediente producido)

int producir_ingrediente(int nhebra)
{
   // calcular milisegundos aleatorios de duración de la acción de fumar)
   chrono::milliseconds duracion_produ( aleatorio<10,100>() );

   // informa de que comienza a producir
   cout << "La hebra " << nhebra << " empieza a producir ingrediente (" << duracion_produ.count() << " milisegundos)" << endl;

   // espera bloqueada un tiempo igual a ''duracion_produ' milisegundos
   this_thread::sleep_for( duracion_produ );

   const int num_ingrediente = aleatorio<0,num_fumadores-1>() ;

   // informa de que ha terminado de producir
   cout << "La hebra " << nhebra << " termina de producir ingrediente " << num_ingrediente << endl;

   return num_ingrediente ;
}

//----------------------------------------------------------------------
// función que ejecuta la hebra de las suministradoras

void funcion_hebras_suministradoras( int nhebra )
{
	while( true ) {
		int i = producir_ingrediente(nhebra);
		sem_wait( vector_con_espacios );
		vec[prim_vacia] = i;
		
		if (prim_ocupada == max_vec)
			prim_ocupada = 0;
		else
			prim_ocupada++;
	}
}

//----------------------------------------------------------------------
// función que ejecuta la hebra del estanquero

void funcion_hebra_estanquero(  )
{
	while( true ) {
		sem_wait( mostr_vacio );
		cout << "Puesto ingr.: " << vec[prim_ocupada] << endl;
		int i = vec[prim_ocupada];
		
		if (prim_vacia == max_vec)
			prim_vacia = 0;
		else
			prim_vacia++;
			
		sem_signal( ingr_disp[i] );
		sem_signal( vector_con_espacios );
		
	}
}

//-------------------------------------------------------------------------
// Función que simula la acción de fumar, como un retardo aleatoria de la hebra

void fumar( int num_fumador )
{

   // calcular milisegundos aleatorios de duración de la acción de fumar)
   chrono::milliseconds duracion_fumar( aleatorio<20,200>() );

   // informa de que comienza a fumar

    cout << "Fumador " << num_fumador << "  :"
          << " empieza a fumar (" << duracion_fumar.count() << " milisegundos)" << endl;

   // espera bloqueada un tiempo igual a ''duracion_fumar' milisegundos
   this_thread::sleep_for( duracion_fumar );

   // informa de que ha terminado de fumar

    cout << "Fumador " << num_fumador << "  : termina de fumar, comienza espera de ingrediente." << endl;

}

//----------------------------------------------------------------------
// función que ejecuta la hebra del fumador
void  funcion_hebra_fumador( int num_fumador )
{
   while( true )
   {
   	sem_wait( ingr_disp[num_fumador] );
   	cout << "Retirado ing.: " << num_fumador << endl;
   	fumar(num_fumador);
   	sem_signal( mostr_vacio );
   }
}

//----------------------------------------------------------------------

int main()
{
   thread hebras_fumadores[num_fumadores], hebra_estanquero(funcion_hebra_estanquero);
   thread hebras_suministradoras[num_suministradoras];
   
   for (int i = 0; i < num_suministradoras; i++)
   	hebras_suministradoras[i] = thread(funcion_hebras_suministradoras, i);
   	
   
   for (int i = 0; i < num_fumadores; i++)
   	hebras_fumadores[i] = thread(funcion_hebra_fumador, i);
   	
   hebra_estanquero.join();
   
   for (int i = 0; i < num_fumadores; i++)
   	hebras_fumadores[i].join();
   	
   for (int i = 0; i < num_suministradoras; i++)
   	hebras_suministradoras[i].join();
   
}
