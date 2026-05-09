//Álvaro García Zafra
//c++ -std=c++11 -pthread -o multi_fifo multi-prodcons-fifo.cpp scd.cpp scd.h
#include <iostream>
#include <cassert>
#include <thread>
#include <mutex>
#include <random>
#include "scd.h"

using namespace std ;
using namespace scd ;

//**********************************************************************
// Variables globales

const unsigned 
   num_items = 100 ,   // número de items
	tam_vec   = 6 ,   // tamaño del buffer
	np = 5 ,	//num de hebras productoras
	nc = 4 , //num de hebras consumidoras
	p = num_items/np , //cuantos produce cada productor
	c = num_items/nc ; //cuantos produce cada consumidor
	
unsigned  
	vec[tam_vec],	//vector que almacena los valores producidos
	primera_ocupada = 0,
	primera_libre = 0,
   cont_prod[num_items] = {0}, // contadores de verificación: para cada dato, número de veces que se ha producido.
   cont_cons[num_items] = {0}, // contadores de verificación: para cada dato, número de veces que se ha consumido.
	vec_items_producidos[np] = {0};	//vector que nos indica el numero de items producido por cada hebra

Semaphore libres (tam_vec);
Semaphore ocupadas(0);
Semaphore em_cons (1);		//semaforo exclusion mutua lectura
Semaphore em_prod (1);	//semaforo exclusion mutua escritura
//**********************************************************************
// funciones comunes a las dos soluciones (fifo y lifo)
//----------------------------------------------------------------------

unsigned producir_dato(unsigned nhebra)
{
	assert(nhebra < np);
   this_thread::sleep_for( chrono::milliseconds( aleatorio<20,100>() ));
   const unsigned dato_producido = vec_items_producidos[nhebra] + p*nhebra ;
   cont_prod[dato_producido] ++ ;
   vec_items_producidos[nhebra]++;
   cout << "la hebra " << nhebra << " ha producido el valor " << dato_producido << endl << flush;
   return dato_producido ;
}
//----------------------------------------------------------------------

void consumir_dato( unsigned dato, unsigned nhebra )
{
	assert(nhebra < np);
   assert( dato < num_items );
   cont_cons[dato] ++ ;
   this_thread::sleep_for( chrono::milliseconds( aleatorio<20,100>() ));

   cout << "			la hebra " << nhebra << " ha consumido el valor " << dato << endl << flush;

}


//----------------------------------------------------------------------

void test_contadores()
{
   bool ok = true ;
   cout << "comprobando contadores ...." ;
   for( unsigned i = 0 ; i < num_items ; i++ )
   {  if ( cont_prod[i] != 1 )
      {  cout << "error: valor " << i << " producido " << cont_prod[i] << " veces." << endl ;
         ok = false ;
      }
      if ( cont_cons[i] != 1 )
      {  cout << "error: valor " << i << " consumido " << cont_cons[i] << " veces" << endl ;
         ok = false ;
      }
   }
   if (ok)
      cout << endl << flush << "solución (aparentemente) correcta." << endl << flush ;
}

//----------------------------------------------------------------------

void  funcion_hebra_productora( unsigned nhebra )
{
   for( unsigned i = 0 ; i < p ; i++ )
   {
      int dato = producir_dato(nhebra) ;
      
      sem_wait(libres);
      sem_wait(em_prod);
   	vec[primera_libre] = dato;
   	//cout << "	ha entrado"<<endl;
 
   	primera_libre = (primera_libre + 1) % tam_vec; 
   		
      sem_signal(ocupadas); 
      sem_signal(em_prod);
   }
}

//----------------------------------------------------------------------

void funcion_hebra_consumidora( unsigned nhebra )
{
   for( unsigned i = 0 ; i < c ; i++ )
   {
      int dato ;
      sem_wait(ocupadas);
      sem_wait(em_cons);
//cout << "																	ha entrado la hebra " << nhebra<<endl;
   	dato = vec[primera_ocupada];	
   	primera_ocupada = (primera_ocupada + 1) % tam_vec;
   		
      sem_signal(libres);
      sem_signal(em_cons);
      consumir_dato( dato, nhebra ) ;
    }
}
//----------------------------------------------------------------------

int main()
{
   cout << "-----------------------------------------------------------------" << endl
        << "Problema de los productores-consumidores (solución multi FIFO)." << endl
        << "------------------------------------------------------------------" << endl
        << flush ;

   thread hebras_productoras[np], hebras_consumidoras[nc];
	
	for(int i = 0; i < np; i++)
		hebras_productoras[i] = thread (funcion_hebra_productora, i);
		
	for(int i = 0; i < nc; i++)
		hebras_consumidoras[i] = thread (funcion_hebra_consumidora, i);
		
	for(int i = 0; i < np; i++)
		hebras_productoras[i].join() ;
		
	for(int i = 0; i < nc; i++)
		hebras_consumidoras[i].join() ;

   test_contadores();
}
