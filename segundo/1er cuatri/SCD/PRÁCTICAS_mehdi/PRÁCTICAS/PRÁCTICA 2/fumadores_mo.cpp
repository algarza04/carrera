/* MEHDI IABOUTEN --> K568645 */

#include <iostream>
#include <iomanip>
#include <cassert>
#include <random>
#include <thread>
#include <chrono>
#include "scd.h"

using namespace std ;
using namespace scd ;

constexpr int
    num_fumadores = 3  , // número de fumadores
    tabaco = 0  ,
    papel = 1  ,
    cerrillas = 2  ;

constexpr int               
    min_ms    = 5,     // tiempo minimo de espera en sleep_for
    max_ms    = 20 ;   // tiempo máximo de espera en sleep_for

mutex
    mtx ;                 // mutex de escritura en pantalla

class Estanco : public HoareMonitor
{
 private:
    int mostrador ; 

 CondVar                    // colas condicion:
    mostrador_vacio ,
    ingr_disponible[num_fumadores] ; 

 public: 
    Estanco() ; 
    
    int obtener_ingrediente( int ingrediente ) ;    
    void poner_ingrediente( int ingrediente ) ; 
    void esperarRecogidaIngrediente();            
    
    // void Fumador( MRef<Estanco>  monitor, int fumador ) ;
    // void Estanquero( MRef<Estanco> monitor ) ; 
} ;
// -----------------------------------------------------------------------------

Estanco::Estanco(  )
{
    mostrador = -1 ; 
    mostrador_vacio = newCondVar()  ;
    for (int i = 0 ; i < num_fumadores ; i++)
        ingr_disponible[i] = newCondVar();
}

int producir_ingrediente()
{
   // calcular milisegundos aleatorios de duración de la acción de fumar)
   chrono::milliseconds duracion_produ( aleatorio<10,100>() );

   // informa de que comienza a producir
   cout << "\nEstanquero : empieza a producir ingrediente (" << duracion_produ.count() << " milisegundos)" << endl;

   // espera bloqueada un tiempo igual a ''duracion_produ' milisegundos
   this_thread::sleep_for( duracion_produ );

   const int num_ingrediente = aleatorio<0,num_fumadores-1>() ;

   // informa de que ha terminado de producir
   cout << "Estanquero : termina de producir ingrediente " << num_ingrediente << endl;

   return num_ingrediente ;
}

int Estanco::obtener_ingrediente( int ingrediente ){
    if ( mostrador != ingrediente )
        ingr_disponible[ingrediente].wait();

    mostrador = -1; 
    mostrador_vacio.signal();

    return ingrediente;
}

void Estanco::poner_ingrediente( int ingrediente ){
    mostrador = ingrediente; 
    ingr_disponible[ingrediente].signal();
}

void Estanco::esperarRecogidaIngrediente(){
    if (mostrador != -1)
        mostrador_vacio.wait();
}

void fumar( int fumador )
{
    // calcular milisegundos aleatorios de duración de la acción de fumar)
   chrono::milliseconds duracion_fumar( aleatorio<20,200>() );

   // informa de que comienza a fumar

    cout << "Fumador " << fumador << "  :"
          << " empieza a fumar (" << duracion_fumar.count() << " milisegundos)" << endl;

   // espera bloqueada un tiempo igual a ''duracion_fumar' milisegundos
   this_thread::sleep_for( duracion_fumar );

   // informa de que ha terminado de fumar

    cout << "Fumador " << fumador << "  : termina de fumar, comienza espera de ingrediente." << endl;
}
// -----------------------------------------------------------------------------
// *****************************************************************************
// funciones de hebras

void Estanquero( MRef<Estanco> monitor )
{
   int ingrediente; 
   while (true)
   {
    ingrediente = producir_ingrediente();
    monitor->poner_ingrediente( ingrediente );
    monitor->esperarRecogidaIngrediente();
   }
}
// -----------------------------------------------------------------------------

void Fumador( MRef<Estanco>  monitor, int fumador )
{
   while ( true )
   {
    monitor->obtener_ingrediente( fumador );
    fumar( fumador );
   }
}

// -----------------------------------------------------------------------------

int main()
{
   cout << "--------------------------------------------------------------------" << endl
        << "Problema del productor-consumidor únicos (Monitor SU). " << endl
        << "--------------------------------------------------------------------" << endl
        << flush ;

   // crear monitor  ('monitor' es una referencia al mismo, de tipo MRef<...>)
   MRef<Estanco> monitor = Create<Estanco>() ;

   thread estanquero ( Estanquero, monitor ),
          fumadores[num_fumadores];

   for ( int f = 0 ; f < num_fumadores ; f++)
      fumadores[f] = thread (Fumador, monitor, f);
      
   estanquero.join();

   for ( int f = 0 ; f < num_fumadores ; f++)
      fumadores[f].join();
}