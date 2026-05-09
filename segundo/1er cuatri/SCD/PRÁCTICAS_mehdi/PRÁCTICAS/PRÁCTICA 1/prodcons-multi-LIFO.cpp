/* MEHDI IABOUTEN --> K568645 */

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
   num_items = 40 ,   // número de items
	tam_vec   = 10 ,   // tamaño del buffer
	np = 4,
	nc = 2,
	p = num_items/np,
	c = num_items/nc;
unsigned  
   cont_prod[num_items] = {0}, // contadores de verificación: para cada dato, número de veces que se ha producido.
   cont_cons[num_items] = {0}, // contadores de verificación: para cada dato, número de veces que se ha consumido.
   siguiente_dato       = 0 ,  // siguiente dato a producir en 'producir_dato' (solo se usa ahí)
   compartido[np] = {0};

//**********************************************************************
// funciones comunes a las dos soluciones (fifo y lifo)
//----------------------------------------------------------------------
Semaphore libres(tam_vec);
Semaphore ocupadas(0);
Semaphore ex_mutua(1);

int vec [tam_vec] = {0};
int primera_libre = 0;


unsigned producir_dato( unsigned nhebra )
{
   this_thread::sleep_for( chrono::milliseconds( aleatorio<20,100>() ));
   const unsigned dato_producido = siguiente_dato ;
   siguiente_dato++ ;
   cont_prod[dato_producido] ++ ;
   cout << "producido: " << dato_producido << " por la hebra " << nhebra << endl << flush ;
	compartido[nhebra]++;
   return dato_producido ;
}
//----------------------------------------------------------------------

void consumir_dato( unsigned dato, unsigned nhebra )
{
   assert( dato < num_items );
   cont_cons[dato] ++ ;
   this_thread::sleep_for( chrono::milliseconds( aleatorio<20,100>() ));
	
   cout << "                  consumido: " << dato << " por la  hebra " << nhebra << endl ;
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

	for ( unsigned j = 0 ; j < np ; j++)
	{	cout << "Hebra " << j << " producido " << compartido[j] << "\n"; 
	}

}

//----------------------------------------------------------------------

void  funcion_hebra_productora( unsigned i )
{
	for( long j = p*i ; j < p*i+(p); j++ )
   {
      int dato = producir_dato( i ) ;
      sem_wait(libres); 
      sem_wait(ex_mutua);
      vec[primera_libre] = dato;
      primera_libre++;
      sem_signal(ocupadas);
      sem_signal(ex_mutua);
   }
}

//----------------------------------------------------------------------

void funcion_hebra_consumidora( unsigned i )
{
   for( long j = c*i ; j < c*i+(c); j++ )
   {
      sem_wait(ocupadas);
      sem_wait(ex_mutua);
      primera_libre--;
      int dato = vec[primera_libre]; 
      vec[primera_libre] = 0; 
      sem_signal(libres);
      sem_signal(ex_mutua);
      consumir_dato( dato, i );
    }
}
//----------------------------------------------------------------------

int main()
{
   cout << "-----------------------------------------------------------------" << endl
        << "Problema de los productores-consumidores LIFO." << endl
        << "------------------------------------------------------------------" << endl
        << flush ;

	thread prod[np],
			 cons[nc];

	for ( int p = 0 ; p < np ; p++)
		prod[p] = thread (funcion_hebra_productora, p);

	for ( int c = 0 ; c < nc ; c++)
		cons[c] = thread (funcion_hebra_consumidora, c);

   for ( int p = 0 ; p < np ; p++)
		prod[p].join() ;

	for ( int c = 0 ; c < nc ; c++)
		cons[c].join() ;

   test_contadores();
}

