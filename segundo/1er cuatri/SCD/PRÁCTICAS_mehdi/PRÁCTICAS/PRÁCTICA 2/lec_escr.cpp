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
    num_lectores = 5,
    num_escritores = 2,         
    min_ms    = 5,     // tiempo minimo de espera en sleep_for
    max_ms    = 20 ;   // tiempo máximo de espera en sleep_for

mutex
    mtx ;                 // mutex de escritura en pantalla

class Lec_Esc : public HoareMonitor
{
 private:
    bool escrib;
    int n_lec; 

 CondVar                    // colas condicion:
    lectura,
    escritura;

 public: 
    Lec_Esc() ; 
    void ini_lectura();
    void ini_escritura();
    void fin_lectura();
    void fin_escritura();
} ;
// -----------------------------------------------------------------------------

Lec_Esc::Lec_Esc(  )
{
    escrib = false;
    n_lec = 0;
    lectura = newCondVar();
    escritura = newCondVar();
}

void Lec_Esc::ini_lectura()
{
    if (escrib)
        lectura.wait();
    
    n_lec++;
    lectura.signal();
}

void Lec_Esc::fin_lectura()
{
    n_lec--;
    
    if (n_lec == 0)
        escritura.signal();
}

void Lec_Esc::ini_escritura()
{
    if (n_lec > 0 || escrib)
        escritura.wait();
    
    escrib = true;
}

void Lec_Esc::fin_escritura()
{
    escrib = false;

    if (!lectura.empty())
        lectura.signal();
    
    else 
        escritura.signal();
}

void Lector( MRef<Lec_Esc> Lec_Esc , int lector)
{
    while (true)
    {
        Lec_Esc->ini_lectura();
        mtx.lock();
        cout << "El lector " << lector << " está leyendo. \n";
        mtx.unlock();
        this_thread::sleep_for( chrono::milliseconds( aleatorio<min_ms,max_ms>() ));
        cout << "El lector " << lector << " ha finalizado la lectura. \n";
        Lec_Esc->fin_lectura();
        this_thread::sleep_for( chrono::milliseconds( aleatorio<min_ms,max_ms>() ));
    }
}
void Escritor( MRef<Lec_Esc> Lec_Esc , int escritor)
{
    while (true)
    {
        Lec_Esc->ini_escritura();
        mtx.lock();
        cout << "El escritor " << escritor << " está escribiendo. \n"; 
        mtx.unlock();
        this_thread::sleep_for( chrono::milliseconds( aleatorio<min_ms,max_ms>() ));
        cout << "El escritor " << escritor << " ha finalizado la escritura. \n";
        Lec_Esc->fin_escritura();
        this_thread::sleep_for( chrono::milliseconds( aleatorio<min_ms,max_ms>() ));
    }
}
// -----------------------------------------------------------------------------

int main()
{
   cout << "--------------------------------------------------------------------" << endl
        << "Problema de lectores_escritores (Monitor SU). " << endl
        << "--------------------------------------------------------------------" << endl
        << flush ;

   // crear monitor  ('monitor' es una referencia al mismo, de tipo MRef<...>)
    MRef<Lec_Esc> monitor = Create<Lec_Esc>() ;

    thread lectores[num_lectores],
        escritores[num_escritores];

    for ( int e = 0 ; e < num_escritores ; e++)
        escritores[e] = thread (Escritor, monitor, e);

    for ( int l = 0 ; l < num_lectores ; l++)
        lectores[l] = thread (Lector, monitor, l);
    

    for ( int e = 0 ; e < num_escritores ; e++)
        escritores[e].join();

    for ( int l = 0 ; l < num_lectores ; l++)
        lectores[l].join();
    
    

    
    
    
}