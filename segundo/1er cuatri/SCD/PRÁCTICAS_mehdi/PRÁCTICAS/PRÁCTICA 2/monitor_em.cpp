#include <iostream>
#include <cassert>
#include <thread>
#include <mutex>
#include <random>
#include "scd.h"

using namespace std ;
using namespace scd ;

const int num_incrementos = 10000 ;

// *****************************************************************************
// clase contador, sin exclusión mutua

class MContador1
{
   private:
   int cont ;

   public:
   MContador1( int valor_ini ) ;
   void incrementa();
   int leer_valor();
} ;
// -----------------------------------------------------------------------------

MContador1::MContador1( int valor_ini )
{
   cont = valor_ini ;
}
// -----------------------------------------------------------------------------

void MContador1::incrementa()
{
   cont ++ ;
}
// -----------------------------------------------------------------------------

int MContador1::leer_valor()
{
   return cont ;
}

// *****************************************************************************
// clase contador, con exclusión mutua mediante herencia de 'HoareMonitor'

class MContador2 : public HoareMonitor
{
   private:
   int cont ;

   public:
   MContador2( int valor_ini ) ;
   void incrementa();
   int leer_valor();
} ;

// -----------------------------------------------------------------------------

MContador2::MContador2( int valor_ini )
{
   cont = valor_ini ;
}
// -----------------------------------------------------------------------------

void MContador2::incrementa()
{
   cont ++ ;  
}
// -----------------------------------------------------------------------------

int MContador2::leer_valor()
{
   return cont ;
}

// *****************************************************************************

void funcion_hebra_M1( MContador1 & monitor )
{
   for( int i = 0 ; i < num_incrementos ; i++ )
      monitor.incrementa();
}
// -----------------------------------------------------------------------------

void test_1()
{
   MContador1 monitor(0) ;

   thread hebra1( funcion_hebra_M1, ref(monitor) ),
          hebra2( funcion_hebra_M1, ref(monitor) );

   hebra1.join();
   hebra2.join();

   cout  << "Monitor contador (sin exclusión mutua):" << endl
         << endl
         << "  valor esperado == " << 2*num_incrementos << endl
         << "  valor obtenido == " << monitor.leer_valor() << endl
         << endl;
}
// *****************************************************************************

void funcion_hebra_M2( MRef<MContador2>  monitor )
{
   for( int i = 0 ; i < num_incrementos ; i++ )
      monitor->incrementa();
}
// -----------------------------------------------------------------------------

void test_2()
{
   MRef<MContador2> monitor = Create<MContador2>(0) ;

   thread hebra1( funcion_hebra_M2, monitor ),
          hebra2( funcion_hebra_M2, monitor );

   hebra1.join();
   hebra2.join();

   cout  << "Monitor contador (EM usando clase derivada de HoareMonitor):" << endl
         << endl
         << "  valor esperado == " << 2*num_incrementos << endl
         << "  valor obtenido == " << monitor->leer_valor() << endl
         << endl ;
}
// *****************************************************************************

int main()
{
   test_1();
   test_2();
}
